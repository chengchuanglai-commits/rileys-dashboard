// Plan C 模拟盘持仓 — 每日自动更新（跳空过滤版）
window.PORTFOLIO_C = {
  "capital_usd": 2000,
  "open_positions": [
    {
      "ticker": "KLIC",
      "name": "Kulicke and Soffa Industries Inc.",
      "action": "SELL",
      "signal_date": "2026-06-03",
      "entry_price": 108.36,
      "allocated_usd": 500,
      "take_profit": 99.69,
      "stop_loss": 112.69,
      "max_hold_date": "2026-06-10",
      "day1_open": 103.9,
      "daily_prices": {
        "2026-06-04": {
          "open": 104.03,
          "high": 109.39,
          "low": 103.06,
          "close": 107.52,
          "pnl_pct": 0.78
        },
        "2026-06-05": {
          "close": 101.11,
          "pnl_pct": 6.69
        }
      },
      "gap_checked": true,
      "day1_gap_pct": -4.12
    },
    {
      "ticker": "ADMA",
      "name": "ADMA Biologics",
      "action": "SELL",
      "signal_date": "2026-06-05",
      "entry_price": 7.98,
      "allocated_usd": 500,
      "take_profit": 7.34,
      "stop_loss": 8.3,
      "max_hold_date": "2026-06-12",
      "day1_open": 8.07,
      "daily_prices": {
        "2026-06-05": {
          "close": 8.02,
          "pnl_pct": -0.5
        }
      },
      "gap_checked": true,
      "day1_gap_pct": 1.13
    },
    {
      "ticker": "LRCX",
      "name": "Lam Research Corporation",
      "action": "BUY",
      "signal_date": "2026-06-05",
      "entry_price": 318.5,
      "allocated_usd": 500,
      "take_profit": 343.98,
      "stop_loss": 305.76,
      "max_hold_date": "2026-06-12",
      "gap_checked": true,
      "daily_prices": {
        "2026-06-05": {
          "close": 316.9,
          "pnl_pct": -0.5
        }
      },
      "day1_open": 318.74,
      "day1_gap_pct": 0.08
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
      "take_profit": 94.46,
      "stop_loss": 83.96,
      "max_hold_date": "2026-06-03",
      "day1_open": 90.38,
      "daily_prices": {
        "2026-05-28": {
          "open": 90.38,
          "high": 90.8,
          "low": 84.35,
          "close": 87.29,
          "pnl_pct": -0.19
        },
        "2026-05-29": {
          "open": 88.11,
          "high": 89.34,
          "low": 83.23,
          "close": 85.57,
          "pnl_pct": -4.0
        }
      },
      "close_date": "2026-05-29",
      "close_price": 83.96,
      "final_pnl_pct": -4.0,
      "close_reason": "stop_loss",
      "realized_pnl_usd": -20.0
    },
    {
      "ticker": "WTTR",
      "name": "Select Water Solutions Inc.",
      "action": "SELL",
      "signal_date": "2026-05-27",
      "entry_price": 19.35,
      "allocated_usd": 500,
      "take_profit": 17.8,
      "stop_loss": 20.12,
      "max_hold_date": "2026-06-03",
      "day1_open": 18.78,
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
        },
        "2026-06-01": {
          "open": 18.14,
          "high": 18.44,
          "low": 17.86,
          "close": 18.38,
          "pnl_pct": 5.01
        },
        "2026-06-02": {
          "open": 18.51,
          "high": 19.02,
          "low": 18.45,
          "close": 18.86,
          "pnl_pct": 2.53
        },
        "2026-06-03": {
          "open": 18.99,
          "high": 19.12,
          "low": 18.79,
          "close": 18.98,
          "pnl_pct": 1.91
        }
      },
      "close_date": "2026-06-03",
      "close_price": 18.98,
      "final_pnl_pct": 1.91,
      "close_reason": "max_hold",
      "realized_pnl_usd": 9.55
    },
    {
      "ticker": "MXL",
      "name": "MaxLinear Inc.",
      "action": "SELL",
      "signal_date": "2026-05-28",
      "entry_price": 101.1,
      "allocated_usd": 500,
      "take_profit": 93.01,
      "stop_loss": 105.14,
      "max_hold_date": "2026-06-04",
      "day1_open": 99.24,
      "daily_prices": {
        "2026-05-29": {
          "open": 99.24,
          "high": 99.86,
          "low": 85.64,
          "close": 92.93,
          "pnl_pct": 8.0
        }
      },
      "close_date": "2026-05-29",
      "close_price": 93.01,
      "final_pnl_pct": 8.0,
      "close_reason": "take_profit",
      "realized_pnl_usd": 40.0
    },
    {
      "ticker": "ALGT",
      "name": "Allegiant Travel Company",
      "action": "SELL",
      "signal_date": "2026-05-28",
      "entry_price": 91.0,
      "allocated_usd": 500,
      "take_profit": 83.72,
      "stop_loss": 94.64,
      "max_hold_date": "2026-06-04",
      "day1_open": 90.73,
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
        },
        "2026-06-02": {
          "open": 90.7,
          "high": 90.7,
          "low": 87.02,
          "close": 87.67,
          "pnl_pct": 3.66
        },
        "2026-06-03": {
          "open": 86.15,
          "high": 86.24,
          "low": 82.62,
          "close": 82.98,
          "pnl_pct": 8.0
        }
      },
      "close_date": "2026-06-03",
      "close_price": 83.72,
      "final_pnl_pct": 8.0,
      "close_reason": "take_profit",
      "realized_pnl_usd": 40.0
    },
    {
      "ticker": "IMOS",
      "name": "ChipMOS Technologies",
      "action": "SELL",
      "signal_date": "2026-06-01",
      "entry_price": 67.75,
      "allocated_usd": 500,
      "take_profit": 62.33,
      "stop_loss": 70.46,
      "max_hold_date": "2026-06-08",
      "day1_open": 64.1,
      "daily_prices": {
        "2026-06-02": {
          "open": 64.1,
          "high": 64.74,
          "low": 61.75,
          "close": 64.61,
          "pnl_pct": 8.0
        }
      },
      "close_date": "2026-06-02",
      "close_price": 62.33,
      "final_pnl_pct": 8.0,
      "close_reason": "take_profit",
      "realized_pnl_usd": 40.0
    },
    {
      "ticker": "MU",
      "name": "Micron Technology",
      "action": "BUY",
      "signal_date": "2026-06-02",
      "entry_price": 1036.48,
      "allocated_usd": 500,
      "take_profit": 1119.4,
      "stop_loss": 995.02,
      "max_hold_date": "2026-06-09",
      "day1_open": 1079.01,
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
          "pnl_pct": -4.0
        }
      },
      "close_date": "2026-06-04",
      "close_price": 995.02,
      "final_pnl_pct": -4.0,
      "close_reason": "stop_loss",
      "realized_pnl_usd": -20.0
    },
    {
      "ticker": "OKLO",
      "name": "Oklo Inc.",
      "action": "SELL",
      "signal_date": "2026-06-05",
      "entry_price": 65.39,
      "allocated_usd": 500,
      "take_profit": 60.16,
      "stop_loss": 68.01,
      "max_hold_date": "2026-06-12",
      "day1_open": 64.8,
      "daily_prices": {
        "2026-06-05": {
          "close": 59.35,
          "pnl_pct": 9.24
        }
      },
      "gap_checked": true,
      "day1_gap_pct": -0.9,
      "close_date": "2026-06-05",
      "close_price": 59.35,
      "final_pnl_pct": 9.24,
      "close_reason": "take_profit",
      "realized_pnl_usd": 46.18
    }
  ],
  "_note": "Plan C 模拟盘：TP +8% / SL -4% / 最大5交易日 / 不利跳空>1.5%跳过",
  "stats": {
    "total_trades": 7,
    "win_trades": 5,
    "win_rate": 71.4,
    "total_realized_pnl_usd": 135.73,
    "open_unrealized_pnl_usd": 28.45,
    "portfolio_value": 2164.18,
    "skipped_gap": 2,
    "updated_at": "2026-06-06"
  }
};
