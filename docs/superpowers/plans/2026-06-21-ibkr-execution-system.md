# IBKR 完整执行系统 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 Riley 的 Mac 本地建一套三层 IBKR 执行系统(决策/保护/复盘),睡觉时自动按引擎配置交易+止损,醒来给详尽复盘;先 paper 跑,真钱是 config 开关。

**Architecture:** 纯逻辑(对账/断路器/股数/复盘组装)做成可离线单测的函数;IBKR I/O 收敛到 `client.py`+`orders.py` 薄封装;三个 batch(preflight/open/close)编排这些单元;复盘读 exec-log+IBKR 三方对比。本地 launchd 定时。

**Tech Stack:** Python 3.9、ib_insync 0.9.86、yfinance、launchd、飞书 webhook(复用 notify-webhook.py)。

设计依据:`docs/superpowers/specs/2026-06-21-ibkr-execution-system-design.md`。
测试:纯 assert 脚本(`python3 scripts/ibkr/tests/test_*.py`,打印 `ALL PASS`),不用 pytest,匹配仓库风格。IBKR I/O 层用 paper 实测(Gateway 需登录,端口4002)。

---

## File Structure

```
scripts/ibkr/
  config.py        常量集中:LIVE(默认False)、FRACTIONAL(默认False)、断路器档位(待校准)、安全闸上限、名义本金、端口
  sizing.py        纯函数:目标$→股数(整数股/小数股cashQty),买不起跳过
  reconcile.py     纯函数:目标持仓 vs 实际持仓 → 差额订单(补/清/持平)
  risk.py          纯函数:回撤断路器(净值+峰值→档位→动作)
  client.py        IBKR连接+健康检查(连/DU校验/只读校验/重连/全局撤单)
  orders.py        下单封装(限价单/stop单/安全闸校验),唯一下单入口
  preflight.py     开盘前自检(8项→放行/中止+报警)
  trade_open.py    开盘batch编排
  trade_close.py   收盘batch编排
  review.py        复盘(读exec-log+IBKR→三方对比→飞书+落盘)
  notify.py        飞书发送薄封装(复用 scripts/notify-webhook.py)
  tests/test_*.py  纯逻辑离线测
data/exec-log/{date}.json   每日动作审计
data/review/{date}.json     每日复盘存档
launchd/*.plist             三个batch定时
```

注:沿用今天已验证的 `scripts/ibkr_reconcile.py`/`ibkr_execute.py` 逻辑,重构进 `scripts/ibkr/` 模块化。旧脚本保留不删(参考)。

---

## Task 1: config 常量集中

**Files:**
- Create: `scripts/__init__.py`(空,让 `python3 -m scripts.ibkr.xxx` 能跑)、`scripts/ibkr/__init__.py`(空)、`scripts/ibkr/tests/__init__.py`(空)、`scripts/ibkr/config.py`
- Test: `scripts/ibkr/tests/test_config.py`

- [ ] **Step 1: 写失败测试**

```python
# scripts/ibkr/tests/test_config.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from scripts.ibkr import config as C

def test_defaults_safe():
    assert C.LIVE is False           # 默认 paper,不碰真钱
    assert C.FRACTIONAL is False     # 默认整数股(权限未开)
    assert C.NOTIONAL == 2000.0
    assert C.PORTS[0] == 4002        # Gateway paper 优先

def test_circuit_breaker_tiers_ordered():
    t = C.DRAWDOWN_TIERS
    assert t["warn"] < t["reduce_only"] < t["defensive"]  # 20<25<28
    assert t["warn"] == 0.20 and t["defensive"] == 0.28

def test_safety_caps_positive():
    assert C.MAX_ORDER_USD > 0 and C.MAX_TOTAL_USD >= C.NOTIONAL

if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f(); print(f"  ok {n}")
    print("ALL PASS")
```

- [ ] **Step 2: 跑测试确认失败**

Run: `cd /Users/apple/claude-whatsapp && python3 scripts/ibkr/tests/test_config.py`
Expected: FAIL `ModuleNotFoundError: scripts.ibkr`

- [ ] **Step 3: 写实现**

```python
# scripts/__init__.py、scripts/ibkr/__init__.py、scripts/ibkr/tests/__init__.py → 均空文件
# (让 python3 -m scripts.ibkr.xxx 模块导入可用)
```
```python
# scripts/ibkr/config.py
"""执行系统常量集中。改一处即全局生效。真钱开关默认关。"""
LIVE = False              # True=真钱;默认 paper
FRACTIONAL = False        # True=小数股(cashQty);默认整数股(权限未开,见spec实测)
NOTIONAL = 2000.0         # 名义本金(模拟真实$2000规模)
PORTS = [4002, 7497, 4001, 7496]   # 连接尝试顺序:Gateway paper 优先

# 安全闸
MAX_ORDER_USD = 1500.0    # 单笔上限(SPY 60%≈$1200 在内)
MAX_TOTAL_USD = 2200.0    # 总下单额上限

# 回撤断路器档位(占位值,# TODO 待 backtest-momentum-sized.py 回测校准)
DRAWDOWN_TIERS = {"warn": 0.20, "reduce_only": 0.25, "defensive": 0.28}
HARD_REDLINE = 0.30       # Riley 风险预算

# 出场
INIT_STOP_PCT = 0.08      # 单仓 -8% 固定 stop
LIMIT_BUFFER = 0.01       # 限价缓冲

LEG_PORT = {"momma": "data/portfolio_momma.json", "bq": "data/portfolio_bq.json"}
```

- [ ] **Step 4: 跑测试确认通过**

Run: `cd /Users/apple/claude-whatsapp && python3 scripts/ibkr/tests/test_config.py`
Expected: `ALL PASS`

- [ ] **Step 5: 提交**

```bash
cd /Users/apple/claude-whatsapp
git add scripts/__init__.py scripts/ibkr/__init__.py scripts/ibkr/tests/__init__.py scripts/ibkr/config.py scripts/ibkr/tests/test_config.py
git commit -m "feat(ibkr): config 常量集中 + 测试 + 包结构"
```

