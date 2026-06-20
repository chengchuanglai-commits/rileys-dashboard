"""
MOM 回测·仓位模型严谨版 (position-sizing rigorous) —— 修正"固定金额+隐性杠杆"两大失误,重测。

之前的错:每仓固定$500、不复利、且不查现金(隐性3-4倍杠杆),还拿它去比复利的SPY=不公平。
本版改对:
  ① 真现金账本 (cash ledger):开仓占用现金,平仓归还,现金不足不开 → 无隐性杠杆。
  ② 真复利 (compounding):仓位 = 当前净值的百分比,赚的钱继续上场。
  ③ 三种仓位模型全测:
       frac25 = 每仓 25% 当前净值(4仓满仓)
       frac20 = 每仓 20% 当前净值(5仓,略分散)
       risk2  = 每笔风险 2% 净值(按止损宽窄定仓:紧止损上大仓,宽止损上小仓)
  ④ 对标**复利 SPY** (买入持有,同窗口) → 公平比较。
  ⑤ 滑点扫描 0/0.2%/0.4%。佣金默认 $0 (IBKR Lite,真实执行)。

复用 data/fmp-cache/ 已缓存数据,零新增 FMP 调用。选股 analyze() 与实盘逐字一致。
用法: python scripts/backtest-momentum-sized.py
"""
import os, json, glob
from datetime import datetime
import numpy as np

WIN_FROM = "2021-06-01"; WIN_TO = "2026-06-18"
MKT_MIN = 3_000_000_000
TOP_N = 10
REBALANCE_EVERY = 5
INIT = 2000.0
COMMISSION = 0.0          # IBKR Lite 美股$0(真实执行);改这里可测$1对照
MIN_TICKET = 5.0
CACHE = "data/fmp-cache"; PX_DIR = f"{CACHE}/px"; MC_DIR = f"{CACHE}/mc"
OUT = "data/backtest-momentum-sized.json"

CURATED_DELISTED = [
    "ATVI","VMW","SGEN","ABMD","PXD","SPLK","TWTR","CTLT","ZEN","MNDT","CTXS","CERN",
    "NUAN","XLNX","MXIM","WORK","AVLR","COUP","CONE","QTS","CXO","KSU","INFO","TIF",
    "ALXN","VG","STOR","FLIR","ACIA","SIVB","FRC","SBNY","BBBY","WE","SAVE","TWNK",
]


# ---- 选股逻辑:与 screen-momentum.py 逐字一致 ----
def sma(a, n):
    return float(np.mean(a[-n:])) if len(a) >= n else None

def analyze(close, high, low, vol, spy_ret_6m):
    if len(close) < 220: return None
    c = close[-1]
    ma50, ma150, ma200 = sma(close,50), sma(close,150), sma(close,200)
    ma10, ma20 = sma(close,10), sma(close,20)
    if None in (ma50,ma150,ma200,ma10,ma20): return None
    ma200_1mo = sma(close[:-22],200)
    hi52 = float(np.max(close[-252:])); lo52 = float(np.min(close[-252:]))
    if not all([c>ma150 and c>ma200, ma150>ma200, ma200_1mo is not None and ma200>ma200_1mo,
                ma50>ma150>ma200, c>ma50, c>=1.30*lo52, c>=0.75*hi52]): return None
    ret6 = c/close[-126]-1 if len(close)>=126 else 0.0
    rs = ret6 - spy_ret_6m
    mb = max(ma10,ma20); dist=(c-mb)/mb
    epb = float(np.clip(1-dist/0.12,0,1))
    v5,v50 = sma(vol,5), sma(vol,50)
    vr = (v5/v50) if (v5 and v50 and v50>0) else 1.0
    evc = float(np.clip(1-(vr-0.6)/0.8,0,1))
    enh = float(np.clip(1+((c-hi52)/hi52)/0.25,0,1))
    return {"rs":rs,"epb":epb,"evc":evc,"enh":enh}

def screen_asof(data, spy6):
    rows=[]
    for tk,s in data.items():
        r=analyze(s["C"],s["H"],s["L"],s["V"],spy6)
        if r: rows.append({"tk":tk,**r})
    if not rows: return []
    rss=sorted(rows,key=lambda r:-r["rs"]); n=len(rss)
    for i,r in enumerate(rss): r["rsr"]=1-i/(n-1) if n>1 else 0.5
    for r in rows: r["sc"]=0.40*r["rsr"]+0.25*r["epb"]+0.15*r["evc"]+0.20*r["enh"]
    rows.sort(key=lambda r:-r["sc"])
    return [r["tk"] for r in rows[:TOP_N]]


