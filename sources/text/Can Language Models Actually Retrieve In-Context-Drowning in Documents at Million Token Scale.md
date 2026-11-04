<!-- page 1 -->
Can Language Models Actually Retrieve In-Context?
Drowning in Documents at Million Token Scale
Siddharth Gollapudi∗
UC Berkeley
Nilesh Gupta
UT Austin
Prasann Singhal
UC Berkeley
Sewon Min
UC Berkeley
Abstract
Language models (LMs) raise an intriguing alternative to vector-based retrieval:
conditioning on an in-context corpus and directly generating a relevant answer.
However, prior work has largely focused on proprietary systems or the smaller-
scale reranking task, leaving corpus-scale in-context retrieval largely unexplored.
In this work, we present the first systematic study of in-context retrieval on two
scales practical retrievers demand:million-tokencorpora andlength-generalization
far beyond training-time sizes. We first introduce BLOCKSEARCH, a 0.6B LCLM
retriever whose architectural and training modifications improve over prior LM
baselines and length-generalize up to 10× beyond its training regime. Nevertheless,
its retrieval still collapses under more extreme extrapolation. We trace this failure
to anattention dilutioneffect: as the corpus grows, irrelevant documents dominate
the softmax denominator and the normalized mass on the gold document collapses.
Individual attention heads continue to locate the gold document more reliably
than the model decodes it, even at million-token scale, though this signal also
weakens as the corpus grows. Motivated by this analysis, we introducelength-
awareadjustments to the attention softmax anddocument-level sparse attention,
improving retrieval at million-token scale to performance comparable to a same-
backbone dense retriever. On the lexical LIMIT benchmark, these gains also
transfer out of distribution: at a million-token corpus, Recall@1 reaches 13.5%
versus 2.9% for the dense baseline. Together, our results position in-context
retrieval a promising alternative to classical retrieval while emphasizing attention
control under extreme context growth as a new challenge.
1 Introduction
Retrieval—identifying the relevant document(s) in a corpus {D1, . . . , DN } for a query Q—has long
been dominated by vector-based methods [1]. Recent advances in language modeling (LMs) suggest a
more radical alternative: casting retrieval asconditionalgeneration, where the model directly decodes
the identifier of the relevant document from the corpus in-context [ 2]. Suchin-context retrieval
(ICR) could collapse retrieval and generation into a single model, replacing the two-stage retrieval-
augmented generation pipeline [3] and enabling complex retrieval behavior beyond inner-product
similarity [4]. In other words, rather than relying on external harnesses (retrievers), the model itself
decides which parts of its context are relevant to the task at hand. However, this possibility remains
largely untested at realistic scale: prior work either relies on proprietary systems without controlled
evaluation [2] or studies reranking over small candidate sets [ 5, 6], rather than true corpus-scale
retrieval. As a result, it remains unclear whether LMs can reliably retrieve relevant documents from
large in-context corpora [7, 6, 8].
ICR differs fundamentally from standard long-context modeling. Rather than processing a single
coherent sequence, it operates over large collections of independent documents, creating both
∗Correspondence tosgollapu@berkeley.edu.
Preprint.
arXiv:2607.01538v2  [cs.CL]  3 Oct 2026

<!-- page 2 -->
opportunities and challenges. On one hand, document-level independence naturally enables parallel
encoding and caching. On the other hand, effective retrieval requires two capabilities that current
LMs struggle with:(C1)scaling to corpora containing millions of tokens, and(C2)generalizing
to corpus sizes far beyond those seen during training. Both are difficult in practice: million-token
attention remains computationally expensive, while extrapolation to substantially longer contexts is
known to be brittle in modern LMs [7, 9, 10].
To this end, we present the first systematic study of whether an LM can act as a corpus-scale
retriever under these conditions. We first introduce BLOCKSEARCH(§3), a 0.6B-parameter LM
retriever that builds on prior ICR architectures using block-sparse attention [5]. For scale and length
generalization, it adds randomized per-document identifier codes, in-batch negative training, and an
on-policy auxiliary loss that trains on the model’s own rolled-out digit prefixes. We then compare
BLOCKSEARCHagainst dense retrieval, the standard baseline any practical ICR system must match if
it is to subsume the retrieval stage. BLOCKSEARCHmatches a dense retriever at smaller corpus sizes
(95.8% vs. 95.5% Recall@1 on MS MARCO at ∼45k tokens), and maintains non-trivial accuracy
beyond the LM baseline, generalizing up to10×beyond its training context.
Despite these improvements, BLOCKSEARCHstill collapses at large scale: recall approaches zero
near million-token contexts, remaining far below even a simple dense retrieval baseline. We trace
this failure to anattention dilutioneffect, a degradation that has also been observed in other
settings [9, 11, 12]. Leveraging the natural alignment between queries and their gold documents,
we find that the aggregate contribution of irrelevant documents to the softmax denominator grows
with corpus size and drives the normalized attention mass on the gold document toward zero (§4).
Individual heads still rank the gold document first more often than the model decodes it at every
corpus size we test, up toN=10,000, but this per-head signal also degrades withN.
Motivated by this analysis, we consider two families of techniques to mitigate attention dispersion
at extreme context lengths (§5). First,length-aware softmaxadjustments change how scores are
normalized as the corpus grows; scaling pre-softmax scores withlogN (SSMax) is effective, whereas
an additive length-aware sink barely helps. Second,document-level sparse attentionreduces the
number of documents participating in attention at intermediate layers [13, 14, 10, 15, 16]. Together,
these methods substantially mitigate the effects of attention dilution, improving Recall@1 at million-
token context from as little as 0.2% to 20.0%, a near 100× improvement that recovers most of the
gap to the Qwen3-dense gold standard (e.g. 18.8 vs. 20.2 on MS MARCO and 78.5 vs. 79.5 on
HotpotQA at N=10k; table 2). On LIMIT, which requires a notion of relevance that fixed embeddings
struggle to express, our modifications enable BLOCKSEARCHto substantially outperform dense
retrieval at a million-token corpus (13.5%vs.2.9%Recall@1; §6).
In summary, our contributions are:
• BLOCKSEARCH(§3). We introduce an in-context retriever that matches a same-backbone dense
retriever on small corpora (95.8 vs. 95.5 Recall@1 on MS MARCO) and generalizes to corpora
10×larger than those seen in training, but still collapses near a million tokens.
• Diagnosis(§4). We trace this collapse to attention dilution. At L19, the gold document’s share
of the attention output falls from 0.91 to 0.01 as the corpus grows, while the output’s overall
magnitude barely changes. Individual heads still find the gold document more often than the
model decodes it, although this signal also weakens with N. We see the same pattern on a second
backbone.
• Modifications(§5). Length-aware softmax scaling and document-level routing raise million-
token Recall@1 on MS MARCO from0.2to20.0, close to the dense baseline’s20.2.
• Out-of-distribution retrieval(§6). On LIMIT, the same modifications outperform dense retrieval
at a million-token corpus (13.5vs.2.9Recall@1).
Together, our results establish corpus-scale in-context retrieval as a viable alternative to dense retrieval
under both scale and length extrapolation. More broadly, they identify attention dilution as the primary
bottleneck at million-token scale: while simple modifications can substantially mitigate its effects, it
remains a fundamental challenge for scalable in-context retrieval.
2

<!-- page 3 -->
2 Related Work
In-context and generative retrieval.Most long-context evaluation work focuses on synthetic
retrieval-style tasks such as Needle-in-a-Haystack and RULER [17, 7, 8], potentially overstating real-
world retrieval capability. The premise that an LM can subsume dense retrieval is first articulated by
[2], primarily evaluating proprietary Gemini systems. Subsequent work studies LMs as rerankers over
small candidate pools using block-sparse attention and relevance heads in intermediate Transformer
layers [6, 5]. In contrast, we study LMs as corpus-scale retrievers, training with small contexts and
evaluating up to10 4 documents (∼1M tokens) in an effort to elicit length-generalization.
Generative retrieval [18, 19, 20] also decodes with identifiers, but stores corpus information in model
parameters, requiring retraining when the corpus changes. In contrast, ICR encodes the corpus
explicitly in context, allowing corpus updates without retraining.
Sparse and routed attention.A large body of work makes long-context attention tractable by
routing or sparsification; our document-level sparse attention proposed in §4 builds on this line of
work. Prior approaches reduce attention cost through inference-time pruning [21, 22], block-sparse
kernels [16], learned block routing [13, 14], or hierarchical sparse attention [10, 23]. Our work is
grounded in this literature, but the retrieval setting introduces unique opportunities and challenges.
The most directly comparable work is concurrent: MSA-4B [15], which, like BLOCKSEARCH, learns
to perform generative document citation from an in-context corpus. However, the two works focus on
different questions: MSA primarily scales the retrieval recipe through larger models and extensive
training, whereas our work studies the fundamental failure modes of ICR as corpus size grows. We
report MSA-4B as an external reference point rather than a decisive baseline; our primary comparison
throughout is a same-backbone dense retriever trained on the same data (§5).
Attention sinks and softmax dilution.Streaming-LLM [ 24] introduces explicit attention sinks for
stable long-context decoding, and the gpt-oss model card [25] documents a null-attention mechanism
that absorbs unused softmax mass. Whereas these works use sinks for streaming stability, we apply
them to mitigate softmax dilution under large N. A number of results show that as the number of
attended tokens grows, the softmax distribution flattens, removing attention peaks [9, 11, 26]; this
loss of sensitivity has been tied to representational collapse in longer contexts [ 12, 27]. We show
that the primary cause of retrieval degradation with growing context is softmax dilution, and that
softmax-adjusting mechanisms such as sinks may hold the key to mitigating its effects.
3 BLOCKSEARCH: Model and Million-Token Evaluation
We first investigate several training-time improvements to the standard long-context retrieval recipe.
After reviewing the problem setup (§3.1), we describe the changes that constitute BLOCKSEARCH
(§3.2), our evaluation setup (§3.3), and the results (§3.4). These results motivate the later analysis of
possible failure modes (§4) and promising lines for even further improvements (§5).
3.1 Setup
Given a corpus of N documents and a query, the model must generate the identifier of the document
that best answers the query. The corpus is tokenized with at most Tdoc=300 tokens per document
and prefilled into the KV cache; the query is appended, and the model autoregressively decodes a
four-digit code in{0, . . . ,9999}that maps back to one document (that’s hopefully relevant).
This concretizes challenges C1 and C2 from §1: just 10,000 documents at ∼100 tokens each well
exceeds the 32K-token native context of the Qwen3-0.6B backbone, and the model must generalize
to corpora substantially larger than those seen during training: again, a requirement that distinguishes
retrievers from rerankers and has been largely overlooked in prior LM-retrieval work.
3.2 Method: BLOCKSEARCH
We now describe BLOCKSEARCH: whenever possible, we follow prior ICR work, but our require-
ments C1 and C2 expose several limitations that motivate our proposed improvements.
Prompt format.Prior in-context work assigns each document a sequential integer identifier from 1
to N [5, 2]. In our regime, training-time IDs are a strict subset of inference IDs and risk overfitting
3