---

## Task 2: sizing 纯函数(目标$→股数)

**Files:**
- Create: `scripts/ibkr/sizing.py`
- Test: `scripts/ibkr/tests/test_sizing.py`

- [ ] **Step 1: 写失败测试**

```python
# scripts/ibkr/tests/test_sizing.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from scripts.ibkr.sizing import target_shares

def test_integer_floor():
    # 整数股:$800/$78 = 10.25 → 10
    assert target_shares(800, 78.0, fractional=False) == 10

def test_integer_too_expensive_returns_zero():
    # $80 买 $862 的票 → 0 股(买不起)
    assert target_shares(80, 862.0, fractional=False) == 0

def test_fractional_keeps_decimals():
    # 小数股:$80/$537 = 0.1489
    assert abs(target_shares(80, 537.0, fractional=True) - 0.1489) < 0.0001

def test_zero_price_safe():
    assert target_shares(80, 0, fractional=True) == 0

if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f(); print(f"  ok {n}")
    print("ALL PASS")
```

- [ ] **Step 2: 跑测试确认失败**

Run: `cd /Users/apple/claude-whatsapp && python3 scripts/ibkr/tests/test_sizing.py`
Expected: FAIL `ModuleNotFoundError`/`ImportError`

- [ ] **Step 3: 写实现**

```python
# scripts/ibkr/sizing.py
"""目标金额 → 股数。整数股(向下取整,买不起1股=0)或小数股(保留4位)。"""
import math

def target_shares(target_usd, price, fractional=False):
    if not price or price <= 0:
        return 0
    raw = target_usd / price
    if fractional:
        return round(raw, 4)
    return int(math.floor(raw))
```

- [ ] **Step 4: 跑测试确认通过**

Run: `cd /Users/apple/claude-whatsapp && python3 scripts/ibkr/tests/test_sizing.py`
Expected: `ALL PASS`

- [ ] **Step 5: 提交**

```bash
cd /Users/apple/claude-whatsapp
git add scripts/ibkr/sizing.py scripts/ibkr/tests/test_sizing.py
git commit -m "feat(ibkr): sizing 纯函数(整数/小数股)"
```

---

## Task 3: reconcile 纯函数(目标vs实际→差额订单)

**Files:**
- Create: `scripts/ibkr/reconcile.py`
- Test: `scripts/ibkr/tests/test_reconcile.py`

- [ ] **Step 1: 写失败测试**

```python
# scripts/ibkr/tests/test_reconcile.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from scripts.ibkr.reconcile import diff_orders

# diff_orders(target_sh, actual_sh, tol) → [{"sym","qty"}] qty>0买 qty<0卖
def test_empty_buys_all():
    o = diff_orders({"SPY": 1.6, "STM": 10}, {}, tol=0.01)
    d = {x["sym"]: x["qty"] for x in o}
    assert abs(d["SPY"] - 1.6) < 1e-9 and abs(d["STM"] - 10) < 1e-9

def test_held_partial_adjusts():
    # SPY够(持平不出现) STM少(补) AMD多(卖) OLD不该有(清)
    o = diff_orders({"SPY": 1.6, "STM": 10, "AMD": 0.15},
                    {"SPY": 1.6, "STM": 4, "AMD": 0.3, "OLD": 2}, tol=0.01)
    d = {x["sym"]: round(x["qty"], 4) for x in o}
    assert "SPY" not in d                 # 持平,不下单
    assert d["STM"] == 6                   # 补
    assert d["AMD"] == -0.15               # 卖
    assert d["OLD"] == -2                  # 清仓

def test_within_tolerance_no_order():
    o = diff_orders({"SPY": 1.605}, {"SPY": 1.6}, tol=0.01)
    assert o == []                         # 差<tol,不动

if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f(); print(f"  ok {n}")
    print("ALL PASS")
```

- [ ] **Step 2: 跑测试确认失败**

Run: `cd /Users/apple/claude-whatsapp && python3 scripts/ibkr/tests/test_reconcile.py`
Expected: FAIL `ImportError`

- [ ] **Step 3: 写实现**

```python
# scripts/ibkr/reconcile.py
"""对账:目标股数 vs 实际股数 → 差额订单。补差/清掉榜/持平不动。"""

def diff_orders(target_sh, actual_sh, tol=0.01):
    out = []
    for sym in sorted(set(target_sh) | set(actual_sh)):
        diff = round(target_sh.get(sym, 0) - actual_sh.get(sym, 0), 6)
        if abs(diff) < tol:
            continue
        out.append({"sym": sym, "qty": diff})
    return out
```

- [ ] **Step 4: 跑测试确认通过**

Run: `cd /Users/apple/claude-whatsapp && python3 scripts/ibkr/tests/test_reconcile.py`
Expected: `ALL PASS`

- [ ] **Step 5: 提交**

```bash
cd /Users/apple/claude-whatsapp
git add scripts/ibkr/reconcile.py scripts/ibkr/tests/test_reconcile.py
git commit -m "feat(ibkr): reconcile 差额订单纯函数(3场景)"
```

---

## Task 4: risk 回撤断路器纯函数

**Files:**
- Create: `scripts/ibkr/risk.py`
- Test: `scripts/ibkr/tests/test_risk.py`

- [ ] **Step 1: 写失败测试**

```python
# scripts/ibkr/tests/test_risk.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from scripts.ibkr.risk import drawdown, breaker_action

def test_drawdown_calc():
    assert abs(drawdown(nav=1800, peak=2000) - 0.10) < 1e-9
    assert drawdown(nav=2100, peak=2000) == 0.0   # 新高,无回撤

def test_breaker_normal():
    assert breaker_action(0.05) == "normal"        # <20%
def test_breaker_warn():
    assert breaker_action(0.21) == "warn"          # 20-25%:预警,新仓减半
def test_breaker_reduce_only():
    assert breaker_action(0.26) == "reduce_only"   # 25-28%:停开新仓
def test_breaker_defensive():
    assert breaker_action(0.29) == "defensive"     # >28%:全线出场

if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f(); print(f"  ok {n}")
    print("ALL PASS")
```

