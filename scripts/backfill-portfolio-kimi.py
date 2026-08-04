"""kimi 影子腿回填:Kimi K2.6 信号 + 移动止损(init-4%/trail4%/10d/gap1.0)。
2026-07-30 上线:与 hdstr 完全同出场同资金,唯一变量=信号大脑(Kimi vs DeepSeek)。
裁决预注册:攒 80 笔平仓 → analyze-leg-edge 配对对比(见 memory project-kimi-ab-test);纯影子绝不碰真钱。
用法: python3 scripts/backfill-portfolio-kimi.py  (run.sh review 每日调用 + kimi-broad 云端调用,零API成本)"""
import os, sys, json, time

sys.path.insert(0, os.path.dirname(__file__))
import plan_variants as pv
from portfolio_compound import compound_portfolio

KM_DIR = "dashboard/trading-signals-history/kimi"
PORTFOLIO_PATH = "data/portfolio_kimi.json"
GAP = 1.0
INIT = 2000.0
NOTE = ("kimi 影子腿:Kimi K2.6 信号+移动止损(init-4%/trail4%/10d/gap1.0)。"
        "与 hdstr 同出场同资金,唯一变量=大脑;80笔平仓后配对裁决,纯影子不碰真钱。")


def _open_pct(p):
    dp = p.get("daily_prices") or {}
    return list(dp.values())[-1]["pnl_pct"] if dp else 0.0


def main():
    signals = []
    for fname in sorted(os.listdir(KM_DIR) if os.path.isdir(KM_DIR) else []):
        if fname.endswith("-kimi.json"):
            d = json.load(open(os.path.join(KM_DIR, fname)))
            sd = fname.replace("-kimi.json", "")
            for s in d.get("signals", []):
                signals.append((sd, s))

    closed, opens, gap_n = [], [], 0
    for sd, s in signals:
        tk, ac, ep = s.get("ticker"), s.get("action"), s.get("current_price")
        if ac not in ("BUY", "SELL") or not ep or ep != ep:
            continue
        cd, cp, reason, pct, daily, _ = pv.simulate_trail(tk, ac, ep, sd, 4, 4, 10, GAP)
        if reason == "gap_filtered":
            gap_n += 1; continue
        pos = {"ticker": tk, "action": ac, "signal_date": sd, "entry_price": ep,
               "close_date": cd, "close_price": cp, "close_reason": reason,
               "final_pnl_pct": pct, "daily_prices": daily}
        (opens if (reason == "open" or pct is None) else closed).append(pos)

    fc, fo, _pv_, realized, unreal, skipped = compound_portfolio(closed, opens, _open_pct, INIT)
    wins = sum(1 for p in fc if p.get("realized_pnl_usd", 0) > 0)
    n = len(fc)
    out = {
        "capital_usd": INIT, "_note": NOTE,
        "open_positions": fo, "closed_positions": fc,
        "stats": {
            "total_trades": n,
            "win_trades": wins,
            "win_rate": round(wins / n * 100, 1) if n else 0,
            "total_realized_pnl_usd": round(realized, 2),
            "open_unrealized_pnl_usd": round(unreal, 2),
            "portfolio_value": round(INIT + realized + unreal, 2),
            "skipped_gap": gap_n,
            "skipped_no_cash": skipped,
            "updated_at": time.strftime("%Y-%m-%d"),
        },
    }
    from ledger_guard import safe_write_ledger
    if not safe_write_ledger(PORTFOLIO_PATH, out): return
    s = out["stats"]
    print(f"kimi 净值${s['portfolio_value']:,.2f} ({(s['portfolio_value']/INIT-1)*100:+.2f}%) "
          f"平仓{n}笔 胜率{s['win_rate']}% 持仓{len(fo)} gap{gap_n} 无现金跳过{skipped}")


if __name__ == "__main__":
    main()
