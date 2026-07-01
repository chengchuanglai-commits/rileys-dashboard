"""开盘batch:自检过→对账→下单→挂止损→落exec-log。LIVE=False只算不下。"""
import os, json, time
from scripts.ibkr.client import connect, health, cancel_all
from scripts.ibkr.targets import build_targets, build_master_targets
from scripts.ibkr.sizing import target_shares
from scripts.ibkr.reconcile import diff_orders
from scripts.ibkr.risk import drawdown, breaker_action
from scripts.ibkr.orders import check_gates, place_limit, place_stop
from scripts.ibkr.config import (LIVE, FRACTIONAL, NOTIONAL, MAX_ORDER_USD,
                                 MAX_TOTAL_USD, INIT_STOP_PCT)
from scripts.ibkr.notify import send

def _prices(syms):
    """yfinance 兜底取价。优先当日1分钟盘中价(真盘中价),失败退2日日线收盘。"""
    import yfinance as yf
    px = {}
    for period, interval in (("1d", "1m"), ("2d", "1d")):   # 先盘中分钟,再日线
        miss = [s for s in syms if not px.get(s)]
        if not miss: break
        try:
            d = yf.download(miss, period=period, interval=interval, progress=False)["Close"]
            for s in miss:
                try: px[s] = float(d[s].dropna().iloc[-1]) if len(miss) > 1 else float(d.dropna().iloc[-1])
                except Exception: pass
        except Exception: pass
    return px

def _ib_prices(ib, syms):
    """从 IBKR(我们正在交易的券商)取盘中价——根治"yfinance日线旧价→开盘后买单limit挂太低买不进"。
    用延迟数据类型(3),paper无实时订阅也能取;marketPrice→last→close 逐级兜底。返回 {sym: price or None}。"""
    from ib_insync import Stock
    out = {}
    try: ib.reqMarketDataType(3)   # 3=延迟数据(免实时订阅);取不到再说
    except Exception: pass
    cs = []
    for s in syms:
        try:
            c = Stock(s, "SMART", "USD"); ib.qualifyContracts(c); cs.append(c)
        except Exception: out[s] = None
    if cs:
        try:
            for t in ib.reqTickers(*cs):
                p = None
                for cand in (t.marketPrice(), t.last, t.close):
                    if cand and cand == cand and cand > 0: p = float(cand); break
                out[t.contract.symbol] = p
        except Exception: pass
    return out

def run():
    ib, port = connect(client_id=21)
    if not ib:
        send("⚠️ 开盘batch:网关连不上,中止\n（交易信号系统）"); return
    h = health(ib)
    if not h["is_paper"] and not LIVE:
        send(f"⚠️ 开盘batch:账户{h['account']}非paper且LIVE=False,中止\n（交易信号系统）")
        ib.disconnect(); return
    # 开盘前全局撤单(仅LIVE):reqGlobalCancel跨session可靠,根治跨日/跨session遗留单+止损重复堆叠
    #(cancelOrder只能撤本session会报10147→旧止损撤不掉再重挂=越堆越多)。batch末尾按当前多头重挂唯一止损。
    if LIVE:
        left = cancel_all(ib)
        print(f"全局撤单后剩余挂单 {left}")
    # 三线统一目标(指数+长线+波动);master不存在则退回旧的双线目标
    targets_usd = build_master_targets(notional=NOTIONAL) or build_targets(notional=NOTIONAL)
    actual = {p.contract.symbol: p.position for p in ib.positions(h["account"])}
    syms = sorted(set(list(targets_usd) + list(actual)))
    # 取价:先用IBKR盘中价(准),缺的再用yfinance兜底(根治旧价导致买单挂太低买不进)
    px = _ib_prices(ib, syms)
    miss = [s for s in syms if not px.get(s)]
    if miss:
        for s, p in _prices(miss).items(): px[s] = p

    # 断路器
    dd = drawdown(h["nav"], max(h["nav"], NOTIONAL))
    act = breaker_action(dd)

    # 目标股数
    tgt_sh = {}
    for s, usd in targets_usd.items():
        p = px.get(s)
        if not (p and p == p): continue
        tgt_sh[s] = target_shares(usd, p, fractional=FRACTIONAL)
    orders = diff_orders(tgt_sh, actual, tol=(0.01 if FRACTIONAL else 1))
    # 断路器 reduce_only/defensive:过滤掉买单
    if act in ("reduce_only", "defensive"):
        orders = [o for o in orders if o["qty"] < 0]
    plan = []
    for o in orders:
        p = px.get(o["sym"])
        if not p: continue
        plan.append({"sym": o["sym"], "qty": o["qty"], "px": p, "usd": abs(o["qty"]) * p})

    ok, reason = check_gates(plan, MAX_ORDER_USD, MAX_TOTAL_USD)
    log = {"date": time.strftime("%Y-%m-%d"), "live": LIVE, "drawdown": round(dd, 4),
           "breaker": act, "plan": plan, "gate_ok": ok, "gate_reason": reason, "placed": []}
    if not ok:
        send(f"🛑 开盘batch安全闸拦截: {reason}\n（交易信号系统）")
    elif not LIVE:
        log["note"] = "DRY-RUN(LIVE=False),未下单"
    else:
        for o in plan:
            try:
                tr = place_limit(ib, o["sym"], o["qty"], o["px"])
                log["placed"].append({"sym": o["sym"], "qty": o["qty"], "status": tr.orderStatus.status})
            except Exception as e:
                log["placed"].append({"sym": o["sym"], "error": str(e)[:80]})
        ib.sleep(8)
    # 重挂止损:LIVE下总是执行(开盘已全局撤掉旧止损,这里按当前多头补回唯一止损;
    # 即使gate拦截/无单也要补,否则全局撤后裸奔)。每仓正好1个,跨session不会再重复。
    if LIVE:
        for p in ib.positions(h["account"]):
            if p.position > 0:
                try: place_stop(ib, p.contract.symbol, p.position, p.avgCost * (1 - INIT_STOP_PCT))
                except Exception: pass
    os.makedirs("data/exec-log", exist_ok=True)
    json.dump(log, open(f"data/exec-log/{log['date']}.json", "w"), ensure_ascii=False, indent=2)
    ib.disconnect()
    print(json.dumps(log, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    run()