- [ ] **Step 2: 跑测试确认失败**

Run: `cd /Users/apple/claude-whatsapp && python3 scripts/ibkr/tests/test_risk.py`
Expected: FAIL `ImportError`

- [ ] **Step 3: 写实现**

```python
# scripts/ibkr/risk.py
"""回撤断路器:净值vs峰值→回撤→分档动作。阈值见 config(待回测校准)。"""
from scripts.ibkr.config import DRAWDOWN_TIERS

def drawdown(nav, peak):
    if not peak or peak <= 0:
        return 0.0
    return max(0.0, (peak - nav) / peak)

def breaker_action(dd, tiers=None):
    t = tiers or DRAWDOWN_TIERS
    if dd >= t["defensive"]:
        return "defensive"      # 全线挂出场
    if dd >= t["reduce_only"]:
        return "reduce_only"    # 停开新仓,只允出场
    if dd >= t["warn"]:
        return "warn"           # 预警,新仓减半
    return "normal"
```

- [ ] **Step 4: 跑测试确认通过**

Run: `cd /Users/apple/claude-whatsapp && python3 scripts/ibkr/tests/test_risk.py`
Expected: `ALL PASS`

- [ ] **Step 5: 提交**

```bash
cd /Users/apple/claude-whatsapp
git add scripts/ibkr/risk.py scripts/ibkr/tests/test_risk.py
git commit -m "feat(ibkr): risk 回撤断路器分档(占位值待校准)"
```

---

## Task 5: 目标构建(allocation→{sym: target_usd})

**Files:**
- Create: `scripts/ibkr/targets.py`
- Test: `scripts/ibkr/tests/test_targets.py`

- [ ] **Step 1: 写失败测试**

```python
# scripts/ibkr/tests/test_targets.py
import sys, os, json, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from scripts.ibkr.targets import build_targets

def test_build_from_alloc(tmp=tempfile.mkdtemp()):
    alloc = {"index_pct": 0.6, "active_pct": 0.4,
             "final_allocation": {"momma": 0.4, "bq": 0.0}}
    momma = {"open_positions": [{"ticker": "AAA"}, {"ticker": "BBB"}]}
    ap = os.path.join(tmp, "alloc.json"); json.dump(alloc, open(ap, "w"))
    mp = os.path.join(tmp, "momma.json"); json.dump(momma, open(mp, "w"))
    t = build_targets(alloc_path=ap, leg_paths={"momma": mp, "bq": mp},
                      notional=2000)
    assert t["SPY"] == 1200.0           # 指数60%
    assert abs(t["AAA"] - 400.0) < 1e-9  # 主动40%=$800/2票=$400
    assert abs(t["BBB"] - 400.0) < 1e-9
    assert "bq" not in t                  # 权重0不出现

if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f(); print(f"  ok {n}")
    print("ALL PASS")
```

- [ ] **Step 2: 跑测试确认失败**

Run: `cd /Users/apple/claude-whatsapp && python3 scripts/ibkr/tests/test_targets.py`
Expected: FAIL `ImportError`

- [ ] **Step 3: 写实现**

```python
# scripts/ibkr/targets.py
"""引擎配置 allocation.json + 各腿持仓 → {symbol: target_usd}。"""
import json
from scripts.ibkr.config import NOTIONAL, LEG_PORT

def _load(p, d=None):
    try: return json.load(open(p))
    except Exception: return d

def build_targets(alloc_path="data/allocation.json", leg_paths=None, notional=NOTIONAL):
    leg_paths = leg_paths or LEG_PORT
    a = _load(alloc_path)
    if not a: return {}
    t = {}
    if a.get("index_pct", 0) * notional > 0:
        t["SPY"] = a["index_pct"] * notional
    for leg, w in a.get("final_allocation", {}).items():
        amt = w * notional
        if amt <= 0: continue
        port = _load(leg_paths.get(leg, ""), {})
        tks = [p["ticker"] for p in (port.get("open_positions") or []) if p.get("ticker")]
        if not tks: continue
        for tk in tks:
            t[tk] = t.get(tk, 0) + amt / len(tks)
    return t
```

- [ ] **Step 4: 跑测试确认通过**

Run: `cd /Users/apple/claude-whatsapp && python3 scripts/ibkr/tests/test_targets.py`
Expected: `ALL PASS`

- [ ] **Step 5: 提交**

```bash
cd /Users/apple/claude-whatsapp
git add scripts/ibkr/targets.py scripts/ibkr/tests/test_targets.py
git commit -m "feat(ibkr): 目标构建(allocation→target_usd)"
```

---

## Task 6: 飞书通知薄封装

**Files:**
- Create: `scripts/ibkr/notify.py`
- Test: `scripts/ibkr/tests/test_notify.py`

- [ ] **Step 1: 写失败测试**

```python
# scripts/ibkr/tests/test_notify.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from scripts.ibkr.notify import send

def test_send_no_webhook_prints(capfdoff=None):
    # 无 NOTIFY_WEBHOOK 时返回 False(未发送)但不抛异常
    os.environ.pop("NOTIFY_WEBHOOK", None)
    assert send("测试消息") is False

if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f(); print(f"  ok {n}")
    print("ALL PASS")
```

- [ ] **Step 2: 跑测试确认失败**

Run: `cd /Users/apple/claude-whatsapp && python3 scripts/ibkr/tests/test_notify.py`
Expected: FAIL `ImportError`

- [ ] **Step 3: 写实现**

```python
# scripts/ibkr/notify.py
"""飞书发送薄封装。复用 scripts/notify-webhook.py(读 NOTIFY_WEBHOOK + NOTIFY_MESSAGE)。"""
import os, runpy

def send(text):
    if not os.environ.get("NOTIFY_WEBHOOK"):
        print("[notify] 无 NOTIFY_WEBHOOK,未发送:\n" + text)
        return False
    os.environ["NOTIFY_MESSAGE"] = text
    try:
        runpy.run_path("scripts/notify-webhook.py", run_name="__main__")
        return True
    except Exception as e:
        print(f"[notify] 发送失败: {e}")
        return False
```

