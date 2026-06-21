"""持续提醒:开通 IBKR 小数股权限 (Trade in Fractions)。
自终止——data/fractional-done 存在则停。否则每次工作流跑就推飞书(建议接每周一次的cron)。
这是 $2000 分散方案的地基:权限没开→只能整数股→$2000买不全10只高价票。
"""
import os, runpy

if os.path.exists("data/fractional-done"):
    print("[reminder] 小数股权限已开,跳过"); raise SystemExit

msg = "\n".join([
    "🔔 待办提醒:IBKR 小数股权限(Trade in Fractions)",
    "这是 $2000 分散方案的地基——没开只能整数股,$2000 买不全高价票(IESC/STRL等)。",
    "实测确认:paper 账户现在下小数股报错 10243/10244 = 权限未开。",
    "卡点:实盘入金墙挡住 Client Portal。解法(按优先级):",
    "  1. 取消那些失败的 pending 存款申请(很可能解开墙)",
    "  2. 不行→ IBKR 客服开 ticket(Support→Message Center),让后台清卡住的待办",
    "  3. 进 Portal 后:Settings→Trading Permissions→Stocks→勾 Trade in Fractions",
    "开好后跟 Claude 说一声,他重测 cashQty 小数股→通过就把系统从整数股切小数股(只是开关)。",
    "(系统已用整数股先跑通 paper,不阻塞;但真钱前这个必须解决)",
    "（交易信号系统）",
])
os.environ["NOTIFY_MESSAGE"] = msg
if os.environ.get("NOTIFY_WEBHOOK"):
    runpy.run_path("scripts/notify-webhook.py", run_name="__main__")
else:
    print(msg + "\n[reminder] 无 NOTIFY_WEBHOOK,仅打印")
