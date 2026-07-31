"""QQQ指数核心托管执行器(2026-07-29建,Riley批"接管":大部分交易时间他在睡觉)。
只买不卖:①reclaim信号买1批 ②深跌阶梯(距52周高点-10/-15/-20%)每档买1批,每档只触发一次
③永不卖出(择时卖出已被证明输34pp,不写进代码=永不发生)。
标的:新买入=QQQM(同纳指100,费率更低,整股~$278≈单批节奏;API禁碎股→QQQ整股太贵)。
硬约束:月度预算帽$700 / 指数核心总市值帽$6000 / 可用资金地板$500(护hdstr额度) / kill-switch必读。
用法: python3 -m scripts.ibkr.qqq_dca_exec   (run.sh trade_open 段每日调用,QQQDCA_ARM=1才动真钱)
状态: data/qqq-dca-state.json  协议: 见memory+飞书预注册
"""
import json, os, time

from ib_insync import IB, Stock, LimitOrder

STATE = "data/qqq-dca-state.json"
KS = "data/kill-switches.json"
ALERT = "data/qqq-alert-state.json"

ARM = os.environ.get("QQQDCA_ARM", "0") == "1"
REAL_ACCOUNT = os.environ.get("QQQDCA_ACCOUNT", "")
PORT = int(os.environ.get("QQQDCA_PORT", "4001"))
BUY_SYM = "QQQM"
BATCH_SHARES = 1
MONTHLY_CAP_USD = 700.0
CORE_VALUE_CAP = 6000.0     # QQQ+QQQM合计市值帽
FUNDS_FLOOR = 500.0         # 买后可用资金不得低于此(护hdstr)
TIERS = [-10.0, -15.0, -20.0]   # 距52周高点%,每档一批
LIMIT_BUFFER = 0.0015


def load(p, d):
    try: return json.load(open(p))
    except Exception: return d


def notify(msg):
    print(msg)
    if os.environ.get("NOTIFY_WEBHOOK"):
        os.environ["NOTIFY_MESSAGE"] = msg
        import runpy
        try: runpy.run_path("scripts/notify-webhook.py", run_name="__main__")
        except Exception: pass


