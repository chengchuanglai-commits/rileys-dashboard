"""
方法 A —— 出场规则配对回放(用 c 的真实信号,现在就能算)。

把同一批真实信号的价格路径,分别跑 Plan C / Plan H / 移动止损 三种出场,做**配对差异检验**:
每笔 diff = 某规则收益 − Plan C 收益。信号选股的共同噪音在配对里两两相消,只剩出场差异。
故所需样本远少于"绝对打赢 SPY"的 80 笔门槛。

只取三规则都已平仓的信号(干净配对),跳空过滤统一 1.5%(=三者同入场集,完美配对)。
自助法(bootstrap)出配对均值 95% CI:CI 不含 0 → 该规则相对 C 有显著差异。
纯打印,按需运行。
"""
import random
from statistics import mean, pstdev
import plan_variants as pv

GAP = 1.5
RULES = {
    "Plan C (基线 TP8/SL4/5d)": lambda tk, ac, ep, sd: pv.simulate_fixed(tk, ac, ep, sd, 8, 4, 5, GAP),
    "Plan H (TP15/SL2/2d)":     lambda tk, ac, ep, sd: pv.simulate_fixed(tk, ac, ep, sd, 15, 2, 2, GAP),
    "移动止损 (init-4%/trail4%/10d)": lambda tk, ac, ep, sd: pv.simulate_trail(tk, ac, ep, sd, 4, 4, 10, GAP),
}
BASE = "Plan C (基线 TP8/SL4/5d)"


def rule_return(res):
    """从 simulate 六元组取本笔收益%。返回 (pct, state)。"""
    _cd, _cp, reason, final_pct, daily, _d1 = res
    if reason == "gap_filtered":
        return None, "gap"
    if reason == "open" or final_pct is None:
        return None, "open"  # 只取全平仓做干净配对
    return final_pct, "closed"


def boot_ci(diffs, iters=5000):
    n = len(diffs)
    ms = sorted(mean(random.choices(diffs, k=n)) for _ in range(iters))
    return ms[int(iters * .025)], ms[int(iters * .975)]


# ── 逐信号跑三规则 ──
rows = {name: {} for name in RULES}   # name -> {(tk,sd): pct}
for sd, s in pv._read_signals():
    tk, ac, ep = s.get("ticker"), s.get("action"), s.get("current_price")
    if ac not in ("BUY", "SELL") or not ep or int(pv.PER_POSITION_USD / ep) == 0:
        continue
    key = (tk, sd, ac)
    for name, fn in RULES.items():
        pct, st = rule_return(fn(tk, ac, ep, sd))
        if st == "closed":
            rows[name][key] = pct

# 只保留三规则都平仓的信号(完美配对集)
common = set.intersection(*(set(rows[n].keys()) for n in RULES))
common = sorted(common, key=lambda k: (k[1], k[0]))
n = len(common)

print("=" * 68)
print(f"  方法A · 出场规则配对回放  (真实信号, 三规则均已平仓的 {n} 笔)")
print("=" * 68)
if n < 5:
    print(f"  配对样本仅 {n} 笔,太少,等前向再攒。"); raise SystemExit(0)

base_rets = [rows[BASE][k] for k in common]
print(f"  基线 {BASE}: 均收益 {mean(base_rets):+.2f}%/笔")
print("-" * 68)
for name in RULES:
    if name == BASE:
        continue
    rets = [rows[name][k] for k in common]
    diffs = [rows[name][k] - rows[BASE][k] for k in common]
    md = mean(diffs)
    lo, hi = boot_ci(diffs)
    wins = sum(1 for d in diffs if d > 1e-9); losses = sum(1 for d in diffs if d < -1e-9)
    sig = "🟢 显著优于C" if lo > 0 else ("🔴 显著劣于C" if hi < 0 else "⚪ 与C无显著差异")
    print(f"  {name}")
    print(f"    均收益 {mean(rets):+.2f}%/笔 | 配对差 {md:+.2f}%pt  95%CI[{lo:+.2f},{hi:+.2f}]")
    print(f"    赢C {wins} / 平 {n-wins-losses} / 输C {losses} 笔   → {sig}")
    print("-" * 68)
print("  注:样本内、真信号但样本少;差异大能抓、细微差异抓不到(需配合方法B与前向)。")
