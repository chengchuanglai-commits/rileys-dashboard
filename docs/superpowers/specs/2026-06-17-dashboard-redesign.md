# Dashboard 整体重设计规格

> **For agentic workers:** This is a design spec. Use `superpowers:writing-plans` to generate the implementation plan from this document.

**Goal:** 对个人 dashboard 进行全面视觉与信息架构重设计，统一设计调性，提升每个板块的可读性与使用效率。

**File:** `/Users/apple/claude-whatsapp/dashboard/index.html`  
**Deploy:** GitHub Pages via `git push origin main`

---

## 1. 设计系统（全局约束）

### 1.1 颜色
- **禁止高饱和色**，所有颜色使用低饱和度版本
- 主文字：`#111111`
- 次级文字：`#6b7280`
- 辅助文字/标签：`#9ca3af`
- 分隔线/边框：`#f0f0f0`
- 卡片背景：`#ffffff`
- 页面背景：`#f8f9fa`
- 指标卡片背景：`#f8f9fa`（不用纯白，与卡片区分）
- 状态色（低饱和）：
  - 正向/涨：`#16a34a`（绿，饱和度可接受）
  - 负向/跌：`#dc2626`（红）
  - 强调/主要：`#374151`（深灰，替代品牌蓝）
  - Buy 信号背景：`#f0fdf4`，边框 `#bbf7d0`
  - Sell 信号背景：`#fef2f2`，边框 `#fecaca`

### 1.2 字体
- 全部使用 `system-ui, -apple-system, sans-serif`（当前已使用）
- 标签/标题：`font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; color: #9ca3af`
- 卡片标题：`font-size: 11px; font-weight: 700; color: #111`
- 数字大值：`font-size: 20–32px; font-weight: 800; color: #111`
- 正文/描述：`font-size: 10px; line-height: 1.6; color: #374151`
- 辅助信息：`font-size: 9px; color: #9ca3af`

### 1.3 禁止 Emoji
- **全局禁用 emoji**，包括导航、卡片标题、标签等所有位置
- 用文字或 SVG icon 替代（可使用 Heroicons 内联 SVG 小图标）

### 1.4 间距 & 圆角
- 卡片圆角：`border-radius: 12px`
- 内部元素圆角：`border-radius: 8px`
- 卡片内边距：`padding: 16px 18px`
- 卡片间距：`gap: 12px` 或 `margin-bottom: 12px`
- 分隔线：`1px solid #f0f0f0`

### 1.5 阴影
- 卡片阴影：`box-shadow: 0 1px 4px rgba(0,0,0,.06)`（极淡）

---

## 2. 导航结构（保持不变）

- 左侧 Sidebar：4个分组（生活 / 投资 / 项目 / 资讯）
- 每组内：顶部 sticky 水平 Tab 切换子板块
- 默认落地：生活分组
- 底部 bottom nav bar 保持不变

---

## 3. 投资分组（grp-invest）

### 3.1 行情条（Ticker Tape）
- 移至投资分组**最顶部**，在 Tab bar 下方、所有子板块上方
- 放置在 `grp-invest` 内、`.sec-tab-bar` 下方，作为固定区块，切换投资子 Tab 时始终保持可见（不在任何 Tab 内容区内）
- 保持现有 TradingView 深色 widget

### 3.2 晨报（sec-morning）
布局：**左列（固定 180px）数字 / 右列（flex-grow）文章**

左列（关键数据）：
- 标签：`关键数据`（全大写，#9ca3af）
- 4张指标卡：S&P 500 / 10Y 美债 / Q1 EPS 超预期率 / API 今日费用
- 每卡：指标名（9px #9ca3af）+ 大数值（18px bold #111）+ 变化（9px 红/绿）
- 卡片背景 `#f8f9fa`，圆角 8px

右列（AI 分析）：
- 标签：`今日分析`
- 正文 10px，行高 1.7，颜色 `#374151`
- 按宏观 / 科技 / 风险三段落排列，段落标题 bold `#111`

