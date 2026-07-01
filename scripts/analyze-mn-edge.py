"""mn(H-广池)腿 edge 体检 —— 毕业5关硬指标。
自门控:平仓<80笔时静默退出;满80且未报过→跑全套+飞书+落flag(只报一次)。
由 run.sh review 每日调用,mn一跨过80笔自动触发。
手动强制跑: FORCE=1 python scripts/analyze-mn-edge.py
关:①样本≥80 ②alpha vs SPY 95%CI下沿>0 ③去最赚2笔仍正 ④扣0.5%/边滑点仍正 ⑤多空分开。
"""
import os, json, random
from statistics import mean

NEED = 80
FLAG = "data/mn-edge-80-done"


def analyze():
    import yfinance as yf
    d = json.load(open("data/portfolio_mn.json"))
    cp = d.get("closed_positions", [])
    spy = yf.download("SPY", start="2026-05-15", end="2026-12-31", progress=False)["Close"]
    spy = spy["SPY"] if hasattr(spy, "columns") else spy
    sp = {str(k.date()): float(v) for k, v in spy.dropna().items()}

    def spy_near(dt):
        ks = [k for k in sp if k <= dt]
        return sp[max(ks)] if ks else None

    trades = []
    for t in cp:
        dr = 1 if t["action"] == "BUY" else -1
        ret = dr * (t["close_price"] / t["entry_price"] - 1)
        s0, s1 = spy_near(t["signal_date"]), spy_near(t["close_date"])
        if not (s0 and s1):
            continue
        trades.append({"ret": ret, "spy": dr * (s1 / s0 - 1),
                       "alpha": ret - dr * (s1 / s0 - 1), "dir": dr})
    n = len(trades)
    alphas = [x["alpha"] for x in trades]; rets = [x["ret"] for x in trades]
    ms = sorted(mean(random.choices(alphas, k=n)) for _ in range(3000))
    lo, hi = ms[75], ms[2925]                      # 95% bootstrap CI
    top2 = sorted(range(n), key=lambda i: alphas[i])[-2:]
    rest = mean([alphas[i] for i in range(n) if i not in top2])
    slip05 = mean([r - 2 * 0.005 for r in rets])
    longs = [x for x in trades if x["dir"] == 1]
    gate2 = lo > 0
    lines = [f"🎓 mn(H-广池) edge体检 · {n}笔",
             f"① 样本 {n}/{NEED} {'✅' if n >= NEED else '❌'}",
             f"② alpha {mean(alphas)*100:+.2f}% CI[{lo*100:+.2f}%,{hi*100:+.2f}%] 下沿>0? {'✅' if gate2 else '❌不显著'}",
             f"③ 去最赚2笔 {rest*100:+.2f}% {'✅' if rest > 0 else '❌'}",
             f"④ 扣0.5%滑点 {slip05*100:+.2f}% {'✅' if slip05 > 0 else '❌'}",
             f"⑤ 多{len(longs)}/空{n-len(longs)}笔",
             ("🟢 5关全过→可考虑给真钱(小额学费)!" if (n >= NEED and gate2 and rest > 0 and slip05 > 0)
              else "⚠️ 未全过,继续攒/别上真钱"),
             "（交易信号系统·mn edge体检）"]
    return "\n".join(lines)


def run():
    force = os.environ.get("FORCE") == "1"
    try:
        cp = json.load(open("data/portfolio_mn.json")).get("closed_positions", [])
    except Exception:
        return
    n = len(cp)
    if not force:
        if n < NEED:
            print(f"[mn-edge] 平仓{n}/{NEED}笔,未到线,静默"); return
        if os.path.exists(FLAG):
            print("[mn-edge] 已报过80笔体检,跳过"); return
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
