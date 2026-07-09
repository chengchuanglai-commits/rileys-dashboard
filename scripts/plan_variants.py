"""
Plan 变体引擎 — c 腿的平行 A/B 变体共用核心。

c 原样不动(backfill-portfolio-c.py 继续跑 26 笔基线)。本模块把 c 的模拟逻辑参数化,供:
  - cng (c-nogap): 关掉/放宽跳空过滤,其余同 c
  - ch  (c-H):     出场换 Plan H (TP15/SL2/2天),其余同 c
  - ct  (c-trail): 出场换移动止损(让赢家跑),其余同 c
以及 backtest-gap-filter.py 的跳空阈值扫描。

fixed 模式与 backfill-portfolio-c.py 逐笔一致(以 c 的 portfolio_value 复现为验收)。
compound 口径与 c 相同:frac10 复利、佣金另记不进净值(apples-to-apples)。
"""
import json, os, math
from datetime import datetime, timedelta
import yfinance as yf
from portfolio_compound import compound_portfolio

SIGNALS_DIR = "dashboard/trading-signals-history"
STARTING_CAPITAL = 2000
PER_POSITION_USD = 500


def ibkr_commission(shares):
    return round(max(1.00, shares * 0.005), 2)


def next_n_trading_days(start_str, n):
    dt = datetime.strptime(start_str, "%Y-%m-%d")
    days = []
    while len(days) < n:
        dt += timedelta(days=1)
        if dt.weekday() < 5:
            days.append(dt.strftime("%Y-%m-%d"))
    return days


_BAR_CACHE = {}

def _load_bars(ticker, signal_date, target_dates):
    """取信号日到最后目标日的日线;返回 {date_str: (o,hi,lo,cl)}。NaN bar 剔除。带内存缓存(同参数多轮扫描不重复拉)。"""
    ckey = (ticker, signal_date, target_dates[-1])
    if ckey in _BAR_CACHE:
        return _BAR_CACHE[ckey]
    fetch_end = (datetime.strptime(target_dates[-1], "%Y-%m-%d") + timedelta(days=2)).strftime("%Y-%m-%d")
    try:
        df = yf.Ticker(ticker).history(start=signal_date, end=fetch_end)
        df.index = df.index.tz_localize(None) if df.index.tz is not None else df.index
    except Exception as e:
        print(f"  [warn] yfinance failed for {ticker}: {e}")
        return None
    bars = {}
    for idx, r in df.iterrows():
        ds = idx.strftime("%Y-%m-%d")
        o, hi, lo, cl = (round(float(r[k]), 2) for k in ("Open", "High", "Low", "Close"))
        if any(v != v for v in (o, hi, lo, cl)):  # NaN bar(OTC延迟)剔除,否则污染净值
            continue
        bars[ds] = (o, hi, lo, cl)
    _BAR_CACHE[ckey] = bars
    return bars


def _gap_ok(action, entry_price, day1_open, gap_filter):
    """第一交易日不利跳空过滤。gap_filter=None → 不过滤(永远通过)。"""
    if gap_filter is None:
        return True
    gap_pct = (day1_open - entry_price) / entry_price * 100
    unfavorable = -gap_pct if action == "BUY" else gap_pct
    return unfavorable <= gap_filter


# ── 出场判定核心(实盘 simulate_* / 配对回放 A / 大样本回测 B 三处共用,单一真相源)──

def _fixed_hit(action, hi, lo, tp_price, sl_price):
    """固定 TP/SL 单日判定:止损优先于止盈。返回 (close_reason, close_price) 或 (None, None)。"""
    if action == "BUY":
        if lo <= sl_price:   return "stop_loss", sl_price
        if hi >= tp_price:   return "take_profit", tp_price
    else:
        if hi >= sl_price:   return "stop_loss", sl_price
        if lo <= tp_price:   return "take_profit", tp_price
    return None, None


def _trail_hit(action, hi, lo, stop):
    """移动止损单日是否触发。返回触发价或 None。"""
    if action == "BUY" and lo <= stop:  return stop
    if action == "SELL" and hi >= stop: return stop
    return None


def _trail_update(action, hi, lo, extreme, stop, trail_pct):
    """用当日极值把移动止损棘轮跟上(只朝有利方向)。返回 (new_extreme, new_stop)。"""
    if action == "BUY":
        extreme = max(extreme, hi); stop = max(stop, extreme * (1 - trail_pct / 100))
    else:
        extreme = min(extreme, lo); stop = min(stop, extreme * (1 + trail_pct / 100))
    return extreme, stop


