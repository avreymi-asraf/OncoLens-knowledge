---
type: claim
status: proposed
created: 2026-11-02
verified: partial
description: agentic RAG vs standard RAG evaluation, LLM judge, 86.9% vs 73.1%, no-knowledge-base baseline 36%, huggingface_doc_qa_eval
---
# On an LLM-judged QA set over Hugging Face documentation, agentic RAG scored 86.9% versus 73.1% for standard RAG, and an LLM without the knowledge base scored 36%.

Caveat (from the code): the agent used Llama-3.1-70B-Instruct while the standard RAG reader used Qwen2.5-72B-Instruct, so the comparison also changes the reader model; single run, author's own result.

## Relations
- derived_from::[[sources/agentic-rag-turbocharge-your-rag-with-query-reformulation-and-self-query]]
  > Average score for agentic RAG: 86.9%
- derived_from::[[sources/agentic-rag-turbocharge-your-rag-with-query-reformulation-and-self-query]]
  > (For a baseline, using Llama-3-70B without the knowledge base got 36%)
- derived_from::[[sources/agentic-rag-turbocharge-your-rag-with-query-reformulation-and-self-query]]
  > reader_llm = InferenceClient("Qwen/Qwen2.5-72B-Instruct")
- supports::[[claims/a-rag-agent-formulates-its-own-retrieval-query-and-re-retrieves-recovering-hyde-and-self-query-behaviour]]
  - reported gain of the agent setup over single-step RAG
