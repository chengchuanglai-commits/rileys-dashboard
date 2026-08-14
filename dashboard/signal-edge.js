// 信号 edge 分析 — analyze-signal-edge.py 自动生成
window.SIGNAL_EDGE = {
  "generated_at": "2026-08-14 14:00",
  "sample_total": 54,
  "date_range": [
    "2026-05-27",
    "2026-07-15"
  ],
  "benchmark": "SPY",
  "horizons": [
    {
      "horizon": 1,
      "n": 48,
      "hit_rate": 45.8,
      "ci_lo": 32,
      "ci_hi": 60,
      "beat_spy_pct": 43.8,
      "avg_pnl": 0.97,
      "avg_alpha": 1.06,
      "verdict": "⚠️ 与噪声难区分"
    },
    {
      "horizon": 3,
      "n": 48,
      "hit_rate": 56.2,
      "ci_lo": 42,
      "ci_hi": 70,
      "beat_spy_pct": 54.2,
      "avg_pnl": 1.64,
      "avg_alpha": 1.76,
      "verdict": "✅ 初步有正 edge"
    },
    {
      "horizon": 5,
      "n": 48,
      "hit_rate": 56.2,
      "ci_lo": 42,
      "ci_hi": 70,
      "beat_spy_pct": 56.2,
      "avg_pnl": 1.79,
      "avg_alpha": 2.07,
      "verdict": "✅ 初步有正 edge"
    }
  ]
};
