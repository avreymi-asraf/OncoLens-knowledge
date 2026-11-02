---
type: claim
status: proposed
created: 2026-11-02
verified: pass
description: retriever tool description, affirmative-form queries not questions, multiple diverse queries, prompt engineering for agentic RAG
---
# The Hugging Face agentic RAG cookbook instructs the agent to write retrieval queries as affirmative sentences rather than questions and to call the retriever several times with semantically different queries.

## Relations
- derived_from::[[sources/agentic-rag-turbocharge-your-rag-with-query-reformulation-and-self-query]]
  > Use the affirmative form rather than a question.
- derived_from::[[sources/agentic-rag-turbocharge-your-rag-with-query-reformulation-and-self-query]]
  > Make sure to have covered the question completely by calling the retriever tool several times with semantically different queries.
- supports::[[claims/using-the-user-question-as-the-similarity-reference-can-miss-answer-documents-written-in-affirmative-form]]
  - the prompt is the practical response to the question-vs-affirmative mismatch
