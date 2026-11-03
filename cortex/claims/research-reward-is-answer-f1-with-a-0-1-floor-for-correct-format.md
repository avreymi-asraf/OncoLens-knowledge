---
type: claim
status: proposed
created: 2026-11-03
verified: pass
description: ReSearch reward function, F1 answer reward, format reward 0.1, rule-based reward, boxed answer, reward shaping
---
# ReSearch uses a rule-based reward equal to the answer F1 score, with 0.1 for a zero-F1 rollout in correct format and 0 otherwise.

Note: the format floor rewards producing a well-formed boxed answer, which is comparable in spirit to the action-level penalties reported elsewhere for preventing F1 answer-avoidance collapse; ReSearch itself does not test this.

## Relations
- derived_from::[[sources/ReSearch Learning to Reason with Search for LLMs]]
  > only rule-based reward
  > function is enough to successfully elicit capabilities of reasoning with search for LLMs.
- derived_from::[[sources/ReSearch Learning to Reason with Search for LLMs]]
  > 0.1,if f1 score is 0 and format is correct
- relates_to::[[claims/f1-reward-training-collapses-through-answer-avoidance-and-underperforms-em]]
  - ReSearch trains on F1 without reporting collapse; its format floor makes withholding an answer score below a formatted wrong answer
- relates_to::[[claims/action-level-penalties-for-missing-search-or-answer-stabilize-f1-training-and-surpass-em]]
  - similar shaping: a well-formed answer earns more than no answer
