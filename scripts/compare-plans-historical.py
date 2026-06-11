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

# (name, desc, simulator) — B/C/D/H 单档；E VIX动态(仅SELL)；F 分档
PLANS = [
    ("B",   "TP8/SL4/5日/gap0",     lambda rows, i, a: simulate(rows, i, a, 8, 4, 5, 0.0)),
    ("C",   "TP8/SL4/5日/gap1.5",   lambda rows, i, a: simulate(rows, i, a, 8, 4, 5, 1.5)),
    ("D=G", "TP15/SL3/2日/gap1.0",  lambda rows, i, a: simulate(rows, i, a, 15, 3, 2, 1.0)),
    ("E",   "VIX动态/仅SELL/跳过恐慌", lambda rows, i, a: simulate_e(rows, i, a)),
    ("F",   "分档7.5%+15%/3日",      lambda rows, i, a: simulate_f(rows, i, a)),
    ("H",   "TP15/SL2/2日/gap1.0",  lambda rows, i, a: simulate(rows, i, a, 15, 2, 2, 1.0)),
]
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

# VIX（供 E 用）
vix_by_date = {}
try:
    vdf = yf.Ticker("^VIX").history(start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d"))
    vdf.index = vdf.index.tz_localize(None) if vdf.index.tz else vdf.index
    vix_by_date = {idx.strftime("%Y-%m-%d"): float(r["Close"]) for idx, r in vdf.iterrows() if float(r["Close"])==float(r["Close"])}
except Exception:
    pass

def simulate_e(rows, i, action):
    """Plan E：只做 SELL；VIX 分档 TP/SL；fear 跳过；1.5%跳空。"""
    if action == "BUY":
        return None
    vix = vix_by_date.get(rows[i][0].strftime("%Y-%m-%d"), 18.0)
    if vix < 20:   tp, sl, hold = 10.0, 3.0, 3
    elif vix < 25: tp, sl, hold = 8.0, 2.5, 2
    else:          return "fear"
    return simulate(rows, i, "SELL", tp, sl, hold, 1.5)

def simulate_f(rows, i, action):
    """Plan F：分两档 半仓@中点(+7.5%)+半仓@满额(+15%)，SL-3%两档共用，3日，1%跳空。"""
    TP, SL, HOLD, GAP = 15, 3, 3, 1.0
    entry = float(rows[i][1]["Close"])
    if entry != entry or entry <= 0: return None
    tp2 = entry*(1+TP/100) if action=="BUY" else entry*(1-TP/100)
    tp1 = entry + (tp2-entry)*0.5
    sl_p = entry*(1-SL/100) if action=="BUY" else entry*(1+SL/100)
    t1 = t2 = None
    for j in range(1, HOLD+1):
        if i+j >= len(rows): return None
        r = rows[i+j][1]
        o,hi,lo,cl = float(r["Open"]),float(r["High"]),float(r["Low"]),float(r["Close"])
        if any(x!=x for x in (o,hi,lo,cl)): return None
        if j==1 and GAP>0:
            g=(o-entry)/entry*100
            if (-g if action=="BUY" else g) > GAP: return "gap"
        sl_hit = lo<=sl_p if action=="BUY" else hi>=sl_p
        if sl_hit:
            if t1 is None: t1 = -SL
            t2 = -SL; break
        if t1 is None and (hi>=tp1 if action=="BUY" else lo<=tp1): t1 = TP/2
        if t1 is not None and t2 is None and (hi>=tp2 if action=="BUY" else lo<=tp2): t2 = TP
        if j==HOLD:
            raw=(cl-entry)/entry*100; mret = raw if action=="BUY" else -raw
            if t1 is None: t1 = mret
            if t2 is None: t2 = mret
            break
    if t1 is None or t2 is None: return None
    return 0.5*t1 + 0.5*t2

rows_cache = {t:[(idx,r) for idx,r in df.iterrows()] for t,df in data.items()}
summary = []
for name, desc, fn in PLANS:
    pnls = []
    for t, i in entries:
        rows = rows_cache[t]
        for action in ("BUY", "SELL"):
            res = fn(rows, i, action)
            if isinstance(res, (int, float)): pnls.append(res)
    if not pnls: continue
    wins=[p for p in pnls if p>0]; losses=[p for p in pnls if p<=0]
    wr=len(wins)/len(pnls)*100
    aw=sum(wins)/len(wins) if wins else 0
    al=sum(losses)/len(losses) if losses else 0
    pf=(sum(wins)/abs(sum(losses))) if losses and sum(losses)!=0 else float('inf')
    ev=sum(pnls)/len(pnls)
    summary.append((name, desc, len(pnls), wr, aw, al, pf, ev))

summary.sort(key=lambda x: -x[6])  # 按 PF 排序
print(f"{'方案':<6}{'参数':<24}{'N':>6}{'胜率':>8}{'平均盈':>8}{'平均亏':>8}{'盈亏比PF':>9}{'每笔EV':>9}")
for name, desc, n, wr, aw, al, pf, ev in summary:
    print(f"{name:<6}{desc:<24}{n:>6}{wr:>7.1f}%{aw:>7.2f}%{al:>7.2f}%{pf:>9.2f}{ev:>8.2f}%")
print("\n注：随机入场，非真实信号(胜率~随机)，仅测出场机制。E 仅做SELL且跳过恐慌市场故 N 较小。")