def simulate_fixed(ticker, action, entry_price, signal_date, tp_pct, sl_pct, max_hold, gap_filter):
    """固定 TP/SL/最大持仓出场(Plan C / Plan H 都走这条)。返回 c 同款六元组。"""
    tp_price = round(entry_price * (1 + (tp_pct if action == "BUY" else -tp_pct) / 100), 2)
    sl_price = round(entry_price * (1 - (sl_pct if action == "BUY" else -sl_pct) / 100), 2)
    target_dates = next_n_trading_days(signal_date, max_hold)
    bars = _load_bars(ticker, signal_date, target_dates)
    if bars is None:
        return None, None, "open", None, {}, None

    today_str = datetime.now().strftime("%Y-%m-%d")
    daily_prices, day1_open = {}, None
    for td in target_dates:
        if td not in bars:
            if td > today_str:
                return None, None, "open", None, daily_prices, day1_open
            continue
        o, hi, lo, cl = bars[td]
        if day1_open is None:
            day1_open = o
            if not _gap_ok(action, entry_price, o, gap_filter):
                return None, None, "gap_filtered", None, {}, day1_open

        close_reason, close_price = _fixed_hit(action, hi, lo, tp_price, sl_price)
        if close_reason is None:
            close_price = cl

        raw = (close_price - entry_price) / entry_price * 100
        pnl_pct = raw if action == "BUY" else -raw
        daily_prices[td] = {"open": o, "high": hi, "low": lo, "close": cl, "pnl_pct": round(pnl_pct, 2)}
        if close_reason:
            return td, close_price, close_reason, round(pnl_pct, 2), daily_prices, day1_open
        if td == target_dates[-1]:
            raw = (cl - entry_price) / entry_price * 100
            pnl_pct = raw if action == "BUY" else -raw
            daily_prices[td]["pnl_pct"] = round(pnl_pct, 2)
            return td, cl, "max_hold", round(pnl_pct, 2), daily_prices, day1_open
    return None, None, "open", None, daily_prices, day1_open


def simulate_trail(ticker, action, entry_price, signal_date, sl_pct, trail_pct, max_hold, gap_filter):
    """移动止损出场:初始止损 -sl%,随价格有利移动把止损棘轮跟上(peak*(1-trail%));无固定止盈,让赢家跑。
    保守惯例:当日 low/high 先撞'昨日止损',再用当日极值更新明日止损。返回 c 同款六元组。"""
    target_dates = next_n_trading_days(signal_date, max_hold)
    bars = _load_bars(ticker, signal_date, target_dates)
    if bars is None:
        return None, None, "open", None, {}, None

    today_str = datetime.now().strftime("%Y-%m-%d")
    daily_prices, day1_open = {}, None
    if action == "BUY":
        stop = entry_price * (1 - sl_pct / 100)
    else:
        stop = entry_price * (1 + sl_pct / 100)
    extreme = entry_price

    for i, td in enumerate(target_dates):
        if td not in bars:
            if td > today_str:
                return None, None, "open", None, daily_prices, day1_open
            continue
        o, hi, lo, cl = bars[td]
        if day1_open is None:
            day1_open = o
            if not _gap_ok(action, entry_price, o, gap_filter):
                return None, None, "gap_filtered", None, {}, day1_open

        close_reason, close_price = None, None
        hit = _trail_hit(action, hi, lo, stop)
        if hit is not None:
            close_reason = "stop_loss" if i == 0 else "trail_stop"
            close_price = round(hit, 2)
        else:
            close_price = cl
        raw = (close_price - entry_price) / entry_price * 100
        pnl_pct = raw if action == "BUY" else -raw
        daily_prices[td] = {"open": o, "high": hi, "low": lo, "close": cl, "pnl_pct": round(pnl_pct, 2)}
        if close_reason:
            return td, close_price, close_reason, round(pnl_pct, 2), daily_prices, day1_open

        # 棘轮:用当日极值更新明日止损
        extreme, stop = _trail_update(action, hi, lo, extreme, stop, trail_pct)

        if td == target_dates[-1]:
            return td, cl, "max_hold", round(pnl_pct, 2), daily_prices, day1_open
    return None, None, "open", None, daily_prices, day1_open


def _read_signals():
    all_signals = []
    for fname in sorted(os.listdir(SIGNALS_DIR)):
        if not fname.endswith(".json") or "-report" in fname:
            continue
        date_str = fname.replace(".json", "")
        with open(os.path.join(SIGNALS_DIR, fname)) as f:
            d = json.load(f)
        for s in d.get("signals", []):
            all_signals.append((date_str, s))
    return all_signals


