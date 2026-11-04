---
type: claim
status: proposed
created: 2026-11-04
verified: pass
description: SFT data mix D_guided vs D_explore 7:3 ratio, masked guidance vs question-only trajectories, avoid overfitting longest reasoning paths
---
# MedResearcher-R1 SFT data mixes guided (masked-trajectory) and exploratory (question-only) trajectories at a 7:3 ratio to avoid over-reliance on guidance.

## Relations
- derived_from::[[sources/MedResearcher-R1]]
  > We maintain a 7:3 ratio between these subsets.
  > This balances structured learning with exploration.
  - section 4
- derived_from::[[sources/MedResearcher-R1]]
  > This prevents over-reliance on trajectory guidance in case there are easier reasoning ways
  > to reach the answers.
