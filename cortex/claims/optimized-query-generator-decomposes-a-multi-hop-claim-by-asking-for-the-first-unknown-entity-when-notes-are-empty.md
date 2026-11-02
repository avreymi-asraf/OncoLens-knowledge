---
type: claim
status: proposed
created: 2026-11-02
verified: pass
description: Optimized DSPy hop query generator with empty notes issues a sub-question for the missing bridge entity (author of Up Against It), query decomposition per hop.
---
# With empty notes, the optimized hop query generator asks only for the first missing bridge entity of a multi-hop claim rather than querying the whole claim.

Example: for the claim about the author of the Beatles script Up Against It, the first query asks who the author is; the later hop retrieves Joe Orton.

## Relations
- derived_from::[[sources/multi-hop-rag-dspy]]
  > Who is the author of the 1960s unproduced script written for The Beatles, Up Against It?
  - generated query in the inspected history, notes were N/A
