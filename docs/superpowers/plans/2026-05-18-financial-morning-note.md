# Financial Morning Note Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a full-width 金融晨报 card (Row 2.6) to Riley's Dashboard that displays daily market data, a morning briefing note, and 5 AI-selected stock picks with buy/sell timing — data sourced from a `morning-note.js` file written daily by a scheduled Claude Code agent.

**Architecture:** A scheduled agent searches for market data each morning at 07:30 and writes `dashboard/morning-note.js` (a JS variable file) and a dated archive to `dashboard/morning-note-history/`. The dashboard loads the JS file via a `<script>` tag — no fetch() needed, works reliably with file:// protocol. The card uses Tab switching between "今日晨报" (note text) and "📈 买卖时机" (5 stock picks).

**Tech Stack:** Vanilla HTML/CSS/JS (no build tools), Claude Code schedule skill for daily agent, Anthropic Claude API + WebSearch via scheduled routine.

---

## File Map

| File | Action | Responsibility |
|------|--------|---------------|
| `dashboard/morning-note.js` | **Create** | Live data (JS variable, overwritten daily by agent) |
| `dashboard/morning-note-history/.gitkeep` | **Create** | Keeps history directory in version control |
| `dashboard/index.html` line 317 | **Modify** | Add CSS for morning note card |
| `dashboard/index.html` line 319 | **Modify** | Add `<script src="morning-note.js">` tag in `<head>` |
| `dashboard/index.html` line 601–603 | **Modify** | Insert Row 2.6 HTML between analytics and ticker tape |
| `dashboard/index.html` line 1889 | **Modify** | Add JS functions + wire `loadMorningNote()` into init |

---

## Task 1: Create initial `morning-note.js` with sample data

**Files:**
- Create: `dashboard/morning-note.js`
- Create: `dashboard/morning-note-history/.gitkeep`

- [ ] **Step 1: Create `dashboard/morning-note.js`**

```javascript
// 金融晨报数据 — 每日 07:30 自动更新
window.MORNING_NOTE = {
  "date": "2026-05-18",
  "generated_at": "2026-05-18T07:30:00",
  "market_status": "pre-market",
  "market": {
    "sp500_futures_pct": -0.4,
    "treasury_10y": 4.55,
    "treasury_10y_change_bps": 9,
    "eps_beat_rate": 84
  },
  "note": {
    "market_overview": "美股期货延续上周五跌势，S&P 500 期货下跌 0.4%。市场情绪谨慎，投资者等待本周 Nvidia 财报（预期 EPS $1.78），视为 AI 行情风向标。自3月30日低点，S&P 已累计反弹 +13%。",
    "macro": "10年期美债升至 4.55%（一年新高），加息概率升至 45%。新Fed主席 Kevin Warsh 接替 Powell，政策不确定性上升。油价因伊朗局势走高。",
    "earnings": "Q1 财报季亮眼：84% 公司 EPS 超预期，超预期幅度 +18.2%（历史均值7%）。Alphabet 4月涨 +34%，为2004年来最强单月。全年 EPS 增速预期调升至 18.6%。",
    "trade_ideas": "⚡ 谨慎科技多单：收益率飙升压制高估值成长股。⚡ 关注能源板块：油价受地缘支撑，中期机会。⚡ NVDA 期权：财报前 IV 高企，可考虑卖出宽跨式策略。"
  },
  "stock_picks": [
    {
      "ticker": "NVDA",
      "name": "Nvidia",
      "sector": "科技/半导体",
      "direction": "watch",
      "buy_zone": "$900–$920",
      "target": "$980",
      "stop_loss": "$870",
      "reason": "财报前 IV 高企，等财报方向确认后再入场，勿追涨"
    },
    {
      "ticker": "XOM",
      "name": "ExxonMobil",
      "sector": "能源",
      "direction": "buy",
      "buy_zone": "$118–$122",
      "target": "$135",
      "stop_loss": "$112",
      "reason": "地缘风险支撑油价，能源板块中期受益，估值合理"
    },
    {
      "ticker": "UNH",
      "name": "UnitedHealth",
      "sector": "医疗保险",
      "direction": "watch",
      "buy_zone": "$480–$495",
      "target": "$530",
      "stop_loss": "$465",
      "reason": "医疗板块防御性强，等待回调至支撑位再买入"
    },
    {
      "ticker": "TLT",
      "name": "iShares 20Y美债ETF",
      "sector": "固定收益",
      "direction": "sell",
      "buy_zone": "—",
      "target": "—",
      "stop_loss": "—",
      "reason": "收益率上升期长债价格承压，暂时回避，等加息预期降温"
    },
    {
      "ticker": "COST",
      "name": "Costco",
      "sector": "消费/零售",
      "direction": "buy",
      "buy_zone": "$890–$910",
      "target": "$960",
      "stop_loss": "$875",
      "reason": "通胀环境下消费者首选，会员续费率稳健，防御性强"
    }
  ]
};
```

