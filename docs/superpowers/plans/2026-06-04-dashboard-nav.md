# Dashboard 导航重构 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `dashboard/index.html` 中新增左侧固定导航栏（桌面端 >480px）和底部 Tab 栏（手机端 ≤480px），将现有板块重组为 4 个分组：❤️生活、💹投资、🚀项目、📰资讯。

**Architecture:** 单文件修改（`dashboard/index.html`）。新增 CSS → 新增 HTML 壳结构 → 拆分混合行 → 移动行、添加分组 `<section>` 标签 → 新增 JS。全程 vanilla HTML/CSS/JS，无框架依赖。

**Tech Stack:** HTML/CSS/JS (vanilla)，单文件架构。

---

## 现有内容区结构（重构前，`.container` 内部）

```
标题栏 (581-591)
Row 1 col-2 (593-678): [💰账户总览] + [❤健康中心+运动]  ← 混合分组
Calendar col-1 (680-696): [📅日程安排]
History col-2 (698-719): [🗂日程归档] + [📈资产历史]    ← 混合分组
Row 2 col-1 (721-841):  [🚀项目追踪]
Row 2.5 col-1 (843-915): [🌐网站数据]
Row 2.6 col-1 (917-999): [📊金融晨报]
Row 2.7 col-1 (1000-1015): [🤖AI深度信号]
Row 2.8 col-1 (1017-1036): [📉模拟盘]
Row 3 (1038-1064): Ticker tape
Row 3.5 col-1 (1066-1124): [📊Questrade持仓]
Row 4 col-2 (1126-1160): [📊指数走势] + [📰财经资讯]   ← 混合分组
Row 5 col-2 (1162-1205): [🤖AI资讯] + [👟潮流资讯]
Row 6 (1207-1216): 经济日历
```

## 目标内容区结构（重构后）

```
标题栏（不变）

<section data-grp="life">
  [❤健康中心+运动]  id="sec-health"   (从 Row1 拆出)
  [📅日程安排]       id="sec-calendar" (添加 id)
  [🗂日程归档]       id="sec-archive"  (从 History 拆出)
</section>

<section data-grp="invest">
  [💰账户总览]       id="sec-accounts"  (从 Row1 拆出，移到此处)
  [📊金融晨报]       id="sec-morning"   (添加 id)
  [🤖AI深度信号]     id="sec-signals"   (添加 id)
  [📉模拟盘]         id="sec-sim"       (添加 id)
  Ticker tape        (不变)
  [📊Questrade持仓]  id="sec-questrade" (添加 id)
  [📊指数走势]       (从 Row4 拆出)
  [📈资产历史]       (从 History 拆出，移到此处)
  经济日历           (移到此处)
</section>

<section data-grp="project">
  [🚀项目追踪]      id="sec-projects"  (添加 id)
  [🌐网站数据]      id="sec-ga"        (添加 id)
</section>

<section data-grp="news">
  [📰财经资讯]      id="sec-news"      (从 Row4 拆出)
  [🤖AI资讯+👟潮流] (原 Row5，不变)
</section>
```

---

### Task 1: 添加导航 CSS

**Files:**
- Modify: `dashboard/index.html:566` (插入到 `</style>` 前)

- [ ] **Step 1: 在 `</style>` 前插入 CSS**

找到第 566 行末尾（`</style>` 的上一行），在其前插入以下 CSS：

