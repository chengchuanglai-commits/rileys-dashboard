import json
import os
import sys
import time
import yfinance as yf
from datetime import datetime, timezone, timedelta

beijing_tz = timezone(timedelta(hours=8))
now_beijing = datetime.now(beijing_tz)

# BACKFILL_DATE 允许手动指定日期（GitHub Actions workflow_dispatch 传入）
_backfill = os.environ.get('BACKFILL_DATE', '').strip()
if _backfill:
    today = _backfill
    yesterday = (datetime.strptime(_backfill, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
    generated_at = f"{_backfill}T20:30:00"
    print(f"[backfill] 回填模式，目标日期: {today}")
else:
    today = now_beijing.strftime('%Y-%m-%d')
    yesterday = (now_beijing - timedelta(days=1)).strftime('%Y-%m-%d')
    generated_at = now_beijing.strftime('%Y-%m-%dT%H:%M:00')

HISTORY_DIR = "dashboard/trading-signals-history"
os.makedirs(HISTORY_DIR, exist_ok=True)

# Token usage tracking — wraps anthropic.Anthropic to intercept all API calls
_total_input_tokens = 0
_total_output_tokens = 0

def _patch_anthropic():
    try:
        import anthropic
        original_create = anthropic.Anthropic().messages.create.__func__ if False else None
        _orig = anthropic.resources.messages.Messages.create
        def _tracked_create(self, *args, **kwargs):
            global _total_input_tokens, _total_output_tokens
            resp = _orig(self, *args, **kwargs)
            if hasattr(resp, 'usage'):
                _total_input_tokens  += getattr(resp.usage, 'input_tokens',  0)
                _total_output_tokens += getattr(resp.usage, 'output_tokens', 0)
            return resp
        anthropic.resources.messages.Messages.create = _tracked_create
    except Exception as e:
        print(f"[warn] Token tracking patch failed: {e}")

_patch_anthropic()


BLACKLIST = {
    "NVDA","AAPL","MSFT","AMZN","GOOGL","GOOG","META","TSLA","JPM","JNJ","XOM",
    "BRK","V","MA","UNH","PG","HD","CVX","MRK","ABBV","BAC","KO","PEP","COST",
    "WMT","AVGO","TSM","LLY","ORCL","NFLX","AMD","INTC","TLT","BND","SPY","QQQ"
}

def select_stocks():
    # GitHub Actions cron can be delayed several hours; if script runs past midnight Beijing,
    # fall back to yesterday's morning note (stocks are valid for the whole trading day)
    history_file = f"dashboard/morning-note-history/{today}.json"
    if not os.path.exists(history_file):
        fallback = f"dashboard/morning-note-history/{yesterday}.json"
        if os.path.exists(fallback):
            print(f"[warn] Today's morning note not found, using yesterday's: {fallback}")
            history_file = fallback
        else:
            print(f"[warn] Morning note not found: {history_file}")
            return []
    with open(history_file) as f:
        data = json.load(f)
    picks = data.get('stock_picks', [])
    sp500 = data.get('market', {}).get('sp500_futures_pct', 0)
    # Include both buy and sell direction candidates — TradingAgents decides final direction
    all_picks = [p for p in picks if p.get('ticker', '').upper() not in BLACKLIST]
    if sp500 >= 0:
        preferred = ['科技', '半导体', '消费可选', '能源']
    else:
        preferred = ['医疗', '消费必需', '生物科技', '固收']
    # Prioritize buy-direction stocks in preferred sectors, then sell-direction, as fallback pool
    all_picks.sort(key=lambda p: (
        2 if p.get('direction') == 'buy' and any(s in p.get('sector', '') for s in preferred) else
        1 if p.get('direction') == 'buy' else 0
    ), reverse=True)
    # Return up to 5 candidates — main loop stops when 2 BUY/SELL signals are found
    candidates = all_picks[:5]
    print(f"[select] Candidate pool: {[p['ticker'] for p in candidates]} (S&P {sp500:+.2f}%)")
    return candidates


def run_tradingagents(ticker):
    from tradingagents.graph.trading_graph import TradingAgentsGraph
    from tradingagents.default_config import DEFAULT_CONFIG
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = "anthropic"
    config["deep_think_llm"] = "claude-haiku-4-5-20251001"
    config["quick_think_llm"] = "claude-haiku-4-5-20251001"
    config["max_debate_rounds"] = 2
    config["online_tools"] = True
    print(f"[tradingagents] Analyzing {ticker}...")
    ta = TradingAgentsGraph(debug=False, config=config)
    state, decision = ta.propagate(ticker, today)
    return state, str(decision)


def parse_action(decision_str):
    d = decision_str.upper()
    if 'BUY' in d or 'OVERWEIGHT' in d or 'STRONG BUY' in d:
        return 'BUY'
    if 'SELL' in d or 'UNDERWEIGHT' in d or 'REDUCE' in d or 'STRONG SELL' in d:
        return 'SELL'
    return 'HOLD'


def extract_full_report(state):
    """Extract all analysis sections from TradingAgents state."""
    debate  = state.get("investment_debate_state") or {}
    risk    = state.get("risk_debate_state") or {}
    return {
        "market":       state.get("market_report")            or "",
        "sentiment":    state.get("sentiment_report")         or "",
        "news":         state.get("news_report")              or "",
        "fundamentals": state.get("fundamentals_report")      or "",
        "debate":       debate.get("judge_decision")          or debate.get("history") or "",
        "investment_plan": state.get("investment_plan")       or "",
        "trader_plan":  state.get("trader_investment_plan")   or "",
        "risk":         risk.get("judge_decision")            or risk.get("history")   or "",
        "final":        state.get("final_trade_decision")     or "",
    }


def translate_report_to_chinese(report, ticker):
    """Translate all non-empty report sections to Chinese using Haiku."""
    import anthropic
    MAX_CHARS = 2000  # truncate each section so total output fits in max_tokens
    to_translate = {
        k: (v.strip()[:MAX_CHARS] + ("…" if len(v.strip()) > MAX_CHARS else ""))
        for k, v in report.items() if v and v.strip()
    }
    if not to_translate:
        return report
    try:
        client = anthropic.Anthropic()
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=12000,
            messages=[{"role": "user", "content": (
                f"将以下{ticker}股票分析报告各章节翻译成中文，保持专业金融术语。"
                f"严格返回相同结构的JSON（只翻译值，不改变键名，不添加任何其他文字）：\n\n"
                f"{json.dumps(to_translate, ensure_ascii=False)}"
            )}]
        )
        text = resp.content[0].text.strip()
        start = text.find('{')
        end = text.rfind('}') + 1
        if start >= 0 and end > start:
            translated = json.loads(text[start:end])
            result = dict(report)
            result.update(translated)
            print(f"[translate] {ticker}: translated {len(translated)} sections to Chinese")
            return result
        print(f"[warn] Translation response not parseable for {ticker}")
        return report
    except Exception as e:
        print(f"[warn] Translation failed for {ticker}: {e}")
        return report


def summarize(report):
    """Build a 2-sentence summary from final decision + investment plan."""
    final = (report.get("final") or "").strip()
    plan  = (report.get("investment_plan") or "").strip()
    text  = final if final else plan
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    out   = ' '.join(lines)
    return out[:400] + ('…' if len(out) > 400 else '')


def get_day_ohlc(ticker):
    """Fetch latest trading day OHLC in one API call. Returns (open, high, low, close)."""
    try:
        hist = yf.Ticker(ticker).history(period="5d")
        if len(hist) == 0:
            return None, None, None, None
        row = hist.iloc[-1]
        data_date = hist.index[-1].strftime('%Y-%m-%d')
        o = round(float(row['Open']), 2)
        h = round(float(row['High']), 2)
        l = round(float(row['Low']), 2)
        c = round(float(row['Close']), 2)
        print(f"[price] {ticker}: O=${o} H=${h} L=${l} C=${c} (data: {data_date})")
        return o, h, l, c
    except Exception as e:
        print(f"[warn] yfinance OHLC fetch failed for {ticker}: {e}")
        return None, None, None, None


def get_ohlc_for_date(ticker, target_date):
    """Fetch OHLC for a specific past trading date (for backfill verification)."""
    try:
        hist = yf.Ticker(ticker).history(period="10d")
        for idx in hist.index:
            if idx.strftime('%Y-%m-%d') == target_date:
                row = hist.loc[idx]
                o = round(float(row['Open']), 2)
                h = round(float(row['High']), 2)
                l = round(float(row['Low']), 2)
                c = round(float(row['Close']), 2)
                print(f"[backfill price] {ticker} on {target_date}: O=${o} H=${h} L=${l} C=${c}")
                return o, h, l, c
        print(f"[warn] {ticker}: no data found for {target_date}")
        return None, None, None, None
    except Exception as e:
        print(f"[warn] get_ohlc_for_date failed for {ticker} on {target_date}: {e}")
        return None, None, None, None


def get_close_for_date(ticker, target_date):
    """Get closing price for a specific past trading date (for backfill signal price)."""
    _, _, _, c = get_ohlc_for_date(ticker, target_date)
    return c


def get_price(ticker):
    """Get latest close price."""
    _, _, _, c = get_day_ohlc(ticker)
    return c


def get_open_price(ticker):
    """Get latest open price."""
    o, _, _, _ = get_day_ohlc(ticker)
    return o


def is_us_market_open():
    """True when NYSE/NASDAQ are actively trading (conservative 13:00–21:00 UTC window covers DST)."""
    now_utc = datetime.now(timezone.utc)
    if now_utc.weekday() >= 5:
        return False
    market_open  = now_utc.replace(hour=13, minute=0,  second=0, microsecond=0)
    market_close = now_utc.replace(hour=21, minute=0,  second=0, microsecond=0)
    return market_open <= now_utc < market_close


def _verify_signal(sig, open_px, day_high, day_low, current):
    """Fill verification fields into a signal dict in-place. Returns True if updated."""
    entry  = sig.get('current_price')
    action = sig.get('action', 'HOLD')
    if not entry or current is None:
        return False
    real_entry = open_px if open_px else entry
    pct        = (current - real_entry) / real_entry * 100
    pct_signal = (current - entry)      / entry      * 100
    sig['actual_price']        = current
    sig['open_price']          = open_px
    sig['day_high']            = day_high
    sig['day_low']             = day_low
    sig['pct_change']          = round(pct, 2)
    sig['pct_from_prev_close'] = round(pct_signal, 2)
    if action == 'BUY':
        sig['correct']           = pct > 0
        sig['correct_direction'] = pct_signal > 0
    elif action == 'SELL':
        sig['correct']           = pct < 0
        sig['correct_direction'] = pct_signal < 0
    else:
        sig['correct']           = abs(pct) < 2
        sig['correct_direction'] = abs(pct_signal) < 2
    GAP_THRESHOLD = 0.01
    if open_px:
        gap_pct = (open_px - entry) / entry
        if action == 'BUY':
            sig['gap_filtered'] = gap_pct > GAP_THRESHOLD
        elif action == 'SELL':
            sig['gap_filtered'] = gap_pct < -GAP_THRESHOLD
        else:
            sig['gap_filtered'] = False
        sig['gap_pct'] = round(gap_pct * 100, 2)
    else:
        sig['gap_filtered'] = False
        sig['gap_pct']      = None
    if action == 'BUY':
        sig['limit_filled'] = bool(day_low  and day_low  <= entry)
    elif action == 'SELL':
        sig['limit_filled'] = bool(day_high and day_high >= entry)
    else:
        sig['limit_filled'] = False
    gap_tag   = ' [GAP SKIP]' if sig['gap_filtered'] else ''
    limit_tag = ' [LIMIT✓]'   if sig['limit_filled'] else ' [LIMIT✗]'
    print(f"[accuracy] {sig['ticker']} {action}: signal=${entry} open=${open_px} close=${current} ({pct:+.2f}%){gap_tag}{limit_tag} → {'✓' if sig['correct'] else '✗'}")
    return True


def check_unverified_accuracy():
    """Scan ALL history files for unverified signals and fill in outcomes.

    Fixes two bugs in the old check_yesterday_accuracy():
      1. Only checked yesterday — if a run was delayed or skipped, that day was PERMANENTLY lost.
      2. Used get_day_ohlc() (latest prices) for all files — if verifying an older file on a later
         date, the wrong OHLC date was used (e.g. June 3 signals verified with June 5 prices).

    Now: every unverified file is checked on every run, using the signal file's own date to
    fetch the correct OHLC via get_ohlc_for_date(). This is robust to multi-day delays.
    """
    if is_us_market_open():
        print("[warn] US market currently open — skipping accuracy fill to avoid incomplete OHLC")
        return

    for fname in sorted(os.listdir(HISTORY_DIR)):
        if not fname.endswith('.json') or '-report' in fname or fname == f"{today}.json":
            continue
        file_date = fname.replace('.json', '')
        fpath     = os.path.join(HISTORY_DIR, fname)
        try:
            with open(fpath) as f:
                hist_data = json.load(f)
        except Exception as e:
            print(f"[warn] Could not read {fname}: {e}")
            continue

        pending = [s for s in hist_data.get('signals', []) if 'correct' not in s]
        if not pending:
            continue

        print(f"[accuracy] {len(pending)} unverified signal(s) in {file_date} — fetching OHLC...")
        updated = False
        for sig in pending:
            ticker = sig.get('ticker')
            if not ticker:
                continue
            # Always use the signal file's own date for OHLC — this is the trade session
            # (signal was generated pre-market for `file_date`; trade happened during `file_date`)
            open_px, day_high, day_low, current = get_ohlc_for_date(ticker, file_date)
            if current is None:
                # Fallback: latest data (works if file_date is yesterday and market is closed)
                open_px, day_high, day_low, current = get_day_ohlc(ticker)
            if _verify_signal(sig, open_px, day_high, day_low, current):
                updated = True

        if updated:
            with open(fpath, 'w') as f:
                json.dump(hist_data, f, ensure_ascii=False, indent=2)


def build_accuracy():
    history = []
    total = correct = 0
    for fname in sorted(os.listdir(HISTORY_DIR)):
        if not fname.endswith('.json') or fname == f"{today}.json":
            continue
        try:
            with open(os.path.join(HISTORY_DIR, fname)) as f:
                h = json.load(f)
            for sig in h.get('signals', []):
                if 'correct' in sig:
                    total += 1
                    if sig['correct']:
                        correct += 1
                    history.append(sig['correct'])
        except Exception:
            pass
    return {
        "total": total,
        "correct": correct,
        "rate": round(correct / total, 3) if total > 0 else None,
        "history": history[-10:]
    }


# ── Main ──────────────────────────────────────────────

check_unverified_accuracy()

selected_picks = select_stocks()
if not selected_picks:
    morning_file = f"dashboard/morning-note-history/{today}.json"
    fallback_file = f"dashboard/morning-note-history/{yesterday}.json"
    if not os.path.exists(morning_file) and not os.path.exists(fallback_file):
        print(f"[abort] Morning note for {today} (and {yesterday}) not found. Exiting without writing signal file.")
        sys.exit(0)
    print("[warn] No stocks selected (morning note exists but no valid buy picks).")
    data = {
        "date": today, "generated_at": generated_at,
        "signals": [], "accuracy": build_accuracy(), "api_cost_usd": 0.0
    }
else:
    def analyze_pick(pick):
        ticker = pick['ticker']
        for attempt in range(3):
            try:
                state, decision = run_tradingagents(ticker)
                report = extract_full_report(state)
                # parse action BEFORE translating — translated Chinese text breaks keyword matching
                action = parse_action(decision or report.get("final", ""))
                report = translate_report_to_chinese(report, ticker)
                # 回填模式：信号价 = 回填日期前一天的收盘价（正常交易前的信号基准）
                price = get_close_for_date(ticker, yesterday) if _backfill else get_price(ticker)
                target = round(price * 1.10, 2) if price else None
                stop = round(price * 0.95, 2) if price else None
                summary = summarize(report)
                # save full report as backup file
                report_path = os.path.join(HISTORY_DIR, f"{today}-{ticker}-report.json")
                with open(report_path, "w", encoding="utf-8") as rf:
                    json.dump({"date": today, "ticker": ticker, "action": action,
                               "current_price": price, "report": report}, rf,
                              ensure_ascii=False, indent=2)
                print(f"[signal] {ticker}: {action} @ ${price} → target ${target} / stop ${stop}")
                return {
                    "ticker": ticker,
                    "name": pick.get('name', ''),
                    "sector": pick.get('sector', ''),
                    "action": action,
                    "current_price": price,
                    "target_price": target,
                    "stop_loss": stop,
                    "summary": summary,
                    "report": report,
                }
            except Exception as e:
                if '529' in str(e) or 'overloaded' in str(e).lower():
                    wait = 30 * (attempt + 1)
                    print(f"[warn] API overloaded for {ticker}, retry {attempt+1}/3 in {wait}s...")
                    time.sleep(wait)
                else:
                    print(f"[error] TradingAgents failed for {ticker}: {e}")
                    break
        price = get_close_for_date(ticker, yesterday) if _backfill else get_price(ticker)
        return {
            "ticker": ticker,
            "name": pick.get('name', ''),
            "sector": pick.get('sector', ''),
            "action": "HOLD",
            "current_price": price,
            "target_price": round(price * 1.10, 2) if price else None,
            "stop_loss": round(price * 0.95, 2) if price else None,
            "summary": f"API 过载，暂无深度分析",
        }

    signals = []
    hold_fallbacks = []
    for pick in selected_picks:
        sig = analyze_pick(pick)
        if sig['action'] != 'HOLD':
            signals.append(sig)
            print(f"[accept] {pick['ticker']}: {sig['action']} — added ({len(signals)}/2)")
        else:
            hold_fallbacks.append(sig)
            print(f"[skip-hold] {pick['ticker']}: HOLD — trying next candidate")
        if len(signals) >= 2:
            break
    # Fill up to 2 with HOLDs only if we ran out of directional signals
    if len(signals) < 2:
        needed = 2 - len(signals)
        signals.extend(hold_fallbacks[:needed])
        print(f"[warn] Only {len(signals) - needed} directional signals found, padded with {needed} HOLD(s)")

    # claude-haiku-4-5 pricing: $0.80/MTok in, $4.00/MTok out
    api_cost = round(_total_input_tokens * 0.8 / 1_000_000 + _total_output_tokens * 4.0 / 1_000_000, 4)
    print(f"[cost] tokens in={_total_input_tokens} out={_total_output_tokens} cost=${api_cost}")
    data = {
        "date": today,
        "generated_at": generated_at,
        "signals": signals,
        "accuracy": build_accuracy(),
        "api_cost_usd": api_cost
    }

os.makedirs("dashboard", exist_ok=True)
js_content = (
    "// TradingAgents 信号数据 — 每日 20:30 自动更新\n"
    f"window.TRADING_SIGNALS = {json.dumps(data, ensure_ascii=False, indent=2)};\n"
)
with open("dashboard/trading-signals.js", "w", encoding="utf-8") as f:
    f.write(js_content)

archive_path = os.path.join(HISTORY_DIR, f"{today}.json")
with open(archive_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ Trading signals generated for {today}: {[s['ticker'] for s in data['signals']]}")

# 回填模式：当天市场已收盘，立即填入实际 OHLC（复用 check_unverified_accuracy 逻辑）
if _backfill and data['signals']:
    print(f"[backfill] 立即验证 {today} 的信号（该日市场已收盘）...")
    archive_path_bf = os.path.join(HISTORY_DIR, f"{today}.json")
    with open(archive_path_bf) as f:
        bf_data = json.load(f)
    updated = False
    for sig in bf_data.get('signals', []):
        if 'correct' in sig:
            continue
        ticker = sig.get('ticker')
        if not ticker:
            continue
        open_px, day_high, day_low, current = get_ohlc_for_date(ticker, today)
        if current is None:
            print(f"[warn] 无法获取 {ticker} 在 {today} 的数据，跳过验证")
            continue
        if _verify_signal(sig, open_px, day_high, day_low, current):
            updated = True
    if updated:
        with open(archive_path_bf, 'w') as f:
            json.dump(bf_data, f, ensure_ascii=False, indent=2)
        data = bf_data
        js_content = (
            "// TradingAgents 信号数据 — 每日 20:30 自动更新\n"
            f"window.TRADING_SIGNALS = {json.dumps(data, ensure_ascii=False, indent=2)};\n"
        )
        with open("dashboard/trading-signals.js", "w", encoding="utf-8") as f:
            f.write(js_content)
        print(f"[backfill] 验证完成，已写回 {archive_path_bf}")


# ── Plan B 模拟盘：开仓登记 ──────────────────────────────────────
def update_portfolio_b(new_signals, signal_date):
    portfolio_path = "data/portfolio_b.json"
    os.makedirs("data", exist_ok=True)
    if os.path.exists(portfolio_path):
        with open(portfolio_path) as f:
            portfolio = json.load(f)
    else:
        portfolio = {"capital_usd": 1000, "open_positions": [], "closed_positions": []}

    open_tickers = {p["ticker"] for p in portfolio["open_positions"]}
    for sig in new_signals:
        action = sig.get("action")
        ticker = sig.get("ticker")
        if action not in ("BUY", "SELL") or not ticker:
            continue
        if ticker in open_tickers:
            print(f"[portfolio-b] {ticker} already open, skip")
            continue
        entry_price = sig.get("current_price")
        if not entry_price:
            continue
        # Take profit +8%, stop loss -4% (from entry, direction-adjusted)
        take_profit = round(entry_price * (1.08 if action == "BUY" else 0.92), 2)
        stop_loss   = round(entry_price * (0.96 if action == "BUY" else 1.04), 2)
        # Max hold = 5 trading days from signal date
        sig_dt = datetime.strptime(signal_date, "%Y-%m-%d")
        trading_days = 0
        max_dt = sig_dt
        while trading_days < 5:
            max_dt += timedelta(days=1)
            if max_dt.weekday() < 5:
                trading_days += 1
        position = {
            "ticker": ticker,
            "name": sig.get("name", ""),
            "action": action,
            "signal_date": signal_date,
            "entry_price": entry_price,
            "allocated_usd": 500,
            "take_profit": take_profit,
            "stop_loss": stop_loss,
            "max_hold_date": max_dt.strftime("%Y-%m-%d"),
            "daily_prices": {},
        }
        portfolio["open_positions"].append(position)
        print(f"[portfolio-b] Opened {action} {ticker} @ ${entry_price} | TP ${take_profit} | SL ${stop_loss} | max {max_dt.strftime('%Y-%m-%d')}")

    with open(portfolio_path, "w") as f:
        json.dump(portfolio, f, ensure_ascii=False, indent=2)

update_portfolio_b(data.get("signals", []), today)

# ── Plan C：与 Plan B 相同逻辑开仓，跳空过滤在 daily-report.py 收盘后判断 ──
def update_portfolio_c(new_signals, signal_date):
    portfolio_path = "data/portfolio_c.json"
    os.makedirs("data", exist_ok=True)
    if os.path.exists(portfolio_path):
        with open(portfolio_path) as f:
            portfolio = json.load(f)
    else:
        portfolio = {"capital_usd": 1000, "open_positions": [], "closed_positions": [],
                     "_note": "Plan C: TP+8%/SL-4%/5日 + 不利跳空>1.5%跳过"}

    open_tickers = {p["ticker"] for p in portfolio["open_positions"]}
    for sig in new_signals:
        action = sig.get("action")
        ticker = sig.get("ticker")
        if action not in ("BUY", "SELL") or not ticker:
            continue
        if ticker in open_tickers:
            print(f"[portfolio-c] {ticker} already open, skip")
            continue
        entry_price = sig.get("current_price")
        if not entry_price:
            continue
        take_profit = round(entry_price * (1.08 if action == "BUY" else 0.92), 2)
        stop_loss   = round(entry_price * (0.96 if action == "BUY" else 1.04), 2)
        sig_dt = datetime.strptime(signal_date, "%Y-%m-%d")
        trading_days, max_dt = 0, sig_dt
        while trading_days < 5:
            max_dt += timedelta(days=1)
            if max_dt.weekday() < 5:
                trading_days += 1
        position = {
            "ticker": ticker, "name": sig.get("name", ""),
            "action": action, "signal_date": signal_date,
            "entry_price": entry_price, "allocated_usd": 500,
            "take_profit": take_profit, "stop_loss": stop_loss,
            "max_hold_date": max_dt.strftime("%Y-%m-%d"),
            "gap_checked": False,   # daily-report 收盘后检查跳空
            "daily_prices": {},
        }
        portfolio["open_positions"].append(position)
        print(f"[portfolio-c] Opened {action} {ticker} @ ${entry_price} (gap check pending)")

    with open(portfolio_path, "w") as f:
        json.dump(portfolio, f, ensure_ascii=False, indent=2)

update_portfolio_c(data.get("signals", []), today)

# Sync to Cloudflare KV so all devices get fresh data without redeployment
import urllib.request, urllib.error
SYNC_URL = 'https://questrade-proxy.chengchuang-lai.workers.dev/sync'
UA = {'User-Agent': 'DashboardSync/1.0'}
try:
    req = urllib.request.Request(SYNC_URL, headers=UA)
    current = json.loads(urllib.request.urlopen(req, timeout=10).read())
    if not isinstance(current, dict):
        current = {}
    current['trading_signals'] = data
    body = json.dumps(current, ensure_ascii=False).encode('utf-8')
    req2 = urllib.request.Request(SYNC_URL, data=body,
                                   headers={**UA, 'Content-Type': 'application/json'},
                                   method='POST')
    urllib.request.urlopen(req2, timeout=10)
    print('✅ KV 同步成功 — 所有设备将在下次加载时获取最新信号')
except Exception as e:
    print(f'⚠️ KV 同步失败（不影响本地文件）: {e}')
