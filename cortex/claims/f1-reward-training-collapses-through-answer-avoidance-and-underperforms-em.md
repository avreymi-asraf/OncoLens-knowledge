---
type: claim
status: proposed
created: 2026-11-03
verified: pass
description: F1 vs exact match EM reward, answer avoidance, answer rate drop, outcome reward, training collapse, deep research RL
---
# Training a search agent with an F1 outcome reward collapses through answer avoidance and ends below EM-reward training, because withholding an answer earns the same zero reward as a wrong answer.

## Relations
- derived_from::[[sources/How to Train Your Deep Research Agent]]
  > Since missing an answer receives the same zero reward as an incorrect one,
  > the policy tends to collapse into a simpler state of generating no answer
- derived_from::[[sources/How to Train Your Deep Research Agent]]
  > the model trained with the
  > stricter EM reward consistently outperforms the F1-trained model on both EM and F1 validation benchmarks
