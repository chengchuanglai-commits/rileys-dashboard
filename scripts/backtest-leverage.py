"""杠杆指数腿深化回测:多历史窗口(含2008金融危机等灾难期)跑lev_engine,报CAGR/回撤/爆仓。
QQQ用FMP(2006-今,含2008/2020/2022);2000-02互联网崩盘用纳指^IXIC(yfinance)作代理补测。
用法: FMP_API_KEY=... python3 scripts/backtest-leverage.py"""
import sys, os, json, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
import pandas as pd
from lev_engine import simulate_leverage

FMP_KEY = os.environ.get("FMP_API_KEY", "pOJlglH08lKz9RUmFeO5yYxOc87v5HzA")
CONFIGS = [("1x基准", dict(base_lev=1.0)),
           ("1.5x+闸门(选定)", dict(base_lev=1.5)),
           ("2x+闸门(对照)", dict(base_lev=2.0))]


def fmp_series(sym):
    url = f"https://financialmodelingprep.com/stable/historical-price-eod/full?symbol={sym}&from=1999-01-01&apikey={FMP_KEY}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    hist = json.load(urllib.request.urlopen(req, timeout=40))
    hist = hist if isinstance(hist, list) else hist.get("historical", [])
    df = pd.DataFrame(hist)
    df["date"] = pd.to_datetime(df["date"])
    s = df.set_index("date")["adjClose" if "adjClose" in df else "close"].sort_index()
    return s.astype(float)


def yf_series(sym):
    import yfinance as yf
    d = yf.download(sym, start="1999-01-01", end="2003-06-30", progress=False, auto_adjust=True)["Close"]
    return (d[sym] if hasattr(d, "columns") else d).dropna()


def run_window(name, seg):
    if len(seg) < 250:
        print(f"\n{name}: 数据不足({len(seg)}),跳过"); return
    print(f"\n=== {name} (n={len(seg)}, {seg.index[0].date()}→{seg.index[-1].date()}) ===")
    for cname, cfg in CONFIGS:
        r = simulate_leverage(seg, start=2000.0, **cfg)
        flag = " 💀爆仓" if r["ruined"] else ""
        print(f"  {cname:18} 终值${r['final']:>10,.0f} | CAGR {r['cagr']*100:>+6.1f}% | 最大回撤 {r['maxdd']*100:>4.0f}%{flag}")


def main():
    qqq = fmp_series("QQQ")
    for name, s, e in [("2007-06→2009-06 金融危机", "2007-06-01", "2009-06-30"),
                       ("2019-06→2022-12 崩盘+熊市", "2019-06-01", "2022-12-31"),
                       ("全程 2006→今(QQQ)", "2006-01-01", "2026-12-31")]:
        run_window(name, qqq[(qqq.index >= s) & (qqq.index <= e)])
    # 2000-02 互联网崩盘:QQQ数据不可得,用纳指综合^IXIC代理(测极端崩盘下杠杆是否爆仓)
    try:
        ndx = yf_series("^IXIC")
        run_window("2000-01→2003-01 互联网崩盘(^IXIC代理)", ndx[(ndx.index >= "2000-01-01") & (ndx.index <= "2003-01-31")])
    except Exception as ex:
        print(f"\n2000-02 代理取数失败({str(ex)[:60]}),跳过——以2008金融危机为主灾难测")


if __name__ == "__main__":
    main()
