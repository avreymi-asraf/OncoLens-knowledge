---
type: claim
status: proposed
created: 2026-11-02
verified: pass
description: MIPROv2 jointly optimizing the query-generation and note-appending prompts, GPT-4o teacher, Llama-3.1-8B, top5_recall 31% to 59%, about 35 minutes and 5 dollars.
---
# Jointly optimizing the two prompts of a multi-hop retrieval program with MIPROv2 roughly doubles top-5 recall from about 31% to about 59%.

Optimization used GPT-4o as prompt model and teacher for the 8B Llama student.

## Relations
- derived_from::[[sources/multi-hop-rag-dspy]]
  > It looks like the system improved drastically from around 30% recall to a little below 60% recall.
  - after optimization the dev average was 59.11 (59.1%)
- derived_from::[[sources/multi-hop-rag-dspy]]
  > This may take around 35 minutes and make some $5 worth of calls to GPT-4o to optimize Llama-3.1-8B.
  - cost of the optimization run
