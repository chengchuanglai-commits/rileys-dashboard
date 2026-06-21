"""云端看门狗 (heartbeat watchdog) —— 查 Mac 心跳新鲜度,太旧=Mac关机/掉线→飞书报警。
在 GitHub Actions 跑(云端一直在线,Mac关了也发得出)。读 heartbeat 分支最新提交时间。
用法: STALE_MIN=40 BEFORE_BATCH="今晚21:30的交易" NOTIFY_WEBHOOK=... python scripts/heartbeat-watchdog.py
"""
import os, subprocess, runpy
from datetime import datetime, timezone

STALE_MIN = int(os.environ.get("STALE_MIN", "40"))
BEFORE = os.environ.get("BEFORE_BATCH", "")   # 可选:说明这是哪个batch前的检查
REPO = "https://github.com/chengchuanglai-commits/rileys-dashboard.git"


def heartbeat_age_min():
    """返回 heartbeat 分支最新提交距今分钟数,拿不到返回 None。"""
    try:
        out = subprocess.check_output(
            ["git", "ls-remote", REPO, "refs/heads/heartbeat"], text=True, timeout=30).strip()
        if not out:
            return None
        sha = out.split()[0]
        # 浅拉该提交读时间
        subprocess.run(["git", "fetch", "-q", "--depth=1", REPO, "heartbeat"], timeout=30,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        ts = subprocess.check_output(["git", "show", "-s", "--format=%cI", "FETCH_HEAD"],
                                     text=True, timeout=30).strip()
        commit_dt = datetime.fromisoformat(ts)
        return (datetime.now(timezone.utc) - commit_dt).total_seconds() / 60
    except Exception as e:
        print(f"[watchdog] 读心跳失败: {e}")
        return None


def notify(text):
    if os.environ.get("NOTIFY_WEBHOOK"):
        os.environ["NOTIFY_MESSAGE"] = text
        try: runpy.run_path("scripts/notify-webhook.py", run_name="__main__")
        except Exception as e: print(f"[watchdog] 发送失败: {e}")
    else:
        print("[watchdog] 无 NOTIFY_WEBHOOK:\n" + text)


def main():
    age = heartbeat_age_min()
    ctx = f"(在{BEFORE}之前的检查)" if BEFORE else ""
    if age is None:
        notify(f"⚠️ 交易系统看门狗:读不到 Mac 心跳{ctx}\nMac 可能从未上线/网络异常。请检查电脑+IB Gateway。\n（交易信号系统）")
        return
    if age > STALE_MIN:
        warn = f"\n⚠️ {BEFORE}不会执行!" if BEFORE else ""
        notify(f"🔴 交易系统看门狗:Mac 已 {age:.0f} 分钟无心跳{ctx}\n判定=电脑关机/掉线/IB Gateway断。{warn}\n请开机+确认 Gateway 登录。\n（交易信号系统）")
        print(f"[watchdog] 心跳 {age:.0f}分钟前 > {STALE_MIN} → 已报警")
    else:
        print(f"[watchdog] Mac 心跳正常({age:.0f}分钟前 ≤ {STALE_MIN}),不报警")


if __name__ == "__main__":
    main()
