"""
MOM 历史回测（yfinance 快版）——验证动量/趋势腿的两套出场(MOM-H vs MOM-MA)在过去 ~2-3 年的表现。

诚实性：纯价量、point-in-time（每个再平衡日只用"截止当天"的K线重算选股），无前视、无AI泄漏。
   选股逻辑 analyze() 与实盘 screen-momentum.py 逐字一致；出场引擎与 backfill-portfolio-momh/momma.py 一致。
⚠️ 唯一偏差：universe 用"今天"的流动票名单 → 幸存者偏差（偏乐观）。MOM-H/MOM-MA 是同一批票，
   故"两套出场哪个好"的相对比较稳健；"绝对跑不跑赢SPY"要打折看（要彻底治需 FMP 诚实池版）。

用法：FMP_API_KEY=... python scripts/backtest-momentum.py   （FMP 仅取 universe，2次调用；其余 yfinance 免费）
"""
import os, json, sys
from datetime import datetime
import urllib.request
import numpy as np

FMP_KEY = os.environ.get("FMP_API_KEY", "").strip()
PERIOD = os.environ.get("BT_PERIOD", "3y")
TOP_N = 10
REBALANCE_EVERY = 5
PER_POSITION_USD = 500
INIT = 2000
COMMISSION = 1.0
OUT = "data/backtest-momentum.json"

FALLBACK_UNIVERSE = ["AAPL","MSFT","NVDA","AMZN","GOOGL","META","AVGO","TSLA","JPM","V",
    "MU","AMD","COIN","LSCC","DDOG","NET","CRSP","UEC","DECK","RJF","PLTR","SMCI",
    "ANET","CRWD","NOW","PANW","SNOW","UBER","SHOP","ABNB","CELH","VRT","ZS","MDB"]


# ============ 选股逻辑：与 screen-momentum.py 逐字一致 ============
def sma(arr, n):
    if len(arr) < n: return None
    return float(np.mean(arr[-n:]))


def analyze(close, high, low, vol, spy_ret_6m):
    if len(close) < 220:
        return None
    c = close[-1]
    ma50, ma150, ma200 = sma(close, 50), sma(close, 150), sma(close, 200)
    ma10, ma20 = sma(close, 10), sma(close, 20)
    if None in (ma50, ma150, ma200, ma10, ma20):
        return None
    ma200_1mo_ago = sma(close[:-22], 200)
    hi_52 = float(np.max(close[-252:])); lo_52 = float(np.min(close[-252:]))
    tt = [
        c > ma150 and c > ma200,
        ma150 > ma200,
        ma200_1mo_ago is not None and ma200 > ma200_1mo_ago,
        ma50 > ma150 > ma200,
        c > ma50,
        c >= 1.30 * lo_52,
        c >= 0.75 * hi_52,
    ]
    if not all(tt):
        return None
    ret_6m = c / close[-126] - 1 if len(close) >= 126 else 0.0
    rs = ret_6m - spy_ret_6m
    ma_band = max(ma10, ma20)
    dist_to_ma = (c - ma_band) / ma_band
    edge_pullback = float(np.clip(1 - dist_to_ma / 0.12, 0, 1))
    v5, v50 = sma(vol, 5), sma(vol, 50)
    vol_ratio = (v5 / v50) if (v5 and v50 and v50 > 0) else 1.0
    edge_volcontract = float(np.clip(1 - (vol_ratio - 0.6) / 0.8, 0, 1))
    near_high = (c - hi_52) / hi_52
    edge_nearhigh = float(np.clip(1 + near_high / 0.25, 0, 1))
    return {"price": round(c, 2), "rs": rs, "edge_pullback": edge_pullback,
            "edge_volcontract": edge_volcontract, "edge_nearhigh": edge_nearhigh}


