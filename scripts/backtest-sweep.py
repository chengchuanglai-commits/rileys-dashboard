"""全配置扫描 —— 找"牛市最大化收益 + 熊市保本/少亏"的最优配置。
统一: 复利(净值%) + 定投$500/月 + 佣金0.1% + 滑点0.2% + 5年(含2022完整熊市)。
扫描: 动量权重 × 熊市动作 × 动量股数。每个配置报 收益/最大回撤/熊市段表现。
对照: 定投QQQ / 定投SPY。
"""
import os, json
import numpy as np
import yfinance as yf

CACHE="data/fmp-cache"; PX_DIR=f"{CACHE}/px"; MC_DIR=f"{CACHE}/mc"
INIT=2000.0; MONTHLY=500.0
MKT_MIN=3_000_000_000; REBAL=5; SLIP=0.002; COMM=0.0010
CURATED=["ATVI","VMW","SGEN","ABMD","PXD","SPLK","TWTR","CTLT","ZEN","MNDT","CTXS","CERN",
    "NUAN","XLNX","MXIM","WORK","AVLR","COUP","CONE","QTS","CXO","KSU","INFO","TIF",
    "ALXN","VG","STOR","FLIR","ACIA","SIVB","FRC","SBNY","BBBY","WE","SAVE","TWNK"]

def load(sym,d):
    f=f"{d}/{sym}.json"; return json.load(open(f)) if os.path.exists(f) else None
def sma(a,n): return float(np.mean(a[-n:])) if len(a)>=n else None
def strong(close,spy6):
    if len(close)<220: return None
    c=close[-1]; ma50,ma150,ma200=sma(close,50),sma(close,150),sma(close,200); ma20=sma(close,20)
    if None in (ma50,ma150,ma200,ma20): return None
    ma200_1=sma(close[:-22],200); hi52=float(np.max(close[-252:])); lo52=float(np.min(close[-252:]))
    if not all([c>ma150 and c>ma200,ma150>ma200,ma200_1 is not None and ma200>ma200_1,ma50>ma150>ma200,c>ma50,c>=1.30*lo52,c>=0.75*hi52]): return None
    return c/close[-126]-1 - spy6 if len(close)>=126 else 0.0
def maxdd(s):
    peak=s[0]; dd=0
    for v in s: peak=max(peak,v); dd=min(dd,(v-peak)/peak if peak>0 else 0)
    return dd*100

# ===== 数据加载(一次) =====
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
qd=yf.Ticker("QQQ").history(start=sidx[0])["Close"].dropna(); qqq={d.strftime("%Y-%m-%d"):float(v) for d,v in qd.items()}
def mc_at(tk,d):
    s=mc.get(tk,[])
    if not s: return 0.0
    if d<s[0][0]: return s[0][1]
    v=0.0
    for dt,cap in s:
        if dt<=d: v=cap
        else: break
    return v
cal=sidx; start=252; bt=cal[start:]
def bull(d):
    q=spos.get(d); return q is not None and q>=200 and sC[q]>float(np.mean(sC[q-199:q+1]))
def qv(d): return qqq.get(d)
# 动量信号(各股数都从同一打分取topN)
sig_full={}
for i in range(start,len(cal),REBAL):
    d=cal[i]; q=spos.get(d)
    if q is None or q<200 or sC[q]<float(np.mean(sC[q-199:q+1])): continue
    spy6=float(sC[q]/sC[q-126]-1); rows=[]
    for tk,o in ohlc.items():
        p=posmap[tk].get(d)
        if p is None or p<220 or mc_at(tk,d)<MKT_MIN: continue
        sc=strong(o["C"][:p+1],spy6)
        if sc is not None: rows.append((sc,tk))
    rows.sort(reverse=True); sig_full[d]=[tk for _,tk in rows]
def ma20(tk,p):
    C=ohlc[tk]["C"]; return float(np.mean(C[p-19:p+1])) if p>=19 else None
def buy(px): return px*(1+SLIP+COMM)
def sell(px): return px*(1-SLIP-COMM)

# 熊市段索引(SPY回撤>10%)
sv=[float(sC[spos[d]]) for d in bt]; peak=sv[0]; bear_idx=[]
for i,v in enumerate(sv):
    peak=max(peak,v)
    if (peak-v)/peak>0.10: bear_idx.append(i)