<!-- page 4 -->
to absolute position. We instead insert each document as <bos>Doc {code}: {text} (Doc
{code})<eos>, with {code} drawn uniformly at random per training step, breaking any association
between code, semantics, or position. We also drop the query prefix from prior work [5, 2]: while it
improves performance, it prevents corpus reuse across queries, which is cost-prohibitive at our scale.
For a full example of a corpus/query prompt, we refer the reader to §A.
Block-sparse attention.Causal prefill scales quadratically in tokens, which is prohibitive at our
target N. Since documents are disjoint, we use a block-sparse mask [ 5]: document tokens attend
causally only within their own block, and the query block attends over the full corpus and causally to
itself. Following common practice [28, 5], we reset RoPE [29] positions at each document start and
shift the query to position 300. The mask is materialized viaflex_attention[30].
Training data.We train on the ReLabeled Hard Negatives (RLHN) version of BEIR [ 31],
which uses an LLM judge to prune false negatives from mined hard negatives in datasets such
as MS MARCO [32]. Per query we keep one pruned positive and 15 hard negatives; per-query
relevance scores for the auxiliary loss are from Qwen3-Embedding-8B [ 33]. The training corpus
totals ∼100M tokens; full mix and cleaning details are in §C. We ablate the RLHN filtering and
report how often documents are truncated in §P.
Training regime.Inspired by in-batch contrastive training [ 1, 34], we adapt in-batch negatives to
this setting. For a batch of b (query, 16-document) tuples (1 positive + 15 hard negatives each), we
prefill all b×16 documents once and score every query against the shared corpus, converting one
prefill intobtraining signals. Every model is trained with 256 documents in its corpus, i.e.b=16.
Training objective.We train with teacher forcing on the gold code, but this alon causes an exposure
bias issue: at inference, each digit conditions on the model’s own potentially incorrect prefix, which
lies off the training distribution. We therefore add an on-policy auxiliary loss. The model first rolls
out a four-digit code from its own distribution with gradients disabled. For each digit position, we
construct a teacher distribution from in-batch document scores, restricted to candidates whose prefix
matches the rollout. We then replay the rollout with gradients enabled at the four answer positions
and average the resulting cross-entropy losses. The total loss is L=L CE +λL aux with λ ramped in
after a warmup; the full algorithm can be found in algorithm 1 (§F).
3.3 Evaluation
The model is judged by whether it can recover the relevant document from those placed in context;
our metric is Recall@1 over the generated four-digit codes, decoded by a beam search over the digit
sequence. We also evaluate Recall@5 using beam search over the top five predictions and observe
trends consistent with Recall@1; see §K for details.
Evaluation data.We evaluate on three BEIR datasets [ 35]: MS MARCO (dev), HotpotQA (test),
and NQ (test). For each dataset, we independently sample 400 queries without replacement from
the its split. For each query, we take its gold document and 24 hard negatives (retrieved using
Qwen3-Embedding-8B [36]); by taking a union of these documents across all 400 queries, we get a
10000 document corpus. In contrast with prior work [2], the substantial use of hard negatives makes
the input corpus far more challenging. 2
To evaluate across varying corpus sizes (e.g. N=500 to N=10,000), we also construct smaller
versions of each dataset. We first include every query’s gold document (400 documents), then fill out
the rest of the dataset with documents randomly selected from the full 10,000 document corpus.
Baselines.We compare against two reference retrievers and two ablations of BLOCKSEARCHitself:
• BLOCKSEARCH-position: sequential codes ( 0, . . . ,9999by document position) to isolate the
contribution of random codes, and no auxiliary loss; this corresponds to the prior ICR recipe.
• BLOCKSEARCH-offpolicy: BLOCKSEARCHwith the on-policy auxiliary loss removed (teacher-
forced CE only); isolates the exposure-bias fix.
•Qwen3-dense (0.6B) : a dense retriever trained on the same RLHN data [31] with a contrastive
objective [1] from the same Qwen3-0.6B backbone (§E); our primary reference point and the
dense-retrieval gold standard BLOCKSEARCHmust clear to be practical.
2For NQ, we use fewer hard negatives per query due to longer documents; per-dataset sizes are in §B (table 4).
4

<!-- page 5 -->
58k 116k 290k 580k 1.0M
0
50
100
Approx. prefill size (tokens)
Recall@1 (%)
Natural Questions
45k 90k 225k 450k 900k
0
50
100
Approx. prefill size (tokens)
MS MARCO
40k 80k 200k 400k 800k
0
50
100
Approx. prefill size (tokens)
HotpotQA
Qwen3-dense-0.6B MSA-4B M-position M-offpolicy M(full)
Figure 1: Recall@1 vs. approximate prefill size (N× mean doc length; see §B) on NQ, MS MARCO,
and HotpotQA. Solid: ICR variants (BLOCKSEARCH, BLOCKSEARCH-position, BLOCKSEARCH-
offpolicy); dashed: baselines (Qwen3-dense, MSA-4B). Vertical dotted line marks the Qwen3-0.6B
native context limit (∼32k tokens).
• MSA-4B[ 15]: a concurrent multi-million-token LM, ∼7× larger and trained with a much larger
long-context budget, sidestepping the C2 generalization requirement; an external reference point
rather than a decisive baseline.
3.4 Results: BLOCKSEARCHis competitive, but collapses asNscales
We train Qwen3-0.6B into BLOCKSEARCH(and variants) on 8× NVIDIA A100s using the above
changes; full hyperparameters are in §D. The performance of the models is demonstrated in fig. 1.
BLOCKSEARCHimproves extrapolation in LMs, up to ~500,000 tokens.All LMs perform
strongly at small N (>95% on MS MARCO at N=1,000), but baselines degrade much faster. The
position-coded variant, which is the prior ICR method, collapses to near-zero by N=5,000 on every
dataset. BLOCKSEARCH-offpolicy trails BLOCKSEARCH(MS MARCO 15.0 vs. 18.8 at N=5,000;
HotpotQA 6.2 vs. 13.0), showing that random codes and the on-policy loss contribute distinct gains.
Note that, while BLOCKSEARCHsubstantially improves extrapolation, all variants eventually collapse
beyond roughly500,000tokens, corresponding to about10×the training context length.
BLOCKSEARCHvs. MSA-4B.Despite having ∼7× fewer parameters than MSA [ 15],
BLOCKSEARCHmatches MSA at N=500,1000 and 2500, e.g., on MS MARCO, achieving
95.8%,75.2%,43.8% vs. 93.8%,70.2%,42.2% for MSA. At large corpus sizes, MSA-4B pulls
ahead (27.5% vs. 18.8% at N=5,000, 16.0% vs. 0.2% at N=10,000), which is expected given that
MSA is explicitly trained for long-context tasks, whereas these settings require BLOCKSEARCHto
generalize to corpora20–40×larger than those seen during training.
Despite near-perfect long-context performance on synthetic evaluation such as RULER’s needle-
in-a-haystack (NIAH) [17] as reported in the original paper [ 15], MSA degrades sharply on real
retrieval tasks: substantially more than the dense retrieval baseline. This suggests that realistic
retrieval settings are significantly more challenging than existing synthetic long-context benchmarks,
highlighting the need for the long-context literature to adopt more semantically meaningful retrieval
tasks in evaluation.
BLOCKSEARCHvs. dense retrieval.Dense retrieval also degrades with N but without the sharp
LM collapse: BLOCKSEARCHmatches the Qwen3-dense gold standard at small and mid N but
trails it at large N (MS MARCO 18.8 vs. 38.5 at N=5,000; near-zero vs. 20.2 at N=10,000), with
similar trends on NQ and HotpotQA. Closing this large- N gap remains the central challenge for
practical in-context retrieval and motivates the mechanistic analysis in §4.
5

<!-- page 6 -->
4 Understanding the Large-NDeterioration
§3 shows that BLOCKSEARCHgeneralizes well past its training-time context length, but still collapses
at N=10,000. In this section, we posit that this collapse can be decomposed into two parts: a per-
head, per-layer measure ofattention recall(does the relevant document receive the highest attention
score?) degrades more slowly thangeneration recall(does the model decode the correct identifier?),
staying ahead of it all the way to N=10,000, though it also degrades with N. We also find that the
share of each attention layer’s output that comes from gold tokens collapses while the layer’s overall
output magnitude is preserved, cleanly encapsulating the aformentioned attention dilution issue.
4.1 Setup
Decoder language models are not a homogeneous stack: layers and heads take on specific functional
roles, with FFNs promoting concepts [ 37, 38], induction heads carrying in-context learning [ 39],
and a sparse subset of retrieval heads carrying the long-context retrieval signal [40]. For in-context
retrieval specifically, BlockRank [5], ICR2 [6], and QRHeads [41] build on those results, observing
that per-head attention scores can serve directly as a relevance signal. This observation is the starting
point for the measurements we report.
Preliminary.We write L∈ {0, . . . ,27}for layer index, and h∈ {1, . . . , H=16}for attention-
head index. We probe BLOCKSEARCHat the final token of the query block, immediately before
the first generated code digit (which we denote d1). At this position let qhL ∈R dhead be the post-
RoPE query vector and khL,t, vhL,t the key and value at prefill position t, where dhead is the per-head
dimension. The pre- and post-softmax attention scores assigned to positiontare:
shL,t = qhL ·k hL,t√dhead , α hL,t = exp(shL,t)Pt′ exp(shL,t′) ,(1)
and the layer’s attention output is
aL =

u1L;u 2L;. . .;uHL  W OL , u hL = X
t
αhL,t vhL,t,(2)
where uhL ∈R dhead is the per-head attention readout, [·;·] denotes concatenation along the head
dimension into a vector inRH·dhead, and W OL ∈R (H·dhead)×dmodel is the layer’s learned output projection.
Metrics.For each query, partition the prefill tokens into thegoldset G (the tokens of the gold
document) and its complement ¯G. We use three measurements throughout this section:AttnRank,
GoldShare, andfirst-digit accuracy.
AttnRankmeasures whether attention identifies the right document. More precisely, for each document
d in the prefill, we collapse its tokens to a single per-head score using the MaxSim operator from
late-interaction retrieval [42]:
MaxSimhL(d) = maxt∈d shL,t.(3)
Writing d⋆ for the gold document, the per-head Recall@1 at layer L is R(h)L , the fraction of queries
for whicharg max d MaxSimhL(d) =d ⋆. We report two cross-head aggregators ofR (h)L :
•R sumL —sum-across-heads: rank documents by Ph MaxSimhL(d) and check whether thetop-ranked document isd ⋆.
•R anyL = fraction of queries for which at least one head ranks d⋆ strictly first, i.e.
MaxSimhL(d⋆)>MaxSim hL(d)for everyd̸=d ⋆.
GoldSharemeasures gold’s contribution to the layer’s attention output (before the residual add). By
linearity of eq. (2) in the per-head readoutsu hL, we decomposea L into a gold and a non-gold piece:
aL =a GL +a ¯GL, a GL =  u1,GL ;. . .;uH,GL  W OL , u h,GL = X
t∈G
αhL,t vhL,t,(4)
and report the gold-driven fraction∥a GL∥/∥aL∥alongside the total magnitude∥a L∥.
6

<!-- page 7 -->
First-digit accuracyprobes how decisively the model has committed to the first code digit at a given
layer, via an LM-head probe [43]: we project the layer-L output through the model’s final RMSNorm
and lm_head and record the maximum probability assigned to any of the ten digit tokens at the d1
position. We treat this as a coarse indicator of when the digit decision emerges, not as a calibrated
probability at intermediate layers.
4.2 Layer Roles and the Recall–Generation Gap
Figure 2 reportsR sumL and first-digit accuracy on BLOCKSEARCHat thed 1-emission position in the
in-domain, small-N regime (N=500). Two qualitatively distinct transitions emerge. First, RsumL rises
across L11–L20: the model accumulates relevance information over many layers, consistent with
prior reports of middle-layer retrieval in decoder LMs [ 5, 6, 41, 40]. We refer to this contiguous
range as theretrieval band. Second, first-digit accuracy rises sharply at L18→L19, after which the
model has effectively committed tod 1; we refer toL19onwards as thedecode band.
0 3 6 9 12 15 18 21 24 27
0
0.25
0.5
0.75
1
L18→L19
LayerL
recall / accuracy RsumL
first-digit accuracy
Figure 2: Per-layer RsumL and LM-head first-digit accuracy on BLOCKSEARCH, MS MARCO, N=500,
400queries. Retrieval signal emerges acrossL11–L20; first-digit signal atL18→L19.
Heads no longer agree on the gold document.Sweeping N∈ {500,1000,2500,5000,10000}
on MS MARCO (fig. 3), we see these behaviors degrade. The retrieval band erodes under the
sum aggregator: Rsum19 drops from 0.98 at N=500 to 0.00 at N=10,000, matching the collapse in
generation recall reported in §3.4. RanyL degrades more slowly: Rany19 falls from 0.98 at N=500 to
0.51 at N=2,500 and 0.33 at N=5,000, where Rsum19 is already down to 0.06. Over the intermediate
range, individual heads still rank the gold document first for a sizable fraction of queries even as the
agreementbetween heads breaks down. By N=10,000, however, per-head signal is also largely gone
(Rany19 =0.08; the best layer,L11, reaches0.14).
0 4 8 12 16 20 24
0
0.25
0.5
0.75
1
LayerL
RsumL
(a)R sumL vsL
0 4 8 12 16 20 24
0
0.25
0.5
0.75
1
LayerL
RanyL
(b)R anyL vsL
N=500 N=1k N=2.5k N=5k N=10k
Figure 3: Per-layer recall vs. L across N∈ {500,1000,2500,5000,10000} on BLOCKSEARCH,
MS MARCO, 400 queries.(a) RsumL drops monotonically as N grows, reaching ≈0 across all layers
atN=10k.(b)R anyL decays more slowly thanR sumL at intermediateN
7

