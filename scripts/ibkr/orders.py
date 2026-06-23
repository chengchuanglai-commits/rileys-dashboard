"""下单封装:安全闸校验 + 限价单 + stop单。唯一下单入口。"""
from ib_insync import Stock, LimitOrder, StopOrder
from scripts.ibkr.config import LIMIT_BUFFER, FRACTIONAL

def check_gates(plan, max_order, max_total):
    """plan: [{"sym","usd","qty"...}]。返回 (ok, reason)。
    总额只算**买入**(净新增敞口);卖出是回收资金不该计入——否则换仓(卖A买B)被绝对值之和误拦。"""
    for o in plan:
        if o["usd"] > max_order:
            return False, f"单笔 {o['sym']} ${o['usd']:.0f} > 上限 ${max_order:.0f}"
    buy_total = sum(o["usd"] for o in plan if o.get("qty", 0) > 0)   # 只算买入
    if buy_total > max_total:
        return False, f"买入总额 ${buy_total:.0f} > 上限 ${max_total:.0f}"
    return True, ""

def place_limit(ib, sym, qty, price, fractional=FRACTIONAL):
    """限价单。fractional=True 用 cashQty(qty 此时是金额);否则整数股数。"""
    ct = Stock(sym, "SMART", "USD"); ib.qualifyContracts(ct)
    side = "BUY" if qty > 0 else "SELL"
    lmt = round(price * (1 + LIMIT_BUFFER) if qty > 0 else price * (1 - LIMIT_BUFFER), 2)
    if fractional:
        o = LimitOrder(side, 0, lmt); o.cashQty = abs(qty)
    else:
        o = LimitOrder(side, abs(qty), lmt)
    o.tif = "DAY"
    return ib.placeOrder(ct, o)

def place_stop(ib, sym, qty, stop_price):
    """固定 stop(到价市价卖)。qty=持仓股数(正)。"""
    ct = Stock(sym, "SMART", "USD"); ib.qualifyContracts(ct)
    o = StopOrder("SELL", abs(qty), round(stop_price, 2)); o.tif = "GTC"
    return ib.placeOrder(ct, o)
