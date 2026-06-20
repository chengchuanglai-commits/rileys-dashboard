"""
共享现金约束 (shared cash constraint) —— 修掉模拟盘的隐性杠杆 (implicit leverage)。

问题：各 backfill 每来一个信号就开 $500,从不查现金。$2000 本金却同时持 10-16 仓
      = $5-8k 敞口 = 3-4倍杠杆,净值虚胖。真实账户做不到。

修法：按信号时间顺序 (chronological) 跑一遍现金账本——
   - 起始 cash = INIT($2000)
   - 开仓占用 cost(≈$500),平仓归还 cost + 该仓已实现盈亏
   - 现金 < cost 时,后来的信号**跳过不开** (skipped_no_cash),只保留真能开的
   → 最多同时 INIT/PER_POSITION = 4 个仓,净值反映真实 $2000 账户。

用法:在 backfill 算 stats 前调用,用返回的 filled 列表重算。
"""


def apply_cash_constraint(closed, opens, init=2000, per_position=500):
    """
    closed: 已平仓列表(含 signal_date / close_date / realized_pnl_usd)
    opens : 持仓中列表(含 signal_date,无 close_date=占用现金到底)
    返回: (filled_closed, filled_opens, skipped_no_cash)
    """
    def cost_of(p):
        return float(p.get("actual_position_usd") or per_position)

    # 统一打标:来源 + 排序键
    items = []
    for p in closed:
        items.append({"p": p, "open": False, "sig": p.get("signal_date", ""),
                      "close": p.get("close_date") or "9999-99-99",
                      "cost": cost_of(p), "pnl": float(p.get("realized_pnl_usd") or 0)})
    for p in opens:
        items.append({"p": p, "open": True, "sig": p.get("signal_date", ""),
                      "close": "9999-99-99", "cost": cost_of(p), "pnl": 0.0})

    # 按信号日排队(同日保持原顺序=原打分/优先级);稳定排序
    items.sort(key=lambda x: x["sig"])

    cash = float(init)
    active = []   # (close_date, cost, pnl) 已开、未释放
    filled_closed, filled_opens, skipped = [], [], 0

    for it in items:
        # 释放:close_date <= 本信号日 的仓,归还本金+盈亏
        still = []
        for cl, cost, pnl in active:
            if cl <= it["sig"]:
                cash += cost + pnl
            else:
                still.append((cl, cost, pnl))
        active = still
        # 能否开
        if cash >= it["cost"]:
            cash -= it["cost"]
            active.append((it["close"], it["cost"], it["pnl"]))
            (filled_opens if it["open"] else filled_closed).append(it["p"])
        else:
            skipped += 1

    return filled_closed, filled_opens, skipped
