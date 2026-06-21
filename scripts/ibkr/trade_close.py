"""收盘batch:MOM-MA持仓收盘<20MA→挂次日卖单。LIVE=False只算不下。落exec-log。"""
import os, json, time
import numpy as np
from scripts.ibkr.client import connect, health
from scripts.ibkr.orders import place_limit
from scripts.ibkr.config import LIVE
from scripts.ibkr.notify import send

def _ma20_break(sym):
    """返回 (破位?, 收盘, ma20)。yfinance 近2月日线。"""
    import yfinance as yf
    try:
        c = np.asarray(yf.download(sym, period="2mo", interval="1d", progress=False)["Close"].dropna()).ravel()
        if len(c) < 20: return False, None, None
        ma20 = float(np.mean(c[-20:])); close = float(c[-1])
        return close < ma20, close, ma20
    except Exception:
        return False, None, None

def run():
    ib, port = connect(client_id=22)
    if not ib:
        send("⚠️ 收盘batch:网关连不上,中止\n（交易信号系统）"); return
    h = health(ib)
    exits = []
    for p in ib.positions(h["account"]):
        if p.position <= 0: continue
        sym = p.contract.symbol
        brk, close, ma20 = _ma20_break(sym)
        if brk:
            exits.append({"sym": sym, "qty": p.position, "close": close, "ma20": ma20})
    log = {"date": time.strftime("%Y-%m-%d"), "type": "close", "live": LIVE, "exits": exits, "placed": []}
    if exits and LIVE:
        for e in exits:
            try:
                tr = place_limit(ib, e["sym"], -e["qty"], e["close"])
                log["placed"].append({"sym": e["sym"], "status": tr.orderStatus.status})
            except Exception as ex:
                log["placed"].append({"sym": e["sym"], "error": str(ex)[:80]})
    elif exits:
        log["note"] = "DRY-RUN,未下出场单"
    os.makedirs("data/exec-log", exist_ok=True)
    # 收盘 log 追加到当日(不覆盖开盘)
    path = f"data/exec-log/{log['date']}.json"
    existing = json.load(open(path)) if os.path.exists(path) else {}
    existing["close_batch"] = log
    json.dump(existing, open(path, "w"), ensure_ascii=False, indent=2)
    ib.disconnect()
    print(json.dumps(log, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    run()