def screen_asof(tickers, data, spy_ret_6m):
    """对一组票在某截止点(各自序列已截断)做选股,返回 top_n ticker 列表(与实盘同口径打分)。"""
    rows = []
    for tk, sl in data.items():
        r = analyze(sl["C"], sl["H"], sl["L"], sl["V"], spy_ret_6m)
        if r:
            rows.append({"ticker": tk, **r})
    if not rows:
        return []
    rs_sorted = sorted(rows, key=lambda r: -r["rs"])
    n = len(rs_sorted)
    for i, r in enumerate(rs_sorted):
        r["rs_rank"] = 1 - i / (n - 1) if n > 1 else 0.5
    for r in rows:
        r["score"] = (0.40*r["rs_rank"] + 0.25*r["edge_pullback"]
                      + 0.15*r["edge_volcontract"] + 0.20*r["edge_nearhigh"])
    rows.sort(key=lambda r: -r["score"])
    return [r["ticker"] for r in rows[:TOP_N]]


# ============ universe ============
def get_universe():
    if not FMP_KEY:
        print(f"[universe] 无 FMP_KEY,用内置 {len(FALLBACK_UNIVERSE)} 只"); return FALLBACK_UNIVERSE
    out = []
    for exch in ("NASDAQ", "NYSE"):
        url = (f"https://financialmodelingprep.com/stable/company-screener?marketCapMoreThan=3000000000"
               f"&exchange={exch}&isActivelyTrading=true&isFund=false&isEtf=false&limit=250&apikey={FMP_KEY}")
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                d = json.loads(r.read())
            for x in (d if isinstance(d, list) else []):
                sym = (x.get("symbol") or "").strip()
                if sym and sym.isalpha() and len(sym) <= 5:
                    out.append(sym)
        except Exception as e:
            print(f"  [fmp] {exch} 失败: {str(e)[:60]}")
    syms = sorted(set(out))
    if len(syms) < 50:
        print(f"[universe] FMP 太少({len(syms)}),用内置"); return FALLBACK_UNIVERSE
    print(f"[universe] FMP 流动中大盘 {len(syms)} 只"); return syms


# ============ 出场引擎（与 backfill-portfolio-momh/momma 一致） ============
def simulate(exit_rule, signals_by_date, ohlc, posmap, cal, slip=0.0):
    """slip = 单边滑点(小数,如0.004=0.4%)。多头:进场买在更高价、出场卖在更低价。"""
    held, closed = {}, []
    comm = 0.0

    def ma_at(tk, p, n):
        C = ohlc[tk]["C"]
        if p < n - 1: return None
        return float(np.mean(C[p-n+1:p+1]))

    def open_pos(tk, date):
        nonlocal comm
        p = posmap.get(tk, {}).get(date)
        if p is None: return
        entry = round(float(ohlc[tk]["C"][p]), 2)
        if entry <= 0: return
        shares = round(PER_POSITION_USD / entry, 4)
        d = {"ticker": tk, "signal_date": date, "entry_price": entry,
             "entry_fill": entry * (1 + slip), "shares": shares, "pos": p}
        if exit_rule == "H":
            d["take_profit"] = round(entry*1.15, 2); d["stop_loss"] = round(entry*0.98, 2)
        else:
            d["stop_loss"] = round(entry*0.92, 2)
        held[tk] = d; comm += COMMISSION

    def close_pos(tk, date, price, reason):
        nonlocal comm
        pos = held.pop(tk); comm += COMMISSION
        exit_fill = price * (1 - slip)           # 卖在更低价
        move = exit_fill - pos["entry_fill"]     # 进出都含滑点
        closed.append({"ticker": tk, "signal_date": pos["signal_date"], "entry_price": pos["entry_price"],
                       "shares": pos["shares"], "close_date": date, "close_price": round(price, 2),
                       "close_reason": reason,
                       "final_pnl_pct": round(move/pos["entry_fill"]*100, 2),
                       "realized_pnl_usd": round(pos["shares"]*move - 2*COMMISSION, 2)})

    last_rebal = -999
    for i, date in enumerate(cal):
        for tk in list(held.keys()):
            p = posmap.get(tk, {}).get(date)
            if p is None: continue
            pos = held[tk]
            hi, lo, cl = ohlc[tk]["H"][p], ohlc[tk]["L"][p], ohlc[tk]["C"][p]
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
            for tk in signals_by_date[date]:
                if tk not in held: open_pos(tk, date)
            last_rebal = i

    # 收尾：未平仓按最后一日收盘估浮盈(出场估值也含滑点)
    unreal = 0.0
    for tk, pos in held.items():
        p = posmap.get(tk, {}).get(cal[-1])
        cur = float(ohlc[tk]["C"][p]) if p is not None else pos["entry_price"]
        unreal += pos["shares"] * (cur * (1 - slip) - pos["entry_fill"])
    return closed, round(unreal, 2), round(comm, 2), len(held)


