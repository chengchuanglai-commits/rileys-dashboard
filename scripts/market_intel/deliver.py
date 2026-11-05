"""每晚市场情报 · 第三段:校验 AI 产出 → 推飞书 → 追加日志/归档(纯 Python,AI 不直接对外发消息)。
任何一环失败都推"今日情报未完成+原因",绝不静默(晨报/DeepSeek 都死在静默失败上)。
用法:
  python3 -m scripts.market_intel.deliver --claude-json PATH --exit N [--timed-out]
  python3 -m scripts.market_intel.deliver --stage-fail STAGE --reason TEXT"""
import argparse, json, os, shutil, subprocess, sys
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from scripts.market_intel.config import ANALYSTS, paths

LEANS = {"bullish", "neutral", "bearish"}
CONF = {"low", "medium", "high"}
ACTIONS = {"hold", "wait", "reduce_leverage", "increase"}
CATALYSTS = {"earnings", "guidance", "rating", "mna", "regulatory", "macro", "product", "other", "unknown"}
MAX_SUMMARY_LINES = 30
NOTIFY = Path(__file__).resolve().parents[1] / "notify-webhook.py"
FOOTER = "仅供参考:系统不会自动下单,任何交易需 Riley 批准"


def validate_verdict(v, snap):
    errs = []
    if not isinstance(v, dict):
        return ["verdict.json 不是对象"]
    if v.get("date") != snap["session_date"]:
        errs.append(f"verdict 日期 {v.get('date')} ≠ 交易日 {snap['session_date']}")
    try:
        if abs(float(v["qqq_close"]) / float(snap["qqq"]["close"]) - 1) > 0.001:
            errs.append(f"verdict 的 QQQ 收盘 {v['qqq_close']} 与快照 {snap['qqq']['close']} 不符")
    except (KeyError, TypeError, ValueError):
        errs.append("verdict 缺 qqq_close")
    an = v.get("analysts") or {}
    for name in ANALYSTS:
        a = an.get(name)
        if not isinstance(a, dict) or a.get("lean") not in LEANS or a.get("confidence") not in CONF:
            errs.append(f"分析师 {name} 的 lean/confidence 缺失或不合法")
    f = v.get("final") or {}
    if f.get("action") not in ACTIONS or f.get("lean") not in LEANS or f.get("confidence") not in CONF:
        errs.append("final 的 action/lean/confidence 缺失或不合法")
    if not isinstance(f.get("horizon_days"), int) or f.get("horizon_days", 0) <= 0:
        errs.append("final.horizon_days 不是正整数")
    return errs


def validate_watchlist(items, snap):
    movers = {m["symbol"] for m in snap.get("movers", [])}
    kept, notes = [], []
    for w in items if isinstance(items, list) else []:
        sym = w.get("symbol") if isinstance(w, dict) else None
        if sym not in movers:
            notes.append(f"观察名单已剔除快照外代码 {sym}")
            continue
        ok = (w.get("catalyst") in CATALYSTS and w.get("direction") in {"up", "down"}
              and isinstance(w.get("price"), (int, float)) and isinstance(w.get("note"), str))
        if ok:
            kept.append(w)
        else:
            notes.append(f"观察名单 {sym} 字段不合法,已剔除")
    return kept, notes


def classify_failure(cj, exit_code, timed_out, extra=""):
    if timed_out:
        return "超过 75 分钟被强制停止"
    text = ((cj or {}).get("result") or "") + "\n" + (extra or "")
    low = text.lower()
    if "authenticate" in low or "not logged in" in low or "oauth" in low:
        return "Claude 登录失效:需在终端重新运行 claude setup-token 并更新 .secrets/claude.env"
    if "usage limit" in low or "rate limit" in low or "limit reached" in low:
        return "Claude 订阅额度用完"
    return "Claude 运行出错:" + text.strip()[:200]


def build_message(summary, snap, notes, weekly):
    lines = summary.strip().splitlines()
    if len(lines) > MAX_SUMMARY_LINES:
        lines = lines[:MAX_SUMMARY_LINES] + ["(摘要过长已截断,完整报告见本机 archive/reports)"]
    out = [f"📡 每晚市场情报 {snap['session_date']}(信号)", *lines]
    extra = list(snap.get("data_issues") or []) + list(notes)
    if extra:
        out += ["", "⚠️ 数据说明:"] + [f"· {x}" for x in extra]
    if weekly:
        out += ["", weekly]
    return "\n".join(out + ["", FOOTER])


def usage_row(cj, session_date):
    mu = cj.get("modelUsage") or {}
    total = sum(int(m.get(k, 0) or 0) for m in mu.values()
                for k in ("inputTokens", "outputTokens", "cacheReadInputTokens", "cacheCreationInputTokens"))
    return {"date": session_date, "duration_ms": cj.get("duration_ms"), "num_turns": cj.get("num_turns"),
            "cost_usd_notional": cj.get("total_cost_usd"), "total_tokens": total, "models": sorted(mu)}


