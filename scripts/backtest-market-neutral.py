"""市场中性腿回测 (market-neutral / crisis alpha #2) —— 多强势股 + 空弱势股,对冲大盘涨跌。

逻辑:
  - **多头**:动量选股(强势领导股,RS高) —— 复用 backtest-momentum 的选股。
  - **空头**:弱势股(RS最低、跌破均线) —— 复用 trend-short 的弱势选股。
  - **每边各占净值50%**(美元中性 dollar-neutral),多空同时持有→对冲掉大盘beta。
  - 不依赖牛熊:牛市多头赚多/空头亏少,熊市空头赚多/多头亏少,赚的是**选股价差(强-弱)**。
  - 出场:多头破20MA平/空头站上20MA平;周再平衡。frac10口径(每边各5仓)。
复用FMP缓存。重点看:总收益(能赚吗)、与SPY相关性(够中性吗)、崩盘表现、波动。
输出 data/market-neutral-backtest.json。
"""
import os, json
import numpy as np

CACHE="data/fmp-cache"; PX_DIR=f"{CACHE}/px"; MC_DIR=f"{CACHE}/mc"
INIT=2000.0; MKT_MIN=3_000_000_000; N_SIDE=5; REBAL=5; SLIP=0.002
# 借券成本(borrow fee,年化)——做空要付。没历史数据,保守分档估:
#   普通大盘股易借~3%/年;濒死/暴雷股(将退市)极难借~80%/年甚至借不到。
import os as _os
BORROW_NORMAL=0.03      # 普通可借股年化借券费
BORROW_DISTRESSED=0.80  # 濒死股(临近退市)年化借券费(现实可能更高/借不到)
# 这些是回测窗口内真退市的票:做空它们现实中借券极贵/可能借不到→打上濒死标记
DISTRESSED={"SIVB","FRC","SBNY","BBBY","WE","SAVE","TWNK","FTX","ATVI","VMW","SGEN","ABMD",
    "PXD","SPLK","TWTR","CTLT","ZEN","MNDT","CTXS","CERN","NUAN","XLNX","MXIM","WORK","AVLR",
    "COUP","CONE","QTS","CXO","KSU","INFO","TIF","ALXN","VG","STOR","FLIR","ACIA"}
EXCLUDE_UNBORROWABLE=_os.environ.get("MN_EXCLUDE_DISTRESSED","")=="1"  # =1则干脆不空濒死股(更保守)
CURATED=["ATVI","VMW","SGEN","ABMD","PXD","SPLK","TWTR","CTLT","ZEN","MNDT","CTXS","CERN",
    "NUAN","XLNX","MXIM","WORK","AVLR","COUP","CONE","QTS","CXO","KSU","INFO","TIF",
    "ALXN","VG","STOR","FLIR","ACIA","SIVB","FRC","SBNY","BBBY","WE","SAVE","TWNK"]

def load(sym,d):
    f=f"{d}/{sym}.json"; return json.load(open(f)) if os.path.exists(f) else None
def sma(a,n): return float(np.mean(a[-n:])) if len(a)>=n else None

def strong_score(close,high,low,vol,spy6):
    """强势分(动量,做多)。"""
    if len(close)<220: return None
    c=close[-1]; ma50,ma150,ma200=sma(close,50),sma(close,150),sma(close,200); ma10,ma20=sma(close,10),sma(close,20)
    if None in (ma50,ma150,ma200,ma10,ma20): return None
    ma200_1=sma(close[:-22],200); hi52=float(np.max(close[-252:])); lo52=float(np.min(close[-252:]))
    if not all([c>ma150 and c>ma200,ma150>ma200,ma200_1 is not None and ma200>ma200_1,ma50>ma150>ma200,c>ma50,c>=1.30*lo52,c>=0.75*hi52]): return None
    ret6=c/close[-126]-1 if len(close)>=126 else 0.0
    return ret6-spy6   # RS

def weak_score(close,high,low,vol,spy6):
    """弱势分(做空)。"""
    if len(close)<220: return None
    c=close[-1]; ma50,ma150,ma200=sma(close,50),sma(close,150),sma(close,200); ma20=sma(close,20)
    if None in (ma50,ma150,ma200,ma20): return None
    lo52=float(np.min(close[-252:]))
    if not (c<ma150 and c<ma200 and ma50<ma150 and c<ma20 and c<=1.25*lo52): return None
    ret6=c/close[-126]-1 if len(close)>=126 else 0.0
    return -(ret6-spy6)   # -RS,越大越弱

