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
    "qqq_now_usd": 699.5525,
    "value_usd": 349.78,
    "pnl_usd": -10.84,
    "pnl_pct": -3.01,
    "usdcad": 1.4062,
    "cost_cad_approx": 507.1,
    "value_cad_approx": 491.86,
    "pnl_cad_approx": -15.24,
    "updated_at": "2026-07-20 15:15"
  }
};
