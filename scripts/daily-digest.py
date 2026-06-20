"""
每日「健康 + 决策」飞书推送 (daily digest) —— 让系统主动告诉 Riley 今天该不该动手。

一条消息包含:
  ① 今天配置(主动X%/指数Y%)+ 有没有变化
  ② 具体执行(指数买多少SPY;主动买哪条腿的哪些票,各多少)
  ③ 谁在赚(已实现复利 vs SPY)+ 平盘噪音提醒
  ④ 健康:所有腿今天都更新了吗(静默失败 silent-failure 检测)
  ⑤ Phase 进度

变化检测:把上次状态存 data/digest-state.json,这次 diff(active%变了 / 某腿信念变了 / 过关了)。
发送:复用 notify-webhook.py(读 NOTIFY_WEBHOOK + NOTIFY_MESSAGE)。零额外API成本(只读已有产物)。
用法: NOTIFY_WEBHOOK=... python scripts/daily-digest.py
"""
import os, json, runpy
from datetime import date

CAPITAL = 2000.0
STATE = "data/digest-state.json"
LEG_NAMES = {"momma": "MOM-MA", "momh": "MOM-H", "bq": "B-quant", "bai": "B-AI",
             "h": "H·小盘", "hds": "H-DS", "mn": "H-广池", "c": "C"}


def load(path, default=None):
    try:
        return json.load(open(path))
    except Exception:
        return default


def main():
    a = load("data/allocation.json")
    if not a:
        print("[digest] 无 allocation.json,跳过"); return
    today = date.today().isoformat()
    act, idx = a["active_pct"], a["index_pct"]
    legs = a.get("legs", {})
    final_alloc = a.get("final_allocation", {})
    spy = a.get("spy_fwd_ret_pct", 0.0)

    # ── 变化检测 ──
    prev = load(STATE, {}) or {}
    changes = []
    if prev.get("active_pct") is not None and abs(prev["active_pct"] - act) > 1e-6:
        changes.append(f"配置 主动 {prev['active_pct']*100:.0f}%→{act*100:.0f}%")
    for k, m in legs.items():
        pc = (prev.get("convictions") or {}).get(k)
        if pc is not None and abs(pc - m["conviction"]) >= 0.02:
            changes.append(f"{LEG_NAMES.get(k,k)} 信念 {pc:.2f}→{m['conviction']:.2f}")
    # 过关检测
    prev_passed = set((prev.get("phase2") or {}).get("passed_legs", []))
    now_passed = set(a.get("phase2", {}).get("passed_legs", []))
    for k in now_passed - prev_passed:
        changes.append(f"🎓 {LEG_NAMES.get(k,k)} 过了毕业关!")

    # ── 执行 ──
    exec_lines = [f"  • 指数 ${idx*CAPITAL:,.0f} → SPY/VOO"]
    for k, w in sorted(final_alloc.items(), key=lambda x: -x[1]):
        if w <= 0: continue
        port = load(f"data/portfolio_{k}.json", {})
        tks = [p.get("ticker") for p in (port.get("open_positions") or []) if p.get("ticker")]
        amt = w * CAPITAL
        if tks:
            exec_lines.append(f"  • 主动 ${amt:,.0f} → {LEG_NAMES.get(k,k)}: {' '.join(tks)} (各~${amt/len(tks):,.0f})")
        else:
            exec_lines.append(f"  • 主动 ${amt:,.0f} → {LEG_NAMES.get(k,k)} (暂无持仓,等信号)")

    # ── 谁在赚(按已实现复利排序) ──
    rank = sorted(legs.items(), key=lambda x: -x[1]["fwd_ret_pct"])
    top = [f"{LEG_NAMES.get(k,k)} {m['fwd_ret_pct']:+.1f}%" for k, m in rank if m["n"] > 0][:4]
    flat_warn = "(⚠️平盘期,领先=噪音)" if abs(spy) < 2 else ""

    # ── 健康(静默失败检测) ──
    updated = {}
    for k in LEG_NAMES:
        port = load(f"data/portfolio_{k}.json")
        if port:
            updated[k] = (port.get("stats", {}) or {}).get("updated_at", "?")
    latest = max([v for v in updated.values() if v and v != "?"], default="?")
    stale = [LEG_NAMES.get(k, k) for k, v in updated.items() if v != latest and v != "?"]
    health = f"✅ {len(updated)}腿均更新于{latest}" if not stale else f"⚠️ 落后: {' '.join(stale)} (其余{latest})"

    # ── Phase ──
    p2 = a.get("phase2", {})
    phase = f"Phase 1 (证据{len(p2.get('passed_legs',[]))}腿过关 / 市场振幅{p2.get('market_amp_pct','?')}%{'✓' if p2.get('market_ok') else '✗'})"
    if p2.get("complete"):
        phase = "🚀 Phase 2 可升级!(证据+市场都达标)"

    # ── 组装 ──
    msg = [f"📊 投资日报 {today}",
           f"配置: 主动 {act*100:.0f}% / 指数 {idx*100:.0f}%" + (f"  [{changes[0]}]" if changes else "  [无变化]"),
           "执行:", *exec_lines,
           f"谁在赚(已实现复利,SPY {spy:+.1f}%){flat_warn}: " + " · ".join(top) if top else "谁在赚: 暂无已平仓",
           "变化: " + (" / ".join(changes) if changes else "无"),
           f"健康: {health}",
           phase,
           "（交易信号系统）"]
    text = "\n".join(msg)
    print(text)

    # ── 存状态供下次 diff ──
    json.dump({"active_pct": act, "convictions": {k: m["conviction"] for k, m in legs.items()},
               "phase2": {"passed_legs": list(now_passed)}, "date": today},
              open(STATE, "w"), ensure_ascii=False, indent=2)

    # ── 发送 ──
    if os.environ.get("NOTIFY_WEBHOOK"):
        os.environ["NOTIFY_MESSAGE"] = text
        try:
            runpy.run_path("scripts/notify-webhook.py", run_name="__main__")
        except Exception as e:
            print(f"[digest] 发送失败: {e}")
    else:
        print("[digest] 无 NOTIFY_WEBHOOK,仅打印未发送")


if __name__ == "__main__":
    main()
