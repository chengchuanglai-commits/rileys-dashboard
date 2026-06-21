import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from scripts.ibkr.risk import drawdown, breaker_action

def test_drawdown_calc():
    assert abs(drawdown(nav=1800, peak=2000) - 0.10) < 1e-9
    assert drawdown(nav=2100, peak=2000) == 0.0   # 新高,无回撤

def test_breaker_normal():
    assert breaker_action(0.05) == "normal"        # <20%
def test_breaker_warn():
    assert breaker_action(0.21) == "warn"          # 20-25%:预警,新仓减半
def test_breaker_reduce_only():
    assert breaker_action(0.26) == "reduce_only"   # 25-28%:停开新仓
def test_breaker_defensive():
    assert breaker_action(0.29) == "defensive"     # >28%:全线出场

if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f(); print(f"  ok {n}")
    print("ALL PASS")
