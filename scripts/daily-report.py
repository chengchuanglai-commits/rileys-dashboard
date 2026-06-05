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
total_d = correct_d = 0              # plan D: limit order at signal price
total_active = 0                     # non-HOLD signals
sim_exec = sim_dir = sim_gap = sim_d = 1000.0
daily_dates = []
daily_returns = []
daily_returns_dir = []
daily_returns_gap = []
daily_returns_d = []
# cumulative capital per day (starts at 1000)
cum_exec = [1000.0]
cum_dir  = [1000.0]
cum_gap  = [1000.0]
cum_d    = [1000.0]
signals_history = []  # all verified signals across all days

for fname in sorted(os.listdir(SIGNALS_DIR)):
    if not fname.endswith('.json') or '-report' in fname or fname == f"{today}.json":
        continue
    try:
        date_label = fname.replace('.json', '')
        with open(os.path.join(SIGNALS_DIR, fname)) as f:
            h = json.load(f)
        day_signals = [s for s in h.get("signals", []) if "correct" in s]
        if not day_signals:
            continue
        n = len(day_signals)
        active_sigs = [s for s in day_signals if s.get("action", "HOLD") != "HOLD"]
        n_active_day = len(active_sigs) if active_sigs else 1  # avoid /0
        per_exec = sim_exec / n_active_day
        per_dir  = sim_dir  / n_active_day
        per_gap  = sim_gap  / n_active_day
        day_exec = day_dir = day_gap = day_d = 0.0
        # plan D: allocate only among limit_filled non-HOLD signals
        d_sigs = [s for s in day_signals if s.get("limit_filled") and s.get("action") != "HOLD"]
        per_d = sim_d / len(d_sigs) if d_sigs else 0
        for s in day_signals:
            total += 1
            action     = s.get("action", "HOLD")
            pct_open   = s.get("pct_change", 0) or 0
            pct_signal = s.get("pct_from_prev_close", 0) or 0
            skipped    = s.get("gap_filtered", False)
            filled     = s.get("limit_filled", False)
            if action == "BUY":
                day_exec += per_exec * pct_open / 100
                day_dir  += per_dir  * pct_signal / 100
                if not skipped: day_gap += per_gap * pct_open / 100
                if filled:      day_d   += per_d   * pct_signal / 100
            elif action == "SELL":
                day_exec += per_exec * (-pct_open) / 100
                day_dir  += per_dir  * (-pct_signal) / 100
                if not skipped: day_gap += per_gap * (-pct_open) / 100
                if filled:      day_d   += per_d   * (-pct_signal) / 100
            if action != "HOLD": total_active += 1
            if s.get("correct"):           correct_exec += 1
            if s.get("correct_direction"): correct_dir  += 1
            if not skipped and action != "HOLD":
                total_gap += 1
                if s.get("correct"): correct_gap += 1
            if filled and action != "HOLD":
                total_d += 1
                if s.get("correct_direction"): correct_d += 1
        for s in day_signals:
            signals_history.append({
                "date":             date_label,
                "ticker":           s.get("ticker"),
                "name":             s.get("name", ""),
                "action":           s.get("action", "HOLD"),
                "signal_price":     s.get("current_price"),
                "open_price":       s.get("open_price"),
                "close_price":      s.get("actual_price"),
                "pct_change":       s.get("pct_change"),
                "pct_from_signal":  s.get("pct_from_prev_close"),
                "correct":          s.get("correct"),
                "correct_direction":s.get("correct_direction"),
                "limit_filled":     s.get("limit_filled", False),
                "gap_filtered":     s.get("gap_filtered", False),
            })
        daily_dates.append(date_label)
        daily_returns.append(round((day_exec / sim_exec) * 100, 3))
        daily_returns_dir.append(round((day_dir / sim_dir) * 100, 3))
        daily_returns_gap.append(round((day_gap / sim_gap) * 100, 3))
        daily_returns_d.append(round((day_d / sim_d) * 100, 3))
        sim_exec += day_exec
        sim_dir  += day_dir
        sim_gap  += day_gap
        sim_d    += day_d
        cum_exec.append(round(sim_exec, 2))
        cum_dir.append(round(sim_dir, 2))
        cum_gap.append(round(sim_gap, 2))
        cum_d.append(round(sim_d, 2))
    except Exception as e:
        report["warnings"].append(f"统计文件读取失败 {fname}: {e}")

