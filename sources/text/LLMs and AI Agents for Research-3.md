<!-- page 1 -->


<!-- page 2 -->


<!-- page 3 -->
From single agent perspective, can think of other agents as part of the 
environment.
Cooperates with others. Reasons about others’ motivations.
Competition and Cooperation. Motivations of various agents can be at 
odds with each other. If a + reward to an agent means – to another then 
that is competition. If both get +, that can lead to cooperation.
Human-in-loop as multi agent

<!-- page 4 -->


<!-- page 5 -->


<!-- page 6 -->


<!-- page 7 -->
longer-term plans 
higher-level reflections

<!-- page 8 -->


<!-- page 9 -->
Generative Agent Simulations of 1,000 People

<!-- page 10 -->


<!-- page 11 -->


<!-- page 12 -->


<!-- page 13 -->


<!-- page 14 -->


<!-- page 15 -->


<!-- page 16 -->


<!-- page 17 -->
llamaindex

<!-- page 18 -->
llamaindex

<!-- page 19 -->
llamaindex

<!-- page 20 -->


<!-- page 21 -->
Scientific Discovery + AI
AI as helpers:
Accelerate the pace of scientific discovery by building agents that help with 
specific aspects of the scientific discovery process. For example:
• A literature search tool that helps you find relevant papers
• An ideation tool that helps you come up with new ideas
• An experiment builder tool to help you design experiments
• etc.
Autonomous Discovery:
Design agents for end-to-end discovery -- that can, entirely on their own 
(with minimal human intervention), come up with ideas, hypothesis, design 
and run experiments, and report the results. 
 

<!-- page 22 -->
Scientific Discovery + AI
AI as helpers:
Accelerate the pace of scientific discovery by building agents that help with 
specific aspects of the scientific discovery process. For example:
• A literature search tool that helps you find relevant papers
• An ideation tool that helps you come up with new ideas
• An experiment builder tool to help you design experiments
• etc.
Autonomous Discovery:
Design agents for end-to-end discovery -- that can, entirely on their own 
(with minimal human intervention), come up with ideas, hypothesis, design 
and run experiments, and report the results. 
 

<!-- page 23 -->
… 
Problems
… 
Directions
Huge Hypothesis Spaces

<!-- page 24 -->
An NLP-based ideator might help generate new ideas based on 
existing ideas in the scientific literature (i.e. by reading 
papers).
It might work automatically, or it might work by asking a human 
to provide idea generation parameters, and iterate on these (i.e. 
“human-in-the-loop”).


<!-- page 25 -->
Literature-based discovery (LBD), Don Swanson ‘86
● Leveraging the literature for automatically generating 
new hypotheses


<!-- page 26 -->
Literature-based discovery (LBD), Don Swanson ‘86
● ABC paradigm


<!-- page 27 -->
Literature-based discovery (LBD), Don Swanson ‘86
● ABC paradigm
A + B
 “Drug A regulates 
levels of B…” 

<!-- page 28 -->
Literature-based discovery (LBD), Don Swanson ‘86
● ABC paradigm
A + B
 B + C
“Disease C aﬀects 
levels of B…” 

<!-- page 29 -->
Literature-based discovery (LBD), Don Swanson ‘86
● ABC paradigm
A + B
 B + C
 A + C ???


<!-- page 30 -->
Narrowing of arteries supplying blood to skin
Raynaud syndrome 
Fish oil
 Blood viscosity

<!-- page 31 -->
Narrowing of arteries supplying blood to skin
Raynaud syndrome 
Fish oil
 Blood viscosity
 Treatment 

<!-- page 32 -->
Sybrandt et al., KDD 2017


<!-- page 33 -->
Nature 2019

<!-- page 34 -->
Nature 2019

<!-- page 35 -->


<!-- page 36 -->


<!-- page 37 -->
Scimon: Scientiﬁc Inspiration Machines 
Optimized for Novelty
Q. Wang, D. Downey, H. Ji, T. Hope , ACL 2024; arXiv v1: 5/2023  

<!-- page 38 -->
Background 
Context
Problems, 
motivations, 
focus points… 
Scimon: Scientiﬁc Inspiration Machines 
Optimized for Novelty
Q. Wang, D. Downey, H. Ji, T. Hope , ACL 2024; arXiv v1: 5/2023  