```css
        /* ── Navigation Shell ── */
        #dashboard-shell {
          display: flex;
          align-items: flex-start;
          min-height: 100vh;
        }

        /* ── Sidebar ── */
        #sidebar {
          width: 160px;
          background: #1a1a2e;
          position: sticky;
          top: 0;
          height: 100vh;
          overflow-y: auto;
          flex-shrink: 0;
          z-index: 100;
        }
        .sb-header { padding: 16px; border-bottom: 1px solid rgba(255,255,255,.08); }
        .sb-title  { font-size: 13px; font-weight: 700; color: #fff; }
        .sb-sub    { font-size: 10px; color: #555; margin-top: 2px; }
        .sb-nav    { padding: 12px 0; }
        .sb-group-lbl {
          padding: 0 16px 4px;
          font-size: 9px; font-weight: 700; color: #444;
          text-transform: uppercase; letter-spacing: .1em;
        }
        .sb-item {
          display: flex; align-items: center; gap: 7px;
          margin: 0 8px 2px; border-radius: 8px;
          padding: 7px 10px; font-size: 12px; color: #555;
          cursor: pointer; text-decoration: none;
          transition: background .15s, color .15s;
        }
        .sb-item:hover  { background: rgba(255,255,255,.07); color: #aaa; }
        .sb-item.active { background: rgba(255,255,255,.12); color: #fff; }

        /* ── Main content ── */
        #main-content { flex: 1; min-width: 0; }

        /* ── Group sections ── */
        .grp-section { display: block; }

        /* ── Bottom tab bar ── */
        #bottom-tabs {
          display: none;
          position: fixed; bottom: 0; left: 0; right: 0;
          height: 56px; background: #fff;
          border-top: 1px solid #e8e8e8;
          z-index: 200;
        }
        .bt-item {
          flex: 1; display: flex; flex-direction: column;
          align-items: center; justify-content: center;
          cursor: pointer; gap: 2px;
        }
        .bt-icon { font-size: 20px; line-height: 1; }
        .bt-lbl  { font-size: 9px; color: #999; font-weight: 500; }
        .bt-item.active .bt-lbl { color: #007aff; font-weight: 600; }

        /* ── Mobile overrides ── */
        @media (max-width: 480px) {
          #sidebar      { display: none; }
          #bottom-tabs  { display: flex; }
          #main-content { padding-bottom: 56px; }
          .grp-section.grp-hidden { display: none; }
        }
```

- [ ] **Step 2: Commit**

```bash
git add dashboard/index.html
git commit -m "feat: add navigation CSS — sidebar, bottom tabs, group sections"
```

---

### Task 2: 新增 Shell 包装 + Sidebar + Bottom Tabs HTML

**Files:**
- Modify: `dashboard/index.html` — body 开头和结尾

- [ ] **Step 1: 在 `<body>` 后插入 shell + sidebar + main-content 开标签**

找到：
```
<body>
<div class="container">
```

替换为：
```html
<body>
<div id="dashboard-shell">

<div id="sidebar">
  <div class="sb-header">
    <div class="sb-title">Dashboard</div>
    <div class="sb-sub">个人中心</div>
  </div>
  <nav class="sb-nav">
    <div class="sb-group-lbl">生活</div>
    <a class="sb-item active" data-grp="life" data-target="sec-health" onclick="sbNav(this)">❤️ 健康</a>
    <a class="sb-item" data-grp="life" data-target="sec-calendar" onclick="sbNav(this)">📅 日程</a>
    <a class="sb-item" data-grp="life" data-target="sec-workout" onclick="sbNav(this)">💪 运动</a>

    <div class="sb-group-lbl" style="margin-top:12px">投资</div>
    <a class="sb-item" data-grp="invest" data-target="sec-morning" onclick="sbNav(this)">📊 晨报</a>
    <a class="sb-item" data-grp="invest" data-target="sec-signals" onclick="sbNav(this)">🤖 AI 信号</a>
    <a class="sb-item" data-grp="invest" data-target="sec-questrade" onclick="sbNav(this)">📈 持仓</a>
    <a class="sb-item" data-grp="invest" data-target="sec-sim" onclick="sbNav(this)">📉 模拟盘</a>
    <a class="sb-item" data-grp="invest" data-target="sec-accounts" onclick="sbNav(this)">💰 账户 & 资产</a>

    <div class="sb-group-lbl" style="margin-top:12px">项目</div>
    <a class="sb-item" data-grp="project" data-target="sec-projects" onclick="sbNav(this)">🚀 项目追踪</a>
    <a class="sb-item" data-grp="project" data-target="sec-ga" onclick="sbNav(this)">🌐 网站数据</a>

    <div class="sb-group-lbl" style="margin-top:12px">资讯</div>
    <a class="sb-item" data-grp="news" data-target="sec-news" onclick="sbNav(this)">📰 财经/AI/潮流</a>
  </nav>
</div>

<div id="main-content">
<div class="container">
```

