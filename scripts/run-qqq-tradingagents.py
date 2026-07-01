"""一次性:用 TradingAgents 多智能体框架分析 QQQ(或任意ticker),中文输出。
用法: python scripts/run-qqq-tradingagents.py [TICKER]   (默认QQQ)
环境变量 MODEL=deepseek|haiku(默认haiku) 选大脑;deepseek需 DEEPSEEK_API_KEY,haiku需 ANTHROPIC_API_KEY。
跑牛熊研究员辩论+风险辩论+裁决,给最终决策。翻译用Haiku(需ANTHROPIC_API_KEY)。
"""
import os, sys, json, datetime

# 本地跑时载入 .env(CI里用secrets注入env,.env不存在就跳过)
if os.path.exists(".env"):
    for line in open(".env"):
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.strip().split("=", 1)
            os.environ.setdefault(k, v)

TICKER = (sys.argv[1] if len(sys.argv) > 1 else "QQQ").upper()
MODEL = os.environ.get("MODEL", "haiku").lower()
today = datetime.date.today().strftime("%Y-%m-%d")


def run():
    from tradingagents.graph.trading_graph import TradingAgentsGraph
    from tradingagents.default_config import DEFAULT_CONFIG
    config = DEFAULT_CONFIG.copy()
    if MODEL == "deepseek":
        # DeepSeek 是 OpenAI 兼容接口;TradingAgents 的 openai 客户端读 OPENAI_API_KEY
        os.environ["OPENAI_API_KEY"] = os.environ.get("DEEPSEEK_API_KEY", "")
        config["llm_provider"] = "deepseek"
        config["backend_url"] = "https://api.deepseek.com"
        config["deep_think_llm"] = "deepseek-v4-pro"
        config["quick_think_llm"] = "deepseek-v4-flash"
    else:
        config["llm_provider"] = "anthropic"
        config["deep_think_llm"] = "claude-haiku-4-5-20251001"
        config["quick_think_llm"] = "claude-haiku-4-5-20251001"
    config["max_debate_rounds"] = 2
    config["online_tools"] = True
    print(f"[tradingagents] 用 {MODEL} 分析 {TICKER} @ {today} ... (多智能体辩论,请稍候)")
    ta = TradingAgentsGraph(debug=False, config=config)
    state, decision = ta.propagate(TICKER, today)

    debate = state.get("investment_debate_state") or {}
    risk = state.get("risk_debate_state") or {}
    report = {
        "市场技术面": state.get("market_report") or "",
        "情绪面": state.get("sentiment_report") or "",
        "新闻面": state.get("news_report") or "",
        "基本面": state.get("fundamentals_report") or "",
        "牛熊辩论裁决": debate.get("judge_decision") or "",
        "投资计划": state.get("investment_plan") or "",
        "风险辩论裁决": risk.get("judge_decision") or "",
        "最终决策": state.get("final_trade_decision") or "",
    }

    # 中文翻译(源报告是英文)
    try:
        import anthropic
        to_tr = {k: v.strip()[:2500] for k, v in report.items() if v and v.strip()}
        client = anthropic.Anthropic()
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001", max_tokens=16000,
            messages=[{"role": "user", "content": (
                f"将以下{TICKER}分析报告各章节翻译成中文,保持专业金融术语。"
                f"严格返回相同结构JSON(只翻译值,键名不变,不加其他文字):\n\n{json.dumps(to_tr, ensure_ascii=False)}")}])
        t = resp.content[0].text
        s, e = t.find("{"), t.rfind("}") + 1
        if s >= 0:
            report.update(json.loads(t[s:e]))
    except Exception as ex:
        print(f"[warn] 翻译失败(用英文原文): {ex}")

    print("\n" + "=" * 66)
    print(f"  TradingAgents({MODEL}) 完整分析 · {TICKER} · {today}")
    print("=" * 66)
    for k, v in report.items():
        if v and v.strip():
            print(f"\n【{k}】\n{v.strip()}")
    print("\n" + "=" * 66)
    print(f"  决策: {decision}")
    print("=" * 66)

    # 飞书推送简报(最终决策+投资计划前段)
    if os.environ.get("NOTIFY_WEBHOOK"):
        fin = (report.get("最终决策") or report.get("投资计划") or str(decision)).strip()
        msg = "\n".join([f"🤖 TradingAgents({MODEL}) · {TICKER} · {today}",
                         f"决策: {decision}", "", fin[:700],
                         "（TradingAgents多智能体分析）"])
        os.environ["NOTIFY_MESSAGE"] = msg
        import runpy
        try: runpy.run_path("scripts/notify-webhook.py", run_name="__main__")
        except Exception: pass


if __name__ == "__main__":
    run()
