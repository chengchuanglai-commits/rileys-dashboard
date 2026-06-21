import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from scripts.ibkr.sizing import target_shares

def test_integer_floor():
    # 整数股:$800/$78 = 10.25 → 10
    assert target_shares(800, 78.0, fractional=False) == 10

def test_integer_too_expensive_returns_zero():
    # $80 买 $862 的票 → 0 股(买不起)
    assert target_shares(80, 862.0, fractional=False) == 0

def test_fractional_keeps_decimals():
    # 小数股:$80/$537 = 0.1489
    assert abs(target_shares(80, 537.0, fractional=True) - 0.1489) < 0.0001

def test_zero_price_safe():
    assert target_shares(80, 0, fractional=True) == 0

if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f(); print(f"  ok {n}")
    print("ALL PASS")