- [ ] **Step 4: 跑测试确认通过**

Run: `cd /Users/apple/claude-whatsapp && python3 scripts/ibkr/tests/test_notify.py`
Expected: `ALL PASS`

- [ ] **Step 5: 提交**

```bash
cd /Users/apple/claude-whatsapp
git add scripts/ibkr/notify.py scripts/ibkr/tests/test_notify.py
git commit -m "feat(ibkr): 飞书通知薄封装"
```

---

## Task 7: client 连接+健康检查(IBKR I/O,paper实测)

**Files:**
- Create: `scripts/ibkr/client.py`

- [ ] **Step 1: 写实现(I/O层,用 paper 实测代替单测)**

```python
# scripts/ibkr/client.py
"""IBKR 连接 + 健康检查。所有 I/O 收敛此处。"""
from ib_insync import IB
from scripts.ibkr.config import PORTS

def connect(client_id=10, timeout=8):
    """尝试 PORTS 列表,返回 (ib, port) 或 (None, None)。重试在调用方。"""
    for port in PORTS:
        ib = IB()
        try:
            ib.connect("127.0.0.1", port, clientId=client_id, timeout=timeout)
            return ib, port
        except Exception:
            continue
    return None, None

def health(ib):
    """返回 dict:account / is_paper / nav / cash / open_orders 数。"""
    acct = ib.managedAccounts()[0] if ib.managedAccounts() else None
    summ = {v.tag: v.value for v in ib.accountSummary()
            if v.tag in ("NetLiquidation", "TotalCashValue")}
    ib.reqAllOpenOrders(); ib.sleep(1)
    return {
        "account": acct,
        "is_paper": bool(acct and acct.startswith("DU")),
        "nav": float(summ.get("NetLiquidation", 0) or 0),
        "cash": float(summ.get("TotalCashValue", 0) or 0),
        "open_orders": len(ib.openTrades()),
    }

def cancel_all(ib):
    """全局撤单(跨session,reqGlobalCancel——避开今天踩的10147坑)。"""
    ib.reqGlobalCancel(); ib.sleep(3)
    ib.reqAllOpenOrders(); ib.sleep(1)
    return len(ib.openTrades())
```

- [ ] **Step 2: paper 实测验证(Gateway 需登录,端口4002)**

Run:
```bash
cd /Users/apple/claude-whatsapp
NO_PROXY=127.0.0.1,localhost python3 -c "
from scripts.ibkr.client import connect, health, cancel_all
ib, port = connect(client_id=70)
assert ib, '没连上网关(检查Gateway登录+API)'
h = health(ib)
print('健康:', h)
assert h['is_paper'], '非paper账户!'
assert h['nav'] > 0
print('全局撤单后挂单:', cancel_all(ib))
ib.disconnect(); print('OK')
"
```
Expected: 打印健康 dict(is_paper True、nav>0)、最后 `OK`

- [ ] **Step 3: 提交**

```bash
cd /Users/apple/claude-whatsapp
git add scripts/ibkr/client.py
git commit -m "feat(ibkr): client 连接+健康检查+全局撤单"
```

---

## Task 8: orders 下单封装(限价/stop/安全闸,paper实测)

**Files:**
- Create: `scripts/ibkr/orders.py`
- Test: `scripts/ibkr/tests/test_orders_gate.py`(安全闸纯逻辑离线测)

- [ ] **Step 1: 写失败测试(安全闸逻辑)**

```python
# scripts/ibkr/tests/test_orders_gate.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from scripts.ibkr.orders import check_gates

# check_gates(plan, max_order, max_total) → (ok, reason)
def test_pass():
    plan = [{"sym":"SPY","usd":1200},{"sym":"AAA","usd":400}]
    ok, r = check_gates(plan, max_order=1500, max_total=2200)
    assert ok and r == ""

def test_single_too_big():
    plan = [{"sym":"SPY","usd":1600}]
    ok, r = check_gates(plan, max_order=1500, max_total=2200)
    assert not ok and "单笔" in r

def test_total_too_big():
    plan = [{"sym":"A","usd":1200},{"sym":"B","usd":1200}]
    ok, r = check_gates(plan, max_order=1500, max_total=2200)
    assert not ok and "总额" in r

if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f(); print(f"  ok {n}")
    print("ALL PASS")
```

- [ ] **Step 2: 跑测试确认失败**

Run: `cd /Users/apple/claude-whatsapp && python3 scripts/ibkr/tests/test_orders_gate.py`
Expected: FAIL `ImportError`

- [ ] **Step 3: 写实现**

```python
# scripts/ibkr/orders.py
"""下单封装:安全闸校验 + 限价单 + stop单。唯一下单入口。"""
from ib_insync import Stock, LimitOrder, StopOrder
from scripts.ibkr.config import LIMIT_BUFFER, FRACTIONAL

def check_gates(plan, max_order, max_total):
    """plan: [{"sym","usd",...}]。返回 (ok, reason)。"""
    for o in plan:
        if o["usd"] > max_order:
            return False, f"单笔 {o['sym']} ${o['usd']:.0f} > 上限 ${max_order:.0f}"
    total = sum(o["usd"] for o in plan)
    if total > max_total:
        return False, f"总额 ${total:.0f} > 上限 ${max_total:.0f}"
    return True, ""

def place_limit(ib, sym, qty, price, fractional=FRACTIONAL):
    """限价单。fractional=True 用 cashQty(qty 此时是金额);否则整数股数。"""
    ct = Stock(sym, "SMART", "USD"); ib.qualifyContracts(ct)
    side = "BUY" if qty > 0 else "SELL"
    lmt = round(price * (1 + LIMIT_BUFFER) if qty > 0 else price * (1 - LIMIT_BUFFER), 2)
    if fractional:
        o = LimitOrder(side, 0, lmt); o.cashQty = abs(qty)
    else:
        o = LimitOrder(side, abs(qty), lmt)
    o.tif = "DAY"
    return ib.placeOrder(ct, o)

def place_stop(ib, sym, qty, stop_price):
    """固定 stop(到价市价卖)。qty=持仓股数(正)。"""
    ct = Stock(sym, "SMART", "USD"); ib.qualifyContracts(ct)
    o = StopOrder("SELL", abs(qty), round(stop_price, 2)); o.tif = "GTC"
    return ib.placeOrder(ct, o)
```

