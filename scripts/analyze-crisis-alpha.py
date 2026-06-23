"""危机 alpha 分析 (crisis alpha) —— 回答 Riley:"大盘大跌时,我们的动量腿少跌吗?"

复用 FMP 缓存(2021-06起,含完整2022熊市)。跑 MOM-MA+SPY200闸门+frac10,生成逐日净值曲线,
对比 SPY 买入持有。重点:找出 SPY 的大回撤时段,看动量腿在那些时段跌多少。
输出 data/crisis-alpha.json(供报告/dashboard)。
"""
import os, json, sys
from datetime import datetime
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
# 复用回测引擎的选股+模拟逻辑
import importlib.util
spec = importlib.util.spec_from_file_location("btsized", os.path.join(os.path.dirname(__file__), "backtest-momentum-sized.py"))
bt = importlib.util.module_from_spec(spec)

CACHE = "data/fmp-cache"; PX_DIR = f"{CACHE}/px"; MC_DIR = f"{CACHE}/mc"
INIT = 2000.0; MKT_MIN = 3_000_000_000; TOP_N = 10; REBAL = 5
CURATED = ["ATVI","VMW","SGEN","ABMD","PXD","SPLK","TWTR","CTLT","ZEN","MNDT","CTXS","CERN",
    "NUAN","XLNX","MXIM","WORK","AVLR","COUP","CONE","QTS","CXO","KSU","INFO","TIF",
    "ALXN","VG","STOR","FLIR","ACIA","SIVB","FRC","SBNY","BBBY","WE","SAVE","TWNK"]


def load(sym, d):
    f=f"{d}/{sym}.json"
    return json.load(open(f)) if os.path.exists(f) else None


# ---- 选股逻辑(与实盘screen-momentum一致,简版内联) ----
def sma(a,n): return float(np.mean(a[-n:])) if len(a)>=n else None
def analyze(close,high,low,vol,spy6):
    if len(close)<220: return None
    c=close[-1]; ma50,ma150,ma200=sma(close,50),sma(close,150),sma(close,200); ma10,ma20=sma(close,10),sma(close,20)
    if None in (ma50,ma150,ma200,ma10,ma20): return None
    ma200_1=sma(close[:-22],200); hi52=float(np.max(close[-252:])); lo52=float(np.min(close[-252:]))
    if not all([c>ma150 and c>ma200,ma150>ma200,ma200_1 is not None and ma200>ma200_1,ma50>ma150>ma200,c>ma50,c>=1.30*lo52,c>=0.75*hi52]): return None
    ret6=c/close[-126]-1 if len(close)>=126 else 0.0; rs=ret6-spy6
    mb=max(ma10,ma20); epb=float(np.clip(1-((c-mb)/mb)/0.12,0,1))
    v5,v50=sma(vol,5),sma(vol,50); vr=(v5/v50) if (v5 and v50 and v50>0) else 1.0
    evc=float(np.clip(1-(vr-0.6)/0.8,0,1)); enh=float(np.clip(1+((c-hi52)/hi52)/0.25,0,1))
    return {"rs":rs,"epb":epb,"evc":evc,"enh":enh}
def screen(data,spy6):
    rows=[{"tk":tk,**analyze(s["C"],s["H"],s["L"],s["V"],spy6)} for tk,s in data.items() if analyze(s["C"],s["H"],s["L"],s["V"],spy6)]
    if not rows: return []
    rss=sorted(rows,key=lambda r:-r["rs"]); n=len(rss)
    for i,r in enumerate(rss): r["rsr"]=1-i/(n-1) if n>1 else 0.5
    for r in rows: r["sc"]=0.40*r["rsr"]+0.25*r["epb"]+0.15*r["evc"]+0.20*r["enh"]
    rows.sort(key=lambda r:-r["sc"]); return [r["tk"] for r in rows[:TOP_N]]


