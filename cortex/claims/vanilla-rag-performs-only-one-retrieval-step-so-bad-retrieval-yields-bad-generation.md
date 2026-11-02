---
type: claim
status: proposed
created: 2026-11-02
verified: pass
description: vanilla RAG limitation, single retrieval step, retrieval failure propagates to generation, no retry
---
# Vanilla RAG performs only one retrieval step, so when retrieval results are bad the generated answer is bad too.

## Relations
- derived_from::[[sources/agentic-rag-turbocharge-your-rag-with-query-reformulation-and-self-query]]
  > It **performs only one retrieval step**: if the results are bad, the generation in turn will be bad.
- relates_to::[[claims/rewriting-the-question-and-retrying-retrieval-lets-an-agent-recover-from-a-weak-first-retrieval]]
  - the retry loop addresses exactly this single-step failure mode
