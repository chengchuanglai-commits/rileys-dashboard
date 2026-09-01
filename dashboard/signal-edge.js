// 信号 edge 分析 — analyze-signal-edge.py 自动生成
window.SIGNAL_EDGE = {
  "generated_at": "2026-09-01 16:41",
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
      "hit_rate": 49.0,
      "ci_lo": 35,
      "ci_hi": 63,
      "beat_spy_pct": 46.9,
      "avg_pnl": 1.61,
      "avg_alpha": 1.67,
      "verdict": "⚠️ 与噪声难区分"
    },
    {
      "horizon": 3,
      "n": 48,
      "hit_rate": 56.2,
      "ci_lo": 42,
      "ci_hi": 70,
      "beat_spy_pct": 54.2,
      "avg_pnl": 1.71,
      "avg_alpha": 1.84,
      "verdict": "✅ 初步有正 edge"
    },
    {
      "horizon": 5,
      "n": 48,
      "hit_rate": 56.2,
      "ci_lo": 42,
      "ci_hi": 70,
      "beat_spy_pct": 58.3,
      "avg_pnl": 1.86,
      "avg_alpha": 2.15,
      "verdict": "✅ 初步有正 edge"
    }
  ]
};
