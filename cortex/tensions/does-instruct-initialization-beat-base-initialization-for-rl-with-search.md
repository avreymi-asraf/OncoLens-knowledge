---
type: tension
status: open
created: 2026-11-03
description: base vs instruct starting checkpoint for search RL; ReSearch says instruct better, Search-R1 says final reward similar
---
# Does starting RL-with-search from an instruction-tuned model give better final performance than starting from a base model?

ReSearch reports instruct initialization is consistently better; Search-R1 reports instruct only converges faster and the final training reward is highly similar (and its own Table 3 PPO-7B base beats instruct on EM).

## Relations
- supports::[[claims/rl-from-instruction-tuned-models-outperforms-rl-from-base-models-in-research]]
  - side A: instruct better at end (ReSearch, GRPO, 7B/32B, evaluation metrics)
- contradicts::[[claims/search-r1-instruct-models-converge-faster-but-reach-similar-final-reward-to-base-models]]
  - side B: parity after training (Search-R1, PPO/GRPO, 3B/7B, training reward); differences in algorithm, scale and metric may explain it
