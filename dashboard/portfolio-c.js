// Plan C 模拟盘持仓 — 历史回溯 + 实时更新（跳空过滤版）
window.PORTFOLIO_C = {
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
      "take_profit": 11.37,
      "stop_loss": 12.85,
      "max_hold_date": "2026-06-16",
      "day1_open": null,
      "daily_prices": {},
      "position_usd": 206.03,
      "unrealized_pnl_usd": 0.0
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
      "take_profit": 150.13,
      "stop_loss": 133.45,
      "max_hold_date": "2026-06-26",
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
          "pnl_pct": -0.77
        },
        "2026-06-24": {
          "open": 138.0,
          "high": 139.89,
          "low": 133.74,
          "close": 136.13,
          "pnl_pct": -2.07
        }
      },
      "position_usd": 211.77,
      "unrealized_pnl_usd": -4.38
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
      "take_profit": 127.89,
      "stop_loss": 144.57,
      "max_hold_date": "2026-06-29",
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
        }
      },
      "position_usd": 212.69,
      "unrealized_pnl_usd": 4.4
    },
    {
      "ticker": "LGND",
      "name": "LGND",
      "action": "SELL",
      "signal_date": "2026-06-24",
      "entry_price": 279.44,
      "allocated_usd": 500,
      "shares": 1,
      "actual_position_usd": 279.44,
      "entry_commission": 1.0,
      "take_profit": 257.08,
      "stop_loss": 290.62,
      "max_hold_date": "2026-07-01",
      "day1_open": null,
      "daily_prices": {},
      "position_usd": 208.75,
      "unrealized_pnl_usd": 0.0
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
      "take_profit": 15.34,
      "stop_loss": 17.34,
      "max_hold_date": "2026-07-01",
      "day1_open": null,
      "daily_prices": {},
      "position_usd": 208.75,
      "unrealized_pnl_usd": 0.0
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
      "take_profit": 33.58,
      "stop_loss": 37.96,
      "max_hold_date": "2026-07-01",
      "day1_open": null,
      "daily_prices": {},
      "position_usd": 208.75,
      "unrealized_pnl_usd": 0.0
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
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -8.0,
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
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 3.82,
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
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 16.0,
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
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 16.0,
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
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 16.06,
      "position_usd": 200.8
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
          "pnl_pct": 8.0
        }
      },
      "close_date": "2026-06-05",
      "close_price": 99.69,
      "final_pnl_pct": 8.0,
      "close_reason": "take_profit",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 16.35,
      "position_usd": 204.39
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
          "pnl_pct": 8.0
        }
      },
      "close_date": "2026-06-09",
      "close_price": 343.98,
      "final_pnl_pct": 8.0,
      "close_reason": "take_profit",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 16.48,
      "position_usd": 206.02
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
          "pnl_pct": -3.99
        }
      },
      "close_date": "2026-06-09",
      "close_price": 50.28,
      "final_pnl_pct": -3.99,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -8.22,
      "position_usd": 206.02
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
      "day1_open": 39.43,
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
      "realized_pnl_usd": -8.22,
      "position_usd": 206.02
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
          "pnl_pct": 7.98
        }
      },
      "close_date": "2026-06-10",
      "close_price": 16.5,
      "final_pnl_pct": 7.98,
      "close_reason": "take_profit",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 16.44,
      "position_usd": 206.02
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
      "day1_open": 14.88,
      "daily_prices": {
        "2026-06-12": {
          "open": 14.88,
          "high": 15.45,
          "low": 13.72,
          "close": 15.45,
          "pnl_pct": 8.03
        }
      },
      "close_date": "2026-06-12",
      "close_price": 13.98,
      "final_pnl_pct": 8.03,
      "close_reason": "take_profit",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 16.68,
      "position_usd": 207.67
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
      "take_profit": 9.1,
      "stop_loss": 10.29,
      "max_hold_date": "2026-06-18",
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
        }
      },
      "close_date": "2026-06-18",
      "close_price": 9.53,
      "final_pnl_pct": 3.64,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 7.56,
      "position_usd": 207.67
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
          "pnl_pct": 8.0
        }
      },
      "close_date": "2026-06-16",
      "close_price": 159.71,
      "final_pnl_pct": 8.0,
      "close_reason": "take_profit",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 16.75,
      "position_usd": 209.34
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
      "take_profit": 9.03,
      "stop_loss": 10.2,
      "max_hold_date": "2026-06-22",
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
        }
      },
      "close_date": "2026-06-22",
      "close_price": 9.38,
      "final_pnl_pct": 4.38,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 9.17,
      "position_usd": 209.34
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
      "take_profit": 14.94,
      "stop_loss": 16.89,
      "max_hold_date": "2026-06-23",
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
          "pnl_pct": 0.8
        },
        "2026-06-23": {
          "open": 16.0,
          "high": 16.73,
          "low": 15.93,
          "close": 16.66,
          "pnl_pct": -2.59
        }
      },
      "close_date": "2026-06-23",
      "close_price": 16.66,
      "final_pnl_pct": -2.59,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -5.47,
      "position_usd": 211.01
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
      "take_profit": 34.08,
      "stop_loss": 38.52,
      "max_hold_date": "2026-06-23",
      "day1_open": 37.03,
      "daily_prices": {
        "2026-06-17": {
          "open": 37.03,
          "high": 37.04,
          "low": 36.26,
          "close": 36.38,
          "pnl_pct": 1.78
        },
        "2026-06-18": {
          "open": 36.57,
          "high": 37.11,
          "low": 36.05,
          "close": 37.06,
          "pnl_pct": -0.05
        },
        "2026-06-22": {
          "open": 36.99,
          "high": 37.6,
          "low": 36.79,
          "close": 37.49,
          "pnl_pct": -1.21
        },
        "2026-06-23": {
          "open": 37.86,
          "high": 38.82,
          "low": 37.69,
          "close": 38.8,
          "pnl_pct": -4.0
        }
      },
      "close_date": "2026-06-23",
      "close_price": 38.52,
      "final_pnl_pct": -4.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -8.44,
      "position_usd": 211.01
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
      "take_profit": 33.39,
      "stop_loss": 37.74,
      "max_hold_date": "2026-06-26",
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
          "pnl_pct": -4.0
        }
      },
      "close_date": "2026-06-24",
      "close_price": 37.74,
      "final_pnl_pct": -4.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -8.47,
      "position_usd": 211.77
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
      "take_profit": 14.79,
      "stop_loss": 16.72,
      "max_hold_date": "2026-06-29",
      "day1_open": 16.17,
      "daily_prices": {
        "2026-06-23": {
          "open": 16.17,
          "high": 17.5,
          "low": 16.02,
          "close": 16.67,
          "pnl_pct": -3.98
        }
      },
      "close_date": "2026-06-23",
      "close_price": 16.72,
      "final_pnl_pct": -3.98,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -8.46,
      "position_usd": 212.69
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
      "take_profit": 33.39,
      "stop_loss": 37.74,
      "max_hold_date": "2026-06-29",
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
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -8.51,
      "position_usd": 212.69
    }
  ],
  "_note": "Plan C 模拟盘：TP +8% / SL -4% / 最大5交易日 / 不利跳空>1.5%跳过 / IBKR佣金$0.005/股min$1",
  "stats": {
    "total_trades": 19,
    "win_trades": 11,
    "win_rate": 57.9,
    "total_realized_pnl_usd": 87.52,
    "open_unrealized_pnl_usd": 0.02,
    "portfolio_value": 2087.54,
    "total_commission_usd": 38.0,
    "skipped_gap": 8,
    "skipped_zero_shares": 1,
    "updated_at": "2026-06-25"
  }
};
