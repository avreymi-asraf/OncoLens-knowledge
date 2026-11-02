---
type: claim
status: proposed
created: 2026-11-02
verified: pass
description: DSPy multi-hop retrieval baseline, Hop module, query generation plus note appending, BM25S over Wikipedia 2017 abstracts, HoVer 3-hop, top-5 recall about 31% with Llama-3.1-8B.
---
# An unoptimized two-module multi-hop retrieval program on Llama-3.1-8B reaches only about 31% top-5 recall on 3-hop HoVer claims.

The program loops over hops: generate a query from claim and notes, retrieve with BM25, then append new notes and titles.

## Relations
- derived_from::[[sources/multi-hop-rag-dspy]]
  > 2024/12/25 12:18:04 INFO dspy.evaluate.evaluate: Average Metric: 93.99999999999993 / 300 (31.3%)
  - baseline evaluation of Hop() on the dev set
