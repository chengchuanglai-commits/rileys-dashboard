# 动态配置引擎 Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 给所有策略腿算"信念分"，按 30-70% 动态滑动配主动 vs 指数(SPY)，并在 dashboard 可视化，全程盈利为中心、零额外 API 成本。

**Architecture:** 纯计算脚本 `compute-allocation.py` 读各腿 `portfolio_*.json` 的前向已平仓交易，复用共享 frac20 复利模块算每腿前向 alpha 与信念分(sample×alpha×robustness)，输出 `data/allocation.json`+`dashboard/allocation.js`；`compare-compounded.py` 扩展出每腿复利净值曲线；dashboard 用自包含 SVG/CSS 渲染 4 块（配置环图/信念 gauge/净值曲线/Phase 追踪）。

**Tech Stack:** Python 3.12（标准库 + yfinance 仅 SPY 振幅）、原生 JS + 内联 SVG（不引图表库）、Playwright 自检。

设计依据：`docs/superpowers/specs/2026-06-20-dynamic-allocation-engine-design.md`。
测试用纯 assert 脚本（`python3` 直接跑，不依赖 pytest，匹配本仓库 scripts 风格）。

---

## File Structure

- `scripts/portfolio_compound.py`（新）：共享 frac20 复利——`compound_frac20()` + `compound_frac20_curve()`。单一职责：把 (signal_date, close_date, pnl_pct) 交易流按"每仓20%净值、最多5并发、现金约束"复利成净值/曲线。
- `scripts/compute-allocation.py`（新）：信念分配引擎。纯函数 `conviction_score/active_fraction/active_weights/leg_metrics` + `main()` 写 `data/allocation.json`+`dashboard/allocation.js`。
- `scripts/compare-compounded.py`（改）：复用 `portfolio_compound`，新增写 `dashboard/compounded-curves.js`（各腿+SPY 复利曲线）。
- `scripts/tests/test_compound.py`、`test_allocation.py`（新）：纯 assert 测试。
- `dashboard/index.html`（改）：新增"配置引擎"板块 4 个自包含组件 + 加载 allocation.js/compounded-curves.js + BUILD bump。
- `.github/workflows/trading-signals.yml`（改）：信号步骤后跑 compute-allocation + compare-compounded。

常量集中在各脚本顶部：`N_FULL=40, ALPHA_TARGET=0.10, ACTIVE_FLOOR=0.30, ACTIVE_CEILING=0.70, FRAC=0.20, MAX_CONC=5, MOMMA_PRIOR=0.10, PHASE2_MKT=0.10`。

---

## Task 1: 共享 frac20 复利模块

**Files:**
- Create: `scripts/portfolio_compound.py`
- Test: `scripts/tests/test_compound.py`

- [ ] **Step 1: 写失败测试**

```python
# scripts/tests/test_compound.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from portfolio_compound import compound_frac20, compound_frac20_curve

def test_single_winning_trade_compounds():
    # 一笔 +10%：$2000 → 开 20%=$400 → 平仓 $400*1.10=$440 → 终值 $2040
    trades = [("2026-06-01", "2026-06-03", 10.0)]
    assert abs(compound_frac20(trades, init=2000, frac=0.20, max_conc=5) - 2040.0) < 0.01

def test_max_concurrency_skips_excess():
    # 6 笔同一天开、晚平：max_conc=5 → 第6笔被跳过(现金/并发约束)
    trades = [("2026-06-01", "2026-06-30", 5.0)] * 6
    final = compound_frac20(trades, init=2000, frac=0.20, max_conc=5)
    # 5 笔各占 20%*递减净值,均 +5%;第6笔不开 → 终值 < 6 笔全开的情形
    assert final > 2000 and final < 2000 * (1.05)

def test_curve_returns_dated_points():
    trades = [("2026-06-01", "2026-06-03", 10.0)]
    curve = compound_frac20_curve(trades, init=2000, frac=0.20, max_conc=5)
    assert curve[-1][0] == "2026-06-03" and abs(curve[-1][1] - 2040.0) < 0.01

if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"): fn(); print(f"  ok {name}")
    print("ALL PASS")
```

