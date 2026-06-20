"""
Plan C 历史回溯模拟
Plan B 规则 + 跳空过滤：次日开盘若对持仓方向不利跳空 > GAP_FILTER_PCT，跳过该信号。

⚠️ 观察候选淘汰：2026-06-11 的 12 个月历史回测中，本参数(TP8/SL4/5日/1.5%跳空)排名 ~#351/700，
   属中下游（同 Plan B 的弱出场参数）。优选方向见 Plan H(TP15/SL2/2日，历史 PF 最高)。

入场规则：信号价（prev close），BUY/SELL 方向，且次日开盘不利跳空 ≤ GAP_FILTER_PCT
出场规则：TP +8%、SL -4%、最大持仓 5 交易日
佣金：IBKR $0.005/股，最低 $1.00/单（入场+出场各一次）
"""
import json, os
from datetime import datetime, timedelta
import yfinance as yf
from portfolio_compound import compound_portfolio   # frac10 复利回填(与决策视图排名同口径)

SIGNALS_DIR = "dashboard/trading-signals-history"
PORTFOLIO_PATH = "data/portfolio_c.json"
os.makedirs("data", exist_ok=True)

TP_PCT = 8
SL_PCT = 4
MAX_HOLD_TRADING_DAYS = 5
PER_POSITION_USD = 500
STARTING_CAPITAL = 2000
GAP_FILTER_PCT = 1.5   # 不利跳空超过此值则跳过

def ibkr_commission(shares):
    return round(max(1.00, shares * 0.005), 2)

def next_n_trading_days(start_str, n):
    dt = datetime.strptime(start_str, "%Y-%m-%d")
    days = []
    while len(days) < n:
        dt += timedelta(days=1)
        if dt.weekday() < 5:
            days.append(dt.strftime("%Y-%m-%d"))
    return days

def simulate_position(ticker, action, entry_price, signal_date):
    tp_price = round(entry_price * (1 + TP_PCT / 100 if action == "BUY" else 1 - TP_PCT / 100), 2)
    sl_price = round(entry_price * (1 - SL_PCT / 100 if action == "BUY" else 1 + SL_PCT / 100), 2)

    target_dates = next_n_trading_days(signal_date, MAX_HOLD_TRADING_DAYS)
    fetch_end = (datetime.strptime(target_dates[-1], "%Y-%m-%d") + timedelta(days=2)).strftime("%Y-%m-%d")

    try:
        df = yf.Ticker(ticker).history(start=signal_date, end=fetch_end)
        df.index = df.index.tz_localize(None) if df.index.tz is not None else df.index
    except Exception as e:
        print(f"  [warn] yfinance failed for {ticker}: {e}")
        return None, None, "open", None, {}, None

    today_str = datetime.now().strftime("%Y-%m-%d")
    daily_prices = {}
    day1_open = None

    for target_date in target_dates:
        row = None
        for idx, r in df.iterrows():
            if idx.strftime("%Y-%m-%d") == target_date:
                row = r
                break

        if row is None:
            if target_date > today_str:
                return None, None, "open", None, daily_prices, day1_open
            continue

        o  = round(float(row["Open"]),  2)
        hi = round(float(row["High"]),  2)
        lo = round(float(row["Low"]),   2)
        cl = round(float(row["Close"]), 2)
        if any(v != v for v in (o, hi, lo, cl)):  # 跳过 yfinance NaN bar(OTC延迟)，否则污染净值
            continue

        # ── 第一个交易日：检查跳空过滤 ──
        if day1_open is None:
            day1_open = o
            gap_pct = (o - entry_price) / entry_price * 100
            unfavorable_gap = -gap_pct if action == "BUY" else gap_pct
            if unfavorable_gap > GAP_FILTER_PCT:
                return None, None, "gap_filtered", None, {}, day1_open

        close_reason = None
        close_price = cl
        if action == "BUY":
            if lo <= sl_price:
                close_reason, close_price = "stop_loss", sl_price
            elif hi >= tp_price:
                close_reason, close_price = "take_profit", tp_price
        else:
            if hi >= sl_price:
                close_reason, close_price = "stop_loss", sl_price
            elif lo <= tp_price:
                close_reason, close_price = "take_profit", tp_price

        raw_pct = (close_price - entry_price) / entry_price * 100
        pnl_pct = raw_pct if action == "BUY" else -raw_pct
        daily_prices[target_date] = {"open": o, "high": hi, "low": lo, "close": cl, "pnl_pct": round(pnl_pct, 2)}

        if close_reason:
            return target_date, close_price, close_reason, round(pnl_pct, 2), daily_prices, day1_open

        if target_date == target_dates[-1]:
            raw_pct = (cl - entry_price) / entry_price * 100
            pnl_pct = raw_pct if action == "BUY" else -raw_pct
            daily_prices[target_date]["pnl_pct"] = round(pnl_pct, 2)
            return target_date, cl, "max_hold", round(pnl_pct, 2), daily_prices, day1_open

    return None, None, "open", None, daily_prices, day1_open

