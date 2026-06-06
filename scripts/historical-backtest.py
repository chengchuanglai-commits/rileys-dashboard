"""
大规模历史回测 — 纯出场参数验证（不依赖 AI 信号，免费）

思路：
  取 30+ 只小盘/中盘股过去 12 个月 OHLC 数据，
  对每个日期 × 每只股票生成模拟入场，
  测试所有 TP/SL/持仓天数/跳空过滤组合，
  在不同"信号胜率假设"下找出期望值最大的出场参数。

输出: data/historical_backtest.json + dashboard/historical-backtest.js
"""
import json, os, itertools, random, math
from datetime import datetime, timedelta, date
import yfinance as yf

# ── 股票池：小盘/中盘，与 AI 信号风格一致 ──────────────────
UNIVERSE = [
    # 已出现在我们信号里的
    "UCTT", "WTTR", "MXL", "ALGT", "IMOS", "KLIC", "CAMT", "DXCM", "AMBA", "FLR",
    # 同类小盘半导体/工业
    "ACLS", "AEHR", "COHU", "FORM", "ICHR", "NTAP", "ONTO", "POWI", "SMTC", "SITM",
    # 小盘生物/工业
    "AAON", "APOG", "ARCB", "BOOT", "CEIX", "GFF", "HCC", "ITIC", "JBSS", "MGPI",
    # 波动性适中的中盘
    "LRCX", "MU", "SWKS", "WOLF", "QRVO",
]

# ── 参数网格 ──────────────────────────────────────────────
TP_LIST   = [3, 5, 6, 8, 10, 12, 15]
SL_LIST   = [2, 3, 4, 5, 6]
HOLD_LIST = [2, 3, 5, 7, 10]
GAP_LIST  = [0, 1.0, 1.5, 2.0]

# ── 回测设置 ──────────────────────────────────────────────
HIST_MONTHS   = 12
PER_TRADE     = 500
# 每只股票每月最多采样 N 个入场点（控制样本量，避免过多数据倾斜）
SAMPLES_PER_STOCK_MONTH = 2
RANDOM_SEED   = 42

random.seed(RANDOM_SEED)

end_date   = datetime.now()
start_date = end_date - timedelta(days=HIST_MONTHS * 31)

OUTPUT_JSON = "data/historical_backtest.json"
OUTPUT_JS   = "dashboard/historical-backtest.js"
os.makedirs("data", exist_ok=True)

# ── 辅助函数 ──────────────────────────────────────────────
def next_n_trading_days_from(start_dt, n):
    days = []
    dt = start_dt
    while len(days) < n:
        dt += timedelta(days=1)
        if dt.weekday() < 5:
            days.append(dt)
    return days

# ── 拉取历史数据 ──────────────────────────────────────────
print(f"Fetching {len(UNIVERSE)} stocks × {HIST_MONTHS} months...")
stock_data = {}
failed = []
for ticker in UNIVERSE:
    try:
        df = yf.Ticker(ticker).history(start=start_date.strftime("%Y-%m-%d"),
                                        end=end_date.strftime("%Y-%m-%d"))
        if df.empty:
            failed.append(ticker)
            continue
        df.index = df.index.tz_localize(None) if df.index.tz else df.index
        rows = {}
        for idx, r in df.iterrows():
            rows[idx.date()] = {
                "open":  round(float(r["Open"]),  2),
                "high":  round(float(r["High"]),  2),
                "low":   round(float(r["Low"]),   2),
                "close": round(float(r["Close"]), 2),
            }
        stock_data[ticker] = rows
        print(f"  {ticker}: {len(rows)} trading days")
    except Exception as e:
        print(f"  {ticker}: FAILED — {e}")
        failed.append(ticker)

print(f"\nLoaded {len(stock_data)} stocks, {len(failed)} failed: {failed}\n")

# ── 生成入场点 ────────────────────────────────────────────
# 对每只股票，每月随机选 SAMPLES_PER_STOCK_MONTH 个交易日作为入场点
entries = []  # [(ticker, entry_date, action)]
today = datetime.now().date()