<!-- page 8 -->
Normalization breaks the final attention distribution.The gap between RanyL and RsumL might
suggest the per-head signal can be recovered by a better aggregator. But what the rest of the model
sees is not a per-head ranking; it is the layer’s attention output aL, into which gold’s value vectors
enter in proportion to their post-softmax mass αhL,t, not the per-head ranking of gold over other
documents. So even where some head still ranks gold first, the relevant question is what aL contains.
Table 1 reports ∥a19∥ andGoldShareacross the N sweep. The total magnitude ∥a19∥ shrinks by only
∼36% from N=500 to N=10k — the layer keeps writing into the residual at roughly its original
amplitude.GoldShare, however, drops from 0.91 to 0.01, a factor of about 130. The L19 attention
output is rewritten from a gold-token average to a non-gold-token average of comparable size; by the
time the LM head reads the residual at L21, the slot that carried gold-derived information at small
N now carries an aggregate of distractors. Additional per-head softmax statistics behind this swap
(gold’s pre-softmax score eroding while the non-gold log-sum-exp grows) are reported in §G.
Table 1: Attention-output decomposition a19 =a G19 +a ¯G19 on BLOCKSEARCH, MS MARCO, 100
queries; norms are medians over queries and the share is the median of per-query ratios. Total
magnitude shrinks only∼36%, but the gold-driven share drops from0.91to0.01.
N∥a G19∥ ∥a ¯G19∥ ∥a 19∥ ∥a G19∥/∥a19∥
500 43.03 17.47 47.48 0.91
1k 30.99 21.11 45.36 0.74
2.5k 7.64 33.64 43.03 0.19
5k 2.10 34.61 36.90 0.06
10k 0.21 29.88 30.27 0.01
Conclusion: softmax attention dispersion as N grows.The vector-level result of table 1 is driven
by a single mechanism inside each head. As N grows, gold’s largest pre-softmax score shL,t⋆ (with
t⋆ = arg maxt∈G shL,t) no longer dominates over the larger pool of competing distractor scores, so
the post-softmax weight assigned to gold’s value vector shrinks and the per-head readoutuhL becomes
a non-gold average at comparable magnitude. This length-driven softmax dispersion is a generic
phenomenon [9, 11, 12] and an empirical driver of length-generalization failure across tasks [44, 45];
the contribution here is connecting it to a vector-level swap at the residual stream rather than treating
it as an abstract probability-mass collapse. §5 then evaluates two avenues of improvement that target
this mechanism.
Beyond Qwen3 and BLOCKSEARCH.The collapse is not specific to our backbone or training.
An off-the-shelf proprietary long-context LM, Gemini-3-flash, evaluated on the same MS MARCO
setup with no task training, falls from 95.0 to 16.2 Recall@1 between N=500 and N=10,000. A
BLOCKSEARCHtrained on SmolLM2-360M [ 46] collapses earlier, and repeating the analyses of this
section on it reproduces the same picture: a retrieval band followed by a decode band (shifted deeper,
to L17–L23 and L24 onward), RsumL falling to zero by N=10,000, and the gold-driven share of the
decode-onset layer’s output falling from0.64to0.00while its magnitude stays comparable (§N).
5 Addressing the Attention Dilution Problem
Having identified softmax dispersion under growing N as the guilty party, we study two potential
directions that address it. We first consider two length-aware modifications to attention softmax that
mitigate the dispersion issue. We also considerdocument-level sparse attention, thereby pruning the
set of tokens that enter the softmax.
5.1 Method
Length-aware softmax.We first describe two methods that change how softmax converts the
pre-softmax scores shL,t to attention weights. Both arelength-aware: each carries a corpus-size signal
that lets the softmax adapt to the large N setting. Anadditive sinkappends a learned constant to
the softmax denominator, so a head whose largest scores fall below that constant leaks probability
mass into the appended slot and emits a small attention output [24, 25]; the per-token weights ˜αhL,t
no longer sum to one. The length-awareness is implicit: training under a wide range of effective
8

<!-- page 9 -->
Table 2: Recall@1 (×100) vs. corpus size N (400 queries). SSMax, top-B=256 routing at L16, and
their combination are close to Qwen3-dense; MSA-4B is an external reference. NQ caps at N=8,607.
Natural Questions MS MARCO HotpotQA
N0.5k 1k 2.5k 5k 8.6k 0.5k 1k 2.5k 5k 10k 0.5k 1k 2.5k 5k 10k
BLOCKSEARCHattn.,R any19 100.0 100.0 96.2 100.0 97.0 100.0 100.0 99.8 100.0 100.0 100.0 100.0 99.2 99.8 100.0
Qwen3-dense95.5 86.5 62.9 51.4 39.6 95.5 75.2 52.8 38.5 20.2 99.0 97.5 92.2 87.5 79.5
MSA-4B 59.7 51.6 36.3 26.8 18.6 93.8 70.2 42.2 27.5 16.0 97.0 96.8 90.8 84.0 75.5
BLOCKSEARCH92.2 77.7 43.9 4.8 0.2 95.8 75.2 43.8 18.8 0.2 97.0 95.2 64.2 13.0 0.5
- sink 91.2 76.2 45.6 10.3 1.5 96.5 75.2 45.2 21.2 2.5 95.0 93.2 58.0 14.5 1.0
- SSMax 90.5 79.5 58.1 42.6 30.3 95.5 74.5 49.8 33.8 16.5 96.5 95.2 85.8 73.5 56.8
- routing 93.2 82.7 63.2 48.1 34.6 96.0 74.5 50.7 38.2 18.8 98.2 98.2 91.8 86.5 78.5
- SSMax+routing 91.5 81.4 61.4 46.1 34.3 95.5 75.0 50.0 38.2 20.5 97.5 95.8 90.8 84.8 72.5
corpus sizes Neff ∼LogUniform(128,5000) ) lets the learned scalar absorb a length signal, so the
gate fires more often at large N where attention is diffuse.Multiplicative score rescalingkeeps
a proper softmax but sharpens it, and is length-aware by construction: SSMax [ 9] multiplies the
pre-softmax scores by s·logN (for a tuned scaling parameter s) so that the gap between the largest
score and the bulk grows directly withN.
Following GPT-OSS [25] we instantiate the sink with a learned scalarb L ∈Rper attention layer:
˜αhL,t = exp(shL,t)P
t′ exp(shL,t′) + exp(bL) .(5)
The appended slot has no value vector, so Pt ˜αhL,t ≤1 and a layer with diffuse attention writes asmaller residual update (gate-form derivation in §I). We refer to this model as BLOCKSEARCH-sink.
We also produce BLOCKSEARCH-SSMax following [ 9] with s initialized to 0.43 at every attention
layer. Both models compose with the block-sparse attention pattern and work with the changes in §3.
Document-level sparse attention.On the flip side, we also consider scoring documents and
keeping a top- B shortlist before the code generation is performed; this is a popular approach in
long-context research that prunes the context down [15, 13, 16, 21, 22, 23]. We perform a doc-level
routing step at L16, before the retrieval band (§4.2). A forward pass through L0–L15 produces a
per-document score Rsum16 (d) from §4.2; only the top B=256 documents participate in dense attention
at L17 onward. We call this BLOCKSEARCH-routing, picking doc-level over token-level as each
document is a coherent semantic unit. §J has more information on the choice ofB.
5.2 Results
The additive sink barely moves the large-N collapse.BLOCKSEARCH-sink yields only modest
mid-N gains and a small lift at MS MARCON=10k (0.2→2.5 , from a near-floor base); its absolute
level stays low across all three datasets and tracks the no-modification curve at largeN. A learned
constant cannot restore the gold token’s post-softmax weight once the softmax denominator has grown
by orders of magnitude: it shifts the denominator uniformly and cannot rescale itsN-dependence.
SSMax holds up across the full N sweep.SSMax closes most of the gap to Qwen3-dense on
every dataset (e.g. 17.8 vs. 20.2 on MS MARCO at N=10k, where the sink reaches only 2.5).
Multiplying the scores by slogN makes the gold document’s advantage grow with N: if gold scores
∆ above a typical distractor, its attention weight is roughly 1/(1 +N 1−s∆), which stays bounded as
long as s∆>1 . The fix is only partial, though. At N=10k, gold still receives just 0.019 of the L19
attention mass, up from0.0018without SSMax (§G).
Top-B routing matches the dense baseline at largeN.Routing applied to vanilla BLOCKSEARCH
reaches 18.8 at MS MARCO N=10k, within 1.4 points of the dense baseline, and 78.5 on HotpotQA
(vs. 79.5). Routing does add a shortlisting step, but unlike a retrieve-then-read pipeline, the shortlist
is computed from the model’s own L16 attention scores in the same forward pass, without a separate
encoder, index, or fixed document representation. We include it mainly as a test of the diagnosis in
§4, since SSMax recovers most of the same gap without any shortlist.
SSMax plus routing?Combining the two gives the best result on MS MARCO at N=10k (20.0,
vs. 20.2 for the dense baseline), matches routing alone on NQ, and is worse than routing on HotpotQA
(74.5vs.78.5). A gap toQwen3-denseremains on all three datasets at the largestN.
9

