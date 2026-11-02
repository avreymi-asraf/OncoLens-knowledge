---
type: claim
status: proposed
created: 2026-11-02
verified: pass
description: DSPy teacher LM GPT-4o invoked few times for small student LM; teacher not strictly necessary, gives robustness to initial optimizer configuration.
---
# A small model can typically teach itself tasks like multi-hop retrieval in DSPy, with a larger teacher serving mainly as insurance against a poor initial configuration.

## Relations
- derived_from::[[sources/multi-hop-rag-dspy]]
  > This is technically not necessary; the small model can typically teach itself tasks like this in DSPy. But using a larger teacher will give us some peace of mind, where the initial system or optimizer configuration doesn't matter as much.
  - tutorial setup section
