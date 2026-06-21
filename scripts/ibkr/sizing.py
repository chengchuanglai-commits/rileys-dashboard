"""目标金额 → 股数。整数股(向下取整,买不起1股=0)或小数股(保留4位)。"""
import math

def target_shares(target_usd, price, fractional=False):
    if not price or price <= 0:
        return 0
    raw = target_usd / price
    if fractional:
        return round(raw, 4)
    return int(math.floor(raw))
