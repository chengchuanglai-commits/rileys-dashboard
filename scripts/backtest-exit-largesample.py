"""
方法 B —— 大样本出场回测(几千笔合成入场,真正的统计火力)。

变体只差出场规则。所以拿信号里出现过的股票 + 多年历史价格,机械造出成千上万个入场点
(每隔几天、多空各一),把 Plan C / Plan H / 移动止损三种出场各跑一遍,做配对差异检验。
入场是代理(非真 AI 信号),故答的是"对这类小盘股,哪种出场结构更好"——与方法A(真信号前向配对)三角互证。
出场判定复用 plan_variants 的共享核心(_fixed_hit/_trail_hit/_trail_update),与实盘/方法A同一份逻辑。

跳空过滤关闭(三规则同入场集,纯出场对比;跳空是另一个已单独研究的问题)。
大样本用解析正态 CI(均值 ± 1.96·SE)。
"""
import os, json, math
from statistics import mean, pstdev
from datetime import datetime
import yfinance as yf
import plan_variants as pv

STEP = 3          # 每隔3个交易日造一个入场点
MAX_TICKERS = 60  # 控制 yfinance 拉取量
PERIOD = "2y"
DIRECTIONS = ["BUY", "SELL"]


def signal_tickers():
    seen = []
    for sd, s in pv._read_signals():
        t = s.get("ticker")
        if t and t not in seen:
            seen.append(t)
    return seen[:MAX_TICKERS]


def walk_fixed(action, entry, seq, tp_pct, sl_pct):
    """seq = 持仓日 [(o,h,l,c), ...]。复用 _fixed_hit。返回收益%(按方向)。"""
    tp = entry * (1 + (tp_pct if action == "BUY" else -tp_pct) / 100)
    sl = entry * (1 - (sl_pct if action == "BUY" else -sl_pct) / 100)
    for (o, h, l, c) in seq:
        reason, price = pv._fixed_hit(action, h, l, tp, sl)
        if reason:
            raw = (price - entry) / entry * 100
            return raw if action == "BUY" else -raw
    c = seq[-1][3]
    raw = (c - entry) / entry * 100
    return raw if action == "BUY" else -raw


def walk_trail(action, entry, seq, sl_pct, trail_pct):
    """复用 _trail_hit/_trail_update。返回收益%(按方向)。"""
    stop = entry * (1 - sl_pct / 100) if action == "BUY" else entry * (1 + sl_pct / 100)
    extreme = entry
    for (o, h, l, c) in seq:
        hit = pv._trail_hit(action, h, l, stop)
        if hit is not None:
            raw = (hit - entry) / entry * 100
            return raw if action == "BUY" else -raw
        extreme, stop = pv._trail_update(action, h, l, extreme, stop, trail_pct)
    raw = (c - entry) / entry * 100
    return raw if action == "BUY" else -raw


RULES = {
    "Plan C (TP8/SL4/5d)":  lambda ac, ep, seq: walk_fixed(ac, ep, seq[:5], 8, 4),
    "Plan H (TP15/SL2/2d)": lambda ac, ep, seq: walk_fixed(ac, ep, seq[:2], 15, 2),
    "移动止损 (-4%/trail4%/10d)": lambda ac, ep, seq: walk_trail(ac, ep, seq[:10], 4, 4),
}
BASE = "Plan C (TP8/SL4/5d)"


def collect():
    """返回 {rule: {dir: [rets]}} 配对(同 idx 同 entry)。用 idx 对齐配对。"""
    tickers = signal_tickers()
    print(f"  股票池 {len(tickers)} 只,拉 {PERIOD} 历史,每 {STEP} 日造入场,多空各一...")
    # per-direction 配对列表:pairs[dir] = list of (retC, retH, retTrail)
    pairs = {d: [] for d in DIRECTIONS}
    ok = 0
    for tk in tickers:
        try:
            df = yf.Ticker(tk).history(period=PERIOD)
        except Exception:
            continue
        if df is None or len(df) < 15:
            continue
        bars = []
        for _, r in df.iterrows():
            o, h, l, c = (round(float(r[k]), 4) for k in ("Open", "High", "Low", "Close"))
            if any(v != v for v in (o, h, l, c)):
                continue
            bars.append((o, h, l, c))
        if len(bars) < 15:
            continue
        ok += 1
        for i in range(0, len(bars) - 11, STEP):
            entry = bars[i][3]            # 入场=当日收盘
            seq = bars[i + 1:i + 11]      # 之后最多10个持仓日
            if not seq or entry <= 0:
                continue
            for d in DIRECTIONS:
                rc = RULES[BASE](d, entry, seq)
                rh = RULES["Plan H (TP15/SL2/2d)"](d, entry, seq)
                rt = RULES["移动止损 (-4%/trail4%/10d)"](d, entry, seq)
                pairs[d].append((rc, rh, rt))
    print(f"  成功股票 {ok} 只")
    return pairs


def report_pairs(label, rows):
    n = len(rows)
    if n < 30:
        print(f"  [{label}] 样本 {n} 太少,跳过"); return
    rc = [x[0] for x in rows]
    print(f"\n  【{label}】配对样本 {n} 笔 | 基线 Plan C 均收益 {mean(rc):+.3f}%/笔")
    for idx, name in [(1, "Plan H (TP15/SL2/2d)"), (2, "移动止损 (-4%/trail4%/10d)")]:
        rr = [x[idx] for x in rows]
        diffs = [x[idx] - x[0] for x in rows]
        md = mean(diffs)
        se = pstdev(diffs) / math.sqrt(n)
        lo, hi = md - 1.96 * se, md + 1.96 * se
        wins = sum(1 for d in diffs if d > 1e-9); losses = sum(1 for d in diffs if d < -1e-9)
        sig = "🟢 显著优于C" if lo > 0 else ("🔴 显著劣于C" if hi < 0 else "⚪ 无显著差异")
        print(f"    {name:26} 均收益 {mean(rr):+.3f}% | 配对差 {md:+.4f}%pt "
              f"95%CI[{lo:+.4f},{hi:+.4f}] 赢/输 {wins}/{losses} → {sig}")


pairs = collect()
print("=" * 78)
print(f"  方法B · 大样本出场回测  (合成入场, {PERIOD} 历史, 步长{STEP}d)")
print("=" * 78)
allrows = pairs["BUY"] + pairs["SELL"]
report_pairs("全部(多+空)", allrows)
report_pairs("仅做多 BUY", pairs["BUY"])
report_pairs("仅做空 SELL(=真策略主体,88%是空)", pairs["SELL"])
print("\n  注:入场为机械代理非真信号,测的是出场结构的稳健性;真信号裁决看方法A+前向80笔。")
