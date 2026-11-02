# Knowledge repo

An LLM-maintained knowledge base for Claude Code, in the spirit of Karpathy's "LLM wiki",
built around one idea: **the model proposes, deterministic code decides what is valid.**

```
sources/raw/   -> you drop files here (md, txt, html, pdf). Never edited afterwards.
cortex/        -> compiled, typed, linked notes (claims, mechanisms, concepts, tensions, questions)
studio/        -> your outputs, built from the cortex
scripts/kb.py  -> the gatekeeper: check, index, search, nav, preflight, verification helpers
```

## Setup

1. `git init` (or clone), then start Claude Code in this folder. The SessionStart hook sets
   `core.hooksPath` to `.githooks` and runs `uv sync --locked` (creates `.venv` from `uv.lock`).
   Without Claude Code, run once: `git config core.hooksPath .githooks && uv sync`.
2. Requirements: git, bash (Git Bash on Windows) and [uv](https://docs.astral.sh/uv/). Python runs **only through uv**:
   `kb.py` refuses to start outside the project's uv environment, and Claude's permissions deny
   direct `python`, `python3` and `pip` calls. Dependencies live in `pyproject.toml` / `uv.lock`.
3. Works in Claude Code on the web: everything lives in the repo. Open the session on this repo
   directly (not inside a claude.ai Project thread, and not a multi-repo session - repo hooks do not run there).
   Push before you leave a web session; an unpushed commit lives only in that session's VM.

## Daily use

1. Add a file to `sources/raw/` named `YYYY-MM-short-slug.ext`.
2. In Claude Code: `/ingest` (next unprocessed source) or `/ingest <source-id>`.
   - a script builds a preflight report (similar nodes, existing mechanisms);
   - a clean-context `ingestor` subagent writes nodes;
   - a separate `verifier` subagent checks each new claim against its quote, without seeing the draft;
   - when the ingestor stops, a hook runs `kb.py check --strict`; failures send it back to work,
     success indexes and commits (`ingest: <source-id>`).
3. `git push` when you are happy. `git revert <sha>` undoes one ingest completely.
4. `/ask <question>` for cited answers. `/consolidate` now and then.

## Why it is built this way

- **Search cost.** Agents waste tokens by reading whole files to find out what is in them. Here every node
  has a one-line description, `catalog.md` lists them all, `kb.py search` (SQLite FTS5 / BM25) returns
  line ranges and snippets, and `kb.py nav` shows edge reasons without opening files.
- **Drift.** Repeated LLM rewriting drifts toward the model's own style and loses rare details. So sources
  are immutable and kept forever, nodes are edited in small steps from the source, and nothing is deleted.
- **Hallucinated grounding.** Quotes are checked verbatim against the extracted text. Claims are
  verified by a separate subagent that sees only the claim and the evidence, not the draft.
- **Forced analogies.** LLMs prefer word overlap to shared structure. Mechanisms need a one-to-one
  mapping table, a causal link, a prediction, a "breaks when" section and a distractor check, and
  start as `proposed` until a second source or real use supports them.

## kb.py commands

```
uv run scripts/kb.py check [--strict]   validate everything
uv run scripts/kb.py index              rebuild cortex/_index/
uv run scripts/kb.py search "query" [--kind cortex|sources] [-k 8]
uv run scripts/kb.py nav <node>
uv run scripts/kb.py preflight [source-id]
uv run scripts/kb.py distractor <node> <mechanism>
uv run scripts/kb.py hubs
uv run scripts/kb.py pairs | verdict <claim> pass|partial|fail
```

Searches that return nothing are logged to `cortex/_index/search-misses.log`. If it fills with misses
that a semantic search would have caught, that is the signal to add embeddings (for example `qmd`).
