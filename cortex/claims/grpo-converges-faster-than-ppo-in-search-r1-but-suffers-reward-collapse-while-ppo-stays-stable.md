---
type: claim
status: proposed
created: 2026-11-03
verified: pass
description: PPO vs GRPO, convergence speed, reward collapse, training stability, critic warm-up, Search-R1
---
# In Search-R1 training, GRPO converges faster than PPO but can suffer reward collapse after many steps, while PPO stays stable and both reach comparable final reward.

## Relations
- derived_from::[[sources/Search-R1 Training LLMs to Reason and Leverage Search]]
  > (1) GRPO converges faster than PPO across all cases. This is because PPO relies
  > on a critic model, which requires several warm-up steps before effective training begins.
  > (2) PPO demonstrates greater training stability. As shown in Figure 2(a), GRPO leads to
  > reward collapse after training for many steps, whereas PPO remains stable. (3) The final
  > training rewards of PPO and GRPO are comparable.
  - section 5.1
- supports::[[claims/reinforce-outperforms-ppo-and-grpo-for-search-r1-training-with-fewer-search-actions]]
  - independent original-paper evidence for the "GRPO least stable" part only; REINFORCE was not tested
