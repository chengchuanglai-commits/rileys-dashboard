# Context:动量/趋势腿(MOM-H / MOM-MA)+ 小数股统一 — 2026-06-20

> 这份 context 用于把本次对话的成果交接给后续会话。项目北极星见记忆 `project_investment_goal`:
> **找最优交易策略、实现盈利**,不是工程任务。代码仓库 `/Users/apple/claude-whatsapp/`。

## 1. 起因

Riley 在抖音看到「旅居交易员 YC / Chill Trading」($280→$50万,Kinfo 认证),想:
(a) 把 YC 打法和现有信号工作流对比,有无可学;
(b) 找更多「有趣但真实」的交易员对照;
(c) 把学到的东西落地成可对照的新策略腿。

## 2. 研究结论(交易员对标)

| 交易员 | 性质 | 对我们的价值 |
|--------|------|--------------|
| **旅居交易员 YC** | 抖音网红,美股当冲,Kinfo 券商验证为真,**但被 USIC 投资锦标赛踢出榜单** | ⚠️ **反面教材**:$280→$50万 = 极端方差+幸存者偏差,不可复制。印证我们「小样本盈利排名大概率是运气」「去掉最赚1-2笔仍要有edge」的纪律 |
| **Mark Minervini** | USIC 审计冠军(1997 +255%,2021 +334.8%),方法全公开 | 🥇 金标准:SEPA / VCP / **8点趋势模板** / RS。可编程 |
| **J Law(罗伟森)** | 首位港人 USIC 冠军,2年累计 **+1499%**,美股实盘 | 🥈 **M.E.T.A. 多重优势进场**(10/20MA回调+缩量+趋势共振,只在多优势汇聚才买);「process over strategy」「降低交易频率」——正中我们"高换手被佣金咬死"的教训 |

**核心洞见**:YC 给的是「结果」(不可复制);Minervini/J Law 给的是「可复制的流程」。所以新策略腿学后两者,YC 只当警示。

## 3. 落地成果:C方案 = 第三条独立腿(无 AI、纯价量)

### 新增/修改文件
- `scripts/screen-momentum.py` —— **新建**。Minervini 8点趋势模板做**硬闸门**(只在确立上升趋势的领导股里选),再用 `RS 40% + 回调进场 25% + 缩量 15% + 贴近高点 20%` 打分。long-only。每日归档 `data/momentum-history/{date}.json`(前向无前视)。universe 同多因子腿(FMP 市值>$3B;无 key 用内置 34 只)。需要 `numpy`。
- `scripts/backfill-portfolio-momh.py` —— **新建**。**MOM-H** = 动量信号 + Plan H 出场(TP15/SL2/2日)。输出 `data/portfolio_momh.json` + `dashboard/portfolio-momh.js`(`window.PORTFOLIO_MOMH`)。
- `scripts/backfill-portfolio-momma.py` —— **新建**。**MOM-MA** = 同信号 + J Law 10/20MA 移动止盈(收盘破 20MA 才走,让赢家跑)+ 初始 -8% 硬止损。输出 `data/portfolio_momma.json` + `dashboard/portfolio-momma.js`。
- `.github/workflows/multifactor-bq.yml` —— **修改**。把动量腿折叠进现有「独立量化腿」工作流(12:30 UTC,**零额外 API 成本**):加 `numpy` 依赖、3 个步骤(screen-momentum + 两条 backfill)、git add、飞书通知两行。
- `dashboard/index.html` —— **修改**。4 处注册:`SIM_SCHEME_COLORS`(momh 琥珀 #ca8a04 / momma 青 #0891b2)、`_SCHEME_PORT`、`_SCHEME_NAMES`、`schemeRanking` 数组 + 两个 `document.write` 脚本加载。BUILD 与 `version.js` 同步 bump 到 `20260620120500`。

### 三轴对照(为什么这样设计)
- **MOM-H vs H / H-DS / H-广池** → 只差信号源(动量客观筛 vs AI)。
- **MOM-H vs MOM-MA** → 同信号同仓位,只差出场(紧止损快出 vs 趋势跟随)。
- **MOM 整腿 vs B-quant 多因子** → 都无 AI,只差选股逻辑(动量 vs 多因子)。

## 4. 小数股统一(2026-06-20,本次第二轮改动)

**问题**:原 `int(PER_POSITION_USD/价)` 让股价 >$500 的票拿 0 股被丢——动量腿专抓领导股(常是高价票如 MU ~$1134),恰恰丢了最该买的。

**改法**:全部改成 `round(500/价, 4)` 小数股(IBKR 真实支持),$500/仓不变。**没用 ATR 风险定额**——那会让不同止损宽窄的腿仓位不同,污染「只比出场」的控制变量。

**改动范围**:MOM-H、MOM-MA、**以及统一改了现实盘 H 系列**(`backfill-portfolio-h.py` / `-hds.py` / `-mn.py`),`skipped_zero_shares` 保留为 0。

**H 系列轨迹变化一次**(Riley 已认可):
| 腿 | 改前 | 改后 | 笔数 | 跳过 |
|----|------|------|------|------|
| H | $2158.96 | $2176.75 | 17→18 | 1→0 |
| H-DS | $2088.01 | $2107.30 | 15→16 | 1→0 |
| H-广池 | $2225.49 | **$2467.95** | 74→79 | 6→0 |

H-广池跳 +$242:之前被丢的 6 只高价晨报票含强势股。

## 5. 当前状态 & 下一步

- ✅ 三脚本跑通;回溯造数据验证两套出场真触发(momh 走 stop_loss/max_hold,momma 走 ma_break 且让利润奔跑,初始硬止损未误触发);两 js node 解析通过;dashboard 四处注册一致;H 系列重跑跳过归零。
- ⚠️ **截至 2026-06-20 全是本地改动,未 git commit/push**。push 后 `multifactor-bq.yml` 才会每天累积 MOM 腿。
- **MOM 腿目前仅 1 天归档(首日,0 已平,全持仓)**,需前向攒几周才有统计意义。
- **待办**:(a) commit + push 启用;(c) 攒样本后扩展 `scripts/analyze-signal-edge.py` 把 MOM-H/MOM-MA 和 AI 腿一起做 alpha vs SPY 对照。
- **毕业上实盘 5 关**仍适用(见记忆 `signal_edge_measurement`):n≥60-80、alpha CI 下沿>0、去最赚 1-2 笔仍有 edge、扛 0.3-0.5% 滑点、多空分开。很可能结论是"没稳定 edge→不上实盘才对",别因沉没成本硬上。

## 关键文件速查
```
scripts/screen-momentum.py            # 动量选股(Minervini闸门+J Law M.E.T.A.打分)
scripts/backfill-portfolio-momh.py    # MOM-H: + Plan H出场
scripts/backfill-portfolio-momma.py   # MOM-MA: + J Law 20MA移动止盈
.github/workflows/multifactor-bq.yml  # 折叠进"独立量化腿"工作流(12:30 UTC)
dashboard/index.html                  # 4处注册 momh/momma
data/momentum-history/{date}.json     # 每日归档(前向无前视)
```