- [ ] **Step 2: Create history directory placeholder**

```bash
touch /Users/apple/claude-whatsapp/dashboard/morning-note-history/.gitkeep
```

- [ ] **Step 3: Verify files exist**

```bash
ls /Users/apple/claude-whatsapp/dashboard/morning-note.js
ls /Users/apple/claude-whatsapp/dashboard/morning-note-history/
```

Expected: both paths exist with no errors.

---

## Task 2: Add CSS styles to `index.html`

**Files:**
- Modify: `dashboard/index.html:317` (insert before `    </style>` on line 318)

- [ ] **Step 1: Insert CSS block before `    </style>` (line 318)**

Find the exact string `        /* ── Responsive ──` in the CSS section and insert the following block immediately before it:

```css
        /* ── Morning Note ────────────────────────── */
        .mn-tab {
            background:#f5f5f5; color:#777; border:1px solid #e8e8e8;
            padding:3px 14px; border-radius:20px; font-size:10px; font-weight:600;
            cursor:pointer; font-family:inherit; transition:all .15s; letter-spacing:.04em;
        }
        .mn-tab.active { background:#111; color:#fff; border-color:#111; }
        .mn-tab:hover:not(.active) { color:#555; border-color:#ccc; }
        .mn-key-card { background:#f8f8f8; border:1px solid #e8e8e8; border-radius:8px; padding:10px 12px; }
        .mn-key-lbl { font-size:9px; color:#999; text-transform:uppercase; letter-spacing:.06em; margin-bottom:3px; }
        .mn-key-val { font-size:20px; font-weight:800; color:#111; font-family:'Poppins',sans-serif; letter-spacing:-.3px; }
        .mn-key-sub { font-size:9px; color:#bbb; margin-top:2px; }
        .mn-section { margin-bottom:14px; }
        .mn-section-lbl {
            display:inline-block; padding:1px 8px; border-radius:4px;
            font-size:9px; font-weight:600; text-transform:uppercase; letter-spacing:.06em; margin-bottom:6px;
        }
        .mn-lbl-default { background:#f0f0f0; color:#777; }
        .mn-lbl-green   { background:#f0fdf4; color:#16a34a; }
        .mn-lbl-orange  { background:#fff7ed; color:#ea580c; }
        .mn-section-text { font-size:12px; color:#555; line-height:1.75; margin:0; }
        .mn-stock-card { border:1px solid #e8e8e8; border-radius:10px; padding:12px 14px; margin-bottom:8px; background:#f8f8f8; }
        .mn-stock-hd { display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; }
        .mn-ticker { font-size:14px; font-weight:800; color:#111; margin-right:6px; }
        .mn-stock-name { font-size:10px; color:#777; }
        .mn-direction { font-size:9px; font-weight:700; padding:2px 10px; border-radius:10px; flex-shrink:0; }
        .mn-direction.buy   { background:#f0fdf4; color:#16a34a; }
        .mn-direction.sell  { background:#fef2f2; color:#dc2626; }
        .mn-direction.watch { background:#fff7ed; color:#ea580c; }
        .mn-stock-nums { display:grid; grid-template-columns:repeat(3,1fr); gap:8px; margin-bottom:8px; }
        .mn-num-lbl { font-size:9px; color:#999; margin-bottom:2px; }
        .mn-num-val { font-size:11px; font-weight:600; color:#111; }
        .mn-reason { font-size:10px; color:#888; padding-top:8px; border-top:1px solid #eee; line-height:1.5; }
        .mn-empty { color:#999; font-size:12px; text-align:center; padding:20px 0; }

```

- [ ] **Step 2: Verify CSS was inserted**

