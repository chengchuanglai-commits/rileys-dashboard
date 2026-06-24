#!/bin/zsh
# 盘中刷新 paper 实时盈亏 → push dashboard。每5分钟跑(仅美股时段)。
# 只读账户+取价,不下单。采集后 push paper-status.js 到云端 dashboard。
cd /Users/apple/claude-whatsapp
export GIT_TERMINAL_PROMPT=0
# 仅美股时段跑(北京21:30-次日04:05=美东9:30-16:05)。其余时段直接退,不空转/不空采集。
H=$(date +%H); M=$(date +%M); HM=$((10#$H*60 + 10#$M))
# 21:30=1290分 .. 24:00=1440 ; 00:00=0 .. 04:05=245
if ! { [ $HM -ge 1290 ] || [ $HM -le 245 ]; }; then exit 0; fi
# 采集到临时文件(不碰工作区的 paper-status.js,避免和主仓库/我的提交抢状态)
PS=$(mktemp); JS=$(mktemp)
/usr/bin/python3 -m scripts.ibkr.paper_status >> data/exec-log/paper-refresh.log 2>&1
# paper_status 写到了 data/paper-status.json + dashboard/paper-status.js;读出来后立刻还原工作区
cp data/paper-status.json "$PS" 2>/dev/null; cp dashboard/paper-status.js "$JS" 2>/dev/null
git checkout -- data/paper-status.json dashboard/paper-status.js 2>/dev/null  # 工作区保持干净,不撞车
# 连不上Gateway→不更新,避免空数据覆盖好数据
if ! grep -q '"connected": true' "$PS" 2>/dev/null; then
  echo "[$(date '+%F %T')] 网关未连,跳过更新" >> data/exec-log/paper-refresh.log
  rm -f "$PS" "$JS"; exit 0
fi
# 用 GitHub API 原子更新 main 上的两个文件(不commit/不push/不动本地工作区→根治撞车)
REPO="chengchuanglai-commits/rileys-dashboard"
GH=/Users/apple/bin/gh   # launchd PATH 不全,写绝对路径
update_file() {  # $1=本地临时文件 $2=仓库路径
  local sha=$("$GH" api "repos/$REPO/contents/$2?ref=main" --jq .sha 2>/dev/null)
  local b64=$(base64 < "$1" | tr -d '\n')
  "$GH" api -X PUT "repos/$REPO/contents/$2" \
    -f message="chore: paper实时盈亏 $(date '+%H:%M')" \
    -f content="$b64" -f sha="$sha" -f branch=main >/dev/null 2>&1
}
update_file "$JS" "dashboard/paper-status.js" && update_file "$PS" "data/paper-status.json" \
  && echo "[$(date '+%F %T')] paper刷新已更新(API) ✅" >> data/exec-log/paper-refresh.log \
  || echo "[$(date '+%F %T')] ⚠️ API更新失败" >> data/exec-log/paper-refresh.log
rm -f "$PS" "$JS"
