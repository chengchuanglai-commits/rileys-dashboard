import anthropic
import json
import os
import sys
import time
import yfinance as yf
from datetime import datetime, timezone, timedelta

client = anthropic.Anthropic(max_retries=5)

beijing_tz = timezone(timedelta(hours=8))
now_beijing = datetime.now(beijing_tz)
today = now_beijing.strftime('%Y-%m-%d')
generated_at = now_beijing.strftime('%Y-%m-%dT%H:%M:00')


def fetch_market_data():
    sp = yf.Ticker("ES=F")
    hist = sp.history(period="5d")
    sp500_pct = round(
        (float(hist['Close'].iloc[-1]) - float(hist['Close'].iloc[-2])) /
        float(hist['Close'].iloc[-2]) * 100, 2
    )
    tnx = yf.Ticker("^TNX")
    tnx_hist = tnx.history(period="5d")
    treasury_now = round(float(tnx_hist['Close'].iloc[-1]), 3)
    treasury_prev = round(float(tnx_hist['Close'].iloc[-2]), 3)
    treasury_bps = round((treasury_now - treasury_prev) * 100, 1)
    return {"sp500_pct": sp500_pct, "treasury_10y": treasury_now, "treasury_bps": treasury_bps}


save_tool = {
    "name": "save_morning_note",
    "description": "Save the generated financial morning note data",
    "input_schema": {
        "type": "object",
        "properties": {
            "market": {
                "type": "object",
                "properties": {
                    "sp500_futures_pct": {"type": "number"},
                    "treasury_10y": {"type": "number"},
                    "treasury_10y_change_bps": {"type": "number"},
                    "eps_beat_rate": {"type": "number"}
                },
                "required": ["sp500_futures_pct", "treasury_10y", "treasury_10y_change_bps", "eps_beat_rate"]
            },
            "note": {
                "type": "object",
                "properties": {
                    "market_overview": {"type": "string"},
                    "macro": {"type": "string"},
                    "earnings": {"type": "string"},
                    "trade_ideas": {"type": "string"}
                },
                "required": ["market_overview", "macro", "earnings", "trade_ideas"]
            },
            "stock_picks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "ticker": {"type": "string"},
                        "name": {"type": "string"},
                        "sector": {"type": "string"},
                        "direction": {"type": "string", "enum": ["buy", "sell", "watch"]},
                        "buy_zone": {"type": "string"},
                        "target": {"type": "string"},
                        "stop_loss": {"type": "string"},
                        "reason": {"type": "string"}
                    },
                    "required": ["ticker", "name", "sector", "direction", "buy_zone", "target", "stop_loss", "reason"]
                }
            },
        },
        "required": ["market", "note", "stock_picks"]
    }
}


def call_with_retry(market_data, max_attempts=5):
    search_prompt = (
        f"今天是{today}。\n\n"
        f"市场数据（已确认）：\n"
        f"- S&P 500 期货：{market_data['sp500_pct']:+.2f}%\n"
        f"- 10年期美债：{market_data['treasury_10y']:.3f}%（{market_data['treasury_bps']:+.1f} bps）\n\n"
        f"请用 web_search 搜索今日各板块值得关注的小盘/中盘股"
        f"（科技/半导体/能源/核能/医疗/生物科技/消费必需/消费可选/金融/固收ETF，每板块1支共10支），"
        f"同时获取当前财报季EPS超预期率。\n\n"
        f"选股要求：市值在$5亿–$100亿之间，禁止出现：NVDA、AAPL、MSFT、AMZN、GOOGL、GOOG、META、TSLA、"
        f"JPM、JNJ、XOM、BRK、V、MA、UNH、PG、HD、CVX、MRK、ABBV、BAC、KO、PEP、COST、WMT、AVGO、TSM、"
        f"LLY、ORCL、NFLX、AMD、INTC、TLT、BND、SPY、QQQ。"
    )

    for attempt in range(max_attempts):
        try:
            # Turn 1: web research only
            print(f"[morning] Turn 1: web search (attempt {attempt+1}/{max_attempts})...")
            resp1 = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=8000,
                tools=[{"type": "web_search_20250305", "name": "web_search"}],
                messages=[{"role": "user", "content": search_prompt}]
            )
            ct1 = [getattr(b, 'type', str(b)) for b in resp1.content]
            print(f"[morning] Turn 1 done. Content types: {ct1}")

            research_text = "\n\n".join(
                block.text for block in resp1.content
                if hasattr(block, 'type') and block.type == 'text' and block.text.strip()
            )

            # Turn 2: force save_morning_note with gathered research
            print(f"[morning] Turn 2: forcing save_morning_note...")
            resp2 = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=8000,
                tools=[save_tool],
                tool_choice={"type": "tool", "name": "save_morning_note"},
                messages=[{"role": "user", "content": (
                    f"根据以下市场研究结果，调用save_morning_note工具保存结构化数据。\n\n"
                    f"今日市场数据：\n"
                    f"- S&P 500 期货：{market_data['sp500_pct']:+.2f}%\n"
                    f"- 10年期美债：{market_data['treasury_10y']:.3f}%（变动 {market_data['treasury_bps']:+.1f} bps）\n\n"
                    f"研究结果：\n{research_text}\n\n"
                    f"保存要求：\n"
                    f"- market.eps_beat_rate: 当前财报季EPS超预期率（纯数字，如75.5）\n"
                    f"- stock_picks: 正好10支股票，每板块1支，市值$5亿–$100亿\n"
                    f"- note和stock_picks中的reason字段用中文\n"
                    f"- direction只能是 buy/sell/watch 之一\n"
                    f"- 严禁包含以下大市值股票（黑名单）：NVDA、AAPL、MSFT、AMZN、GOOGL、GOOG、META、TSLA、"
                    f"JPM、JNJ、XOM、BRK、V、MA、UNH、PG、HD、CVX、MRK、ABBV、BAC、KO、PEP、COST、WMT、"
                    f"AVGO、TSM、LLY、ORCL、NFLX、AMD、INTC、TLT、BND、SPY、QQQ"
                )}]
            )
            ct2 = [getattr(b, 'type', str(b)) for b in resp2.content]
            print(f"[morning] Turn 2 done. Content types: {ct2}")
            return resp1, resp2

        except anthropic.RateLimitError:
            if attempt == max_attempts - 1:
                raise
            wait = 60 * (attempt + 1)
            print(f"Rate limit hit, waiting {wait}s before retry {attempt + 2}/{max_attempts}...")
            time.sleep(wait)
    raise RuntimeError("call_with_retry: all attempts exhausted without response")


