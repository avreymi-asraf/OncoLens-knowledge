---
type: claim
status: proposed
created: 2026-11-03
verified: partial
description: ReSearch results, multi-hop QA, HotpotQA 2Wiki MuSiQue Bamboogle, exact match, LLM-as-judge, IRCoT, Iter-RetGen baselines
---
# ReSearch improves over the best prompt-based multi-step RAG baseline by an average of 15.81% EM and 17.56% LLM-as-judge at 7B, and 14.82% EM and 15.46% LLM-as-judge at 32B.

Baselines: Naive Generation, Naive RAG, Iter-RetGen, IRCoT on the same-size instruct models; authors' own evaluation.

## Relations
- derived_from::[[sources/ReSearch Learning to Reason with Search for LLMs]]
  > the average improvement ofReSearchover the best baseline
  > is15.81%in exact match and17.56%in LLM-as-a-judge, for Qwen2.5 model with 7B parameters.
  > For Qwen2.5 model with 32B parameters, the average improvement is14.82%in exact match and
  > 15.46%in LLM-as-a-judge.
