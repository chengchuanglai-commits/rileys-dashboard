"""复盘:exec-log + IBKR实际 + 引擎目标 → 三方对比。异常优先。飞书+落盘。"""
import os, json, time
from scripts.ibkr.config import NOTIONAL, HARD_REDLINE

PENDING_EXIT = "data/review-pending-exit.json"  # {sym: 首次发现日} 不在目标里的持仓,连续2个复盘日才算异常


def build_review(exec_log, actual_mv, target_usd, nav, peak):
    """actual_mv/target_usd 均为美元市值口径(2026-07-15修:原来目标传全0的桩,13仓天天假报'对不上')。"""
    anomalies, infos = [], []
    # 下单失败/拒单
    for p in exec_log.get("placed", []):
        if p.get("error") or p.get("status") in ("Cancelled", "Inactive"):
            anomalies.append(f"下单异常 {p.get('sym')}: {p.get('error') or p.get('status')}")
    # 安全闸拦截
    if exec_log.get("gate_ok") is False:
        anomalies.append(f"安全闸拦截: {exec_log.get('gate_reason','')}")
    # 持仓 vs 三线目标(市值口径,容差要吃下"sim早盘换仓→IBKR当晚才执行"的一天滞后)
    try: pending = json.load(open(PENDING_EXIT))
    except Exception: pending = {}
    today = exec_log.get("date", time.strftime("%Y-%m-%d"))
    new_pending = {}
    for s in set(list(target_usd) + list(actual_mv)):
        t, a = target_usd.get(s, 0), actual_mv.get(s, 0)
        if t > 0 and a <= 0:
            anomalies.append(f"缺仓 {s}: 目标${t:.0f} 实际0")
        elif t > 0 and abs(a - t) > max(0.5 * t, 500):
            anomalies.append(f"持仓对不上 {s}: 目标${t:.0f} 实际${a:.0f}")
        elif t <= 0 and a > 200:   # 不在目标里(>$200防碎股噪音):首日=正常滞后,连续2天=该卖没卖
            if pending.get(s) and pending[s] < today:
                anomalies.append(f"该卖未卖 {s}: 已持续2个复盘日,市值${a:.0f}")
                new_pending[s] = pending[s]
            else:
                infos.append(f"待出场 {s} ${a:.0f}(sim已剔除,今晚开盘batch应卖出)")
                new_pending[s] = pending.get(s, today)
    try: json.dump(new_pending, open(PENDING_EXIT, "w"), ensure_ascii=False)
    except Exception: pass
    # 回撤红线
    dd = (peak - nav) / peak if peak > 0 else 0
    if dd >= HARD_REDLINE * 0.8:
        anomalies.append(f"逼近回撤红线: 回撤{dd*100:.1f}% (红线{HARD_REDLINE*100:.0f}%)")
    return {"date": exec_log.get("date", time.strftime("%Y-%m-%d")),
            "anomalies": anomalies, "infos": infos, "nav": nav, "drawdown_pct": round(dd*100, 1),
            "actions": exec_log.get("placed", []), "breaker": exec_log.get("breaker", "normal")}

def format_msg(r):
    lines = [f"📋 IBKR交易日复盘 {r['date']}"]
    if r["anomalies"]:
        lines.append("🔴 异常:")
        lines += [f"  - {a}" for a in r["anomalies"]]
    else:
        lines.append("✅ 今日无异常")
    for i in r.get("infos", []):
        lines.append(f"  ℹ️ {i}")
    lines.append(f"📊 净值 ${r['nav']:.0f} · 回撤 {r['drawdown_pct']}% · 断路器 {r['breaker']}")
    lines.append(f"   动作 {len(r['actions'])} 笔")
    lines.append("（交易信号系统）")
    return "\n".join(lines)

def run():
    from scripts.ibkr.client import connect, health
    from scripts.ibkr.targets import build_master_targets
    from scripts.ibkr.notify import send
    date = time.strftime("%Y-%m-%d")
    exec_log = json.load(open(f"data/exec-log/{date}.json")) if os.path.exists(f"data/exec-log/{date}.json") else {"date": date}
    ib, _ = connect(client_id=23)
    actual_mv, nav = {}, NOTIONAL
    connected = False
    if ib:
        h = health(ib); nav = h["nav"] or NOTIONAL
        # 市值口径(portfolio给marketValue;只看股票,滤掉外汇等)
        for it in ib.portfolio():
            if it.contract.secType == "STK":
                actual_mv[it.contract.symbol] = actual_mv.get(it.contract.symbol, 0) + float(it.marketValue)
        connected = True
        ib.disconnect()
    # 三线统一目标(2026-07-15修:原build_targets只盖指数+动量,长线全0;且传的是{k:0}的桩→13仓天天假报)
    target_usd = build_master_targets(notional=NOTIONAL) if connected else {}
    r = build_review(exec_log, actual_mv, target_usd, nav, max(nav, NOTIONAL))
    if not connected:
        r["anomalies"].insert(0, "IBKR未连接:持仓对账跳过(数据不可信,非无异常)")
    os.makedirs("data/review", exist_ok=True)
    json.dump(r, open(f"data/review/{date}.json", "w"), ensure_ascii=False, indent=2)
    send(format_msg(r))
    print(format_msg(r))
    # 附:各腿对照(模拟盘 vs SPY)——独立一条飞书,失败不影响复盘
    try:
        import runpy
        runpy.run_path("scripts/legs-digest.py", run_name="__main__")
    except Exception as e:
        print(f"[review] 各腿对照失败: {e}")

if __name__ == "__main__":
    run()
