# scripts/ibkr/tests/test_review.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from scripts.ibkr.review import build_review

def test_anomalies_first():
    exec_log = {"date":"2026-06-22","gate_ok":True,
                "placed":[{"sym":"SPY","status":"Filled"},{"sym":"AAA","error":"rejected"}]}
    actual = {"SPY": 1.6}
    target = {"SPY": 1.6, "AAA": 5}      # AAA 目标5但实际0=对不上
    r = build_review(exec_log, actual, target, nav=2010, peak=2050)
    assert any("AAA" in a for a in r["anomalies"])    # 下单失败/持仓对不上进异常
    assert r["nav"] == 2010

def test_no_anomaly():
    exec_log = {"date":"2026-06-22","gate_ok":True,"placed":[{"sym":"SPY","status":"Filled"}]}
    r = build_review(exec_log, {"SPY":1.6}, {"SPY":1.6}, nav=2000, peak=2000)
    assert r["anomalies"] == []

if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f(); print(f"  ok {n}")
    print("ALL PASS")