def main():
    st = load(STATE, {"buys": [], "fired_tiers": {}, "reclaim_bought_epoch": None})
    ks = load(KS, {})
    if isinstance(ks.get("qqq_dca"), dict) and ks["qqq_dca"].get("halted"):
        print("[qqq-dca] kill-switch停用,跳过"); return
    month = time.strftime("%Y-%m")
    spent = sum(b["usd"] for b in st["buys"] if b["date"][:7] == month)

    # 信号与价格
    import yfinance as yf
    q = yf.Ticker("QQQ").history(period="1y")
    if q.empty: print("[qqq-dca] 无行情,跳过"); return
    px = float(q["Close"].iloc[-1]); hi52 = float(q["Close"].max())
    dd = (px / hi52 - 1) * 100
    alert = load(ALERT, {})
    epoch = str(round(hi52))          # 创新高=新纪元,阶梯重置
    fired = st["fired_tiers"].get(epoch, [])

    reasons = []
    if alert.get("reclaim") and st.get("reclaim_bought_epoch") != epoch:
        reasons.append(("reclaim", f"收复$722趋势修复"))
    for t in TIERS:
        if dd <= t and t not in fired:
            reasons.append((t, f"距高点{dd:.1f}%触及{t:.0f}%档"))
            break   # 一晚最多补一档,防单日暴跌连买穿预算

    if not reasons:
        print(f"[qqq-dca] 无触发(距高点{dd:.1f}%,本月已用${spent:.0f})"); return

    reason_key, reason_txt = reasons[0]
    # 预算三闸
    ib = IB()
    for attempt in range(3):   # 网关每日自动重启~21:30撞批次(7/30/7/31实炸),重试3轮×等5分钟
        if attempt: time.sleep(300)
        try:
            ib.connect("127.0.0.1", PORT, clientId=63, timeout=15); break
        except Exception as e:
            if attempt == 2:
                notify(f"🛑 qqq-dca:连不上网关,3轮重试后放弃({e})"); return
    acct = (ib.managedAccounts() or [""])[0]
    if ARM and (not REAL_ACCOUNT or acct != REAL_ACCOUNT or acct.startswith("DU")):
        notify(f"🛑 qqq-dca拒跑:账户{acct}与配置不符"); ib.disconnect(); return
    if not ARM and not acct.startswith("DU"):
        notify(f"🛑 qqq-dca拒跑:未arm却连到真钱{acct}"); ib.disconnect(); return

    ct = Stock(BUY_SYM, "SMART", "USD"); ib.qualifyContracts(ct)
    ib.reqMarketDataType(3)
    tkr = ib.reqMktData(ct, "", False, False); ib.sleep(3)
    bpx = tkr.last if (tkr.last and tkr.last == tkr.last) else tkr.close
    ib.cancelMktData(ct)
    if not bpx or bpx != bpx:
        notify("🛑 qqq-dca:拿不到QQQM报价,跳过"); ib.disconnect(); return
    cost = float(bpx) * BATCH_SHARES
    core_mv = sum(abs(p.position) * (float(bpx) if p.contract.symbol == BUY_SYM else px)
                  for p in ib.positions(acct) if p.contract.symbol in ("QQQ", "QQQM"))
    av = {v.tag: float(v.value) for v in ib.accountValues(acct) if v.tag == "AvailableFunds"}
    funds = av.get("AvailableFunds", 0)
    block = None
    if spent + cost > MONTHLY_CAP_USD: block = f"月帽(已用${spent:.0f}+${cost:.0f}>{MONTHLY_CAP_USD:.0f})"
    elif core_mv + cost > CORE_VALUE_CAP: block = f"总仓帽(现${core_mv:.0f})"
    elif funds - cost < FUNDS_FLOOR: block = f"资金地板(可用${funds:.0f})"
    if block:
        notify(f"⏸️ qqq-dca:触发{reason_txt}但被{block}拦下——纪律优先"); ib.disconnect(); return

    lmt = round(float(bpx) * (1 + LIMIT_BUFFER), 2)
    o = LimitOrder("BUY", BATCH_SHARES, lmt); o.tif = "DAY"
    tr = ib.placeOrder(ct, o); ib.sleep(5)
    stt = tr.orderStatus.status
    if stt in ("Cancelled", "ApiCancelled", "Inactive"):
        why = next((l.message[:50] for l in tr.log if l.errorCode), stt)
        notify(f"🛑 qqq-dca:买入被拒({why})"); ib.disconnect(); return
    # 记账(以委托为准;成交细节次日对账)
    st["buys"].append({"date": time.strftime("%Y-%m-%d"), "sym": BUY_SYM, "shares": BATCH_SHARES,
                       "usd": round(cost, 2), "reason": reason_txt, "limit": lmt})
    if reason_key == "reclaim":
        st["reclaim_bought_epoch"] = epoch
    else:
        st["fired_tiers"].setdefault(epoch, []).append(reason_key)
    json.dump(st, open(STATE, "w"), ensure_ascii=False, indent=1)
    ib.disconnect()
    notify(f"🤖💰 QQQ核心托管买入: {BUY_SYM}×{BATCH_SHARES} ≈${cost:.0f} [{tr.orderStatus.status}]\n"
           f"触发: {reason_txt} (QQQ ${px:.2f},距高点{dd:.1f}%)\n"
           f"本月已投 ${spent + cost:.0f}/{MONTHLY_CAP_USD:.0f} | 核心市值 ${core_mv + cost:.0f}/{CORE_VALUE_CAP:.0f}\n"
           f"（QQQ托管·只买不卖·系统自动）")


if __name__ == "__main__":
    main()
