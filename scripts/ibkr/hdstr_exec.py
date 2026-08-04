"""hdstr 真钱执行层(2026-07-22建,Riley批:周一直接真钱+自动执行)。
策略:DeepSeek信号 + 移动止损(IBKR服务器端TRAIL 4% GTC,睡觉安全) + 10交易日超时平仓。

安全架构(层层设防):
  ①账户路由:HDSTR_ARM=1才允许真钱账户;未arm时只接受DU*(paper)。账户不匹配=直接拒跑。
  ②kill-switch:开单前必读data/kill-switches.json(tripwire破线/gate FAIL→停新仓)。
  ③gate联动:data/hds-gate.json verdict=FAIL→停新仓(试运行中止,存量由TRAIL自然出清)。
  ④tradability硬过滤:OTC名单/ADV<$5M/做空shortable无数据→跳过。
  ⑤仓位:$500/仓,最多4并发;入场marketable limit DAY(不成交不追)。
  ⑥自愈:每晚审计所有在手仓的TRAIL保护单,缺失即补挂(paper体检期主batch全局撤单会扫掉GTC单,靠这条活)。
用法: python3 -m scripts.ibkr.hdstr_exec open|close   (run.sh trade_open/trade_close 调用)
状态: data/hdstr-trial.json  日志打印由run.sh收集。
"""
import json, os, sys, time
from datetime import datetime, timedelta

from ib_insync import Stock, LimitOrder, Order
from scripts.ibkr.client import connect as _connect_any


def connect(client_id):
    """端口路由:HDSTR_PORT指定则只连它(真钱=4001第二网关,防撞进paper);未指定走默认(paper体检)。
    真钱口重试3轮×等5分钟:网关每日自动重启~21:30正撞开盘批次(7/27/7/30/7/31三炸),
    重启后端口几分钟内恢复,等一等就好;幂等安全(状态文件防重复开仓)。"""
    port = int(os.environ.get("HDSTR_PORT", "0"))
    if not port:
        return _connect_any(client_id=client_id, retries=2, retry_wait=6)
    from ib_insync import IB
    for attempt in range(3):
        if attempt:
            print(f"[hdstr] 第{attempt+1}次尝试连{port}(等300s后,网关可能在自动重启)")
            time.sleep(300)
        ib = IB()
        try:
            ib.connect("127.0.0.1", port, clientId=client_id, timeout=15)
            return ib, port
        except Exception as e:
            print(f"[hdstr] 连{port}失败: {e}")
    return None, None

STATE = "data/hdstr-trial.json"
KS = "data/kill-switches.json"
GATE = "data/hds-gate.json"
UNTRADABLE = "data/borrow-untradable.json"
DS_DIR = "dashboard/trading-signals-history/deepseek"

ARM = os.environ.get("HDSTR_ARM", "0") == "1"          # 1=允许真钱账户
REAL_ACCOUNT = os.environ.get("HDSTR_ACCOUNT", "")      # 真钱账户号(arm时必须匹配)
POS_PCT = 0.25            # 单仓=试运行净值的25%(×4并发=满仓)。Riley铁律2026-08-01:真钱必须复利,绝不固定金额
TRIAL_BASE_USD = 2000.0   # 复利净值算不出时的回退基准(=预注册本金)
SIZING_FREEZE_USD = 1200.0  # gate裁决前仓位基准上限(2026-08-04 Riley批:入金先行至全仓$3000,
                            # 但加码严格等gate PASS——先例2026-07-27"跳过预注册加码=四周后凭数据谈"。
                            # verdict=PASS当天自动解冻按真实净值复利;FAIL则entries_halted已接管)
MAX_CONC = 4
TRAIL_PCT = 4.0
MAX_HOLD_TD = 10
GAP_FILTER_PCT = 1.0
MIN_ADV = 5_000_000
LIMIT_BUFFER = 0.015


def load(p, d):
    try: return json.load(open(p))
    except Exception: return d


def save_state(st):
    json.dump(st, open(STATE, "w"), ensure_ascii=False, indent=1)


