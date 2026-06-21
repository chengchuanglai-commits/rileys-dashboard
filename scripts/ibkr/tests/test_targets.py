import sys, os, json, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from scripts.ibkr.targets import build_targets

def test_build_from_alloc(tmp=tempfile.mkdtemp()):
    alloc = {"index_pct": 0.6, "active_pct": 0.4,
             "final_allocation": {"momma": 0.4, "bq": 0.0}}
    momma = {"open_positions": [{"ticker": "AAA"}, {"ticker": "BBB"}]}
    ap = os.path.join(tmp, "alloc.json"); json.dump(alloc, open(ap, "w"))
    mp = os.path.join(tmp, "momma.json"); json.dump(momma, open(mp, "w"))
    t = build_targets(alloc_path=ap, leg_paths={"momma": mp, "bq": mp},
                      notional=2000)
    assert t["SPY"] == 1200.0           # 指数60%
    assert abs(t["AAA"] - 400.0) < 1e-9  # 主动40%=$800/2票=$400
    assert abs(t["BBB"] - 400.0) < 1e-9
    assert "bq" not in t                  # 权重0不出现

if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f(); print(f"  ok {n}")
    print("ALL PASS")
