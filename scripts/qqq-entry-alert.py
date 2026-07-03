"""QQQ 入场价格提醒 —— 把"该加仓/该避险"的信号自动飞书推给 Riley。
触发点对齐 DeepSeek TradingAgents(2026-07-01)的裁决,不是我原来的20日线:
  - 突破 BREAKOUT $748.65 → 趋势确认,强加仓点
  - 回调 PULLBACK 到 $700-707(50日线)站稳 → 吸纳点
  - 跌破200日线 → 转熊暂停
  - 当前 ~$728 = 两者都不是,不提醒(DeepSeek说这是模糊中间地带,别加)
每次运行取最新价+均线,命中触发就飞书。状态去重不刷屏:回到区外(留缓冲)才重新武装。
由 launchd 在美股时段每小时跑。DeepSeek复检节点:7/10后重估触发位(改BREAKOUT/顶部常量)。
"""
import os, json

TICKER = "QQQ"
STATE = "data/qqq-alert-state.json"
BREAKOUT = 748.65   # DeepSeek突破触发位(6月高点)
PULLBACK = 707.0    # DeepSeek吸纳区上沿(固定,非漂移的50日线——50MA会随时间涨,用固定值才贴DeepSeek原意)
ADD_USD = 300       # 每次加仓建议额


def levels():
    import yfinance as yf
    c = yf.download(TICKER, period="260d", progress=False)["Close"]
    c = (c[TICKER] if hasattr(c, "columns") else c).dropna()
    px = float(c.iloc[-1])
    ma50 = float(c.rolling(50).mean().iloc[-1])
    ma200 = float(c.rolling(200).mean().iloc[-1])
    delta = c.diff(); up = delta.clip(lower=0).rolling(14).mean(); dn = (-delta.clip(upper=0)).rolling(14).mean()
    rsi = float((100 - 100 / (1 + up / dn)).iloc[-1])
    return px, ma50, ma200, rsi


def run():
    try:
        px, ma50, ma200, rsi = levels()
    except Exception as e:
        print(f"[qqq-alert] 取价失败,跳过: {e}"); return
    st = {}
    if os.path.exists(STATE):
        try: st = json.load(open(STATE))
        except Exception: pass

    alerts = []
    # 跌破200日线=转熊,暂停买入(最高优先)
    if px < ma200 and not st.get("bear"):
        alerts.append(f"🐻 QQQ ${px:.2f} 跌破200日线 ${ma200:.2f} → 趋势转熊,暂停买入(等站回200线上)")
        st["bear"] = True
    if px >= ma200 * 1.01:
        st["bear"] = False

    # 突破触发(DeepSeek: 破$748.65=趋势确认强加仓点)
    if px >= BREAKOUT and not st.get("breakout"):
        alerts.append(f"🚀 QQQ ${px:.2f} 突破 ${BREAKOUT} → DeepSeek触发1:趋势确认,可加 ≈${ADD_USD}(RSI {rsi:.0f})")
        st["breakout"] = True
    if px <= BREAKOUT * 0.985:
        st["breakout"] = False

    # 回调触发(DeepSeek吸纳区上沿固定$707,不用漂移的50日线)
    if px >= ma200 and px <= PULLBACK and not st.get("pullback"):
        alerts.append(f"🟢 QQQ ${px:.2f} 跌进DeepSeek吸纳区(≤${PULLBACK:.0f}) → 触发2:吸纳点,可加 ≈${ADD_USD}(RSI {rsi:.0f})")
        st["pullback"] = True
    if px >= PULLBACK * 1.01:
        st["pullback"] = False

    os.makedirs("data", exist_ok=True)
    st["last_px"], st["last_check"] = round(px, 2), __import__("time").strftime("%F %T")
    json.dump(st, open(STATE, "w"), ensure_ascii=False, indent=2)

    if not alerts:
        print(f"[qqq-alert] QQQ ${px:.2f} (50MA${ma50:.0f}/200MA${ma200:.0f}/突破位${BREAKOUT}),无新入场信号-等待")
        return
    msg = "\n".join(["📥 QQQ 入场提醒"] + alerts + ["（入场价格提醒·交易信号系统）"])
    print(msg)
    if os.environ.get("NOTIFY_WEBHOOK"):
        os.environ["NOTIFY_MESSAGE"] = msg
        import runpy
        try: runpy.run_path("scripts/notify-webhook.py", run_name="__main__")
        except Exception: pass


if __name__ == "__main__":
    run()
