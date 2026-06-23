// Plan MOM-MA — 动量/趋势选股(无AI) + J Law 10/20MA移动止盈
window.PORTFOLIO_MOMMA = {
  "capital_usd": 2000,
  "open_positions": [
    {
      "ticker": "STRL",
      "action": "BUY",
      "signal_date": "2026-06-18",
      "entry_price": 861.88,
      "shares": 0.5801,
      "stop_loss": 792.93,
      "score": 74.6,
      "actual_position_usd": 499.98,
      "position_usd": 200.0,
      "unrealized_pnl_usd": 7.36
    },
    {
      "ticker": "IESC",
      "action": "BUY",
      "signal_date": "2026-06-18",
      "entry_price": 712.39,
      "shares": 0.7019,
      "stop_loss": 655.4,
      "score": 76.2,
      "actual_position_usd": 500.03,
      "position_usd": 200.0,
      "unrealized_pnl_usd": 5.52
    },
    {
      "ticker": "VICR",
      "action": "BUY",
      "signal_date": "2026-06-18",
      "entry_price": 331.37,
      "shares": 1.5089,
      "stop_loss": 304.86,
      "score": 77.0,
      "actual_position_usd": 500.0,
      "position_usd": 200.0,
      "unrealized_pnl_usd": 5.35
    },
    {
      "ticker": "COHR",
      "action": "BUY",
      "signal_date": "2026-06-18",
      "entry_price": 389.57,
      "shares": 1.2835,
      "stop_loss": 358.4,
      "score": 75.9,
      "actual_position_usd": 500.01,
      "position_usd": 200.0,
      "unrealized_pnl_usd": 1.85
    },
    {
      "ticker": "AMD",
      "action": "BUY",
      "signal_date": "2026-06-18",
      "entry_price": 537.37,
      "shares": 0.9305,
      "stop_loss": 494.38,
      "score": 74.3,
      "actual_position_usd": 500.02,
      "position_usd": 200.0,
      "unrealized_pnl_usd": -3.68
    },
    {
      "ticker": "RVMD",
      "action": "BUY",
      "signal_date": "2026-06-18",
      "entry_price": 162.99,
      "shares": 3.0677,
      "stop_loss": 149.95,
      "score": 75.4,
      "actual_position_usd": 500.0,
      "position_usd": 200.0,
      "unrealized_pnl_usd": 8.84
    }
  ],
  "closed_positions": [
    {
      "ticker": "STM",
      "action": "BUY",
      "signal_date": "2026-06-18",
      "entry_price": 78.39,
      "shares": 6.3784,
      "stop_loss": 72.12,
      "score": 78.7,
      "close_date": "2026-06-23",
      "close_price": 72.12,
      "close_reason": "init_stop",
      "final_pnl_pct": -8.0,
      "realized_pnl_usd": -16.0,
      "commission_total": 2.0,
      "position_usd": 200.0
    },
    {
      "ticker": "ON",
      "action": "BUY",
      "signal_date": "2026-06-18",
      "entry_price": 121.62,
      "shares": 4.1112,
      "stop_loss": 111.89,
      "score": 76.2,
      "close_date": "2026-06-23",
      "close_price": 119.77,
      "close_reason": "ma_break",
      "final_pnl_pct": -1.52,
      "realized_pnl_usd": -3.04,
      "commission_total": 2.0,
      "position_usd": 200.0
    },
    {
      "ticker": "HUT",
      "action": "BUY",
      "signal_date": "2026-06-18",
      "entry_price": 124.44,
      "shares": 4.018,
      "stop_loss": 114.48,
      "score": 79.1,
      "close_date": "2026-06-23",
      "close_price": 114.48,
      "close_reason": "init_stop",
      "final_pnl_pct": -8.0,
      "realized_pnl_usd": -16.0,
      "commission_total": 2.0,
      "position_usd": 200.0
    }
  ],
  "_note": "MOM-MA：动量/趋势选股(同MOM-H) + J Law 10/20MA移动止盈(收盘破20MA才走,让赢家跑)+初始-8%硬止损。$500/仓(小数股),现金约束(最多10仓,$2000无杠杆),周再平衡,前向无前视。",
  "stats": {
    "total_trades": 3,
    "win_trades": 0,
    "win_rate": 0.0,
    "total_realized_pnl_usd": -35.04,
    "open_unrealized_pnl_usd": 25.23,
    "portfolio_value": 1990.19,
    "total_commission_usd": 12.0,
    "skipped_no_cash": 0,
    "updated_at": "2026-06-24"
  }
};
