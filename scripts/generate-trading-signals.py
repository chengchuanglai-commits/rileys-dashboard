import json
import os
import sys
import time
import yfinance as yf
from datetime import datetime, timezone, timedelta
from unittest.mock import patch

beijing_tz = timezone(timedelta(hours=8))
now_beijing = datetime.now(beijing_tz)
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


def select_stocks():
    history_file = f"dashboard/morning-note-history/{today}.json"
    if not os.path.exists(history_file):
        print(f"[warn] Morning note not found: {history_file}")
        return []
    with open(history_file) as f:
        data = json.load(f)
    picks = data.get('stock_picks', [])
    sp500 = data.get('market', {}).get('sp500_futures_pct', 0)
    buy_picks = [p for p in picks if p.get('direction') == 'buy']
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
    if 'BUY' in d:
        return 'BUY'
    if 'SELL' in d:
        return 'SELL'
    return 'HOLD'


def summarize(decision_str, max_chars=600):
    lines = [l.strip() for l in decision_str.splitlines() if l.strip()]
    text = '\n'.join(lines)
    return text[:max_chars] + ('…' if len(text) > max_chars else '')


def get_price(ticker):
    try:
        hist = yf.Ticker(ticker).history(period="5d")
        if len(hist) == 0:
            return None
        return round(float(hist['Close'].iloc[-1]), 2)
    except Exception as e:
        print(f"[warn] yfinance price fetch failed for {ticker}: {e}")
        return None


def check_yesterday_accuracy():
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
        current = get_price(ticker)
        if current is None:
            continue
        pct = (current - entry) / entry * 100
        sig['actual_price'] = current
        sig['pct_change'] = round(pct, 2)
        if action == 'BUY':
            sig['correct'] = pct > 0
        elif action == 'SELL':
            sig['correct'] = pct < 0
        else:
            sig['correct'] = abs(pct) < 2
        print(f"[accuracy] {ticker} {action}: entry=${entry} actual=${current} ({pct:+.2f}%) → {'✓' if sig['correct'] else '✗'}")
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
    print("[warn] No stocks selected. Writing empty signal file.")
    data = {
        "date": today, "generated_at": generated_at,
        "signals": [], "accuracy": build_accuracy(), "api_cost_usd": 0.0
    }
else:
    signals = []
    for pick in selected_picks:
        ticker = pick['ticker']
        try:
            state, decision = run_tradingagents(ticker)
            action = parse_action(decision)
            price = get_price(ticker)
            target = round(price * 1.10, 2) if price else None
            stop = round(price * 0.95, 2) if price else None
            summary = summarize(decision)
            signals.append({
                "ticker": ticker,
                "name": pick.get('name', ''),
                "sector": pick.get('sector', ''),
                "action": action,
                "current_price": price,
                "target_price": target,
                "stop_loss": stop,
                "summary": summary,
            })
            print(f"[signal] {ticker}: {action} @ ${price} → target ${target} / stop ${stop}")
        except Exception as e:
            print(f"[error] TradingAgents failed for {ticker}: {e}")
            signals.append({
                "ticker": ticker,
                "name": pick.get('name', ''),
                "sector": pick.get('sector', ''),
                "action": "HOLD",
                "current_price": get_price(ticker),
                "target_price": None,
                "stop_loss": None,
                "summary": f"分析失败: {str(e)[:100]}",
            })

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