def sim(mom_w, bear_action, mom_n):
    """mom_w=动量权重(0-1,余为QQQ); bear_action='cash'/'hold'/'half'; mom_n=动量股数"""
    qqq_w=1-mom_w
    cash=INIT; qsh=0.0; held={}; month=""; curve=[]
    for i,d in enumerate(bt):
        q=qv(d)
        if d[:7]!=month: month=d[:7]; cash+=MONTHLY
        # 动量出场
        for tk in list(held):
            p=posmap.get(tk,{}).get(d)
            if p is None: pos=held.pop(tk); cash+=pos["sh"]*sell(float(ohlc[tk]["C"][-1])); continue
            pos=held[tk]; lo=ohlc[tk]["L"][p]; cl=float(ohlc[tk]["C"][p])
            if lo<=pos["stop"]: cash+=held.pop(tk)["sh"]*sell(pos["stop"]); continue
            m=ma20(tk,p)
            if m and cl<m: cash+=held.pop(tk)["sh"]*sell(cl); continue
        if i%REBAL==0 and q:
            mval=sum(h["sh"]*float(ohlc[tk]["C"][posmap[tk][d]]) for tk,h in held.items() if posmap.get(tk,{}).get(d) is not None)
            total=cash+qsh*q+mval
            isbull=bull(d)
            # 熊市动作
            if not isbull:
                if bear_action=="cash":
                    if qsh>0: cash+=qsh*sell(q); qsh=0
                    for tk in list(held):
                        p=posmap.get(tk,{}).get(d)
                        if p is not None: cash+=held.pop(tk)["sh"]*sell(float(ohlc[tk]["C"][p]))
                elif bear_action=="half":
                    tq=qqq_w*total*0.5; cq=qsh*q
                    if cq>tq: qsh-=(cq-tq)/q; cash+=(cq-tq)*(1-SLIP-COMM)
                # hold=不动
            else:
                # 牛市:QQQ目标qqq_w
                tq=qqq_w*total; cq=qsh*q
                if cq<tq and cash>0: add=min(tq-cq,cash); qsh+=add/buy(q); cash-=add
                elif cq>tq: qsh-=(cq-tq)/q; cash+=(cq-tq)*(1-SLIP-COMM)
                if mom_w>0 and d in sig_full:
                    per=mom_w*total/mom_n
                    for tk in sig_full[d][:mom_n]:
                        if tk in held or cash<per*0.5: continue
                        p=posmap.get(tk,{}).get(d)
                        if p is None: continue
                        entry=float(ohlc[tk]["C"][p])
                        if entry<=0: continue
                        size=min(per,cash)
                        if size<5: continue
                        sh=size/buy(entry); cash-=size; held[tk]={"sh":sh,"stop":entry*0.92}
        mval=sum(h["sh"]*float(ohlc[tk]["C"][posmap[tk][d]]) for tk,h in held.items() if posmap.get(tk,{}).get(d) is not None)
        curve.append(cash+qsh*(q or 0)+mval)
    invested=INIT+MONTHLY*len(set(d[:7] for d in bt))
    bear_ret=(curve[bear_idx[-1]]/curve[bear_idx[0]]-1)*100 if len(bear_idx)>1 else 0
    return {"final":curve[-1],"ret":(curve[-1]/invested-1)*100,"maxdd":maxdd(curve),"bear_ret":bear_ret,"invested":invested}

# ===== 扫描 =====
print(f"扫描中 (窗口 {bt[0]}→{bt[-1]}, 复利+定投$500/月)...")
results=[]
for mw in [0.0,0.30,0.40,0.50,0.70,1.00]:
    for ba in (["cash","hold","half"] if mw>0 or True else ["hold"]):
        for mn in ([18,10] if mw>0 else [18]):
            if mw==0 and (mn==10 or ba in("cash","half")):  # 纯QQQ无动量,熊市动作仍测cash/hold
                if mn==10: continue
            r=sim(mw,ba,mn)
            results.append((mw,ba,mn,r))
# 对照
def dca(price_fn):
    sh=0.0; inv=INIT; mo=""; p0=price_fn(bt[0]);
    if p0: sh=INIT/p0
    s=[]
    for d in bt:
        p=price_fn(d)
        if d[:7]!=mo: mo=d[:7];
        if p and d[:7]!=getattr(dca,'_m',''): pass
        s.append(sh*(p or 0))
    # 重新正确做
    sh=0.0; inv=INIT; mo=""; s=[]
    if p0: sh=INIT/p0
    for d in bt:
        p=price_fn(d)
        if d[:7]!=mo:
            mo=d[:7]
            if p: sh+=MONTHLY/p; inv+=MONTHLY
        s.append(sh*(p or 0))
    return s,inv
sq,iq=dca(qv); ss,iis=dca(lambda d: float(sC[spos[d]]) if d in spos else None)
peakq=sq[0]; bq=[(peakq:=max(peakq,v),(peakq-v)/peakq)[1] for v in sq]

print(f"\n{'='*82}")
print(f"  全配置扫描 (5年含熊市,复利,定投$500/月,佣金+滑点)")
print(f"{'='*82}")
print(f"  {'动量权重':<8}{'熊市动作':<8}{'股数':<5}{'收益%':>8}{'最大回撤':>9}{'熊市段':>9}")
results.sort(key=lambda x:-x[3]['ret'])
for mw,ba,mn,r in results:
    print(f"  {int(mw*100):>3}%      {ba:<7} {mn:<5}{r['ret']:>+7.0f}%{r['maxdd']:>+8.1f}%{r['bear_ret']:>+8.1f}%")
print(f"  {'-'*78}")
print(f"  定投QQQ                  {(sq[-1]/iq-1)*100:>+7.0f}%{maxdd(sq):>+8.1f}%")
print(f"  定投SPY                  {(ss[-1]/iis-1)*100:>+7.0f}%{maxdd(ss):>+8.1f}%")
print(f"\n  目标:高收益+低回撤+熊市段不亏。⚠️动量腿仍残留幸存者偏差,偏乐观。")

out={"window":[bt[0],bt[-1]],"dca_qqq_ret":round((sq[-1]/iq-1)*100,1),"dca_qqq_dd":round(maxdd(sq),1),
     "configs":[{"mom_w":mw,"bear":ba,"n":mn,"ret":round(r['ret'],1),"maxdd":round(r['maxdd'],1),"bear_ret":round(r['bear_ret'],1)} for mw,ba,mn,r in results]}
json.dump(out,open("data/sweep-backtest.json","w"),ensure_ascii=False,indent=2)
