import sys, os, json, tempfile, copy
from datetime import date
from pathlib import Path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from scripts.market_intel.config import paths
from scripts.market_intel.deliver import (validate_verdict, validate_watchlist, classify_failure, build_message,
                                          weekly_usage, usage_row, run_ok, run_stage_fail)

SNAP = {"session_date": "2026-11-04", "qqq": {"close": 691.95, "gate": {"target": 1.5}},
        "movers": [{"symbol": "APP"}, {"symbol": "BE"}], "data_issues": ["测试数据问题"]}
VERDICT = {"date": "2026-11-04", "qqq_close": 691.95,
           "analysts": {"macro": {"lean": "bearish", "confidence": "medium"},
                        "catalysts": {"lean": "neutral", "confidence": "low"},
                        "qqq_tech": {"lean": "bullish", "confidence": "low"},
                        "qqq_fund": {"lean": "neutral", "confidence": "medium", "reused": True}},
           "final": {"action": "hold", "lean": "neutral", "confidence": "low", "horizon_days": 20}}
WATCH = [{"symbol": "APP", "catalyst": "earnings", "direction": "up", "price": 612.3, "note": "财报超预期"},
         {"symbol": "XYZ", "catalyst": "other", "direction": "down", "price": 10.0, "note": "编造的"}]
CJ = {"is_error": False, "result": "done", "total_cost_usd": 3.21, "duration_ms": 1800000, "num_turns": 12,
      "modelUsage": {"claude-opus-5-5": {"inputTokens": 1000, "outputTokens": 500, "cacheReadInputTokens": 200,
                                         "cacheCreationInputTokens": 300, "costUSD": 2.0},
                     "claude-sonnet-5-5": {"inputTokens": 4000, "outputTokens": 1000, "cacheReadInputTokens": 0,
                                           "cacheCreationInputTokens": 0, "costUSD": 1.21}}}


def test_validate_verdict_ok():
    assert validate_verdict(VERDICT, SNAP) == []


def test_validate_verdict_bad_enum():
    v = copy.deepcopy(VERDICT); v["analysts"]["macro"]["lean"] = "up"
    assert len(validate_verdict(v, SNAP)) == 1


def test_validate_verdict_wrong_date():
    v = copy.deepcopy(VERDICT); v["date"] = "2026-11-03"     # 昨天残留的结论
    assert validate_verdict(v, SNAP)


def test_validate_verdict_close_mismatch():
    v = copy.deepcopy(VERDICT); v["qqq_close"] = round(691.95 * 1.005, 2)
    assert validate_verdict(v, SNAP)


def test_validate_verdict_missing_analyst():
    v = copy.deepcopy(VERDICT); del v["analysts"]["qqq_tech"]
    assert validate_verdict(v, SNAP)


def test_validate_watchlist_drops_unknown():
    kept, notes = validate_watchlist(WATCH, SNAP)
    assert [w["symbol"] for w in kept] == ["APP"]
    assert any("XYZ" in n for n in notes)


def test_classify_failure():
    assert classify_failure(None, 137, True).startswith("超过 75 分钟")
    assert classify_failure({"is_error": True, "result": "Failed to authenticate: OAuth session expired"}, 1,
                            False).startswith("Claude 登录失效")
    assert classify_failure({"is_error": True, "result": "Claude usage limit reached"}, 1,
                            False).startswith("Claude 订阅额度用完")
    assert classify_failure({"is_error": True, "result": "boom"}, 1, False).startswith("Claude 运行出错")
    assert classify_failure(None, 1, False, extra="Not logged in · Please run /login").startswith("Claude 登录失效")


def test_build_message():
    msg = build_message("\n".join(f"第{i}行" for i in range(40)), SNAP, ["已剔除快照外代码 XYZ"], None)
    lines = msg.splitlines()
    assert lines[0] == "📡 每晚市场情报 2026-11-04(信号)"
    assert "第29行" in msg and "第30行" not in msg and "已截断" in msg
    assert "测试数据问题" in msg and "XYZ" in msg and "不会自动下单" in lines[-1]