- [ ] **Step 2: 跑测试确认失败**

Run: `cd /Users/apple/claude-whatsapp && python3 scripts/tests/test_compound.py`
Expected: FAIL，`ModuleNotFoundError: No module named 'portfolio_compound'`

- [ ] **Step 3: 写实现**

```python
# scripts/portfolio_compound.py
"""共享 frac20 复利:把交易流按'每仓20%当前净值、最多MAX_CONC并发、现金约束'复利。"""

def _run(trades, init, frac, max_conc):
    """返回 (final_equity, curve[(date,equity)])。trades=[(signal_date, close_date, pnl_pct)]。"""
    trades = sorted(trades, key=lambda t: (t[0], t[1]))
    cash = float(init)
    open_caps = []   # (close_date, capital, pnl_pct)
    curve = []
    def equity():
        return cash + sum(c for _, c, _ in open_caps)
    for sd, cd, pct in trades:
        still = []
        for ocd, cap, opct in open_caps:
            if ocd <= sd:
                cash += cap * (1 + opct / 100)
                curve.append((ocd, round(cash + sum(c for _, c, _ in still), 2)))
            else:
                still.append((ocd, cap, opct))
        open_caps = still
        if len(open_caps) >= max_conc:
            continue
        eq = equity()
        size = min(frac * eq, cash)
        if size < 5:
            continue
        cash -= size
        open_caps.append((cd, size, pct))
    for ocd, cap, opct in sorted(open_caps, key=lambda x: x[0]):
        cash += cap * (1 + opct / 100)
        curve.append((ocd, round(cash, 2)))
    return round(cash, 2), curve

def compound_frac20(trades, init=2000, frac=0.20, max_conc=5):
    return _run(trades, init, frac, max_conc)[0]

def compound_frac20_curve(trades, init=2000, frac=0.20, max_conc=5):
    return _run(trades, init, frac, max_conc)[1]
```

- [ ] **Step 4: 跑测试确认通过**

Run: `cd /Users/apple/claude-whatsapp && python3 scripts/tests/test_compound.py`
Expected: `ALL PASS`

- [ ] **Step 5: 提交**

```bash
cd /Users/apple/claude-whatsapp
git add scripts/portfolio_compound.py scripts/tests/test_compound.py
git commit -m "feat: 共享 frac20 复利模块 + 测试"
```

---

## Task 2: compare-compounded 复用模块 + 输出净值曲线

**Files:**
- Modify: `scripts/compare-compounded.py`（删内联 `compound_frac20`，改 import；末尾新增写曲线）

- [ ] **Step 1: 改 import + 删内联函数**

把文件内的 `def compound_frac20(...)` 整段删除，顶部加：
```python
from portfolio_compound import compound_frac20, compound_frac20_curve
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
```
（`extract_closed` 返回的就是 `(signal_date, close_date, pnl_pct)`，签名兼容。`compound_frac20(trades)` 之前返回三元组，现在只返回终值——把调用处 `final, n, wr = compound_frac20(tr)` 改为：`final = compound_frac20(tr); n = len(tr); wr = round(len([t for t in tr if t[2]>0])/len(tr)*100,1) if tr else 0`。）

- [ ] **Step 2: 末尾新增写曲线到 dashboard/compounded-curves.js**

在 `main()` 末尾 `print(...)` 之前插入：
```python
    import json as _json
    curves = {}
    for key, name in LEGS.items():
        path = f"data/portfolio_{key}.json"
        if not os.path.exists(path): continue
        tr = extract_closed(path)
        if not tr: continue
        curves[key] = {"name": name, "points": compound_frac20_curve(tr)}
    # SPY 复利曲线退化为单点(买入持有),用 portfolio_spy 终值
    spy_pv = None
    try: spy_pv = _json.load(open("data/portfolio_spy.json"))["stats"]["portfolio_value"]
    except Exception: pass
    out = {"init": INIT, "spy_final": spy_pv, "curves": curves}
    with open("dashboard/compounded-curves.js", "w", encoding="utf-8") as f:
        f.write(f"window.COMPOUNDED_CURVES = {_json.dumps(out, ensure_ascii=False)};\n")
```

