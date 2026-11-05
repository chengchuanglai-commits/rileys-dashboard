import sys, os, json, tempfile
from pathlib import Path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from scripts.market_intel.config import paths
from scripts.market_intel.workspace import prepare_workspace, build_agents_json, assert_no_secrets

AGENT_MD = "---\ndescription: d\nmodel: sonnet\ntools: WebSearch, Read\n---\nbody"


def _assets(tmp):
    a = Path(tmp) / "assets"
    (a / "agents").mkdir(parents=True)
    (a / "lead.md").write_text("lead instructions")
    (a / "agents" / "x.md").write_text(AGENT_MD)
    return a


def test_prepare_clears_stale():
    tmp = tempfile.mkdtemp()
    p = paths(Path(tmp) / "root")
    p.ws_out.mkdir(parents=True)
    (p.ws_out / "summary.txt").write_text("昨天的旧摘要")
    p.logs.mkdir(parents=True)
    (p.logs / "verdicts.jsonl").write_text('{"keep": 1}\n')
    prepare_workspace(p, _assets(tmp))
    assert not (p.ws_out / "summary.txt").exists()          # 旧产出必须清掉,不能当今天的发出去
    assert (p.logs / "verdicts.jsonl").read_text() == '{"keep": 1}\n'   # 日志不能动
    assert (p.ws_prompts / "lead.md").read_text() == "lead instructions"
    assert json.loads((p.ws / "agents.json").read_text())["x"]["model"] == "sonnet"
    for d in (p.ws_snapshot, p.ws_out, p.ws_reports, p.archive_snapshots, p.archive_reports, p.state):
        assert d.is_dir(), d


def test_build_agents_json():
    tmp = tempfile.mkdtemp()
    a = _assets(tmp)
    assert build_agents_json(a / "agents") == {
        "x": {"description": "d", "prompt": "body", "tools": ["WebSearch", "Read"], "model": "sonnet"}}


def test_assert_no_secrets():
    tmp = Path(tempfile.mkdtemp())
    (tmp / "clean.txt").write_text("QQQ 685.28 闸门 1.5x")
    assert assert_no_secrets(tmp) == []
    (tmp / "sub").mkdir()
    (tmp / "sub" / "leak.txt").write_text("https://open.feishu.cn/open-apis/bot/v2/hook/abc")
    hits = assert_no_secrets(tmp)
    assert hits and all("abc" not in h for h in hits)       # 只报文件和模式,不回显命中的值
    assert any("leak.txt" in h for h in hits)


def test_assert_no_secrets_account_number():
    tmp = Path(tempfile.mkdtemp())
    (tmp / "snap.json").write_text('{"account": "U1234567"}')
    assert assert_no_secrets(tmp)


if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f(); print(f"  ok {n}")
    print("ALL PASS")
