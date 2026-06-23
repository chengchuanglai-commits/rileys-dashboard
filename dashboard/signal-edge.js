// 信号 edge 分析 — analyze-signal-edge.py 自动生成
window.SIGNAL_EDGE = {
  "generated_at": "2026-06-23 12:34",
  "sample_total": 31,
  "date_range": [
    "2026-05-27",
    "2026-06-23"
  ],
  "benchmark": "SPY",
  "horizons": [
    {
      "horizon": 1,
      "n": 25,
      "hit_rate": 44.0,
      "ci_lo": 25,
      "ci_hi": 63,
      "beat_spy_pct": 44.0,
      "avg_pnl": 1.01,
      "avg_alpha": 0.99,
      "verdict": "⚠️ 与噪声难区分"
    },
    {
      "horizon": 3,
      "n": 22,
      "hit_rate": 63.6,
      "ci_lo": 44,
      "ci_hi": 84,
      "beat_spy_pct": 63.6,
      "avg_pnl": 1.13,
      "avg_alpha": 1.55,
      "verdict": "✅ 初步有正 edge"
    },
    {
      "horizon": 5,
      "n": 18,
      "hit_rate": 66.7,
      "ci_lo": 45,
      "ci_hi": 88,
      "beat_spy_pct": 66.7,
      "avg_pnl": 3.38,
      "avg_alpha": 4.07,
      "verdict": "✅ 初步有正 edge"
    }
  ]
};
