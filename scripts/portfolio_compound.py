# scripts/portfolio_compound.py
"""共享 frac20 复利:把交易流按'每仓20%当前净值、最多MAX_CONC并发、现金约束'复利。"""
import math

def _nan(x):
    return x is None or (isinstance(x, float) and math.isnan(x))

def _run(trades, init, frac, max_conc):
    """返回 (final_equity, curve[(date,equity)])。trades=[(signal_date, close_date, pnl_pct)]。"""
    trades = sorted(trades, key=lambda t: (t[0], t[1]))
    cash = float(init)
    open_caps = []   # (close_date, capital, pnl_pct)
    curve = []
    def equity():
        return cash + sum(c for _, c, _ in open_caps)
    for sd, cd, pct in trades:
        still = []
        for ocd, cap, opct in open_caps:
            if ocd <= sd:
                cash += cap * (1 + opct / 100)
                curve.append((ocd, round(cash + sum(c for _, c, _ in still), 2)))
            else:
                still.append((ocd, cap, opct))
        open_caps = still
        if len(open_caps) >= max_conc:
            continue
        eq = equity()
        size = min(frac * eq, cash)
        if size < 5:
            continue
        cash -= size
        open_caps.append((cd, size, pct))
    for ocd, cap, opct in sorted(open_caps, key=lambda x: x[0]):
        cash += cap * (1 + opct / 100)
        curve.append((ocd, round(cash, 2)))
    return round(cash, 2), curve

def compound_frac20(trades, init=2000, frac=0.20, max_conc=5):
    return _run(trades, init, frac, max_conc)[0]

def compound_frac20_curve(trades, init=2000, frac=0.20, max_conc=5):
    return _run(trades, init, frac, max_conc)[1]


def compound_portfolio(closed, opens, open_pct, init=2000, frac=0.20, max_conc=5):
    """把模拟盘按 frac20 复利重灌(与决策视图排名同口径,取代固定$500+现金约束)。
    closed: 已平仓 dict(含 signal_date/close_date/final_pnl_pct); opens: 持仓中 dict(含 signal_date)。
    open_pct(open_dict)->最新未实现%。就地给每个被填充仓位写 position_usd + realized_pnl_usd/unrealized_pnl_usd。
    返回 (filled_closed, filled_open, portfolio_value, total_realized, total_unreal, skipped)。"""
    items = []
    for p in closed:
        pct = p.get("final_pnl_pct")
        if _nan(pct):                      # 跳过 NaN/缺失(c 盘有 NaN bug)
            continue
        items.append({"sig": p.get("signal_date", ""), "close": p.get("close_date") or p.get("signal_date", ""),
                      "pct": float(pct), "ref": p, "open": False})
    for p in opens:
        op = open_pct(p)
        items.append({"sig": p.get("signal_date", ""), "close": None,
                      "pct": (0.0 if _nan(op) else float(op)), "ref": p, "open": True})
    items.sort(key=lambda x: (x["sig"], x["close"] or "9999"))
    cash = float(init); held = []
    fc, fo = [], []; realized = 0.0; skipped = 0
    def equity():
        return cash + sum(h[1] for h in held)
    for it in items:
        still = []
        for cd, cap, pct, ref, isop in held:
            if cd is not None and cd <= it["sig"]:
                pnl = cap * pct / 100; cash += cap + pnl; realized += pnl
                ref["position_usd"] = round(cap, 2); ref["realized_pnl_usd"] = round(pnl, 2)
            else:
                still.append((cd, cap, pct, ref, isop))
        held = still
        if len(held) >= max_conc:
            skipped += 1; continue
        size = min(frac * equity(), cash)
        if size < 5:
            skipped += 1; continue
        cash -= size
        held.append((it["close"], size, it["pct"], it["ref"], it["open"]))
        (fo if it["open"] else fc).append(it["ref"])
    unreal = 0.0
    for cd, cap, pct, ref, isop in sorted(held, key=lambda x: (x[0] or "9999")):
        pnl = cap * pct / 100; ref["position_usd"] = round(cap, 2)
        if isop:
            ref["unrealized_pnl_usd"] = round(pnl, 2); unreal += pnl
        else:
            cash += cap + pnl; ref["realized_pnl_usd"] = round(pnl, 2); realized += pnl
    return fc, fo, round(init + realized + unreal, 2), round(realized, 2), round(unreal, 2), skipped