<!-- page 10 -->
6 Out-of-Distribution Generalization: LIMIT
§3–§5 focus on widely studied benchmarks that dense retrieval has been heavily optimized for.
BLOCKSEARCH, with the proposed modifications, matches dense retrieval there: a notable milestone,
since these benchmarks largely define the strengths of dense retrieval. A key question remains:can
in-context retrieval outperform dense retrieval, not just match it?We evaluate BLOCKSEARCHon
LIMIT [4], a benchmark using a lexical notion of similarity, where dense retrieval struggles. Under
an out-of-distribution setup, BLOCKSEARCHsubstantially outperforms dense retrieval. 3
Evaluation setup.In LIMIT, every query has two gold documents drawn from a corpus of 50,000
short biographies. We scale the corpus from N=46 (the gold documents only, “LIMIT-small”) up
to N=10,000 (the limit of the four-digit code vocabulary) by adding distractor biographies, which
grows the prefill from ∼8k to ∼1.7M tokens while each query keeps its two golds. We evaluate the
four BLOCKSEARCHvariants of §5 against a same-backbone pooled dense retriever (table 3) with
n=1,000queries, counting a query as correct if any gold is in the topk; true Recall@kis in §L.1.
Table 3: LIMIT length generalization: Recall@1 (multi-gold, n=1,000) as the corpus grows from
N=46toN=10,000by adding distractor biographies (∼8k to∼1.7M tokens).
Method Scoring46 500 1000 2500 5000 10000
BLOCKSEARCHICR beam0.354 0.094 0.022 0.000 0.000 0.001
-sink ICR beam0.252 0.051 0.018 0.001 0.000 0.000
-SSMax ICR beam0.501 0.271 0.196 0.101 0.074 0.013
-SSMax+routing ICR beam0.501 0.305 0.281 0.262 0.202 0.135
Qwen3-densepooled cosine0.176 0.080 0.061 0.047 0.035 0.029
Random chance —0.043 0.004 0.002 0.001 0.000 0.000
Routing.BLOCKSEARCH-SSMax-routing performs best, reaching 0.202 Recall@1 at N=5,000
and 0.135 at N=10,000, while BLOCKSEARCHand BLOCKSEARCH-sink drop to zero. SSMax
alone helps at intermediate sizes but falls to 0.013 at N=10,000. The sink does not help on this
benchmark: BLOCKSEARCH-sink is below BLOCKSEARCHat every N (e.g. 0.252 vs. 0.354 at
N=46), whereas on MS MARCO it was roughly neutral. BLOCKSEARCH-SSMax-routing also beats
Qwen3-dense at every N (0.135 vs. 0.029 at N=10,000), which suggests that our modifications
generalize better out of distribution and may extend to tasks beyond standard semantic search.
Caveats.Routingdelaysbut does notpreventthe inevitable: BLOCKSEARCH-SSMax-routing is
still declining with N (0.135 at ∼1.7M tokens). Thus, these modifications extend functional LIMIT
retrieval to larger corpora, rather than solving it, which remains an open problem.
7 Conclusion
In this work, we presented the first systematic study of corpus-scale in-context retrieval with long-
context language models, focusing on two requirements of practical retrieval systems: scaling to
million-token corpora and generalizing to corpus sizes far beyond those seen during training. We
showed that, with appropriate training and architectural modifications, LMs can retrieve well beyond
their training regime and approach dense retrieval at moderate scales. At the same time, we identified
attention dilution as a fundamental scaling bottleneck: as the corpus grows, the normalized attention
mass on the gold document collapses, even though individual heads still locate it more often than
the model decodes it, a pattern we observe on two backbones. Motivated by this analysis, we
introduced length-aware softmax scaling and document-level sparse attention, which substantially
improve retrieval at million-token scale. These results come with limitations: keeping the corpus
in a KV cache requires roughly three orders of magnitude more memory than a dense index (§Q),
retrieval-only training reduces the backbone’s general capability (§O), and our evidence comes from
two small backbones evaluated on a single sample of queries per corpus size. Together, our results
suggest that scalable in-context retrieval is promising yet constrained by attention dilution, motivating
new directions for retrieval architectures and long-context modeling.
3For additional out-of-distribution results, we also provide figures for the OBLIQ evaluation [47] in §M.
10

<!-- page 11 -->
Acknowledgment
This research was supported by the NVIDIA Academic Grant Program. Siddharth Gollapudi is
supported by the NSF (CSGrad4US award no. 2313998).
References
[1] Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov,
Danqi Chen, and Wen-tau Yih. Dense passage retrieval for open-domain question answering.
InProceedings of the 2020 conference on empirical methods in natural language processing
(EMNLP), pages 6769–6781, 2020.
[2] Jinhyuk Lee, Anthony Chen, Zhuyun Dai, Dheeru Dua, Devendra Singh Sachan, Michael Bo-
ratko, Yi Luan, Sébastien MR Arnold, Vincent Perot, Siddharth Dalmia, et al. Can long-context
language models subsume retrieval, rag, sql, and more?arXiv preprint arXiv:2406.13121,
2024.
[3] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman
Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, et al. Retrieval-augmented
generation for knowledge-intensive nlp tasks.Advances in neural information processing
systems, 33:9459–9474, 2020.
[4] Orion Weller, Michael Boratko, Iftekhar Naim, and Jinhyuk Lee. On the theoretical limitations
of embedding-based retrieval.arXiv preprint arXiv:2508.21038, 2025.
[5] Nilesh Gupta, Chong You, Srinadh Bhojanapalli, Sanjiv Kumar, Inderjit Dhillon, and Felix Yu.
Scalable in-context ranking with generative models.arXiv preprint arXiv:2510.05396, 2025.
[6] Yifu Qiu, Varun R Embar, Yizhe Zhang, Navdeep Jaitly, Shay B Cohen, and Benjamin Han.
Eliciting in-context retrieval and reasoning for long-context large language models. InFindings
of the Association for Computational Linguistics: ACL 2025, pages 3176–3192, 2025.
[7] Yushi Bai, Shangqing Tu, Jiajie Zhang, Hao Peng, Xiaozhi Wang, Xin Lv, Shulin Cao, Jiazheng
Xu, Lei Hou, Yuxiao Dong, et al. Longbench v2: Towards deeper understanding and reason-
ing on realistic long-context multitasks. InProceedings of the 63rd Annual Meeting of the
Association for Computational Linguistics (Volume 1: Long Papers), pages 3639–3664, 2025.
[8] Kelly Hong, Anton Troynikov, and Jeff Huber. Context rot: How increasing input tokens
impacts llm performance. Technical report, Chroma, July 2025.
[9] Ken M Nakanishi. Scalable-softmax is superior for attention.arXiv preprint arXiv:2501.19399,
2025.
[10] Jiaqi Leng, Xiang Hu, Junxiong Wang, Jianguo Li, Wei Wu, and Yucheng Lu. Understanding
and improving length generalization in hierarchical sparse attention models.arXiv preprint
arXiv:2510.17196, 2025.
[11] Petar Veliˇckovi´c, Christos Perivolaropoulos, Federico Barbero, and Razvan Pascanu. Softmax
is not enough (for sharp size generalisation).arXiv preprint arXiv:2410.01104, 2024.
[12] Federico Barbero, Andrea Banino, Steven Kapturowski, Dharshan Kumaran, João G Araújo,
Alex Vitvitskyi, Razvan Pascanu, and Petar Veliˇckovi´c. Transformers need glasses! informa-
tion over-squashing in language tasks.Advances in Neural Information Processing Systems,
37:98111–98142, 2024.
[13] Enzhe Lu, Zhejun Jiang, Jingyuan Liu, Yulun Du, Tao Jiang, Chao Hong, Shaowei Liu, Weiran
He, Enming Yuan, Yuzhi Wang, et al. Moba: Mixture of block attention for long-context llms.
arXiv preprint arXiv:2502.13189, 2025.
[14] Guangxuan Xiao, Junxian Guo, Kasra Mazaheri, and Song Han. Optimizing mixture of block
attention.arXiv preprint arXiv:2511.11571, 2025.
11

<!-- page 12 -->
[15] Yu Chen, Runkai Chen, Sheng Yi, Xinda Zhao, Xiaohong Li, Jianjin Zhang, Jun Sun, Chuanrui
Hu, Yunyun Han, Lidong Bing, et al. Msa: Memory sparse attention for efficient end-to-end
memory model scaling to 100m tokens.arXiv preprint arXiv:2603.23516, 2026.
[16] Daniel Ohayon, Itay Lamprecht, Itay Hubara, Israel Cohen, Daniel Soudry, and Noam Elata.
Block sparse flash attention.arXiv preprint arXiv:2512.07011, 2025.
[17] Cheng-Ping Hsieh, Simeng Sun, Samuel Kriman, Shantanu Acharya, Dima Rekesh, Fei Jia,
Yang Zhang, and Boris Ginsburg. Ruler: What’s the real context size of your long-context
language models?arXiv preprint arXiv:2404.06654, 2024.
[18] Yi Tay, Vinh Tran, Mostafa Dehghani, Jianmo Ni, Dara Bahri, Harsh Mehta, Zhen Qin, Kai Hui,
Zhe Zhao, Jai Gupta, et al. Transformer memory as a differentiable search index.Advances in
neural information processing systems, 35:21831–21843, 2022.
[19] Yujing Wang, Yingyan Hou, Haonan Wang, Ziming Miao, Shibin Wu, Qi Chen, Yuqing Xia,
Chengmin Chi, Guoshuai Zhao, Zheng Liu, et al. A neural corpus indexer for document retrieval.
Advances in Neural Information Processing Systems, 35:25600–25614, 2022.
[20] Shashank Rajput, Nikhil Mehta, Anima Singh, Raghunandan Hulikal Keshavan, Trung Vu,
Lukasz Heldt, Lichan Hong, Yi Tay, Vinh Tran, Jonah Samost, et al. Recommender systems
with generative retrieval.Advances in Neural Information Processing Systems, 36:10299–10315,
2023.
[21] Jiaming Tang, Yilong Zhao, Kan Zhu, Guangxuan Xiao, Baris Kasikci, and Song Han. Quest:
Query-aware sparsity for efficient long-context llm inference.arXiv preprint arXiv:2406.10774,
2024.
[22] Wei Wu, Zhuoshi Pan, Kun Fu, Chao Wang, Liyi Chen, Yunchu Bai, Tianfu Wang, Zheng
Wang, and Hui Xiong. Tokenselect: Efficient long-context inference and length extrapolation
for llms via dynamic token-level kv cache selection. InProceedings of the 2025 Conference on
Empirical Methods in Natural Language Processing, pages 21275–21292, 2025.
[23] Xiang Hu, Zhihao Teng, Jun Zhao, Wei Wu, and Kewei Tu. Efficient length-generalizable atten-
tion via causal retrieval for long-context language modeling.arXiv preprint arXiv:2410.01651,
2024.
[24] Guangxuan Xiao, Yuandong Tian, Beidi Chen, Song Han, and Mike Lewis. Efficient streaming
language models with attention sinks.arXiv preprint arXiv:2309.17453, 2023.
[25] Sandhini Agarwal, Lama Ahmad, Jason Ai, Sam Altman, Andy Applebaum, Edwin Arbus,
Rahul K Arora, Yu Bai, Bowen Baker, Haiming Bao, et al. gpt-oss-120b & gpt-oss-20b model
card.arXiv preprint arXiv:2508.10925, 2025.
[26] Sai Surya Duvvuri, Nirmal Patel, Nilesh Gupta, and Inderjit S Dhillon. Lucid: Attention with
preconditioned representations.arXiv preprint arXiv:2602.10410, 2026.
[27] Mathew Jacob, Erik Lindgren, Matei Zaharia, Michael Carbin, Omar Khattab, and Andrew
Drozdov. Drowning in documents: consequences of scaling reranker inference.arXiv preprint
arXiv:2411.11767, 2024.
[28] Dongyang Ma, Yan Wang, and Lan Tian. Block-attention for efficient prefilling.arXiv preprint
arXiv:2409.15355, 2024.
[29] Jianlin Su, Murtadha Ahmed, Yu Lu, Shengfeng Pan, Wen Bo, and Yunfeng Liu. Roformer:
Enhanced transformer with rotary position embedding.Neurocomputing, 568:127063, 2024.
[30] Juechu Dong, Boyuan Feng, Driss Guessous, Yanbo Liang, and Horace He. Flex attention: A pro-
gramming model for generating optimized attention kernels.arXiv preprint arXiv:2412.05496,
2(3):4, 2024.
[31] Nandan Thakur, Crystina Zhang, Xueguang Ma, and Jimmy Lin. Hard negatives, hard lessons:
Revisiting training data quality for robust information retrieval with llms.arXiv preprint
arXiv:2505.16967, 2025.
12

