"""
Plan E — 智能市场适应方案
规则来源：Livermore / Paul Tudor Jones / Druckenmiller / Minervini

市场状态  VIX        方向        仓位   TP     SL     持仓
牛市      < 15       BUY+SELL   $600   +12%   -3%    3天
震荡      15-20      仅 SELL     $500   +10%   -3%    3天
谨慎      20-25      仅 SELL     $350   +8%    -2.5%  2天
恐慌      > 25       跳过        —      —      —      —

跳空过滤：不利跳空 > 1.5% 跳过
佣金：IBKR $0.005/股，最低 $1.00/单（入场+出场各一次）
"""
import json, os
from datetime import datetime, timedelta
import yfinance as yf

SIGNALS_DIR = "dashboard/trading-signals-history"
PORTFOLIO_PATH = "data/portfolio_e.json"
os.makedirs("data", exist_ok=True)

STARTING_CAPITAL = 2000
GAP_FILTER_PCT = 1.5

# 市场状态阈值
REGIMES = [
    # (vix_max, label, allow_buy, position_usd, tp_pct, sl_pct, max_days)
    (15,  "bull",    True,  600, 12.0, 3.0, 3),
    (20,  "neutral", False, 500, 10.0, 3.0, 3),
    (25,  "caution", False, 350,  8.0, 2.5, 2),
    (999, "fear",    False,   0,  0.0, 0.0, 0),  # skip
]

def ibkr_commission(shares):
    return round(max(1.00, shares * 0.005), 2)

_vix_cache = {}
_spy_cache = {}

def get_vix(date_str):
    if date_str in _vix_cache:
        return _vix_cache[date_str]
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        start = (dt - timedelta(days=5)).strftime("%Y-%m-%d")
        end   = (dt + timedelta(days=1)).strftime("%Y-%m-%d")
        df = yf.Ticker("^VIX").history(start=start, end=end)
        df.index = df.index.tz_localize(None) if df.index.tz else df.index
        # find closest trading day on or before date
        for idx in reversed(df.index):
            if idx.strftime("%Y-%m-%d") <= date_str:
                val = round(float(df.loc[idx, "Close"]), 2)
                _vix_cache[date_str] = val
                return val
    except Exception as e:
        print(f"  [warn] VIX fetch failed for {date_str}: {e}")
    _vix_cache[date_str] = 18.0  # fallback neutral
    return 18.0

def get_regime(vix):
    for vix_max, label, allow_buy, pos_usd, tp_pct, sl_pct, max_days in REGIMES:
        if vix < vix_max:
            return label, allow_buy, pos_usd, tp_pct, sl_pct, max_days
    return "fear", False, 0, 0, 0, 0

def next_n_trading_days(start_str, n):
    dt = datetime.strptime(start_str, "%Y-%m-%d")
    days = []
    while len(days) < n:
        dt += timedelta(days=1)
        if dt.weekday() < 5:
            days.append(dt.strftime("%Y-%m-%d"))
    return days

def simulate_position(ticker, action, entry_price, signal_date, tp_pct, sl_pct, max_days):
    tp_price = round(entry_price * (1 + tp_pct/100 if action == "BUY" else 1 - tp_pct/100), 2)
    sl_price = round(entry_price * (1 - sl_pct/100 if action == "BUY" else 1 + sl_pct/100), 2)

    target_dates = next_n_trading_days(signal_date, max_days)
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

        # Day-1 gap filter (stricter: 1.5%)
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
    "_note": "Plan E 智能市场适应：VIX自适应仓位+方向过滤，规则来自 Livermore/Jones/Druckenmiller/Minervini / IBKR佣金$0.005/股min$1"
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

skipped_fear = 0
skipped_direction = 0
skipped_gap = 0

