---
type: concept
status: active
created: 2026-11-03
description: AstaBench, Allen AI benchmark suite for scientific research agents, 11 benchmarks, 2400 examples, InspectAI, leaderboard, cost, lit/code/data/discovery
---
# AstaBench

An Allen AI evaluation framework, built on InspectAI, for measuring scientific research abilities of AI agents across 11 benchmarks in four categories (lit, code, data, discovery), with standardized tools and environments and cost measurement.

Task suites (from the README): lit - PaperFindingBench, ScholarQABench2 (SQA), LitQA2-FT, LitQA2-FT-Search, ArxivDIGESTables-Clean; code - CORE-Bench-Hard, DS-1000, SUPER-Expert; data - DiscoveryBench; discovery - E2E-Bench, E2E-Bench-Hard. Each has validation and test splits.

## Relations
- derived_from::[[sources/github-allenai-asta-bench-·-github-20261103165041]]
  > AstaBench is an evaluation framework for measuring the scientific research abilities of AI agents.
- derived_from::[[sources/github-allenai-asta-bench-·-github-20261103165041]]
  > AstaBench includes a comprehensive suite of evaluation tasks across four main categories:
- relates_to::[[concepts/agent-baselines-astabench-solvers]]
  - the baseline solvers evaluated on this suite
- relates_to::[[concepts/react-tool-calling-agent-loop]]
  - the README's example full-suite run uses InspectAI's builtin ReAct agent
