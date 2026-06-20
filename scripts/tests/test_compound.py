# scripts/tests/test_compound.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from portfolio_compound import compound_frac20, compound_frac20_curve

def test_single_winning_trade_compounds():
    # 一笔 +10%：$2000 → 开 20%=$400 → 平仓 $400*1.10=$440 → 终值 $2040
    trades = [("2026-06-01", "2026-06-03", 10.0)]
    assert abs(compound_frac20(trades, init=2000, frac=0.20, max_conc=5) - 2040.0) < 0.01

def test_max_concurrency_skips_excess():
    # 6 笔同一天开、晚平：max_conc=5 → 第6笔被跳过(现金/并发约束)
    trades = [("2026-06-01", "2026-06-30", 5.0)] * 6
    final = compound_frac20(trades, init=2000, frac=0.20, max_conc=5)
    # 5 笔各占 20%*递减净值,均 +5%;第6笔不开 → 终值 < 6 笔全开的情形
    assert final > 2000 and final <= 2000 * (1.05)

def test_curve_returns_dated_points():
    trades = [("2026-06-01", "2026-06-03", 10.0)]
    curve = compound_frac20_curve(trades, init=2000, frac=0.20, max_conc=5)
    assert curve[-1][0] == "2026-06-03" and abs(curve[-1][1] - 2040.0) < 0.01

if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"): fn(); print(f"  ok {name}")
    print("ALL PASS")
