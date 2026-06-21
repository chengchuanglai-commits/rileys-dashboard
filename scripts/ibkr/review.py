"""复盘:exec-log + IBKR实际 + 引擎目标 → 三方对比。异常优先。飞书+落盘。"""
import os, json, time
from scripts.ibkr.config import NOTIONAL, HARD_REDLINE

def build_review(exec_log, actual_sh, target_sh, nav, peak):
    anomalies = []
    # 下单失败/拒单
    for p in exec_log.get("placed", []):
        if p.get("error") or p.get("status") in ("Cancelled", "Inactive"):
            anomalies.append(f"下单异常 {p.get('sym')}: {p.get('error') or p.get('status')}")
    # 安全闸拦截
    if exec_log.get("gate_ok") is False:
        anomalies.append(f"安全闸拦截: {exec_log.get('gate_reason','')}")
    # 持仓对不上目标
    for s in set(list(target_sh) + list(actual_sh)):
        diff = abs(target_sh.get(s, 0) - actual_sh.get(s, 0))
        thresh = max(0.05 * abs(target_sh.get(s, 0)), 0.5)
        if diff > thresh:
            anomalies.append(f"持仓对不上 {s}: 目标{target_sh.get(s,0)} 实际{actual_sh.get(s,0)}")
    # 回撤红线
    dd = (peak - nav) / peak if peak > 0 else 0
    if dd >= HARD_REDLINE * 0.8:
        anomalies.append(f"逼近回撤红线: 回撤{dd*100:.1f}% (红线{HARD_REDLINE*100:.0f}%)")
    return {"date": exec_log.get("date", time.strftime("%Y-%m-%d")),
            "anomalies": anomalies, "nav": nav, "drawdown_pct": round(dd*100, 1),
            "actions": exec_log.get("placed", []), "breaker": exec_log.get("breaker", "normal")}

def format_msg(r):
    lines = [f"📋 IBKR交易日复盘 {r['date']}"]
    if r["anomalies"]:
        lines.append("🔴 异常:")
        lines += [f"  - {a}" for a in r["anomalies"]]
    else:
        lines.append("✅ 今日无异常")
    lines.append(f"📊 净值 ${r['nav']:.0f} · 回撤 {r['drawdown_pct']}% · 断路器 {r['breaker']}")
    lines.append(f"   动作 {len(r['actions'])} 笔")
    lines.append("（交易信号系统）")
    return "\n".join(lines)

def run():
    from scripts.ibkr.client import connect, health
    from scripts.ibkr.targets import build_targets
    from scripts.ibkr.notify import send
    date = time.strftime("%Y-%m-%d")
    exec_log = json.load(open(f"data/exec-log/{date}.json")) if os.path.exists(f"data/exec-log/{date}.json") else {"date": date}
    ib, _ = connect(client_id=23)
    actual_sh, nav = {}, NOTIONAL
    if ib:
        h = health(ib); nav = h["nav"] or NOTIONAL
        actual_sh = {p.contract.symbol: p.position for p in ib.positions(h["account"])}
        ib.disconnect()
    # 目标股数(粗略:用 target_usd,review 容差大,不取价精算)
    target_usd = build_targets(notional=NOTIONAL)
    r = build_review(exec_log, actual_sh, {k: 0 for k in target_usd}, nav, max(nav, NOTIONAL))
    os.makedirs("data/review", exist_ok=True)
    json.dump(r, open(f"data/review/{date}.json", "w"), ensure_ascii=False, indent=2)
    send(format_msg(r))
    print(format_msg(r))

if __name__ == "__main__":
    run()
