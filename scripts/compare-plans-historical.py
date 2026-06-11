"""
一次性分析：把各方案的出场参数放到 12 个月历史随机入场上，看盈利/排名是否与3周真实样本不同。
仅能映射单档 TP/SL/持仓/跳空的方案：B/C/D(=G)/H。E(VIX动态)/F(分档) 无法映射。
随机入场 ≠ 真实信号，结论仅作"出场参数稳健性"的先验。
"""
import random
from datetime import datetime, timedelta
import yfinance as yf

UNIVERSE = ["UCTT","WTTR","MXL","ALGT","IMOS","KLIC","CAMT","DXCM","AMBA","FLR",
    "ACLS","AEHR","COHU","FORM","ICHR","NTAP","ONTO","POWI","SMTC","SITM",
    "AAON","APOG","ARCB","BOOT","CEIX","GFF","HCC","ITIC","JBSS","MGPI",
    "LRCX","MU","SWKS","WOLF","QRVO"]

PLANS = {  # name: (tp, sl, hold, gap)
    "B": (8, 4, 5, 0.0),
    "C": (8, 4, 5, 1.5),
    "D=G": (15, 3, 2, 1.0),
    "H": (15, 2, 2, 1.0),
}
SAMPLES_PER_STOCK_MONTH = 2
random.seed(42)

end = datetime.now(); start = end - timedelta(days=12*31)
print(f"拉取 {len(UNIVERSE)} 只 × 12 个月...")
data = {}
for t in UNIVERSE:
    try:
        df = yf.Ticker(t).history(start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d"))
        if not df.empty:
            df.index = df.index.tz_localize(None) if df.index.tz else df.index
            data[t] = df
    except Exception:
        pass

# 随机采样入场点（每股每月2个），BUY+SELL 都测
entries = []
for t, df in data.items():
    rows = [(idx, r) for idx, r in df.iterrows()]
    bym = {}
    for i, (idx, r) in enumerate(rows[:-11]):
        bym.setdefault(idx.strftime("%Y-%m"), []).append(i)
    for m, idxs in bym.items():
        for i in random.sample(idxs, min(SAMPLES_PER_STOCK_MONTH, len(idxs))):
            entries.append((t, i))
print(f"生成 {len(entries)} 入场点 × BUY/SELL × {len(PLANS)} 方案\n")

def simulate(df_rows, i, action, tp, sl, hold, gap):
    entry = float(df_rows[i][1]["Close"])
    if entry != entry or entry <= 0: return None
    tp_p = entry*(1+tp/100) if action=="BUY" else entry*(1-tp/100)
    sl_p = entry*(1-sl/100) if action=="BUY" else entry*(1+sl/100)
    for j in range(1, hold+1):
        if i+j >= len(df_rows): return None
        r = df_rows[i+j][1]
        o,hi,lo,cl = float(r["Open"]),float(r["High"]),float(r["Low"]),float(r["Close"])
        if any(x!=x for x in (o,hi,lo,cl)): return None
        if j==1 and gap>0:
            g = (o-entry)/entry*100
            if (-g if action=="BUY" else g) > gap: return "gap"
        if action=="BUY":
            if lo<=sl_p: return -sl
            if hi>=tp_p: return tp
        else:
            if hi>=sl_p: return -sl
            if lo<=tp_p: return tp
        if j==hold:
            raw=(cl-entry)/entry*100
            return raw if action=="BUY" else -raw
    return None

rows_cache = {t:[(idx,r) for idx,r in df.iterrows()] for t,df in data.items()}
print(f"{'方案':<6}{'参数':<22}{'N':>6}{'胜率':>8}{'平均盈':>8}{'平均亏':>8}{'盈亏比PF':>9}{'每笔EV':>9}")
for name,(tp,sl,hold,gap) in PLANS.items():
    pnls=[]
    for t,i in entries:
        rows = rows_cache[t]
        for action in ("BUY","SELL"):
            res = simulate(rows, i, action, tp, sl, hold, gap)
            if isinstance(res,(int,float)): pnls.append(res)
    if not pnls: continue
    wins=[p for p in pnls if p>0]; losses=[p for p in pnls if p<=0]
    wr=len(wins)/len(pnls)*100
    aw=sum(wins)/len(wins) if wins else 0
    al=sum(losses)/len(losses) if losses else 0
    pf=(sum(wins)/abs(sum(losses))) if losses and sum(losses)!=0 else float('inf')
    ev=sum(pnls)/len(pnls)  # 平均每笔收益%(真实随机入场)
    print(f"{name:<6}TP{tp}/SL{sl}/{hold}日/gap{gap:<6}{len(pnls):>6}{wr:>7.1f}%{aw:>7.2f}%{al:>7.2f}%{pf:>9.2f}{ev:>8.2f}%")
print("\n注：随机入场，非真实信号。EV%为每笔平均收益(含止损/止盈/到期)。E/F 因动态/分档出场无法纳入此对比。")
