---
type: claim
status: proposed
created: 2026-11-04
verified: pass
description: adaptive difficulty calibration, filter synthetic questions with OpenAI-o3 and GPT-4, regenerate if accuracy above 50%, synthetic QA hardness
---
# KISA regenerates any synthetic question that OpenAI-o3 or GPT-4 answers with more than 50% accuracy, to keep questions hard.

## Relations
- derived_from::[[sources/MedResearcher-R1]]
  > We test each
  > question with OpenAI-o3 and GPT-4. If either model achieves accuracy greater than 50%, the system regenerates the
  > question.
  - section 4
- relates_to::[[concepts/knowledge-informed-trajectory-synthesis]]
  - one stage of KISA
