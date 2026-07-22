// 信号 edge 分析 — analyze-signal-edge.py 自动生成
window.SIGNAL_EDGE = {
  "generated_at": "2026-07-22 12:35",
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
      "hit_rate": 46.9,
      "ci_lo": 33,
      "ci_hi": 61,
      "beat_spy_pct": 42.9,
      "avg_pnl": 0.85,
      "avg_alpha": 0.91,
      "verdict": "⚠️ 与噪声难区分"
    },
    {
      "horizon": 3,
      "n": 48,
      "hit_rate": 56.2,
      "ci_lo": 42,
      "ci_hi": 70,
      "beat_spy_pct": 52.1,
      "avg_pnl": 0.94,
      "avg_alpha": 1.06,
      "verdict": "✅ 初步有正 edge"
    },
    {
      "horizon": 5,
      "n": 47,
      "hit_rate": 55.3,
      "ci_lo": 41,
      "ci_hi": 70,
      "beat_spy_pct": 55.3,
      "avg_pnl": 0.91,
      "avg_alpha": 1.22,
      "verdict": "✅ 初步有正 edge"
    }
  ]
};
