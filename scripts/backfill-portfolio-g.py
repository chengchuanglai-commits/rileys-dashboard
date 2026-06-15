"""
Plan G — 并发仓位限制方案
参数与 Plan D 完全相同：TP +15% / SL -3% / 最大持仓 2 交易日 / 不利跳空 >1% 过滤
新增规则：同时持仓上限 4 笔，超出时跳过新信号（资金管理优化）
佣金：IBKR $0.005/股，最低 $1.00/单（入场+出场各一次）
"""
import json, os
from datetime import datetime, timedelta
import yfinance as yf

SIGNALS_DIR = "dashboard/trading-signals-history"
PORTFOLIO_PATH = "data/portfolio_g.json"
os.makedirs("data", exist_ok=True)

TP_PCT = 15
SL_PCT = 3
MAX_HOLD_TRADING_DAYS = 2
GAP_FILTER_PCT = 1.0
PER_POSITION_USD = 500
STARTING_CAPITAL = 2000
MAX_CONCURRENT = 4  # 同时最多持仓笔数

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

def count_concurrent(all_positions, signal_date):
    """统计 signal_date 当天已有多少笔仓位处于持仓中"""
    count = 0
    for pos in all_positions:
        entry = pos["signal_date"]
        close = pos.get("close_date") or pos.get("max_hold_date", "9999-99-99")
        if entry <= signal_date <= close:
            count += 1
    return count

def simulate_position(ticker, action, entry_price, signal_date):
    tp_price = round(entry_price * (1 + TP_PCT/100 if action=="BUY" else 1 - TP_PCT/100), 2)
    sl_price = round(entry_price * (1 - SL_PCT/100 if action=="BUY" else 1 + SL_PCT/100), 2)

    target_dates = next_n_trading_days(signal_date, MAX_HOLD_TRADING_DAYS)
    fetch_end = (datetime.strptime(target_dates[-1], "%Y-%m-%d") + timedelta(days=2)).strftime("%Y-%m-%d")

    try:
        df = yf.Ticker(ticker).history(start=signal_date, end=fetch_end)
        df.index = df.index.tz_localize(None) if df.index.tz else df.index
    except Exception as e:
        print(f"  [warn] yfinance failed for {ticker}: {e}")
        return None, None, "open", None, {}, False

    daily_prices = {}
    today_str = datetime.now().strftime("%Y-%m-%d")

    for i, target_date in enumerate(target_dates):
        row = None
        for idx, r in df.iterrows():
            if idx.strftime("%Y-%m-%d") == target_date:
                row = r
                break

        if row is None:
            if target_date > today_str:
                return None, None, "open", None, daily_prices, False
            continue

        try:
            o  = round(float(row["Open"]),  2)
            hi = round(float(row["High"]),  2)
            lo = round(float(row["Low"]),   2)
            cl = round(float(row["Close"]), 2)
            if any(v != v for v in [o, hi, lo, cl]):  # NaN check
                if target_date > today_str:
                    return None, None, "open", None, daily_prices, False
                continue
        except (ValueError, TypeError):
            continue

        if i == 0 and GAP_FILTER_PCT > 0:
            gap = (o - entry_price) / entry_price * 100
            unfavorable = -gap if action == "BUY" else gap
            if unfavorable > GAP_FILTER_PCT:
                return None, None, "gap_filtered", None, {}, True

        close_reason = None
        close_price  = cl
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
            return target_date, close_price, close_reason, round(pnl_pct, 2), daily_prices, False

        if target_date == target_dates[-1]:
            raw_pct = (cl - entry_price) / entry_price * 100
            pnl_pct = raw_pct if action == "BUY" else -raw_pct
            daily_prices[target_date]["pnl_pct"] = round(pnl_pct, 2)
            return target_date, cl, "max_hold", round(pnl_pct, 2), daily_prices, False

    return None, None, "open", None, daily_prices, False


