---
name: consolidate
description: Structural maintenance of cortex/ - merge near-duplicates, split catch-all mechanisms, fix links. Never rewrites claims.
disable-model-invocation: true
allowed-tools: Bash(uv run *)
---
## Current state (generated)

!`uv run --quiet --project ${CLAUDE_PROJECT_DIR} ${CLAUDE_PROJECT_DIR}/scripts/kb.py hubs`

## Task

Do structural maintenance only. Run kb.py as `uv run scripts/kb.py <command>`.

1. **Near-duplicates.** Read `cortex/_index/catalog.md`. For nodes whose descriptions look alike, run
   `kb.py search` on the title. If two nodes state the same thing, keep the older one, move the other's
   `derived_from` quotes into it, and mark the newer one `status: superseded` with
   `supersedes::` pointing from the kept node. Do not delete files.
2. **Hub mechanisms** listed above: check whether every incoming link truly fits the mechanism's
   Structure. Links that only share vocabulary: change them to `relates_to::` with a reason.
3. **Promotion.** A `proposed` mechanism or claim with a second, independent `derived_from` source may
   become `supported`. Say which ones you promoted and why.
4. Never change the wording of a claim title, a quote, or a mechanism's Structure. If one looks wrong,
   create a `questions/` node about it instead.
5. Run `kb.py check`, fix errors, then commit with message `consolidate: <summary>`. Do not push.
