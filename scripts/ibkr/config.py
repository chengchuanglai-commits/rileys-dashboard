"""执行系统常量集中。改一处即全局生效。真钱开关默认关。
   支持环境变量临时覆盖(IBKR_LIVE/IBKR_NOTIONAL),用于一次性 paper 验证而不改动安全默认。"""
import os as _os
LIVE = _os.environ.get("IBKR_LIVE", "0") == "1"     # 默认 False(安全);IBKR_LIVE=1 临时开
FRACTIONAL = False        # True=小数股(cashQty);默认整数股(权限未开,见spec实测)
NOTIONAL = float(_os.environ.get("IBKR_NOTIONAL", "2000"))   # 默认$2000;env可临时放大(paper验证规模)
PORTS = [4002, 7497, 4001, 7496]   # 连接尝试顺序:Gateway paper 优先

# 安全闸(随名义本金缩放:上限=名义本金×系数,防写死被放大规模击穿)
MAX_ORDER_USD = NOTIONAL * 0.75    # 单笔上限(SPY 60%在内,留余量)
MAX_TOTAL_USD = NOTIONAL * 1.15    # 总下单额上限

# 回撤断路器档位(占位值,# TODO 待 backtest-momentum-sized.py 回测校准)
DRAWDOWN_TIERS = {"warn": 0.20, "reduce_only": 0.25, "defensive": 0.28}
HARD_REDLINE = 0.30       # Riley 风险预算

# 出场
INIT_STOP_PCT = 0.08      # 单仓 -8% 固定 stop
LIMIT_BUFFER = 0.01       # 限价缓冲

LEG_PORT = {"momma": "data/portfolio_momma.json", "bq": "data/portfolio_bq.json"}

# 指数核心标的(2026-06-23 Riley 由SPY换QQQ:长期收益更高、夏普更优,风险可接受;
# 抗跌交给动量腿=进攻QQQ/防守动量腿分工)。改这一处即全局生效。
INDEX_SYM = "QQQ"
INDEX_CORE_SYMS = {"QQQ", "SPY", "VOO", "VTI"}   # 这些都算指数核心,豁免20MA出场
