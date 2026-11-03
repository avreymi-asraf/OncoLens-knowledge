---
type: claim
status: proposed
verified: pass
created: 2026-11-03
description: eval_then_score.sh, decoupled solve score, cross-version inspect_ai, frozen scorer project solvers/scorer, --no-score
---
# For solvers that cannot share astabench's inspect_ai version, AstaBench offers a decoupled flow that solves with --no-score and then scores in a separately pinned scorer project.

## Relations
- derived_from::[[sources/github-allenai-asta-bench-·-github-20261103165041]]
  > For solver environments that cannot share the same `inspect_ai` version as `astabench`, use:
- relates_to::[[concepts/astabench]]
  - cross-version workflow
- derived_from::[[sources/github-allenai-asta-bench-·-github-20261103165041]]
  > The scorer project is pinned independently in [solvers/scorer/pyproject.toml](https://github.com/allenai/asta-bench/blob/main/solvers/scorer/pyproject.toml).
- relates_to::[[claims/astabench-0-5-2-pins-inspect-ai-0-3-114]]
  - alternative to uv override-dependencies for diverging inspect_ai versions
