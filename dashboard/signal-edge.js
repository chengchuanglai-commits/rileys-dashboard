// 信号 edge 分析 — analyze-signal-edge.py 自动生成
window.SIGNAL_EDGE = {
  "generated_at": "2026-07-08 11:34",
  "sample_total": 47,
  "date_range": [
    "2026-05-27",
    "2026-07-06"
  ],
  "benchmark": "SPY",
  "horizons": [
    {
      "horizon": 1,
      "n": 42,
      "hit_rate": 42.9,
      "ci_lo": 28,
      "ci_hi": 58,
      "beat_spy_pct": 38.1,
      "avg_pnl": 0.21,
      "avg_alpha": 0.24,
      "verdict": "⚠️ 与噪声难区分"
    },
    {
      "horizon": 3,
      "n": 36,
      "hit_rate": 55.6,
      "ci_lo": 39,
      "ci_hi": 72,
      "beat_spy_pct": 52.8,
      "avg_pnl": 0.71,
      "avg_alpha": 0.99,
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