- [ ] **Step 2: 在 `</div><!-- /container -->` 后关闭 main-content，并添加 bottom-tabs + shell 关闭**

找到：
```
</div><!-- /container -->
```

替换为：
```html
</div><!-- /container -->
</div><!-- /#main-content -->

<div id="bottom-tabs">
  <div class="bt-item active" data-grp="life" onclick="switchTab(this)">
    <span class="bt-icon">❤️</span><span class="bt-lbl">生活</span>
  </div>
  <div class="bt-item" data-grp="invest" onclick="switchTab(this)">
    <span class="bt-icon">💹</span><span class="bt-lbl">投资</span>
  </div>
  <div class="bt-item" data-grp="project" onclick="switchTab(this)">
    <span class="bt-icon">🚀</span><span class="bt-lbl">项目</span>
  </div>
  <div class="bt-item" data-grp="news" onclick="switchTab(this)">
    <span class="bt-icon">📰</span><span class="bt-lbl">资讯</span>
  </div>
</div>

</div><!-- /#dashboard-shell -->
```

- [ ] **Step 3: 浏览器验证布局**

用浏览器打开 `dashboard/index.html`：
- 桌面端（>480px）：左侧显示深色侧边栏（160px 宽），右侧为内容区，侧边栏随页面滚动保持固定
- 手机端（模拟 375px）：侧边栏隐藏，底部出现 4 个 Tab

- [ ] **Step 4: Commit**

```bash
git add dashboard/index.html
git commit -m "feat: add dashboard shell, sidebar HTML, bottom tabs"
```

---

### Task 3: 拆分混合行

**Files:**
- Modify: `dashboard/index.html` — 三处 `row col-2` 拆分

**背景：** Row 1、History、Row 4 各自把不同分组的卡片放在同一个 `div.row.col-2` 里，需要拆成各自独立的 `col-1` 行。

#### Step 1: 拆分 Row 1（账户总览 + 健康中心）

**找到（约第 593 行）：**
```html
    <!-- ── Row 1: Accounts · Tasks · Workout ── -->
    <div class="row col-2">

        <div class="card acct-card">
```

**替换为：**
```html
    <!-- ── 账户总览 (invest) ── -->
    <div class="row col-1" id="sec-accounts">

        <div class="card acct-card">
```

**找到（约第 656 行，账户卡片结束后紧接健康卡片开头）：**
```html
        </div>

        <div class="card">
            <div class="card-hd">
                <span class="card-title">❤ 健康中心</span>
```

**替换为：**
```html
        </div>
    </div><!-- /#sec-accounts -->

    <!-- ── 健康中心 & 运动 (life) ── -->
    <div class="row col-1" id="sec-health">
        <div class="card">
            <div class="card-hd">
                <span class="card-title">❤ 健康中心</span>
```

**找到（约第 677 行，健康卡片最后一个 div 之后的 row col-2 关闭标签）：**
```html
        </div>

    </div>

    <!-- ── Calendar / Schedule ── -->
```

**替换为：**
```html
        </div>
    </div><!-- /#sec-health -->

    <!-- ── Calendar / Schedule ── -->
```

#### Step 2: 给运动区块添加锚点 ID

**找到（健康卡片内约第 669 行）：**
```html
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
                <span style="font-size:9px;font-weight:600;color:#888;text-transform:uppercase;letter-spacing:.1em">本周训练</span>
```

**替换为：**
```html
            <div id="sec-workout" style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
                <span style="font-size:9px;font-weight:600;color:#888;text-transform:uppercase;letter-spacing:.1em">本周训练</span>
```

