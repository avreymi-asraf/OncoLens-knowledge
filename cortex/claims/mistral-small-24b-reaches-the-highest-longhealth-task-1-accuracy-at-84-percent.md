---
type: claim
status: disputed
created: 2026-11-04
verified: fail
description: LongHealth Task 1 single-patient shuffled documents, Mistral-Small-24B-Instruct 84%, Llama-4-Scout 81%, Mixtral 76%, 16k tokens accuracy
---
# On LongHealth Task 1 (single-patient documents, 16k-token prompt), Mistral-Small-24B-Instruct-2501 is most accurate at 84%, followed by Llama-4-Scout-17B-16E-Instruct at 81%.

Twelve models tested zero-shot at temperature 0, five shuffled runs each.

## Relations
- derived_from::[[sources/LongHealth - A Question Answering Benchmark with Long Clinical Documents]]
  > Mistral-Small-24B-Instruct-2501 achieved the highest accuracy, correctly answering 84% of the
  - Section 3.1, Table 2
- relates_to::[[concepts/longhealth]]
  - result on the benchmark
