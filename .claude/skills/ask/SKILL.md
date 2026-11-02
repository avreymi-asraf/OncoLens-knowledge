---
name: ask
description: Answer a question from the knowledge repo with file:line citations, in a separate low-context researcher.
argument-hint: "<question>"
context: fork
agent: researcher
background: false
---
Question: $ARGUMENTS

Answer it from this repository, following your ladder. Return the answer with citations.
