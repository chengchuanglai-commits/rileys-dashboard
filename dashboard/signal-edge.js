// 信号 edge 分析 — analyze-signal-edge.py 自动生成
window.SIGNAL_EDGE = {
  "generated_at": "2026-06-22 17:30",
  "sample_total": 30,
  "date_range": [
    "2026-05-27",
    "2026-06-22"
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
      "avg_pnl": 0.33,
      "avg_alpha": 0.32,
      "verdict": "⚠️ 与噪声难区分"
    },
    {
      "horizon": 3,
      "n": 23,
      "hit_rate": 65.2,
      "ci_lo": 46,
      "ci_hi": 85,
      "beat_spy_pct": 60.9,
      "avg_pnl": 1.75,
      "avg_alpha": 2.18,
      "verdict": "✅ 初步有正 edge"
    },
    {
      "horizon": 5,
      "n": 19,
      "hit_rate": 68.4,
      "ci_lo": 48,
      "ci_hi": 89,
      "beat_spy_pct": 68.4,
      "avg_pnl": 4.43,
      "avg_alpha": 5.17,
      "verdict": "✅ 初步有正 edge"
    }
  ]
};
