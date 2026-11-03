---
type: claim
status: proposed
created: 2026-11-03
verified: pass
description: retrieved token loss masking ablation, observation masking, Search-R1, PPO, Qwen2.5-7B base, EM 0.431 vs 0.343
---
# In Search-R1 with PPO on Qwen2.5-7B base, masking retrieved tokens from the loss raises average EM over seven QA datasets from 0.343 to 0.431.

## Relations
- derived_from::[[sources/Search-R1 Training LLMs to Reason and Leverage Search]]
  > SEARCH -R1 w. mask 0.480 0.638 0.457 0.433 0.382 0.196 0.432 0.431
  > SEARCH -R1 w.o. mask 0.388 0.567 0.391 0.325 0.321 0.108 0.304 0.343
  - Table 4, section 5.4
- supports::[[claims/tool-observation-tokens-are-off-policy-and-masked-from-the-grpo-loss]]
  - independent source with an ablation showing masking environment tokens helps
- relates_to::[[claims/research-masks-retrieval-result-tokens-from-the-grpo-loss]]
  - ReSearch uses the same masking without reporting an ablation
