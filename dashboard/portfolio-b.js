// Plan B 模拟盘持仓 — 每日自动更新
window.PORTFOLIO_B = {
  "capital_usd": 2000,
  "open_positions": [
    {
      "ticker": "MFIN",
      "name": "MFIN",
      "action": "SELL",
      "signal_date": "2026-06-11",
      "entry_price": 9.89,
      "allocated_usd": 500,
      "shares": 50,
      "actual_position_usd": 494.5,
      "entry_commission": 1.0,
      "take_profit": 9.1,
      "stop_loss": 10.29,
      "max_hold_date": "2026-06-18",
      "daily_prices": {
        "2026-06-12": {
          "close": 9.79,
          "pnl_pct": 1.01
        }
      }
    },
    {
      "ticker": "ARCB",
      "name": "ARCB",
      "action": "SELL",
      "signal_date": "2026-06-12",
      "entry_price": 173.6,
      "allocated_usd": 500,
      "shares": 2,
      "actual_position_usd": 347.2,
      "entry_commission": 1.0,
      "take_profit": 159.71,
      "stop_loss": 180.54,
      "max_hold_date": "2026-06-19",
      "daily_prices": {
        "2026-06-12": {
          "close": 175.97,
          "pnl_pct": -1.37
        }
      }
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
      "shares": 5,
      "actual_position_usd": 437.3,
      "entry_commission": 1.0,
      "take_profit": 94.46,
      "stop_loss": 83.96,
      "max_hold_date": "2026-06-03",
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
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -19.49
    },
    {
      "ticker": "WTTR",
      "name": "Select Water Solutions Inc.",
      "action": "SELL",
      "signal_date": "2026-05-27",
      "entry_price": 19.35,
      "allocated_usd": 500,
      "shares": 25,
      "actual_position_usd": 483.75,
      "entry_commission": 1.0,
      "take_profit": 17.8,
      "stop_loss": 20.12,
      "max_hold_date": "2026-06-03",
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
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 7.24
    },
    {
      "ticker": "MXL",
      "name": "MaxLinear Inc.",
      "action": "SELL",
      "signal_date": "2026-05-28",
      "entry_price": 101.1,
      "allocated_usd": 500,
      "shares": 4,
      "actual_position_usd": 404.4,
      "entry_commission": 1.0,
      "take_profit": 93.01,
      "stop_loss": 105.14,
      "max_hold_date": "2026-06-04",
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
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 30.35
    },
    {
      "ticker": "ALGT",
      "name": "Allegiant Travel Company",
      "action": "SELL",
      "signal_date": "2026-05-28",
      "entry_price": 91.0,
      "allocated_usd": 500,
      "shares": 5,
      "actual_position_usd": 455.0,
      "entry_commission": 1.0,
      "take_profit": 83.72,
      "stop_loss": 94.64,
      "max_hold_date": "2026-06-04",
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
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 34.4
    },
    {
      "ticker": "IMOS",
      "name": "ChipMOS Technologies",
      "action": "SELL",
      "signal_date": "2026-06-01",
      "entry_price": 67.75,
      "allocated_usd": 500,
      "shares": 7,
      "actual_position_usd": 474.25,
      "entry_commission": 1.0,
      "take_profit": 62.33,
      "stop_loss": 70.46,
      "max_hold_date": "2026-06-08",
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
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 35.94
    },
    {
      "ticker": "KLIC",
      "name": "Kulicke and Soffa Industries Inc.",
      "action": "SELL",
      "signal_date": "2026-06-03",
      "entry_price": 108.36,
      "allocated_usd": 500,
      "shares": 4,
      "actual_position_usd": 433.44,
      "entry_commission": 1.0,
      "take_profit": 99.69,
      "stop_loss": 112.69,
      "max_hold_date": "2026-06-10",
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
          "pnl_pct": 8.0
        }
      },
      "close_date": "2026-06-05",
      "close_price": 99.69,
      "final_pnl_pct": 8.0,
      "close_reason": "take_profit",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 32.68
    },
    {
      "ticker": "KLIC",
      "name": "Kulicke and Soffa Industries Inc.",
      "action": "BUY",
      "signal_date": "2026-06-04",
      "entry_price": 108.4,
      "allocated_usd": 500,
      "shares": 4,
      "actual_position_usd": 433.6,
      "entry_commission": 1.0,
      "take_profit": 117.07,
      "stop_loss": 104.06,
      "max_hold_date": "2026-06-11",
      "daily_prices": {
        "2026-06-05": {
          "open": 103.9,
          "high": 104.75,
          "low": 97.33,
          "close": 98.16,
          "pnl_pct": -4.0
        }
      },
      "close_date": "2026-06-05",
      "close_price": 104.06,
      "final_pnl_pct": -4.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -19.34
    },
    {
      "ticker": "LRCX",
      "name": "Lam Research Corporation",
      "action": "BUY",
      "signal_date": "2026-06-05",
      "entry_price": 318.5,
      "allocated_usd": 500,
      "shares": 1,
      "actual_position_usd": 318.5,
      "entry_commission": 1.0,
      "take_profit": 343.98,
      "stop_loss": 305.76,
      "max_hold_date": "2026-06-12",
      "daily_prices": {
        "2026-06-08": {
          "open": 318.55,
          "high": 330.68,
          "low": 315.0,
          "close": 324.45,
          "pnl_pct": 1.87
        },
        "2026-06-09": {
          "open": 335.5,
          "high": 349.09,
          "low": 306.01,
          "close": 327.16,
          "pnl_pct": 8.0
        }
      },
      "close_date": "2026-06-09",
      "close_price": 343.98,
      "final_pnl_pct": 8.0,
      "close_reason": "take_profit",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 23.48
    },
    {
      "ticker": "FLR",
      "name": "Fluor Corporation",
      "action": "SELL",
      "signal_date": "2026-06-05",
      "entry_price": 48.35,
      "allocated_usd": 500,
      "shares": 10,
      "actual_position_usd": 483.5,
      "entry_commission": 1.0,
      "take_profit": 44.48,
      "stop_loss": 50.28,
      "max_hold_date": "2026-06-12",
      "daily_prices": {
        "2026-06-08": {
          "open": 47.58,
          "high": 49.68,
          "low": 47.12,
          "close": 49.52,
          "pnl_pct": -2.42
        },
        "2026-06-09": {
          "open": 49.85,
          "high": 51.55,
          "low": 47.54,
          "close": 49.48,
          "pnl_pct": -3.99
        }
      },
      "close_date": "2026-06-09",
      "close_price": 50.28,
      "final_pnl_pct": -3.99,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -21.29
    },
    {
      "ticker": "TISI",
      "name": "TISI",
      "action": "SELL",
      "signal_date": "2026-06-08",
      "entry_price": 17.93,
      "allocated_usd": 500,
      "shares": 27,
      "actual_position_usd": 484.11,
      "entry_commission": 1.0,
      "take_profit": 16.5,
      "stop_loss": 18.65,
      "max_hold_date": "2026-06-15",
      "daily_prices": {
        "2026-06-09": {
          "open": 17.79,
          "high": 18.5,
          "low": 16.94,
          "close": 17.5,
          "pnl_pct": 2.4
        },
        "2026-06-10": {
          "open": 17.71,
          "high": 17.86,
          "low": 16.14,
          "close": 16.34,
          "pnl_pct": 7.98
        }
      },
      "close_date": "2026-06-10",
      "close_price": 16.5,
      "final_pnl_pct": 7.98,
      "close_reason": "take_profit",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 36.63
    },
    {
      "ticker": "VLGEA",
      "name": "VLGEA",
      "action": "SELL",
      "signal_date": "2026-06-08",
      "entry_price": 39.33,
      "allocated_usd": 500,
      "shares": 12,
      "actual_position_usd": 471.96,
      "entry_commission": 1.0,
      "take_profit": 36.18,
      "stop_loss": 40.9,
      "max_hold_date": "2026-06-15",
      "daily_prices": {
        "2026-06-09": {
          "open": 39.43,
          "high": 40.93,
          "low": 39.37,
          "close": 39.7,
          "pnl_pct": -3.99
        }
      },
      "close_date": "2026-06-09",
      "close_price": 40.9,
      "final_pnl_pct": -3.99,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -20.83
    },
    {
      "ticker": "TCNNF",
      "name": "TCNNF",
      "action": "SELL",
      "signal_date": "2026-06-09",
      "entry_price": 12.36,
      "allocated_usd": 500,
      "shares": 40,
      "actual_position_usd": 494.4,
      "entry_commission": 1.0,
      "take_profit": 11.37,
      "stop_loss": 12.85,
      "max_hold_date": "2026-06-16",
      "daily_prices": {
        "2026-06-10": {
          "open": 11.78,
          "high": 12.3,
          "low": 10.85,
          "close": 11.5,
          "pnl_pct": 8.01
        }
      },
      "close_date": "2026-06-10",
      "close_price": 11.37,
      "final_pnl_pct": 8.01,
      "close_reason": "take_profit",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 37.6
    },
    {
      "ticker": "STRS",
      "name": "STRS",
      "action": "SELL",
      "signal_date": "2026-06-09",
      "entry_price": 27.55,
      "allocated_usd": 500,
      "shares": 18,
      "actual_position_usd": 495.9,
      "entry_commission": 1.0,
      "take_profit": 25.35,
      "stop_loss": 28.65,
      "max_hold_date": "2026-06-16",
      "daily_prices": {
        "2026-06-10": {
          "open": 28.98,
          "high": 29.4,
          "low": 28.49,
          "close": 28.89,
          "pnl_pct": -3.99
        }
      },
      "close_date": "2026-06-10",
      "close_price": 28.65,
      "final_pnl_pct": -3.99,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -21.79
    },
    {
      "ticker": "PBHC",
      "name": "PBHC",
      "action": "SELL",
      "signal_date": "2026-06-11",
      "entry_price": 15.2,
      "allocated_usd": 500,
      "shares": 32,
      "actual_position_usd": 486.4,
      "entry_commission": 1.0,
      "take_profit": 13.98,
      "stop_loss": 15.81,
      "max_hold_date": "2026-06-18",
      "daily_prices": {
        "2026-06-12": {
          "open": 14.88,
          "high": 15.4,
          "low": 13.72,
          "close": 15.4,
          "pnl_pct": 8.03
        }
      },
      "close_date": "2026-06-12",
      "close_price": 13.98,
      "final_pnl_pct": 8.03,
      "close_reason": "take_profit",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 37.06
    },
    {
      "ticker": "ARCB",
      "name": "ARCB",
      "action": "SELL",
      "signal_date": "2026-06-11",
      "entry_price": 169.06,
      "allocated_usd": 500,
      "shares": 2,
      "actual_position_usd": 338.12,
      "entry_commission": 1.0,
      "take_profit": 155.54,
      "stop_loss": 175.82,
      "max_hold_date": "2026-06-18",
      "daily_prices": {
        "2026-06-12": {
          "open": 174.6,
          "high": 176.54,
          "low": 171.75,
          "close": 175.97,
          "pnl_pct": -4.0
        }
      },
      "close_date": "2026-06-12",
      "close_price": 175.82,
      "final_pnl_pct": -4.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -15.52
    },
    {
      "ticker": "CBRL",
      "name": "CBRL",
      "action": "SELL",
      "signal_date": "2026-06-11",
      "entry_price": 43.76,
      "allocated_usd": 500,
      "shares": 11,
      "actual_position_usd": 481.36,
      "entry_commission": 1.0,
      "take_profit": 40.26,
      "stop_loss": 45.51,
      "max_hold_date": "2026-06-18",
      "daily_prices": {
        "2026-06-12": {
          "open": 46.72,
          "high": 47.76,
          "low": 44.64,
          "close": 47.25,
          "pnl_pct": -4.0
        }
      },
      "close_date": "2026-06-12",
      "close_price": 45.51,
      "final_pnl_pct": -4.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -21.25
    }
  ],
  "_note": "Plan B 模拟盘：TP +8% / SL -4% / 最大5交易日 / IBKR佣金$0.005/股min$1",
  "stats": {
    "total_trades": 16,
    "win_trades": 9,
    "win_rate": 56.2,
    "total_realized_pnl_usd": 135.87,
    "open_unrealized_pnl_usd": -1.8,
    "portfolio_value": 2134.07,
    "updated_at": "2026-06-13"
  }
};
