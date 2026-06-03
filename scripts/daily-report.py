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
                "ticker":            s.get("ticker"),
                "action":            s.get("action"),
                "entry":             s.get("current_price"),
                "open":              s.get("open_price"),
                "actual":            s.get("actual_price"),
                "pct":               s.get("pct_change"),
                "pct_from_signal":   s.get("pct_from_prev_close"),
                "correct":           s.get("correct"),
                "correct_direction": s.get("correct_direction"),
            }
            for s in verified
        ],
    }
    if pending:
        tickers = [s.get("ticker") for s in pending]
        report["warnings"].append(f"昨日信号未完成验证: {tickers}（可能是节假日，次交易日自动补填）")
else:
    report["accuracy_update"] = {"date": yesterday, "total": 0, "note": "无历史信号文件"}

# ── 3. 累计统计（双指标）────────────────────────────────────────

total = correct_exec = correct_dir = 0
total_gap = correct_gap = 0          # gap-filtered: only count non-skipped trades
sim_exec = sim_dir = sim_gap = 1000.0
daily_returns = []
daily_returns_dir = []
daily_returns_gap = []

for fname in sorted(os.listdir(SIGNALS_DIR)):
    if not fname.endswith('.json') or '-report' in fname or fname == f"{today}.json":
        continue
    try:
        with open(os.path.join(SIGNALS_DIR, fname)) as f:
            h = json.load(f)
        day_signals = [s for s in h.get("signals", []) if "correct" in s]
        if not day_signals:
            continue
        n = len(day_signals)
        per_exec = sim_exec / n
        per_dir  = sim_dir  / n
        per_gap  = sim_gap  / n
        day_exec = day_dir = day_gap = 0.0
        for s in day_signals:
            total += 1
            action     = s.get("action", "HOLD")
            pct_open   = s.get("pct_change", 0) or 0
            pct_signal = s.get("pct_from_prev_close", 0) or 0
            skipped    = s.get("gap_filtered", False)
            if action == "BUY":
                day_exec += per_exec * pct_open / 100
                day_dir  += per_dir  * pct_signal / 100
                if not skipped: day_gap += per_gap * pct_open / 100
            elif action == "SELL":
                day_exec += per_exec * (-pct_open) / 100
                day_dir  += per_dir  * (-pct_signal) / 100
                if not skipped: day_gap += per_gap * (-pct_open) / 100
            if s.get("correct"):           correct_exec += 1
            if s.get("correct_direction"): correct_dir  += 1
            if not skipped:
                total_gap += 1
                if s.get("correct"): correct_gap += 1
        daily_returns.append(round((day_exec / sim_exec) * 100, 3))
        daily_returns_dir.append(round((day_dir / sim_dir) * 100, 3))
        daily_returns_gap.append(round((day_gap / sim_gap) * 100, 3))
        sim_exec += day_exec
        sim_dir  += day_dir
        sim_gap  += day_gap
    except Exception as e:
        report["warnings"].append(f"统计文件读取失败 {fname}: {e}")

acc_exec = round(correct_exec / total, 3) if total > 0 else None
acc_dir  = round(correct_dir  / total, 3) if total > 0 else None
acc_gap  = round(correct_gap  / total_gap, 3) if total_gap > 0 else None

report["running_totals"] = {
    "total_signals_verified": total,
    # A. 执行准确率（开盘价入场，含跳空）
    "correct": correct_exec,
    "accuracy_rate": acc_exec,
    "accuracy_pct": f"{round(acc_exec*100,1)}%" if acc_exec else "N/A",
    "simulated_capital": round(sim_exec, 2),
    "simulated_pnl_usd": round(sim_exec - 1000.0, 2),
    "simulated_pnl_pct": f"{(sim_exec/1000-1)*100:+.2f}%",
    "daily_returns": daily_returns,
    # B. 方向准确率（信号价，AI预测质量）
    "correct_direction": correct_dir,
    "accuracy_direction_rate": acc_dir,
    "accuracy_direction_pct": f"{round(acc_dir*100,1)}%" if acc_dir else "N/A",
    "simulated_capital_direction": round(sim_dir, 2),
    "simulated_pnl_direction_usd": round(sim_dir - 1000.0, 2),
    "simulated_pnl_direction_pct": f"{(sim_dir/1000-1)*100:+.2f}%",
    "daily_returns_direction": daily_returns_dir,
    # C. 跳空过滤后（>1%跳空不入场）
    "total_gap_filtered": total_gap,
    "correct_gap": correct_gap,
    "accuracy_gap_rate": acc_gap,
    "accuracy_gap_pct": f"{round(acc_gap*100,1)}%" if acc_gap else "N/A",
    "simulated_capital_gap": round(sim_gap, 2),
    "simulated_pnl_gap_usd": round(sim_gap - 1000.0, 2),
    "simulated_pnl_gap_pct": f"{(sim_gap/1000-1)*100:+.2f}%",
    "daily_returns_gap": daily_returns_gap,
    "gap_cost_usd": round(sim_dir - sim_exec, 2),
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
n_all = rt['total_signals_verified']
n_gap = rt['total_gap_filtered']
skipped = n_all - n_gap
print(f"  {'':12} {'执行(含跳空)':<20} {'AI方向(信号价)':<20} {'过滤跳空(>1%不入)'}")
print(f"  {'准确率':<12} {rt['accuracy_pct']} ({rt['correct']}/{n_all}){'':<9} {rt['accuracy_direction_pct']} ({rt['correct_direction']}/{n_all}){'':<5} {rt['accuracy_gap_pct']} ({rt['correct_gap']}/{n_gap}, 跳过{skipped}笔)")
print(f"  {'模拟本金':<12} ${rt['simulated_capital']:.2f}{'':<14} ${rt['simulated_capital_direction']:.2f}{'':<10} ${rt['simulated_capital_gap']:.2f}")
print(f"  {'累计盈亏':<12} {rt['simulated_pnl_pct']}{'':<16} {rt['simulated_pnl_direction_pct']}{'':<12} {rt['simulated_pnl_gap_pct']}")
print(f"  跳空损失(A vs B): -${rt['gap_cost_usd']:.2f}  |  过滤收益(C vs A): +${rt['simulated_capital_gap']-rt['simulated_capital']:.2f}")

au = report["accuracy_update"]
if au.get("results"):
    print(f"\n  昨日 ({yesterday}) 验证结果:")
    for r in au["results"]:
        exec_mark = '✓' if r.get("correct") else '✗'
        dir_mark  = '✓' if r.get("correct_direction") else '✗'
        open_str  = f"  开盘${r['open']}" if r.get('open') else ''
        gap_note  = ' ←跳空' if exec_mark != dir_mark else ''
        print(f"    执行{exec_mark}/方向{dir_mark} {r['ticker']} {r['action']}  入场${r['entry']}{open_str}  收盘${r['actual']}  {r['pct']:+.2f}%{gap_note}")

if report["warnings"]:
    print(f"\n  ⚠️  警告 ({len(report['warnings'])}):")
    for w in report["warnings"]:
        print(f"    - {w}")

dq_pass = all(c["pass"] for c in report["data_quality"])
print(f"\n  自检状态    {'✅ 全部通过' if dq_pass else '⚠️  有项目未通过'}")
print(f"{'='*55}\n")
