"""趋势做空腿回测 (trend short / crisis alpha #1) —— 验证"崩盘真能赚"。

逻辑(动量的镜像):
  - **只在熊市开空**:SPY < 200MA(大盘下跌趋势)才做空,牛市不碰(空头在牛市被轧)。
  - **选弱势股做空**:用动量选股的反面——RS最低(跑输大盘最多)、跌破均线、近期新低 → 做空。
  - 出场:收盘**站上**20MA(止跌反弹)→平空;初始+8%硬止损(防被轧)。
  - frac10复利,SPY200闸门反向(SPY>200MA则全平不开空)。
复用FMP缓存(2021-06起含2022熊市)。重点看:2022熊市它赚钱吗?与SPY/动量腿相关性?
输出 data/trend-short-backtest.json。
"""
import os, json, sys
import numpy as np

CACHE="data/fmp-cache"; PX_DIR=f"{CACHE}/px"; MC_DIR=f"{CACHE}/mc"
INIT=2000.0; MKT_MIN=3_000_000_000; BOTTOM_N=10; REBAL=5
SLIP=0.002   # 0.2%滑点(做空成本更现实)
CURATED=["ATVI","VMW","SGEN","ABMD","PXD","SPLK","TWTR","CTLT","ZEN","MNDT","CTXS","CERN",
    "NUAN","XLNX","MXIM","WORK","AVLR","COUP","CONE","QTS","CXO","KSU","INFO","TIF",
    "ALXN","VG","STOR","FLIR","ACIA","SIVB","FRC","SBNY","BBBY","WE","SAVE","TWNK"]

def load(sym,d):
    f=f"{d}/{sym}.json"; return json.load(open(f)) if os.path.exists(f) else None
def sma(a,n): return float(np.mean(a[-n:])) if len(a)>=n else None

def weak_score(close,high,low,vol,spy6):
    """弱势分:动量的反面。返回分(越高越该做空)或None(不够弱)。"""
    if len(close)<220: return None
    c=close[-1]; ma50,ma150,ma200=sma(close,50),sma(close,150),sma(close,200); ma20=sma(close,20)
    if None in (ma50,ma150,ma200,ma20): return None
    hi52=float(np.max(close[-252:])); lo52=float(np.min(close[-252:]))
    # 下跌趋势硬闸门(Minervini反面):价在均线下、均线空头排列、近52周低
    if not (c<ma150 and c<ma200 and ma50<ma150 and c<ma20 and c<=1.25*lo52): return None
    ret6=c/close[-126]-1 if len(close)>=126 else 0.0
    rs=ret6-spy6                       # RS越负=越跑输大盘=越弱
    near_low=(c-lo52)/lo52             # 越接近52周低越弱
    return -rs + (1-min(near_low,1))   # 综合弱势分

