// 信号 edge 分析 — analyze-signal-edge.py 自动生成
window.SIGNAL_EDGE = {
  "generated_at": "2026-06-24 12:33",
  "sample_total": 34,
  "date_range": [
    "2026-05-27",
    "2026-06-24"
  ],
  "benchmark": "SPY",
  "horizons": [
    {
      "horizon": 1,
      "n": 28,
      "hit_rate": 42.9,
      "ci_lo": 25,
      "ci_hi": 61,
      "beat_spy_pct": 39.3,
      "avg_pnl": 0.87,
      "avg_alpha": 0.69,
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
      "n": 19,
      "hit_rate": 68.4,
      "ci_lo": 48,
      "ci_hi": 89,
      "beat_spy_pct": 63.2,
      "avg_pnl": 3.28,
      "avg_alpha": 3.8,
      "verdict": "✅ 初步有正 edge"
    }
  ]
};
