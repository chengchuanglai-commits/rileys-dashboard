// 金融晨报数据 — 每日 07:30 自动更新
window.MORNING_NOTE = {
  "date": "2026-05-18",
  "generated_at": "2026-05-18T07:30:00",
  "market_status": "pre-market",
  "market": {
    "sp500_futures_pct": -0.4,
    "treasury_10y": 4.55,
    "treasury_10y_change_bps": 9,
    "eps_beat_rate": 84
  },
  "note": {
    "market_overview": "美股期货延续上周五跌势，S&P 500 期货下跌 0.4%。市场情绪谨慎，投资者等待本周 Nvidia 财报（预期 EPS $1.78），视为 AI 行情风向标。自3月30日低点，S&P 已累计反弹 +13%。",
    "macro": "10年期美债升至 4.55%（一年新高），加息概率升至 45%。新Fed主席 Kevin Warsh 接替 Powell，政策不确定性上升。油价因伊朗局势走高。",
    "earnings": "Q1 财报季亮眼：84% 公司 EPS 超预期，超预期幅度 +18.2%（历史均值7%）。Alphabet 4月涨 +34%，为2004年来最强单月。全年 EPS 增速预期调升至 18.6%。",
    "trade_ideas": "⚡ 谨慎科技多单：收益率飙升压制高估值成长股。⚡ 关注能源板块：油价受地缘支撑，中期机会。⚡ NVDA 期权：财报前 IV 高企，可考虑卖出宽跨式策略。"
  },
  "stock_picks": [
    {
      "ticker": "NVDA",
      "name": "Nvidia",
      "sector": "科技/半导体",
      "direction": "watch",
      "buy_zone": "$900–$920",
      "target": "$980",
      "stop_loss": "$870",
      "reason": "财报前 IV 高企，等财报方向确认后再入场，勿追涨"
    },
    {
      "ticker": "XOM",
      "name": "ExxonMobil",
      "sector": "能源",
      "direction": "buy",
      "buy_zone": "$118–$122",
      "target": "$135",
      "stop_loss": "$112",
      "reason": "地缘风险支撑油价，能源板块中期受益，估值合理"
    },
    {
      "ticker": "UNH",
      "name": "UnitedHealth",
      "sector": "医疗保险",
      "direction": "watch",
      "buy_zone": "$480–$495",
      "target": "$530",
      "stop_loss": "$465",
      "reason": "医疗板块防御性强，等待回调至支撑位再买入"
    },
    {
      "ticker": "TLT",
      "name": "iShares 20Y美债ETF",
      "sector": "固定收益",
      "direction": "sell",
      "buy_zone": "—",
      "target": "—",
      "stop_loss": "—",
      "reason": "收益率上升期长债价格承压，暂时回避，等加息预期降温"
    },
    {
      "ticker": "COST",
      "name": "Costco",
      "sector": "消费/零售",
      "direction": "buy",
      "buy_zone": "$890–$910",
      "target": "$960",
      "stop_loss": "$875",
      "reason": "通胀环境下消费者首选，会员续费率稳健，防御性强"
    }
  ]
};