def main():
    u=load("universe",CACHE) or {}
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
    # 选股(只在熊市选)
    sig={}; bear_days=0
    for d in rebal:
        q=spos.get(d)
        if q is None or q<200: continue
        bear = sC[q] < float(np.mean(sC[q-199:q+1]))   # SPY<200MA=熊市
        if not bear: continue
        bear_days+=1
        spy6=float(sC[q]/sC[q-126]-1)
        rows=[]
        for tk,o in ohlc.items():
            p=posmap[tk].get(d)
            if p is None or p<220 or mc_at(tk,d)<MKT_MIN: continue
            sc=weak_score(o["C"][:p+1],o["H"][:p+1],o["L"][:p+1],o["V"][:p+1],spy6)
            if sc is not None: rows.append((sc,tk))
        rows.sort(reverse=True)
        if rows: sig[d]=set(tk for _,tk in rows[:BOTTOM_N])

    # 模拟做空+frac10复利,逐日记净值
    cash=INIT; held={}; curve=[]
    def ma_at(tk,p,n):
        C=ohlc[tk]["C"]; return float(np.mean(C[p-n+1:p+1])) if p>=n-1 else None
    last_rebal=-999
    for i,date in enumerate(bt_cal):
        q=spos.get(date)
        spy_bull = q is not None and q>=200 and sC[q]>float(np.mean(sC[q-199:q+1]))
        # 出场:站上20MA平空/+8%止损/大盘转牛全平
        for tk in list(held):
            p=posmap.get(tk,{}).get(date)
            if p is None:
                pos=held.pop(tk); cash+=pos["val"]; continue   # 退市按最后估值平
            pos=held[tk]; hi=ohlc[tk]["H"][p]; cl=float(ohlc[tk]["C"][p])
            # 空头盈亏:跌赚涨亏
            if spy_bull or (ma_at(tk,p,20) is not None and cl>ma_at(tk,p,20)) or hi>=pos["stop"]:
                exit_px=pos["stop"] if hi>=pos["stop"] else cl
                exit_fill=exit_px*(1+SLIP)   # 平空=买回,滑点向上
                pnl=pos["sh"]*(pos["entry_fill"]-exit_fill)  # 空头:入场价-平仓价
                cash+=pos["margin"]+pnl
                held.pop(tk)
        # 进场(只熊市)
        if date in sig and (i-last_rebal)>=REBAL and not spy_bull:
            eq=cash+sum(h["margin"]+h["sh"]*(h["entry_fill"]-float(ohlc[tk]["C"][posmap[tk][date]])) for tk,h in held.items() if posmap.get(tk,{}).get(date) is not None)
            for tk in sig[date]:
                if tk in held: continue
                p=posmap.get(tk,{}).get(date)
                if p is None: continue
                entry=float(ohlc[tk]["C"][p])
                if entry<=0: continue
                size=min(0.10*eq,cash)
                if size<5: continue
                entry_fill=entry*(1-SLIP)  # 做空=卖出,滑点向下
                sh=size/entry; cash-=size
                held[tk]={"sh":sh,"entry_fill":entry_fill,"stop":entry*1.08,"margin":size}
            last_rebal=i
        # 记净值
        eq=cash
        for tk,h in held.items():
            p=posmap.get(tk,{}).get(date)
            cur=float(ohlc[tk]["C"][p]) if p is not None else h["entry_fill"]
            eq+=h["margin"]+h["sh"]*(h["entry_fill"]-cur)
            h["val"]=h["margin"]+h["sh"]*(h["entry_fill"]-cur)
        curve.append((date,round(eq,2),round(float(sC[q]/sC[start]*INIT),2) if q else None))

    dates=[c[0] for c in curve]; sht=[c[1] for c in curve]; spv=[c[2] for c in curve]
    # SPY熊市段(回撤>10%)里,做空腿表现
    speak=spv[0]; spy_dd=[]
    for s in spv:
        if s: speak=max(speak,s); spy_dd.append((speak-s)/speak)
        else: spy_dd.append(0)
    crisis=[i for i,dd in enumerate(spy_dd) if dd>0.10]
    short_in_crisis = (sht[crisis[-1]]/sht[crisis[0]]-1)*100 if len(crisis)>1 else 0
    # 相关性(日收益)
    sr=np.diff(sht)/np.array(sht[:-1]); spr=np.diff([x or sht[i] for i,x in enumerate(spv)])/np.array([x or sht[i] for i,x in enumerate(spv)][:-1])
    corr=float(np.corrcoef(sr,spr)[0,1]) if len(sr)>2 else 0

    out={"window":[dates[0],dates[-1]],"short_total_ret_pct":round((sht[-1]/INIT-1)*100,1),
         "spy_total_ret_pct":round((spv[-1]/INIT-1)*100,1) if spv[-1] else None,
         "bear_rebalances":bear_days,"crisis_days":len(crisis),
         "short_ret_during_crisis_pct":round(short_in_crisis,1),
         "corr_with_spy":round(corr,2)}
    json.dump(out,open("data/trend-short-backtest.json","w"),ensure_ascii=False,indent=2)
    print(f"\n{'='*58}\n  趋势做空腿回测 {dates[0]}→{dates[-1]}\n{'='*58}")
    print(f"  做空腿总收益: {out['short_total_ret_pct']:+.1f}%  (SPY {out['spy_total_ret_pct']:+.1f}%)")
    print(f"  熊市再平衡点: {bear_days}个 (只熊市开空)")
    print(f"  🎯 危机时段(SPY回撤>10%): 做空腿 {out['short_ret_during_crisis_pct']:+.1f}%")
    print(f"  与SPY相关性: {out['corr_with_spy']:+.2f} (越负=崩盘越保护)")

if __name__=="__main__":
    main()
