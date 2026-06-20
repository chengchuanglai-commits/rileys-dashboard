"""
Plan H-广池(MN) 模拟盘 — 信号源=每日晨报精选(中大盘,流动好/数据全)，出场规则=Plan H(TP15/SL2/2日/gap1.0)。

设计：与 Plan H / H-DS 控制变量对照——三盘出场规则完全一致，只差「信号来源」：
  H      = 小盘(S&P600) Haiku 信号
  H-DS   = 小盘(S&P600) DeepSeek 信号
  H-广池 = 中大盘(晨报精选) AI 信号   ← 本盘
用来验证「广池+数据好」的票是否比小盘信号更赚(Riley 2026-06-15 决策:换筛选维度,不赌板块)。

入场价取 buy_zone 区间中点(晨报是 pre-market 推荐,视为当日入场,模拟其后2交易日)。
佣金：IBKR $0.005/股，最低 $1.00/单。
"""
import json, os, re, glob
from datetime import datetime, timedelta
import yfinance as yf
from portfolio_compound import compound_portfolio   # frac10 复利回填(与决策视图排名同口径)

MN_DIR = "dashboard/morning-note-history"
PORTFOLIO_PATH = "data/portfolio_mn.json"
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


def simulate_position(ticker, action, signal_date):
    """入场价=晨报当日(signal_date)的真实收盘价(市价入场,与H/H-DS一致)，不用AI的限价区间(否则假成交)。"""
    target_dates = next_n_trading_days(signal_date, MAX_HOLD_TRADING_DAYS)
    fetch_end = (datetime.strptime(target_dates[-1], "%Y-%m-%d") + timedelta(days=2)).strftime("%Y-%m-%d")

    try:
        df = yf.Ticker(ticker).history(start=signal_date, end=fetch_end)
        df.index = df.index.tz_localize(None) if getattr(df.index, "tz", None) else df.index
    except Exception as e:
        print(f"  [warn] yfinance failed for {ticker}: {e}")
        return None, None, None, "open", None, {}, False

    # 入场价 = signal_date 当天(或之后第一根)的真实收盘
    entry_price = None
    for idx, r in df.iterrows():
        if idx.strftime("%Y-%m-%d") >= signal_date:
            c = float(r["Close"])
            if c == c:  # 非NaN
                entry_price = round(c, 2)
                break
    if not entry_price:
        return None, None, None, "open", None, {}, False

    tp_price = round(entry_price * (1 + TP_PCT/100 if action == "BUY" else 1 - TP_PCT/100), 2)
    sl_price = round(entry_price * (1 - SL_PCT/100 if action == "BUY" else 1 + SL_PCT/100), 2)

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
                return entry_price, None, None, "open", None, daily_prices, False
            continue

        o  = round(float(row["Open"]),  2)
        hi = round(float(row["High"]),  2)
        lo = round(float(row["Low"]),   2)
        cl = round(float(row["Close"]), 2)

        if any(x != x for x in (o, hi, lo, cl)):
            continue

        if i == 0 and GAP_FILTER_PCT > 0:
            gap = (o - entry_price) / entry_price * 100
            unfavorable = -gap if action == "BUY" else gap
            if unfavorable > GAP_FILTER_PCT:
                return entry_price, None, None, "gap_filtered", None, {}, True

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
            return entry_price, target_date, close_price, close_reason, round(pnl_pct, 2), daily_prices, False

        if target_date == target_dates[-1]:
            raw_pct = (cl - entry_price) / entry_price * 100
            pnl_pct = raw_pct if action == "BUY" else -raw_pct
            daily_prices[target_date]["pnl_pct"] = round(pnl_pct, 2)
            return entry_price, target_date, cl, "max_hold", round(pnl_pct, 2), daily_prices, False

    return entry_price, None, None, "open", None, daily_prices, False