def main():
    u=load("universe", CACHE) or {}
    universe=sorted(set(u.get("current",[]))|set(u.get("delisted_kept",[]))|set(CURATED))
    ohlc,posmap,last_date,mc={}, {}, {}, {}
    for tk in universe:
        rows=load(tk,PX_DIR)
        if not rows or len(rows)<240: continue
        idx=[r[0] for r in rows]
        ohlc[tk]={"H":np.array([r[1] for r in rows]),"L":np.array([r[2] for r in rows]),"C":np.array([r[3] for r in rows]),"V":np.array([r[4] for r in rows]),"idx":idx}
        posmap[tk]={d:j for j,d in enumerate(idx)}; last_date[tk]=idx[-1]; mc[tk]=load(tk,MC_DIR) or []
    spy=load("SPY",PX_DIR); sidx=[r[0] for r in spy]; sC=np.array([r[3] for r in spy]); spos={d:j for j,d in enumerate(sidx)}
    print(f"[cache] {len(ohlc)}票 SPY {sidx[0]}→{sidx[-1]}")
    def mc_at(tk,date):
        v=0.0
        for dt,cap in mc.get(tk,[]):
            if dt<=date: v=cap
            else: break
        return v
    cal=sidx; start=252
    rebal=[cal[i] for i in range(start,len(cal),REBAL)]
    bt_cal=cal[start:]
    sig={}
    for d in rebal:
        q=spos.get(d)
        if q is None or q<126: continue
        spy6=float(sC[q]/sC[q-126]-1)
        data={}
        for tk,o in ohlc.items():
            p=posmap[tk].get(d)
            if p is None or p<220 or mc_at(tk,d)<MKT_MIN: continue
            data[tk]={"C":o["C"][:p+1],"H":o["H"][:p+1],"L":o["L"][:p+1],"V":o["V"][:p+1]}
        pk=screen(data,spy6)
        if pk: sig[d]=set(pk)
    # SPY-200MA闸门
    mok={d:bool(spos.get(d) is not None and spos[d]>=200 and sC[spos[d]]>float(np.mean(sC[spos[d]-199:spos[d]+1]))) for d in rebal}

    # 模拟 MOM-MA+闸门+frac10,逐日记净值
    cash=INIT; held={}; equity_curve=[]
    def ma_at(tk,p,n):
        C=ohlc[tk]["C"]; return float(np.mean(C[p-n+1:p+1])) if p>=n-1 else None
    last_rebal=-999
    for i,date in enumerate(bt_cal):
        # 出场:20MA破位/初始-8%
        for tk in list(held):
            p=posmap.get(tk,{}).get(date)
            if p is None:
                if date>last_date.get(tk,"9999"):
                    pos=held.pop(tk); cash+=pos["sh"]*float(ohlc[tk]["C"][-1])
                continue
            pos=held[tk]; lo=ohlc[tk]["L"][p]; cl=ohlc[tk]["C"][p]
            if lo<=pos["stop"]: cash+=held.pop(tk)["sh"]*pos["stop"]; continue
            ma=ma_at(tk,p,20)
            if ma is not None and cl<ma: cash+=held.pop(tk)["sh"]*float(cl); continue
        # 进场:闸门放行+frac10
        if date in sig and (i-last_rebal)>=REBAL and mok.get(date,True):
            eq=cash+sum(h["sh"]*float(ohlc[tk]["C"][posmap[tk][date]]) for tk,h in held.items() if posmap.get(tk,{}).get(date) is not None)
            for tk in sig[date]:
                if tk in held: continue
                p=posmap.get(tk,{}).get(date)
                if p is None: continue
                entry=float(ohlc[tk]["C"][p])
                if entry<=0: continue
                size=min(0.10*eq,cash)
                if size<5: continue
                sh=size/entry; cash-=size
                held[tk]={"sh":sh,"entry":entry,"stop":entry*0.92}
            last_rebal=i
        # 记净值
        eq=cash+sum(h["sh"]*float(ohlc[tk]["C"][posmap[tk][date]]) for tk,h in held.items() if posmap.get(tk,{}).get(date) is not None)
        q=spos.get(date)
        equity_curve.append((date,round(eq,2),round(float(sC[q]/sC[start]*INIT),2) if q else None))

    # 找 SPY 大回撤时段 + 对比
    dates=[e[0] for e in equity_curve]; mom=[e[1] for e in equity_curve]; spv=[e[2] for e in equity_curve if e[2]]
    spv_full=[e[2] for e in equity_curve]
    # SPY峰值回撤
    speak=spv_full[0]; mompeak=mom[0]; worst=[]
    spy_dd=[]; mom_dd=[]
    for i,(d,m,s) in enumerate(equity_curve):
        if s:
            speak=max(speak,s); spy_dd.append((speak-s)/speak)
        else: spy_dd.append(0)
        mompeak=max(mompeak,m); mom_dd.append((mompeak-m)/mompeak)
    # 最大回撤
    spy_maxdd=max(spy_dd); mom_maxdd=max(mom_dd)
    # SPY回撤>10%的日子里,动量腿平均回撤
    crisis_idx=[i for i,dd in enumerate(spy_dd) if dd>0.10]
    spy_crisis_dd=np.mean([spy_dd[i] for i in crisis_idx]) if crisis_idx else 0
    mom_crisis_dd=np.mean([mom_dd[i] for i in crisis_idx]) if crisis_idx else 0

    out={"window":[dates[0],dates[-1]],
         "spy_total_ret_pct":round((spv_full[-1]/INIT-1)*100,1) if spv_full[-1] else None,
         "mom_total_ret_pct":round((mom[-1]/INIT-1)*100,1),
         "spy_max_drawdown_pct":round(spy_maxdd*100,1),
         "mom_max_drawdown_pct":round(mom_maxdd*100,1),
         "crisis_days":len(crisis_idx),
         "spy_avg_dd_in_crisis_pct":round(spy_crisis_dd*100,1),
         "mom_avg_dd_in_crisis_pct":round(mom_crisis_dd*100,1),
         "curve":[(d,m,s) for d,m,s in equity_curve[::5]]}  # 每5天采样省空间
    json.dump(out,open("data/crisis-alpha.json","w"),ensure_ascii=False,indent=2)

    print(f"\n{'='*60}\n  危机 alpha 分析 {dates[0]}→{dates[-1]}\n{'='*60}")
    print(f"  总收益: 动量腿 {out['mom_total_ret_pct']:+.1f}%  vs  SPY {out['spy_total_ret_pct']:+.1f}%")
    print(f"  最大回撤: 动量腿 -{out['mom_max_drawdown_pct']}%  vs  SPY -{out['spy_max_drawdown_pct']}%")
    print(f"\n  🎯 危机时段(SPY回撤>10%的{out['crisis_days']}天):")
    print(f"     SPY 平均回撤 -{out['spy_avg_dd_in_crisis_pct']}%")
    print(f"     动量腿平均回撤 -{out['mom_avg_dd_in_crisis_pct']}%")
    diff=out['spy_avg_dd_in_crisis_pct']-out['mom_avg_dd_in_crisis_pct']
    print(f"     → 大跌时动量腿少跌 {diff:+.1f} 个百分点 {'✅有抗跌' if diff>0 else '❌没抗跌'}")
    print(f"\n  详情 → data/crisis-alpha.json")


if __name__=="__main__":
    main()
