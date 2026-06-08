"""
S&P 600 量化选股扫描器
每日收盘后运行，输出评分最高的候选股到 data/screened-stocks.json
筛选标准：量比>=1.2x + ATR 2-8% + 5因子评分
"""
import json, os, re, warnings, time
from datetime import datetime, timedelta, timezone
import yfinance as yf
import pandas as pd

warnings.filterwarnings('ignore')

BLACKLIST = {
    "NVDA","AAPL","MSFT","AMZN","GOOGL","GOOG","META","TSLA","JPM","JNJ","XOM",
    "BRK","V","MA","UNH","PG","HD","CVX","MRK","ABBV","BAC","KO","PEP","COST",
    "WMT","AVGO","TSM","LLY","ORCL","NFLX","AMD","INTC","TLT","BND","SPY","QQQ"
}

OUTPUT_PATH   = "data/screened-stocks.json"
MIN_VOL_RATIO = 1.2
MIN_ATR_PCT   = 2.0
MAX_ATR_PCT   = 8.0
TOP_N         = 20
os.makedirs("data", exist_ok=True)

beijing_tz = timezone(timedelta(hours=8))
today = datetime.now(beijing_tz).strftime("%Y-%m-%d")


def get_sp600_tickers():
    """Pull S&P 600 constituents from Wikipedia. Falls back to a hardcoded core list."""
    try:
        tables = pd.read_html(
            "https://en.wikipedia.org/wiki/List_of_S%26P_600_companies",
            attrs={"id": "constituents"}
        )
        df = tables[0]
        col = next((c for c in df.columns if "Symbol" in c or "Ticker" in c), None)
        if col:
            tickers = [str(t).replace(".", "-") for t in df[col].tolist() if isinstance(t, str)]
            print(f"[screen] Loaded {len(tickers)} S&P 600 tickers from Wikipedia")
            return tickers
    except Exception as e:
        print(f"[warn] Wikipedia fetch failed: {e}, using fallback list")

    # Fallback: curated small/mid cap names representative of S&P 600
    return [
        "ACLS","AEHR","ALGT","AMBA","APOG","ARCB","BOOT","CAMT","COHU","DXCM",
        "FLR","FORM","GFF","HCC","ICHR","IMOS","ITIC","JBSS","KLIC","LRCX",
        "MGPI","MXL","NTAP","ONTO","POWI","QRVO","SITM","SMTC","SWKS","UCTT",
        "WOLF","WTTR","AAON","ACIW","ACNB","ADUS","AGYS","AMPH","AMRX","ANDE",
        "AOUT","APEI","ARCO","ARDX","ARLO","ATRC","AVAV","AVNS","AZEK","BANF",
        "BANR","BCPC","BECN","BLMN","CABO","CADE","CALM","CATY","CBRL","CCOI",
        "CDMO","CDNA","CECO","CENT","CHCO","CHEF","CHRD","CHUY","CLFD","CLNE",
        "CMCO","CMPR","CNMD","CNOB","CNSL","COMM","COOP","CROX","CTAS","CTLP",
        "CTRE","CUTR","CVBF","CVCO","DAKT","DDOG","DFIN","DGII","DIOD","DNOW",
        "DOOR","DXPE","EAT","ECPG","EFSC","EMBC","ENOV","ENPH","EPRT","ESCA",
        "EVRI","EXTR","EZPW","FBMS","FBNC","FCFS","FEIM","FELE","FFBC","FFIN",
        "FISI","FLIC","FLNT","FMBH","FORM","FRME","GABC","GERN","GKOS","GLDD",
        "GMED","GPOR","GSIT","HBCP","HBNC","HCSG","HFWA","HLNE","HOFT","HOLX",
        "HOPE","HRMY","HROW","HTLF","HUBG","IBP","ICFI","IDCC","IIIN","IMMR",
        "INBK","INFU","INMD","INSG","IPGP","IRBT","IRMD","JACK","JJSF","JOUT",
        "KELYA","KMPR","KTOS","LAKE","LAUR","LCNB","LCUT","LGND","LKFN","LMAT",
        "LOCO","LOVE","LQDT","LSEA","LYTS","MBIN","MBWM","MCBC","MCRB","MCRI",
        "MDGL","MDRX","MESA","MFIN","MGPI","MHLD","MLNK","MMSI","MNKD","MNRL",
        "MNRO","MODG","MOFG","MORN","MRCY","MRTN","MSBI","MTRX","MVBF","NBTB",
        "NCBS","NFBK","NMIH","NNBR","NSIT","NTCT","NTST","NUVL","NWBI","OBT",
        "OCFC","OCGN","OFG","OMCL","OPCH","ORCA","ORGO","OSBC","OSIS","OTTR",
        "PAHC","PARR","PATI","PBHC","PBI","PCRX","PDCO","PDFS","PEBO","PFBC",
        "PFIS","PGEN","PGNY","PLCE","PLMR","PLNT","PLRX","PLUS","PLXS","PMD",
        "PNFP","PNNT","PODD","POWL","PPBI","PRFT","PRGO","PRGS","PRIM","PRVA",
        "PSMT","PSTL","PTEN","PTGX","PTLO","PVBC","RBBN","RCKY","RGEN","RGLD",
        "RGNX","RICK","ROCK","RPAY","RRBI","RRGB","SAFE","SAMG","SBCF","SBFG",
        "SBOW","SCSC","SELF","SFBC","SFNC","SHEN","SHYF","SIGA","SKWD","SLCA",
        "SLGN","SMBC","SMPL","SNCY","SNDR","SNEX","SPOK","SPSC","SPTN","SPWH",
        "SPXC","SRCE","SRRK","STAA","STBA","STEM","STFC","STNG","STRA","STRL",
        "STRS","SWBI","SYBT","SYRA","TBBK","TBNK","TCBK","TCMD","TCNNF","TCPC",
        "TCRR","TDOC","TGNA","TILE","TISI","TOWN","TPVG","TRDA","TRMK","TROW",
        "TRST","TRTX","TRVI","TSBK","TTMI","TWNK","TWST","TXRH","UBSI","UCBI",
        "UDMY","UFCS","UFPT","ULBI","UMBF","UMPQ","UNTY","UONE","UPBD","URBN",
        "USAK","USLM","USPH","UTMD","UVSP","VBTX","VCNX","VERX","VGFC","VIRT",
        "VLGEA","VMAR","VNDA","VNOM","VRTS","VSTO","WDFC","WERN","WEYS","WINA",
        "WIRE","WLFC","WNEB","WOOF","WORX","WRLD","WSR","WSBC","WSFS","WTBA",
        "XNCR","XPEL","XXII","YORW","ZEUS","ZION",
    ]


