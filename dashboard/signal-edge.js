// 信号 edge 分析 — analyze-signal-edge.py 自动生成
window.SIGNAL_EDGE = {
  "generated_at": "2026-07-10 13:49",
  "sample_total": 50,
  "date_range": [
    "2026-05-27",
    "2026-07-09"
  ],
  "benchmark": "SPY",
  "horizons": [
    {
      "horizon": 1,
      "n": 45,
      "hit_rate": 40.0,
      "ci_lo": 26,
      "ci_hi": 54,
      "beat_spy_pct": 35.6,
      "avg_pnl": 0.1,
      "avg_alpha": 0.14,
      "verdict": "❌ 无 edge"
    },
    {
      "horizon": 3,
      "n": 42,
      "hit_rate": 54.8,
      "ci_lo": 40,
      "ci_hi": 70,
      "beat_spy_pct": 52.4,
      "avg_pnl": 0.84,
      "avg_alpha": 1.09,
      "verdict": "✅ 初步有正 edge"
    },
    {
      "horizon": 5,
      "n": 40,
      "hit_rate": 50.0,
      "ci_lo": 35,
      "ci_hi": 65,
      "beat_spy_pct": 52.5,
      "avg_pnl": 1.18,
      "avg_alpha": 1.63,
      "verdict": "⚠️ 与噪声难区分"
    }
  ]
};
