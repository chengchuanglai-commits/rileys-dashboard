"""回撤断路器:净值vs峰值→回撤→分档动作。阈值见 config(待回测校准)。"""
from scripts.ibkr.config import DRAWDOWN_TIERS

def drawdown(nav, peak):
    if not peak or peak <= 0:
        return 0.0
    return max(0.0, (peak - nav) / peak)

def breaker_action(dd, tiers=None):
    t = tiers or DRAWDOWN_TIERS
    if dd >= t["defensive"]:
        return "defensive"      # 全线挂出场
    if dd >= t["reduce_only"]:
        return "reduce_only"    # 停开新仓,只允出场
    if dd >= t["warn"]:
        return "warn"           # 预警,新仓减半
    return "normal"
