"""
Plan B-AI 模拟盘 —— 多因子选股 + **DeepSeek 决定** + ATR定价 + 风险定额 + 每周再平衡。

与 B-quant 同候选、同定价、同再平衡,**唯一区别:谁做决定**——
  B-quant: 量化规则直接取榜首/垫底  ;  B-AI: DeepSeek 在这批候选里挑 BUY/SELL(HOLD 不开)。
→ 干净隔离"AI 大脑加不加分"。

读 data/multifactor-ai-history/{date}.json(DeepSeek对多因子候选的判断,点对点无前视)。
"""
import os, json, glob
from datetime import datetime
import yfinance as yf

HIST_DIR = "data/multifactor-ai-history"
PORTFOLIO_PATH = "data/portfolio_bai.json"
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
        print("[bai] 无 DeepSeek 多因子归档(等首跑),写空盘占位"); _write_empty(); return
    archives = {}
    for f in files:
        d = json.load(open(f))
        buy = {s["ticker"] for s in d.get("signals", []) if s.get("action") == "BUY"}
        sell = {s["ticker"] for s in d.get("signals", []) if s.get("action") == "SELL"}
        if buy or sell:
            archives[d["date"]] = {"buy": buy, "sell": sell}
    if not archives:
        print("[bai] 归档里无可操作信号"); _write_empty(); return
    arch_dates = sorted(archives.keys())
    all_tk = set()
    for a in archives.values(): all_tk |= a["buy"] | a["sell"]
    print(f"[bai] 归档 {len(archives)} 天 · {len(all_tk)} 只")

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
    if not ohlc: print("[bai] 无价格,退出"); _write_empty(); return

    cal_all = sorted(max(ohlc.values(), key=lambda o: len(o["idx"]))["idx"])
    arch_on = {}
    for ad in arch_dates:
        td = max((d for d in cal_all if d <= ad), default=None)
        if td: arch_on[td] = archives[ad]
    if not arch_on: print("[bai] 归档日无对应交易日"); _write_empty(); return
    cal = [d for d in cal_all if d >= min(arch_on.keys())]
    today = datetime.now().strftime("%Y-%m-%d")

    def atr(tk, p):
        o = ohlc[tk]
        if p < 15: return None
        H, L, C = o["H"], o["L"], o["C"]
        return sum(max(H[j]-L[j], abs(H[j]-C[j-1]), abs(L[j]-C[j-1])) for j in range(p-13, p+1)) / 14

    held, closed = {}, []
    commission_total = 0.0

    def open_pos(tk, action, date):
        nonlocal commission_total
        p = posmap.get(tk, {}).get(date)
        if p is None: return
        a = atr(tk, p)
        if not a or a <= 0: return
        entry = round(float(ohlc[tk]["C"][p]), 2)
        held[tk] = {"ticker": tk, "action": action, "signal_date": date, "entry_price": entry,
                    "shares": round(RISK_PER_TRADE/(SL_K*a), 3), "atr": round(a, 2),
                    "take_profit": round(entry + TP_K*a if action == "BUY" else entry - TP_K*a, 2),
                    "stop_loss": round(entry - SL_K*a if action == "BUY" else entry + SL_K*a, 2), "pos": p}
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
        if date in arch_on and (i - last_rebal) >= REBALANCE_EVERY:
            a = arch_on[date]
            target = {tk: "BUY" for tk in a["buy"]}; target.update({tk: "SELL" for tk in a["sell"]})
            for tk in list(held.keys()):
                if target.get(tk) != held[tk]["action"]:
                    p = posmap.get(tk, {}).get(date)
                    if p is not None: close_pos(tk, date, float(ohlc[tk]["C"][p]), "rebalance")
            for tk, action in target.items():
                if tk not in held: open_pos(tk, action, date)
            last_rebal = i

    opens, unreal = [], 0.0
    for tk, pos in held.items():
        p = posmap.get(tk, {}).get(cal[-1])
        cur = float(ohlc[tk]["C"][p]) if p is not None else pos["entry_price"]
        move = (cur - pos["entry_price"]) if pos["action"] == "BUY" else (pos["entry_price"] - cur)
        unreal += pos["shares"] * move
        opens.append({k: pos[k] for k in pos if k != "pos"})

    _write(opens, closed, commission_total, unreal, today)


def _stats(opens, closed, commission_total, unreal, today):
    wins = [c for c in closed if c["realized_pnl_usd"] > 0]
    tr = round(sum(c["realized_pnl_usd"] for c in closed) - commission_total, 2)
    return {"total_trades": len(closed), "win_trades": len(wins),
            "win_rate": round(len(wins)/len(closed)*100, 1) if closed else 0,
            "total_realized_pnl_usd": tr, "open_unrealized_pnl_usd": round(unreal, 2),
            "portfolio_value": round(INIT + tr + unreal, 2),
            "total_commission_usd": round(commission_total, 2), "updated_at": today}


def _write(opens, closed, commission_total, unreal, today):
    p = {"capital_usd": INIT, "open_positions": opens, "closed_positions": closed,
         "_note": "B-AI：多因子选股 + DeepSeek决定 + ATR定价 + 风险定额 + 每周再平衡。与B-quant同候选,只差谁做决定。",
         "stats": _stats(opens, closed, commission_total, unreal, today)}
    json.dump(p, open(PORTFOLIO_PATH, "w"), ensure_ascii=False, indent=2)
    with open("dashboard/portfolio-bai.js", "w", encoding="utf-8") as f:
        f.write("// Plan B-AI — 多因子选股+DeepSeek决定+ATR定价+风险定额+周再平衡\n")
        f.write(f"window.PORTFOLIO_BAI = {json.dumps(p, ensure_ascii=False, indent=2)};\n")
    s = p["stats"]
    print(f"💼 B-AI: 已平{s['total_trades']} 胜率{s['win_rate']}% 持仓{len(opens)} | 已实现${s['total_realized_pnl_usd']:+.0f} 浮盈${s['open_unrealized_pnl_usd']:+.0f} 净值${s['portfolio_value']}")


def _write_empty():
    _write([], [], 0.0, 0.0, datetime.now().strftime("%Y-%m-%d"))


if __name__ == "__main__":
    main()
