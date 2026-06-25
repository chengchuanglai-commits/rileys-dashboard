"""长线腿全自动管理 —— 系统自动:选股→定仓→季度盯财报→自动卖出信号。Riley只执行。
持有8-10只(等权),每季度财报后复检:分数跌破阈值/触发红线 → 卖出信号。
为"20%长线持股"(核心-卫星里的长线sleeve)。读 longterm-candidates.json(选股器产出)。

逻辑:
  - 建仓:从候选榜TOP取N只等权(可读理解过滤,但默认按分数)。
  - 持有:记录每只的入选分数。
  - 卖出信号(任一触发):①分数跌破 SELL_SCORE ②营收转负 ③经营现金流转负 ④跌出榜单前60名。
  - 输出 data/longterm-portfolio.json + 卖出/调仓信号,推飞书等Riley执行。
用法: FMP_API_KEY=... python scripts/longterm-manager.py
"""
import os, json, time
import urllib.request

NOTIONAL_PCT=0.20       # 长线腿=总资金20%
HOLD_N=9                # 持有9只(8-10区间中值)
SELL_SCORE=65           # 分数跌破65→卖出信号
RANK_DROP=60            # 跌出候选榜前60→卖出信号
STATE="data/longterm-portfolio.json"

def load(p,d=None):
    try: return json.load(open(p))
    except Exception: return d

def main():
    cands=load("data/longterm-candidates.json")
    if not cands:
        print("无候选榜,先跑 longterm-screener.py"); return
    by_sym={c["sym"]:c for c in cands}
    rank={c["sym"]:i+1 for i,c in enumerate(cands)}   # 榜单排名
    port=load(STATE,{"holdings":{},"updated":"","_note":"长线腿:系统选股+季度复检+自动卖出,Riley只执行"})
    holdings=port.get("holdings",{})

    signals=[]   # 给Riley执行的信号
    today=time.strftime("%Y-%m-%d")

    # ===== 1. 复检现有持仓:该卖吗 =====
    for sym in list(holdings.keys()):
        c=by_sym.get(sym)
        reasons=[]
        if c is None:
            reasons.append("跌出基本面合格池(红线/烧钱)")
        else:
            if c["score"]<SELL_SCORE: reasons.append(f"分数{c['score']}<{SELL_SCORE}")
            if rank.get(sym,999)>RANK_DROP: reasons.append(f"排名跌出前{RANK_DROP}(现{rank.get(sym)})")
            if c["rev_cagr"]<0: reasons.append("营收转负")
        if reasons:
            signals.append(("SELL",sym,"; ".join(reasons)))

    # ===== 2. 选新仓补到 HOLD_N 只 =====
    keep=[s for s in holdings if s not in [x[1] for x in signals if x[0]=="SELL"]]
    need=HOLD_N-len(keep)
    if need>0:
        for c in cands:
            if c["sym"] in keep: continue
            if len(keep)>=HOLD_N: break
            keep.append(c["sym"]); signals.append(("BUY",c["sym"],f"入选分{c['score']} 营收{c['rev_cagr']:+}% 毛利{c['gm']}% PE{c['pe']}"))

    # ===== 3. 更新持仓状态 =====
    new_holdings={}
    for s in keep:
        c=by_sym.get(s,{})
        new_holdings[s]={"score":c.get("score"),"added":holdings.get(s,{}).get("added",today) if s in holdings else today}
    port["holdings"]=new_holdings; port["updated"]=today
    port["hold_n"]=HOLD_N; port["per_weight_pct"]=round(NOTIONAL_PCT/HOLD_N*100,1)
    json.dump(port,open(STATE,"w"),ensure_ascii=False,indent=2)

    # ===== 报告 =====
    print(f"\n{'='*60}\n  长线腿自动管理 {today}\n{'='*60}")
    print(f"  目标:持有{HOLD_N}只等权(各占总资金{port['per_weight_pct']}%)")
    print(f"  当前持仓: {', '.join(new_holdings.keys())}")
    if signals:
        print(f"\n  📋 待执行信号 ({len(signals)}条):")
        for act,sym,why in signals:
            print(f"    {'🔴卖' if act=='SELL' else '🟢买'} {sym}: {why}")
    else:
        print("\n  ✅ 无调仓信号,继续持有")
    print(f"\n  ⚠️ 系统自动决定选股/卖出;Riley只需批准执行。每季度财报后复检。")

    # 飞书(有webhook才推)
    if os.environ.get("NOTIFY_WEBHOOK") and signals:
        msg=[f"📈 长线腿调仓信号 {today}"]
        for act,sym,why in signals: msg.append(f"{'🔴卖' if act=='SELL' else '🟢买'} {sym}: {why[:40]}")
        msg.append("（系统决定,待你执行·交易信号系统）")
        os.environ["NOTIFY_MESSAGE"]="\n".join(msg)
        import runpy
        try: runpy.run_path("scripts/notify-webhook.py",run_name="__main__")
        except Exception: pass

if __name__=="__main__":
    main()
