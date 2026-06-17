// 信号 edge 分析 — analyze-signal-edge.py 自动生成
window.SIGNAL_EDGE = {
  "generated_at": "2026-06-17 11:50",
  "sample_total": 23,
  "date_range": [
    "2026-05-27",
    "2026-06-16"
  ],
  "benchmark": "SPY",
  "horizons": [
    {
      "horizon": 1,
      "n": 20,
      "hit_rate": 50.0,
      "ci_lo": 28,
      "ci_hi": 72,
      "beat_spy_pct": 50.0,
      "avg_pnl": 0.58,
      "avg_alpha": 0.77,
      "verdict": "⚠️ 与噪声难区分"
    },
    {
      "horizon": 3,
      "n": 18,
      "hit_rate": 66.7,
      "ci_lo": 45,
      "ci_hi": 88,
      "beat_spy_pct": 66.7,
      "avg_pnl": 1.57,
      "avg_alpha": 2.26,
      "verdict": "✅ 初步有正 edge"
    },
    {
      "horizon": 5,
      "n": 14,
      "hit_rate": 71.4,
      "ci_lo": 48,
      "ci_hi": 95,
      "beat_spy_pct": 71.4,
      "avg_pnl": 4.99,
      "avg_alpha": 5.53,
      "verdict": "✅ 初步有正 edge"
    }
  ]
};
