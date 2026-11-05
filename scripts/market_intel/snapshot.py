"""每晚市场情报 · 第一段:纯 Python 数据快照(无 AI)。
QQQ:IBKR 日线为主、yfinance 交叉验证;账户(只读);大盘股异动(IBKR 免费扫描器)。
用法: python3 -m scripts.market_intel.snapshot   退出码 0=已写快照 3=没有新交易日(跳过) 2=QQQ 两源都取不到"""
import json, math, os, shutil, sys, time
from datetime import date, datetime, time as dtime
from zoneinfo import ZoneInfo

import pandas as pd

from scripts.lev_engine import gate_signal
from scripts.market_intel.config import (BACKSTOP, XCHECK_TOL, IB_PORT, IB_CLIENT_ID, SCAN_CODES, SCAN_ROWS,
                                         MIN_PRICE, MIN_MCAP_MUSD, MAX_MOVERS, WS_SNAPSHOT_NAME, paths)

SESSION_CLOSE = dtime(16, 15)   # 美东 16:15 前,当天那根日线视为未收盘


def complete_bars(df, now_et):
    """盘中手动运行/补跑时,IBKR 会给当天未收盘的半根K线——丢掉它。"""
    if len(df) and pd.Timestamp(df.index[-1]).date() == now_et.date() and now_et.time() < SESSION_CLOSE:
        return df.iloc[:-1]
    return df


def should_run(last_bar_date, last_done):
    """有比上次成功处理更新的交易日才跑:同时覆盖休市日、补跑、重复运行。"""
    return last_done is None or last_bar_date > last_done


def _pct(x):
    return round(float(x) * 100, 2)


def qqq_section(primary, primary_src, secondary):
    if primary is None or len(primary) < 210:
        raise ValueError(f"QQQ 日线太短({0 if primary is None else len(primary)} 根,需 ≥210)")
    c = primary["close"].astype(float)
    last = primary.index[-1]
    close = float(c.iloc[-1])
    high_52w = float(primary["high"].astype(float).iloc[-252:].max())
    vol = c.pct_change().rolling(20).std().iloc[-1] * math.sqrt(252)

    xcheck = {"status": "single_source", "other_close": None, "diff_pct": None}
    if secondary is not None and len(secondary):
        other = secondary["close"]
        hit = other[[pd.Timestamp(i).date() == pd.Timestamp(last).date() for i in other.index]]
        if len(hit):
            oc = float(hit.iloc[-1])
            diff = oc / close - 1
            xcheck = {"status": "ok" if abs(diff) <= XCHECK_TOL + 1e-12 else "mismatch",
                      "other_close": round(oc, 2), "diff_pct": _pct(diff)}

    return {
        "source": primary_src,
        "date": pd.Timestamp(last).date().isoformat(),
        "close": round(close, 2),
        "high": round(float(primary["high"].iloc[-1]), 2),
        "low": round(float(primary["low"].iloc[-1]), 2),
        "ma20": round(float(c.iloc[-20:].mean()), 2),
        "ma50": round(float(c.iloc[-50:].mean()), 2),
        "ma200": round(float(c.iloc[-200:].mean()), 2),
        "vol20_ann": _pct(vol) if vol == vol else None,      # 单位 %
        "high_52w": round(high_52w, 2),
        "dd_from_high_pct": _pct(close / high_52w - 1),
        "gate": gate_signal(c),
        "backstop": BACKSTOP,
        "backstop_dist_pct": _pct(close / BACKSTOP - 1),
        "xcheck": xcheck,
    }


# ── 异动股 ─────────────────────────────────────────────────────────────
def select_movers(rows, is_etf, max_n):
    """三张扫描榜合并:按代码去重(记下出现在哪些榜),剔除 ETF,按最好名次排序取前 max_n。"""
    merged = {}
    for r in rows:
        m = merged.setdefault(r["symbol"], {"symbol": r["symbol"], "scans": [], "rank": r["rank"]})
        if r["scan"] not in m["scans"]:
            m["scans"].append(r["scan"])
        m["rank"] = min(m["rank"], r["rank"])
    keep = [m for s, m in merged.items() if not is_etf.get(s, False)]
    keep.sort(key=lambda m: (m["rank"], SCAN_CODES.index(m["scans"][0])))
    return keep[:max_n]


def enrich_mover(bars):
    c, v = bars["close"].astype(float), bars["volume"].astype(float)
    return {"close": round(float(c.iloc[-1]), 2),
            "chg_pct": round((float(c.iloc[-1]) / float(c.iloc[-2]) - 1) * 100, 2),
            "vol_ratio": round(float(v.iloc[-1]) / float(v.iloc[-21:-1].mean()), 2)}


