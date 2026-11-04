---
type: claim
status: proposed
created: 2026-11-04
verified: pass
description: hypothesis why LLMs fail to abstain, training rewards answering as helpful, hallucination instead of refusal, missing information, negation
---
# The LongHealth authors hypothesize that LLMs fail to flag missing information because training treats giving an answer as more helpful than abstaining.

Stated as a hypothesis in the discussion, not tested.

## Relations
- derived_from::[[sources/LongHealth - A Question Answering Benchmark with Long Clinical Documents]]
  > One hypothesis is that, during LLM training,
  - Section 4
- derived_from::[[sources/LongHealth - A Question Answering Benchmark with Long Clinical Documents]]
  > providing an answer is inherently perceived as more helpful than refraining from
- relates_to::[[claims/identifying-missing-information-is-the-hardest-longhealth-task-for-all-models]]
  - proposed explanation for that result
- relates_to::[[claims/f1-reward-training-collapses-through-answer-avoidance-and-underperforms-em]]
  - the reward design for answering vs abstaining shapes whether a model answers; there it pushes toward avoidance
