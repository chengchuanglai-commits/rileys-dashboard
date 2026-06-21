"""飞书发送薄封装。复用 scripts/notify-webhook.py(读 NOTIFY_WEBHOOK + NOTIFY_MESSAGE)。"""
import os, runpy

def send(text):
    if not os.environ.get("NOTIFY_WEBHOOK"):
        print("[notify] 无 NOTIFY_WEBHOOK,未发送:\n" + text)
        return False
    os.environ["NOTIFY_MESSAGE"] = text
    try:
        runpy.run_path("scripts/notify-webhook.py", run_name="__main__")
        return True
    except Exception as e:
        print(f"[notify] 发送失败: {e}")
        return False