def get_sp500_pct():
    """Read today's S&P 500 futures % from morning note files."""
    for fname in [
        f"dashboard/morning-note-history/{today}.json",
        "dashboard/morning-note.js",
    ]:
        if not os.path.exists(fname):
            continue
        try:
            with open(fname) as f:
                raw = f.read()
            if fname.endswith(".js"):
                raw = re.sub(r"^.*?window\.MORNING_NOTE\s*=\s*", "", raw, flags=re.DOTALL).rstrip().rstrip(";")
            data = json.loads(raw)
            return data.get("market", {}).get("sp500_futures_pct", 0)
        except Exception:
            pass
    return 0


def get_market_regime():
    """
    判断当前市场状态：bull / bear / neutral
    使用3个免费指标：S&P500 vs 200MA、VIX水平、近20日涨跌幅
    返回 dict，包含 regime 和各指标数值
    """
    result = {
        "regime":        "neutral",
        "spy_vs_200ma":  0.0,
        "vix":           20.0,
        "spy_20d_pct":   0.0,
        "bear_signals":  0,
        "bull_signals":  0,
    }
    try:
        # S&P 500 (用 SPY ETF)
        spy = yf.Ticker("SPY").history(period="1y")
        if not spy.empty:
            spy.index = spy.index.tz_localize(None) if spy.index.tz else spy.index
            close = spy["Close"].astype(float)
            price = float(close.iloc[-1])
            ma200 = float(close.iloc[-200:].mean()) if len(close) >= 200 else float(close.mean())
            spy_vs_200ma = (price / ma200 - 1) * 100
            spy_20d = (price / float(close.iloc[-20]) - 1) * 100 if len(close) >= 20 else 0.0
            result["spy_vs_200ma"] = round(spy_vs_200ma, 2)
            result["spy_20d_pct"]  = round(spy_20d, 2)
    except Exception as e:
        print(f"[regime] SPY fetch failed: {e}")

    try:
        # VIX 恐慌指数
        vix = yf.Ticker("^VIX").history(period="5d")
        if not vix.empty:
            result["vix"] = round(float(vix["Close"].iloc[-1]), 2)
    except Exception as e:
        print(f"[regime] VIX fetch failed: {e}")

    # 计算信号得分
    bear = 0
    bull = 0

    if result["spy_vs_200ma"] < -2:   bear += 2   # 明显跌破200MA — 强熊信号
    elif result["spy_vs_200ma"] < 0:  bear += 1   # 略低于200MA
    elif result["spy_vs_200ma"] > 3:  bull += 2   # 明显在200MA上方 — 强牛信号
    elif result["spy_vs_200ma"] > 0:  bull += 1

    if result["vix"] > 30:   bear += 2   # 极度恐慌
    elif result["vix"] > 20: bear += 1   # 偏高波动
    elif result["vix"] < 15: bull += 1   # 低波动平静

    if result["spy_20d_pct"] < -5:   bear += 1   # 近20日跌超5%
    elif result["spy_20d_pct"] > 3:  bull += 1   # 近20日涨超3%

    result["bear_signals"] = bear
    result["bull_signals"]  = bull

    if bear >= 3:
        result["regime"] = "bear"
    elif bull >= 3:
        result["regime"] = "bull"
    else:
        result["regime"] = "neutral"

    label = {"bull": "🟢 牛市", "bear": "🔴 熊市", "neutral": "🟡 震荡"}[result["regime"]]
    print(f"[regime] {label}  SPY vs 200MA={result['spy_vs_200ma']:+.1f}%  "
          f"VIX={result['vix']}  20d={result['spy_20d_pct']:+.1f}%  "
          f"(熊{bear}/牛{bull})")
    return result


