"""
SPY 基准盘 —— "$2000 在起始日买入 SPY 并持有"的躺平基准，用于衡量各策略有没有跑赢大盘。
起始日 = 模拟盘最早的信号日(与各策略同窗口)。无 AI、无 token 成本，纯价格计算。

注意：这是「买入持有」基准，收益全是未实现(mark-to-market)，不像主动盘有已实现/平仓。
排行榜按已实现排序时不应把 SPY 当竞争者排进去——它是参考线(总收益口径)。
"""
import json, os
from datetime import datetime
import yfinance as yf

STARTING_CAPITAL = 2000
SIGNALS_DIR = "dashboard/trading-signals-history"
PORTFOLIO_PATH = "data/portfolio_spy.json"
os.makedirs("data", exist_ok=True)

# 起始日 = 最早的信号日
dates = []
for f in os.listdir(SIGNALS_DIR):
    if f.endswith(".json") and "-report" not in f and f[:1].isdigit():
        try:
            datetime.strptime(f[:10], "%Y-%m-%d")
            dates.append(f[:10])
        except Exception:
            pass
start = min(dates) if dates else "2026-05-27"
today = datetime.now().strftime("%Y-%m-%d")

df = yf.Ticker("SPY").history(start=start)
df.index = df.index.tz_localize(None) if getattr(df.index, "tz", None) else df.index

start_price = None
for idx, r in df.iterrows():
    if idx.strftime("%Y-%m-%d") >= start:
        c = float(r["Close"])
        if c == c:
            start_price = round(c, 2)
            start = idx.strftime("%Y-%m-%d")
            break
cur_price = round(float(df["Close"].iloc[-1]), 2) if not df.empty else start_price
cur_date = df.index[-1].strftime("%Y-%m-%d") if not df.empty else today

shares = STARTING_CAPITAL / start_price if start_price else 0
value = round(shares * cur_price, 2) if start_price else STARTING_CAPITAL
ret_pct = round((value - STARTING_CAPITAL) / STARTING_CAPITAL * 100, 2)

portfolio = {
    "capital_usd": STARTING_CAPITAL,
    "benchmark": "SPY 买入持有",
    "start_date": start,
    "start_price": start_price,
    "current_price": cur_price,
    "current_date": cur_date,
    "open_positions": [{
        "ticker": "SPY", "name": "SPY 基准", "action": "BUY",
        "signal_date": start, "entry_price": start_price,
        "shares": round(shares, 4), "actual_position_usd": STARTING_CAPITAL,
    }],
    "closed_positions": [],
    "stats": {
        "total_trades": 0,
        "win_trades": 0,
        "win_rate": 0,
        "total_realized_pnl_usd": 0,                  # 买入持有,无已实现
        "open_unrealized_pnl_usd": round(value - STARTING_CAPITAL, 2),
        "portfolio_value": value,                     # = 总收益口径(mark-to-market)
        "total_return_pct": ret_pct,
        "total_commission_usd": 1.0,                  # 一次买入佣金
        "updated_at": today,
    },
    "_note": "SPY 买入持有基准：$2000 在起始日买入 SPY 持有至今。衡量各策略有没有跑赢大盘。收益全为未实现(总收益口径)。",
}

with open(PORTFOLIO_PATH, "w") as f:
    json.dump(portfolio, f, ensure_ascii=False, indent=2)

with open("dashboard/portfolio-spy.js", "w", encoding="utf-8") as f:
    f.write("// SPY 买入持有基准 — $2000 起始日买入持有至今\n")
    f.write(f"window.PORTFOLIO_SPY = {json.dumps(portfolio, ensure_ascii=False, indent=2)};\n")

print(f"📊 SPY 基准：起始 {start} @ ${start_price} → {cur_date} @ ${cur_price}")
print(f"   $2000 买入持有 → ${value} ({ret_pct:+.2f}%)")
