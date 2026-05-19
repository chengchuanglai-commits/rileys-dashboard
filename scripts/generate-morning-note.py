import anthropic
import json
import os
import time
from datetime import datetime, timezone, timedelta

client = anthropic.Anthropic(max_retries=5)

beijing_tz = timezone(timedelta(hours=8))
now_beijing = datetime.now(beijing_tz)
today = now_beijing.strftime('%Y-%m-%d')
generated_at = now_beijing.strftime('%Y-%m-%dT%H:%M:00')

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
            "api_cost_usd": {"type": "number"}
        },
        "required": ["market", "note", "stock_picks"]
    }
}

def call_with_retry(max_attempts=5):
    for attempt in range(max_attempts):
        try:
            return client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=4096,
                tools=[
                    {"type": "web_search_20250305", "name": "web_search"},
                    save_tool
                ],
                messages=[{
                    "role": "user",
                    "content": f"今天是{today}。请用web_search搜索美股最新数据：①S&P500期货涨跌幅 ②10年期美债收益率及今日变化bps ③财报季EPS超预期率 ④来自科技/半导体/能源/核能/医疗/生物科技/消费必需/消费可选/金融/固收ETF这10个不同板块各一支值得关注的股票（共10支）。全部搜索完成后，调用save_morning_note工具一次性保存所有数据，note和reason字段必须用中文。"
                }]
            )
        except anthropic.RateLimitError:
            if attempt == max_attempts - 1:
                raise
            wait = 60 * (attempt + 1)
            print(f"Rate limit hit, waiting {wait}s before retry {attempt + 2}/{max_attempts}...")
            time.sleep(wait)

response = call_with_retry()

# Extract the LAST save_morning_note tool call (most complete)
data = None
for block in response.content:
    if hasattr(block, 'type') and block.type == "tool_use" and block.name == "save_morning_note":
        data = block.input
        print(f"[debug] save_morning_note called, keys: {list(data.keys())}")

if data is None:
    content_types = [getattr(b, 'type', str(b)) for b in response.content]
    raise ValueError(f"save_morning_note not called. Content types: {content_types}")

# Add metadata
data["date"] = today
data["generated_at"] = generated_at
data["market_status"] = "pre-market"

# Validate and fix stock_picks type (model sometimes returns JSON string instead of array)
if "stock_picks" not in data:
    raise ValueError(f"stock_picks missing. Got keys: {list(data.keys())}")
picks = data["stock_picks"]
if isinstance(picks, str):
    picks = json.loads(picks)
    data["stock_picks"] = picks
print(f"[debug] stock_picks count: {len(picks)}, type: {type(picks)}")
if len(picks) != 10:
    raise ValueError(f"Expected 10 picks, got {len(picks)}")
for pick in picks:
    if pick.get("direction") not in ("buy", "sell", "watch"):
        pick["direction"] = "watch"

# Calculate API cost (claude-sonnet-4-6 pricing)
usage = response.usage
input_cost  = usage.input_tokens  * 3.0  / 1_000_000
output_cost = usage.output_tokens * 15.0 / 1_000_000
data["api_cost_usd"] = round(input_cost + output_cost, 4)
print(f"[debug] tokens in={usage.input_tokens} out={usage.output_tokens} cost=${data['api_cost_usd']}")

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
