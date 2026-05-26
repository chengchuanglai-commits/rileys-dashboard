const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const fs = require('fs');
const path = require('path');

const HISTORY_FILE = path.join(__dirname, 'data', 'self_history.json');
const SUMMARY_FILE = path.join(__dirname, 'data', 'summaries.json');
const FINANCE_FILE = path.join(__dirname, 'data', 'finance.json');

const SYNC_URL = 'https://questrade-proxy.chengchuang-lai.workers.dev/sync';

function parseCalendarDate(str) {
    const today = new Date();
    const s = str.trim();
    if (s === '明天') {
        const d = new Date(today); d.setDate(d.getDate() + 1);
        return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
    }
    if (s === '后天') {
        const d = new Date(today); d.setDate(d.getDate() + 2);
        return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
    }
    const slash = s.match(/^(\d{1,2})\/(\d{1,2})$/);
    if (slash) {
        const year = today.getFullYear();
        const m = slash[1].padStart(2,'0'), d = slash[2].padStart(2,'0');
        const candidate = `${year}-${m}-${d}`;
        return new Date(candidate) < today ? `${year+1}-${m}-${d}` : candidate;
    }
    const cn = s.match(/^(\d{1,2})月(\d{1,2})日?$/);
    if (cn) {
        const year = today.getFullYear();
        const m = cn[1].padStart(2,'0'), d = cn[2].padStart(2,'0');
        const candidate = `${year}-${m}-${d}`;
        return new Date(candidate) < today ? `${year+1}-${m}-${d}` : candidate;
    }
    return null;
}

const botMessageIds = new Set();
let myWid = null;
let selfChatId = null;

function loadJSON(file, def) {
    try { if (fs.existsSync(file)) return JSON.parse(fs.readFileSync(file, 'utf8')); } catch (e) {}
    return def;
}
function saveJSON(file, data) {
    fs.writeFileSync(file, JSON.stringify(data, null, 2));
}

let allRecords = loadJSON(HISTORY_FILE, []);
let finance = loadJSON(FINANCE_FILE, { balance: null, expenses: [] });
let chatContext = [];

function createClient() {
    return new Client({
        authStrategy: new LocalAuth(),
        puppeteer: {
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--proxy-server=http://127.0.0.1:7897'],
            timeout: 120000,
            protocolTimeout: 180000
        }
    });
}

let client = createClient();

function initClient(c) {
    c.on('qr', (qr) => {
        console.log('请用 WhatsApp 扫描以下二维码：');
        qrcode.generate(qr, { small: true });
    });

    c.on('ready', async () => {
        myWid = c.info.wid._serialized;
        selfChatId = myWid;
        console.log(`✅ WhatsApp 已连接！(${myWid})`);
        scheduleMonthlyCheck();
        scheduleDailyBalanceReminder(c);
        // 重连后检查余额是否过期
        await checkBalanceOnReconnect(c);
    });

    c.on('disconnected', (reason) => {
        console.log('⚠️ WhatsApp 断线：', reason, '5秒后重连...');
        setTimeout(() => {
            client = createClient();
            initClient(client);
            startWithRetry(client);
        }, 5000);
    });

    c.on('message', (msg) => processMessage(msg));
    c.on('message_create', (msg) => {
        if (!msg.fromMe || !myWid) return;
        if (msg.from !== myWid) return;
        processMessage(msg);
    });
}

// 图片处理队列（防止并发打爆 Ollama）
let imageQueue = Promise.resolve();
function enqueueImage(fn) {
    imageQueue = imageQueue.then(fn).catch(() => {});
    return imageQueue;
}

// 文字模型（带重试）
async function askOllama(messages, systemPrompt) {
    for (let i = 0; i < 3; i++) {
        try {
            const res = await fetch('http://localhost:11434/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    model: 'qwen2.5:7b',
                    messages: [
                        { role: 'system', content: systemPrompt || '你是一个智能助手，通过 WhatsApp 与用户对话。回复要简洁、自然，适合移动端阅读。' },
                        ...messages
                    ],
                    stream: false
                })
            });
            const data = await res.json();
            return data.message.content;
        } catch (e) {
            if (i === 2) throw e;
            await new Promise(r => setTimeout(r, 5000));
        }
    }
}

