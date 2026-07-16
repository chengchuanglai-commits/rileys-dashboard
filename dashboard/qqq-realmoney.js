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
    }
  ],
  "stats": {
    "shares": 0.5,
    "avg_price_usd": 721.24,
    "cost_usd": 360.62,
    "qqq_now_usd": 706.8951,
    "value_usd": 353.45,
    "pnl_usd": -7.17,
    "pnl_pct": -1.99,
    "usdcad": 1.4052,
    "cost_cad_approx": 506.74,
    "value_cad_approx": 496.67,
    "pnl_cad_approx": -10.08,
    "updated_at": "2026-07-16 18:11"
  }
};
