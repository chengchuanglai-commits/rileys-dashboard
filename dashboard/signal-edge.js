// 信号 edge 分析 — analyze-signal-edge.py 自动生成
window.SIGNAL_EDGE = {
  "generated_at": "2026-07-13 12:36",
  "sample_total": 51,
  "date_range": [
    "2026-05-27",
    "2026-07-13"
  ],
  "benchmark": "SPY",
  "horizons": [
    {
      "horizon": 1,
      "n": 45,
      "hit_rate": 42.2,
      "ci_lo": 28,
      "ci_hi": 57,
      "beat_spy_pct": 37.8,
      "avg_pnl": 0.4,
      "avg_alpha": 0.45,
      "verdict": "⚠️ 与噪声难区分"
    },
    {
      "horizon": 3,
      "n": 41,
      "hit_rate": 53.7,
      "ci_lo": 38,
      "ci_hi": 69,
      "beat_spy_pct": 51.2,
      "avg_pnl": 0.29,
      "avg_alpha": 0.53,
      "verdict": "✅ 初步有正 edge"
    },
    {
      "horizon": 5,
      "n": 39,
      "hit_rate": 51.3,
      "ci_lo": 36,
      "ci_hi": 67,
      "beat_spy_pct": 53.8,
      "avg_pnl": 0.68,
      "avg_alpha": 1.14,
      "verdict": "✅ 初步有正 edge"
    }
  ]
};
