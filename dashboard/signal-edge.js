// 信号 edge 分析 — analyze-signal-edge.py 自动生成
window.SIGNAL_EDGE = {
  "generated_at": "2026-06-18 11:47",
  "sample_total": 25,
  "date_range": [
    "2026-05-27",
    "2026-06-18"
  ],
  "benchmark": "SPY",
  "horizons": [
    {
      "horizon": 1,
      "n": 23,
      "hit_rate": 47.8,
      "ci_lo": 27,
      "ci_hi": 68,
      "beat_spy_pct": 47.8,
      "avg_pnl": 0.45,
      "avg_alpha": 0.46,
      "verdict": "⚠️ 与噪声难区分"
    },
    {
      "horizon": 3,
      "n": 19,
      "hit_rate": 68.4,
      "ci_lo": 48,
      "ci_hi": 89,
      "beat_spy_pct": 68.4,
      "avg_pnl": 2.33,
      "avg_alpha": 2.97,
      "verdict": "✅ 初步有正 edge"
    },
    {
      "horizon": 5,
      "n": 14,
      "hit_rate": 71.4,
      "ci_lo": 48,
      "ci_hi": 95,
      "beat_spy_pct": 71.4,
      "avg_pnl": 4.98,
      "avg_alpha": 5.53,
      "verdict": "✅ 初步有正 edge"
    }
  ]
};
