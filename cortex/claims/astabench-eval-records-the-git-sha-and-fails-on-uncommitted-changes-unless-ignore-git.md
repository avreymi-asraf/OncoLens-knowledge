---
type: claim
status: proposed
verified: pass
created: 2026-11-03
description: astabench eval reproducibility, git sha in logs, uncommitted changes, --ignore-git, wrapper around inspect eval-set, --split
---
# astabench eval, a wrapper around inspect eval-set, records the git sha in logs and fails on uncommitted changes unless --ignore-git is set.

## Relations
- derived_from::[[sources/github-allenai-asta-bench-·-github-20261103165041]]
  > By default, for reproducibility, the git sha will be recorded in the logs, and the command will fail if there are uncommitted changes.
- relates_to::[[concepts/astabench]]
  - reproducibility
