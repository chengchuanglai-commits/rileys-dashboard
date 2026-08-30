"""网络自愈看门狗 —— 每5分钟(launchd)检查:
  ① 加拿大SOCKS隧道(127.0.0.1:1080→CA):断了自动踢活launchd隧道任务;踢不活→飞书叫Riley(多半Tailscale掉了)。
  ② IB Gateway↔IBKR:Gateway开着但拿不到NAV=跟IBKR断了→飞书叫Riley退出重开(它不自愈)。
去重:同一故障只飞书一次(state文件),恢复时报一次"已恢复"。
不碰登录密码;Gateway没开=可能Riley主动关的,不打扰(只管"开着却断了"这个真故障)。
"""
import os, json, subprocess, time, urllib.request

REPO = "/Users/apple/claude-whatsapp"
STATE = os.path.join(REPO, "data/net-watchdog-state.json")
WEBHOOK = os.environ.get("NOTIFY_WEBHOOK", "")


def load():
    try: return json.load(open(STATE))
    except Exception: return {}

def save(s):
    try: json.dump(s, open(STATE, "w"), ensure_ascii=False)
    except Exception: pass

def feishu(msg):
    if not WEBHOOK: return
    try:
        d = json.dumps({"msg_type": "text", "content": {"text": msg}}, ensure_ascii=False).encode()
        urllib.request.urlopen(urllib.request.Request(WEBHOOK, data=d, headers={"Content-Type": "application/json"}), timeout=10)
    except Exception: pass

def socks_country():
    try:
        r = subprocess.run(["curl", "-s", "--socks5-hostname", "127.0.0.1:1080", "--max-time", "12", "ipinfo.io/country"],
                           capture_output=True, text=True, timeout=16)
        return r.stdout.strip()
    except Exception: return ""

def gateway_running():
    """4001 API口在监听 = IB Gateway 开着(比匹配进程名可靠)。2026-07-30改:paper 4002已退役,真钱网关=4001。"""
    try:
        r = subprocess.run(["lsof", "-nP", "-iTCP:4001", "-sTCP:LISTEN"], capture_output=True, text=True, timeout=6)
        return bool(r.stdout.strip())
    except Exception: return False

def ib_nav():
    """连真钱网关4001取NAV;拿不到返回None(=跟IBKR断了)。
    2026-08-01改:原走ibkr.client的PORTS=[4002,7497](paper已退役全死)→连续282次假阳性失败。"""
    import random
    try:
        from ib_insync import IB
        ib = IB()
        ib.connect("127.0.0.1", 4001, clientId=random.randint(200, 899), timeout=12)
        nav = float({v.tag: v.value for v in ib.accountSummary()}.get("NetLiquidation", 0) or 0)
        ib.disconnect()
        return nav if nav > 0 else None
    except Exception as e:
        print(f"[ib_nav err] {type(e).__name__}: {str(e)[:120]}")
        return None


FAILS_BEFORE_ALERT = 2   # 连续N次(~10分钟)失败才报警,躲开瞬时抖动


def main():
    os.chdir(REPO)
    st = load()

    # ① 隧道:断了先自动踢活,连续失败才报警
    cc = socks_country()
    if cc != "CA":
        subprocess.run(["launchctl", "kickstart", "-k", f"gui/{os.getuid()}/com.riley.ibkr-ca-socks"],
                       capture_output=True, timeout=15)
        time.sleep(9)
        cc = socks_country()
    if cc != "CA":
        st["tunnel_fail"] = st.get("tunnel_fail", 0) + 1
        if st["tunnel_fail"] >= FAILS_BEFORE_ALERT and not st.get("tunnel_alerted"):
            feishu(f"🚨 加拿大隧道断了,自动踢活没成功(当前出口:{cc or '无'})。多半是 Tailscale 掉线——去 Tailscale App 里连一下就好。")
            st["tunnel_alerted"] = True
    else:
        if st.get("tunnel_alerted"):
            feishu("✅ 加拿大隧道已自动恢复。")
        st["tunnel_fail"] = 0; st["tunnel_alerted"] = False

    # ② IB Gateway↔IBKR(只在Gateway开着时管;连续失败才报警)
    ib_state = "n/a"
    if gateway_running():
        nav = ib_nav()
        if nav is None:
            st["ib_fail"] = st.get("ib_fail", 0) + 1; ib_state = f"fail×{st['ib_fail']}"
            if st["ib_fail"] >= FAILS_BEFORE_ALERT and not st.get("ib_alerted"):
                feishu("🚨 IB Gateway 开着但跟 IBKR 断了。看门狗将在持续失败30分钟后自动重踢网关(会话有效期内会自动重登)。止损单在 IBKR 服务器端,持仓仍受保护。")
                st["ib_alerted"] = True
            # ②b 自动重踢(2026-08-30,Riley定"确保老方法不出问题"):半死≥6次(~30min)自动杀掉重开,
            # 会话有效期内网关会自动重登;失败也只是回到登录页(与不踢等价)。避开21:15-22:15自身重启窗防打架。
            hhmm = time.strftime("%H%M")
            if st["ib_fail"] >= 6 and not ("2115" <= hhmm <= "2215") and st.get("last_kick_day") != time.strftime("%F"):
                subprocess.run(["pkill", "-f", "JavaApplicationStub"], capture_output=True)
                time.sleep(8)
                subprocess.run(["open", "-a",
                    "/Users/apple/Applications/IB Gateway 10.45/IB Gateway 10.45-1.app"], capture_output=True)
                st["last_kick_day"] = time.strftime("%F")   # 每天最多踢一次,防循环风暴
                feishu("🔁 看门狗已自动重踢 IB Gateway(半死30分钟)。若15分钟后仍未恢复=需要人工登录。")
        else:
            if st.get("ib_alerted"):
                feishu(f"✅ IB Gateway 已恢复连接(NAV ${nav:,.0f})。")
            st["ib_fail"] = 0; st["ib_alerted"] = False; ib_state = "ok"

    save(st)
    print(f"[watchdog] socks={cc or '无'} gw={'on' if gateway_running() else 'off'} ib={ib_state} "
          f"tunnel_fail={st.get('tunnel_fail',0)} ib_fail={st.get('ib_fail',0)}")


if __name__ == "__main__":
    main()
