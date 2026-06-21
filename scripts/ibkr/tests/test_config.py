import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from scripts.ibkr import config as C

def test_defaults_safe():
    assert C.LIVE is False           # 默认 paper,不碰真钱
    assert C.FRACTIONAL is False     # 默认整数股(权限未开)
    assert C.NOTIONAL == 2000.0
    assert C.PORTS[0] == 4002        # Gateway paper 优先

def test_circuit_breaker_tiers_ordered():
    t = C.DRAWDOWN_TIERS
    assert t["warn"] < t["reduce_only"] < t["defensive"]  # 20<25<28
    assert t["warn"] == 0.20 and t["defensive"] == 0.28

def test_safety_caps_positive():
    assert C.MAX_ORDER_USD > 0 and C.MAX_TOTAL_USD >= C.NOTIONAL

if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f(); print(f"  ok {n}")
    print("ALL PASS")
