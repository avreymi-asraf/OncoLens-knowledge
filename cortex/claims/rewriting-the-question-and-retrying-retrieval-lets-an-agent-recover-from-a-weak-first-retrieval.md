---
type: claim
status: proposed
created: 2026-11-02
verified: pass
description: query rewriting, retry loop, retrieval failure recovery, hallucination avoidance, agentic RAG
---
# A rewrite-and-retry loop that returns control to the query-generation node lets a RAG agent recover from a weak first retrieval instead of stopping or hallucinating an answer.

## Relations
- derived_from::[[sources/build-a-custom-rag-agent-with-langgraph-docs-by-langchain]]
  > This retry loop is how the agent recovers from a weak first retrieval instead of stopping or hallucinating an answer.
