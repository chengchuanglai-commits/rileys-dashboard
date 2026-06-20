# scripts/compute-allocation.py
"""信念分配引擎:每腿 conviction(sample×alpha×robustness) → 主动30-70%滑动 → 各腿按信念权重。"""
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
