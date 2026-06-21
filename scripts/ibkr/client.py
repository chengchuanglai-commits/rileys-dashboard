"""IBKR 连接 + 健康检查。所有 I/O 收敛此处。"""
import time
from ib_insync import IB
from scripts.ibkr.config import PORTS

def connect(client_id=10, timeout=8, retries=4, retry_wait=6):
    """尝试 PORTS 列表,返回 (ib, port) 或 (None, None)。
    内置重试:Gateway 数据农场初次同步常间歇性超时(Error 1100/farm reconnect),
    单次失败不放弃→整轮 batch 不会因一次卡顿而中止(真钱时=该交易却没交易的洞)。"""
    for attempt in range(retries):
        for port in PORTS:
            ib = IB()
            try:
                ib.connect("127.0.0.1", port, clientId=client_id, timeout=timeout)
                return ib, port
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

def cancel_all(ib):
    """全局撤单(跨session,reqGlobalCancel——避开今天踩的10147坑)。"""
    ib.reqGlobalCancel(); ib.sleep(3)
    ib.reqAllOpenOrders(); ib.sleep(1)
    return len(ib.openTrades())
