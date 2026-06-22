// Plan H-DS 模拟盘持仓 — 历史最优参数(TP15/SL2/2日) 回溯 + 实时更新
window.PORTFOLIO_HDS = {
  "capital_usd": 2000,
  "open_positions": [
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
          "open": 22.72,
          "high": 23.05,
          "low": 22.08,
          "close": 23.01,
          "pnl_pct": 3.05
        }
      },
      "position_usd": 204.69,
      "unrealized_pnl_usd": 6.24
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
          "open": 15.23,
          "high": 16.18,
          "low": 15.12,
          "close": 15.8,
          "pnl_pct": 3.88
        }
      },
      "position_usd": 204.69,
      "unrealized_pnl_usd": 7.94
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
      "daily_prices": {},
      "position_usd": 206.03,
      "unrealized_pnl_usd": 0.0
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
      "daily_prices": {},
      "position_usd": 206.03,
      "unrealized_pnl_usd": 0.0
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
      "daily_prices": {},
      "position_usd": 206.03,
      "unrealized_pnl_usd": 0.0
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
      "daily_prices": {},
      "position_usd": 206.03,
      "unrealized_pnl_usd": 0.0
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
          "open": 1079.01,
          "high": 1089.29,
          "low": 1038.5,
          "close": 1079.57,
          "pnl_pct": 9.98
        },
        "2026-06-04": {
          "open": 1007.1,
          "high": 1036.37,
          "low": 971.68,
          "close": 996.0,
          "pnl_pct": 1.47
        }
      },
      "close_date": "2026-06-04",
      "close_price": 996.0,
      "final_pnl_pct": 1.47,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 2.94,
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
          "open": 103.72,
          "high": 104.57,
          "low": 97.16,
          "close": 97.99,
          "pnl_pct": 13.38
        },
        "2026-06-08": {
          "open": 102.8,
          "high": 103.72,
          "low": 99.83,
          "close": 102.32,
          "pnl_pct": 9.56
        }
      },
      "close_date": "2026-06-08",
      "close_price": 102.32,
      "final_pnl_pct": 9.56,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 19.15,
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
          "open": 28.19,
          "high": 28.74,
          "low": 27.76,
          "close": 28.59,
          "pnl_pct": 0.49
        },
        "2026-06-10": {
          "open": 28.98,
          "high": 29.4,
          "low": 28.49,
          "close": 28.89,
          "pnl_pct": -1.98
        }
      },
      "close_date": "2026-06-10",
      "close_price": 29.3,
      "final_pnl_pct": -1.98,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.0,
      "position_usd": 202.21
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
          "open": 28.98,
          "high": 29.4,
          "low": 28.49,
          "close": 28.89,
          "pnl_pct": -1.98
        }
      },
      "close_date": "2026-06-10",
      "close_price": 29.3,
      "final_pnl_pct": -1.98,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.02,
      "position_usd": 202.93
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
      "daily_prices": {
        "2026-06-10": {
          "open": 11.78,
          "high": 12.3,
          "low": 10.85,
          "close": 11.5,
          "pnl_pct": 14.98
        }
      },
      "close_date": "2026-06-10",
      "close_price": 11.9,
      "final_pnl_pct": 14.98,
      "close_reason": "take_profit",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 30.4,
      "position_usd": 202.93
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
          "open": 174.61,
          "high": 176.69,
          "low": 171.75,
          "close": 173.04,
          "pnl_pct": 0.0
        },
        "2026-06-15": {
          "open": 172.51,
          "high": 172.79,
          "low": 162.32,
          "close": 164.1,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-06-15",
      "close_price": 169.58,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.1,
      "position_usd": 205.17
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
      "daily_prices": {
        "2026-06-12": {
          "open": 123.36,
          "high": 123.45,
          "low": 123.16,
          "close": 123.25,
          "pnl_pct": -0.0
        },
        "2026-06-15": {
          "open": 123.3,
          "high": 123.47,
          "low": 123.24,
          "close": 123.35,
          "pnl_pct": -0.08
        }
      },
      "close_date": "2026-06-15",
      "close_price": 123.35,
      "final_pnl_pct": -0.08,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -0.16,
      "position_usd": 205.17
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
          "open": 28.85,
          "high": 29.07,
          "low": 28.59,
          "close": 28.73,
          "pnl_pct": -0.0
        },
        "2026-06-15": {
          "open": 29.04,
          "high": 29.04,
          "low": 28.48,
          "close": 28.69,
          "pnl_pct": 0.14
        }
      },
      "close_date": "2026-06-15",
      "close_price": 28.69,
      "final_pnl_pct": 0.14,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 0.29,
      "position_usd": 205.17
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
          "open": 37.0,
          "high": 37.25,
          "low": 36.12,
          "close": 36.28,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-06-15",
      "close_price": 36.26,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.1,
      "position_usd": 205.17
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
          "open": 16.08,
          "high": 16.88,
          "low": 15.22,
          "close": 15.22,
          "pnl_pct": -1.49
        },
        "2026-06-16": {
          "open": 14.95,
          "high": 16.1,
          "low": 14.95,
          "close": 15.65,
          "pnl_pct": -2.01
        }
      },
      "close_date": "2026-06-16",
      "close_price": 15.14,
      "final_pnl_pct": -2.01,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.12,
      "position_usd": 205.17
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
          "open": 172.51,
          "high": 172.79,
          "low": 162.32,
          "close": 164.1,
          "pnl_pct": 5.17
        },
        "2026-06-16": {
          "open": 165.18,
          "high": 166.94,
          "low": 159.22,
          "close": 159.8,
          "pnl_pct": 7.65
        }
      },
      "close_date": "2026-06-16",
      "close_price": 159.8,
      "final_pnl_pct": 7.65,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 15.7,
      "position_usd": 205.17
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
          "open": 9.9,
          "high": 10.09,
          "low": 9.82,
          "close": 9.87,
          "pnl_pct": -2.04
        }
      },
      "close_date": "2026-06-16",
      "close_price": 10.01,
      "final_pnl_pct": -2.04,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.17,
      "position_usd": 204.36
    },
    {
      "ticker": "WSBC",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-06-16",
      "entry_price": 36.08,
      "allocated_usd": 500,
      "shares": 13.8581,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 41.49,
      "stop_loss": 35.36,
      "max_hold_date": "2026-06-18",
      "daily_prices": {
        "2026-06-17": {
          "open": 35.95,
          "high": 37.06,
          "low": 35.11,
          "close": 35.39,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-06-17",
      "close_price": 35.36,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.1,
      "position_usd": 205.1
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
      "realized_pnl_usd": -4.09,
      "position_usd": 204.69
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
          "open": 16.52,
          "high": 17.6,
          "low": 16.25,
          "close": 16.85,
          "pnl_pct": 7.94
        }
      },
      "close_date": "2026-06-22",
      "close_price": 16.85,
      "final_pnl_pct": 7.94,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 16.22,
      "position_usd": 204.28
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
          "open": 16.08,
          "high": 16.44,
          "low": 14.52,
          "close": 16.38,
          "pnl_pct": -1.42
        }
      },
      "close_date": "2026-06-22",
      "close_price": 16.38,
      "final_pnl_pct": -1.42,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -2.9,
      "position_usd": 204.28
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
      "daily_prices": {
        "2026-06-22": {
          "open": 123.5,
          "high": 123.55,
          "low": 123.39,
          "close": 123.4,
          "pnl_pct": 0.02
        }
      },
      "close_date": "2026-06-22",
      "close_price": 123.4,
      "final_pnl_pct": 0.02,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 0.04,
      "position_usd": 204.28
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
          "open": 36.1,
          "high": 36.85,
          "low": 36.1,
          "close": 36.64,
          "pnl_pct": 2.0
        }
      },
      "close_date": "2026-06-22",
      "close_price": 36.64,
      "final_pnl_pct": 2.0,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 4.09,
      "position_usd": 204.28
    }
  ],
  "_note": "H-DS 模拟盘：DeepSeek(V4-pro) 信号 + H 出场规则(TP15/SL2/2日/gap1.0)。与 Plan H(Haiku信号+同规则)头对头比模型。仅A/B对比,不是真实交易方案。",
  "stats": {
    "total_trades": 20,
    "win_trades": 10,
    "win_rate": 50.0,
    "total_realized_pnl_usd": 60.29,
    "open_unrealized_pnl_usd": 14.19,
    "portfolio_value": 2074.48,
    "total_commission_usd": 40.0,
    "skipped_gap": 10,
    "skipped_zero_shares": 0,
    "skipped_no_cash": 0,
    "updated_at": "2026-06-22"
  }
};
