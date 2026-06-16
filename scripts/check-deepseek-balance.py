"""DeepSeek 账户余额监控 —— 不同于 Anthropic(无余额API)，DeepSeek 有 /user/balance 接口可直接查。
余额用尽或低于阈值时推飞书提醒(NOTIFY_WEBHOOK)。完全围栏(退出0)，绝不拖垮主流程。

环境变量：DEEPSEEK_API_KEY(必需)、NOTIFY_WEBHOOK(飞书,可选)、DEEPSEEK_ALERT_CNY(阈值,默认20)。
"""
import os, sys, json, urllib.request

ALERT_CNY = float(os.environ.get("DEEPSEEK_ALERT_CNY", "20"))


def feishu(msg):
    wh = os.environ.get("NOTIFY_WEBHOOK", "").strip()
    if not wh:
        print("[ds-balance] 无 NOTIFY_WEBHOOK，跳过推送"); return
    if "信号" not in msg:
        msg = "【交易信号】" + msg
    body = json.dumps({"msg_type": "text", "content": {"text": msg}}, ensure_ascii=False).encode("utf-8")
    try:
        urllib.request.urlopen(urllib.request.Request(wh, data=body, headers={"Content-Type": "application/json"}), timeout=10)
        print("[ds-balance] 飞书已推送")
    except Exception as e:
        print(f"[ds-balance] 飞书推送失败: {e}")


def main():
    key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if not key:
        print("[ds-balance] 无 DEEPSEEK_API_KEY，跳过"); return
    req = urllib.request.Request("https://api.deepseek.com/user/balance",
                                 headers={"Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())

    avail = data.get("is_available")
    infos = data.get("balance_infos", []) or []
    info = next((b for b in infos if b.get("currency") == "CNY"), infos[0] if infos else {})
    bal = float(info.get("total_balance", 0) or 0)
    cur = info.get("currency", "CNY")
    print(f"[ds-balance] DeepSeek 余额: {bal} {cur} | is_available={avail}")

    if not avail or bal <= 0:
        feishu(f"🚨 DeepSeek 余额已用尽({bal} {cur})！广池 edge 验证已停摆，请尽快充值。\n（交易信号系统）")
    elif bal < ALERT_CNY:
        feishu(f"⚠️ DeepSeek 余额不足：仅剩 {bal} {cur}（低于 {ALERT_CNY} 阈值），约够再跑 1-2 天，请及时充值。\n（交易信号系统）")
    else:
        print(f"[ds-balance] 余额充足(≥{ALERT_CNY} {cur})，不提醒")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ds-balance] 查询失败(不影响主流程): {e}")
    sys.exit(0)
