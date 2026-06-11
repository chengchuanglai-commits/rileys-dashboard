"""
Plan F — 分档出场策略
基于 Plan D 参数（TP+15% / SL-3% / 1%跳空过滤），最大持仓延长至 3 天。
每笔交易拆成 2 档出场：
  第1档（50%股数）→ TP1 = 入场到原始TP的中点
  第2档（50%股数）→ TP2 = 原始TP（+15%）
止损：固定，两档共用，全部止损。
佣金：IBKR $0.005/股 最低$1.00/单
"""
import json, os
from datetime import datetime, timedelta
import yfinance as yf

SIGNALS_DIR = "dashboard/trading-signals-history"
PORTFOLIO_PATH = "data/portfolio_f.json"
os.makedirs("data", exist_ok=True)

TP_PCT = 15
SL_PCT = 3
MAX_HOLD_TRADING_DAYS = 3
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


def simulate_position_f(ticker, action, entry_price, shares, signal_date):
    """
    2 档出场模拟。
    Returns dict:
      status: 'gap_filtered' | 'open' | 'closed' | 'error'
      day1_open: float | None
      t1_exit: (date, price, reason) | None   -- 第1档出场
      t2_exit: (date, price, reason) | None   -- 第2档出场
      sl_unified: bool  -- True 表示止损在 T1 未平前触发，一次性平掉全部
      daily_prices: {date: {open, high, low, close, pnl_pct}}
    """
    tp2_price = round(entry_price * (1 + TP_PCT/100 if action == "BUY" else 1 - TP_PCT/100), 2)
    tp1_price = round(entry_price + (tp2_price - entry_price) * 0.5, 2)
    sl_price  = round(entry_price * (1 - SL_PCT/100 if action == "BUY" else 1 + SL_PCT/100), 2)

    target_dates = next_n_trading_days(signal_date, MAX_HOLD_TRADING_DAYS)
    fetch_end = (datetime.strptime(target_dates[-1], "%Y-%m-%d") + timedelta(days=2)).strftime("%Y-%m-%d")

    try:
        df = yf.Ticker(ticker).history(start=signal_date, end=fetch_end)
        df.index = df.index.tz_localize(None) if df.index.tz else df.index
    except Exception as e:
        print(f"  [warn] yfinance failed for {ticker}: {e}")
        return {"status": "error", "daily_prices": {}, "day1_open": None,
                "t1_exit": None, "t2_exit": None, "sl_unified": False}

    daily_prices = {}
    today_str = datetime.now().strftime("%Y-%m-%d")
    t1_exit = None
    t2_exit = None
    sl_unified = False
    day1_open = None

    for i, target_date in enumerate(target_dates):
        row = None
        for idx, r in df.iterrows():
            if idx.strftime("%Y-%m-%d") == target_date:
                row = r
                break

        if row is None:
            if target_date > today_str:
                return {"status": "open", "day1_open": day1_open,
                        "t1_exit": t1_exit, "t2_exit": t2_exit,
                        "sl_unified": sl_unified, "daily_prices": daily_prices}
            continue

        o  = round(float(row["Open"]),  2)
        hi = round(float(row["High"]),  2)
        lo = round(float(row["Low"]),   2)
        cl = round(float(row["Close"]), 2)
        if any(v != v for v in (o, hi, lo, cl)):  # 跳过 yfinance NaN bar(OTC延迟)，否则污染净值
            continue

        if i == 0:
            day1_open = o
            if GAP_FILTER_PCT > 0:
                gap = (o - entry_price) / entry_price * 100
                unfavorable = -gap if action == "BUY" else gap
                if unfavorable > GAP_FILTER_PCT:
                    return {"status": "gap_filtered", "day1_open": o,
                            "daily_prices": {}, "t1_exit": None, "t2_exit": None, "sl_unified": False}

        raw_pct = (cl - entry_price) / entry_price * 100
        pnl_pct = raw_pct if action == "BUY" else -raw_pct
        daily_prices[target_date] = {"open": o, "high": hi, "low": lo, "close": cl, "pnl_pct": round(pnl_pct, 2)}

        if action == "BUY":
            sl_hit = lo <= sl_price
            t1_hit = hi >= tp1_price
            t2_hit = hi >= tp2_price
        else:
            sl_hit = hi >= sl_price
            t1_hit = lo <= tp1_price
            t2_hit = lo <= tp2_price

        # 1. 止损优先：关闭所有剩余仓位
        if sl_hit:
            if t1_exit is None:
                sl_unified = True
                t1_exit = (target_date, sl_price, "stop_loss")
                t2_exit = (target_date, sl_price, "stop_loss")
            else:
                t2_exit = (target_date, sl_price, "stop_loss")
            break

        # 2. 第1档止盈（T1 未平时）
        if t1_hit and t1_exit is None:
            t1_exit = (target_date, tp1_price, "take_profit_1")

        # 3. 第2档止盈（T1 已平后）
        if t2_hit and t1_exit is not None and t2_exit is None:
            t2_exit = (target_date, tp2_price, "take_profit_2")
            break

        # 4. 最后一天：关闭剩余仓位
        if target_date == target_dates[-1]:
            if t1_exit is None:
                t1_exit = (target_date, cl, "max_hold")
            if t2_exit is None:
                t2_exit = (target_date, cl, "max_hold")
            break

    if t1_exit is None or t2_exit is None:
        return {"status": "open", "day1_open": day1_open,
                "t1_exit": t1_exit, "t2_exit": t2_exit,
                "sl_unified": sl_unified, "daily_prices": daily_prices}

    return {"status": "closed", "day1_open": day1_open,
            "t1_exit": t1_exit, "t2_exit": t2_exit,
            "sl_unified": sl_unified, "daily_prices": daily_prices}


