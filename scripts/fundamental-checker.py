"""财报体检工具 —— 输入股票代码,自动从FMP拉数据,输出6问+5指标+红线警告。
用于"20%长线持股"的基本面初筛:系统先筛,你再深读。
用法: FMP_API_KEY=... python scripts/fundamental-checker.py AAPL MSFT NVDA
"""
import os, sys, json, urllib.request

FMP=os.environ.get("FMP_API_KEY","").strip()

def get(path):
    url=f"https://financialmodelingprep.com/stable/{path}{'&' if '?' in path else '?'}apikey={FMP}"
    try:
        with urllib.request.urlopen(url,timeout=20) as r: return json.loads(r.read())
    except Exception as e:
        print(f"  [warn] {path[:40]}: {str(e)[:50]}"); return None

def num(x,d=0):
    try: return float(x)
    except: return d

def check(sym):
    print(f"\n{'='*58}\n  📋 {sym} 财报体检\n{'='*58}")
    # 拉数据:利润表(年,近4年)、比率ttm、关键指标ttm、现金流(年)
    inc=get(f"income-statement?symbol={sym}&period=annual&limit=4")
    cf=get(f"cash-flow-statement?symbol={sym}&period=annual&limit=2")
    rat=get(f"ratios-ttm?symbol={sym}")
    km=get(f"key-metrics-ttm?symbol={sym}")
    bs=get(f"balance-sheet-statement?symbol={sym}&period=annual&limit=1")
    if not inc or not isinstance(inc,list) or len(inc)<2:
        print("  ❌ 拉不到财报数据(代码错/非美股/FMP档位限制)"); return
    inc=sorted(inc,key=lambda x:x.get("date",""))  # 旧→新
    rat=rat[0] if isinstance(rat,list) and rat else {}
    km=km[0] if isinstance(km,list) and km else {}
    cf0=cf[0] if isinstance(cf,list) and cf else {}
    bs0=bs[0] if isinstance(bs,list) and bs else {}

    flags=[]  # 红线
    # ===== 6问 =====
    print("\n  【6个核心问题】")
    # 1 收入涨吗
    revs=[num(x.get("revenue")) for x in inc]
    rev_grow = revs[-1]>revs[0] if len(revs)>=2 else None
    rev_cagr = ((revs[-1]/revs[0])**(1/(len(revs)-1))-1)*100 if (len(revs)>=2 and revs[0]>0) else 0
    print(f"  1.收入趋势: {'/'.join(f'{r/1e9:.1f}B' for r in revs)} → 年化{rev_cagr:+.0f}% {'✅涨' if rev_grow else '⚠️降'}")
    if not rev_grow: flags.append("收入在下滑")
    # 2 真赚钱吗(净利+经营现金流)
    ni=num(inc[-1].get("netIncome")); ocf=num(cf0.get("operatingCashFlow") or cf0.get("netCashProvidedByOperatingActivities"))
    print(f"  2.赚钱吗: 净利润{ni/1e9:+.1f}B · 经营现金流{ocf/1e9:+.1f}B {'✅都正' if ni>0 and ocf>0 else '⚠️有负'}")
    if ocf<0: flags.append("经营现金流为负(烧钱)")
    # 3 利润是真钱吗(OCF vs 净利)
    if ni>0:
        ratio=ocf/ni
        print(f"  3.利润含金量: 经营现金流/净利润 = {ratio:.2f} {'✅真钱(≥0.8)' if ratio>=0.8 else '⚠️利润可能注水(<0.8)'}")
        if ratio<0.7: flags.append("经营现金流远低于净利润(利润含水分)")
    else: print(f"  3.利润含金量: 净利润为负,跳过")
    # 4 负债压垮吗
    debt=num(bs0.get("totalDebt")); cashb=num(bs0.get("cashAndCashEquivalents"))
    netdebt=debt-cashb
    cover = (cashb+ocf)/debt if debt>0 else 99
    print(f"  4.负债: 总债务{debt/1e9:.1f}B · 现金{cashb/1e9:.1f}B · 净负债{netdebt/1e9:+.1f}B (现金+OCF覆盖债务{cover:.1f}x) {'✅稳' if cover>=1 or debt==0 else '⚠️偏高'}")
    if debt>0 and cover<0.5 and ocf<debt*0.2: flags.append("高负债+弱现金流(暴雷风险)")
    # 5 对股东好吗(回购/稀释)
    sh=[num(x.get("weightedAverageShsOut")) for x in inc]
    dilute = sh[-1]>sh[0]*1.05 if len(sh)>=2 and sh[0]>0 else False
    print(f"  5.股本: {'/'.join(f'{s/1e6:.0f}M' for s in sh)} {'⚠️持续增发稀释' if dilute else '✅未明显稀释/回购'}")
    if dilute and ocf<0: flags.append("增发稀释+烧钱(融资续命模式)")
    # 6 护城河(毛利率)
    gm=num(rat.get("grossProfitMarginTTM"),0)*100 if rat.get("grossProfitMarginTTM") else (num(inc[-1].get("grossProfit"))/revs[-1]*100 if revs[-1]>0 else 0)
    print(f"  6.护城河: 毛利率 {gm:.0f}% {'✅高(>40%有定价权)' if gm>40 else ('🟡中' if gm>20 else '⚠️低(薄利)')}")

    # ===== 5指标速览 =====
    roe=num(km.get("returnOnEquityTTM") or rat.get("returnOnEquityTTM"))*100
    pe=num(rat.get("priceToEarningsRatioTTM"))
    print(f"\n  【关键指标】营收增速{rev_cagr:+.0f}% · 毛利率{gm:.0f}% · 经营现金流{ocf/1e9:+.1f}B · 净负债{netdebt/1e9:+.1f}B · ROE{roe:.0f}% · PE{pe:.0f}")

    # ===== 红线 =====
    print(f"\n  【红线检查】")
    if flags:
        for f in flags: print(f"  🔴 {f}")
        print(f"  → {len(flags)}条红线,长线持有需谨慎/排除")
    else:
        print(f"  ✅ 无红线触发,基本面初筛通过(仍需你深读+理解生意+估值判断)")
    print(f"\n  ⚠️ 这只是初筛,不是买入建议。还要:①你理解这门生意 ②估值合不合理 ③写出'买它因为__,卖它如果__'")

def main():
    syms=sys.argv[1:]
    if not syms:
        print("用法: python scripts/fundamental-checker.py AAPL MSFT NVDA"); return
    if not FMP:
        print("需要 FMP_API_KEY"); return
    for s in syms: check(s.upper())

if __name__=="__main__":
    main()
