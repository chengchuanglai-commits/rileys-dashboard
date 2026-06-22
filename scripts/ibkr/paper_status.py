"""Paper 执行实况 → dashboard。读 IBKR paper 真实持仓/成交均价 + 引擎目标 + 模拟假设价,
算滑点(真实成交价 vs 模拟价),写 data/paper-status.json + dashboard/paper-status.js(window.PAPER_STATUS)。
回答"模拟到底准不准"——paper真实结果贴模拟=模拟可信;差很多=edge判断要打折。
LIVE=False 干跑期 paper 无持仓,卡片显示"等待首次执行"。
用法: NO_PROXY=127.0.0.1,localhost python3 -m scripts.ibkr.paper_status
"""
import os, json, time
from scripts.ibkr.config import NOTIONAL, LIVE


def collect():
    from scripts.ibkr.client import connect, health
    from scripts.ibkr.targets import build_targets
    date = time.strftime("%Y-%m-%d")
    out = {"date": date, "live": LIVE, "connected": False, "nav": None, "cash": None,
           "positions": [], "open_orders": 0, "note": ""}

    ib, port = connect(client_id=24)
    if not ib:
        out["note"] = "网关未连上(Gateway没登录/掉线)"
        _write(out); return out
    out["connected"] = True
    h = health(ib)
    out["account"] = h["account"]
    out["nav"] = round(h["nav"], 2)
    out["cash"] = round(h["cash"], 2)
    out["open_orders"] = h["open_orders"]

    # 引擎目标(该买什么) + 模拟盘假设价(算滑点的基准)
    target_usd = build_targets(notional=NOTIONAL)
    syms = [p.contract.symbol for p in ib.positions(h["account"])]
    # 滑点基准 = **下单当日现价(today)**,不是几天前模拟入场价。
    # 纯滑点=真实成交价 vs 当日现价(执行成本,≈0.x%才对);用模拟入场价会把"延迟进场涨幅"误算成滑点。
    today_px = _today_prices(syms)
    sim_px = _sim_prices()   # 仍带模拟入场价供参考(看"延迟进场差多少")

    total_pnl = 0.0
    for p in ib.positions(h["account"]):
        sym = p.contract.symbol
        avg = round(float(p.avgCost), 2)          # paper 真实成交均价(成本)
        tp = today_px.get(sym)                     # 当前价(最新)
        sp = sim_px.get(sym)                       # 模拟入场价(参考)
        slip = round((avg - tp) / tp * 100, 2) if (tp and tp > 0) else None   # 纯执行滑点
        delay = round((avg - sp) / sp * 100, 2) if (sp and sp > 0) else None  # 含延迟进场总差
        # 当前盈亏(现价 vs 成本)
        chg = round((tp - avg) / avg * 100, 2) if (tp and avg > 0) else None
        pnl = round((tp - avg) * p.position, 2) if (tp and avg > 0) else None
        if pnl is not None: total_pnl += pnl
        out["positions"].append({
            "sym": sym, "shares": p.position, "avg_fill": avg,
            "cur_price": tp, "change_pct": chg, "pnl_usd": pnl,   # 当前价/涨跌/盈亏
            "today_price": tp, "slippage_pct": slip,
            "sim_price": sp, "delay_gap_pct": delay,
            "target_usd": round(target_usd.get(sym, 0), 0),
        })
    out["total_unrealized_pnl"] = round(total_pnl, 2)   # 10仓合计浮盈亏
    out["updated_at"] = time.strftime("%Y-%m-%d %H:%M")
    ib.disconnect()
    if not out["positions"]:
        out["note"] = "LIVE=False 干跑中,paper 暂无持仓(等切真下单后填充)" if not LIVE else "无持仓"
    _write(out)
    return out


def _today_prices(syms):
    """各票当日现价(滑点基准)。yfinance 最新收盘。"""
    px = {}
    if not syms:
        return px
    try:
        import yfinance as yf
        data = yf.download(syms, period="2d", progress=False)["Close"]
        for s in syms:
            try:
                px[s] = float(data[s].dropna().iloc[-1]) if len(syms) > 1 else float(data.dropna().iloc[-1])
            except Exception:
                px[s] = None
    except Exception:
        pass
    return px


def _sim_prices():
    """模拟盘各持仓的入场价(参考)。读 momma/bq 持仓的 entry_price。"""
    px = {}
    for f in ("data/portfolio_momma.json", "data/portfolio_bq.json"):
        try:
            d = json.load(open(f))
            for pos in d.get("open_positions", []):
                if pos.get("ticker") and pos.get("entry_price"):
                    px[pos["ticker"]] = float(pos["entry_price"])
        except Exception:
            pass
    return px


def _write(out):
    os.makedirs("data", exist_ok=True)
    json.dump(out, open("data/paper-status.json", "w"), ensure_ascii=False, indent=2)
    with open("dashboard/paper-status.js", "w", encoding="utf-8") as f:
        f.write("// IBKR paper 执行实况(持仓/成交价/滑点 vs 模拟)\n")
        f.write(f"window.PAPER_STATUS = {json.dumps(out, ensure_ascii=False)};\n")
    print(f"paper-status: connected={out['connected']} 持仓{len(out['positions'])} 净值{out.get('nav')} note={out['note']}")


if __name__ == "__main__":
    collect()
