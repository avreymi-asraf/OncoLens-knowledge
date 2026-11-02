---
type: claim
status: proposed
created: 2026-11-02
verified: partial
description: document grading, relevance grader, conditional edge, binary score, corrective RAG, rewrite_question
---
# In the LangGraph agentic RAG design, an LLM grader gives a binary relevance score to retrieved documents and conditionally routes to answer generation if relevant or to question rewriting if not.

## Relations
- derived_from::[[sources/build-a-custom-rag-agent-with-langgraph-docs-by-langchain]]
  > After retrieval, use that pattern to grade whether the documents are relevant: continue to answer generation if they are, or rewrite the question and try again if they are not.
