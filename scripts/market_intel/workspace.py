"""AI 工作区:每次运行前重建 ws/(清掉昨天的产出),放入指令和子智能体定义;启动 AI 前扫描密钥。
用法: python3 -m scripts.market_intel.workspace prepare|check"""
import json, re, shutil, sys
from pathlib import Path

from scripts.market_intel.config import paths, SECRET_PATTERNS

ASSETS = Path(__file__).parent / "assets"


def build_agents_json(agents_dir):
    """agents/*.md(frontmatter: description/model/tools)→ claude --agents 要的 JSON。"""
    out = {}
    for f in sorted(Path(agents_dir).glob("*.md")):
        text = f.read_text()
        _, head, body = text.split("---", 2)
        meta = dict(l.split(":", 1) for l in head.strip().splitlines() if ":" in l)
        meta = {k.strip(): v.strip() for k, v in meta.items()}
        out[f.stem] = {"description": meta["description"], "prompt": body.strip(),
                       "tools": [t.strip() for t in meta["tools"].split(",") if t.strip()],
                       "model": meta["model"]}
    return out


def prepare_workspace(p, assets_dir=ASSETS):
    assets_dir = Path(assets_dir)
    if p.ws.exists():
        shutil.rmtree(p.ws)
    for d in (p.ws_snapshot, p.ws_out, p.ws_reports, p.ws_prompts,
              p.archive_snapshots, p.archive_reports, p.state, p.logs):
        d.mkdir(parents=True, exist_ok=True)
    shutil.copy(assets_dir / "lead.md", p.ws_prompts / "lead.md")
    (p.ws / "agents.json").write_text(
        json.dumps(build_agents_json(assets_dir / "agents"), ensure_ascii=False, indent=2))


def assert_no_secrets(ws):
    """返回 ["相对路径: 模式", ...];只报位置不回显命中的值。"""
    hits = []
    for f in sorted(Path(ws).rglob("*")):
        if not f.is_file():
            continue
        try:
            text = f.read_text(errors="ignore")
        except OSError:
            continue
        for pat in SECRET_PATTERNS:
            if re.search(pat, text):
                hits.append(f"{f.relative_to(ws)}: {pat}")
    return hits


def main(argv):
    p = paths()
    if argv[:1] == ["prepare"]:
        prepare_workspace(p)
        print(f"[workspace] 已重建 {p.ws}")
        return 0
    if argv[:1] == ["check"]:
        hits = assert_no_secrets(p.ws)
        for h in hits:
            print(f"[workspace] ⚠️ 疑似密钥: {h}")
        return 1 if hits else 0
    print("用法: python3 -m scripts.market_intel.workspace prepare|check")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
