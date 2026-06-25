"""引擎配置 allocation.json + 各腿持仓 → {symbol: target_usd}。"""
import json
from scripts.ibkr.config import NOTIONAL, LEG_PORT, INDEX_SYM

def _load(p, d=None):
    try: return json.load(open(p))
    except Exception: return d

def build_targets(alloc_path="data/allocation.json", leg_paths=None, notional=NOTIONAL):
    leg_paths = leg_paths or LEG_PORT
    a = _load(alloc_path)
    if not a: return {}
    t = {}
    if a.get("index_pct", 0) * notional > 0:
        t[INDEX_SYM] = a["index_pct"] * notional   # 指数核心(config.INDEX_SYM=QQQ)
    for leg, w in a.get("final_allocation", {}).items():
        amt = w * notional
        if amt <= 0: continue
        port = _load(leg_paths.get(leg, ""), {})
        tks = [p["ticker"] for p in (port.get("open_positions") or []) if p.get("ticker")]
        if not tks: continue
        for tk in tks:
            t[tk] = t.get(tk, 0) + amt / len(tks)
    return t


def build_master_targets(master_path="data/master-allocation.json", notional=NOTIONAL):
    """三线统一目标:读 master-allocation.json(指数+长线+波动) → {symbol: target_usd}。
    指数=INDEX_SYM;长线=longterm 9只等权;波动=动量腿当前持仓等权(IBKR系统选的)。
    用 notional 重新缩放(master里是$2000名义,paper验证用更大NOTIONAL时按比例放大)。"""
    m = _load(master_path)
    if not m: return {}
    base = m.get("capital", notional) or notional
    scale = notional / base if base > 0 else 1.0
    t = {}
    sl = m.get("sleeves", {})
    # ① 指数核心
    idx = sl.get("index", {})
    if idx.get("target_usd", 0) > 0:
        t[idx.get("holding", INDEX_SYM)] = idx["target_usd"] * scale
    # ② 长线持股(等权)
    lt = sl.get("longterm", {})
    lt_holds = lt.get("holdings", [])
    if lt_holds and lt.get("target_usd", 0) > 0:
        per = lt["target_usd"] * scale / len(lt_holds)
        for tk in lt_holds:
            t[tk] = t.get(tk, 0) + per
    # ③ 波动捕捉(动量腿当前持仓等权)
    vol = sl.get("volatility", {})
    vh = vol.get("current_holdings", [])
    if vh and vol.get("target_usd", 0) > 0:
        per = vol["target_usd"] * scale / len(vh)
        for tk in vh:
            t[tk] = t.get(tk, 0) + per
    return t
