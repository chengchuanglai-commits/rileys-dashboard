"""执行系统常量集中。改一处即全局生效。真钱开关默认关。"""
LIVE = False              # True=真钱;默认 paper
FRACTIONAL = False        # True=小数股(cashQty);默认整数股(权限未开,见spec实测)
NOTIONAL = 2000.0         # 名义本金(模拟真实$2000规模)
PORTS = [4002, 7497, 4001, 7496]   # 连接尝试顺序:Gateway paper 优先

# 安全闸
MAX_ORDER_USD = 1500.0    # 单笔上限(SPY 60%≈$1200 在内)
MAX_TOTAL_USD = 2200.0    # 总下单额上限

# 回撤断路器档位(占位值,# TODO 待 backtest-momentum-sized.py 回测校准)
DRAWDOWN_TIERS = {"warn": 0.20, "reduce_only": 0.25, "defensive": 0.28}
HARD_REDLINE = 0.30       # Riley 风险预算

# 出场
INIT_STOP_PCT = 0.08      # 单仓 -8% 固定 stop
LIMIT_BUFFER = 0.01       # 限价缓冲

LEG_PORT = {"momma": "data/portfolio_momma.json", "bq": "data/portfolio_bq.json"}
