---
type: claim
status: proposed
created: 2026-11-04
verified: partial
description: SFT loss mask, agent tokens vs tool output tokens indicator m=0, loss masking observations in agent fine-tuning
---
# MedResearcher-R1's SFT loss counts only agent tokens and masks out tool output tokens.

## Relations
- derived_from::[[sources/MedResearcher-R1]]
  > Each token yi,t might be an agent token (plain text or tool-call tokens) or a tool output token.
  - section 5.1; indicator m is 1 for agent tokens, 0 for tool output tokens
- relates_to::[[claims/research-masks-retrieval-result-tokens-from-the-grpo-loss]]
  - same masking of tool observations, here in SFT rather than GRPO
