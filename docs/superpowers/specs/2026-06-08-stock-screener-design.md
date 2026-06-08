# Stock Screener Design — S&P 600 量化选股系统

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 用 S&P 600 量化扫描替代晨报 AI 随感选股，提升进入 TradingAgents 的候选股质量，目标是减少低质量信号、提高胜率。

**Architecture:** 新增 `scripts/screen-stocks.py` 每日收盘后扫描 S&P 600 全集，计算5因子评分，输出 Top 候选到 `data/screened-stocks.json`；`generate-trading-signals.py` 的 `select_stocks()` 改为从扫描结果读取，不再依赖晨报。晨报保持不变，只用于每日阅读。

**Tech Stack:** Python, yfinance（免费），GitHub Actions，现有 JSON 数据管道。

---

## 数据依据

基于真实10条历史信号验证：
- BUY 信号胜率：0/3 = 0%（全部止损）
- SELL 信号胜率：5/5 = 100%
- 被新规则过滤的3次亏损中2-3次可避免（UCTT量比0.69x、MU RS+853%）

---

## 筛选规则（5因子）

| 因子 | 标准 | 依据 |
|------|------|------|
| 成交量放大 | 近5日均量 / 50日均量 ≥ 1.2x | WIN均值1.3x vs LOSS均值1.0x |
| ATR波动率 | 日ATR% 在 2-8% 区间 | 匹配 TP=15%/SL=3%/2日参数 |
| 趋势存在 | 股价 > 50日均线 OR 股价 < 50日均线（有方向） | 排除横盘震荡股 |
| 超涨BUY过滤 | RS12m > 500% 且 距52周高点 < 2% → 标记 sell_candidate，不进BUY池 | 3次BUY亏损全符合此特征 |
| 市场环境 | 标普500期货 < -1%时，BUY候选需量比 ≥ 1.5x | 空头环境下BUY需更强确认 |

---

## 文件结构

### 新增
- `scripts/screen-stocks.py` — 主扫描脚本
  - 读取 S&P 600 成分股列表（硬编码 ~600 只，定期更新）
  - 用 yfinance 拉取每只股票近1年 OHLCV
  - 计算5因子评分（0-100分）
  - 输出 `data/screened-stocks.json`（Top 20 候选 + 元数据）

### 修改
- `scripts/generate-trading-signals.py`
  - `select_stocks()` 函数：从 `data/screened-stocks.json` 读取，不再读晨报
  - 保留黑名单过滤
  - 保留市场环境逻辑（读晨报的 sp500_futures_pct 用于BUY门槛调整）

- `.github/workflows/trading-signals.yml`
  - 在 `Generate trading signals` 步骤之前加入 `Run stock screener` 步骤

### 不变
- `scripts/generate-morning-note.py` — 完全不动
- `scripts/daily-report.py` — 完全不动
- `dashboard/` — 完全不动

---

## 评分模型

```python
def score(ticker, hist, sp500_pct):
    close = hist['Close']
    volume = hist['Volume']
    
    price = close.iloc[-1]
    ma50  = close.iloc[-50:].mean()
    high_52 = close.iloc[-252:].max()
    rs_12m  = (price / close.iloc[0] - 1) * 100
    
    vol_ratio = volume.iloc[-5:].mean() / volume.iloc[-50:].mean()
    atr_pct   = (hist['High'] - hist['Low']).iloc[-14:].mean() / price * 100
    dist_high = (high_52 - price) / high_52 * 100
    
    # 硬性门槛（不达标直接跳过）
    if vol_ratio < 1.2: return None  # 无机构参与
    if not (2 <= atr_pct <= 8): return None  # 波动率不匹配
    
    # 打分
    score = 0
    score += min(30, (vol_ratio - 1.2) / 0.8 * 30)   # 量比：1.2=0分，2.0=30分
    score += min(25, (5 - atr_pct) ** 2) if atr_pct < 5 else min(25, (atr_pct - 5) * 3)  # ATR适中最高分
    score += 20 if abs(price / ma50 - 1) > 0.05 else 10  # 有趋势
    score += min(25, (100 - dist_high) / 4)  # 接近高点
    
    # 标记类型
    sell_candidate = rs_12m > 500 and dist_high < 2
    buy_min_vol = 1.5 if sp500_pct < -1 else 1.2
    
    return {
        "score": round(score),
        "vol_ratio": round(vol_ratio, 2),
        "atr_pct": round(atr_pct, 2),
        "rs_12m": round(rs_12m, 1),
        "dist_high": round(dist_high, 1),
        "sell_candidate": sell_candidate,
        "buy_ok": vol_ratio >= buy_min_vol,
    }
```

---

## 输出格式

`data/screened-stocks.json`:
```json
{
  "date": "2026-06-08",
  "sp500_pct": -1.2,
  "scanned": 600,
  "passed": 23,
  "candidates": [
    {
      "ticker": "BOOT",
      "score": 78,
      "vol_ratio": 1.85,
      "atr_pct": 3.4,
      "rs_12m": 142.0,
      "dist_high": 3.1,
      "sell_candidate": false,
      "buy_ok": true
    }
  ]
}
```

---

## GitHub Actions 工作流顺序

```
screen-stocks.py        ← 新增（约3分钟）
generate-trading-signals.py  ← 读 screened-stocks.json
sync-to-db.py
daily-report.py
backtest-optimizer.py
```

---

## 错误处理

- yfinance 拉取失败的股票：跳过，记录警告
- 扫描结果为空（极端市场）：回退到晨报推荐（保持现有逻辑）
- screened-stocks.json 不存在：回退到晨报推荐

---

## 不在范围内

- Dashboard 展示扫描结果（后续可加）
- 基本面数据（EPS增长）— 需付费API，暂不引入
- 多时间框架分析 — 当前单日扫描足够