def score_stock(ticker, hist, sp500_pct, regime="neutral"):
    """Calculate quality score. Returns dict or None if disqualified."""
    if len(hist) < 60:
        return None

    close  = hist["Close"].astype(float)
    volume = hist["Volume"].astype(float)
    price  = float(close.iloc[-1])

    if price < 5:
        return None

    ma50     = float(close.iloc[-50:].mean())
    lookback = min(252, len(close))
    high_52  = float(close.iloc[-lookback:].max())
    rs_12m   = (price / float(close.iloc[0]) - 1) * 100

    vol_50d   = float(volume.iloc[-50:].mean())
    vol_ratio = float(volume.iloc[-5:].mean()) / vol_50d if vol_50d > 0 else 0.0

    atr_pct = float(
        (hist["High"].astype(float) - hist["Low"].astype(float)).iloc[-14:].mean()
    ) / price * 100
    dist_from_high = (high_52 - price) / high_52 * 100

    # Hard disqualifiers
    if vol_ratio < MIN_VOL_RATIO:
        return None
    if not (MIN_ATR_PCT <= atr_pct <= MAX_ATR_PCT):
        return None

    # Scoring 0-100
    vol_score   = min(30.0, (vol_ratio - 1.2) / 0.8 * 30)
    atr_score   = min(25.0, max(0.0, 25 - abs(atr_pct - 4) * 5))
    trend_score = 20.0 if abs(price / ma50 - 1) > 0.05 else 10.0
    high_score  = min(25.0, max(0.0, 25 - dist_from_high))
    total       = vol_score + atr_score + trend_score + high_score

    # 超涨 SELL 候选判断（根据 regime 调整阈值）
    if regime == "bear":
        # 熊市：更宽松——只要距高点<10%就是潜在SELL候选
        sell_candidate = bool(dist_from_high < 10 and rs_12m > 50)
    else:
        # 牛市/中性：严格——RS极高且贴近高点才算SELL候选
        sell_candidate = bool(rs_12m > 500 and dist_from_high < 2)

    # 熊市中 BUY 信号需要更强量比确认
    if regime == "bear":
        buy_min_vol = 1.8
    elif sp500_pct < -1:
        buy_min_vol = 1.5
    else:
        buy_min_vol = MIN_VOL_RATIO

    buy_ok = bool(vol_ratio >= buy_min_vol and not sell_candidate)

    return {
        "ticker":         ticker,
        "score":          round(total),
        "vol_ratio":      round(vol_ratio, 2),
        "atr_pct":        round(atr_pct, 2),
        "rs_12m":         round(rs_12m, 1),
        "dist_from_high": round(dist_from_high, 1),
        "above_ma50":     round((price / ma50 - 1) * 100, 1),
        "price":          round(price, 2),
        "sell_candidate": sell_candidate,
        "buy_ok":         buy_ok,
    }