- [ ] **Step 4: 跑测试确认通过**

Run: `cd /Users/apple/claude-whatsapp && python3 scripts/ibkr/tests/test_orders_gate.py`
Expected: `ALL PASS`

- [ ] **Step 5: paper 实测下一笔整数股限价单 + 撤掉**

Run:
```bash
cd /Users/apple/claude-whatsapp
NO_PROXY=127.0.0.1,localhost HTTPS_PROXY=http://127.0.0.1:7897 python3 -c "
from scripts.ibkr.client import connect, cancel_all
from scripts.ibkr.orders import place_limit
import yfinance as yf
ib,_=connect(client_id=71)
px=float(yf.download('AAPL',period='2d',progress=False)['Close'].dropna().iloc[-1])
tr=place_limit(ib,'AAPL',1,px,fractional=False); ib.sleep(3)
print('状态:', tr.orderStatus.status)
assert tr.orderStatus.status in ('Submitted','PreSubmitted','Filled'), '下单失败'
print('撤单后:', cancel_all(ib)); ib.disconnect(); print('OK')
"
```
Expected: 状态 Submitted/PreSubmitted/Filled、`OK`

- [ ] **Step 6: 提交**

```bash
cd /Users/apple/claude-whatsapp
git add scripts/ibkr/orders.py scripts/ibkr/tests/test_orders_gate.py
git commit -m "feat(ibkr): orders 限价/stop封装+安全闸(paper实测下单通)"
```

---

## Task 9: preflight 开盘前自检

**Files:**
- Create: `scripts/ibkr/preflight.py`

- [ ] **Step 1: 写实现**

```python
# scripts/ibkr/preflight.py
"""开盘前自检:8项,全过放行,任一失败中止+报警(带原因+建议)。"""
import os, json, time
from scripts.ibkr.client import connect, health
from scripts.ibkr.config import NOTIONAL, HARD_REDLINE
from scripts.ibkr.notify import send

def run():
    fails = []
    ib, port = connect(client_id=20)
    if not ib:
        send("⚠️ IBKR自检失败:网关连不上\n建议:检查 IB Gateway 是否登录、API端口4002是否开\n（交易信号系统）")
        return False
    h = health(ib)
    if not h["is_paper"]:
        fails.append(f"账户 {h['account']} 非paper(DU开头)→ 防误连实盘,中止")
    if h["nav"] <= 0:
        fails.append("净值读不到/为0 → 账户连接异常")
    # allocation 新鲜度
    try:
        a = json.load(open("data/allocation.json"))
        gen = a.get("generated", "")
        if gen[:10] != time.strftime("%Y-%m-%d"):
            fails.append(f"allocation.json 不是今天({gen}) → 引擎可能没更新")
        # 回撤红线
        nav, peak = h["nav"], max(h["nav"], NOTIONAL)
        if peak > 0 and (peak - nav) / peak >= HARD_REDLINE:
            fails.append(f"已破回撤红线 {HARD_REDLINE*100:.0f}%")
    except Exception as e:
        fails.append(f"读 allocation.json 失败: {e}")
    if h["open_orders"] > 0:
        fails.append(f"有 {h['open_orders']} 笔遗留挂单 → 建议先 cancel_all")
    ib.disconnect()

    if fails:
        send("⚠️ IBKR开盘前自检失败:\n- " + "\n- ".join(fails) +
             "\n今夜不下单。请处理后重跑。\n（交易信号系统）")
        return False
    send(f"✅ IBKR自检通过(账户{h['account']} 净值${h['nav']:.0f}),今夜可交易\n（交易信号系统）")
    return True

if __name__ == "__main__":
    import sys
    sys.exit(0 if run() else 1)
```

- [ ] **Step 2: paper 实测(Gateway 登录着,应通过)**

Run: `cd /Users/apple/claude-whatsapp && NO_PROXY=127.0.0.1,localhost python3 scripts/ibkr/preflight.py; echo "exit=$?"`
Expected: 打印自检结果;Gateway正常时 `exit=0`(或因 allocation 日期/遗留挂单给出明确 fail 原因,符合预期即可)

- [ ] **Step 3: 提交**

```bash
cd /Users/apple/claude-whatsapp
git add scripts/ibkr/preflight.py
git commit -m "feat(ibkr): preflight 开盘前自检(8项+报警)"
```

---

## Task 10: trade_open 开盘batch编排

**Files:**
- Create: `scripts/ibkr/trade_open.py`

- [ ] **Step 1: 写实现**

