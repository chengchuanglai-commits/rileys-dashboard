import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from scripts.ibkr.reconcile import diff_orders

# diff_orders(target_sh, actual_sh, tol) → [{"sym","qty"}] qty>0买 qty<0卖
def test_empty_buys_all():
    o = diff_orders({"SPY": 1.6, "STM": 10}, {}, tol=0.01)
    d = {x["sym"]: x["qty"] for x in o}
    assert abs(d["SPY"] - 1.6) < 1e-9 and abs(d["STM"] - 10) < 1e-9

def test_held_partial_adjusts():
    # SPY够(持平不出现) STM少(补) AMD多(卖) OLD不该有(清)
    o = diff_orders({"SPY": 1.6, "STM": 10, "AMD": 0.15},
                    {"SPY": 1.6, "STM": 4, "AMD": 0.3, "OLD": 2}, tol=0.01)
    d = {x["sym"]: round(x["qty"], 4) for x in o}
    assert "SPY" not in d                 # 持平,不下单
    assert d["STM"] == 6                   # 补
    assert d["AMD"] == -0.15               # 卖
    assert d["OLD"] == -2                  # 清仓

def test_within_tolerance_no_order():
    o = diff_orders({"SPY": 1.605}, {"SPY": 1.6}, tol=0.01)
    assert o == []                         # 差<tol,不动

if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f(); print(f"  ok {n}")
    print("ALL PASS")
