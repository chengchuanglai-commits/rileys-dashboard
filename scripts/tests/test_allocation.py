# scripts/tests/test_allocation.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from importlib import import_module
ca = import_module("compute-allocation".replace("-", "_")) if False else None
# 文件名带连字符,用 runpy 不便;改为同名下划线导入失败 → 直接 exec
import types
mod = types.ModuleType("alloc")
exec(open(os.path.join(os.path.dirname(__file__), "..", "compute-allocation.py")).read(), mod.__dict__)

def test_conviction_zero_when_no_alpha():
    assert mod.conviction_score(n=40, alpha=-0.05, robust_ok=True) == 0.0

def test_conviction_zero_when_not_robust():
    assert mod.conviction_score(n=40, alpha=0.10, robust_ok=False) == 0.0

def test_conviction_full_when_all_strong():
    # n=40→sample1, alpha=0.10→edge1, robust→1 ⇒ 1.0
    assert abs(mod.conviction_score(n=40, alpha=0.10, robust_ok=True) - 1.0) < 1e-9

def test_conviction_scales_with_sample():
    # n=20→sample0.5, alpha=0.10→edge1 ⇒ 0.5
    assert abs(mod.conviction_score(n=20, alpha=0.10, robust_ok=True) - 0.5) < 1e-9

def test_active_fraction_floor_and_ceiling():
    assert abs(mod.active_fraction(0.0) - 0.30) < 1e-9      # 零信念=地板
    assert abs(mod.active_fraction(1.0) - 0.70) < 1e-9      # 满信念=天花板

def test_active_weights_prior_carries_floor():
    # 全零信念:只有 MOM-MA 有先验0.1 → 拿满主动
    w = mod.active_weights({"momma": 0.0, "bq": 0.0}, {"momma": 0.10, "bq": 0.0})
    assert abs(w["momma"] - 1.0) < 1e-9 and abs(w["bq"] - 0.0) < 1e-9

if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"): fn(); print(f"  ok {name}")
    print("ALL PASS")