def need_fundamentals(session_date, state_file, mode, today=None):
    """基本面分析师:周一跑;没有旧结论或旧结论超过 8 天也跑;降级模式(lite)有旧结论就不跑。"""
    if not state_file.exists():
        return True
    if mode == "lite":
        return False
    age = ((today or date.today()) - date.fromtimestamp(state_file.stat().st_mtime)).days
    return session_date.weekday() == 0 or age > 8


# ── 数据源(失败一律返回 None / [],不抛异常)──────────────────────────
def connect_ib():
    from ib_insync import IB
    for attempt in range(3):
        try:
            ib = IB()
            ib.connect("127.0.0.1", IB_PORT, clientId=IB_CLIENT_ID, readonly=True, timeout=15)
            return ib
        except Exception as e:
            print(f"[snapshot] IBKR 连接失败(第{attempt + 1}次): {type(e).__name__} {str(e)[:80]}")
            if attempt < 2:
                time.sleep(60)   # 网关刚登录要 1-2 分钟同步
    return None


def _frame(df):
    df = df.copy()
    df.index = pd.to_datetime(df.index)
    return df[["close", "high", "low", "volume"]].astype(float).dropna()


def fetch_ib_daily(ib, symbol, duration="2 Y"):
    try:
        from ib_insync import Stock, util
        bars = ib.reqHistoricalData(Stock(symbol, "SMART", "USD"), endDateTime="", durationStr=duration,
                                    barSizeSetting="1 day", whatToShow="TRADES", useRTH=True, formatDate=1)
        if not bars:
            return None
        return _frame(util.df(bars).set_index("date"))
    except Exception as e:
        print(f"[snapshot] IBKR 日线 {symbol} 失败: {type(e).__name__} {str(e)[:80]}")
        return None


def fetch_yf_daily(symbol):
    import yfinance as yf
    for _ in range(3):
        try:
            d = yf.download(symbol, period="2y", progress=False, auto_adjust=False)   # 不复权,与 IBKR 口径一致
            if d is None or d.empty:
                raise ValueError("空数据")
            cols = {}
            for name in ("Close", "High", "Low", "Volume"):
                s = d[name]
                cols[name.lower()] = s[symbol] if hasattr(s, "columns") else s
            return _frame(pd.DataFrame(cols))
        except Exception:
            time.sleep(3)
    return None


def scan_movers(ib):
    from ib_insync import ScannerSubscription
    rows = []
    for code in SCAN_CODES:
        try:
            sub = ScannerSubscription(instrument="STK", locationCode="STK.US.MAJOR", scanCode=code,
                                      numberOfRows=SCAN_ROWS, abovePrice=MIN_PRICE, marketCapAbove=MIN_MCAP_MUSD)
            for r in ib.reqScannerData(sub):
                rows.append({"symbol": r.contractDetails.contract.symbol, "scan": code, "rank": r.rank})
        except Exception as e:
            print(f"[snapshot] 扫描 {code} 失败: {type(e).__name__} {str(e)[:80]}")
    return rows


def etf_flags(ib, symbols):
    from ib_insync import Stock
    out = {}
    for s in symbols:
        try:
            cds = ib.reqContractDetails(Stock(s, "SMART", "USD"))
            out[s] = bool(cds) and cds[0].stockType == "ETF"
        except Exception:
            out[s] = False
    return out


def account_section(ib):
    """净值/杠杆/各币种现金/持仓。刻意不带账户号(公开仓库铁律,AI 也不需要)。"""
    try:
        summ = {v.tag: v for v in ib.accountSummary()}
        nav = float(summ["NetLiquidation"].value)
        gpv = float(summ["GrossPositionValue"].value)
        cash = {v.currency: round(float(v.value), 2) for v in ib.accountValues()
                if v.tag == "CashBalance" and v.currency not in ("BASE", "")}
        pos = [{"symbol": p.contract.symbol, "qty": float(p.position), "avg_cost": round(float(p.avgCost), 2)}
               for p in ib.positions()]
        return {"nav": round(nav, 2), "nav_ccy": summ["NetLiquidation"].currency,
                "gross_position_value": round(gpv, 2), "leverage": round(gpv / nav, 2) if nav else None,
                "cash": cash, "positions": pos}
    except Exception as e:
        return {"missing": f"账户读取失败: {type(e).__name__}"}


