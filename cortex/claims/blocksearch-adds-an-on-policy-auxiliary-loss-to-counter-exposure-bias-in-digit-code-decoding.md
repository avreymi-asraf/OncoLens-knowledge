---
type: claim
status: proposed
created: 2026-11-04
verified: pass
description: on-policy auxiliary loss, exposure bias, teacher forcing, rolled-out digit prefixes, document identifier codes, BlockSearch training
---
# BlockSearch adds an on-policy auxiliary loss over the model's own rolled-out identifier-digit prefixes because teacher forcing alone causes exposure bias.

## Relations
- derived_from::[[sources/Can Language Models Actually Retrieve In-Context-Drowning in Documents at Million Token Scale]]
  > bias issue: at inference, each digit conditions on the model’s own potentially incorrect prefix,
- relates_to::[[concepts/in-context-retrieval]]
  - instance of in-context retrieval
