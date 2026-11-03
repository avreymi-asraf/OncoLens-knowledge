---
type: claim
status: proposed
verified: pass
created: 2026-11-03
description: AstaBench SUPER, CORE-bench, DiscoveryBench, python_session tool, SandboxJupyter, sandbox files, trajectory tracking, scoring requirements
---
# AstaBench coding and data tasks may require the provided sandbox and stateful python_session tool for accurate scores: SUPER tracks trajectories through it, CORE-bench scores a result file written in the sandbox, and DiscoveryBench reads files from the sandbox.

## Relations
- derived_from::[[sources/github-allenai-asta-bench-·-github-20261103165041]]
  > SUPER requires using either the provided `python_session` tool or the `SandboxJupyter` environment to accurately track and score agent trajectories.
- relates_to::[[concepts/astabench]]
  - task-specific scoring constraints
- derived_from::[[sources/github-allenai-asta-bench-·-github-20261103165041]]
  > CORE-bench requires the agent to write its results as a file in the sandbox for scoring
- derived_from::[[sources/github-allenai-asta-bench-·-github-20261103165041]]
  > DiscoveryBench requires the agent to read files from the sandbox for analysis
