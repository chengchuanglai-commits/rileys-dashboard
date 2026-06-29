// 信号 edge 分析 — analyze-signal-edge.py 自动生成
window.SIGNAL_EDGE = {
  "generated_at": "2026-06-29 12:33",
  "sample_total": 36,
  "date_range": [
    "2026-05-27",
    "2026-06-26"
  ],
  "benchmark": "SPY",
  "horizons": [
    {
      "horizon": 1,
      "n": 32,
      "hit_rate": 40.6,
      "ci_lo": 24,
      "ci_hi": 58,
      "beat_spy_pct": 37.5,
      "avg_pnl": 0.38,
      "avg_alpha": 0.24,
      "verdict": "⚠️ 与噪声难区分"
    },
    {
      "horizon": 3,
      "n": 29,
      "hit_rate": 58.6,
      "ci_lo": 41,
      "ci_hi": 77,
      "beat_spy_pct": 55.2,
      "avg_pnl": 1.32,
      "avg_alpha": 1.38,
      "verdict": "✅ 初步有正 edge"
    },
    {
      "horizon": 5,
      "n": 25,
      "hit_rate": 56.0,
      "ci_lo": 37,
      "ci_hi": 75,
      "beat_spy_pct": 52.0,
      "avg_pnl": 1.97,
      "avg_alpha": 2.0,
      "verdict": "✅ 初步有正 edge"
    }
  ]
};
