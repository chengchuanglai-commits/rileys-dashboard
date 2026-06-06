"""
策略参数优化器
网格搜索所有 TP/SL/持仓天数/跳空过滤/入场方式组合，找出历史最优参数。
输出: dashboard/backtest-results.js + data/backtest_results.json
"""
import json, os, itertools, math
from datetime import datetime, timedelta
import yfinance as yf

SIGNALS_DIR  = "dashboard/trading-signals-history"
OUTPUT_JSON  = "data/backtest_results.json"
OUTPUT_JS    = "dashboard/backtest-results.js"
PER_TRADE    = 500     # 每笔固定仓位
START_CAP    = 2000

# ── 参数网格 ──────────────────────────────────────────────
TP_LIST      = [3, 5, 6, 8, 10, 12, 15]          # 止盈 %
SL_LIST      = [2, 3, 4, 5, 6]                    # 止损 %
HOLD_LIST    = [2, 3, 5, 7, 10]                   # 最大持仓交易日
GAP_LIST     = [0, 1.0, 1.5, 2.0, 3.0]            # 跳空过滤 % (0=不过滤)
ENTRY_LIST   = ["signal_price", "next_day_open"]   # 入场价

# ── 工具 ─────────────────────────────────────────────────
def next_n_trading_days(start_str, n):
    dt = datetime.strptime(start_str, "%Y-%m-%d")
    days = []
    while len(days) < n:
        dt += timedelta(days=1)
        if dt.weekday() < 5:
            days.append(dt.strftime("%Y-%m-%d"))
    return days

# ── 缓存 yfinance 数据（避免重复请求）────────────────────
price_cache = {}

def fetch_prices(ticker, signal_date, max_hold):
    key = (ticker, signal_date, max_hold)
    if key in price_cache:
        return price_cache[key]
    target_dates = next_n_trading_days(signal_date, max_hold)
    fetch_end = (datetime.strptime(target_dates[-1], "%Y-%m-%d") + timedelta(days=2)).strftime("%Y-%m-%d")
    try:
        df = yf.Ticker(ticker).history(start=signal_date, end=fetch_end)
        df.index = df.index.tz_localize(None) if df.index.tz else df.index
    except Exception as e:
        price_cache[key] = {}
        return {}
    rows = {}
    today_str = datetime.now().strftime("%Y-%m-%d")
    for target in target_dates:
        for idx, r in df.iterrows():
            if idx.strftime("%Y-%m-%d") == target:
                rows[target] = {
                    "open":  round(float(r["Open"]),  2),
                    "high":  round(float(r["High"]),  2),
                    "low":   round(float(r["Low"]),   2),
                    "close": round(float(r["Close"]), 2),
                }
                break
    price_cache[key] = rows
    return rows

# ── 单笔模拟 ────────────────────────────────────────────
def simulate(ticker, action, signal_price, signal_date,
             tp_pct, sl_pct, max_hold, gap_filter, entry_method):
    today_str = datetime.now().strftime("%Y-%m-%d")
    rows = fetch_prices(ticker, signal_date, max_hold)
    if not rows:
        return None

    target_dates = next_n_trading_days(signal_date, max_hold)
    day1_open = None

    for i, date in enumerate(target_dates):
        r = rows.get(date)
        if r is None:
            if date > today_str:
                return {"status": "open"}
            continue

        o, hi, lo, cl = r["open"], r["high"], r["low"], r["close"]

        if day1_open is None:
            day1_open = o
            # 入场价
            if entry_method == "next_day_open":
                entry = o
            else:
                entry = signal_price

            # 跳空过滤
            if gap_filter > 0:
                gap = (o - signal_price) / signal_price * 100
                unfav = -gap if action == "BUY" else gap
                if unfav > gap_filter:
                    return {"status": "gap_filtered", "gap_pct": round(gap, 2)}

            # 以入场价重新计算 TP/SL
            if action == "BUY":
                tp_price = round(entry * (1 + tp_pct / 100), 2)
                sl_price = round(entry * (1 - sl_pct / 100), 2)
            else:
                tp_price = round(entry * (1 - tp_pct / 100), 2)
                sl_price = round(entry * (1 + sl_pct / 100), 2)
        else:
            entry = entry  # already set

        # TP/SL 触发检测
        reason = exit_price = None
        if action == "BUY":
            if lo <= sl_price:
                reason, exit_price = "stop_loss", sl_price
            elif hi >= tp_price:
                reason, exit_price = "take_profit", tp_price
        else:
            if hi >= sl_price:
                reason, exit_price = "stop_loss", sl_price
            elif lo <= tp_price:
                reason, exit_price = "take_profit", tp_price

        if reason is None and date == target_dates[-1]:
            reason, exit_price = "max_hold", cl

        if reason:
            raw = (exit_price - entry) / entry * 100
            pnl_pct = raw if action == "BUY" else -raw
            pnl_usd = round(PER_TRADE * pnl_pct / 100, 2)
            return {
                "status": "closed",
                "close_reason": reason,
                "pnl_pct": round(pnl_pct, 2),
                "pnl_usd": pnl_usd,
                "entry": entry,
                "exit_price": exit_price,
                "close_date": date,
            }

    return {"status": "open"}

