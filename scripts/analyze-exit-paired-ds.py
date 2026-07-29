"""方法B配对回放 · DeepSeek信号版 —— c系退役时留下的作业(2026-07-17 Riley要求立跑)。

问题:hds 现用 Plan H 出场(TP15/SL2/2日),但 c系方法B证明"移动止损>固定TP"——该结论在
DeepSeek 信号上成立吗?

做法:对 DeepSeek 归档信号(dashboard/trading-signals-history/deepseek/)的同一批信号,
分别回放 Plan H / 移动止损 / Plan C 三种出场,配对差异 diff = 规则 − Plan H(hds现行=基线)。
信号噪音配对相消,bootstrap 出 95% CI:CI 不含 0 → 相对现行规则有显著差异。
跳空过滤统一 1.0%(=hds 现行 gap,三规则同入场集,完美配对)。零 API 成本,纯价格回放。
用法: python3 scripts/analyze-exit-paired-ds.py   (纯打印,按需跑;gate裁决时复跑一次)
"""
import os, sys, json, random
from statistics import mean

sys.path.insert(0, os.path.dirname(__file__))
import plan_variants as pv

DS_DIR = "dashboard/trading-signals-history/deepseek"
GAP = 1.0   # hds 现行跳空过滤
RULES = {
    "Plan H (hds现行 TP15/SL2/2d)":  lambda tk, ac, ep, sd: pv.simulate_fixed(tk, ac, ep, sd, 15, 2, 2, GAP),
    "移动止损 (init-4%/trail4%/10d)": lambda tk, ac, ep, sd: pv.simulate_trail(tk, ac, ep, sd, 4, 4, 10, GAP),
    "Plan C (TP8/SL4/5d)":           lambda tk, ac, ep, sd: pv.simulate_fixed(tk, ac, ep, sd, 8, 4, 5, GAP),
}
BASE = "Plan H (hds现行 TP15/SL2/2d)"


def read_ds_signals():
    out = []
    for fname in sorted(os.listdir(DS_DIR)):
        if not fname.endswith("-deepseek.json"):
            continue
        date_str = fname.replace("-deepseek.json", "")
        with open(os.path.join(DS_DIR, fname)) as f:
            d = json.load(f)
        for s in d.get("signals", []):
            out.append((date_str, s))
    return out


def rule_return(res):
    _cd, _cp, reason, final_pct, _daily, _d1 = res
    if reason == "gap_filtered":
        return None, "gap"
    if reason == "open" or final_pct is None:
        return None, "open"
    return final_pct, "closed"


def boot_ci(diffs, iters=5000):
    n = len(diffs)
    ms = sorted(mean(random.choices(diffs, k=n)) for _ in range(iters))
    return ms[int(iters * .025)], ms[int(iters * .975)]


rows = {name: {} for name in RULES}
n_sig = 0
for sd, s in read_ds_signals():
    tk, ac, ep = s.get("ticker"), s.get("action"), s.get("current_price")
    if ac not in ("BUY", "SELL") or not ep or ep != ep or int(pv.PER_POSITION_USD / ep) == 0:
        continue
    n_sig += 1
    key = (tk, sd, ac)
    for name, fn in RULES.items():
        pct, st = rule_return(fn(tk, ac, ep, sd))
        if st == "closed":
            rows[name][key] = pct

common = set.intersection(*(set(r.keys()) for r in rows.values()))
print(f"DeepSeek信号总数 {n_sig},三规则均已平仓的干净配对 {len(common)} 笔\n")
base_map = rows[BASE]
print(f"基线 = {BASE}")
print(f"  基线均收益 {mean([base_map[k] for k in common]):+.2f}%/笔\n")
for name in RULES:
    if name == BASE:
        continue
    diffs = [rows[name][k] - base_map[k] for k in sorted(common)]
    lo, hi = boot_ci(diffs)
    m = mean(diffs)
    verdict = ("✅ 显著更优" if lo > 0 else ("❌ 显著更差" if hi < 0 else "— 无显著差异"))
    print(f"{name}")
    print(f"  配对均差 {m:+.2f}%/笔  95%CI[{lo:+.2f}%, {hi:+.2f}%]  {verdict}")
    print(f"  赢配对 {sum(1 for d in diffs if d > 0)}/{len(diffs)}\n")
