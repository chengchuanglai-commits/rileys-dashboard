"""
DeepSeek 影子分析 —— 与 Haiku 做 A/B 对比，只记录不交易。

对当天 Haiku 分析过的同一批候选股（读 {today}-{ticker}-report.json 拿到确切的 6 只），
用 DeepSeek V4-pro(deep_think) + V4-flash(quick_think) 再分析一遍，存到
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

today = os.environ.get("BACKFILL_DATE") or date.today().isoformat()   # 支持回填指定日期(测试用)
HISTORY_DIR = "dashboard/trading-signals-history"
DEEPSEEK_DIR = "dashboard/trading-signals-history/deepseek"   # 影子输出独立子目录,避免被主链路日期解析脚本扫到


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
    config["llm_provider"] = "deepseek"               # 关键：deepseek provider 用 Chat Completions(不是openai的Responses API,后者DeepSeek不支持→404)
    config["backend_url"] = "https://api.deepseek.com"
    config["deep_think_llm"] = "deepseek-v4-pro"      # V4 Pro（最强，跑多空辩论；V4 本身是推理模型，对应R1意图）
    config["quick_think_llm"] = "deepseek-v4-flash"   # V4 Flash（便宜快，轻分析）
    config["max_debate_rounds"] = 2
    config["online_tools"] = True
    # 不设 temperature（默认 None）——R1 reasoner 不接受 temperature
    ta = TradingAgentsGraph(debug=False, config=config)
    state, decision = ta.propagate(ticker, today)
    return str(decision)


def main():
    # 广撒：读选股器当天「全部」候选(~18-20只)，不再依赖 Haiku 报告(解耦+扩样本)。
    screened = f"data/screened-stocks-history/{today}.json"
    if not os.path.exists(screened):
        screened = "data/screened-stocks.json"   # 实时跑用当天最新
    try:
        with open(screened, encoding="utf-8") as f:
            sd = json.load(f)
    except Exception as e:
        print(f"[deepseek] 读不到选股器候选({screened}): {e}，跳过")
        return
    cands = sd.get("candidates", [])
    price_map = {c["ticker"]: c.get("price") for c in cands if c.get("ticker")}
    tickers = list(price_map.keys())
    if not tickers:
        print(f"[deepseek] {today} 选股器无候选，跳过")
        return
    print(f"[deepseek] 广池影子分析 {len(tickers)} 只候选: {tickers}")

    from concurrent.futures import ThreadPoolExecutor, as_completed

    def analyze(tk):
        p = price_map.get(tk)
        price = p if (p and p == p) else get_price(tk)   # NaN是真值,显式查;退回yfinance
        if price is not None and price != price:          # get_price 也可能 NaN
            price = None
        try:
            decision = run_deepseek(tk)
            action = parse_action(decision)
            print(f"[deepseek] {tk}: {action} @ ${price}")
            return {
                "ticker": tk, "action": action, "current_price": price,
                "target_price": round(price * 1.10, 2) if price else None,
                "stop_loss": round(price * 0.95, 2) if price else None,
            }
        except Exception as e:
            print(f"[deepseek] {tk} 分析失败: {e}")
            return {"ticker": tk, "action": "HOLD", "current_price": price, "error": str(e)[:200]}

    verdicts = []
    with ThreadPoolExecutor(max_workers=min(len(tickers), 6)) as ex:   # 限并发≤6 防 DeepSeek 限流
        futs = {ex.submit(analyze, tk): tk for tk in tickers}
        for f in as_completed(futs):
            r = f.result()
            if r:
                verdicts.append(r)

    # signals=进 H-DS 现实盘的(仍限4条,$2000账户realistic)；all_verdicts=全部(含HOLD)供 edge 统计
    actionable = [v for v in verdicts if v.get("action") in ("BUY", "SELL")][:4]
    out = {
        "date": today,
        "model": "deepseek-v4-pro",
        "signals": actionable,         # 进 H-DS 模拟盘的
        "all_verdicts": verdicts,      # 全部判断(含HOLD)，供分歧裁决用
    }
    os.makedirs(DEEPSEEK_DIR, exist_ok=True)
    with open(os.path.join(DEEPSEEK_DIR, f"{today}-deepseek.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"[deepseek] ✅ 影子分析完成: {len(actionable)} 条可操作 / {len(verdicts)} 总判断 → {today}-deepseek.json")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[deepseek] 影子分析整体失败(不影响主信号): {e}")
    sys.exit(0)   # 永远退出0，绝不让影子拖垮工作流