# ── 读取信号 ─────────────────────────────────────────────
all_signals = []
for fname in sorted(os.listdir(SIGNALS_DIR)):
    if not fname.endswith(".json") or "-report" in fname:
        continue
    date_str = fname.replace(".json", "")
    with open(os.path.join(SIGNALS_DIR, fname)) as f:
        d = json.load(f)
    for s in d.get("signals", []):
        if s.get("action") in ("BUY", "SELL") and s.get("current_price"):
            all_signals.append({
                "date": date_str,
                "ticker": s["ticker"],
                "name": s.get("name", ""),
                "action": s["action"],
                "signal_price": s["current_price"],
            })

print(f"Signals: {len(all_signals)} BUY/SELL across {len(set(s['date'] for s in all_signals))} days")

# ── 预取所有价格（用最大 hold 天数，避免重复请求）─────────
print("Pre-fetching price data...")
MAX_HOLD_PREFETCH = max(HOLD_LIST)
for s in all_signals:
    fetch_prices(s["ticker"], s["date"], MAX_HOLD_PREFETCH)
    print(f"  Fetched {s['ticker']} from {s['date']}")
print("Done.\n")

# ── 网格搜索 ─────────────────────────────────────────────
results = []
total_combos = len(TP_LIST) * len(SL_LIST) * len(HOLD_LIST) * len(GAP_LIST) * len(ENTRY_LIST)
print(f"Testing {total_combos} parameter combinations...\n")

for tp, sl, hold, gap, entry_m in itertools.product(
        TP_LIST, SL_LIST, HOLD_LIST, GAP_LIST, ENTRY_LIST):

    trades = []
    skipped = 0
    for s in all_signals:
        res = simulate(s["ticker"], s["action"], s["signal_price"], s["date"],
                       tp, sl, hold, gap, entry_m)
        if res is None:
            continue
        if res["status"] == "gap_filtered":
            skipped += 1
        elif res["status"] == "closed":
            trades.append({**res, "ticker": s["ticker"], "action": s["action"], "date": s["date"]})
        # "open" = still active, skip

    if not trades:
        continue

    wins  = [t for t in trades if t["pnl_usd"] > 0]
    losss = [t for t in trades if t["pnl_usd"] < 0]
    total_pnl = sum(t["pnl_usd"] for t in trades)
    win_rate  = round(len(wins) / len(trades) * 100, 1) if trades else 0

    avg_win  = sum(t["pnl_usd"] for t in wins)  / len(wins)  if wins  else 0
    avg_loss = sum(t["pnl_usd"] for t in losss) / len(losss) if losss else 0
    pf = round(avg_win / abs(avg_loss), 2) if losss else (999 if wins else 0)

    avg_per_trade = round(total_pnl / len(trades), 2)

    # 期望值 = 理论 EV per trade
    ev = round(win_rate/100 * (tp * PER_TRADE/100) - (1 - win_rate/100) * (sl * PER_TRADE/100), 2)

    # 最大回撤
    equity = START_CAP
    peak = equity
    max_dd = 0
    for t in sorted(trades, key=lambda x: x["close_date"]):
        equity += t["pnl_usd"]
        peak = max(peak, equity)
        dd = (peak - equity) / peak * 100
        max_dd = max(max_dd, dd)

    results.append({
        "tp": tp, "sl": sl, "hold": hold, "gap": gap, "entry": entry_m,
        "trades": len(trades), "skipped": skipped,
        "wins": len(wins), "losses": len(losss),
        "win_rate": win_rate,
        "total_pnl": round(total_pnl, 2),
        "portfolio_value": round(START_CAP + total_pnl, 2),
        "return_pct": round(total_pnl / START_CAP * 100, 2),
        "profit_factor": pf,
        "avg_per_trade": avg_per_trade,
        "max_drawdown_pct": round(max_dd, 2),
        "ev_per_trade": ev,
        "trade_detail": trades,
    })

