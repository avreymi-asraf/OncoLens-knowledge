---
type: claim
status: proposed
created: 2026-11-03
verified: pass
description: ReSearch framework, reasoning with search, GRPO, no SFT, think/search/result tags, multi-hop RAG, Qwen2.5
---
# ReSearch trains LLMs with GRPO to interleave text-based thinking and search queries in one reasoning chain, without any supervised data on reasoning steps.

## Relations
- derived_from::[[sources/ReSearch Learning to Reason with Search for LLMs]]
  > we don’t provide any supervised data on reasoning steps for
  > LLMs to imitate, instead, we leverage reinforcement learning (i.e., GRPO) to incentivize LLMs to
  > perform reasoning with search.
- relates_to::[[claims/vanilla-rag-performs-only-one-retrieval-step-so-bad-retrieval-yields-bad-generation]]
  - ReSearch targets the multi-step retrieval that single-step RAG lacks
