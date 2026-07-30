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
  export FMP_API_KEY="pOJlglH08lKz9RUmFeO5yYxOc87v5HzA"
  # 信号归档同步(2026-07-22根治):云端workflow产信号提交在GitHub,本地从不pull→回填吃旧信号(7/18-21实炸4天)。
  # 只精准checkout信号目录(本地从不写它,零冲突);全量rebase会撞双写生成物,别改成pull
  git fetch -q origin main 2>/dev/null && git checkout -q origin/main -- \
    dashboard/trading-signals-history data/screened-stocks-history 2>/dev/null || true
  # 2026-07-29大清理:只留活腿hds(gate/tripwire数据源)+hdstr(真钱影子对照)。
  # 退役冻结(账本保留在data/,结论在legs_tested_summary记忆):momma/momh(动量=幸存者偏差)、
  # mn(80笔体检已裁)、c/ctg/ctr(7-17冻结,结论移动止损赢,已由hdstr继承)。复活=加回循环即可。
  for L in hds hdstr kimi; do   # kimi=信号引擎A/B影子(2026-07-30,Kimi K2.6 vs DeepSeek,同出场只换大脑)
    /usr/bin/python3 scripts/backfill-portfolio-$L.py >> data/exec-log/legs-refill.log 2>&1 || true
  done
  # edge体检:自门控,平仓<80笔静默;跨到80笔自动跑一次+飞书裁决
  for L in hds kimi; do
    LEG=$L /usr/bin/python3 scripts/analyze-leg-edge.py >> data/exec-log/launchd.log 2>&1 || true
  done
  # 杠杆指数腿:每日重算净值曲线+回撤(paper跟踪,见 spec 2026-07-07)。FMP_API_KEY上面已export
  /usr/bin/python3 scripts/backfill-portfolio-lev.py >> data/exec-log/launchd.log 2>&1 || true
  # hds真钱上车gate(预注册2026-07-14):日常静默,周五推进度,达标/到期自动裁决→飞书
  /usr/bin/python3 scripts/hds-gate.py >> data/exec-log/launchd.log 2>&1 || true
  # hds引信×2(2026-07-19暴雷预演后装):tripwire防信号静默漂移;tradability观察模式记录真钱会剔除的信号
  /usr/bin/python3 scripts/hds-tripwire.py >> data/exec-log/launchd.log 2>&1 || true
  /usr/bin/python3 scripts/tradability-filter.py >> data/exec-log/launchd.log 2>&1 || true
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
# hdstr试运行执行层:2026-07-27真钱ARMED(Riley批,协议data/hdstr-trial-protocol.json)。
# 回paper体检=去掉三个HDSTR_env。真钱账户U20220368端口4001;账户不匹配执行器自拒(guard_account)
if [ "$1" = "trade_open" ]; then
  # 先同步当晚新信号(deepseek-broad 20:00提交云端;2026-07-27审计:原同步只在review段→hdstr会吃3天前旧信号)
  git fetch -q origin main 2>/dev/null && git checkout -q origin/main -- \
    dashboard/trading-signals-history data/screened-stocks-history 2>/dev/null || true
  HDSTR_ARM=1 HDSTR_ACCOUNT=U20220368 HDSTR_PORT=4001 \
    /usr/bin/python3 -m scripts.ibkr.hdstr_exec open >> data/exec-log/launchd.log 2>&1 || true
  # QQQ指数核心托管(2026-07-29 Riley批"接管"):只买不卖,reclaim/深跌阶梯自动低吸,三重预算闸
  QQQDCA_ARM=1 QQQDCA_ACCOUNT=U20220368 QQQDCA_PORT=4001 \
    /usr/bin/python3 -m scripts.ibkr.qqq_dca_exec >> data/exec-log/launchd.log 2>&1 || true
fi
if [ "$1" = "trade_close" ]; then
  HDSTR_ARM=1 HDSTR_ACCOUNT=U20220368 HDSTR_PORT=4001 \
    /usr/bin/python3 -m scripts.ibkr.hdstr_exec close >> data/exec-log/launchd.log 2>&1 || true
fi
echo "[$(date '+%F %T')] === done $1 (exit $?) ===" >> data/exec-log/launchd.log
# 复盘后追加前向验证账本(三线vs无脑QQQ)——随paper系统一起退役,靠paper NAV没NAV就是废数
if [ "$1" = "review" ] && [ ! -f data/paper-retired ]; then
  /usr/bin/caffeinate -i /usr/bin/python3 -m scripts.ibkr.forward_track >> data/exec-log/launchd.log 2>&1
fi