<!-- page 13 -->
[32] Payal Bajaj, Daniel Campos, Nick Craswell, Li Deng, Jianfeng Gao, Xiaodong Liu, Rangan
Majumder, Andrew McNamara, Bhaskar Mitra, Tri Nguyen, et al. Ms marco: A human
generated machine reading comprehension dataset.arXiv preprint arXiv:1611.09268, 2016.
[33] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu,
Chang Gao, Chengen Huang, Chenxu Lv, et al. Qwen3 technical report.arXiv preprint
arXiv:2505.09388, 2025.
[34] Yingqi Qu, Yuchen Ding, Jing Liu, Kai Liu, Ruiyang Ren, Wayne Xin Zhao, Daxiang Dong,
Hua Wu, and Haifeng Wang. Rocketqa: An optimized training approach to dense passage
retrieval for open-domain question answering. InProceedings of the 2021 conference of the
North American chapter of the association for computational linguistics: human language
technologies, pages 5835–5847, 2021.
[35] Nandan Thakur, Nils Reimers, Andreas Rücklé, Abhishek Srivastava, and Iryna Gurevych. Beir:
A heterogenous benchmark for zero-shot evaluation of information retrieval models.arXiv
preprint arXiv:2104.08663, 2021.
[36] Yanzhao Zhang, Mingxin Li, Dingkun Long, Xin Zhang, Huan Lin, Baosong Yang, Pengjun
Xie, An Yang, Dayiheng Liu, Junyang Lin, et al. Qwen3 embedding: Advancing text embedding
and reranking through foundation models.arXiv preprint arXiv:2506.05176, 2025.
[37] Mor Geva, Roei Schuster, Jonathan Berant, and Omer Levy. Transformer feed-forward layers
are key-value memories. InProceedings of the 2021 Conference on Empirical Methods in
Natural Language Processing, pages 5484–5495, 2021.
[38] Mor Geva, Avi Caciularu, Kevin Wang, and Yoav Goldberg. Transformer feed-forward layers
build predictions by promoting concepts in the vocabulary space. InProceedings of the 2022
conference on empirical methods in natural language processing, pages 30–45, 2022.
[39] Catherine Olsson, Nelson Elhage, Neel Nanda, Nicholas Joseph, Nova DasSarma, Tom
Henighan, Ben Mann, Amanda Askell, Yuntao Bai, Anna Chen, et al. In-context learning
and induction heads.arXiv preprint arXiv:2209.11895, 2022.
[40] Wenhao Wu, Yizhong Wang, Guangxuan Xiao, Hao Peng, and Yao Fu. Retrieval head mecha-
nistically explains long-context factuality.arXiv preprint arXiv:2404.15574, 2024.
[41] Wuwei Zhang, Fangcong Yin, Howard Yen, Danqi Chen, and Xi Ye. Query-focused retrieval
heads improve long-context reasoning and re-ranking. InProceedings of the 2025 Conference
on Empirical Methods in Natural Language Processing, pages 23802–23816, 2025.
[42] Omar Khattab and Matei Zaharia. Colbert: Efficient and effective passage search via contextual-
ized late interaction over bert. InProceedings of the 43rd International ACM SIGIR conference
on research and development in Information Retrieval, pages 39–48, 2020.
[43] nostalgebraist. interpreting GPT: the logit lens. LessWrong, 2020.
[44] Ruining Li, Gabrijel Boduljak, et al. On vanishing variance in transformer length generalization.
arXiv preprint arXiv:2504.02827, 2025.
[45] Pavlo Vasylenko, Hugo Pitorro, André FT Martins, and Marcos Treviso. Long-context general-
ization with sparse attention.arXiv preprint arXiv:2506.16640, 2025.
[46] Loubna Ben Allal, Anton Lozhkov, Elie Bakouch, Gabriel Martín Blázquez, Guilherme Penedo,
Lewis Tunstall, Andrés Marafioti, Hynek Kydlíˇcek, Agustín Piqueres Lajarín, Vaibhav Srivastav,
et al. Smollm2: When smol goes big–data-centric training of a small language model.arXiv
preprint arXiv:2502.02737, 2025.
[47] Diane Tchuindjo, Devavrat Shah, and Omar Khattab. Obliq-bench: Exposing overlooked bottle-
necks in modern retrievers with latent and implicit queries.arXiv preprint arXiv:2605.06235,
2026.
[48] Stéphane Ross, Geoffrey Gordon, and Drew Bagnell. A reduction of imitation learning and
structured prediction to no-regret online learning. InProceedings of the fourteenth interna-
tional conference on artificial intelligence and statistics, pages 627–635. JMLR Workshop and
Conference Proceedings, 2011.
13

<!-- page 14 -->
A Prompt Format
To make the input format used by BLOCKSEARCHconcrete, fig. 4 shows a worked example for
a single MS MARCO query against a four-document corpus. Each document is wrapped between
BOS/EOS markers and bracketed by its randomly-assigned four-digit code (§3.2); RoPE[29] positions
are reset to 0 at every BOS so that the document tokens occupy positions 0–Tdoc regardless of where
the document sits in the prefill. Document tokens attend causally only inside their own block.
After the corpus, the query block is appended at RoPE position Tdoc=300 and attends to the entire
prefilled corpus. The query block carries an instruction prefix, the query, and the four answer slots;
the model is supervised to emit the four-digit code identifying the gold document and is decoded
autoregressively at inference. The same template is used at training and at evaluation, with one
difference: at training time the four answer digits are teacher-forced and the on-policy auxiliary loss
(§F) replays the model’s own rollout at the same four positions.
# Document blocks: one per corpus document, codes sampled uniformly per
training step.
[BOS]Doc 7421: The Apollo program, also known as Project Apollo, was the third
United States human spaceflight program carried out by NASA, which succeeded in
landing the first humans on the Moon from 1969 to 1972 ... (Doc 7421)[EOS]
[BOS]Doc 0394: Yuri Gagarin became the first human to journey into outer space
on 12 April 1961, when his Vostok spacecraft completed one orbit of the Earth
... (Doc 0394)[EOS]
[BOS]Doc 5108: ... (Doc 5108)[EOS]
[BOS]Doc 8862: ... (Doc 8862)[EOS]
# Query block: appended after all documents, at RoPE position 300.
[BOS]Instruct: Given a web search query, retrieve relevant passages that
answer the query
Query: who was the first person to land on the moon
Answer: 7 4 2 1
Figure 4: Worked example of the BLOCKSEARCHprompt. Documents are prefilled with block-sparse
attention (§3.2); the query is then appended and the model autoregressively decodes a four-digit
code. The underlined digits are the supervision target at training time and the autoregressive output at
inference.
B Evaluation Suite
Dataset Split QueriesN max Avg. tokens / doc Tokens @N max
MS MARCO dev 400 10,000 94.8 948,421
HotpotQA test 400 10,000 116.3 1,163,144
NQ test 400 8,600 139.6 1,201,153
Table 4: Datasets used for evaluation. Tokens measured under the Qwen3 tokenizer, capped at 300
tokens per document; means and totals are computed over the actual padded draws.
Because NQ has far more tokens per document than MS MARCO or HotpotQA, we slightly truncate
the dataset size, and reduce the number of hard negatives per query from 24 to either 20 or 21. This
is the result of a round-robin algorithm that prunes out documents evenly from the dataset until we
hit 8600 documents, or around 1.2M tokens.
14

<!-- page 15 -->
C RLHN Training-Data Composition
We train all BLOCKSEARCHvariants on a filtered version of the public RLHN-680K release [ 31].4
Each query in the source ships with one or more positive passages and a pool of mined negatives.
We score every (query, candidate) pair with Qwen3-Embedding-8B [ 33] (last-token pooling, ℓ2-
normalized, max sequence length512), then apply two filters and a fixed-shape trim:
1. drop queries with fewer than16candidates or fewer than15negatives;
2. drop queries where the highest-scoring candidate is a negative, i.e. max score(pos)≤
max score(neg);
3. retain the single best-scoring positive plus the top-15 highest-scoring negatives, giving exactly
16documents per query.
The resulting post-filter, post-trim dataset has 522,487 training samples drawn from 7 source corpora
(table 5); each sample is one query paired with its 16 documents. Optimization steps are stratified per
source: each batch contains queries from a single subset, so the gradient at any step reflects a single
retrieval distribution. Documents are truncated to Tdoc=300 tokens at training time. Token counts
in table 5 use the Qwen3-0.6B tokenizer; document-token averages are estimated from a stratified
random sample of8,000documents per subset (standard error<0.5tokens at thisn).
Table 5: Composition of the post-filter, post-trim RLHN training mix. Source subsets carry their
original RLHN names. Each training sample carries one query plus its16documents.
Source # training samples Avg. query tok Avg. doc tok
MS MARCO 368,961 7.0 84.6
HotpotQA 81,551 24.2 100.6
FEVER 28,561 11.7 265.1
NQ 27,962 10.5 146.5
SCIDOCS-RR 11,787 13.4 221.9
FiQA 2,822 13.9 225.7
ArguAna 843 251.9 209.9
Total 522,487 – –
4https://huggingface.co/datasets/rlhn/rlhn-680K
15

<!-- page 16 -->
D Training Hyperparameters
All BLOCKSEARCHvariants in this paper share a single training recipe, fine-tuning Qwen/Qwen3-
0.6B on the RLHN-filtered mix of §C with the on-policy auxiliary loss of §F. The shared hyperpa-
rameters are listed in table 7; the modification variants of §5 (BLOCKSEARCH-sink, BLOCKSEARCH-
SSMax) layer length-aware attention modifications on top of this recipe and otherwise inherit every
other knob. The variant-specific differences are listed in table 6.
Note on the sink.The per-layer sink scalars bL sit in their own parameter group with LR 1×10−3
and zero weight decay (vs. 3×10−5 / 0.01 for the base weights): the higher LR compensates
for the small gradients flowing through σ(lse−b L) into a single scalar, and zero weight decay
avoids pulling the gate toward an uninformative regime. The length signal is injected by sampling
Neff ∼logU(N 0,5k) per step (N0=128 for our 8-GPU setup) and using bL +αlog(N eff/N0) as the
effective threshold, with the gate strength linearly ramped in over the first ∼2k steps. At evaluation
the gate is disabled entirely: the learned bL stay in the checkpoint but do not affect attention. The
mechanism only shapes what the rest of the model adapts to during training. As a check, we replayed
the gate at evaluation with the trained thresholds and length schedule on MS MARCO: Recall@1 is
96.5 / 75.5 / 45.3 / 21.3 / 2.8 at N=500 / 1k / 2.5k / 5k / 10k, against 96.5 / 75.2 / 45.2 / 21.2 / 2.5
with the gate disabled (table 2), so enabling it at test time is essentially a no-op.
Note on SSMax.The per-layer scalars sL are initialized to 0.43 following [9] and trained in the
shared parameter group — no separate LR or weight decay. Length conditioning is explicit through
logN, so the same scaling applies unchanged at evaluation.
Table 6: Variant-specific hyperparameters: differences between BLOCKSEARCH, BLOCKSEARCH-
sink, and BLOCKSEARCH-SSMax. All other settings are shared (table 7).
BLOCKSEARCHBLOCKSEARCH-sink BLOCKSEARCH-SSMax
Layers modified – all28all28
Per-layer parameter – sink scalarb L scalars L
Initialization –b (0)L = 14.0s (0)L = 0.43
Param-group LR –1×10 −3 shared
Param-group weight decay –0shared
Warmup / ramp (steps) –500/1500—
Length signal –b L +αlog NeffN0 sL logNStrengthα–1.0—
Gated rows –{0,1,2}—
Neff at training –logU(N 0,5k)—
N0 –128—
Table 7: Shared training hyperparameters for all BLOCKSEARCHvariants.
Group Value
Base model Qwen/Qwen3-0.6B (bf16)
Distributed DDP,8×NVIDIA A100
Optimizer AdamW (fused),βdefaults
Base LR / weight decay3×10 −5 /0.01
LR schedule linear warmup (start factor0.05) over1000steps
Per-GPU batch size16queries (effective global128)
Epochs1pass over the RLHN-filtered triples
Documents per query16(stratified from the top-32RLHN candidates)
Document length capT doc = 300tokens
Code width / scheme4digits, sampled uniformly per training step
Query rotary offset300
Loss next-token CE on the4-digit code
+ on-policy aux. loss weightλ= 0.5(§F)
+ KL distillation (auxiliary teacher) EMAα= 0.95
Attention kernel block-sparse FlexAttention [30]
16

