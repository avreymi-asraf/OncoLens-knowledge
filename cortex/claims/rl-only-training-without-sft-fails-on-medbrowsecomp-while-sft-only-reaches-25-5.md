---
type: claim
status: proposed
created: 2026-11-04
verified: pass
description: SFT vs RL ablation, RL only no SFT 12.0/50 vs SFT only 25.5/50 on MedBrowseComp; sparse reward long-horizon medical reasoning; cold start
---
# In MedResearcher-R1 ablations, RL alone without SFT scores 12.0/50 on MedBrowseComp while SFT alone reaches 25.5/50, attributed to sparse rewards in long-horizon medical reasoning.

## Relations
- derived_from::[[sources/MedResearcher-R1]]
  > SFT alone achieves 25.5/50 on
  > MedBrowseComp while RL alone fails (12.0/50). The relative failure of RL can be attributed to the sparse reward
  > signals inherent in long-horizon medical reasoning.
  - section 7, Table 3
- relates_to::[[claims/research-trains-llms-to-interleave-search-with-reasoning-via-grpo-without-supervised-reasoning-data]]
  - ReSearch reports RL without SFT works on multi-hop QA; see tension
