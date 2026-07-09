"""
真钱 QQQ 指数核心台账 —— 读 data/qqq_realmoney.json 的 tranches,
拉 QQQ 实时价 + USDCAD,算成本基准/累计股数/现值/浮盈亏(美元为主,加元换算)。
写回 json.stats + dashboard/qqq-realmoney.js + 打印。加仓只需往 tranches 追加一条再跑。
"""
import json
from datetime import datetime
import yfinance as yf

PATH = "data/qqq_realmoney.json"


def last_price(ticker, fallback=None):
    try:
        h = yf.Ticker(ticker).history(period="5d")
        if len(h):
            return round(float(h["Close"].iloc[-1]), 4)
    except Exception:
        pass
    return fallback


d = json.load(open(PATH))
tr = d.get("tranches", [])
shares = sum(t["shares"] for t in tr)
cost_usd = sum(t.get("cost_usd", t["shares"] * t.get("price_usd", 0)) for t in tr)
avg = cost_usd / shares if shares else 0

qqq = last_price("QQQ", fallback=avg)
fx = last_price("CAD=X", fallback=1.36)   # USDCAD

value_usd = round(shares * qqq, 2)
pnl_usd = round(value_usd - cost_usd, 2)
pnl_pct = round(pnl_usd / cost_usd * 100, 2) if cost_usd else 0

d["stats"] = {
    "shares": round(shares, 4),
    "avg_price_usd": round(avg, 2),
    "cost_usd": round(cost_usd, 2),
    "qqq_now_usd": qqq,
    "value_usd": value_usd,
    "pnl_usd": pnl_usd,
    "pnl_pct": pnl_pct,
    "usdcad": round(fx, 4),
    "cost_cad_approx": round(cost_usd * fx, 2),
    "value_cad_approx": round(value_usd * fx, 2),
    "pnl_cad_approx": round(pnl_usd * fx, 2),
    "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
}

json.dump(d, open(PATH, "w"), ensure_ascii=False, indent=2)
with open("dashboard/qqq-realmoney.js", "w", encoding="utf-8") as f:
    f.write("// 真钱 QQQ 指数核心台账\n")
    f.write(f"window.QQQ_REALMONEY = {json.dumps(d, ensure_ascii=False, indent=2)};\n")

s = d["stats"]
sign = "🟢" if s["pnl_usd"] >= 0 else "🔴"
print("=" * 52)
print("  💰 真钱 QQQ 指数核心台账")
print("=" * 52)
print(f"  持仓        {s['shares']} 股  均价 ${s['avg_price_usd']}")
print(f"  成本        ${s['cost_usd']}  (≈{s['cost_cad_approx']} CAD @ {s['usdcad']})")
print(f"  QQQ 现价    ${s['qqq_now_usd']}")
print(f"  现值        ${s['value_usd']}  (≈{s['value_cad_approx']} CAD)")
print(f"  {sign} 浮盈亏   ${s['pnl_usd']:+} ({s['pnl_pct']:+}%)  ≈ {s['pnl_cad_approx']:+} CAD")
print("=" * 52)
