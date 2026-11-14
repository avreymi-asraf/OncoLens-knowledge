# Cortex profile

> What this cortex is. Read before any operation. Where this file and the `cortex` skill differ on a name or a place, this file wins.

## 1. What the synthesis is for
In the owner's words:

> We aim to develop a method for training small models to extract relevant information from the medical records of cancer patients. The agent will need to answer questions and evaluate specific patient metrics based on these documents, while also navigating and interpreting the documentation.

The reader is the team building that method. A claim or page earns its place when it changes a decision about how to build, train or evaluate such an agent. Areas that need in-depth knowledge:

1. **Training small models for data extraction** (clinical/medical information extraction, structured output, distillation, fine-tuning small LMs).
2. **Training small models with reinforcement learning** (RL for LLMs/agents, reward design, GRPO/PPO and successors, tool-using and document-navigating agents).
3. **The progression of cancer** (staging, disease course, markers of progression and response, how they appear in records).
4. **Cancer treatment** (treatment lines, regimens, response criteria, adverse events, as documented in records).

In scope: anything that bears on what to extract from oncology records, how to measure it, and how to train a small model to do it. Out of scope: clinical advice for individual patients, general oncology with no bearing on records or metrics, large-model-only methods with no path to small models.

## 2. Layout
| Layer | Where | Notes |
|---|---|---|
| Sources | `../sources/`: `raw/` originals, `text/` the text read (written by `cortex.py store`), `<source-id>.md` notes | Never edited |
| Claims | `claims/` | One per file |
| Synthesis | `pages/` (concept, method, comparison), `tensions/`, `questions/` | Cite claims |
| Map | `index.md` | One line per page, tension and question |

## 3. Anchors
| Anchor | Accepted | What it earns here |
|---|---|---|
| `quote` | Yes | The source says it. A page resting only on quotes says so. |
| `experiment` | Yes | Our own training/eval runs, with round and commit. |
| `stated` | No | |

A claim moves from `provisional` to `confirmed` when a second independent source supports it, or one of our experiments reproduces it.

## 4. Checking
`cortex.py check` passes before every commit. Blind verification of new claims (`/cortex verify`): for claims a page will cite.

## 5. Moments
Fusion happens at the end of every `add`. A review runs every ~20 claims, and before a design decision that leans on the cortex.