```bash
grep -n "mn-tab\|mn-key-card\|mn-stock-card" /Users/apple/claude-whatsapp/dashboard/index.html | head -5
```

Expected: 3+ lines found with line numbers in the 310–320 range.

---

## Task 3: Add `<script src="morning-note.js">` to `<head>`

**Files:**
- Modify: `dashboard/index.html:319` (the `</head>` line)

- [ ] **Step 1: Insert script tag before `</head>` (line 319)**

Find `</head>` and replace it with:

```html
    <script src="morning-note.js"></script>
</head>
```

- [ ] **Step 2: Verify**

```bash
grep -n "morning-note.js" /Users/apple/claude-whatsapp/dashboard/index.html
```

Expected: one line found around line 319.

---

## Task 4: Insert Row 2.6 HTML into `index.html`

**Files:**
- Modify: `dashboard/index.html:601–603` (between analytics row closing `</div>` and `<!-- ── Row 3: Ticker tape ──`)

- [ ] **Step 1: Insert morning note HTML row**

Find the comment `    <!-- ── Row 3: Ticker tape ── -->` and insert the following block immediately before it:

```html
    <!-- ── Row 2.6: 金融晨报 ── -->
    <div class="row col-1">
        <div class="card">
            <div class="card-hd">
                <span class="card-title">📊 金融晨报</span>
                <div style="display:flex;align-items:center;gap:10px">
                    <span id="mn-date-badge" style="font-size:9px;background:#f0f0f0;padding:2px 10px;border-radius:10px;color:#888"></span>
                    <span id="mn-status-badge" style="font-size:9px;font-weight:700;background:#fef2f2;color:#dc2626;padding:2px 10px;border-radius:10px;display:none"></span>
                    <span id="mn-updated-lbl" style="font-size:9px;color:#ccc"></span>
                    <button onclick="loadMorningNote()" style="background:none;border:none;color:#ccc;cursor:pointer;font-size:14px;padding:2px" title="刷新" onmouseover="this.style.color='#666'" onmouseout="this.style.color='#ccc'">↻</button>
                </div>
            </div>
            <div style="display:grid;grid-template-columns:200px 1fr;gap:20px;align-items:start">
                <!-- Left: Key Numbers -->
                <div style="border-right:1px solid #f0f0f0;padding-right:20px">
                    <div class="card-title" style="margin-bottom:10px">关键数据</div>
                    <div style="display:flex;flex-direction:column;gap:10px">
                        <div class="mn-key-card">
                            <div class="mn-key-lbl">S&P 500 期货</div>
                            <div id="mn-sp-val" class="mn-key-val">—</div>
                            <div id="mn-sp-sub" class="mn-key-sub">—</div>
                        </div>
                        <div class="mn-key-card">
                            <div class="mn-key-lbl">10年期美债</div>
                            <div id="mn-bond-val" class="mn-key-val">—</div>
                            <div id="mn-bond-sub" class="mn-key-sub">—</div>
                        </div>
                        <div class="mn-key-card">
                            <div class="mn-key-lbl">Q1 EPS 超预期率</div>
                            <div id="mn-eps-val" class="mn-key-val pos">—</div>
                            <div class="mn-key-sub">高于5年均值 78%</div>
                        </div>
                    </div>
                </div>
                <!-- Right: Tabs -->
                <div>
                    <div style="display:flex;gap:6px;margin-bottom:14px">
                        <button class="mn-tab active" id="mn-tab-note" onclick="switchMnTab('note')">今日晨报</button>
                        <button class="mn-tab" id="mn-tab-picks" onclick="switchMnTab('picks')">📈 买卖时机</button>
                    </div>
                    <!-- Tab 1: Note -->
                    <div id="mn-pane-note" style="overflow-y:auto;max-height:260px">
                        <div class="mn-section">
                            <span class="mn-section-lbl mn-lbl-default">市场概况</span>
                            <p id="mn-market-overview" class="mn-section-text mn-empty">加载中…</p>
                        </div>
                        <div class="mn-section">
                            <span class="mn-section-lbl mn-lbl-default">宏观焦点</span>
                            <p id="mn-macro" class="mn-section-text"></p>
                        </div>
                        <div class="mn-section">
                            <span class="mn-section-lbl mn-lbl-green">财报亮点</span>
                            <p id="mn-earnings" class="mn-section-text"></p>
                        </div>
                        <div class="mn-section">
                            <span class="mn-section-lbl mn-lbl-orange">交易建议</span>
                            <p id="mn-trade-ideas" class="mn-section-text"></p>
                        </div>
                    </div>
                    <!-- Tab 2: Stock Picks -->
                    <div id="mn-pane-picks" style="display:none;overflow-y:auto;max-height:260px">
                        <div style="font-size:9px;color:#888;margin-bottom:10px">今日 AI 全市场筛选 · 5支关注股票</div>
                        <div id="mn-picks-list"></div>
                        <div style="font-size:9px;color:#bbb;padding-top:8px;margin-top:4px;border-top:1px solid #f0f0f0">仅供参考，不构成投资建议 · 数据每日 07:30 自动更新并存档</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

```