def main():
    u=load("universe",CACHE) or {}
    universe=sorted(set(u.get("current",[]))|set(u.get("delisted_kept",[]))|set(CURATED))
    ohlc,posmap,last_date,mc={}, {}, {}, {}
    for tk in universe:
        rows=load(tk,PX_DIR)
        if not rows or len(rows)<240: continue
        idx=[r[0] for r in rows]
        ohlc[tk]={"C":np.array([r[3] for r in rows]),"H":np.array([r[1] for r in rows]),"L":np.array([r[2] for r in rows]),"V":np.array([r[4] for r in rows]),"idx":idx}
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
    longs={}; shorts={}
    for d in rebal:
        q=spos.get(d)
        if q is None or q<200: continue
        spy6=float(sC[q]/sC[q-126]-1)
        ls=[]; ws=[]
        for tk,o in ohlc.items():
            p=posmap[tk].get(d)
            if p is None or p<220 or mc_at(tk,d)<MKT_MIN: continue
            sc=strong_score(o["C"][:p+1],o["H"][:p+1],o["L"][:p+1],o["V"][:p+1],spy6)
            if sc is not None: ls.append((sc,tk))
            wc=weak_score(o["C"][:p+1],o["H"][:p+1],o["L"][:p+1],o["V"][:p+1],spy6)
            if wc is not None: ws.append((wc,tk))
        ls.sort(reverse=True); ws.sort(reverse=True)
        longs[d]=set(tk for _,tk in ls[:N_SIDE]); shorts[d]=set(tk for _,tk in ws[:N_SIDE])

    cash=INIT; Lh={}; Sh={}; curve=[]
    def ma_at(tk,p,n):
        C=ohlc[tk]["C"]; return float(np.mean(C[p-n+1:p+1])) if p>=n-1 else None
    last_rebal=-999
    for i,date in enumerate(bt_cal):
        q=spos.get(date)
        # 多头出场:破20MA
        for tk in list(Lh):
            p=posmap.get(tk,{}).get(date)
            if p is None: pos=Lh.pop(tk); cash+=pos["val"]; continue
            pos=Lh[tk]; cl=float(ohlc[tk]["C"][p]); ma=ma_at(tk,p,20)
            if ma is not None and cl<ma:
                cash+=pos["sh"]*cl*(1-SLIP); Lh.pop(tk)
        # 空头出场:站上20MA / +8%止损
        for tk in list(Sh):
            p=posmap.get(tk,{}).get(date)
            if p is None: pos=Sh.pop(tk); cash+=pos["val"]; continue
            pos=Sh[tk]; cl=float(ohlc[tk]["C"][p]); hi=ohlc[tk]["H"][p]; ma=ma_at(tk,p,20)
            if (ma is not None and cl>ma) or hi>=pos["stop"]:
                exit_px=pos["stop"] if hi>=pos["stop"] else cl
                cash+=pos["margin"]+pos["sh"]*(pos["entry_fill"]-exit_px*(1+SLIP)); Sh.pop(tk)
        # 再平衡:每边各开到N_SIDE,各占净值~50%
        if date in longs and (i-last_rebal)>=REBAL:
            eq=cash
            for tk,h in Lh.items():
                p=posmap.get(tk,{}).get(date); eq+=h["sh"]*float(ohlc[tk]["C"][p])*0 # 已在cash估?简化:重算
            # 重算净值
            eq=cash+sum(h["sh"]*float(ohlc[tk]["C"][posmap[tk][date]]) for tk,h in Lh.items() if posmap.get(tk,{}).get(date) is not None)
            eq+=sum(h["margin"]+h["sh"]*(h["entry_fill"]-float(ohlc[tk]["C"][posmap[tk][date]])) for tk,h in Sh.items() if posmap.get(tk,{}).get(date) is not None)
            per=0.10*eq
            for tk in longs[date]:
                if tk in Lh: continue
                p=posmap.get(tk,{}).get(date)
                if p is None: continue
                entry=float(ohlc[tk]["C"][p])
                if entry<=0 or per>cash: continue
                sh=per/(entry*(1+SLIP)); cash-=per; Lh[tk]={"sh":sh,"val":per}
            for tk in shorts[date]:
                if tk in Sh: continue
                if EXCLUDE_UNBORROWABLE and tk in DISTRESSED: continue  # 借不到券→不空(最保守)
                p=posmap.get(tk,{}).get(date)
                if p is None: continue
                entry=float(ohlc[tk]["C"][p])
                if entry<=0 or per>cash: continue
                fee=BORROW_DISTRESSED if tk in DISTRESSED else BORROW_NORMAL
                sh=per/entry; cash-=per
                Sh[tk]={"sh":sh,"entry_fill":entry*(1-SLIP),"stop":entry*1.08,"margin":per,"val":per,"borrow_daily":fee/252,"open_date":date}
            last_rebal=i
        # 净值
        eq=cash
        for tk,h in Lh.items():
            p=posmap.get(tk,{}).get(date); cur=float(ohlc[tk]["C"][p]) if p is not None else h.get("val",0)
            h["val"]=h["sh"]*cur if p is not None else h["val"]; eq+=h["val"]
        for tk,h in Sh.items():
            p=posmap.get(tk,{}).get(date); cur=float(ohlc[tk]["C"][p]) if p is not None else None
            # 每日扣借券费(按当前空头市值计)
            cash-=h["sh"]*(cur if cur is not None else h["entry_fill"])*h.get("borrow_daily",0)
            h["val"]=h["margin"]+h["sh"]*(h["entry_fill"]-cur) if cur is not None else h["val"]; eq+=h["val"]
        curve.append((date,round(eq,2),round(float(sC[q]/sC[start]*INIT),2) if q else None))

    dates=[c[0] for c in curve]; mn=[c[1] for c in curve]; spv=[c[2] for c in curve]
    mnret=np.diff(mn)/np.array(mn[:-1])
    spvf=[x or mn[i] for i,x in enumerate(spv)]; spr=np.diff(spvf)/np.array(spvf[:-1])
    corr=float(np.corrcoef(mnret,spr)[0,1]) if len(mnret)>2 else 0
    years=len(mn)/252; cagr=((mn[-1]/INIT)**(1/years)-1)*100
    vol=float(np.std(mnret)*np.sqrt(252)*100)
    peak=mn[0]; dd=0
    for m in mn: peak=max(peak,m); dd=min(dd,(m-peak)/peak)
    # 崩盘段
    speak=spvf[0]; spy_dd=[]
    for s in spvf: speak=max(speak,s); spy_dd.append((speak-s)/speak)
    crisis=[i for i,x in enumerate(spy_dd) if x>0.10]
    mn_in_crisis=(mn[crisis[-1]]/mn[crisis[0]]-1)*100 if len(crisis)>1 else 0

    out={"window":[dates[0],dates[-1]],"total_ret_pct":round((mn[-1]/INIT-1)*100,1),
         "cagr_pct":round(cagr,1),"spy_total_ret_pct":round((spvf[-1]/INIT-1)*100,1),
         "corr_with_spy":round(corr,2),"annual_vol_pct":round(vol,1),"max_drawdown_pct":round(dd*100,1),
         "crisis_days":len(crisis),"ret_during_crisis_pct":round(mn_in_crisis,1)}
    json.dump(out,open("data/market-neutral-backtest.json","w"),ensure_ascii=False,indent=2)
    print(f"\n{'='*58}\n  市场中性腿回测 {dates[0]}→{dates[-1]}\n{'='*58}")
    print(f"  总收益: {out['total_ret_pct']:+.1f}% (年化{out['cagr_pct']:+.1f}%)  vs SPY {out['spy_total_ret_pct']:+.1f}%")
    print(f"  与SPY相关性: {out['corr_with_spy']:+.2f} (接近0=真中性)")
    print(f"  年化波动: {out['annual_vol_pct']}%  最大回撤: {out['max_drawdown_pct']}%")
    print(f"  🎯 崩盘时段(SPY回撤>10%): {out['ret_during_crisis_pct']:+.1f}%")

if __name__=="__main__":
    main()