- [ ] **Step 3: 跑确认正常 + 产物生成**

Run: `cd /Users/apple/claude-whatsapp && python3 scripts/compare-compounded.py && node -e "require('./dashboard/compounded-curves.js'); console.log('curves keys:', Object.keys(COMPOUNDED_CURVES.curves).length)"`
Expected: 排行表照常打印；`curves keys: >0`

- [ ] **Step 4: 提交**

```bash
cd /Users/apple/claude-whatsapp
git add scripts/compare-compounded.py dashboard/compounded-curves.js
git commit -m "feat: compare-compounded 复用复利模块 + 输出净值曲线"
```

---

## Task 3: 信念分 + 配置纯函数

**Files:**
- Create: `scripts/compute-allocation.py`（先只放纯函数）
- Test: `scripts/tests/test_allocation.py`

- [ ] **Step 1: 写失败测试**

```python
# scripts/tests/test_allocation.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from importlib import import_module
ca = import_module("compute-allocation".replace("-", "_")) if False else None
# 文件名带连字符,用 runpy 不便;改为同名下划线导入失败 → 直接 exec
import types
mod = types.ModuleType("alloc")
exec(open(os.path.join(os.path.dirname(__file__), "..", "compute-allocation.py")).read(), mod.__dict__)

def test_conviction_zero_when_no_alpha():
    assert mod.conviction_score(n=40, alpha=-0.05, robust_ok=True) == 0.0

def test_conviction_zero_when_not_robust():
    assert mod.conviction_score(n=40, alpha=0.10, robust_ok=False) == 0.0

def test_conviction_full_when_all_strong():
    # n=40→sample1, alpha=0.10→edge1, robust→1 ⇒ 1.0
    assert abs(mod.conviction_score(n=40, alpha=0.10, robust_ok=True) - 1.0) < 1e-9

def test_conviction_scales_with_sample():
    # n=20→sample0.5, alpha=0.10→edge1 ⇒ 0.5
    assert abs(mod.conviction_score(n=20, alpha=0.10, robust_ok=True) - 0.5) < 1e-9

def test_active_fraction_floor_and_ceiling():
    assert abs(mod.active_fraction(0.0) - 0.30) < 1e-9      # 零信念=地板
    assert abs(mod.active_fraction(1.0) - 0.70) < 1e-9      # 满信念=天花板

def test_active_weights_prior_carries_floor():
    # 全零信念:只有 MOM-MA 有先验0.1 → 拿满主动
    w = mod.active_weights({"momma": 0.0, "bq": 0.0}, {"momma": 0.10, "bq": 0.0})
    assert abs(w["momma"] - 1.0) < 1e-9 and abs(w["bq"] - 0.0) < 1e-9

if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"): fn(); print(f"  ok {name}")
    print("ALL PASS")
```

- [ ] **Step 2: 跑测试确认失败**

Run: `cd /Users/apple/claude-whatsapp && python3 scripts/tests/test_allocation.py`
Expected: FAIL，`FileNotFoundError` 或 `NameError: conviction_score`

- [ ] **Step 3: 写纯函数实现**

```python
# scripts/compute-allocation.py
"""信念分配引擎:每腿 conviction(sample×alpha×robustness) → 主动30-70%滑动 → 各腿按信念权重。"""
N_FULL = 40
ALPHA_TARGET = 0.10
ACTIVE_FLOOR = 0.30
ACTIVE_CEILING = 0.70
MOMMA_PRIOR = 0.10

def _clip(x, lo, hi):
    return max(lo, min(hi, x))

def conviction_score(n, alpha, robust_ok, n_full=N_FULL, alpha_target=ALPHA_TARGET):
    if not robust_ok or alpha <= 0:
        return 0.0
    sample = min(n / n_full, 1.0)
    edge = _clip(alpha / alpha_target, 0.0, 1.0)
    return round(sample * edge * 1.0, 4)

def active_fraction(max_conviction, floor=ACTIVE_FLOOR, ceiling=ACTIVE_CEILING):
    return round(floor + (ceiling - floor) * _clip(max_conviction, 0.0, 1.0), 4)

def active_weights(convictions, priors):
    raw = {k: convictions.get(k, 0.0) + priors.get(k, 0.0) for k in convictions}
    s = sum(raw.values())
    if s <= 0:
        return {k: 0.0 for k in convictions}
    return {k: round(v / s, 4) for k, v in raw.items()}
```

