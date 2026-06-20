"""周一飞书提醒:IBKR paper 账户设置。自终止——data/ibkr-setup-done 存在则不再提醒。"""
import os, runpy

if os.path.exists("data/ibkr-setup-done"):
    print("[reminder] IBKR 已设置,跳过"); raise SystemExit

msg = "\n".join([
    "🔔 周一待办:IBKR 模拟盘 (paper) 设置",
    "你说周一弄——开始啦(你已有 IBKR 账户,paper 免费附带):",
    "1. 下 IB Gateway(轻量版)→ 用 paper 凭证登录 → 设置里开 API,端口 7497",
    "2. 装 IBC(自动重登,省得每天手动)",
    "3. 跟 Claude 说「网关起来了」,他用 ib_insync 连上跑通下单+对账",
    "(网络不好挂代理。弄完跟 Claude 说一声,这条提醒自动停)",
    "（交易信号系统）",
])
os.environ["NOTIFY_MESSAGE"] = msg
if os.environ.get("NOTIFY_WEBHOOK"):
    runpy.run_path("scripts/notify-webhook.py", run_name="__main__")
else:
    print(msg + "\n[reminder] 无 NOTIFY_WEBHOOK,仅打印")
