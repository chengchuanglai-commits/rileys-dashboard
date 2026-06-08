// Plan D 模拟盘持仓 — 每日自动更新
window.PORTFOLIO_D = {
  "capital_usd": 2000,
  "open_positions": [
    {
      "ticker": "TISI",
      "name": "TISI",
      "action": "SELL",
      "signal_date": "2026-06-08",
      "entry_price": 17.93,
      "allocated_usd": 500,
      "take_profit": 15.24,
      "stop_loss": 18.47,
      "max_hold_date": "2026-06-10",
      "gap_checked": true,
      "daily_prices": {
        "2026-06-08": {
          "close": 17.71,
          "pnl_pct": 1.23
        }
      },
      "day1_open": 17.55,
      "day1_gap_pct": -2.12
    },
    {
      "ticker": "TCNNF",
      "name": "TCNNF",
      "action": "SELL",
      "signal_date": "2026-06-09",
      "entry_price": 12.36,
      "allocated_usd": 500,
      "take_profit": 10.51,
      "stop_loss": 12.73,
      "max_hold_date": "2026-06-11",
      "gap_checked": true,
      "daily_prices": {
        "2026-06-08": {
          "close": 12.35,
          "pnl_pct": 0.08
        }
      },
      "day1_open": 12.15,
      "day1_gap_pct": -1.7
    },
    {
      "ticker": "STRS",
      "name": "STRS",
      "action": "SELL",
      "signal_date": "2026-06-09",
      "entry_price": 27.55,
      "allocated_usd": 500,
      "take_profit": 23.42,
      "stop_loss": 28.38,
      "max_hold_date": "2026-06-11",
      "gap_checked": true,
      "daily_prices": {
        "2026-06-08": {
          "close": 27.55,
          "pnl_pct": -0.0
        }
      },
      "day1_open": 27.6,
      "day1_gap_pct": 0.18
    }
  ],
  "closed_positions": [
    {
      "ticker": "UCTT",
      "name": "Ultra Clean Holdings Inc.",
      "action": "BUY",
      "signal_date": "2026-05-27",
      "entry_price": 87.46,
      "allocated_usd": 500,
      "take_profit": 100.58,
      "stop_loss": 84.84,
      "max_hold_date": "2026-05-29",
      "daily_prices": {
        "2026-05-28": {
          "open": 90.38,
          "high": 90.8,
          "low": 84.35,
          "close": 87.29,
          "pnl_pct": -3.0
        }
      },
      "close_date": "2026-05-28",
      "close_price": 84.84,
      "final_pnl_pct": -3.0,
      "close_reason": "stop_loss",
      "realized_pnl_usd": -15.0
    },
    {
      "ticker": "WTTR",
      "name": "Select Water Solutions Inc.",
      "action": "SELL",
      "signal_date": "2026-05-27",
      "entry_price": 19.35,
      "allocated_usd": 500,
      "take_profit": 16.45,
      "stop_loss": 19.93,
      "max_hold_date": "2026-05-29",
      "daily_prices": {
        "2026-05-28": {
          "open": 18.78,
          "high": 18.88,
          "low": 18.08,
          "close": 18.14,
          "pnl_pct": 6.25
        },
        "2026-05-29": {
          "open": 18.19,
          "high": 18.36,
          "low": 17.82,
          "close": 17.93,
          "pnl_pct": 7.34
        }
      },
      "close_date": "2026-05-29",
      "close_price": 17.93,
      "final_pnl_pct": 7.34,
      "close_reason": "max_hold",
      "realized_pnl_usd": 36.7
    },
    {
      "ticker": "MXL",
      "name": "MaxLinear Inc.",
      "action": "SELL",
      "signal_date": "2026-05-28",
      "entry_price": 101.1,
      "allocated_usd": 500,
      "take_profit": 85.93,
      "stop_loss": 104.13,
      "max_hold_date": "2026-06-01",
      "daily_prices": {
        "2026-05-29": {
          "open": 99.24,
          "high": 99.86,
          "low": 85.64,
          "close": 92.93,
          "pnl_pct": 15.0
        }
      },
      "close_date": "2026-05-29",
      "close_price": 85.93,
      "final_pnl_pct": 15.0,
      "close_reason": "take_profit",
      "realized_pnl_usd": 75.0
    },
    {
      "ticker": "ALGT",
      "name": "Allegiant Travel Company",
      "action": "SELL",
      "signal_date": "2026-05-28",
      "entry_price": 91.0,
      "allocated_usd": 500,
      "take_profit": 77.35,
      "stop_loss": 93.73,
      "max_hold_date": "2026-06-01",
      "daily_prices": {
        "2026-05-29": {
          "open": 90.73,
          "high": 93.68,
          "low": 89.87,
          "close": 91.61,
          "pnl_pct": -0.67
        },
        "2026-06-01": {
          "open": 88.79,
          "high": 89.99,
          "low": 85.02,
          "close": 89.16,
          "pnl_pct": 2.02
        }
      },
      "close_date": "2026-06-01",
      "close_price": 89.16,
      "final_pnl_pct": 2.02,
      "close_reason": "max_hold",
      "realized_pnl_usd": 10.1
    },
    {
      "ticker": "IMOS",
      "name": "ChipMOS Technologies",
      "action": "SELL",
      "signal_date": "2026-06-01",
      "entry_price": 67.75,
      "allocated_usd": 500,
      "take_profit": 57.59,
      "stop_loss": 69.78,
      "max_hold_date": "2026-06-03",
      "daily_prices": {
        "2026-06-02": {
          "open": 64.1,
          "high": 64.74,
          "low": 61.75,
          "close": 64.61,
          "pnl_pct": 4.63
        },
        "2026-06-03": {
          "open": 63.5,
          "high": 63.5,
          "low": 61.16,
          "close": 62.75,
          "pnl_pct": 7.38
        }
      },
      "close_date": "2026-06-03",
      "close_price": 62.75,
      "final_pnl_pct": 7.38,
      "close_reason": "max_hold",
      "realized_pnl_usd": 36.9
    },
    {
      "ticker": "MU",
      "name": "Micron Technology",
      "action": "BUY",
      "signal_date": "2026-06-02",
      "entry_price": 1036.48,
      "allocated_usd": 500,
      "take_profit": 1191.95,
      "stop_loss": 1005.39,
      "max_hold_date": "2026-06-04",
      "daily_prices": {
        "2026-06-03": {
          "open": 1079.01,
          "high": 1089.29,
          "low": 1038.5,
          "close": 1079.57,
          "pnl_pct": 4.16
        },
        "2026-06-04": {
          "open": 1007.1,
          "high": 1036.37,
          "low": 971.68,
          "close": 996.0,
          "pnl_pct": -3.0
        }
      },
      "close_date": "2026-06-04",
      "close_price": 1005.39,
      "final_pnl_pct": -3.0,
      "close_reason": "stop_loss",
      "realized_pnl_usd": -15.0
    },
    {
      "ticker": "KLIC",
      "name": "Kulicke and Soffa Industries Inc.",
      "action": "SELL",
      "signal_date": "2026-06-03",
      "entry_price": 108.36,
      "allocated_usd": 500,
      "take_profit": 92.11,
      "stop_loss": 111.61,
      "max_hold_date": "2026-06-05",
      "daily_prices": {
        "2026-06-04": {
          "open": 104.03,
          "high": 109.39,
          "low": 103.06,
          "close": 107.52,
          "pnl_pct": 0.78
        },
        "2026-06-05": {
          "open": 103.9,
          "high": 104.75,
          "low": 97.33,
          "close": 98.16,
          "pnl_pct": 9.41
        }
      },
      "close_date": "2026-06-05",
      "close_price": 98.16,
      "final_pnl_pct": 9.41,
      "close_reason": "max_hold",
      "realized_pnl_usd": 47.05
    },
    {
      "ticker": "LRCX",
      "name": "Lam Research Corporation",
      "action": "BUY",
      "signal_date": "2026-06-05",
      "entry_price": 318.5,
      "allocated_usd": 500,
      "take_profit": 366.27,
      "stop_loss": 308.94,
      "max_hold_date": "2026-06-09",
      "daily_prices": {
        "2026-06-05": {
          "close": 303.28,
          "pnl_pct": -4.78
        }
      },
      "gap_checked": true,
      "day1_open": 320.37,
      "day1_gap_pct": 0.59,
      "close_date": "2026-06-05",
      "close_price": 303.28,
      "final_pnl_pct": -4.78,
      "close_reason": "stop_loss",
      "realized_pnl_usd": -23.89
    }
  ],
  "_note": "Plan D 模拟盘：TP +15% / SL -3% / 最大2交易日 / 不利跳空>1%过滤",
  "stats": {
    "total_trades": 8,
    "win_trades": 5,
    "win_rate": 62.5,
    "total_realized_pnl_usd": 151.86,
    "open_unrealized_pnl_usd": 6.55,
    "portfolio_value": 2158.41,
    "skipped_gap": 3,
    "updated_at": "2026-06-09"
  }
};
