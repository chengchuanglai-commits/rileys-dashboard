# scripts/ibkr/tests/test_orders_gate.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from scripts.ibkr.orders import check_gates

# check_gates(plan, max_order, max_total) → (ok, reason)
def test_pass():
    plan = [{"sym":"SPY","usd":1200},{"sym":"AAA","usd":400}]
    ok, r = check_gates(plan, max_order=1500, max_total=2200)
    assert ok and r == ""

def test_single_too_big():
    plan = [{"sym":"SPY","usd":1600}]
    ok, r = check_gates(plan, max_order=1500, max_total=2200)
    assert not ok and "单笔" in r

def test_total_too_big():
    plan = [{"sym":"A","usd":1200},{"sym":"B","usd":1200}]
    ok, r = check_gates(plan, max_order=1500, max_total=2200)
    assert not ok and "总额" in r

if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f(); print(f"  ok {n}")
    print("ALL PASS")
