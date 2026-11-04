---
type: claim
status: proposed
created: 2026-11-04
verified: partial
description: ChemCrow ReAct format, Thought Action Action Input Observation, generation pauses, tool execution, iterative loop until final answer
---
# In ChemCrow, after the LLM emits an Action and Action Input, text generation pauses, the program executes the requested tool, and the result is returned prepended by 'Observation' before the next Thought, iterating until a final answer.

## Relations
- derived_from::[[sources/LLMs and AI Agents for Research-2]]
  > The result is returned to the LLM 
  > prepended by the keyword ‘Observation’, and the LLM proceeds to the
- relates_to::[[concepts/react-tool-calling-agent-loop]]
  - ChemCrow is an instance of the ReAct loop
