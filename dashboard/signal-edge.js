// 信号 edge 分析 — analyze-signal-edge.py 自动生成
window.SIGNAL_EDGE = {
  "generated_at": "2026-07-01 11:49",
  "sample_total": 38,
  "date_range": [
    "2026-05-27",
    "2026-07-01"
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
      "avg_pnl": 0.14,
      "avg_alpha": 0.1,
      "verdict": "❌ 无 edge"
    },
    {
      "horizon": 3,
      "n": 32,
      "hit_rate": 56.2,
      "ci_lo": 39,
      "ci_hi": 73,
      "beat_spy_pct": 53.1,
      "avg_pnl": 1.06,
      "avg_alpha": 1.2,
      "verdict": "✅ 初步有正 edge"
    },
    {
      "horizon": 5,
      "n": 29,
      "hit_rate": 55.2,
      "ci_lo": 37,
      "ci_hi": 73,
      "beat_spy_pct": 51.7,
      "avg_pnl": 2.09,
      "avg_alpha": 2.13,
      "verdict": "✅ 初步有正 edge"
    }
  ]
};