def notify(msg):
    print(msg)
    if os.environ.get("NOTIFY_WEBHOOK"):
        os.environ["NOTIFY_MESSAGE"] = msg
        import runpy
        try: runpy.run_path("scripts/notify-webhook.py", run_name="__main__")
        except Exception: pass


def guard_account(ib):
    """账户白名单:防拿错网关。返回账户号或None(拒跑)。"""
    accts = ib.managedAccounts()
    acct = accts[0] if accts else ""
    if ARM:
        if not REAL_ACCOUNT or acct != REAL_ACCOUNT:
            notify(f"🛑 hdstr执行拒跑:ARM=1但账户{acct}≠配置{REAL_ACCOUNT}"); return None
        if acct.startswith("DU"):
            notify(f"🛑 hdstr执行拒跑:ARM=1但连到paper账户{acct}"); return None
    else:
        if not acct.startswith("DU"):
            notify(f"🛑 hdstr执行拒跑:未arm却连到真钱账户{acct}(防呆)"); return None
    return acct


def entries_halted():
    ks = load(KS, {})
    h = ks.get("hds_new_entries", {})
    if isinstance(h, dict) and h.get("halted"):
        return f"kill-switch: {h.get('reason','')}"
    g = load(GATE, {})
    if g.get("verdict") == "FAIL":
        return "gate裁决FAIL,试运行中止(存量由TRAIL出清)"
    return None


def latest_signals():
    files = sorted(f for f in os.listdir(DS_DIR) if f.endswith("-deepseek.json"))
    if not files: return None, []
    day = files[-1].replace("-deepseek.json", "")
    return day, load(os.path.join(DS_DIR, files[-1]), {}).get("signals", [])


def adv_ok(tk):
    try:
        import yfinance as yf
        h = yf.Ticker(tk).history(period="1mo")
        if h.empty: return False
        return float((h["Close"] * h["Volume"]).tail(20).mean()) >= MIN_ADV
    except Exception:
        return False


def snap_price(ib, ct):
    ib.reqMarketDataType(3)
    t = ib.reqMktData(ct, "", False, False); ib.sleep(2.5)
    px = t.last if (t.last and t.last == t.last) else (t.close if (t.close and t.close == t.close) else None)
    ib.cancelMktData(ct)
    return float(px) if px else None


def trial_equity_usd(ib, acct):
    """hdstr复利净值(USD)=账户NAV折美元-指数核心(QQQ/QQQM)市值。含已实现+未实现,天然复利。
    任何环节算不出→回退预注册基准$2000(宁可保守也不停摆)。"""
    try:
        vals = {}
        for v in ib.accountValues(acct):
            if v.tag == "NetLiquidation" and v.currency == "CAD": vals["nav_cad"] = float(v.value)
            if v.tag == "ExchangeRate" and v.currency == "USD": vals["usdcad"] = float(v.value)
        nav_usd = vals["nav_cad"] / vals["usdcad"]
        core = 0.0
        for p in ib.positions(acct):
            if p.contract.symbol in ("QQQ", "QQQM"):
                ct = Stock(p.contract.symbol, "SMART", "USD")
                px = snap_price(ib, ct) if ib.qualifyContracts(ct) else None
                core += abs(p.position) * (px or p.avgCost)
        eq = nav_usd - core
        if not (500 <= eq <= 20000):   # 数据错乱护栏(FX缺失/NAV异常)
            raise ValueError(f"equity异常{eq:.0f}")
        return eq
    except Exception as e:
        print(f"[hdstr] 复利净值计算失败({e}),回退${TRIAL_BASE_USD:.0f}")
        return TRIAL_BASE_USD


def place_entry_with_trail(ib, ct, px, action, shares):
    """入场marketable limit(DAY) + 子单TRAIL 4% GTC(父单成交才激活)。px由调用方先取好(跳空过滤在下单前)。"""
    sym = ct.symbol
    side = "BUY" if action == "BUY" else "SELL"
    cover = "SELL" if action == "BUY" else "BUY"
    lmt = round(px * (1 + LIMIT_BUFFER) if side == "BUY" else px * (1 - LIMIT_BUFFER), 2)
    parent = LimitOrder(side, shares, lmt); parent.tif = "DAY"; parent.transmit = False
    parent.orderId = ib.client.getReqId()
    trail = Order(action=cover, orderType="TRAIL", totalQuantity=shares,
                  trailingPercent=TRAIL_PCT, tif="GTC", parentId=parent.orderId, transmit=True)
    trail.ocaGroup = f"hdstr_{sym}"; trail.ocaType = 2
    et = ib.placeOrder(ct, parent)
    ib.placeOrder(ct, trail)
    return et