for ticker, rows in stock_data.items():
    sorted_dates = sorted(rows.keys())
    # 按月分组
    from collections import defaultdict
    by_month = defaultdict(list)
    for d in sorted_dates:
        by_month[(d.year, d.month)].append(d)

    for (y, m), days in by_month.items():
        # 需要 entry_date 后面还有足够的数据用于模拟出场
        valid = [d for d in days if len([x for x in sorted_dates if x > d]) >= max(HOLD_LIST)]
        if not valid:
            continue
        sampled = random.sample(valid, min(SAMPLES_PER_STOCK_MONTH, len(valid)))
        for entry_date in sampled:
            # 同时生成 BUY 和 SELL 方向，用入场日收盘价
            entries.append((ticker, entry_date, "BUY"))
            entries.append((ticker, entry_date, "SELL"))

print(f"Generated {len(entries)} entry points across {len(stock_data)} stocks\n")

# ── 核心模拟函数 ──────────────────────────────────────────
def simulate_exit(ticker, action, entry_date, tp_pct, sl_pct, max_hold, gap_filter):
    rows = stock_data[ticker]
    entry_price = rows[entry_date]["close"]

    hold_dates = next_n_trading_days_from(entry_date, max_hold)
    day1 = hold_dates[0]
    day1_row = rows.get(day1)
    if not day1_row:
        return None

    day1_open = day1_row["open"]
    # 跳空过滤
    if gap_filter > 0:
        gap = (day1_open - entry_price) / entry_price * 100
        unfav = -gap if action == "BUY" else gap
        if unfav > gap_filter:
            return {"status": "gap_filtered"}

    tp_price = entry_price * (1 + tp_pct/100) if action == "BUY" else entry_price * (1 - tp_pct/100)
    sl_price = entry_price * (1 - sl_pct/100) if action == "BUY" else entry_price * (1 + sl_pct/100)

    for hold_date in hold_dates:
        row = rows.get(hold_date)
        if not row:
            continue
        hi, lo, cl = row["high"], row["low"], row["close"]

        if action == "BUY":
            if lo <= sl_price:
                return {"status": "closed", "reason": "stop_loss",  "pnl_pct": -sl_pct}
            if hi >= tp_price:
                return {"status": "closed", "reason": "take_profit", "pnl_pct": +tp_pct}
        else:
            if hi >= sl_price:
                return {"status": "closed", "reason": "stop_loss",  "pnl_pct": -sl_pct}
            if lo <= tp_price:
                return {"status": "closed", "reason": "take_profit", "pnl_pct": +tp_pct}

        if hold_date == hold_dates[-1]:
            raw = (cl - entry_price) / entry_price * 100
            pnl = raw if action == "BUY" else -raw
            return {"status": "closed", "reason": "max_hold", "pnl_pct": round(pnl, 3)}

    return None

# ── 网格搜索 ──────────────────────────────────────────────
combos = list(itertools.product(TP_LIST, SL_LIST, HOLD_LIST, GAP_LIST))
total = len(combos)
print(f"Testing {total} parameter combinations on {len(entries)} entry points...\n")

results = []
for ci, (tp, sl, hold, gap) in enumerate(combos):
    if ci % 20 == 0:
        print(f"  {ci}/{total}...")

    tp_hits = sl_hits = mh_exits = gap_filtered = 0
    all_pnl = []

    for ticker, entry_date, action in entries:
        res = simulate_exit(ticker, action, entry_date, tp, sl, hold, gap)
        if res is None:
            continue
        if res["status"] == "gap_filtered":
            gap_filtered += 1
            continue
        pnl = res["pnl_pct"]
        all_pnl.append(pnl)
        if res["reason"] == "take_profit": tp_hits += 1
        elif res["reason"] == "stop_loss": sl_hits += 1
        else: mh_exits += 1

    if not all_pnl:
        continue

    n = len(all_pnl)
    wins = [p for p in all_pnl if p > 0]
    loss = [p for p in all_pnl if p < 0]
    win_rate = len(wins) / n * 100

    avg_win  = sum(wins) / len(wins) if wins else 0
    avg_loss = sum(loss) / len(loss) if loss else 0
    pf = round(avg_win / abs(avg_loss), 3) if loss else 999

    avg_pnl   = sum(all_pnl) / n
    std_pnl   = (sum((x - avg_pnl)**2 for x in all_pnl) / n) ** 0.5
    sharpe    = round(avg_pnl / std_pnl, 3) if std_pnl > 0 else 0

    # 按不同胜率假设计算理论期望值（模拟 AI 信号质量）
    # EV = accuracy × avg_win% × PER_TRADE  - (1-accuracy) × avg_loss% × PER_TRADE
    ev_by_acc = {}
    for acc in [0.50, 0.55, 0.60, 0.65]:
        ev = acc * (tp * PER_TRADE / 100) - (1 - acc) * (sl * PER_TRADE / 100)
        ev_by_acc[str(int(acc*100))] = round(ev, 2)

    # 实际期望值（基于历史价格的纯随机入场）
    actual_ev = round(win_rate/100 * avg_win * PER_TRADE/100 - (1 - win_rate/100) * abs(avg_loss) * PER_TRADE/100, 2)

    results.append({
        "tp": tp, "sl": sl, "hold": hold, "gap": gap,
        "n": n, "gap_filtered": gap_filtered,
        "win_rate": round(win_rate, 1),
        "tp_rate":  round(tp_hits/n*100, 1),
        "sl_rate":  round(sl_hits/n*100, 1),
        "mh_rate":  round(mh_exits/n*100, 1),
        "avg_win_pct":  round(avg_win, 3),
        "avg_loss_pct": round(avg_loss, 3),
        "profit_factor": pf,
        "sharpe": sharpe,
        "actual_ev_per_trade": actual_ev,
        "ev_at_50pct": ev_by_acc["50"],
        "ev_at_55pct": ev_by_acc["55"],
        "ev_at_60pct": ev_by_acc["60"],
        "ev_at_65pct": ev_by_acc["65"],
    })

