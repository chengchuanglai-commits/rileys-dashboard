// Plan H 模拟盘持仓 — 历史最优参数(TP15/SL2/2日) 回溯 + 实时更新
window.PORTFOLIO_H = {
  "capital_usd": 2000,
  "open_positions": [
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
      "stop_loss": 16.56,
      "max_hold_date": "2026-06-18",
      "daily_prices": {
        "2026-06-17": {
          "open": 16.25,
          "high": 16.55,
          "low": 16.18,
          "close": 16.28,
          "pnl_pct": -0.25
        }
      }
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
      "stop_loss": 37.78,
      "max_hold_date": "2026-06-18",
      "daily_prices": {
        "2026-06-17": {
          "open": 37.03,
          "high": 37.04,
          "low": 36.26,
          "close": 36.38,
          "pnl_pct": 1.78
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
      "take_profit": 100.58,
      "stop_loss": 85.71,
      "max_hold_date": "2026-05-29",
      "daily_prices": {
        "2026-05-28": {
          "open": 90.38,
          "high": 90.8,
          "low": 84.35,
          "close": 87.29,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-05-28",
      "close_price": 85.71,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -10.75
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
      "stop_loss": 19.74,
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
      "stop_loss": 103.12,
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
      "stop_loss": 92.82,
      "max_hold_date": "2026-06-01",
      "daily_prices": {
        "2026-05-29": {
          "open": 90.73,
          "high": 93.68,
          "low": 89.87,
          "close": 91.61,
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-05-29",
      "close_price": 92.82,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -11.1
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
      "stop_loss": 69.11,
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
      "stop_loss": 110.53,
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
      "stop_loss": 312.13,
      "max_hold_date": "2026-06-09",
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
          "pnl_pct": -2.0
        }
      },
      "close_date": "2026-06-09",
      "close_price": 312.13,
      "final_pnl_pct": -2.0,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -8.37
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
      "stop_loss": 49.32,
      "max_hold_date": "2026-06-09",
      "daily_prices": {
        "2026-06-08": {
          "open": 47.58,
          "high": 49.68,
          "low": 47.12,
          "close": 49.52,
          "pnl_pct": -2.01
        }
      },
      "close_date": "2026-06-08",
      "close_price": 49.32,
      "final_pnl_pct": -2.01,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -11.72
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
      "stop_loss": 18.29,
      "max_hold_date": "2026-06-10",
      "daily_prices": {
        "2026-06-09": {
          "open": 17.79,
          "high": 18.5,
          "low": 16.94,
          "close": 17.5,
          "pnl_pct": -2.01
        }
      },
      "close_date": "2026-06-09",
      "close_price": 18.29,
      "final_pnl_pct": -2.01,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -11.73
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
      "stop_loss": 40.12,
      "max_hold_date": "2026-06-10",
      "daily_prices": {
        "2026-06-09": {
          "open": 39.43,
          "high": 40.93,
          "low": 39.37,
          "close": 39.7,
          "pnl_pct": -2.01
        }
      },
      "close_date": "2026-06-09",
      "close_price": 40.12,
      "final_pnl_pct": -2.01,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -11.49
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
      "stop_loss": 12.61,
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
      "stop_loss": 15.5,
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
          "pnl_pct": -1.97
        }
      },
      "close_date": "2026-06-15",
      "close_price": 15.5,
      "final_pnl_pct": -1.97,
      "close_reason": "stop_loss",
      "exit_commission": 1.0,
      "commission_total": 2.0,
      "realized_pnl_usd": -11.58
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
      "stop_loss": 10.09,
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
      "stop_loss": 177.07,
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
      "realized_pnl_usd": -12.01
    }
  ],
  "_note": "Plan H 模拟盘：历史最优参数 TP +15% / SL -2% / 最大2交易日 / 不利跳空>1%过滤 / IBKR佣金$0.005/股min$1（D的收紧止损版）",
  "stats": {
    "total_trades": 15,
    "win_trades": 6,
    "win_rate": 40.0,
    "total_realized_pnl_usd": 172.8,
    "open_unrealized_pnl_usd": 5.35,
    "portfolio_value": 2178.15,
    "total_commission_usd": 30.0,
    "skipped_gap": 5,
    "skipped_zero_shares": 1,
    "updated_at": "2026-06-17"
  }
};
