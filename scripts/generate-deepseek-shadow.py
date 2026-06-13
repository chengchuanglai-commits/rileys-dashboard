"""
DeepSeek 影子分析 —— 与 Haiku 做 A/B 对比，只记录不交易。

对当天 Haiku 分析过的同一批候选股（读 {today}-{ticker}-report.json 拿到确切的 6 只），
用 DeepSeek R1(deep_think) + V3(quick_think) 再分析一遍，存到
dashboard/trading-signals-history/{today}-deepseek.json。

设计要点：
- 完全独立、完全围栏：任何失败只打印 + 退出码 0，绝不影响 Haiku 主信号工作流。
- 读主信号的 report 文件拿标的 → 保证和 Haiku 分析的是同一批（配对对比有效）。
- gated：无 DEEPSEEK_API_KEY 则直接跳过。
- 只记录信号，不进任何真实模拟盘（交易盈利对比由 backfill-portfolio-hds.py 用 H 规则单独跑）。
"""
import os, sys, json, glob
from datetime import date

if not os.environ.get("DEEPSEEK_API_KEY"):
    print("[deepseek] 无 DEEPSEEK_API_KEY，跳过影子分析")
    sys.exit(0)
# TradingAgents 的 openai 客户端读 OPENAI_API_KEY；DeepSeek 是 OpenAI 兼容接口
os.environ["OPENAI_API_KEY"] = os.environ["DEEPSEEK_API_KEY"]

today = date.today().isoformat()
HISTORY_DIR = "dashboard/trading-signals-history"


def get_price(ticker):
    import yfinance as yf
    try:
        df = yf.Ticker(ticker).history(period="5d")
        return round(float(df["Close"].iloc[-1]), 2) if not df.empty else None
    except Exception:
        return None


def parse_action(s):
    d = (s or "").upper()
    if 'BUY' in d or 'OVERWEIGHT' in d or 'STRONG BUY' in d:
        return 'BUY'
    if 'SELL' in d or 'UNDERWEIGHT' in d or 'REDUCE' in d or 'STRONG SELL' in d:
        return 'SELL'
    return 'HOLD'


def run_deepseek(ticker):
    from tradingagents.graph.trading_graph import TradingAgentsGraph
    from tradingagents.default_config import DEFAULT_CONFIG
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = "openai"                 # OpenAI 兼容客户端
    config["backend_url"] = "https://api.deepseek.com"
    config["deep_think_llm"] = "deepseek-reasoner"    # R1，跑多空辩论
    config["quick_think_llm"] = "deepseek-chat"       # V3，便宜快
    config["max_debate_rounds"] = 2
    config["online_tools"] = True
    # 不设 temperature（默认 None）——R1 reasoner 不接受 temperature
    ta = TradingAgentsGraph(debug=False, config=config)
    state, decision = ta.propagate(ticker, today)
    return str(decision)


def main():
    # 读主信号当天分析的标的（确切同一批 6 只）
    reports = glob.glob(os.path.join(HISTORY_DIR, f"{today}-*-report.json"))
    tickers = []
    for p in reports:
        base = os.path.basename(p)
        # {today}-{ticker}-report.json  且排除 -deepseek-report
        if base.endswith("-report.json") and "-deepseek" not in base:
            tk = base[len(today) + 1:-len("-report.json")]
            if tk and tk not in tickers:
                tickers.append(tk)
    if not tickers:
        print(f"[deepseek] 没找到 {today} 的主信号 report 文件，跳过（Haiku 可能没跑/无候选）")
        return
    print(f"[deepseek] 对同一批 {len(tickers)} 只候选做影子分析: {tickers}")

    from concurrent.futures import ThreadPoolExecutor, as_completed

    def analyze(tk):
        try:
            decision = run_deepseek(tk)
            action = parse_action(decision)
            price = get_price(tk)
            print(f"[deepseek] {tk}: {action} @ ${price}")
            return {
                "ticker": tk, "action": action, "current_price": price,
                "target_price": round(price * 1.10, 2) if price else None,
                "stop_loss": round(price * 0.95, 2) if price else None,
            }
        except Exception as e:
            print(f"[deepseek] {tk} 分析失败: {e}")
            return {"ticker": tk, "action": "HOLD", "current_price": get_price(tk), "error": str(e)[:200]}

    verdicts = []
    with ThreadPoolExecutor(max_workers=len(tickers)) as ex:
        futs = {ex.submit(analyze, tk): tk for tk in tickers}
        for f in as_completed(futs):
            r = f.result()
            if r:
                verdicts.append(r)

    # 可操作信号(BUY/SELL)，口径同主信号——不发 HOLD
    actionable = [v for v in verdicts if v.get("action") in ("BUY", "SELL")][:4]
    out = {
        "date": today,
        "model": "deepseek-reasoner",
        "signals": actionable,         # 进 H-DS 模拟盘的
        "all_verdicts": verdicts,      # 全部判断(含HOLD)，供分歧裁决用
    }
    os.makedirs(HISTORY_DIR, exist_ok=True)
    with open(os.path.join(HISTORY_DIR, f"{today}-deepseek.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"[deepseek] ✅ 影子分析完成: {len(actionable)} 条可操作 / {len(verdicts)} 总判断 → {today}-deepseek.json")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[deepseek] 影子分析整体失败(不影响主信号): {e}")
    sys.exit(0)   # 永远退出0，绝不让影子拖垮工作流
