---
type: claim
status: proposed
verified: pass
created: 2026-11-03
description: AstaBench parallelism, --max-samples, CPU cores, asyncio.to_thread ThreadPool deadlock, INSPECT_DOCKER_CLI_CONCURRENCY 2N, ASTA_TOOL_KEY rate limit 8 samples
---
# AstaBench advises --max-samples no greater than CPU cores (about 8 for literature tasks, saturating the ~4 req/s Asta tool rate limit) and INSPECT_DOCKER_CLI_CONCURRENCY of at least twice that, to avoid deadlocks.

## Relations
- derived_from::[[sources/github-allenai-asta-bench-·-github-20261103165041]]
  > this is why we suggest setting `--max-samples` no greater than the number of CPU cores.
- relates_to::[[concepts/astabench]]
  - operational guidance
- derived_from::[[sources/github-allenai-asta-bench-·-github-20261103165041]]
  > For literature tasks with fast LLMs, it should be no greater than roughly `--max-samples=8`, which is empirically what we found to saturate the default `ASTA_TOOL_KEY` rate limit of roughly 4 requests per second for MCP tools.
- relates_to::[[concepts/code-action-agent]]
  - SandboxToolManager code agents need INSPECT_DOCKER_CLI_CONCURRENCY of at least N+1, ideally 2N
