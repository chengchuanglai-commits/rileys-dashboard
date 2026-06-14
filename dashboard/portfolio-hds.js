// Plan H-DS 模拟盘持仓 — 历史最优参数(TP15/SL2/2日) 回溯 + 实时更新
window.PORTFOLIO_HDSDS = {
  "capital_usd": 2000,
  "open_positions": [
    {
      "ticker": "WEYS",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-06-12",
      "entry_price": 37.0,
      "allocated_usd": 500,
      "shares": 13,
      "actual_position_usd": 481.0,
      "entry_commission": 1.0,
      "take_profit": 42.55,
      "stop_loss": 36.26,
      "max_hold_date": "2026-06-16",
      "daily_prices": {}
    },
    {
      "ticker": "PBHC",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-06-12",
      "entry_price": 15.45,
      "allocated_usd": 500,
      "shares": 32,
      "actual_position_usd": 494.4,
      "entry_commission": 1.0,
      "take_profit": 17.77,
      "stop_loss": 15.14,
      "max_hold_date": "2026-06-16",
      "daily_prices": {}
    },
    {
      "ticker": "ARCB",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-06-12",
      "entry_price": 173.04,
      "allocated_usd": 500,
      "shares": 2,
      "actual_position_usd": 346.08,
      "entry_commission": 1.0,
      "take_profit": 147.08,
      "stop_loss": 176.5,
      "max_hold_date": "2026-06-16",
      "daily_prices": {}
    },
    {
      "ticker": "HOFT",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-06-12",
      "entry_price": 15.35,
      "allocated_usd": 500,
      "shares": 32,
      "actual_position_usd": 491.2,
      "entry_commission": 1.0,
      "take_profit": 13.05,
      "stop_loss": 15.66,
      "max_hold_date": "2026-06-16",
      "daily_prices": {}
    }
  ],
  "closed_positions": [],
  "_note": "H-DS 模拟盘：DeepSeek(V4-pro) 信号 + H 出场规则(TP15/SL2/2日/gap1.0)。与 Plan H(Haiku信号+同规则)头对头比模型。仅A/B对比,不是真实交易方案。",
  "stats": {
    "total_trades": 0,
    "win_trades": 0,
    "win_rate": 0,
    "total_realized_pnl_usd": 0,
    "open_unrealized_pnl_usd": 0,
    "portfolio_value": 2000,
    "total_commission_usd": 0,
    "skipped_gap": 0,
    "skipped_zero_shares": 0,
    "updated_at": "2026-06-14"
  }
};
