---
type: claim
status: proposed
created: 2026-11-04
verified: pass
description: medical RAG limitation, static heuristic one-shot retrieval, no adaptive re-query, irrelevant or conflicting evidence
---
# Existing medical RAG systems typically perform static one-shot retrieval on the initial query and fail to adapt when retrieved evidence is insufficient, irrelevant or conflicting.

## Relations
- derived_from::[[sources/End-to-End Agentic RAG System Training for Traceable Diagnostic Reasoning]]
  > They typically perform a “one-shot”
  > failing to adapt when the retrieved evidence is insufficient, irrelevant,
- relates_to::[[claims/vanilla-rag-performs-only-one-retrieval-step-so-bad-retrieval-yields-bad-generation]]
  - same one-shot retrieval limitation, stated for the medical domain
