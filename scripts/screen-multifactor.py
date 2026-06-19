"""
多因子选股器（B 方案底座，B-quant / B-AI 共用）。
学术标配因子：价值 + 质量 + 成长 + 动量。横截面排名→综合分→买入榜首/卖出垫底。

数据源：
  - 基本面/比率/财报 → FMP(stable API, FMP_API_KEY)。**缓存到 data/fundamentals-cache.json，每周刷新**(基本面不天天变,省额度)。
  - 价格/动量 → yfinance(免费)。

输出：data/screened-multifactor.json （候选 + 因子分 + 买卖方向），供 backfill-portfolio-bq.py(纯量化) 和 DeepSeek 广撒(B-AI) 用。

设计:保持因子简单/标准,防过拟合。FMP 失败/缺数据的票直接剔除(宁缺毋滥)。
"""
import os, sys, json, time, urllib.request
from datetime import datetime, timedelta

FMP_KEY = os.environ.get("FMP_API_KEY", "").strip()
CACHE_PATH = "data/fundamentals-cache.json"
OUT_PATH = "data/screened-multifactor.json"
CACHE_MAX_AGE_DAYS = 7          # 基本面缓存有效期(周更)
TOP_N = 10                      # 买入榜首 N
BOTTOM_N = 10                   # 卖出垫底 N
os.makedirs("data", exist_ok=True)


def fmp_get(path):
    url = f"https://financialmodelingprep.com/stable/{path}{'&' if '?' in path else '?'}apikey={FMP_KEY}"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            d = json.loads(r.read())
        return d if isinstance(d, list) else []
    except Exception as e:
        print(f"  [fmp] {path} 失败: {str(e)[:80]}")
        return []


def get_universe():
    """FMP 选股器:流动好的中大盘美股(市值>$3B,在交易)。比 S&P500 更贴合'会动+数据好',且可靠。"""
    out, prices = [], {}
    for exch in ("NASDAQ", "NYSE"):
        d = fmp_get(f"company-screener?marketCapMoreThan=3000000000&exchange={exch}&isActivelyTrading=true&isFund=false&isEtf=false&limit=250")
        for x in d:
            sym = (x.get("symbol") or "").strip()
            if sym and sym.isalpha() and len(sym) <= 5:
                out.append(sym)
                if x.get("price"): prices[sym] = x["price"]   # FMP现价,用于校验yfinance脏数据
    syms = sorted(set(out))
    if len(syms) < 50:
        print(f"[universe] FMP screener 返回太少({len(syms)}),用内置列表")
        return ["AAPL","MSFT","NVDA","AMZN","GOOGL","META","AVGO","TSLA","JPM","V",
                "MU","AMD","COIN","LSCC","DDOG","NET","CRSP","UEC","DECK","RJF"], {}
    print(f"[universe] FMP 流动中大盘: {len(syms)} 只")
    return syms, prices


def fetch_fundamentals(ticker):
    """拉一只票的多因子原料(3个接口)。返回 dict 或 None。"""
    rt = fmp_get(f"ratios-ttm?symbol={ticker}")
    km = fmp_get(f"key-metrics-ttm?symbol={ticker}")
    inc = fmp_get(f"income-statement?symbol={ticker}&limit=2")
    if not rt or not km:
        return None
    r, m = rt[0], km[0]
    # 成长:最近两期营收/净利同比
    rev_g = ni_g = None
    if len(inc) >= 2 and inc[1].get("revenue"):
        try:
            rev_g = (inc[0]["revenue"] - inc[1]["revenue"]) / abs(inc[1]["revenue"])
            ni_g = (inc[0]["netIncome"] - inc[1]["netIncome"]) / abs(inc[1]["netIncome"]) if inc[1].get("netIncome") else None
        except Exception:
            pass
    return {
        "ticker": ticker,
        "pe": r.get("priceToEarningsRatioTTM"),
        "pb": r.get("priceToBookRatioTTM"),
        "earnings_yield": m.get("earningsYieldTTM"),       # 直接用FMP的盈利收益率(处理负盈利更稳)
        "roe": m.get("returnOnEquityTTM"),                  # ROE 在 key-metrics-ttm,不在 ratios
        "net_margin": r.get("netProfitMarginTTM"),
        "debt_equity": r.get("debtToEquityRatioTTM"),
        "rev_growth": rev_g, "ni_growth": ni_g,
        "mkt_cap": m.get("marketCap"),
    }


def load_cache():
    if os.path.exists(CACHE_PATH):
        try:
            c = json.load(open(CACHE_PATH))
            age = (datetime.now() - datetime.fromisoformat(c.get("as_of", "2000-01-01"))).days
            if age < CACHE_MAX_AGE_DAYS:
                return c.get("data", {}), True
        except Exception:
            pass
    return {}, False


