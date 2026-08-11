"""hds 真钱上车 gate —— 预注册裁决(Riley 2026-07-14批准)。
与 analyze-leg-edge(80笔edge体检,看统计显著性)互补:本gate裁"真钱资格"。

预注册标准(中途不许改,改=作废重开):
  锚点 2026-07-13收盘(baseline_pv/baseline_trades取当日) → 到期 2026-09-08(8周)
  ① 累计平仓 ≥80 笔(锚点48笔;2026-07-17从100修订对齐edge体检线,留痕见gate json)
  ② 窗口收益(净值口径,佣金已含) > 同窗口 QQQ 收益
  ③ 窗口内 QQQ 最大回撤 ≥3%(测试有效性:SL-2%没经历过回撤考验不算数)
裁决:
  ①②③全过 → PASS:从波动腿$10000切20%($2000)给hds真钱试运行4周,对比真实滑点(执行仍需Riley批准)
  仅③不满足(市场太平静) → EXTEND 一次至 2026-10-06,再到期只裁①②
  其余 → FAIL:不上真钱,不讨论
行为:每日静默;注册日+周五推进度到飞书;到期推裁决(一次,flag防重)。
用法: python3 scripts/hds-gate.py   (run.sh review 每日调用; FORCE=1 强制推进度)
"""
import json, os, datetime

GATE = "data/hds-gate.json"
PORT = "data/portfolio_hds.json"


def qqq_closes(start):
    import yfinance as yf
    px = yf.download("QQQ", start=start, end="2027-01-01", progress=False)["Close"]
    px = (px["QQQ"] if hasattr(px, "columns") else px).dropna()
    return [(str(k.date()), float(v)) for k, v in px.items()]


def max_dd_pct(vals):
    peak, dd = float("-inf"), 0.0
    for v in vals:
        peak = max(peak, v)
        if peak > 0:
            dd = max(dd, (peak - v) / peak)
    return dd * 100


def notify(msg):
    print(msg)
    if os.environ.get("NOTIFY_WEBHOOK"):
        os.environ["NOTIFY_MESSAGE"] = msg
        import runpy
        try: runpy.run_path("scripts/notify-webhook.py", run_name="__main__")
        except Exception as e: print(f"[hds-gate] 推送失败: {e}")


