"""
Plan B 历史回溯模拟
从所有已验证信号重建 portfolio_b.json，用于 A vs B 对比分析。

入场规则：信号价（prev close） + BUY/SELL 方向
出场规则：TP +8%、SL -4%、最大持仓 5 交易日（用 yfinance 日线 high/low 判断触达）
"""
import json, os, sys
from datetime import datetime, timedelta
import yfinance as yf

SIGNALS_DIR = "dashboard/trading-signals-history"
PORTFOLIO_PATH = "data/portfolio_b.json"
os.makedirs("data", exist_ok=True)

TP_PCT = 8   # take profit %
SL_PCT = 4   # stop loss %
MAX_HOLD_TRADING_DAYS = 5
PER_POSITION_USD = 500
STARTING_CAPITAL = 2000

# ── 工具函数 ────────────────────────────────────────────────────

def next_n_trading_days(start_str, n):
    dt = datetime.strptime(start_str, "%Y-%m-%d")
    days = []
    while len(days) < n:
        dt += timedelta(days=1)
        if dt.weekday() < 5:
            days.append(dt.strftime("%Y-%m-%d"))
    return days

def simulate_position(ticker, action, entry_price, signal_date):
    """
    从 signal_date 后的 MAX_HOLD_TRADING_DAYS 个交易日模拟持仓。
    使用 yfinance 日线 Open/High/Low/Close 判断 TP/SL/到期。
    返回: (close_date, close_price, close_reason, pnl_pct, daily_prices_dict)
    """
    tp_price = round(entry_price * (1 + TP_PCT / 100 if action == "BUY" else 1 - TP_PCT / 100), 2)
    sl_price = round(entry_price * (1 - SL_PCT / 100 if action == "BUY" else 1 + SL_PCT / 100), 2)

    target_dates = next_n_trading_days(signal_date, MAX_HOLD_TRADING_DAYS)
    fetch_end = (datetime.strptime(target_dates[-1], "%Y-%m-%d") + timedelta(days=2)).strftime("%Y-%m-%d")

    try:
        df = yf.Ticker(ticker).history(start=signal_date, end=fetch_end)
        df.index = df.index.tz_localize(None) if df.index.tz is not None else df.index
    except Exception as e:
        print(f"  [warn] yfinance failed for {ticker}: {e}")
        return None, None, None, None, {}

    daily_prices = {}
    today_str = datetime.now().strftime("%Y-%m-%d")

    for target_date in target_dates:
        # Find the matching row (yfinance index is datetime)
        row = None
        for idx, r in df.iterrows():
            if idx.strftime("%Y-%m-%d") == target_date:
                row = r
                break

        if row is None:
            if target_date > today_str:
                # Future date — still open
                return None, None, "open", None, daily_prices
            # Missing trading day (holiday): skip
            continue

        o  = round(float(row["Open"]),  2)
        hi = round(float(row["High"]),  2)
        lo = round(float(row["Low"]),   2)
        cl = round(float(row["Close"]), 2)

        # Intraday TP/SL check (conservative: use close if hit, else close)
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
            return target_date, close_price, close_reason, round(pnl_pct, 2), daily_prices

        # Last day = max hold exit at close
        if target_date == target_dates[-1]:
            raw_pct = (cl - entry_price) / entry_price * 100
            pnl_pct = raw_pct if action == "BUY" else -raw_pct
            daily_prices[target_date]["pnl_pct"] = round(pnl_pct, 2)
            return target_date, cl, "max_hold", round(pnl_pct, 2), daily_prices

    return None, None, "open", None, daily_prices

# ── 读取所有历史信号 ──────────────────────────────────────────────

