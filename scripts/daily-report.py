"""
每日自检报告 — 在 generate-trading-signals.py 之后运行
输出: dashboard/daily-report.json (最新一天，dashboard 读取)
      dashboard/daily-reports/{date}.json (历史存档)
"""
import json
import os
from datetime import datetime, timezone, timedelta

beijing_tz = timezone(timedelta(hours=8))
now_beijing = datetime.now(beijing_tz)
today = now_beijing.strftime('%Y-%m-%d')
yesterday = (now_beijing - timedelta(days=1)).strftime('%Y-%m-%d')

SIGNALS_DIR = "dashboard/trading-signals-history"
MORNING_DIR = "dashboard/morning-note-history"
REPORT_DIR  = "dashboard/daily-reports"
os.makedirs(REPORT_DIR, exist_ok=True)

report = {
    "date": today,
    "generated_at": now_beijing.strftime('%Y-%m-%dT%H:%M:00'),
    "pipeline": {},
    "data_quality": [],
    "signals_today": [],
    "accuracy_update": {},
    "running_totals": {},
    "warnings": [],
    "api_cost_usd": 0.0,
}

# ── 1. Pipeline 状态 ──────────────────────────────────────────

morning_file = f"{MORNING_DIR}/{today}.json"
signal_file  = f"{SIGNALS_DIR}/{today}.json"

morning_found = os.path.exists(morning_file)
signal_found  = os.path.exists(signal_file)

report["pipeline"]["morning_note_found"] = morning_found
report["pipeline"]["signal_file_found"]  = signal_found

if not morning_found:
    report["warnings"].append(f"晨报文件不存在: {morning_file}（周末/节假日正常）")

if signal_found:
    with open(signal_file) as f:
        sig_data = json.load(f)
    signals = sig_data.get("signals", [])
    report["pipeline"]["signals_generated"] = len(signals)
    report["api_cost_usd"] = sig_data.get("api_cost_usd", 0.0)
    for s in signals:
        entry = {
            "ticker":        s.get("ticker"),
            "action":        s.get("action"),
            "current_price": s.get("current_price"),
            "target_price":  s.get("target_price"),
            "stop_loss":     s.get("stop_loss"),
        }
        report["signals_today"].append(entry)
        # 数据质量检查
        if not s.get("current_price"):
            report["warnings"].append(f"{s.get('ticker')}: current_price 为空")
        if not s.get("action") or s.get("action") == "HOLD":
            report["warnings"].append(f"{s.get('ticker')}: 信号为 HOLD（可能是 API 失败的 fallback）")
        if not s.get("report"):
            report["warnings"].append(f"{s.get('ticker')}: 无完整报告（翻译可能失败）")
else:
    report["pipeline"]["signals_generated"] = 0
    report["warnings"].append(f"信号文件不存在: {signal_file}")

# ── 2. 昨日准确率核验 ─────────────────────────────────────────

prev_file = f"{SIGNALS_DIR}/{yesterday}.json"
if os.path.exists(prev_file):
    with open(prev_file) as f:
        prev = json.load(f)
    prev_signals = prev.get("signals", [])
    verified = [s for s in prev_signals if "correct" in s]
    pending  = [s for s in prev_signals if "correct" not in s]
    report["accuracy_update"] = {
        "date":     yesterday,
        "total":    len(prev_signals),
        "verified": len(verified),
        "pending":  len(pending),
        "results":  [
            {
                "ticker":    s.get("ticker"),
                "action":    s.get("action"),
                "entry":     s.get("current_price"),
                "open":      s.get("open_price"),
                "actual":    s.get("actual_price"),
                "pct":       s.get("pct_change"),
                "correct":   s.get("correct"),
            }
            for s in verified
        ],
    }
    if pending:
        tickers = [s.get("ticker") for s in pending]
        report["warnings"].append(f"昨日信号未完成验证: {tickers}（可能是节假日，次交易日自动补填）")
else:
    report["accuracy_update"] = {"date": yesterday, "total": 0, "note": "无历史信号文件"}

# ── 3. 累计统计 ───────────────────────────────────────────────

total = correct = 0
sim_capital = 1000.0
daily_returns = []