def stats_block(name, closed, unreal, comm, n_open, spy_ret_pct):
    realized = sum(c["realized_pnl_usd"] for c in closed)
    wins = [c for c in closed if c["realized_pnl_usd"] > 0]
    losses = [c for c in closed if c["realized_pnl_usd"] <= 0]
    gross_win = sum(c["realized_pnl_usd"] for c in wins)
    gross_loss = abs(sum(c["realized_pnl_usd"] for c in losses))
    pf = round(gross_win / gross_loss, 2) if gross_loss > 0 else float("inf")
    total = realized + unreal
    ret_pct = total / INIT * 100
    # 去掉最赚的1/2笔后还剩多少(毕业关③)
    srt = sorted(closed, key=lambda c: -c["realized_pnl_usd"])
    drop1 = realized - (srt[0]["realized_pnl_usd"] if srt else 0)
    drop2 = realized - sum(c["realized_pnl_usd"] for c in srt[:2])
    return {
        "name": name, "trades": len(closed), "open_now": n_open,
        "win_rate": round(len(wins)/len(closed)*100, 1) if closed else 0,
        "realized_usd": round(realized, 2), "unrealized_usd": unreal,
        "total_pnl_usd": round(total, 2), "return_pct": round(ret_pct, 1),
        "profit_factor": pf, "commission_usd": comm,
        "avg_win_usd": round(gross_win/len(wins), 2) if wins else 0,
        "avg_loss_usd": round(-gross_loss/len(losses), 2) if losses else 0,
        "realized_drop_top1": round(drop1, 2), "realized_drop_top2": round(drop2, 2),
        "vs_spy_pp": round(ret_pct - spy_ret_pct, 1),
    }