# ── 组装 ─────────────────────────────────────────────────────────────
def build_snapshot(now_et, ib, last_done, mode="full", fetch_yf=fetch_yf_daily, fetch_ib=fetch_ib_daily, p=None):
    p = p or paths()
    issues = []
    ib_q = fetch_ib(ib, "QQQ") if ib is not None else None
    yf_q = fetch_yf("QQQ")
    ib_q = complete_bars(ib_q, now_et) if ib_q is not None else None
    yf_q = complete_bars(yf_q, now_et) if yf_q is not None else None
    if ib is None:
        issues.append("IBKR 网关离线:账户与异动股缺失,QQQ 仅 yfinance 单一来源")
    elif ib_q is None:
        issues.append("IBKR 日线取不到,QQQ 改用 yfinance 单一来源")
    if ib_q is not None:
        qqq = qqq_section(ib_q, "ibkr", yf_q)
    elif yf_q is not None:
        qqq = qqq_section(yf_q, "yfinance", None)
    else:
        raise RuntimeError("QQQ 日线 IBKR 和 yfinance 都取不到")
    if qqq["xcheck"]["status"] == "mismatch":
        issues.append(f"QQQ 收盘两源相差 {qqq['xcheck']['diff_pct']}%(IBKR {qqq['close']} / yfinance "
                      f"{qqq['xcheck']['other_close']}),以 IBKR 为准,请核对")
    elif ib_q is not None and qqq["xcheck"]["status"] == "single_source":
        issues.append("yfinance 没有同日收盘,QQQ 未交叉验证")

    session = date.fromisoformat(qqq["date"])
    if not should_run(session, last_done):
        return None

    if ib is None:
        account, movers = {"missing": "网关离线"}, []
    elif now_et.date() != session:
        # 扫描器只反映"当前/最近"交易日;补跑撞上次日(尤其盘中)时榜单和快照交易日对不上,宁缺勿错
        account, movers = account_section(ib), []
        issues.append(f"补跑时间(美东 {now_et:%m-%d %H:%M})与交易日 {session} 不是同一天,扫描器反映的是盘中/"
                      f"之后的行情,异动股略过")
    else:
        account = account_section(ib)
        rows = scan_movers(ib)
        cand = select_movers(rows, etf_flags(ib, sorted({r["symbol"] for r in rows})), MAX_MOVERS[mode])
        movers = []
        for m in cand:
            bars = fetch_ib(ib, m["symbol"], "2 M")
            bars = complete_bars(bars, now_et) if bars is not None else None
            if bars is None or len(bars) < 21:
                issues.append(f"{m['symbol']} 日线取不到,已跳过")
                continue
            movers.append({**m, **enrich_mover(bars)})
        if not rows:
            issues.append("IBKR 扫描器无结果,异动股缺失")

    return {"session_date": qqq["date"], "generated_at": now_et.isoformat(timespec="seconds"), "mode": mode,
            "run_fundamentals": need_fundamentals(session, p.state / "fundamentals_latest.md", mode,
                                                  today=now_et.date()),
            "qqq": qqq, "account": account, "movers": movers, "data_issues": issues}


def main():
    p = paths()
    now_et = datetime.now(ZoneInfo("America/New_York"))
    f = p.state / "last_session.txt"
    last_done = date.fromisoformat(f.read_text().strip()) if f.exists() else None
    mode = os.environ.get("INTEL_MODE", "full")
    ib = connect_ib()
    try:
        snap = build_snapshot(now_et, ib, last_done, mode, p=p)
    except RuntimeError as e:
        print(f"[snapshot] ❌ {e}")
        return 2
    finally:
        if ib is not None:
            ib.disconnect()
    if snap is None:
        print(f"[snapshot] skip:没有比 {last_done} 更新的交易日(休市或已处理)")
        return 3
    body = json.dumps(snap, ensure_ascii=False, indent=2)
    for f in (p.ws_snapshot / WS_SNAPSHOT_NAME, p.archive_snapshots / f"{snap['session_date']}.json"):
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(body)
    prev = p.state / "fundamentals_latest.md"
    if not snap["run_fundamentals"] and prev.exists():
        shutil.copy(prev, p.ws_snapshot / "fundamentals_prev.md")
    print(f"[snapshot] ✅ {snap['session_date']} QQQ {snap['qqq']['close']}({snap['qqq']['source']},"
          f"交叉验证 {snap['qqq']['xcheck']['status']}),异动股 {len(snap['movers'])} 只,问题 {len(snap['data_issues'])} 条")
    return 0


if __name__ == "__main__":
    sys.exit(main())
