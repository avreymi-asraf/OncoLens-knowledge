---
type: claim
status: proposed
verified: partial
created: 2026-11-03
description: AstaBench cost logging, accuracy and cost, model usage tracking, record_model_usage_with_inspect, bridge, AsyncOpenAI
---
# AstaBench measures a solver's cost as well as its accuracy, so solvers must ensure all model usage is logged (automatically via InspectAI model calls, or manually with record_model_usage_with_inspect).

## Relations
- derived_from::[[sources/github-allenai-asta-bench-·-github-20261103165041]]
  > A key part of AstaBench's design philosophy is measuring not only the accuracy of a solver, but also the cost of running it. Thus, it is crucial that solvers ensure all model usages are correctly logged.
- relates_to::[[concepts/astabench]]
  - design philosophy: accuracy plus cost
