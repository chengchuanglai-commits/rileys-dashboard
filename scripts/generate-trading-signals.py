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
    buy_picks = [p for p in picks
                 if p.get('direction') == 'buy'
                 and p.get('ticker', '').upper() not in BLACKLIST]
    if sp500 >= 0:
        preferred = ['科技', '半导体', '消费可选', '能源']
    else:
        preferred = ['医疗', '消费必需', '生物科技', '固收']
    buy_picks.sort(key=lambda p: 1 if any(s in p.get('sector', '') for s in preferred) else 0, reverse=True)
    selected = buy_picks[:2]
    print(f"[select] Selected {[p['ticker'] for p in selected]} from {len(buy_picks)} buy picks (S&P {sp500:+.2f}%)")
    return selected


def run_tradingagents(ticker):
    from tradingagents.graph.trading_graph import TradingAgentsGraph
    from tradingagents.default_config import DEFAULT_CONFIG
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = "anthropic"
    config["deep_think_llm"] = "claude-haiku-4-5-20251001"
    config["quick_think_llm"] = "claude-haiku-4-5-20251001"
    config["max_debate_rounds"] = 1
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


def check_yesterday_accuracy():
    if is_us_market_open():
        print("[warn] US market currently open — skipping accuracy fill to avoid incomplete OHLC; will run on next scheduled execution")
        return
    prev_file = os.path.join(HISTORY_DIR, f"{yesterday}.json")
    if not os.path.exists(prev_file):
        return
    with open(prev_file) as f:
        prev = json.load(f)
    updated = False
    for sig in prev.get('signals', []):
        if 'correct' in sig:
            continue
        ticker = sig.get('ticker')
        action = sig.get('action')
        entry = sig.get('current_price')
        if not ticker or not action or not entry:
            continue
        open_px, day_high, day_low, current = get_day_ohlc(ticker)
        if current is None:
            continue
        # use open price as real entry if available (more accurate than prev close)
        real_entry = open_px if open_px else entry
        pct = (current - real_entry) / real_entry * 100
        pct_signal = (current - entry) / entry * 100   # signal price → close (AI direction quality)
        sig['actual_price'] = current
        sig['open_price'] = open_px
        sig['day_high'] = day_high
        sig['day_low'] = day_low
        sig['pct_change'] = round(pct, 2)                        # open → close (execution P&L)
        sig['pct_from_prev_close'] = round(pct_signal, 2)        # signal → close (AI direction)
        # correct_execution: did we make money after gap/slippage?
        if action == 'BUY':
            sig['correct'] = pct > 0
        elif action == 'SELL':
            sig['correct'] = pct < 0
        else:
            sig['correct'] = abs(pct) < 2
        # correct_direction: was AI's directional call right (ignoring gap)?
        if action == 'BUY':
            sig['correct_direction'] = pct_signal > 0
        elif action == 'SELL':
            sig['correct_direction'] = pct_signal < 0
        else:
            sig['correct_direction'] = abs(pct_signal) < 2
        # gap filter: skip trade if open deviates from signal price by > 1%
        GAP_THRESHOLD = 0.01
        if open_px:
            gap_pct = (open_px - entry) / entry
            if action == 'BUY':
                sig['gap_filtered'] = gap_pct > GAP_THRESHOLD     # gapped up too much, skip
            elif action == 'SELL':
                sig['gap_filtered'] = gap_pct < -GAP_THRESHOLD    # already dropped, skip
            else:
                sig['gap_filtered'] = False
            sig['gap_pct'] = round(gap_pct * 100, 2)
        else:
            sig['gap_filtered'] = False
            sig['gap_pct'] = None
        # plan D: limit order at signal price — filled if price touches signal level intraday
        if action == 'BUY':
            sig['limit_filled'] = bool(day_low and day_low <= entry)
        elif action == 'SELL':
            sig['limit_filled'] = bool(day_high and day_high >= entry)
        else:
            sig['limit_filled'] = False
        gap_tag = ' [GAP SKIP]' if sig['gap_filtered'] else ''
        limit_tag = ' [LIMIT✓]' if sig['limit_filled'] else ' [LIMIT✗]'
        print(f"[accuracy] {ticker} {action}: signal=${entry} open=${open_px} close=${current} ({pct:+.2f}% from open){gap_tag}{limit_tag} → {'✓' if sig['correct'] else '✗'}")
        updated = True
    if updated:
        with open(prev_file, 'w') as f:
            json.dump(prev, f, ensure_ascii=False, indent=2)


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

check_yesterday_accuracy()

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
    for pick in selected_picks:
        signals.append(analyze_pick(pick))

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

# 回填模式：当天市场已收盘，立即填入实际 OHLC（不等次日运行）
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
        action = sig.get('action')
        entry  = sig.get('current_price')
        if not ticker or not action or not entry:
            continue
        open_px, day_high, day_low, current = get_ohlc_for_date(ticker, today)
        if current is None:
            print(f"[warn] 无法获取 {ticker} 在 {today} 的数据，跳过验证")
            continue
        real_entry = open_px if open_px else entry
        pct = (current - real_entry) / real_entry * 100
        pct_signal = (current - entry) / entry * 100
        sig['actual_price'] = current
        sig['open_price']   = open_px
        sig['day_high']     = day_high
        sig['day_low']      = day_low
        sig['pct_change']          = round(pct, 2)
        sig['pct_from_prev_close'] = round(pct_signal, 2)
        if action == 'BUY':
            sig['correct']           = pct > 0
            sig['correct_direction'] = pct_signal > 0
            gap_pct = (open_px - entry) / entry if open_px else 0
            sig['gap_filtered']      = gap_pct > 0.01
            sig['limit_filled']      = bool(day_low and day_low <= entry)
        elif action == 'SELL':
            sig['correct']           = pct < 0
            sig['correct_direction'] = pct_signal < 0
            gap_pct = (open_px - entry) / entry if open_px else 0
            sig['gap_filtered']      = gap_pct < -0.01
            sig['limit_filled']      = bool(day_high and day_high >= entry)
        else:
            sig['correct']           = abs(pct) < 2
            sig['correct_direction'] = abs(pct_signal) < 2
            sig['gap_filtered']      = False
            sig['limit_filled']      = False
        sig['gap_pct'] = round((open_px - entry) / entry * 100, 2) if open_px else None
        lim_tag = ' [限价✓]' if sig['limit_filled'] else ' [限价✗]'
        print(f"[backfill verify] {ticker} {action}: 信号${entry} 开${open_px} 收${current} ({pct:+.2f}%){lim_tag} → {'✓' if sig['correct'] else '✗'}")
        updated = True
    if updated:
        with open(archive_path_bf, 'w') as f:
            json.dump(bf_data, f, ensure_ascii=False, indent=2)
        # 同步更新 trading-signals.js 和主 data 对象
        data = bf_data
        js_content = (
            "// TradingAgents 信号数据 — 每日 20:30 自动更新\n"
            f"window.TRADING_SIGNALS = {json.dumps(data, ensure_ascii=False, indent=2)};\n"
        )
        with open("dashboard/trading-signals.js", "w", encoding="utf-8") as f:
            f.write(js_content)
        print(f"[backfill] 验证完成，已写回 {archive_path_bf}")

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