- [ ] **Step 4: 跑测试确认通过**

Run: `cd /Users/apple/claude-whatsapp && python3 scripts/tests/test_allocation.py`
Expected: `ALL PASS`

- [ ] **Step 5: 提交**

```bash
cd /Users/apple/claude-whatsapp
git add scripts/compute-allocation.py scripts/tests/test_allocation.py
git commit -m "feat: 信念分/主动占比/权重 纯函数 + 测试"
```

---

## Task 4: 每腿前向指标 (n / alpha / robustness)

**Files:**
- Modify: `scripts/compute-allocation.py`（新增 `leg_metrics`）
- Modify: `scripts/tests/test_allocation.py`（新增测试）

- [ ] **Step 1: 追加失败测试**

在 `test_allocation.py` 的 `if __name__` 之前追加：
```python
def test_leg_metrics_alpha_and_robust():
    # 3 笔: +30,+30,-5(pct);frac20复利前向 > spy → alpha>0;去掉最赚2笔(两个+30)剩-5 → 不robust
    port = {"closed_positions": [
        {"signal_date": "2026-06-01", "close_date": "2026-06-02", "final_pnl_pct": 30.0},
        {"signal_date": "2026-06-03", "close_date": "2026-06-04", "final_pnl_pct": 30.0},
        {"signal_date": "2026-06-05", "close_date": "2026-06-06", "final_pnl_pct": -5.0},
    ]}
    n, alpha, robust, final = mod.leg_metrics(port, spy_ret_pct=0.0)
    assert n == 3
    assert alpha > 0          # 复利前向为正,SPY=0
    assert robust is False     # 去掉两笔+30只剩-5
```

- [ ] **Step 2: 跑确认失败**

Run: `cd /Users/apple/claude-whatsapp && python3 scripts/tests/test_allocation.py`
Expected: FAIL，`NameError: ... leg_metrics`

- [ ] **Step 3: 实现 leg_metrics**

在 `compute-allocation.py` 顶部加 import：
```python
import os, sys, json, math
sys.path.insert(0, os.path.dirname(__file__))
from portfolio_compound import compound_frac20
```
并新增：
```python
INIT = 2000.0

def _closed_trades(port):
    out = []
    for p in port.get("closed_positions", []):
        pct = p.get("final_pnl_pct")
        if pct is None:
            rp, cost = p.get("realized_pnl_usd"), (p.get("actual_position_usd") or p.get("allocated_usd"))
            if rp is not None and cost: pct = rp / cost * 100
        if pct is None or (isinstance(pct, float) and math.isnan(pct)): continue
        out.append((p.get("signal_date", ""), p.get("close_date", p.get("signal_date", "")), float(pct)))
    return out

def leg_metrics(port, spy_ret_pct):
    """返回 (n, alpha, robust_ok, final_eq)。alpha = 该腿frac20复利前向收益% − SPY同期%(小数)。"""
    trades = _closed_trades(port)
    n = len(trades)
    if n == 0:
        return 0, 0.0, False, INIT
    final = compound_frac20(trades, init=INIT)
    ret_pct = (final / INIT - 1) * 100
    alpha = (ret_pct - spy_ret_pct) / 100.0
    # robustness:去掉最赚2笔(按pct),剩余复利仍 > 起始
    rest = sorted(trades, key=lambda t: t[2])[:-2] if n > 2 else []
    robust_ok = compound_frac20(rest, init=INIT) > INIT if rest else False
    return n, alpha, robust_ok, final
```

