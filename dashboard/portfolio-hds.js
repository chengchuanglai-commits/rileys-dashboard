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
      "position_usd": 202.2,
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
      "position_usd": 205.96,
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
      "position_usd": 209.05,
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
          "open": 22.72,
          "high": 23.05,
          "low": 22.08,
          "close": 23.01,
          "pnl_pct": 3.05
        }
      },
      "position_usd": 211.69,
      "unrealized_pnl_usd": 6.46
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
      "position_usd": 211.69,
      "unrealized_pnl_usd": 8.21
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
      "position_usd": 211.26,
      "unrealized_pnl_usd": 0.0
    },
    {
      "ticker": "SPXC",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-07-01",
      "entry_price": 245.17,
      "allocated_usd": 500,
      "shares": 2.0394,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 208.39,
      "stop_loss": 250.07,
      "max_hold_date": "2026-07-03",
      "daily_prices": {
        "2026-07-02": {
          "open": 233.25,
          "high": 235.45,
          "low": 221.86,
          "close": 227.74,
          "pnl_pct": 7.11
        }
      },
      "position_usd": 221.56,
      "unrealized_pnl_usd": 15.75
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
        }
      },
      "position_usd": 223.5,
      "unrealized_pnl_usd": 2.7
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
          "high": 29.42,
          "low": 28.91,
          "close": 29.21,
          "pnl_pct": -0.44
        }
      },
      "position_usd": 223.5,
      "unrealized_pnl_usd": -0.98
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
      "daily_prices": {},
      "position_usd": 223.06,
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
      "realized_pnl_usd": 30.33,
      "position_usd": 202.2
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
      "realized_pnl_usd": 30.89,
      "position_usd": 205.96
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
      "position_usd": 209.05
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
      "realized_pnl_usd": -4.18,
      "position_usd": 209.05
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
      "realized_pnl_usd": -4.24,
      "position_usd": 212.19
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
      "realized_pnl_usd": -4.26,
      "position_usd": 212.19
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
      "realized_pnl_usd": 16.23,
      "position_usd": 212.19
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
      "realized_pnl_usd": -4.3,
      "position_usd": 210.92
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
      "realized_pnl_usd": -4.24,
      "position_usd": 212.11
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
      "realized_pnl_usd": -4.23,
      "position_usd": 211.69
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
          "high": 17.65,
          "low": 16.25,
          "close": 17.0,
          "pnl_pct": 8.9
        }
      },
      "close_date": "2026-06-22",
      "close_price": 17.0,
      "final_pnl_pct": 8.9,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 18.8,
      "position_usd": 211.26
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
          "open": 15.95,
          "high": 16.44,
          "low": 14.39,
          "close": 16.31,
          "pnl_pct": -0.99
        }
      },
      "close_date": "2026-06-22",
      "close_price": 16.31,
      "final_pnl_pct": -0.99,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -2.09,
      "position_usd": 211.26
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
          "close": 36.7,
          "pnl_pct": 2.17
        }
      },
      "close_date": "2026-06-22",
      "close_price": 36.7,
      "final_pnl_pct": 2.17,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 4.58,
      "position_usd": 211.26
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
          "open": 16.03,
          "high": 17.35,
          "low": 15.88,
          "close": 16.53,
          "pnl_pct": -1.99
        }
      },
      "close_date": "2026-06-23",
      "close_price": 16.4,
      "final_pnl_pct": -1.99,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.25,
      "position_usd": 213.39
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
          "open": 16.99,
          "high": 17.61,
          "low": 16.65,
          "close": 17.25,
          "pnl_pct": 9.18
        },
        "2026-06-24": {
          "open": 17.36,
          "high": 17.61,
          "low": 16.82,
          "close": 17.05,
          "pnl_pct": 7.91
        }
      },
      "close_date": "2026-06-24",
      "close_price": 17.05,
      "final_pnl_pct": 7.91,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 16.88,
      "position_usd": 213.39
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
      "realized_pnl_usd": -3.41,
      "position_usd": 213.39
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
          "open": 22.93,
          "high": 23.29,
          "low": 22.8,
          "close": 23.15,
          "pnl_pct": 0.61
        },
        "2026-06-24": {
          "open": 23.25,
          "high": 24.05,
          "low": 22.85,
          "close": 23.81,
          "pnl_pct": 3.48
        }
      },
      "close_date": "2026-06-24",
      "close_price": 23.81,
      "final_pnl_pct": 3.48,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 7.43,
      "position_usd": 213.39
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
      "realized_pnl_usd": 31.95,
      "position_usd": 212.97
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
          "open": 36.55,
          "high": 37.19,
          "low": 36.55,
          "close": 36.89,
          "pnl_pct": 1.07
        },
        "2026-06-26": {
          "open": 37.02,
          "high": 37.71,
          "low": 36.5,
          "close": 36.95,
          "pnl_pct": 1.23
        }
      },
      "close_date": "2026-06-26",
      "close_price": 36.95,
      "final_pnl_pct": 1.23,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 2.68,
      "position_usd": 218.25
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
          "open": 38.67,
          "high": 39.19,
          "low": 38.4,
          "close": 38.7,
          "pnl_pct": 0.78
        },
        "2026-06-26": {
          "open": 38.7,
          "high": 39.27,
          "low": 38.04,
          "close": 38.93,
          "pnl_pct": 1.38
        }
      },
      "close_date": "2026-06-26",
      "close_price": 38.93,
      "final_pnl_pct": 1.38,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 3.01,
      "position_usd": 218.25
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
      "realized_pnl_usd": 20.56,
      "position_usd": 218.25
    },
    {
      "ticker": "HOFT",
      "name": "",
      "action": "SELL",
      "signal_date": "2026-06-25",
      "entry_price": 17.05,
      "allocated_usd": 500,
      "shares": 29.3255,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 14.49,
      "stop_loss": 17.39,
      "max_hold_date": "2026-06-29",
      "daily_prices": {
        "2026-06-26": {
          "open": 16.97,
          "high": 17.41,
          "low": 16.8,
          "close": 17.1,
          "pnl_pct": -1.99
        }
      },
      "close_date": "2026-06-26",
      "close_price": 17.39,
      "final_pnl_pct": -1.99,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.34,
      "position_usd": 218.25
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
          "open": 44.79,
          "high": 44.8,
          "low": 44.05,
          "close": 44.63,
          "pnl_pct": 0.56
        },
        "2026-06-30": {
          "open": 44.47,
          "high": 44.81,
          "low": 44.0,
          "close": 44.81,
          "pnl_pct": 0.16
        }
      },
      "close_date": "2026-06-30",
      "close_price": 44.81,
      "final_pnl_pct": 0.16,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 0.35,
      "position_usd": 220.44
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
          "open": 24.71,
          "high": 24.91,
          "low": 23.62,
          "close": 24.46,
          "pnl_pct": 5.43
        },
        "2026-06-30": {
          "open": 24.5,
          "high": 25.67,
          "low": 24.12,
          "close": 25.27,
          "pnl_pct": 8.92
        }
      },
      "close_date": "2026-06-30",
      "close_price": 25.27,
      "final_pnl_pct": 8.92,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 19.66,
      "position_usd": 220.44
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
      "realized_pnl_usd": -4.41,
      "position_usd": 220.44
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
          "open": 25.44,
          "high": 25.73,
          "low": 23.89,
          "close": 25.59,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-07-01",
      "close_price": 23.97,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.44,
      "position_usd": 222.01
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
      "realized_pnl_usd": 0.33,
      "position_usd": 222.01
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
      "realized_pnl_usd": -4.42,
      "position_usd": 222.01
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
      "realized_pnl_usd": -3.89,
      "position_usd": 222.01
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
      "realized_pnl_usd": -4.42,
      "position_usd": 220.76
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
      "realized_pnl_usd": 2.56,
      "position_usd": 220.76
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
          "open": 29.28,
          "high": 29.77,
          "low": 28.7,
          "close": 28.91,
          "pnl_pct": 3.12
        }
      },
      "close_date": "2026-07-06",
      "close_price": 28.91,
      "final_pnl_pct": 3.12,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 6.89,
      "position_usd": 220.76
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
          "open": 71.53,
          "high": 71.53,
          "low": 69.14,
          "close": 69.33,
          "pnl_pct": 4.74
        },
        "2026-07-08": {
          "open": 68.21,
          "high": 69.49,
          "low": 67.25,
          "close": 68.06,
          "pnl_pct": 6.49
        }
      },
      "close_date": "2026-07-08",
      "close_price": 68.06,
      "final_pnl_pct": 6.49,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 14.36,
      "position_usd": 221.27
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
          "open": 37.68,
          "high": 37.99,
          "low": 36.32,
          "close": 36.49,
          "pnl_pct": 3.08
        },
        "2026-07-08": {
          "open": 36.37,
          "high": 36.68,
          "low": 35.6,
          "close": 36.2,
          "pnl_pct": 3.85
        }
      },
      "close_date": "2026-07-08",
      "close_price": 36.2,
      "final_pnl_pct": 3.85,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 8.52,
      "position_usd": 221.27
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
        }
      },
      "close_date": "2026-07-08",
      "close_price": 28.01,
      "final_pnl_pct": 4.76,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 10.53,
      "position_usd": 221.27
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
          "open": 274.02,
          "high": 274.43,
          "low": 270.97,
          "close": 272.37,
          "pnl_pct": 1.58
        },
        "2026-07-10": {
          "open": 273.3,
          "high": 277.85,
          "low": 271.41,
          "close": 276.0,
          "pnl_pct": 0.27
        }
      },
      "close_date": "2026-07-10",
      "close_price": 276.0,
      "final_pnl_pct": 0.27,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 0.61,
      "position_usd": 224.61
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
      "realized_pnl_usd": 19.11,
      "position_usd": 224.61
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
      "realized_pnl_usd": 2.25,
      "position_usd": 224.61
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
      "realized_pnl_usd": 0.93,
      "position_usd": 226.81
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
      "realized_pnl_usd": -1.47,
      "position_usd": 226.81
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
        }
      },
      "close_date": "2026-07-15",
      "close_price": 273.6,
      "final_pnl_pct": 0.87,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 1.97,
      "position_usd": 226.81
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
      "realized_pnl_usd": 2.81,
      "position_usd": 226.75
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
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-07-16",
      "close_price": 61.27,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.54,
      "position_usd": 226.75
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
      "realized_pnl_usd": -4.56,
      "position_usd": 226.95
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
      "realized_pnl_usd": -4.49,
      "position_usd": 226.78
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
      "realized_pnl_usd": -4.47,
      "position_usd": 226.78
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
          "open": 60.61,
          "high": 60.61,
          "low": 59.61,
          "close": 59.8,
          "pnl_pct": 2.29
        },
        "2026-07-21": {
          "open": 59.59,
          "high": 60.07,
          "low": 59.38,
          "close": 60.04,
          "pnl_pct": 1.9
        }
      },
      "close_date": "2026-07-21",
      "close_price": 60.04,
      "final_pnl_pct": 1.9,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 4.28,
      "position_usd": 225.42
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
      "realized_pnl_usd": -4.49,
      "position_usd": 225.42
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
      "realized_pnl_usd": -4.46,
      "position_usd": 225.42
    },
    {
      "ticker": "LCNB",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-07-21",
      "entry_price": 19.81,
      "allocated_usd": 500,
      "shares": 25.2398,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 22.78,
      "stop_loss": 19.41,
      "max_hold_date": "2026-07-23",
      "daily_prices": {
        "2026-07-22": {
          "open": 19.68,
          "high": 20.24,
          "low": 19.35,
          "close": 19.57,
          "pnl_pct": -2.02
        }
      },
      "close_date": "2026-07-22",
      "close_price": 19.41,
      "final_pnl_pct": -2.02,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.54,
      "position_usd": 224.96
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
      "realized_pnl_usd": 9.25,
      "position_usd": 224.96
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
      "realized_pnl_usd": 2.59,
      "position_usd": 224.96
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
      "realized_pnl_usd": 8.15,
      "position_usd": 224.5
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
          "open": 19.61,
          "high": 20.28,
          "low": 19.18,
          "close": 20.0,
          "pnl_pct": -1.99
        }
      },
      "close_date": "2026-07-24",
      "close_price": 19.96,
      "final_pnl_pct": -1.99,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.49,
      "position_usd": 225.69
    },
    {
      "ticker": "SFNC",
      "name": "",
      "action": "BUY",
      "signal_date": "2026-07-23",
      "entry_price": 23.11,
      "allocated_usd": 500,
      "shares": 21.6357,
      "actual_position_usd": 500.0,
      "entry_commission": 1.0,
      "take_profit": 26.58,
      "stop_loss": 22.65,
      "max_hold_date": "2026-07-27",
      "daily_prices": {
        "2026-07-24": {
          "open": 23.01,
          "high": 23.38,
          "low": 22.98,
          "close": 23.18,
          "pnl_pct": 0.3
        },
        "2026-07-27": {
          "open": 23.33,
          "high": 23.5,
          "low": 22.96,
          "close": 22.97,
          "pnl_pct": -0.61
        }
      },
      "close_date": "2026-07-27",
      "close_price": 22.97,
      "final_pnl_pct": -0.61,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -1.38,
      "position_usd": 225.69
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
      "realized_pnl_usd": -4.52,
      "position_usd": 226.05
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
      "realized_pnl_usd": 4.27,
      "position_usd": 226.05
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
      "realized_pnl_usd": -2.73,
      "position_usd": 225.91
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
      "realized_pnl_usd": -4.52,
      "position_usd": 225.89
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
          "open": 64.24,
          "high": 64.72,
          "low": 63.51,
          "close": 63.53,
          "pnl_pct": -0.73
        },
        "2026-07-30": {
          "open": 63.76,
          "high": 64.57,
          "low": 63.05,
          "close": 63.83,
          "pnl_pct": -0.27
        }
      },
      "close_date": "2026-07-30",
      "close_price": 63.83,
      "final_pnl_pct": -0.27,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -0.61,
      "position_usd": 225.89
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
      "realized_pnl_usd": 1.78,
      "position_usd": 225.16
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
          "open": 48.84,
          "high": 49.49,
          "low": 46.16,
          "close": 48.84,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-07-31",
      "close_price": 48.12,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.5,
      "position_usd": 225.1
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
      "realized_pnl_usd": -4.61,
      "position_usd": 225.1
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
      "realized_pnl_usd": 3.55,
      "position_usd": 224.37
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
      "realized_pnl_usd": -4.44,
      "position_usd": 224.37
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
      "realized_pnl_usd": 5.68,
      "position_usd": 224.37
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
      "realized_pnl_usd": -4.49,
      "position_usd": 224.28
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
          "open": 84.59,
          "high": 84.95,
          "low": 83.19,
          "close": 83.56,
          "pnl_pct": 0.16
        },
        "2026-08-06": {
          "open": 83.56,
          "high": 83.8,
          "low": 77.81,
          "close": 82.46,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-08-06",
      "close_price": 81.76,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.49,
      "position_usd": 224.28
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
          "open": 21.5,
          "high": 22.29,
          "low": 20.52,
          "close": 20.76,
          "pnl_pct": -1.99
        }
      },
      "close_date": "2026-08-06",
      "close_price": 21.16,
      "final_pnl_pct": -1.99,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -4.47,
      "position_usd": 224.4
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
          "open": 44.89,
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
      "realized_pnl_usd": -4.47,
      "position_usd": 223.5
    }
  ],
  "_note": "H-DS 模拟盘：DeepSeek(V4-pro) 信号 + H 出场规则(TP15/SL2/2日/gap1.0)。与 Plan H(Haiku信号+同规则)头对头比模型。仅A/B对比,不是真实交易方案。",
  "stats": {
    "total_trades": 74,
    "win_trades": 38,
    "win_rate": 51.4,
    "total_realized_pnl_usd": 230.57,
    "open_unrealized_pnl_usd": 32.14,
    "portfolio_value": 2262.71,
    "total_commission_usd": 148.0,
    "skipped_gap": 50,
    "skipped_zero_shares": 0,
    "skipped_no_cash": 32,
    "updated_at": "2026-08-07"
  }
};
