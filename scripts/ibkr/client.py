"""IBKR 连接 + 健康检查。所有 I/O 收敛此处。"""
import time
from ib_insync import IB
from scripts.ibkr.config import PORTS

def connect(client_id=10, timeout=8, retries=9, retry_wait=18):
    """尝试 PORTS 列表,返回 (ib, port) 或 (None, None)。
    内置重试(~2.7分钟):①数据农场初次同步间歇超时 ②**IB Gateway每5.5小时滚动自动重启**
    (无固定时间可设,重启窗口会飘移撞上任何批次),重启期间端口ConnectionRefused~1-2分钟。
    重试够久=撞上重启也只是多等会儿就连上,不会误报"网关连不上"中止批次(真钱时=该交易却没交易的洞)。"""
    for attempt in range(retries):
        for port in PORTS:
            ib = IB()
            try:
                ib.connect("127.0.0.1", port, clientId=client_id, timeout=timeout)
                # socket通还不够:重启后数据农场resync期间"连上但positions/account超时"(2026-07-06踩坑)。
                # 必须验证数据真的在流(nav可取)才算ready,否则断开继续等农场同步。
                try:
                    ib.sleep(1)
                    summ = {v.tag: v.value for v in ib.accountSummary()}
                    nav = float(summ.get("NetLiquidation", 0) or 0)
                except Exception:
                    nav = 0
                if nav > 0:
                    return ib, port          # 连上且数据就绪
                try: ib.disconnect()          # 连上但农场没同步→断开重试
                except Exception: pass
            except Exception:
                try: ib.disconnect()
                except Exception: pass
                continue
        if attempt < retries - 1:
            time.sleep(retry_wait)   # 等数据农场重连后再试
    return None, None

def health(ib):
    """返回 dict:account / is_paper / nav / cash / open_orders 数。"""
    acct = ib.managedAccounts()[0] if ib.managedAccounts() else None
    summ = {v.tag: v.value for v in ib.accountSummary()
            if v.tag in ("NetLiquidation", "TotalCashValue")}
    ib.reqAllOpenOrders(); ib.sleep(1)
    return {
        "account": acct,
        "is_paper": bool(acct and acct.startswith("DU")),
        "nav": float(summ.get("NetLiquidation", 0) or 0),
        "cash": float(summ.get("TotalCashValue", 0) or 0),
        "open_orders": len(ib.openTrades()),
    }

def cancel_all(ib, wait=24):
    """全局撤单(跨session,reqGlobalCancel——避开10147坑)。
    ⚠️reqGlobalCancel是异步的,传播要~15s。固定sleep(3)太短→旧止损没真撤掉就返回,
    调用方接着下rebalance单时旧止损仍可能触发→双卖把多头超卖成空头(2026-06-29 GFS踩坑)。
    故改为轮询:等到无活跃挂单或超时,确保旧单(尤其止损)真的清掉再返回。"""
    ib.reqGlobalCancel()
    deadline = time.time() + wait
    while time.time() < deadline:
        ib.sleep(2)
        ib.reqAllOpenOrders(); ib.sleep(1)
        active = [t for t in ib.openTrades()
                  if t.orderStatus.status in ("PreSubmitted", "Submitted", "PendingSubmit", "PendingCancel")]
        if not active:
            break
    ib.reqAllOpenOrders(); ib.sleep(1)
    return len([t for t in ib.openTrades()
                if t.orderStatus.status in ("PreSubmitted", "Submitted")])

def cancel_orphan_limits(ib):
    """清掉非止损的遗留挂单(LMT/MKT等),保留STP止损单。
    根治"跨日遗留限价单"——batch开始前调用,确保对账从干净状态开始。
    用全局撤单(跨session可靠)清掉所有限价单;止损单由各batch成交后重挂。"""
    ib.reqAllOpenOrders(); ib.sleep(1)
    nonstop = [t for t in ib.openTrades() if t.order.orderType not in ("STP", "STP LMT")]
    if not nonstop:
        return 0
    # 有非止损遗留单→记下止损单,全局撤,重挂止损
    from ib_insync import Stock, StopOrder
    stops = {}
    for t in ib.openTrades():
        if t.order.orderType == "STP":
            stops[t.contract.symbol] = float(t.order.auxPrice)
    ib.reqGlobalCancel(); ib.sleep(4)
    acct = ib.managedAccounts()[0] if ib.managedAccounts() else None
    # 重挂止损(给仍持有的多头仓)
    for pos in ib.positions(acct):
        sym = pos.contract.symbol
        if pos.position > 0 and sym in stops:
            try:
                ct = Stock(sym, "SMART", "USD"); ib.qualifyContracts(ct)
                o = StopOrder("SELL", pos.position, round(stops[sym], 2)); o.tif = "GTC"
                ib.placeOrder(ct, o)
            except Exception:
                pass
    ib.sleep(2)
    return len(nonstop)