- [ ] **Step 4: 跑确认通过**

Run: `cd /Users/apple/claude-whatsapp && python3 scripts/tests/test_allocation.py`
Expected: `ALL PASS`

- [ ] **Step 5: 提交**

```bash
cd /Users/apple/claude-whatsapp
git add scripts/compute-allocation.py scripts/tests/test_allocation.py
git commit -m "feat: leg_metrics 前向 n/alpha/robustness"
```

---

## Task 5: main() — 组装 + 写 allocation.json/js + Phase2 进度

**Files:**
- Modify: `scripts/compute-allocation.py`（新增 `main()` + Phase2 + SPY 振幅）

- [ ] **Step 1: 实现 main()**

在 `compute-allocation.py` 末尾加：
```python
LEGS = {"momma":"MOM-MA·动量+20MA","momh":"MOM-H·动量+H","bq":"B-quant·多因子","bai":"B-AI·多因子+DS",
        "h":"H·小盘Haiku","hds":"H-DS·小盘DS","mn":"H-广池·晨报","c":"C·B+跳空"}
TRADEABLE = {"momma", "bq"}   # real-money 起步只投可手动低换手腿
PHASE2_MKT = 0.10

def _spy_forward_ret():
    try:
        s = json.load(open("data/portfolio_spy.json"))["stats"]
        return (s.get("portfolio_value", INIT) / INIT - 1) * 100
    except Exception:
        return 0.0

def _spy_peak_trough():
    """SPY 前向峰谷振幅(yfinance,近6mo),判 Phase2 市场条件。失败返回0。"""
    try:
        import numpy as np, yfinance as yf
        c = np.asarray(yf.download("SPY", period="6mo", interval="1d", progress=False)["Close"].dropna()).ravel()
        if len(c) < 5: return 0.0
        return float((c.max() - c.min()) / c.max())
    except Exception:
        return 0.0

def main():
    spy_ret = _spy_forward_ret()
    convictions, priors, metrics = {}, {}, {}
    for key, name in LEGS.items():
        path = f"data/portfolio_{key}.json"
        if not os.path.exists(path): continue
        port = json.load(open(path))
        n, alpha, robust, final = leg_metrics(port, spy_ret)
        conv = conviction_score(n, alpha, robust)
        convictions[key] = conv
        priors[key] = MOMMA_PRIOR if key == "momma" else 0.0
        metrics[key] = {"name": name, "n": n, "alpha_pct": round(alpha*100,2),
                        "robust": robust, "conviction": conv, "fwd_ret_pct": round((final/INIT-1)*100,2),
                        "tradeable": key in TRADEABLE}
    max_conv = max(convictions.values()) if convictions else 0.0
    active = active_fraction(max_conv)
    weights = active_weights(convictions, priors)
    # 各腿最终占总资金% = active × 主动内部权重(只对 tradeable 归一上钱;其余腿权重展示但置灰)
    tw = {k: weights[k] for k in weights if k in TRADEABLE}
    tsum = sum(tw.values()) or 1.0
    final_alloc = {k: round(active * (tw[k]/tsum), 4) for k in tw}
    # Phase2 进度
    passed_legs = [k for k,m in metrics.items() if m["n"]>=40 and m["alpha_pct"]>0 and m["robust"]]
    mkt = _spy_peak_trough()
    phase2 = {"evidence_ok": len(passed_legs)>0, "passed_legs": passed_legs,
              "market_amp_pct": round(mkt*100,1), "market_ok": mkt>=PHASE2_MKT,
              "complete": len(passed_legs)>0 and mkt>=PHASE2_MKT}
    out = {"generated": __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M"),
           "spy_fwd_ret_pct": round(spy_ret,2), "max_conviction": round(max_conv,4),
           "active_pct": active, "index_pct": round(1-active,4),
           "legs": metrics, "weights": weights, "final_allocation": final_alloc,
           "tradeable": sorted(TRADEABLE), "phase2": phase2,
           "params": {"floor":ACTIVE_FLOOR,"ceiling":ACTIVE_CEILING,"n_full":N_FULL,"alpha_target":ALPHA_TARGET}}
    json.dump(out, open("data/allocation.json","w"), ensure_ascii=False, indent=2)
    with open("dashboard/allocation.js","w",encoding="utf-8") as f:
        f.write(f"window.ALLOCATION = {json.dumps(out, ensure_ascii=False)};\n")
    print(f"主动{active*100:.0f}% / 指数{(1-active)*100:.0f}% · 最强信念{max_conv:.2f} · Phase2 {'✅' if phase2['complete'] else '进行中'}")
    print("  tradeable 配置:", {k: f"{v*100:.0f}%" for k,v in final_alloc.items()})

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 跑确认产物生成 + 合法**

Run: `cd /Users/apple/claude-whatsapp && python3 scripts/compute-allocation.py && node -e "require('./dashboard/allocation.js'); const a=ALLOCATION; console.log('active', a.active_pct, 'legs', Object.keys(a.legs).length, 'phase2', a.phase2.complete)"`
Expected: 打印当前配置（现在应≈主动30%/指数70%，Phase2 进行中）；node 打出 `active 0.3 legs >0 phase2 false`

- [ ] **Step 3: 跑全部测试回归**

Run: `cd /Users/apple/claude-whatsapp && python3 scripts/tests/test_compound.py && python3 scripts/tests/test_allocation.py`
Expected: 两个 `ALL PASS`

- [ ] **Step 4: 提交**

```bash
cd /Users/apple/claude-whatsapp
git add scripts/compute-allocation.py data/allocation.json dashboard/allocation.js
git commit -m "feat: compute-allocation main 组装 + allocation.json/js + Phase2 进度"
```

---

## Task 6: Dashboard 4 块可视化（自包含 SVG/CSS）

**Files:**
- Modify: `dashboard/index.html`（新增"配置引擎"板块 + 加载两个 js + BUILD bump）

- [ ] **Step 1: 加载数据脚本**

在 index.html 已有的 `document.write(...portfolio-*.js...)` 同区域追加：
```html
<script src="allocation.js"></script>
<script src="compounded-curves.js"></script>
```

- [ ] **Step 2: 加配置引擎板块容器**

在投资板块合适位置插入：
```html
<section id="alloc-engine" style="margin:24px 0;padding:16px;border:1px solid #e5e7eb;border-radius:12px">
  <h3 style="margin:0 0 12px">⚙️ 动态配置引擎 <span id="alloc-phase" style="font-size:12px;color:#6b7280"></span></h3>
  <div style="display:flex;flex-wrap:wrap;gap:24px">
    <div id="alloc-donut"></div>
    <div id="alloc-gauges" style="flex:1;min-width:260px"></div>
  </div>
  <div id="alloc-curves" style="margin-top:16px"></div>