#### Step 3: 拆分 History 行（日程归档 + 资产历史）

**找到（约第 698 行）：**
```html
    <!-- ── History ── -->
    <div class="row col-2">

        <!-- 日程归档 -->
        <div class="card">
```

**替换为：**
```html
    <!-- ── 日程归档 (life) ── -->
    <div class="row col-1" id="sec-archive">

        <!-- 日程归档 -->
        <div class="card">
```

**找到（约第 708 行，日程归档卡片结束后紧接资产历史）：**
```html
        </div>

        <!-- 资产快照 -->
        <div class="card">
```

**替换为：**
```html
        </div>
    </div><!-- /#sec-archive -->

    <!-- ── 资产历史 (invest) ── -->
    <div class="row col-1" id="sec-asset-history">
        <!-- 资产快照 -->
        <div class="card">
```

**找到（约第 718 行，资产历史卡片关闭后的 row col-2 关闭标签）：**
```html
        </div>

    </div>

    <!-- ── Row 2: Project ── -->
```

**替换为：**
```html
        </div>
    </div><!-- /#sec-asset-history -->

    <!-- ── Row 2: Project ── -->
```

#### Step 4: 拆分 Row 4（指数走势 + 财经资讯）

**找到（约第 1126 行）：**
```html
    <!-- ── Row 4: Chart + Financial News ── -->
    <div class="row col-2">

        <div class="card" style="padding:0;overflow:hidden">
```

**替换为：**
```html
    <!-- ── 指数走势 (invest) ── -->
    <div class="row col-1" id="sec-chart">

        <div class="card" style="padding:0;overflow:hidden">
```

**找到（约第 1138 行，指数走势 div 关闭后紧接财经资讯）：**
```html
        </div>

        <div class="card news-card">
            <div class="news-card-inner">
                <div class="card-hd" style="margin-bottom:10px">
                    <span class="card-title">📰 财经资讯</span>
```

**替换为：**
```html
        </div>
    </div><!-- /#sec-chart -->

    <!-- ── 财经资讯 (news) ── -->
    <div class="row col-1" id="sec-news">
        <div class="card news-card">
            <div class="news-card-inner">
                <div class="card-hd" style="margin-bottom:10px">
                    <span class="card-title">📰 财经资讯</span>
```

**找到（约第 1158 行，财经资讯卡片关闭后的 row col-2 关闭标签）：**
```html
        </div>

    </div>

    <!-- ── Row 5: AI News + Fashion News ── -->
```

**替换为：**
```html
        </div>
    </div><!-- /#sec-news -->

    <!-- ── Row 5: AI News + Fashion News ── -->
```

- [ ] **Step 5: 验证拆分正确**

打开浏览器，检查：
1. 所有板块仍然正常显示（没有漏掉内容）
2. DevTools Elements 中账户总览、健康中心各是独立的 `div.row.col-1`
3. 日程归档、资产历史各是独立的 `div.row.col-1`
4. 指数走势、财经资讯各是独立的 `div.row.col-1`

- [ ] **Step 6: Commit**

```bash
git add dashboard/index.html
git commit -m "refactor: split mixed-group rows into individual col-1 rows"
```

---

### Task 4: 给现有行添加锚点 ID

**Files:**
- Modify: `dashboard/index.html`

以下 7 处 `div.row` 需要添加 id，供侧边栏导航 `scrollIntoView` 使用。

- [ ] **Step 1: 日程安排行**

找到：
```html
    <!-- ── Calendar / Schedule ── -->
    <div class="row col-1">
        <div class="card">
            <div class="card-hd">
                <span class="card-title">📅 日程安排</span>
```

替换为：
```html
    <!-- ── Calendar / Schedule ── -->
    <div class="row col-1" id="sec-calendar">
        <div class="card">
            <div class="card-hd">
                <span class="card-title">📅 日程安排</span>
```

