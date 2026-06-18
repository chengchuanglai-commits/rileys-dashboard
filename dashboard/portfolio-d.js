// Plan D 模拟盘持仓 — 每日自动更新
window.PORTFOLIO_D = {
  "capital_usd": 2000,
  "open_positions": [
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
        "2026-06-18": {
          "close": 23.01,
          "pnl_pct": -2.22
        }
      },
      "gap_checked": true,
      "day1_open": 22.72,
      "day1_gap_pct": 0.93
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
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 33.0
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
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 38.79
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
        "2026-06-10": {
          "open": 11.78,
          "high": 12.3,
          "low": 10.85,
          "close": 11.5,
          "pnl_pct": 6.96
        },
        "2026-06-11": {
          "open": 11.89,
          "high": 12.0,
          "low": 10.26,
          "close": 11.55,
          "pnl_pct": 14.97
        }
      },
      "close_date": "2026-06-11",
      "close_price": 10.51,
      "final_pnl_pct": 14.97,
      "close_reason": "take_profit",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": 72.01
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
        }
      },
      "close_date": "2026-06-18",
      "close_price": 37.06,
      "final_pnl_pct": -0.05,
      "close_reason": "max_hold",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -2.24
    }
  ],
  "_note": "Plan D 模拟盘：TP +15% / SL -3% / 最大2交易日 / 不利跳空>1%过滤 / IBKR佣金$0.005/股min$1",
  "stats": {
    "total_trades": 17,
    "win_trades": 10,
    "win_rate": 58.8,
    "total_realized_pnl_usd": 185.25,
    "open_unrealized_pnl_usd": -11.1,
    "portfolio_value": 2174.15,
    "skipped_gap": 6,
    "updated_at": "2026-06-19"
  }
};
