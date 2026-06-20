"""
MOM 历史回测（FMP 诚实版）—— 治幸存者偏差 + 加 SPY-200MA 市场闸门 + 拉长到含熊市窗口。

与 yfinance 快版的区别（这版更诚实）：
  1. 池子含**退市票**：现存>$3B + 窗口内US主板曾>$3B的退市票(FRC/SIVB/ATVI/TWTR…)。持仓票中途退市→按最后可得价强平,捕捉"买了然后归零"。
  2. **point-in-time 池子**：每个日期只纳入"当天市值≥$3B"的票(用 FMP 历史市值),不偷看"今天才大"的。
  3. **窗口 2021-06→2026-06(含2022熊市)**,能测 regime。
  4. **SPY-200MA 市场闸门**:跌破200线不开新动量仓。gate on/off 并排对照,看闸门在2022救了多少。
  5. 沿用滑点敏感度(0/0.3/0.4/0.5%)。选股 analyze()/出场引擎与实盘逐字一致。

三段全缓存(data/fmp-cache/):建池→拉价/市值→回测。拉过落盘,迭代零新增FMP调用。
用法: FMP_API_KEY=... python scripts/backtest-momentum-fmp.py   (加 BT_REFRESH=1 强制重拉)
"""
import os, json, time, urllib.request, urllib.parse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import numpy as np

FMP_KEY = os.environ.get("FMP_API_KEY", "").strip()
REFRESH = os.environ.get("BT_REFRESH", "") == "1"
WIN_FROM = os.environ.get("BT_FROM", "2021-06-01")
WIN_TO   = os.environ.get("BT_TO",   "2026-06-18")
MKT_MIN = 3_000_000_000
TOP_N = 10
REBALANCE_EVERY = 5
PER_POSITION_USD = 500
INIT = 2000
COMMISSION = 1.0
THROTTLE = 0.05          # 并发下靠 worker 数限速,throttle 仅作礼貌间隔
WORKERS = 8              # 8并发 × ~3.3s/调用 ≈ 144/min,远低于 STARTER ~300/min 上限
CACHE = "data/fmp-cache"
PX_DIR = f"{CACHE}/px"
MC_DIR = f"{CACHE}/mc"
OUT = "data/backtest-momentum-fmp.json"
for d in (CACHE, PX_DIR, MC_DIR):
    os.makedirs(d, exist_ok=True)

# 手工补:2021-2026 美股曾>$3B 的退市大票(FMP STARTER 翻不了历史退市页,手工补关键名单)。
# 含 M&A并购(acquired,常涨入收购价=动量会持有的赢家) + 暴雷/破产(failure,如银行)。市值门会剔除不合格的。
CURATED_DELISTED = [
    # 并购退市 (M&A delisting,常涨入收购价)
    "ATVI","VMW","SGEN","ABMD","PXD","SPLK","TWTR","CTLT","ZEN","MNDT","CTXS","CERN",
    "NUAN","XLNX","MXIM","WORK","AVLR","COUP","CONE","QTS","CXO","KSU","INFO","TIF",
    "ALXN","VG","STOR","FLIR","ACIA",
    # 暴雷/破产退市 (failure/bankruptcy delisting)
    "SIVB","FRC","SBNY","BBBY","WE","SAVE","TWNK",
]

_calls = 0
def fmp_get(path):
    global _calls
    url = f"https://financialmodelingprep.com/stable/{path}{'&' if '?' in path else '?'}apikey={FMP_KEY}"
    for attempt in range(3):
        try:
            time.sleep(THROTTLE); _calls += 1
            with urllib.request.urlopen(url, timeout=30) as r:
                d = json.loads(r.read())
            return d if isinstance(d, list) else []
        except Exception as e:
            if attempt == 2:
                print(f"  [fmp] {path[:50]} 失败: {str(e)[:60]}")
            time.sleep(1.0)
    return []


def prefetch(syms, loader, label):
    """并发预热缓存(loader 内部自带缓存,已缓存的秒回)。"""
    todo = list(syms)
    done = [0]
    def _one(s):
        loader(s); done[0] += 1
        if done[0] % 100 == 0: print(f"    …{label} {done[0]}/{len(todo)} (FMP调用≈{_calls})")
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        list(ex.map(_one, todo))
    print(f"    {label} 完成 {len(todo)} (FMP调用≈{_calls})")