# ---- 复利 + 现金约束 + 三种仓位模型的引擎 ----
def simulate(exit_rule, signals, ohlc, posmap, last_date, cal, market_ok, slip, sizing, commission):
    """sizing: ('frac',0.25) / ('frac',0.20) / ('risk',0.02)"""
    cash = INIT
    held = {}     # tk -> {shares, entry_fill, cost, pos, tp, sl}
    closed = []
    peak = INIT; max_dd = 0.0

    def price_on(tk, date):
        idx = posmap[tk].get(date)
        return float(ohlc[tk]["C"][idx]) if idx is not None else None

    def equity_on(date):
        eq = cash
        for tk,p in held.items():
            px = price_on(tk,date)
            eq += p["shares"] * (px if px is not None else float(ohlc[tk]["C"][-1]))
        return eq

    def do_close(tk, date, raw, reason):
        nonlocal cash
        p = held.pop(tk)
        exit_fill = raw*(1-slip)
        proceeds = p["shares"]*exit_fill - commission
        cash += proceeds
        closed.append({"tk":tk,"sig":p["sig"],"close_date":date,"reason":reason,
                       "pnl":round(proceeds - p["cost"],2),
                       "ret_pct":round((exit_fill-p["entry_fill"])/p["entry_fill"]*100,2)})

    def ma_at(tk,p,n):
        C=ohlc[tk]["C"]; return float(np.mean(C[p-n+1:p+1])) if p>=n-1 else None

    last_rebal=-999
    for i,date in enumerate(cal):
        # 出场
        for tk in list(held):
            p=posmap.get(tk,{}).get(date)
            if p is None:
                if date>last_date.get(tk,"9999"): do_close(tk,date,float(ohlc[tk]["C"][-1]),"delisted")
                continue
            pos=held[tk]; hi,lo,cl=ohlc[tk]["H"][p],ohlc[tk]["L"][p],ohlc[tk]["C"][p]
            if exit_rule=="H":
                if lo<=pos["sl"]: do_close(tk,date,pos["sl"],"stop"); continue
                if hi>=pos["tp"]: do_close(tk,date,pos["tp"],"tp"); continue
                if (p-pos["pos"])>=2: do_close(tk,date,float(cl),"maxhold")
            else:
                if lo<=pos["sl"]: do_close(tk,date,pos["sl"],"initstop"); continue
                ma=ma_at(tk,p,20)
                if ma is not None and cl<ma: do_close(tk,date,float(cl),"mabreak"); continue
                if (p-pos["pos"])>=60: do_close(tk,date,float(cl),"maxhold")
        # 进场(复利定仓)
        if date in signals and (i-last_rebal)>=REBALANCE_EVERY:
            if market_ok.get(date,True):
                eq = equity_on(date)
                for tk in signals[date]:
                    if tk in held: continue
                    p=posmap.get(tk,{}).get(date)
                    if p is None: continue
                    entry=round(float(ohlc[tk]["C"][p]),4)
                    if entry<=0: continue
                    entry_fill=entry*(1+slip)
                    if sizing[0]=="frac":
                        target=sizing[1]*eq
                    else:  # risk:每笔风险=param*eq,按止损距离定仓
                        stop_pct = 0.02 if exit_rule=="H" else 0.08
                        target=min((sizing[1]*eq)/stop_pct, eq)   # 单仓不超100%净值
                    target=min(target, cash-commission)
                    if target<MIN_TICKET: continue
                    shares=target/entry_fill
                    cash-=(shares*entry_fill + commission)
                    d={"shares":shares,"entry_fill":entry_fill,"cost":shares*entry_fill+commission,
                       "pos":p,"sig":date}
                    if exit_rule=="H": d["tp"]=round(entry*1.15,4); d["sl"]=round(entry*0.98,4)
                    else: d["sl"]=round(entry*0.92,4)
                    held[tk]=d
                last_rebal=i
        # 回撤跟踪
        eq=equity_on(date); peak=max(peak,eq); max_dd=max(max_dd,(peak-eq)/peak)

    final_eq = equity_on(cal[-1])
    wins=[c for c in closed if c["pnl"]>0]
    gl=abs(sum(c["pnl"] for c in closed if c["pnl"]<=0)); gw=sum(c["pnl"] for c in wins)
    srt=sorted(closed,key=lambda c:-c["pnl"])
    return {"final_eq":round(final_eq,0), "ret_pct":round((final_eq/INIT-1)*100,1),
            "trades":len(closed), "win_rate":round(len(wins)/len(closed)*100,1) if closed else 0,
            "pf":round(gw/gl,2) if gl>0 else 99.9, "max_dd_pct":round(max_dd*100,1),
            "drop2_eq_effect":round(sum(c["pnl"] for c in srt[2:]),0),
            "delisted":sum(1 for c in closed if c["reason"]=="delisted")}


def load_cache_series(sym, d):
    f=f"{d}/{sym}.json"
    return json.load(open(f)) if os.path.exists(f) else None

