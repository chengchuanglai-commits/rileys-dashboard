#!/bin/zsh
# IBKR 执行 batch 统一入口。caffeinate 防睡眠:盖盖子也能跑(需插电源)。
# 用法: run.sh <module>  (preflight/trade_open/trade_close/review)
cd /Users/apple/claude-whatsapp
export NO_PROXY=127.0.0.1,localhost
export HTTPS_PROXY=http://127.0.0.1:7897 HTTP_PROXY=http://127.0.0.1:7897
export NOTIFY_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/c540b4d3-4764-488c-bf22-2b3373a1edf3"
mkdir -p data/exec-log
echo "[$(date '+%F %T')] === run $1 ===" >> data/exec-log/launchd.log
# caffeinate -i: 跑期间阻止系统空闲睡眠(合盖+插电也保持唤醒执行)
/usr/bin/caffeinate -i /usr/bin/python3 -m scripts.ibkr.$1 >> data/exec-log/launchd.log 2>&1
echo "[$(date '+%F %T')] === done $1 (exit $?) ===" >> data/exec-log/launchd.log
