"""hds空头票借券体检:查SELL票池的可借股数(tick 236),分类可借/紧张/无数据→飞书。
背景:paper未计借券费/可得性(2026-07-18风险分析:费率不致命,availability才是真风险)。
用法:盘前/盘中跑(周末数据冻结查不到)。python3 scripts/check-borrow.py
Phase2真钱试运行时升级为逐日过滤器。"""
import json, os, sys, random

# 仓库根进path:ibkr.client内部import scripts.ibkr.config,而`python3 scripts/xx.py`只把scripts/放进path(7/21实炸的坑)
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (_ROOT, os.path.join(_ROOT, "scripts")):
    if _p not in sys.path: sys.path.insert(0, _p)


def notify(msg):
    print(msg)
    if os.environ.get("NOTIFY_WEBHOOK"):
        os.environ["NOTIFY_MESSAGE"] = msg
        import runpy
        try: runpy.run_path("scripts/notify-webhook.py", run_name="__main__")
        except Exception: pass


def main():
    d = json.load(open("data/portfolio_hds.json"))
    tks = sorted({p["ticker"] for p in d["closed_positions"] + d["open_positions"] if p["action"] == "SELL"})
    from ibkr.client import connect
    from ib_insync import Stock
    ib, _ = connect(client_id=random.randint(200, 899), retries=2, retry_wait=5)
    if not ib:
        print("[borrow] 连不上IBKR,跳过"); sys.exit(1)   # 非0退出→run.sh一次性flag不落,明天重试
    ib.reqMarketDataType(3)   # 接受延迟行情(paper无实时订阅,tick236走延迟也给;7/22实炸10089的解)
    easy, tight, nodata, notfound = [], [], [], []
    for tk in tks:
        try:
            c = Stock(tk, "SMART", "USD")
            q = ib.qualifyContracts(c)
            if not q:
                notfound.append(tk); continue
            t = ib.reqMktData(c, "236", "", False)
            ib.sleep(2)
            ss = t.shortableShares
            ib.cancelMktData(c)
            if ss is None or ss != ss:
                nodata.append(tk)
            elif ss > 100000:
                easy.append((tk, ss))
            else:
                tight.append((tk, ss))
        except Exception:
            nodata.append(tk)
    ib.disconnect()
    if len(nodata) + len(notfound) == len(tks):
        print("[borrow] 全部无数据(数据源冻结?),明天重试"); sys.exit(1)
    # 无合约名单落盘 → tradability-filter 每日引用
    json.dump(sorted(notfound), open("data/borrow-untradable.json", "w"))
    n = len(tks)
    lines = [f"🔎 hds空头票借券体检({n}只)",
             f"✅ 可借充足(>10万股): {len(easy)} — {','.join(t for t,_ in easy) or '无'}",
             f"⚠️ 可借紧张: {len(tight)} — {','.join(f'{t}({s:,.0f})' for t,s in tight) or '无'}",
             f"❓ 无数据: {len(nodata)} — {','.join(nodata) or '无'}",
             f"🚫 无合约(OTC等,真钱做不了): {len(notfound)} — {','.join(notfound) or '无'}",
             "→ 真钱试运行需过滤🚫,⚠️逐票看费率。(交易信号系统·借券体检)"]
    notify("\n".join(lines))


if __name__ == "__main__":
    main()
