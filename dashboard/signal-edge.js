// 信号 edge 分析 — analyze-signal-edge.py 自动生成
window.SIGNAL_EDGE = {
  "generated_at": "2026-06-16 11:47",
  "sample_total": 23,
  "date_range": [
    "2026-05-27",
    "2026-06-16"
  ],
  "benchmark": "SPY",
  "horizons": [
    {
      "horizon": 1,
      "n": 18,
      "hit_rate": 50.0,
      "ci_lo": 27,
      "ci_hi": 73,
      "beat_spy_pct": 50.0,
      "avg_pnl": 0.37,
      "avg_alpha": 0.52,
      "verdict": "⚠️ 与噪声难区分"
    },
    {
      "horizon": 3,
      "n": 14,
      "hit_rate": 64.3,
      "ci_lo": 39,
      "ci_hi": 89,
      "beat_spy_pct": 64.3,
      "avg_pnl": 1.82,
      "avg_alpha": 2.22,
      "verdict": "✅ 初步有正 edge"
    },
    {
      "horizon": 5,
      "n": 10,
      "hit_rate": 80.0,
      "ci_lo": 55,
      "ci_hi": 100,
      "beat_spy_pct": 80.0,
      "avg_pnl": 4.78,
      "avg_alpha": 4.76,
      "verdict": "✅ 初步有正 edge"
    }
  ]
};