# ── 排序 & 输出 ──────────────────────────────────────────
results.sort(key=lambda r: r["total_pnl"], reverse=True)

print(f"\n{'='*70}")
print(f"  TOP 20 策略 （按总盈亏排序）")
print(f"{'='*70}")
print(f"  {'TP':>4} {'SL':>4} {'Hold':>5} {'Gap':>5} {'Entry':>12}  "
      f"{'笔数':>4} {'胜率':>6} {'总盈亏':>10} {'盈亏比':>6} {'平均/笔':>8} {'回撤':>6}")
print(f"  {'-'*70}")
for r in results[:20]:
    entry_short = "信号价" if r["entry"] == "signal_price" else "开盘价"
    print(f"  {r['tp']:>3}% {r['sl']:>3}% {r['hold']:>4}日 {r['gap']:>4}% {entry_short:>6}  "
          f"{r['trades']:>4} {r['win_rate']:>5}% {r['total_pnl']:>+9.2f} "
          f"{r['profit_factor']:>6.2f} {r['avg_per_trade']:>+7.2f} {r['max_drawdown_pct']:>5.1f}%")

# 当前 B/C 方案的排名
def find_rank(tp, sl, hold, gap, entry):
    for i, r in enumerate(results):
        if r['tp']==tp and r['sl']==sl and r['hold']==hold and r['gap']==gap and r['entry']==entry:
            return i+1, r
    return None, None

b_rank, b_res = find_rank(8, 4, 5, 0, "signal_price")
c_rank, c_res = find_rank(8, 4, 5, 1.5, "signal_price")
print(f"\n  当前 B 方案 (TP8/SL4/5日/无过滤/信号价) 排名: #{b_rank}  总盈亏: ${b_res['total_pnl'] if b_res else 'N/A'}")
print(f"  当前 C 方案 (TP8/SL4/5日/1.5%过滤/信号价) 排名: #{c_rank}  总盈亏: ${c_res['total_pnl'] if c_res else 'N/A'}")

# ── 保存 ─────────────────────────────────────────────────
os.makedirs("data", exist_ok=True)
out = {
    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "total_signals": len(all_signals),
    "total_combos_tested": total_combos,
    "top_strategies": results[:50],   # 前50
    "plan_b_rank": b_rank,
    "plan_c_rank": c_rank,
    "_note": "样本量仅10笔，结果仅供参考，需随信号积累持续更新",
}

with open(OUTPUT_JSON, "w") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

with open(OUTPUT_JS, "w", encoding="utf-8") as f:
    f.write("// 策略回测优化结果\n")
    f.write(f"window.BACKTEST_RESULTS = {json.dumps(out, ensure_ascii=False, indent=2)};\n")

print(f"\n已保存 → {OUTPUT_JSON} / {OUTPUT_JS}")
print(f"共测试 {total_combos} 种参数组合，最优策略总盈亏 ${results[0]['total_pnl']:+.2f}")
