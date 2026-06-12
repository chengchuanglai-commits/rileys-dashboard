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
const WORKFLOW = "trading-signals.yml";

async function dispatch(env) {
  const res = await fetch(
    `https://api.github.com/repos/${REPO}/actions/workflows/${WORKFLOW}/dispatches`,
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
  console.log(ok ? `dispatched ${WORKFLOW} @ ${new Date().toISOString()}` : `dispatch FAILED: ${detail}`);
  return { ok, detail };
}

export default {
  // 定时触发：Cloudflare 在 cron 时刻调用
  async scheduled(event, env, ctx) {
    ctx.waitUntil(dispatch(env));
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
      const r = await dispatch(env);
      return new Response(r.ok ? "✅ dispatched trading-signals" : `❌ failed: ${r.detail}`,
        { status: r.ok ? 200 : 502 });
    }
    return new Response("rileys-signal-cron alive · cron 30 11 * * 1-5 UTC · ?check=<TOKEN> 只读诊断 · ?token=<TOKEN> 手动触发", { status: 200 });
  },
};