def main():
    if not FMP_KEY:
        print("[multifactor] 无 FMP_API_KEY，退出"); return
    universe, fmp_prices = get_universe()
    cache, fresh = load_cache()
    print(f"[cache] {'命中(周内)' if fresh else '过期/无,重新拉取'} · 已有 {len(cache)} 只")

    funds = {}
    pulled = 0
    for tk in universe:
        if tk in cache and fresh:
            funds[tk] = cache[tk]; continue
        f = fetch_fundamentals(tk)
        if f:
            funds[tk] = f; pulled += 1
            if pulled % 20 == 0:
                print(f"  ...已拉 {pulled} 只"); time.sleep(0.3)
    # 更新缓存
    json.dump({"as_of": datetime.now().isoformat(), "data": funds},
              open(CACHE_PATH, "w"), ensure_ascii=False)
    print(f"[fundamentals] 可用 {len(funds)} 只(本次新拉 {pulled})")

    # 价格 + 6月动量(yfinance 批量)
    import yfinance as yf
    tickers = list(funds.keys())
    mom, price = {}, {}
    try:
        df = yf.download(tickers, period="7mo", interval="1d", progress=False, group_by="ticker", threads=True)
        bad = 0
        for tk in tickers:
            try:
                cl = df[tk]["Close"].dropna()
                if len(cl) > 100:
                    p = round(float(cl.iloc[-1]), 2)
                    # 用 FMP 现价校验 yfinance 脏数据(如MU $1133):偏离>40%则丢弃该票
                    fp = fmp_prices.get(tk)
                    if fp and fp > 0 and abs(p / fp - 1) > 0.40:
                        bad += 1; continue
                    price[tk] = p
                    mom[tk] = float(cl.iloc[-1] / cl.iloc[0] - 1)
            except Exception:
                pass
        if bad: print(f"[price] 剔除 {bad} 只 yfinance 价格异常(与FMP偏离>40%)")
    except Exception as e:
        print(f"[yfinance] 批量失败: {e}")

    # 组装可打分的票(基本面+价格齐全)
    rows = []
    for tk, f in funds.items():
        if tk not in price:
            continue
        f = {**f, "price": price[tk], "momentum": mom.get(tk)}
        rows.append(f)
    print(f"[score] 可打分 {len(rows)} 只")
    if len(rows) < 20:
        print("[score] 可打分太少,退出"); return

    # 横截面排名(每因子排名0~1,缺失给中位0.5);方向:价值/低负债 越小越好,其余越大越好
    def rank_factor(key, higher_better):
        vals = [(r["ticker"], r.get(key)) for r in rows if r.get(key) is not None]
        vals.sort(key=lambda x: x[1], reverse=higher_better)
        n = len(vals)
        return {tk: 1 - i / (n - 1) if n > 1 else 0.5 for i, (tk, _) in enumerate(vals)}

    # earnings_yield 已由 FMP 提供;缺失时退回 1/PE
    for r in rows:
        if r.get("earnings_yield") is None and r.get("pe") and r["pe"] > 0:
            r["earnings_yield"] = 1.0 / r["pe"]

    # winsorize:把极端值裁到 5-95 分位,防脏数据(如MU动量402%)/单只异常霸榜(因子标准操作)
    def winsorize(key):
        vals = sorted(r[key] for r in rows if r.get(key) is not None)
        if len(vals) < 10: return
        lo, hi = vals[int(len(vals)*0.05)], vals[int(len(vals)*0.95)]
        for r in rows:
            if r.get(key) is not None:
                r[key] = max(lo, min(hi, r[key]))
    for k in ("momentum", "rev_growth", "earnings_yield", "pb", "roe", "net_margin", "debt_equity"):
        winsorize(k)

    ranks = {
        "value_ey": rank_factor("earnings_yield", True),
        "value_pb": rank_factor("pb", False),     # 低PB好
        "qual_roe": rank_factor("roe", True),
        "qual_margin": rank_factor("net_margin", True),
        "qual_lowdebt": rank_factor("debt_equity", False),  # 低负债好
        "growth_rev": rank_factor("rev_growth", True),
        "momentum": rank_factor("momentum", True),
    }
    # 综合分:价值30% 质量30% 成长20% 动量20%
    W = {"value_ey":0.15,"value_pb":0.15,"qual_roe":0.10,"qual_margin":0.10,"qual_lowdebt":0.10,"growth_rev":0.20,"momentum":0.20}
    for r in rows:
        tk = r["ticker"]
        r["score"] = round(sum(ranks[f].get(tk, 0.5) * w for f, w in W.items()) * 100, 1)

    rows.sort(key=lambda r: -r["score"])
    buys = rows[:TOP_N]
    sells = rows[-BOTTOM_N:][::-1]

    out = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "universe_size": len(universe), "scored": len(rows),
        "factors": list(W.keys()),
        "buy": [{"ticker":r["ticker"],"action":"BUY","score":r["score"],"price":r["price"],
                 "pe":r.get("pe"),"roe":r.get("roe"),"momentum":round(r["momentum"],3) if r.get("momentum") else None} for r in buys],
        "sell": [{"ticker":r["ticker"],"action":"SELL","score":r["score"],"price":r["price"],
                  "pe":r.get("pe"),"roe":r.get("roe"),"momentum":round(r["momentum"],3) if r.get("momentum") else None} for r in sells],
    }
    json.dump(out, open(OUT_PATH, "w"), ensure_ascii=False, indent=2)
    # 每日归档(点对点快照:用当时基本面选股,前向回测无前视)
    os.makedirs("data/multifactor-history", exist_ok=True)
    json.dump(out, open(f"data/multifactor-history/{out['date']}.json", "w"), ensure_ascii=False, indent=2)
    print(f"\n{'='*55}\n  多因子选股结果 {out['date']}（{len(rows)}只打分）\n{'='*55}")
    print("  🟢 买入榜首:")
    for r in buys[:5]: print(f"    {r['ticker']:6} 分{r['score']} PE={r.get('pe')} ROE={r.get('roe')} 动量={round(r['momentum']*100,1) if r.get('momentum') else '?'}%")
    print("  🔴 卖出垫底:")
    for r in sells[:5]: print(f"    {r['ticker']:6} 分{r['score']} PE={r.get('pe')} ROE={r.get('roe')} 动量={round(r['momentum']*100,1) if r.get('momentum') else '?'}%")


if __name__ == "__main__":
    main()
