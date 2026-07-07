"""通用腿 edge 体检 —— 毕业5关硬指标,任意腿。自门控:平仓<80笔静默;满80且未报过→跑全套+飞书(只报一次)。
用法: LEG=hds python scripts/analyze-leg-edge.py   (默认mn)
由 run.sh review 每日为 mn/hds 各调一次,腿一跨过80笔自动飞书裁决。
关:①样本≥80 ②alpha vs SPY 95%CI下沿>0 ③去最赚2笔仍正 ④扣0.5%/边滑点仍正 ⑤多空分开。
支持多空腿(dir=BUY+1/SELL-1,alpha按方向调=市场中性口径)。
"""
import os, json, random
from statistics import mean

LEG = os.environ.get("LEG", "mn")
NEED = 80
FLAG = f"data/{LEG}-edge-80-done"
PORT = f"data/portfolio_{LEG}.json"


def analyze():
    import yfinance as yf
    cp = json.load(open(PORT)).get("closed_positions", [])
    spy = yf.download("SPY", start="2026-05-15", end="2026-12-31", progress=False)["Close"]
    spy = (spy["SPY"] if hasattr(spy, "columns") else spy).dropna()
    sp = {str(k.date()): float(v) for k, v in spy.items()}

    def near(dt):
        ks = [k for k in sp if k <= dt]
        return sp[max(ks)] if ks else None

    tr = []
    for t in cp:
        dr = 1 if t["action"] == "BUY" else -1
        ret = dr * (t["close_price"] / t["entry_price"] - 1)
        s0, s1 = near(t["signal_date"]), near(t["close_date"])
        if not (s0 and s1):
            continue
        tr.append({"ret": ret, "alpha": ret - dr * (s1 / s0 - 1), "dir": dr})
    n = len(tr)
    al = [x["alpha"] for x in tr]; rets = [x["ret"] for x in tr]
    ms = sorted(mean(random.choices(al, k=n)) for _ in range(3000))
    lo, hi = ms[75], ms[2925]
    top2 = sorted(range(n), key=lambda i: al[i])[-2:]
    rest = mean([al[i] for i in range(n) if i not in top2])
    slip = mean([r - 2 * 0.005 for r in rets])
    longs = sum(1 for x in tr if x["dir"] == 1)
    g2, g3, g4 = lo > 0, rest > 0, slip > 0
    lines = [f"🎓 {LEG} edge体检 · {n}笔",
             f"① 样本 {n}/{NEED} {'✅' if n >= NEED else '❌'}",
             f"② alpha {mean(al)*100:+.2f}% CI[{lo*100:+.2f}%,{hi*100:+.2f}%] 下沿>0? {'✅' if g2 else '❌不显著'}",
             f"③ 去最赚2笔 {rest*100:+.2f}% {'✅' if g3 else '❌'}",
             f"④ 扣0.5%滑点 {slip*100:+.2f}% {'✅' if g4 else '❌'}",
             f"⑤ 多{longs}/空{n-longs}笔",
             ("🟢 5关全过→可考虑给真钱(小额学费)!" if (n >= NEED and g2 and g3 and g4)
              else "⚠️ 未全过,继续攒/别上真钱"),
             "（交易信号系统·leg edge体检）"]
    return "\n".join(lines)


def run():
    force = os.environ.get("FORCE") == "1"
    try:
        n = len(json.load(open(PORT)).get("closed_positions", []))
    except Exception:
        return
    if not force:
        if n < NEED:
            print(f"[{LEG}-edge] 平仓{n}/{NEED}笔,未到线,静默"); return
        if os.path.exists(FLAG):
            print(f"[{LEG}-edge] 已报过80笔体检,跳过"); return
    msg = analyze()
    print(msg)
    if n >= NEED:
        open(FLAG, "w").write(f"reported at {n} trades\n")
    if os.environ.get("NOTIFY_WEBHOOK"):
        os.environ["NOTIFY_MESSAGE"] = msg
        import runpy
        try: runpy.run_path("scripts/notify-webhook.py", run_name="__main__")
        except Exception: pass


if __name__ == "__main__":
    run()