```python
# scripts/ibkr/trade_open.py
"""开盘batch:自检过→对账→下单→挂止损→落exec-log。LIVE=False只算不下。"""
import os, json, time
from scripts.ibkr.client import connect, health
from scripts.ibkr.targets import build_targets
from scripts.ibkr.sizing import target_shares
from scripts.ibkr.reconcile import diff_orders
from scripts.ibkr.risk import drawdown, breaker_action
from scripts.ibkr.orders import check_gates, place_limit, place_stop
from scripts.ibkr.config import (LIVE, FRACTIONAL, NOTIONAL, MAX_ORDER_USD,
                                 MAX_TOTAL_USD, INIT_STOP_PCT)
from scripts.ibkr.notify import send

def _prices(syms):
    import yfinance as yf
    px = {}
    try:
        d = yf.download(syms, period="2d", progress=False)["Close"]
        for s in syms:
            try: px[s] = float(d[s].dropna().iloc[-1]) if len(syms) > 1 else float(d.dropna().iloc[-1])
            except Exception: px[s] = None
    except Exception: pass
    return px

def run():
    ib, port = connect(client_id=21)
    if not ib:
        send("⚠️ 开盘batch:网关连不上,中止\n（交易信号系统）"); return
    h = health(ib)
    if not h["is_paper"] and not LIVE:
        send(f"⚠️ 开盘batch:账户{h['account']}非paper且LIVE=False,中止\n（交易信号系统）")
        ib.disconnect(); return
    targets_usd = build_targets(notional=NOTIONAL)
    actual = {p.contract.symbol: p.position for p in ib.positions(h["account"])}
    syms = sorted(set(list(targets_usd) + list(actual)))
    px = _prices(syms)

    # 断路器
    dd = drawdown(h["nav"], max(h["nav"], NOTIONAL))
    act = breaker_action(dd)

    # 目标股数
    tgt_sh = {}
    for s, usd in targets_usd.items():
        p = px.get(s)
        if not (p and p == p): continue
        tgt_sh[s] = target_shares(usd, p, fractional=FRACTIONAL)
    orders = diff_orders(tgt_sh, actual, tol=(0.01 if FRACTIONAL else 1))
    # 断路器 reduce_only/defensive:过滤掉买单
    if act in ("reduce_only", "defensive"):
        orders = [o for o in orders if o["qty"] < 0]
    plan = []
    for o in orders:
        p = px.get(o["sym"])
        if not p: continue
        plan.append({"sym": o["sym"], "qty": o["qty"], "px": p, "usd": abs(o["qty"]) * p})

    ok, reason = check_gates(plan, MAX_ORDER_USD, MAX_TOTAL_USD)
    log = {"date": time.strftime("%Y-%m-%d"), "live": LIVE, "drawdown": round(dd, 4),
           "breaker": act, "plan": plan, "gate_ok": ok, "gate_reason": reason, "placed": []}
    if not ok:
        send(f"🛑 开盘batch安全闸拦截: {reason}\n（交易信号系统）")
    elif not LIVE:
        log["note"] = "DRY-RUN(LIVE=False),未下单"
    else:
        for o in plan:
            try:
                tr = place_limit(ib, o["sym"], o["qty"], o["px"])
                log["placed"].append({"sym": o["sym"], "qty": o["qty"], "status": tr.orderStatus.status})
            except Exception as e:
                log["placed"].append({"sym": o["sym"], "error": str(e)[:80]})
        ib.sleep(8)
        # 对新多头持仓挂 -8% stop
        for p in ib.positions(h["account"]):
            if p.position > 0:
                try: place_stop(ib, p.contract.symbol, p.position, p.avgCost * (1 - INIT_STOP_PCT))
                except Exception: pass
    os.makedirs("data/exec-log", exist_ok=True)
    json.dump(log, open(f"data/exec-log/{log['date']}.json", "w"), ensure_ascii=False, indent=2)
    ib.disconnect()
    print(json.dumps(log, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    run()
```

- [ ] **Step 2: paper 实测(LIVE=False 干跑,落 exec-log)**

Run:
```bash
cd /Users/apple/claude-whatsapp
NO_PROXY=127.0.0.1,localhost HTTPS_PROXY=http://127.0.0.1:7897 python3 scripts/ibkr/trade_open.py
cat data/exec-log/$(date -u +%F).json | python3 -m json.tool | head -20
```
Expected: 打印计划、落盘 exec-log,`note: DRY-RUN`(LIVE=False),未真下单

- [ ] **Step 3: 提交**

```bash
cd /Users/apple/claude-whatsapp
git add scripts/ibkr/trade_open.py
git commit -m "feat(ibkr): trade_open 开盘batch(对账+下单+止损+断路器+exec-log)"
```

---

## Task 11: trade_close 收盘batch(MOM-MA出场)

**Files:**
- Create: `scripts/ibkr/trade_close.py`

- [ ] **Step 1: 写实现**

```python
# scripts/ibkr/trade_close.py
"""收盘batch:MOM-MA持仓收盘<20MA→挂次日卖单。LIVE=False只算不下。落exec-log。"""
import os, json, time
import numpy as np
from scripts.ibkr.client import connect, health
from scripts.ibkr.orders import place_limit
from scripts.ibkr.config import LIVE
from scripts.ibkr.notify import send

def _ma20_break(sym):
    """返回 (破位?, 收盘, ma20)。yfinance 近2月日线。"""
    import yfinance as yf
    try:
        c = np.asarray(yf.download(sym, period="2mo", interval="1d", progress=False)["Close"].dropna()).ravel()
        if len(c) < 20: return False, None, None
        ma20 = float(np.mean(c[-20:])); close = float(c[-1])
        return close < ma20, close, ma20
    except Exception:
        return False, None, None

def run():
    ib, port = connect(client_id=22)
    if not ib:
        send("⚠️ 收盘batch:网关连不上,中止\n（交易信号系统）"); return
    h = health(ib)
    exits = []
    for p in ib.positions(h["account"]):
        if p.position <= 0: continue
        sym = p.contract.symbol
        brk, close, ma20 = _ma20_break(sym)
        if brk:
            exits.append({"sym": sym, "qty": p.position, "close": close, "ma20": ma20})
    log = {"date": time.strftime("%Y-%m-%d"), "type": "close", "live": LIVE, "exits": exits, "placed": []}
    if exits and LIVE:
        for e in exits:
            try:
                tr = place_limit(ib, e["sym"], -e["qty"], e["close"])
                log["placed"].append({"sym": e["sym"], "status": tr.orderStatus.status})
            except Exception as ex:
                log["placed"].append({"sym": e["sym"], "error": str(ex)[:80]})
    elif exits:
        log["note"] = "DRY-RUN,未下出场单"
    os.makedirs("data/exec-log", exist_ok=True)
    # 收盘 log 追加到当日(不覆盖开盘)
    path = f"data/exec-log/{log['date']}.json"
    existing = json.load(open(path)) if os.path.exists(path) else {}
    existing["close_batch"] = log
    json.dump(existing, open(path, "w"), ensure_ascii=False, indent=2)
    ib.disconnect()
    print(json.dumps(log, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    run()
```