### 3.3 AI 信号（sec-signals）
合并原「AI 深度信号」和「信号 Edge」为**一张卡**，内部 Tab 切换：

Tab 1 — 今日信号：
- 每条信号：`[BUY/SELL 标签] [股票代码] [信心百分比] [入场价 → TP]`
- BUY 行背景 `#f0fdf4`，左边框 3px `#16a34a`
- SELL 行背景 `#fef2f2`，左边框 3px `#dc2626`
- 标签文字：BUY=`#16a34a`，SELL=`#dc2626`，font-weight 700，9px

Tab 2 — Edge 分析：
- 3个指标卡横排：30天收益 / SPY 基准 / 超额收益
- 配色与指标卡统一（低饱和）

### 3.4 模拟盘（sec-sim）
**统一面板 + 内部 4个 Tab：概览 / 持仓 / 历史 / 排名**

Tab 1 — 概览（默认）：
- 顶部摘要行（小字）：运行天数 / 总投入 / 最高净值
- 8个方案**排行榜**，按当前净值降序排列
  - 每行：`排名序号 | 方案名 | 进度条（相对最高值） | 净值 | 收益率`
  - 第1名：背景 `#fafafa`，序号加粗
  - 进度条高度 4px，颜色跟随方案原有颜色（低饱和版本）
- 收益曲线图（现有 SVG）放在排行榜**下方**，高度保持 240px
- 图例 2列排列（现有 HTML legend，保持）

Tab 2 — 持仓：
- 当前折叠的「当前持仓」内容移至此 Tab

Tab 3 — 历史：
- 现有「交易历史表格」移至此 Tab

Tab 4 — 排名：
- 现有「策略优化排名」+ 「大规模历史验证」移至此 Tab

### 3.5 账户总览（sec-accounts）
布局：**总资产大字在上 + 4账户 2×2 网格**

顶部 Hero 区：
- 标签：`总资产（≈ USD）`（9px 全大写 #9ca3af）
- 总额：`font-size: 32px; font-weight: 800; color: #111`
- 本月变化：`+$420 本月`（9px，正绿/负红）
- 背景：`#f8f9fa`，圆角 10px，内边距 14px，居中

2×2 账户卡：
- 4张卡：工行 CNY / HSBC HKD / BMO CAD / IBKR USD
- 每卡：账户名（8px #9ca3af）+ 原始金额（14px bold #111）+ ≈USD 换算（9px #6b7280）
- 编辑按钮（✏）保留，样式：8px，`#d1d5db`，hover 变 `#6b7280`

经济日历 & 指数走势 Widget：
- 保持现有 TradingView widget，移至账户总览下方
- 不属于任何 Tab（跟随账户 Tab 可见）

---

## 4. 生活分组（grp-life）

### 4.1 健康（sec-health）
4个指标卡 **2×2 网格**：

| 指标 | 颜色 | 单位 |
|------|------|------|
| 步数 | `#6b7280`（中灰） | 步 / 目标10000 |
| 卡路里 | `#9ca3af`（浅灰） | kcal |
| 站立 | `#6b7280` | 小时 |
| 静息心率 | `#374151` | bpm |

每卡：指标名（7px uppercase #9ca3af）+ 数值（18px bold）+ 4px 进度条（灰底，深色填充）

训练计划区（卡片下部分隔线后）：
- 标签：`本周训练 3/4`（9px #9ca3af）
- 训练打点：7个圆点（周一到周日），完成=深色实心，未完成=灰色虚线圆

### 4.2 日程（sec-calendar）
布局：**今天 / 明天 / 本周**三区块（仅显示有内容的）

- 区块标签：`今天 · 6月17日`（8px uppercase #9ca3af）
- 每条日程：时间（8px bold，颜色跟随分类）+ 内容（10px #111）
- 左侧 3px 色条区分分类（无emoji）：
  - 默认：`#d1d5db`（浅灰）
  - 投资/交易相关：`#374151`（深灰）
  - 项目相关：`#9ca3af`
