"""
Plan H-DS 历史回溯模拟 — 历史回测最优参数（TP15/SL2/2日/gap1.0）
来源：historical-backtest.py 在 12 个月 ~1620 笔随机入场上，此参数组 PF 最高(~2.18)。
与 Plan D 唯一差别：止损 SL 从 -3% 收紧到 -2%（D vs H 是控制变量对照）。
佣金：IBKR $0.005/股，最低 $1.00/单（入场+出场各一次）
"""
import json, os
from datetime import datetime, timedelta
import yfinance as yf

SIGNALS_DIR = "dashboard/trading-signals-history"
PORTFOLIO_PATH = "data/portfolio_hds.json"
os.makedirs("data", exist_ok=True)

TP_PCT = 15
SL_PCT = 2
MAX_HOLD_TRADING_DAYS = 2
GAP_FILTER_PCT = 1.0
PER_POSITION_USD = 500
STARTING_CAPITAL = 2000

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
    tp_price = round(entry_price * (1 + TP_PCT/100 if action=="BUY" else 1 - TP_PCT/100), 2)
    sl_price = round(entry_price * (1 - SL_PCT/100 if action=="BUY" else 1 + SL_PCT/100), 2)

    target_dates = next_n_trading_days(signal_date, MAX_HOLD_TRADING_DAYS)
    fetch_end = (datetime.strptime(target_dates[-1], "%Y-%m-%d") + timedelta(days=2)).strftime("%Y-%m-%d")

    try:
        df = yf.Ticker(ticker).history(start=signal_date, end=fetch_end)
        df.index = df.index.tz_localize(None) if df.index.tz else df.index
    except Exception as e:
        print(f"  [warn] yfinance failed for {ticker}: {e}")
        return None, None, None, None, {}, False

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

        o  = round(float(row["Open"]),  2)
        hi = round(float(row["High"]),  2)
        lo = round(float(row["Low"]),   2)
        cl = round(float(row["Close"]), 2)

        # 跳过 yfinance NaN bar（OTC 股数据延迟时会出现，否则污染组合净值）
        if any(x != x for x in (o, hi, lo, cl)):
            continue

        # Day-1 gap filter
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
    "_note": "H-DS 模拟盘：DeepSeek(R1) 信号 + H 出场规则(TP15/SL2/2日/gap1.0)。与 Plan H(Haiku信号+同规则)头对头比模型。仅A/B对比,不是真实交易方案。"
}

# H-DS 用 DeepSeek 影子信号（{date}-deepseek.json），出场规则同 Plan H
all_signals = []
for fname in sorted(os.listdir(SIGNALS_DIR)):
    if not fname.endswith("-deepseek.json"):
        continue
    date_str = fname.replace("-deepseek.json", "")
    with open(os.path.join(SIGNALS_DIR, fname)) as f:
        d = json.load(f)
    for s in d.get("signals", []):
        all_signals.append((date_str, s))

print(f"Found {len(all_signals)} DeepSeek signals")

skipped_gap = 0
skipped_zero_shares = 0
for signal_date, s in all_signals:
    ticker = s.get("ticker")
    action = s.get("action")
    entry_price = s.get("current_price")
    if action not in ("BUY", "SELL") or not entry_price:
        print(f"  Skip {signal_date} {ticker} {action}")
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
    close_date, close_price, close_reason, final_pnl_pct, daily_prices, gap_filt = simulate_position(
        ticker, action, entry_price, signal_date
    )

    if gap_filt:
        print(f"    → Gap filtered (unfavorable >{GAP_FILTER_PCT}%)")
        skipped_gap += 1
        continue

    if action == "BUY":
        tp = round(entry_price * (1 + TP_PCT/100), 2)
        sl = round(entry_price * (1 - SL_PCT/100), 2)
    else:
        tp = round(entry_price * (1 - TP_PCT/100), 2)
        sl = round(entry_price * (1 + SL_PCT/100), 2)

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
        latest = list(daily_prices.values())[-1] if daily_prices else {}
        print(f"    → Still OPEN (latest pnl: {latest.get('pnl_pct', 'N/A')}%)")
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

all_closed = portfolio["closed_positions"]
wins = [p for p in all_closed if p.get("realized_pnl_usd", 0) > 0]
total_realized = sum(p.get("realized_pnl_usd", 0) for p in all_closed)
total_commission = sum(p.get("commission_total", 0) for p in all_closed)
open_unrealized = sum(
    p["actual_position_usd"] * list(p["daily_prices"].values())[-1]["pnl_pct"] / 100 - p["entry_commission"]
    for p in portfolio["open_positions"] if p["daily_prices"]
)

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

with open(PORTFOLIO_PATH, "w") as f:
    json.dump(portfolio, f, ensure_ascii=False, indent=2)

with open("dashboard/portfolio-hds.js", "w", encoding="utf-8") as f:
    f.write("// Plan H-DS 模拟盘持仓 — 历史最优参数(TP15/SL2/2日) 回溯 + 实时更新\n")
    f.write(f"window.PORTFOLIO_HDSDS = {json.dumps(portfolio, ensure_ascii=False, indent=2)};\n")

s = portfolio["stats"]
print(f"\n{'='*55}")
print(f"  💼 Plan H-DS 模拟盘回溯结果（历史最优参数）")
print(f"{'='*55}")
print(f"  参数：TP+{TP_PCT}% / SL-{SL_PCT}% / {MAX_HOLD_TRADING_DAYS}日 / 跳空>{GAP_FILTER_PCT}%过滤")
print(f"  起始本金: ${STARTING_CAPITAL}")
print(f"  总交易:   {s['total_trades']} 笔  胜率: {s['win_rate']}%  跳过: {s['skipped_gap']} 笔")
print(f"  已实现:   ${s['total_realized_pnl_usd']:+.2f}  (佣金 -${s['total_commission_usd']:.2f})")
print(f"  浮盈:     ${s['open_unrealized_pnl_usd']:+.2f}")
print(f"  组合价值: ${s['portfolio_value']}")
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
