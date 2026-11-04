---
type: claim
status: proposed
created: 2026-11-04
verified: pass
description: SSMax, scalable softmax, log N scaling of pre-softmax scores, attention sink, length-aware softmax, mitigation of attention dilution
---
# Scaling pre-softmax scores with log N (SSMax) is effective against attention dilution, whereas an additive length-aware attention sink barely helps.

## Relations
- derived_from::[[sources/Can Language Models Actually Retrieve In-Context-Drowning in Documents at Million Token Scale]]
  > corpus grows; scaling pre-softmax scores withlogN (SSMax) is effective, whereas
- relates_to::[[concepts/in-context-retrieval]]
  - instance of in-context retrieval
