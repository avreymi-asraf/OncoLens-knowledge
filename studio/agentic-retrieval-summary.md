# From Fixed Pipelines to Agents That Search and Learn: A Joint Summary

*We prepared and present this summary together, as a group. Each part is shared work, not one person's section.*

## The common thread

The four articles we read share one idea: a language model works better when it can **decide for itself how to search**, rather than running a fixed "retrieve once, then answer" pipeline. They move from better prompting, to self-correcting agents, to training with reinforcement learning. Read in this order, each article solves a problem the previous one leaves open.

## 1. Why plain RAG falls short (Hugging Face: *Agentic RAG*)

Standard retrieval-augmented generation (RAG) retrieves documents once. If that retrieval is poor, the answer is poor too, and nothing in the pipeline notices. A second problem is quieter: the user's question is used as the reference for similarity search, but the documents that answer it are usually written as statements, not questions. Those answer documents can rank below other documents that merely look like questions.

The article's fix is to give the model a retriever *tool* instead of a fixed retrieval step. The tool's description tells the agent to write queries as affirmative sentences and to call the retriever several times with semantically different queries. The agent then reads what comes back, judges it, and searches again if needed. The author notes that this simple setup recovers, almost for free, the behaviour of more advanced techniques such as HyDE (searching with a hypothetical answer) and Self-Query.

On an LLM-judged question set about Hugging Face documentation, the agent scored 86.9% against 73.1% for standard RAG, and 36% with no knowledge base at all. We note one caveat: the agent and the standard pipeline used different reader models (Llama-3.1-70B versus Qwen2.5-72B), and it is a single run.

## 2. An agent that checks its own work (LangChain: *Custom RAG agent with LangGraph*)

The LangChain tutorial makes the loop explicit as a graph of steps:

1. **Decide:** the model chooses whether to call the retriever or to answer directly. This choice is what makes the system agentic rather than a fixed pipeline.
2. **Retrieve:** if it calls the tool, documents are fetched.
3. **Grade:** a second LLM call gives the documents a yes/no relevance score.
4. **Route:** relevant documents go to answer generation; irrelevant ones send the agent to rewrite the question and try again.

This rewrite-and-retry loop lets the agent recover from a weak first search instead of stopping or inventing an answer. The tutorial also adds a security point: both the grader and the answer generator are told to treat retrieved text as data only, and to ignore any instructions hidden inside it (a defence against prompt injection).

## 3. Searching in several hops (DSPy: *Multi-hop RAG*)

Some questions cannot be answered from one document. To check a claim about "the author of the Beatles script *Up Against It*", the system must first find who the author is, then search for facts about that person. The DSPy program handles this with a loop of "hops": generate a query from the claim and the notes so far, retrieve with BM25 over Wikipedia abstracts, then append new notes and relevant page titles.

Unoptimized, this program on the small Llama-3.1-8B model found the right pages only about 31% of the time on 3-hop HoVer claims. DSPy's MIPROv2 optimizer then rewrote both prompts together, using GPT-4o as a teacher. Recall rose to about 59%, for roughly 35 minutes and $5. The optimized model learned a sensible strategy: with empty notes, it asks only for the first missing entity (here, the author, who turns out to be Joe Orton) instead of searching for the whole claim. The article adds that a small model can often teach itself; the larger teacher mainly protects against a poor starting setup.

## 4. Training agents to use tools (*VerlTool*)

The last paper moves from prompting to training. It studies *agentic reinforcement learning with tool use*: the model's output alternates between its own actions and observations returned by tools such as code, search, SQL and vision. VerlTool offers one framework for all of these, with several practical lessons:

- **Mask tool outputs.** Tool observation tokens are not produced by the model, so they are excluded from the training loss.
- **Tokenize pieces separately.** Actions and observations are tokenized one at a time and joined, which avoids token mismatches at the boundaries.
- **Run asynchronously.** Letting each trajectory call tools on its own, instead of waiting for the whole batch, makes rollouts about 1.2–2× faster.

Trained this way, models match or beat task-specific systems across six domains (for example, 45.9% average on knowledge QA against Search-R1). The paper also warns that tool use does not appear on its own: without suitable reward design, models can stop calling tools within a few training steps. Tool use also adapts to the tool: calls drop when outputs can be memorized (SQL results) and rise when they cannot (rich search results).

## How the four fit together

| Article | Main idea | Key result |
|---|---|---|
| Hugging Face | Let the agent write and repeat its own queries | 86.9% vs 73.1% |
| LangChain | Grade results, rewrite, retry | Recovers from weak retrieval |
| DSPy | Multi-hop search plus prompt optimization | 31% → 59% recall |
| VerlTool | Train tool use with reinforcement learning | Matches specialized systems in six domains |

## What we take away

The gains come from giving the model control of the search loop and a way to recover from failed searches. The first three articles get there through prompts and program structure; VerlTool shows how to train the same behaviour into the model, and warns that it needs careful rewards to stick. For the key terms in English and Hebrew, see the companion lexicon in `studio/lexicon-agentic-rag-and-agentic-rl.md`.