def write_balance_warning_note(today):
    data = {
        "date": today,
        "generated_at": generated_at,
        "market_status": "pre-market",
        "market": {"sp500_futures_pct": 0, "treasury_10y": 0, "treasury_10y_change_bps": 0, "eps_beat_rate": 0},
        "note": {
            "market_overview": "⚠️ Anthropic API 余额不足，请前往 console.anthropic.com/billing 充值后恢复。",
            "macro": "",
            "earnings": "",
            "trade_ideas": ""
        },
        "stock_picks": [],
        "api_cost_usd": 0,
        "balance_warning": True,
        "estimated_days_left": 0,
        "cumulative_cost_usd": 0,
        "avg_daily_cost_usd": 0,
        "budget_usd": float(os.environ.get("ANTHROPIC_BUDGET_USD", "5"))
    }
    os.makedirs("dashboard", exist_ok=True)
    js_content = (
        "// 金融晨报数据 — 每日 07:30 自动更新\n"
        f"window.MORNING_NOTE = {json.dumps(data, ensure_ascii=False, indent=2)};\n"
    )
    with open("dashboard/morning-note.js", "w", encoding="utf-8") as f:
        f.write(js_content)
    os.makedirs("dashboard/morning-note-history", exist_ok=True)
    with open(f"dashboard/morning-note-history/{today}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"⚠️  Balance warning note written for {today}")


# ── Main execution ──────────────────────────────────────────────────────────

try:
    market_data = fetch_market_data()
    print(f"[market] S&P futures: {market_data['sp500_pct']:+.2f}% | 10Y: {market_data['treasury_10y']:.3f}% ({market_data['treasury_bps']:+.1f}bps)")
except Exception as e:
    print(f"⚠️  yfinance fetch failed: {e}. Using zero values.")
    market_data = {"sp500_pct": 0.0, "treasury_10y": 0.0, "treasury_bps": 0.0}

try:
    resp1, response = call_with_retry(market_data)
except anthropic.BadRequestError as e:
    if 'credit balance' in str(e).lower():
        print(f"⚠️  Anthropic credit balance too low: {e}")
        write_balance_warning_note(today)
        sys.exit(0)
    raise

# Extract save_morning_note tool call from turn 2
data = None
for block in response.content:
    if hasattr(block, 'type') and block.type == "tool_use" and block.name == "save_morning_note":
        data = block.input
        print(f"[debug] save_morning_note called, keys: {list(data.keys())}")

if data is None:
    content_types = [getattr(b, 'type', str(b)) for b in response.content]
    raise ValueError(f"save_morning_note not called. Content types: {content_types}")

# Override market data with yfinance values (more accurate than AI's text output)
data["market"]["sp500_futures_pct"] = market_data["sp500_pct"]
data["market"]["treasury_10y"] = market_data["treasury_10y"]
data["market"]["treasury_10y_change_bps"] = market_data["treasury_bps"]

# Add metadata
data["date"] = today
data["generated_at"] = generated_at
data["market_status"] = "pre-market"

BLACKLIST = {
    "NVDA","AAPL","MSFT","AMZN","GOOGL","GOOG","META","TSLA","JPM","JNJ","XOM",
    "BRK","V","MA","UNH","PG","HD","CVX","MRK","ABBV","BAC","KO","PEP","COST",
    "WMT","AVGO","TSM","LLY","ORCL","NFLX","AMD","INTC","TLT","BND","SPY","QQQ"
}

# Validate and fix stock_picks type (model sometimes returns JSON string instead of array)
if "stock_picks" not in data:
    raise ValueError(f"stock_picks missing. Got keys: {list(data.keys())}")
picks = data["stock_picks"]
if isinstance(picks, str):
    picks = json.loads(picks)
    data["stock_picks"] = picks

# Filter out blacklisted large-cap stocks
before = len(picks)
picks = [p for p in picks if p.get("ticker","").upper() not in BLACKLIST]
data["stock_picks"] = picks
if len(picks) < before:
    removed = before - len(picks)
    print(f"[filter] Removed {removed} blacklisted ticker(s). Remaining: {len(picks)}")

print(f"[debug] stock_picks count: {len(picks)}, type: {type(picks)}")
if len(picks) == 0:
    raise ValueError(f"Expected picks, got 0 after blacklist filter")
if len(picks) != 10:
    print(f"[warn] Expected 10 picks, got {len(picks)} — continuing anyway")
for pick in picks:
    if pick.get("direction") not in ("buy", "sell", "watch"):
        pick["direction"] = "watch"

# Calculate API cost across both turns (claude-haiku-4-5: $0.80/MTok in, $4/MTok out)
total_in  = resp1.usage.input_tokens  + response.usage.input_tokens
total_out = resp1.usage.output_tokens + response.usage.output_tokens
data["api_cost_usd"] = round(total_in * 0.8 / 1_000_000 + total_out * 4.0 / 1_000_000, 4)
print(f"[debug] tokens in={total_in} out={total_out} cost=${data['api_cost_usd']}")

# Calculate cumulative cost from history files
history_dir = "dashboard/morning-note-history"
os.makedirs(history_dir, exist_ok=True)
cumulative = 0.0
day_costs = []
for fname in sorted(os.listdir(history_dir)):
    if fname.endswith(".json") and fname != f"{today}.json":
        try:
            with open(os.path.join(history_dir, fname)) as fh:
                h = json.load(fh)
                c = h.get("api_cost_usd", 0) or 0
                cumulative += c
                day_costs.append(c)
        except Exception:
            pass
cumulative += data["api_cost_usd"]
day_costs.append(data["api_cost_usd"])
avg_daily = sum(day_costs[-7:]) / max(len(day_costs[-7:]), 1)  # 7-day avg

budget = float(os.environ.get("ANTHROPIC_BUDGET_USD", "5"))
remaining = max(budget - cumulative, 0)
days_left = int(remaining / avg_daily) if avg_daily > 0 else 999

data["budget_usd"] = budget
data["cumulative_cost_usd"] = round(cumulative, 4)
data["avg_daily_cost_usd"] = round(avg_daily, 4)
data["estimated_days_left"] = days_left
data["balance_warning"] = days_left <= 7

print(f"[budget] cumulative=${cumulative:.4f} avg_daily=${avg_daily:.4f} days_left={days_left} warning={data['balance_warning']}")

# Write morning-note.js
js_content = (
    "// 金融晨报数据 — 每日 07:30 自动更新\n"
    f"window.MORNING_NOTE = {json.dumps(data, ensure_ascii=False, indent=2)};\n"
)

os.makedirs("dashboard", exist_ok=True)
with open("dashboard/morning-note.js", "w", encoding="utf-8") as f:
    f.write(js_content)

# Write history archive
os.makedirs("dashboard/morning-note-history", exist_ok=True)
archive_path = f"dashboard/morning-note-history/{today}.json"
with open(archive_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ Morning note generated for {today}")
print(f"   S&P futures: {data['market']['sp500_futures_pct']}%")
print(f"   10Y Treasury: {data['market']['treasury_10y']}%")
print(f"   Stock picks: {[p['ticker'] for p in data['stock_picks']]}")

# Sync to Cloudflare KV so all devices get fresh data without redeployment
import urllib.request, urllib.error
SYNC_URL = 'https://questrade-proxy.chengchuang-lai.workers.dev/sync'
UA = {'User-Agent': 'DashboardSync/1.0'}
try:
    req = urllib.request.Request(SYNC_URL, headers=UA)
    current = json.loads(urllib.request.urlopen(req, timeout=10).read())
    if not isinstance(current, dict):
        current = {}
    current['morning_note'] = data
    body = json.dumps(current, ensure_ascii=False).encode('utf-8')
    req2 = urllib.request.Request(SYNC_URL, data=body,
                                   headers={**UA, 'Content-Type': 'application/json'},
                                   method='POST')
    urllib.request.urlopen(req2, timeout=10)
    print('✅ KV 同步成功 — 所有设备将在下次加载时获取最新晨报')
except Exception as e:
    print(f'⚠️ KV 同步失败（不影响本地文件）: {e}')
