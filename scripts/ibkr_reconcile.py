"""IBKR 只读对账 (read-only reconcile) —— 阶段1:不下单,只对比。

读 IBKR paper 实际持仓 vs 引擎目标配置(data/allocation.json + 各腿持仓),
按 NOTIONAL 名义本金($2000,模拟真实规模,不用paper的百万)算目标股数,
打印"该买/该卖什么"。**绝不下单**。

目标构成:
  指数 index_pct × NOTIONAL → SPY
  主动 final_allocation[leg] × NOTIONAL → 该腿 open_positions 等权
用法: python3 scripts/ibkr_reconcile.py   (Gateway 需登录+API开,端口4002)
"""
import json, os
from ib_insync import IB, Stock

NOTIONAL = 2000.0          # 名义本金(模拟真实$2000规模),非paper百万
LEG_PORT = {"momma": "data/portfolio_momma.json", "bq": "data/portfolio_bq.json"}


def load(p, d=None):
    try: return json.load(open(p))
    except Exception: return d


def build_targets():
    """返回 {symbol: target_usd}。"""
    a = load("data/allocation.json")
    if not a:
        print("无 allocation.json"); return {}
    targets = {}
    # 指数
    idx_usd = a["index_pct"] * NOTIONAL
    if idx_usd > 0:
        targets["SPY"] = targets.get("SPY", 0) + idx_usd
    # 主动各腿 → 该腿持仓等权
    for leg, w in a.get("final_allocation", {}).items():
        amt = w * NOTIONAL
        if amt <= 0: continue
        port = load(LEG_PORT.get(leg, ""), {})
        tks = [p["ticker"] for p in (port.get("open_positions") or []) if p.get("ticker")]
        if not tks:
            print(f"  [warn] {leg} 无持仓,${amt:.0f} 暂挂现金"); continue
        per = amt / len(tks)
        for tk in tks:
            targets[tk] = targets.get(tk, 0) + per
    return targets, a


def main():
    res = build_targets()
    if not res: return
    targets, a = res

    ib = IB()
    for port in (4002, 7497, 4001, 7496):
        try: ib.connect("127.0.0.1", port, clientId=11, timeout=8); break
        except Exception: continue
    if not ib.isConnected():
        print("❌ 没连上网关(检查 Gateway 登录+API)"); return
    acct = ib.managedAccounts()[0]
    print(f"✅ 连上 paper 账户 {acct}\n")

    # 实际持仓(股数)
    actual = {}
    for pos in ib.positions(acct):
        actual[pos.contract.symbol] = pos.position

    # 取价(用 yfinance,paper无实时行情;此处只为换算股数,延迟价够用)
    import yfinance as yf
    syms = sorted(set(list(targets) + list(actual)))
    px = {}
    try:
        data = yf.download(syms, period="2d", progress=False)["Close"]
        for s in syms:
            try: px[s] = float(data[s].dropna().iloc[-1]) if len(syms) > 1 else float(data.dropna().iloc[-1])
            except Exception: px[s] = None
    except Exception as e:
        print(f"[warn] 取价失败: {e}")

    print(f"{'='*70}")
    print(f"  对账 (名义本金 ${NOTIONAL:.0f}) — 配置: 指数{a['index_pct']*100:.0f}% / 主动{a['active_pct']*100:.0f}%")
    print(f"{'='*70}")
    print(f"  {'代码':<8}{'目标$':>9}{'目标股':>9}{'实际股':>9}{'差额股':>9}  动作")
    allsym = sorted(set(list(targets) + list(actual)))
    orders = []
    for s in allsym:
        tgt_usd = targets.get(s, 0)
        p = px.get(s)
        tgt_sh = round(tgt_usd / p, 4) if (p and p == p) else 0
        act_sh = actual.get(s, 0)
        diff = round(tgt_sh - act_sh, 4)
        if abs(diff) < 0.01:
            act = "—持平"
        elif tgt_sh == 0:
            act = f"清仓 卖{abs(diff)}"
        elif diff > 0:
            act = f"买 {diff}"
        else:
            act = f"卖 {abs(diff)}"
        if abs(diff) >= 0.01 and tgt_sh > 0 or (tgt_sh == 0 and act_sh != 0):
            orders.append((s, diff))
        pxs = f"${p:.0f}" if (p and p == p) else "?"
        print(f"  {s:<8}{tgt_usd:>8.0f}{tgt_sh:>9}{act_sh:>9}{diff:>+9}  {act} @{pxs}")

    print(f"\n  📋 需执行 {len(orders)} 笔(阶段1仅打印,未下单):")
    for s, d in orders:
        print(f"     {'买' if d>0 else '卖'} {abs(d)} 股 {s}")
    print(f"\n  ⚠️ 这是只读对账,没有下任何单。确认逻辑对了,再进阶段2(单笔测试单)。")
    ib.disconnect()


if __name__ == "__main__":
    main()