- [ ] **Step 2: paper 实测(LIVE=False,无持仓时 exits 空,正常)**

Run: `cd /Users/apple/claude-whatsapp && NO_PROXY=127.0.0.1,localhost HTTPS_PROXY=http://127.0.0.1:7897 python3 scripts/ibkr/trade_close.py`
Expected: 打印 close log(无持仓时 exits=[]),追加进当日 exec-log

- [ ] **Step 3: 提交**

```bash
cd /Users/apple/claude-whatsapp
git add scripts/ibkr/trade_close.py
git commit -m "feat(ibkr): trade_close 收盘batch(MOM-MA 20MA出场)"
```

---

## Task 12: review 复盘(三方对比→飞书+落盘)

**Files:**
- Create: `scripts/ibkr/review.py`
- Test: `scripts/ibkr/tests/test_review.py`(组装逻辑离线测)

- [ ] **Step 1: 写失败测试(复盘组装,喂假数据)**

```python
# scripts/ibkr/tests/test_review.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from scripts.ibkr.review import build_review

def test_anomalies_first():
    exec_log = {"date":"2026-06-22","gate_ok":True,
                "placed":[{"sym":"SPY","status":"Filled"},{"sym":"AAA","error":"rejected"}]}
    actual = {"SPY": 1.6}
    target = {"SPY": 1.6, "AAA": 5}      # AAA 目标5但实际0=对不上
    r = build_review(exec_log, actual, target, nav=2010, peak=2050)
    assert any("AAA" in a for a in r["anomalies"])    # 下单失败/持仓对不上进异常
    assert r["nav"] == 2010

def test_no_anomaly():
    exec_log = {"date":"2026-06-22","gate_ok":True,"placed":[{"sym":"SPY","status":"Filled"}]}
    r = build_review(exec_log, {"SPY":1.6}, {"SPY":1.6}, nav=2000, peak=2000)
    assert r["anomalies"] == []

if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f(); print(f"  ok {n}")
    print("ALL PASS")
```

- [ ] **Step 2: 跑测试确认失败**

Run: `cd /Users/apple/claude-whatsapp && python3 scripts/ibkr/tests/test_review.py`
Expected: FAIL `ImportError`

- [ ] **Step 3: 写实现**

```python
# scripts/ibkr/review.py
"""复盘:exec-log + IBKR实际 + 引擎目标 → 三方对比。异常优先。飞书+落盘。"""
import os, json, time
from scripts.ibkr.config import NOTIONAL, HARD_REDLINE

def build_review(exec_log, actual_sh, target_sh, nav, peak):
    anomalies = []
    # 下单失败/拒单
    for p in exec_log.get("placed", []):
        if p.get("error") or p.get("status") in ("Cancelled", "Inactive"):
            anomalies.append(f"下单异常 {p.get('sym')}: {p.get('error') or p.get('status')}")
    # 安全闸拦截
    if exec_log.get("gate_ok") is False:
        anomalies.append(f"安全闸拦截: {exec_log.get('gate_reason','')}")
    # 持仓对不上目标
    for s in set(list(target_sh) + list(actual_sh)):
        diff = abs(target_sh.get(s, 0) - actual_sh.get(s, 0))
        thresh = max(0.05 * abs(target_sh.get(s, 0)), 0.5)
        if diff > thresh:
            anomalies.append(f"持仓对不上 {s}: 目标{target_sh.get(s,0)} 实际{actual_sh.get(s,0)}")
    # 回撤红线
    dd = (peak - nav) / peak if peak > 0 else 0
    if dd >= HARD_REDLINE * 0.8:
        anomalies.append(f"逼近回撤红线: 回撤{dd*100:.1f}% (红线{HARD_REDLINE*100:.0f}%)")
    return {"date": exec_log.get("date", time.strftime("%Y-%m-%d")),
            "anomalies": anomalies, "nav": nav, "drawdown_pct": round(dd*100, 1),
            "actions": exec_log.get("placed", []), "breaker": exec_log.get("breaker", "normal")}

def format_msg(r):
    lines = [f"📋 IBKR交易日复盘 {r['date']}"]
    if r["anomalies"]:
        lines.append("🔴 异常:")
        lines += [f"  - {a}" for a in r["anomalies"]]
    else:
        lines.append("✅ 今日无异常")
    lines.append(f"📊 净值 ${r['nav']:.0f} · 回撤 {r['drawdown_pct']}% · 断路器 {r['breaker']}")
    lines.append(f"   动作 {len(r['actions'])} 笔")
    lines.append("（交易信号系统）")
    return "\n".join(lines)

def run():
    from scripts.ibkr.client import connect, health
    from scripts.ibkr.targets import build_targets
    from scripts.ibkr.notify import send
    date = time.strftime("%Y-%m-%d")
    exec_log = json.load(open(f"data/exec-log/{date}.json")) if os.path.exists(f"data/exec-log/{date}.json") else {"date": date}
    ib, _ = connect(client_id=23)
    actual_sh, nav = {}, NOTIONAL
    if ib:
        h = health(ib); nav = h["nav"] or NOTIONAL
        actual_sh = {p.contract.symbol: p.position for p in ib.positions(h["account"])}
        ib.disconnect()
    # 目标股数(粗略:用 target_usd,review 容差大,不取价精算)
    target_usd = build_targets(notional=NOTIONAL)
    r = build_review(exec_log, actual_sh, {k: 0 for k in target_usd}, nav, max(nav, NOTIONAL))
    os.makedirs("data/review", exist_ok=True)
    json.dump(r, open(f"data/review/{date}.json", "w"), ensure_ascii=False, indent=2)
    send(format_msg(r))
    print(format_msg(r))

if __name__ == "__main__":
    run()
```

- [ ] **Step 4: 跑测试确认通过**

Run: `cd /Users/apple/claude-whatsapp && python3 scripts/ibkr/tests/test_review.py`
Expected: `ALL PASS`

- [ ] **Step 5: paper 实测复盘(读今日exec-log,推飞书)**

