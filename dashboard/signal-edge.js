// 信号 edge 分析 — analyze-signal-edge.py 自动生成
window.SIGNAL_EDGE = {
  "generated_at": "2026-06-30 12:33",
  "sample_total": 36,
  "date_range": [
    "2026-05-27",
    "2026-06-26"
  ],
  "benchmark": "SPY",
  "horizons": [
    {
      "horizon": 1,
      "n": 34,
      "hit_rate": 38.2,
      "ci_lo": 22,
      "ci_hi": 55,
      "beat_spy_pct": 35.3,
      "avg_pnl": 0.11,
      "avg_alpha": 0.07,
      "verdict": "❌ 无 edge"
    },
    {
      "horizon": 3,
      "n": 32,
      "hit_rate": 56.2,
      "ci_lo": 39,
      "ci_hi": 73,
      "beat_spy_pct": 53.1,
      "avg_pnl": 1.03,
      "avg_alpha": 1.17,
      "verdict": "✅ 初步有正 edge"
    },
    {
      "horizon": 5,
      "n": 28,
      "hit_rate": 57.1,
      "ci_lo": 39,
      "ci_hi": 75,
      "beat_spy_pct": 53.6,
      "avg_pnl": 2.3,
      "avg_alpha": 2.28,
      "verdict": "✅ 初步有正 edge"
    }
  ]
};
