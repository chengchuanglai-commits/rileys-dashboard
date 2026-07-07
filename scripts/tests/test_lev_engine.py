import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import pandas as pd, numpy as np
from lev_engine import simulate_leverage

def _series(vals, start="2020-01-01"):
    idx = pd.bdate_range(start=start, periods=len(vals))
    return pd.Series(vals, index=idx)

def test_flat_prices_stay_1x_flat():
    # 平价:price==MA(不>MA)→目标1x→无融资→权益不动
    s = _series([100.0]*260)
    r = simulate_leverage(s, start=2000.0)
    assert abs(r["final"] - 2000.0) < 1.0 and r["ruined"] is False

def test_uptrend_applies_leverage():
    # 稳升趋势(>MA)→1.5x→权益增速快于标的本身
    s = _series([100.0*(1.001**i) for i in range(300)])
    r = simulate_leverage(s, start=2000.0)
    underlying = s.iloc[-1]/s.iloc[210]-1
    assert r["final"] > 2000.0*(1+underlying)
    assert any(l > 1.4 for _, _, l in r["curve"])

def test_vol_spike_deleverages():
    calm = [100.0*(1.001**i) for i in range(250)]
    wild = [calm[-1]*(1.15 if i%2 else 0.87)**1 for i in range(30)]
    r = simulate_leverage(_series(calm+wild), start=2000.0)
    tail_lev = [l for _, _, l in r["curve"][-15:]]
    assert min(tail_lev) <= 1.05

def test_deep_crash_at_leverage_ruins():
    up = [100.0*(1.002**i) for i in range(230)]
    crash = [up[-1]*0.25]
    r = simulate_leverage(_series(up+crash), start=2000.0)
    assert r["ruined"] is True and r["final"] == 0.0

def test_below_ma_no_leverage():
    s = _series([100.0*(0.999**i) for i in range(300)])
    r = simulate_leverage(s, start=2000.0)
    assert all(l <= 1.05 for _, _, l in r["curve"][210:])

if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"): fn(); print(f"  ok {name}")
    print("ALL PASS")