def next_trading_days(start, n):
    dt = datetime.strptime(start, "%Y-%m-%d"); out = []
    while len(out) < n:
        dt += timedelta(days=1)
        if dt.weekday() < 5: out.append(dt.strftime("%Y-%m-%d"))
    return out


def open_batch():
    st = load(STATE, {"positions": [], "log": []})
    today = time.strftime("%Y-%m-%d")
    halted = entries_halted()
    ib, _ = connect(61)
    if not ib: notify("🛑 hdstr open:连不上网关"); return
    acct = guard_account(ib)
    if not acct: ib.disconnect(); return

    # ①自愈:先审计存量仓的TRAIL保护(主batch全局撤单会扫掉GTC;每晚必查必补)
    open_pos = [p for p in st["positions"] if p["status"] == "open"]
    live_trails = {o.contract.symbol for o in ib.reqAllOpenOrders() if o.order.orderType == "TRAIL"} if open_pos else set()
    healed = []
    for p in open_pos:
        if p["ticker"] not in live_trails:
            ct = Stock(p["ticker"], "SMART", "USD")
            if ib.qualifyContracts(ct):
                cover = "SELL" if p["action"] == "BUY" else "BUY"
                tr = Order(action=cover, orderType="TRAIL", totalQuantity=p["shares"],
                           trailingPercent=TRAIL_PCT, tif="GTC")
                tr.ocaGroup = f"hdstr_{p['ticker']}"; tr.ocaType = 2
                ib.placeOrder(ct, tr); healed.append(p["ticker"])
    # ②新开仓
    placed, skipped, pending = [], [], []
    if halted:
        notify(f"⏸️ hdstr 新开仓已停({halted}),仅维护存量")
    else:
        day, sigs = latest_signals()
        # 信号新鲜度守卫(2026-07-27审计):只吃当天信号;文件不是今天=工作流没出/同步失败→宁可不开仓
        if day != today:
            notify(f"⏸️ hdstr:最新信号是{day}非今天,不开仓(防吃旧信号;查deepseek-broad工作流/信号同步)")
            sigs = []
        done_keys = {(p["ticker"], p["signal_date"]) for p in st["positions"]}
        untradable = set(load(UNTRADABLE, []))
        slots = MAX_CONC - len(open_pos)
        per_usd = 0
        if slots > 0 and sigs:
            eq = trial_equity_usd(ib, acct)
            unlocked = load(GATE, {}).get("verdict") == "PASS"
            base = eq if unlocked else min(eq, SIZING_FREEZE_USD)
            per_usd = base * POS_PCT
            print(f"[hdstr] 复利单仓额 ${per_usd:.0f} (基准${base:.0f}×{POS_PCT:.0%}"
                  f"{',已解冻' if unlocked else f',gate前冻结帽${SIZING_FREEZE_USD:.0f}'};净值${eq:.0f})")
        for s in sigs:
            if slots <= 0: break
            tk, ac, sp = s.get("ticker"), s.get("action"), s.get("current_price")
            if ac not in ("BUY", "SELL") or not sp or sp != sp: continue
            if (tk, day) in done_keys: continue
            if tk in untradable: skipped.append(f"{tk}(OTC)"); continue
            if not adv_ok(tk): skipped.append(f"{tk}(ADV)"); continue
            shares = int(per_usd / sp)
            if shares < 1: skipped.append(f"{tk}(价太高)"); continue
            ct = Stock(tk, "SMART", "USD")
            if not ib.qualifyContracts(ct): skipped.append(f"{tk}(无合约)"); continue
            px = snap_price(ib, ct)
            if not px: skipped.append(f"{tk}(无报价)"); continue
            # 跳空过滤在下单**前**(先下再撤可能已成交→裸仓,2026-07-22设计修正)
            gap = (px - sp) / sp * 100 * (1 if ac == "BUY" else -1)
            if gap > GAP_FILTER_PCT:
                skipped.append(f"{tk}(gap{gap:+.1f}%)"); continue
            et = place_entry_with_trail(ib, ct, px, ac, shares)
            if not et: skipped.append(f"{tk}(下单失败)"); continue
            pending.append((et, {
                "ticker": tk, "action": ac, "signal_date": day, "entry_date": today,
                "shares": shares, "signal_price": sp, "ref_price": px,
                "max_hold_date": next_trading_days(today, MAX_HOLD_TD)[-1], "status": "open"}))
            slots -= 1
    # 下单后验证(2026-07-28修:ECPG被拒但记成了open——拒单消息在断连后才回传):
    # 等5秒收异步状态,Cancelled/Inactive=被拒(SSR/无券等),不记账并报原因
    ib.sleep(5)
    for et, pos in pending:
        stt = et.orderStatus.status
        if stt in ("Cancelled", "ApiCancelled", "Inactive"):
            why = next((l.message[:50] for l in et.log if l.errorCode), stt)
            skipped.append(f"{pos['ticker']}(被拒:{why})")
        else:
            st["positions"].append(pos)
            placed.append(f"{pos['action']} {pos['ticker']}×{pos['shares']}@~{pos['ref_price']}")
    ib.disconnect()
    save_state(st)
    mode = "💰真钱" if ARM else "🧪paper体检"
    notify(f"{mode} hdstr开盘batch({acct})\n开仓{len(placed)}: {placed or '无'}\n"
           f"跳过: {skipped or '无'}{f' | 补挂TRAIL: {healed}' if healed else ''}\n"
           f"在手{len([p for p in st['positions'] if p['status']=='open'])}/{MAX_CONC}\n（hdstr真钱试运行·自动）")


