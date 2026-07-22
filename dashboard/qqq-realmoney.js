// 真钱 QQQ 指数核心台账
window.QQQ_REALMONEY = {
  "_note": "真钱 QQQ 指数核心台账(独立于IBKR模拟盘与研究腿)。数字取自券商截图,美元计价(均价721.24≈美元报价720.49→判定USD)。加仓时往 tranches 追加一条,脚本自动重算。若账户实为加元,改 currency 与成本。",
  "currency": "USD",
  "tranches": [
    {
      "date": "2026-07-09",
      "shares": 0.5,
      "price_usd": 721.24,
      "cost_usd": 360.62,
      "note": "第一批DCA(券商截图:均价721.24/成本360.62)"
    },
    {
      "date": "2026-07-14",
      "shares": 0.5,
      "price_usd": 721.67,
      "cost_usd": 360.84,
      "note": "第二批DCA(收复$722入场信号,飞书23:30,限价721.77成交721.67)"
    }
  ],
  "stats": {
    "shares": 1.0,
    "avg_price_usd": 721.46,
    "cost_usd": 721.46,
    "qqq_now_usd": 705.35,
    "value_usd": 705.35,
    "pnl_usd": -16.11,
    "pnl_pct": -2.23,
    "usdcad": 1.4082,
    "cost_cad_approx": 1015.96,
    "value_cad_approx": 993.27,
    "pnl_cad_approx": -22.69,
    "updated_at": "2026-07-22 21:11"
  }
};
