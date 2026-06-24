"""每日各腿对照 → 飞书。收盘后附在复盘里:各腿净值/浮盈/持仓 + vs SPY,重点标抗跌。
只读 data/portfolio_*.json(回填已算进当天),不连IBKR。
用法: NOTIFY_WEBHOOK=... python scripts/legs-digest.py  (或被 review 调用)
"""
import json, os, runpy

# 关注的腿(可交易优先 + 观察对照)。括号=类型标注
LEGS = [
    ("momma", "MOM-MA 动量", "可交易"),
    ("momh",  "MOM-H 动量",  "对照"),
    ("bq",    "B-quant 多因子", "可交易"),
    ("bai",   "B-AI 多因子+AI", "对照"),
    ("mn",    "H-广池 晨报",  "观察"),
    ("c",     "C 出场参数",   "退役候选"),
    ("h",     "H 小盘",      "对照"),
    ("hds",   "H-DS 小盘",   "对照"),
]
INIT = 2000.0


def _load(k):
    try: return json.load(open(f"data/portfolio_{k}.json"))
    except Exception: return None


def build():
    spy = _load("spy")
    spy_ret = ((spy["stats"]["portfolio_value"] / INIT - 1) * 100) if spy else None
    rows = []
    for k, name, tag in LEGS:
        d = _load(k)
        if not d: continue
        s = d.get("stats", {})
        pv = s.get("portfolio_value")
        if pv is None or pv != pv: continue
        ret = (pv / INIT - 1) * 100
        rows.append({
            "name": name, "tag": tag, "pv": pv, "ret": ret,
            "unreal": s.get("open_unrealized_pnl_usd", 0) or 0,
            "open": len(d.get("open_positions", [])),
            "closed": len(d.get("closed_positions", [])),
            "vs_spy": (ret - spy_ret) if spy_ret is not None else None,
        })
    rows.sort(key=lambda r: -r["ret"])
    return rows, spy_ret


def format_msg(rows, spy_ret):
    lines = ["📊 各腿对照(收盘)"]
    if spy_ret is not None:
        lines.append(f"SPY基准 {spy_ret:+.1f}%")
    for r in rows:
        vs = f" vs SPY{r['vs_spy']:+.1f}" if r["vs_spy"] is not None else ""
        lines.append(f"{r['name']}({r['tag']}): ${r['pv']:.0f} {r['ret']:+.1f}%{vs} 持{r['open']}/平{r['closed']}")
    lines.append("（交易信号系统）")
    return "\n".join(lines)


def run():
    rows, spy_ret = build()
    if not rows:
        print("[legs] 无数据"); return
    msg = format_msg(rows, spy_ret)
    print(msg)
    if os.environ.get("NOTIFY_WEBHOOK"):
        os.environ["NOTIFY_MESSAGE"] = msg
        try: runpy.run_path("scripts/notify-webhook.py", run_name="__main__")
        except Exception as e: print(f"[legs] 发送失败: {e}")


if __name__ == "__main__":
    run()
