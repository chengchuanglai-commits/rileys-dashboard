// Plan H-DS 模拟盘持仓 — 历史最优参数(TP15/SL2/2日) 回溯 + 实时更新
window.PORTFOLIO_HDS = {
  "capital_usd": 2000,
  "open_positions": [
    {
      "ticker": "TCNNF",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-06-08",
      "entry_price": 10.35,
      "allocated_usd": 500,
      "shares": 48.3092,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 8.8,
      "stop_loss": 10.56,
      "max_hold_date": "2026-06-10",
      "daily_prices": {},
      "position_usd": 202.25,
      "unrealized_pnl_usd": 0.0
    },
    {
      "ticker": "TCNNF",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-06-09",
      "entry_price": 10.35,
      "allocated_usd": 500,
      "shares": 48.3092,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 11.9,
      "stop_loss": 10.14,
      "max_hold_date": "2026-06-11",
      "daily_prices": {},
      "position_usd": 206.01,
      "unrealized_pnl_usd": 0.0
    },
    {
      "ticker": "NUVL",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-06-11",
      "entry_price": 123.25,
      "allocated_usd": 500,
      "shares": 4.0568,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 104.76,
      "stop_loss": 125.72,
      "max_hold_date": "2026-06-15",
      "daily_prices": {},
      "position_usd": 209.1,
      "unrealized_pnl_usd": 0.0
    },
    {
      "ticker": "SBFG",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-06-17",
      "entry_price": 22.33,
      "allocated_usd": 500,
      "shares": 22.3914,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 25.68,
      "stop_loss": 21.88,
      "max_hold_date": "2026-06-19",
      "daily_prices": {
        "2026-06-18": {
          "open": 22.59,
          "high": 22.92,
          "low": 21.95,
          "close": 22.88,
          "pnl_pct": 2.46
        }
      },
      "position_usd": 213.49,
      "unrealized_pnl_usd": 5.25
    },
    {
      "ticker": "HOFT",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-06-17",
      "entry_price": 15.21,
      "allocated_usd": 500,
      "shares": 32.8731,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 17.49,
      "stop_loss": 14.91,
      "max_hold_date": "2026-06-19",
      "daily_prices": {
        "2026-06-18": {
          "open": 15.1,
          "high": 16.05,
          "low": 15.0,
          "close": 15.67,
          "pnl_pct": 3.02
        }
      },
      "position_usd": 213.49,
      "unrealized_pnl_usd": 6.45
    },
    {
      "ticker": "NUVL",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-06-18",
      "entry_price": 123.43,
      "allocated_usd": 500,
      "shares": 4.0509,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 104.92,
      "stop_loss": 125.9,
      "max_hold_date": "2026-06-22",
      "daily_prices": {},
      "position_usd": 213.06,
      "unrealized_pnl_usd": 0.0
    },
    {
      "ticker": "INFU",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-09-24",
      "entry_price": 12.7,
      "allocated_usd": 500,
      "shares": 39.3701,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 14.6,
      "stop_loss": 12.45,
      "max_hold_date": "2026-09-28",
      "daily_prices": {
        "2026-09-25": {
          "open": 12.69,
          "high": 12.8,
          "low": 12.47,
          "close": 12.76,
          "pnl_pct": 0.47
        }
      },
      "position_usd": 234.79,
      "unrealized_pnl_usd": 1.1
    },
    {
      "ticker": "MBIN",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-09-24",
      "entry_price": 51.37,
      "allocated_usd": 500,
      "shares": 9.7333,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 59.08,
      "stop_loss": 50.34,
      "max_hold_date": "2026-09-28",
      "daily_prices": {
        "2026-09-25": {
          "open": 52.29,
          "high": 52.8,
          "low": 51.99,
          "close": 52.4,
          "pnl_pct": 2.01
        }
      },
      "position_usd": 234.79,
      "unrealized_pnl_usd": 4.72
    },
    {
      "ticker": "TISI",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-09-24",
      "entry_price": 28.9,
      "allocated_usd": 500,
      "shares": 17.301,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 24.56,
      "stop_loss": 29.48,
      "max_hold_date": "2026-09-28",
      "daily_prices": {
        "2026-09-25": {
          "open": 28.87,
          "high": 28.97,
          "low": 28.65,
          "close": 28.97,
          "pnl_pct": -0.24
        }
      },
      "position_usd": 234.79,
      "unrealized_pnl_usd": -0.56
    }
  ],
  "closed_positions": [
    {
      "ticker": "MU",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-06-02",
      "entry_price": 981.61,
      "allocated_usd": 500,
      "shares": 0.5094,
      "actual_position_usd": 500.03,
      "entry_commission": 1.0,
      "take_profit": 1128.85,
      "stop_loss": 961.98,
      "max_hold_date": "2026-06-04",
      "daily_prices": {
        "2026-06-03": {
          "open": 1078.84,
          "high": 1089.12,
          "low": 1038.34,
          "close": 1079.4,
          "pnl_pct": 9.96
        },
        "2026-06-04": {
          "open": 1006.95,
          "high": 1036.21,
          "low": 971.53,
          "close": 995.85,
          "pnl_pct": 1.45
        }
      },
      "close_date": "2026-06-04",
      "close_price": 995.85,
      "final_pnl_pct": 1.45,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 2.9,
      "position_usd": 200.0
    },
    {
      "ticker": "KLIC",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-06-04",
      "entry_price": 113.13,
      "allocated_usd": 500,
      "shares": 4.4197,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 96.16,
      "stop_loss": 115.39,
      "max_hold_date": "2026-06-08",
      "daily_prices": {
        "2026-06-05": {
          "open": 103.45,
          "high": 104.3,
          "low": 96.91,
          "close": 97.73,
          "pnl_pct": 13.61
        },
        "2026-06-08": {
          "open": 102.53,
          "high": 103.45,
          "low": 99.58,
          "close": 102.06,
          "pnl_pct": 9.79
        }
      },
      "close_date": "2026-06-08",
      "close_price": 102.06,
      "final_pnl_pct": 9.79,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 19.61,
      "position_usd": 200.29
    },
    {
      "ticker": "ADMA",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-06-05",
      "entry_price": 8.21,
      "allocated_usd": 500,
      "shares": 60.9013,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 6.98,
      "stop_loss": 8.37,
      "max_hold_date": "2026-06-09",
      "daily_prices": {
        "2026-06-08": {
          "open": 7.88,
          "high": 8.11,
          "low": 7.88,
          "close": 8.06,
          "pnl_pct": 1.83
        },
        "2026-06-09": {
          "open": 8.09,
          "high": 8.3,
          "low": 8.02,
          "close": 8.12,
          "pnl_pct": 1.1
        }
      },
      "close_date": "2026-06-09",
      "close_price": 8.12,
      "final_pnl_pct": 1.1,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 2.2,
      "position_usd": 200.29
    },
    {
      "ticker": "FLR",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-06-05",
      "entry_price": 50.76,
      "allocated_usd": 500,
      "shares": 9.8503,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 43.15,
      "stop_loss": 51.78,
      "max_hold_date": "2026-06-09",
      "daily_prices": {
        "2026-06-08": {
          "open": 47.58,
          "high": 49.68,
          "low": 47.12,
          "close": 49.52,
          "pnl_pct": 2.44
        },
        "2026-06-09": {
          "open": 49.85,
          "high": 51.55,
          "low": 47.54,
          "close": 49.48,
          "pnl_pct": 2.52
        }
      },
      "close_date": "2026-06-09",
      "close_price": 49.48,
      "final_pnl_pct": 2.52,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 5.05,
      "position_usd": 200.29
    },
    {
      "ticker": "STRS",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-06-08",
      "entry_price": 28.73,
      "allocated_usd": 500,
      "shares": 17.4034,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 24.42,
      "stop_loss": 29.3,
      "max_hold_date": "2026-06-10",
      "daily_prices": {
        "2026-06-09": {
          "open": 22.78,
          "high": 23.22,
          "low": 22.43,
          "close": 23.1,
          "pnl_pct": 15.0
        }
      },
      "close_date": "2026-06-09",
      "close_price": 24.42,
      "final_pnl_pct": 15.0,
      "close_reason": "take_profit",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 30.34,
      "position_usd": 202.25
    },
    {
      "ticker": "STRS",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-06-09",
      "entry_price": 28.73,
      "allocated_usd": 500,
      "shares": 17.4034,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 24.42,
      "stop_loss": 29.3,
      "max_hold_date": "2026-06-11",
      "daily_prices": {
        "2026-06-10": {
          "open": 23.42,
          "high": 23.76,
          "low": 23.02,
          "close": 23.34,
          "pnl_pct": 15.0
        }
      },
      "close_date": "2026-06-10",
      "close_price": 24.42,
      "final_pnl_pct": 15.0,
      "close_reason": "take_profit",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 30.9,
      "position_usd": 206.01
    },
    {
      "ticker": "STRS",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-06-11",
      "entry_price": 28.73,
      "allocated_usd": 500,
      "shares": 17.4034,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 24.42,
      "stop_loss": 29.3,
      "max_hold_date": "2026-06-15",
      "daily_prices": {
        "2026-06-12": {
          "open": 23.31,
          "high": 23.49,
          "low": 23.1,
          "close": 23.22,
          "pnl_pct": 15.0
        }
      },
      "close_date": "2026-06-12",
      "close_price": 24.42,
      "final_pnl_pct": 15.0,
      "close_reason": "take_profit",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 31.36,
      "position_usd": 209.1
    },
    {
      "ticker": "ARCB",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-06-11",
      "entry_price": 173.04,
      "allocated_usd": 500,
      "shares": 2.8895,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 199.0,
      "stop_loss": 169.58,
      "max_hold_date": "2026-06-15",
      "daily_prices": {
        "2026-06-12": {
          "open": 174.46,
          "high": 176.53,
          "low": 171.6,
          "close": 172.89,
          "pnl_pct": -0.09
        },
        "2026-06-15": {
          "open": 172.36,
          "high": 172.64,
          "low": 162.18,
          "close": 163.95,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-06-15",
      "close_price": 169.58,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.18,
      "position_usd": 209.1
    },
    {
      "ticker": "WEYS",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-06-12",
      "entry_price": 37.0,
      "allocated_usd": 500,
      "shares": 13.5135,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 42.55,
      "stop_loss": 36.26,
      "max_hold_date": "2026-06-16",
      "daily_prices": {
        "2026-06-15": {
          "open": 36.77,
          "high": 37.02,
          "low": 35.9,
          "close": 36.06,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-06-15",
      "close_price": 36.26,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.24,
      "position_usd": 212.24
    },
    {
      "ticker": "PBHC",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-06-12",
      "entry_price": 15.45,
      "allocated_usd": 500,
      "shares": 32.3625,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 17.77,
      "stop_loss": 15.14,
      "max_hold_date": "2026-06-16",
      "daily_prices": {
        "2026-06-15": {
          "open": 15.98,
          "high": 16.78,
          "low": 15.13,
          "close": 15.13,
          "pnl_pct": -2.01
        }
      },
      "close_date": "2026-06-15",
      "close_price": 15.14,
      "final_pnl_pct": -2.01,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.27,
      "position_usd": 212.24
    },
    {
      "ticker": "ARCB",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-06-12",
      "entry_price": 173.04,
      "allocated_usd": 500,
      "shares": 2.8895,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 147.08,
      "stop_loss": 176.5,
      "max_hold_date": "2026-06-16",
      "daily_prices": {
        "2026-06-15": {
          "open": 172.36,
          "high": 172.64,
          "low": 162.18,
          "close": 163.95,
          "pnl_pct": 5.25
        },
        "2026-06-16": {
          "open": 165.03,
          "high": 166.79,
          "low": 159.08,
          "close": 159.66,
          "pnl_pct": 7.73
        }
      },
      "close_date": "2026-06-16",
      "close_price": 159.66,
      "final_pnl_pct": 7.73,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 16.41,
      "position_usd": 212.24
    },
    {
      "ticker": "MFIN",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-06-15",
      "entry_price": 9.81,
      "allocated_usd": 500,
      "shares": 50.9684,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 8.34,
      "stop_loss": 10.01,
      "max_hold_date": "2026-06-17",
      "daily_prices": {
        "2026-06-16": {
          "open": 9.78,
          "high": 9.97,
          "low": 9.7,
          "close": 9.75,
          "pnl_pct": 0.61
        },
        "2026-06-17": {
          "open": 9.77,
          "high": 9.81,
          "low": 9.35,
          "close": 9.4,
          "pnl_pct": 4.18
        }
      },
      "close_date": "2026-06-17",
      "close_price": 9.4,
      "final_pnl_pct": 4.18,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 8.82,
      "position_usd": 210.97
    },
    {
      "ticker": "CHEF",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-06-17",
      "entry_price": 93.14,
      "allocated_usd": 500,
      "shares": 5.3683,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 79.17,
      "stop_loss": 95.0,
      "max_hold_date": "2026-06-19",
      "daily_prices": {
        "2026-06-18": {
          "open": 93.72,
          "high": 96.38,
          "low": 91.68,
          "close": 95.4,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-06-18",
      "close_price": 95.0,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.27,
      "position_usd": 213.49
    },
    {
      "ticker": "HOFT",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-06-18",
      "entry_price": 15.61,
      "allocated_usd": 500,
      "shares": 32.0307,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 17.95,
      "stop_loss": 15.3,
      "max_hold_date": "2026-06-22",
      "daily_prices": {
        "2026-06-22": {
          "open": 16.38,
          "high": 17.5,
          "low": 16.12,
          "close": 16.86,
          "pnl_pct": 8.01
        }
      },
      "close_date": "2026-06-22",
      "close_price": 16.86,
      "final_pnl_pct": 8.01,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 17.07,
      "position_usd": 213.06
    },
    {
      "ticker": "SWBI",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-06-18",
      "entry_price": 16.15,
      "allocated_usd": 500,
      "shares": 30.9598,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 13.73,
      "stop_loss": 16.47,
      "max_hold_date": "2026-06-22",
      "daily_prices": {
        "2026-06-22": {
          "open": 15.79,
          "high": 16.27,
          "low": 14.25,
          "close": 16.15,
          "pnl_pct": -0.0
        }
      },
      "close_date": "2026-06-22",
      "close_price": 16.15,
      "final_pnl_pct": -0.0,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -0.0,
      "position_usd": 213.06
    },
    {
      "ticker": "WSBC",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-06-18",
      "entry_price": 35.92,
      "allocated_usd": 500,
      "shares": 13.9198,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 41.31,
      "stop_loss": 35.2,
      "max_hold_date": "2026-06-22",
      "daily_prices": {
        "2026-06-22": {
          "open": 35.77,
          "high": 36.51,
          "low": 35.77,
          "close": 36.36,
          "pnl_pct": 1.22
        }
      },
      "close_date": "2026-06-22",
      "close_price": 36.36,
      "final_pnl_pct": 1.22,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 2.6,
      "position_usd": 213.06
    },
    {
      "ticker": "SWBI",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-06-22",
      "entry_price": 16.08,
      "allocated_usd": 500,
      "shares": 31.0945,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 13.67,
      "stop_loss": 16.4,
      "max_hold_date": "2026-06-24",
      "daily_prices": {
        "2026-06-23": {
          "open": 15.87,
          "high": 17.18,
          "low": 15.72,
          "close": 16.36,
          "pnl_pct": -1.99
        }
      },
      "close_date": "2026-06-23",
      "close_price": 16.4,
      "final_pnl_pct": -1.99,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.28,
      "position_usd": 215.03
    },
    {
      "ticker": "HOFT",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-06-22",
      "entry_price": 15.8,
      "allocated_usd": 500,
      "shares": 31.6456,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 18.17,
      "stop_loss": 15.48,
      "max_hold_date": "2026-06-24",
      "daily_prices": {
        "2026-06-23": {
          "open": 16.85,
          "high": 17.46,
          "low": 16.51,
          "close": 17.11,
          "pnl_pct": 8.29
        },
        "2026-06-24": {
          "open": 17.22,
          "high": 17.46,
          "low": 16.68,
          "close": 16.91,
          "pnl_pct": 7.03
        }
      },
      "close_date": "2026-06-24",
      "close_price": 16.91,
      "final_pnl_pct": 7.03,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 15.12,
      "position_usd": 215.03
    },
    {
      "ticker": "HBNC",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-06-22",
      "entry_price": 19.34,
      "allocated_usd": 500,
      "shares": 25.8532,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 16.44,
      "stop_loss": 19.73,
      "max_hold_date": "2026-06-24",
      "daily_prices": {
        "2026-06-23": {
          "open": 19.26,
          "high": 19.56,
          "low": 19.15,
          "close": 19.53,
          "pnl_pct": -0.98
        },
        "2026-06-24": {
          "open": 19.55,
          "high": 19.65,
          "low": 19.45,
          "close": 19.65,
          "pnl_pct": -1.6
        }
      },
      "close_date": "2026-06-24",
      "close_price": 19.65,
      "final_pnl_pct": -1.6,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -3.44,
      "position_usd": 215.03
    },
    {
      "ticker": "SBFG",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-06-22",
      "entry_price": 23.01,
      "allocated_usd": 500,
      "shares": 21.7297,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 26.46,
      "stop_loss": 22.55,
      "max_hold_date": "2026-06-24",
      "daily_prices": {
        "2026-06-23": {
          "open": 22.8,
          "high": 23.15,
          "low": 22.67,
          "close": 23.01,
          "pnl_pct": 0.0
        },
        "2026-06-24": {
          "open": 23.11,
          "high": 23.91,
          "low": 22.72,
          "close": 23.67,
          "pnl_pct": 2.87
        }
      },
      "close_date": "2026-06-24",
      "close_price": 23.67,
      "final_pnl_pct": 2.87,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 6.17,
      "position_usd": 215.03
    },
    {
      "ticker": "SNEX",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-06-23",
      "entry_price": 138.79,
      "allocated_usd": 500,
      "shares": 3.6026,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 117.97,
      "stop_loss": 141.57,
      "max_hold_date": "2026-06-25",
      "daily_prices": {
        "2026-06-24": {
          "open": 92.0,
          "high": 93.26,
          "low": 89.16,
          "close": 90.75,
          "pnl_pct": 15.0
        }
      },
      "close_date": "2026-06-24",
      "close_price": 117.97,
      "final_pnl_pct": 15.0,
      "close_reason": "take_profit",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 32.19,
      "position_usd": 214.6
    },
    {
      "ticker": "OBT",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-06-24",
      "entry_price": 36.5,
      "allocated_usd": 500,
      "shares": 13.6986,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 41.97,
      "stop_loss": 35.77,
      "max_hold_date": "2026-06-26",
      "daily_prices": {
        "2026-06-25": {
          "open": 36.38,
          "high": 37.02,
          "low": 36.38,
          "close": 36.72,
          "pnl_pct": 0.6
        },
        "2026-06-26": {
          "open": 36.85,
          "high": 37.53,
          "low": 36.33,
          "close": 36.78,
          "pnl_pct": 0.77
        }
      },
      "close_date": "2026-06-26",
      "close_price": 36.78,
      "final_pnl_pct": 0.77,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 1.69,
      "position_usd": 219.6
    },
    {
      "ticker": "FISI",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-06-24",
      "entry_price": 38.4,
      "allocated_usd": 500,
      "shares": 13.0208,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 44.16,
      "stop_loss": 37.63,
      "max_hold_date": "2026-06-26",
      "daily_prices": {
        "2026-06-25": {
          "open": 38.37,
          "high": 38.88,
          "low": 38.1,
          "close": 38.4,
          "pnl_pct": 0.0
        },
        "2026-06-26": {
          "open": 38.4,
          "high": 38.96,
          "low": 37.74,
          "close": 38.63,
          "pnl_pct": 0.6
        }
      },
      "close_date": "2026-06-26",
      "close_price": 38.63,
      "final_pnl_pct": 0.6,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 1.32,
      "position_usd": 219.6
    },
    {
      "ticker": "SWBI",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-06-24",
      "entry_price": 16.67,
      "allocated_usd": 500,
      "shares": 29.994,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 14.17,
      "stop_loss": 17.0,
      "max_hold_date": "2026-06-26",
      "daily_prices": {
        "2026-06-25": {
          "open": 15.89,
          "high": 16.09,
          "low": 15.32,
          "close": 15.4,
          "pnl_pct": 7.62
        },
        "2026-06-26": {
          "open": 15.26,
          "high": 15.41,
          "low": 14.57,
          "close": 14.95,
          "pnl_pct": 10.32
        }
      },
      "close_date": "2026-06-26",
      "close_price": 14.95,
      "final_pnl_pct": 10.32,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 22.66,
      "position_usd": 219.6
    },
    {
      "ticker": "WSBC",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-06-25",
      "entry_price": 37.86,
      "allocated_usd": 500,
      "shares": 13.2066,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 43.54,
      "stop_loss": 37.1,
      "max_hold_date": "2026-06-29",
      "daily_prices": {
        "2026-06-26": {
          "open": 38.25,
          "high": 38.89,
          "low": 38.15,
          "close": 38.44,
          "pnl_pct": 1.53
        },
        "2026-06-29": {
          "open": 38.22,
          "high": 38.45,
          "low": 37.87,
          "close": 38.43,
          "pnl_pct": 1.51
        }
      },
      "close_date": "2026-06-29",
      "close_price": 38.43,
      "final_pnl_pct": 1.51,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 3.32,
      "position_usd": 219.6
    },
    {
      "ticker": "TSBK",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-06-26",
      "entry_price": 44.88,
      "allocated_usd": 500,
      "shares": 11.1408,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 38.15,
      "stop_loss": 45.78,
      "max_hold_date": "2026-06-30",
      "daily_prices": {
        "2026-06-29": {
          "open": 44.49,
          "high": 44.5,
          "low": 43.76,
          "close": 44.33,
          "pnl_pct": 1.23
        },
        "2026-06-30": {
          "open": 44.17,
          "high": 44.51,
          "low": 43.71,
          "close": 44.51,
          "pnl_pct": 0.82
        }
      },
      "close_date": "2026-06-30",
      "close_price": 44.51,
      "final_pnl_pct": 0.82,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 1.82,
      "position_usd": 222.17
    },
    {
      "ticker": "SBFG",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-06-26",
      "entry_price": 23.2,
      "allocated_usd": 500,
      "shares": 21.5517,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 26.68,
      "stop_loss": 22.74,
      "max_hold_date": "2026-06-30",
      "daily_prices": {
        "2026-06-29": {
          "open": 24.57,
          "high": 24.76,
          "low": 23.48,
          "close": 24.32,
          "pnl_pct": 4.83
        },
        "2026-06-30": {
          "open": 24.36,
          "high": 25.52,
          "low": 23.98,
          "close": 25.12,
          "pnl_pct": 8.28
        }
      },
      "close_date": "2026-06-30",
      "close_price": 25.12,
      "final_pnl_pct": 8.28,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 18.4,
      "position_usd": 222.17
    },
    {
      "ticker": "PTGX",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-06-29",
      "entry_price": 121.88,
      "allocated_usd": 500,
      "shares": 4.1024,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 103.6,
      "stop_loss": 124.32,
      "max_hold_date": "2026-07-01",
      "daily_prices": {
        "2026-06-30": {
          "open": 122.04,
          "high": 124.71,
          "low": 119.57,
          "close": 122.58,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-06-30",
      "close_price": 124.32,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.45,
      "position_usd": 222.5
    },
    {
      "ticker": "SBFG",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-06-30",
      "entry_price": 24.46,
      "allocated_usd": 500,
      "shares": 20.4415,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 28.13,
      "stop_loss": 23.97,
      "max_hold_date": "2026-07-02",
      "daily_prices": {
        "2026-07-01": {
          "open": 25.29,
          "high": 25.58,
          "low": 23.75,
          "close": 25.44,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-07-01",
      "close_price": 23.97,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.48,
      "position_usd": 224.08
    },
    {
      "ticker": "SRRK",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-06-30",
      "entry_price": 54.96,
      "allocated_usd": 500,
      "shares": 9.0975,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 46.72,
      "stop_loss": 56.06,
      "max_hold_date": "2026-07-02",
      "daily_prices": {
        "2026-07-01": {
          "open": 54.79,
          "high": 55.02,
          "low": 52.84,
          "close": 52.84,
          "pnl_pct": 3.86
        },
        "2026-07-02": {
          "open": 52.8,
          "high": 54.94,
          "low": 51.32,
          "close": 54.88,
          "pnl_pct": 0.15
        }
      },
      "close_date": "2026-07-02",
      "close_price": 54.88,
      "final_pnl_pct": 0.15,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 0.34,
      "position_usd": 224.08
    },
    {
      "ticker": "SKWD",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-06-30",
      "entry_price": 60.19,
      "allocated_usd": 500,
      "shares": 8.307,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 51.16,
      "stop_loss": 61.39,
      "max_hold_date": "2026-07-02",
      "daily_prices": {
        "2026-07-01": {
          "open": 58.35,
          "high": 59.81,
          "low": 57.88,
          "close": 59.51,
          "pnl_pct": 1.13
        },
        "2026-07-02": {
          "open": 59.4,
          "high": 62.2,
          "low": 58.6,
          "close": 61.42,
          "pnl_pct": -1.99
        }
      },
      "close_date": "2026-07-02",
      "close_price": 61.39,
      "final_pnl_pct": -1.99,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.46,
      "position_usd": 224.08
    },
    {
      "ticker": "LGND",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-06-30",
      "entry_price": 314.04,
      "allocated_usd": 500,
      "shares": 1.5922,
      "actual_position_usd": 500.01,
      "entry_commission": 1.0,
      "take_profit": 266.93,
      "stop_loss": 320.32,
      "max_hold_date": "2026-07-02",
      "daily_prices": {
        "2026-07-01": {
          "open": 315.2,
          "high": 318.41,
          "low": 305.31,
          "close": 312.01,
          "pnl_pct": 0.65
        },
        "2026-07-02": {
          "open": 314.81,
          "high": 320.0,
          "low": 308.76,
          "close": 319.55,
          "pnl_pct": -1.75
        }
      },
      "close_date": "2026-07-02",
      "close_price": 319.55,
      "final_pnl_pct": -1.75,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -3.92,
      "position_usd": 224.08
    },
    {
      "ticker": "SBFG",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-07-01",
      "entry_price": 25.27,
      "allocated_usd": 500,
      "shares": 19.7863,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 29.06,
      "stop_loss": 24.76,
      "max_hold_date": "2026-07-03",
      "daily_prices": {
        "2026-07-02": {
          "open": 25.5,
          "high": 25.85,
          "low": 24.63,
          "close": 24.93,
          "pnl_pct": -2.02
        }
      },
      "close_date": "2026-07-02",
      "close_price": 24.76,
      "final_pnl_pct": -2.02,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.52,
      "position_usd": 223.63
    },
    {
      "ticker": "LGND",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-02",
      "entry_price": 312.01,
      "allocated_usd": 500,
      "shares": 1.6025,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 265.21,
      "stop_loss": 318.25,
      "max_hold_date": "2026-07-06",
      "daily_prices": {
        "2026-07-06": {
          "open": 319.94,
          "high": 322.31,
          "low": 315.76,
          "close": 320.42,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-07-06",
      "close_price": 318.25,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.45,
      "position_usd": 222.38
    },
    {
      "ticker": "SKWD",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-07-02",
      "entry_price": 59.51,
      "allocated_usd": 500,
      "shares": 8.4019,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 68.44,
      "stop_loss": 58.32,
      "max_hold_date": "2026-07-06",
      "daily_prices": {
        "2026-07-06": {
          "open": 61.0,
          "high": 61.37,
          "low": 59.29,
          "close": 60.2,
          "pnl_pct": 1.16
        }
      },
      "close_date": "2026-07-06",
      "close_price": 60.2,
      "final_pnl_pct": 1.16,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 2.58,
      "position_usd": 222.38
    },
    {
      "ticker": "MVBF",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-02",
      "entry_price": 29.84,
      "allocated_usd": 500,
      "shares": 16.756,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 25.36,
      "stop_loss": 30.44,
      "max_hold_date": "2026-07-06",
      "daily_prices": {
        "2026-07-06": {
          "open": 29.12,
          "high": 29.6,
          "low": 28.54,
          "close": 28.75,
          "pnl_pct": 3.65
        }
      },
      "close_date": "2026-07-06",
      "close_price": 28.75,
      "final_pnl_pct": 3.65,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 8.12,
      "position_usd": 222.38
    },
    {
      "ticker": "SBFG",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-02",
      "entry_price": 25.59,
      "allocated_usd": 500,
      "shares": 19.5389,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 21.75,
      "stop_loss": 26.1,
      "max_hold_date": "2026-07-06",
      "daily_prices": {
        "2026-07-06": {
          "open": 24.93,
          "high": 25.84,
          "low": 24.76,
          "close": 25.84,
          "pnl_pct": -0.98
        }
      },
      "close_date": "2026-07-06",
      "close_price": 25.84,
      "final_pnl_pct": -0.98,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -2.18,
      "position_usd": 222.38
    },
    {
      "ticker": "UTMD",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-06",
      "entry_price": 72.78,
      "allocated_usd": 500,
      "shares": 6.87,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 61.86,
      "stop_loss": 74.24,
      "max_hold_date": "2026-07-08",
      "daily_prices": {
        "2026-07-07": {
          "open": 71.23,
          "high": 71.23,
          "low": 68.85,
          "close": 69.04,
          "pnl_pct": 5.14
        },
        "2026-07-08": {
          "open": 67.92,
          "high": 69.2,
          "low": 66.97,
          "close": 67.78,
          "pnl_pct": 6.87
        }
      },
      "close_date": "2026-07-08",
      "close_price": 67.78,
      "final_pnl_pct": 6.87,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 15.31,
      "position_usd": 222.78
    },
    {
      "ticker": "OBT",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-06",
      "entry_price": 37.65,
      "allocated_usd": 500,
      "shares": 13.2802,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 32.0,
      "stop_loss": 38.4,
      "max_hold_date": "2026-07-08",
      "daily_prices": {
        "2026-07-07": {
          "open": 37.5,
          "high": 37.81,
          "low": 36.15,
          "close": 36.32,
          "pnl_pct": 3.53
        },
        "2026-07-08": {
          "open": 36.2,
          "high": 36.51,
          "low": 35.43,
          "close": 36.03,
          "pnl_pct": 4.3
        }
      },
      "close_date": "2026-07-08",
      "close_price": 36.03,
      "final_pnl_pct": 4.3,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 9.58,
      "position_usd": 222.78
    },
    {
      "ticker": "MVBF",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-06",
      "entry_price": 29.41,
      "allocated_usd": 500,
      "shares": 17.001,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 25.0,
      "stop_loss": 30.0,
      "max_hold_date": "2026-07-08",
      "daily_prices": {
        "2026-07-07": {
          "open": 28.99,
          "high": 29.14,
          "low": 28.41,
          "close": 28.46,
          "pnl_pct": 3.23
        },
        "2026-07-08": {
          "open": 28.33,
          "high": 28.33,
          "low": 27.45,
          "close": 27.85,
          "pnl_pct": 5.3
        }
      },
      "close_date": "2026-07-08",
      "close_price": 27.85,
      "final_pnl_pct": 5.3,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 11.81,
      "position_usd": 222.78
    },
    {
      "ticker": "AOUT",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-07",
      "entry_price": 14.28,
      "allocated_usd": 500,
      "shares": 35.014,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 12.14,
      "stop_loss": 14.57,
      "max_hold_date": "2026-07-09",
      "daily_prices": {
        "2026-07-08": {
          "open": 13.91,
          "high": 14.25,
          "low": 13.65,
          "close": 13.93,
          "pnl_pct": 2.45
        },
        "2026-07-09": {
          "open": 13.83,
          "high": 14.28,
          "low": 13.5,
          "close": 14.27,
          "pnl_pct": 0.07
        }
      },
      "close_date": "2026-07-09",
      "close_price": 14.27,
      "final_pnl_pct": 0.07,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 0.16,
      "position_usd": 222.78
    },
    {
      "ticker": "ITIC",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-08",
      "entry_price": 276.75,
      "allocated_usd": 500,
      "shares": 1.8067,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 235.24,
      "stop_loss": 282.29,
      "max_hold_date": "2026-07-10",
      "daily_prices": {
        "2026-07-09": {
          "open": 273.59,
          "high": 274.0,
          "low": 270.55,
          "close": 271.94,
          "pnl_pct": 1.74
        },
        "2026-07-10": {
          "open": 272.87,
          "high": 277.42,
          "low": 270.99,
          "close": 275.57,
          "pnl_pct": 0.43
        }
      },
      "close_date": "2026-07-10",
      "close_price": 275.57,
      "final_pnl_pct": 0.43,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 0.97,
      "position_usd": 226.45
    },
    {
      "ticker": "TRVI",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-08",
      "entry_price": 19.5,
      "allocated_usd": 500,
      "shares": 25.641,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 16.57,
      "stop_loss": 19.89,
      "max_hold_date": "2026-07-10",
      "daily_prices": {
        "2026-07-09": {
          "open": 18.62,
          "high": 18.93,
          "low": 18.32,
          "close": 18.4,
          "pnl_pct": 5.64
        },
        "2026-07-10": {
          "open": 18.32,
          "high": 18.33,
          "low": 17.52,
          "close": 17.84,
          "pnl_pct": 8.51
        }
      },
      "close_date": "2026-07-10",
      "close_price": 17.84,
      "final_pnl_pct": 8.51,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 19.27,
      "position_usd": 226.45
    },
    {
      "ticker": "LGND",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-08",
      "entry_price": 319.43,
      "allocated_usd": 500,
      "shares": 1.5653,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 271.52,
      "stop_loss": 325.82,
      "max_hold_date": "2026-07-10",
      "daily_prices": {
        "2026-07-09": {
          "open": 320.08,
          "high": 323.33,
          "low": 315.02,
          "close": 322.61,
          "pnl_pct": -1.0
        },
        "2026-07-10": {
          "open": 322.23,
          "high": 322.81,
          "low": 310.67,
          "close": 316.24,
          "pnl_pct": 1.0
        }
      },
      "close_date": "2026-07-10",
      "close_price": 316.24,
      "final_pnl_pct": 1.0,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 2.26,
      "position_usd": 226.45
    },
    {
      "ticker": "ITIC",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-09",
      "entry_price": 273.45,
      "allocated_usd": 500,
      "shares": 1.8285,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 232.43,
      "stop_loss": 278.92,
      "max_hold_date": "2026-07-13",
      "daily_prices": {
        "2026-07-10": {
          "open": 272.87,
          "high": 277.42,
          "low": 270.99,
          "close": 275.57,
          "pnl_pct": -0.78
        },
        "2026-07-13": {
          "open": 275.57,
          "high": 280.42,
          "low": 269.04,
          "close": 278.76,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-07-13",
      "close_price": 278.92,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.53,
      "position_usd": 226.47
    },
    {
      "ticker": "PTGX",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-10",
      "entry_price": 131.81,
      "allocated_usd": 500,
      "shares": 3.7933,
      "actual_position_usd": 499.99,
      "entry_commission": 1.0,
      "take_profit": 112.04,
      "stop_loss": 134.45,
      "max_hold_date": "2026-07-14",
      "daily_prices": {
        "2026-07-13": {
          "open": 130.05,
          "high": 131.36,
          "low": 125.32,
          "close": 129.89,
          "pnl_pct": 1.46
        },
        "2026-07-14": {
          "open": 131.89,
          "high": 131.95,
          "low": 128.68,
          "close": 131.27,
          "pnl_pct": 0.41
        }
      },
      "close_date": "2026-07-14",
      "close_price": 131.27,
      "final_pnl_pct": 0.41,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 0.94,
      "position_usd": 228.72
    },
    {
      "ticker": "YORW",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-10",
      "entry_price": 30.8,
      "allocated_usd": 500,
      "shares": 16.2338,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 26.18,
      "stop_loss": 31.42,
      "max_hold_date": "2026-07-14",
      "daily_prices": {
        "2026-07-13": {
          "open": 30.78,
          "high": 31.03,
          "low": 30.61,
          "close": 30.97,
          "pnl_pct": -0.55
        },
        "2026-07-14": {
          "open": 30.97,
          "high": 31.34,
          "low": 30.91,
          "close": 31.0,
          "pnl_pct": -0.65
        }
      },
      "close_date": "2026-07-14",
      "close_price": 31.0,
      "final_pnl_pct": -0.65,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -1.49,
      "position_usd": 228.72
    },
    {
      "ticker": "ITIC",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-13",
      "entry_price": 276.0,
      "allocated_usd": 500,
      "shares": 1.8116,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 234.6,
      "stop_loss": 281.52,
      "max_hold_date": "2026-07-15",
      "daily_prices": {
        "2026-07-14": {
          "open": 277.78,
          "high": 280.7,
          "low": 277.0,
          "close": 278.28,
          "pnl_pct": -0.83
        },
        "2026-07-15": {
          "open": 273.12,
          "high": 278.86,
          "low": 271.11,
          "close": 273.17,
          "pnl_pct": 1.03
        }
      },
      "close_date": "2026-07-15",
      "close_price": 273.17,
      "final_pnl_pct": 1.03,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 2.35,
      "position_usd": 228.27
    },
    {
      "ticker": "PTGX",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-13",
      "entry_price": 131.42,
      "allocated_usd": 500,
      "shares": 3.8046,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 111.71,
      "stop_loss": 134.05,
      "max_hold_date": "2026-07-15",
      "daily_prices": {
        "2026-07-14": {
          "open": 131.89,
          "high": 131.95,
          "low": 128.68,
          "close": 131.27,
          "pnl_pct": 0.11
        },
        "2026-07-15": {
          "open": 128.0,
          "high": 139.22,
          "low": 126.97,
          "close": 135.46,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-07-15",
      "close_price": 134.05,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.57,
      "position_usd": 228.27
    },
    {
      "ticker": "STRS",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-14",
      "entry_price": 20.93,
      "allocated_usd": 500,
      "shares": 23.8892,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 17.79,
      "stop_loss": 21.35,
      "max_hold_date": "2026-07-16",
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
          "pnl_pct": 1.24
        }
      },
      "close_date": "2026-07-16",
      "close_price": 20.67,
      "final_pnl_pct": 1.24,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 2.83,
      "position_usd": 228.21
    },
    {
      "ticker": "TCBK",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-14",
      "entry_price": 60.07,
      "allocated_usd": 500,
      "shares": 8.3236,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 51.06,
      "stop_loss": 61.27,
      "max_hold_date": "2026-07-16",
      "daily_prices": {
        "2026-07-15": {
          "open": 59.03,
          "high": 59.53,
          "low": 58.2,
          "close": 59.03,
          "pnl_pct": 1.73
        },
        "2026-07-16": {
          "open": 59.12,
          "high": 61.3,
          "low": 58.91,
          "close": 61.21,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-07-16",
      "close_price": 61.27,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.56,
      "position_usd": 228.21
    },
    {
      "ticker": "TRVI",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-15",
      "entry_price": 17.91,
      "allocated_usd": 500,
      "shares": 27.9174,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 15.22,
      "stop_loss": 18.27,
      "max_hold_date": "2026-07-17",
      "daily_prices": {
        "2026-07-16": {
          "open": 17.97,
          "high": 18.13,
          "low": 17.02,
          "close": 17.36,
          "pnl_pct": 3.07
        },
        "2026-07-17": {
          "open": 17.58,
          "high": 20.22,
          "low": 17.23,
          "close": 19.07,
          "pnl_pct": -2.01
        }
      },
      "close_date": "2026-07-17",
      "close_price": 18.27,
      "final_pnl_pct": -2.01,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.58,
      "position_usd": 227.99
    },
    {
      "ticker": "SMPL",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-15",
      "entry_price": 12.35,
      "allocated_usd": 500,
      "shares": 40.4858,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 10.5,
      "stop_loss": 12.6,
      "max_hold_date": "2026-07-17",
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
        }
      },
      "close_date": "2026-07-17",
      "close_price": 11.08,
      "final_pnl_pct": 10.28,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 23.44,
      "position_usd": 227.99
    },
    {
      "ticker": "STRS",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-07-16",
      "entry_price": 20.7,
      "allocated_usd": 500,
      "shares": 24.1546,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 23.8,
      "stop_loss": 20.29,
      "max_hold_date": "2026-07-20",
      "daily_prices": {
        "2026-07-17": {
          "open": 20.82,
          "high": 21.05,
          "low": 20.23,
          "close": 20.72,
          "pnl_pct": -1.98
        }
      },
      "close_date": "2026-07-17",
      "close_price": 20.29,
      "final_pnl_pct": -1.98,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.51,
      "position_usd": 227.82
    },
    {
      "ticker": "PBHC",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-16",
      "entry_price": 16.24,
      "allocated_usd": 500,
      "shares": 30.7882,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 13.8,
      "stop_loss": 16.56,
      "max_hold_date": "2026-07-20",
      "daily_prices": {
        "2026-07-17": {
          "open": 15.76,
          "high": 16.71,
          "low": 15.76,
          "close": 16.39,
          "pnl_pct": -1.97
        }
      },
      "close_date": "2026-07-17",
      "close_price": 16.56,
      "final_pnl_pct": -1.97,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.49,
      "position_usd": 227.82
    },
    {
      "ticker": "TCBK",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-17",
      "entry_price": 61.2,
      "allocated_usd": 500,
      "shares": 8.1699,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 52.02,
      "stop_loss": 62.42,
      "max_hold_date": "2026-07-21",
      "daily_prices": {
        "2026-07-20": {
          "open": 60.2,
          "high": 60.2,
          "low": 59.21,
          "close": 59.4,
          "pnl_pct": 2.94
        },
        "2026-07-21": {
          "open": 59.19,
          "high": 59.67,
          "low": 58.98,
          "close": 59.64,
          "pnl_pct": 2.55
        }
      },
      "close_date": "2026-07-21",
      "close_price": 59.64,
      "final_pnl_pct": 2.55,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 5.83,
      "position_usd": 228.8
    },
    {
      "ticker": "CDNA",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-07-17",
      "entry_price": 38.67,
      "allocated_usd": 500,
      "shares": 12.9299,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 44.47,
      "stop_loss": 37.9,
      "max_hold_date": "2026-07-21",
      "daily_prices": {
        "2026-07-20": {
          "open": 39.3,
          "high": 39.84,
          "low": 38.03,
          "close": 38.37,
          "pnl_pct": -0.78
        },
        "2026-07-21": {
          "open": 37.7,
          "high": 39.22,
          "low": 37.25,
          "close": 38.54,
          "pnl_pct": -1.99
        }
      },
      "close_date": "2026-07-21",
      "close_price": 37.9,
      "final_pnl_pct": -1.99,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.55,
      "position_usd": 228.8
    },
    {
      "ticker": "PBHC",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-07-17",
      "entry_price": 16.15,
      "allocated_usd": 500,
      "shares": 30.9598,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 18.57,
      "stop_loss": 15.83,
      "max_hold_date": "2026-07-21",
      "daily_prices": {
        "2026-07-20": {
          "open": 16.08,
          "high": 16.08,
          "low": 16.05,
          "close": 16.05,
          "pnl_pct": -0.62
        },
        "2026-07-21": {
          "open": 15.86,
          "high": 16.26,
          "low": 15.82,
          "close": 16.0,
          "pnl_pct": -1.98
        }
      },
      "close_date": "2026-07-21",
      "close_price": 15.83,
      "final_pnl_pct": -1.98,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.53,
      "position_usd": 228.8
    },
    {
      "ticker": "UTMD",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-20",
      "entry_price": 69.8,
      "allocated_usd": 500,
      "shares": 7.1633,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 59.33,
      "stop_loss": 71.2,
      "max_hold_date": "2026-07-22",
      "daily_prices": {
        "2026-07-21": {
          "open": 68.23,
          "high": 69.22,
          "low": 67.06,
          "close": 68.86,
          "pnl_pct": 1.35
        },
        "2026-07-22": {
          "open": 68.51,
          "high": 70.57,
          "low": 67.95,
          "close": 68.9,
          "pnl_pct": 1.29
        }
      },
      "close_date": "2026-07-22",
      "close_price": 68.9,
      "final_pnl_pct": 1.29,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 2.95,
      "position_usd": 228.8
    },
    {
      "ticker": "ACIW",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-21",
      "entry_price": 56.87,
      "allocated_usd": 500,
      "shares": 8.792,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 48.34,
      "stop_loss": 58.01,
      "max_hold_date": "2026-07-23",
      "daily_prices": {
        "2026-07-22": {
          "open": 56.36,
          "high": 57.2,
          "low": 54.25,
          "close": 54.71,
          "pnl_pct": 3.8
        },
        "2026-07-23": {
          "open": 54.64,
          "high": 55.28,
          "low": 53.98,
          "close": 54.53,
          "pnl_pct": 4.11
        }
      },
      "close_date": "2026-07-23",
      "close_price": 54.53,
      "final_pnl_pct": 4.11,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 9.39,
      "position_usd": 228.48
    },
    {
      "ticker": "CHEF",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-21",
      "entry_price": 95.58,
      "allocated_usd": 500,
      "shares": 5.2312,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 81.24,
      "stop_loss": 97.49,
      "max_hold_date": "2026-07-23",
      "daily_prices": {
        "2026-07-22": {
          "open": 95.49,
          "high": 96.17,
          "low": 92.28,
          "close": 93.93,
          "pnl_pct": 1.73
        },
        "2026-07-23": {
          "open": 92.48,
          "high": 95.41,
          "low": 91.76,
          "close": 94.48,
          "pnl_pct": 1.15
        }
      },
      "close_date": "2026-07-23",
      "close_price": 94.48,
      "final_pnl_pct": 1.15,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 2.63,
      "position_usd": 228.48
    },
    {
      "ticker": "CDNA",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-22",
      "entry_price": 38.54,
      "allocated_usd": 500,
      "shares": 12.9735,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 32.76,
      "stop_loss": 39.31,
      "max_hold_date": "2026-07-24",
      "daily_prices": {
        "2026-07-23": {
          "open": 38.44,
          "high": 38.72,
          "low": 37.38,
          "close": 37.61,
          "pnl_pct": 2.41
        },
        "2026-07-24": {
          "open": 37.8,
          "high": 38.48,
          "low": 37.05,
          "close": 37.14,
          "pnl_pct": 3.63
        }
      },
      "close_date": "2026-07-24",
      "close_price": 37.14,
      "final_pnl_pct": 3.63,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 8.3,
      "position_usd": 228.77
    },
    {
      "ticker": "XNCR",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-22",
      "entry_price": 20.45,
      "allocated_usd": 500,
      "shares": 24.4499,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 17.38,
      "stop_loss": 20.86,
      "max_hold_date": "2026-07-24",
      "daily_prices": {
        "2026-07-23": {
          "open": 19.18,
          "high": 20.02,
          "low": 18.83,
          "close": 19.53,
          "pnl_pct": 4.5
        },
        "2026-07-24": {
          "open": 19.53,
          "high": 19.9,
          "low": 18.94,
          "close": 19.44,
          "pnl_pct": 4.94
        }
      },
      "close_date": "2026-07-24",
      "close_price": 19.44,
      "final_pnl_pct": 4.94,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 11.3,
      "position_usd": 228.77
    },
    {
      "ticker": "LCNB",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-23",
      "entry_price": 19.57,
      "allocated_usd": 500,
      "shares": 25.5493,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 16.63,
      "stop_loss": 19.96,
      "max_hold_date": "2026-07-27",
      "daily_prices": {
        "2026-07-24": {
          "open": 19.39,
          "high": 20.05,
          "low": 18.96,
          "close": 19.77,
          "pnl_pct": -1.99
        }
      },
      "close_date": "2026-07-24",
      "close_price": 19.96,
      "final_pnl_pct": -1.99,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.58,
      "position_usd": 229.97
    },
    {
      "ticker": "CDNA",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-07-23",
      "entry_price": 37.78,
      "allocated_usd": 500,
      "shares": 13.2345,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 43.45,
      "stop_loss": 37.02,
      "max_hold_date": "2026-07-27",
      "daily_prices": {
        "2026-07-24": {
          "open": 37.8,
          "high": 38.48,
          "low": 37.05,
          "close": 37.14,
          "pnl_pct": -1.69
        },
        "2026-07-27": {
          "open": 37.21,
          "high": 37.74,
          "low": 36.25,
          "close": 36.36,
          "pnl_pct": -2.01
        }
      },
      "close_date": "2026-07-27",
      "close_price": 37.02,
      "final_pnl_pct": -2.01,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.62,
      "position_usd": 229.97
    },
    {
      "ticker": "HBCP",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-24",
      "entry_price": 69.86,
      "allocated_usd": 500,
      "shares": 7.1572,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 59.38,
      "stop_loss": 71.26,
      "max_hold_date": "2026-07-28",
      "daily_prices": {
        "2026-07-27": {
          "open": 70.19,
          "high": 71.06,
          "low": 69.51,
          "close": 69.96,
          "pnl_pct": -0.14
        },
        "2026-07-28": {
          "open": 69.96,
          "high": 71.71,
          "low": 69.96,
          "close": 71.28,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-07-28",
      "close_price": 71.26,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.63,
      "position_usd": 231.48
    },
    {
      "ticker": "HFWA",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-24",
      "entry_price": 30.22,
      "allocated_usd": 500,
      "shares": 16.5453,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 25.69,
      "stop_loss": 30.82,
      "max_hold_date": "2026-07-28",
      "daily_prices": {
        "2026-07-27": {
          "open": 29.96,
          "high": 30.48,
          "low": 29.54,
          "close": 29.56,
          "pnl_pct": 2.18
        },
        "2026-07-28": {
          "open": 29.77,
          "high": 30.6,
          "low": 29.39,
          "close": 29.65,
          "pnl_pct": 1.89
        }
      },
      "close_date": "2026-07-28",
      "close_price": 29.65,
      "final_pnl_pct": 1.89,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 4.37,
      "position_usd": 231.48
    },
    {
      "ticker": "LCNB",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-27",
      "entry_price": 20.0,
      "allocated_usd": 500,
      "shares": 25.0,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 17.0,
      "stop_loss": 20.4,
      "max_hold_date": "2026-07-29",
      "daily_prices": {
        "2026-07-28": {
          "open": 20.07,
          "high": 21.08,
          "low": 20.03,
          "close": 20.74,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-07-28",
      "close_price": 20.4,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.62,
      "position_usd": 231.01
    },
    {
      "ticker": "BANR",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-07-27",
      "entry_price": 70.29,
      "allocated_usd": 500,
      "shares": 7.1134,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 80.83,
      "stop_loss": 68.88,
      "max_hold_date": "2026-07-29",
      "daily_prices": {
        "2026-07-28": {
          "open": 70.31,
          "high": 70.53,
          "low": 69.31,
          "close": 70.03,
          "pnl_pct": -0.37
        },
        "2026-07-29": {
          "open": 69.69,
          "high": 70.17,
          "low": 68.93,
          "close": 69.44,
          "pnl_pct": -1.21
        }
      },
      "close_date": "2026-07-29",
      "close_price": 69.44,
      "final_pnl_pct": -1.21,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -2.8,
      "position_usd": 231.01
    },
    {
      "ticker": "ECPG",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-28",
      "entry_price": 94.45,
      "allocated_usd": 500,
      "shares": 5.2938,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 80.28,
      "stop_loss": 96.34,
      "max_hold_date": "2026-07-30",
      "daily_prices": {
        "2026-07-29": {
          "open": 95.16,
          "high": 97.8,
          "low": 93.4,
          "close": 93.83,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-07-29",
      "close_price": 96.34,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.61,
      "position_usd": 230.53
    },
    {
      "ticker": "LCNB",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-28",
      "entry_price": 20.36,
      "allocated_usd": 500,
      "shares": 24.558,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 17.31,
      "stop_loss": 20.77,
      "max_hold_date": "2026-07-30",
      "daily_prices": {
        "2026-07-29": {
          "open": 20.54,
          "high": 21.01,
          "low": 19.98,
          "close": 20.07,
          "pnl_pct": -2.01
        }
      },
      "close_date": "2026-07-29",
      "close_price": 20.77,
      "final_pnl_pct": -2.01,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.63,
      "position_usd": 230.53
    },
    {
      "ticker": "ACNB",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-07-28",
      "entry_price": 64.0,
      "allocated_usd": 500,
      "shares": 7.8125,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 73.6,
      "stop_loss": 62.72,
      "max_hold_date": "2026-07-30",
      "daily_prices": {
        "2026-07-29": {
          "open": 63.82,
          "high": 64.3,
          "low": 63.1,
          "close": 63.12,
          "pnl_pct": -1.38
        },
        "2026-07-30": {
          "open": 63.35,
          "high": 64.15,
          "low": 62.64,
          "close": 63.42,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-07-30",
      "close_price": 62.72,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.61,
      "position_usd": 230.53
    },
    {
      "ticker": "IMMR",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-29",
      "entry_price": 7.62,
      "allocated_usd": 500,
      "shares": 65.6168,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 6.48,
      "stop_loss": 7.77,
      "max_hold_date": "2026-07-31",
      "daily_prices": {
        "2026-07-30": {
          "open": 7.36,
          "high": 7.57,
          "low": 7.21,
          "close": 7.41,
          "pnl_pct": 2.76
        },
        "2026-07-31": {
          "open": 7.38,
          "high": 7.6,
          "low": 7.38,
          "close": 7.56,
          "pnl_pct": 0.79
        }
      },
      "close_date": "2026-07-31",
      "close_price": 7.56,
      "final_pnl_pct": 0.79,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 1.81,
      "position_usd": 229.32
    },
    {
      "ticker": "RCKY",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-07-30",
      "entry_price": 49.1,
      "allocated_usd": 500,
      "shares": 10.1833,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 56.46,
      "stop_loss": 48.12,
      "max_hold_date": "2026-08-03",
      "daily_prices": {
        "2026-07-31": {
          "open": 48.66,
          "high": 49.3,
          "low": 45.99,
          "close": 48.66,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-07-31",
      "close_price": 48.12,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.58,
      "position_usd": 228.86
    },
    {
      "ticker": "IMMR",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-30",
      "entry_price": 7.33,
      "allocated_usd": 500,
      "shares": 68.2128,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 6.23,
      "stop_loss": 7.48,
      "max_hold_date": "2026-08-03",
      "daily_prices": {
        "2026-07-31": {
          "open": 7.38,
          "high": 7.6,
          "low": 7.38,
          "close": 7.56,
          "pnl_pct": -2.05
        }
      },
      "close_date": "2026-07-31",
      "close_price": 7.48,
      "final_pnl_pct": -2.05,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.69,
      "position_usd": 228.86
    },
    {
      "ticker": "UTMD",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-30",
      "entry_price": 70.94,
      "allocated_usd": 500,
      "shares": 7.0482,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 60.3,
      "stop_loss": 72.36,
      "max_hold_date": "2026-08-03",
      "daily_prices": {
        "2026-07-31": {
          "open": 69.73,
          "high": 70.46,
          "low": 69.12,
          "close": 70.22,
          "pnl_pct": 1.01
        },
        "2026-08-03": {
          "open": 71.71,
          "high": 74.7,
          "low": 70.73,
          "close": 72.45,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-08-03",
      "close_price": 72.36,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.58,
      "position_usd": 228.86
    },
    {
      "ticker": "GKOS",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-07-31",
      "entry_price": 167.87,
      "allocated_usd": 500,
      "shares": 2.9785,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 193.05,
      "stop_loss": 164.51,
      "max_hold_date": "2026-08-04",
      "daily_prices": {
        "2026-08-03": {
          "open": 168.66,
          "high": 173.98,
          "low": 168.6,
          "close": 170.87,
          "pnl_pct": 1.79
        },
        "2026-08-04": {
          "open": 171.75,
          "high": 172.91,
          "low": 167.64,
          "close": 170.53,
          "pnl_pct": 1.58
        }
      },
      "close_date": "2026-08-04",
      "close_price": 170.53,
      "final_pnl_pct": 1.58,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 3.6,
      "position_usd": 228.12
    },
    {
      "ticker": "IMMR",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-08-03",
      "entry_price": 7.56,
      "allocated_usd": 500,
      "shares": 66.1376,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 6.43,
      "stop_loss": 7.71,
      "max_hold_date": "2026-08-05",
      "daily_prices": {
        "2026-08-04": {
          "open": 7.58,
          "high": 7.78,
          "low": 7.56,
          "close": 7.73,
          "pnl_pct": -1.98
        }
      },
      "close_date": "2026-08-04",
      "close_price": 7.71,
      "final_pnl_pct": -1.98,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.51,
      "position_usd": 227.66
    },
    {
      "ticker": "GKOS",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-08-03",
      "entry_price": 166.72,
      "allocated_usd": 500,
      "shares": 2.999,
      "actual_position_usd": 499.99,
      "entry_commission": 1.0,
      "take_profit": 191.73,
      "stop_loss": 163.39,
      "max_hold_date": "2026-08-05",
      "daily_prices": {
        "2026-08-04": {
          "open": 171.75,
          "high": 172.91,
          "low": 167.64,
          "close": 170.53,
          "pnl_pct": 2.29
        },
        "2026-08-05": {
          "open": 172.01,
          "high": 172.01,
          "low": 167.81,
          "close": 170.93,
          "pnl_pct": 2.53
        }
      },
      "close_date": "2026-08-05",
      "close_price": 170.93,
      "final_pnl_pct": 2.53,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 5.76,
      "position_usd": 227.66
    },
    {
      "ticker": "CDNA",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-08-04",
      "entry_price": 47.03,
      "allocated_usd": 500,
      "shares": 10.6315,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 54.08,
      "stop_loss": 46.09,
      "max_hold_date": "2026-08-06",
      "daily_prices": {
        "2026-08-05": {
          "open": 47.0,
          "high": 47.08,
          "low": 45.39,
          "close": 45.5,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-08-05",
      "close_price": 46.09,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.55,
      "position_usd": 227.57
    },
    {
      "ticker": "STRA",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-08-04",
      "entry_price": 83.43,
      "allocated_usd": 500,
      "shares": 5.993,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 95.94,
      "stop_loss": 81.76,
      "max_hold_date": "2026-08-06",
      "daily_prices": {
        "2026-08-05": {
          "open": 83.97,
          "high": 84.33,
          "low": 82.58,
          "close": 82.95,
          "pnl_pct": -0.58
        },
        "2026-08-06": {
          "open": 82.95,
          "high": 83.19,
          "low": 77.24,
          "close": 81.86,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-08-06",
      "close_price": 81.76,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.55,
      "position_usd": 227.57
    },
    {
      "ticker": "CMCO",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-08-05",
      "entry_price": 21.59,
      "allocated_usd": 500,
      "shares": 23.1589,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 24.83,
      "stop_loss": 21.16,
      "max_hold_date": "2026-08-07",
      "daily_prices": {
        "2026-08-06": {
          "open": 21.43,
          "high": 22.21,
          "low": 20.45,
          "close": 20.69,
          "pnl_pct": -1.99
        }
      },
      "close_date": "2026-08-06",
      "close_price": 21.16,
      "final_pnl_pct": -1.99,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.53,
      "position_usd": 227.69
    },
    {
      "ticker": "CDNA",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-08-06",
      "entry_price": 45.5,
      "allocated_usd": 500,
      "shares": 10.989,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 38.67,
      "stop_loss": 46.41,
      "max_hold_date": "2026-08-10",
      "daily_prices": {
        "2026-08-07": {
          "open": 44.88,
          "high": 46.74,
          "low": 44.57,
          "close": 46.69,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-08-07",
      "close_price": 46.41,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.54,
      "position_usd": 226.78
    },
    {
      "ticker": "ESCA",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-08-06",
      "entry_price": 22.33,
      "allocated_usd": 500,
      "shares": 22.3914,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 25.68,
      "stop_loss": 21.88,
      "max_hold_date": "2026-08-10",
      "daily_prices": {
        "2026-08-07": {
          "open": 22.53,
          "high": 23.07,
          "low": 22.24,
          "close": 22.6,
          "pnl_pct": 1.21
        },
        "2026-08-10": {
          "open": 22.6,
          "high": 22.6,
          "low": 21.21,
          "close": 21.37,
          "pnl_pct": -2.02
        }
      },
      "close_date": "2026-08-10",
      "close_price": 21.88,
      "final_pnl_pct": -2.02,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.58,
      "position_usd": 226.78
    },
    {
      "ticker": "INBK",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-08-06",
      "entry_price": 29.34,
      "allocated_usd": 500,
      "shares": 17.0416,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 33.74,
      "stop_loss": 28.75,
      "max_hold_date": "2026-08-10",
      "daily_prices": {
        "2026-08-07": {
          "open": 29.3,
          "high": 29.43,
          "low": 28.91,
          "close": 29.21,
          "pnl_pct": -0.44
        },
        "2026-08-10": {
          "open": 29.24,
          "high": 29.87,
          "low": 28.93,
          "close": 29.32,
          "pnl_pct": -0.07
        }
      },
      "close_date": "2026-08-10",
      "close_price": 29.32,
      "final_pnl_pct": -0.07,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -0.16,
      "position_usd": 226.78
    },
    {
      "ticker": "MMSI",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-08-06",
      "entry_price": 87.18,
      "allocated_usd": 500,
      "shares": 5.7353,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 100.26,
      "stop_loss": 85.44,
      "max_hold_date": "2026-08-10",
      "daily_prices": {
        "2026-08-07": {
          "open": 88.09,
          "high": 89.27,
          "low": 87.47,
          "close": 89.04,
          "pnl_pct": 2.13
        },
        "2026-08-10": {
          "open": 89.04,
          "high": 90.59,
          "low": 88.99,
          "close": 89.75,
          "pnl_pct": 2.95
        }
      },
      "close_date": "2026-08-10",
      "close_price": 89.75,
      "final_pnl_pct": 2.95,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 6.69,
      "position_usd": 226.78
    },
    {
      "ticker": "PCRX",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-08-07",
      "entry_price": 25.58,
      "allocated_usd": 500,
      "shares": 19.5465,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 21.74,
      "stop_loss": 26.09,
      "max_hold_date": "2026-08-11",
      "daily_prices": {
        "2026-08-10": {
          "open": 24.74,
          "high": 25.25,
          "low": 24.24,
          "close": 24.43,
          "pnl_pct": 4.5
        },
        "2026-08-11": {
          "open": 24.49,
          "high": 24.78,
          "low": 24.26,
          "close": 24.38,
          "pnl_pct": 4.69
        }
      },
      "close_date": "2026-08-11",
      "close_price": 24.38,
      "final_pnl_pct": 4.69,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 10.61,
      "position_usd": 226.33
    },
    {
      "ticker": "NSIT",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-08-10",
      "entry_price": 149.32,
      "allocated_usd": 500,
      "shares": 3.3485,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 171.72,
      "stop_loss": 146.33,
      "max_hold_date": "2026-08-12",
      "daily_prices": {
        "2026-08-11": {
          "open": 153.39,
          "high": 155.99,
          "low": 150.76,
          "close": 150.95,
          "pnl_pct": 1.09
        },
        "2026-08-12": {
          "open": 151.17,
          "high": 155.74,
          "low": 149.69,
          "close": 154.67,
          "pnl_pct": 3.58
        }
      },
      "close_date": "2026-08-12",
      "close_price": 154.67,
      "final_pnl_pct": 3.58,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 8.11,
      "position_usd": 226.52
    },
    {
      "ticker": "BLMN",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-08-10",
      "entry_price": 10.95,
      "allocated_usd": 500,
      "shares": 45.6621,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 12.59,
      "stop_loss": 10.73,
      "max_hold_date": "2026-08-12",
      "daily_prices": {
        "2026-08-11": {
          "open": 10.87,
          "high": 11.27,
          "low": 10.82,
          "close": 11.12,
          "pnl_pct": 1.55
        },
        "2026-08-12": {
          "open": 11.24,
          "high": 11.43,
          "low": 10.94,
          "close": 11.39,
          "pnl_pct": 4.02
        }
      },
      "close_date": "2026-08-12",
      "close_price": 11.39,
      "final_pnl_pct": 4.02,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 9.11,
      "position_usd": 226.52
    },
    {
      "ticker": "PGEN",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-08-10",
      "entry_price": 7.23,
      "allocated_usd": 500,
      "shares": 69.1563,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 6.15,
      "stop_loss": 7.37,
      "max_hold_date": "2026-08-12",
      "daily_prices": {
        "2026-08-11": {
          "open": 7.1,
          "high": 7.1,
          "low": 6.75,
          "close": 6.86,
          "pnl_pct": 5.12
        },
        "2026-08-12": {
          "open": 6.88,
          "high": 6.95,
          "low": 6.65,
          "close": 6.85,
          "pnl_pct": 5.26
        }
      },
      "close_date": "2026-08-12",
      "close_price": 6.85,
      "final_pnl_pct": 5.26,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 11.92,
      "position_usd": 226.52
    },
    {
      "ticker": "BLMN",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-08-11",
      "entry_price": 11.02,
      "allocated_usd": 500,
      "shares": 45.3721,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 12.67,
      "stop_loss": 10.8,
      "max_hold_date": "2026-08-13",
      "daily_prices": {
        "2026-08-12": {
          "open": 11.24,
          "high": 11.43,
          "low": 10.94,
          "close": 11.39,
          "pnl_pct": 3.36
        },
        "2026-08-13": {
          "open": 11.41,
          "high": 11.64,
          "low": 10.76,
          "close": 10.79,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-08-13",
      "close_price": 10.8,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.55,
      "position_usd": 227.58
    },
    {
      "ticker": "ITIC",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-08-12",
      "entry_price": 283.36,
      "allocated_usd": 500,
      "shares": 1.7645,
      "actual_position_usd": 499.99,
      "entry_commission": 1.0,
      "take_profit": 325.86,
      "stop_loss": 277.69,
      "max_hold_date": "2026-08-14",
      "daily_prices": {
        "2026-08-13": {
          "open": 282.54,
          "high": 282.54,
          "low": 276.78,
          "close": 282.35,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-08-13",
      "close_price": 277.69,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.61,
      "position_usd": 230.5
    },
    {
      "ticker": "ESCA",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-08-12",
      "entry_price": 20.76,
      "allocated_usd": 500,
      "shares": 24.0848,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 23.87,
      "stop_loss": 20.34,
      "max_hold_date": "2026-08-14",
      "daily_prices": {
        "2026-08-13": {
          "open": 21.04,
          "high": 21.37,
          "low": 20.57,
          "close": 20.82,
          "pnl_pct": 0.29
        },
        "2026-08-14": {
          "open": 20.9,
          "high": 20.9,
          "low": 20.0,
          "close": 20.07,
          "pnl_pct": -2.02
        }
      },
      "close_date": "2026-08-14",
      "close_price": 20.34,
      "final_pnl_pct": -2.02,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.66,
      "position_usd": 230.5
    },
    {
      "ticker": "ULBI",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-08-12",
      "entry_price": 7.16,
      "allocated_usd": 500,
      "shares": 69.8324,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 8.23,
      "stop_loss": 7.02,
      "max_hold_date": "2026-08-14",
      "daily_prices": {
        "2026-08-13": {
          "open": 7.26,
          "high": 7.49,
          "low": 7.2,
          "close": 7.44,
          "pnl_pct": 3.91
        },
        "2026-08-14": {
          "open": 7.37,
          "high": 7.65,
          "low": 7.01,
          "close": 7.51,
          "pnl_pct": -1.96
        }
      },
      "close_date": "2026-08-14",
      "close_price": 7.02,
      "final_pnl_pct": -1.96,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.52,
      "position_usd": 230.5
    },
    {
      "ticker": "ULBI",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-08-13",
      "entry_price": 7.22,
      "allocated_usd": 500,
      "shares": 69.2521,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 8.3,
      "stop_loss": 7.08,
      "max_hold_date": "2026-08-17",
      "daily_prices": {
        "2026-08-14": {
          "open": 7.37,
          "high": 7.65,
          "low": 7.01,
          "close": 7.51,
          "pnl_pct": -1.94
        }
      },
      "close_date": "2026-08-14",
      "close_price": 7.08,
      "final_pnl_pct": -1.94,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.45,
      "position_usd": 229.58
    },
    {
      "ticker": "LQDT",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-08-13",
      "entry_price": 43.11,
      "allocated_usd": 500,
      "shares": 11.5982,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 49.58,
      "stop_loss": 42.25,
      "max_hold_date": "2026-08-17",
      "daily_prices": {
        "2026-08-14": {
          "open": 43.04,
          "high": 43.53,
          "low": 42.93,
          "close": 43.47,
          "pnl_pct": 0.84
        },
        "2026-08-17": {
          "open": 43.19,
          "high": 43.65,
          "low": 42.65,
          "close": 42.71,
          "pnl_pct": -0.93
        }
      },
      "close_date": "2026-08-17",
      "close_price": 42.71,
      "final_pnl_pct": -0.93,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -2.14,
      "position_usd": 229.58
    },
    {
      "ticker": "LQDT",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-08-14",
      "entry_price": 42.94,
      "allocated_usd": 500,
      "shares": 11.6442,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 49.38,
      "stop_loss": 42.08,
      "max_hold_date": "2026-08-18",
      "daily_prices": {
        "2026-08-17": {
          "open": 43.19,
          "high": 43.65,
          "low": 42.65,
          "close": 42.71,
          "pnl_pct": -0.54
        },
        "2026-08-18": {
          "open": 42.98,
          "high": 43.32,
          "low": 42.38,
          "close": 43.26,
          "pnl_pct": 0.75
        }
      },
      "close_date": "2026-08-18",
      "close_price": 43.26,
      "final_pnl_pct": 0.75,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 1.71,
      "position_usd": 228.22
    },
    {
      "ticker": "CHEF",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-08-17",
      "entry_price": 109.08,
      "allocated_usd": 500,
      "shares": 4.5838,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 125.44,
      "stop_loss": 106.9,
      "max_hold_date": "2026-08-19",
      "daily_prices": {
        "2026-08-18": {
          "open": 110.91,
          "high": 111.8,
          "low": 108.23,
          "close": 108.3,
          "pnl_pct": -0.72
        },
        "2026-08-19": {
          "open": 106.86,
          "high": 109.91,
          "low": 105.39,
          "close": 107.36,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-08-19",
      "close_price": 106.9,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.56,
      "position_usd": 228.0
    },
    {
      "ticker": "EAT",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-08-17",
      "entry_price": 237.15,
      "allocated_usd": 500,
      "shares": 2.1084,
      "actual_position_usd": 500.01,
      "entry_commission": 1.0,
      "take_profit": 272.72,
      "stop_loss": 232.41,
      "max_hold_date": "2026-08-19",
      "daily_prices": {
        "2026-08-18": {
          "open": 239.92,
          "high": 242.95,
          "low": 234.59,
          "close": 235.65,
          "pnl_pct": -0.63
        },
        "2026-08-19": {
          "open": 236.36,
          "high": 240.35,
          "low": 230.85,
          "close": 233.46,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-08-19",
      "close_price": 232.41,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.56,
      "position_usd": 228.0
    },
    {
      "ticker": "WEYS",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-08-17",
      "entry_price": 45.26,
      "allocated_usd": 500,
      "shares": 11.0473,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 52.05,
      "stop_loss": 44.35,
      "max_hold_date": "2026-08-19",
      "daily_prices": {
        "2026-08-18": {
          "open": 46.0,
          "high": 46.06,
          "low": 44.54,
          "close": 45.41,
          "pnl_pct": 0.33
        },
        "2026-08-19": {
          "open": 45.8,
          "high": 46.12,
          "low": 45.04,
          "close": 45.8,
          "pnl_pct": 1.19
        }
      },
      "close_date": "2026-08-19",
      "close_price": 45.8,
      "final_pnl_pct": 1.19,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 2.71,
      "position_usd": 228.0
    },
    {
      "ticker": "RRGB",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-08-19",
      "entry_price": 10.21,
      "allocated_usd": 500,
      "shares": 48.9716,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 8.68,
      "stop_loss": 10.41,
      "max_hold_date": "2026-08-21",
      "daily_prices": {
        "2026-08-20": {
          "open": 9.33,
          "high": 9.65,
          "low": 9.19,
          "close": 9.42,
          "pnl_pct": 7.74
        },
        "2026-08-21": {
          "open": 9.5,
          "high": 10.0,
          "low": 9.21,
          "close": 9.99,
          "pnl_pct": 2.15
        }
      },
      "close_date": "2026-08-21",
      "close_price": 9.99,
      "final_pnl_pct": 2.15,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 4.89,
      "position_usd": 227.53
    },
    {
      "ticker": "TCMD",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-08-19",
      "entry_price": 23.85,
      "allocated_usd": 500,
      "shares": 20.9644,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 20.27,
      "stop_loss": 24.33,
      "max_hold_date": "2026-08-21",
      "daily_prices": {
        "2026-08-20": {
          "open": 23.43,
          "high": 23.9,
          "low": 23.03,
          "close": 23.43,
          "pnl_pct": 1.76
        },
        "2026-08-21": {
          "open": 23.57,
          "high": 23.94,
          "low": 23.15,
          "close": 23.82,
          "pnl_pct": 0.13
        }
      },
      "close_date": "2026-08-21",
      "close_price": 23.82,
      "final_pnl_pct": 0.13,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 0.3,
      "position_usd": 227.53
    },
    {
      "ticker": "TISI",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-08-19",
      "entry_price": 23.32,
      "allocated_usd": 500,
      "shares": 21.4408,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 19.82,
      "stop_loss": 23.79,
      "max_hold_date": "2026-08-21",
      "daily_prices": {
        "2026-08-20": {
          "open": 22.5,
          "high": 23.14,
          "low": 22.5,
          "close": 22.8,
          "pnl_pct": 2.23
        },
        "2026-08-21": {
          "open": 22.72,
          "high": 23.15,
          "low": 22.45,
          "close": 22.72,
          "pnl_pct": 2.57
        }
      },
      "close_date": "2026-08-21",
      "close_price": 22.72,
      "final_pnl_pct": 2.57,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 5.85,
      "position_usd": 227.53
    },
    {
      "ticker": "ITIC",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-08-20",
      "entry_price": 292.39,
      "allocated_usd": 500,
      "shares": 1.71,
      "actual_position_usd": 499.99,
      "entry_commission": 1.0,
      "take_profit": 336.25,
      "stop_loss": 286.54,
      "max_hold_date": "2026-08-24",
      "daily_prices": {
        "2026-08-21": {
          "open": 289.61,
          "high": 293.52,
          "low": 280.5,
          "close": 288.81,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-08-21",
      "close_price": 286.54,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.55,
      "position_usd": 227.53
    },
    {
      "ticker": "SCSC",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-08-24",
      "entry_price": 54.35,
      "allocated_usd": 500,
      "shares": 9.1996,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 62.5,
      "stop_loss": 53.26,
      "max_hold_date": "2026-08-26",
      "daily_prices": {
        "2026-08-25": {
          "open": 54.61,
          "high": 56.21,
          "low": 53.76,
          "close": 56.19,
          "pnl_pct": 3.39
        },
        "2026-08-26": {
          "open": 56.09,
          "high": 56.6,
          "low": 55.0,
          "close": 56.17,
          "pnl_pct": 3.35
        }
      },
      "close_date": "2026-08-26",
      "close_price": 56.17,
      "final_pnl_pct": 3.35,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 7.64,
      "position_usd": 228.18
    },
    {
      "ticker": "VIRT",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-08-24",
      "entry_price": 67.93,
      "allocated_usd": 500,
      "shares": 7.3605,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 57.74,
      "stop_loss": 69.29,
      "max_hold_date": "2026-08-26",
      "daily_prices": {
        "2026-08-25": {
          "open": 65.74,
          "high": 66.44,
          "low": 63.57,
          "close": 64.96,
          "pnl_pct": 4.37
        },
        "2026-08-26": {
          "open": 64.68,
          "high": 65.95,
          "low": 64.51,
          "close": 65.5,
          "pnl_pct": 3.58
        }
      },
      "close_date": "2026-08-26",
      "close_price": 65.5,
      "final_pnl_pct": 3.58,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 8.17,
      "position_usd": 228.18
    },
    {
      "ticker": "UTMD",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-08-24",
      "entry_price": 71.55,
      "allocated_usd": 500,
      "shares": 6.9881,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 60.82,
      "stop_loss": 72.98,
      "max_hold_date": "2026-08-26",
      "daily_prices": {
        "2026-08-25": {
          "open": 71.6,
          "high": 71.6,
          "low": 70.06,
          "close": 70.66,
          "pnl_pct": 1.24
        },
        "2026-08-26": {
          "open": 70.65,
          "high": 70.83,
          "low": 69.53,
          "close": 70.59,
          "pnl_pct": 1.34
        }
      },
      "close_date": "2026-08-26",
      "close_price": 70.59,
      "final_pnl_pct": 1.34,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 3.06,
      "position_usd": 228.18
    },
    {
      "ticker": "OSIS",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-08-25",
      "entry_price": 204.05,
      "allocated_usd": 500,
      "shares": 2.4504,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 173.44,
      "stop_loss": 208.13,
      "max_hold_date": "2026-08-27",
      "daily_prices": {
        "2026-08-26": {
          "open": 203.92,
          "high": 211.43,
          "low": 203.67,
          "close": 211.04,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-08-26",
      "close_price": 208.13,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.56,
      "position_usd": 228.18
    },
    {
      "ticker": "VIRT",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-08-26",
      "entry_price": 65.2,
      "allocated_usd": 500,
      "shares": 7.6687,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 55.42,
      "stop_loss": 66.5,
      "max_hold_date": "2026-08-28",
      "daily_prices": {
        "2026-08-27": {
          "open": 65.18,
          "high": 66.81,
          "low": 65.16,
          "close": 66.79,
          "pnl_pct": -1.99
        }
      },
      "close_date": "2026-08-27",
      "close_price": 66.5,
      "final_pnl_pct": -1.99,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.57,
      "position_usd": 229.61
    },
    {
      "ticker": "SCSC",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-08-26",
      "entry_price": 56.19,
      "allocated_usd": 500,
      "shares": 8.8984,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 64.62,
      "stop_loss": 55.07,
      "max_hold_date": "2026-08-28",
      "daily_prices": {
        "2026-08-27": {
          "open": 56.13,
          "high": 58.17,
          "low": 56.07,
          "close": 58.1,
          "pnl_pct": 3.4
        },
        "2026-08-28": {
          "open": 58.15,
          "high": 59.31,
          "low": 56.32,
          "close": 56.55,
          "pnl_pct": 0.64
        }
      },
      "close_date": "2026-08-28",
      "close_price": 56.55,
      "final_pnl_pct": 0.64,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 1.47,
      "position_usd": 229.61
    },
    {
      "ticker": "SELF",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-08-26",
      "entry_price": 5.65,
      "allocated_usd": 500,
      "shares": 88.4956,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 4.8,
      "stop_loss": 5.76,
      "max_hold_date": "2026-08-28",
      "daily_prices": {
        "2026-08-27": {
          "open": 5.61,
          "high": 5.61,
          "low": 5.34,
          "close": 5.52,
          "pnl_pct": 2.3
        },
        "2026-08-28": {
          "open": 5.55,
          "high": 5.62,
          "low": 5.37,
          "close": 5.41,
          "pnl_pct": 4.25
        }
      },
      "close_date": "2026-08-28",
      "close_price": 5.41,
      "final_pnl_pct": 4.25,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 9.76,
      "position_usd": 229.61
    },
    {
      "ticker": "EZPW",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-08-27",
      "entry_price": 33.9,
      "allocated_usd": 500,
      "shares": 14.7493,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 38.98,
      "stop_loss": 33.22,
      "max_hold_date": "2026-08-31",
      "daily_prices": {
        "2026-08-28": {
          "open": 34.5,
          "high": 34.87,
          "low": 32.8,
          "close": 33.0,
          "pnl_pct": -2.01
        }
      },
      "close_date": "2026-08-28",
      "close_price": 33.22,
      "final_pnl_pct": -2.01,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.61,
      "position_usd": 229.16
    },
    {
      "ticker": "SELF",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-08-27",
      "entry_price": 5.61,
      "allocated_usd": 500,
      "shares": 89.1266,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 4.77,
      "stop_loss": 5.72,
      "max_hold_date": "2026-08-31",
      "daily_prices": {
        "2026-08-28": {
          "open": 5.55,
          "high": 5.62,
          "low": 5.37,
          "close": 5.41,
          "pnl_pct": 3.57
        },
        "2026-08-31": {
          "open": 5.4,
          "high": 5.52,
          "low": 5.17,
          "close": 5.17,
          "pnl_pct": 7.84
        }
      },
      "close_date": "2026-08-31",
      "close_price": 5.17,
      "final_pnl_pct": 7.84,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 17.97,
      "position_usd": 229.16
    },
    {
      "ticker": "URBN",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-08-28",
      "entry_price": 81.09,
      "allocated_usd": 500,
      "shares": 6.166,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 68.93,
      "stop_loss": 82.71,
      "max_hold_date": "2026-09-01",
      "daily_prices": {
        "2026-08-31": {
          "open": 80.44,
          "high": 81.33,
          "low": 79.11,
          "close": 80.69,
          "pnl_pct": 0.49
        },
        "2026-09-01": {
          "open": 79.12,
          "high": 80.5,
          "low": 76.87,
          "close": 79.29,
          "pnl_pct": 2.22
        }
      },
      "close_date": "2026-09-01",
      "close_price": 79.29,
      "final_pnl_pct": 2.22,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 5.1,
      "position_usd": 229.82
    },
    {
      "ticker": "ITIC",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-08-28",
      "entry_price": 299.34,
      "allocated_usd": 500,
      "shares": 1.6703,
      "actual_position_usd": 499.99,
      "entry_commission": 1.0,
      "take_profit": 254.44,
      "stop_loss": 305.33,
      "max_hold_date": "2026-09-01",
      "daily_prices": {
        "2026-08-31": {
          "open": 297.23,
          "high": 299.59,
          "low": 290.6,
          "close": 293.94,
          "pnl_pct": 1.8
        },
        "2026-09-01": {
          "open": 294.85,
          "high": 298.32,
          "low": 292.39,
          "close": 293.51,
          "pnl_pct": 1.95
        }
      },
      "close_date": "2026-09-01",
      "close_price": 293.51,
      "final_pnl_pct": 1.95,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 4.48,
      "position_usd": 229.82
    },
    {
      "ticker": "TISI",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-08-31",
      "entry_price": 24.74,
      "allocated_usd": 500,
      "shares": 20.2102,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 21.03,
      "stop_loss": 25.23,
      "max_hold_date": "2026-09-02",
      "daily_prices": {
        "2026-09-01": {
          "open": 24.75,
          "high": 25.25,
          "low": 24.28,
          "close": 24.75,
          "pnl_pct": -1.98
        }
      },
      "close_date": "2026-09-01",
      "close_price": 25.23,
      "final_pnl_pct": -1.98,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.59,
      "position_usd": 231.62
    },
    {
      "ticker": "MVBF",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-08-31",
      "entry_price": 30.43,
      "allocated_usd": 500,
      "shares": 16.4312,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 25.87,
      "stop_loss": 31.04,
      "max_hold_date": "2026-09-02",
      "daily_prices": {
        "2026-09-01": {
          "open": 30.06,
          "high": 30.32,
          "low": 29.81,
          "close": 30.25,
          "pnl_pct": 0.59
        },
        "2026-09-02": {
          "open": 30.4,
          "high": 31.26,
          "low": 30.22,
          "close": 30.85,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-09-02",
      "close_price": 31.04,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.63,
      "position_usd": 231.62
    },
    {
      "ticker": "TISI",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-09-01",
      "entry_price": 24.7,
      "allocated_usd": 500,
      "shares": 20.2429,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 20.99,
      "stop_loss": 25.19,
      "max_hold_date": "2026-09-03",
      "daily_prices": {
        "2026-09-02": {
          "open": 24.59,
          "high": 26.76,
          "low": 24.3,
          "close": 26.52,
          "pnl_pct": -1.98
        }
      },
      "close_date": "2026-09-02",
      "close_price": 25.19,
      "final_pnl_pct": -1.98,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.6,
      "position_usd": 232.12
    },
    {
      "ticker": "MVBF",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-09-01",
      "entry_price": 30.07,
      "allocated_usd": 500,
      "shares": 16.6279,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 34.58,
      "stop_loss": 29.47,
      "max_hold_date": "2026-09-03",
      "daily_prices": {
        "2026-09-02": {
          "open": 30.4,
          "high": 31.26,
          "low": 30.22,
          "close": 30.85,
          "pnl_pct": 2.59
        },
        "2026-09-03": {
          "open": 31.11,
          "high": 31.23,
          "low": 30.84,
          "close": 30.91,
          "pnl_pct": 2.79
        }
      },
      "close_date": "2026-09-03",
      "close_price": 30.91,
      "final_pnl_pct": 2.79,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 6.48,
      "position_usd": 232.12
    },
    {
      "ticker": "IPGP",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-09-01",
      "entry_price": 76.97,
      "allocated_usd": 500,
      "shares": 6.496,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 65.42,
      "stop_loss": 78.51,
      "max_hold_date": "2026-09-03",
      "daily_prices": {
        "2026-09-02": {
          "open": 75.21,
          "high": 77.03,
          "low": 73.95,
          "close": 76.48,
          "pnl_pct": 0.64
        },
        "2026-09-03": {
          "open": 76.48,
          "high": 77.86,
          "low": 75.18,
          "close": 76.46,
          "pnl_pct": 0.66
        }
      },
      "close_date": "2026-09-03",
      "close_price": 76.46,
      "final_pnl_pct": 0.66,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 1.53,
      "position_usd": 232.12
    },
    {
      "ticker": "URBN",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-09-02",
      "entry_price": 79.29,
      "allocated_usd": 500,
      "shares": 6.306,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 91.18,
      "stop_loss": 77.7,
      "max_hold_date": "2026-09-04",
      "daily_prices": {
        "2026-09-03": {
          "open": 79.93,
          "high": 81.37,
          "low": 78.41,
          "close": 80.58,
          "pnl_pct": 1.63
        },
        "2026-09-04": {
          "open": 79.55,
          "high": 81.37,
          "low": 79.51,
          "close": 80.97,
          "pnl_pct": 2.12
        }
      },
      "close_date": "2026-09-04",
      "close_price": 80.97,
      "final_pnl_pct": 2.12,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 4.9,
      "position_usd": 231.19
    },
    {
      "ticker": "XNCR",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-09-02",
      "entry_price": 27.91,
      "allocated_usd": 500,
      "shares": 17.9147,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 23.72,
      "stop_loss": 28.47,
      "max_hold_date": "2026-09-04",
      "daily_prices": {
        "2026-09-03": {
          "open": 27.18,
          "high": 27.23,
          "low": 26.06,
          "close": 26.62,
          "pnl_pct": 4.62
        },
        "2026-09-04": {
          "open": 26.05,
          "high": 26.76,
          "low": 25.4,
          "close": 26.61,
          "pnl_pct": 4.66
        }
      },
      "close_date": "2026-09-04",
      "close_price": 26.61,
      "final_pnl_pct": 4.66,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 10.77,
      "position_usd": 231.19
    },
    {
      "ticker": "SWKS",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-09-04",
      "entry_price": 73.48,
      "allocated_usd": 500,
      "shares": 6.8046,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 84.5,
      "stop_loss": 72.01,
      "max_hold_date": "2026-09-08",
      "daily_prices": {
        "2026-09-08": {
          "open": 75.0,
          "high": 75.85,
          "low": 73.5,
          "close": 75.38,
          "pnl_pct": 2.59
        }
      },
      "close_date": "2026-09-08",
      "close_price": 75.38,
      "final_pnl_pct": 2.59,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 6.05,
      "position_usd": 233.56
    },
    {
      "ticker": "AOUT",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-09-04",
      "entry_price": 14.09,
      "allocated_usd": 500,
      "shares": 35.4862,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 16.2,
      "stop_loss": 13.81,
      "max_hold_date": "2026-09-08",
      "daily_prices": {
        "2026-09-08": {
          "open": 14.65,
          "high": 16.09,
          "low": 13.85,
          "close": 14.77,
          "pnl_pct": 4.83
        }
      },
      "close_date": "2026-09-08",
      "close_price": 14.77,
      "final_pnl_pct": 4.83,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 11.28,
      "position_usd": 233.56
    },
    {
      "ticker": "MTRX",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-09-04",
      "entry_price": 10.31,
      "allocated_usd": 500,
      "shares": 48.4966,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 8.76,
      "stop_loss": 10.52,
      "max_hold_date": "2026-09-08",
      "daily_prices": {
        "2026-09-08": {
          "open": 10.6,
          "high": 10.9,
          "low": 10.6,
          "close": 10.81,
          "pnl_pct": -2.04
        }
      },
      "close_date": "2026-09-08",
      "close_price": 10.52,
      "final_pnl_pct": -2.04,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.76,
      "position_usd": 233.56
    },
    {
      "ticker": "DAKT",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-09-04",
      "entry_price": 19.15,
      "allocated_usd": 500,
      "shares": 26.1097,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 16.28,
      "stop_loss": 19.53,
      "max_hold_date": "2026-09-08",
      "daily_prices": {
        "2026-09-08": {
          "open": 19.34,
          "high": 19.95,
          "low": 19.34,
          "close": 19.67,
          "pnl_pct": -1.98
        }
      },
      "close_date": "2026-09-08",
      "close_price": 19.53,
      "final_pnl_pct": -1.98,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.62,
      "position_usd": 233.56
    },
    {
      "ticker": "SWBI",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-09-08",
      "entry_price": 13.08,
      "allocated_usd": 500,
      "shares": 38.2263,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 11.12,
      "stop_loss": 13.34,
      "max_hold_date": "2026-09-10",
      "daily_prices": {
        "2026-09-09": {
          "open": 12.99,
          "high": 13.4,
          "low": 12.91,
          "close": 13.27,
          "pnl_pct": -1.99
        }
      },
      "close_date": "2026-09-09",
      "close_price": 13.34,
      "final_pnl_pct": -1.99,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.66,
      "position_usd": 234.36
    },
    {
      "ticker": "ANDE",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-09-08",
      "entry_price": 71.23,
      "allocated_usd": 500,
      "shares": 7.0195,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 81.91,
      "stop_loss": 69.81,
      "max_hold_date": "2026-09-10",
      "daily_prices": {
        "2026-09-09": {
          "open": 71.26,
          "high": 72.0,
          "low": 69.82,
          "close": 71.32,
          "pnl_pct": 0.13
        },
        "2026-09-10": {
          "open": 71.48,
          "high": 72.69,
          "low": 70.98,
          "close": 71.88,
          "pnl_pct": 0.91
        }
      },
      "close_date": "2026-09-10",
      "close_price": 71.88,
      "final_pnl_pct": 0.91,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 2.13,
      "position_usd": 234.36
    },
    {
      "ticker": "ATRC",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-09-09",
      "entry_price": 53.73,
      "allocated_usd": 500,
      "shares": 9.3058,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 45.67,
      "stop_loss": 54.8,
      "max_hold_date": "2026-09-11",
      "daily_prices": {
        "2026-09-10": {
          "open": 52.31,
          "high": 53.66,
          "low": 51.86,
          "close": 52.96,
          "pnl_pct": 1.43
        },
        "2026-09-11": {
          "open": 53.53,
          "high": 55.16,
          "low": 53.52,
          "close": 54.54,
          "pnl_pct": -1.99
        }
      },
      "close_date": "2026-09-11",
      "close_price": 54.8,
      "final_pnl_pct": -1.99,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.65,
      "position_usd": 233.89
    },
    {
      "ticker": "SWBI",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-09-09",
      "entry_price": 13.23,
      "allocated_usd": 500,
      "shares": 37.7929,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 15.21,
      "stop_loss": 12.97,
      "max_hold_date": "2026-09-11",
      "daily_prices": {
        "2026-09-10": {
          "open": 13.18,
          "high": 13.21,
          "low": 12.98,
          "close": 13.16,
          "pnl_pct": -0.53
        },
        "2026-09-11": {
          "open": 13.27,
          "high": 13.33,
          "low": 12.91,
          "close": 13.02,
          "pnl_pct": -1.97
        }
      },
      "close_date": "2026-09-11",
      "close_price": 12.97,
      "final_pnl_pct": -1.97,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.61,
      "position_usd": 233.89
    },
    {
      "ticker": "TISI",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-09-09",
      "entry_price": 27.0,
      "allocated_usd": 500,
      "shares": 18.5185,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 22.95,
      "stop_loss": 27.54,
      "max_hold_date": "2026-09-11",
      "daily_prices": {
        "2026-09-10": {
          "open": 26.67,
          "high": 26.85,
          "low": 26.31,
          "close": 26.52,
          "pnl_pct": 1.78
        },
        "2026-09-11": {
          "open": 27.54,
          "high": 27.54,
          "low": 25.74,
          "close": 25.86,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-09-11",
      "close_price": 27.54,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.68,
      "position_usd": 233.89
    },
    {
      "ticker": "ATRC",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-09-10",
      "entry_price": 53.03,
      "allocated_usd": 500,
      "shares": 9.4286,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 45.08,
      "stop_loss": 54.09,
      "max_hold_date": "2026-09-14",
      "daily_prices": {
        "2026-09-11": {
          "open": 53.53,
          "high": 55.16,
          "low": 53.52,
          "close": 54.54,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-09-11",
      "close_price": 54.09,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.68,
      "position_usd": 234.1
    },
    {
      "ticker": "TBBK",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-09-11",
      "entry_price": 50.87,
      "allocated_usd": 500,
      "shares": 9.829,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 58.5,
      "stop_loss": 49.85,
      "max_hold_date": "2026-09-15",
      "daily_prices": {
        "2026-09-14": {
          "open": 50.45,
          "high": 51.0,
          "low": 49.6,
          "close": 50.23,
          "pnl_pct": -2.01
        }
      },
      "close_date": "2026-09-14",
      "close_price": 49.85,
      "final_pnl_pct": -2.01,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.67,
      "position_usd": 232.24
    },
    {
      "ticker": "SWBI",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-09-11",
      "entry_price": 13.13,
      "allocated_usd": 500,
      "shares": 38.0807,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 11.16,
      "stop_loss": 13.39,
      "max_hold_date": "2026-09-15",
      "daily_prices": {
        "2026-09-14": {
          "open": 13.04,
          "high": 13.09,
          "low": 12.8,
          "close": 13.07,
          "pnl_pct": 0.46
        },
        "2026-09-15": {
          "open": 13.07,
          "high": 13.07,
          "low": 12.81,
          "close": 12.97,
          "pnl_pct": 1.22
        }
      },
      "close_date": "2026-09-15",
      "close_price": 12.97,
      "final_pnl_pct": 1.22,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 2.83,
      "position_usd": 232.24
    },
    {
      "ticker": "AOUT",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-09-11",
      "entry_price": 15.55,
      "allocated_usd": 500,
      "shares": 32.1543,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 13.22,
      "stop_loss": 15.86,
      "max_hold_date": "2026-09-15",
      "daily_prices": {
        "2026-09-14": {
          "open": 15.67,
          "high": 15.68,
          "low": 15.14,
          "close": 15.23,
          "pnl_pct": 2.06
        },
        "2026-09-15": {
          "open": 15.36,
          "high": 15.41,
          "low": 14.92,
          "close": 15.31,
          "pnl_pct": 1.54
        }
      },
      "close_date": "2026-09-15",
      "close_price": 15.31,
      "final_pnl_pct": 1.54,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 3.58,
      "position_usd": 232.24
    },
    {
      "ticker": "TISI",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-09-11",
      "entry_price": 26.82,
      "allocated_usd": 500,
      "shares": 18.6428,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 22.8,
      "stop_loss": 27.36,
      "max_hold_date": "2026-09-15",
      "daily_prices": {
        "2026-09-14": {
          "open": 25.61,
          "high": 26.9,
          "low": 25.61,
          "close": 26.9,
          "pnl_pct": -0.3
        },
        "2026-09-15": {
          "open": 26.81,
          "high": 27.42,
          "low": 26.17,
          "close": 26.99,
          "pnl_pct": -2.01
        }
      },
      "close_date": "2026-09-15",
      "close_price": 27.36,
      "final_pnl_pct": -2.01,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.67,
      "position_usd": 232.24
    },
    {
      "ticker": "SWKS",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-09-14",
      "entry_price": 88.35,
      "allocated_usd": 500,
      "shares": 5.6593,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 75.1,
      "stop_loss": 90.12,
      "max_hold_date": "2026-09-16",
      "daily_prices": {
        "2026-09-15": {
          "open": 80.54,
          "high": 90.31,
          "low": 79.43,
          "close": 90.0,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-09-15",
      "close_price": 90.12,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.64,
      "position_usd": 231.77
    },
    {
      "ticker": "ATRC",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-09-15",
      "entry_price": 55.79,
      "allocated_usd": 500,
      "shares": 8.9622,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 47.42,
      "stop_loss": 56.91,
      "max_hold_date": "2026-09-17",
      "daily_prices": {
        "2026-09-16": {
          "open": 55.66,
          "high": 57.25,
          "low": 55.66,
          "close": 57.14,
          "pnl_pct": -2.01
        }
      },
      "close_date": "2026-09-16",
      "close_price": 56.91,
      "final_pnl_pct": -2.01,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.65,
      "position_usd": 231.48
    },
    {
      "ticker": "TBBK",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-09-15",
      "entry_price": 50.23,
      "allocated_usd": 500,
      "shares": 9.9542,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 42.7,
      "stop_loss": 51.23,
      "max_hold_date": "2026-09-17",
      "daily_prices": {
        "2026-09-16": {
          "open": 50.37,
          "high": 51.0,
          "low": 49.8,
          "close": 50.73,
          "pnl_pct": -1.0
        },
        "2026-09-17": {
          "open": 51.0,
          "high": 51.25,
          "low": 49.89,
          "close": 50.65,
          "pnl_pct": -1.99
        }
      },
      "close_date": "2026-09-17",
      "close_price": 51.23,
      "final_pnl_pct": -1.99,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.61,
      "position_usd": 231.48
    },
    {
      "ticker": "FEIM",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-09-15",
      "entry_price": 85.5,
      "allocated_usd": 500,
      "shares": 5.848,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 72.67,
      "stop_loss": 87.21,
      "max_hold_date": "2026-09-17",
      "daily_prices": {
        "2026-09-16": {
          "open": 85.83,
          "high": 86.6,
          "low": 82.51,
          "close": 84.6,
          "pnl_pct": 1.05
        },
        "2026-09-17": {
          "open": 85.81,
          "high": 87.0,
          "low": 83.0,
          "close": 83.82,
          "pnl_pct": 1.96
        }
      },
      "close_date": "2026-09-17",
      "close_price": 83.82,
      "final_pnl_pct": 1.96,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 4.54,
      "position_usd": 231.48
    },
    {
      "ticker": "FEIM",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-09-16",
      "entry_price": 85.05,
      "allocated_usd": 500,
      "shares": 5.8789,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 72.29,
      "stop_loss": 86.75,
      "max_hold_date": "2026-09-18",
      "daily_prices": {
        "2026-09-17": {
          "open": 85.81,
          "high": 87.0,
          "low": 83.0,
          "close": 83.82,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-09-17",
      "close_price": 86.75,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.62,
      "position_usd": 231.02
    },
    {
      "ticker": "SWKS",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-09-16",
      "entry_price": 90.0,
      "allocated_usd": 500,
      "shares": 5.5556,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 76.5,
      "stop_loss": 91.8,
      "max_hold_date": "2026-09-18",
      "daily_prices": {
        "2026-09-17": {
          "open": 86.76,
          "high": 91.46,
          "low": 84.44,
          "close": 91.32,
          "pnl_pct": -1.47
        },
        "2026-09-18": {
          "open": 92.05,
          "high": 92.05,
          "low": 87.48,
          "close": 88.76,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-09-18",
      "close_price": 91.8,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.62,
      "position_usd": 231.02
    },
    {
      "ticker": "FEIM",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-09-17",
      "entry_price": 84.6,
      "allocated_usd": 500,
      "shares": 5.9102,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 97.29,
      "stop_loss": 82.91,
      "max_hold_date": "2026-09-21",
      "daily_prices": {
        "2026-09-18": {
          "open": 83.82,
          "high": 86.15,
          "low": 83.08,
          "close": 85.53,
          "pnl_pct": 1.1
        },
        "2026-09-21": {
          "open": 85.68,
          "high": 89.6,
          "low": 85.54,
          "close": 89.0,
          "pnl_pct": 5.2
        }
      },
      "close_date": "2026-09-21",
      "close_price": 89.0,
      "final_pnl_pct": 5.2,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 11.99,
      "position_usd": 230.55
    },
    {
      "ticker": "QRVO",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-09-17",
      "entry_price": 113.97,
      "allocated_usd": 500,
      "shares": 4.3871,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 131.07,
      "stop_loss": 111.69,
      "max_hold_date": "2026-09-21",
      "daily_prices": {
        "2026-09-18": {
          "open": 120.76,
          "high": 120.76,
          "low": 115.88,
          "close": 117.18,
          "pnl_pct": 2.82
        },
        "2026-09-21": {
          "open": 118.44,
          "high": 119.89,
          "low": 116.66,
          "close": 117.21,
          "pnl_pct": 2.84
        }
      },
      "close_date": "2026-09-21",
      "close_price": 117.21,
      "final_pnl_pct": 2.84,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 6.55,
      "position_usd": 230.55
    },
    {
      "ticker": "ATRC",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-09-18",
      "entry_price": 58.79,
      "allocated_usd": 500,
      "shares": 8.5048,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 49.97,
      "stop_loss": 59.97,
      "max_hold_date": "2026-09-22",
      "daily_prices": {
        "2026-09-21": {
          "open": 58.23,
          "high": 59.11,
          "low": 56.97,
          "close": 58.32,
          "pnl_pct": 0.8
        },
        "2026-09-22": {
          "open": 58.62,
          "high": 59.69,
          "low": 57.94,
          "close": 58.83,
          "pnl_pct": -0.07
        }
      },
      "close_date": "2026-09-22",
      "close_price": 58.83,
      "final_pnl_pct": -0.07,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -0.16,
      "position_usd": 230.09
    },
    {
      "ticker": "STNG",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-09-18",
      "entry_price": 88.47,
      "allocated_usd": 500,
      "shares": 5.6516,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 75.2,
      "stop_loss": 90.24,
      "max_hold_date": "2026-09-22",
      "daily_prices": {
        "2026-09-21": {
          "open": 85.7,
          "high": 89.82,
          "low": 84.73,
          "close": 86.21,
          "pnl_pct": 2.55
        },
        "2026-09-22": {
          "open": 83.0,
          "high": 85.02,
          "low": 82.0,
          "close": 82.33,
          "pnl_pct": 6.94
        }
      },
      "close_date": "2026-09-22",
      "close_price": 82.33,
      "final_pnl_pct": 6.94,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 15.97,
      "position_usd": 230.09
    },
    {
      "ticker": "HRMY",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-09-21",
      "entry_price": 42.02,
      "allocated_usd": 500,
      "shares": 11.8991,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 48.32,
      "stop_loss": 41.18,
      "max_hold_date": "2026-09-23",
      "daily_prices": {
        "2026-09-22": {
          "open": 42.1,
          "high": 42.37,
          "low": 41.36,
          "close": 41.53,
          "pnl_pct": -1.17
        },
        "2026-09-23": {
          "open": 41.61,
          "high": 42.08,
          "low": 39.72,
          "close": 40.48,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-09-23",
      "close_price": 41.18,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.64,
      "position_usd": 231.94
    },
    {
      "ticker": "QRVO",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-09-21",
      "entry_price": 117.18,
      "allocated_usd": 500,
      "shares": 4.2669,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 134.76,
      "stop_loss": 114.84,
      "max_hold_date": "2026-09-23",
      "daily_prices": {
        "2026-09-22": {
          "open": 116.61,
          "high": 119.18,
          "low": 116.61,
          "close": 118.44,
          "pnl_pct": 1.08
        },
        "2026-09-23": {
          "open": 118.44,
          "high": 121.09,
          "low": 117.84,
          "close": 119.59,
          "pnl_pct": 2.06
        }
      },
      "close_date": "2026-09-23",
      "close_price": 119.59,
      "final_pnl_pct": 2.06,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 4.78,
      "position_usd": 231.94
    },
    {
      "ticker": "NSIT",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-09-22",
      "entry_price": 156.7,
      "allocated_usd": 500,
      "shares": 3.1908,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 180.2,
      "stop_loss": 153.57,
      "max_hold_date": "2026-09-24",
      "daily_prices": {
        "2026-09-23": {
          "open": 157.02,
          "high": 162.22,
          "low": 156.63,
          "close": 158.25,
          "pnl_pct": 0.99
        },
        "2026-09-24": {
          "open": 157.09,
          "high": 161.57,
          "low": 154.46,
          "close": 159.73,
          "pnl_pct": 1.93
        }
      },
      "close_date": "2026-09-24",
      "close_price": 159.73,
      "final_pnl_pct": 1.93,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 4.51,
      "position_usd": 233.52
    },
    {
      "ticker": "TISI",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-09-22",
      "entry_price": 28.01,
      "allocated_usd": 500,
      "shares": 17.8508,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 32.21,
      "stop_loss": 27.45,
      "max_hold_date": "2026-09-24",
      "daily_prices": {
        "2026-09-23": {
          "open": 28.65,
          "high": 29.0,
          "low": 28.62,
          "close": 28.9,
          "pnl_pct": 3.18
        },
        "2026-09-24": {
          "open": 28.84,
          "high": 29.57,
          "low": 28.84,
          "close": 28.97,
          "pnl_pct": 3.43
        }
      },
      "close_date": "2026-09-24",
      "close_price": 28.97,
      "final_pnl_pct": 3.43,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 8.01,
      "position_usd": 233.52
    }
  ],
  "_note": "H-DS 模拟盘：DeepSeek(V4-pro) 信号 + H 出场规则(TP15/SL2/2日/gap1.0)。与 Plan H(Haiku信号+同规则)头对头比模型。仅A/B对比,不是真实交易方案。",
  "stats": {
    "total_trades": 150,
    "win_trades": 78,
    "win_rate": 52.0,
    "total_realized_pnl_usd": 347.87,
    "open_unrealized_pnl_usd": 16.96,
    "portfolio_value": 2364.83,
    "total_commission_usd": 300.0,
    "skipped_gap": 91,
    "skipped_zero_shares": 0,
    "skipped_no_cash": 38,
    "updated_at": "2026-09-25"
  }
};
