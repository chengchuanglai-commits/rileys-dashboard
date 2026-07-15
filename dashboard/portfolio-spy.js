// SPY 买入持有基准 — $2000 起始日买入持有至今
window.PORTFOLIO_SPY = {
  "capital_usd": 2000,
  "benchmark": "SPY 买入持有",
  "start_date": "2026-05-26",
  "start_price": 748.66,
  "current_price": 752.93,
  "current_date": "2026-07-15",
  "open_positions": [
    {
      "ticker": "SPY",
      "name": "SPY 基准",
      "action": "BUY",
      "signal_date": "2026-05-26",
      "entry_price": 748.66,
      "shares": 2.6714,
      "actual_position_usd": 2000
    }
  ],
  "closed_positions": [],
  "stats": {
    "total_trades": 0,
    "win_trades": 0,
    "win_rate": 0,
    "total_realized_pnl_usd": 0,
    "open_unrealized_pnl_usd": 11.41,
    "portfolio_value": 2011.41,
    "total_return_pct": 0.57,
    "total_commission_usd": 1.0,
    "updated_at": "2026-07-15"
  },
  "_note": "SPY 买入持有基准：$2000 在起始日买入 SPY 持有至今。衡量各策略有没有跑赢大盘。收益全为未实现(总收益口径)。"
};
