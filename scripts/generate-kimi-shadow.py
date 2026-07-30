"""
Kimi 影子分析 —— 与 DeepSeek 做信号引擎 A/B(2026-07-30 Riley 立项,方案见 memory project-kimi-ab-test)。

严格配对设计:只读 deepseek-broad 当天已提交的 data/screened-stocks-history/{today}.json
(同一批候选、同分析框架、同出场规则,唯一变量=大脑)。当天候选文件不存在→直接跳过,
绝不自己重新选股(那会破坏配对,变成两个变量)。

- 完全围栏:任何失败只打印+退出0。gated:无 KIMI_API_KEY 直接跳过。
- 输出 dashboard/trading-signals-history/kimi/{today}-kimi.json,由 backfill-portfolio-kimi.py 记账。
- Moonshot 是 OpenAI 兼容接口;走 TradingAgents 的 deepseek provider(Chat Completions 路径,
  openai provider 的 Responses API 路径 Moonshot 不支持,同 DeepSeek 的坑)。
"""
import os, sys, json
from datetime import date

if not os.environ.get("KIMI_API_KEY"):
    print("[kimi] 无 KIMI_API_KEY，跳过影子分析")
    sys.exit(0)
# 锁定版 TradingAgents 原生支持 kimi provider,key 变量名=MOONSHOT_API_KEY(api_key_env.py)
os.environ["MOONSHOT_API_KEY"] = os.environ["KIMI_API_KEY"]

today = os.environ.get("BACKFILL_DATE") or date.today().isoformat()   # 支持指定日期(测试/补跑用)
KIMI_DIR = "dashboard/trading-signals-history/kimi"   # 独立子目录,与 deepseek/ 平行


def parse_action(s):
    d = (s or "").upper()
    if 'BUY' in d or 'OVERWEIGHT' in d or 'STRONG BUY' in d:
        return 'BUY'
    if 'SELL' in d or 'UNDERWEIGHT' in d or 'REDUCE' in d or 'STRONG SELL' in d:
        return 'SELL'
    return 'HOLD'


def run_kimi(ticker):
    from tradingagents.graph.trading_graph import TradingAgentsGraph
    from tradingagents.default_config import DEFAULT_CONFIG
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = "kimi"                   # 原生 provider(勿走deepseek壳:其key校验只认DEEPSEEK_API_KEY且实测env注入不生效)
    config["backend_url"] = "https://api.moonshot.cn/v1"   # 必须覆盖:spec默认.ai国际版,Riley的key是.cn国内版,两边账户不通
    config["deep_think_llm"] = "kimi-k3"              # Riley拍板方案B(2026-07-30):K3旗舰跑多空深度辩论
    config["quick_think_llm"] = "kimi-k2.6"           # K2.6跑轻分析,镜像deepseek pro/flash分档,控成本~¥5-10/天
    config["max_debate_rounds"] = 2                   # 与 deepseek 影子完全一致
    config["online_tools"] = True
    # 不设 temperature——K2.6 是推理模型,与 R1 同理
    ta = TradingAgentsGraph(debug=False, config=config)
    state, decision = ta.propagate(ticker, today)
    return str(decision)


def main():
    # 严格配对:只认 deepseek-broad 当天提交的定日期候选文件,没有=不跑(保配对有效性)
    screened = f"data/screened-stocks-history/{today}.json"
    if not os.path.exists(screened):
        print(f"[kimi] {screened} 不存在(deepseek-broad 未跑/未提交)→跳过,保持严格配对")
        return
    with open(screened, encoding="utf-8") as f:
        sd = json.load(f)
    cands = sd.get("candidates", [])
    price_map = {c["ticker"]: c.get("price") for c in cands if c.get("ticker")}
    tickers = list(price_map.keys())
    if not tickers:
        print(f"[kimi] {today} 候选为空，跳过")
        return
    print(f"[kimi] 配对影子分析 {len(tickers)} 只候选: {tickers}")

    from concurrent.futures import ThreadPoolExecutor, as_completed

    def analyze(tk):
        price = price_map.get(tk)
        if price is not None and price != price:
            price = None
        try:
            decision = run_kimi(tk)
            action = parse_action(decision)
            print(f"[kimi] {tk}: {action} @ ${price}")
            return {
                "ticker": tk, "action": action, "current_price": price,
                "target_price": round(price * 1.10, 2) if price else None,
                "stop_loss": round(price * 0.95, 2) if price else None,
            }
        except Exception as e:
            print(f"[kimi] {tk} 分析失败: {e}")
            return {"ticker": tk, "action": "HOLD", "current_price": price, "error": str(e)[:200]}

    verdicts = []
    with ThreadPoolExecutor(max_workers=min(len(tickers), 3)) as ex:   # 并发≤3:Moonshot 新账户 RPM/TPM 比 DeepSeek 紧
        futs = {ex.submit(analyze, tk): tk for tk in tickers}
        for f in as_completed(futs):
            r = f.result()
            if r:
                verdicts.append(r)

    if verdicts and all(v.get("error") for v in verdicts):
        print(f"[kimi] ❌ 全部{len(verdicts)}只分析失败,不写归档(防垃圾数据入台账);首个错误: {verdicts[0]['error'][:150]}")
        return

    actionable = [v for v in verdicts if v.get("action") in ("BUY", "SELL")][:4]   # 与 H-DS 同帽
    out = {
        "date": today,
        "model": "kimi-k3+k2.6",
        "signals": actionable,
        "all_verdicts": verdicts,
    }
    os.makedirs(KIMI_DIR, exist_ok=True)
    with open(os.path.join(KIMI_DIR, f"{today}-kimi.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"[kimi] ✅ 影子分析完成: {len(actionable)} 条可操作 / {len(verdicts)} 总判断 → {today}-kimi.json")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[kimi] 影子分析整体失败(不影响其他管线): {e}")
    sys.exit(0)   # 永远退出0，绝不拖垮工作流