- [ ] **Step 2: 项目追踪行**

找到：
```html
    <!-- ── Row 2: Project ── -->
    <div class="row col-1">
        <div class="card proj-card">
```

替换为：
```html
    <!-- ── Row 2: Project ── -->
    <div class="row col-1" id="sec-projects">
        <div class="card proj-card">
```

- [ ] **Step 3: 网站数据行**

找到：
```html
    <!-- ── Row 2.5: Website Analytics ── -->
    <div class="row col-1">
        <div class="card">
            <div class="card-hd">
                <div style="display:flex;align-items:center;gap:8px">
                    <span class="card-title">🌐 Seedclay.com 网站数据</span>
```

替换为：
```html
    <!-- ── Row 2.5: Website Analytics ── -->
    <div class="row col-1" id="sec-ga">
        <div class="card">
            <div class="card-hd">
                <div style="display:flex;align-items:center;gap:8px">
                    <span class="card-title">🌐 Seedclay.com 网站数据</span>
```

- [ ] **Step 4: 金融晨报行**

找到：
```html
    <!-- ── Row 2.6: 金融晨报 ── -->
    <div class="row col-1">
```

替换为：
```html
    <!-- ── Row 2.6: 金融晨报 ── -->
    <div class="row col-1" id="sec-morning">
```

- [ ] **Step 5: AI 深度信号行**

找到：
```html
    <!-- ── Row 2.7: TradingAgents 信号 ── -->
    <div class="row col-1" style="margin-bottom:16px">
```

替换为：
```html
    <!-- ── Row 2.7: TradingAgents 信号 ── -->
    <div class="row col-1" id="sec-signals" style="margin-bottom:16px">
```

- [ ] **Step 6: 模拟盘行**

找到：
```html
    <!-- ── Row 2.8: A vs B 模拟系统（统一面板）── -->
    <div class="row col-1" style="margin-bottom:16px">
```

替换为：
```html
    <!-- ── Row 2.8: A vs B 模拟系统（统一面板）── -->
    <div class="row col-1" id="sec-sim" style="margin-bottom:16px">
```

- [ ] **Step 7: Questrade 持仓行**

找到：
```html
    <!-- ── Row 3.5: Stock Portfolio ── -->
    <div class="row col-1">
        <div class="card">
            <div class="card-hd">
                <div style="display:flex;align-items:center;gap:8px">
                    <span class="card-title">📊 Questrade 持仓</span>
```

替换为：
```html
    <!-- ── Row 3.5: Stock Portfolio ── -->
    <div class="row col-1" id="sec-questrade">
        <div class="card">
            <div class="card-hd">
                <div style="display:flex;align-items:center;gap:8px">
                    <span class="card-title">📊 Questrade 持仓</span>
```

- [ ] **Step 8: Commit**

```bash
git add dashboard/index.html
git commit -m "feat: add anchor IDs to all dashboard section rows"
```

---

### Task 5: 移动行并添加分组 Section 标签

**Files:**
- Modify: `dashboard/index.html`

**背景：** 经过 Task 3-4 后，行的顺序是：
```
标题栏
sec-accounts (invest)   ← 需要移到 life section 之后
sec-health (life)
sec-calendar (life)
sec-archive (life)
sec-asset-history (invest) ← 需要移到 sec-chart 之后
sec-projects (project)
sec-ga (project)
sec-morning (invest)
sec-signals (invest)
sec-sim (invest)
Ticker (invest)
sec-questrade (invest)
sec-chart (invest)
sec-news (news)
AI+潮流 row (news)
经济日历 (invest)       ← 需要移到 sec-news 之前
```

需要做 3 次行移动，然后加 section 标签。

#### Step 1: 移动 sec-accounts 到 sec-archive 之后

把整个 `sec-accounts` 行（含注释、`<div class="row col-1" id="sec-accounts">` 到对应 `</div><!-- /#sec-accounts -->`）从标题栏下方剪切，粘贴到 `</div><!-- /#sec-archive -->` 之后、`<!-- ── Row 2: Project ── -->` 注释之前。

