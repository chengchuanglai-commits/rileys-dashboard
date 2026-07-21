// c-trail 变体:移动止损(初始-4%/棘轮4%/最多10天)+ 跳空过滤 1.5%(信号同 c)
window.PORTFOLIO_CTR = {
  "capital_usd": 2000,
  "open_positions": [
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
      "max_hold_date": "2026-06-09",
      "day1_open": null,
      "daily_prices": {},
      "position_usd": 206.23,
      "unrealized_pnl_usd": 0.0
    },
    {
      "ticker": "SMPL",
      "name": "SMPL",
      "action": "SELL",
      "signal_date": "2026-07-15",
      "entry_price": 12.35,
      "allocated_usd": 500,
      "shares": 40,
      "actual_position_usd": 494.0,
      "entry_commission": 1.0,
      "max_hold_date": "2026-07-21",
      "day1_open": 12.19,
      "daily_prices": {
        "2026-07-16": {
          "open": 12.19,
          "high": 12.37,
          "low": 11.94,
          "close": 12.07,
          "pnl_pct": 2.27
        },
        "2026-07-17": {
          "open": 12.04,
          "high": 12.36,
          "low": 11.03,
          "close": 11.08,
          "pnl_pct": 10.28
        },
        "2026-07-20": {
          "open": 11.02,
          "high": 11.29,
          "low": 10.74,
          "close": 10.92,
          "pnl_pct": 11.58
        },
        "2026-07-21": {
          "open": 10.77,
          "high": 11.12,
          "low": 10.71,
          "close": 10.88,
          "pnl_pct": 11.9
        }
      },
      "position_usd": 212.37,
      "unrealized_pnl_usd": 25.27
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
      "max_hold_date": "2026-05-29",
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
          "pnl_pct": -0.33
        }
      },
      "close_date": "2026-05-29",
      "close_price": 87.17,
      "final_pnl_pct": -0.33,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -0.66,
      "position_usd": 200.0
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
      "max_hold_date": "2026-06-02",
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
          "pnl_pct": 4.24
        }
      },
      "close_date": "2026-06-02",
      "close_price": 18.53,
      "final_pnl_pct": 4.24,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 8.48,
      "position_usd": 200.0
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
      "max_hold_date": "2026-06-01",
      "day1_open": 99.24,
      "daily_prices": {
        "2026-05-29": {
          "open": 99.24,
          "high": 99.86,
          "low": 85.64,
          "close": 92.93,
          "pnl_pct": 8.08
        },
        "2026-06-01": {
          "open": 92.29,
          "high": 93.51,
          "low": 85.21,
          "close": 86.23,
          "pnl_pct": 11.9
        }
      },
      "close_date": "2026-06-01",
      "close_price": 89.07,
      "final_pnl_pct": 11.9,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 23.8,
      "position_usd": 200.0
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
      "max_hold_date": "2026-06-02",
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
          "pnl_pct": 2.84
        }
      },
      "close_date": "2026-06-02",
      "close_price": 88.42,
      "final_pnl_pct": 2.84,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 5.68,
      "position_usd": 200.0
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
      "max_hold_date": "2026-06-04",
      "day1_open": 63.27,
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
        },
        "2026-06-04": {
          "open": 62.0,
          "high": 63.51,
          "low": 61.06,
          "close": 63.1,
          "pnl_pct": 7.34
        }
      },
      "close_date": "2026-06-04",
      "close_price": 62.78,
      "final_pnl_pct": 7.34,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 14.85,
      "position_usd": 202.31
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
      "max_hold_date": "2026-06-08",
      "day1_open": 103.85,
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
        },
        "2026-06-08": {
          "open": 102.8,
          "high": 103.72,
          "low": 99.83,
          "close": 102.32,
          "pnl_pct": 6.75
        }
      },
      "close_date": "2026-06-08",
      "close_price": 101.05,
      "final_pnl_pct": 6.75,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 13.75,
      "position_usd": 203.73
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
      "max_hold_date": "2026-06-09",
      "day1_open": 318.33,
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
          "pnl_pct": -0.4
        }
      },
      "close_date": "2026-06-09",
      "close_price": 317.23,
      "final_pnl_pct": -0.4,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -0.82,
      "position_usd": 205.21
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
      "max_hold_date": "2026-06-09",
      "day1_open": 47.58,
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
          "pnl_pct": -1.34
        }
      },
      "close_date": "2026-06-09",
      "close_price": 49.0,
      "final_pnl_pct": -1.34,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -2.75,
      "position_usd": 205.21
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
      "max_hold_date": "2026-06-10",
      "day1_open": 17.79,
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
          "pnl_pct": 1.73
        }
      },
      "close_date": "2026-06-10",
      "close_price": 17.62,
      "final_pnl_pct": 1.73,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 3.57,
      "position_usd": 206.59
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
      "max_hold_date": "2026-06-10",
      "day1_open": 39.2,
      "daily_prices": {
        "2026-06-09": {
          "open": 39.2,
          "high": 40.69,
          "low": 39.14,
          "close": 39.47,
          "pnl_pct": -0.36
        },
        "2026-06-10": {
          "open": 39.77,
          "high": 41.25,
          "low": 39.02,
          "close": 41.12,
          "pnl_pct": -3.51
        }
      },
      "close_date": "2026-06-10",
      "close_price": 40.71,
      "final_pnl_pct": -3.51,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -7.25,
      "position_usd": 206.59
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
      "max_hold_date": "2026-06-18",
      "day1_open": 23.42,
      "daily_prices": {
        "2026-06-10": {
          "open": 23.42,
          "high": 23.76,
          "low": 23.02,
          "close": 23.34,
          "pnl_pct": 15.28
        },
        "2026-06-11": {
          "open": 23.34,
          "high": 23.41,
          "low": 22.99,
          "close": 23.41,
          "pnl_pct": 15.03
        },
        "2026-06-12": {
          "open": 23.31,
          "high": 23.49,
          "low": 23.1,
          "close": 23.22,
          "pnl_pct": 15.72
        },
        "2026-06-15": {
          "open": 23.47,
          "high": 23.47,
          "low": 23.01,
          "close": 23.18,
          "pnl_pct": 15.86
        },
        "2026-06-16": {
          "open": 23.25,
          "high": 23.56,
          "low": 22.79,
          "close": 23.03,
          "pnl_pct": 16.41
        },
        "2026-06-17": {
          "open": 23.12,
          "high": 23.35,
          "low": 22.86,
          "close": 23.15,
          "pnl_pct": 15.97
        },
        "2026-06-18": {
          "open": 23.19,
          "high": 23.79,
          "low": 23.19,
          "close": 23.55,
          "pnl_pct": 13.97
        }
      },
      "close_date": "2026-06-18",
      "close_price": 23.7,
      "final_pnl_pct": 13.97,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 28.81,
      "position_usd": 206.23
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
      "max_hold_date": "2026-06-15",
      "day1_open": 14.79,
      "daily_prices": {
        "2026-06-12": {
          "open": 14.79,
          "high": 15.35,
          "low": 13.64,
          "close": 15.35,
          "pnl_pct": -0.99
        },
        "2026-06-15": {
          "open": 15.98,
          "high": 16.78,
          "low": 15.13,
          "close": 15.13,
          "pnl_pct": 6.64
        }
      },
      "close_date": "2026-06-15",
      "close_price": 14.19,
      "final_pnl_pct": 6.64,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 13.67,
      "position_usd": 205.87
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
      "max_hold_date": "2026-06-23",
      "day1_open": 9.71,
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
        },
        "2026-06-16": {
          "open": 9.9,
          "high": 10.09,
          "low": 9.82,
          "close": 9.87,
          "pnl_pct": 0.2
        },
        "2026-06-17": {
          "open": 9.89,
          "high": 9.93,
          "low": 9.47,
          "close": 9.52,
          "pnl_pct": 3.74
        },
        "2026-06-18": {
          "open": 9.59,
          "high": 9.69,
          "low": 9.38,
          "close": 9.53,
          "pnl_pct": 3.64
        },
        "2026-06-22": {
          "open": 9.53,
          "high": 9.62,
          "low": 9.36,
          "close": 9.38,
          "pnl_pct": 5.16
        },
        "2026-06-23": {
          "open": 9.4,
          "high": 9.8,
          "low": 9.4,
          "close": 9.66,
          "pnl_pct": 1.62
        }
      },
      "close_date": "2026-06-23",
      "close_price": 9.73,
      "final_pnl_pct": 1.62,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 3.34,
      "position_usd": 205.87
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
      "max_hold_date": "2026-06-25",
      "day1_open": 172.51,
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
        },
        "2026-06-17": {
          "open": 159.92,
          "high": 160.18,
          "low": 144.63,
          "close": 145.85,
          "pnl_pct": 15.99
        },
        "2026-06-18": {
          "open": 146.94,
          "high": 149.51,
          "low": 142.79,
          "close": 144.53,
          "pnl_pct": 16.75
        },
        "2026-06-22": {
          "open": 146.31,
          "high": 148.02,
          "low": 144.13,
          "close": 145.6,
          "pnl_pct": 16.13
        },
        "2026-06-23": {
          "open": 146.46,
          "high": 146.46,
          "low": 143.54,
          "close": 143.74,
          "pnl_pct": 17.2
        },
        "2026-06-24": {
          "open": 143.84,
          "high": 146.22,
          "low": 141.25,
          "close": 145.18,
          "pnl_pct": 16.37
        },
        "2026-06-25": {
          "open": 146.24,
          "high": 153.87,
          "low": 145.92,
          "close": 150.02,
          "pnl_pct": 15.38
        }
      },
      "close_date": "2026-06-25",
      "close_price": 146.9,
      "final_pnl_pct": 15.38,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 31.66,
      "position_usd": 205.87
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
      "max_hold_date": "2026-06-23",
      "day1_open": 9.9,
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
        },
        "2026-06-18": {
          "open": 9.59,
          "high": 9.69,
          "low": 9.38,
          "close": 9.53,
          "pnl_pct": 2.85
        },
        "2026-06-22": {
          "open": 9.53,
          "high": 9.62,
          "low": 9.36,
          "close": 9.38,
          "pnl_pct": 4.38
        },
        "2026-06-23": {
          "open": 9.4,
          "high": 9.8,
          "low": 9.4,
          "close": 9.66,
          "pnl_pct": 0.82
        }
      },
      "close_date": "2026-06-23",
      "close_price": 9.73,
      "final_pnl_pct": 0.82,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 1.7,
      "position_usd": 207.23
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
      "max_hold_date": "2026-06-22",
      "day1_open": 16.25,
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
        },
        "2026-06-22": {
          "open": 16.21,
          "high": 16.4,
          "low": 16.01,
          "close": 16.11,
          "pnl_pct": -0.74
        }
      },
      "close_date": "2026-06-22",
      "close_price": 16.36,
      "final_pnl_pct": -0.74,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -1.53,
      "position_usd": 207.23
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
      "max_hold_date": "2026-06-22",
      "day1_open": 36.67,
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
        },
        "2026-06-22": {
          "open": 36.63,
          "high": 37.24,
          "low": 36.44,
          "close": 37.13,
          "pnl_pct": -0.24
        }
      },
      "close_date": "2026-06-22",
      "close_price": 37.13,
      "final_pnl_pct": -0.24,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -0.5,
      "position_usd": 207.23
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
      "max_hold_date": "2026-06-23",
      "day1_open": 140.64,
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
          "pnl_pct": -1.94
        }
      },
      "close_date": "2026-06-23",
      "close_price": 136.31,
      "final_pnl_pct": -1.94,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.08,
      "position_usd": 210.11
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
      "max_hold_date": "2026-06-24",
      "day1_open": 36.1,
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
        },
        "2026-06-24": {
          "open": 37.28,
          "high": 38.09,
          "low": 36.92,
          "close": 37.86,
          "pnl_pct": -3.44
        }
      },
      "close_date": "2026-06-24",
      "close_price": 37.54,
      "final_pnl_pct": -3.44,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -7.23,
      "position_usd": 210.11
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
      "max_hold_date": "2026-06-23",
      "day1_open": 16.03,
      "daily_prices": {
        "2026-06-23": {
          "open": 16.03,
          "high": 17.35,
          "low": 15.88,
          "close": 16.53,
          "pnl_pct": -3.98
        }
      },
      "close_date": "2026-06-23",
      "close_price": 16.72,
      "final_pnl_pct": -3.98,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -8.35,
      "position_usd": 209.91
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
      "max_hold_date": "2026-06-24",
      "day1_open": 36.59,
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
          "pnl_pct": -4.0
        }
      },
      "close_date": "2026-06-24",
      "close_price": 37.74,
      "final_pnl_pct": -4.0,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -8.4,
      "position_usd": 209.91
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
      "max_hold_date": "2026-06-25",
      "day1_open": 135.42,
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
        },
        "2026-06-25": {
          "open": 138.06,
          "high": 139.18,
          "low": 135.62,
          "close": 137.28,
          "pnl_pct": -0.06
        }
      },
      "close_date": "2026-06-25",
      "close_price": 139.09,
      "final_pnl_pct": -0.06,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -0.13,
      "position_usd": 209.91
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
      "max_hold_date": "2026-06-29",
      "day1_open": 16.05,
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
        },
        "2026-06-29": {
          "open": 15.54,
          "high": 15.56,
          "low": 15.04,
          "close": 15.27,
          "pnl_pct": 8.22
        }
      },
      "close_date": "2026-06-29",
      "close_price": 15.3,
      "final_pnl_pct": 8.22,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 17.07,
      "position_usd": 207.61
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
      "max_hold_date": "2026-07-01",
      "day1_open": 36.55,
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
          "pnl_pct": -1.23
        },
        "2026-06-29": {
          "open": 36.97,
          "high": 37.7,
          "low": 36.67,
          "close": 37.24,
          "pnl_pct": -2.03
        },
        "2026-06-30": {
          "open": 37.04,
          "high": 37.4,
          "low": 36.55,
          "close": 36.78,
          "pnl_pct": -0.77
        },
        "2026-07-01": {
          "open": 36.56,
          "high": 37.97,
          "low": 36.56,
          "close": 37.64,
          "pnl_pct": -4.0
        }
      },
      "close_date": "2026-07-01",
      "close_price": 37.96,
      "final_pnl_pct": -4.0,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -8.3,
      "position_usd": 207.61
    },
    {
      "ticker": "TRVI",
      "name": "TRVI",
      "action": "SELL",
      "signal_date": "2026-06-26",
      "entry_price": 17.93,
      "allocated_usd": 500,
      "shares": 27,
      "actual_position_usd": 484.11,
      "entry_commission": 1.0,
      "max_hold_date": "2026-06-29",
      "day1_open": 18.15,
      "daily_prices": {
        "2026-06-29": {
          "open": 18.15,
          "high": 18.86,
          "low": 17.79,
          "close": 18.63,
          "pnl_pct": -4.02
        }
      },
      "close_date": "2026-06-29",
      "close_price": 18.65,
      "final_pnl_pct": -4.02,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -8.47,
      "position_usd": 210.76
    },
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
      "max_hold_date": "2026-07-06",
      "day1_open": 52.8,
      "daily_prices": {
        "2026-07-02": {
          "open": 52.8,
          "high": 54.94,
          "low": 51.32,
          "close": 54.88,
          "pnl_pct": 0.22
        },
        "2026-07-06": {
          "open": 54.94,
          "high": 56.03,
          "low": 54.0,
          "close": 55.36,
          "pnl_pct": 2.96
        }
      },
      "close_date": "2026-07-06",
      "close_price": 53.37,
      "final_pnl_pct": 2.96,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 6.24,
      "position_usd": 210.79
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
      "max_hold_date": "2026-07-09",
      "day1_open": 72.21,
      "daily_prices": {
        "2026-07-06": {
          "open": 72.21,
          "high": 75.31,
          "low": 72.05,
          "close": 73.22,
          "pnl_pct": 1.21
        },
        "2026-07-07": {
          "open": 72.7,
          "high": 72.7,
          "low": 69.56,
          "close": 70.16,
          "pnl_pct": 5.34
        },
        "2026-07-08": {
          "open": 69.43,
          "high": 71.58,
          "low": 68.73,
          "close": 71.33,
          "pnl_pct": 3.76
        },
        "2026-07-09": {
          "open": 72.73,
          "high": 74.45,
          "low": 72.05,
          "close": 72.36,
          "pnl_pct": 3.56
        }
      },
      "close_date": "2026-07-09",
      "close_price": 71.48,
      "final_pnl_pct": 3.56,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 7.5,
      "position_usd": 210.79
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
      "max_hold_date": "2026-07-10",
      "day1_open": 29.28,
      "daily_prices": {
        "2026-07-06": {
          "open": 29.28,
          "high": 29.77,
          "low": 28.7,
          "close": 28.91,
          "pnl_pct": 3.12
        },
        "2026-07-07": {
          "open": 29.15,
          "high": 29.31,
          "low": 28.58,
          "close": 28.62,
          "pnl_pct": 4.09
        },
        "2026-07-08": {
          "open": 28.49,
          "high": 28.49,
          "low": 27.61,
          "close": 28.01,
          "pnl_pct": 6.13
        },
        "2026-07-09": {
          "open": 28.0,
          "high": 28.61,
          "low": 27.92,
          "close": 28.46,
          "pnl_pct": 4.62
        },
        "2026-07-10": {
          "open": 28.48,
          "high": 29.47,
          "low": 28.25,
          "close": 28.66,
          "pnl_pct": 3.79
        }
      },
      "close_date": "2026-07-10",
      "close_price": 28.71,
      "final_pnl_pct": 3.79,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 7.99,
      "position_usd": 210.79
    },
    {
      "ticker": "LGND",
      "name": "LGND",
      "action": "SELL",
      "signal_date": "2026-07-03",
      "entry_price": 319.55,
      "allocated_usd": 500,
      "shares": 1,
      "actual_position_usd": 319.55,
      "entry_commission": 1.0,
      "max_hold_date": "2026-07-08",
      "day1_open": 319.94,
      "daily_prices": {
        "2026-07-06": {
          "open": 319.94,
          "high": 322.31,
          "low": 315.76,
          "close": 320.42,
          "pnl_pct": -0.27
        },
        "2026-07-07": {
          "open": 317.97,
          "high": 323.3,
          "low": 312.74,
          "close": 319.43,
          "pnl_pct": 0.04
        },
        "2026-07-08": {
          "open": 321.91,
          "high": 326.63,
          "low": 311.73,
          "close": 314.88,
          "pnl_pct": -1.78
        }
      },
      "close_date": "2026-07-08",
      "close_price": 325.25,
      "final_pnl_pct": -1.78,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -3.75,
      "position_usd": 210.79
    },
    {
      "ticker": "MVBF",
      "name": "MVBF",
      "action": "SELL",
      "signal_date": "2026-07-03",
      "entry_price": 29.41,
      "allocated_usd": 500,
      "shares": 17,
      "actual_position_usd": 499.97,
      "entry_commission": 1.0,
      "max_hold_date": "2026-07-10",
      "day1_open": 29.28,
      "daily_prices": {
        "2026-07-06": {
          "open": 29.28,
          "high": 29.77,
          "low": 28.7,
          "close": 28.91,
          "pnl_pct": 1.7
        },
        "2026-07-07": {
          "open": 29.15,
          "high": 29.31,
          "low": 28.58,
          "close": 28.62,
          "pnl_pct": 2.69
        },
        "2026-07-08": {
          "open": 28.49,
          "high": 28.49,
          "low": 27.61,
          "close": 28.01,
          "pnl_pct": 4.76
        },
        "2026-07-09": {
          "open": 28.0,
          "high": 28.61,
          "low": 27.92,
          "close": 28.46,
          "pnl_pct": 3.23
        },
        "2026-07-10": {
          "open": 28.48,
          "high": 29.47,
          "low": 28.25,
          "close": 28.66,
          "pnl_pct": 2.38
        }
      },
      "close_date": "2026-07-10",
      "close_price": 28.71,
      "final_pnl_pct": 2.38,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 5.02,
      "position_usd": 210.79
    },
    {
      "ticker": "LGND",
      "name": "LGND",
      "action": "SELL",
      "signal_date": "2026-07-06",
      "entry_price": 319.55,
      "allocated_usd": 500,
      "shares": 1,
      "actual_position_usd": 319.55,
      "entry_commission": 1.0,
      "max_hold_date": "2026-07-08",
      "day1_open": 317.97,
      "daily_prices": {
        "2026-07-07": {
          "open": 317.97,
          "high": 323.3,
          "low": 312.74,
          "close": 319.43,
          "pnl_pct": 0.04
        },
        "2026-07-08": {
          "open": 321.91,
          "high": 326.63,
          "low": 311.73,
          "close": 314.88,
          "pnl_pct": -1.78
        }
      },
      "close_date": "2026-07-08",
      "close_price": 325.25,
      "final_pnl_pct": -1.78,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -3.76,
      "position_usd": 211.41
    },
    {
      "ticker": "MVBF",
      "name": "MVBF",
      "action": "SELL",
      "signal_date": "2026-07-06",
      "entry_price": 29.41,
      "allocated_usd": 500,
      "shares": 17,
      "actual_position_usd": 499.97,
      "entry_commission": 1.0,
      "max_hold_date": "2026-07-10",
      "day1_open": 29.15,
      "daily_prices": {
        "2026-07-07": {
          "open": 29.15,
          "high": 29.31,
          "low": 28.58,
          "close": 28.62,
          "pnl_pct": 2.69
        },
        "2026-07-08": {
          "open": 28.49,
          "high": 28.49,
          "low": 27.61,
          "close": 28.01,
          "pnl_pct": 4.76
        },
        "2026-07-09": {
          "open": 28.0,
          "high": 28.61,
          "low": 27.92,
          "close": 28.46,
          "pnl_pct": 3.23
        },
        "2026-07-10": {
          "open": 28.48,
          "high": 29.47,
          "low": 28.25,
          "close": 28.66,
          "pnl_pct": 2.38
        }
      },
      "close_date": "2026-07-10",
      "close_price": 28.71,
      "final_pnl_pct": 2.38,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 5.03,
      "position_usd": 211.41
    },
    {
      "ticker": "PFIS",
      "name": "PFIS",
      "action": "SELL",
      "signal_date": "2026-07-09",
      "entry_price": 65.25,
      "allocated_usd": 500,
      "shares": 7,
      "actual_position_usd": 456.75,
      "entry_commission": 1.0,
      "max_hold_date": "2026-07-15",
      "day1_open": 65.92,
      "daily_prices": {
        "2026-07-10": {
          "open": 65.92,
          "high": 66.8,
          "low": 65.9,
          "close": 66.52,
          "pnl_pct": -1.95
        },
        "2026-07-13": {
          "open": 66.47,
          "high": 67.12,
          "low": 66.22,
          "close": 66.71,
          "pnl_pct": -2.24
        },
        "2026-07-14": {
          "open": 66.76,
          "high": 67.61,
          "low": 66.06,
          "close": 66.68,
          "pnl_pct": -2.19
        },
        "2026-07-15": {
          "open": 67.4,
          "high": 67.92,
          "low": 66.28,
          "close": 67.74,
          "pnl_pct": -4.0
        }
      },
      "close_date": "2026-07-15",
      "close_price": 67.86,
      "final_pnl_pct": -4.0,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -8.46,
      "position_usd": 211.41
    },
    {
      "ticker": "SKWD",
      "name": "SKWD",
      "action": "SELL",
      "signal_date": "2026-07-09",
      "entry_price": 60.37,
      "allocated_usd": 500,
      "shares": 8,
      "actual_position_usd": 482.96,
      "entry_commission": 1.0,
      "max_hold_date": "2026-07-16",
      "day1_open": 60.1,
      "daily_prices": {
        "2026-07-10": {
          "open": 60.1,
          "high": 61.22,
          "low": 59.14,
          "close": 59.34,
          "pnl_pct": 1.71
        },
        "2026-07-13": {
          "open": 59.97,
          "high": 60.89,
          "low": 58.14,
          "close": 59.76,
          "pnl_pct": 1.01
        },
        "2026-07-14": {
          "open": 59.43,
          "high": 60.46,
          "low": 58.23,
          "close": 58.36,
          "pnl_pct": 3.33
        },
        "2026-07-15": {
          "open": 58.33,
          "high": 58.33,
          "low": 56.13,
          "close": 56.87,
          "pnl_pct": 5.8
        },
        "2026-07-16": {
          "open": 58.1,
          "high": 59.71,
          "low": 57.62,
          "close": 58.47,
          "pnl_pct": 3.3
        }
      },
      "close_date": "2026-07-16",
      "close_price": 58.38,
      "final_pnl_pct": 3.3,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 6.98,
      "position_usd": 211.41
    },
    {
      "ticker": "ITIC",
      "name": "ITIC",
      "action": "SELL",
      "signal_date": "2026-07-13",
      "entry_price": 276.0,
      "allocated_usd": 500,
      "shares": 1,
      "actual_position_usd": 276.0,
      "entry_commission": 1.0,
      "max_hold_date": "2026-07-16",
      "day1_open": 278.21,
      "daily_prices": {
        "2026-07-14": {
          "open": 278.21,
          "high": 281.14,
          "low": 277.43,
          "close": 278.72,
          "pnl_pct": -0.99
        },
        "2026-07-15": {
          "open": 273.55,
          "high": 279.3,
          "low": 271.53,
          "close": 273.6,
          "pnl_pct": 0.87
        },
        "2026-07-16": {
          "open": 277.65,
          "high": 283.97,
          "low": 277.65,
          "close": 283.96,
          "pnl_pct": -2.32
        }
      },
      "close_date": "2026-07-16",
      "close_price": 282.39,
      "final_pnl_pct": -2.32,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.95,
      "position_usd": 213.22
    },
    {
      "ticker": "TCBK",
      "name": "TCBK",
      "action": "SELL",
      "signal_date": "2026-07-14",
      "entry_price": 60.07,
      "allocated_usd": 500,
      "shares": 8,
      "actual_position_usd": 480.56,
      "entry_commission": 1.0,
      "max_hold_date": "2026-07-16",
      "day1_open": 59.43,
      "daily_prices": {
        "2026-07-15": {
          "open": 59.43,
          "high": 59.93,
          "low": 58.59,
          "close": 59.43,
          "pnl_pct": 1.07
        },
        "2026-07-16": {
          "open": 59.52,
          "high": 61.71,
          "low": 59.31,
          "close": 61.62,
          "pnl_pct": -1.43
        }
      },
      "close_date": "2026-07-16",
      "close_price": 60.93,
      "final_pnl_pct": -1.43,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -3.05,
      "position_usd": 213.22
    },
    {
      "ticker": "STRS",
      "name": "STRS",
      "action": "SELL",
      "signal_date": "2026-07-14",
      "entry_price": 20.93,
      "allocated_usd": 500,
      "shares": 23,
      "actual_position_usd": 481.39,
      "entry_commission": 1.0,
      "max_hold_date": "2026-07-16",
      "day1_open": 20.66,
      "daily_prices": {
        "2026-07-15": {
          "open": 20.66,
          "high": 21.29,
          "low": 20.15,
          "close": 20.7,
          "pnl_pct": 1.1
        },
        "2026-07-16": {
          "open": 20.79,
          "high": 21.0,
          "low": 20.21,
          "close": 20.67,
          "pnl_pct": -0.14
        }
      },
      "close_date": "2026-07-16",
      "close_price": 20.96,
      "final_pnl_pct": -0.14,
      "close_reason": "trail_stop",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -0.3,
      "position_usd": 213.22
    }
  ],
  "_note": "c-trail 变体:移动止损(初始-4%/棘轮4%/最多10天)+ 跳空过滤 1.5%(信号同 c)",
  "stats": {
    "total_trades": 37,
    "win_trades": 18,
    "win_rate": 48.6,
    "total_realized_pnl_usd": 122.4,
    "open_unrealized_pnl_usd": 25.27,
    "portfolio_value": 2147.67,
    "total_commission_usd": 74.0,
    "skipped_gap": 14,
    "skipped_zero_shares": 1,
    "updated_at": "2026-07-21"
  }
};
