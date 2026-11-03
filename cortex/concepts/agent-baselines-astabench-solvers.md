---
type: concept
status: active
created: 2026-11-03
description: allenai agent-baselines repo, AstaBench baseline agents, InspectAI solvers, astabench eval, ReAct, smolagents, Asta science agents, STORM, FutureHouse
---
# agent-baselines (AstaBench baseline solvers)

An Allen AI repository of baseline agent implementations reported in AstaBench, packaged as InspectAI solvers runnable with `astabench eval`. It groups them into general baselines (ReAct, smolagents coder), Asta science agents (Asta-v0, ScholarQA, DataVoyager, Paper Finder, Tables, Code, Panda) and other baselines (STORM, FutureHouse).

## Relations
- derived_from::[[sources/github-allenai-agent-baselines-·-github-20261103165019]]
  > These agents are implemented as InspectAI solvers and can be run on the AstaBench suit with the `astabench eval` command.
- relates_to::[[concepts/react-tool-calling-agent-loop]]
  - the basic general baseline in the repo
- relates_to::[[concepts/code-action-agent]]
  - the smolagents coder baseline
- relates_to::[[concepts/astabench]]
  - the benchmark suite these solvers are run on
