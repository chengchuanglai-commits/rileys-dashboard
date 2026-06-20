# scripts/compute-allocation.py
"""信念分配引擎:每腿 conviction(sample×alpha×robustness) → 主动30-70%滑动 → 各腿按信念权重。"""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.dirname(os.path.abspath(sys.argv[0])))
from portfolio_compound import compound_frac20

N_FULL = 40
ALPHA_TARGET = 0.10
ACTIVE_FLOOR = 0.30
ACTIVE_CEILING = 0.70
MOMMA_PRIOR = 0.10

def _clip(x, lo, hi):
    return max(lo, min(hi, x))

def conviction_score(n, alpha, robust_ok, n_full=N_FULL, alpha_target=ALPHA_TARGET):
    if not robust_ok or alpha <= 0:
        return 0.0
    sample = min(n / n_full, 1.0)
    edge = _clip(alpha / alpha_target, 0.0, 1.0)
    return round(sample * edge * 1.0, 4)

def active_fraction(max_conviction, floor=ACTIVE_FLOOR, ceiling=ACTIVE_CEILING):
    return round(floor + (ceiling - floor) * _clip(max_conviction, 0.0, 1.0), 4)

def active_weights(convictions, priors):
    raw = {k: convictions.get(k, 0.0) + priors.get(k, 0.0) for k in convictions}
    s = sum(raw.values())
    if s <= 0:
        return {k: 0.0 for k in convictions}
    return {k: round(v / s, 4) for k, v in raw.items()}

INIT = 2000.0

def _closed_trades(port):
    out = []
    for p in port.get("closed_positions", []):
        pct = p.get("final_pnl_pct")
        if pct is None:
            rp, cost = p.get("realized_pnl_usd"), (p.get("actual_position_usd") or p.get("allocated_usd"))
            if rp is not None and cost: pct = rp / cost * 100
        if pct is None or (isinstance(pct, float) and math.isnan(pct)): continue
        out.append((p.get("signal_date", ""), p.get("close_date", p.get("signal_date", "")), float(pct)))
    return out

def leg_metrics(port, spy_ret_pct):
    """返回 (n, alpha, robust_ok, final_eq)。alpha = 该腿frac20复利前向收益% − SPY同期%(小数)。"""
    trades = _closed_trades(port)
    n = len(trades)
    if n == 0:
        return 0, 0.0, False, INIT
    final = compound_frac20(trades, init=INIT)
    ret_pct = (final / INIT - 1) * 100
    alpha = (ret_pct - spy_ret_pct) / 100.0
    # robustness:去掉最赚2笔(按pct),剩余复利仍 > 起始
    rest = sorted(trades, key=lambda t: t[2])[:-2] if n > 2 else []
    robust_ok = compound_frac20(rest, init=INIT) > INIT if rest else False
    return n, alpha, robust_ok, final