# ── 读取所有历史信号 ──────────────────────────────────────────────

portfolio = {
    "capital_usd": STARTING_CAPITAL,
    "open_positions": [],
    "closed_positions": [],
    "_note": "Plan F 分档出场：TP+15%/2档/SL-3%/3日/1%跳空过滤 / IBKR佣金$0.005/股min$1"
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

for signal_date, s in all_signals:
    ticker = s.get("ticker")
    action = s.get("action")
    entry_price = s.get("current_price")
    if action not in ("BUY", "SELL") or not entry_price:
        continue

    shares = int(PER_POSITION_USD / entry_price)
    if shares < 2:
        print(f"  Skip {signal_date} {ticker} @ ${entry_price} (<2 shares, can't split)")
        skipped_zero_shares += 1
        continue

    t1_shares = shares // 2
    t2_shares = shares - t1_shares
    actual_position_usd = round(shares * entry_price, 2)
    entry_comm = ibkr_commission(shares)

    tp2_price = round(entry_price * (1 + TP_PCT/100 if action == "BUY" else 1 - TP_PCT/100), 2)
    tp1_price = round(entry_price + (tp2_price - entry_price) * 0.5, 2)
    sl_price  = round(entry_price * (1 - SL_PCT/100 if action == "BUY" else 1 + SL_PCT/100), 2)

    print(f"  {action} {ticker} @ ${entry_price} x{shares}sh (T1:{t1_shares} T2:{t2_shares}) "
          f"TP1${tp1_price} TP2${tp2_price} SL${sl_price} [{signal_date}]")

    result = simulate_position_f(ticker, action, entry_price, shares, signal_date)

    if result["status"] == "gap_filtered":
        print(f"    → Gap filtered (unfavorable >{GAP_FILTER_PCT}%)")
        skipped_gap += 1
        continue

    if result["status"] == "error":
        print(f"    → Error fetching data, skipping")
        continue

    t1_exit = result["t1_exit"]
    t2_exit = result["t2_exit"]
    sl_unified = result["sl_unified"]

    max_dates = next_n_trading_days(signal_date, MAX_HOLD_TRADING_DAYS)

    pos = {
        "ticker": ticker,
        "name": s.get("name", ticker),
        "action": action,
        "signal_date": signal_date,
        "entry_price": entry_price,
        "allocated_usd": PER_POSITION_USD,
        "shares": shares,
        "t1_shares": t1_shares,
        "t2_shares": t2_shares,
        "actual_position_usd": actual_position_usd,
        "entry_commission": entry_comm,
        "take_profit_1": tp1_price,
        "take_profit_2": tp2_price,
        "stop_loss": sl_price,
        "max_hold_date": max_dates[-1],
        "day1_open": result["day1_open"],
        "daily_prices": result["daily_prices"],
    }

    if result["status"] == "open":
        if t1_exit is not None:
            # T1 已平，T2 仍持仓
            t1_d, t1_p, t1_r = t1_exit
            t1_gross = round(t1_shares * (t1_p - entry_price if action == "BUY" else entry_price - t1_p), 2)
            t1_comm_val = ibkr_commission(t1_shares)
            pos["t1_exit_date"]   = t1_d
            pos["t1_exit_price"]  = t1_p
            pos["t1_exit_reason"] = t1_r
            pos["t1_locked_pnl"]  = round(t1_gross - entry_comm - t1_comm_val, 2)
        portfolio["open_positions"].append(pos)
        print(f"    → Still OPEN (T1: {'done' if t1_exit else 'pending'})")
    else:
        # Both tranches closed
        t1_d, t1_p, t1_r = t1_exit
        t2_d, t2_p, t2_r = t2_exit

        if action == "BUY":
            t1_gross = round(t1_shares * (t1_p - entry_price), 2)
            t2_gross = round(t2_shares * (t2_p - entry_price), 2)
        else:
            t1_gross = round(t1_shares * (entry_price - t1_p), 2)
            t2_gross = round(t2_shares * (entry_price - t2_p), 2)

        if sl_unified:
            # 止损一次性平掉所有股数：入场佣金 + 一次出场佣金
            exit_comm = ibkr_commission(shares)
            t1_comm_val = exit_comm
            t2_comm_val = 0.0
        else:
            t1_comm_val = ibkr_commission(t1_shares)
            t2_comm_val = ibkr_commission(t2_shares)

        total_gross = round(t1_gross + t2_gross, 2)
        total_comm  = round(entry_comm + t1_comm_val + t2_comm_val, 2)
        realized_pnl = round(total_gross - total_comm, 2)
        final_pnl_pct = round(total_gross / actual_position_usd * 100, 2)

        close_summary = f"{t1_r}+{t2_r}"
        close_date = t2_d  # 最后一档的平仓日期

        pos.update({
            "t1_exit_date":   t1_d,
            "t1_exit_price":  t1_p,
            "t1_exit_reason": t1_r,
            "t2_exit_date":   t2_d,
            "t2_exit_price":  t2_p,
            "t2_exit_reason": t2_r,
            "t1_gross_pnl":   t1_gross,
            "t2_gross_pnl":   t2_gross,
            "close_date":     close_date,
            "close_reason":   close_summary,
            "final_pnl_pct":  final_pnl_pct,
            "commission_total": total_comm,
            "realized_pnl_usd": realized_pnl,
            "sl_unified":     sl_unified,
        })
        portfolio["closed_positions"].append(pos)
        print(f"    → T1:{t1_r}@${t1_p} T2:{t2_r}@${t2_p} "
              f"gross=${total_gross:+.2f} comm=-${total_comm:.2f} net=${realized_pnl:+.2f}")


# ── 统计 ──────────────────────────────────────────────────────────

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
        latest_pnl_pct = float(raw_pct) if raw_pct is not None else 0.0
        if latest_pnl_pct != latest_pnl_pct:  # NaN check
            latest_pnl_pct = 0.0
    except (TypeError, ValueError):
        latest_pnl_pct = 0.0
    # Use remaining shares only (if T1 already closed, use t2_shares)
    if p.get("t1_exit_date"):
        remaining_usd = p["t2_shares"] * p["entry_price"]
        locked = p.get("t1_locked_pnl", 0)
    else:
        remaining_usd = p["actual_position_usd"]
        locked = -p["entry_commission"]
    open_unrealized += remaining_usd * latest_pnl_pct / 100 + locked

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

js_content = f"window.PORTFOLIO_F = {json.dumps(portfolio, indent=2, ensure_ascii=False)};\n"
with open("dashboard/portfolio-f.js", "w") as f:
    f.write(js_content)

s = portfolio["stats"]
print(f"\n{'='*60}")
print(f"  Plan F 分档出场回测结果")
print(f"{'='*60}")
print(f"  参数：TP+{TP_PCT}%(2档) / SL-{SL_PCT}% / {MAX_HOLD_TRADING_DAYS}日 / 跳空>{GAP_FILTER_PCT}%过滤")
print(f"  起始本金: ${STARTING_CAPITAL}")
print(f"  总交易:   {s['total_trades']} 笔  胜率: {s['win_rate']}%  跳过: {s['skipped_gap']} 笔")
print(f"  已实现:   ${s['total_realized_pnl_usd']:+.2f}  (佣金 -${s['total_commission_usd']:.2f})")
print(f"  浮盈:     ${s['open_unrealized_pnl_usd']:+.2f}")
print(f"  组合价值: ${s['portfolio_value']}")
print()
print("  已平仓明细:")
for p in all_closed:
    print(f"    {p['action']:4} {p['ticker']:6} {p['signal_date']} "
          f"T1:{p['t1_exit_reason']}@${p['t1_exit_price']} "
          f"T2:{p['t2_exit_reason']}@${p['t2_exit_price']} "
          f"net=${p['realized_pnl_usd']:+.2f}")
print(f"\nSaved to {PORTFOLIO_PATH} and dashboard/portfolio-f.js")