// 从模型输出中提取合法 JSON（忽略前后多余文字）
function extractJSON(text) {
    const start = text.indexOf('{');
    if (start === -1) return null;
    let depth = 0, inStr = false, esc = false;
    for (let i = start; i < text.length; i++) {
        const c = text[i];
        if (esc) { esc = false; continue; }
        if (c === '\\' && inStr) { esc = true; continue; }
        if (c === '"') { inStr = !inStr; continue; }
        if (inStr) continue;
        if (c === '{' || c === '[') depth++;
        else if (c === '}' || c === ']') {
            depth--;
            if (depth === 0) {
                try { return JSON.parse(text.slice(start, i + 1)); } catch (_) {}
            }
        }
    }
    // 兜底：模型漏掉结尾 }，手动补上再试
    try { return JSON.parse(text.slice(start) + '}'); } catch (_) {}
    return null;
}

// 视觉模型：识别图片（带重试）
async function askOllamaVision(base64Image, prompt) {
    for (let i = 0; i < 3; i++) {
        try {
            const res = await fetch('http://localhost:11434/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    model: 'qwen2.5vl:7b',
                    messages: [{
                        role: 'user',
                        content: prompt,
                        images: [base64Image]
                    }],
                    stream: false
                })
            });
            const data = await res.json();
            return data.message.content;
        } catch (e) {
            if (i === 2) throw e;
            await new Promise(r => setTimeout(r, 5000));
        }
    }
}

// 解析图片内容并更新财务数据（两步法：视觉识别 → 文字解析）
async function handleFinanceImage(base64Image) {
    // 第一步：视觉模型自由描述图片内容
    const rawText = await askOllamaVision(base64Image,
        '请完整描述这张图片里所有的文字和数字内容，特别是金额、商家名称、账户余额等信息。直接输出原始内容，不要分析。'
    );
    console.log('[图片识别原文]', rawText);

    // 第二步：文字模型把原文解析成结构化 JSON
    const parseResult = await askOllama([{
        role: 'user',
        content: `以下是从截图中识别出的文字内容：\n\n${rawText}\n\n请判断这是【余额截图】还是【消费截图】，并提取数据：
- 余额截图：提取账户人民币余额，返回 {"type":"balance","amount":数字}
- 消费截图：只提取本次实际支付金额（如"支付成功 ¥138.50"、"实付款"、"付款金额"等），忽略页面中"为您推荐"、商品推荐、广告等无关内容。商家名称取支付平台或店铺名（如"山姆"、"支付宝"等），返回 {"type":"expense","items":[{"name":"商家名","amount":数字}]}
只返回 JSON，不要其他文字。`
    }], '你是一个财务数据解析助手，只提取实际发生的交易金额，忽略推荐商品和广告，只输出合法 JSON。');
    console.log('[解析结果]', parseResult);

    const now = new Date().toISOString();
    let reply = '';

    try {
        const parsed = extractJSON(parseResult);
        if (!parsed) throw new Error('未找到合法 JSON');

        if (parsed.type === 'balance' && parsed.amount) {
            const newAmount = parseFloat(parsed.amount);
            const oldAmount = finance.balance?.amount ?? null;
            const oldDate = finance.balance?.date ?? null;

            // 计算与上次记录余额的差额
            if (oldAmount !== null) {
                const todayRecorded = finance.expenses
                    .filter(e => e.date > oldDate)
                    .reduce((s, e) => s + e.amount, 0);
                const expectedBalance = parseFloat((oldAmount - todayRecorded).toFixed(2));
                const gap = parseFloat((expectedBalance - newAmount).toFixed(2));

                finance.balance = { amount: newAmount, date: now };
                saveJSON(FINANCE_FILE, finance);
                syncIcbcToDashboard(newAmount);

                reply = `✅ 余额已更新：¥${newAmount.toLocaleString()}`;
                if (gap > 1) {
                    reply += `\n\n⚠️ *检测到 ¥${gap.toFixed(2)} 未记录支出*\n（上次余额 ¥${oldAmount.toLocaleString()} - 已记录消费 ¥${todayRecorded.toFixed(2)} = 预期 ¥${expectedBalance.toLocaleString()}，实际 ¥${newAmount.toLocaleString()}）\n\n请补录漏掉的消费，可以：\n• 发送消费截图\n• 或发送文字：/消费 金额 备注\n  例：/消费 38 iCloud订阅`;
                }
            } else {
                finance.balance = { amount: newAmount, date: now };
                saveJSON(FINANCE_FILE, finance);
                syncIcbcToDashboard(newAmount);
                reply = `✅ 已记录初始余额：¥${newAmount.toLocaleString()}\n日期：${now}`;
            }
        }

        else if (parsed.type === 'expense' && parsed.items?.length > 0) {
            let total = 0;
            const items = parsed.items.map(i => ({
                name: i.name || '未知商家',
                amount: parseFloat(i.amount),
                date: now
            }));
            total = items.reduce((s, i) => s + i.amount, 0);

            finance.expenses.push(...items);

            if (finance.balance) {
                finance.balance.amount = parseFloat((finance.balance.amount - total).toFixed(2));
            }
            saveJSON(FINANCE_FILE, finance);

            reply = `✅ 已记录消费（${now}）：\n`;
            items.forEach(i => { reply += `• ${i.name}：¥${i.amount}\n`; });
            reply += `本次合计：¥${total.toFixed(2)}`;

            if (finance.balance) {
                reply += `\n\n💰 扣减后余额：¥${finance.balance.amount.toLocaleString()}`;
            } else {
                reply += '\n\n⚠️ 尚未记录账户余额，请先发送余额截图';
            }
        }
    } catch (e) {
        console.error('[解析失败]', e.message, parseResult);
        reply = `图片已识别，但解析失败，原始内容：\n${rawText}`;
    }

    return reply || `图片内容：\n${rawText}`;
}