- [ ] **Step 2: Verify HTML inserted**

```bash
grep -n "Row 2.6\|mn-pane-note\|mn-picks-list" /Users/apple/claude-whatsapp/dashboard/index.html | head -5
```

Expected: lines found around the 603–650 area.

---

## Task 5: Add JS functions to `index.html`

**Files:**
- Modify: `dashboard/index.html:1889` (insert before the closing `</script>` tag, after the async news IIFE)

- [ ] **Step 1: Insert JS functions before `</script>` (line 1890)**

Find `</script>` at the very end of the file (line 1890) and insert the following block immediately before it:

```javascript

// ── Morning Note ──────────────────────────────────────
function loadMorningNote() {
    if (window.MORNING_NOTE) {
        renderMorningNote(window.MORNING_NOTE);
    } else {
        const el = document.getElementById('mn-market-overview');
        if (el) { el.textContent = '今日晨报生成中，请稍后刷新…'; el.classList.add('mn-empty'); }
        ['mn-macro','mn-earnings','mn-trade-ideas'].forEach(id => {
            const e = document.getElementById(id); if (e) e.textContent = '';
        });
    }
}

function renderMorningNote(d) {
    // Header badges
    const dateBadge = document.getElementById('mn-date-badge');
    if (dateBadge && d.date) dateBadge.textContent = '🗓 ' + d.date;

    const updLbl = document.getElementById('mn-updated-lbl');
    if (updLbl && d.generated_at) updLbl.textContent = '最后更新 ' + d.generated_at.slice(11, 16);

    const statusBadge = document.getElementById('mn-status-badge');
    if (statusBadge) {
        statusBadge.style.display = 'inline';
        statusBadge.textContent = d.market_status === 'pre-market' ? '● 盘前' :
                                  d.market_status === 'open'       ? '● 开盘中' : '● 收盘';
    }

    // Left: key numbers
    const sp = d.market.sp500_futures_pct;
    const spEl = document.getElementById('mn-sp-val');
    if (spEl) {
        spEl.textContent = (sp >= 0 ? '↑ +' : '↓ ') + Math.abs(sp).toFixed(1) + '%';
        spEl.className = 'mn-key-val ' + (sp >= 0 ? 'pos' : 'neg');
    }
    const spSub = document.getElementById('mn-sp-sub');
    if (spSub) spSub.textContent = '纳指同步' + (sp >= 0 ? '上涨' : '下跌');

    const bondEl = document.getElementById('mn-bond-val');
    if (bondEl) bondEl.textContent = d.market.treasury_10y.toFixed(2) + '%';
    const bondSub = document.getElementById('mn-bond-sub');
    if (bondSub) {
        const bps = d.market.treasury_10y_change_bps;
        bondSub.textContent = (bps >= 0 ? '+' : '') + bps + 'bps · ' + (bps >= 0 ? '上升' : '下降');
    }

    const epsEl = document.getElementById('mn-eps-val');
    if (epsEl) {
        epsEl.textContent = d.market.eps_beat_rate + '%';
        epsEl.className = 'mn-key-val ' + (d.market.eps_beat_rate >= 70 ? 'pos' : 'neg');
    }

    // Right: note sections
    const fields = {
        'mn-market-overview': d.note.market_overview,
        'mn-macro':           d.note.macro,
        'mn-earnings':        d.note.earnings,
        'mn-trade-ideas':     d.note.trade_ideas,
    };
    Object.entries(fields).forEach(([id, text]) => {
        const el = document.getElementById(id);
        if (el) { el.textContent = text; el.classList.remove('mn-empty'); }
    });

    // Stock picks
    renderStockPicks(d.stock_picks);
}

function renderStockPicks(picks) {
    const container = document.getElementById('mn-picks-list');
    if (!container) return;
    if (!picks || picks.length === 0) {
        container.innerHTML = '<div class="mn-empty">暂无推荐股票</div>';
        return;
    }
    container.innerHTML = picks.map(p => {
        const dirClass = p.direction === 'buy' ? 'buy' : p.direction === 'sell' ? 'sell' : 'watch';
        const dirText  = p.direction === 'buy'  ? '✓ 买入' :
                         p.direction === 'sell' ? '✗ 卖出/避开' : '⏳ 观望';
        return `<div class="mn-stock-card">
            <div class="mn-stock-hd">
                <div>
                    <span class="mn-ticker">${p.ticker}</span>
                    <span class="mn-stock-name">${p.name} · ${p.sector}</span>
                </div>
                <span class="mn-direction ${dirClass}">${dirText}</span>
            </div>
            <div class="mn-stock-nums">
                <div><div class="mn-num-lbl">买入区间</div><div class="mn-num-val">${p.buy_zone}</div></div>
                <div><div class="mn-num-lbl">目标价</div><div class="mn-num-val pos">${p.target}</div></div>
                <div><div class="mn-num-lbl">止损价</div><div class="mn-num-val neg">${p.stop_loss}</div></div>
            </div>
            <div class="mn-reason">${p.reason}</div>
        </div>`;
    }).join('');
}

function switchMnTab(tab) {
    document.getElementById('mn-pane-note').style.display  = tab === 'note'  ? 'block' : 'none';
    document.getElementById('mn-pane-picks').style.display = tab === 'picks' ? 'block' : 'none';
    document.getElementById('mn-tab-note').classList.toggle('active',  tab === 'note');
    document.getElementById('mn-tab-picks').classList.toggle('active', tab === 'picks');
}
```

