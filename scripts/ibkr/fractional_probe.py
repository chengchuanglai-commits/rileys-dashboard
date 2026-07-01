"""小数股权限自动探测 (tripwire,替代原来的死提醒)。

每周一由 launchd 本地跑(必须本地——GitHub Action连不到本机Gateway):
连 Gateway 下一笔 0.5股 小数限价单(限价$1,远低于市价绝不会成交)+立即撤,看是否报 10243/10244。
- 仍报错(小数股被挡) → 保持安静(不再每周刷屏,只在状态变化时通知)。
- 不报错(小数股可用) → 写 data/fractional-done(自终止)+飞书✅通知,提示可把 config.FRACTIONAL 切 True。
- Gateway 离线 → 跳过。

注:探的是当前 Gateway 连的账户。现在是 paper(DUQ627583),IBKR模拟盘对小数股API支持受限,大概率一直报错。
真正有意义的是 Riley 把 Gateway 切到真账户(U20220368,已实测手动小数股可用)时,这探针会自动测出
"真账户API小数单是否通"=真钱启动前的最后一关端到端确认,通了立刻飞书叫人。
"""
import os, time
from scripts.ibkr.client import connect, health
from scripts.ibkr.notify import send
from ib_insync import Stock, LimitOrder

DONE = "data/fractional-done"


def run():
    if os.path.exists(DONE):
        print("[probe] 已标记小数股可用,跳过"); return
    ib, _ = connect(client_id=28)
    if not ib:
        print("[probe] Gateway 离线,跳过"); return
    h = health(ib)
    errs = []
    ib.errorEvent += lambda reqId, code, msg, c=None: errs.append(code)
    ct = Stock("F", "SMART", "USD"); ib.qualifyContracts(ct)
    o = LimitOrder("BUY", 0.5, 1.00); o.tif = "DAY"   # 0.5股,限价$1不会成交
    tr = ib.placeOrder(ct, o); ib.sleep(3)
    blocked = any(c in (10243, 10244) for c in errs)
    try: ib.cancelOrder(o); ib.sleep(1)
    except Exception: pass
    acct = h["account"]; ib.disconnect()

    if blocked:
        print(f"[probe] {acct} 小数股仍被挡(10243/10244),保持安静")
        return
    # 不报错 = 小数股可用!
    with open(DONE, "w") as f:
        f.write(f"fractional confirmed on {acct} at {time.strftime('%F %T')}\n")
    print(f"[probe] ✅ {acct} 小数股可用,已写 {DONE}")
    if os.environ.get("NOTIFY_WEBHOOK"):
        send("\n".join([
            f"✅ 小数股已生效!账户 {acct} 下小数单不再报 10243/10244。",
            "下一步:跟 Claude 说一声,把 config.FRACTIONAL 切 True,",
            "$2000 就能按 frac10 买全所有仓位(不再被高价票挡)。",
            "（交易信号系统·小数股探针自动检测）"]))


if __name__ == "__main__":
    run()
