"""
真钱指数核心台账(QQQ+QQQM 双标的) —— 读 data/qqq_realmoney.json 的 tranches,
拉各标的实时价 + USDCAD,算成本/现值/浮盈亏(美元为主,加元换算)。
写回 json.stats + dashboard/qqq-realmoney.js + 打印。
2026-08-05 升级双标的:QQQ托管首笔 QQQM 自动买入落地(API禁碎股→QQQM整股方案)。
tranche 可带 sym 字段(缺省=QQQ);托管自动买入由本脚本从 data/qqq-dca-state.json
按 date+sym 幂等同步,人工买入仍手动追加一条再跑。
"""
import json
from datetime import datetime
import yfinance as yf

PATH = "data/qqq_realmoney.json"
DCA_STATE = "data/qqq-dca-state.json"


def last_price(ticker, fallback=None):
    try:
        h = yf.Ticker(ticker).history(period="5d")
        if len(h):
            return round(float(h["Close"].iloc[-1]), 4)
    except Exception:
        pass
    return fallback


d = json.load(open(PATH))
tr = d.setdefault("tranches", [])
for t in tr:
    t.setdefault("sym", "QQQ")

# 同步托管自动买入(qqq_dca_exec 记账在 dca-state;date+sym 去重幂等)
try:
    dca = json.load(open(DCA_STATE))
    seen = {(t["date"], t["sym"]) for t in tr}
    for b in dca.get("buys", []):
        if (b["date"], b["sym"]) not in seen:
            tr.append({"date": b["date"], "sym": b["sym"], "shares": b["shares"],
                       "price_usd": round(b["usd"] / b["shares"], 2),
                       "cost_usd": round(b["usd"], 2),
                       "note": f"托管自动买入({b.get('reason','')})"})
            print(f"[台账] 同步托管买入: {b['sym']}×{b['shares']} {b['date']}")
except Exception:
    pass

syms = sorted({t["sym"] for t in tr})
px = {s: last_price(s) for s in syms}
fx = last_price("CAD=X", fallback=1.36)   # USDCAD

per, cost_usd, value_usd = {}, 0.0, 0.0
for s in syms:
    ts = [t for t in tr if t["sym"] == s]
    sh = sum(t["shares"] for t in ts)
    c = sum(t.get("cost_usd", t["shares"] * t.get("price_usd", 0)) for t in ts)
    p = px[s] or (c / sh if sh else 0)
    v = sh * p
    per[s] = {"shares": round(sh, 4), "avg_price_usd": round(c / sh, 2) if sh else 0,
              "cost_usd": round(c, 2), "now_usd": p, "value_usd": round(v, 2),
              "pnl_usd": round(v - c, 2)}
    cost_usd += c
    value_usd += v

pnl_usd = round(value_usd - cost_usd, 2)
d["stats"] = {
    "per_symbol": per,
    "cost_usd": round(cost_usd, 2),
    "value_usd": round(value_usd, 2),
    "pnl_usd": pnl_usd,
    "pnl_pct": round(pnl_usd / cost_usd * 100, 2) if cost_usd else 0,
    "usdcad": round(fx, 4),
    "cost_cad_approx": round(cost_usd * fx, 2),
    "value_cad_approx": round(value_usd * fx, 2),
    "pnl_cad_approx": round(pnl_usd * fx, 2),
    "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
}

json.dump(d, open(PATH, "w"), ensure_ascii=False, indent=2)
with open("dashboard/qqq-realmoney.js", "w", encoding="utf-8") as f:
    f.write("// 真钱指数核心台账(QQQ+QQQM)\n")
    f.write(f"window.QQQ_REALMONEY = {json.dumps(d, ensure_ascii=False, indent=2)};\n")

s = d["stats"]
sign = "🟢" if s["pnl_usd"] >= 0 else "🔴"
print("=" * 52)
print("  💰 真钱指数核心台账 (QQQ+QQQM)")
print("=" * 52)
for sym, q in s["per_symbol"].items():
    print(f"  {sym:5} {q['shares']}股 均价${q['avg_price_usd']} 现价${q['now_usd']} 浮盈亏${q['pnl_usd']:+}")
print(f"  成本合计    ${s['cost_usd']}  (≈{s['cost_cad_approx']} CAD @ {s['usdcad']})")
print(f"  现值合计    ${s['value_usd']}  (≈{s['value_cad_approx']} CAD)")
print(f"  {sign} 浮盈亏   ${s['pnl_usd']:+} ({s['pnl_pct']:+}%)  ≈ {s['pnl_cad_approx']:+} CAD")
print("=" * 52)
