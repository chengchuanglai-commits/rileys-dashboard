// Cloudflare Worker —— 每个工作日 11:30 UTC 准点派发 GitHub trading-signals 工作流。
// 背景：GitHub Actions 的 schedule 触发器历史上延迟 3 小时甚至丢运行（见 6/9、6/10），
//       盘前出信号这种对时间敏感的任务不能靠它。Cloudflare cron 是秒级准点的。
//
// 部署（你来做，需 2 个东西）：
//   1. GitHub 细粒度 PAT：github.com/settings/personal-access-tokens → 只授权 rileys-dashboard 仓库，
//      权限 Actions = Read and write（这样才能 workflow_dispatch）
//   2. 在 cron-trigger/ 目录：
//        npx wrangler secret put GH_PAT      # 粘贴上面的 PAT
//        npx wrangler deploy
//
// 手动测试（不用等 11:30）：部署后 curl 这个 worker 的 URL 加 ?token=<TRIGGER_TOKEN>。
//   可选：npx wrangler secret put TRIGGER_TOKEN 设一个口令，再 curl "https://<worker>.workers.dev/?token=口令"

const REPO = "chengchuanglai-commits/rileys-dashboard";
const WORKFLOW = "trading-signals.yml";          // 默认(手动触发用)
const DEEPSEEK_WF = "deepseek-broad.yml";
const MULTIFACTOR_WF = "multifactor-bq.yml";     // 多因子量化+动量+更新allocation(决策引擎配置,IBKR自检靠它)
// 哪个 cron 派发哪个工作流
const CRON_WF = {
  "30 11 * * 1-5": WORKFLOW,         // 11:30 主信号
  "0 12 * * 1-5":  DEEPSEEK_WF,      // 12:00 DeepSeek 广撒
  "30 12 * * 1-5": MULTIFACTOR_WF,   // 12:30 多因子量化(更新allocation,绝不能漏→IBKR自检会失败)
};

async function dispatch(env, workflow = WORKFLOW) {
  const res = await fetch(
    `https://api.github.com/repos/${REPO}/actions/workflows/${workflow}/dispatches`,
    {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${env.GH_PAT}`,
        "Accept": "application/vnd.github+json",
        "User-Agent": "rileys-signal-cron",
        "X-GitHub-Api-Version": "2022-11-28",
      },
      body: JSON.stringify({ ref: "main" }),
    },
  );
  const ok = res.ok;
  const detail = ok ? "" : `${res.status} ${await res.text()}`;
  console.log(ok ? `dispatched ${workflow} @ ${new Date().toISOString()}` : `dispatch FAILED ${workflow}: ${detail}`);
  return { ok, detail };
}

export default {
  // 定时触发：按 event.cron 派发对应工作流(11:30→主信号, 12:00→DeepSeek广撒)
  async scheduled(event, env, ctx) {
    const workflow = CRON_WF[event.cron] || WORKFLOW;
    ctx.waitUntil(dispatch(env, workflow));
  },

  // HTTP：健康检查 / 只读PAT诊断 / 带口令的手动测试触发
  async fetch(request, env) {
    const url = new URL(request.url);
    const token = url.searchParams.get("token");
    const check = url.searchParams.get("check");
    // 只读诊断：GET 工作流验证 PAT 是否有效+有权限（不触发运行、不花钱）
    if (env.TRIGGER_TOKEN && check === env.TRIGGER_TOKEN) {
      const res = await fetch(
        `https://api.github.com/repos/${REPO}/actions/workflows/${WORKFLOW}`,
        { headers: {
            "Authorization": `Bearer ${env.GH_PAT}`,
            "Accept": "application/vnd.github+json",
            "User-Agent": "rileys-signal-cron",
            "X-GitHub-Api-Version": "2022-11-28",
        }});
      const body = await res.text();
      return new Response(res.ok
        ? `✅ PAT 有效，能访问工作流 (${res.status})`
        : `❌ PAT 问题: ${res.status} ${body.slice(0,300)}`,
        { status: res.ok ? 200 : 502 });
    }
    if (env.TRIGGER_TOKEN && token === env.TRIGGER_TOKEN) {
      const workflow = url.searchParams.get("wf") === "deepseek" ? DEEPSEEK_WF : WORKFLOW;
      const r = await dispatch(env, workflow);
      return new Response(r.ok ? `✅ dispatched ${workflow}` : `❌ failed: ${r.detail}`,
        { status: r.ok ? 200 : 502 });
    }
    return new Response("rileys-signal-cron alive · crons 30 11(主信号) + 0 12(DeepSeek广撒) * * 1-5 UTC · ?check=<T> 诊断 · ?token=<T>[&wf=deepseek] 手动触发", { status: 200 });
  },
};
