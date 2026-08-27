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
FILLS = "data/hdstr-fills.json"
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
MARGINAL_PASS_CAP = 2100.0  # 边缘PASS条款(2026-08-11审查后Riley批,协议修订#3):PASS但领先<2pp=
                            # 可能是噪音上的胜利,只解冻到中位帽$2100;领先≥2pp才全解冻。8/24评估时复核
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


def harvest_fills(ib, acct):
    """抓当日真实成交进独立台账(2026-08-04 优化#1:执行质量度量闭环,8/24滑点评估的数据源)。
    execId去重可重复调用;有参照价时附滑点(正数=不利成本,BUY付贵/SELL卖贱都记正)。围栏:失败不影响主流程。"""
    try:
        from ib_insync import ExecutionFilter
        led = load(FILLS, {"fills": []})
        seen = {f["exec_id"] for f in led["fills"]}
        ref = {p["ticker"]: p for p in load(STATE, {"positions": []})["positions"]}
        new = 0
        fills = ib.reqExecutions(ExecutionFilter(acctCode=acct))
        print(f"[hdstr fills] 本session可见成交{len(fills)}笔")   # 仪表(2026-08-12:连续两次0捕获,先量化再诊断)
        for tr in fills:
            e = tr.execution
            if e.execId in seen: continue
            row = {"exec_id": e.execId, "time": str(e.time), "sym": tr.contract.symbol,
                   "side": e.side, "shares": e.shares, "price": e.price}
            p = ref.get(tr.contract.symbol)
            rp = (p or {}).get("ref_price") or (p or {}).get("signal_price")
            if rp:
                sgn = 1 if e.side == "BOT" else -1
                row["slip_vs_ref_pct"] = round((e.price - rp) / rp * 100 * sgn, 3)
            led["fills"].append(row); new += 1
        if new:
            json.dump(led, open(FILLS, "w"), ensure_ascii=False, indent=1)
            print(f"[hdstr fills] 新记{new}笔真实成交(累计{len(led['fills'])})")
    except Exception as ex:
        print(f"[hdstr fills] 抓取失败(不影响主流程): {ex}")


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
    harvest_fills(ib, acct)   # 开盘批先收割隔夜/当日成交(TRAIL夜里触发的在这里入账)

    # ①自愈:先审计存量仓的TRAIL保护(主batch全局撤单会扫掉GTC;每晚必查必补)
    # closing_timeout(超时单已挂待成交)期间实股仍在手:占槽+享受TRAIL自愈,直到对账确认清仓
    open_pos = [p for p in st["positions"] if p["status"] in ("open", "closing_timeout")]
    # ①a 孤儿单清扫(2026-08-24 BANR裸空实炸:平仓后残留TRAIL未被OCA撤掉,数日后被触发→-7裸空
    # 无人知晓躺了近两周,靠回补价恰等成本才零损失。本clientId=61与挂TRAIL同client,可撤自己的单):
    # 凡挂单symbol不在在册持仓集合(含closing_timeout)且非指数核心 → 撤
    known = {p["ticker"] for p in open_pos} | {"QQQ", "QQQM"}
    for o in ib.reqAllOpenOrders():
        if (o.contract.symbol not in known
                and o.orderStatus.status in ("PreSubmitted", "Submitted")):
            ib.cancelOrder(o.order)
            print(f"[hdstr] 撤孤儿单: {o.contract.symbol} {o.order.action} {o.order.orderType}")
    ib.sleep(2)
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
    # ①b 超时平仓(2026-08-11移入开盘批:04:00收盘批下单必被Error 201"已收盘"拒绝,只有开盘时段能成交)
    # 不受halted影响——这是出场不是进场
    working = {o.contract.symbol for o in ib.reqAllOpenOrders()
               if o.order.orderType != "TRAIL" and o.orderStatus.status in ("PreSubmitted", "Submitted")}
    timeout_placed = []
    for p in open_pos:
        if today < p["max_hold_date"] or p["ticker"] in working: continue
        ct = Stock(p["ticker"], "SMART", "USD")
        if not ib.qualifyContracts(ct): continue
        px = snap_price(ib, ct)
        side = "SELL" if p["action"] == "BUY" else "BUY"
        lmt = round((px or p["ref_price"]) * (1 - LIMIT_BUFFER if side == "SELL" else 1 + LIMIT_BUFFER), 2)
        o = LimitOrder(side, p["shares"], lmt); o.tif = "DAY"
        o.ocaGroup = f"hdstr_{p['ticker']}"; o.ocaType = 2   # 与TRAIL互斥防双出
        tr_ = ib.placeOrder(ct, o); ib.sleep(3)
        if tr_.orderStatus.status in ("Cancelled", "ApiCancelled", "Inactive"):
            why = next((l.message[:40] for l in tr_.log if l.errorCode), tr_.orderStatus.status)
            print(f"[hdstr] {p['ticker']}超时平仓被拒:{why}")
        else:
            p["status"] = "closing_timeout"; timeout_placed.append(p["ticker"])
            fp = tr_.orderStatus.avgFillPrice
            if fp and fp == fp and fp > 0:   # 出场成交现场入账(会话级成交查询靠不住)
                led = load(FILLS, {"fills": []})
                led["fills"].append({"exec_id": f"timeout-{p['ticker']}-{today}", "time": time.strftime("%F %T"),
                                     "sym": p["ticker"], "side": "SLD" if side == "SELL" else "BOT",
                                     "shares": p["shares"], "price": fp, "src": "order_status@timeout"})
                json.dump(led, open(FILLS, "w"), ensure_ascii=False, indent=1)
                print(f"[hdstr fills] 超时出场现场入账: {p['ticker']} @ {fp}")
    if timeout_placed:
        notify(f"⏰ hdstr超时平仓单已挂(开盘时段): {timeout_placed}\n（hdstr真钱试运行·自动）")

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
            g = load(GATE, {})
            if g.get("verdict") == "PASS":
                fin = g.get("final", {})
                margin = fin.get("hds_ret_pct", 0) - fin.get("qqq_ret_pct", 0)
                if margin >= 2.0:
                    base, tag = eq, f"PASS(领先{margin:+.1f}pp)全解冻"
                else:
                    base, tag = min(eq, MARGINAL_PASS_CAP), f"边缘PASS(领先{margin:+.1f}pp<2pp)半解冻帽${MARGINAL_PASS_CAP:.0f}"
            else:
                base, tag = min(eq, SIZING_FREEZE_USD), f"gate前冻结帽${SIZING_FREEZE_USD:.0f}"
            per_usd = base * POS_PCT
            print(f"[hdstr] 复利单仓额 ${per_usd:.0f} (基准${base:.0f}×{POS_PCT:.0%},{tag};净值${eq:.0f})")
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
            # 成交价当场落台账(2026-08-25:reqExecutions是会话级,网关每日重启抹掉当日成交
            # →收盘批永远捞0笔。下单现场的avgFillPrice是唯一可靠时点)
            fp = et.orderStatus.avgFillPrice
            if fp and fp == fp and fp > 0:
                led = load(FILLS, {"fills": []})
                sgn = 1 if pos["action"] == "BUY" else -1
                led["fills"].append({"exec_id": f"entry-{pos['ticker']}-{today}", "time": time.strftime("%F %T"),
                                     "sym": pos["ticker"], "side": "BOT" if pos["action"] == "BUY" else "SLD",
                                     "shares": pos["shares"], "price": fp, "src": "order_status@place",
                                     "slip_vs_ref_pct": round((fp - pos["ref_price"]) / pos["ref_price"] * 100 * sgn, 3)})
                json.dump(led, open(FILLS, "w"), ensure_ascii=False, indent=1)
                print(f"[hdstr fills] 入场成交现场入账: {pos['ticker']} @ {fp}")
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
    harvest_fills(ib, acct)   # 收盘批收割当日全部成交(入场/超时平仓/日内TRAIL)
    real = {}
    for p in ib.positions(acct):
        real[p.contract.symbol] = real.get(p.contract.symbol, 0) + p.position
    closed_now, timeout_closed = [], []
    # 同标的多笔支持(2026-08-27修:EZPW止损后当晚再入场,按symbol对账把新旧都当开着→幽灵仓):
    # 按symbol汇总期望股数,与真实持仓比对;缺口按先进先出把最老的标记平仓
    from collections import defaultdict
    by_sym = defaultdict(list)
    for p in st["positions"]:
        if p["status"] in ("open", "closing_timeout"):
            by_sym[p["ticker"]].append(p)
    for sym, plist in by_sym.items():
        plist.sort(key=lambda x: x["entry_date"], reverse=True)   # 新仓优先覆盖真实持仓→旧仓先关(幸存者的超时日期才正确)
        held = real.get(sym, 0)
        for p in plist:
            expect = p["shares"] if p["action"] == "BUY" else -p["shares"]
            # 方向不符或该笔股数已不被真实持仓覆盖 → 先进先出关最老的
            if held == 0 or (expect > 0) != (held > 0):
                covered = False
            elif abs(held) >= abs(expect):
                covered = True
            else:
                # 部分覆盖=部分成交/部分平仓(2026-08-27 EZPW限价单6股只成5股实炸):
                # 台账缩到真实股数保留为存活仓,IB子单TRAIL会自动同步父单实成数
                p["shares"] = abs(held)
                p["partial_note"] = f"对账缩至实持{abs(held)}股({today})"
                print(f"[hdstr] {sym} 部分覆盖,台账缩至{abs(held)}股")
                held = 0
                continue
            if not covered:
                p["close_via"] = "timeout" if p["status"] == "closing_timeout" else "trail/manual"
                p["status"] = "closed"; p["close_date"] = today
                closed_now.append(f"{sym}({p['close_via']})")
            else:
                held -= expect
    for p in st["positions"]:
        if p["status"] not in ("open", "closing_timeout"): continue
        # 超时平仓下单已移至开盘批(2026-08-11:04:00=美东刚收盘,此处下单必被Error 201拒;
        # 收盘批只做对账,到期仓由下一个开盘批在交易时段内平)
    # 未知持仓警报(2026-08-24 BANR裸空实炸:孤儿单成交出的仓不在state里,对账循环只看在册→隐身12天):
    # 真实持仓中凡非在册、非指数核心的 → 强警报,人工核查
    known_now = {p["ticker"] for p in st["positions"] if p["status"] in ("open", "closing_timeout")} | {"QQQ", "QQQM"}
    unknown = [(s, q) for s, q in real.items() if s not in known_now and q != 0]
    if unknown:
        notify(f"🚨 hdstr对账发现未知持仓 {unknown} ——疑孤儿单成交或人工操作,需核查!\n（hdstr真钱试运行·自动）")
    ib.sleep(3); ib.disconnect()
    save_state(st)
    if closed_now or timeout_closed:
        notify(f"hdstr收盘对账: 已出场{closed_now or '无'} | 超时平仓单{timeout_closed or '无'}\n（hdstr真钱试运行·自动）")
    else:
        print("[hdstr close] 无变化")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "open"
    (open_batch if cmd == "open" else close_batch)()
