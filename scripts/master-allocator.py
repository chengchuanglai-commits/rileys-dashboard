"""统一组合调度器 (master allocator) —— 三线合体:30%指数+20%长线+50%波动,一份总信号,Riley一次执行。
系统全自动决定每条线买什么/卖什么/多少;Riley只批准执行(见 feedback_riley_role_execute_only)。

三线:
  - 指数核心(默认30%): QQQ 买入持有,定投注入。
  - 长线持股(默认20%): longterm-manager 选的9只等权(季度复检)。
  - 波动捕捉(默认50%): IBKR动量腿(MOM-MA,已在IBKR系统自动跑)——这里只汇报目标,实际下单走IBKR执行层。
权重可调(读 config),且未来可接动态配置引擎按regime/信念调。
输出 data/master-allocation.json + dashboard/master-allocation.js + 飞书总信号。
用法: python scripts/master-allocator.py   (CAPITAL/权重见顶部常量)
"""
import os, json, time

CAPITAL=20000.0          # 当前总资金(真实账户净值,先用名义)
W_INDEX=0.30            # 指数核心
W_LONGTERM=0.20         # 长线持股
W_VOLATILITY=0.50       # 波动捕捉(动量)
INDEX_SYM="QQQ"

def load(p,d=None):
    try: return json.load(open(p))
    except Exception: return d

def main():
    cap=CAPITAL
    today=time.strftime("%Y-%m-%d")
    out={"date":today,"capital":cap,"weights":{"index":W_INDEX,"longterm":W_LONGTERM,"volatility":W_VOLATILITY},
         "sleeves":{}}

    # ===== 1. 指数核心 =====
    idx_usd=W_INDEX*cap
    out["sleeves"]["index"]={"target_usd":round(idx_usd),"holding":INDEX_SYM,
        "action":f"持有 {INDEX_SYM} ≈${idx_usd:.0f}(定投时按比例注入)"}

    # ===== 2. 长线持股(读longterm-portfolio) =====
    lt=load("data/longterm-portfolio.json",{})
    lt_holds=list((lt.get("holdings") or {}).keys())
    lt_usd=W_LONGTERM*cap
    per_lt=lt_usd/len(lt_holds) if lt_holds else 0
    out["sleeves"]["longterm"]={"target_usd":round(lt_usd),"holdings":lt_holds,
        "per_each":round(per_lt),"action":f"{len(lt_holds)}只等权各≈${per_lt:.0f}: {', '.join(lt_holds)}"}

    # ===== 3. 波动捕捉(动量腿,IBKR系统在跑) =====
    vol_usd=W_VOLATILITY*cap
    momma=load("data/portfolio_momma.json",{})
    mom_holds=[p.get("ticker") for p in (momma.get("open_positions") or []) if p.get("ticker")]
    vol_warn=""
    # 护栏:momma空大概率是断网/回填失败(2026-06-27踩坑)→若上次master有持仓,保留之,绝不把波动腿清零
    #(否则trade_open会把动量仓全卖掉=误清仓)。真要空仓避险也得连续两次确认,这里宁可滞后不误清。
    if not mom_holds:
        prev=load("data/master-allocation.json",{})
        prev_holds=(prev.get("sleeves",{}).get("volatility",{}) or {}).get("current_holdings",[])
        if prev_holds:
            mom_holds=prev_holds
            vol_warn=f" ⚠️momma为空(疑回填失败),保留上次持仓{prev_holds}防误清仓"
            print(f"  ⚠️ 护栏触发:momma open_positions为空→保留上次波动腿持仓{prev_holds}(防断网导致误清仓)")
    out["sleeves"]["volatility"]={"target_usd":round(vol_usd),"engine":"IBKR动量腿(MOM-MA自动)",
        "current_holdings":mom_holds,"warn":vol_warn,
        "action":f"动量腿 ≈${vol_usd:.0f},IBKR系统自动选股/止损/出场。当前持仓{len(mom_holds)}只: {', '.join(mom_holds) if mom_holds else '(空仓避险)'}{vol_warn}"}

    json.dump(out,open("data/master-allocation.json","w"),ensure_ascii=False,indent=2)
    with open("dashboard/master-allocation.js","w",encoding="utf-8") as f:
        f.write(f"window.MASTER_ALLOCATION = {json.dumps(out,ensure_ascii=False)};\n")

    # 报告
    print(f"\n{'='*64}\n  统一组合 {today} (总资金${cap:.0f})\n{'='*64}")
    print(f"  ① 指数核心 {int(W_INDEX*100)}% (${idx_usd:.0f}): 持有{INDEX_SYM}")
    print(f"  ② 长线持股 {int(W_LONGTERM*100)}% (${lt_usd:.0f}): {len(lt_holds)}只等权各${per_lt:.0f}")
    print(f"       {', '.join(lt_holds)}")
    print(f"  ③ 波动捕捉 {int(W_VOLATILITY*100)}% (${vol_usd:.0f}): IBKR动量腿自动")
    print(f"       当前{len(mom_holds)}只: {', '.join(mom_holds) if mom_holds else '空仓避险'}")
    print(f"\n  ⚠️ 系统全自动决定;Riley只批准执行。指数+长线手动/半自动下单,波动腿IBKR全自动。")

    # 飞书总信号
    if os.environ.get("NOTIFY_WEBHOOK"):
        msg=[f"📊 统一组合 {today} (${cap:.0f})",
             f"① 指数 {int(W_INDEX*100)}%: {INDEX_SYM} ${idx_usd:.0f}",
             f"② 长线 {int(W_LONGTERM*100)}%: {len(lt_holds)}只 {','.join(lt_holds[:5])}...",
             f"③ 波动 {int(W_VOLATILITY*100)}%: 动量腿{len(mom_holds)}只(IBKR自动)",
             "（系统决定,待执行·交易信号系统）"]
        os.environ["NOTIFY_MESSAGE"]="\n".join(msg)
        import runpy
        try: runpy.run_path("scripts/notify-webhook.py",run_name="__main__")
        except Exception: pass

if __name__=="__main__":
    main()
