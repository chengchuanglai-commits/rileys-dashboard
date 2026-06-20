"""
Plan MOM-MA —— 动量/趋势选股(screen-momentum) + J Law 式 10/20MA 移动止盈出场。
与 MOM-H 控制变量对照:**完全相同的进场信号,只差出场规则**——
  MOM-H = 紧止损快出(TP15/SL2/2日),  MOM-MA = 趋势跟随(收盘跌破20MA才走,让利润奔跑)。

出场("趁弱卖",J Law):持仓后,某日**收盘价跌破 20MA** 即了结;不设固定止盈,让赢家跑。
另加初始硬止损 -8%(风控优先,防进场即崩;J Law 用利润软垫但仍止损)。
long-only。$500/仓,周再平衡补新领导股(已持有的不动,靠均线规则自然了结)。
读 data/momentum-history/{date}.json,前向无前视。
"""
import os, json, glob
from datetime import datetime
import numpy as np
import yfinance as yf
from portfolio_compound import compound_portfolio   # frac20 复利回填(与决策视图排名同口径)

HIST_DIR = "data/momentum-history"
PORTFOLIO_PATH = "data/portfolio_momma.json"
JS_PATH = "dashboard/portfolio-momma.js"
JS_VAR = "PORTFOLIO_MOMMA"
REBALANCE_EVERY = 5
MA_EXIT = 20                 # 收盘跌破此均线则出场(J Law 趁弱卖)
INIT_STOP_PCT = 8.0          # 初始硬止损(风控,防进场即崩)
MAX_HOLD = 60                # 安全上限(交易日),正常靠均线了结,极少触发
PER_POSITION_USD = 500
INIT = 2000
COMMISSION = 1.0
os.makedirs("data", exist_ok=True)


def load_archives():
    files = sorted(glob.glob(os.path.join(HIST_DIR, "*.json")))
    archives = {}
    for f in files:
        d = json.load(open(f))
        archives[d["date"]] = {"buy": {x["ticker"] for x in d.get("buy", [])},
                               "score": {x["ticker"]: x.get("score", 0) for x in d.get("buy", [])}}
    return archives


def main():
    archives = load_archives()
    if not archives:
        print("[mom-ma] 无动量归档,先跑 screen-momentum.py"); return
    arch_dates = sorted(archives)
    all_tk = set()
    for a in archives.values(): all_tk |= a["buy"]
    print(f"[mom-ma] 归档 {len(archives)} 天 ({arch_dates[0]}→{arch_dates[-1]}) · {len(all_tk)} 只")
    if not all_tk:
        print("[mom-ma] 归档全是空榜"); _write_empty(); return

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
        print("[mom-ma] 无价格数据"); _write_empty(); return

    cal_all = sorted(max(ohlc.values(), key=lambda o: len(o["idx"]))["idx"])
    arch_on = {}
    for ad in arch_dates:
        td = max((d for d in cal_all if d <= ad), default=None)
        if td: arch_on[td] = archives[ad]
    cal = [d for d in cal_all if d >= min(arch_on.keys())]
    today = datetime.now().strftime("%Y-%m-%d")

    def ma_at(tk, p, n):
        C = ohlc[tk]["C"]
        if p < n - 1: return None
        return float(np.mean(C[p-n+1:p+1]))

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
                    "shares": shares, "stop_loss": round(entry*(1-INIT_STOP_PCT/100), 2),
                    "pos": p, "score": score}
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
        # 1. 出场:初始硬止损(盘中) → 收盘跌破20MA(趁弱卖) → 安全上限
        for tk in list(held.keys()):
            p = posmap.get(tk, {}).get(date)
            if p is None: continue
            pos = held[tk]
            lo, cl = ohlc[tk]["L"][p], ohlc[tk]["C"][p]
            if lo <= pos["stop_loss"]: close_pos(tk, date, pos["stop_loss"], "init_stop"); continue
            ma = ma_at(tk, p, MA_EXIT)
            if ma is not None and cl < ma: close_pos(tk, date, float(cl), "ma_break"); continue
            if (p - pos["pos"]) >= MAX_HOLD: close_pos(tk, date, float(cl), "max_hold")
        # 2. 周再平衡:补榜单新领导股(已持有的让均线规则管,不强平)
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
        "_note": "MOM-MA：动量/趋势选股(同MOM-H) + J Law 10/20MA移动止盈(收盘破20MA才走,让赢家跑)+初始-8%硬止损。$500/仓(小数股),现金约束(最多4仓,$2000无杠杆),周再平衡,前向无前视。",
        "stats": {"total_trades": len(closed), "win_trades": len(wins),
                  "win_rate": round(len(wins)/len(closed)*100, 1) if closed else 0,
                  "total_realized_pnl_usd": total_realized, "open_unrealized_pnl_usd": round(unreal, 2),
                  "portfolio_value": round(INIT + total_realized + unreal, 2),
                  "total_commission_usd": comm, "skipped_no_cash": skipped, "updated_at": today}}
    json.dump(portfolio, open(PORTFOLIO_PATH, "w"), ensure_ascii=False, indent=2)
    with open(JS_PATH, "w", encoding="utf-8") as f:
        f.write("// Plan MOM-MA — 动量/趋势选股(无AI) + J Law 10/20MA移动止盈\n")
        f.write(f"window.{JS_VAR} = {json.dumps(portfolio, ensure_ascii=False, indent=2)};\n")
    s = portfolio["stats"]
    print(f"💼 MOM-MA: 已平{s['total_trades']} 胜率{s['win_rate']}% 持仓{len(opens)} | 已实现${s['total_realized_pnl_usd']:+.0f} 浮盈${s['open_unrealized_pnl_usd']:+.0f} 净值${s['portfolio_value']} 佣金${s['total_commission_usd']}")


def _write_empty():
    portfolio = {"capital_usd": INIT, "open_positions": [], "closed_positions": [],
                 "_note": "MOM-MA：暂无可交易",
                 "stats": {"total_trades": 0, "win_trades": 0, "win_rate": 0, "total_realized_pnl_usd": 0,
                           "open_unrealized_pnl_usd": 0, "portfolio_value": INIT, "total_commission_usd": 0,
                           "updated_at": datetime.now().strftime("%Y-%m-%d")}}
    json.dump(portfolio, open(PORTFOLIO_PATH, "w"), ensure_ascii=False, indent=2)
    with open(JS_PATH, "w", encoding="utf-8") as f:
        f.write(f"window.{JS_VAR} = {json.dumps(portfolio, ensure_ascii=False, indent=2)};\n")


if __name__ == "__main__":
    main()
