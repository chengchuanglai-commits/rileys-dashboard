// 真钱指数核心台账(QQQ+QQQM)
window.QQQ_REALMONEY = {
  "_note": "真钱 QQQ 指数核心台账(独立于IBKR模拟盘与研究腿)。数字取自券商截图,美元计价(均价721.24≈美元报价720.49→判定USD)。加仓时往 tranches 追加一条,脚本自动重算。若账户实为加元,改 currency 与成本。",
  "currency": "USD",
  "tranches": [
    {
      "date": "2026-07-09",
      "shares": 0.5,
      "price_usd": 721.24,
      "cost_usd": 360.62,
      "note": "第一批DCA(券商截图:均价721.24/成本360.62)",
      "sym": "QQQ"
    },
    {
      "date": "2026-07-14",
      "shares": 0.5,
      "price_usd": 721.67,
      "cost_usd": 360.84,
      "note": "第二批DCA(收复$722入场信号,飞书23:30,限价721.77成交721.67)",
      "sym": "QQQ"
    },
    {
      "date": "2026-08-05",
      "sym": "QQQM",
      "shares": 1,
      "price_usd": 298.51,
      "cost_usd": 298.51,
      "note": "托管自动买入(收复$722趋势修复)"
    }
  ],
  "stats": {
    "per_symbol": {
      "QQQ": {
        "shares": 1.0,
        "avg_price_usd": 721.46,
        "cost_usd": 721.46,
        "now_usd": 711.37,
        "value_usd": 711.37,
        "pnl_usd": -10.09
      },
      "QQQM": {
        "shares": 1,
        "avg_price_usd": 298.51,
        "cost_usd": 298.51,
        "now_usd": 292.9,
        "value_usd": 292.9,
        "pnl_usd": -5.61
      }
    },
    "cost_usd": 1019.97,
    "value_usd": 1004.27,
    "pnl_usd": -15.7,
    "pnl_pct": -1.54,
    "usdcad": 1.3874,
    "cost_cad_approx": 1415.11,
    "value_cad_approx": 1393.32,
    "pnl_cad_approx": -21.78,
    "updated_at": "2026-08-26 20:38"
  }
};