# ── 排序 & 输出 ──────────────────────────────────────────
results.sort(key=lambda r: r["ev_at_60pct"], reverse=True)

print(f"\n{'='*75}")
print(f"  TOP 20（按 60% 胜率假设下的每笔期望值）")
print(f"{'='*75}")
print(f"  {'TP':>4} {'SL':>4} {'Hold':>5} {'Gap':>5}  {'N':>5} {'胜率':>6} {'TP触发':>7} {'SL触发':>7} "
      f"{'EV@50%':>7} {'EV@55%':>7} {'EV@60%':>7} {'PF':>5} {'Sharpe':>6}")
print(f"  {'-'*75}")

for r in results[:20]:
    print(f"  {r['tp']:>3}% {r['sl']:>3}% {r['hold']:>4}日 {r['gap']:>4}%  "
          f"{r['n']:>5} {r['win_rate']:>5}% {r['tp_rate']:>6}% {r['sl_rate']:>6}%  "
          f"${r['ev_at_50pct']:>5.2f} ${r['ev_at_55pct']:>5.2f} ${r['ev_at_60pct']:>5.2f}  "
          f"{r['profit_factor']:>4.2f}  {r['sharpe']:>5.3f}")

# 当前 B/C 的排名
b_rank = c_rank = None
for i, r in enumerate(results):
    if r['tp']==8 and r['sl']==4 and r['hold']==5 and r['gap']==0:
        b_rank = i+1
    if r['tp']==8 and r['sl']==4 and r['hold']==5 and r['gap']==1.5:
        c_rank = i+1

print(f"\n  当前 B 方案参数 (TP8/SL4/5日/无过滤) 排名: #{b_rank}")
print(f"  当前 C 方案参数 (TP8/SL4/5日/1.5%过滤) 排名: #{c_rank}")

best = results[0]
print(f"\n  大规模历史验证最优参数:")
print(f"  TP={best['tp']}% / SL={best['sl']}% / {best['hold']}日 / Gap={best['gap']}%")
print(f"  N={best['n']}笔  胜率={best['win_rate']}%  EV@60%=${best['ev_at_60pct']}/笔  PF={best['profit_factor']}")

# ── 保存 ─────────────────────────────────────────────────
out = {
    "generated_at":   datetime.now().strftime("%Y-%m-%d %H:%M"),
    "hist_months":    HIST_MONTHS,
    "universe_size":  len(stock_data),
    "total_entries":  len(entries),
    "combos_tested":  total,
    "top_strategies": results[:50],
    "plan_b_rank":    b_rank,
    "plan_c_rank":    c_rank,
    "_note": "基于历史价格的大规模参数验证，入场随机（非AI信号），用于评估出场参数本身的统计优势",
}

with open(OUTPUT_JSON, "w") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
with open(OUTPUT_JS, "w", encoding="utf-8") as f:
    f.write("// 大规模历史出场参数回测结果\n")
    f.write(f"window.HIST_BACKTEST = {json.dumps(out, ensure_ascii=False, indent=2)};\n")

print(f"\n已保存 → {OUTPUT_JSON} / {OUTPUT_JS}")
print(f"共 {len(entries)} 笔模拟交易 × {total} 种参数组合")
