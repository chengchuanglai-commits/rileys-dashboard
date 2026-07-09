"""
c-trail 变体 — c 的平行 A/B(只改一个变量:固定止盈 → 移动止损让赢家跑)。
c 本尊不动。同信号、同跳空过滤(1.5%),出场换成移动止损:初始止损 -4%,
价格有利移动时把止损棘轮跟到 peak*(1-4%);无固定止盈,最多持仓 10 天。
测"让利润奔跑"vs c 的固定 TP8 谁更强。
"""
from functools import partial
import plan_variants as pv

sim = partial(pv.simulate_trail, sl_pct=4, trail_pct=4, max_hold=10, gap_filter=1.5)
print("=" * 55)
print("  💼 c-trail 变体(移动止损 -4% 让赢家跑,跳空同 c 1.5%)")
print("=" * 55)
pv.run_variant(
    sim,
    "c-trail 变体:移动止损(初始-4%/棘轮4%/最多10天)+ 跳空过滤 1.5%(信号同 c)",
    "data/portfolio_ctr.json",
    "dashboard/portfolio-ctr.js",
    "PORTFOLIO_CTR",
)
