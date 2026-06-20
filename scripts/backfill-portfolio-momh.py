"""
Plan MOM-H —— 动量/趋势选股(screen-momentum) + Plan H 出场(TP+15%/SL-2%/最大2交易日)。
与现有 H/H-DS/H-广池 控制变量对照:**只差信号来源**(这条腿=Minervini+J Law 客观动量筛,无AI)。

读每日归档 data/momentum-history/{date}.json(当时价量快照,前向无前视)。
机制:周再平衡(REBALANCE_EVERY 交易日)按最新榜单开新仓,持仓按 Plan H 规则每日触发出场。
long-only(动量做多领导股)。$500/仓,与现实盘 H 系列同口径可比。
"""
import os, json, glob
from datetime import datetime
import yfinance as yf
from portfolio_compound import compound_portfolio   # frac20 复利回填(与决策视图排名同口径)

HIST_DIR = "data/momentum-history"
PORTFOLIO_PATH = "data/portfolio_momh.json"
JS_PATH = "dashboard/portfolio-momh.js"
JS_VAR = "PORTFOLIO_MOMH"
REBALANCE_EVERY = 5
TP_PCT, SL_PCT = 15.0, 2.0
MAX_HOLD = 2                 # 交易日
PER_POSITION_USD = 500
INIT = 2000
COMMISSION = 1.0            # IBKR 每次成交 min $1
os.makedirs("data", exist_ok=True)


def load_archives():
    files = sorted(glob.glob(os.path.join(HIST_DIR, "*.json")))
    archives = {}
    for f in files:
        d = json.load(f if False else open(f))
        archives[d["date"]] = {"buy": {x["ticker"] for x in d.get("buy", [])},
                               "score": {x["ticker"]: x.get("score", 0) for x in d.get("buy", [])}}
    return archives


def main():
    archives = load_archives()
    if not archives:
        print("[mom-h] 无动量归档,先跑 screen-momentum.py"); return
    arch_dates = sorted(archives)
    all_tk = set()
    for a in archives.values(): all_tk |= a["buy"]
    print(f"[mom-h] 归档 {len(archives)} 天 ({arch_dates[0]}→{arch_dates[-1]}) · {len(all_tk)} 只")
    if not all_tk:
        print("[mom-h] 归档全是空榜,无可交易"); _write_empty(); return

    raw = yf.download(list(all_tk), period="11mo", interval="1d", progress=False, group_by="ticker", threads=True)
    ohlc, posmap = {}, {}
    for tk in all_tk:
        try:
            x = raw[tk][["High", "Low", "Close"]].dropna()
            if len(x) > 60:
                idx = [t.strftime("%Y-%m-%d") for t in x.index]
                ohlc[tk] = {"H": x["High"].values, "L": x["Low"].values, "C": x["Close"].values, "idx": idx}
                posmap[tk] = {dt: i for i, dt in enumerate(idx)}
        except Exception:
            pass
    if not ohlc:
        print("[mom-h] 无价格数据"); _write_empty(); return

    cal_all = sorted(max(ohlc.values(), key=lambda o: len(o["idx"]))["idx"])
    arch_on = {}
    for ad in arch_dates:
        td = max((d for d in cal_all if d <= ad), default=None)
        if td: arch_on[td] = archives[ad]
    cal = [d for d in cal_all if d >= min(arch_on.keys())]
    today = datetime.now().strftime("%Y-%m-%d")

    held, closed = {}, []
    commission_total = 0.0

    def open_pos(tk, date, score):
        nonlocal commission_total
        p = posmap.get(tk, {}).get(date)
        if p is None: return
        entry = round(float(ohlc[tk]["C"][p]), 2)
        if entry <= 0: return
        shares = round(PER_POSITION_USD / entry, 4)  # 小数股:$500/仓不受股价高低限制,高价领导股也能纳入
        held[tk] = {"ticker": tk, "action": "BUY", "signal_date": date, "entry_price": entry,
                    "shares": shares, "take_profit": round(entry*(1+TP_PCT/100), 2),
                    "stop_loss": round(entry*(1-SL_PCT/100), 2), "pos": p, "score": score}
        commission_total += COMMISSION

    def close_pos(tk, date, price, reason):
        nonlocal commission_total
        pos = held.pop(tk)
        move = price - pos["entry_price"]
        commission_total += COMMISSION
        closed.append({k: pos[k] for k in pos if k != "pos"} | {
            "close_date": date, "close_price": round(price, 2), "close_reason": reason,
            "final_pnl_pct": round(move/pos["entry_price"]*100, 2),
            "realized_pnl_usd": round(pos["shares"]*move - 2*COMMISSION, 2), "commission_total": 2*COMMISSION})

    last_rebal = -999
    for i, date in enumerate(cal):
        # 1. Plan H 出场:每日 TP/SL/最大持有
        for tk in list(held.keys()):
            p = posmap.get(tk, {}).get(date)
            if p is None: continue
            pos = held[tk]
            hi, lo, cl = ohlc[tk]["H"][p], ohlc[tk]["L"][p], ohlc[tk]["C"][p]
            if lo <= pos["stop_loss"]: close_pos(tk, date, pos["stop_loss"], "stop_loss"); continue
            if hi >= pos["take_profit"]: close_pos(tk, date, pos["take_profit"], "take_profit"); continue
            if (p - pos["pos"]) >= MAX_HOLD: close_pos(tk, date, float(cl), "max_hold")
        # 2. 周再平衡:开当日榜单里还没持有的票(long-only,不强平,持仓靠H规则自然了结)
        if date in arch_on and (i - last_rebal) >= REBALANCE_EVERY:
            a = arch_on[date]
            for tk in a["buy"]:
                if tk not in held: open_pos(tk, date, a["score"].get(tk, 0))
            last_rebal = i

    _finalize(held, closed, commission_total, posmap, ohlc, cal, today)


