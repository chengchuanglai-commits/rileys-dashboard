"""hds-tr 影子腿回填:DeepSeek信号 + 移动止损(init-4%/trail4%/10d/gap1.0)。
2026-07-17 上线依据(三重证据):①方法B配对 +1.23%/笔 95%CI[+0.40,+2.18](analyze-exit-paired-ds.py)
②组合级回测 $2379 vs H版 $2298(+4.05pp,同引擎frac10) ③H复刻与真实hds只差$1(管线自验证)。
影子腿=与hds同信号只换出场,不参与gate(gate裁hds本体);若gate PASS且影子前向确认→真钱试运行用移动止损。
用法: python3 scripts/backfill-portfolio-hdstr.py  (run.sh review 每日调用,零API成本)"""
import os, sys, json, time

sys.path.insert(0, os.path.dirname(__file__))
import plan_variants as pv
from portfolio_compound import compound_portfolio

DS_DIR = "dashboard/trading-signals-history/deepseek"
PORTFOLIO_PATH = "data/portfolio_hdstr.json"
GAP = 1.0
INIT = 2000.0
NOTE = ("hds-tr 影子腿【理想化上界:信号价零滑点成交/碎股/无借券约束/10并发,真钱只有4并发+整股+滑点,"
        "两者数字不可直接比较】:DeepSeek信号+移动止损(init-4%/trail4%/10d/gap1.0)。与hds同信号只换出场。"
        "2026-07-17方法B配对+组合回测双确认后开跑;影子不参与gate,gate裁hds本体。")


def _open_pct(p):
    dp = p.get("daily_prices") or {}
    return list(dp.values())[-1]["pnl_pct"] if dp else 0.0


def main():
    signals = []
    for fname in sorted(os.listdir(DS_DIR) if os.path.isdir(DS_DIR) else []):
        if fname.endswith("-deepseek.json"):
            d = json.load(open(os.path.join(DS_DIR, fname)))
            sd = fname.replace("-deepseek.json", "")
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
    print(f"hds-tr 净值${s['portfolio_value']:,.2f} ({(s['portfolio_value']/INIT-1)*100:+.2f}%) "
          f"平仓{n}笔 胜率{s['win_rate']}% 持仓{len(fo)} gap{gap_n} 无现金跳过{skipped}")


if __name__ == "__main__":
    main()
