# rileys-signal-cron —— 准点触发信号工作流的 Cloudflare Worker

## 为什么有它
GitHub Actions 的 `schedule` 触发器不可靠：历史上延迟 3 小时甚至完全不触发
（6/9 实际 15:31、6/10 实际 16:11、6/11 完全没触发）。盘前出信号这种对时间敏感的任务
不能靠它。Cloudflare 的 cron 是秒级准点的，所以由这个 worker 在**工作日 11:30 UTC**
准点调 GitHub API 派发 `trading-signals.yml`。

## 一次性部署（3 步）

### 第 1 步：建 GitHub PAT（只有你能做）
1. 打开 https://github.com/settings/personal-access-tokens/new （Fine-grained token）
2. **Token name**：`rileys-signal-cron`
3. **Expiration**：建议选 **No expiration**（或最长）——否则 PAT 过期后 cron 会静默失效、又 miss 数据
4. **Resource owner**：选 `chengchuanglai-commits`（仓库所属账号）
5. **Repository access** → **Only select repositories** → 勾 `rileys-dashboard`
6. **Permissions** → **Repository permissions** → 找到 **Actions** → 设为 **Read and write**
   （Metadata 会自动变 Read-only，正常）
7. **Generate token** → 复制（`github_pat_...`，只显示一次）

### 第 2 步：设密钥 + 部署（已登录 Cloudflare，无需 login）
```bash
cd "/Users/apple/claude-whatsapp/cron-trigger"
wrangler secret put GH_PAT      # 粘贴第1步的 github_pat_... 回车
wrangler deploy                 # 部署；输出会显示 URL 和 "schedules: 30 11 * * 1-5"
```

### 第 3 步：立刻测试（可选，不用等 11:30）
```bash
wrangler secret put TRIGGER_TOKEN     # 随便设个口令，如 test123
curl "https://rileys-signal-cron.chengchuang-lai.workers.dev/?token=test123"
# 应返回：✅ dispatched trading-signals
```
然后去 GitHub Actions 看，应出现一个新的 trading-signals run。

## 部署成功后
告诉 Claude，把 `trading-signals.yml` 里的 `schedule:` 删掉（只留 workflow_dispatch），
否则 GitHub schedule（虽然晚）也会触发，导致**双跑双花钱**。

## 维护
- **PAT 过期** = cron 静默失效。用 No expiration，或日历提醒自己续。
- 检测手段：信号没出 → WhatsApp 没有 "📊 交易信号" 消息；3 天一次的 edge 监控 agent 也会显示数据停更。
- 看 cron 日志：`wrangler tail rileys-signal-cron`
- 改触发时间：编辑 `wrangler.jsonc` 的 `crons` 后 `wrangler deploy`。
