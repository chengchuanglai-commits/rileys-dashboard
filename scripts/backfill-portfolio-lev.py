"""杠杆指数腿 paper 回填:近窗口跑lev_engine → portfolio_lev.json + dashboard/portfolio-lev.js。
对照1x QQQ买入持有。QQQ用FMP(可靠长历史)。用法: FMP_API_KEY=... python3 scripts/backfill-portfolio-lev.py"""
import sys, os, json, time, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
import pandas as pd
from lev_engine import simulate_leverage

FMP_KEY = os.environ.get("FMP_API_KEY", "pOJlglH08lKz9RUmFeO5yYxOc87v5HzA")
START_DATE = "2020-01-01"   # 回填起点(含2020崩盘+2022熊市,给足历史看回撤)
INIT = 2000.0
NOTE = ("杠杆指数腿:1.5x QQQ + 200MA闸门(跌破退1x,连站5天才重加杠防whipsaw) + 20日波动>30%降杠 + "
        "6%/年融资 + 再平衡带[1.3,1.7]。对照1x QQQ买入持有。见 spec 2026-07-07。")


def qqq_series():
    url = f"https://financialmodelingprep.com/stable/historical-price-eod/full?symbol=QQQ&from=1999-01-01&apikey={FMP_KEY}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    h = json.load(urllib.request.urlopen(req, timeout=40))
    h = h if isinstance(h, list) else h.get("historical", [])
    df = pd.DataFrame(h); df["date"] = pd.to_datetime(df["date"])
    col = "adjClose" if "adjClose" in df.columns else "close"
    return df.set_index("date")[col].sort_index().astype(float)


def main():
    px = qqq_series()
    seg = px[px.index >= START_DATE]
    lev = simulate_leverage(seg, start=INIT)
    p0 = float(seg.iloc[0]); p1 = float(seg.iloc[-1])
    qqq_1x = INIT * p1 / p0
    out = {
        "capital_usd": INIT, "_note": NOTE,
        "curve": lev["curve"][-260:],
        "stats": {
            "portfolio_value": round(lev["final"], 2),
            "cagr_pct": round(lev["cagr"] * 100, 2),
            "maxdd_pct": round(lev["maxdd"] * 100, 1),
            "current_lev": lev["curve"][-1][2] if lev["curve"] else 1.0,
            "qqq_1x_value": round(qqq_1x, 2),
            "vs_qqq_1x_usd": round(lev["final"] - qqq_1x, 2),
            "ruined": lev["ruined"],
            "updated_at": time.strftime("%Y-%m-%d"),
        },
    }
    os.makedirs("data", exist_ok=True)
    json.dump(out, open("data/portfolio_lev.json", "w"), ensure_ascii=False, indent=2)
    with open("dashboard/portfolio-lev.js", "w", encoding="utf-8") as f:
        f.write(f"window.PORTFOLIO_LEV = {json.dumps(out, ensure_ascii=False)};\n")
    s = out["stats"]
    print(f"杠杆腿 净值${s['portfolio_value']:,.0f} CAGR{s['cagr_pct']:+.1f}% 最大回撤{s['maxdd_pct']:.0f}% "
          f"当前{s['current_lev']}x | vs 1xQQQ ${s['vs_qqq_1x_usd']:+,.0f}")


if __name__ == "__main__":
    main()
