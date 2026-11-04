---
type: claim
status: proposed
created: 2026-11-04
verified: pass
description: LongHealth context length effect, accuracy decline 4000 to 16000 tokens, nine of 16k models, gpt-3.5 -5%, vicuna-7b -13%, Yi-6B outlier
---
# On LongHealth Task 1, nine of the 16k-capable models lose accuracy as the prompt grows from 4,000 to 16,000 tokens.

Longer prompts were made by adding distractor texts from other patients. Yi-6B-200K was the only model that improved.

## Relations
- derived_from::[[sources/LongHealth - A Question Answering Benchmark with Long Clinical Documents]]
  > For prompt lengths of 4000, 8000, 12,000, and 16,000 tokens, nine of the 16
  - Section 3.1; the sentence continues "ble models showed an accuracy decline"
- derived_from::[[sources/LongHealth - A Question Answering Benchmark with Long Clinical Documents]]
  > Yi-6B-200  K remained the
- relates_to::[[claims/attention-dilution-drives-the-gold-document-attention-share-toward-zero-as-the-corpus-grows]]
  - another source reporting accuracy loss as irrelevant in-context documents are added
