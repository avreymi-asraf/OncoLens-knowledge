---
type: concept
status: active
created: 2026-11-03
description: code agent, CodeAgent, code actions, agent writes Python instead of JSON tool calls, smolagents, sandboxed execution
---
# Code-action agent

An agent that expresses its actions as executable Python code rather than JSON tool-call objects; because it runs generated code it needs a sandbox, from which tools are exposed (in agent-baselines via `SandboxToolManager`).

## Relations
- derived_from::[[sources/github-allenai-agent-baselines-·-github-20261103165019]]
  > which takes actions by writing Python code rather than using JSON tool-calling. Requires a sandbox and uses `SandboxToolManager` to access tools from sandboxed code.
- relates_to::[[claims/a-rag-agent-formulates-its-own-retrieval-query-and-re-retrieves-recovering-hyde-and-self-query-behaviour]]
  - both use smolagents; that claim uses the JSON ToolCallingAgent, this concept is the CodeAgent alternative