def main():
    sp500_pct = get_sp500_pct()
    print(f"[screen] Date={today}  S&P500 futures={sp500_pct:+.2f}%")

    regime_data = get_market_regime()
    regime      = regime_data["regime"]

    tickers = [t for t in get_sp600_tickers() if t.upper() not in BLACKLIST]
    print(f"[screen] Scanning {len(tickers)} tickers (regime={regime})...")

    start_date = (datetime.now() - timedelta(days=380)).strftime("%Y-%m-%d")
    candidates = []
    skipped    = 0

    for i, ticker in enumerate(tickers):
        try:
            hist = yf.Ticker(ticker).history(start=start_date)
            if hist.empty:
                skipped += 1
                continue
            hist.index = hist.index.tz_localize(None) if hist.index.tz else hist.index
            result = score_stock(ticker, hist, sp500_pct, regime)
            if result:
                candidates.append(result)
        except Exception:
            skipped += 1
        if (i + 1) % 50 == 0:
            print(f"[screen] Progress: {i+1}/{len(tickers)}, passed={len(candidates)}")
        time.sleep(0.05)

    # 熊市：SELL候选排前面；牛市：BUY候选排前面
    if regime == "bear":
        candidates.sort(key=lambda x: (not x["sell_candidate"], -x["score"]))
    elif regime == "bull":
        candidates.sort(key=lambda x: (not x["buy_ok"], -x["score"]))
    else:
        candidates.sort(key=lambda x: -x["score"])

    top = candidates[:TOP_N]

    output = {
        "date":        today,
        "sp500_pct":   sp500_pct,
        "regime":      regime,
        "regime_data": regime_data,
        "scanned":     len(tickers),
        "skipped":     skipped,
        "passed":      len(candidates),
        "candidates":  top,
    }
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    regime_label = {"bull": "🟢 牛市", "bear": "🔴 熊市", "neutral": "🟡 震荡"}[regime]
    print(f"\n[screen] Done: scanned={len(tickers)} passed={len(candidates)} skipped={skipped}")
    print(f"[screen] 市场状态: {regime_label} → Top {len(top)} candidates saved")
    for c in top[:10]:
        flag = " [SELL候选]" if c["sell_candidate"] else ""
        ok   = " BUY_OK"    if c["buy_ok"]          else " ❌BUY限制"
        print(f"  {c['ticker']:<6} {c['score']:>3}分  vol={c['vol_ratio']:.2f}x  "
              f"atr={c['atr_pct']:.1f}%  rs12m={c['rs_12m']:+.0f}%  "
              f"dist={c['dist_from_high']:.1f}%{flag}{ok}")


if __name__ == "__main__":
    main()
