// 信号 edge 分析 — analyze-signal-edge.py 自动生成
window.SIGNAL_EDGE = {
  "generated_at": "2026-07-17 13:55",
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
      "hit_rate": 45.8,
      "ci_lo": 32,
      "ci_hi": 60,
      "beat_spy_pct": 41.7,
      "avg_pnl": 0.23,
      "avg_alpha": 0.33,
      "verdict": "⚠️ 与噪声难区分"
    },
    {
      "horizon": 3,
      "n": 47,
      "hit_rate": 53.2,
      "ci_lo": 39,
      "ci_hi": 67,
      "beat_spy_pct": 51.1,
      "avg_pnl": 0.62,
      "avg_alpha": 0.79,
      "verdict": "✅ 初步有正 edge"
    },
    {
      "horizon": 5,
      "n": 44,
      "hit_rate": 54.5,
      "ci_lo": 40,
      "ci_hi": 69,
      "beat_spy_pct": 56.8,
      "avg_pnl": 0.96,
      "avg_alpha": 1.35,
      "verdict": "✅ 初步有正 edge"
    }
  ]
};
