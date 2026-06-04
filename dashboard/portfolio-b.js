// Plan B 模拟盘持仓 — 每日自动更新
// 初始状态：无持仓，等待首个 BUY/SELL 信号开仓
window.PORTFOLIO_B = {
  "capital_usd": 1000,
  "open_positions": [],
  "closed_positions": [],
  "stats": {
    "total_trades": 0,
    "win_trades": 0,
    "win_rate": 0,
    "total_realized_pnl_usd": 0,
    "open_unrealized_pnl_usd": 0,
    "portfolio_value": 1000,
    "updated_at": ""
  }
};
