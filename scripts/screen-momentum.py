"""
动量/趋势选股器（第三条独立腿，不依赖 AI，不依赖基本面）——综合两位真实可验证冠军的公开规则：
  - Mark Minervini（USIC 审计冠军）：8 点趋势模板 + 相对强度 RS（领导股比大盘强）。
  - J Law（首位港人 USIC 冠军，2年累计 1499%）：M.E.T.A. 多重优势进场——
    10/20MA 支撑区回调 + 缩量 + 趋势共振，只在多优势汇聚时买。

纯价量计算（yfinance 免费），long-only（动量本质做多领导股，不做空）。
输出 data/screened-momentum.json + 每日归档 data/momentum-history/{date}.json（当时价量快照,前向无前视）,
供 backfill-portfolio-momh.py(Plan H 出场) 和 backfill-portfolio-momma.py(J Law 10/20MA 移动止盈) 用。

设计：用 Minervini 趋势模板做硬闸门（只在确立上升趋势的领导股里选），再用 M.E.T.A. 多优势打分。
规则简单、参数固定，防过拟合。数据不足的票直接剔除（宁缺毋滥）。
"""
import os, json, urllib.request
from datetime import datetime
import numpy as np

FMP_KEY = os.environ.get("FMP_API_KEY", "").strip()
OUT_PATH = "data/screened-momentum.json"
TOP_N = 10
os.makedirs("data", exist_ok=True)

FALLBACK_UNIVERSE = ["AAPL","MSFT","NVDA","AMZN","GOOGL","META","AVGO","TSLA","JPM","V",
    "MU","AMD","COIN","LSCC","DDOG","NET","CRSP","UEC","DECK","RJF","PLTR","SMCI",
    "ANET","CRWD","NOW","PANW","SNOW","UBER","SHOP","ABNB","CELH","VRT","ZS","MDB"]


def fmp_get(path):
    url = f"https://financialmodelingprep.com/stable/{path}{'&' if '?' in path else '?'}apikey={FMP_KEY}"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            d = json.loads(r.read())
        return d if isinstance(d, list) else []
    except Exception as e:
        print(f"  [fmp] {path} 失败: {str(e)[:80]}"); return []


def get_universe():
    """流动好的中大盘美股(市值>$3B,在交易)。与多因子腿同口径:'会动+数据好'。无 FMP key 用内置列表。"""
    if not FMP_KEY:
        print(f"[universe] 无 FMP_KEY,用内置列表 {len(FALLBACK_UNIVERSE)} 只")
        return FALLBACK_UNIVERSE
    out = []
    for exch in ("NASDAQ", "NYSE"):
        d = fmp_get(f"company-screener?marketCapMoreThan=3000000000&exchange={exch}&isActivelyTrading=true&isFund=false&isEtf=false&limit=250")
        for x in d:
            sym = (x.get("symbol") or "").strip()
            if sym and sym.isalpha() and len(sym) <= 5:
                out.append(sym)
    syms = sorted(set(out))
    if len(syms) < 50:
        print(f"[universe] FMP 返回太少({len(syms)}),用内置列表"); return FALLBACK_UNIVERSE
    print(f"[universe] FMP 流动中大盘: {len(syms)} 只"); return syms


def sma(arr, n):
    if len(arr) < n: return None
    return float(np.mean(arr[-n:]))


def analyze(close, high, low, vol, spy_ret_6m):
    """对一只票算 Minervini 趋势模板(硬闸门) + M.E.T.A. 多优势分。返回 dict 或 None。"""
    if len(close) < 220:                      # 需 200MA + 52周
        return None
    c = close[-1]
    ma50, ma150, ma200 = sma(close, 50), sma(close, 150), sma(close, 200)
    ma10, ma20 = sma(close, 10), sma(close, 20)
    if None in (ma50, ma150, ma200, ma10, ma20):
        return None
    ma200_1mo_ago = sma(close[:-22], 200)     # 1个月前的200MA,判趋势向上
    hi_52 = float(np.max(close[-252:])); lo_52 = float(np.min(close[-252:]))

    # ---- Minervini 8 点趋势模板（硬闸门，必须全过）----
    tt = [
        c > ma150 and c > ma200,              # 1 价在 150/200MA 之上
        ma150 > ma200,                        # 2 150MA > 200MA
        ma200_1mo_ago is not None and ma200 > ma200_1mo_ago,  # 3 200MA 向上
        ma50 > ma150 > ma200,                 # 4 均线多头排列
        c > ma50,                             # 5 价在 50MA 之上
        c >= 1.30 * lo_52,                    # 6 距52周低 ≥30%
        c >= 0.75 * hi_52,                    # 7 距52周高 ≤25%
    ]
    if not all(tt):
        return None

    # ---- 相对强度 RS：个股 6 月收益 − SPY 6 月收益 ----
    ret_6m = c / close[-126] - 1 if len(close) >= 126 else 0.0
    rs = ret_6m - spy_ret_6m

    # ---- M.E.T.A. 多优势打分（0~1 各项，越大越好）----
    # ① 接近 10/20MA 支撑区(J Law:回调到均线买,不追高)。用价距均线区上沿的距离,越近越好,跌破则差。
    ma_band = max(ma10, ma20)
    dist_to_ma = (c - ma_band) / ma_band      # >0 在均线上方
    edge_pullback = float(np.clip(1 - dist_to_ma / 0.12, 0, 1))  # 贴着均线(0%)=1分,高出12%+=0分

    # ② 缩量回调(J Law:健康回调量缩)。近5日均量 / 50日均量,越低越好。
    v5, v50 = sma(vol, 5), sma(vol, 50)
    vol_ratio = (v5 / v50) if (v5 and v50 and v50 > 0) else 1.0
    edge_volcontract = float(np.clip(1 - (vol_ratio - 0.6) / 0.8, 0, 1))  # ≤60%均量=1分,≥140%=0分

    # ③ 距52周高(强势但不过度延伸):距高 0~25% 内,越近越强。
    near_high = (c - hi_52) / hi_52           # ≤0
    edge_nearhigh = float(np.clip(1 + near_high / 0.25, 0, 1))  # 在高点=1分,-25%=0分

    return {
        "price": round(c, 2),
        "rs": round(rs, 4), "ret_6m": round(ret_6m, 4),
        "ma10": round(ma10, 2), "ma20": round(ma20, 2), "ma50": round(ma50, 2),
        "dist_to_ma_pct": round(dist_to_ma * 100, 1),
        "vol_ratio": round(vol_ratio, 2),
        "edge_pullback": round(edge_pullback, 3),
        "edge_volcontract": round(edge_volcontract, 3),
        "edge_nearhigh": round(edge_nearhigh, 3),
    }