def main():
    import yfinance as yf
    universe = get_universe()
    print(f"[dl] 下载 {len(universe)} 票 + SPY 的 {PERIOD} 日线 ...")
    raw = yf.download(universe + ["SPY"], period=PERIOD, interval="1d",
                      progress=False, group_by="ticker", threads=True)

    # SPY 日历 + 收盘
    spy = raw["SPY"][["Close"]].dropna()
    spy_idx = [t.strftime("%Y-%m-%d") for t in spy.index]
    spy_close = spy["Close"].values
    spy_pos = {d: i for i, d in enumerate(spy_idx)}

    ohlc, posmap, series = {}, {}, {}
    for tk in universe:
        try:
            x = raw[tk][["High", "Low", "Close", "Volume"]].dropna()
            if len(x) < 240:
                continue
            idx = [t.strftime("%Y-%m-%d") for t in x.index]
            ohlc[tk] = {"H": x["High"].values, "L": x["Low"].values,
                        "C": x["Close"].values, "idx": idx}
            posmap[tk] = {d: i for i, d in enumerate(idx)}
            series[tk] = ohlc[tk]
        except Exception:
            pass
    print(f"[dl] {len(ohlc)} 票数据可用")
    if len(ohlc) < 10:
        print("数据太少,退出"); sys.exit(1)

    cal = spy_idx  # 主交易日历用 SPY
    start_i = 252  # 留足回看
    rebal_dates = [cal[i] for i in range(start_i, len(cal), REBALANCE_EVERY)]
    bt_cal = cal[start_i:]
    print(f"[bt] 回测窗口 {bt_cal[0]} → {bt_cal[-1]}  ({len(bt_cal)}个交易日, {len(rebal_dates)}个再平衡点)")

    # 每个再平衡日做 point-in-time 选股
    signals_by_date = {}
    empty_boards = 0
    for d in rebal_dates:
        q = spy_pos.get(d)
        if q is None or q < 126:
            continue
        spy_ret_6m = float(spy_close[q] / spy_close[q-126] - 1)
        # 各票截断到 <= d
        data_asof = {}
        for tk, s in series.items():
            p = posmap[tk].get(d)
            if p is None or p < 220:
                continue
            data_asof[tk] = {"C": s["C"][:p+1], "H": s["H"][:p+1],
                             "L": s["L"][:p+1], "V": raw[tk]["Volume"].dropna().values[:p+1]}
        picks = screen_asof(universe, data_asof, spy_ret_6m)
        if picks:
            signals_by_date[d] = set(picks)
        else:
            empty_boards += 1
    print(f"[bt] {len(signals_by_date)}个再平衡日出榜 / {empty_boards}个空榜(趋势模板闸门挡住=大盘弱)")

    # SPY 基准（同窗口买入持有）
    spy_ret_pct = float(spy_close[-1] / spy_close[start_i] - 1) * 100

    # 滑点敏感度扫描：每笔单边滑点 0 / 0.3% / 0.4% / 0.5%
    scenarios = [0.0, 0.003, 0.004, 0.005]
    sweep = {"H": {}, "MA": {}}
    detail = {}
    for slip in scenarios:
        for rule, name in (("H", "MOM-H (TP15/SL2/2日)"), ("MA", "MOM-MA (20MA移动止盈)")):
            closed, unreal, comm, n_open = simulate(rule, signals_by_date, ohlc, posmap, bt_cal, slip=slip)
            s = stats_block(name, closed, unreal, comm, n_open, spy_ret_pct)
            sweep[rule][f"{slip*100:.1f}%"] = s["return_pct"]
            if abs(slip - 0.004) < 1e-9:        # 0.4% 作为中心情形存详情
                detail[rule] = s

    result = {"generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
              "period": PERIOD, "window": [bt_cal[0], bt_cal[-1]],
              "universe_size": len(ohlc), "rebalance_points": len(rebal_dates),
              "boards_with_picks": len(signals_by_date), "empty_boards": empty_boards,
              "spy_return_pct": round(spy_ret_pct, 1),
              "slippage_sweep_return_pct": sweep,
              "detail_at_0.4pct_slip": detail,
              "caveat": "universe=今日流动票,有幸存者偏差(偏乐观);出场相对比较稳健,绝对edge打折看"}
    json.dump(result, open(OUT, "w"), ensure_ascii=False, indent=2)

    def show(s):
        print(f"\n  ● {s['name']}  [含0.4%/笔滑点]")
        print(f"    交易 {s['trades']}笔  胜率 {s['win_rate']}%  盈亏比PF {s['profit_factor']}  (持仓中{s['open_now']})")
        print(f"    总盈亏 ${s['total_pnl_usd']:+.0f} ({s['return_pct']:+.1f}%)  已实现${s['realized_usd']:+.0f} 浮盈${s['unrealized_usd']:+.0f}  佣金${s['commission_usd']:.0f}")
        print(f"    均盈${s['avg_win_usd']:+.0f} / 均亏${s['avg_loss_usd']:+.0f}")
        print(f"    去掉最赚2笔后已实现 ${s['realized_drop_top2']:+.0f}  ← 毕业关③")
        print(f"    vs SPY同期: {s['vs_spy_pp']:+.1f} 个百分点")

    print(f"\n{'='*62}\n  MOM 历史回测 ({PERIOD}, {bt_cal[0]}→{bt_cal[-1]})\n{'='*62}")
    print(f"  universe {len(ohlc)}只 · SPY同期 {spy_ret_pct:+.1f}%")
    print(f"\n  📉 滑点敏感度（总收益%，每笔单边滑点）:")
    print(f"    {'滑点/笔':<10}{'0%':>10}{'0.3%':>10}{'0.4%':>10}{'0.5%':>10}")
    print(f"    {'MOM-H':<10}" + "".join(f"{sweep['H'][k]:>+9.1f}%" for k in ['0.0%','0.3%','0.4%','0.5%']))
    print(f"    {'MOM-MA':<10}" + "".join(f"{sweep['MA'][k]:>+9.1f}%" for k in ['0.0%','0.3%','0.4%','0.5%']))
    show(detail["H"]); show(detail["MA"])
    print(f"\n  ⚠️ {result['caveat']}")
    print(f"  详情已存 {OUT}")


if __name__ == "__main__":
    main()