<!-- page 17 -->
E Training details forQwen3-dense
We fine-tune Qwen3-0.6B (FlashAttention-2, gradient checkpointing) into a last-token-pooled, ℓ2-
normalized embedding model on the same RLHN-filtered mix used for BLOCKSEARCHtraining (§C).
Each training example pairs one query with C=16 teacher-scored candidates; queries are formatted
with the same instruction prefix used at evaluation (“Given a web search query, retrieve relevant
passages that answer the query”), and only the last hidden state of each sequence is pooled. The loss
is a contrastive term plus a teacher-distillation term:
L=L CE +λ KL LKL,L CE = CE

1
τs q C⊤all, y ,L KL = KL σ(st/τt)∥σ(s s/τs),(6)
where Call is the candidate matrix gathered (with gradient) across all DDP ranks, so each query
is contrasted against W·B·C documents in total; y points at the gold candidate within the
gathered block; and the KL term distills the teacher’s softmax over the local 16 candidates into the
student’s softmax over the same 16. Hyperparameters are listed in table 8; we train a single epoch
over the RLHN-filtered triples on 8× NVIDIA A100, with cosine decay to 0.1η 0 after a 500-step
linear warmup, AdamW (β defaults), and gradient clipping at 1.0. The resulting checkpoint is the
Qwen3-dense-0.6Bdense baseline used throughout the paper.
Table 8:Qwen3-densetraining configuration.
Component Setting Value
Backbone Qwen3-0.6B, bf16, FlashAttn-2, grad-ckpt —
Pooling last-token,ℓ 2-normalized —
Query / doc len max tokens128/300
Candidates per query (RLHN teacher-scored)C=16
Negatives cross-rank gathered in-batchW·B·C
Batch size per-GPU×GPUs32×8
Optimizer AdamW, weight decay0.01
Learning rate peakη 0 / floor2×10 −5 /0.1η 0
Schedule linear warmup→cosine decay500steps warmup
Grad clipℓ 2 1.0
Student / teacher temperatureτ s /τ t 0.02/0.02
KL weightλ KL 0.5
Epochs over RLHN-filtered1
17

<!-- page 18 -->
F On-Policy Auxiliary Loss
§3.2 introduces an on-policy auxiliary loss to mitigate exposure bias when decoding the four-digit
code. The procedure is given in algorithm 1. For each query in the batch, we have K candidate
documents (1 positive, 15 hard negatives) with their full four-digit codes and Qwen3-Embedding-8B
relevance scores, and the corpus has already been prefilled into the shared block-sparse cache (§3.2).
Algorithm 1On-policy auxiliary loss for ICR decoding (per minibatch).
Require: model πθ; batch of queries with prefilled document cache; per-query candidate codes
c(1), . . . , c(K) (each a length-Ldigit string) with teacher relevance scoresr (1), . . . , r(K).
1:Compute teacher weightsw k ∝exp(r (k)/τtch)over theKcandidates.
2: (1) Rollout the model on its own.Sample a code ˆa= ˆa1 . . .ˆaL autoregressively from πθ with
gradients off.
3:(2) Build a per-position teacher.For each digit positiont:
4:Keep candidates whose firstt−1digits match the rollout:M t ={k:c (k)<t = ˆa<t}.
5:Set the teacher distribution over the10digits to the candidate-weighted vote:
qt(d)∝
X
k∈Mt
wk ·1[c (k)t =d].
6: (3) Replay with gradients.Re-decode the four answer positions conditioned on ˆa<t (the rollout’s
prefix, not the gold prefix) with gradients on, obtaining the student distributionsπ θ(· |ˆa<t).
7:Loss:L aux = 1L PLt=1 CE qt, πθ(· |ˆa<t), added to the total loss asL=L CE +λL aux.
The rollout uses the model’s own distribution rather than the gold code, so the prefixes that the
four answer positions condition on are exactly the prefixes the model would visit at inference. The
per-position teacher qt thus plays the role of a DAgger expert [ 48]: at every state visited along
the model’s own trajectory, it specifies what the model should have done. We ramp λ in linearly
from 0 over the first warmup steps so early training is dominated by the standard teacher-forced
cross-entropy.
18

<!-- page 19 -->
G Per-head softmax statistics atL19
§4 shows that at L19 the gold document’s share of the attention output collapses while the output’s
magnitude stays roughly constant. This appendix looks at the per-head attention statistics behind that
result.
For a single head, the attention mass on the gold document is a sigmoid of the difference between two
log-sum-exps, one over gold tokens and one over all other tokens: mG =σ
 
lseG −lse ¯G

. We track
two quantities at L19 as N grows (table 9): gold’s largest attention score smaxG , which dominates
lseG, and the gap lse ¯G −lse G. We report medians over the six L19 heads that carry the retrieval signal
(heads 4, 5, 7, 9, 12, and 13). Six other heads at this layer act as attention sinks and give the gold
document a mass of1/Nat everyN, so including them would hide most of the collapse.
For BLOCKSEARCH, gold’s largest score falls from 25.31 to 13.86 between N=500 and N=10k,
and the gap grows from −1.59 to +6.34. As a result, gold’s attention mass falls from 0.82 to 0.0018,
a drop of 7.94 nats in log-odds, or a factor of about 2,800. A corpus that is 20× larger would by itself
account for log 20 = 3.00 nats of this [11, 12]. The remaining 4.94 nats come from gold’s score
falling relative to the other documents.5
Table 9 also includes the sink and SSMax variants from §5. The sink behaves almost like BLOCK-
SEARCH, which matches its small effect on recall. SSMax raises gold’s score as N grows (+7.06
instead of −11.45), but it raises the scores of the other documents even more (table 10). Gold’s
attention mass at N=10k is therefore 11× higher than for BLOCKSEARCHbut still below 2%, which
is consistent with the partial recovery in recall.
Table 9: Per-head attention statistics at L19 on MS MARCO (n=100), taking the median over the
six retrieval heads within each query and then over queries. smaxG is gold’s largest pre-softmax score,
the gap lse ¯G −lse G is lower when it favors gold, and gold mass is gold’s share of the post-softmax
attention.
CheckpointN s maxG lse ¯G −lse G Gold mass
BLOCKSEARCH500 25.31−1.59 0.823
1k 24.71 +0.09 0.478
2.5k 23.35 +2.19 0.102
5k 19.85 +4.06 0.018
10k 13.86 +6.34 0.002
BLOCKSEARCH-sink500 26.42−1.82 0.853
1k 26.02−0.09 0.521
2.5k 24.25 +2.24 0.100
5k 21.99 +3.55 0.028
10k 16.86 +5.74 0.003
BLOCKSEARCH-SSMax500 33.97−2.60 0.915
1k 35.77−0.63 0.625
2.5k 37.90 +1.81 0.142
5k 38.99 +2.80 0.057
10k 41.03 +4.04 0.019
Table 10: Change in gold’s attention at L19 from N=500 to N=10k for each model, from the same
measurements as table 9. The odds drop is the fall in gold’s log-odds against the rest of the corpus, in
nats and as a factor. A20×larger corpus alone would account for3.00nats (20×).
Checkpoint Odds drop∆s maxG ∆ lse¯G Gold mass at10k
BLOCKSEARCH7.94 2,800× −11.45−2.57 0.0018
BLOCKSEARCH-sink7.56 1,929× −9.56−1.45 0.0034
BLOCKSEARCH-SSMax6.64 764×+7.06 +12.64 0.0195
5A document’s code depends on its position in the sorted corpus, so the same passage receives a different code, and
therefore different keys after the code tokens, at each N. Assigning codes by document identity instead changes smaxG by at
most0.17at anyNand leaves the drop in gold’s attention mass unchanged (0.824to0.0018).
19

<!-- page 20 -->
H What fills the attention output at largeN
Table 1 shows that the L19 output stops being driven by the gold document at large N. To see what
replaces it, we split the output into three pieces that together cover all document tokens: the shared
first token of every document (Doc), the gold document’s content tokens, and the other documents’
content tokens (table 11). We report each piece’s length as a share of the total output length, as a
median over 100 queries. The pieces point in different directions, so the shares do not sum to one,
and together they reconstruct the full output to within about0.3%.
The shared first token absorbs much of the attention mass in many heads, so it could in principle
come to dominate the output at large N. It does not. Its share grows only from 0.21 to 0.35, while
the share from other documents’ content grows from 0.28 to 0.87, so the layer is writing the content
of the wrong documents rather than a generic signal. The gold document’s own first token contributes
at most0.0004of the output, so it does not inflate the gold share in table 1.
As N grows, the output also becomes less specific to the query. The median cosine similarity
between the L19 outputs of different queries rises from 0.47 at N=500 to 0.90 at N=10k, while the
gold-driven piece stays query-specific (0.30 to 0.36) but shrinks. The model does not fall back to
a single default answer, however. At N=10k, greedy decoding produces 78 distinct codes for 100
queries, and for N≤5k , beam search produces 385 to 398 distinct top-1 answers for 400 queries.
The model retrieves the wrong documents rather than emitting a fixed answer.
Table 11: Three-way split of the L19 attention output on BLOCKSEARCH, MS MARCO, 100 queries.
Each share is a piece’s length divided by the total output length, computed per query and then taken
as the median.
N∥a 19∥sharedDoctoken gold content non-gold content
500 47.48 0.210 0.905 0.282
1k 45.36 0.218 0.742 0.426
2.5k 43.03 0.227 0.193 0.798
5k 36.90 0.280 0.060 0.871
10k 30.27 0.347 0.007 0.872
20

<!-- page 21 -->
I Equivalence of the additive-sink and sigmoid-gate forms of attention
We prove that the additive-sink softmax of eq. (5) is exactly equivalent to multiplying the standard
softmax of eq. (1) by a sigmoid gate.
Proposition 1.Fix a layer L and head h. Let s= (s hL,1, . . . , shL,T )∈R T be the pre-softmax logits
at the d1-emission position, bL ∈R the learned sink scalar, αhL,t the standard softmax weight from
eq.(1), and˜αhL,t the additive-sink weight from eq.(5). Define the layer-and-head-wise gate
ghL =σ  lse(s)−b L,lse(s) = log TX
t=1
exp(shL,t), σ(x) = 11 +e −x .
Then for everyt∈ {1, . . . , T},
˜αhL,t =α hL,t ·g hL.
Proof. Let Z= PTt′=1 exp(shL,t′) = exp(lse(s)) denote the standard softmax normalizer. By eq. (1),
αhL,t = exp(shL,t)/Z. By eq. (5), the additive-sink weight is
˜αhL,t = exp(shL,t)Z+ exp(b L) .
Multiply numerator and denominator by1/Z:
˜αhL,t = exp(shL,t)/Z1 + exp(bL)/Z =α hL,t · 11 + exp(bL −lse(s)) =α hL,t ·σ lse(s)−b L =α hL,t ·g hL,
where the third equality usesσ(x) = 1/(1 +e −x)withx= lse(s)−b L.
Interpretation.The gate ghL ∈(0,1) depends only on the per-(layer, head) comparison between
lse(s) — a measure of how much pre-softmax mass the layer’s logits already concentrate — and
the learned threshold bL. When the layer’s logits are sharp and concentrated relative to bL (large
lse), ghL →1 and eq. (5) reduces to the standard softmax. When the logits are diffuse and many
tokens contribute small amounts (small lse relative to bL), ghL →0 and the layer’s contribution to the
residual update aL is suppressed multiplicatively. This is the mechanism by which the sink “costs”
a noisy layer its write to the residual stream without altering the relative ranking of the per-token
weights.
21

