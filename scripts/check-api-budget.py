"""
Anthropic API 余额监控 —— 估算剩余余额，预计不足以再跑时 WhatsApp 提醒充值。

背景：Anthropic 无公开余额查询 API，无法直接读账户余额。这里靠 data/api_budget.json
里手填的余额 + 保守日均估算倒推。之前余额烧光才发现、信号停跑 miss 了数据，此脚本为提前预警。

充值后：更新 data/api_budget.json 的 balance_usd 和 as_of(=充值当天)。
不调用任何付费 API（只读文件 + POST WhatsApp），所以即使 Anthropic 余额已为 0 也能正常发提醒。
"""
import json, os, glob
import urllib.request
from datetime import date, datetime, timezone

BUDGET_PATH = "data/api_budget.json"
SYNC_URL = os.environ.get("SYNC_URL", "")

if not os.path.exists(BUDGET_PATH):
    print("[budget] 无 data/api_budget.json，跳过余额检查")
    raise SystemExit(0)

b = json.load(open(BUDGET_PATH))
balance   = float(b.get("balance_usd", 0))
as_of     = b.get("as_of", "")
est_daily = float(b.get("est_daily_usd", 1.8))
threshold = float(b.get("alert_threshold_usd", 3.5))

today = date.today()
try:
    as_of_d = datetime.strptime(as_of, "%Y-%m-%d").date()
except Exception:
    print(f"[budget] as_of 格式错误({as_of})，跳过")
    raise SystemExit(0)
days_elapsed = max((today - as_of_d).days, 0)

# 已记录的信号成本(偏低，不含晨报/取消的run)作为下限；×1.4 粗补未记录部分
recorded = 0.0
for f in glob.glob("dashboard/daily-reports/*.json"):
    d = os.path.basename(f).replace(".json", "")
    if d >= as_of:
        try:
            recorded += float(json.load(open(f)).get("api_cost_usd", 0) or 0)
        except Exception:
            pass

# 取"保守日均×天数"与"记录成本×1.4"的较大者，宁可高估花费、早提醒
est_spent = round(max(days_elapsed * est_daily, recorded * 1.4), 2)
remaining = round(balance - est_spent, 2)
runs_left = remaining / est_daily if est_daily > 0 else 0

print(f"[budget] 余额=${balance} 记录日={as_of} 过去{days_elapsed}天 "
      f"已花(估)=${est_spent}(记录下限${recorded:.2f}) → 剩余~${remaining} (~{runs_left:.1f}次)")

if remaining > threshold:
    print(f"[budget] 余额充足(>${threshold})，不提醒")
    raise SystemExit(0)

# 余额不足 → WhatsApp 提醒
msg = (f"⚠️ Anthropic API 余额预计不足\n"
       f"估算剩余 ~${remaining}（约够再跑 {runs_left:.0f} 次）\n"
       f"再不充值，信号会停跑、miss 数据！\n"
       f"充值后更新 data/api_budget.json 的 balance_usd 和 as_of")

if not SYNC_URL:
    print("[budget] 无 SYNC_URL，仅打印提醒：\n" + msg)
    raise SystemExit(0)

UA = 'Mozilla/5.0 (compatible; trading-bot/1.0)'
try:
    req = urllib.request.Request(SYNC_URL, headers={'User-Agent': UA})
    current = json.loads(urllib.request.urlopen(req, timeout=10).read())
except Exception:
    current = {}
notifications = current.get('pending_notifications', [])
notifications.append({
    'workflow': 'API 余额监控',
    'time': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'status': 'WARNING',
    'message': msg,
})
current['pending_notifications'] = notifications
data = json.dumps(current, ensure_ascii=False).encode('utf-8')
try:
    urllib.request.urlopen(
        urllib.request.Request(SYNC_URL, data=data,
                               headers={'Content-Type': 'application/json', 'User-Agent': UA},
                               method='POST'), timeout=10)
    print("[budget] ✅ 已发余额不足提醒")
except Exception as e:
    print(f"[budget] 发送失败: {e}\n{msg}")