def weekly_usage(rows, today_sz):
    if today_sz.weekday() != 5:
        return None
    since = today_sz - timedelta(days=7)
    wk = [r for r in rows if since <= date.fromisoformat(r["date"]) <= today_sz]
    if not wk:
        return None
    tok = sum(r.get("total_tokens") or 0 for r in wk)
    cost = sum(r.get("cost_usd_notional") or 0 for r in wk)
    return f"📊 本周用量:{len(wk)} 次运行,共 {tok:,} tokens(按 API 价折算约 ${cost:.2f},订阅内不另付费)"


def send(msg):
    print(msg)
    try:
        subprocess.run([sys.executable, str(NOTIFY)], env={**os.environ, "NOTIFY_MESSAGE": msg}, timeout=30)
    except Exception as e:
        print(f"[deliver] 飞书发送异常: {e}")


def _fail_msg(session, reason):
    return f"⚠️ 今日情报未完成({session}):{reason}\n系统没有做任何交易;下次运行会自动重试。"


def _append(f, rows):
    f.parent.mkdir(parents=True, exist_ok=True)
    with open(f, "a") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")


def _load_json(f):
    try:
        return json.loads(Path(f).read_text())
    except (OSError, ValueError):
        return None


def run_ok(p, claude_json_path, exit_code, timed_out, send=send, today_sz=None):
    today_sz = today_sz or datetime.now(ZoneInfo("Asia/Shanghai")).date()
    snaps = sorted(p.ws_snapshot.glob("*.json"))
    if not snaps:
        send(_fail_msg("?", "快照文件缺失"))
        return 0
    snap = json.loads(snaps[-1].read_text())
    session = snap["session_date"]
    claude_json_path = Path(claude_json_path)
    cj = _load_json(claude_json_path)
    if cj is not None:
        _append(p.logs / "usage.jsonl", [usage_row(cj, session)])
    if timed_out or exit_code != 0 or cj is None or cj.get("is_error"):
        err = claude_json_path.with_suffix(".err")
        extra = err.read_text(errors="ignore")[-2000:] if err.exists() else ""
        send(_fail_msg(session, classify_failure(cj, exit_code, timed_out, extra)))
        return 0

    errs = []
    summary_f, report_f = p.ws_out / "summary.txt", p.ws_reports / f"{session}.md"
    if not summary_f.exists() or not summary_f.read_text().strip():
        errs.append("摘要 out/summary.txt 缺失")
    if not report_f.exists():
        errs.append(f"报告 reports/{session}.md 缺失")
    verdict = _load_json(p.ws_out / "verdict.json")
    errs += ["out/verdict.json 缺失或不是合法 JSON"] if verdict is None else validate_verdict(verdict, snap)
    if errs:
        send(_fail_msg(session, "AI 产出不合格:" + ";".join(errs[:5])))
        return 0

    watch = _load_json(p.ws_out / "watchlist.json")
    kept, notes = validate_watchlist(watch, snap) if watch is not None else ([], ["观察名单 out/watchlist.json 缺失"])
    rows = [json.loads(l) for l in (p.logs / "usage.jsonl").read_text().splitlines()] \
        if (p.logs / "usage.jsonl").exists() else []
    send(build_message(summary_f.read_text(), snap, notes, weekly_usage(rows, today_sz)))

    _append(p.logs / "verdicts.jsonl",
            [{**verdict, "qqq_close_snapshot": snap["qqq"]["close"], "gate": snap["qqq"].get("gate")}])
    _append(p.logs / "watchlist.jsonl", [{**w, "date": session} for w in kept])
    p.archive_reports.mkdir(parents=True, exist_ok=True)
    shutil.move(str(report_f), str(p.archive_reports / f"{session}.md"))
    p.state.mkdir(parents=True, exist_ok=True)
    if (p.ws_out / "fundamentals.md").exists():
        shutil.copy(p.ws_out / "fundamentals.md", p.state / "fundamentals_latest.md")
    (p.state / "last_session.txt").write_text(session + "\n")
    print(f"[deliver] ✅ {session} 已推送,观察名单 {len(kept)} 只")
    return 0


def run_stage_fail(stage, reason, send=send):
    send(_fail_msg(datetime.now(ZoneInfo("America/New_York")).date().isoformat(), f"{stage}阶段失败 — {reason}"))
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--claude-json")
    ap.add_argument("--exit", type=int, default=0)
    ap.add_argument("--timed-out", action="store_true")
    ap.add_argument("--stage-fail")
    ap.add_argument("--reason", default="")
    a = ap.parse_args(argv)
    if a.stage_fail:
        return run_stage_fail(a.stage_fail, a.reason)
    return run_ok(paths(), a.claude_json, a.exit, a.timed_out)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
