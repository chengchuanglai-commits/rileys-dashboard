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

def _oca(sym):
    """该票的保护OCA组名。止损单 + 任何卖出单 都进这一组→IBKR原生保证互斥,根治超卖。"""
    return f"prot_{sym}"

def place_limit(ib, sym, qty, price, fractional=FRACTIONAL, oca_sell=False):
    """限价单。fractional=True 用 cashQty(qty 此时是金额);否则整数股数。
    oca_sell=True:卖单加入该票OCA组→成交即与该票止损互斥(成交后撤掉止损,防退出后留孤儿止损→未来做空)。
    仅 trade_close 退出用True;trade_open 开盘已 cancel_all 清空止损,其卖单设False——否则会误撤掉本批末尾
    给该票重挂的止损(2026-06-30 RVMD被trim后裸奔的坑)。"""
    ct = Stock(sym, "SMART", "USD"); ib.qualifyContracts(ct)
    side = "BUY" if qty > 0 else "SELL"
    lmt = round(price * (1 + LIMIT_BUFFER) if qty > 0 else price * (1 - LIMIT_BUFFER), 2)
    if fractional:
        o = LimitOrder(side, 0, lmt); o.cashQty = abs(qty)
    else:
        o = LimitOrder(side, abs(qty), lmt)
    o.tif = "DAY"
    if side == "SELL" and oca_sell:
        o.ocaGroup = _oca(sym); o.ocaType = 2   # 2=REDUCE:成交后同组其余按量缩减(非block)
    return ib.placeOrder(ct, o)

def place_stop(ib, sym, qty, stop_price):
    """固定 stop(到价市价卖)。qty=持仓股数(正)。
    进该票OCA组→与卖单/其它止损互斥:即使止损重复或撞上rebalance卖单,OCA保证净卖出≤持仓,绝不超卖成空头。"""
    ct = Stock(sym, "SMART", "USD"); ib.qualifyContracts(ct)
    o = StopOrder("SELL", abs(qty), round(stop_price, 2)); o.tif = "GTC"
    o.ocaGroup = _oca(sym); o.ocaType = 2
    return ib.placeOrder(ct, o)
