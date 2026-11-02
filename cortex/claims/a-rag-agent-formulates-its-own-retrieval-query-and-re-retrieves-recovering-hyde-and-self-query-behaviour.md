---
type: claim
status: proposed
created: 2026-11-02
verified: pass
description: RAG agent with retriever tool, query reformulation, HyDE, Self-Query, re-retrieval, smolagents ToolCallingAgent
---
# An agent armed with a retriever tool formulates its own retrieval query and critiques results to re-retrieve, naively recovering advanced RAG techniques like HyDE and Self-Query.

## Relations
- derived_from::[[sources/agentic-rag-turbocharge-your-rag-with-query-reformulation-and-self-query]]
  > This agent will: ✅ Formulate the query itself and ✅ Critique to re-retrieve if needed.
- derived_from::[[sources/agentic-rag-turbocharge-your-rag-with-query-reformulation-and-self-query]]
  > the agent formulates itself a reference sentence that can be closer to the targeted documents, as in [HyDE]
- relates_to::[[claims/the-model-deciding-whether-to-call-the-retriever-makes-rag-agentic-rather-than-a-fixed-pipeline]]
  - both define agentic RAG as giving the model control over the retriever tool
- relates_to::[[concepts/agentic-rag-retrieve-grade-rewrite-loop]]
  - same retrieve-critique-rewrite pattern, here implicit in a ReAct agent rather than an explicit graph
