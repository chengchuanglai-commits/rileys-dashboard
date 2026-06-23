# scripts/ibkr/tests/test_orders_gate.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from scripts.ibkr.orders import check_gates

# check_gates(plan, max_order, max_total) → (ok, reason)。qty>0买/<0卖;总额只算买入。
def test_pass():
    plan = [{"sym":"SPY","usd":1200,"qty":1},{"sym":"AAA","usd":400,"qty":2}]
    ok, r = check_gates(plan, max_order=1500, max_total=2200)
    assert ok and r == ""

def test_single_too_big():
    plan = [{"sym":"SPY","usd":1600,"qty":1}]
    ok, r = check_gates(plan, max_order=1500, max_total=2200)
    assert not ok and "单笔" in r

def test_buy_total_too_big():
    plan = [{"sym":"A","usd":1200,"qty":1},{"sym":"B","usd":1200,"qty":1}]
    ok, r = check_gates(plan, max_order=1500, max_total=2200)
    assert not ok and "总额" in r

def test_swap_not_blocked():
    # 换仓:卖SPY$1200+买QQQ$1000 → 绝对值和$2200会误拦,但买入只$1000应放行
    plan = [{"sym":"SPY","usd":1200,"qty":-2},{"sym":"QQQ","usd":1000,"qty":3}]
    ok, r = check_gates(plan, max_order=1500, max_total=1500)
    assert ok, f"换仓被误拦: {r}"

if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f(); print(f"  ok {n}")
    print("ALL PASS")