// 把工行余额同步到 Dashboard（Cloudflare KV）
async function syncIcbcToDashboard(icbc) {
    try {
        const res = await fetch(SYNC_URL);
        let data = await res.json().catch(() => null);
        if (!data || typeof data !== 'object' || Array.isArray(data)) data = {};
        const accounts = data.accounts_v2 || { icbc:0, hsbc:0, bmo:0, bmo_tfsa:0, bmo_rrsp:0, bmo_inv:0, futu:0 };
        accounts.icbc = icbc;
        data.accounts_v2 = accounts;
        await fetch(SYNC_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        console.log(`[Dashboard] 工行余额已同步：¥${icbc.toLocaleString()}`);
    } catch (e) {
        console.error('[Dashboard] 同步失败：', e.message);
    }
}

// 月度支出总结
async function generateMonthlySummary(yearMonth) {
    const monthExpenses = finance.expenses.filter(e => e.date.startsWith(yearMonth));
    if (monthExpenses.length === 0) return null;

    const total = monthExpenses.reduce((s, e) => s + e.amount, 0);
    const byName = {};
    monthExpenses.forEach(e => { byName[e.name] = (byName[e.name] || 0) + e.amount; });
    const sorted = Object.entries(byName).sort((a, b) => b[1] - a[1]);

    let detail = `📊 *${yearMonth} 支出明细*\n\n`;
    detail += `总支出：¥${total.toFixed(2)}\n\n`;
    detail += `*各类消费：*\n`;
    sorted.forEach(([name, amount]) => {
        detail += `• ${name}：¥${amount.toFixed(2)}\n`;
    });

    const aiSummary = await askOllama(
        [{ role: 'user', content: `我${yearMonth}的消费记录如下：\n${JSON.stringify(monthExpenses)}\n请给一个简短的消费分析和建议。` }],
        '你是一个个人财务助手，分析要简洁，适合手机阅读。'
    );
    detail += `\n💡 *AI分析：*\n${aiSummary}`;
    return detail;
}

function getYearMonth(date) {
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
}

// 重连后检查余额是否超过 6 小时未更新，自动提醒
async function checkBalanceOnReconnect(c) {
    await new Promise(r => setTimeout(r, 3000)); // 等连接稳定
    const chat = await c.getChatById(myWid).catch(() => null);
    if (!chat) return;

    if (!finance.balance) {
        await chat.sendMessage('👋 检测到尚未记录账户余额，请发送一张余额截图来初始化。');
        return;
    }

    const lastUpdate = new Date(finance.balance.date);
    const hoursSince = (Date.now() - lastUpdate.getTime()) / 3600000;

    if (hoursSince > 6) {
        const msg = `🔄 *余额同步提醒*\n\n上次余额更新于 ${finance.balance.date}（${Math.floor(hoursSince)}小时前）\n当前记录余额：¥${finance.balance.amount.toLocaleString()}\n\n请发送最新余额截图以同步余额，避免因离线期间的消费导致数据偏差。`;
        await chat.sendMessage(msg);
        console.log('已发送余额同步提醒');
    }
}

// 每天早上 8:00 自动提醒更新余额
function scheduleDailyBalanceReminder(c) {
    const scheduleNext = () => {
        const now = new Date();
        const next = new Date();
        next.setHours(8, 0, 0, 0);
        if (next <= now) next.setDate(next.getDate() + 1);
        const delay = next.getTime() - now.getTime();

        setTimeout(async () => {
            try {
                const chat = await c.getChatById(myWid).catch(() => null);
                if (chat && finance.balance) {
                    await chat.sendMessage(`☀️ *早安！每日余额提醒*\n\n昨日记录余额：¥${finance.balance.amount.toLocaleString()}\n\n如有未记录的消费，请发送最新余额截图或消费截图更新数据。`);
                }
            } catch (e) {
                console.error('每日提醒发送失败:', e.message);
            }
            scheduleNext();
        }, delay);

        console.log(`下次余额提醒：${next.toLocaleString()}`);
    };
    scheduleNext();
}

function scheduleMonthlyCheck() {
    const check = async () => {
        const now = new Date();
        if (now.getDate() !== 1) return;
        const lastMonth = new Date(now.getFullYear(), now.getMonth() - 1, 1);
        const yearMonth = getYearMonth(lastMonth);
        const summaries = loadJSON(SUMMARY_FILE, {});
        if (summaries[yearMonth]) return;
        const summary = await generateMonthlySummary(yearMonth);
        if (!summary) return;
        summaries[yearMonth] = summary;
        saveJSON(SUMMARY_FILE, summaries);
        if (selfChatId) {
            const chat = await client.getChatById(selfChatId);
            await chat.sendMessage(summary);
            console.log(`✅ ${yearMonth} 月度总结已发送`);
        }
    };
    check();
    setInterval(check, 24 * 60 * 60 * 1000);
}

async function processMessage(msg) {
    const isImage = msg.type === 'image';
    const isText = msg.type === 'chat';
    if (!isImage && !isText) return;
    if (msg.isGroupMsg) return;

    if (botMessageIds.has(msg.id._serialized)) {
        botMessageIds.delete(msg.id._serialized);
        return;
    }

    if (!selfChatId) selfChatId = msg.from;

    let reply = '';

    if (isImage) {
        // 处理图片（排队，避免并发打爆 Ollama）
        await enqueueImage(async () => {
        try {
            const media = await msg.downloadMedia();
            if (!media) { await msg.reply('图片下载失败，请重试。'); return; }
            reply = await handleFinanceImage(media.data);

            // 把图片交互写入对话上下文，让后续文字对话能接续
            chatContext.push({ role: 'user', content: '[用户发送了一张截图]' });
            chatContext.push({ role: 'assistant', content: reply });
            if (chatContext.length > 20) chatContext.splice(0, chatContext.length - 20);

            // 记录到历史
            allRecords.push({ role: 'user', text: '[图片]', time: new Date().toISOString().slice(0, 16).replace('T', ' ') });
            allRecords.push({ role: 'assistant', text: reply, time: new Date().toISOString().slice(0, 16).replace('T', ' ') });
            saveJSON(HISTORY_FILE, allRecords);
        } catch (err) {
            console.error('图片处理错误:', err.message);
            reply = '图片识别失败，请重试。';
        }
        if (reply) {
            try {
                const sent = await msg.reply(reply);
                if (sent) botMessageIds.add(sent.id._serialized);
            } catch (err) {
                console.error('发送回复失败（连接可能已断开）:', err.message);
            }
        }
        }); // end enqueueImage
        return;
    } else {
        // 处理文字
        const userText = msg.body.trim();
        if (!userText) return;
        const now = new Date().toISOString();

        // 手动录入消费指令：/消费 金额 备注
        if (userText.startsWith('/消费')) {
            const parts = userText.replace('/消费', '').trim().split(/\s+/);
            const amount = parseFloat(parts[0]);
            const name = parts.slice(1).join(' ') || '手动录入';
            if (!isNaN(amount) && amount > 0) {
                const item = { name, amount, date: now };
                finance.expenses.push(item);
                if (finance.balance) {
                    finance.balance.amount = parseFloat((finance.balance.amount - amount).toFixed(2));
                }
                saveJSON(FINANCE_FILE, finance);
                reply = `✅ 已手动录入消费：${name} ¥${amount}` +
                    (finance.balance ? `\n💰 当前余额：¥${finance.balance.amount.toLocaleString()}` : '');
            } else {
                reply = '格式错误，请使用：/消费 金额 备注\n例：/消费 38 iCloud订阅';
            }

        // 任务管理
        } else if (userText === '任务') {
            try {
                const resp = await fetch(SYNC_URL);
                const data = await resp.json();
                const tasks = data.tasks || [];
                if (tasks.length === 0) {
                    reply = '📋 今日暂无任务';
                } else {
                    const lines = tasks.map((t, i) => {
                        const status = t.done ? '✅' : '⬜';
                        const note = t.note ? ` (备注: ${t.note})` : '';
                        return `${status} ${i+1}. ${t.text}${note}`;
                    });
                    reply = '📋 今日任务\n' + lines.join('\n') + '\n\n完成 N / 备注 N 内容 / 删任务 N';
                }
            } catch (e) {
                reply = '❌ 获取任务失败';
            }

        } else if (/^完成\s*\d+$/.test(userText)) {
            const idx = parseInt(userText.match(/\d+/)[0]) - 1;
            try {
                const resp = await fetch(SYNC_URL);
                const data = await resp.json();
                const tasks = data.tasks || [];
                if (idx < 0 || idx >= tasks.length) {
                    reply = `❌ 没有第 ${idx+1} 条任务`;
                } else {
                    tasks[idx].done = !tasks[idx].done;
                    data.tasks = tasks;
                    data.tasks_date = new Date().toDateString();
                    await fetch(SYNC_URL, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
                    reply = tasks[idx].done
                        ? `✅ 已完成：${tasks[idx].text}`
                        : `⬜ 已撤销完成：${tasks[idx].text}`;
                }
            } catch (e) {
                reply = '❌ 操作失败，请重试';
            }

        } else if (/^备注\s*\d+\s+/.test(userText)) {
            const m = userText.match(/^备注\s*(\d+)\s+(.+)$/);
            if (!m) {
                reply = '请用格式：备注 1 备注内容';
            } else {
                const idx = parseInt(m[1]) - 1;
                const note = m[2].trim();
                try {
                    const resp = await fetch(SYNC_URL);
                    const data = await resp.json();
                    const tasks = data.tasks || [];
                    if (idx < 0 || idx >= tasks.length) {
                        reply = `❌ 没有第 ${idx+1} 条任务`;
                    } else {
                        tasks[idx].note = note;
                        data.tasks = tasks;
                        data.tasks_date = new Date().toDateString();
                        await fetch(SYNC_URL, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
                        reply = `📝 已添加备注：${tasks[idx].text}\n备注：${note}`;
                    }
                } catch (e) {
                    reply = '❌ 操作失败，请重试';
                }
            }

        } else if (/^删任务\s*\d+$/.test(userText)) {
            const idx = parseInt(userText.match(/\d+/)[0]) - 1;
            try {
                const resp = await fetch(SYNC_URL);
                const data = await resp.json();
                const tasks = data.tasks || [];
                if (idx < 0 || idx >= tasks.length) {
                    reply = `❌ 没有第 ${idx+1} 条任务`;
                } else {
                    const removed = tasks.splice(idx, 1)[0];
                    data.tasks = tasks;
                    data.tasks_date = new Date().toDateString();
                    await fetch(SYNC_URL, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
                    reply = `🗑 已删除：${removed.text}`;
                }
            } catch (e) {
                reply = '❌ 操作失败，请重试';
            }

        // 查看本月支出报告：/报告
        } else if (userText === '/报告') {
            const ym = getYearMonth(new Date());
            const summary = await generateMonthlySummary(ym);
            reply = summary || '本月暂无消费记录。';

        } else if (userText === '日程') {
            try {
                const resp = await fetch(SYNC_URL);
                const data = await resp.json();
                const todayMs = Date.now();
                const events = (data.calendar_events || [])
                    .filter(ev => {
                        const evMs = new Date(ev.date + 'T00:00:00').getTime();
                        const diffDays = (evMs - todayMs) / 86400000;
                        return diffDays > -1 && diffDays < 7;
                    })
                    .sort((a, b) => (a.date + a.time).localeCompare(b.date + b.time));
                if (events.length === 0) {
                    reply = '📅 未来7天暂无日程';
                } else {
                    const lines = events.map(ev => {
                        const [, m, d] = ev.date.split('-');
                        return `  ${parseInt(m)}/${parseInt(d)} ${ev.time} ${ev.title}`;
                    });
                    reply = '📅 未来7天日程\n' + lines.join('\n');
                }
            } catch (e) {
                reply = '❌ 获取日程失败';
            }

        } else if (userText.startsWith('提醒')) {
            const parts = userText.slice(2).trim().split(/\s+/);
            if (parts.length < 3) {
                reply = '请用格式：提醒 6/15 09:00 事件内容';
            } else {
                const date = parseCalendarDate(parts[0]);
                const timeMatch = parts[1].match(/^(\d{1,2})[:\.](\d{2})$/) || parts[1].match(/^(\d{1,2})点(\d{0,2})$/);
                const title = parts.slice(2).join(' ');
                if (!date || !timeMatch) {
                    reply = '日期或时间格式不对，请用：提醒 6/15 09:00 事件内容';
                } else {
                    const hh = timeMatch[1].padStart(2,'0');
                    const mm = (timeMatch[2] || '00').padStart(2,'0');
                    const time = `${hh}:${mm}`;
                    try {
                        const resp = await fetch(SYNC_URL);
                        const data = await resp.json();
                        const events = data.calendar_events || [];
                        events.push({ id: Date.now().toString(36), date, time, title });
                        data.calendar_events = events;
                        await fetch(SYNC_URL, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(data)
                        });
                        const [, m, d] = date.split('-');
                        reply = `✅ 已添加日程：${parseInt(m)}月${parseInt(d)}日 ${time} ${title}`;
                    } catch (e) {
                        reply = '❌ 添加日程失败，请重试';
                    }
                }
            }

        } else {
        allRecords.push({ role: 'user', text: userText, time: new Date().toISOString().slice(0, 16).replace('T', ' ') });
        saveJSON(HISTORY_FILE, allRecords);

        chatContext.push({ role: 'user', content: userText });
        if (chatContext.length > 20) chatContext.splice(0, chatContext.length - 20);

        try {
            const balanceInfo = finance.balance
                ? `当前账户余额：¥${finance.balance.amount}（最后更新：${finance.balance.date.slice(0,16).replace('T',' ')}）`
                : '账户余额：尚未记录';
            const todayExpenses = finance.expenses.filter(e => e.date.startsWith(new Date().toISOString().slice(0, 10)));
            const todayTotal = todayExpenses.reduce((s, e) => s + e.amount, 0);
            const expenseInfo = todayExpenses.length > 0
                ? `今日已消费：¥${todayTotal.toFixed(2)}，共${todayExpenses.length}笔`
                : '今日暂无消费记录';
            reply = await askOllama(chatContext,
                `你是一个智能助手兼个人财务助手。财务状态：${balanceInfo}；${expenseInfo}。回复简洁，适合手机阅读。`
            );
            chatContext.push({ role: 'assistant', content: reply });
            allRecords.push({ role: 'assistant', text: reply, time: new Date().toISOString().slice(0, 16).replace('T', ' ') });
            saveJSON(HISTORY_FILE, allRecords);
        } catch (err) {
            console.error('Ollama 错误:', err.message);
            reply = '抱歉，出现了错误，请稍后再试。';
        }
        } // end else (normal chat)
    }

    try {
        const sent = await msg.reply(reply);
        if (sent) botMessageIds.add(sent.id._serialized);
    } catch (err) {
        console.error('发送回复失败（连接可能已断开）:', err.message);
    }
}

async function startWithRetry(c) {
    try {
        await c.initialize();
    } catch (e) {
        console.error('初始化失败，30秒后重试：', e.message);
        setTimeout(() => {
            client = createClient();
            initClient(client);
            startWithRetry(client);
        }, 30000);
    }
}

process.on('uncaughtException', (e) => {
    console.error('未捕获异常，30秒后重启：', e.message);
    setTimeout(() => {
        client = createClient();
        initClient(client);
        startWithRetry(client);
    }, 30000);
});

initClient(client);
startWithRetry(client);
