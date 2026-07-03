// 信号 edge 分析 — analyze-signal-edge.py 自动生成
window.SIGNAL_EDGE = {
  "generated_at": "2026-07-03 13:38",
  "sample_total": 45,
  "date_range": [
    "2026-05-27",
    "2026-07-03"
  ],
  "benchmark": "SPY",
  "horizons": [
    {
      "horizon": 1,
      "n": 36,
      "hit_rate": 38.9,
      "ci_lo": 23,
      "ci_hi": 55,
      "beat_spy_pct": 36.1,
      "avg_pnl": 0.16,
      "avg_alpha": 0.12,
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
      "n": 32,
      "hit_rate": 53.1,
      "ci_lo": 36,
      "ci_hi": 70,
      "beat_spy_pct": 50.0,
      "avg_pnl": 1.79,
      "avg_alpha": 1.99,
      "verdict": "✅ 初步有正 edge"
    }
  ]
};
