---
type: claim
status: proposed
created: 2026-11-04
verified: pass
description: retrieval heads, per-head gold document ranking, attention heads vs decoded answer, latent retrieval signal, degrades with corpus size
---
# Individual attention heads rank the gold document first more often than the model decodes it, though this signal also weakens as corpus size grows.

## Relations
- derived_from::[[sources/Can Language Models Actually Retrieve In-Context-Drowning in Documents at Million Token Scale]]
  > Individual heads still rank the gold document first more often than the model decodes it at every
- relates_to::[[concepts/in-context-retrieval]]
  - instance of in-context retrieval