# ---------------- 选股逻辑：与 screen-momentum.py 逐字一致 ----------------
def sma(arr, n):
    if len(arr) < n: return None
    return float(np.mean(arr[-n:]))

def analyze(close, high, low, vol, spy_ret_6m):
    if len(close) < 220: return None
    c = close[-1]
    ma50, ma150, ma200 = sma(close, 50), sma(close, 150), sma(close, 200)
    ma10, ma20 = sma(close, 10), sma(close, 20)
    if None in (ma50, ma150, ma200, ma10, ma20): return None
    ma200_1mo_ago = sma(close[:-22], 200)
    hi_52 = float(np.max(close[-252:])); lo_52 = float(np.min(close[-252:]))
    tt = [c > ma150 and c > ma200, ma150 > ma200,
          ma200_1mo_ago is not None and ma200 > ma200_1mo_ago,
          ma50 > ma150 > ma200, c > ma50, c >= 1.30*lo_52, c >= 0.75*hi_52]
    if not all(tt): return None
    ret_6m = c / close[-126] - 1 if len(close) >= 126 else 0.0
    rs = ret_6m - spy_ret_6m
    ma_band = max(ma10, ma20); dist_to_ma = (c - ma_band)/ma_band
    edge_pullback = float(np.clip(1 - dist_to_ma/0.12, 0, 1))
    v5, v50 = sma(vol, 5), sma(vol, 50)
    vol_ratio = (v5/v50) if (v5 and v50 and v50 > 0) else 1.0
    edge_volcontract = float(np.clip(1 - (vol_ratio-0.6)/0.8, 0, 1))
    near_high = (c - hi_52)/hi_52
    edge_nearhigh = float(np.clip(1 + near_high/0.25, 0, 1))
    return {"rs": rs, "edge_pullback": edge_pullback,
            "edge_volcontract": edge_volcontract, "edge_nearhigh": edge_nearhigh}

def screen_asof(data_asof, spy_ret_6m):
    rows = []
    for tk, sl in data_asof.items():
        r = analyze(sl["C"], sl["H"], sl["L"], sl["V"], spy_ret_6m)
        if r: rows.append({"ticker": tk, **r})
    if not rows: return []
    rs_sorted = sorted(rows, key=lambda r: -r["rs"]); n = len(rs_sorted)
    for i, r in enumerate(rs_sorted):
        r["rs_rank"] = 1 - i/(n-1) if n > 1 else 0.5
    for r in rows:
        r["score"] = 0.40*r["rs_rank"] + 0.25*r["edge_pullback"] + 0.15*r["edge_volcontract"] + 0.20*r["edge_nearhigh"]
    rows.sort(key=lambda r: -r["score"])
    return [r["ticker"] for r in rows[:TOP_N]]


# ---------------- Phase A：建池(现存 + 退市,全 point-in-time 市值门) ----------------
def build_universe():
    cache_f = f"{CACHE}/universe.json"
    if os.path.exists(cache_f) and not REFRESH:
        u = json.load(open(cache_f))
        print(f"[universe] 读缓存: 现存{len(u['current'])} + 退市保留{len(u['delisted_kept'])}")
        return u
    # 现存流动票
    current = []
    for exch in ("NASDAQ", "NYSE"):
        d = fmp_get(f"company-screener?marketCapMoreThan=3000000000&exchange={exch}&isActivelyTrading=true&isFund=false&isEtf=false&limit=250")
        for x in d:
            s = (x.get("symbol") or "").strip()
            if s and s.isalpha() and len(s) <= 5: current.append(s)
    current = sorted(set(current))
    print(f"[universe] 现存流动票 {len(current)} 只")
    # 退市票:分页(新→旧),保留 US主板 且 delistedDate 落在窗口
    delisted_cand = []
    page = 0
    while page < 90:
        d = fmp_get(f"delisted-companies?page={page}")
        if not d: break
        oldest = min((x.get("delistedDate", "9999") for x in d), default="9999")
        for x in d:
            exch = x.get("exchange", ""); dd = x.get("delistedDate", "")
            if exch in ("NASDAQ", "NYSE", "AMEX") and dd >= WIN_FROM:
                s = (x.get("symbol") or "").strip()
                if s and s.replace(".", "").replace("-", "").isalnum() and len(s) <= 6:
                    delisted_cand.append(s)
        page += 1
        if oldest < WIN_FROM: break   # 已翻过窗口起点
    delisted_cand = sorted(set(delisted_cand))
    print(f"[universe] 窗口内US主板退市候选 {len(delisted_cand)} 只,并发查曾否>$3B…")
    prefetch(delisted_cand, load_mktcap, "退市市值")
    kept = []
    for s in delisted_cand:
        mc = load_mktcap(s)   # 走缓存
        if mc and max((v for _, v in mc), default=0) >= MKT_MIN:
            kept.append(s)
    print(f"[universe] 退市票曾>$3B保留 {len(kept)} 只: {kept[:20]}{'…' if len(kept)>20 else ''}")
    u = {"current": current, "delisted_kept": kept, "from": WIN_FROM, "to": WIN_TO,
         "built": datetime.now().strftime("%Y-%m-%d %H:%M")}
    json.dump(u, open(cache_f, "w"), ensure_ascii=False, indent=2)
    return u


