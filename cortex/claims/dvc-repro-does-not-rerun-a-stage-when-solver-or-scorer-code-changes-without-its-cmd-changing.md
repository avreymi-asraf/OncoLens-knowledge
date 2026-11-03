---
type: claim
status: proposed
created: 2026-11-03
verified: pass
description: dvc repro caching, stale eval results, force rerun, score_sqa --force --downstream, dvc.lock hash, SQA release runs
---
# In the agent-baselines SQA dvc pipeline, a code change to a solver or scorer that leaves the stage cmd unchanged does not trigger a rerun, so the stage must be forced (e.g. with --force --downstream).

dvc reruns a stage only when a dependency hash or the stage definition changes.

## Relations
- derived_from::[[sources/github-allenai-agent-baselines-·-github-20261103165019]]
  > Sometimes we need to manually force a stage to run since the code for a stage can change (for example a bugfix or improvement to a solver or scorer) without the `cmd` for that stage changing.
- derived_from::[[sources/github-allenai-agent-baselines-·-github-20261103165019]]
  > Any of the `dependencies` changed. (This is determined by comparing the hash with the hash stored in `dvc.lock`)