<!-- page 22 -->
J Top-BRouting Recall
The top- B routing of §5 hinges on the assumption that the router can keep the gold document
inside a small top- B shortlist with high probability across our checkpoints. We measure exactly
that: for B∈ {32,64,128,256,512,1024} we report the fraction of queries whose gold document
survives the QK-MaxSim router at layer 16, the default routing configuration used in §5. Evaluation
uses N=10,000 MS MARCO documents and n=400 queries (the same query slice for all three
checkpoints). Recall@B is derived per query from the gold document’s rank under the router’s score
relative to the fullN=10,000ranking.
Across all three checkpoints the gold document is retained for at least 93.5% of queries at the default
B=256 (BLOCKSEARCH: 0.962; BLOCKSEARCH-sink: 0.962; BLOCKSEARCH-SSMax: 0.935),
and the curves flatten between B=256 and B=512 — going from B=256 to B=1024 recovers
an additional ≤5 percentage points on every checkpoint (fig. 5). This is consistent with B=256
being a practical routing budget on this corpus: the remaining miss rate is dominated by the long
tail of routing errors (gold ranked beyond the top- 1024), which is unaffected by any reasonable
enlargement of B. BLOCKSEARCH-SSMax’s lower curve at small B (0.762 at B=32 vs. 0.838
for BLOCKSEARCH) is consistent with SSMax placing slightly less probability mass on the gold
document at the routing layer, but the gap closes byB=512.
32 64 128 256 512 10240
0.25
0.5
0.75
1
B= 256
Top-Brouting budget
Recall@B(gold survives)
BLOCKSEARCH
BLOCKSEARCH-sink
BLOCKSEARCH-SSMax
Figure 5: Routing recall@B for QK-MaxSim routing at layer 16 on MS MARCO with N=10,000
andn=400queries. Dashed line marks the defaultB=256used throughout the paper.
22

<!-- page 23 -->
Algorithm 2Digit-by-digit beam search for a single query.
Require: model πθ with the document corpus prefilled into its (block-sparse) KV cache; digit token
ids D={id(0), . . . ,id(9)}; code length L=4; beam width B; per-step prune kstep; return depth
kret.
1: Append the query and forward once; let ℓ1 = log softmax of the next-token logits restricted to
D.
2: Initialize B beams from the top-min(B,10) first digits, with beam scores =ℓ 1 of the chosen
digits; broadcast the KV cache across theBbeams.
3:fort= 2, . . . , Ldo
4:Forward all live beams one step; letℓ (b)t be the digit log-probs for beamb.
5:Candidate scores:score(b, d) = beam_score(b) +ℓ (b)t (d).
6:Per beam, keep only its top-k step digits (set the rest to−∞).
7: Flatten over (b, d)and keep the global top-B survivors; record each survivor’s parent beam
and digit.
8:Reorder the KV cache by parent index; append the chosen digit to each surviving beam.
9:end for
10:Sort theBcompleted beams by score;returnthe top-k ret digit strings.
K Beam Search and Recall@5
The main text reports Recall@1 over the single highest-probability four-digit code (§3.3). Here we
(i) specify the decoding procedure used to turn the model’s per-digit distributions into a ranked list of
document codes, and (ii) report the correspondingRecall@5across the full length-generalization
sweep, so that the main-text Recall@1 conclusions can be checked at a wider cutoff.
K.1 Decoding
A query is answered by a digit-by-digit beam search over the full N-document corpus (context-
parallel across GPUs), returning a ranked list of complete codes. Recall@k is computed over this
ranking.
K.2 Digit-by-digit beam search
Constrained beam search over a tree of identifier tokens is the standard decoder for generative and
in-context retrieval, and we follow that practice rather than introduce a new procedure [18, 19, 5].
Because each identifier here is exactly four digits drawn from a 10-symbol vocabulary, the search
tree has depth 4 and branching factor 10, and the beam is over digit strings rather than free-form
text. Algorithm 2 shows the routine; our default configuration is beam width B=25, per-step pruning
kstep=5, and return depthk ret=5(so Recall@5 reads the top five returned codes).
K.3 Recall@5 across the length-generalization sweep
Table 12 reports Recall@5 for the same variants, datasets, and corpus sizes as the main-text Recall@1
(fig. 1 and table 2). The qualitative picture is identical to Recall@1: the position-coded variant and the
no-modification model collapse by N=5k–10k on every dataset, while SSMax, top-B routing, and
their composition hold up across the full sweep. Recall@5 stays low wherever Recall@1 collapses
and rises with it wherever the modifications hold (e.g. MS MARCO BLOCKSEARCHat N=10k:
R@1 0.2, R@5 0.2; BLOCKSEARCH-routing 18.8→47.5 ), confirming that the main-text collapse
is not an artifact of the top-1 cutoff. For HotpotQA, whose queries have two golds, we also report
Recall@2 in table 13 for completeness.
23

<!-- page 24 -->
Table 12:Recall@5( ×100) vs. corpus size N, mirroring table 2 (n=400). NQ caps at N=8,607.
HotpotQA has two golds per query, so its columns report true recall (the fraction of the two golds
that land in the top 5); Natural Questions and MS MARCO are effectively single-gold, where this
matches the hit-based metric used in the main body.
Natural Questions MS MARCO HotpotQA
N0.5k 1k 2.5k 5k 8.6k 0.5k 1k 2.5k 5k 10k 0.5k 1k 2.5k 5k 10k
BLOCKSEARCH96.0 91.7 62.9 9.5 0.2 99.5 98.0 76.2 38.2 0.2 70.6 67.9 47.8 11.0 0.0
BLOCKSEARCH-position 96.7 90.7 39.4 2.8 0.2 99.2 96.5 67.0 7.8 1.0 67.9 64.4 34.6 1.9 0.0
BLOCKSEARCH-offpolicy 95.5 90.7 56.9 6.0 0.2 99.8 97.0 77.8 29.2 0.5 68.2 66.4 43.0 6.1 0.0
BLOCKSEARCH-sink 95.5 90.5 65.7 21.8 2.3 99.8 97.8 76.8 45.2 9.0 73.1 70.6 46.2 13.6 0.0
BLOCKSEARCH-SSMax 96.7 93.5 80.2 70.2 56.9 99.5 97.8 83.2 63.5 44.5 69.8 68.5 59.4 52.4 41.9
BLOCKSEARCH-routing 98.2 95.2 85.2 71.2 60.2 99.5 98.5 83.0 66.8 47.5 75.0 74.4 67.8 60.1 53.6
BLOCKSEARCH-SSMax-routing 97.0 94.5 79.7 73.9 61.2 99.2 97.8 80.5 65.8 46.0 74.2 72.5 67.0 59.6 52.4
Table 13: HotpotQARecall@2( ×100, true recall = fraction of a query’s two golds in the top 2,
n=400), for completeness alongside the HotpotQA Recall@5 column of table 12 (same runs).
Method 0.5k 1k 2.5k 5k 10k
BLOCKSEARCH63.4 61.2 39.8 8.9 0.0
BLOCKSEARCH-position 61.2 58.0 29.6 1.2 0.0
BLOCKSEARCH-offpolicy 61.2 58.5 36.5 3.8 0.0
BLOCKSEARCH-sink 65.0 61.1 38.5 9.5 0.0
BLOCKSEARCH-SSMax 62.4 61.1 52.9 44.8 35.2
BLOCKSEARCH-routing 68.1 67.2 58.6 52.1 46.0
BLOCKSEARCH-SSMax-routing 65.8 64.0 57.8 50.9 45.4
L LIMIT worked example
Figure 6 shows a worked LIMIT-small example for the lexical retrieval task evaluated in §6.
# LIMIT-small corpus: one short biography per person (46 documents).
[BOS]Doc 6359: Geneva Durben likes Quokkas, River Otters, Tapirs, Asymmetry,
Snow Leopards, ..., Joshua Trees, Pansies, Soy Sauce, Cards Against Humanity
and Elm Trees. (Doc 6359)[EOS]
[BOS]Doc 9841: ... (a different person, whose list does not contain Joshua
Trees) ... (Doc 9841)[EOS]
# Query block: appended after all 46 documents, at RoPE position 300.
[BOS]Instruct: Given a web search query, retrieve relevant passages that
answer the query
Query: Who likes Joshua Trees?
Answer: 6 3 5 9
Figure 6: Worked LIMIT-small example. Relevance is lexical: the gold document is a person whose
preference list contains the queried item (Joshua Trees ), among the 46 documents. Each query has
two gold documents (we show one); either code is a correct answer. The query and gold text are from
the evaluated corpus.
L.1 Recall@2 and Recall@5
The main-text table 3 reports Recall@1 under the metric used throughout the body (a query counts if
either gold is in the top 1). Here we additionally report standard Recall@k: the fraction of a query’s
two golds that appear in the top k, at k=2 (table 14) and k=5 (table 15). The picture is the same:
SSMax+routing holds up across the sweep while BLOCKSEARCHand BLOCKSEARCH-sink collapse
byN=2.5k.
24

<!-- page 25 -->
Table 14: LIMITRecall@2(fraction of a query’s two golds in the top 2, n=1,000) vs. corpus size
N, for the same runs as table 3. The dense baseline’sN=10,000cell is not available.
Method Scoring46 500 1000 2500 5000 10000
BLOCKSEARCHICR beam0.286 0.069 0.015 0.000 0.000 0.001
BLOCKSEARCH-sink ICR beam0.198 0.038 0.016 0.002 0.000 0.000
BLOCKSEARCH-SSMax ICR beam0.344 0.177 0.130 0.070 0.048 0.013
BLOCKSEARCH-SSMax-routingICR beam0.344 0.197 0.177 0.170 0.133 0.093
Qwen3-densepooled cosine0.160 0.063 0.045 0.036 0.025—
Random chance —0.043 0.004 0.002 0.001 0.000 0.000
Table 15: LIMITRecall@5(fraction of a query’s two golds in the top 5, n=1,000) vs. corpus size
N, for the same runs as table 3. The dense baseline’sN=10,000cell is not available.
Method Scoring46 500 1000 2500 5000 10000
BLOCKSEARCHICR beam0.436 0.104 0.027 0.000 0.000 0.003
BLOCKSEARCH-sink ICR beam0.340 0.070 0.032 0.004 0.000 0.000
BLOCKSEARCH-SSMax ICR beam0.488 0.231 0.164 0.095 0.067 0.019
BLOCKSEARCH-SSMax-routingICR beam0.488 0.258 0.241 0.225 0.182 0.135
Qwen3-densepooled cosine0.300 0.098 0.066 0.050 0.039—
Random chance —0.109 0.010 0.005 0.002 0.001 0.001
M OBLIQ results
We additionally evaluate on OBLIQ [47], a benchmark of “oblique” retrieval, where relevance is
indirect rather than lexical or topical. We use three of its tasks.MathandWritingareanalogues
tasks: the query is a passage (a competition mathematics problem, or a paragraph of prose), and
the gold documents are other passages that share an abstract reasoning pattern or argument with it
despite entirely different surface content.Twitteris adescriptivetask: the query is a natural-language
description of a class of posts, and the gold documents are tweets matching that description (see
fig. 7 for one example per task). Corpus size N is set per task by feasibility: Math uses the full
corpus, while Twitter and Writing use gold-preserving subsamples (drawn from the full 72k- and
10,388-document corpora); per-dataset document counts, query counts, and average lengths are given
in table 16. We apply the OBLIQ self-match exclusion (each query’s own source passage is dropped
from its ranking). As in §6 we evaluate the four BLOCKSEARCHvariants and the same-backbone
pooled dense retriever, and additionally a long-context generative-retrieval baseline,MSA-4B [15];
for ICR the ranked list is the beam search output. Unlike the main body, here we report standard
Recall@k: the fraction of a query’s gold documents that appear in the top k. Recall is inversely
related to the number of golds per query — a top- k list can hold at most k of them — so with
OBLIQ’s many golds (a mean of∼9–13per query) the values are correspondingly small.
Table 16: OBLIQ dataset statistics for the evaluated subsets. Lengths are in Qwen3-0.6B tokens
(mean over documents, and over queries that have a gold). Documents are truncated to 300 tokens at
prefill, which affects mainly Writing. Twitter and Writing corpora are gold-preserving subsamples of
the full72k- and10,388-document corpora.
Avg. tokens
Dataset Documents Queries Doc Query
Math (analogue)3,507 151 116 181
Twitter (descriptive)10,000 281 52 53
Writing (analogue)4,000 512 498 653
25

