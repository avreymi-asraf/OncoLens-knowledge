---
type: claim
status: proposed
created: 2026-11-03
verified: pass
description: response length dynamics, decrease-increase-stabilize, valid search calls grow, training dynamics, Search-R1 Qwen2.5-7B base
---
# During Search-R1 training on Qwen2.5-7B base, response length first drops sharply for about 100 steps and then rises as the model learns to call search more often.

## Relations
- derived_from::[[sources/Search-R1 Training LLMs to Reason and Leverage Search]]
  > (1) Early Stage (First 100 Steps): The response length sharply decreases, while
  > the training reward exhibits a slight increase.
  > (2) Later Stage
  > (After 100 Steps): Both response length and training reward increase significantly. At this
  > point, the LLM learns to call the search engine frequently
  - section 5.3