def main():
    universe = get_universe()
    import yfinance as yf

    # SPY 基准 6 月收益
    spy_ret_6m = 0.0
    try:
        spy = np.asarray(yf.download("SPY", period="14mo", interval="1d", progress=False)["Close"].dropna()).ravel()
        if len(spy) >= 126:
            spy_ret_6m = float(spy[-1] / spy[-126] - 1)
    except Exception as e:
        print(f"[spy] 取SPY失败,RS退化为绝对动量: {e}")
    print(f"[spy] 6月收益 {spy_ret_6m*100:+.1f}%")

    df = yf.download(universe, period="14mo", interval="1d", progress=False, group_by="ticker", threads=True)
    rows = []
    for tk in universe:
        try:
            x = df[tk][["High", "Low", "Close", "Volume"]].dropna()
            if len(x) < 220:
                continue
            r = analyze(x["Close"].values, x["High"].values, x["Low"].values, x["Volume"].values, spy_ret_6m)
            if r:
                rows.append({"ticker": tk, **r})
        except Exception:
            pass
    print(f"[trend] {len(rows)} 只通过 Minervini 趋势模板闸门")
    if not rows:
        # 闸门后没货(熊市常见)：出空榜,backfill 当天不开新仓
        out = {"date": datetime.now().strftime("%Y-%m-%d"), "universe_size": len(universe),
               "passed_trend": 0, "buy": [], "_note": "无票通过趋势模板闸门(可能大盘走弱)"}
        json.dump(out, open(OUT_PATH, "w"), ensure_ascii=False, indent=2)
        os.makedirs("data/momentum-history", exist_ok=True)
        json.dump(out, open(f"data/momentum-history/{out['date']}.json", "w"), ensure_ascii=False, indent=2)
        print("[trend] 空榜,已归档"); return

    # RS 横截面排名(0~1) + 三项 M.E.T.A. 优势 → 综合分
    rs_sorted = sorted(rows, key=lambda r: -r["rs"])
    n = len(rs_sorted)
    for i, r in enumerate(rs_sorted):
        r["rs_rank"] = 1 - i / (n - 1) if n > 1 else 0.5
    # 综合分:RS 40% + 回调进场 25% + 缩量 15% + 贴近高点 20%
    for r in rows:
        r["score"] = round((0.40*r["rs_rank"] + 0.25*r["edge_pullback"]
                            + 0.15*r["edge_volcontract"] + 0.20*r["edge_nearhigh"]) * 100, 1)
    rows.sort(key=lambda r: -r["score"])
    buys = rows[:TOP_N]

    out = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "universe_size": len(universe), "passed_trend": len(rows),
        "factors": ["rs_rank", "edge_pullback", "edge_volcontract", "edge_nearhigh"],
        "buy": [{"ticker": r["ticker"], "action": "BUY", "score": r["score"], "price": r["price"],
                 "rs": r["rs"], "ret_6m": r["ret_6m"], "dist_to_ma_pct": r["dist_to_ma_pct"],
                 "vol_ratio": r["vol_ratio"]} for r in buys],
    }
    json.dump(out, open(OUT_PATH, "w"), ensure_ascii=False, indent=2)
    os.makedirs("data/momentum-history", exist_ok=True)
    json.dump(out, open(f"data/momentum-history/{out['date']}.json", "w"), ensure_ascii=False, indent=2)

    print(f"\n{'='*58}\n  动量/趋势选股 {out['date']}（{len(rows)}只过闸 / 取前{TOP_N}）\n{'='*58}")
    for r in buys:
        print(f"    {r['ticker']:6} 分{r['score']:5} RS={r['rs']:+.2f} 6月={r['ret_6m']*100:+.0f}% "
              f"距均线{r['dist_to_ma_pct']:+.1f}% 量比{r['vol_ratio']}")


if __name__ == "__main__":
    main()