def test_weekly_usage():
    rows = [{"date": "2026-11-0%d" % d, "total_tokens": 100, "cost_usd_notional": 1.5} for d in range(2, 7)]
    s = weekly_usage(rows, date(2026, 11, 7))                    # 周六
    assert s and "5 次" in s and "500" in s
    assert weekly_usage(rows, date(2026, 11, 4)) is None         # 周三


def test_usage_row():
    r = usage_row(CJ, "2026-11-04")
    assert r["total_tokens"] == 7000 and r["cost_usd_notional"] == 3.21
    assert r["models"] == ["claude-opus-5-5", "claude-sonnet-5-5"] and r["date"] == "2026-11-04"


def _fake_run(tmp, drop=None):
    p = paths(Path(tmp))
    for d in (p.ws_snapshot, p.ws_out, p.ws_reports, p.logs):
        d.mkdir(parents=True, exist_ok=True)
    (p.ws_snapshot / "2026-11-04.json").write_text(json.dumps(SNAP, ensure_ascii=False))
    (p.ws_out / "summary.txt").write_text("【宏观】测试")
    (p.ws_out / "verdict.json").write_text(json.dumps(VERDICT))
    (p.ws_out / "watchlist.json").write_text(json.dumps(WATCH))
    (p.ws_out / "fundamentals.md").write_text("基本面结论")
    (p.ws_reports / "2026-11-04.md").write_text("# 报告")
    if drop:
        (p.ws_out / drop).unlink()
    cjp = p.logs / "claude-2026-11-04.json"
    cjp.write_text(json.dumps(CJ))
    return p, cjp


def _lines(f):
    return f.read_text().splitlines() if f.exists() else []


def test_deliver_end_to_end():
    p, cjp = _fake_run(tempfile.mkdtemp())
    sent = []
    assert run_ok(p, cjp, 0, False, send=sent.append, today_sz=date(2026, 11, 5)) == 0
    assert len(sent) == 1 and sent[0].startswith("📡 每晚市场情报 2026-11-04")
    v = json.loads(_lines(p.logs / "verdicts.jsonl")[0])
    assert v["qqq_close_snapshot"] == 691.95 and v["gate"] == {"target": 1.5}
    w = [json.loads(l) for l in _lines(p.logs / "watchlist.jsonl")]
    assert [x["symbol"] for x in w] == ["APP"] and w[0]["date"] == "2026-11-04"
    assert len(_lines(p.logs / "usage.jsonl")) == 1
    assert (p.archive_reports / "2026-11-04.md").exists()
    assert (p.state / "last_session.txt").read_text().strip() == "2026-11-04"
    assert (p.state / "fundamentals_latest.md").read_text() == "基本面结论"


def test_deliver_missing_verdict_sends_failure():
    p, cjp = _fake_run(tempfile.mkdtemp(), drop="verdict.json")
    sent = []
    run_ok(p, cjp, 0, False, send=sent.append, today_sz=date(2026, 11, 5))
    assert len(sent) == 1 and sent[0].startswith("⚠️ 今日情报未完成")
    assert not (p.state / "last_session.txt").exists()          # 下次运行重试
    assert _lines(p.logs / "verdicts.jsonl") == []
    assert len(_lines(p.logs / "usage.jsonl")) == 1              # 用量照记


def test_deliver_claude_error_sends_reason():
    p, cjp = _fake_run(tempfile.mkdtemp())
    cjp.write_text(json.dumps({"is_error": True, "result": "Failed to authenticate"}))
    sent = []
    run_ok(p, cjp, 1, False, send=sent.append, today_sz=date(2026, 11, 5))
    assert "登录失效" in sent[0] and not (p.state / "last_session.txt").exists()


def test_run_stage_fail():
    sent = []
    run_stage_fail("快照", "QQQ 两源都取不到", send=sent.append)
    assert sent[0].startswith("⚠️ 今日情报未完成") and "快照" in sent[0] and "QQQ 两源都取不到" in sent[0]


if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f(); print(f"  ok {n}")
    print("ALL PASS")
