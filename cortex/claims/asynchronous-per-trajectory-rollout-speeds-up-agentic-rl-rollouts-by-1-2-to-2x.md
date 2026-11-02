---
type: claim
status: proposed
created: 2026-11-02
verified: pass
description: async rollout, synchronous batch, tool call latency, GPU idle bubbles, speedup, VerlTool agentic RL
---
# Letting each trajectory call the tool server independently (asynchronous rollout) instead of batch-synchronously speeds up rollouts by about 1.2x to 2x depending on the task.

## Relations
- derived_from::[[sources/VERLTOOL TOWARDS HOLISTIC AGENTIC]]
  > Speed Up (×) 1.32 1.22 1.97
  - Table 2: Math-TIR, SQL, DeepSearch on 8 H100 GPUs
