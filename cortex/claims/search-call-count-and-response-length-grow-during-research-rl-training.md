---
type: claim
status: proposed
created: 2026-11-03
verified: pass
description: number of search operations, response length, training dynamics, tool call growth, ReSearch, multi-hop
---
# During ReSearch RL training, the average number of search operations per rollout grows consistently and response length generally increases.

## Relations
- derived_from::[[sources/ReSearch Learning to Reason with Search for LLMs]]
  > the number of search operations shows consistent growth throughout the training process.
- derived_from::[[sources/ReSearch Learning to Reason with Search for LLMs]]
  > it is evident that the response length generally increases throughout the
  > training process.
- supports::[[claims/tool-call-frequency-during-rl-falls-for-memorizable-tool-outputs-and-rises-for-unmemorizable-ones]]
  - search results on multi-hop QA are not memorizable, and search calls rise