portfolio = {
    "capital_usd": STARTING_CAPITAL,
    "open_positions": [],
    "closed_positions": [],
    "_note": "Plan H-广池 模拟盘：信号源=晨报中大盘精选，出场=H规则(TP+15%/SL-2%/2交易日/跳空>1%过滤)。与 H/H-DS 控制变量对照(只差信号来源)。"
}

# 读所有晨报历史的 buy 精选 → (date, ticker)
all_signals = []
for path in sorted(glob.glob(os.path.join(MN_DIR, "*.json"))):
    date_str = os.path.basename(path).replace(".json", "")
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    for p in d.get("stock_picks", []):
        if p.get("direction") != "buy" or not p.get("ticker"):
            continue
        all_signals.append((date_str, {"ticker": p["ticker"], "name": p.get("name", ""), "action": "BUY"}))

print(f"Found {len(all_signals)} 晨报 buy 信号")

skipped_gap = 0
skipped_zero_shares = 0
for signal_date, s in all_signals:
    ticker = s.get("ticker")
    action = s.get("action")

    # 入场价由 simulate 从真实市场数据取(signal_date 收盘)，不用 AI 限价区间
    entry_price, close_date, close_price, close_reason, final_pnl_pct, daily_prices, gap_filt = simulate_position(
        ticker, action, signal_date
    )
    if not entry_price:
        print(f"  Skip {signal_date} {ticker} (无市场数据)")
        continue

    if gap_filt:
        print(f"    → {ticker} Gap filtered (unfavorable >{GAP_FILTER_PCT}%)")
        skipped_gap += 1
        continue

    shares = round(PER_POSITION_USD / entry_price, 4)   # 小数股:不再因股价高丢票(与MOM腿/H系列统一,对比纯净)
    actual_position_usd = round(shares * entry_price, 2)
    entry_comm = ibkr_commission(shares)
    exit_comm = ibkr_commission(shares)
    print(f"  {action} {ticker} @ ${entry_price} x{shares}sh [{signal_date}] → {close_reason}")

    tp = round(entry_price * (1 + TP_PCT/100), 2)
    sl = round(entry_price * (1 - SL_PCT/100), 2)

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
        print(f"    → Closed {close_reason} @ ${close_price} {final_pnl_pct:+.2f}% net=${realized_pnl:+.2f}")

# frac10 复利回填:每仓=当前净值20%,复利,最多5并发(取代固定$500,与决策视图排名同口径)
def _open_pct(p):
    dp = p.get("daily_prices") or {}
    return list(dp.values())[-1]["pnl_pct"] if dp else 0.0
fc, fo, _pv, total_realized, open_unrealized, skipped_no_cash = compound_portfolio(
    portfolio["closed_positions"], portfolio["open_positions"], _open_pct, STARTING_CAPITAL)
portfolio["closed_positions"] = fc
portfolio["open_positions"] = fo

all_closed = portfolio["closed_positions"]
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
    "skipped_no_cash": skipped_no_cash,
    "updated_at": datetime.now().strftime("%Y-%m-%d"),
}

with open(PORTFOLIO_PATH, "w") as f:
    json.dump(portfolio, f, ensure_ascii=False, indent=2)

with open("dashboard/portfolio-mn.js", "w", encoding="utf-8") as f:
    f.write("// Plan H-广池 模拟盘持仓 — 晨报中大盘精选 + H出场规则\n")
    f.write(f"window.PORTFOLIO_MN = {json.dumps(portfolio, ensure_ascii=False, indent=2)};\n")

s = portfolio["stats"]
print(f"\n{'='*55}")
print(f"  💼 Plan H-广池 模拟盘（晨报精选 + H规则）")
print(f"{'='*55}")
print(f"  总交易: {s['total_trades']} 笔  胜率: {s['win_rate']}%  跳空过滤: {s['skipped_gap']} 笔")
print(f"  已实现: ${s['total_realized_pnl_usd']:+.2f}  浮盈: ${s['open_unrealized_pnl_usd']:+.2f}")
print(f"  组合价值: ${s['portfolio_value']}")
