# scripts/portfolio_compound.py
"""共享 frac20 复利:把交易流按'每仓20%当前净值、最多MAX_CONC并发、现金约束'复利。"""

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