- [ ] **Step 2: Verify functions exist**

```bash
grep -n "function loadMorningNote\|function renderMorningNote\|function renderStockPicks\|function switchMnTab" /Users/apple/claude-whatsapp/dashboard/index.html
```

Expected: 4 lines found.

---

## Task 6: Wire `loadMorningNote()` into page init

**Files:**
- Modify: `dashboard/index.html` — the `(async () => {` IIFE near line 1883

- [ ] **Step 1: Add `loadMorningNote()` call to init IIFE**

Find this exact block:

```javascript
// Init news on load
(async () => {
    await Promise.all([
        loadSection('fin'),
```

Replace it with:

```javascript
// Init news on load
(async () => {
    loadMorningNote();
    await Promise.all([
        loadSection('fin'),
```

- [ ] **Step 2: Verify**

```bash
grep -n "loadMorningNote" /Users/apple/claude-whatsapp/dashboard/index.html
```

Expected: 2 lines — the function definition and the init call.

---

## Task 7: Manual browser verification

- [ ] **Step 1: Open dashboard in browser**

```bash
open /Users/apple/claude-whatsapp/dashboard/index.html
```

- [ ] **Step 2: Check morning note card appears**

Scroll down past project tracking and website analytics. Verify:
- "📊 金融晨报" card is visible
- Left column shows 3 key number cards: S&P 500 (red ↓ 0.4%), 10Y美债 (4.55%), EPS (84%)
- "今日晨报" tab is active by default, showing 4 text sections

- [ ] **Step 3: Check stock picks tab**

Click "📈 买卖时机" tab. Verify:
- 5 stock cards appear (NVDA, XOM, UNH, TLT, COST)
- Each card shows direction badge (green/red/orange), 3 price fields, and a reason line

- [ ] **Step 4: Check refresh button**

Click ↻ button in card header. Page should reload the note without errors (console shows no JS errors).

---

## Task 8: Configure daily scheduled agent

**Files:** None (uses Claude Code `schedule` skill)

- [ ] **Step 1: Invoke the schedule skill**

Run: `/schedule`

When prompted, configure a new routine with:
- **Name:** `金融晨报生成`
- **Schedule:** Daily at 07:30 (Beijing time) — cron: `30 23 * * *` (UTC, Beijing = UTC+8)
- **Prompt:** (exact text below)

