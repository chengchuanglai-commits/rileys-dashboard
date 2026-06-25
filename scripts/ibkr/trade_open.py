"""开盘batch:自检过→对账→下单→挂止损→落exec-log。LIVE=False只算不下。"""
import os, json, time
from scripts.ibkr.client import connect, health, cancel_orphan_limits
from scripts.ibkr.targets import build_targets, build_master_targets
from scripts.ibkr.sizing import target_shares
from scripts.ibkr.reconcile import diff_orders
from scripts.ibkr.risk import drawdown, breaker_action
from scripts.ibkr.orders import check_gates, place_limit, place_stop
from scripts.ibkr.config import (LIVE, FRACTIONAL, NOTIONAL, MAX_ORDER_USD,
                                 MAX_TOTAL_USD, INIT_STOP_PCT)
from scripts.ibkr.notify import send

def _prices(syms):
    import yfinance as yf
    px = {}
    try:
        d = yf.download(syms, period="2d", progress=False)["Close"]
        for s in syms:
            try: px[s] = float(d[s].dropna().iloc[-1]) if len(syms) > 1 else float(d.dropna().iloc[-1])
            except Exception: px[s] = None
    except Exception: pass
    return px

def run():
    ib, port = connect(client_id=21)
    if not ib:
        send("⚠️ 开盘batch:网关连不上,中止\n（交易信号系统）"); return
    h = health(ib)
    if not h["is_paper"] and not LIVE:
        send(f"⚠️ 开盘batch:账户{h['account']}非paper且LIVE=False,中止\n（交易信号系统）")
        ib.disconnect(); return
    # 开盘前清遗留非止损单(根治跨日遗留限价单→对账从干净状态开始)
    cleared = cancel_orphan_limits(ib)
    if cleared: print(f"清掉 {cleared} 笔遗留非止损单")
    # 三线统一目标(指数+长线+波动);master不存在则退回旧的双线目标
    targets_usd = build_master_targets(notional=NOTIONAL) or build_targets(notional=NOTIONAL)
    actual = {p.contract.symbol: p.position for p in ib.positions(h["account"])}
    syms = sorted(set(list(targets_usd) + list(actual)))
    px = _prices(syms)

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
        # 对新多头持仓挂 -8% stop
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
