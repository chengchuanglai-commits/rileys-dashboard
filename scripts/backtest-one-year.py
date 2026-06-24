"""一年实测:去年今天投$2000,用当前策略(50%QQQ + 50%动量腿),到今天账户多少钱。
逐日真实价格。动量腿=选强势股+20MA出场去现金+frac10再平衡。
⚠️幸存者偏差:动量universe是今天的票→偏乐观,标注。
用法: python scripts/backtest-one-year.py
"""
import json, os
import numpy as np
from datetime import date, timedelta
import yfinance as yf

INIT = 2000.0
INDEX_PCT = 0.50      # QQQ核心
ACTIVE_PCT = 0.50     # 动量腿
TOP_N = 10
REBAL = 5
SLIP = 0.002

# 动量腿 universe(同实盘momma:今日流动中大盘 + 当前持仓票)。简化:用一组当前流动龙头
UNIVERSE = ["NVDA","MSFT","AAPL","AMZN","GOOGL","META","AVGO","TSLA","AMD","MU","COHR","HUT",
    "GFS","ON","RVMD","VICR","STM","IESC","STRL","CRWD","PLTR","ANET","VRT","LRCX","KLAC",
    "MRVL","SMCI","DELL","PANW","NOW","SNOW","UBER","NET","DDOG","CEG","VST","DECK","CELH"]


def sma(a,n): return float(np.mean(a[-n:])) if len(a)>=n else None
def strong(close,spy6):
    if len(close)<220: return None
    c=close[-1]; ma50,ma150,ma200=sma(close,50),sma(close,150),sma(close,200); ma20=sma(close,20)
    if None in (ma50,ma150,ma200,ma20): return None
    ma200_1=sma(close[:-22],200); hi52=float(np.max(close[-252:])); lo52=float(np.min(close[-252:]))
    if not all([c>ma150 and c>ma200,ma150>ma200,ma200_1 is not None and ma200>ma200_1,ma50>ma150>ma200,c>ma50,c>=1.30*lo52,c>=0.75*hi52]): return None
    return c/close[-126]-1 - spy6 if len(close)>=126 else 0.0


def main():
    today=date.today()
    start=(today-timedelta(days=520)).isoformat()  # 多拉留足200MA回看
    bt_start=(today-timedelta(days=365)).isoformat()
    print(f"一年实测: {bt_start} → {today.isoformat()} · $2000起")

    # 下载
    syms=UNIVERSE+["QQQ","SPY"]
    raw=yf.download(syms,start=start,progress=False,group_by="ticker",threads=True)
    px={}
    for tk in syms:
        try:
            c=raw[tk]["Close"].dropna()
            px[tk]={d.strftime("%Y-%m-%d"):float(v) for d,v in c.items()}
        except Exception: pass
    spy=px.get("SPY",{}); qqq=px.get("QQQ",{})
    cal=sorted(d for d in spy if d>=bt_start)
    if not cal: print("无数据"); return

    # ---- 指数核心:QQQ买入持有(50%) ----
    q0=qqq.get(cal[0])
    idx_cap=INIT*INDEX_PCT
    idx_shares=idx_cap/q0 if q0 else 0

    # ---- 动量腿(50%):逐日模拟 ----
    full_cal=sorted(spy.keys())
    def hist(tk,upto):  # tk 截止 upto 的收盘序列
        return [px[tk][d] for d in full_cal if d<=upto and d in px.get(tk,{})]
    cash=INIT*ACTIVE_PCT; held={}; last_rebal=-999
    mom_curve=[]
    rebal_days=set(cal[i] for i in range(0,len(cal),REBAL))
    for i,d in enumerate(cal):
        # 出场:20MA破位/-8%止损
        for tk in list(held):
            if d not in px.get(tk,{}): continue
            h=hist(tk,d); cl=px[tk][d]
            pos=held[tk]
            if cl<=pos["stop"]: cash+=held.pop(tk)["sh"]*pos["stop"]*(1-SLIP); continue
            ma20=sma(np.array(h),20)
            if ma20 and cl<ma20: cash+=held.pop(tk)["sh"]*cl*(1-SLIP); continue
        # 进场(再平衡日,SPY>200MA)
        if d in rebal_days and (i-last_rebal)>=REBAL:
            sh_=hist("SPY",d)
            if len(sh_)>=200 and sh_[-1]>sma(np.array(sh_),200):
                spy6=sh_[-1]/sh_[-126]-1 if len(sh_)>=126 else 0
                rows=[]
                for tk in UNIVERSE:
                    h=hist(tk,d)
                    sc=strong(np.array(h),spy6)
                    if sc is not None: rows.append((sc,tk))
                rows.sort(reverse=True)
                eq=cash+sum(h2["sh"]*px[tk][d] for tk,h2 in held.items() if d in px.get(tk,{}))
                for _,tk in rows[:TOP_N]:
                    if tk in held or d not in px.get(tk,{}): continue
                    entry=px[tk][d]; size=min(0.10*eq,cash)
                    if size<5: continue
                    sh=size/(entry*(1+SLIP)); cash-=size; held[tk]={"sh":sh,"stop":entry*0.92}
                last_rebal=i
        mom_eq=cash+sum(h2["sh"]*px[tk][d] for tk,h2 in held.items() if d in px.get(tk,{}))
        idx_eq=idx_shares*qqq.get(d,q0)
        mom_curve.append((d,round(idx_eq+mom_eq,2)))

    final=mom_curve[-1][1]
    # 对照:全押QQQ / 全押SPY
    qf=INIT*qqq.get(cal[-1],q0)/q0
    s0=spy.get(cal[0]); sf=INIT*spy.get(cal[-1],s0)/s0

    out={"window":[cal[0],cal[-1]],"init":INIT,"final":round(final,2),
         "ret_pct":round((final/INIT-1)*100,1),
         "vs_allQQQ":round(qf,0),"vs_allSPY":round(sf,0),
         "note":"50%QQQ买入持有+50%动量腿(20MA去现金).幸存者偏差(universe今日票)→偏乐观."}
    json.dump(out,open("data/one-year-test.json","w"),ensure_ascii=False,indent=2)
    print(f"\n{'='*56}\n  一年实测结果 ({cal[0]} → {cal[-1]})\n{'='*56}")
    print(f"  起始: ${INIT:.0f}")
    print(f"  💰 今天账户: ${final:.0f}  ({(final/INIT-1)*100:+.1f}%)")
    print(f"\n  对照(同样$2000):")
    print(f"    全押QQQ: ${qf:.0f} ({(qf/INIT-1)*100:+.1f}%)")
    print(f"    全押SPY: ${sf:.0f} ({(sf/INIT-1)*100:+.1f}%)")
    print(f"\n  ⚠️ {out['note']}")

if __name__=="__main__":
    main()
