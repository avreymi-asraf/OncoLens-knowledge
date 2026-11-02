---
type: concept
status: active
created: 2026-11-02
description: ARLT, agentic RL with tool use, multi-turn RLVR with tool observations, trajectory of actions and observation tokens
---
# Agentic Reinforcement Learning with Tool use (ARLT)

Multi-turn RL with verifiable rewards where the LLM interleaves action tokens with observation tokens returned by external tools (code, search, SQL, vision), rather than single-turn RLVR.

## Relations
- derived_from::[[sources/VERLTOOL TOWARDS HOLISTIC AGENTIC]]
  > the trajectory can be written asτ={a 0, o0, . . . , an−1, on−1, an}
