// 信号 edge 分析 — analyze-signal-edge.py 自动生成
window.SIGNAL_EDGE = {
  "generated_at": "2026-09-15 12:17",
  "sample_total": 54,
  "date_range": [
    "2026-05-27",
    "2026-07-15"
  ],
  "benchmark": "SPY",
  "horizons": [
    {
      "horizon": 1,
      "n": 48,
      "hit_rate": 47.9,
      "ci_lo": 34,
      "ci_hi": 62,
      "beat_spy_pct": 45.8,
      "avg_pnl": 1.14,
      "avg_alpha": 1.24,
      "verdict": "⚠️ 与噪声难区分"
    },
    {
      "horizon": 3,
      "n": 48,
      "hit_rate": 56.2,
      "ci_lo": 42,
      "ci_hi": 70,
      "beat_spy_pct": 54.2,
      "avg_pnl": 1.81,
      "avg_alpha": 1.94,
      "verdict": "✅ 初步有正 edge"
    },
    {
      "horizon": 5,
      "n": 48,
      "hit_rate": 56.2,
      "ci_lo": 42,
      "ci_hi": 70,
      "beat_spy_pct": 60.4,
      "avg_pnl": 1.96,
      "avg_alpha": 2.25,
      "verdict": "✅ 初步有正 edge"
    }
  ]
};
