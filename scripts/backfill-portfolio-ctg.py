"""
c-tight 变体 — c 的平行 A/B(只改一个变量:跳空过滤 1.5% → 1.0% 更紧)。
c 本尊(backfill-portfolio-c.py)不动。回测显示跳空过滤越紧胜率越高,本变体前向验证"再紧一点是否更好"。
出场同 c:TP8/SL4/5天。
"""
from functools import partial
import plan_variants as pv

sim = partial(pv.simulate_fixed, tp_pct=8, sl_pct=4, max_hold=5, gap_filter=1.0)
print("=" * 55)
print("  💼 c-tight 变体(跳空过滤 1.0% 更紧,出场同 Plan C)")
print("=" * 55)
pv.run_variant(
    sim,
    "c-tight 变体:Plan C 出场(TP8/SL4/5天)+ 跳空过滤 >1.0% 跳过(比 c 更紧)",
    "data/portfolio_ctg.json",
    "dashboard/portfolio-ctg.js",
    "PORTFOLIO_CTG",
)