def run():
    today = datetime.date.today().isoformat()
    port = json.load(open(PORT))
    s = port.get("stats", {})
    pv = s.get("portfolio_value")
    trades = s.get("total_trades", 0)

    # ---- 初始化(预注册,只发生一次) ----
    if not os.path.exists(GATE):
        g = {
            "_note": "hds真钱上车gate·预注册2026-07-14·标准见scripts/hds-gate.py,中途不许改",
            "anchor_date": "2026-07-13",
            "end": "2026-09-08",
            "extended_end": "2026-10-06",
            "extended": False,
            "min_trades_total": 100,
            "qqq_dd_required_pct": 3.0,
            "baseline_pv": pv,
            "baseline_trades": trades,
            "verdict": None,
            "last_progress_push": None,
        }
        json.dump(g, open(GATE, "w"), ensure_ascii=False, indent=2)
        notify("🚦 hds 真钱gate 已预注册(2026-07-14)\n"
               f"锚点07-13收盘: 净值${pv:.0f} / 已平{trades}笔\n"
               "标准(到期机械裁决,不许中途改):\n"
               f"① 累计平仓≥100笔\n"
               "② 窗口净值收益 > 同期QQQ(佣金已含)\n"
               "③ 窗口内QQQ回撤≥3%(仅此项不满足→顺延4周一次)\n"
               "到期 2026-09-08 · PASS→波动腿20%($2000)真钱试4周\n"
               "（交易信号系统·hds gate）")
        return

    g = json.load(open(GATE))
    if g.get("verdict"):
        print(f"[hds-gate] 已裁决 {g['verdict']},跳过"); return

    # ---- 计算三项进度 ----
    closes = qqq_closes(g["anchor_date"])
    if not closes:
        print("[hds-gate] QQQ数据为空,跳过"); return
    q0, q1 = closes[0][1], closes[-1][1]
    qqq_ret = (q1 / q0 - 1) * 100
    hds_ret = (pv / g["baseline_pv"] - 1) * 100
    qdd = max_dd_pct([v for _, v in closes])
    c1 = trades >= g["min_trades_total"]
    c2 = hds_ret > qqq_ret
    c3 = qdd >= g["qqq_dd_required_pct"]

    end = g["extended_end"] if g["extended"] else g["end"]
    expired = today >= end
    # 早裁条款(2026-07-18修订,Riley批):三条标准同时满足即刻裁决,不等日历(标准一字未降,只去掉人为时间下限)
    early_all_met = c1 and c2 and c3

    # ---- 到期/达标裁决(一次) ----
    if expired or early_all_met:
        if c1 and c2 and c3:
            verdict = "PASS"
        elif c1 and c2 and not c3 and not g["extended"]:
            g["extended"] = True
            json.dump(g, open(GATE, "w"), ensure_ascii=False, indent=2)
            notify("🚦 hds gate 到期:①②过但QQQ全程回撤<3%(市场太平静)\n"
                   f"→ 按预注册规则顺延一次至 {g['extended_end']},再到期只裁①②\n"
                   "（交易信号系统·hds gate）")
            return
        else:
            verdict = "FAIL"
        # extended到期:只裁①②
        if g["extended"] and c1 and c2:
            verdict = "PASS"
        g["verdict"] = verdict
        g["verdict_date"] = today
        g["final"] = {"trades": trades, "hds_ret_pct": round(hds_ret, 2),
                      "qqq_ret_pct": round(qqq_ret, 2), "qqq_maxdd_pct": round(qdd, 2)}
        json.dump(g, open(GATE, "w"), ensure_ascii=False, indent=2)
        icon = "🟢" if verdict == "PASS" else "🔴"
        margin = hds_ret - qqq_ret
        act = ((f"→ 通过预注册决策规则(80笔样本无统计学证明力,只代表'允许继续小额实验')。\n"
                f"→ 仓位解冻:领先{margin:+.1f}pp{'≥2pp,按净值全解冻' if margin >= 2 else '<2pp属边缘PASS,半解冻帽$2100(协议修订#3)'}")
               if verdict == "PASS" else "→ 不上真钱。按预注册纪律退役,证据归档,不讨价还价")
        notify(f"{icon} hds 真钱gate 裁决: {verdict}\n"
               f"① 平仓 {trades}/{g['min_trades_total']} {'✅' if c1 else '❌'}\n"
               f"② hds {hds_ret:+.1f}% vs QQQ {qqq_ret:+.1f}% {'✅' if c2 else '❌'}\n"
               f"③ QQQ窗口最大回撤 {qdd:.1f}%/{g['qqq_dd_required_pct']}% {'✅' if c3 else '❌'}\n"
               f"{act}\n（交易信号系统·hds gate）")
        return

    # ---- 未到期:周五推进度(其余静默) ----
    is_friday = datetime.date.today().weekday() == 4
    if (is_friday and g.get("last_progress_push") != today) or os.environ.get("FORCE") == "1":
        g["last_progress_push"] = today
        json.dump(g, open(GATE, "w"), ensure_ascii=False, indent=2)
        notify(f"🚦 hds gate 进度(到期{end})\n"
               f"① 平仓 {trades}/{g['min_trades_total']} {'✅' if c1 else '⏳'}\n"
               f"② hds {hds_ret:+.1f}% vs QQQ {qqq_ret:+.1f}% {'✅领先' if c2 else '❌落后'}\n"
               f"③ QQQ窗口最大回撤 {qdd:.1f}%/{g['qqq_dd_required_pct']}% {'✅' if c3 else '未经历'}\n"
               "（交易信号系统·hds gate）")
    else:
        print(f"[hds-gate] 进度: 平仓{trades}/{g['min_trades_total']} hds{hds_ret:+.1f}% QQQ{qqq_ret:+.1f}% dd{qdd:.1f}% (静默)")


if __name__ == "__main__":
    run()
