// 信号 edge 分析 — analyze-signal-edge.py 自动生成
window.SIGNAL_EDGE = {
  "generated_at": "2026-07-07 11:34",
  "sample_total": 47,
  "date_range": [
    "2026-05-27",
    "2026-07-06"
  ],
  "benchmark": "SPY",
  "horizons": [
    {
      "horizon": 1,
      "n": 40,
      "hit_rate": 40.0,
      "ci_lo": 25,
      "ci_hi": 55,
      "beat_spy_pct": 37.5,
      "avg_pnl": 0.16,
      "avg_alpha": 0.21,
      "verdict": "❌ 无 edge"
    },
    {
      "horizon": 3,
      "n": 34,
      "hit_rate": 55.9,
      "ci_lo": 39,
      "ci_hi": 73,
      "beat_spy_pct": 52.9,
      "avg_pnl": 0.8,
      "avg_alpha": 1.07,
      "verdict": "✅ 初步有正 edge"
    },
    {
      "horizon": 5,
      "n": 34,
      "hit_rate": 50.0,
      "ci_lo": 33,
      "ci_hi": 67,
      "beat_spy_pct": 50.0,
      "avg_pnl": 1.32,
      "avg_alpha": 1.68,
      "verdict": "⚠️ 与噪声难区分"
    }
  ]
};