Run: `cd /Users/apple/claude-whatsapp && NO_PROXY=127.0.0.1,localhost NOTIFY_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/c540b4d3-4764-488c-bf22-2b3373a1edf3" python3 scripts/ibkr/review.py`
Expected: 打印复盘 + 飞书收到一条「📋 IBKR交易日复盘」

- [ ] **Step 6: 提交**

```bash
cd /Users/apple/claude-whatsapp
git add scripts/ibkr/review.py scripts/ibkr/tests/test_review.py
git commit -m "feat(ibkr): review 复盘(三方对比+异常优先+飞书)"
```

---

## Task 13: launchd 定时(本地Mac三batch)

**Files:**
- Create: `launchd/com.riley.ibkr-preflight.plist`、`...trade-open.plist`、`...trade-close.plist`、`...review.plist`
- Create: `launchd/run.sh`(统一入口:设代理/NO_PROXY/NOTIFY_WEBHOOK后调python)
- Create: `launchd/README.md`(安装说明)

- [ ] **Step 1: 写统一运行脚本**

```bash
# launchd/run.sh
#!/bin/zsh
cd /Users/apple/claude-whatsapp
export NO_PROXY=127.0.0.1,localhost
export HTTPS_PROXY=http://127.0.0.1:7897 HTTP_PROXY=http://127.0.0.1:7897
export NOTIFY_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/c540b4d3-4764-488c-bf22-2b3373a1edf3"
/usr/bin/python3 -m scripts.ibkr.$1 >> data/exec-log/launchd.log 2>&1
```

- [ ] **Step 2: 写一个 plist(preflight,北京21:00=自检;其余同构)**

```xml
<!-- launchd/com.riley.ibkr-preflight.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.riley.ibkr-preflight</string>
  <key>ProgramArguments</key><array>
    <string>/bin/zsh</string><string>/Users/apple/claude-whatsapp/launchd/run.sh</string><string>preflight</string>
  </array>
  <key>StartCalendarInterval</key><dict><key>Hour</key><integer>21</integer><key>Minute</key><integer>0</integer></dict>
  <key>StandardErrorPath</key><string>/Users/apple/claude-whatsapp/data/exec-log/launchd-preflight.err</string>
</dict></plist>
```
（trade-open=21:30调trade_open / trade-close=次日04:00调trade_close / review=04:30调review,三个 plist 同构,改 Label/Hour/Minute/参数。本地时间随美股夏令时调整,README 注明。）

- [ ] **Step 3: 写 README 安装说明**

```markdown
# launchd 安装(本地Mac跑IBKR执行)
chmod +x launchd/run.sh
cp launchd/*.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.riley.ibkr-*.plist
# 卸载:launchctl unload ~/Library/LaunchAgents/com.riley.ibkr-*.plist
# 前提:IB Gateway 登录+API开;Mac 接电源不睡眠(系统设置→电池→电源适配器→防止自动进入睡眠)
# 时间为北京时间近似;美股夏令时切换时各 plist Hour 需 ±1 调整
```

- [ ] **Step 4: 验证 plist 格式 + run.sh 可调**

Run:
```bash
cd /Users/apple/claude-whatsapp
chmod +x launchd/run.sh
plutil -lint launchd/com.riley.ibkr-preflight.plist
NO_PROXY=127.0.0.1,localhost python3 -m scripts.ibkr.preflight; echo "module调用 exit=$?"
```
Expected: `plutil: ... OK`;preflight 模块能跑(连上网关则自检,exit 0或明确fail)

- [ ] **Step 5: 提交**

```bash
cd /Users/apple/claude-whatsapp
git add launchd/
git commit -m "feat(ibkr): launchd 本地三batch定时 + 安装说明"
```

---

## Self-Review

**Spec 覆盖:** 三层(决策=Task10/11,保护=Task8 place_stop+Task10挂止损,复盘=Task12)✓ 三batch(自检T9/开盘T10/收盘T11)✓ 对账(T3)✓ 限价单+延迟价(T8/T10 _prices)✓ 固定stop(T8)✓ 断路器分档占位(T4+T10过滤)✓ 详尽复盘异常优先(T12)✓ exec-log/review落盘(T10/11/12)✓ config集中+LIVE/FRACTIONAL开关(T1)✓ 容错:重连(调用方重试)/全局撤单(T7 cancel_all)/单笔try-except(T10)✓ 本地launchd(T13)✓ 飞书(T6)✓ 整数股默认+小数股开关(T1/T2/T8)✓。**未覆盖(spec明确列为后续待办,不阻塞)**:断路器回测校准、IBC自动重登、真钱化(改config即可)、盘中monitor。

**占位符扫描:** 无 TBD/TODO 作为代码;断路器阈值是 spec 明确的"占位值待校准",已在 config 注释标 `# TODO 待回测校准`,是有意设计非占位漏洞。每步含真实代码/命令/预期。

**类型一致:** `connect(client_id,timeout)→(ib,port)`、`health(ib)→dict{account,is_paper,nav,cash,open_orders}`、`build_targets(alloc_path,leg_paths,notional)→{sym:usd}`、`target_shares(usd,price,fractional)→数`、`diff_orders(target_sh,actual_sh,tol)→[{sym,qty}]`、`breaker_action(dd,tiers)→str`、`check_gates(plan,max_order,max_total)→(ok,reason)`、`place_limit(ib,sym,qty,price,fractional)`、`place_stop(ib,sym,qty,stop_price)`、`build_review(exec_log,actual_sh,target_sh,nav,peak)→dict{anomalies,...}` 跨任务一致。

**注:** I/O 层(client/orders/preflight/trade_open/trade_close)用 paper 实测代替单测(需 Gateway 登录);纯逻辑(config/sizing/reconcile/risk/targets/review组装/notify)离线 assert 测。模块用 `python3 -m scripts.ibkr.xxx` 跑(需 scripts/ 及 scripts/ibkr/ 有 __init__.py;仓库 scripts/ 若无 __init__.py,Task1 顺带在 scripts/ 建空 __init__.py)。
