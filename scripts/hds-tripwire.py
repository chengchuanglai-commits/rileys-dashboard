"""hds 信号漂移 tripwire —— 防"静默换脑"(暴雷点#2,2026-07-19装)。
DeepSeek模型/上游依赖若悄悄变化,信号质量衰减只能从成绩单上滞后发现。本脚本把"发现"自动化:
滚动最近20笔平仓,胜率<45% 或 均笔收益<0 → 飞书警报(破线一次报一次,恢复报解除)。
基线参考:全史胜率66.7%/均笔+2.5%。阈值预注册,别看着数据调。
用法: python3 scripts/hds-tripwire.py  (run.sh review 每日调用)"""
import json, os

PORT = "data/portfolio_hds.json"
STATE = "data/hds-tripwire-state.json"
WINDOW = 20
MIN_WINRATE = 45.0   # %
MIN_MEAN_PCT = 0.0   # 每笔收益%


def notify(msg):
    print(msg)
    if os.environ.get("NOTIFY_WEBHOOK"):
        os.environ["NOTIFY_MESSAGE"] = msg
        import runpy
        try: runpy.run_path("scripts/notify-webhook.py", run_name="__main__")
        except Exception: pass


def main():
    d = json.load(open(PORT))
    cl = [p for p in d.get("closed_positions", []) if p.get("final_pnl_pct") is not None]
    cl.sort(key=lambda p: (p.get("close_date") or "", p.get("signal_date") or ""))
    if len(cl) < WINDOW:
        print(f"[tripwire] 平仓{len(cl)}<{WINDOW},样本不足静默"); return
    recent = cl[-WINDOW:]
    pcts = [float(p["final_pnl_pct"]) for p in recent]
    wr = sum(1 for x in pcts if x > 0) / WINDOW * 100
    mp = sum(pcts) / WINDOW
    breach = wr < MIN_WINRATE or mp < MIN_MEAN_PCT
    try: st = json.load(open(STATE))
    except Exception: st = {"breached": False}
    prev_breached = st.get("breached")
    # 数据回退守卫(2026-08-03实炸:行情拉不到→27笔平仓被误标在手→窗口漂移→tripwire被假"恢复"骗开闸):
    # 平仓总数只会单调增,变少=上游数据故障→本次不做任何判断/不写状态,保持现有闸位
    if len(cl) < st.get("n_closed", 0):
        print(f"[tripwire] ⚠️ 数据回退({len(cl)}<{st['n_closed']}笔),疑似行情缺失,跳过本次判断保持闸位"); return
    st["n_closed"] = len(cl)
    # 状态先落盘再通知(2026-07-29实炸:notify曾被SystemExit穿透,状态没写→自动解除永不触发)
    json.dump({"breached": breach, "n_closed": len(cl),
               "last": {"win_rate": round(wr, 1), "mean_pct": round(mp, 2)}},
              open(STATE, "w"))
    # 执行器(sleep-safe原则2026-07-19):破线不等人,直接落kill-switch;真钱执行层开单前必读此开关
    KS = "data/kill-switches.json"
    try: ks = json.load(open(KS))
    except Exception: ks = {}
    if breach and not prev_breached:
        ks["hds_new_entries"] = {"halted": True, "reason": f"tripwire破线 胜率{wr:.0f}%/均笔{mp:+.2f}%",
                                 "since": __import__("time").strftime("%Y-%m-%d %H:%M")}
        json.dump(ks, open(KS, "w"), ensure_ascii=False, indent=1)
        notify(f"🚨 hds tripwire 破线 → 已自动处置,无需你操作\n"
               f"滚动{WINDOW}笔: 胜率{wr:.0f}%(线45%) 均笔{mp:+.2f}%(线0)\n"
               f"✅ 系统已做: kill-switch落盘,真钱端新开仓自动停(paper继续攒数据)\n"
               f"你醒后可做: 看排查清单①DeepSeek模型版本②依赖③regime,再决定复活或退役\n"
               f"（交易信号系统·hds tripwire·已自动处置）")
    elif not breach and prev_breached:
        ks["hds_new_entries"] = {"halted": False, "recovered": __import__("time").strftime("%Y-%m-%d %H:%M")}
        json.dump(ks, open(KS, "w"), ensure_ascii=False, indent=1)
        notify(f"✅ hds tripwire 解除(自动):滚动{WINDOW}笔 胜率{wr:.0f}% 均笔{mp:+.2f}% 回线上,kill-switch已释放\n（交易信号系统·hds tripwire）")
    else:
        tag = "破线持续" if breach else "正常"
        print(f"[tripwire] {tag}: 滚动{WINDOW}笔 胜率{wr:.0f}% 均笔{mp:+.2f}%")


if __name__ == "__main__":
    main()
