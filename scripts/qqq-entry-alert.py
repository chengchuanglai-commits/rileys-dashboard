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
RECLAIM = 722.0     # DeepSeek(2026-07-08反转为Underweight后)新加仓触发:收复$722=死叉修复趋势重新确认
BREAKDOWN = 700.0   # 破位警告:跌破$700(布林下轨$695在下面)=加速下跌,别抄底该减
ADD_USD = 300       # 每次加仓建议额
# 注:2026-07-08 DeepSeek 从"低买$707"反转为"收复$722才买/跌破$700是危险"。旧的$707抄底逻辑已弃用。


def levels():
    """取当前价+今日日内低(low)+均线+RSI。用day_low判断吸纳区→哪怕瞬间探一下又弹回也抓得到。
    取价加重试(yfinance偶发抖动)。"""
    import yfinance as yf, time
    for attempt in range(3):
        try:
            d = yf.download(TICKER, period="260d", progress=False)
            c = (d["Close"][TICKER] if hasattr(d["Close"], "columns") else d["Close"]).dropna()
            lo = (d["Low"][TICKER] if hasattr(d["Low"], "columns") else d["Low"]).dropna()
            if len(c) < 200:
                raise ValueError("数据太短")
            px = float(c.iloc[-1]); day_low = float(lo.iloc[-1])
            ma50 = float(c.rolling(50).mean().iloc[-1]); ma200 = float(c.rolling(200).mean().iloc[-1])
            delta = c.diff(); up = delta.clip(lower=0).rolling(14).mean(); dn = (-delta.clip(upper=0)).rolling(14).mean()
            rsi = float((100 - 100 / (1 + up / dn)).iloc[-1])
            return px, day_low, ma50, ma200, rsi
        except Exception:
            time.sleep(3)
    raise RuntimeError("取价失败(重试3次)")


def run():
    try:
        px, day_low, ma50, ma200, rsi = levels()
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

    # 收复触发(DeepSeek新逻辑:站回$722=死叉修复趋势重新确认,可加)
    if px >= RECLAIM and not st.get("reclaim"):
        alerts.append(f"🚀 QQQ ${px:.2f} 收复 ${RECLAIM:.0f} → 死叉修复/趋势重新确认,可加 ≈${ADD_USD}(RSI {rsi:.0f})")
        st["reclaim"] = True
    if px <= RECLAIM * 0.99:
        st["reclaim"] = False

    # 破位警告(DeepSeek新逻辑:跌破$700=加速下跌,别抄底该减)
    if day_low <= BREAKDOWN and not st.get("breakdown"):
        alerts.append(f"🔻 QQQ 现${px:.2f}(今日低${day_low:.2f}) 跌破 ${BREAKDOWN:.0f} → 破位!别抄底(布林下轨$695在下面)")
        st["breakdown"] = True
    if px >= BREAKDOWN * 1.015:
        st["breakdown"] = False

    os.makedirs("data", exist_ok=True)
    st["last_px"], st["last_check"] = round(px, 2), __import__("time").strftime("%F %T")
    json.dump(st, open(STATE, "w"), ensure_ascii=False, indent=2)

    if not alerts:
        print(f"[qqq-alert] QQQ ${px:.2f}(今日低${day_low:.2f}) 收复${RECLAIM:.0f}加/破${BREAKDOWN:.0f}减/突破${BREAKOUT:.0f},无新信号-等待")
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
