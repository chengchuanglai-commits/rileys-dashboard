"""
信号 edge 分析 — 用已有的 trading-signals-history + SPY 基准，回答"AI 信号到底有没有 edge"

口径（避免前视偏差）：
  - 入场 = 信号文件里记录的 current_price（信号价/prev close）
  - 出场 = signal_date 之后第 N 个交易日的收盘价
  - 方向 P&L = 个股收益 ×(+1 BUY / -1 SELL)
  - 市场中性 alpha = (个股收益 - SPY同窗收益) ×(+1 BUY / -1 SELL)
      （把信号当多空组合 vs 大盘，剔除 beta；做空时个股跑输 SPY 才算赢）

多个持仓窗 N（1/3/5 日）都报，看 edge 在哪个时间尺度。
纯只读，不写任何文件。
"""
import json, os, sys
from datetime import datetime
import yfinance as yf

HISTORY_DIR = "dashboard/trading-signals-history"
HORIZONS = [1, 3, 5]          # 评估的持仓交易日数
BENCH = "SPY"

# ── 收集所有已发出的信号 ───────────────────────────────────────
def load_signals():
    sigs = []
    for fname in sorted(os.listdir(HISTORY_DIR)):
        if not fname.endswith(".json") or "-report" in fname:
            continue
        date = fname.replace(".json", "")
        try:
            data = json.load(open(os.path.join(HISTORY_DIR, fname)))
        except Exception:
            continue
        for s in data.get("signals", []):
            action = s.get("action")
            entry = s.get("current_price")
            if action not in ("BUY", "SELL") or not entry:
                continue
            sigs.append({
                "date": data.get("date", date),
                "ticker": s.get("ticker"),
                "action": action,
                "entry": float(entry),
            })
    return sigs

# ── 取某 ticker 在 signal_date 之后第 N 个交易日的收盘价 ──────────
def fwd_close(prices, signal_date, n):
    """prices: dict{date_str: close}。返回 signal_date 之后第 n 个交易日(close)，没有则 None。"""
    dates = sorted(d for d in prices if d > signal_date)
    if len(dates) < n:
        return None
    return prices[dates[n - 1]]

def fetch_closes(ticker, start, end):
    try:
        df = yf.Ticker(ticker).history(start=start, end=end)
        out = {}
        for idx, row in df.iterrows():
            c = float(row["Close"])
            if c == c and c > 0:          # 跳过 NaN / 非正价格
                out[str(idx)[:10]] = round(c, 4)
        return out
    except Exception as e:
        print(f"  [warn] {ticker} fetch failed: {e}")
        return {}

# ── 主流程 ─────────────────────────────────────────────────────
def main():
    signals = load_signals()
    if not signals:
        print("没有可分析的信号")
        return
    dmin = min(s["date"] for s in signals)
    dmax = max(s["date"] for s in signals)
    print(f"信号样本: {len(signals)} 条，{dmin} ~ {dmax}\n")

    # 价格区间：最早信号日 ~ 最晚信号日 + 缓冲
    start = dmin
    end = (datetime.strptime(dmax, "%Y-%m-%d")).strftime("%Y-%m-%d")
    # 多取 15 天缓冲覆盖最长持仓窗
    end_buf = datetime.strptime(dmax, "%Y-%m-%d")
    from datetime import timedelta
    end_buf = (end_buf + timedelta(days=15)).strftime("%Y-%m-%d")

    tickers = sorted(set(s["ticker"] for s in signals))
    print(f"拉取 {len(tickers)} 只个股 + {BENCH} 价格 ({start} ~ {end_buf})...")
    px = {t: fetch_closes(t, start, end_buf) for t in tickers}
    spy = fetch_closes(BENCH, start, end_buf)
    print()

    summary = []   # 供 dashboard 用
    # 对每个持仓窗 N 汇总
    for n in HORIZONS:
        rows = []
        for s in signals:
            closes = px.get(s["ticker"], {})
            exit_px = fwd_close(closes, s["date"], n)
            # SPY 入场：用 signal_date 当天收盘（信号价同口径），出场同 N 日
            spy_entry = spy.get(s["date"])
            spy_exit = fwd_close(spy, s["date"], n)
            if exit_px is None or spy_entry is None or spy_exit is None:
                continue
            stock_ret = (exit_px - s["entry"]) / s["entry"]
            spy_ret = (spy_exit - spy_entry) / spy_entry
            sign = 1 if s["action"] == "BUY" else -1
            pnl = stock_ret * sign                       # 方向 P&L
            alpha = (stock_ret - spy_ret) * sign         # 市场中性 alpha
            rows.append({"pnl": pnl, "alpha": alpha, **s})

        if not rows:
            print(f"=== 持仓 {n} 日：无足够数据 ===\n")
            continue

        k = len(rows)
        hit = sum(1 for r in rows if r["pnl"] > 0)
        hit_a = sum(1 for r in rows if r["alpha"] > 0)
        avg_pnl = sum(r["pnl"] for r in rows) / k * 100
        avg_alpha = sum(r["alpha"] for r in rows) / k * 100
        # 方向命中率的二项标准误
        p = hit / k
        se = (p * (1 - p) / k) ** 0.5
        ci_lo, ci_hi = max(0, p - 1.96 * se), min(1, p + 1.96 * se)

        print(f"=== 持仓 {n} 个交易日（n={k} 条有效）===")
        print(f"  方向命中率:   {p*100:5.1f}%   95%CI [{ci_lo*100:.0f}%, {ci_hi*100:.0f}%]")
        print(f"  跑赢SPY比例:  {hit_a/k*100:5.1f}%   (alpha>0)")
        print(f"  平均方向收益: {avg_pnl:+5.2f}% / 笔")
        print(f"  平均alpha:    {avg_alpha:+5.2f}% / 笔   ← 剔除大盘后的真实 edge")
        verdict = "✅ 初步有正 edge" if avg_alpha > 0 and p > 0.5 else ("⚠️ 与噪声难区分" if 0.4 < p < 0.6 else "❌ 无 edge")
        print(f"  判定: {verdict}（样本{'偏小，仅供参考' if k < 30 else ''}）\n")
        summary.append({
            "horizon": n, "n": k,
            "hit_rate": round(p * 100, 1),
            "ci_lo": round(ci_lo * 100), "ci_hi": round(ci_hi * 100),
            "beat_spy_pct": round(hit_a / k * 100, 1),
            "avg_pnl": round(avg_pnl, 2), "avg_alpha": round(avg_alpha, 2),
            "verdict": verdict,
        })

    print("注：样本 <30 时置信区间很宽，结论仅为方向性参考，不能作为实盘依据。")

    # 写 dashboard 数据文件
    out = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "sample_total": len(signals),
        "date_range": [dmin, dmax],
        "benchmark": BENCH,
        "horizons": summary,
    }
    os.makedirs("dashboard", exist_ok=True)
    with open("dashboard/signal-edge.js", "w") as f:
        f.write("// 信号 edge 分析 — analyze-signal-edge.py 自动生成\n")
        f.write("window.SIGNAL_EDGE = " + json.dumps(out, ensure_ascii=False, indent=2) + ";\n")
    print("→ dashboard/signal-edge.js 已更新")

if __name__ == "__main__":
    main()