</section>
```

- [ ] **Step 3: 加渲染脚本（自包含,内联 SVG）**

在 index.html 末尾 `</body>` 前加：
```html
<script>
(function(){
  var A = window.ALLOCATION, C = window.COMPOUNDED_CURVES;
  if(!A) return;
  // ① 配置环图(主动 vs 指数 + 主动内部)
  var act=A.active_pct, idx=A.index_pct;
  var donut='<svg width="180" height="180" viewBox="0 0 36 36">';
  var seg=[['指数',idx,'#94a3b8'],['主动',act,'#6366f1']], off=0;
  seg.forEach(function(s){var d=s[1]*100;donut+='<circle cx="18" cy="18" r="15.9" fill="none" stroke="'+s[2]+'" stroke-width="3.5" stroke-dasharray="'+d+' '+(100-d)+'" stroke-dashoffset="'+(25-off)+'"/>';off+=d;});
  donut+='<text x="18" y="17" text-anchor="middle" font-size="4">主动'+Math.round(act*100)+'%</text><text x="18" y="22" text-anchor="middle" font-size="3" fill="#6b7280">指数'+Math.round(idx*100)+'%</text></svg>';
  document.getElementById('alloc-donut').innerHTML='<div style="text-align:center">'+donut+'<div style="font-size:12px;color:#6b7280">SPY前向 '+A.spy_fwd_ret_pct+'%</div></div>';
  // ② 信念 gauge(各腿)
  var g='<table style="width:100%;border-collapse:collapse;font-size:13px"><tr style="color:#6b7280"><td>腿</td><td>信念</td><td>n</td><td>alpha</td><td>稳健</td><td>占资金</td></tr>';
  Object.keys(A.legs).forEach(function(k){var m=A.legs[k];var fa=A.final_allocation[k];
    var bar='<div style="background:#eef;border-radius:4px;width:80px;height:8px;display:inline-block"><div style="background:#6366f1;height:8px;border-radius:4px;width:'+Math.round(m.conviction*80)+'px"></div></div>';
    g+='<tr style="'+(m.tradeable?'':'opacity:.5')+'"><td>'+m.name+'</td><td>'+bar+' '+m.conviction+'</td><td>'+m.n+'</td><td>'+m.alpha_pct+'%</td><td>'+(m.robust?'✓':'✗')+'</td><td>'+(fa!=null?Math.round(fa*100)+'%':'纸面')+'</td></tr>';});
  g+='</table>';
  document.getElementById('alloc-gauges').innerHTML=g;
  // ③ 复利净值曲线 vs SPY
  if(C&&C.curves){
    var W=560,H=160,pad=24,all=[];Object.values(C.curves).forEach(function(c){c.points.forEach(function(p){all.push(p[1]);});});
    if(C.spy_final)all.push(C.spy_final); all.push(C.init);
    var mn=Math.min.apply(null,all),mx=Math.max.apply(null,all),rng=(mx-mn)||1;
    var dates=[];Object.values(C.curves).forEach(function(c){c.points.forEach(function(p){dates.push(p[0]);});});
    dates=dates.sort();var d0=dates[0],d1=dates[dates.length-1];
    function xx(d){return pad+(W-2*pad)*((new Date(d)-new Date(d0))/((new Date(d1)-new Date(d0))||1));}
    function yy(v){return H-pad-(H-2*pad)*((v-mn)/rng);}
    var svg='<svg width="'+W+'" height="'+H+'" style="max-width:100%">';
    var cols=['#6366f1','#0d9488','#db2777','#ca8a04','#0891b2','#64748b','#16a34a','#f97316'],ci=0;
    Object.keys(C.curves).forEach(function(k){var pts=C.curves[k].points;if(!pts.length)return;
      var dd='M '+xx(C.init&&pts[0]?d0:pts[0][0])+' '+yy(C.init);pts.forEach(function(p){dd+=' L '+xx(p[0])+' '+yy(p[1]);});
      svg+='<path d="'+dd+'" fill="none" stroke="'+cols[ci%cols.length]+'" stroke-width="1.5"/>';ci++;});
    if(C.spy_final){svg+='<line x1="'+pad+'" y1="'+yy(C.spy_final)+'" x2="'+(W-pad)+'" y2="'+yy(C.spy_final)+'" stroke="#000" stroke-dasharray="3 3" stroke-width="1"/><text x="'+(W-pad)+'" y="'+(yy(C.spy_final)-2)+'" font-size="10" text-anchor="end">SPY</text>';}
    svg+='</svg><div style="font-size:11px;color:#6b7280">frac20 复利净值 vs SPV(虚线)</div>';
    document.getElementById('alloc-curves').innerHTML='<div style="font-weight:600;font-size:13px;margin-bottom:4px">复利净值曲线 vs SPY</div>'+svg;
  }
  // ④ Phase 追踪
  var p2=A.phase2;
  document.getElementById('alloc-phase').textContent='· Phase 1'+(p2.complete?' → 可升级!':' (证据'+(p2.evidence_ok?'✓':'✗')+' / 市场振幅'+p2.market_amp_pct+'%'+(p2.market_ok?'✓':' 需≥10%')+')');
})();
</script>
```

- [ ] **Step 4: BUILD + version 同步 bump**

```bash
cd /Users/apple/claude-whatsapp
V=$(date -u +%Y%m%d%H%M%S)
echo "window.DASHBOARD_VERSION = \"$V\";" > dashboard/version.js
sed -i '' "s/var BUILD=\"[0-9]*\"/var BUILD=\"$V\"/" dashboard/index.html
```

- [ ] **Step 5: Playwright 自检不白屏 + 板块渲染**

```bash
cd /Users/apple/claude-whatsapp
cat > _ac.js <<'EOF'
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();const e=[];p.on('pageerror',x=>e.push(x.message));
await p.goto('file://'+process.cwd()+'/dashboard/index.html',{waitUntil:'networkidle',timeout:30000});await p.waitForTimeout(1500);
const has=await p.evaluate(()=>!!document.getElementById('alloc-engine')&&!!window.ALLOCATION);
console.log('alloc板块+数据:',has,'| 真JS错误:',e.filter(x=>!/rss2json|tradingview|fonts/.test(x)).length);await b.close();})();
EOF
node _ac.js; rm -f _ac.js
```
Expected: `alloc板块+数据: true | 真JS错误: 0`

- [ ] **Step 6: 提交**

```bash
cd /Users/apple/claude-whatsapp
git add dashboard/index.html dashboard/version.js
git commit -m "feat: dashboard 动态配置引擎 4块可视化(环图/信念/曲线/Phase)"
```

---

## Task 7: 接入每日工作流

**Files:**
- Modify: `.github/workflows/trading-signals.yml`（信号步骤后跑 compute-allocation + compare-compounded）

- [ ] **Step 1: 加步骤**

在 `trading-signals.yml` 提交步骤**之前**、各 backfill 步骤之后，加：
```yaml
      - name: 复利曲线
        continue-on-error: true
        run: python scripts/compare-compounded.py
      - name: 动态配置引擎
        continue-on-error: true
        run: python scripts/compute-allocation.py
