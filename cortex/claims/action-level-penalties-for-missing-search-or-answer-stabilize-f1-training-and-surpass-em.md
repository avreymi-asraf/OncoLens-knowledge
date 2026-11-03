---
type: claim
status: proposed
created: 2026-11-03
verified: pass
description: F1+ reward, action-level penalty, no search penalty, no answer penalty, reward shaping, stability, deep research agent
---
# Adding small penalties for omitting the search or answer action to the F1 reward removes the answer-refusal collapse and lets F1-based training surpass the EM baseline.

## Relations
- derived_from::[[sources/How to Train Your Deep Research Agent]]
  > the F1-based
  > model with action penalties not only recovers from instability, but also surpasses the EM baseline in final
  > performance
- relates_to::[[claims/tool-use-vanishes-during-rl-without-suitable-reward-design]]
  - both report that action omission (tool use or answering) emerges under outcome-only rewards and is countered by reward design
