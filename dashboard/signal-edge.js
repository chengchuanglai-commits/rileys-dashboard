// 信号 edge 分析 — analyze-signal-edge.py 自动生成
window.SIGNAL_EDGE = {
  "generated_at": "2026-06-25 12:33",
  "sample_total": 34,
  "date_range": [
    "2026-05-27",
    "2026-06-24"
  ],
  "benchmark": "SPY",
  "horizons": [
    {
      "horizon": 1,
      "n": 29,
      "hit_rate": 41.4,
      "ci_lo": 23,
      "ci_hi": 59,
      "beat_spy_pct": 37.9,
      "avg_pnl": 0.83,
      "avg_alpha": 0.66,
      "verdict": "⚠️ 与噪声难区分"
    },
    {
      "horizon": 3,
      "n": 24,
      "hit_rate": 58.3,
      "ci_lo": 39,
      "ci_hi": 78,
      "beat_spy_pct": 58.3,
      "avg_pnl": 0.75,
      "avg_alpha": 0.98,
      "verdict": "✅ 初步有正 edge"
    },
    {
      "horizon": 5,
      "n": 22,
      "hit_rate": 59.1,
      "ci_lo": 39,
      "ci_hi": 80,
      "beat_spy_pct": 54.5,
      "avg_pnl": 1.66,
      "avg_alpha": 1.83,
      "verdict": "✅ 初步有正 edge"
    }
  ]
};
