// 信号 edge 分析 — analyze-signal-edge.py 自动生成
window.SIGNAL_EDGE = {
  "generated_at": "2026-07-16 11:43",
  "sample_total": 54,
  "date_range": [
    "2026-05-27",
    "2026-07-15"
  ],
  "benchmark": "SPY",
  "horizons": [
    {
      "horizon": 1,
      "n": 47,
      "hit_rate": 44.7,
      "ci_lo": 30,
      "ci_hi": 59,
      "beat_spy_pct": 40.4,
      "avg_pnl": 0.19,
      "avg_alpha": 0.3,
      "verdict": "⚠️ 与噪声难区分"
    },
    {
      "horizon": 3,
      "n": 44,
      "hit_rate": 56.8,
      "ci_lo": 42,
      "ci_hi": 71,
      "beat_spy_pct": 54.5,
      "avg_pnl": 0.78,
      "avg_alpha": 1.0,
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
