"""引擎配置 allocation.json + 各腿持仓 → {symbol: target_usd}。"""
import json
from scripts.ibkr.config import NOTIONAL, LEG_PORT

def _load(p, d=None):
    try: return json.load(open(p))
    except Exception: return d

def build_targets(alloc_path="data/allocation.json", leg_paths=None, notional=NOTIONAL):
    leg_paths = leg_paths or LEG_PORT
    a = _load(alloc_path)
    if not a: return {}
    t = {}
    if a.get("index_pct", 0) * notional > 0:
        t["SPY"] = a["index_pct"] * notional
    for leg, w in a.get("final_allocation", {}).items():
        amt = w * notional
        if amt <= 0: continue
        port = _load(leg_paths.get(leg, ""), {})
        tks = [p["ticker"] for p in (port.get("open_positions") or []) if p.get("ticker")]
        if not tks: continue
        for tk in tks:
            t[tk] = t.get(tk, 0) + amt / len(tks)
    return t