```
Search the web for today's US stock market data: S&P 500 futures change percentage, 10-year Treasury yield and basis point change, Q1 earnings beat rate. Also search for 5 notable stocks from different sectors (tech, energy, healthcare, consumer, fixed income) with current market context.

Then write a morning note JSON to two files:

1. Write to /Users/apple/claude-whatsapp/dashboard/morning-note.js with this exact format (replace all values with today's real data):

window.MORNING_NOTE = {
  "date": "YYYY-MM-DD",
  "generated_at": "YYYY-MM-DDTHH:MM:00",
  "market_status": "pre-market",
  "market": {
    "sp500_futures_pct": NUMBER,
    "treasury_10y": NUMBER,
    "treasury_10y_change_bps": NUMBER,
    "eps_beat_rate": NUMBER
  },
  "note": {
    "market_overview": "2-3 sentences in Chinese, beginner-friendly, explain what the numbers mean",
    "macro": "2-3 sentences in Chinese about rates, Fed, geopolitics",
    "earnings": "2-3 sentences in Chinese about this earnings season",
    "trade_ideas": "3 bullet points in Chinese starting with ⚡, short actionable ideas"
  },
  "stock_picks": [
    {
      "ticker": "TICKER",
      "name": "Company Name",
      "sector": "板块/细分",
      "direction": "buy OR sell OR watch",
      "buy_zone": "$X–$Y or —",
      "target": "$X or —",
      "stop_loss": "$X or —",
      "reason": "One sentence in Chinese, beginner-friendly explanation"
    }
  ]
};

2. Also write the same data as JSON to /Users/apple/claude-whatsapp/dashboard/morning-note-history/YYYY-MM-DD.json (use today's date).

Rules:
- Exactly 5 stock picks, covering different sectors
- All text in Chinese
- direction must be exactly "buy", "sell", or "watch"
- Keep explanations simple — the reader is a stock market beginner
```

- [ ] **Step 2: Verify schedule was created**

Run: `/schedule list`

Expected: routine named "金融晨报生成" appears with daily schedule.

- [ ] **Step 3: Run once manually to test**

Run: `/schedule run 金融晨报生成`

After completion, verify:

```bash
cat /Users/apple/claude-whatsapp/dashboard/morning-note.js | head -5
ls /Users/apple/claude-whatsapp/dashboard/morning-note-history/
```

Expected: `morning-note.js` has today's date, history directory has a dated JSON file.

- [ ] **Step 4: Reload dashboard in browser and confirm live data appears**

```bash
open /Users/apple/claude-whatsapp/dashboard/index.html
```

Verify the date badge shows today's date and market numbers reflect real data.

---

## Self-Review Checklist

**Spec coverage:**
- ✅ Row 3 全宽独立行 → Task 4 (HTML insertion)
- ✅ 左侧3个关键数字 → Task 4 HTML + Task 5 `renderMorningNote()`
- ✅ Tab切换：今日晨报/买卖时机 → Task 4 HTML + Task 5 `switchMnTab()`
- ✅ 每日5支股票，买入区间/目标/止损/理由 → Task 5 `renderStockPicks()` + Task 1 data structure
- ✅ direction枚举 buy/sell/watch → Task 5 renderStockPicks dirClass/dirText
- ✅ JSON存档到morning-note-history/ → Task 8 agent prompt
- ✅ 每天07:30自动生成 → Task 8 schedule
- ✅ 数据缺失时显示占位 → Task 5 `loadMorningNote()` else branch
- ✅ 手动刷新按钮 → Task 4 HTML (↻ button calls `loadMorningNote()`)
- ✅ 新手友好文字说明 → Task 8 agent prompt instructions

**Type consistency:** `window.MORNING_NOTE` set in Task 1, read in Task 5 `loadMorningNote()` — consistent. `d.market.sp500_futures_pct`, `d.market.treasury_10y`, `d.market.treasury_10y_change_bps`, `d.market.eps_beat_rate` used in `renderMorningNote()` — all match Task 1 JSON keys. `d.stock_picks[].direction` / `.buy_zone` / `.target` / `.stop_loss` / `.reason` used in `renderStockPicks()` — match Task 1 and Task 8 prompt format.