def _safe_pnl(p):
    if not p.get("daily_prices"):
        return 0
    v = list(p["daily_prices"].values())[-1].get("pnl_pct")
    return 0 if (v is None or (isinstance(v, float) and math.isnan(v))) else v


def _clean_nan(obj):
    if isinstance(obj, float):
        return None if (math.isnan(obj) or math.isinf(obj)) else obj
    if isinstance(obj, dict):
        return {k: _clean_nan(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_clean_nan(v) for v in obj]
    return obj


def run_variant(sim_fn, note, out_json, out_js, js_var, verbose=True):
    """跑一条变体:sim_fn(ticker, action, entry, signal_date) 已 partial 好参数。
    返回 stats dict。保存 json + dashboard js(与 c 同结构)。"""
    portfolio = {"capital_usd": STARTING_CAPITAL, "open_positions": [], "closed_positions": [], "_note": note}
    skipped_gap = skipped_zero_shares = 0
    for signal_date, s in _read_signals():
        ticker, action, entry_price = s.get("ticker"), s.get("action"), s.get("current_price")
        if action not in ("BUY", "SELL") or not entry_price:
            continue
        shares = int(PER_POSITION_USD / entry_price)
        if shares == 0:
            skipped_zero_shares += 1
            continue
        actual = round(shares * entry_price, 2)
        entry_comm = exit_comm = ibkr_commission(shares)
        close_date, close_price, close_reason, final_pct, daily, day1_open = sim_fn(ticker, action, entry_price, signal_date)
        if close_reason == "gap_filtered":
            skipped_gap += 1
            continue
        mhd = list(daily.keys())[-1] if daily else signal_date  # 展示用:最后有数据的一天
        pos = {"ticker": ticker, "name": s.get("name", ""), "action": action, "signal_date": signal_date,
               "entry_price": entry_price, "allocated_usd": PER_POSITION_USD, "shares": shares,
               "actual_position_usd": actual, "entry_commission": entry_comm,
               "max_hold_date": mhd, "day1_open": day1_open, "daily_prices": daily}
        if close_reason == "open":
            portfolio["open_positions"].append(pos)
        elif close_date:
            gross = round(actual * final_pct / 100, 2)
            portfolio["closed_positions"].append({**pos, "close_date": close_date, "close_price": close_price,
                "final_pnl_pct": final_pct, "close_reason": close_reason, "exit_commission": exit_comm,
                "commission_total": round(entry_comm + exit_comm, 2), "realized_pnl_usd": round(gross - entry_comm - exit_comm, 2)})

    fc, fo, _pv, total_realized, open_unreal, _sk = compound_portfolio(
        portfolio["closed_positions"], portfolio["open_positions"], _safe_pnl, STARTING_CAPITAL)
    portfolio["closed_positions"], portfolio["open_positions"] = fc, fo
    wins = [p for p in fc if p.get("realized_pnl_usd", 0) > 0]
    total_comm = sum(p.get("commission_total", 0) for p in fc)
    portfolio["stats"] = {
        "total_trades": len(fc), "win_trades": len(wins),
        "win_rate": round(len(wins) / len(fc) * 100, 1) if fc else 0,
        "total_realized_pnl_usd": round(total_realized, 2),
        "open_unrealized_pnl_usd": round(open_unreal, 2),
        "portfolio_value": round(STARTING_CAPITAL + total_realized + open_unreal, 2),
        "total_commission_usd": round(total_comm, 2),
        "skipped_gap": skipped_gap, "skipped_zero_shares": skipped_zero_shares,
        "updated_at": datetime.now().strftime("%Y-%m-%d"),
    }
    portfolio = _clean_nan(portfolio)
    if out_json:
        with open(out_json, "w") as f:
            json.dump(portfolio, f, ensure_ascii=False, indent=2)
    if out_js:
        with open(out_js, "w", encoding="utf-8") as f:
            f.write(f"// {note}\n")
            f.write(f"window.{js_var} = {json.dumps(portfolio, ensure_ascii=False, indent=2)};\n")
    if verbose:
        st = portfolio["stats"]
        print(f"  {note}")
        print(f"  交易 {st['total_trades']} 笔 胜率 {st['win_rate']}% | 跳空跳过 {st['skipped_gap']} | "
              f"已实现 ${st['total_realized_pnl_usd']:+.2f} 浮盈 ${st['open_unrealized_pnl_usd']:+.2f} | "
              f"净值 ${st['portfolio_value']}")
    return portfolio["stats"]
