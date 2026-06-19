"""
B-AI 的"大脑"——DeepSeek 分析**多因子选股器选出的候选**(中大盘),给 BUY/SELL/HOLD。
与 B-quant 同一批候选(读 screened-multifactor.json),区别只在"量化规则决定 vs AI决定"→隔离"AI大脑加不加分"。

读 data/screened-multifactor.json 的 buy+sell 候选 → DeepSeek(V4) 逐只分析 → 归档
data/multifactor-ai-history/{date}.json。完全围栏(失败退出0,绝不拖垮主流程)。
"""
import os, sys, json
from datetime import date

if not os.environ.get("DEEPSEEK_API_KEY"):
    print("[bai] 无 DEEPSEEK_API_KEY，跳过"); sys.exit(0)
os.environ["OPENAI_API_KEY"] = os.environ["DEEPSEEK_API_KEY"]

today = os.environ.get("BACKFILL_DATE") or date.today().isoformat()
SRC = "data/screened-multifactor.json"
OUT_DIR = "data/multifactor-ai-history"


def parse_action(s):
    d = (s or "").upper()
    if "BUY" in d or "OVERWEIGHT" in d or "STRONG BUY" in d: return "BUY"
    if "SELL" in d or "UNDERWEIGHT" in d or "REDUCE" in d or "STRONG SELL" in d: return "SELL"
    return "HOLD"


def run_deepseek(ticker):
    from tradingagents.graph.trading_graph import TradingAgentsGraph
    from tradingagents.default_config import DEFAULT_CONFIG
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = "deepseek"
    config["backend_url"] = "https://api.deepseek.com"
    config["deep_think_llm"] = "deepseek-v4-pro"
    config["quick_think_llm"] = "deepseek-v4-flash"
    config["max_debate_rounds"] = 2
    config["online_tools"] = True
    ta = TradingAgentsGraph(debug=False, config=config)
    _, decision = ta.propagate(ticker, today)
    return str(decision)


def main():
    if not os.path.exists(SRC):
        print(f"[bai] 无 {SRC},先跑 screen-multifactor.py,跳过"); return
    d = json.load(open(SRC))
    cands = {}  # ticker -> (multifactor建议方向, price)
    for x in d.get("buy", []): cands[x["ticker"]] = ("BUY", x.get("price"))
    for x in d.get("sell", []): cands[x["ticker"]] = ("SELL", x.get("price"))
    tickers = list(cands.keys())
    if not tickers:
        print("[bai] 多因子无候选,跳过"); return
    print(f"[bai] DeepSeek 分析 {len(tickers)} 只多因子候选: {tickers}")

    from concurrent.futures import ThreadPoolExecutor, as_completed

    def analyze(tk):
        mf_action, price = cands[tk]
        try:
            action = parse_action(run_deepseek(tk))
            print(f"[bai] {tk}: AI={action} (多因子={mf_action}) @ ${price}")
            return {"ticker": tk, "action": action, "mf_action": mf_action, "current_price": price}
        except Exception as e:
            print(f"[bai] {tk} 失败: {e}")
            return {"ticker": tk, "action": "HOLD", "mf_action": mf_action, "current_price": price, "error": str(e)[:200]}

    verdicts = []
    with ThreadPoolExecutor(max_workers=min(len(tickers), 6)) as ex:
        for f in as_completed({ex.submit(analyze, tk): tk for tk in tickers}):
            r = f.result()
            if r: verdicts.append(r)

    out = {"date": today, "model": "deepseek-v4-pro",
           "signals": [v for v in verdicts if v.get("action") in ("BUY", "SELL")],
           "all_verdicts": verdicts}
    os.makedirs(OUT_DIR, exist_ok=True)
    json.dump(out, open(os.path.join(OUT_DIR, f"{today}.json"), "w"), ensure_ascii=False, indent=2)
    print(f"[bai] ✅ {len(out['signals'])} 条可操作 / {len(verdicts)} 总判断 → {today}.json")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[bai] 整体失败(不影响主流程): {e}")
    sys.exit(0)
