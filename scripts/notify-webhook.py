"""国内通知渠道(飞书/钉钉 群机器人) —— GitHub 云端直发 webhook，链路不经过任何本地 Mac。

读环境变量：
  NOTIFY_WEBHOOK  机器人 webhook URL(GitHub secret)；URL 自动识别飞书 vs 钉钉
  NOTIFY_MESSAGE  消息正文

设计：完全围栏——任何失败只打印 + 退出 0，绝不拖垮主信号流程(与 WhatsApp 通知并行、互不影响)。
机器人安全设置用「自定义关键词=信号」，故确保消息含「信号」二字。
"""
import os, sys, json, urllib.request


def main():
    url = os.environ.get("NOTIFY_WEBHOOK", "").strip()
    msg = os.environ.get("NOTIFY_MESSAGE", "").strip()
    if not url:
        print("[webhook] 无 NOTIFY_WEBHOOK，跳过")
        return
    if not msg:
        print("[webhook] 无消息内容，跳过")
        return
    # 确保命中机器人自定义关键词「信号」
    if "信号" not in msg:
        msg = "【交易信号】\n" + msg

    if "dingtalk" in url:                       # 钉钉
        payload = {"msgtype": "text", "text": {"content": msg}}
    else:                                       # 飞书 open.feishu.cn / larksuite
        payload = {"msg_type": "text", "content": {"text": msg}}

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            print(f"[webhook] 已发送 HTTP {r.status}: {r.read()[:200]}")
    except Exception as e:
        print(f"[webhook] 发送失败(不影响主流程): {e}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[webhook] 整体失败: {e}")
    sys.exit(0)