<!-- page 39 -->
Background 
Context
Inspiration 
Retrieval
Prior Literature 
{(Background_i, idea_i)}
Problems, 
motivations, 
focus points… 
Scimon: Scientiﬁc Inspiration Machines 
Optimized for Novelty
Q. Wang, D. Downey, H. Ji, T. Hope , ACL 2024; arXiv v1: 5/2023  

<!-- page 40 -->
Background 
Context
Inspiration 
Retrieval
Idea Generation
Prior Literature 
{(Background_i, idea_i)}
Problems, 
motivations, 
focus points… 
“Given [context], 
a [new idea]...”
Scimon: Scientiﬁc Inspiration Machines 
Optimized for Novelty
Q. Wang, D. Downey, H. Ji, T. Hope , ACL 2024; arXiv v1: 5/2023  

<!-- page 41 -->
Background 
Context
Inspiration 
Retrieval
Idea Generation
Iterative 
Novelty 
Boosting
Prior Literature 
{(Background_i, idea_i)}
𝛥
Problems, 
motivations, 
focus points… 
“Given [context], 
a [new idea], 
𝛥 vs. prior work…”
Scimon: Scientiﬁc Inspiration Machines 
Optimized for Novelty
Q. Wang, D. Downey, H. Ji, T. Hope , ACL 2024; arXiv v1: 5/2023  

<!-- page 42 -->
Synthesize 
New Direction 
Problem
Description
Find Literature 
Inspirations
+ continual learning
+ meta ﬁne-tuning
+ memory networks
+ knowledge distillation
Meta learning for 
integrating new 
information … 
external memory 
matrix to selectively 
retrieve information …
Periodic knowledge 
distillation…
Input Retrieve inspirations
pre – training with 
streaming data,  
lifelong learning.
Suggest a new idea
Preliminary Results: Example
Q. Wang, D. Downey, H. Ji, T. Hope , ACL 2024; arXiv v1: 5/2023  

<!-- page 43 -->
Optional input: seed concept 
to guide hypothesis gen.

<!-- page 44 -->
Solutions to past 
similar problems
Affordances 
KG (methods and uses)
Citation-based (assume we 
know all the references of a 
future idea paper; including 
noisy irrelevant refs)

<!-- page 45 -->


<!-- page 46 -->


<!-- page 47 -->


<!-- page 48 -->


<!-- page 49 -->


<!-- page 50 -->
Extracting Training Data + Inspirations 
from Past Papers

<!-- page 51 -->
Encouraging Novelty vs. Background: In Training
In-context negatives

<!-- page 52 -->
Target 
In-context
negative k 
In-context contrastive objective
Encouraging Novelty vs. Background: In Training

<!-- page 53 -->
Generated idea Global reference literature
Novelty Penalty
Encouraging Novelty vs. Literature: In Inference

<!-- page 54 -->
Generated idea Global reference literature
Novelty Penalty
Encouraging Novelty vs. Literature: In Inference
 Minimize 
s.t.
      remains relevant to the background context


<!-- page 55 -->
Retrieve-Compare-Update
Encouraging Novelty vs. Literature: In Inference
- Retrieve related work
- If similarity < threshold:
- Instruct model to update in light of related work + initial problem 

<!-- page 56 -->
LLMs for Scientiﬁc Inspirations?
- Human evaluation studies
- Idea quality: relevant, novel, reasonable, speciﬁc, clear, 
technical detail 
- Rated also versus the ground truth idea
- Evaluating novelty boosting
1.5X - 2X boost vs. GPT-4 idea ratings 
(CS/biomed experts evaluations)

<!-- page 57 -->
1st / 2nd iteration ideas 
that gained novelty over 
the initial idea
Type of inspiration retrieval
(solutions to past problems,
citation-based, knowledge graph)
Novelty Boosting Evaluation

<!-- page 58 -->
Novelty Boosting Evaluation

<!-- page 59 -->


<!-- page 60 -->
LLMs for Scientiﬁc Inspirations?
- Still often generic suggestions, woven with details copied from context 
- “NLP with ML algorithms and sentiment analysis for X” 
- “Data augmentation and transfer learning for X” 

<!-- page 61 -->
LLMs for Scientiﬁc Inspirations?
- Often generic suggestions, woven with details copied from context 
- “NLP with ML algorithms and sentiment analysis for X” 
- “Data augmentation and transfer learning for X” 
- Simple logical modiﬁcations to the context 
- “high latency” / “eﬃciency limitations” -> “low latency” / “highly eﬃcient”

