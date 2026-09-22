// 信号 edge 分析 — analyze-signal-edge.py 自动生成
window.SIGNAL_EDGE = {
  "generated_at": "2026-09-22 12:27",
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
      "hit_rate": 50.0,
      "ci_lo": 36,
      "ci_hi": 64,
      "beat_spy_pct": 47.9,
      "avg_pnl": 1.2,
      "avg_alpha": 1.3,
      "verdict": "⚠️ 与噪声难区分"
    },
    {
      "horizon": 3,
      "n": 48,
      "hit_rate": 58.3,
      "ci_lo": 44,
      "ci_hi": 72,
      "beat_spy_pct": 54.2,
      "avg_pnl": 1.87,
      "avg_alpha": 1.99,
      "verdict": "✅ 初步有正 edge"
    },
    {
      "horizon": 5,
      "n": 48,
      "hit_rate": 56.2,
      "ci_lo": 42,
      "ci_hi": 70,
      "beat_spy_pct": 60.4,
      "avg_pnl": 2.02,
      "avg_alpha": 2.31,
      "verdict": "✅ 初步有正 edge"
    }
  ]
};