# ── 读取所有历史信号 ──────────────────────────────────────────────

portfolio = {
    "capital_usd": STARTING_CAPITAL,
    "open_positions": [],
    "closed_positions": [],
    "_note": f"Plan C 模拟盘：TP +8% / SL -4% / 最大5交易日 / 不利跳空>{GAP_FILTER_PCT}%跳过 / IBKR佣金$0.005/股min$1"
}

all_signals = []
for fname in sorted(os.listdir(SIGNALS_DIR)):
    if not fname.endswith(".json") or "-report" in fname:
        continue
    date_str = fname.replace(".json", "")
    with open(os.path.join(SIGNALS_DIR, fname)) as f:
        d = json.load(f)
    for s in d.get("signals", []):
        all_signals.append((date_str, s))

print(f"Found {len(all_signals)} signals across {len([f for f in os.listdir(SIGNALS_DIR) if f.endswith('.json') and '-report' not in f])} days")

# ── 逐个信号模拟 ──────────────────────────────────────────────────

skipped_gap = 0
skipped_zero_shares = 0
for signal_date, s in all_signals:
    ticker  = s.get("ticker")
    action  = s.get("action")
    entry_price = s.get("current_price")

    if action not in ("BUY", "SELL") or not entry_price:
        print(f"  Skip {signal_date} {ticker} {action} (HOLD or no price)")
        continue

    shares = int(PER_POSITION_USD / entry_price)
    if shares == 0:
        print(f"  Skip {signal_date} {ticker} @ ${entry_price} (too expensive, 0 shares with ${PER_POSITION_USD})")
        skipped_zero_shares += 1
        continue

    actual_position_usd = round(shares * entry_price, 2)
    entry_comm = ibkr_commission(shares)
    exit_comm = ibkr_commission(shares)

    print(f"  Simulating {action} {ticker} @ ${entry_price} x{shares}sh [{signal_date}]...")
    close_date, close_price, close_reason, final_pnl_pct, daily_prices, day1_open = simulate_position(
        ticker, action, entry_price, signal_date
    )

    if close_reason == "gap_filtered":
        gap_pct = (day1_open - entry_price) / entry_price * 100
        print(f"    → GAP FILTERED: open=${day1_open} gap={gap_pct:+.1f}% (不利跳空>{GAP_FILTER_PCT}%，跳过)")
        skipped_gap += 1
        continue

    if action == "BUY":
        tp = round(entry_price * (1 + TP_PCT / 100), 2)
        sl = round(entry_price * (1 - SL_PCT / 100), 2)
    else:
        tp = round(entry_price * (1 - TP_PCT / 100), 2)
        sl = round(entry_price * (1 + SL_PCT / 100), 2)

    max_dates = next_n_trading_days(signal_date, MAX_HOLD_TRADING_DAYS)
    max_hold_date = max_dates[-1]

    position = {
        "ticker": ticker,
        "name": s.get("name", ""),
        "action": action,
        "signal_date": signal_date,
        "entry_price": entry_price,
        "allocated_usd": PER_POSITION_USD,
        "shares": shares,
        "actual_position_usd": actual_position_usd,
        "entry_commission": entry_comm,
        "take_profit": tp,
        "stop_loss": sl,
        "max_hold_date": max_hold_date,
        "day1_open": day1_open,
        "daily_prices": daily_prices,
    }

    if close_reason == "open":
        portfolio["open_positions"].append(position)
        latest_pnl = list(daily_prices.values())[-1]['pnl_pct'] if daily_prices else 'N/A'
        print(f"    → Still OPEN (latest pnl: {latest_pnl}%)")
    elif close_date:
        gross_pnl = round(actual_position_usd * final_pnl_pct / 100, 2)
        realized_pnl = round(gross_pnl - entry_comm - exit_comm, 2)
        closed = {**position, "close_date": close_date, "close_price": close_price,
                  "final_pnl_pct": final_pnl_pct, "close_reason": close_reason,
                  "exit_commission": exit_comm,
                  "commission_total": round(entry_comm + exit_comm, 2),
                  "realized_pnl_usd": realized_pnl}
        portfolio["closed_positions"].append(closed)
        print(f"    → Closed {close_reason} @ ${close_price} {final_pnl_pct:+.2f}% gross=${gross_pnl:+.2f} comm=-${entry_comm+exit_comm:.2f} net=${realized_pnl:+.2f}")
    else:
        print(f"    → No data available, skipping")

