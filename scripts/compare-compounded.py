"""
所有模拟腿·统一 frac20 复利口径,对标 SPY (compounded forward comparison)。

只读分析:把每条腿**已平仓交易**(各有 final_pnl_pct)按 frac20 复利重算 →
  起始 $2000,每仓=当前净值20%(最多~5并发,现金约束),平仓按%收益复利。
→ 排一个 vs SPY 同期前向收益的榜,统一口径公平比。

⚠️ 诚实边界:
  - 动量腿(MOM)有长窗口诚实回测(见 backtest-momentum-sized.py);这里只是前向。
  - AI腿/B-quant 无法历史回测(LLM泄漏/基本面前视),只有前向,样本小(几周)→ 仅结构性参考,不能据此定生死。
用法: python scripts/compare-compounded.py
"""
import json, os, glob, math
import sys
sys.path.insert(0, os.path.dirname(__file__))
from portfolio_compound import compound_frac20, compound_frac20_curve

INIT = 2000.0
FRAC = 0.10            # 每仓 = 当前净值 10%(frac20,回测里最优)
MAX_CONC = 10
LEGS = {
    "h":"H·小盘Haiku","hds":"H-DS·小盘DeepSeek","mn":"H-广池·晨报中大盘",
    "b":"B·TP8/SL4/5d","c":"C·B+跳空","d":"D·TP15/SL3/2d","e":"E·VIX动态","f":"F·分档","g":"G·广池(退役)",
    "momh":"MOM-H·动量+H出场","momma":"MOM-MA·动量+20MA","bq":"B-quant·多因子","bai":"B-AI·多因子+DeepSeek",
}


def extract_closed(path):
    """返回 [(signal_date, close_date, pnl_pct)],跳过 NaN/缺失。"""
    try:
        d = json.load(open(path))
    except Exception:
        return None
    out = []
    for p in d.get("closed_positions", []):
        pct = p.get("final_pnl_pct")
        if pct is None:
            # bq/bai 可能只有 realized_pnl_usd + 仓位额,折算 pct
            rp = p.get("realized_pnl_usd"); cost = p.get("actual_position_usd") or p.get("allocated_usd")
            if rp is not None and cost:
                pct = rp / cost * 100
        if pct is None or (isinstance(pct, float) and math.isnan(pct)):
            continue
        sd = p.get("signal_date", ""); cd = p.get("close_date", p.get("signal_date", ""))
        out.append((sd, cd, float(pct)))
    return out


def spy_forward():
    try:
        d = json.load(open("data/portfolio_spy.json")); s = d.get("stats", {})
        pv = s.get("portfolio_value")
        if pv: return (pv/INIT - 1)*100
        # 退路:用未实现
        un = s.get("open_unrealized_pnl_usd", 0); return un/INIT*100
    except Exception:
        return None


def main():
    spy_ret = spy_forward()
    rows = []
    for key, name in LEGS.items():
        path = f"data/portfolio_{key}.json"
        if not os.path.exists(path): continue
        tr = extract_closed(path)
        if tr is None: continue
        final = compound_frac20(tr); n = len(tr); wr = round(len([t for t in tr if t[2]>0])/len(tr)*100,1) if tr else 0
        rows.append((key, name, final, (final/INIT-1)*100, n, wr))
    rows.sort(key=lambda r: -r[2])

    print(f"\n{'='*72}\n  所有腿·frac10复利 前向对比 (forward, 统一口径)\n{'='*72}")
    print(f"  起始${INIT:.0f} · 每仓10%净值复利 · 最多{MAX_CONC}并发")
    if spy_ret is not None:
        print(f"  📏 SPY 同期前向基准: {spy_ret:+.2f}%  (买入持有,几周窗口基本平盘)")
    print(f"\n  {'腿':<22}{'复利终值':>10}{'收益%':>9}{'笔数':>6}{'胜率':>7}  vs SPY")
    for key, name, final, ret, n, wr in rows:
        vs = f"{ret - (spy_ret or 0):+.1f}pp" if spy_ret is not None else "?"
        flag = "✅赢" if (spy_ret is not None and ret > spy_ret) else "❌输"
        print(f"  {name:<22}{final:>9.0f}{ret:>+8.1f}%{n:>6}{wr:>6}%  {vs:>8} {flag}")
    import json as _json
    curves = {}
    for key, name in LEGS.items():
        path = f"data/portfolio_{key}.json"
        if not os.path.exists(path): continue
        tr = extract_closed(path)
        if not tr: continue
        curves[key] = {"name": name, "points": compound_frac20_curve(tr)}
    # SPY 复利曲线退化为单点(买入持有),用 portfolio_spy 终值
    spy_pv = None
    try: spy_pv = _json.load(open("data/portfolio_spy.json"))["stats"]["portfolio_value"]
    except Exception: pass
    out = {"init": INIT, "spy_final": spy_pv, "curves": curves}
    with open("dashboard/compounded-curves.js", "w", encoding="utf-8") as f:
        f.write(f"window.COMPOUNDED_CURVES = {_json.dumps(out, ensure_ascii=False)};\n")

    print(f"\n  ⚠️ 样本小(前向几周)→仅结构参考,不能据此定生死。动量腿的长窗口诚实回测见 backtest-momentum-sized.py。")


if __name__ == "__main__":
    main()
