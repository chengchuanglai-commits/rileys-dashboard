"""每晚市场情报 —— 常量与运行时目录(spec: docs/superpowers/specs/2026-11-04-nightly-market-intel-design.md)。
运行时目录全在仓库外的 ~/claude-market-intel/;AI 只在其中的 ws/ 里运行,日志/归档/状态在 ws 之外,AI 读不到。"""
import os
from pathlib import Path
from types import SimpleNamespace

BACKSTOP = 648.43          # 与 scripts/qqq-entry-alert.py 的 BACKSTOP 一致(Riley 11/3 定的防线 B,只提醒)
IB_PORT = 4001             # 真钱网关,只读连接
IB_CLIENT_ID = 95
SCAN_CODES = ("TOP_PERC_GAIN", "TOP_PERC_LOSE", "HOT_BY_VOLUME")
SCAN_ROWS = 15
MIN_PRICE = 5
MIN_MCAP_MUSD = 10000      # 市值 > 100 亿美元(IBKR 扫描器单位:百万美元)
MAX_MOVERS = {"full": 20, "lite": 10}
XCHECK_TOL = 0.002         # QQQ 收盘两源相差 > 0.2% 标红
TIMEOUT_SEC = 4500         # 整个 AI 段 75 分钟强杀
WS_SNAPSHOT_NAME = "snapshot.json"   # AI 没有列目录的工具,工作区快照用固定文件名(归档仍按日期)
ANALYSTS = ("macro", "catalysts", "qqq_tech", "qqq_fund")
ALLOWED_AGENT_TOOLS = {"WebSearch", "WebFetch", "Read"}
SECRET_PATTERNS = [
    r"apikey=",
    r"FMP_API_KEY",
    r"open-apis/bot",
    r"CLAUDE_CODE_OAUTH_TOKEN",
    r"sk-ant-",
    r"sk-[A-Za-z0-9]{20,}",
    r"\b[DU]U?\d{7,8}\b",   # IBKR 账户号
]


def paths(root=None):
    root = Path(root or os.environ.get("MARKET_INTEL_ROOT") or Path.home() / "claude-market-intel")
    ws = root / "ws"
    return SimpleNamespace(
        root=root, ws=ws,
        ws_snapshot=ws / "snapshot", ws_out=ws / "out", ws_reports=ws / "reports", ws_prompts=ws / "prompts",
        archive_snapshots=root / "archive" / "snapshots", archive_reports=root / "archive" / "reports",
        state=root / "state", logs=root / "logs")