def _finalize(held, closed, commission_total, posmap, ohlc, cal, today):
    opens = []
    for tk, pos in held.items():
        p = posmap.get(tk, {}).get(cal[-1])
        cur = float(ohlc[tk]["C"][p]) if p is not None else pos["entry_price"]
        d = {k: pos[k] for k in pos if k != "pos"}
        d["_unreal"] = round(pos["shares"] * (cur - pos["entry_price"]), 2)
        d["actual_position_usd"] = round(pos["shares"] * pos["entry_price"], 2)
        opens.append(d)
    # frac20 复利回填(取代固定$500,与决策视图排名同口径)
    def _open_pct(o):
        base = o.get("actual_position_usd") or 0
        return (o.get("_unreal", 0) / base * 100) if base else 0.0
    closed, opens, _pv, _real, unreal, skipped = compound_portfolio(closed, opens, _open_pct, INIT)
    for o in opens: o.pop("_unreal", None)
    wins = [c for c in closed if c["realized_pnl_usd"] > 0]
    total_realized = round(sum(c["realized_pnl_usd"] for c in closed), 2)
    comm = round((len(closed)*2 + len(opens)) * COMMISSION, 2)
    portfolio = {
        "capital_usd": INIT, "open_positions": opens, "closed_positions": closed,
        "_note": "MOM-H：动量/趋势选股(Minervini趋势模板+J Law M.E.T.A.,无AI) + Plan H出场(TP15/SL2/2日)。$500/仓(小数股),现金约束(最多4仓,$2000无杠杆),周再平衡,前向无前视。",
        "stats": {"total_trades": len(closed), "win_trades": len(wins),
                  "win_rate": round(len(wins)/len(closed)*100, 1) if closed else 0,
                  "total_realized_pnl_usd": total_realized, "open_unrealized_pnl_usd": round(unreal, 2),
                  "portfolio_value": round(INIT + total_realized + unreal, 2),
                  "total_commission_usd": comm, "skipped_no_cash": skipped, "updated_at": today}}
    json.dump(portfolio, open(PORTFOLIO_PATH, "w"), ensure_ascii=False, indent=2)
    with open(JS_PATH, "w", encoding="utf-8") as f:
        f.write("// Plan MOM-H — 动量/趋势选股(无AI) + Plan H出场(TP15/SL2/2日)\n")
        f.write(f"window.{JS_VAR} = {json.dumps(portfolio, ensure_ascii=False, indent=2)};\n")
    s = portfolio["stats"]
    print(f"💼 MOM-H: 已平{s['total_trades']} 胜率{s['win_rate']}% 持仓{len(opens)} | 已实现${s['total_realized_pnl_usd']:+.0f} 浮盈${s['open_unrealized_pnl_usd']:+.0f} 净值${s['portfolio_value']} 佣金${s['total_commission_usd']}")


def _write_empty():
    portfolio = {"capital_usd": INIT, "open_positions": [], "closed_positions": [],
                 "_note": "MOM-H：暂无可交易(动量归档为空或无价格)",
                 "stats": {"total_trades": 0, "win_trades": 0, "win_rate": 0, "total_realized_pnl_usd": 0,
                           "open_unrealized_pnl_usd": 0, "portfolio_value": INIT, "total_commission_usd": 0,
                           "updated_at": datetime.now().strftime("%Y-%m-%d")}}
    json.dump(portfolio, open(PORTFOLIO_PATH, "w"), ensure_ascii=False, indent=2)
    with open(JS_PATH, "w", encoding="utf-8") as f:
        f.write(f"window.{JS_VAR} = {json.dumps(portfolio, ensure_ascii=False, indent=2)};\n")


if __name__ == "__main__":
    main()
