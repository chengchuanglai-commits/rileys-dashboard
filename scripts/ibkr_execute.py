"""IBKR 执行层 (阶段2) —— 按引擎目标配置下单(限价单+安全闸+回读对账)。

复用 ibkr_reconcile 的目标构建,对差额下**限价单**(yfinance价×缓冲),带多重安全闸:
  ① 只在 paper(DU/DUQ 开头)下单,误连实盘直接拒绝
  ② 单笔金额 > MAX_ORDER_USD 拒绝;总下单额 > MAX_TOTAL_USD 拒绝
  ③ 默认 DRY_RUN(只打印),--live 才真下
  ④ 下完等成交,回读实际持仓做事后对账
用法:
  python3 scripts/ibkr_execute.py          # 干跑(只打印计划)
  python3 scripts/ibkr_execute.py --live    # 真下单(paper)
"""
import sys, json
from ib_insync import IB, Stock, LimitOrder

NOTIONAL = 20000.0         # paper 名义本金放大10倍:高价票也能凑出整数股(API不支持小数股)
INTEGER_SHARES = True      # API 只能下整数股 → 股数向下取整
MAX_ORDER_USD = 14000.0    # 单笔上限(SPY 60%≈$12000 在内)
MAX_TOTAL_USD = 22000.0    # 总下单额上限(略高于名义本金)
LIMIT_BUFFER = 0.01        # 限价缓冲:买价×1.01,卖价×0.99(吃得到又不失控)
LEG_PORT = {"momma": "data/portfolio_momma.json", "bq": "data/portfolio_bq.json"}


def load(p, d=None):
    try: return json.load(open(p))
    except Exception: return d


def build_targets():
    a = load("data/allocation.json")
    if not a: return None, None
    targets = {}
    if a["index_pct"] * NOTIONAL > 0:
        targets["SPY"] = a["index_pct"] * NOTIONAL
    for leg, w in a.get("final_allocation", {}).items():
        amt = w * NOTIONAL
        if amt <= 0: continue
        port = load(LEG_PORT.get(leg, ""), {})
        tks = [p["ticker"] for p in (port.get("open_positions") or []) if p.get("ticker")]
        if not tks: continue
        for tk in tks:
            targets[tk] = targets.get(tk, 0) + amt / len(tks)
    return targets, a


def get_prices(syms):
    import yfinance as yf
    px = {}
    try:
        data = yf.download(syms, period="2d", progress=False)["Close"]
        for s in syms:
            try: px[s] = float(data[s].dropna().iloc[-1]) if len(syms) > 1 else float(data.dropna().iloc[-1])
            except Exception: px[s] = None
    except Exception as e:
        print(f"[warn] 取价失败: {e}")
    return px


def main():
    live = "--live" in sys.argv
    targets, a = build_targets()
    if not targets:
        print("无目标配置"); return

    ib = IB()
    for port in (4002, 7497, 4001, 7496):
        try: ib.connect("127.0.0.1", port, clientId=12, timeout=8); break
        except Exception: continue
    if not ib.isConnected():
        print("❌ 没连上网关"); return
    acct = ib.managedAccounts()[0]

    # 安全闸①:必须 paper
    if not (acct.startswith("DU")):
        print(f"🛑 账户 {acct} 不是 paper(DU开头),拒绝下单!"); ib.disconnect(); return
    print(f"✅ paper 账户 {acct} · 模式: {'🔴 LIVE下单' if live else '🟡 DRY-RUN(干跑)'}\n")

    actual = {p.contract.symbol: p.position for p in ib.positions(acct)}
    syms = sorted(set(list(targets) + list(actual)))
    px = get_prices(syms)

    # 算差额订单
    plan = []
    for s in syms:
        p = px.get(s)
        if not (p and p == p):
            print(f"  [skip] {s} 无价,跳过"); continue
        tgt_sh = targets.get(s, 0) / p
        if INTEGER_SHARES:
            import math
            tgt_sh = math.floor(tgt_sh)          # API只能整数股,向下取整
        diff = round(tgt_sh - actual.get(s, 0), 4)
        if INTEGER_SHARES: diff = int(diff)
        if abs(diff) < (1 if INTEGER_SHARES else 0.01):
            if targets.get(s, 0) > 0 and tgt_sh == 0:
                print(f"  [skip] {s} @${p:.0f} 目标${targets.get(s,0):.0f}<1股,买不起,跳过")
            continue
        usd = abs(diff) * p
        plan.append({"sym": s, "qty": diff, "px": p, "usd": usd})

    # 安全闸②:逐笔 + 总额
    total = sum(o["usd"] for o in plan)
    print(f"  计划 {len(plan)} 笔,合计 ${total:.0f}")
    for o in plan:
        if o["usd"] > MAX_ORDER_USD:
            print(f"🛑 {o['sym']} 单笔 ${o['usd']:.0f} > 上限 ${MAX_ORDER_USD},中止!"); ib.disconnect(); return
    if total > MAX_TOTAL_USD:
        print(f"🛑 总额 ${total:.0f} > 上限 ${MAX_TOTAL_USD},中止!"); ib.disconnect(); return

    # 下单
    trades = []
    for o in plan:
        s, qty, p = o["sym"], o["qty"], o["px"]
        side = "BUY" if qty > 0 else "SELL"
        lmt = round(p * (1 + LIMIT_BUFFER) if qty > 0 else p * (1 - LIMIT_BUFFER), 2)
        line = f"  {side} {abs(qty)} {s} @限价${lmt} (≈${o['usd']:.0f})"
        if not live:
            print(line + "  [干跑]"); continue
        ct = Stock(s, "SMART", "USD")
        ib.qualifyContracts(ct)
        order = LimitOrder(side, abs(qty), lmt)
        tr = ib.placeOrder(ct, order)
        trades.append(tr)
        print(line + "  ✅已提交")

    if not live:
        print("\n  🟡 干跑结束,未下单。加 --live 真下(paper)。"); ib.disconnect(); return

    # 等成交 + 回读对账
    print("\n  ⏳ 等成交(最多30秒)…")
    ib.sleep(5)
    for _ in range(5):
        if all(t.isDone() for t in trades): break
        ib.sleep(5)
    print("\n  📊 成交回读:")
    for t in trades:
        st = t.orderStatus
        print(f"     {t.contract.symbol}: {st.status} 成交{st.filled}/{abs(t.order.totalQuantity)} 均价${st.avgFillPrice or '?'}")
    print("\n  实际持仓:")
    for p in ib.positions(acct):
        print(f"     {p.contract.symbol}: {p.position} @均价${round(p.avgCost,2)}")
    ib.disconnect()
    print("\n  ✅ 执行完成。下一步:每日自动对账+止损+断路器。")


if __name__ == "__main__":
    main()
