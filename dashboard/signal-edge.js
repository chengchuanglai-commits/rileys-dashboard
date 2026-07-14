// 信号 edge 分析 — analyze-signal-edge.py 自动生成
window.SIGNAL_EDGE = {
  "generated_at": "2026-07-14 12:28",
  "sample_total": 53,
  "date_range": [
    "2026-05-27",
    "2026-07-14"
  ],
  "benchmark": "SPY",
  "horizons": [
    {
      "horizon": 1,
      "n": 45,
      "hit_rate": 44.4,
      "ci_lo": 30,
      "ci_hi": 59,
      "beat_spy_pct": 40.0,
      "avg_pnl": 0.84,
      "avg_alpha": 0.9,
      "verdict": "⚠️ 与噪声难区分"
    },
    {
      "horizon": 3,
      "n": 41,
      "hit_rate": 56.1,
      "ci_lo": 41,
      "ci_hi": 71,
      "beat_spy_pct": 53.7,
      "avg_pnl": 0.78,
      "avg_alpha": 1.01,
      "verdict": "✅ 初步有正 edge"
    },
    {
      "horizon": 5,
      "n": 41,
      "hit_rate": 56.1,
      "ci_lo": 41,
      "ci_hi": 71,
      "beat_spy_pct": 58.5,
      "avg_pnl": 1.26,
      "avg_alpha": 1.68,
      "verdict": "✅ 初步有正 edge"
    }
  ]
};
