"""各腿相关性矩阵 + 最优组合 —— 抄大机构(WorldQuant)作业:找"互不相关的弱signal组合"。
不是找冠军腿,是找互补腿:负/低相关的腿组合起来降风险提夏普(文艺复兴核心)。
用各腿的日收益率(从已有回测/缓存重建净值曲线),算相关矩阵 + 等权组合 vs 单腿对照。
诚实:动量腿有幸存者偏差(偏乐观),但**相关性结构**受偏差影响小(相对关系比绝对收益稳)。
"""
import os, json
import numpy as np
import yfinance as yf

CACHE="data/fmp-cache"; PX_DIR=f"{CACHE}/px"; MC_DIR=f"{CACHE}/mc"
INIT=2000.0; MKT_MIN=3e9; REBAL=5; SLIP=0.002; COMM=0.001

def load(s,d):
    f=f"{d}/{s}.json"; return json.load(open(f)) if os.path.exists(f) else None
def sma(a,n): return float(np.mean(a[-n:])) if len(a)>=n else None

# 数据
syms=[f.replace(".json","") for f in os.listdir(PX_DIR) if f.endswith(".json")]
ohlc,posmap,mc={}, {}, {}
for tk in syms:
    if tk in("SPY","QQQ"): continue
    rows=load(tk,PX_DIR)
    if not rows or len(rows)<240: continue
    idx=[r[0] for r in rows]
    ohlc[tk]={"C":np.array([r[3] for r in rows]),"H":np.array([r[1] for r in rows]),"L":np.array([r[2] for r in rows]),"idx":idx}
    posmap[tk]={d:j for j,d in enumerate(idx)}; mc[tk]=load(tk,MC_DIR) or []
spy=load("SPY",PX_DIR); sidx=[r[0] for r in spy]; sC=np.array([r[3] for r in spy]); spos={d:j for j,d in enumerate(sidx)}
qd=yf.Ticker("QQQ").history(start=sidx[0])["Close"].dropna(); qqq={d.strftime("%Y-%m-%d"):float(v) for d,v in qd.items()}
def mc_at(tk,d):
    s=mc.get(tk,[])
    if not s: return 0
    if d<s[0][0]: return s[0][1]
    v=0
    for dt,c in s:
        if dt<=d: v=c
        else: break
    return v
cal=sidx; start=252; bt=cal[start:]
print(f"窗口 {bt[0]}→{bt[-1]}")

def strong(c,s6):
    if len(c)<220: return None
    x=c[-1]; m50,m150,m200=sma(c,50),sma(c,150),sma(c,200); m20=sma(c,20)
    if None in(m50,m150,m200,m20): return None
    m2=sma(c[:-22],200); hi=float(np.max(c[-252:])); lo=float(np.min(c[-252:]))
    if not all([x>m150 and x>m200,m150>m200,m2 is not None and m200>m2,m50>m150>m200,x>m50,x>=1.30*lo,x>=0.75*hi]): return None
    return x/c[-126]-1-s6 if len(c)>=126 else 0
def weak(c,s6):
    if len(c)<220: return None
    x=c[-1]; m50,m150,m200=sma(c,50),sma(c,150),sma(c,200); m20=sma(c,20)
    if None in(m50,m150,m200,m20): return None
    lo=float(np.min(c[-252:]))
    if not(x<m150 and x<m200 and m50<m150 and x<m20 and x<=1.25*lo): return None
    return -(x/c[-126]-1-s6) if len(c)>=126 else 0

