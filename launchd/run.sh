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
  for L in momma momh mn c ctg ctr hds hdstr; do   # h退役(2026-07-09);c/ctg/ctr=冻结实验(2026-07-17停Haiku信号;结论:移动止损赢固定TP);hdstr=hds移动止损影子(2026-07-17三重证据后上线,不参与gate)
    /usr/bin/python3 scripts/backfill-portfolio-$L.py >> data/exec-log/legs-refill.log 2>&1 || true
  done
  # momma回填后立刻重算三线统一目标(否则master-allocation停在旧日期→波动腿目标用已剔除的幽灵票)
  /usr/bin/python3 scripts/master-allocator.py >> data/exec-log/launchd.log 2>&1 || true
  # 腿edge体检:自门控,平仓<80笔静默;跨到80笔自动跑一次+飞书裁决(通用脚本)
  # c=最强前向基线,ctg=c-tight,ctr=c-trail(方法B证移动止损最稳)→ 攒够80笔各自自动裁决
  for L in mn hds c ctg ctr; do
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
# caffeinate -i: 跑期间阻止系统空闲睡眠(合盖+插电也保持唤醒执行)
/usr/bin/caffeinate -i /usr/bin/python3 -m scripts.ibkr.$1 >> data/exec-log/launchd.log 2>&1
echo "[$(date '+%F %T')] === done $1 (exit $?) ===" >> data/exec-log/launchd.log
# 复盘后追加前向验证账本(此刻NAV已结算、日bar已出,三线vs无脑QQQ的alpha才是当天收盘真值)
if [ "$1" = "review" ]; then
  /usr/bin/caffeinate -i /usr/bin/python3 -m scripts.ibkr.forward_track >> data/exec-log/launchd.log 2>&1
fi
