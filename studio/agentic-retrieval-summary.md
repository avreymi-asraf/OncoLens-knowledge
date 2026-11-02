# From Fixed Pipelines to Agents That Search and Learn: A Joint Summary

*We prepared and present this summary together, as a group. Each part is shared work, not one person's section.*

## The common thread

The four articles we read share one idea: a language model works better when it can **decide for itself how to search**, rather than running a fixed "retrieve once, then answer" pipeline. They move from better prompting, to self-correcting agents, to training with reinforcement learning.

## 1. Why plain RAG falls short (Hugging Face: *Agentic RAG*)

Standard retrieval-augmented generation (RAG) retrieves documents once. If that retrieval is poor, the answer is poor too. A second problem: a user's question is phrased as a question, while the documents that answer it are written as statements, so searching with the raw question can miss them. The article gives the model a retriever tool and lets it write its own queries (as statements, in several varied versions) and search again. On a question set about Hugging Face documentation, the agent scored 86.9% against 73.1% for standard RAG (36% with no knowledge base). We note one caveat: the two setups used different models.

## 2. An agent that checks its own work (LangChain: *Custom RAG agent with LangGraph*)

This tutorial builds the loop as a graph. The model first decides whether to search at all. Retrieved documents are then graded for relevance: relevant ones go to answer generation; irrelevant ones trigger a rewritten question and a new search. Retrieved text is treated as data only, against prompt injection.

## 3. Searching in several hops (DSPy: *Multi-hop RAG*)

Some questions need facts from several documents in sequence. The DSPy program loops over "hops": write a query, retrieve, keep notes, repeat. Unoptimized, a small Llama-3.1-8B model found the right pages only 31% of the time. Automatic prompt optimization (MIPROv2) raised this to 59%, for about 35 minutes and $5.

## 4. Training agents to use tools (*VerlTool*)

The last paper moves from prompting to training. VerlTool is one framework for reinforcement learning with tools such as code, search, SQL and vision. It hides tool outputs from the training loss, runs trajectories asynchronously (1.2–2× faster), and matches specialized systems across six domains. It also warns that without good reward design, models simply stop using tools.

## What we take away

The gains come from giving the model control of the search loop and a way to recover from failed searches.