<!-- page 62 -->
LLMs for Scientiﬁc Inspirations?
- Often generic suggestions, woven with details copied from context 
- “NLP with ML algorithms and sentiment analysis for X” 
- “Data augmentation and transfer learning for X” 
- Simple logical modiﬁcations to the context 
- “high latency” / “eﬃciency limitations” -> “low latency” / “highly eﬃcient”
- Novelty boosting adds combinations of “buzz concepts” :
- Dynamic/adaptive modeling, graph models and representations, 
fusion of multiple modalities and sources…
“Dynamic Syntax-Aware Graph Fusion Networks (DSAGFN)”

<!-- page 63 -->
LLMs for Scientiﬁc Inspirations?
- Our modelling augmentations produced promising signal
- Higher technical detail, less generic
- Higher perceived novelty, utility
… but: 
Directions still judged as
far from suﬃcient in novelty, utility. 

<!-- page 64 -->
Input: Problem description
Find novel idea abstractions, perspectives 
& interdisciplinary inspirations 

<!-- page 65 -->
Solar 
System
Atom
Analogies
for ﬁnding
cross-domain 
inspirations

<!-- page 66 -->
Critique and Enhance Ideas
MARG: Multi-Agent Review Generation for Scientiﬁc Papers, 2024
Multiple LLM agents, each focusing on reviewing diﬀerent aspects

<!-- page 67 -->


<!-- page 68 -->
Recombination


<!-- page 69 -->


<!-- page 70 -->
Scideator: Human-LLM Scientific Idea Generation Grounded in Research-Paper Facet Recombination

<!-- page 71 -->


<!-- page 72 -->
Extract components of 
papers
Combine 
components in 
novel fashion
Check whether the ideas 
are novel
Figure 1

<!-- page 73 -->
User provides a set of input 
papers that they would like to 
use as a starting point for 
ideation
The tool responds by 
retrieving analogous papers 
to the input papers and 
extracting facets (purpose, 
mechanism) from the input 
and analogous papers.
Analogous: papers with similar 
purpose but diﬀerent 
mechanism, or vice versa 

<!-- page 74 -->
User then selects paper 
facets as well as adds their 
own facets for which
they want to generate ideas.
The tool recombines these 
selected facets into ideas 
with one purpose and one 
mechanism. If the user
did not select any facets of a 
certain type, the tool selects 
one for them


<!-- page 75 -->
The user selects an idea to 
assess for novelty
The tool classiﬁes the idea as 
"novel" or "not novel" and 
provides a short reason as to 
why.


<!-- page 76 -->
The user reviews the novelty 
classiﬁcation and
adjusts it if they disagree
If the idea is determined to 
be "not novel," the tool 
provides suggestions for 
more novel ideas that replace
one of the initial idea’s facets.


<!-- page 77 -->


<!-- page 78 -->


<!-- page 79 -->


<!-- page 80 -->
Search API
Input Idea
Papers Related to Input Paper 
from Semantic Scholar
Analogous Papers 
Idea-Keyword 
Papers
From Previous Steps  (Sections 3.3.1, 3.3.2)
Candidate Papers
STEP 2: Filtering for Most Relevant Papers
STEP 1: Identifying a Broad 
Collection of Papers Relevant to Idea
STEP 3: Evaluating Novelty of the Idea
Compare Specter 
Embeddings 
RankGPT  
Re-Ranking
T op N Papers 
Similar to Idea Most Relevant Papers
Novelty Classification and Reasoning
Input Idea
Most Relevant Papers
Keywords
Extract 
keywords 
from Idea 
Input Idea
Expert Labeled Examples 
..
Classification: Not Novel
Reasoning: The idea is not novel because it closely resembles existing tools like 'Bursting Scientific 
Filter Bubbles'[4], Bridger[9] and ResearchRabbit[3], which also use citation-based suggestions 
and visualizations. The proposed tool's combination of citation networks and author profiles is already 
well-covered by these systems.
…
Most Relevant 
Papers
Idea Classification 
and Reasoning
..
Input Idea
This idea is not novel 
because…
This idea is novel 
because…
This idea is not novel 
because…

<!-- page 81 -->
10 Most Relevant Papers
(Title, and Abstract)
Research Idea
Novelty Reasoning

<!-- page 82 -->