def main():
    uf=f"{CACHE}/universe.json"
    if not os.path.exists(uf):
        print("缺 universe 缓存,先跑 backtest-momentum-fmp.py"); return
    u=json.load(open(uf))
    universe=sorted(set(u["current"]) | set(u["delisted_kept"]) | set(CURATED_DELISTED))

    ohlc,posmap,last_date,mc_series={},{},{},{}
    for tk in universe:
        rows=load_cache_series(tk,PX_DIR)
        if not rows or len(rows)<240: continue
        idx=[r[0] for r in rows]
        ohlc[tk]={"H":np.array([r[1] for r in rows]),"L":np.array([r[2] for r in rows]),
                  "C":np.array([r[3] for r in rows]),"V":np.array([r[4] for r in rows]),"idx":idx}
        posmap[tk]={dt:j for j,dt in enumerate(idx)}
        last_date[tk]=idx[-1]
        mc_series[tk]=load_cache_series(tk,MC_DIR) or []
    spy=load_cache_series("SPY",PX_DIR)
    spy_idx=[r[0] for r in spy]; spy_C=np.array([r[3] for r in spy]); spy_pos={d:j for j,d in enumerate(spy_idx)}
    print(f"[cache] {len(ohlc)} 票 + SPY 已载入")

    def mc_asof(tk,date):
        v=0.0
        for dt,cap in mc_series.get(tk,[]):
            if dt<=date: v=cap
            else: break
        return v

    cal=spy_idx; start_i=252
    rebal=[cal[i] for i in range(start_i,len(cal),REBALANCE_EVERY)]
    bt=cal[start_i:]
    signals,empty={},0
    for d in rebal:
        q=spy_pos.get(d)
        if q is None or q<126: continue
        spy6=float(spy_C[q]/spy_C[q-126]-1)
        data={}
        for tk,o in ohlc.items():
            p=posmap[tk].get(d)
            if p is None or p<220: continue
            if mc_asof(tk,d)<MKT_MIN: continue
            data[tk]={"C":o["C"][:p+1],"H":o["H"][:p+1],"L":o["L"][:p+1],"V":o["V"][:p+1]}
        pk=screen_asof(data,spy6)
        if pk: signals[d]=set(pk)
        else: empty+=1
    market_ok={d:bool(spy_pos.get(d) is not None and spy_pos[d]>=200 and spy_C[spy_pos[d]]>float(np.mean(spy_C[spy_pos[d]-199:spy_pos[d]+1]))) for d in rebal}

    # 复利 SPY 基准
    spy_ret=round((spy_C[-1]/spy_C[start_i]-1)*100,1)

    sizings=[("frac",0.20),("frac",0.10),("frac",0.0714)]   # 5仓(集中) / 10仓 / 14仓(分散)——海龟式分散度对照
    snames={("frac",0.20):"frac20(~5仓集中)",("frac",0.10):"frac10(~10仓)",("frac",0.0714):"frac7(~14仓分散)"}
    slips=[0.0,0.002,0.004]
    table={}
    for rule in ("H","MA"):
        for gate,gn in ((False,"无闸门"),(True,"SPY200闸门")):
            mok=market_ok if gate else {d:True for d in rebal}
            for sz in sizings:
                key=f"{rule}/{gn}/{snames[sz]}"
                table[key]={f"{s*100:.1f}%": simulate(rule,signals,ohlc,posmap,last_date,bt,mok,s,sz,COMMISSION)
                            for s in slips}

    result={"generated":datetime.now().strftime("%Y-%m-%d %H:%M"),"window":[bt[0],bt[-1]],
            "commission":COMMISSION,"compounding":True,"spy_buyhold_ret_pct":spy_ret,
            "empty_boards":empty,"table":table}
    json.dump(result,open(OUT,"w"),ensure_ascii=False,indent=2)

    print(f"\n{'='*78}\n  MOM 仓位模型严谨版(复利+现金约束) {bt[0]}→{bt[-1]}\n{'='*78}")
    print(f"  佣金${COMMISSION}/笔(IBKR Lite) · 复利SPY买入持有 {spy_ret:+.1f}% · 空榜{empty}")
    print(f"  口径: 总收益%(复利) [trades/胜率/PF/最大回撤/退市] — 列=滑点 0/0.2%/0.4%\n")
    for key,row in table.items():
        cells=" | ".join(f"{row[f'{s*100:.1f}%']['ret_pct']:+7.1f}%" for s in slips)
        r0=row["0.0%"]
        print(f"  {key:34} {cells}   [DD{r0['max_dd_pct']}% 平{r0['trades']} 胜{r0['win_rate']}% PF{r0['pf']} 退{r0['delisted']}]")
    print(f"\n  ← 每格是该滑点下的复利总收益;和 SPY {spy_ret:+.1f}% 比。详情 {OUT}")


if __name__=="__main__":
    main()
