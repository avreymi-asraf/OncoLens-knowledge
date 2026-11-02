---
type: claim
status: proposed
created: 2026-11-02
verified: pass
description: agentic RAG, retriever as tool, bind_tools, model decides to retrieve or answer directly, LangGraph
---
# Letting the model decide whether to call the retriever tool, instead of always retrieving, is what makes a RAG system agentic rather than a fixed retrieve-then-generate pipeline.

## Relations
- derived_from::[[sources/build-a-custom-rag-agent-with-langgraph-docs-by-langchain]]
  > That choice is what makes the system agentic rather than a fixed retrieve-then-generate pipeline: retrieval runs only when the model requests it.
