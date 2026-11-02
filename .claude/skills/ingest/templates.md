# Node templates

Copy the matching template. `kb.py check` enforces everything marked "required".

## Claim - `cortex/claims/<claim-as-kebab-case-sentence>.md`

```
---
type: claim
status: proposed
created: 2026-11-02
verified: pending
description: <one line with the key terms and synonyms someone would search for>
---
# <The claim as one complete, falsifiable sentence.>

<Optional: 1-3 sentences of scope or conditions, in your own words. No new facts here.>

## Relations
- derived_from::[[sources/<source-id>]]
  > <exact text copied from sources/text/<source-id>.md - required, verbatim; use ... to elide>
  - <optional: where in the source, e.g. section 4.2>
- implements_mechanism::[[mechanisms/<mechanism>]]
  - <why this claim is an instance of the mechanism - one line>
```

Rules: one claim per file. The title is the claim. If a source contradicts an existing claim,
do not edit that claim - create a tension.

## Mechanism - `cortex/mechanisms/<abstract-name-without-domain-words>.md`

A mechanism is a domain-free causal structure that at least two concrete instances share.
If you cannot fill every section honestly, do not create the mechanism - link with `relates_to::` instead.

```
---
type: mechanism
status: proposed
kind: explanatory | generative
created: 2026-11-02
description: <one line, domain-free wording plus the domains it appears in>
---
# <Name of the mechanism>

## Structure
- regulated: <what is kept stable or optimized>
- driver: <what pushes on it>
- causal_link: <how the driver changes the regulated quantity - the higher-order relation>

## Instances
| role | <instance A> | <instance B> |
|---|---|---|
| <role 1> | <element in A> | <element in B> |
| <role 2> | <element in A> | <element in B> |

(One-to-one: an element may fill only one role per instance. At least two rows.)

## Candidate inference
<Something the mechanism predicts in one instance that comes from the other and is not yet checked.>

## Breaks when
<Conditions where the mapping fails or the instances diverge.>

## Distractor check
<Run `kb.py distractor <node> <this mechanism>`. One sentence: why the mapping holds for the true
instance but not for the distractor, despite shared words.>

## Relations
- derived_from::[[sources/<source-id>]]
  - <which source supplied which instance>
```

`kind: explanatory` claims the same causality in both instances. `kind: generative` only offers
a productive angle. When unsure, use generative.

## Concept - `cortex/concepts/<term>.md`

```
---
type: concept
status: active
created: 2026-11-02
description: <term, synonyms, domain>
---
# <Term>

<Definition in 1-3 sentences.>

## Relations
- derived_from::[[sources/<source-id>]]
  > <defining sentence from the source, optional but preferred>
```

## Tension - `cortex/tensions/<what-is-disputed>.md`

```
---
type: tension
status: open
created: 2026-11-02
description: <the disagreement in one line>
---
# <Question the sources disagree on>

<Each side in one sentence. Do not decide between them.>

## Relations
- supports::[[claims/<side-a>]]
  - <side A>
- contradicts::[[claims/<side-b>]]
  - <side B, and the likely reason for the difference: conditions, scale, method>
```

## Question - `cortex/questions/<question>.md`

```
---
type: question
status: open
created: 2026-11-02
description: <the open question in one line>
---
# <The question?>

<What evidence would answer it.>
```
