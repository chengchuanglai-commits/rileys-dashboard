"""
c-H 变体 — c 的平行 A/B(只改一个变量:出场参数 Plan C → Plan H)。
c 本尊不动。同信号、同跳空过滤(1.5%),出场换成历史回测排第一的 Plan H:TP15/SL2/2天。
测"更高止盈+更紧止损+更短持仓"的出场是否打赢 c 的 TP8/SL4/5天。
"""
from functools import partial
import plan_variants as pv

sim = partial(pv.simulate_fixed, tp_pct=15, sl_pct=2, max_hold=2, gap_filter=1.5)
print("=" * 55)
print("  💼 c-H 变体(Plan H 出场 TP15/SL2/2天,跳空同 c 1.5%)")
print("=" * 55)
pv.run_variant(
    sim,
    "c-H 变体:Plan H 出场(TP15/SL2/2天)+ 跳空过滤 1.5%(信号同 c)",
    "data/portfolio_ch.json",
    "dashboard/portfolio-ch.js",
    "PORTFOLIO_CH",
)
