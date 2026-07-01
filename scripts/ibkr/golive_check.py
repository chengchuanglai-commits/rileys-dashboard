"""上真钱 5 闸门自动体检 (go-live readiness)。每周一 launchd 本地跑→飞书报告几个绿、还差啥。

闸门:
  ① 账户入金 >2500 CAD(或USD)   —— 手动标记(做完 touch data/golive/funded)
  ② IBKR Pro→Lite($0佣金)       —— 手动标记(做完 touch data/golive/lite)
  ③ paper 连续干净 N 交易日       —— 自动:扫 exec-log,自 clean-since 起 gate_ok且无error且断路器normal
  ④ 小数股 API 端到端确认         —— 自动:data/fractional-done 存在(由小数股探针自动写)
  ⑤ 前向样本够 + 某腿够毕业线     —— 自动:forward-track行数 + 各腿最大交易数

①② 是钱/账户层面只能人来做的事,脚本只记状态;③④⑤ 全自动。
全绿才考虑第一笔真钱(且先上指数小额)。任一闸门红=别上。
"""
import os, json, glob, time

GDIR = "data/golive"
CLEAN_NEED = 12      # ③ 需要的干净交易日(~2.5周)
FWD_NEED = 12        # ⑤ 前向账本需要的行数(交易日)
TRADES_NEED = 60     # ⑤ 某条腿毕业需要的最少交易数


def _flag(name):
    return os.path.exists(os.path.join(GDIR, name))


def gate_funded():
    return _flag("funded"), "账户入金 >2500 CAD(或直接USD)"


def gate_lite():
    return _flag("lite"), "IBKR Pro→Lite($0佣金)"


def gate_clean():
    since = "2026-06-27"
    p = os.path.join(GDIR, "clean-since")
    if os.path.exists(p):
        try: since = open(p).read().strip()[:10]
        except Exception: pass
    n = 0
    for f in sorted(glob.glob("data/exec-log/20*-*.json")):
        date = os.path.basename(f)[:10]
        if date < since:
            continue
        try:
            l = json.load(open(f))
            clean = (l.get("gate_ok") and l.get("breaker", "normal") == "normal"
                     and not any(x.get("error") for x in l.get("placed", [])))
            if clean:
                n += 1
        except Exception:
            pass
    return n >= CLEAN_NEED, f"paper 连续干净 {n}/{CLEAN_NEED} 交易日(自{since})"


def gate_fractional():
    return os.path.exists("data/fractional-done"), "小数股 API 端到端确认"


def gate_sample():
    rows = 0
    try:
        rows = len(json.load(open("data/forward-track.json")).get("rows", []))
    except Exception:
        pass
    best = 0
    for f in glob.glob("data/portfolio_*.json"):
        try:
            best = max(best, json.load(open(f)).get("stats", {}).get("total_trades", 0))
        except Exception:
            pass
    ok = rows >= FWD_NEED and best >= TRADES_NEED
    return ok, f"前向账本 {rows}/{FWD_NEED}日 · 最多腿 {best}/{TRADES_NEED}笔"


def run():
    gates = [gate_funded(), gate_lite(), gate_clean(), gate_fractional(), gate_sample()]
    green = sum(1 for ok, _ in gates if ok)
    lines = [f"🚦 上真钱体检 {time.strftime('%m-%d')}: {green}/5 绿"]
    for ok, desc in gates:
        lines.append(f"{'✅' if ok else '⬜'} {desc}")
    if green == 5:
        lines.append("🟢 5闸全绿!可考虑第一笔真钱(先上指数小额)。跟 Claude 确认后执行。")
    else:
        manual = [d for ok, d in (gates[0], gates[1]) if not ok]
        tip = "①②做完手动 touch data/golive/funded 或 lite;③④⑤系统自己会变绿。"
        lines.append(f"还差 {5-green} 个。{tip}")
    msg = "\n".join(lines) + "\n（交易信号系统·上真钱体检）"
    print(msg)
    if os.environ.get("NOTIFY_WEBHOOK"):
        from scripts.ibkr.notify import send
        try: send(msg)
        except Exception: pass


if __name__ == "__main__":
    run()
