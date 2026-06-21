#!/bin/zsh
# Mac 心跳 (heartbeat / dead-man's switch):往独立 heartbeat 分支 force-push 时间戳。
# 云端看门狗查这个分支的提交时间,太旧=Mac关机/掉线→飞书报警。
# force-push 单文件单提交,不污染 main 历史。
cd /Users/apple/claude-whatsapp
export GIT_TERMINAL_PROMPT=0
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
TMP=$(mktemp -d)
# 用独立工作区构建 orphan 提交,避免碰当前工作区
git --git-dir="$(pwd)/.git" cat-file -e HEAD 2>/dev/null
{
  echo "$TS"
  echo "host: $(hostname)"
} > "$TMP/heartbeat.txt"
cd "$TMP"
git init -q
git checkout -q -b heartbeat
git add heartbeat.txt
git -c user.name=heartbeat -c user.email=hb@local commit -q -m "heartbeat $TS"
git push -q -f "https://github.com/chengchuanglai-commits/rileys-dashboard.git" heartbeat 2>/dev/null \
  && echo "[$(date '+%F %T')] heartbeat pushed $TS" >> /Users/apple/claude-whatsapp/data/exec-log/heartbeat.log \
  || echo "[$(date '+%F %T')] heartbeat push FAILED" >> /Users/apple/claude-whatsapp/data/exec-log/heartbeat.log
cd /; rm -rf "$TMP"