portfolio = {
    "capital_usd": STARTING_CAPITAL,
    "open_positions": [],
    "closed_positions": [],
    "_note": "Plan B 模拟盘：TP +8% / SL -4% / 最大5交易日"
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

open_tickers = set()
for signal_date, s in all_signals:
    ticker = s.get("ticker")
    action = s.get("action")
    entry_price = s.get("current_price")

    if action not in ("BUY", "SELL") or not entry_price:
        print(f"  Skip {signal_date} {ticker} {action} (HOLD or no price)")
        continue

    print(f"  Simulating {action} {ticker} @ ${entry_price} [{signal_date}]...")
    close_date, close_price, close_reason, final_pnl_pct, daily_prices = simulate_position(
        ticker, action, entry_price, signal_date
    )

    if action == "BUY":
        tp = round(entry_price * (1 + TP_PCT / 100), 2)
        sl = round(entry_price * (1 - SL_PCT / 100), 2)
    else:
        tp = round(entry_price * (1 - TP_PCT / 100), 2)
        sl = round(entry_price * (1 + SL_PCT / 100), 2)

    # Calculate max_hold_date
    max_dates = next_n_trading_days(signal_date, MAX_HOLD_TRADING_DAYS)
    max_hold_date = max_dates[-1]

    position = {
        "ticker": ticker,
        "name": s.get("name", ""),
        "action": action,
        "signal_date": signal_date,
        "entry_price": entry_price,
        "allocated_usd": PER_POSITION_USD,
        "take_profit": tp,
        "stop_loss": sl,
        "max_hold_date": max_hold_date,
        "daily_prices": daily_prices,
    }

    if close_reason == "open":
        portfolio["open_positions"].append(position)
        print(f"    → Still OPEN (latest pnl: {list(daily_prices.values())[-1]['pnl_pct'] if daily_prices else 'N/A'}%)")
    elif close_date:
        realized_pnl = round(PER_POSITION_USD * final_pnl_pct / 100, 2)
        closed = {**position, "close_date": close_date, "close_price": close_price,
                  "final_pnl_pct": final_pnl_pct, "close_reason": close_reason,
                  "realized_pnl_usd": realized_pnl}
        portfolio["closed_positions"].append(closed)
        print(f"    → Closed {close_reason} @ ${close_price} {final_pnl_pct:+.2f}% / ${realized_pnl:+.2f}")
    else:
        print(f"    → No data available, skipping")

# ── 计算统计 ─────────────────────────────────────────────────────

all_closed = portfolio["closed_positions"]
wins = [p for p in all_closed if p.get("final_pnl_pct", 0) > 0]
total_realized = sum(p.get("realized_pnl_usd", 0) for p in all_closed)
open_unrealized = sum(
    p["allocated_usd"] * list(p["daily_prices"].values())[-1]["pnl_pct"] / 100
    for p in portfolio["open_positions"] if p["daily_prices"]
)

portfolio["stats"] = {
    "total_trades": len(all_closed),
    "win_trades": len(wins),
    "win_rate": round(len(wins) / len(all_closed) * 100, 1) if all_closed else 0,
    "total_realized_pnl_usd": round(total_realized, 2),
    "open_unrealized_pnl_usd": round(open_unrealized, 2),
    "portfolio_value": round(STARTING_CAPITAL + total_realized + open_unrealized, 2),
    "updated_at": datetime.now().strftime("%Y-%m-%d"),
}

# ── 保存 ──────────────────────────────────────────────────────────

with open(PORTFOLIO_PATH, "w") as f:
    json.dump(portfolio, f, ensure_ascii=False, indent=2)

# Generate JS
with open("dashboard/portfolio-b.js", "w", encoding="utf-8") as f:
    f.write("// Plan B 模拟盘持仓 — 历史回溯 + 实时更新\n")
    f.write(f"window.PORTFOLIO_B = {json.dumps(portfolio, ensure_ascii=False, indent=2)};\n")

s = portfolio["stats"]
print(f"\n{'='*55}")
print(f"  💼 Plan B 模拟盘回溯结果")
print(f"{'='*55}")
print(f"  起始本金: ${STARTING_CAPITAL}")
print(f"  总交易:   {s['total_trades']} 笔  胜率: {s['win_rate']}%")
print(f"  已实现:   ${s['total_realized_pnl_usd']:+.2f}")
print(f"  浮盈:     ${s['open_unrealized_pnl_usd']:+.2f}")
print(f"  组合价值: ${s['portfolio_value']}")
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
        print(f"    {p['action']:4} {p['ticker']:6} {p['signal_date']} (到期 {p['max_hold_date']}) "
              f"浮盈 {latest.get('pnl_pct', 0):+.2f}%")
