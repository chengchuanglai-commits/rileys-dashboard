#!/bin/zsh
# IBKR 执行 batch 统一入口。caffeinate 防睡眠:盖盖子也能跑(需插电源)。
# 用法: run.sh <module>  (preflight/trade_open/trade_close/review)
cd /Users/apple/claude-whatsapp
# 网络:Tailscale Exit Node(gl-mt2500,加拿大出口)= 系统级全局VPN,流量自动出墙,
# 不需要 HTTP 代理。yfinance 裸连即可取美股价。(2026-06-22 从 Clash 7897 切到 Tailscale)
# IBKR 本机(127.0.0.1)不走任何代理 —— 系统级Tailscale对localhost本就直连。
export NOTIFY_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/c540b4d3-4764-488c-bf22-2b3373a1edf3"
# 自动交易开关(2026-06-22 切LIVE:让自动batch全权管paper的10仓——20MA出场/再平衡/止损全自动)。
# 仍是 paper 账户(orders.py DU安全闸:非DU账户拒绝下单),真钱要换账户+另行决定。
# NOTIONAL=20000 与首次建仓规模一致,否则再平衡按$2000算会乱。关闭自动交易=把下面两行改0/2000或注释。
export IBKR_LIVE=0   # 暂关:trade_close的SPY豁免bug刚修,先观察再开自动
export IBKR_NOTIONAL=20000
mkdir -p data/exec-log
echo "[$(date '+%F %T')] === run $1 ===" >> data/exec-log/launchd.log
# caffeinate -i: 跑期间阻止系统空闲睡眠(合盖+插电也保持唤醒执行)
/usr/bin/caffeinate -i /usr/bin/python3 -m scripts.ibkr.$1 >> data/exec-log/launchd.log 2>&1
echo "[$(date '+%F %T')] === done $1 (exit $?) ===" >> data/exec-log/launchd.log
