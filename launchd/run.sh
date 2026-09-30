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
export IBKR_LIVE=1   # 自动交易开(2026-06-22,两bug验完):自动batch全权管paper 10仓
export IBKR_NOTIONAL=20000
mkdir -p data/exec-log
echo "[$(date '+%F %T')] === run $1 ===" >> data/exec-log/launchd.log
# review batch(收盘后)前先回填模拟盘——这时当天日bar已出,各腿对照才是当天收盘最新值(否则慢一天)
if [ "$1" = "review" ]; then
  source "$HOME/claude-whatsapp/.secrets/fmp.env"
  # 🪦 hds/hdstr/kimi 全线退役(2026-09-29 Riley终审叫停:真钱19笔前向≈-1.1%/笔,
  # 理想化影子+2.6%的edge未在真钱兑现,折价~3pp/笔系统性存在;结论在legs_tested_summary记忆)。
  # 台账/信号归档/裁决记录全部冻结留档;信号workflow已disable;复活=enable workflow+加回循环
  # 杠杆指数腿:每日重算净值曲线+回撤(paper跟踪,唯一存活的研究腿)
  /usr/bin/python3 scripts/backfill-portfolio-lev.py >> data/exec-log/launchd.log 2>&1 || true
fi
# 一次性:hds空头票借券体检(2026-07-18风险分析后,盘前查tick236;跑成一次即退休,重跑=删flag)
if [ "$1" = "preflight" ] && [ ! -f data/borrow-check-done ]; then
  /usr/bin/python3 scripts/check-borrow.py >> data/exec-log/launchd.log 2>&1 && touch data/borrow-check-done || true
fi
# paper动量系统退役(2026-07-29大清理):4002被真钱网关顶掉+幸存者偏差结论(指数才赢)→不再恢复。
# scripts.ibkr.*模块只管paper统一组合($20k momma),真钱路径(hdstr/qqq-dca)在下方独立段不受影响。
# 复活=删 data/paper-retired + 重登paper网关(独立~/Jts配置!别共用真钱的)。
if [ ! -f data/paper-retired ]; then
  # caffeinate -i: 跑期间阻止系统空闲睡眠(合盖+插电也保持唤醒执行)
  # 20分钟超时强杀(2026-07-23:IBKR农场故障致batch卡死52分钟,无超时会挂到天亮;正常batch1-3分钟)
  /usr/bin/caffeinate -i /usr/bin/python3 -m scripts.ibkr.$1 >> data/exec-log/launchd.log 2>&1 &
  BPID=$!
  ( sleep 1200; kill $BPID 2>/dev/null && echo "[$(date '+%F %T')] ⏱️ $1 batch超20分钟,已强杀(次日对账自动补齐)" >> data/exec-log/launchd.log ) &
  TPID=$!
  wait $BPID 2>/dev/null
  kill $TPID 2>/dev/null; wait $TPID 2>/dev/null
fi
# 🪦 hdstr真钱试运行已终审退役(2026-09-29 Riley叫停,19笔前向宣判;执行器/协议/台账全留档,
# kill-switch已拉;复活=Riley明示+重启信号workflow+恢复此段调用)
if [ "$1" = "trade_open" ]; then
  # QQQ指数核心托管(2026-07-29 Riley批"接管",终审后唯一存活的真钱自动化):只买不卖,三重预算闸
  QQQDCA_ARM=1 QQQDCA_ACCOUNT=U20220368 QQQDCA_PORT=4001 \
    /usr/bin/python3 -m scripts.ibkr.qqq_dca_exec >> data/exec-log/launchd.log 2>&1 &
  QP=$!; ( sleep 1500; kill $QP 2>/dev/null && echo "[$(date '+%F %T')] ⏱️ qqq-dca超25分钟,已强杀" >> data/exec-log/launchd.log ) &
  QT=$!; wait $QP 2>/dev/null; kill $QT 2>/dev/null; wait $QT 2>/dev/null
fi
echo "[$(date '+%F %T')] === done $1 (exit $?) ===" >> data/exec-log/launchd.log
# 复盘后追加前向验证账本(三线vs无脑QQQ)——随paper系统一起退役,靠paper NAV没NAV就是废数
if [ "$1" = "review" ] && [ ! -f data/paper-retired ]; then
  /usr/bin/caffeinate -i /usr/bin/python3 -m scripts.ibkr.forward_track >> data/exec-log/launchd.log 2>&1
fi
