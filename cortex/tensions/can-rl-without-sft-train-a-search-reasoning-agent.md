---
type: tension
status: open
created: 2026-11-04
description: RL from scratch without SFT works for search agents (ReSearch) vs RL only fails without SFT cold start (MedResearcher-R1)
---
# Can reinforcement learning without prior SFT train an effective search-and-reasoning agent?

ReSearch trains search-interleaved reasoning with GRPO and no supervised reasoning data. MedResearcher-R1 finds RL alone scores 12.0/50 vs 25.5/50 for SFT alone on MedBrowseComp.

## Relations
- supports::[[claims/research-trains-llms-to-interleave-search-with-reasoning-via-grpo-without-supervised-reasoning-data]]
  - RL without SFT suffices (multi-hop QA benchmarks)
- contradicts::[[claims/rl-only-training-without-sft-fails-on-medbrowsecomp-while-sft-only-reaches-25-5]]
  - RL alone fails; likely difference: much longer-horizon, sparser-reward medical tasks and harder benchmark