**剪切范围（搜索这段唯一文本）：**
```
    <!-- ── 账户总览 (invest) ── -->
    <div class="row col-1" id="sec-accounts">
```
到（含）：
```
    </div><!-- /#sec-accounts -->
```

**粘贴到：**
```
    </div><!-- /#sec-archive -->
```
的下方（紧接其后，在 `<!-- ── Row 2: Project ── -->` 之前）。

最终该区域结构：
```
    </div><!-- /#sec-archive -->

    <!-- ── 账户总览 (invest) ── -->
    <div class="row col-1" id="sec-accounts">
        ...
    </div><!-- /#sec-accounts -->

    <!-- ── Row 2: Project ── -->
```

#### Step 2: 移动 sec-asset-history 到 sec-chart 之后

把整个 `sec-asset-history` 行剪切，粘贴到 `</div><!-- /#sec-chart -->` 之后、`<!-- ── 财经资讯 (news) ── -->` 注释之前。

**剪切范围：**
```
    <!-- ── 资产历史 (invest) ── -->
    <div class="row col-1" id="sec-asset-history">
```
到（含）：
```
    </div><!-- /#sec-asset-history -->
```

**粘贴到：**
```
    </div><!-- /#sec-chart -->
```
的下方（在 `<!-- ── 财经资讯 (news) ── -->` 之前）。

#### Step 3: 移动经济日历到财经资讯之前

把经济日历 `div.card`（约 `<!-- ── Row 6: Economic Calendar ── -->` 到其关闭 `</div>`）剪切，粘贴到 `<!-- ── 财经资讯 (news) ── -->` 之前、`sec-asset-history` 之后。

**剪切范围：**
```
    <!-- ── Row 6: Economic Calendar ── -->
    <div class="card" style="padding:0;overflow:hidden;margin-bottom:20px">
```
到（含）其关闭 `</div>`（含最后一个 `</div>` 的那一行）。

**粘贴到：** `</div><!-- /#sec-asset-history -->` 的下方，`<!-- ── 财经资讯 (news) ── -->` 之前。

#### Step 4: 添加 4 个分组 `<section>` 标签

完成以上 3 次移动后，行的顺序应为：
```
标题栏
sec-health
sec-calendar
sec-archive
sec-accounts
sec-morning
sec-signals
sec-sim
Ticker
sec-questrade
sec-chart
sec-asset-history
经济日历
sec-news
AI+潮流 row
```

**添加 life section 开标签：**
找到：
```
    <!-- ── 健康中心 & 运动 (life) ── -->
    <div class="row col-1" id="sec-health">
```
在其前插入：
```html
    <section class="grp-section" data-grp="life" id="grp-life">
```

**添加 life section 闭标签 + invest section 开标签：**
找到：
```
    </div><!-- /#sec-archive -->

    <!-- ── 账户总览 (invest) ── -->
```
替换为：
```html
    </div><!-- /#sec-archive -->
    </section><!-- /#grp-life -->

    <section class="grp-section" data-grp="invest" id="grp-invest">
    <!-- ── 账户总览 (invest) ── -->
```

**添加 invest section 闭标签 + project section 开标签：**

找到经济日历卡片的关闭标签（`</div>` 结尾，紧跟 `<!-- ── 财经资讯 -->` 注释），在经济日历 `</div>` 之后、`<!-- ── 财经资讯 (news) ── -->` 之前插入：
```html
    </section><!-- /#grp-invest -->

    <section class="grp-section" data-grp="news" id="grp-news">
```

等等——项目组应该在 invest 和 news 之间！重新确认行顺序：

**实际目标行顺序（Task 5 完成后）：**
```
标题栏
[life open]
  sec-health
  sec-calendar
  sec-archive
[life close]
[invest open]
  sec-accounts
  sec-morning
  sec-signals
  sec-sim
  Ticker
  sec-questrade
  sec-chart
  sec-asset-history
  经济日历
[invest close]
[project open]
  sec-projects
  sec-ga
[project close]
[news open]
  sec-news
  AI+潮流
[news close]
```

