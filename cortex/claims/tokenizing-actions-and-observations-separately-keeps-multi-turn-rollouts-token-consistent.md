---
type: claim
status: proposed
created: 2026-11-02
verified: pass
description: tokenization, concatenation, token prefix consistency, on-policy, multi-turn rollout, Qwen2.5 tokenizer
---
# Tokenizing LLM action strings and tool observation strings separately and appending token lists avoids boundary-merging mismatches that joint tokenization of the concatenated string can cause.

## Relations
- derived_from::[[sources/VERLTOOL TOWARDS HOLISTIC AGENTIC]]
  > we adopt the first approach and always keep a consistent token list prefix during
  - Section 3.3, Figure 4
