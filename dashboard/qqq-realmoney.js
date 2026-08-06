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
        "now_usd": 717.96,
        "value_usd": 717.96,
        "pnl_usd": -3.5
      },
      "QQQM": {
        "shares": 1,
        "avg_price_usd": 298.51,
        "cost_usd": 298.51,
        "now_usd": 295.725,
        "value_usd": 295.73,
        "pnl_usd": -2.78
      }
    },
    "cost_usd": 1019.97,
    "value_usd": 1013.69,
    "pnl_usd": -6.28,
    "pnl_pct": -0.62,
    "usdcad": 1.4033,
    "cost_cad_approx": 1431.32,
    "value_cad_approx": 1422.5,
    "pnl_cad_approx": -8.81,
    "updated_at": "2026-08-06 15:17"
  }
};