- 添加按钮：右上角，9px 文字，`#9ca3af`，hover 变 `#111`

### 4.3 归档（sec-archive）
- 每条：左侧 3px 色条（完成=`#9ca3af`，待办=`#d1d5db`）+ 事件名 + 日期
- max-height: 300px，overflow-y: auto

---

## 5. 项目分组（grp-project）

### 5.1 项目追踪（sec-projects）
每个项目**独立卡片**，包含：
- 项目名（11px bold #111）+ 状态 badge（右上角，9px，低饱和背景）
- 4px 进度条：背景 `#f0f0f0`，填充颜色低饱和（进行中=`#9ca3af`，完成=`#6b7280`）
- **点击进度条卡片**（或点击展开箭头）→ 在进度条下方展开一段进度总结文字
  - 展开区：`font-size: 10px; color: #6b7280; line-height: 1.7; padding-top: 10px; border-top: 1px solid #f0f0f0`
  - 展开/收起动画：`max-height` transition 200ms ease
  - 展开箭头：右侧 `›` 符号，旋转 90° 表示展开状态
  - 总结文字来源：每个项目对象中增加 `summary` 字段（字符串），由 `renderProjects()` 渲染时写入展开区，内容在 Cloudflare KV 的 `self_history.json` 或 JS 静态数据中维护

### 5.2 网站数据（sec-ga）
2×2 指标卡：7日访客 / 平均时长 / 今日订单 / 跳出率
- 样式与健康指标卡统一（#f8f9fa 背景，18px bold 数值，7px uppercase 标签）
- 变化方向：上升=`#16a34a` ↑，下降（视指标）= `#dc2626` 或 `#16a34a`

---

## 6. 资讯分组（grp-news）

### 6.1 资讯（sec-news）
内部 Tab 切换：**财经 / AI / 潮流**（三个 Tab，复用 `.sec-tab` 样式）

新闻列表：
- 每条：`[分类 Tag] [标题] [来源 · 时间]`
- 分类 Tag：9px，低饱和背景色
  - 财经：背景 `#f3f4f6`，文字 `#374151`
  - AI：背景 `#f5f3ff`，文字 `#5b21b6`（低饱和紫）
  - 潮流：背景 `#fff7ed`，文字 `#9a3412`（低饱和橙）
- 标题：10px bold `#111`，行高 1.4
- 来源+时间：8px `#9ca3af`
- **点击任意新闻条目** → 在该条下方展开新闻摘要（2-3句话）
  - 展开区样式：`font-size: 10px; color: #6b7280; line-height: 1.7; padding: 8px 10px; background: #fafafa; border-radius: 0 0 8px 8px`
  - 展开/收起：click toggle，动画同项目进度总结
  - 摘要文字来源：新闻数据对象中的 `summary` 字段（现有 `loadNews()` 返回的 JSON 已含此字段，若无则展开区显示「暂无摘要」）
- 条目间用 `1px solid #f5f5f5` 分隔线

---

## 7. 交互规范

### 折叠展开（项目总结 & 新闻摘要）
```css
.expandable-body {
  max-height: 0;
  overflow: hidden;
  transition: max-height 200ms ease;
}
.expandable-body.open {
  max-height: 200px; /* 足够大即可 */
}
```

点击父元素 → toggle `.open` class → CSS 动画展开

### 模拟盘内部 Tab
- 复用现有 `.sec-tab` / `.sec-tab.active` 样式（缩小版，padding 更小）
- Tab 切换只控制对应内容区域显示/隐藏，不影响卡片外部

### 信号 Tab（AI 信号卡内）
- 同上，复用缩小版 Tab 样式

---

## 8. 不变的部分

- 所有数据加载逻辑（loadMorningNote、loadTradingSignals、loadSimCurve 等）完全不变
- Cloudflare Worker 接口不变
- GitHub Pages 部署方式不变（git push origin main）
- BUILD 版本号格式不变（`var BUILD="YYYYMMDDHHMMSS"`）