def close_batch():
    """收盘后:①对账真实持仓更新状态②超时仓平掉。"""
    st = load(STATE, {"positions": [], "log": []})
    today = time.strftime("%Y-%m-%d")
    ib, _ = connect(62)
    if not ib: notify("🛑 hdstr close:连不上网关"); return
    acct = guard_account(ib)
    if not acct: ib.disconnect(); return
    real = {}
    for p in ib.positions(acct):
        real[p.contract.symbol] = real.get(p.contract.symbol, 0) + p.position
    closed_now, timeout_closed = [], []
    for p in st["positions"]:
        if p["status"] != "open": continue
        held = real.get(p["ticker"], 0)
        expect = p["shares"] if p["action"] == "BUY" else -p["shares"]
        if held == 0 or (expect > 0) != (held > 0):
            p["status"] = "closed"; p["close_date"] = today; p["close_via"] = "trail/manual"
            closed_now.append(p["ticker"]); continue
        if today >= p["max_hold_date"]:
            ct = Stock(p["ticker"], "SMART", "USD")
            if ib.qualifyContracts(ct):
                px = snap_price(ib, ct)
                side = "SELL" if p["action"] == "BUY" else "BUY"
                lmt = round((px or p["ref_price"]) * (1 - LIMIT_BUFFER if side == "SELL" else 1 + LIMIT_BUFFER), 2)
                o = LimitOrder(side, abs(int(held)), lmt); o.tif = "DAY"
                o.ocaGroup = f"hdstr_{p['ticker']}"; o.ocaType = 2   # 与TRAIL互斥,防双出
                ib.placeOrder(ct, o)
                p["status"] = "closing_timeout"; timeout_closed.append(p["ticker"])
    ib.sleep(3); ib.disconnect()
    save_state(st)
    if closed_now or timeout_closed:
        notify(f"hdstr收盘对账: TRAIL已出{closed_now or '无'} | 超时平仓单{timeout_closed or '无'}\n（hdstr真钱试运行·自动）")
    else:
        print("[hdstr close] 无变化")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "open"
    (open_batch if cmd == "open" else close_batch)()