portfolio = {
    "capital_usd": STARTING_CAPITAL,
    "open_positions": [],
    "closed_positions": [],
    "_note": "Plan G：与D参数相同，新增最多4笔并发限制 / IBKR佣金$0.005/股min$1"
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

print(f"Found {len(all_signals)} signals")

skipped_gap = 0
skipped_zero_shares = 0
skipped_concurrent = 0

# 所有已处理仓位（用于并发统计）
all_processed = []

for signal_date, s in all_signals:
    ticker = s.get("ticker")
    action = s.get("action")
    entry_price = s.get("current_price")
    if action not in ("BUY", "SELL") or not entry_price:
        continue

    shares = int(PER_POSITION_USD / entry_price)
    if shares == 0:
        print(f"  Skip {signal_date} {ticker} @ ${entry_price} (too expensive)")
        skipped_zero_shares += 1
        continue

    # 并发上限检查
    concurrent = count_concurrent(all_processed, signal_date)
    if concurrent >= MAX_CONCURRENT:
        print(f"  Skip {signal_date} {ticker} → 并发上限 ({concurrent}/{MAX_CONCURRENT}笔已开仓)")
        skipped_concurrent += 1
        continue

    actual_position_usd = round(shares * entry_price, 2)
    entry_comm = ibkr_commission(shares)
    exit_comm = ibkr_commission(shares)

    tp = round(entry_price * (1 + TP_PCT/100 if action == "BUY" else 1 - TP_PCT/100), 2)
    sl = round(entry_price * (1 - SL_PCT/100 if action == "BUY" else 1 + SL_PCT/100), 2)

    print(f"  {action} {ticker} @ ${entry_price} x{shares}sh [{signal_date}] 并发:{concurrent+1}/{MAX_CONCURRENT}...")

    close_date, close_price, close_reason, final_pnl_pct, daily_prices, gap_filt = simulate_position(
        ticker, action, entry_price, signal_date
    )

    if gap_filt:
        print(f"    → Gap filtered (unfavorable >{GAP_FILTER_PCT}%)")
        skipped_gap += 1
        continue

    max_dates = next_n_trading_days(signal_date, MAX_HOLD_TRADING_DAYS)
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
        "max_hold_date": max_dates[-1],
        "daily_prices": daily_prices,
    }

    if close_reason == "open":
        portfolio["open_positions"].append(position)
        all_processed.append({**position, "close_date": None})
        print(f"    → Still OPEN")
    elif close_date:
        gross_pnl = round(actual_position_usd * final_pnl_pct / 100, 2)
        realized_pnl = round(gross_pnl - entry_comm - exit_comm, 2)
        closed = {**position,
                  "close_date": close_date, "close_price": close_price,
                  "final_pnl_pct": final_pnl_pct, "close_reason": close_reason,
                  "exit_commission": exit_comm,
                  "commission_total": round(entry_comm + exit_comm, 2),
                  "realized_pnl_usd": realized_pnl}
        portfolio["closed_positions"].append(closed)
        all_processed.append(closed)
        print(f"    → {close_reason} @ ${close_price} {final_pnl_pct:+.2f}% gross=${gross_pnl:+.2f} comm=-${entry_comm+exit_comm:.2f} net=${realized_pnl:+.2f}")

all_closed = portfolio["closed_positions"]
wins = [p for p in all_closed if p.get("realized_pnl_usd", 0) > 0]
total_realized = sum(p.get("realized_pnl_usd", 0) for p in all_closed)
total_commission = sum(p.get("commission_total", 0) for p in all_closed)
open_unrealized = 0
for p in portfolio["open_positions"]:
    dp = p.get("daily_prices", {})
    if not dp:
        continue
    raw_pct = list(dp.values())[-1].get("pnl_pct", 0)
    try:
        pct = float(raw_pct) if raw_pct is not None else 0.0
        if pct != pct:
            pct = 0.0
    except (TypeError, ValueError):
        pct = 0.0
    open_unrealized += p["actual_position_usd"] * pct / 100 - p["entry_commission"]

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
    "skipped_concurrent": skipped_concurrent,
    "updated_at": datetime.now().strftime("%Y-%m-%d"),
}

with open(PORTFOLIO_PATH, "w") as f:
    json.dump(portfolio, f, ensure_ascii=False, indent=2)

js_content = f"window.PORTFOLIO_G = {json.dumps(portfolio, indent=2, ensure_ascii=False)};\n"
with open("dashboard/portfolio-g.js", "w") as f:
    f.write(js_content)

s = portfolio["stats"]
print(f"\n{'='*60}")
print(f"  Plan G 并发限制回测结果")
print(f"{'='*60}")
print(f"  参数：TP+{TP_PCT}% / SL-{SL_PCT}% / {MAX_HOLD_TRADING_DAYS}日 / 跳空>{GAP_FILTER_PCT}%过滤 / 并发≤{MAX_CONCURRENT}")
print(f"  起始本金: ${STARTING_CAPITAL}")
print(f"  总交易:   {s['total_trades']} 笔  胜率: {s['win_rate']}%")
print(f"  跳过:     跳空{s['skipped_gap']} / 并发{s['skipped_concurrent']} / 价格{s['skipped_zero_shares']}")
print(f"  已实现:   ${s['total_realized_pnl_usd']:+.2f}  (佣金 -${s['total_commission_usd']:.2f})")
print(f"  浮盈:     ${s['open_unrealized_pnl_usd']:+.2f}")
print(f"  组合价值: ${s['portfolio_value']}")
print()
print("  已平仓明细:")
for p in all_closed:
    print(f"    {p['action']:4} {p['ticker']:6} {p['signal_date']} → {p['close_date']} "
          f"({p['close_reason']:12}) {p['final_pnl_pct']:+.2f}% / ${p['realized_pnl_usd']:+.2f}")
print(f"\nSaved to {PORTFOLIO_PATH} and dashboard/portfolio-g.js")