<!-- page 26 -->
Math (analogues).Instruction:Given a mathematical problem statement, retrieve passages that present
analogous problems or techniques.
Query:Let(M, d)be a nonempty complete metric space andS:M→MwithS 2 a strict contraction;
show thatShas a unique fixed point. . . .
Gold:LetUbe a nonempty bounded open set inR n; . . . show that there is an affine transformation
carryingUto the unit ball.
Writing (analogues).Instruction:Given a passage of writing, retrieve other passages with analogous
ideas, arguments, or stylistic techniques.
Query:“We see some good news in alignment – as models become more capable, they are also more
aligned . . . but still far from the reliability required in high-stakes applications.”
Gold:“Leonard Shelby, the protagonist of Christopher Nolan’s filmMemento, suffers from anterograde
amnesia . . . he uses notes, photos, and tattoos to communicate facts to his future self.”
Twitter (descriptive).Instruction:Given a description of a tweet, retrieve tweets that match the
description.
Query:Find tweets where users implicitly mock feel-good branding and token measures from tech moguls
and politicians while actual wars intensify.
Gold:“@user ‘but we decided to send 8000 helmets to the Strait of Hormuz to help defend the free
world’ ”
Figure 7: Worked OBLIQ examples, one per task. Math and Writing areanaloguestasks (the gold
shares an abstract pattern with the query despite different surface content); Twitter is adescriptivetask.
Query and gold text are from the evaluated corpora, abbreviated; the Twitter handle is anonymized.
Table 17: OBLIQ results: Recall@1 / Recall@5 (the fraction of a query’s gold documents that appear
in the top k; with many golds per query these values are small), with the OBLIQ self-match exclusion
applied.MSA-4Bemits∼1citation per query, so its R@5 is close to its R@1.
Math (N=3.5k) Twitter (N=10k) Writing (N=4k)
Method Scoring R@1 R@5 R@1 R@5 R@1 R@5
BLOCKSEARCHICR beam0.000 0.000 0.000 0.000 0.002 0.004
BLOCKSEARCH-sink ICR beam0.000 0.001 0.000 0.001 0.000 0.003
BLOCKSEARCH-SSMax ICR beam0.000 0.011 0.001 0.004 0.000 0.005
BLOCKSEARCH-SSMax-routing ICR beam0.007 0.029 0.000 0.003 0.001 0.006
Qwen3-densepooled cosine0.014 0.057 0.000 0.004 0.009 0.025
MSA-4Bgen. citations0.013 0.027 0.002 0.008 0.004 0.008
N Generality beyond Qwen3 and BLOCKSEARCH
We test whether the collapse of §3.4 and its mechanism (§4) are specific to Qwen3-0.6B and our
training recipe, in two ways: an inference-only evaluation of an off-the-shelf proprietary long-context
LM, and a BLOCKSEARCHtrained on a second backbone family.
Off-the-shelf long-context LM.We evaluate Gemini-3-flash on the MS MARCO setup of §3.3 with
no task training, prompting it to emit the codes of the relevant documents (400 queries). Its Recall@1
falls from 95.0 at N=500 to 16.2 at N=10,000 (table 18): the same corpus-scale degradation appears
without our architecture, data, or training. Because the model is only reachable through an API, the
mechanistic analyses below are not possible for it.
Second backbone: SmolLM2-360M.We train BLOCKSEARCHwith the same recipe on SmolLM2-
360M (LlamaForCausalLM, 32 layers), with the learning rate raised to 10−4. It starts lower than the
Qwen3 model and collapses earlier (table 18), reaching ≤1% Recall@1 by N=5,000 on all three
datasets. On LIMIT its Recall@1 is 0.117 at N=46 and at most 0.002 from N=500 onward; on
OBLIQ it is at most0.001(Recall@5 at most0.003) on every task.
The mechanism on SmolLM2.We repeat the analyses of §4 on the SmolLM2 model. The same
two-band structure appears, shifted deeper: at N=500, RsumL peaks at 0.59–0.69 across L17–L23
while first-digit accuracy is still at chance ( ≈0.10 ), and first-digit accuracy lifts off at L23→L24
(0.10→0.19 , reaching 0.33 by L31) (400 queries). As N grows (fig. 8), RsumL falls to 0.00 at every
26

<!-- page 27 -->
Table 18: Recall@1 (×100) for an off-the-shelf long-context LM and for BLOCKSEARCHon two
backbones. 400 queries per corpus size. Gemini-3-flash was evaluated on MS MARCO only. NQ’s
largest corpus isN=8,607.
Natural Questions MS MARCO HotpotQA
N0.5k 1k 2.5k 5k 8.6k 0.5k 1k 2.5k 5k 10k 0.5k 1k 2.5k 5k 10k
Gemini-3-flash (no training) — — — — — 95.0 72.8 52.0 35.0 16.2 — — — — —
BLOCKSEARCH(Qwen3-0.6B) 92.2 77.7 43.9 4.8 0.2 95.8 75.2 43.8 18.8 0.2 97.0 95.2 64.2 13.0 0.5
BLOCKSEARCH(SmolLM2-360M) 58.9 23.8 1.0 0.0 0.2 85.3 55.5 12.5 1.0 0.0 70.0 59.5 2.0 0.2 0.0
layer by N=10,000, and RanyL decays more slowly but is also near zero at N=10,000 (at most 0.15,
at L17; 0.09 at L18). The same shared-prefix sink behavior described in §4.2 appears in this model.
Finally, the attention-output decomposition at L23, the decode onset, shows the same swap as Qwen3
at L19 (table 19): the layer keeps writing into the residual at a comparable magnitude while the
gold-driven share falls from0.64to0.00.
0 4 8 12 16 20 24 28
0
0.25
0.5
0.75
1
LayerL
RsumL
(a)R sumL vsL
0 4 8 12 16 20 24 28
0
0.25
0.5
0.75
1
LayerL
RanyL
(b)R anyL vsL
N=500 N=1k N=2.5k N=5k N=10k
Figure 8: Per-layer recall vs. L across N∈ {500,1000,2500,5000,10000} on BLOCKSEARCH
trained on SmolLM2-360M, MS MARCO,100queries.(a)R sumL ;(b)R anyL . Compare fig. 3.
Table 19: Attention-output decomposition at L23 on BLOCKSEARCHtrained on SmolLM2-360M,
MS MARCO, 400 queries; norms are medians over queries and the share is the median of per-query
ratios. Compare table 1.
N∥a G23∥ ∥a ¯G23∥ ∥a 23∥ ∥a G23∥/∥a23∥
500 35.87 32.84 60.16 0.64
1k 15.93 40.06 57.59 0.27
2.5k 1.29 40.71 43.50 0.03
5k 0.07 35.94 36.08 0.00
10k 0.01 34.50 34.51 0.00
27

<!-- page 28 -->
O General capability after retrieval training
BLOCKSEARCHis trained only to emit four-digit document codes, so we measure how much general
capability the backbone retains, using lm-eval-harness (0-shot) under standard causal attention
(table 20). Retrieval-only fine-tuning costs 6.6 points of MMLU and 9.0 of HellaSwag on Qwen3-
0.6B, and 9.0 of HellaSwag on SmolLM2-360M (whose stock MMLU is already at chance, so it
cannot show a drop). Both models stay well above chance on HellaSwag. The sink variant matches
BLOCKSEARCH; we did not evaluate the SSMax and routing variants.
We read this as the cost of single-objective fine-tuning with no general-purpose or instruction data
in the mixture, not as evidence that retrieval and generation are incompatible. Our goal was to
isolate whether a decoder can learn corpus-scale retrieval at all; a model meant to do both would mix
general-purpose data into training, which we leave to future work.
Table 20: General capability (lm-eval-harness, 0-shot) before and after retrieval training. Random
chance is25.0on both tasks.
Checkpoint MMLU HellaSwag (acc_norm)
Qwen3-0.6B (stock) 40.2 47.3
BLOCKSEARCH33.6 38.3
BLOCKSEARCH-sink 33.5 37.9
SmolLM2-360M (stock) 25.4 56.4
BLOCKSEARCH(SmolLM2-360M) 24.8 47.4
P Training data and document truncation
How much comes from RLHN filtering?We compare two checkpoints with an identical recipe
(architecture, auxiliary loss, randomized codes, hyperparameters, seed) that differ only in training
data: the RLHN-filtered mix of §C and our original MS MARCO mix with false negatives left in
(table 21). The filtered mix helps little through N=2,500 (at most 1.5 points), roughly doubles recall
at N=5,000, and makes no difference atN=10,000, where both collapse. Most of BLOCKSEARCH’s
performance therefore does not come from data filtering. The comparison with Qwen3-dense is
data-controlled in any case, since it trains on the same RLHN mix.
Table 21: MS MARCO Recall@1 (×100) for two BLOCKSEARCHcheckpoints that differ only in
training data;400queries.
N500 1k 2.5k 5k 10k
RLHN-filtered mix (BLOCKSEARCH) 95.75 75.25 43.75 18.75 0.25
Original MS MARCO mix 95.25 74.00 42.25 9.00 0.00
How often does the 300-token cap truncate?Each document block is capped at 300 tokens, of
which 18 are the fixed identifier wrapper, so a document is truncated once its text exceeds 282 tokens.
In the training mixture this happens for 0.04% of MS MARCO (q, d)pairs, 0.69% of HotpotQA
pairs, and 0.04% of NQ pairs (estimated from a 25k-document sample per source), so truncation
plays essentially no role for these datasets. The cap is a property of our evaluation budget rather than
of the method: block-sparse prefill encodes each document independently, so longer blocks only
increase prefill cost.
28

<!-- page 29 -->
Q System cost
In-context retrieval moves the index into the KV cache, so its costs differ in kind from dense retrieval.
We report decode latency, which we measured, and memory, which follows from the architecture.
Latency.Table 22 reports the per-query decode time on MS MARCO (BLOCKSEARCH, 400
queries, 8×A100-80GB, a single timed run per cell). Dense decode grows roughly linearly with
the corpus, from 0.37 s at N=500 to 4.51 s at N=10k (12.3×). With top-B=256 routing, only the
shortlisted documents enter attention from L17 onward, and latency grows from 0.49 s to 0.84 s
(1.7× over a 20× larger corpus), a 5.4× speedup over dense decode at N=10k. Routed decode is
therefore much less sensitive to corpus size than dense decode, though not flat; at N=500 the routing
pass is pure overhead. The corpus prefill is computed once and reused across queries, so its cost
(5.5–11.9s per corpus in our runs) is amortized rather than paid per query.
Memory.Memory is the main practical cost. Qwen3-0.6B has 28 layers with 8 KV heads of
dimension 128, so its bf16 KV cache takes 112 KiB per token. At N=10k MS MARCO documents
(≈0.95 M tokens) this is ≈101 GiB, which we shard across 8 GPUs by context parallelism. A dense
index over the same corpus with 1,024-dimensional bf16 embeddings takes ≈20 MB, about three
orders of magnitude less. Dense retrieval also benefits from sublinear approximate nearest-neighbor
search, whereas attention compares the query against every key. Routing is a coarse step toward
avoiding that comparison; attention that is simultaneously sparse, differentiable, and GPU-efficient,
together with KV-cache compression, is in our view the central systems problem for this direction.
Table 22: Per-query decode latency (seconds) on MS MARCO, BLOCKSEARCH, 400 queries,
8×A100-80GB, single run per cell. Routing uses top-B=256 at L16. Recall@1 for each cell matches
table 2.
N500 1k 2.5k 5k 10k
Dense attention 0.37 0.57 1.20 2.34 4.51
Top-Brouting 0.49 0.53 0.57 0.65 0.84
Speedup0.75×1.07×2.11×3.61×5.35×
29
