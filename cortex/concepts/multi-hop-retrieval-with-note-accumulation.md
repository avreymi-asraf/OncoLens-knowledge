---
type: concept
status: active
created: 2026-11-02
description: Multi-hop retrieval loop, iterative query generation, retrieve, append notes and titles; DSPy Hop module, HoVer fact-checking, top-5 recall.
---
# Multi-hop retrieval with note accumulation

A loop that for a fixed number of hops generates a search query from the claim and running notes, retrieves documents, and has an LM add new notes and relevant page titles; the final output is the deduplicated title set.

## Relations
- derived_from::[[sources/multi-hop-rag-dspy]]
  > It will do this via two sub-modules: `generate_query` and `append_notes`.
