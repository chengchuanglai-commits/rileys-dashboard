// 信号 edge 分析 — analyze-signal-edge.py 自动生成
window.SIGNAL_EDGE = {
  "generated_at": "2026-07-20 12:34",
  "sample_total": 54,
  "date_range": [
    "2026-05-27",
    "2026-07-15"
  ],
  "benchmark": "SPY",
  "horizons": [
    {
      "horizon": 1,
      "n": 49,
      "hit_rate": 46.9,
      "ci_lo": 33,
      "ci_hi": 61,
      "beat_spy_pct": 42.9,
      "avg_pnl": 0.85,
      "avg_alpha": 0.91,
      "verdict": "⚠️ 与噪声难区分"
    },
    {
      "horizon": 3,
      "n": 47,
      "hit_rate": 55.3,
      "ci_lo": 41,
      "ci_hi": 70,
      "beat_spy_pct": 51.1,
      "avg_pnl": 0.71,
      "avg_alpha": 0.88,
      "verdict": "✅ 初步有正 edge"
    },
    {
      "horizon": 5,
      "n": 44,
      "hit_rate": 54.5,
      "ci_lo": 40,
      "ci_hi": 69,
      "beat_spy_pct": 56.8,
      "avg_pnl": 1.01,
      "avg_alpha": 1.39,
      "verdict": "✅ 初步有正 edge"
    }
  ]
};