for fname in sorted(os.listdir(SIGNALS_DIR)):
    if not fname.endswith('.json') or '-report' in fname or fname == f"{today}.json":
        continue
    try:
        with open(os.path.join(SIGNALS_DIR, fname)) as f:
            h = json.load(f)
        day_signals = [s for s in h.get("signals", []) if "correct" in s]
        if not day_signals:
            continue
        per_trade = sim_capital / len(day_signals)
        day_end = 0.0
        for s in day_signals:
            total += 1
            pct = s.get("pct_change", 0) or 0
            action = s.get("action", "HOLD")
            if action == "BUY":
                gain = per_trade * pct / 100
            elif action == "SELL":
                gain = per_trade * (-pct) / 100
            else:
                gain = 0
            day_end += per_trade + gain
            if s["correct"]:
                correct += 1
        daily_return = (day_end - sim_capital) / sim_capital * 100
        daily_returns.append(round(daily_return, 3))
        sim_capital = day_end
    except Exception as e:
        report["warnings"].append(f"统计文件读取失败 {fname}: {e}")

accuracy_rate = round(correct / total, 3) if total > 0 else None
sim_pnl = round(sim_capital - 1000.0, 2)
sim_pnl_pct = round((sim_capital / 1000.0 - 1) * 100, 2)

report["running_totals"] = {
    "total_signals_verified": total,
    "correct": correct,
    "accuracy_rate": accuracy_rate,
    "accuracy_pct": f"{round(accuracy_rate*100,1)}%" if accuracy_rate else "N/A",
    "simulated_capital": round(sim_capital, 2),
    "simulated_pnl_usd": sim_pnl,
    "simulated_pnl_pct": f"{sim_pnl_pct:+.2f}%",
    "daily_returns": daily_returns,
}

# ── 4. 数据质量小结 ───────────────────────────────────────────

report["data_quality"] = [
    {"check": "晨报文件",       "pass": morning_found,  "detail": today},
    {"check": "信号文件",       "pass": signal_found,   "detail": today},
    {"check": "昨日准确率填充", "pass": report["accuracy_update"].get("pending", 0) == 0,
     "detail": f"{report['accuracy_update'].get('verified', 0)} 条已验证"},
    {"check": "无警告",         "pass": len(report["warnings"]) == 0,
     "detail": f"{len(report['warnings'])} 条警告"},
]

# ── 5. 输出 ──────────────────────────────────────────────────

# 固定路径（dashboard 读取）
with open("dashboard/daily-report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

# 历史存档
archive_path = os.path.join(REPORT_DIR, f"{today}.json")
with open(archive_path, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

# ── 终端打印 ──────────────────────────────────────────────────

print(f"\n{'='*55}")
print(f"  📊 每日自检报告 — {today}")
print(f"{'='*55}")
print(f"  Pipeline    晨报:{('✅' if morning_found else '⚠️ ')}  信号:{('✅' if signal_found else '⚠️ ')}  今日信号:{report['pipeline'].get('signals_generated',0)}条")
print(f"  成本        ${report['api_cost_usd']:.4f}")

rt = report["running_totals"]
print(f"  累计准确率  {rt['accuracy_pct']}  ({rt['correct']}/{rt['total_signals_verified']} 条已验证)")
print(f"  模拟收益    {rt['simulated_pnl_pct']}  (${rt['simulated_capital']:.2f})")

au = report["accuracy_update"]
if au.get("results"):
    print(f"\n  昨日 ({yesterday}) 验证结果:")
    for r in au["results"]:
        mark = '✓' if r.get("correct") else '✗'
        open_str = f"  开盘${r['open']}" if r.get('open') else ''
        print(f"    {mark} {r['ticker']} {r['action']}  入场${r['entry']}{open_str}  收盘${r['actual']}  {r['pct']:+.2f}%")

if report["warnings"]:
    print(f"\n  ⚠️  警告 ({len(report['warnings'])}):")
    for w in report["warnings"]:
        print(f"    - {w}")

dq_pass = all(c["pass"] for c in report["data_quality"])
print(f"\n  自检状态    {'✅ 全部通过' if dq_pass else '⚠️  有项目未通过'}")
print(f"{'='*55}\n")
