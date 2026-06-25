"""长线潜力选股扫描 —— AI 主动扫全市场,筛"基本面健康+成长+护城河+不贵"的长线候选,排榜给 Riley。
为"20%长线持股"自动选股(Riley定方向/决策,AI做筛选+盯财报)。
标准: 收入持续增长 + 现金流真实 + 高毛利护城河 + 低负债 + 高ROE + 估值不离谱。
用法: FMP_API_KEY=... python scripts/longterm-screener.py [N]   (N=扫多少只,默认全universe)
"""
import os, sys, json, urllib.request
from concurrent.futures import ThreadPoolExecutor

FMP=os.environ.get("FMP_API_KEY","").strip()
def get(path):
    url=f"https://financialmodelingprep.com/stable/{path}{'&' if '?' in path else '?'}apikey={FMP}"
    try:
        with urllib.request.urlopen(url,timeout=20) as r: return json.loads(r.read())
    except Exception: return None
def num(x,d=0):
    try: return float(x)
    except: return d

def score(sym):
    """对一只票评长线潜力分(0-100)+体检数据。不合格返回None。"""
    inc=get(f"income-statement?symbol={sym}&period=annual&limit=4")
    if not inc or not isinstance(inc,list) or len(inc)<3: return None
    inc=sorted(inc,key=lambda x:x.get("date",""))
    rat=get(f"ratios-ttm?symbol={sym}"); rat=rat[0] if isinstance(rat,list) and rat else {}
    km=get(f"key-metrics-ttm?symbol={sym}"); km=km[0] if isinstance(km,list) and km else {}
    cf=get(f"cash-flow-statement?symbol={sym}&period=annual&limit=1"); cf0=cf[0] if isinstance(cf,list) and cf else {}
    bs=get(f"balance-sheet-statement?symbol={sym}&period=annual&limit=1"); bs0=bs[0] if isinstance(bs,list) and bs else {}

    revs=[num(x.get("revenue")) for x in inc]
    if revs[0]<=0: return None
    rev_cagr=((revs[-1]/revs[0])**(1/(len(revs)-1))-1)*100
    ni=num(inc[-1].get("netIncome"))
    ocf=num(cf0.get("operatingCashFlow") or cf0.get("netCashProvidedByOperatingActivities"))
    gm=(num(inc[-1].get("grossProfit"))/revs[-1]*100) if revs[-1]>0 else 0
    debt=num(bs0.get("totalDebt")); cashb=num(bs0.get("cashAndCashEquivalents"))
    roe=num(km.get("returnOnEquityTTM") or rat.get("returnOnEquityTTM"))*100
    pe=num(rat.get("priceToEarningsRatioTTM"))
    ocf_q=(ocf/ni) if ni>0 else (1 if ocf>0 else 0)
    cover=(cashb+ocf)/debt if debt>0 else 99
    # 钳制异常值(脏数据防护)
    rev_cagr=max(min(rev_cagr,80),-50)            # 营收增速封顶80%(防一次性暴涨)
    roe=max(min(roe,150),-50)                     # ROE 钳到[-50,150],防-5642%脏数据
    ocf_q=max(min(ocf_q,3),0)                     # 现金质钳到[0,3],防AFRM式15.21

    # 硬性排除(红线)
    if ocf<0: return None                        # 烧钱
    if rev_cagr<0: return None                    # 收入下滑
    if ni<=0 and ocf<revs[-1]*0.05: return None   # 既不赚钱现金流也弱
    if pe>120 or pe<0: return None                # 估值疯了(PE>120)或亏损,长线不碰

    # 评分(各项0-1加权)
    s_grow=min(max(rev_cagr/30,0),1)              # 成长:30%年化=满分
    s_ocf=min(max(ocf_q,0),1.2)/1.2               # 现金流含金量
    s_moat=min(max(gm/60,0),1)                    # 护城河:60%毛利=满分
    s_safe=min(cover/3,1)                          # 安全:覆盖3x=满分
    s_roe=min(max(roe/25,0),1)                    # 效率:25%ROE=满分
    s_val=1-min(max((pe-20)/40,0),1) if pe>0 else 0.3  # 估值:PE20以下满分,60以上0(收紧)
    total=(0.25*s_grow+0.15*s_ocf+0.18*s_moat+0.12*s_safe+0.15*s_roe+0.15*s_val)*100  # 估值权重10→15
    return {"sym":sym,"score":round(total,1),"rev_cagr":round(rev_cagr),"gm":round(gm),
            "ocf_q":round(ocf_q,2),"roe":round(roe),"pe":round(pe),"cover":round(cover,1),
            "ni_pos":ni>0}

def main():
    if not FMP: print("需要 FMP_API_KEY"); return
    u=json.load(open("data/fmp-cache/universe.json"))
    syms=sorted(set(u["current"]))   # 只扫现存票(长线投资不会买退市票)
    if len(sys.argv)>1: syms=syms[:int(sys.argv[1])]
    print(f"扫描 {len(syms)} 只票的长线潜力...")
    results=[]
    done=[0]
    def one(s):
        r=score(s); done[0]+=1
        if done[0]%50==0: print(f"  …{done[0]}/{len(syms)}")
        if r: results.append(r)
    with ThreadPoolExecutor(max_workers=6) as ex: list(ex.map(one,syms))
    results.sort(key=lambda x:-x["score"])
    json.dump(results,open("data/longterm-candidates.json","w"),ensure_ascii=False,indent=2)
    print(f"\n{'='*70}\n  长线潜力榜 TOP 25 (基本面健康+成长+护城河+不贵)\n{'='*70}")
    print(f"  {'代码':<7}{'分':>5}{'营收增速':>8}{'毛利':>6}{'现金质':>7}{'ROE':>6}{'PE':>6}{'债务覆盖':>8}")
    for r in results[:25]:
        print(f"  {r['sym']:<7}{r['score']:>5}{r['rev_cagr']:>+7}%{r['gm']:>5}%{r['ocf_q']:>7}{r['roe']:>5}%{r['pe']:>6}{r['cover']:>7}x")
    print(f"\n  共 {len(results)} 只通过初筛。完整榜 → data/longterm-candidates.json")
    print(f"  ⚠️ 这是基本面初筛榜,不是买入建议。Riley 从中挑你理解的生意 + 判断估值时机。")

if __name__=="__main__":
    main()
