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
BACKSTOP = 648.43   # Riley 2026-11-03 定的防线 B:52周高点 762.86 × 0.85(−15%)。只提醒,不自动下单
FAIL_ALERT_N = 3    # 连续取价失败几次就飞书报警(每 30 分钟一次,3 次≈1.5 小时没人盯防线)


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
            return px, day_low, ma50, ma200, rsi, c
        except Exception:
            time.sleep(3)
    return levels_fmp()


def _fmp(path):
    """FMP stable API。key 从仓库外的 .secrets/fmp.env 读(launchd 环境里没有这个变量)。"""
    import urllib.request
    key = os.environ.get("FMP_API_KEY", "")
    if not key and os.path.exists(".secrets/fmp.env"):
        key = open(".secrets/fmp.env").read().split('FMP_API_KEY="')[1].split('"')[0]
    url = f"https://financialmodelingprep.com/stable/{path}&apikey={key}"
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30))


def levels_fmp():
    """yfinance 失败时的备用源(2026-11-03 加:yfinance 近月频繁返回空,防线不能因此失明)。"""
    import datetime, pandas as pd
    since = (datetime.date.today() - datetime.timedelta(days=420)).isoformat()
    h = pd.DataFrame(_fmp(f"historical-price-eod/full?symbol={TICKER}&from={since}"))
    h["date"] = pd.to_datetime(h["date"]); h = h.set_index("date").sort_index()
    c, lo = h["close"].astype(float), h["low"].astype(float)
    q = _fmp(f"quote?symbol={TICKER}")[0]
    day = pd.Timestamp(datetime.datetime.fromtimestamp(q["timestamp"]).date())
    c.loc[day], lo.loc[day] = float(q["price"]), float(q["dayLow"])   # 盘中报价覆盖/追加当天
    if len(c) < 200:
        raise RuntimeError("FMP 数据太短")
    px, day_low = float(c.iloc[-1]), float(lo.iloc[-1])
    ma50 = float(c.rolling(50).mean().iloc[-1]); ma200 = float(c.rolling(200).mean().iloc[-1])
    delta = c.diff(); up = delta.clip(lower=0).rolling(14).mean(); dn = (-delta.clip(upper=0)).rolling(14).mean()
    rsi = float((100 - 100 / (1 + up / dn)).iloc[-1])
    return px, day_low, ma50, ma200, rsi, c


def confirm_low(day_low):
    """防线命中时用另一个源交叉验证(铁律:行情必须交叉验证,防 yfinance 那种脏数据误报)。
    返回另一源的今日低点;取不到返回 None(此时照常报警,但注明单一来源)。"""
    try:
        return float(_fmp(f"quote?symbol={TICKER}")[0]["dayLow"])
    except Exception:
        return None


def run():
    st = {}
    if os.path.exists(STATE):
        try: st = json.load(open(STATE))
        except Exception: pass
    try:
        px, day_low, ma50, ma200, rsi, c = levels()
    except Exception as e:
        st["fail_n"] = st.get("fail_n", 0) + 1
        print(f"[qqq-alert] 取价失败(连续第{st['fail_n']}次),跳过: {e}")
        if st["fail_n"] == FAIL_ALERT_N:
            notify(f"⚠️ QQQ 价格提醒连续 {FAIL_ALERT_N} 次取价失败(yfinance 和 FMP 都取不到),"
                   f"${BACKSTOP:.0f} 防线暂时没人盯。系统没有做任何交易;恢复后会自动继续。")
        json.dump(st, open(STATE, "w"), ensure_ascii=False, indent=2)
        return
    st["fail_n"] = 0

    alerts = []
    # 防线 B(Riley 2026-11-03):用今日低点判断,盘中探到也算;回到防线上方 3% 才重新武装
    if day_low <= BACKSTOP and not st.get("backstop"):
        other = confirm_low(day_low)
        if other is not None and other > BACKSTOP * 1.01:
            print(f"[qqq-alert] 防线疑似误报:主源今日低 ${day_low:.2f},FMP 今日低 ${other:.2f},不报警")
        else:
            src = f"FMP 交叉验证今日低 ${other:.2f}" if other is not None else "⚠️只有单一数据源,请在 IBKR 核对"
            alerts.append(f"🛑 QQQ 触及防线 ${BACKSTOP:.0f}(现 ${px:.2f},今日低 ${day_low:.2f};{src})\n"
                          f"   这是你 11/3 定的防线 B(距52周高点 −15%):应降杠杆到约 1 倍=卖 3 股 QQQM 还借款。\n"
                          f"   系统没有自动下单,等你回复批准后执行。")
            st["backstop"] = True
    if px >= BACKSTOP * 1.03:
        st["backstop"] = False
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

    # ── 杠杆闸门信号(1.5x 真钱保证金/paper腿用;与 lev_engine 同逻辑)──
    # 只在闸门档位切换时提醒:跌破200线/波动>30%→降杠回1x;连站5天+波动正常→可加杠回1.5x
    try:
        import sys as _sys; _sys.path.insert(0, "scripts")
        from lev_engine import gate_signal
        g = gate_signal(c)
        cur_lev = f"{g['target']}x"; prev_lev = st.get("lev_state")
        if prev_lev is None:
            st["lev_state"] = cur_lev            # 首次静默建基线,不刷屏
        elif cur_lev != prev_lev:
            if g["target"] < 1.5:
                why = "跌破200日线" if not g["above_ma"] else ("波动>30%" if g["highv"] else f"未连站{g['confirm_days']}天")
                alerts.append(f"⚙️🔻 杠杆闸门 降杠→1.0x({why};QQQ ${g['price']}/200线 ${g['ma']},20日波动 {g['vol_ann']*100:.0f}%)\n   Riley 11/3 决定:闸门触发先不卖,以 ${BACKSTOP:.0f} 防线为准(仅提醒)")
            else:
                armed = "★这就是启动真钱小步上杠的绿灯(前提:IBKR保证金账户已开+你确认扛得住深坑)" if not st.get("lev_realmoney") else "已在杠杆:借0.5x加仓QQQ回到1.5x"
                alerts.append(f"⚙️🚀🟢 杠杆闸门 →1.5x(连站200线{g['streak']}天+波动{g['vol_ann']*100:.0f}%正常)\n   {armed}")
            st["lev_state"] = cur_lev
    except Exception as _e:
        print(f"[qqq-alert] 杠杆闸门信号跳过: {_e}")

    os.makedirs("data", exist_ok=True)
    st["last_px"], st["last_check"] = round(px, 2), __import__("time").strftime("%F %T")
    json.dump(st, open(STATE, "w"), ensure_ascii=False, indent=2)

    if not alerts:
        print(f"[qqq-alert] QQQ ${px:.2f}(今日低${day_low:.2f}) 收复${RECLAIM:.0f}加/破${BREAKDOWN:.0f}减/突破${BREAKOUT:.0f},无新信号-等待")
        return
    notify("\n".join(["📥 QQQ 入场提醒"] + alerts + ["（入场价格提醒·交易信号系统）"]))


def notify(msg):
    print(msg)
    if os.environ.get("NOTIFY_WEBHOOK"):
        os.environ["NOTIFY_MESSAGE"] = msg
        import runpy
        try: runpy.run_path("scripts/notify-webhook.py", run_name="__main__")
        except Exception: pass


if __name__ == "__main__":
    run()
