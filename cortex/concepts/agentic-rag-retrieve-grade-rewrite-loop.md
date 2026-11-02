---
type: concept
status: active
created: 2026-11-02
description: Agentic RAG graph, LangGraph, generate_query_or_respond, retriever tool, grade documents, rewrite question, generate answer; self-correcting retrieval loop
---
# Agentic RAG retrieve-grade-rewrite loop

A graph of nodes where the model first decides to answer or call a retriever tool, retrieved documents are graded for relevance, and irrelevant results trigger a question rewrite and another attempt; relevant ones go to answer generation. Contrast with [[concepts/multi-hop-retrieval-with-note-accumulation]], which loops to gather further evidence rather than to repair a failed retrieval.

## Relations
- derived_from::[[sources/build-a-custom-rag-agent-with-langgraph-docs-by-langchain]]
  > If `generate_query_or_respond` returned `tool_calls`, call `retriever_tool` to retrieve context.
- relates_to::[[concepts/multi-hop-retrieval-with-note-accumulation]]
  - both are iterative retrieval loops with an LM-generated query at each pass
