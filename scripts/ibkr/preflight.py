"""开盘前自检:8项,全过放行,任一失败中止+报警(带原因+建议)。"""
import os, json, time
from scripts.ibkr.client import connect, health
from scripts.ibkr.config import NOTIONAL, HARD_REDLINE
from scripts.ibkr.notify import send

def run():
    fails = []
    ib, port = connect(client_id=20)
    if not ib:
        send("⚠️ IBKR自检失败:网关连不上\n建议:检查 IB Gateway 是否登录、API端口4002是否开\n（交易信号系统）")
        return False
    h = health(ib)
    if not h["is_paper"]:
        fails.append(f"账户 {h['account']} 非paper(DU开头)→ 防误连实盘,中止")
    if h["nav"] <= 0:
        fails.append("净值读不到/为0 → 账户连接异常")
    # 区分止损单(STP/STP LMT,正常常驻保护) vs 非止损的真遗留挂单
    ib.reqAllOpenOrders(); ib.sleep(1)
    nonstop = [t for t in ib.openTrades() if t.order.orderType not in ("STP", "STP LMT")]
    stop_cnt = len(ib.openTrades()) - len(nonstop)
    # 三线目标新鲜度:检查 master-allocation.json(实际驱动下单的文件,由review批次每日重算)。
    # 旧的 allocation.json 是从不触发的fallback、且由独立的Cloudflare/GitHub管道更新常掉链子→曾反复误报,不再检查它。
    try:
        m = json.load(open("data/master-allocation.json"))
        gen = m.get("date", "")
        if gen[:10] != time.strftime("%Y-%m-%d"):
            fails.append(f"master-allocation.json 不是今天({gen}) → 三线目标没刷新(查review批次的master-allocator)")
        # 回撤红线
        nav, peak = h["nav"], max(h["nav"], NOTIONAL)
        if peak > 0 and (peak - nav) / peak >= HARD_REDLINE:
            fails.append(f"已破回撤红线 {HARD_REDLINE*100:.0f}%")
    except Exception as e:
        fails.append(f"读 master-allocation.json 失败: {e}")
    # 只有"非止损"的遗留挂单才警告(止损单是正常常驻保护,不算遗留)
    if nonstop:
        syms = ",".join(t.contract.symbol for t in nonstop[:5])
        fails.append(f"有 {len(nonstop)} 笔非止损遗留挂单({syms}) → 建议先 cancel_all")
    ib.disconnect()

    if fails:
        send("⚠️ IBKR开盘前自检失败:\n- " + "\n- ".join(fails) +
             "\n今夜不下单。请处理后重跑。\n（交易信号系统）")
        return False
    send(f"✅ IBKR自检通过(账户{h['account']} 净值${h['nav']:.0f} · {stop_cnt}个止损单守护),今夜可交易\n（交易信号系统）")
    return True

if __name__ == "__main__":
    import sys
    sys.exit(0 if run() else 1)
