import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from scripts.ibkr.notify import send

def test_send_no_webhook_prints(capfdoff=None):
    # 无 NOTIFY_WEBHOOK 时返回 False(未发送)但不抛异常
    os.environ.pop("NOTIFY_WEBHOOK", None)
    assert send("测试消息") is False

if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f(); print(f"  ok {n}")
    print("ALL PASS")