def load_mktcap(sym):
    """历史市值序列 [(date, cap)],缓存。"""
    f = f"{MC_DIR}/{sym}.json"
    if os.path.exists(f) and not REFRESH:
        return json.load(open(f))
    d = fmp_get(f"historical-market-capitalization?symbol={urllib.parse.quote(sym)}&from={WIN_FROM}&to={WIN_TO}&limit=2000")
    series = sorted([[x["date"], float(x.get("marketCap") or 0)] for x in d if x.get("date")])
    json.dump(series, open(f, "w"))
    return series


def load_px(sym):
    """复权 OHLCV [[date,H,L,C,V],…],缓存。"""
    f = f"{PX_DIR}/{sym}.json"
    if os.path.exists(f) and not REFRESH:
        return json.load(open(f))
    d = fmp_get(f"historical-price-eod/dividend-adjusted?symbol={urllib.parse.quote(sym)}&from={WIN_FROM}&to={WIN_TO}")
    rows = []
    for x in d:
        try:
            rows.append([x["date"], float(x["adjHigh"]), float(x["adjLow"]), float(x["adjClose"]), float(x.get("volume") or 0)])
        except Exception:
            pass
    rows.sort()
    json.dump(rows, open(f, "w"))
    return rows


# ---------------- Phase C：回测引擎(含退市强平 + SPY-200MA闸门 + 滑点) ----------------
def simulate(exit_rule, signals_by_date, ohlc, posmap, last_date, cal, market_ok, slip):
    held, closed = {}, []
    comm = 0.0
    def ma_at(tk, p, n):
        C = ohlc[tk]["C"]
        return float(np.mean(C[p-n+1:p+1])) if p >= n-1 else None
    def open_pos(tk, date):
        nonlocal comm
        p = posmap.get(tk, {}).get(date)
        if p is None: return
        entry = round(float(ohlc[tk]["C"][p]), 2)
        if entry <= 0: return
        d = {"ticker": tk, "signal_date": date, "entry_price": entry,
             "entry_fill": entry*(1+slip), "shares": round(PER_POSITION_USD/entry, 4), "pos": p}
        if exit_rule == "H":
            d["take_profit"] = round(entry*1.15, 2); d["stop_loss"] = round(entry*0.98, 2)
        else:
            d["stop_loss"] = round(entry*0.92, 2)
        held[tk] = d; comm += COMMISSION
    def close_pos(tk, date, price, reason):
        nonlocal comm
        pos = held.pop(tk); comm += COMMISSION
        exit_fill = price*(1-slip); move = exit_fill - pos["entry_fill"]
        closed.append({"ticker": tk, "signal_date": pos["signal_date"], "close_date": date,
                       "close_reason": reason, "final_pnl_pct": round(move/pos["entry_fill"]*100, 2),
                       "realized_pnl_usd": round(pos["shares"]*move - 2*COMMISSION, 2)})
    last_rebal = -999
    for i, date in enumerate(cal):
        for tk in list(held.keys()):
            p = posmap.get(tk, {}).get(date)
            if p is None:
                if date > last_date.get(tk, "9999"):   # 数据到头=退市→强平
                    C = ohlc[tk]["C"]; close_pos(tk, date, float(C[-1]), "delisted")
                continue
            pos = held[tk]; hi, lo, cl = ohlc[tk]["H"][p], ohlc[tk]["L"][p], ohlc[tk]["C"][p]
            if exit_rule == "H":
                if lo <= pos["stop_loss"]: close_pos(tk, date, pos["stop_loss"], "stop_loss"); continue
                if hi >= pos["take_profit"]: close_pos(tk, date, pos["take_profit"], "take_profit"); continue
                if (p - pos["pos"]) >= 2: close_pos(tk, date, float(cl), "max_hold")
            else:
                if lo <= pos["stop_loss"]: close_pos(tk, date, pos["stop_loss"], "init_stop"); continue
                ma = ma_at(tk, p, 20)
                if ma is not None and cl < ma: close_pos(tk, date, float(cl), "ma_break"); continue
                if (p - pos["pos"]) >= 60: close_pos(tk, date, float(cl), "max_hold")
        if date in signals_by_date and (i - last_rebal) >= REBALANCE_EVERY:
            if market_ok.get(date, True):           # SPY-200MA 闸门
                for tk in signals_by_date[date]:
                    if tk not in held: open_pos(tk, date)
            last_rebal = i
    unreal = 0.0
    for tk, pos in held.items():
        C = ohlc[tk]["C"]; cur = float(C[-1])
        unreal += pos["shares"] * (cur*(1-slip) - pos["entry_fill"])
    return closed, round(unreal, 2), round(comm, 2), len(held)


