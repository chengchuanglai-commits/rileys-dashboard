"""可交易性过滤器(观察模式)——暴雷点#4点差/#1部分,2026-07-19装。
每天检查当日DeepSeek信号:ADV<$5M 或 在不可交易名单(OTC等,check-borrow维护)→ 标记"真钱会剔除"。
⚠️ 只记录不拦截:paper模拟照常吃全部信号(gate期间不改行为);Phase2真钱时本脚本转正为硬过滤。
积累数据回答:真钱过滤会损失多少信号/多少利润。日志: data/tradability-log.json
用法: python3 scripts/tradability-filter.py  (run.sh review 每日调用)"""
import json, os
from datetime import date

DS_DIR = "dashboard/trading-signals-history/deepseek"
LOG = "data/tradability-log.json"
UNTRADABLE = "data/borrow-untradable.json"   # check-borrow 的 notfound 落这里
MIN_ADV = 5_000_000


def adv20(tk):
    import yfinance as yf
    try:
        h = yf.Ticker(tk).history(period="1mo")
        if h.empty: return None
        return float((h["Close"] * h["Volume"]).tail(20).mean())
    except Exception:
        return None


def main():
    today = date.today().isoformat()
    f = os.path.join(DS_DIR, f"{today}-deepseek.json")
    if not os.path.exists(f):
        # 找最近一个信号文件(周末/休市日复盘时看最新交易日的)
        files = sorted(x for x in os.listdir(DS_DIR) if x.endswith("-deepseek.json"))
        if not files: print("[tradability] 无信号文件"); return
        f = os.path.join(DS_DIR, files[-1])
    day = os.path.basename(f).replace("-deepseek.json", "")
    try: log = json.load(open(LOG))
    except Exception: log = {}
    if day in log:
        print(f"[tradability] {day} 已记录,跳过"); return
    try: untradable = set(json.load(open(UNTRADABLE)))
    except Exception: untradable = set()
    sigs = json.load(open(f)).get("signals", [])
    flags = []
    for s in sigs:
        tk, ac = s.get("ticker"), s.get("action")
        if ac not in ("BUY", "SELL"): continue
        why = []
        if tk in untradable: why.append("无合约/OTC")
        a = adv20(tk)
        if a is not None and a < MIN_ADV: why.append(f"ADV${a/1e6:.1f}M<5M")
        if why: flags.append({"ticker": tk, "action": ac, "why": ",".join(why)})
    log[day] = {"total": len(sigs), "flagged": flags}
    json.dump(log, open(LOG, "w"), ensure_ascii=False, indent=1)
    n_flag = len(flags)
    print(f"[tradability] {day}: 信号{len(sigs)}个,真钱将剔除{n_flag}个: "
          f"{[x['ticker']+'('+x['why']+')' for x in flags] if flags else '无'}")


if __name__ == "__main__":
    main()