# ── 统计 ──────────────────────────────────────────────────────────

import math
def safe_pnl(p):
    if not p.get("daily_prices"): return 0
    v = list(p["daily_prices"].values())[-1].get("pnl_pct")
    return 0 if (v is None or (isinstance(v, float) and math.isnan(v))) else v

# frac10 复利回填:每仓=当前净值20%,复利,最多5并发(取代固定$500,与决策视图排名同口径)
fc, fo, _pv, total_realized, open_unrealized, skipped_no_cash = compound_portfolio(
    portfolio["closed_positions"], portfolio["open_positions"], safe_pnl, STARTING_CAPITAL)
portfolio["closed_positions"] = fc
portfolio["open_positions"] = fo
all_closed = fc
wins = [p for p in all_closed if p.get("realized_pnl_usd", 0) > 0]
total_commission = sum(p.get("commission_total", 0) for p in all_closed)

portfolio["stats"] = {
    "total_trades": len(all_closed),
    "win_trades": len(wins),
    "win_rate": round(len(wins) / len(all_closed) * 100, 1) if all_closed else 0,
    "total_realized_pnl_usd": round(total_realized, 2),
    "open_unrealized_pnl_usd": round(open_unrealized, 2),
    "portfolio_value": round(STARTING_CAPITAL + total_realized + open_unrealized, 2),
    "total_commission_usd": round(total_commission, 2),
    "skipped_gap": skipped_gap,
    "skipped_zero_shares": skipped_zero_shares,
    "updated_at": datetime.now().strftime("%Y-%m-%d"),
}

# ── 保存 ──────────────────────────────────────────────────────────

def clean_nan(obj):
    """递归将 NaN/Inf 替换为 None，使 JSON 合法。"""
    import math
    if isinstance(obj, float):
        return None if (math.isnan(obj) or math.isinf(obj)) else obj
    if isinstance(obj, dict):
        return {k: clean_nan(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean_nan(v) for v in obj]
    return obj

portfolio = clean_nan(portfolio)

with open(PORTFOLIO_PATH, "w") as f:
    json.dump(portfolio, f, ensure_ascii=False, indent=2)

with open("dashboard/portfolio-c.js", "w", encoding="utf-8") as f:
    f.write("// Plan C 模拟盘持仓 — 历史回溯 + 实时更新（跳空过滤版）\n")
    f.write(f"window.PORTFOLIO_C = {json.dumps(portfolio, ensure_ascii=False, indent=2)};\n")

s = portfolio["stats"]
print(f"\n{'='*55}")
print(f"  💼 Plan C 模拟盘回溯结果（跳空过滤 >{GAP_FILTER_PCT}%）")
print(f"{'='*55}")
print(f"  起始本金: ${STARTING_CAPITAL}")
print(f"  总交易:   {s['total_trades']} 笔  胜率: {s['win_rate']}%")
print(f"  跳过信号: {skipped_gap} 笔（不利跳空）")
print(f"  已实现:   ${s['total_realized_pnl_usd']:+.2f}  (佣金 -${s['total_commission_usd']:.2f})")
unreal = s['open_unrealized_pnl_usd'] or 0
pv = s['portfolio_value'] or (STARTING_CAPITAL + total_realized)
print(f"  浮盈:     ${unreal:+.2f}")
print(f"  组合价值: ${pv}")
print(f"  持仓中:   {len(portfolio['open_positions'])} 只")
print()
print("  已平仓明细:")
for p in all_closed:
    print(f"    {p['action']:4} {p['ticker']:6} {p['signal_date']} → {p['close_date']} "
          f"({p['close_reason']:12}) {p['final_pnl_pct']:+.2f}% / ${p['realized_pnl_usd']:+.2f}")
if portfolio["open_positions"]:
    print("  持仓中:")
    for p in portfolio["open_positions"]:
        latest = list(p["daily_prices"].values())[-1] if p["daily_prices"] else {}
        pnl_show = latest.get('pnl_pct') or 0
        print(f"    {p['action']:4} {p['ticker']:6} {p['signal_date']} (到期 {p['max_hold_date']}) "
              f"浮盈 {pnl_show:+.2f}%")
