---
type: claim
status: proposed
created: 2026-11-03
verified: pass
description: outcome-based reward, exact match EM reward, no format reward, no neural reward model, rule-based, Search-R1
---
# Search-R1 trains with a rule-based outcome reward equal to exact match of the final answer, without format rewards or a neural reward model.

## Relations
- derived_from::[[sources/Search-R1 Training LLMs to Reason and Leverage Search]]
  > we adopt a rule-based reward system that consists solely of
  > final outcome rewards
  > Unlike Guo et al. (2025), we do not incorporate format rewards
  > we avoid training neural reward
  > models
  - section 3.4
- relates_to::[[claims/research-reward-is-answer-f1-with-a-0-1-floor-for-correct-format]]
  - ReSearch instead uses F1 plus a format floor
