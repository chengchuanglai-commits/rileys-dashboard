"""三线组合前向验证账本 (forward validation ledger)。

为什么要它:paper账户有~$1M闲置现金,直接看账户NAV%会把我们$20k子组合的信号稀释~50倍=废。
做法:把paper账户里属于我们三线(指数+长线+波动)的持仓,当成一个独立的$NOTIONAL子组合跟踪。
  - 用持仓变化反推现金流:某票今天比昨天多了delta股→买入扣virtual_cash;少了→卖出加virtual_cash。
    这样动量腿"去现金避险"的钱也算进子组合,不丢。
  - 子组合净值 book = virtual_cash + 持仓市值,逐日对照"无脑全仓QQQ"基准,算真实forward alpha。
这是唯一无幸存者偏差的诚实裁决(见 legs_tested_summary 记忆)。

输出 data/forward-track.json(时间序列) + dashboard/forward-track.js + 飞书。
每天收盘后由 review batch 触发(run.sh review 末尾),同日重跑幂等。
"""
import os, json, time
from scripts.ibkr.client import connect, health
from scripts.ibkr.targets import build_master_targets
from scripts.ibkr.config import NOTIONAL, INDEX_SYM
from scripts.ibkr.notify import send

HIST = "data/forward-track.json"


def _prices(syms):
    """yfinance 批量取最新收盘价。"""
    import yfinance as yf
    px = {}
    try:
        d = yf.download(list(syms), period="2d", progress=False)["Close"]
        for s in syms:
            try:
                px[s] = float(d[s].dropna().iloc[-1]) if len(syms) > 1 else float(d.dropna().iloc[-1])
            except Exception:
                px[s] = None
    except Exception:
        pass
    return px


def our_universe():
    """我们三线的全部标的:master目标的keys(QQQ+9长线+动量当前持仓)。"""
    return set(build_master_targets(notional=NOTIONAL).keys()) | {INDEX_SYM}


def run():
    ib, _ = connect(client_id=24)
    if not ib:
        print("forward-track: 网关连不上,跳过"); return
    h = health(ib)
    uni = our_universe()
    # 当前我们universe内的实际持股(paper账户里只取属于三线的票)
    shares = {p.contract.symbol: round(p.position, 4)
              for p in ib.positions(h["account"])
              if p.contract.symbol in uni and abs(p.position) > 1e-6}
    # 价格趁连接还在时从IBKR取(和下单同源,免yfinance周末/盘后残缺),缺的再yfinance兜底
    from scripts.ibkr.trade_open import _ib_prices
    need = set(list(shares) + [INDEX_SYM])
    px = _ib_prices(ib, need)
    ib.disconnect()
    miss0 = [s for s in need if not px.get(s)]
    if miss0:
        for s, p in _prices(miss0).items(): px[s] = p

    today = time.strftime("%Y-%m-%d")
    qqq = px.get(INDEX_SYM)
    # 护栏:取价不全(yfinance抖动)就跳过不写,绝不用残缺价污染账本(覆盖好行→历史毁了)
    missing = [s for s in shares if not px.get(s)]
    if not qqq or len(missing) > max(1, 0.1 * len(shares)):
        print(f"forward-track: 取价不全(qqq={qqq}, 缺{len(missing)}/{len(shares)}: {missing[:5]}),跳过不写")
        return
    mv = sum(shares[s] * px[s] for s in shares if px.get(s))

    hist = json.load(open(HIST)) if os.path.exists(HIST) else {"inception": None, "notional": NOTIONAL, "rows": []}
    rows = [r for r in hist.get("rows", []) if r["date"] != today]  # 同日重跑幂等:去掉旧的今天

    if hist.get("inception") is None or not hist.get("rows"):
        # 建仓首日:子组合净值基线=NOTIONAL($20k),virtual_cash=NOTIONAL-当前市值
        hist["inception"] = {"date": today, "book": float(NOTIONAL), "qqq": qqq}
        vcash = float(NOTIONAL) - mv
    else:
        # 上一交易日(rows已去掉今天,最后一行即上一日)
        prev = rows[-1] if rows else hist["rows"][-1]
        vcash = prev["vcash"]
        prev_shares, prev_px = prev.get("shares", {}), prev.get("price", {})
        # 持仓变化反推现金流:买入(+delta)扣现金,卖出(-delta)加现金
        for s in set(list(shares) + list(prev_shares)):
            delta = shares.get(s, 0) - prev_shares.get(s, 0)
            p = px.get(s) or prev_px.get(s) or 0
            vcash -= delta * p

    book = vcash + mv
    inc = hist["inception"]
    port_ret = book / inc["book"] - 1 if inc["book"] else 0
    qqq_ret = (qqq / inc["qqq"] - 1) if (qqq and inc.get("qqq")) else None
    alpha = (port_ret - qqq_ret) if qqq_ret is not None else None

    row = {"date": today, "book": round(book, 2), "mv": round(mv, 2), "vcash": round(vcash, 2),
           "qqq": round(qqq, 2) if qqq else None, "nholdings": len(shares),
           "port_ret": round(port_ret, 4),
           "qqq_ret": round(qqq_ret, 4) if qqq_ret is not None else None,
           "alpha": round(alpha, 4) if alpha is not None else None,
           "shares": shares, "price": {s: round(px[s], 2) for s in shares if px.get(s)}}
    rows.append(row)
    hist["rows"] = rows
    hist["notional"] = float(NOTIONAL)
    os.makedirs("data", exist_ok=True)
    json.dump(hist, open(HIST, "w"), ensure_ascii=False, indent=2)
    with open("dashboard/forward-track.js", "w", encoding="utf-8") as f:
        f.write(f"window.FORWARD_TRACK = {json.dumps(hist, ensure_ascii=False)};\n")

    # 报告
    days = len(rows)
    pr = f"{port_ret*100:+.2f}%"
    qr = f"{qqq_ret*100:+.2f}%" if qqq_ret is not None else "?"
    al = f"{alpha*100:+.2f}%" if alpha is not None else "?"
    print(f"前向验证 {today} 第{days}个交易日 | 三线组合 {pr} | 无脑QQQ {qr} | alpha {al} "
          f"(book ${book:.0f}, 持仓{len(shares)}只)")

    # 飞书(每周或有意义时;这里每天发简报,样本少时也能看趋势)
    if os.environ.get("NOTIFY_WEBHOOK"):
        msg = [f"📈 前向验证 {today} (第{days}日)",
               f"三线组合 {pr} | 无脑QQQ {qr}",
               f"alpha {al}  (净值${book:.0f}/持仓{len(shares)}只)",
               "（forward validation·交易信号系统）"]
        try: send("\n".join(msg))
        except Exception: pass

    return row


if __name__ == "__main__":
    run()
