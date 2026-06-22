#!/bin/zsh
# 盘中刷新 paper 实时盈亏 → push dashboard。每5分钟跑(仅美股时段)。
# 只读账户+取价,不下单。采集后 push paper-status.js 到云端 dashboard。
cd /Users/apple/claude-whatsapp
export GIT_TERMINAL_PROMPT=0
# 仅美股时段跑(北京21:30-次日04:05=美东9:30-16:05)。其余时段直接退,不空转/不空采集。
H=$(date +%H); M=$(date +%M); HM=$((10#$H*60 + 10#$M))
# 21:30=1290分 .. 24:00=1440 ; 00:00=0 .. 04:05=245
if ! { [ $HM -ge 1290 ] || [ $HM -le 245 ]; }; then exit 0; fi
# 采集(只读,LIVE无关——paper_status不下单)
/usr/bin/python3 -m scripts.ibkr.paper_status >> data/exec-log/paper-refresh.log 2>&1
# 连不上Gateway(connected=false)→不push,避免空数据覆盖好数据
if ! grep -q '"connected": true' data/paper-status.json 2>/dev/null; then
  echo "[$(date '+%F %T')] 网关未连,跳过push(不覆盖好数据)" >> data/exec-log/paper-refresh.log
  # 把刚采集的坏文件还原(git checkout 丢弃未提交改动)
  git checkout -- dashboard/paper-status.js data/paper-status.json 2>/dev/null
  exit 0
fi
# 有变化才 push(避免空提交)
if ! git diff --quiet dashboard/paper-status.js data/paper-status.json 2>/dev/null; then
  git add dashboard/paper-status.js data/paper-status.json 2>/dev/null
  git -c user.name=paper-bot -c user.email=pb@local commit -q -m "chore: paper实时盈亏刷新 $(date '+%H:%M')" 2>/dev/null
  for i in 1 2 3; do git pull --rebase -q origin main 2>/dev/null && git push -q origin main 2>/dev/null && break; sleep 3; done
  echo "[$(date '+%F %T')] paper刷新已push" >> data/exec-log/paper-refresh.log
fi
