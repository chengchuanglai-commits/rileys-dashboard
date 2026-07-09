"""
c 腿跳空过滤阈值扫描 — 为 c-nogap 变体定阈值。
用 Plan C 出场(TP8/SL4/5天)在同一批历史信号上跑不同跳空阈值,对比净值/胜率。
gap=1.5 应复现 backfill-portfolio-c.py 的净值($2216.07)= 引擎忠实度验收。
不保存任何文件,纯打印。
"""
from functools import partial
import plan_variants as pv

EXIT = dict(tp_pct=8, sl_pct=4, max_hold=5)
THRESHOLDS = [("1.5%(=c基线,验收)", 1.5), ("3.0%(放宽)", 3.0), ("关闭(全交易)", None)]

print("=" * 64)
print("  c 腿跳空过滤阈值扫描  (Plan C 出场 TP8/SL4/5天, frac10 复利)")
print("=" * 64)
rows = []
for label, gap in THRESHOLDS:
    sim = partial(pv.simulate_fixed, gap_filter=gap, **EXIT)
    st = pv.run_variant(sim, f"gap={label}", None, None, None, verbose=False)
    rows.append((label, st))
    print(f"  跳空阈值 {label:16} → 交易 {st['total_trades']:2}笔 "
          f"胜率 {st['win_rate']:4}% | 跳过 {st['skipped_gap']:2} | "
          f"净值 ${st['portfolio_value']:.2f} (已实现 ${st['total_realized_pnl_usd']:+.2f} 浮盈 ${st['open_unrealized_pnl_usd']:+.2f})")

print("=" * 64)
base = rows[0][1]["portfolio_value"]
print(f"  验收:gap=1.5 净值 ${base}  (c 实际 $2216.07 → {'✅ 复现' if abs(base-2216.07)<3 else '⚠️ 不符,需查'})")
