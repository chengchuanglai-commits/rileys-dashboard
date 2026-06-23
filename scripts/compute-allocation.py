# scripts/compute-allocation.py
"""信念分配引擎:每腿 conviction(sample×alpha×robustness) → 主动30-70%滑动 → 各腿按信念权重。"""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.dirname(os.path.abspath(sys.argv[0])))
from portfolio_compound import compound_frac20

N_FULL = 40
ALPHA_TARGET = 0.10
ACTIVE_FLOOR = 0.50   # 2026-06-23 Riley 由40→50:主动地板50%/指数50%(多10%进抗跌的动量腿)
ACTIVE_CEILING = 0.70
MOMMA_PRIOR = 0.10

def _clip(x, lo, hi):
    return max(lo, min(hi, x))

def conviction_score(n, alpha, robust_ok, n_full=N_FULL, alpha_target=ALPHA_TARGET):
    if not robust_ok or alpha <= 0:
        return 0.0
    sample = min(n / n_full, 1.0)
    edge = _clip(alpha / alpha_target, 0.0, 1.0)
    return round(sample * edge * 1.0, 4)

def active_fraction(max_conviction, floor=ACTIVE_FLOOR, ceiling=ACTIVE_CEILING):
    return round(floor + (ceiling - floor) * _clip(max_conviction, 0.0, 1.0), 4)

def active_weights(convictions, priors):
    raw = {k: convictions.get(k, 0.0) + priors.get(k, 0.0) for k in convictions}
    s = sum(raw.values())
    if s <= 0:
        return {k: 0.0 for k in convictions}
    return {k: round(v / s, 4) for k, v in raw.items()}

INIT = 2000.0

def _closed_trades(port):
    out = []
    for p in port.get("closed_positions", []):
        pct = p.get("final_pnl_pct")
        if pct is None:
            rp, cost = p.get("realized_pnl_usd"), (p.get("actual_position_usd") or p.get("allocated_usd"))
            if rp is not None and cost: pct = rp / cost * 100
        if pct is None or (isinstance(pct, float) and math.isnan(pct)): continue
        out.append((p.get("signal_date", ""), p.get("close_date", p.get("signal_date", "")), float(pct)))
    return out

def leg_metrics(port, spy_ret_pct):
    """返回 (n, alpha, robust_ok, final_eq)。
    **单一真相源**:已实现直接读卡片 stats.total_realized_pnl_usd(= backfill 的 compound_portfolio),
    保证 决策视图排名 与 实验室卡片 分毫不差。用已实现(closed track record),不含浮盈。"""
    trades = _closed_trades(port)
    n = len(trades)
    if n == 0:
        return 0, 0.0, False, INIT
    realized = (port.get("stats", {}) or {}).get("total_realized_pnl_usd", 0) or 0
    ret_pct = realized / INIT * 100
    alpha = (ret_pct - spy_ret_pct) / 100.0
    # robustness:去掉最赚2笔(按pct),剩余复利仍 > 起始
    rest = sorted(trades, key=lambda t: t[2])[:-2] if n > 2 else []
    robust_ok = compound_frac20(rest, init=INIT) > INIT if rest else False
    return n, alpha, robust_ok, INIT + realized

LEGS = {"momma":"MOM-MA·动量+20MA","momh":"MOM-H·动量+H","bq":"B-quant·多因子","bai":"B-AI·多因子+DS",
        "h":"H·小盘Haiku","hds":"H-DS·小盘DS","mn":"H-广池·晨报","c":"C·B+跳空"}
TRADEABLE = {"momma", "bq"}   # real-money 起步只投可手动低换手腿
PHASE2_MKT = 0.10

def _spy_forward_ret():
    try:
        s = json.load(open("data/portfolio_spy.json"))["stats"]
        return (s.get("portfolio_value", INIT) / INIT - 1) * 100
    except Exception:
        return 0.0

def _spy_peak_trough():
    """SPY 前向峰谷振幅(yfinance,近6mo),判 Phase2 市场条件。失败返回0。"""
    try:
        import numpy as np, yfinance as yf
        c = np.asarray(yf.download("SPY", period="6mo", interval="1d", progress=False)["Close"].dropna()).ravel()
        if len(c) < 5: return 0.0
        return float((c.max() - c.min()) / c.max())
    except Exception:
        return 0.0

def main():
    spy_ret = _spy_forward_ret()
    convictions, priors, metrics = {}, {}, {}
    for key, name in LEGS.items():
        path = f"data/portfolio_{key}.json"
        if not os.path.exists(path): continue
        port = json.load(open(path))
        n, alpha, robust, final = leg_metrics(port, spy_ret)
        conv = conviction_score(n, alpha, robust)
        convictions[key] = conv
        priors[key] = MOMMA_PRIOR if key == "momma" else 0.0
        metrics[key] = {"name": name, "n": n, "alpha_pct": round(alpha*100,2),
                        "robust": robust, "conviction": conv, "fwd_ret_pct": round((final/INIT-1)*100,2),
                        "tradeable": key in TRADEABLE}
    # active% 只由"可交易腿(tradeable)"的最强信念驱动 —— 真金只在我们真交易、真证明了的腿上加仓,
    # 不被 h/c 等不交易的 AI 腿的(平盘)alpha 拉高(避免把 flat-market 噪音当 edge)。非tradeable腿信念仍上 dashboard 供观察。
    tradeable_convs = [convictions[k] for k in convictions if k in TRADEABLE]
    max_conv = max(tradeable_convs) if tradeable_convs else 0.0
    active = active_fraction(max_conv)
    weights = active_weights(convictions, priors)
    # 各腿最终占总资金% = active × 主动内部权重(只对 tradeable 归一上钱;其余腿权重展示但置灰)
    tw = {k: weights[k] for k in weights if k in TRADEABLE}
    tsum = sum(tw.values()) or 1.0
    final_alloc = {k: round(active * (tw[k]/tsum), 4) for k in tw}
    # Phase2 进度
    passed_legs = [k for k,m in metrics.items() if m["n"]>=40 and m["alpha_pct"]>0 and m["robust"]]
    mkt = _spy_peak_trough()
    phase2 = {"evidence_ok": len(passed_legs)>0, "passed_legs": passed_legs,
              "market_amp_pct": round(mkt*100,1), "market_ok": mkt>=PHASE2_MKT,
              "complete": len(passed_legs)>0 and mkt>=PHASE2_MKT}
    out = {"generated": __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M"),
           "spy_fwd_ret_pct": round(spy_ret,2), "max_conviction": round(max_conv,4),
           "active_pct": active, "index_pct": round(1-active,4),
           "legs": metrics, "weights": weights, "final_allocation": final_alloc,
           "tradeable": sorted(TRADEABLE), "phase2": phase2,
           "params": {"floor":ACTIVE_FLOOR,"ceiling":ACTIVE_CEILING,"n_full":N_FULL,"alpha_target":ALPHA_TARGET}}
    json.dump(out, open("data/allocation.json","w"), ensure_ascii=False, indent=2)
    with open("dashboard/allocation.js","w",encoding="utf-8") as f:
        f.write(f"window.ALLOCATION = {json.dumps(out, ensure_ascii=False)};\n")
    print(f"主动{active*100:.0f}% / 指数{(1-active)*100:.0f}% · 最强信念{max_conv:.2f} · Phase2 {'✅' if phase2['complete'] else '进行中'}")
    print("  tradeable 配置:", {k: f"{v*100:.0f}%" for k,v in final_alloc.items()})

if __name__ == "__main__":
    main()
