"""
Plan B-quant 模拟盘（前向干净版）—— 多因子量化 + ATR定价 + 风险定额 + 每周再平衡。全程无 AI。

**读每日归档 data/multifactor-history/{date}.json**(选股器当时用当时基本面选的=点对点快照,无前视)。
模拟:持有组合,每周(REBALANCE_EVERY交易日)按最新归档再平衡(只交易变动),期间 ATR 止盈/止损每日触发。
价格用 yfinance(历史,算ATR+出场)。归档从今天起累积→B-quant 历史从今天起干净增长。
"""
import os, json, glob
from datetime import datetime
import yfinance as yf

HIST_DIR = "data/multifactor-history"
PORTFOLIO_PATH = "data/portfolio_bq.json"
REBALANCE_EVERY = 5
TP_K, SL_K = 4.0, 2.5
RISK_PER_TRADE = 40.0
MAX_HOLD = 15
COMMISSION = 1.0
INIT = 2000
os.makedirs("data", exist_ok=True)


def main():
    files = sorted(glob.glob(os.path.join(HIST_DIR, "*.json")))
    if not files:
        print("[bq] 无多因子归档,先跑 screen-multifactor.py"); return
    archives = {}
    for f in files:
        d = json.load(open(f))
        archives[d["date"]] = {
            "buy": {x["ticker"] for x in d.get("buy", [])},
            "sell": {x["ticker"] for x in d.get("sell", [])},
            "score": {x["ticker"]: x.get("score", 0) for x in d.get("buy", []) + d.get("sell", [])},
        }
    arch_dates = sorted(archives.keys())
    all_tk = set()
    for a in archives.values(): all_tk |= a["buy"] | a["sell"]
    print(f"[bq] 归档 {len(archives)} 天 ({arch_dates[0]}→{arch_dates[-1]}) · 涉及 {len(all_tk)} 只")

    raw = yf.download(list(all_tk), period="11mo", interval="1d", progress=False, group_by="ticker", threads=True)
    ohlc, posmap = {}, {}
    for tk in all_tk:
        try:
            x = raw[tk][["High", "Low", "Close"]].dropna()
            if len(x) > 150:
                idx = [t.strftime("%Y-%m-%d") for t in x.index]
                ohlc[tk] = {"H": x["High"].values, "L": x["Low"].values, "C": x["Close"].values, "idx": idx}
                posmap[tk] = {dt: i for i, dt in enumerate(idx)}
        except Exception:
            pass

    cal_all = sorted(max(ohlc.values(), key=lambda o: len(o["idx"]))["idx"])
    # 归档日期(=当天)可能晚于最新价格bar →映射到≤它的最近交易日上再平衡
    arch_on = {}
    for ad in arch_dates:
        td = max((d for d in cal_all if d <= ad), default=None)
        if td: arch_on[td] = archives[ad]
    if not arch_on:
        print("[bq] 归档日无对应价格交易日,退出"); return
    cal = [d for d in cal_all if d >= min(arch_on.keys())]
    today = datetime.now().strftime("%Y-%m-%d")

    def atr(tk, p):
        o = ohlc[tk]
        if p < 15: return None
        H, L, C = o["H"], o["L"], o["C"]
        return sum(max(H[j]-L[j], abs(H[j]-C[j-1]), abs(L[j]-C[j-1])) for j in range(p-13, p+1)) / 14

    held, closed = {}, []
    commission_total = 0.0

    def open_pos(tk, action, date, score):
        nonlocal commission_total
        p = posmap.get(tk, {}).get(date)
        if p is None: return
        a = atr(tk, p)
        if not a or a <= 0: return
        entry = round(float(ohlc[tk]["C"][p]), 2)
        held[tk] = {"ticker": tk, "action": action, "signal_date": date, "entry_price": entry,
                    "shares": round(RISK_PER_TRADE/(SL_K*a), 3), "atr": round(a, 2),
                    "take_profit": round(entry + TP_K*a if action == "BUY" else entry - TP_K*a, 2),
                    "stop_loss": round(entry - SL_K*a if action == "BUY" else entry + SL_K*a, 2),
                    "pos": p, "score": score}
        commission_total += COMMISSION

    def close_pos(tk, date, price, reason):
        nonlocal commission_total
        pos = held.pop(tk)
        move = (price - pos["entry_price"]) if pos["action"] == "BUY" else (pos["entry_price"] - price)
        commission_total += COMMISSION
        closed.append({**{k: pos[k] for k in pos if k != "pos"}, "close_date": date,
                       "close_price": round(price, 2), "close_reason": reason,
                       "final_pnl_pct": round(move/pos["entry_price"]*100, 2),
                       "realized_pnl_usd": round(pos["shares"]*move, 2), "commission_total": 2.0})

    last_rebal = -999
    for i, date in enumerate(cal):
        # 1. 每日 ATR 止盈止损 / 最大持有
        for tk in list(held.keys()):
            p = posmap.get(tk, {}).get(date)
            if p is None: continue
            hi, lo, cl = ohlc[tk]["H"][p], ohlc[tk]["L"][p], ohlc[tk]["C"][p]
            pos = held[tk]
            if pos["action"] == "BUY":
                if lo <= pos["stop_loss"]: close_pos(tk, date, pos["stop_loss"], "stop_loss"); continue
                if hi >= pos["take_profit"]: close_pos(tk, date, pos["take_profit"], "take_profit"); continue
            else:
                if hi >= pos["stop_loss"]: close_pos(tk, date, pos["stop_loss"], "stop_loss"); continue
                if lo <= pos["take_profit"]: close_pos(tk, date, pos["take_profit"], "take_profit"); continue
            if (p - held[tk]["pos"]) >= MAX_HOLD:
                close_pos(tk, date, float(cl), "max_hold")
        # 2. 再平衡:该交易日有归档 且 距上次≥REBALANCE_EVERY
        if date in arch_on and (i - last_rebal) >= REBALANCE_EVERY:
            a = arch_on[date]
            target = {tk: "BUY" for tk in a["buy"]}; target.update({tk: "SELL" for tk in a["sell"]})
            for tk in list(held.keys()):
                if target.get(tk) != held[tk]["action"]:
                    p = posmap.get(tk, {}).get(date)
                    if p is not None: close_pos(tk, date, float(ohlc[tk]["C"][p]), "rebalance")
            for tk, action in target.items():
                if tk not in held: open_pos(tk, action, date, a["score"].get(tk, 0))
            last_rebal = i

    opens, unreal = [], 0.0
    for tk, pos in held.items():
        p = posmap.get(tk, {}).get(cal[-1])
        cur = float(ohlc[tk]["C"][p]) if p is not None else pos["entry_price"]
        move = (cur - pos["entry_price"]) if pos["action"] == "BUY" else (pos["entry_price"] - cur)
        unreal += pos["shares"] * move
        opens.append({k: pos[k] for k in pos if k != "pos"})

    wins = [c for c in closed if c["realized_pnl_usd"] > 0]
    total_realized = round(sum(c["realized_pnl_usd"] for c in closed), 2)   # 佣金单列,不预扣进已实现(0平仓=0)
    portfolio = {
        "capital_usd": INIT, "open_positions": opens, "closed_positions": closed,
        "_note": "B-quant：多因子量化+ATR定价(TP4/SL2.5×ATR)+风险定额(2%)+每周再平衡。读点对点归档,前向无前视。全程无AI。",
        "stats": {
            "total_trades": len(closed), "win_trades": len(wins),
            "win_rate": round(len(wins)/len(closed)*100, 1) if closed else 0,
            "total_realized_pnl_usd": total_realized, "open_unrealized_pnl_usd": round(unreal, 2),
            "portfolio_value": round(INIT + total_realized + unreal, 2),
            "total_commission_usd": round(commission_total, 2), "updated_at": today,
        },
    }
    json.dump(portfolio, open(PORTFOLIO_PATH, "w"), ensure_ascii=False, indent=2)
    with open("dashboard/portfolio-bq.js", "w", encoding="utf-8") as f:
        f.write("// Plan B-quant — 多因子量化+ATR定价+风险定额+每周再平衡(前向无前视,无AI)\n")
        f.write(f"window.PORTFOLIO_BQ = {json.dumps(portfolio, ensure_ascii=False, indent=2)};\n")
    s = portfolio["stats"]
    print(f"💼 B-quant: 已平{s['total_trades']} 胜率{s['win_rate']}% 持仓{len(opens)} | 已实现${s['total_realized_pnl_usd']:+.0f} 浮盈${s['open_unrealized_pnl_usd']:+.0f} 净值${s['portfolio_value']} 佣金${s['total_commission_usd']}")


if __name__ == "__main__":
    main()
