---
type: claim
status: proposed
created: 2026-11-04
verified: pass
description: Masked Trajectory Guidance MTG, entity masking Entity A placeholders, avoid answer leakage, o3 with tools generates SFT trajectories with tool calls
---
# Masked Trajectory Guidance replaces knowledge-graph path entities with placeholders like "Entity A" in the guidance given to o3, so that tool-retrievable information is not leaked into the generated SFT trajectories.

## Relations
- derived_from::[[sources/MedResearcher-R1]]
  > we must not leak information that requires retrieval from tool
  > invocations.
  - section 4
- derived_from::[[sources/MedResearcher-R1]]
  > It replaces them
  > with placeholders, such as "Entity A".
- relates_to::[[concepts/knowledge-informed-trajectory-synthesis]]
  - final stage of KISA