acc_exec = round(correct_exec / total, 3) if total > 0 else None
acc_dir  = round(correct_dir  / total, 3) if total > 0 else None
acc_gap  = round(correct_gap  / total_gap, 3) if total_gap > 0 else None
acc_d    = round(correct_d    / total_d,   3) if total_d   > 0 else None

report["running_totals"] = {
    "total_signals_verified": total,
    "total_signals_active": total_active,
    "total_signals_hold": total - total_active,
    "hold_rate_pct": round((total - total_active) / total * 100, 1) if total > 0 else 0,
    # 选股历史记录（时间倒序）
    "signals_history": list(reversed(signals_history)),
    # 曲线图用：日期标签 + 累计资金（含起始$1000）
    "daily_dates": daily_dates,
    "cum_capital_a": cum_exec,
    "cum_capital_b": cum_dir,
    "cum_capital_c": cum_gap,
    "cum_capital_d": cum_d,
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
    # D. 限价单（信号价触及才入场）
    "total_limit": total_d,
    "correct_limit": correct_d,
    "accuracy_limit_rate": acc_d,
    "accuracy_limit_pct": f"{round(acc_d*100,1)}%" if acc_d else "N/A",
    "simulated_capital_limit": round(sim_d, 2),
    "simulated_pnl_limit_usd": round(sim_d - 1000.0, 2),
    "simulated_pnl_limit_pct": f"{(sim_d/1000-1)*100:+.2f}%",
    "daily_returns_limit": daily_returns_d,
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

# JS 变量文件（file:// 协议下 fetch 不可用，改为 script 注入）
with open("dashboard/daily-report.js", "w", encoding="utf-8") as f:
    f.write("// 每日自检报告 — 自动生成，勿手动修改\n")
    f.write(f"window.DAILY_REPORT = {json.dumps(report, ensure_ascii=False)};\n")

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
n_d   = rt['total_limit']
skipped  = n_all - n_gap
n_active = rt.get('total_signals_active', n_all)  # non-HOLD signals
missed   = n_active - n_d if n_active >= n_d else 0
print(f"  {'':12} {'A 开盘市价':<18} {'B AI方向':<18} {'C 过滤跳空':<18} {'D 限价单'}")
print(f"  {'准确率':<12} {rt['accuracy_pct']} ({rt['correct']}/{n_all}){'':<5} "
      f"{rt['accuracy_direction_pct']} ({rt['correct_direction']}/{n_all}){'':<3} "
      f"{rt['accuracy_gap_pct']} ({rt['correct_gap']}/{n_gap}){'':<5} "
      f"{rt['accuracy_limit_pct']} ({rt['correct_limit']}/{n_d})")
print(f"  {'模拟本金':<12} ${rt['simulated_capital']:.2f}{'':<11} "
      f"${rt['simulated_capital_direction']:.2f}{'':<8} "
      f"${rt['simulated_capital_gap']:.2f}{'':<9} "
      f"${rt['simulated_capital_limit']:.2f}")
print(f"  {'累计盈亏':<12} {rt['simulated_pnl_pct']}{'':<13} "
      f"{rt['simulated_pnl_direction_pct']}{'':<9} "
      f"{rt['simulated_pnl_gap_pct']}{'':<10} "
      f"{rt['simulated_pnl_limit_pct']}")
print(f"  跳空损失(A-B):-${rt['gap_cost_usd']:.2f}  限价优势(D-A):+${rt['simulated_capital_limit']-rt['simulated_capital']:.2f}  错过{missed}笔")

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

# ── Plan B 模拟盘：更新持仓价格，平仓判断，生成 portfolio-b.js ────
import yfinance as yf

PORTFOLIO_PATH = "data/portfolio_b.json"

def _trading_days_between(start_str, end_str):
    start = datetime.strptime(start_str, "%Y-%m-%d")
    end   = datetime.strptime(end_str,   "%Y-%m-%d")
    d = start
    count = 0
    while d < end:
        d += timedelta(days=1)
        if d.weekday() < 5:
            count += 1
    return count

def refresh_portfolio_b():
    if not os.path.exists(PORTFOLIO_PATH):
        return
    with open(PORTFOLIO_PATH) as f:
        portfolio = json.load(f)

    still_open = []
    for pos in portfolio.get("open_positions", []):
        ticker   = pos["ticker"]
        action   = pos["action"]
        entry    = pos["entry_price"]
        tp       = pos["take_profit"]
        sl       = pos["stop_loss"]
        max_date = pos["max_hold_date"]

        try:
            df = yf.Ticker(ticker).history(period="5d")
            if df.empty:
                still_open.append(pos)
                continue
            close_today = round(float(df["Close"].iloc[-1]), 2)
            date_today  = df.index[-1].strftime("%Y-%m-%d")
        except Exception as e:
            print(f"[portfolio-b] {ticker} 价格获取失败: {e}")
            still_open.append(pos)
            continue

        # P&L direction: BUY profits when price rises, SELL when falls
        raw_pct = (close_today - entry) / entry * 100
        pnl_pct = raw_pct if action == "BUY" else -raw_pct
        pos["daily_prices"][date_today] = {
            "close": close_today,
            "pnl_pct": round(pnl_pct, 2)
        }

        # Close conditions
        close_reason = None
        if action == "BUY":
            if close_today >= tp:  close_reason = "take_profit"
            elif close_today <= sl: close_reason = "stop_loss"
        else:
            if close_today <= tp:  close_reason = "take_profit"
            elif close_today >= sl: close_reason = "stop_loss"
        if date_today >= max_date:
            close_reason = close_reason or "max_hold"

        if close_reason:
            realized_usd = round(pos["allocated_usd"] * pnl_pct / 100, 2)
            closed = {**pos, "close_date": date_today, "close_price": close_today,
                      "final_pnl_pct": round(pnl_pct, 2), "close_reason": close_reason,
                      "realized_pnl_usd": realized_usd}
            portfolio["closed_positions"].append(closed)
            print(f"[portfolio-b] Closed {action} {ticker} @ ${close_today} ({close_reason}) {pnl_pct:+.2f}% / ${realized_usd:+.2f}")
        else:
            still_open.append(pos)

    portfolio["open_positions"] = still_open

    # Summary stats
    all_closed = portfolio.get("closed_positions", [])
    wins = [p for p in all_closed if p.get("final_pnl_pct", 0) > 0]
    total_realized = sum(p.get("realized_pnl_usd", 0) for p in all_closed)
    open_unrealized = sum(
        pos["allocated_usd"] * list(pos["daily_prices"].values())[-1]["pnl_pct"] / 100
        for pos in still_open if pos["daily_prices"]
    )
    portfolio["stats"] = {
        "total_trades": len(all_closed),
        "win_trades": len(wins),
        "win_rate": round(len(wins) / len(all_closed) * 100, 1) if all_closed else 0,
        "total_realized_pnl_usd": round(total_realized, 2),
        "open_unrealized_pnl_usd": round(open_unrealized, 2),
        "portfolio_value": round(portfolio["capital_usd"] + total_realized + open_unrealized, 2),
        "updated_at": today,
    }

    with open(PORTFOLIO_PATH, "w") as f:
        json.dump(portfolio, f, ensure_ascii=False, indent=2)

    # Generate dashboard JS
    with open("dashboard/portfolio-b.js", "w", encoding="utf-8") as f:
        f.write("// Plan B 模拟盘持仓 — 每日自动更新\n")
        f.write(f"window.PORTFOLIO_B = {json.dumps(portfolio, ensure_ascii=False, indent=2)};\n")

    s = portfolio["stats"]
    print(f"\n  💼 Plan B 模拟盘  持仓:{len(still_open)}  已平:{s['total_trades']}  "
          f"胜率:{s['win_rate']}%  已实现:{s['total_realized_pnl_usd']:+.2f}  "
          f"浮盈:{s['open_unrealized_pnl_usd']:+.2f}  组合价值:${s['portfolio_value']}")

refresh_portfolio_b()

# ── Plan C 模拟盘：同 Plan B，但首个交易日检查不利跳空 >1.5% 则取消 ──
GAP_FILTER_PCT = 1.5

def refresh_portfolio_c():
    path = "data/portfolio_c.json"
    if not os.path.exists(path):
        return
    with open(path) as f:
        portfolio = json.load(f)

    still_open = []
    for pos in portfolio.get("open_positions", []):
        ticker   = pos["ticker"]
        action   = pos["action"]
        entry    = pos["entry_price"]
        tp       = pos["take_profit"]
        sl       = pos["stop_loss"]
        max_date = pos["max_hold_date"]

        try:
            df = yf.Ticker(ticker).history(period="5d")
            if df.empty:
                still_open.append(pos)
                continue
            close_today = round(float(df["Close"].iloc[-1]), 2)
            open_today  = round(float(df["Open"].iloc[-1]), 2)
            date_today  = df.index[-1].strftime("%Y-%m-%d")
        except Exception as e:
            print(f"[portfolio-c] {ticker} 价格获取失败: {e}")
            still_open.append(pos)
            continue

        # ── 跳空过滤：首次更新时检查 day-1 open ──
        if not pos.get("gap_checked"):
            gap_pct = (open_today - entry) / entry * 100
            unfavorable = -gap_pct if action == "BUY" else gap_pct
            pos["gap_checked"] = True
            pos["day1_open"] = open_today
            pos["day1_gap_pct"] = round(gap_pct, 2)
            if unfavorable > GAP_FILTER_PCT:
                print(f"[portfolio-c] {action} {ticker} 跳空过滤: open={open_today} gap={gap_pct:+.1f}% (不利>{GAP_FILTER_PCT}%) → 取消")
                continue   # 不加入 still_open，相当于取消

        raw_pct = (close_today - entry) / entry * 100
        pnl_pct = raw_pct if action == "BUY" else -raw_pct
        pos["daily_prices"][date_today] = {"close": close_today, "pnl_pct": round(pnl_pct, 2)}

        close_reason = None
        if action == "BUY":
            if close_today >= tp:   close_reason = "take_profit"
            elif close_today <= sl: close_reason = "stop_loss"
        else:
            if close_today <= tp:   close_reason = "take_profit"
            elif close_today >= sl: close_reason = "stop_loss"
        if date_today >= max_date:
            close_reason = close_reason or "max_hold"

        if close_reason:
            realized_usd = round(pos["allocated_usd"] * pnl_pct / 100, 2)
            closed = {**pos, "close_date": date_today, "close_price": close_today,
                      "final_pnl_pct": round(pnl_pct, 2), "close_reason": close_reason,
                      "realized_pnl_usd": realized_usd}
            portfolio["closed_positions"].append(closed)
            print(f"[portfolio-c] Closed {action} {ticker} @ ${close_today} ({close_reason}) {pnl_pct:+.2f}% / ${realized_usd:+.2f}")
        else:
            still_open.append(pos)

    portfolio["open_positions"] = still_open

    all_closed = portfolio.get("closed_positions", [])
    wins = [p for p in all_closed if p.get("final_pnl_pct", 0) > 0]
    total_realized = sum(p.get("realized_pnl_usd", 0) for p in all_closed)
    open_unrealized = sum(
        pos["allocated_usd"] * list(pos["daily_prices"].values())[-1]["pnl_pct"] / 100
        for pos in still_open if pos["daily_prices"]
    )
    skipped = portfolio.get("stats", {}).get("skipped_gap", 0)
    portfolio["stats"] = {
        "total_trades": len(all_closed),
        "win_trades": len(wins),
        "win_rate": round(len(wins) / len(all_closed) * 100, 1) if all_closed else 0,
        "total_realized_pnl_usd": round(total_realized, 2),
        "open_unrealized_pnl_usd": round(open_unrealized, 2),
        "portfolio_value": round(portfolio["capital_usd"] + total_realized + open_unrealized, 2),
        "skipped_gap": skipped,
        "updated_at": today,
    }

    with open(path, "w") as f:
        json.dump(portfolio, f, ensure_ascii=False, indent=2)

    with open("dashboard/portfolio-c.js", "w", encoding="utf-8") as f:
        f.write("// Plan C 模拟盘持仓 — 每日自动更新（跳空过滤版）\n")
        f.write(f"window.PORTFOLIO_C = {json.dumps(portfolio, ensure_ascii=False, indent=2)};\n")

    s = portfolio["stats"]
    print(f"\n  💼 Plan C 模拟盘  持仓:{len(still_open)}  已平:{s['total_trades']}  "
          f"胜率:{s['win_rate']}%  已实现:{s['total_realized_pnl_usd']:+.2f}  "
          f"跳过跳空:{s['skipped_gap']}  组合价值:${s['portfolio_value']}")

refresh_portfolio_c()

dq_pass = all(c["pass"] for c in report["data_quality"])
print(f"\n  自检状态    {'✅ 全部通过' if dq_pass else '⚠️  有项目未通过'}")
print(f"{'='*55}\n")
