---
type: claim
status: proposed
created: 2026-11-04
verified: partial
description: LongHealth Task 2 multi-patient distractor documents, gpt-3.5 drops to 27%, Mixtral 38%, only Mistral-Small 93% and Llama-4-Scout improve
---
# When documents from other patients are mixed in (LongHealth Task 2), most models lose much accuracy, e.g. gpt-3.5-turbo falls to 27%, while only Mistral-Small-24B (93%) and Llama-4-Scout (82%) improve.

## Relations
- derived_from::[[sources/LongHealth - A Question Answering Benchmark with Long Clinical Documents]]
  > gpt-3.5-turbo-1106 fell to 27%
  - Section 3.2, Table 3
- derived_from::[[sources/LongHealth - A Question Answering Benchmark with Long Clinical Documents]]
  > Only Mistral-Small-24B-Instruct-2501 and
- relates_to::[[concepts/longhealth]]
  - Task 2 of the benchmark
