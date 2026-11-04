---
type: concept
status: active
created: 2026-11-03
description: ReAct agent, LLM tool-calling in a loop, reason-act loop, max_steps budget, basic agent baseline
---
# ReAct tool-calling agent loop

An agent that repeatedly calls an LLM with tool-calling enabled, executes the chosen tool, and feeds the result back, until it answers or hits a step limit (`max_steps`).

## Relations
- derived_from::[[sources/github-allenai-agent-baselines-·-github-20261103165019]]
  > a simple ReAct implementation that uses LLM tool-calling in a loop. It supports all [AstaBench tool options](https://github.com/allenai/asta-bench?tab=readme-ov-file#tools-and-utilities) and configurable `max_steps`.
- derived_from::[[sources/LLMs and AI Agents for Research-2]]
  > The text generation then pauses, and the program attempts to execute the 
  - lecture slides (ChemCrow, p.41) describe the same Thought/Action/Observation loop