# ===== 各腿净值曲线(统一frac10复利,无定投,看纯策略相关性) =====
def sim_leg(score_fn, side, gate_bull, n=10):
    """通用单腿:score_fn选股,side=1多/-1空,gate_bull=只在牛市开仓"""
    cash=INIT; held={}; curve=[]; last=-999
    def ma20(tk,p):
        C=ohlc[tk]["C"]; return float(np.mean(C[p-19:p+1])) if p>=19 else None
    sig={}
    for i in range(start,len(cal),REBAL):
        d=cal[i]; q=spos.get(d)
        if q is None or q<200: continue
        above=sC[q]>float(np.mean(sC[q-199:q+1]))
        if gate_bull and not above: continue
        if not gate_bull and above: continue  # 空头腿只在熊市
        s6=float(sC[q]/sC[q-126]-1); rows=[]
        for tk,o in ohlc.items():
            p=posmap[tk].get(d)
            if p is None or p<220 or mc_at(tk,d)<MKT_MIN: continue
            sc=score_fn(o["C"][:p+1],s6)
            if sc is not None: rows.append((sc,tk))
        rows.sort(reverse=True)
        if rows: sig[d]=[tk for _,tk in rows[:n]]
    for i,d in enumerate(bt):
        for tk in list(held):
            p=posmap.get(tk,{}).get(d)
            if p is None: pos=held.pop(tk); cash+=pos["v"]; continue
            pos=held[tk]; cl=float(ohlc[tk]["C"][p])
            if side>0:
                if cl<=pos["stop"]: cash+=held.pop(tk)["sh"]*cl*(1-SLIP-COMM); continue
                m=ma20(tk,p)
                if m and cl<m: cash+=held.pop(tk)["sh"]*cl*(1-SLIP-COMM); continue
            else:
                if cl>=pos["stop"]: cash+=pos["margin"]+pos["sh"]*(pos["ef"]-cl*(1+SLIP+COMM)); held.pop(tk); continue
                m=ma20(tk,p)
                if m and cl>m: cash+=held.pop(tk)["margin"]+held.get(tk,{}).get("sh",0)*0;
        if i%REBAL==0 and d in sig:
            eq=cash+sum((h["sh"]*float(ohlc[tk]["C"][posmap[tk][d]]) if side>0 else h["margin"]+h["sh"]*(h["ef"]-float(ohlc[tk]["C"][posmap[tk][d]]))) for tk,h in held.items() if posmap.get(tk,{}).get(d) is not None)
            per=eq/n
            for tk in sig[d]:
                if tk in held: continue
                p=posmap.get(tk,{}).get(d)
                if p is None: continue
                e=float(ohlc[tk]["C"][p])
                if e<=0 or cash<per*0.5: continue
                size=min(per,cash); cash-=size
                if side>0: held[tk]={"sh":size/(e*(1+SLIP+COMM)),"stop":e*0.92,"v":size}
                else: held[tk]={"sh":size/e,"ef":e*(1-SLIP),"stop":e*1.08,"margin":size,"v":size}
            last=i
        eq=cash+sum((h["sh"]*float(ohlc[tk]["C"][posmap[tk][d]]) if side>0 else h["margin"]+h["sh"]*(h["ef"]-float(ohlc[tk]["C"][posmap[tk][d]]))) for tk,h in held.items() if posmap.get(tk,{}).get(d) is not None)
        curve.append(eq)
    return curve

# 指数腿
def idx_curve(d_px):
    p0=d_px(bt[0]); s=[]
    for d in bt:
        p=d_px(d); s.append(INIT*p/p0 if (p and p0) else (s[-1] if s else INIT))
    return s

print("计算各腿净值曲线...")
legs={}
legs["QQQ"]=idx_curve(qqq.get)
legs["SPY"]=idx_curve(lambda d: float(sC[spos[d]]) if d in spos else None)
legs["动量(多)"]=sim_leg(strong,1,True,10)
legs["做空(熊市)"]=sim_leg(weak,-1,False,10)

# 日收益率
rets={}
for k,c in legs.items():
    c=np.array(c); r=np.diff(c)/np.where(np.array(c[:-1])==0,1,c[:-1]); rets[k]=r
keys=list(rets.keys()); L=min(len(r) for r in rets.values())
M=np.array([rets[k][:L] for k in keys])
corr=np.corrcoef(M)

print(f"\n{'='*52}\n  各腿相关性矩阵(日收益,越低越互补)\n{'='*52}")
print("        "+" ".join(f"{k[:6]:>7}" for k in keys))
for i,k in enumerate(keys):
    print(f"  {k[:7]:<7}"+" ".join(f"{corr[i][j]:>7.2f}" for j in range(len(keys))))

# 等权组合 vs 单腿:夏普对照
def stats(c):
    c=np.array(c); r=np.diff(c)/np.where(c[:-1]==0,1,c[:-1])
    ret=(c[-1]/INIT-1)*100; vol=np.std(r)*np.sqrt(252)*100
    sharpe=(np.mean(r)*252)/(np.std(r)*np.sqrt(252)+1e-9)
    peak=c[0]; dd=0
    for v in c: peak=max(peak,v); dd=min(dd,(v-peak)/peak if peak>0 else 0)
    return ret,vol,sharpe,dd*100
print(f"\n{'='*52}\n  单腿 vs 组合(夏普=风险调整收益,越高越好)\n{'='*52}")
print(f"  {'腿/组合':<14}{'收益%':>8}{'波动%':>8}{'夏普':>7}{'回撤%':>8}")
for k in keys:
    r,v,s,dd=stats(legs[k]); print(f"  {k:<14}{r:>+7.0f}%{v:>7.0f}%{s:>7.2f}{dd:>+7.1f}%")
# 等权组合(动量+做空+QQQ)
combo=np.mean([np.array(legs["动量(多)"][:L+1]),np.array(legs["做空(熊市)"][:L+1]),np.array(legs["QQQ"][:L+1])],axis=0)
r,v,s,dd=stats(combo); print(f"  {'等权组合(3腿)':<13}{r:>+7.0f}%{v:>7.0f}%{s:>7.2f}{dd:>+7.1f}%")
print(f"\n  ⚠️ 动量腿幸存者偏差→绝对收益偏乐观;但相关性/夏普的'相对结论'更稳。")