但 Step 1 把 sec-accounts 放到了 sec-archive 之后，而 sec-projects 原本在 sec-asset-history 之后（positions 7-8）。执行 Task 5 Step 1-3 后，完整行顺序为：

```
标题栏
sec-health
sec-calendar
sec-archive
sec-accounts       ← 移入（Step 1）
sec-projects       ← 原来在这里
sec-ga             ← 原来在这里
sec-morning
sec-signals
sec-sim
Ticker
sec-questrade
sec-chart
sec-asset-history  ← 移入（Step 2）
经济日历           ← 移入（Step 3）
sec-news
AI+潮流 row
```

这个顺序中 projects 和 ga 夹在 invest 行里面！需要也把它们移到 invest section 之后。

**Step 3b: 移动 sec-projects + sec-ga 到经济日历之后**

把 `sec-projects` 行和 `sec-ga` 行（两个连续行）剪切，粘贴到经济日历 div 之后、`<!-- ── 财经资讯 (news) ── -->` 之前。

**剪切范围：**
```
    <!-- ── Row 2: Project ── -->
    <div class="row col-1" id="sec-projects">
```
到（含）sec-ga 的关闭 `</div>`（约第 915 行原来的位置）。

**粘贴到：** 经济日历 `</div>` 之后，`<!-- ── 财经资讯 (news) ── -->` 之前。

完成后行顺序：
```
标题栏
sec-health
sec-calendar
sec-archive
sec-accounts
sec-morning
sec-signals
sec-sim
Ticker
sec-questrade
sec-chart
sec-asset-history
经济日历
sec-projects       ← 移入
sec-ga             ← 移入
sec-news
AI+潮流 row
```

#### Step 4 (revised): 添加 4 个分组 `<section>` 标签

**life section：**

在 `<!-- ── 健康中心 & 运动 (life) ── -->` 之前插入：
```html
    <section class="grp-section" data-grp="life" id="grp-life">
```

在 `</div><!-- /#sec-archive -->` 之后、`<!-- ── 账户总览 (invest) ── -->` 之前插入：
```html
    </section><!-- /#grp-life -->
```

**invest section：**

在 `<!-- ── 账户总览 (invest) ── -->` 之前插入：
```html
    <section class="grp-section" data-grp="invest" id="grp-invest">
```

在经济日历 `</div>` 之后、`<!-- ── Row 2: Project ── -->` 之前插入：
```html
    </section><!-- /#grp-invest -->
```

**project section：**

在 `<!-- ── Row 2: Project ── -->` 之前插入：
```html
    <section class="grp-section" data-grp="project" id="grp-project">
```

在 `sec-ga` 行的关闭 `</div>` 之后、`<!-- ── 财经资讯 (news) ── -->` 之前插入：
```html
    </section><!-- /#grp-project -->
```

**news section：**

在 `<!-- ── 财经资讯 (news) ── -->` 之前插入：
```html
    <section class="grp-section" data-grp="news" id="grp-news">
```

在 `<!-- ── Row 5: AI News + Fashion News ── -->` 内的最后一个 `</div>` 之后（AI+潮流行结束后）、`</div><!-- /container -->` 之前插入：
```html
    </section><!-- /#grp-news -->
```

- [ ] **Step 5: 浏览器验证分组结构**

打开 DevTools Elements，展开 `.container`，确认：
1. 存在 4 个 `section.grp-section` 元素，`data-grp` 分别为 life/invest/project/news
2. 各 section 内只包含属于该分组的行
3. 页面所有板块正常显示（内容没有丢失）

- [ ] **Step 6: Commit**

```bash
git add dashboard/index.html
git commit -m "refactor: reorganize rows into life/invest/project/news group sections"
```

---

### Task 6: 添加导航 JS

