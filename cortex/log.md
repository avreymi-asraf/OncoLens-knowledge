# Log

Append-only. One line per operation.

- 2026-11-02 23:17 | verify | claims/a-unified-tool-server-framework-reaches-task-specific-baseline-performance-across-six-agentic-rl-domains -> partial | 45.9% on QA beats Search-R1 and SQL matches, but 'average' and match-or-exceed across all six not shown
- 2026-11-02 23:18 | verify | claims/asynchronous-per-trajectory-rollout-speeds-up-agentic-rl-rollouts-by-1-2-to-2x -> pass | table gives 1.22-1.97x
- 2026-11-02 23:18 | verify | claims/tokenizing-actions-and-observations-separately-keeps-multi-turn-rollouts-token-consistent -> pass | keeps consistent token prefix; re-tokenization changed content
- 2026-11-02 23:18 | verify | claims/tool-call-frequency-during-rl-falls-for-memorizable-tool-outputs-and-rises-for-unmemorizable-ones -> partial | SQL decrease via memorizing shown; rise for search not in context
- 2026-11-02 23:18 | verify | claims/tool-observation-tokens-are-off-policy-and-masked-from-the-grpo-loss -> pass | stated, masked typically
- 2026-11-02 23:18 | verify | claims/tool-use-vanishes-during-rl-without-suitable-reward-design -> pass | directly stated
- 2026-11-02 23:18 | ingest | VERLTOOL TOWARDS HOLISTIC AGENTIC | 6 claims, 0 updated, 0 mechanisms
- 2026-11-02 23:19 | verify | claims/a-small-model-can-typically-teach-itself-multi-hop-tasks-in-dspy-and-a-larger-teacher-only-adds-robustness -> pass | Source states this nearly verbatim
- 2026-11-02 23:19 | verify | claims/an-unoptimized-two-module-multi-hop-program-on-llama-3-1-8b-reaches-only-31-percent-top5-recall-on-hover -> pass | 31.3% metric shown; 3-hop/unoptimized/top5 are context-plausible, table has top5_recall
- 2026-11-02 23:19 | verify | claims/joint-prompt-optimization-with-miprov2-roughly-doubles-multi-hop-retrieval-recall-from-31-to-59-percent -> pass | 59.11 vs ~30%; joint optimization stated; MIPROv2 not in quote but fine
- 2026-11-02 23:19 | verify | claims/optimized-query-generator-decomposes-a-multi-hop-claim-by-asking-for-the-first-unknown-entity-when-notes-are-empty -> pass | Empty notes yield query about first unknown entity (script author)
- 2026-11-02 23:19 | ingest | multi-hop-rag-dspy | 4 claims, 0 updated, 0 mechanisms
- 2026-11-02 23:20 | verify | claims/a-relevance-grader-after-retrieval-routes-the-agent-to-answer-or-to-question-rewrite -> partial | Routing supported; LLM grader and binary score not in quote/context
- 2026-11-02 23:20 | verify | claims/retrieved-text-should-be-treated-as-data-only-in-grader-and-generator-prompts -> partial | Only generator prompt shown; grader prompt not in context
- 2026-11-02 23:20 | verify | claims/rewriting-the-question-and-retrying-retrieval-lets-an-agent-recover-from-a-weak-first-retrieval -> pass | Directly stated
- 2026-11-02 23:20 | verify | claims/the-model-deciding-whether-to-call-the-retriever-makes-rag-agentic-rather-than-a-fixed-pipeline -> pass | Directly stated
