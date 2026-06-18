// 信号 edge 分析 — analyze-signal-edge.py 自动生成
window.SIGNAL_EDGE = {
  "generated_at": "2026-06-18 15:30",
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
      "n": 20,
      "hit_rate": 70.0,
      "ci_lo": 50,
      "ci_hi": 90,
      "beat_spy_pct": 70.0,
      "avg_pnl": 2.38,
      "avg_alpha": 2.93,
      "verdict": "✅ 初步有正 edge"
    },
    {
      "horizon": 5,
      "n": 18,
      "hit_rate": 66.7,
      "ci_lo": 45,
      "ci_hi": 88,
      "beat_spy_pct": 66.7,
      "avg_pnl": 4.11,
      "avg_alpha": 4.76,
      "verdict": "✅ 初步有正 edge"
    }
  ]
};