```
并确保提交步骤的 `git add` 覆盖：`data/allocation.json dashboard/allocation.js dashboard/compounded-curves.js`。

- [ ] **Step 2: 校验 YAML**

Run: `cd /Users/apple/claude-whatsapp && python3 -c "import yaml; yaml.safe_load(open('.github/workflows/trading-signals.yml')); print('YAML ok')"`
Expected: `YAML ok`

- [ ] **Step 3: 提交**

```bash
cd /Users/apple/claude-whatsapp
git add .github/workflows/trading-signals.yml
git commit -m "feat: 工作流接入复利曲线 + 动态配置引擎"
```

---

## Self-Review

**Spec 覆盖：** 信念分(T3)✓ 30-70滑动(T3)✓ 权重+先验(T3)✓ leg_metrics/alpha/robust(T4)✓ active_fraction(T3)✓ main/Phase2/振幅(T5)✓ 4块可视化(T6)✓ 每周重算→工作流(T7)✓ 共享复利(T1/T2)✓。**未覆盖**：每月再平衡/±15%上限/下行对称——这些是 real-money 执行纪律(手动)，引擎每次输出最新目标即满足"下行对称"(重算自动降权)，再平衡节奏属执行手册非代码，记入执行手册不进本plan。

**占位符扫描：** 无 TBD/TODO；每步含真实代码/命令/预期输出。

**类型一致：** `compound_frac20(trades,init,frac,max_conc)`、`leg_metrics→(n,alpha,robust_ok,final)`、`conviction_score(n,alpha,robust_ok)`、`active_fraction(max_conv)`、`active_weights(convictions,priors)`、产物 `window.ALLOCATION`/`window.COMPOUNDED_CURVES` 跨任务一致。

**注**：`compute-allocation.py` 文件名带连字符不可 import，测试用 `exec(open(...).read())` 加载(T3 已写)；脚本间靠 `portfolio_compound.py`(下划线,可 import)共享。