**Files:**
- Modify: `dashboard/index.html` — 在最后一个 `</script>` 前（约第 3384 行）插入

- [ ] **Step 1: 在最后的 TradingAgents `</script>` 之前插入导航 JS**

找到：
```javascript
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeTsModal(); });
</script>
```

在 `</script>` 前插入：

```javascript
// ── Dashboard Navigation ──

function sbNav(el) {
  document.querySelectorAll('.sb-item').forEach(i => i.classList.remove('active'));
  el.classList.add('active');
  const target = document.getElementById(el.dataset.target);
  if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function switchTab(el) {
  const grp = el.dataset.grp;
  document.querySelectorAll('.bt-item').forEach(i => i.classList.remove('active'));
  el.classList.add('active');
  document.querySelectorAll('.grp-section').forEach(s => {
    s.classList.toggle('grp-hidden', s.dataset.grp !== grp);
  });
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

(function initScrollSpy() {
  if (window.innerWidth <= 480) return;
  const items = document.querySelectorAll('.sb-item[data-target]');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        items.forEach(i => i.classList.toggle('active', i.dataset.target === id));
      }
    });
  }, { threshold: 0.25 });
  items.forEach(i => {
    const el = document.getElementById(i.dataset.target);
    if (el) observer.observe(el);
  });
})();

(function initMobileTabs() {
  if (window.innerWidth > 480) return;
  document.querySelectorAll('.grp-section').forEach(s => {
    if (s.dataset.grp !== 'life') s.classList.add('grp-hidden');
  });
})();
```

- [ ] **Step 2: 验证桌面端导航功能**

在浏览器中（宽度 >480px）：
1. 点击侧边栏「📊 晨报」→ 页面平滑滚动到金融晨报板块，该项高亮
2. 手动滚动页面 → 当前可见板块对应的侧边栏项自动高亮

- [ ] **Step 3: 验证手机端 Tab 功能**

在 DevTools 切换到手机模拟（375px）：
1. 初始只显示生活板块（健康、日程、归档），其他分组隐藏
2. 点击底部「💹 投资」→ 投资分组显示，其他隐藏，页面滚到顶部
3. 点击底部「🚀 项目」→ 项目分组显示

- [ ] **Step 4: Commit**

```bash
git add dashboard/index.html
git commit -m "feat: add sidebar and bottom tab navigation JavaScript"
```

---

### Task 7: 部署到 Cloudflare Pages

**Files:**
- Run: `wrangler pages deploy dashboard/`

- [ ] **Step 1: 部署**

```bash
NODE_OPTIONS="" wrangler pages deploy dashboard/ --project-name riley-dashboard
```

Expected output:
```
✨ Success! Deployed to https://riley-dashboard.pages.dev
```

- [ ] **Step 2: 打开线上地址验证**

在手机 Chrome 上访问 Cloudflare Pages URL：
1. 底部 Tab 栏正常显示
2. 切换 Tab 正确隐藏/显示各分组

- [ ] **Step 3: Commit**

```bash
git add dashboard/index.html
git commit -m "chore: deploy dashboard navigation redesign to Cloudflare Pages"
```

---

## 自检清单

- [ ] 所有 4 个 `section.grp-section` 元素存在（life/invest/project/news）
- [ ] 每个 section 只包含属于该分组的行
- [ ] 侧边栏所有 `data-target` ID 在 HTML 中存在（sec-health, sec-workout, sec-calendar, sec-archive, sec-accounts, sec-morning, sec-signals, sec-questrade, sec-sim, sec-projects, sec-ga, sec-news）
- [ ] 桌面端：点击侧边栏项目能平滑滚动到对应板块
- [ ] 桌面端：滚动时侧边栏高亮自动更新
- [ ] 手机端：默认显示生活分组，其他分组隐藏
- [ ] 手机端：切换 Tab 正确切换显示的分组
- [ ] 所有原有板块数据和功能正常（账户同步、晨报、信号等）
