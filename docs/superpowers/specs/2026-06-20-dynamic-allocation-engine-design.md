# 动态配置引擎 (Dynamic Allocation Engine) — Phase 1 设计

日期：2026-06-20　·　作者：Riley + Claude

## 北极星 (North Star)

**盈利为中心。** 模拟盘、token、方案——一切服务于"让 $2000(及其增长)赚最多的钱，同时不因噪音重注而暴雷"。本引擎决定**每条策略腿 vs 指数(SPY)各拿多少钱**，并随前向证据**动态调整**——不是写死 60/40，而是"挣来的"配置。

## 背景与前提

- 跑完严谨回测(`backtest-momentum-sized.py`)：修正了"固定金额+隐性杠杆+$1佣金"三个失误后，**MOM-MA+SPY200闸门+frac20** 是有长窗口证据的真竞争者（0.2%滑点 +64%、回撤21%<SPY；完美执行 +120%>SPY+92%）。
- **只有动量腿能诚实历史回测**；AI 腿(H/H-DS/广池/C/B-AI)有 LLM 泄漏、B-quant 有基本面前视 → **只能靠前向数据**。
- 前向数据现在样本小、且 SPY 平盘(-0.26%) → **vs SPY 暂无信息量**（平盘 trap）。
- 决策：用**动态 ratchet**(Riley 选 A) + **混合信念分**(选 C，且明确"只是前期")。

## Phase 1：信念分配引擎

### 组件 1 — 每腿信念分 (Conviction Score, 0~1)

```
conviction_i = sample_i × edge_i × robustness_i
```
- `sample_i = min(n_i / N_FULL, 1)`，`N_FULL = 40`（攒满 40 笔才完全信任）。
- `alpha_i = (该腿 frac20 复利前向收益) − (SPY 同窗口前向收益)`。
- `edge_i = clip(alpha_i / ALPHA_TARGET, 0, 1)`，`ALPHA_TARGET = 0.10`（+10pp alpha → 满分）；**alpha ≤ 0 → edge = 0**。
- `robustness_i = 1 if (去掉最赚 2 笔后已实现 > 0) else 0`（靠一两笔运气 → 归零）。

三因子相乘：必须"样本够 + 真 alpha + 不靠运气"同时成立，分才高。

### 组件 2 — 总信念 → 主动/指数 split

```
active_pct = ACTIVE_FLOOR + (ACTIVE_CEILING − ACTIVE_FLOOR) × max_i(conviction_i)
index_pct  = 1 − active_pct
```
- `ACTIVE_FLOOR = 0.30`（永远 ≥30% 主动 = 在场盈利、不瘫痪）。
- `ACTIVE_CEILING = 0.70`（指数永远 ≥30% 兜底防暴雷）。
- 用 **max(可交易腿 tradeable 的最强信念)** 驱动整体激进度（2026-06-20 修正：原为 max(全部腿)，会被 h/c 等不交易的 AI 腿的平盘 alpha 拉高=把噪音当 edge；改为只看真交易的腿，真金只在"我们真交易且真证明了的腿"上加仓）。非 tradeable 腿信念仍上 dashboard 供观察。
- 这俩常量 = **风险旋钮**，Riley 已定 30/70。

### 组件 3 — 主动内部按信念权重

```
weight_i = (conviction_i + prior_i) / Σ_j (conviction_j + prior_j)
```
- `prior_i`：仅 **MOM-MA = 0.10**（唯一有长窗口回测的腿），其余 = 0。
- 作用：零信念状态下(现在)，地板 30% 主动主要落到 MOM-MA 当探路；有前向证据后由 conviction 接管。
- **real-money 只投"可手动执行的低换手腿"**（起步 MOM-MA、B-quant；其余腿照算 conviction 上 dashboard，但留纸面直到可执行+被证明）。

### 组件 4 — 节奏与防抖

- **信念分 + 目标配置：每周重算**。
- **真金白银再平衡：每月一次，或目标偏离实际 >10% 时才动**（省手续费/滑点）。
- **单次调仓最多 ±15%**（防某腿急剧变坏时一次性大挪）。
- **下行对称**：conviction 每周用最新数据重算，腿变坏 → 分降 → 钱自动流回指数，不硬扛烂策略。

### 组件 5 — Phase 1 → Phase 2 触发（两条件同时满足）

- **证据**：≥1 腿过完整毕业 5 关（n≥40-60 + alpha 置信下沿>0 + 去尾仍正 + 扛 0.3-0.5% 滑点 + 多空分开）。
- **市场**：前向窗口 SPY 峰谷振幅 ≥ ±10%（不再平盘）。
- 两者亮 → dashboard 提示"Phase 1 完成，升级机制"。**Phase 2 不预先设计**(YAGNI)。

## 架构与数据流

1. **`scripts/compute-allocation.py`**（新，纯计算）：
   - 读 `data/portfolio_*.json`（各腿前向已平仓 final_pnl_pct/signal_date/close_date）+ `data/portfolio_spy.json`。
   - 复用 frac20 复利逻辑算每腿前向复利收益与 alpha；算 conviction、active_pct、各腿权重。
   - 判 Phase-2 两条件进度（最强腿过关数 / SPY 峰谷振幅）。
   - 输出 `data/allocation.json` + `dashboard/allocation.js`(`window.ALLOCATION`)。
2. **`scripts/compare-compounded.py`**（扩展）：除排行外，输出**每腿 frac20 复利净值时间序列** + SPY，供画曲线。
3. **Dashboard 可视化**（4 块，读上面两个产物）：
   - ① 配置环图：index% vs active% + 主动内部各腿切片。
   - ② 各腿信念分 gauge：0~1 + 拆 sample/alpha/robustness 子因子。
   - ③ frac20 复利净值曲线 vs SPY（同起点）。
   - ④ Phase 追踪器：Phase 1 + 距两个毕业条件进度。
4. 接入每日工作流（信号 pipeline 之后跑 compute-allocation），BUILD+version.js 同步 bump。

## 可调参数 (tunable constants)

`N_FULL=40`、`ALPHA_TARGET=0.10`、`ACTIVE_FLOOR=0.30`、`ACTIVE_CEILING=0.70`、`MOM-MA prior=0.10`、再平衡阈值 `10%`、单次上限 `±15%`、Phase2 市场阈值 `±10%`。集中放脚本顶部便于调。

## 不做 (YAGNI)

- 不设计 Phase 2（等前期学到再说）。
- 不自动下单（real-money 仍手动 IBKR Lite 执行；引擎只给目标配置）。
- 不碰 B-quant/B-AI 的内部 ATR 风险定额模型（与本引擎的 frac20 口径并存，conviction 用其前向 alpha 即可）。

## 成功标准

- Dashboard 能直观看到：当前配置、各腿凭什么拿这些钱、谁真在赢(vs SPY)、离 Phase 2 多远。
- 配置随前向证据自动滑动（现在≈地板30%主动 → 证据firm后爬向70%），下行对称。
- 全程零额外 API 成本（只读已有产物 + 本地计算）。
