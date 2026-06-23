"""收盘batch:**仅动量腿(MOM-MA)持仓**收盘<20MA→挂次日卖单。指数核心(SPY)豁免(长期持有,不走20MA)。
LIVE=False只算不下。落exec-log。"""
import os, json, time
import numpy as np
from scripts.ibkr.client import connect, health
from scripts.ibkr.orders import place_limit
from scripts.ibkr.config import LIVE, INDEX_CORE_SYMS as INDEX_CORE
from scripts.ibkr.notify import send
# 指数核心(config.INDEX_CORE_SYMS):长期持有,豁免20MA出场

def _momentum_syms():
    """哪些持仓属于动量腿(MOM-MA)——只有这些走20MA出场。读 momma 持仓。"""
    syms = set()
    try:
        d = json.load(open("data/portfolio_momma.json"))
        for p in d.get("open_positions", []):
            if p.get("ticker"): syms.add(p["ticker"])
    except Exception:
        pass
    return syms

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
    mom_syms = _momentum_syms()
    exits = []
    for p in ib.positions(h["account"]):
        if p.position <= 0: continue
        sym = p.contract.symbol
        # 指数核心豁免;只有动量腿的票才走20MA出场(指数长持/B-quant另有再平衡逻辑)
        if sym in INDEX_CORE or sym not in mom_syms:
            continue
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
