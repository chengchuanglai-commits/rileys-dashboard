// Plan D 模拟盘持仓 — 每日自动更新
window.PORTFOLIO_D = {
  "capital_usd": 2000,
  "open_positions": [
    {
      "ticker": "SRRK",
      "name": "SRRK",
      "action": "SELL",
      "signal_date": "2026-07-01",
      "entry_price": 55.0,
      "allocated_usd": 500,
      "shares": 9,
      "actual_position_usd": 495.0,
      "entry_commission": 1.0,
      "take_profit": 46.75,
      "stop_loss": 56.65,
      "max_hold_date": "2026-07-03",
      "daily_prices": {
        "2026-07-02": {
          "close": 52.6,
          "pnl_pct": 4.36
        }
      },
      "gap_checked": true,
      "day1_open": 52.8,
      "day1_gap_pct": -4.0
    },
    {
      "ticker": "LGND",
      "name": "LGND",
      "action": "SELL",
      "signal_date": "2026-07-02",
      "entry_price": 312.01,
      "allocated_usd": 500,
      "shares": 1,
      "actual_position_usd": 312.01,
      "entry_commission": 1.0,
      "take_profit": 265.21,
      "stop_loss": 321.37,
      "max_hold_date": "2026-07-06",
      "daily_prices": {
        "2026-07-02": {
          "close": 311.49,
          "pnl_pct": 0.17
        }
      },
      "gap_checked": true,
      "day1_open": 314.81,
      "day1_gap_pct": 0.9
    },
    {
      "ticker": "MVBF",
      "name": "MVBF",
      "action": "SELL",
      "signal_date": "2026-07-02",
      "entry_price": 29.84,
      "allocated_usd": 500,
      "shares": 16,
      "actual_position_usd": 477.44,
      "entry_commission": 1.0,
      "take_profit": 25.36,
      "stop_loss": 30.74,
      "max_hold_date": "2026-07-06",
      "daily_prices": {
        "2026-07-02": {
          "close": 29.62,
          "pnl_pct": 0.74
        }
      },
      "gap_checked": true,
      "day1_open": 29.99,
      "day1_gap_pct": 0.5
    },
    {
      "ticker": "DGII",
      "name": "DGII",
      "action": "SELL",
      "signal_date": "2026-07-02",
      "entry_price": 74.12,
      "allocated_usd": 500,
      "shares": 6,
      "actual_position_usd": 444.72,
      "entry_commission": 1.0,
      "take_profit": 63.0,
      "stop_loss": 76.34,
      "max_hold_date": "2026-07-06",
      "daily_prices": {
        "2026-07-02": {
          "close": 72.71,
          "pnl_pct": 1.9
        }
      },
      "gap_checked": true,
      "day1_open": 73.97,
      "day1_gap_pct": -0.2
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
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -15.12
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
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 33.51
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
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 58.66
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
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 7.19
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
      "take_profit": 57.59,
      "stop_loss": 69.78,
      "max_hold_date": "2026-06-03",
      "daily_prices": {
        "2026-06-02": {
          "open": 63.27,
          "high": 63.9,
          "low": 60.95,
          "close": 63.77,
          "pnl_pct": 5.87
        },
        "2026-06-03": {
          "open": 62.68,
          "high": 62.68,
          "low": 60.37,
          "close": 61.94,
          "pnl_pct": 8.58
        }
      },
      "close_date": "2026-06-03",
      "close_price": 61.94,
      "final_pnl_pct": 8.58,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 38.69
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
      "take_profit": 92.11,
      "stop_loss": 111.61,
      "max_hold_date": "2026-06-05",
      "daily_prices": {
        "2026-06-04": {
          "open": 103.85,
          "high": 109.2,
          "low": 102.88,
          "close": 107.33,
          "pnl_pct": 0.95
        },
        "2026-06-05": {
          "open": 103.72,
          "high": 104.57,
          "low": 97.16,
          "close": 97.99,
          "pnl_pct": 9.57
        }
      },
      "close_date": "2026-06-05",
      "close_price": 97.99,
      "final_pnl_pct": 9.57,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 39.48
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
      "take_profit": 366.27,
      "stop_loss": 308.94,
      "max_hold_date": "2026-06-09",
      "daily_prices": {
        "2026-06-08": {
          "open": 318.33,
          "high": 330.45,
          "low": 314.78,
          "close": 324.22,
          "pnl_pct": 1.8
        },
        "2026-06-09": {
          "open": 335.26,
          "high": 348.84,
          "low": 305.79,
          "close": 326.93,
          "pnl_pct": -3.0
        }
      },
      "close_date": "2026-06-09",
      "close_price": 308.94,
      "final_pnl_pct": -3.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -11.55
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
      "take_profit": 41.1,
      "stop_loss": 49.8,
      "max_hold_date": "2026-06-09",
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
          "pnl_pct": -3.0
        }
      },
      "close_date": "2026-06-09",
      "close_price": 49.8,
      "final_pnl_pct": -3.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -16.51
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
      "take_profit": 15.24,
      "stop_loss": 18.47,
      "max_hold_date": "2026-06-10",
      "daily_prices": {
        "2026-06-09": {
          "open": 17.79,
          "high": 18.5,
          "low": 16.94,
          "close": 17.5,
          "pnl_pct": -3.01
        }
      },
      "close_date": "2026-06-09",
      "close_price": 18.47,
      "final_pnl_pct": -3.01,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -16.57
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
      "take_profit": 33.43,
      "stop_loss": 40.51,
      "max_hold_date": "2026-06-10",
      "daily_prices": {
        "2026-06-09": {
          "open": 39.43,
          "high": 40.93,
          "low": 39.37,
          "close": 39.7,
          "pnl_pct": -3.0
        }
      },
      "close_date": "2026-06-09",
      "close_price": 40.51,
      "final_pnl_pct": -3.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -16.16
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
      "take_profit": 12.92,
      "stop_loss": 15.66,
      "max_hold_date": "2026-06-15",
      "daily_prices": {
        "2026-06-12": {
          "open": 14.88,
          "high": 15.45,
          "low": 13.72,
          "close": 15.45,
          "pnl_pct": -1.64
        },
        "2026-06-15": {
          "open": 16.08,
          "high": 16.88,
          "low": 15.22,
          "close": 15.22,
          "pnl_pct": -3.03
        }
      },
      "close_date": "2026-06-15",
      "close_price": 15.66,
      "final_pnl_pct": -3.03,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -16.74
    },
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
      "take_profit": 8.41,
      "stop_loss": 10.19,
      "max_hold_date": "2026-06-15",
      "daily_prices": {
        "2026-06-12": {
          "open": 9.71,
          "high": 9.95,
          "low": 9.71,
          "close": 9.81,
          "pnl_pct": 0.81
        },
        "2026-06-15": {
          "open": 9.82,
          "high": 9.92,
          "low": 9.76,
          "close": 9.85,
          "pnl_pct": 0.4
        }
      },
      "close_date": "2026-06-15",
      "close_price": 9.85,
      "final_pnl_pct": 0.4,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -0.02
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
      "take_profit": 147.56,
      "stop_loss": 178.81,
      "max_hold_date": "2026-06-16",
      "daily_prices": {
        "2026-06-15": {
          "open": 172.51,
          "high": 172.79,
          "low": 162.32,
          "close": 164.1,
          "pnl_pct": 5.47
        },
        "2026-06-16": {
          "open": 165.18,
          "high": 166.94,
          "low": 159.22,
          "close": 159.8,
          "pnl_pct": 7.95
        }
      },
      "close_date": "2026-06-16",
      "close_price": 159.8,
      "final_pnl_pct": 7.95,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 25.6
    },
    {
      "ticker": "MFIN",
      "name": "MFIN",
      "action": "SELL",
      "signal_date": "2026-06-15",
      "entry_price": 9.81,
      "allocated_usd": 500,
      "shares": 50,
      "actual_position_usd": 490.5,
      "entry_commission": 1.0,
      "take_profit": 8.34,
      "stop_loss": 10.1,
      "max_hold_date": "2026-06-17",
      "daily_prices": {
        "2026-06-16": {
          "open": 9.9,
          "high": 10.09,
          "low": 9.82,
          "close": 9.87,
          "pnl_pct": -0.61
        },
        "2026-06-17": {
          "open": 9.89,
          "high": 9.93,
          "low": 9.47,
          "close": 9.52,
          "pnl_pct": 2.96
        }
      },
      "close_date": "2026-06-17",
      "close_price": 9.52,
      "final_pnl_pct": 2.96,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 12.52
    },
    {
      "ticker": "AMRX",
      "name": "AMRX",
      "action": "SELL",
      "signal_date": "2026-06-16",
      "entry_price": 16.24,
      "allocated_usd": 500,
      "shares": 30,
      "actual_position_usd": 487.2,
      "entry_commission": 1.0,
      "take_profit": 13.8,
      "stop_loss": 16.73,
      "max_hold_date": "2026-06-18",
      "daily_prices": {
        "2026-06-17": {
          "open": 16.25,
          "high": 16.55,
          "low": 16.18,
          "close": 16.28,
          "pnl_pct": -0.25
        },
        "2026-06-18": {
          "open": 16.47,
          "high": 16.61,
          "low": 15.73,
          "close": 16.21,
          "pnl_pct": 0.18
        }
      },
      "close_date": "2026-06-18",
      "close_price": 16.21,
      "final_pnl_pct": 0.18,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -1.12
    },
    {
      "ticker": "CTRE",
      "name": "CTRE",
      "action": "SELL",
      "signal_date": "2026-06-16",
      "entry_price": 37.04,
      "allocated_usd": 500,
      "shares": 13,
      "actual_position_usd": 481.52,
      "entry_commission": 1.0,
      "take_profit": 31.48,
      "stop_loss": 38.15,
      "max_hold_date": "2026-06-18",
      "daily_prices": {
        "2026-06-17": {
          "open": 36.67,
          "high": 36.68,
          "low": 35.91,
          "close": 36.03,
          "pnl_pct": 2.73
        },
        "2026-06-18": {
          "open": 36.22,
          "high": 36.75,
          "low": 35.7,
          "close": 36.7,
          "pnl_pct": 0.92
        }
      },
      "close_date": "2026-06-18",
      "close_price": 36.7,
      "final_pnl_pct": 0.92,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 2.43
    },
    {
      "ticker": "PBHC",
      "name": "PBHC",
      "action": "SELL",
      "signal_date": "2026-06-18",
      "entry_price": 15.84,
      "allocated_usd": 500,
      "shares": 31,
      "actual_position_usd": 491.04,
      "entry_commission": 1.0,
      "take_profit": 13.46,
      "stop_loss": 16.32,
      "max_hold_date": "2026-06-22",
      "daily_prices": {
        "2026-06-22": {
          "open": 16.39,
          "high": 16.4,
          "low": 15.91,
          "close": 16.2,
          "pnl_pct": -3.03
        }
      },
      "close_date": "2026-06-22",
      "close_price": 16.32,
      "final_pnl_pct": -3.03,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -16.88
    },
    {
      "ticker": "SBFG",
      "name": "SBFG",
      "action": "SELL",
      "signal_date": "2026-06-18",
      "entry_price": 22.51,
      "allocated_usd": 500,
      "shares": 22,
      "actual_position_usd": 495.22,
      "entry_commission": 1.0,
      "take_profit": 19.13,
      "stop_loss": 23.19,
      "max_hold_date": "2026-06-22",
      "daily_prices": {
        "2026-06-22": {
          "open": 23.01,
          "high": 23.08,
          "low": 22.54,
          "close": 23.03,
          "pnl_pct": -2.31
        }
      },
      "close_date": "2026-06-22",
      "close_price": 23.03,
      "final_pnl_pct": -2.31,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -13.44
    },
    {
      "ticker": "SNEX",
      "name": "SNEX",
      "action": "BUY",
      "signal_date": "2026-06-19",
      "entry_price": 139.01,
      "allocated_usd": 500,
      "shares": 3,
      "actual_position_usd": 417.03,
      "entry_commission": 1.0,
      "take_profit": 159.86,
      "stop_loss": 134.84,
      "max_hold_date": "2026-06-23",
      "daily_prices": {
        "2026-06-22": {
          "open": 140.64,
          "high": 141.99,
          "low": 137.61,
          "close": 138.79,
          "pnl_pct": -0.16
        },
        "2026-06-23": {
          "open": 135.42,
          "high": 141.27,
          "low": 134.75,
          "close": 137.94,
          "pnl_pct": -3.0
        }
      },
      "close_date": "2026-06-23",
      "close_price": 134.84,
      "final_pnl_pct": -3.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -14.51
    },
    {
      "ticker": "WSBC",
      "name": "WSBC",
      "action": "SELL",
      "signal_date": "2026-06-19",
      "entry_price": 36.29,
      "allocated_usd": 500,
      "shares": 13,
      "actual_position_usd": 471.77,
      "entry_commission": 1.0,
      "take_profit": 30.85,
      "stop_loss": 37.38,
      "max_hold_date": "2026-06-23",
      "daily_prices": {
        "2026-06-22": {
          "open": 36.1,
          "high": 36.85,
          "low": 36.1,
          "close": 36.7,
          "pnl_pct": -1.13
        },
        "2026-06-23": {
          "open": 36.59,
          "high": 37.36,
          "low": 36.59,
          "close": 37.28,
          "pnl_pct": -2.73
        }
      },
      "close_date": "2026-06-23",
      "close_price": 37.28,
      "final_pnl_pct": -2.73,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -14.88
    },
    {
      "ticker": "SWBI",
      "name": "SWBI",
      "action": "SELL",
      "signal_date": "2026-06-22",
      "entry_price": 16.08,
      "allocated_usd": 500,
      "shares": 31,
      "actual_position_usd": 498.48,
      "entry_commission": 1.0,
      "take_profit": 13.67,
      "stop_loss": 16.56,
      "max_hold_date": "2026-06-24",
      "daily_prices": {
        "2026-06-23": {
          "open": 16.03,
          "high": 17.35,
          "low": 15.88,
          "close": 16.53,
          "pnl_pct": -2.99
        }
      },
      "close_date": "2026-06-23",
      "close_price": 16.56,
      "final_pnl_pct": -2.99,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -16.9
    },
    {
      "ticker": "SNEX",
      "name": "SNEX",
      "action": "SELL",
      "signal_date": "2026-06-22",
      "entry_price": 139.01,
      "allocated_usd": 500,
      "shares": 3,
      "actual_position_usd": 417.03,
      "entry_commission": 1.0,
      "take_profit": 118.16,
      "stop_loss": 143.18,
      "max_hold_date": "2026-06-24",
      "daily_prices": {
        "2026-06-23": {
          "open": 135.42,
          "high": 141.27,
          "low": 134.75,
          "close": 137.94,
          "pnl_pct": 0.77
        },
        "2026-06-24": {
          "open": 138.0,
          "high": 139.89,
          "low": 133.74,
          "close": 136.13,
          "pnl_pct": 2.07
        }
      },
      "close_date": "2026-06-24",
      "close_price": 136.13,
      "final_pnl_pct": 2.07,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 6.63
    },
    {
      "ticker": "WSBC",
      "name": "WSBC",
      "action": "SELL",
      "signal_date": "2026-06-22",
      "entry_price": 36.29,
      "allocated_usd": 500,
      "shares": 13,
      "actual_position_usd": 471.77,
      "entry_commission": 1.0,
      "take_profit": 30.85,
      "stop_loss": 37.38,
      "max_hold_date": "2026-06-24",
      "daily_prices": {
        "2026-06-23": {
          "open": 36.59,
          "high": 37.36,
          "low": 36.59,
          "close": 37.28,
          "pnl_pct": -2.73
        },
        "2026-06-24": {
          "open": 37.28,
          "high": 38.09,
          "low": 36.92,
          "close": 37.86,
          "pnl_pct": -3.0
        }
      },
      "close_date": "2026-06-24",
      "close_price": 37.38,
      "final_pnl_pct": -3.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -16.15
    },
    {
      "ticker": "SWBI",
      "name": "SWBI",
      "action": "SELL",
      "signal_date": "2026-06-24",
      "entry_price": 16.67,
      "allocated_usd": 500,
      "shares": 29,
      "actual_position_usd": 483.43,
      "entry_commission": 1.0,
      "take_profit": 14.17,
      "stop_loss": 17.17,
      "max_hold_date": "2026-06-26",
      "daily_prices": {
        "2026-06-25": {
          "open": 16.05,
          "high": 16.25,
          "low": 15.48,
          "close": 15.55,
          "pnl_pct": 6.72
        },
        "2026-06-26": {
          "open": 15.42,
          "high": 15.56,
          "low": 14.71,
          "close": 15.1,
          "pnl_pct": 9.42
        }
      },
      "close_date": "2026-06-26",
      "close_price": 15.1,
      "final_pnl_pct": 9.42,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 43.54
    },
    {
      "ticker": "OBT",
      "name": "OBT",
      "action": "SELL",
      "signal_date": "2026-06-24",
      "entry_price": 36.5,
      "allocated_usd": 500,
      "shares": 13,
      "actual_position_usd": 474.5,
      "entry_commission": 1.0,
      "take_profit": 31.02,
      "stop_loss": 37.59,
      "max_hold_date": "2026-06-26",
      "daily_prices": {
        "2026-06-25": {
          "open": 36.55,
          "high": 37.19,
          "low": 36.55,
          "close": 36.89,
          "pnl_pct": -1.07
        },
        "2026-06-26": {
          "open": 37.02,
          "high": 37.71,
          "low": 36.5,
          "close": 36.95,
          "pnl_pct": -2.99
        }
      },
      "close_date": "2026-06-26",
      "close_price": 37.59,
      "final_pnl_pct": -2.99,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -16.19
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
      "take_profit": 10.51,
      "stop_loss": 12.73,
      "max_hold_date": "2026-06-11",
      "daily_prices": {
        "2026-07-01": {
          "close": 9.54,
          "pnl_pct": 22.82
        }
      },
      "gap_checked": true,
      "day1_open": 9.85,
      "day1_gap_pct": -20.31,
      "close_date": "2026-07-01",
      "close_price": 9.54,
      "final_pnl_pct": 22.82,
      "close_reason": "take_profit",
      "realized_pnl_usd": 114.08
    },
    {
      "ticker": "SKWD",
      "name": "SKWD",
      "action": "SELL",
      "signal_date": "2026-07-02",
      "entry_price": 59.51,
      "allocated_usd": 500,
      "shares": 8,
      "actual_position_usd": 476.08,
      "entry_commission": 1.0,
      "take_profit": 50.58,
      "stop_loss": 61.3,
      "max_hold_date": "2026-07-06",
      "daily_prices": {
        "2026-07-02": {
          "close": 61.69,
          "pnl_pct": -3.66
        }
      },
      "gap_checked": true,
      "day1_open": 59.4,
      "day1_gap_pct": -0.18,
      "close_date": "2026-07-02",
      "close_price": 61.69,
      "final_pnl_pct": -3.66,
      "close_reason": "stop_loss",
      "realized_pnl_usd": -18.32
    }
  ],
  "_note": "Plan D 模拟盘：TP +15% / SL -3% / 最大2交易日 / 不利跳空>1%过滤 / IBKR佣金$0.005/股min$1",
  "stats": {
    "total_trades": 27,
    "win_trades": 13,
    "win_rate": 48.1,
    "total_realized_pnl_usd": 161.27,
    "open_unrealized_pnl_usd": 35.85,
    "portfolio_value": 2197.12,
    "skipped_gap": 10,
    "updated_at": "2026-07-03"
  }
};