# ===== 静态互补组合 v1: 1x QQQ 锚 + 动量卫星(剔除做空) =====
# 设计+红队: docs/superpowers/specs/2026-07-10-static-combo-design.md
import sys as _sys, pandas as _pd; _sys.path.insert(0, "scripts")
from lev_engine import simulate_leverage
# lev(杠杆闸门指数)基准: 同窗口重归一到 bt[0]=INIT。curve元素=(date_str,equity,lev)
_qd=sorted(qqq.keys())
_ser=_pd.Series([qqq[d] for d in _qd], index=_pd.to_datetime(_qd))
_lev=simulate_leverage(_ser)["curve"]
_ceq={row[0]:row[1] for row in _lev}
_bv=next((_ceq[d] for d in sorted(_ceq) if d>=bt[0]), _lev[0][1])
_levbt=[]; _prev=INIT
for d in bt:
    _v=_ceq.get(d)
    if _v is not None: _prev=INIT*_v/_bv
    _levbt.append(_prev)
legs["lev(杠杆闸门)"]=_levbt
# QQQ+动量 锚重权重带(每日定权重再平衡, 不优化)
_qc=np.array(legs["QQQ"]); _mc=np.array(legs["动量(多)"]); _L2=min(len(_qc),len(_mc))
_qr=np.diff(_qc[:_L2])/np.where(_qc[:_L2-1]==0,1,_qc[:_L2-1])
_mr=np.diff(_mc[:_L2])/np.where(_mc[:_L2-1]==0,1,_mc[:_L2-1])
def _combo(wm):
    r=wm*_mr+(1-wm)*_qr; c=[INIT]
    for x in r: c.append(c[-1]*(1+float(x)))
    return c
_band={0.10:"90/10",0.20:"80/20",0.30:"70/30"}
print(f"\n{'='*56}\n  静态组合: 1x QQQ 锚 + 动量卫星 (锚重带, 剔除做空)\n{'='*56}")
print(f"  {'配置':<16}{'收益%':>8}{'波动%':>8}{'夏普':>7}{'回撤%':>8}")
for k in ["QQQ","动量(多)","lev(杠杆闸门)"]:
    r,v,s,dd=stats(legs[k]); print(f"  {k:<16}{r:>+7.0f}%{v:>7.0f}%{s:>7.2f}{dd:>+7.1f}%")
_cs={}
for wm,lab in _band.items():
    r,v,s,dd=stats(_combo(wm)); _cs[lab]=[r,v,s,dd]
    print(f"  {'QQQ+动量 '+lab:<15}{r:>+7.0f}%{v:>7.0f}%{s:>7.2f}{dd:>+7.1f}%")
# lev+动量 叠加带(杠杆指数锚 + 动量卫星)——测叠加能否顶过0.91
_lc=np.array(legs["lev(杠杆闸门)"]); _L3=min(len(_lc),len(_mc))
_lr=np.diff(_lc[:_L3])/np.where(_lc[:_L3-1]==0,1,_lc[:_L3-1])
_mr3=np.diff(_mc[:_L3])/np.where(_mc[:_L3-1]==0,1,_mc[:_L3-1])
def _combo_lev(wm):
    r=wm*_mr3+(1-wm)*_lr; c=[INIT]
    for x in r: c.append(c[-1]*(1+float(x)))
    return c
_cl={}
for wm,lab in _band.items():
    r,v,s,dd=stats(_combo_lev(wm)); _cl[lab]=[r,v,s,dd]
    print(f"  {'lev+动量 '+lab:<15}{r:>+7.0f}%{v:>7.0f}%{s:>7.2f}{dd:>+7.1f}%")
_qs=stats(legs["QQQ"])[2]; _ls=stats(legs["lev(杠杆闸门)"])[2]
_bq=max(_cs.items(),key=lambda kv:kv[1][2]); _bl=max(_cl.items(),key=lambda kv:kv[1][2])
print(f"\n  裁决(夏普): 裸QQQ {_qs:.2f} | 裸lev {_ls:.2f} | QQQ+动量最佳 {_bq[1][2]:.2f}({_bq[0]}) | lev+动量最佳 {_bl[1][2]:.2f}({_bl[0]})")
print(f"    → lev+动量叠加 {'✅ 顶过lev(叠加有效)' if _bl[1][2]>_ls+0.005 else '❌ 没顶过lev(叠加≈冗余防御)'}")
print("  ⚠️ 5年单一牛市窗口+动量幸存者偏差; lev与动量崩盘都去防御→可能冗余; 真裁决在前向.")

out={"window":[bt[0],bt[-1]],"legs":keys,"corr":corr.tolist(),
     "stats":{k:list(stats(legs[k])) for k in keys},
     "static_combo":{"lev_sharpe":_ls,"qqq_sharpe":_qs,"qqq_mom_band":_cs,"lev_mom_band":_cl}}
json.dump(out,open("data/leg-correlation.json","w"),ensure_ascii=False,indent=2)
