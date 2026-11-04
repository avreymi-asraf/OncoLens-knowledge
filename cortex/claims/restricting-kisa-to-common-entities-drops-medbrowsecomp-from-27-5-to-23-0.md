---
type: claim
status: proposed
created: 2026-11-04
verified: pass
description: KISA data ablation, rare entities vs common entities knowledge graph, MedBrowseComp 27.5 to 23.0, training data complexity for multi-hop reasoning
---
# Building KISA training questions from common instead of rare entities lowers MedBrowseComp accuracy from 27.5 to 23.0.

## Relations
- derived_from::[[sources/MedResearcher-R1]]
  > Restricting the knowledge graph to common entities results in a significant
  > performance degradation, with scores on MedBrowseComp falling from 27.5 to 23.0.
  - section 7
- relates_to::[[concepts/knowledge-informed-trajectory-synthesis]]
  - ablation of the rare-entity stage