def perf(closed, unreal):
    realized = sum(c["realized_pnl_usd"] for c in closed)
    wins = [c for c in closed if c["realized_pnl_usd"] > 0]
    gl = abs(sum(c["realized_pnl_usd"] for c in closed if c["realized_pnl_usd"] <= 0))
    gw = sum(c["realized_pnl_usd"] for c in wins)
    srt = sorted(closed, key=lambda c: -c["realized_pnl_usd"])
    drop2 = realized - sum(c["realized_pnl_usd"] for c in srt[:2])
    delisted_losses = sum(1 for c in closed if c["close_reason"] == "delisted")
    return {"trades": len(closed), "win_rate": round(len(wins)/len(closed)*100, 1) if closed else 0,
            "return_pct": round((realized+unreal)/INIT*100, 1), "realized_usd": round(realized, 2),
            "unreal_usd": unreal, "pf": round(gw/gl, 2) if gl > 0 else 99.9,
            "realized_drop2": round(drop2, 2), "delisted_hits": delisted_losses}


def main():
    u = build_universe()
    # 并入手工退市清单(去重),让报告与回测都计入
    u["delisted_kept"] = sorted(set(u["delisted_kept"]) | set(CURATED_DELISTED))
    universe = sorted(set(u["current"]) | set(u["delisted_kept"]))
    print(f"\n[px] 并发拉 {len(universe)} 票 + SPY 复权价 & 市值(缓存)…")
    prefetch(universe + ["SPY"], load_px, "价格")
    prefetch(universe, load_mktcap, "市值")
    ohlc, posmap, last_date, mc_series = {}, {}, {}, {}
    for tk in universe:
        rows = load_px(tk)            # 走缓存
        if len(rows) < 240: continue
        idx = [r[0] for r in rows]
        ohlc[tk] = {"H": np.array([r[1] for r in rows]), "L": np.array([r[2] for r in rows]),
                    "C": np.array([r[3] for r in rows]), "V": np.array([r[4] for r in rows]), "idx": idx}
        posmap[tk] = {dt: j for j, dt in enumerate(idx)}
        last_date[tk] = idx[-1]
        mc_series[tk] = load_mktcap(tk)
    print(f"[px] {len(ohlc)} 票可用 · 总FMP调用≈{_calls}")

    spy = load_px("SPY")
    spy_idx = [r[0] for r in spy]; spy_C = np.array([r[3] for r in spy])
    spy_pos = {d: j for j, d in enumerate(spy_idx)}

    def mc_asof(tk, date):
        s = mc_series.get(tk) or []
        v = 0.0
        for dt, cap in s:
            if dt <= date: v = cap
            else: break
        return v

    cal = spy_idx
    start_i = 252
    rebal_dates = [cal[i] for i in range(start_i, len(cal), REBALANCE_EVERY)]
    bt_cal = cal[start_i:]
    print(f"[bt] 窗口 {bt_cal[0]}→{bt_cal[-1]} ({len(bt_cal)}日,{len(rebal_dates)}再平衡点)")

    # point-in-time 选股 + 市值门
    signals_by_date, empty = {}, 0
    for d in rebal_dates:
        q = spy_pos.get(d)
        if q is None or q < 126: continue
        spy_ret_6m = float(spy_C[q]/spy_C[q-126] - 1)
        data_asof = {}
        for tk, o in ohlc.items():
            p = posmap[tk].get(d)
            if p is None or p < 220: continue
            if mc_asof(tk, d) < MKT_MIN: continue      # 当天市值门(point-in-time)
            data_asof[tk] = {"C": o["C"][:p+1], "H": o["H"][:p+1], "L": o["L"][:p+1], "V": o["V"][:p+1]}
        picks = screen_asof(data_asof, spy_ret_6m)
        if picks: signals_by_date[d] = set(picks)
        else: empty += 1
    print(f"[bt] {len(signals_by_date)}出榜 / {empty}空榜(趋势模板挡住=大盘弱,含2022应有不少)")

    # SPY-200MA 市场闸门
    market_ok = {}
    for d in rebal_dates:
        q = spy_pos.get(d)
        market_ok[d] = bool(q is not None and q >= 200 and spy_C[q] > float(np.mean(spy_C[q-199:q+1])))
    gate_open_days = sum(1 for d in rebal_dates if market_ok.get(d))
    spy_ret_pct = float(spy_C[-1]/spy_C[start_i] - 1)*100

    # 跑：两出场 × {闸门关,闸门开} × 滑点sweep
    slips = [0.0, 0.003, 0.004]
    table = {}
    for rule in ("H", "MA"):
        for gate, gname in ((False, "无闸门"), (True, "SPY200闸门")):
            mok = market_ok if gate else {d: True for d in rebal_dates}
            row = {}
            for slip in slips:
                cl, un, cm, op = simulate(rule, signals_by_date, ohlc, posmap, last_date, bt_cal, mok, slip)
                p = perf(cl, un)
                row[f"{slip*100:.1f}%"] = p
            table[f"{rule}/{gname}"] = row

    result = {"generated": datetime.now().strftime("%Y-%m-%d %H:%M"), "window": [bt_cal[0], bt_cal[-1]],
              "universe_current": len(u["current"]), "universe_delisted_kept": len(u["delisted_kept"]),
              "usable": len(ohlc), "rebalance_points": len(rebal_dates),
              "boards_with_picks": len(signals_by_date), "empty_boards": empty,
              "gate_open_rebalances": gate_open_days, "spy_return_pct": round(spy_ret_pct, 1),
              "fmp_calls": _calls, "table": table,
              "note": "诚实版:含退市票强平+point-in-time市值门+复权价。残留偏差:仅覆盖'现存>$3B+窗口内退市曾>$3B',漏'仍上市但已缩水到<$3B'的票(较小)。"}
    json.dump(result, open(OUT, "w"), ensure_ascii=False, indent=2)

    # 打印
    print(f"\n{'='*70}\n  MOM 诚实版回测 {bt_cal[0]}→{bt_cal[-1]}\n{'='*70}")
    print(f"  池: 现存{len(u['current'])} + 退市保留{len(u['delisted_kept'])} = 可用{len(ohlc)}只")
    print(f"  SPY同期 {spy_ret_pct:+.1f}% · 再平衡{len(rebal_dates)}点(闸门放行{gate_open_days}) · 空榜{empty} · FMP调用{_calls}")
    print(f"\n  总收益% [trades/胜率/PF/去尾2笔已实现/退市强平数] — 按滑点:")
    for key, row in table.items():
        print(f"\n  ● {key}")
        for slipk, p in row.items():
            print(f"    滑{slipk:>5}: {p['return_pct']:+7.1f}%  [{p['trades']}笔 胜{p['win_rate']}% PF{p['pf']} 去尾2笔${p['realized_drop2']:+.0f} 退市{p['delisted_hits']}]")
    print(f"\n  详情 → {OUT}")


if __name__ == "__main__":
    main()
