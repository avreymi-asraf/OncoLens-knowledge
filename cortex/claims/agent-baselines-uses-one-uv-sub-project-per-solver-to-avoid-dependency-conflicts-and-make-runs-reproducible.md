---
type: claim
status: proposed
created: 2026-11-03
verified: pass
description: per-solver uv sub-projects, lockfiles, dependency isolation, inspect_ai version conflicts, reproducibility, agent-baselines
---
# The agent-baselines repo gives each solver its own uv sub-project and lockfile to avoid cross-solver dependency conflicts (notably inspect_ai versions) and to make runs reproducible per solver.

## Relations
- derived_from::[[sources/github-allenai-agent-baselines-·-github-20261103165019]]
  > This repo uses **one uv sub-project per solver**
- derived_from::[[sources/github-allenai-agent-baselines-·-github-20261103165019]]
  > Avoid dependency conflicts across solvers (especially different `inspect_ai` needs).
- derived_from::[[sources/github-allenai-agent-baselines-·-github-20261103165019]]
  > Make runs reproducible per solver via lockfiles.
- relates_to::[[concepts/agent-baselines-astabench-solvers]]
  - repo structure
