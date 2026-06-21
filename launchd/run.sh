#!/bin/zsh
cd /Users/apple/claude-whatsapp
export NO_PROXY=127.0.0.1,localhost
export HTTPS_PROXY=http://127.0.0.1:7897 HTTP_PROXY=http://127.0.0.1:7897
export NOTIFY_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/c540b4d3-4764-488c-bf22-2b3373a1edf3"
/usr/bin/python3 -m scripts.ibkr.$1 >> data/exec-log/launchd.log 2>&1