for signal_date, s in all_signals:
    ticker = s.get("ticker")
    action = s.get("action", "").upper()
    entry_price = s.get("current_price")

    if not ticker or action not in ("BUY", "SELL") or not entry_price:
        continue

    # 获取当日 VIX，判断市场状态
    vix = get_vix(signal_date)
    regime, allow_buy, pos_usd, tp_pct, sl_pct, max_days = get_regime(vix)

    print(f"  {signal_date} {action:4} {ticker:6}  VIX={vix:.1f} [{regime}]", end="")

    # 恐慌市场跳过所有信号
    if regime == "fear":
        print(f" → 跳过（恐慌市场）")
        skipped_fear += 1
        continue

    # 震荡/谨慎市场跳过 BUY 信号
    if action == "BUY" and not allow_buy:
        print(f" → 跳过（{regime}市场不做多）")
        skipped_direction += 1
        continue

    # 计算整数股数和佣金
    shares = int(pos_usd / entry_price)
    if shares == 0:
        print(f" → 跳过（价格过高，${entry_price:.2f}/股，${pos_usd}仓位买不到1股）")
        continue

    actual_position_usd = round(shares * entry_price, 2)
    entry_comm = ibkr_commission(shares)
    exit_comm = ibkr_commission(shares)

    close_date, close_price, close_reason, final_pnl_pct, daily_prices, gap_filtered = \
        simulate_position(ticker, action, entry_price, signal_date, tp_pct, sl_pct, max_days)

    tp_price = round(entry_price * (1 + tp_pct/100 if action == "BUY" else 1 - tp_pct/100), 2)
    sl_price = round(entry_price * (1 - sl_pct/100 if action == "BUY" else 1 + sl_pct/100), 2)

    pos = {
        "ticker": ticker,
        "name": s.get("name", ticker),
        "action": action,
        "signal_date": signal_date,
        "entry_price": entry_price,
        "allocated_usd": pos_usd,
        "shares": shares,
        "actual_position_usd": actual_position_usd,
        "entry_commission": entry_comm,
        "take_profit": tp_price,
        "stop_loss": sl_price,
        "max_hold_days": max_days,
        "max_hold_date": next_n_trading_days(signal_date, max_days)[-1],
        "regime": regime,
        "vix": vix,
        "daily_prices": daily_prices,
    }

    if gap_filtered:
        print(f" → 跳空过滤")
        skipped_gap += 1
        continue

    if close_reason == "open":
        pos["gap_checked"] = True
        if daily_prices:
            first_date = list(daily_prices.keys())[0]
            pos["day1_open"] = daily_prices[first_date].get("open")
        portfolio["open_positions"].append(pos)
        print(f" → 开仓中 ({shares}股 实际${actual_position_usd})")
    else:
        gross_pnl = round(actual_position_usd * final_pnl_pct / 100, 2)
        realized_pnl = round(gross_pnl - entry_comm - exit_comm, 2)
        pos.update({
            "close_date": close_date,
            "close_price": close_price,
            "final_pnl_pct": final_pnl_pct,
            "close_reason": close_reason,
            "exit_commission": exit_comm,
            "commission_total": round(entry_comm + exit_comm, 2),
            "realized_pnl_usd": realized_pnl,
        })
        portfolio["closed_positions"].append(pos)
        print(f" → {close_reason} {final_pnl_pct:+.1f}% gross=${gross_pnl:+.2f} comm=-${entry_comm+exit_comm:.2f} net=${realized_pnl:+.2f}")

# 统计
closed = portfolio["closed_positions"]
wins = [p for p in closed if p.get("realized_pnl_usd", 0) > 0]
total_realized = sum(p.get("realized_pnl_usd", 0) for p in closed)
total_commission = sum(p.get("commission_total", 0) for p in closed)
open_unrealized = sum(
    p.get("actual_position_usd", p.get("allocated_usd", 0)) * list(p["daily_prices"].values())[-1]["pnl_pct"] / 100 - p.get("entry_commission", 0)
    for p in portfolio["open_positions"] if p.get("daily_prices")
)

portfolio["stats"] = {
    "total_trades": len(closed),
    "win_trades": len(wins),
    "win_rate": round(len(wins) / len(closed) * 100, 1) if closed else 0,
    "total_realized_pnl_usd": round(total_realized, 2),
    "open_unrealized_pnl_usd": round(open_unrealized, 2),
    "portfolio_value": round(STARTING_CAPITAL + total_realized + open_unrealized, 2),
    "total_commission_usd": round(total_commission, 2),
    "skipped_fear": skipped_fear,
    "skipped_direction": skipped_direction,
    "skipped_gap": skipped_gap,
    "updated_at": datetime.now().strftime("%Y-%m-%d"),
}

print(f"\n=== Plan E 结果 ===")
print(f"执行交易: {len(closed)}笔  开仓: {len(portfolio['open_positions'])}笔")
print(f"跳过（恐慌）: {skipped_fear}  跳过（方向）: {skipped_direction}  跳过（跳空）: {skipped_gap}")
print(f"胜率: {portfolio['stats']['win_rate']}%")
print(f"总盈亏: ${total_realized:+.2f}  佣金: -${total_commission:.2f}  组合价值: ${portfolio['stats']['portfolio_value']:.2f}")

with open(PORTFOLIO_PATH, "w") as f:
    json.dump(portfolio, f, indent=2, ensure_ascii=False)

js_content = f"window.PORTFOLIO_E = {json.dumps(portfolio, indent=2, ensure_ascii=False)};\n"
with open("dashboard/portfolio-e.js", "w") as f:
    f.write(js_content)

print(f"Saved to {PORTFOLIO_PATH} and dashboard/portfolio-e.js")
