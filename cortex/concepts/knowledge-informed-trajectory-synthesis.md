---
type: concept
status: active
created: 2026-11-04
description: KISA, knowledge-informed trajectory synthesis, knowledge graph multi-hop QA generation from rare PubMed entities, longest path, masked trajectory guidance, agent SFT data
---
# Knowledge-Informed Trajectory Synthesis (KISA)

A data synthesis pipeline for training deep-research agents: extract rare entities from PubMed, build a local knowledge graph per entity via search, take its longest path, enrich with neighbor nodes, and generate multi-hop questions plus tool-using reasoning trajectories via masked trajectory guidance.

## Relations
- derived_from::[[sources/MedResearcher-R1]]
  > KISA consists of five stages (Figure 2):
  > (i) rare entity extraction and selection (ii) knowledge graph construction via search engine (iii) longest path extraction
  > (iv) path enrichment with adjacent nodes and (v) reasoning trajectory generation with masked trajectory guidance.
