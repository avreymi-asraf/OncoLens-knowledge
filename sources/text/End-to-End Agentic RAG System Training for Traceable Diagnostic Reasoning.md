<!-- page 1 -->
End-to-End Agentic RAG System Training for
Traceable Diagnostic Reasoning
Qiaoyu Zheng1,2, Yuze Sun1, Chaoyi Wu1, Weike Zhao1,2, Pengcheng Qiu1,2, Ge Wang1,4,
Yongguo Yu3, Kun Sun3, Jian Zhang5, Yanfeng Wang1, Ya Zhang1,2,6,† and Weidi Xie1,2,†
1Shanghai Jiao Tong University, Shanghai, China 2Shanghai AI Laboratory, Shanghai, China
3Xinhua Hospital affiliated to Shanghai Jiao Tong University School of Medicine, Shanghai, China
4Shanghai Ninth People’s Hospital, Shanghai Jiao Tong University School of Medicine, Shanghai, China
5Department of Pharmaceutical and Artificial-Intelligence Sciences, Shanghai Jiao Tong University
School of Medicine, Shanghai, China
6Institute of Artificial Intelligence for Medicine, School of Medicine, Shanghai Jiao Tong University,
Shanghai, China
The integration of Large Language Models (LLMs) into healthcare is currently constrained by inherent
knowledge limitations, hallucinations, and a fundamental disconnect from theprinciples of Evidence-
Based Medicine (EBM). While Retrieval-Augmented Generation (RAG) offers a potential solution,
current systems typically rely on static, heuristic-driven workflows that fail to capture the iterative,
hypothetico-deductive reasoning characteristic of clinical experts. To address this, we introduceDeep-
DxSearch, an agentic RAG system trained end-to-end via reinforcement learning (RL) to enable traceable
diagnostic reasoning. Unlike passive predictors, Deep-DxSearch operates as an active investigator, treating
the LLM as an agent and a comprehensive corpus—comprising over 16,000 guideline-derived disease profiles,
a structured database of 150,000+ patient records for case-based reasoning, and a massive repository of over
27 million biomedical literature-as its environment. By utilizing soft verifiable rewards that co-optimize
retrieval and reasoning, the model is trained to formulate queries, evaluate evidence utility, and refine
search strategies to close diagnostic gaps. Experiments demonstrate that our end-to-end agentic RL
training framework consistently outperforms prompt-engineering and training-free RAG approaches. Across
in-distribution (ID) and out-of-distribution (OOD) benchmarks for common and rare disease diagnosis, Deep-
DxSearch consistently surpasses strong baselines—including GPT-4o, DeepSeek-R1, and medical-specific
frameworks—achieving an average accuracy improvement of 22.7% over the second-best model. Crucially, in
a validation involving 150 real-world cases, Deep-DxSearch assistance elevates physicians’ average diagnostic
accuracy from 45.6% to 69.1%. These results suggest that evolving agentic systems to exploit statistical
regularities in large-scale healthcare data is essential for deploying trustworthy, transparent diagnostic
assistants. All data, code, and checkpoints are available athttps://qiaoyu-zheng.github.io/Deep-DxSearch.
1 INTRODUCTION
The integration of Large Language Models (LLMs) into clinical workflows holds the promise of democratizing
expert-level diagnostic support, potentially reducing diagnostic errors and alleviating physician burnout [1, 2,
3, 4, 5, 6, 7, 8, 9]. As these models grow in capability, the prospect of an “AI co-pilot” that can synthesize
vast amounts of patient data is becoming increasingly tangible [10, 11, 12, 13, 14, 15, 16, 17]. However, the
translation of these tools from research benchmarks to real-world physician assistants is currently hindered
by a fundamental discordance with theprinciples of Evidence-Based Medicine (EBM)[18, 19, 20].
Modern clinical decision-making is not merely about generating a correct prediction; it is a rigorous process of
substantiating hypotheses with established guidelines, verified literature, and historical precedents [20]. In
contrast, standard LLMs operate as “black boxes”, generating answers via parametric intuition, a process that
is prone to hallucination, and decoupled from verifiable sources [8, 21, 22]. Consequently, clinicians are often
left with a correct answer but no reliable way to verify its provenance, creating a “trust gap” that prevents
widespread adoption in high-stakes healthcare environments. For an AI system to be clinically viable, it must
transition from opaque prediction to traceable, evidence-anchored reasoning.
arXiv:2508.15746v2  [cs.CL]  1 Feb 2026

<!-- page 2 -->
To address this,Retrieval-Augmented Generation (RAG)has emerged as a mechanism to ground
LLMs in external data, allowing models to access up-to-date information without retraining [23, 24, 25, 26].
Yet, existing medical RAG systems remain largely static and heuristic-driven [23, 27, 28, 29, 30], treating
retrieval as a keyword-matching step rather than a reasoning process. They typically perform a “one-shot”
retrieval based on the initial query, failing to adapt when the retrieved evidence is insufficient, irrelevant,
or conflicting. This rigid approach contrasts sharply with the cognitive workflow of a human clinician, who
engages in a dynamic and progressive analysis [31, 32, 33]: formulating a differential diagnosis, consulting
specific guidelines to verify symptoms, searching for similar historical cases when presentations are atypical,
and refining the hypothesis based on new information. When a physician encounters ambiguity, they do not
stop; they dig deeper, cross-referencing sources until a consensus is reached. Existing AI frameworks lack
this “meta-cognitive” ability to recognize their own uncertainty and actively seek out the missing information
required to close the diagnostic loop.
Here, we introduceDeep-DxSearch, an agentic diagnostic system (Fig. 1a) that bridges this gap by learning
to mimic the iterative information-seeking behavior of physicians. Unlike previous frameworks that rely on
fixed prompt engineering or static retrieval pipelines, Deep-DxSearch is trained end-to-end (optimizing under
unified policy) with reinforcement learning (RL) to navigate a complex information landscape. By framing
the LLM as an autonomous agent and the medical corpus as its environment, we optimize a policy that learns
when to reason internally, when to query external databases, and how to synthesize heterogeneous evidence
into a coherent diagnostic argument. This approach moves beyond simple question-answering; the agent is
taught to formulate specific search queries, evaluate the utility of the returned documents, and iteratively refine
its search strategy if the initial results are unsatisfactory. This mimics the “hypothetico-deductive” reasoning
model used in clinical education, transforming the AI from a passive predictor into an active investigator.
Central to our approach is the construction of a comprehensive medical retrieval environment, designed to
replicate the diverse resources available to a practicing doctor. We integrate over 16,000 guideline-derived
disease profiles, a structured database of 150,000+ patient records for case-based reasoning, and a massive
repository of over 27 million biomedical literature to cover rare and emerging conditions. Within this
environment, Deep-DxSearch is incentivized not just for diagnostic accuracy, but for the validity of its retrieval
trajectory—rewarding the agent for uncovering high-fidelity evidence that explicitly supports its conclusions.
This multi-modal retrieval capability allows the system to triangulate answers, validating a diagnosis against
clinical guidelines while simultaneously checking for similar historical patient presentations. By grounding
the reward signal in evidence retrieval, we ensure that the model’s “thought process” is aligned with the
availability of concrete medical facts rather than the model’s likelihoods alone.
We demonstrate that this agentic reinforcement learning paradigm significantly enhances diagnostic perfor-
mance (Fig. 1b), achieving state-of-the-art accuracy across a multi-center cohort cases covering both common
and rare diseases. In a thorough evaluation spanning 8 clinical centers, Deep-DxSearch consistently outper-
formed both strong reasoning LLMs [34, 35, 36, 37] and training-free RAG or agentic baselines [25, 38, 39, 40].
Specifically, our agentic strategy surpassed standard RAG approaches by margins of 29.7% (p<0.01) on
in-distribution (ID) data and 9.7% (p<0.05) on out-of-distribution (OOD) data, while improving upon special-
ized medical foundation models by up to 31.8% (p<0.001) for rare diseases. Ablation studies reveal that these
gains are driven by our process-based reward design, which simultaneously optimizes retrieval and reasoning
policies—yielding a 13.7% (p<0.01) accuracy boost over target-only supervision. Beyond quantitative metrics,
interpretability analyses quantify how the agent evolves during training, learning to execute more diverse search
trajectories that prioritize differential diagnosis and irrelevance exclusion. Crucially, in physician-in-the-loop
studies, clinicians favored Deep-DxSearch’s auditable “Chain of Evidence” over the opaque “Chain of Thought”
of strong reasoners like DeepSeek-R1; while the latter excel at internal logic, Deep-DxSearch provides a
verifiable trail of medical literature for every claim, offering a blueprint for the next generation of trustworthy,
transparent diagnostic assistants.
|2

<!-- page 3 -->
Disease Information 
Guideline (n = 16,371)
Patient Record 
Database (n = 155,442)
Clinical Knowledge 
Collection (n > 27 million)
Medical Retrieval Corpus
Trajectories assessed by rewards
a. Workflow Overview
Deep-
DxSearch
Reinforcement
Learning
Physician
Only
Physician + 
DeepSeek-R1
Physician + 
Deep-DxSearch
vs. vs.
Overall Correctness
Clinical
Utility
Hallucination
Prevention
Diagnostic
Fidelity
Reasoning
Consistency
Physician
judge
LLM-as-
a judge
Evaluation on AI diagnostic decision support (average accuracy)
Evaluation on diagnostic reasoning quality (score 1~4)
b. Benchmark Overview
Trajectory 
Exploration
Evidence
Aqusition
Format
Alignment
Diagnostic 
Accuracy
Total Rewards
...
Evidence Retrieval 1
Lookup disease guideline: SLE, 
Rosacea, Dermatomyositis ...
      [SLE]: A chronic autoimmune 
disease characterized by a 
butterfly rash, arthritis, and often 
systemic involvement ...
      [Rosacea]: A chronic skin 
condition presenting with facial 
erythema and telangiectasia. It is 
limited to he skin and eyes and...
......
Match similar patients with: 
malar rash, arthritis, proteinuria...
Evidence Retrieval 2
      [Case A]: A 29-year-old 
female with a history of SLE 
presented with a worsening facial 
rash, fatigue, and proteinuria,...
      [Case B]: A patient diagnosed 
with Dermatomyositis presented 
with proximal muscle weakness 
and rash, but renal function...
......
Evidence Retrieval 3
Search knowledge: |PMC| 
Rosacea renal complications 
proteinuria, |Book| SLE 
diagnostic criteria..
      [PMC Doc]: A meta-analysis ... 
Rosacea is associated with...
      [Book Doc]: Clinical 
Manifestations of SLE: ... Renal 
Disorder: Persistent proteinuria 
(>0.5 g/d) or cellular casts...
......
Comparison with previous methods (average accuracy)
General-purpose LLMs
 Medical-specific
Diagnostic Methods
Deep-DxSearch (Ours)
%
% Excellent (4)
Good (3)
Fair (2)
Poor (1)
19.9%
16.8%
4.5%
19.1%
19.9%
19.1%
21.4%
14.0%
44.1%
45.6%
60.9%
69.1%
Figure 1 | Contribution Overview. a.The proposed workflow. Top: The medical retrieval corpus serving as the search
environment during both training and inference. Middle: Illustration of the Deep-DxSearch rollout process, where diagnostic
trajectories are generated and optimized via reinforcement learning based on trajectory-level rewards. Bottom: An exemplar log
demonstrating the system’s traceable evidence retrieval.b.Key performance highlights across three dimensions: Deep-DxSearch
achieves superior diagnostic accuracy compared to both general-purpose LLMs and specialized medical methods; demonstrates
notable clinical utility in physician assistance, surpassing the performance of DeepSeek-R1; and consistently attains high reasoning
quality (rated>“Good”) across five dimensions in both “LLM-as-a-judge” and human evaluations.
|3

<!-- page 4 -->
2 RESULTS
2.1 Deep-DxSearch Enables T raceable Diagnostic Reasoning via Agentic RL
We presentDeep-DxSearch, an agentic framework that transforms diagnosis from a static classification task
into a dynamic, multi-step inquiry. Unlike conventional Retrieval-Augmented Generation (RAG) systems
that rely on “one-shot” retrieval, Deep-DxSearch operates as an autonomous agent orchestrating five clinical
primitives: <reason> for hypothesis generation,<lookup> for guideline verification,<match> for case-based
reasoning,<search>for literature review, and<diagnose>for final assessment.
This architecture is underpinned by a tripartite reinforcement learning (RL) framework, optimizing a policy
that balances diagnostic accuracy with valid evidence retrieval and diverse trajectory exploration, the system
learns to mimic the hypothetic-deductive reasoning of human clinicians. To support this, we constructed a
massive medical retrieval environment comprising structured disease guidelines, validated patient records,
and a semantic knowledge base large-scale biomedical documents (see Sec. 4.1 for the details of corpus
construction).
In the following sections, we train and evaluate Deep-DxSearch against state-of-the-art foundation models
and specialized diagnostic systems across a multi-center cohort of over 24k patient cases. We further present
a physician-in-the-loop evaluation to validate clinical utility and provide an analysis on how end-to-end RL
reshapes diagnostic policy.
2.2 Baselines
We benchmark the performance of Deep-DxSearch against diverse models. First, we detail baseline LLM
enhancement techniques, including both prompting and training strategies, to isolate the specific contributions
of our agentic RL approach. Subsequently, we compare our whole final system against seven distinct categories
of state-of-the-art diagnosis methods.
Baseline LLM enhancement techniques.To rigorously evaluate the efficacy of our agentic RL approach,
we compare it against four representative LLM enhancement strategies:(i) vanilla model with direct
prompting. By properly designing instructions, we can prompt the base model to preform diagnosis directly
from its internal knowledge without any post-training or external retrieval, which is the most basic and
widely-used method for clinical LLM alignment [41, 42, 43]. The input is the free-text clinical presentation,
and no chain-of-thought inference is implemented;(ii) training-free RAG prompting. By adopting
prompts that equip clinical LLMs to interact with the retrieval corpus at will, the model can further integrate
domain-specific knowledge during inference [25, 29, 30]. For fair comparison, this inference-only (no traininig)
setting employs the same prompt design and tool access as our agentic system but relies solely on in-context
learning without any reward-based optimization;(iii) supervised fine-tuning (SFT). By further fine-tune
the LLM using the training dataset and cases from the patient record database in a generative way, we can align
latest LLMs with clinical tasks [44, 4, 45]. This baseline establishes the performance ceiling achievable through
traditional supervised learning on the same data distribution used for our reinforcement learning approach,
tested on the identical evaluation set;(iv) target-only RL training. This is a variant of our method,
employing reinforcement learning but removes the specialized policy reward that guides the optimization of
the reasoning and retrieval processes. Supervision is provided based solely on target outputs, using the same
environment and parameters as our full method for ablation study on the value of process-oriented guidance.
Other clinical diagnosis models.We further compare Deep-DxSearch against established state-of-the-
art diagnostic systems:(i) general-purpose large language models. We adopt the Qwen2.5 [46] and
Llama3.1 [47] series as our primary backbones. Specifically, considering the computational cost, we use
Qwen2.5-7B-Instruct, Qwen2.5-14B-Instruct, and Llama3.1-8B-Instruct. For high-capability baselines,
we employ GPT-4o (proprietary) [34] and DeepSeek-R1 (open-source) [35], accessing their official APIs
with the models DeepSeek-R1-0528 and gpt-4o-2024-11-20;(ii) biomedical CLIP-based encoders.
We adopt MedCPT [48], a contrastive learning approach that treats the clinical presentation as a query
to retrieve the most likely diagnosis, using their official checkpoint;(iii) medical large language &
foundation models. This category groups domain-adapted models trained on medical corpora [1] and
multi-modal foundation models [10]. We pick Meditron [36] and MedGemma [37] as representative models
|4

<!-- page 5 -->
with strong instruction-following capabilities, using their official checkpoints;(iv) medical RAG-based
frameworks. We include the MedRAG [25] framework, which relies on a general medical knowledge corpus
specified via system prompts without fine-tuning, using their official implementation;(v) chain-of-thought
agentic models. We evaluate CoD [39], a model that incorporates chain-of-thought paradigm through
supervised fine-tuning, using their official checkpoint;(vi) multi-agent consultation systems. We test
MAC [38], a framework employing multiple role-playing agents to simulate expert consultation with their
official implementation;(vii) multi-agent systems trained with reinforcement learning. We include
DoctorAgent [40], a system that combines multi-agent interaction with reinforcement learning and supervised
fine-tuning, using their official implementation.
2.3 Datasets
Medical retrieval corpus.The model is augmented by a comprehensive retrieval corpus, which comprises
three distinct knowledge sources: (1) structured disease guidelines mapping over 250k disease-phenotype
pairs to standard terminologies; (2) a patient record database containing 155k validated clinical cases for
similar-case retrieval; and (3) a massive clinical knowledge collection spanning millions of PubMed articles
and biomedical documents from Wikipaedia to provide broad semantic context (see Sec. 4.1 for more details).
Training & evaluation datasets.To rigorously evaluate Deep-DxSearch, we curated a diverse multi-center
cohort of over 24k clinical cases spanning seven international sources from America, Asia, and Europe. This
collection balances common pathologies (73.1%) with a significant representation of rare diseases (26.9%),
covering over 3,000 distinct diseases with high phenotypic complexity (averaging 4–12 symptoms per case).
We adopted a robust validation strategy to assess both internal consistency and external generalization. Five
core datasets (MIMIC-IV [49], PMC-Patients [50], MedDialog [51], RareArena1, and RareBench [43]) were
partitioned at a 3:1 ratio to form the in-distribution training and test sets. Crucially, to measure the model’s
ability to generalize to unseen clinical environments, we reserved the Mendeley [52] and Xinhua-Rare [53]
datasets exclusively for out-of-distribution zero-shot evaluation (see Extended Data Fig. 1 and Sec. 4.1 for
detailed dataset statistics and pre-processing protocols).
2.4 Evaluation Settings
In this section, we define the main metrics for model evaluation and interpretability of the RAG policy.
Performance metrics.We employ four quantitative metrics to assess system performance:(i) top-N
accuracy (Acc@N): measures if the ground-truth diagnosis appears within the top-N predictions.(ii)
Hit@N:evaluates the retrieval policy; a “hit” occurs if any of the top-N retrieved patients have the same
diagnosis as ground-truth(iii) hint score:the proportion of diagnostic workflows where the ground-truth
disease is explicitly mentioned during reasoning, even if not the final prediction;(iv) retrieval action steps:
The count of external information seeking actions (⟨lookup⟩,⟨match⟩,⟨search⟩) per trajectory, quantifying
the extent of evidence acquisition.
Assessment on reasoning (LLM-as-a-Judge).To scale the evaluation of reasoning quality, we implemented
an automated “LLM-as-a-judge” protocol [6]. We adopted two foundation models: DeepSeek-R1 [35] (for
general reasoning) and Meditron-70B [5] (for domain knowledge). These models scored cases across the five
holistic dimensions defined in Tab. 1, as defined by collaborating with expert clinician (8-year experience in
both clinical practice and AI). To ensure robustness, scores were averaged across three independent runs with
these two LLMs. The system prompt used to instruct these evaluators is provided in supplementary Sec. A.5.
Interpretability of RAG policy.We analyzed the learned RAG policy using four indicators:(i) symptom
association:proxied by Hit@20, this measures the model’s ability to extract pertinent clinical features that
lead to relevant case retrieval;(ii) differential diagnosis:measured by top-5 accuracy when the model is
provided with retrieved context containing both the ground-truth and differentials, assessing discriminative
capacity;(iii) irrelevance exclusion:measured by the maintenance of top-5 accuracy when the retrieval
module may return irrelevant noise, quantifying robustness against distraction;(iv) reasoning complexity:
quantified by the average number of action steps per trajectory, serving as a proxy for the thoroughness of
the diagnostic investigation.
1https://huggingface.co/datasets/THUMedInfo/RareArena
|5

<!-- page 6 -->
Table 1|Holistic evaluation framework for clinical reasoning (Score 1–4).
Dimension Score Criteria Description
Overall Correctness1–4From incorrect/dangerous (1) to precise identification of ground truth and exclusions (4).
Clinical Utility1–4From disorganized/no insight (1) to consultant-level analysis and management (4).
Reasoning Consistency1–4From chaotic/fallacious logic (1) to complex synthesis and robust coherence (4).
Diagnostic Filedity1–4From off-topic/irrelevant (1) to highly pertinent, high signal-to-noise ratio (4).
Hallucination Severity1–4From severe fabrication of symptoms (1) to completely faithful to case description (4).
a. In-distribution Comparison with General-purpose LLMs Prompted for Diagnosis in Average
Top-1 Accuracy in Common Disease Diagnosis
Top-1 Accuracy in Rare Disease Diagnosis
Top-5 Accuracy in Common Disease Diagnosis
Top-5 Accuracy in Rare Disease Diagnosis
b. In-distribution Comparison with Other Medical Diagnosis Alignment Methods across 6 Data Centers
Top-1 Accuracy in Common Disease Diagnosis Top-5 Accuracy in Common Disease Diagnosis
MIMIC-C PMC-Patients MedDialog MIMIC-C MedDialog
Top-1 Accuracy in Rare Disease Diagnosis Top-5 Accuracy in Rare Disease Diagnosis
MIMIC-R RareArena RareBench MIMIC-R RareArena RareBench
Top-1 Accuracy (%)Top-1 Accuracy (%)
Top-5 Accuracy (%)Top-5 Accuracy (%)
c. Out-of-distribution Comparison on Mendeley and Xinhua-Rare
MedCPT Meditron70B CoD MedRAG MAC DoctorAgentRL Deep-DxSearch
Top-1 Accuracy (%)
Top-5 Accuracy (%)
Top-1 Accuracy (%)
Top-5 Accuracy (%)
Accuracy on Mendeley (Common Disease Diagnosis) Accuracy on Xinhua-Rare (Rare Disease Diagnosis)
DeepSeek-R1 GPT-4o
PMC-Patients
Figure 2 | Comparison with previous diagnostic methods. a,Comparison of Deep-DxSearch with general-purpose
LLMs—including GPT-4o, GPT-4o with retrieval, and DeepSeek-R1—on common and rare disease diagnosis (averaged across
in-distribution datasets).b,Detailed performance breakdown of Deep-DxSearch versus medical-specific systems across individual
in-distribution datasets.c,Comparative evaluation of Deep-DxSearch against all these diagnostic methods on out-of-distribution
(OOD) datasets. Note, GPT-4o was excluded on Xinhua-Rare due to privacy constraints associated with this in-house dataset.
|6

<!-- page 7 -->
2.5 Deep-DxSearch Outperforms State-of-the-Art Models in Multi-Center Benchmarks
We evaluated diagnostic accuracy across the multi-center cohort, implementing Deep-DxSearch with the
MedGemma-27Bbackbone. The system demonstrated consistent superiority over both general-purpose
reasoners and specialized medical frameworks.
In-distribution (ID) evaluation.On common disease datasets, Deep-DxSearch achieved an average Top-1
accuracy of 42.2%, substantially outperforming DeepSeek-R1 (23.0%) and GPT-4o (18.8%) (Fig. 2a). Notably,
simply augmenting GPT-4o with our retrieval corpus (RAG-only) yielded only 24.0%, highlighting that access
to data alone is insufficient without a learned retrieval policy. For rare diseases—a critical stress test for
diagnostic AI—Deep-DxSearch attained 52.5% top-1 accuracy, widening the gap against DeepSeek-R1 (34.0%)
and GPT-4o (29.4%). Among medical-specific systems (Fig. 2c), our framework consistently led the field,
surpassing the strong Meditron-70B baseline by over 20 percentage points in common disease accuracy and
outperforming the multi-agent MAC system in rare disease scenarios.
Out-of-distribution (OOD) evaluation.The robustness of the learned policy was evidenced by zero-shot
performance on unseen datasets (Fig. 2d). On the Mendeley benchmark, Deep-DxSearch achieved 52.7% top-1
accuracy, surpassing the second-best method (MedRAG) by 5.8%. Similarly, on the Xinhua-Rare dataset, it
attained 46.3% accuracy, outperforming MAC (45.1%) and MedRAG (35.8%). These results indicate that
the agentic reasoning patterns learned via RL transfer effectively to novel clinical environments, maintaining
top-5 accuracy consistently above 60%.
2.6 Process-Based Rewards and Structured Retrieval Drive Performance Gains
To deconstruct the performance gains, we analyzed the contributions of the end-to-end RL training paradigm,
the reward structure, and the retrieval corpus.
Impact of end-to-end policy optimization with reinforcement learning.We compared the full
Deep-DxSearch framework against vanilla LLM, training-free RAG, and Supervised Fine-Tuning (SFT). Across
all tested backbones (Qwen, Llama, Baichuan, MedGemma), the RL-trained agent consistently yielded the
highest accuracy (Fig. 3a-c). For instance, on the MedDialog dataset, Qwen7B trained with Deep-DxSearch
achieves 49.3% accuracy, surpassing vanilla (9.0%) and RAG (19.6%); similarly, on the Xinhua-Rare dataset,
BaichuanM2 trained via Deep-DxSearch attains a top-1 accuracy of 39.3%, exceeding the vanilla (27.6%)
and RAG (35.8%), respectively. Crucially, Deep-DxSearch addresses the overfitting observed in supervised
fine-tuning (SFT), while SFT improves in-distribution performance (e.g., MedGemma on MIMIC-R improves
from 16.4% to 42.3%), it often degrades on out-of-distribution benchmarks due to overfitting (e.g., Llama8B
drops from 17.5% to 9.6% on Xinhua-Rare). In contrast, Deep-DxSearch maintains the strong performance
on out-of-distribution benchmarks.
Additionally, using an “LLM-as-a-judge” protocol (DeepSeek-R1 and Meditron-70B) (detailed in Sec. 2.4), we
find that Deep-DxSearch achieves superior reasoning quality compared to vanilla and RAG baselines (Fig. 3d).
Specifically, on OOD common disease settings, Deep-DxSearch attains areasoning consistencyscore of 3.37,
surpassing both vanilla (2.91) and RAG (3.15) methods. For OOD rare diseases, the model demonstrates
enhanced safety, achieving ahallucination severityscore of 3.75, outperforming the vanilla baseline (2.87) and
improving upon standard RAG (3.50).
Ablation on reinforcement learning rewards.We validate our composite reward function by progressively
removing components (Fig. 4a):(i) removing the trajectory exploration rewardreduces accuracy by
∼4% across datasets, resulting in rigid diagnostic workflows;(ii) removing the evidence acquisition
rewardscauses a sharp decline on accuracy (6.6% common, 10.9% rare), confirming the need to incentivize
valid intermediate steps;(iii) removing the diagnostic accuracy rewardcauses a further drop on
accuracy (∼2–6%). This ablation suggests that while the final diagnostic target provides the primary
directional signal, the retrieve-reason incentive is the most critical driver for navigating the complex search
space, with trajectory exploration serving as a necessary regularizer to prevent policy collapse.
Ablation on the retrieval corpus.We evaluate the impact of the retrieval corpus by progressively
removing components from the environment (Fig. 4a):(i) removing the clinical knowledge collection
results in a net accuracy decline (3.2% common, 1.1% rare);(ii) removing structured guidelinesleads to
|7

<!-- page 8 -->
a. In-domain evaluation of system design on common disease diagnostic accuracy
MIMIC-Common 
Top-1 Acc (%)Top-5  Acc (%)
PMC-Patients Med-Dialog
Top-1 Acc (%)Top-5  Acc (%)
Top-1 Acc (%)Top-5  Acc (%)
b. In-domain evaluation of system design on rare disease diagnostic accuracy
MIMIC-Rare RareArena RareBench
Top-1 Acc (%)Top-5  Acc (%)
Top-1 Acc (%)Top-5  Acc (%)
Top-1 Acc (%)Top-5  Acc (%)
c. Out-of-domain evaluation of system design
Top-1 Acc (%)Top-5  Acc (%)
Mendeley (Common Disease Diagnosis) 
Xinhua (Rare Disease Diagnosis) 
Vanilla model RAG SFT Deep-DxSearch 
Vanilla model RAG
SFT Deep-DxSearch 
d. LLMs-based evaluation on retrieval-augmented diagnostic reasoning
Top-1 Acc (%)Top-5  Acc (%)
In-domain Evaluation Out-of-domain Evaluation
Overall Correctness
Hallucination
Severity
Clinical Utility
Common Disease
Rare Disease
Diagnostic 
Fidelity
Reasoning 
Consistency
Overall Correctness
Clinical Utility
Overall Correctness
Clinical Utility
Overall Correctness
Clinical Utility
Common Disease
Rare Disease
Vanilla (MedGemma base) RAG (MedGemma base) Deep-DxSearch (MedGemma base)
Reasoning 
Consistency
Reasoning 
Consistency
Reasoning 
Consistency
Diagnostic 
Fidelity
Diagnostic 
Fidelity
Diagnostic 
Fidelity
Hallucination
Severity
Hallucination
Severity
Hallucination
Severity
Figure 3 | Evaluation of Deep-DxSearch system design. a. In-distribution evaluation on common disease diagnosis
comparing top-1 and top-5 accuracy among vanilla, RAG, SFT, and Deep-DxSearch approaches.b. In-distribution evaluation on
rare disease diagnosis following identical settings.c. Out-of-distribution evaluation covering both common and rare diseases.d.
Assessment of diagnostic reasoning quality using an “LLM-as-a-judge” protocol across five clinical dimensions. Scores range from
1 to 4; notably, hallucination severity is scored inversely, such that a score of 4 indicates the minimal degree of hallucination.
consistent decreases (1.6% common, 3.1% rare), validating their supportive function;(iii) excluding patient
record matchingyields the most substantial performance drop (5.5% common, 4.1% rare), underscoring the
dominant role of evidence-based matching (see Extended Data Tab. 1 for more details about the granular
progressive removal analysis). Overall, these results indicate that while similar-case retrieval serves as the
cornerstone of diagnostic accuracy, the system relies on the synergistic integration of summarized knowledge
and structured guidelines to maximize precision and coverage. For further analysis regarding the impact of
these retrieval actions on temporal efficiency, please refer to Extended Data Tab. 2.
|8

<!-- page 9 -->
 
a. Ablation study on components impact 
Top-1 Accuracy (Common Average)
Top-1 Accuracy (Rare Average)
Hint Score (Common Average)
Top-5 Accuracy (Common Average)
Top-5 Accuracy (Rare Average)
Hint Score (Rare Average)
 
full-component Deep-DxSearch w/o trajectory exploration reward
remove knowledge collection remove disease guideline 
remove patient record database
Reward-level Ablation
Retrieval corpus-level Ablation
b. Results of interpretability quantification 
Symptom Association
Differential Diagnosis
Irrelevance Exclusion
Reasoning Complexity
w/o evidence aquisition rewards w/o diagnostic accuracy reward
Figure 4 | Ablation study and interpretability analysis. a, Performance variation following stepwise removal of Deep-
DxSearch’s components. The top section evaluates reward designs: trajectory exploration, retrieve-reason, and diagnostic target
rewards. The bottom section evaluates the retrieval corpus: document summarizer, knowledge collection, disease guidelines,
and patient records. “Hint” denotes cases where the correct disease is considered during reasoning.b, Quantitative metrics for
diagnostic policy. Panels display: “Symptom association” (hit@20 for case retrieval); “Differential diagnosis” (top-5 accuracy);
“Irrelevance exclusion” (robustness to misleading evidence); and “Reasoning complexity” (average action steps). Deep-DxSearch is
compared against a “target-only” baseline trained without intermediate supervision.
Evolution of diagnostic policy.As shown in Fig. 4b, we also tracked the evolution of Deep-DxSearch’s
policy (as explained in Sec. 2.4) when comparing to a target-only baseline, Deep-DxSearch demonstrates:(i)
improved symptom association:hit@20—defined as the proportion of cases where the top-20 retrieved
patient records contain the ground-truth diagnosis—rises from 25.8% to 60.4%;(ii) differential diagnosis:
we assess the ability to identify the correct diagnosis among candidates using top-5 accuracy. While the baseline
improves moderately from 38.7% to 45%, Deep-DxSearch achieves significant increase to 71.1%, indicating a
stronger capability to distinguish the correct pathology from plausible alternatives;(iii) robustness:while
injecting with irrelevant documents during test time, Deep-DxSearch maintains a 10% accuracy gain over
the baseline;(iv) reasoning complexity:the average trajectory length increases to>5.5 steps, whereas
the baseline shrinks to∼3 steps, indicating that Deep-DxSearch learns to engage in comprehensive iterative
reasoning rather than guessing. Extended Data Fig. 2 presents further results regarding the evolution of
Deep-DxSearch’s diagnostic policy.
|9

<!-- page 10 -->
Overall Average (N=150) Common Cases (N=50)
Rare Cases (N=50) Out-of-distribution Cases (N=50)
a. Diagnostic accuracy of physicians with/without assistance
Physician Physician + DeepSeek-R1 Physician + Deep-DxSearch
b. Comparison on helpfulness to human physicians
Diagnostic Accuracy (%)
Diagnostic Accuracy (%)
Diagnostic Accuracy (%)
Diagnostic Accuracy (%)
Deep-DxSearch Both DeepSeek-R1 Both Not
c. Comparison on five clinical dimensions by physicians
Time Efficiency
Diagnostic ConfidenceClinical Safety
Clinical Utility
Reasoning Transparency
Deep-DxSearch
DeepSeek-R1
d. Step-wise human annotation on diagnostic reasoning
Overall 
Correctness
Clinical 
Utility
Reasoning
Consistency
Diagnostic
Filedity
Hallucination
Severity
Helpful Valid Redundant Factual Error
e. Holistic human impression on diagnostic reasoning
Excellent/None Good/Minor Fair/Moderate Poor/Severe
(N = 110) (N = 110)
Figure 5 | Physician-involved Evaluation Results. a, Diagnostic accuracy comparison under unaided, DeepSeek-R1-aided,
and Deep-DxSearch-aided conditions (N = 150).b, Physician preference distribution across dataset types.c, Multidimensional
clinical assessment of AI assistants.d, Expert adjudication of step-wise action validity (N = 110).e, Holistic evaluation of full
diagnostic trajectories across correctness, utility, and hallucination.
2.7 Physicians Prefer Deep-DxSearch for T ransparent Decision Support
To assess clinical utility, we conducted aphysician-in-the-loop studyinvolving three clinicians (junior,
medium, senior). The evaluation focused on two dimensions: the impact on diagnostic accuracy and the
transparency of the reasoning process.
Case preparations.To facilitate the annotation process, we developed a custom web interface (based on
Gradio) that presents extensive clinical data (EHRs) alongside Deep-DxSearch’s reasoning trajectories. The
interface delineates critical reasoning steps for assessment and allows evaluators to navigate and annotate the
diagnostic workflow flexibly, ensuring a streamlined review process.
We collaborated with an experienced clinician from Shanghai Ninth People’s Hospital, Shanghai Jiao Tong
University School of Medicine, with 8 years of clinical experience and an AI background, to curate a total of
260 test cases (with both common and rare disease), drawn from both in-distribution and out-of-distribution
sources. All diagnostic labels for these records were strictly excluded and manually verified to prevent
information leakage. This collection was split into two distinct subsets for evaluation. The first subset
(N = 150), designed for theAI assistance study, consists of raw EHRs to represent authentic clinical
encounters. It comprises 50 common and 50 rare cases from in-distribution datasets, along with 50 out-of-
|10

<!-- page 11 -->
Table 2| Five-dimensional evaluation framework for AI-assisted clinical diagnosis (Score 1–5) with “3” denotes the medium level.
Dimension Score Criteria Description
Reasoning Transparency Low (1-2)Opaque logic; contradictions; vague or hallucinated evidence.High (4-5)Clear reasoning steps; perfect evidence chain anchored to verifiable sources.
Clinical Utility Low (1-2)Irrelevant noise; generic textbook knowledge without patient specificity.High (4-5) Highlights overlooked symptoms; provides consultant-level insight that optimizes decisions.
Diagnostic Confidence Low (1-2)Physician rejects advice or requires rigorous cross-verification.High (4-5)Physician trusts the output; willing to adopt diagnosis as primary basis.
Clinical Safety Low (1-2)Missed life-threatening conditions; contraindicated actions; major errors.High (4-5)Safe; compliant with standard care; actively flags contraindications.
Time Efficiency Low (1-2)System response>30 seconds.High (4-5)System response<20 seconds.
distribution cases from the Xinhua-Rare dataset. The second subset (N = 110), spanning both common
and rare diseases, was employed for thereasoning evaluation. For these cases, we preserved the complete
inference trajectories, including inputs, intermediate retrieval-reasoning steps, and ground truth, to facilitate
granular expert adjudication.
Study-I: impact on AI assistance in clinical decision-making.Three physicians—senior (>10 years),
medium (8 years), and junior (6 years)—performed diagnoses underunassistedandAI-assistedconditions
(using DeepSeek-R1 vs. Deep-DxSearch). To minimize carryover effects, the assistance order was randomized,
and physicians were required to justify rational of their model preferences. As shown in Fig. 5a, the average
physician accuracy reached 69.1% when aided by Deep-DxSearch, exceeding the 45.6% unassisted baseline and
the 60.9% achieved with DeepSeek-R1. Notably, for OOD cases, Deep-DxSearch assistance yielded an accuracy
of 67.3% compared to 44.0% (unassisted) and 58.7% (DeepSeek-R1). Physicians also rated their preference on
common, rare, and OOD datasets (Fig. 5b), where Deep-DxSearch clearly shows stronger preference than
DeepSeek-R1 or without AI assistance. In a multi-dimensional assessment with metrics shown in Tab. 2,
Deep-DxSearch scored significantly higher than DeepSeek-R1 inreasoning transparency(4.2 vs. 3.3) and
clinical utility(4.5 vs. 3.2), although it received lower scores fortime efficiency(2.0 vs. 4.0) due to the
time load required to review the retrieved evidence evidence, as shown in Fig. 5c.
Study-II: evaluation of diagnostic reasoning steps.To validate the intermediate reasoning process, the
model’s outputs of the sampled 110 cases are decomposed into 942 distinct action steps (<reason>, <lookup>,
<match>, <search>, <diagnose>). Three independent clinicians (junior, medium, senior) evaluated these
steps as either “factual error”, “redundant” (correct but unnecessary), “valid” (logical and grounded), or
“helpful” (key reference). Results (Fig. 5d) indicate a high density of useful information: steps rated as “helpful”
comprised 34.9% of <reason> steps, 46.3% of <lookup>, and 76.1% of<diagnose> steps. The combined
proportion of “valid” and “helpful” steps reached 99.3% for<reason>and 98.8% for<lookup>.
Study-III: holistic reasoning evaluation.Physicians further evaluated full diagnostic trajectories with
the same rubric as “LLM-as-judge”. As shown in Fig. 5e, Deep-DxSearch was rated as “excellent” in overall
correctness for 59.1% of cases. Additionally, 61.8% of trajectories were deemed to have high clinical utility,
and 66.7% were consideredfree fromhallucinations. To strictly validate the reliability of these evaluations, we
calculated thepositive percent agreement (PPA)averaged among three physicians based on binarized
outcomes (positive: score 3–4 vs. negative: score 1–2). The analysis reveals a strong consensus among
evaluators, yielding PPA values of 96.7% for overall correctness, 96.1% for clinical utility, 98.7% for reasoning
consistency, 95.5% for reference information relevance, and 99.7% for hallucination severity.
2.8 F ailure Analysis
To elucidate the limitations, we conducted a failure analysis on 216 cases—defined as instances where the
correct diagnosis was absent from the model’s top-5 predictions—stratified evenly between common (n = 108)
and rare (n = 108) diseases. We established a taxonomy of failure modes comprising four domains subdivided
into 12 specific categories:(i) clinical input ambiguity(including insufficient details, atypical presentation,
and debatable ground truth);(ii) information retrieval issues(failure to identify key features, retrieval
|11

<!-- page 12 -->
Clinical Input Ambiguity Diagnostic Strategy Failures
Reasoning & Synthesis Errors Information Retrieval Issues 
Insufficient 
Clinical Details
Atypical Clinical 
Presentation
Debatable 
Ground Truth
Premature 
Diagnostic Closure
Incorrect 
Diagnostic Pathway
Ineffective Infor-
mation Seeking
Failures to Identify 
Key Features
Retrieval Noise 
& Distraction
Knowledge Gap 
in Database
Dismissal of 
Valid Evidence
Forced Association 
& Hallucination
Failed Differential 
Diagnosis
b. Failure reasoning annotation results on 216 cases by physicians
common disease diagnosis (N=108) rare disease diagnosis (N=108)
Failure Cases
<Reason> 
<Retrieve> 
<Diagnose> 
...
...
Clinical Input
Ambiguity
Diagnostic
Strategy Failures
Information 
Retrieval Issues
Reasoning &
Synthesis Errors
Physicians Eval
Failure Reason Taxonomy
...
a. Failure reason evaluation framework
Figure 6 | Failure Analysis. a, Schematic of the physician-led evaluation framework and taxonomy used to categorize
diagnostic errors into four primary domains.b, Quantitative comparison of failure reasons for common (N = 108) and rare
(N = 108) disease cases across twelve specific error types. Error bars represent the deviation among the three physician evaluators.
noise, and database knowledge gaps);(iii) diagnostic strategy failures(premature closure, incorrect
pathway, and ineffective information seeking); and(iv) reasoning & synthesis errors(dismissal of valid
evidence, hallucination, and failed differential diagnosis). Three external physicians with varying seniority (6
to>10 years of experience across three tertiary hospitals) adjudicated the primary factor(s) contributing to
the diagnostic failure for each case (Fig. 6a).
Failure pattern in common disease diagnosis.Failures in common diseases stemmed primarily from
clinical input ambiguity and retrieval issues (Fig. 6b). Notably, “debatable ground truth” accounted for
40 cases (vs. 15.3 in rare diseases), suggesting the model’s diagnosis was often clinically justifiable despite
differing from the label. Similarly, “failure to identify key features” was the dominant retrieval error (20 vs. 15
cases), indicating challenges in prioritizing symptoms.
Failure pattern in rare disease diagnosis.Conversely, failures in rare disease were driven by diagnostic
strategy and reasoning errors. “Premature diagnostic closure” (finalizing diagnosis without sufficient evidence)
occurred in 31 cases, surpassing the 24 observed in common diseases. Additionally, “failed differential
diagnosis” (errors in distinguishing competing hypotheses) was identified in 18.7 cases (vs. 12 for common),
highlighting deficits in managing complex knowledge.
These results reveal distinct failure modes: common disease diagnosis is hindered by input noise and retrieval
precision, whereas rare disease diagnosis suffers from strategic reasoning deficits. This divergence explains
the observed performance disparities and underscores the need for both cleaner retrieval corpora and robust
reasoning synthesis.
|12

<!-- page 13 -->
3 DISCUSSION
The integration of artificial intelligence into clinical diagnostics has historically been constrained by a
dichotomy: the “black box” opacity of deep learning versus the hallucination risks inherent in generative
large language models (LLMs). In this study, we introduce Deep-DxSearch, a framework that transitions
diagnostic AI from static classification to dynamic, agentic inquiry. By coupling a massive medical retrieval
environment with a policy optimized via reinforcement learning, our system demonstrates that mimicking
the hypothetico-deductive process of human clinicians—rather than merely predicting the next token—yields
superior diagnostic accuracy and generalization.
From pattern matching to deliberative reasoning. A critical finding of our work is the limitation
of standard Supervised Fine-Tuning (SFT) for complex diagnostics. While SFT improves in-distribution
performance, our results show it often degrades on out-of-distribution cohorts (e.g., Xinhua-Rare), suggesting a
tendency to memorize specific disease-symptom associations. In contrast, Deep-DxSearch, trained via agentic
reinforcement learning, learns a transferablediagnostic policy. This aligns with the cognitive distinction
between System 1 (fast, intuitive) and System 2 (slow, deliberative) thinking. By explicitly rewarding the
acquisition of valid evidence and the exploration of diverse search trajectories, Deep-DxSearch effectively
implements evidence-based reasoning. This allows the agent to navigate unseen clinical environments with a
robustness that standard RAG and SFT approaches lack, bridging the gap between rigid heuristic workflows
and purely generative models.
Addressing the long-tail of rare diseases. Rare diseases represent a distinct challenge due to their
low prevalence and phenotypic complexity, often resulting in a “diagnostic odyssey” for patients. Existing
benchmarks, such as the RareArena dataset, highlight the struggle of current foundation models to identify
these conditions due to the sparsity of training data. Deep-DxSearch significantly advances this frontier,
achieving substantial accuracy gains over strong baselines like GPT-4o and DeepSeek-R1 in rare disease cohorts.
This performance leap is attributable to the system’s ability to anchor reasoning in retrieved, validated cases
via the<match>primitive. By referencing a database of over 170k patient records rather than relying solely
on parametric memory, our model mitigates the “long-tail” forgetting problem. However, our failure analysis
indicates that challenges remain; specifically, the model occasionally exhibits “premature closure”, finalizing
diagnoses before fully exploring latent pathologies. This suggests that future iterations must enforce even
more rigorous differential diagnosis protocols before the agent is permitted to conclude a case.
Clinical utility and the transparency trade-off. The ultimate measure of a diagnostic tool is its utility
in human-AI collaboration. Our physician-in-the-loop study demonstrates that Deep-DxSearch not only
improves diagnostic accuracy (69.1% assisted vs. 45.6% unassisted) but also fosters trust through transparency.
Unlike opaque predictions, the explicit action steps (e.g.,<lookup>, <search>) provide an audit trail that
physicians rated highly for reasoning transparency. It is notable that this deliberative process resulted in
lower ratings for time efficiency compared to direct-answer models. In the context of high-stakes medicine,
we argue this is a necessary trade-off: the “glass box” nature of Deep-DxSearch offers a safeguard, allowing
clinicians to verify the evidence chain before accepting an AI’s conclusion. This shifts the role of the AI from
an oracle to a transparent research assistant, aligning with the requirements of evidence-based medicine.
Limitations and future directions. Our study has limitations that outline the path for future research.
First, while the retrieval corpus is extensive, it is not exhaustive; “database knowledge gaps” were identified
as a contributing factor to errors. Real-world viability will require mechanisms for continuous, automated
updating of the knowledge base to reflect the latest biomedical literature.Second, the current modality is
text-only. Clinical diagnosis is inherently multimodal, often relying on radiology, pathology, and genomics.
Extending the agentic framework to process multimodal evidence is a critical next step.Finally, while
hallucination severity was significantly reduced, it was not eliminated. The persistence of synthesis errors
suggests that even with perfect retrieval, the reasoning engine requires further refinement to ensure logical
consistency in complex scenarios.
Conclusion. Deep-DxSearch establishes a new standard for automated diagnosis by formalizing the clinical
workflow as a reinforcement learning problem. By prioritizing theprocessof reasoning over the immediate
output, we provide a blueprint for the next generation of medical AI: systems that are not only accurate but
also transparent, verifiable, and aligned with the rigorous standards of clinical practice.
|13

<!-- page 14 -->
4 METHODS
In this section, we aim to provide the details for developing Deep-DxSearch, starting from the construction of
the medical retrieval ecosystem and the automated pipeline used to curate high-fidelity clinical data. Next,
we formulate the diagnostic task as a sequential decision-making process, defining the agent-environment
interaction dynamics. Finally, we outline the composite reward mechanism and the reinforcement learning
strategies employed to optimize the system for active, evidence-driven inquiry.
4.1 Dataset Description and Statistics
To construct a comprehensive ecosystem comprising training datasets, evaluation benchmarks, and retrieval
corpora, the curation process involved aggregating diverse clinical resources from eight primary sources,
applying a rigorous automated processing pipeline, and validating data quality through expert review.
Data Sources
The foundation of our study rests on a diverse collection of large-scale clinical narratives used for model
training and patient record retrieval. We aggregated Electronic Health Records (EHRs) and case reports from
four primary sources: MIMIC-IV [49], comprising 332k de-identified discharge summaries from Beth Israel
Deaconess Medical Center; PMC-Patients [50], which provides 250k patient profiles derived from biomedical
literature in PubMed Central; and MedDialog [51], containing 257k clinical consultations from online platform.
To enhance rare disease coverage, we incorporated the dataset from Xinhua Hospital [53], a proprietary
in-house collection of 352k diagnostic records spanning a decade (2014–2025).
To support specific diagnostic tasks, we integrated specialized benchmark datasets. RareArena2 provided
approximately 50,000 cases specifically curated for rare disease screening and confirmation. RareBench [43]
contributed 1,122 cases aggregated from RAMEDIS, MME, HMS, and LIRICAL. We also employed the
Mendeley dataset [52], a structured resource of binary disease-symptom associations released in June 2025.
Finally, to curate the retrieval corpus, we integrated structured taxonomies (ICD-10-CM, Orphanet). For
unstructured evidence, we aggregated 23.9 million PubMed abstracts, 3.31 million Wikipedia entries, 18
authoritative medical textbooks, and 1,419 distinct web resources (e.g., specific sections from NCBI, NHS) for
further processing. More details and licensing information are provided in Supplementary.
Data Processing and Curation Pipeline
Raw clinical data from the sources listed above (excluding the pre-structured Mendeley and RareBench
datasets) went through a four-stage processing pipeline to ensure high fidelity and standardization.
Stage-I: disease classification.Cases were split into “common” and “rare” categories based on the
Orphanet ontology. A condition was classified as rare if it was listed in the Orphanet database or possessed
a BioLORD [54] semantic embedding similarity of> 0.95with a known entry. For structured data (e.g.,
MIMIC-IV), we utilized ICD-to-Orphanet cross-referencing. For unstructured datasets (e.g., PMC-Patients,
MedDialog), we implemented a rigorous annotation pipeline: candidate diagnoses were first extracted via a
consensus of Large Language Models (GPT-4o and DeepSeek) and subsequently verified against the Orphanet
definition via BioLORD embeddings. Existing rare disease benchmarks (RareArena, RareBench) retained
their native classifications.
Stage-II: pre-filtering.To mitigate noise inherent in large-scale datasets, we employed GPT-4o to screen
raw cases with strict criteria. We removed the ones that lack causal logic, where the diagnosis contradicted or
preceded the clinical presentation; narrative incoherence, such as garbled text or administrative metadata; and
information insufficiency, where the record lacked substantial clinical history. For the RareArena, RareBench
and Mendeley dataset, which were pre-curated using similar protocols, we bypassed this step to avoid
redundancy.
Stage-III: extraction and stratification.We adopted GPT-4o to extract confirmed diagnoses and
phenotypes using a robust two-step prompting strategy to ensure fidelity and prevent information leakage.
First, we employedextraction with reflection, using Chain-of-Thought to distinguish active symptoms from
medical history while pinpointing the definitive diagnosis. Second, we enforcedconsistency verification,
2https://github.com/zhao-zy15/RareArena
|14

<!-- page 15 -->
Table 3 | Manual verification of data quality.Evaluation results from a stratified sample of 150 cases reviewed by senior
physicians. “Overall ACC” denotes the proportion of cases where both diagnosis and symptom extraction were error-free.
Metric MIMIC-Common PMC-Patients MIMIC-Rare RareArena Xinhua-Rare
Sample Size25 25 25 25 50
Overall Accuracy23/25 (92.0%) 23/25 (92.0%) 25/25 (100.0%) 24/25 (96.0%) 48/50 (96.0%)
Disease Label Accuracy24/25 (96.0%) 25/25 (100.0%) 25/25 (100.0%) 24/25 (96.0%) 50/50 (100.0%)
Symptom Recall208/218 (95.4%) 175/208 (84.1%) 254/254 (100.0%) 190/210 (90.5%) 201/215 (93.5%)
Symptom Precision208/219 (95.0%) 175/180 (97.2%) 254/269 (94.4%) 190/195 (97.4%) 201/219 (91.8%)
Data Integrity (No Leakage)24/25 (96.0%) 24/25 (96.0%) 22/25 (88.0%) 25/25 (100.0%) 50/50 (100.0%)
ICD-10 Accuracy21/25 (84.0%) 22/25 (88.0%) - - -
ORPHA Accuracy- - 29/36 (80.6%) 22/25 (88.0%) 45/50 (90.0%)
HPO Accuracy203/219 (92.7%) 172/180 (95.6%) 251/269 (93.3%) 181/195 (92.8%) 207/219 (94.5%)
cross-referencing extracted entities against the source text to flag unsupported elements. We then applied
strict quality criteria: (i) diseases must be well-defined clinical entities rather than vague qualifiers or simple
symptoms; (ii) phenotypes must be distinctive and not merely restate the diagnosis to strictly exclude label
leakage; and (iii) demographic context must align with the case. Cases satisfying these rigorous standards
were designated fortraining and evaluation, while valid clinical records lacking this specific structural
precision were reallocated to the patient record database to preserve real-world diversity.
Stage-IV: terminology normalization.The extracted entities were normalized to standard ontologies
via BioLORD embedding similarity. Phenotypes were mapped to the Human Phenotype Ontology (HPO),
common diseases to ICD-10-CM, and rare diseases to Orphanet (ORPHA).
Stage-V: manual verification of data quality.To validate the reliability of the automated pipeline, a
panel of three senior physicians, with experience ranging from 6 to 10 years, reviewed a set of random sample
of 150 cases. The review protocol assessedtwo primary dimensions: validity, ensuring extracted symptoms
and ontology mappings were clinically accurate; and completeness, verifying that no critical diagnostic clues
were omitted or leaked. As shown in Tab. 3, the pipeline achieves high fidelity:disease label accuracy
reaches 98.7% (148/150), whilesymptom extractionconsistently maintains both precision and recall above
90%. Theoverall accuracy(cases free from extraction errors) stands at 95.3% (143 /150). Note that,
to ensure rigorous benchmarking, the manual validation was extended to the entire test set, guaranteeing
high-quality ground-truth for all reported metrics.
Final Dataset Components and Statistics
In this section, we start by detailing the retrieval corpus, followed by the training and evaluation datasets for
model development.
Medical retrieval corpus.The retrieval corpus integrates diverse medical knowledge to mitigate coverage
gaps, encompassingbothcommonandrarediseasesthroughthreemajorcomponents:(i)diseaseinformation
guideline. This component contains a structured knowledge base to support evidence-based reasoning,
including disease-symptom guideline for 16,371 diseases. For rare diseases, we integrated expert-curated
phenotype data from Orphanet; for common diseases, we utilized DeepSeek-V3 to summarize symptom
profiles from authoritative web sources (e.g., Mayo Clinic, NIH). In total, this component contains 257,022
disease–phenotype/symptom pairs (142,141 common; 114,881 rare), as each disease may correspond to multiple
symptoms. Each item is mapped to standard ICD, ORPHA, and HPO terminologies, and the dataset achieves
complete coverage of ICD codes (to one decimal place) and 38.68% coverage of ORPHA codes, with over 50%
of HPO terms included;(ii) patient record database. To enable similar-case retrieval, we constructed a
massive repository with 155,442 patient records, with the disease distribution following a long-tailed pattern
across 14 major body systems [55]. This database comprises validated diagnoses, clinical presentations, and
medication histories, that met quality standards but were not selected for the training set, ensuring the
retrieval corpus retains the diversity of real-world distributions without leaking ground-truth training data.
The final database integrates 44,821 cases from MIMIC-IV, 49,633 from PMC-Patients, 6,414 from MedDialog,
46,518 from RareArena, and 324 from RareBench;(iii) clinical knowledge collection. To provide broad
semantic coverage, we incorporated 3.31 million biomedical documents from Wikipedia, 23.9 million PubMed
articles, entries into chunks of 1,000 characters to facilitate dense retrieval.
|15

<!-- page 16 -->
Training & evaluation dataset.We curated a diverse cohort of 24,142 clinical cases, comprising clinical
presentations paired with confirmed diagnoses from seven sources spanning America, Asia, and Europe.
Following strict quality control for clarity and causality, cases were categorized into common and rare
disease groups using the Orphanet coding system. Common diseases constitute 73.1% of the cohort, drawn
from MIMIC-C (7,257), PMC-Patients (6,421), MedDialog (3,206), and Mendeley (757). The remaining
26.9% represents rare diseases, sourced from RareArena (3,242), MIMIC-R (2,184), RareBench (277) and
Xinhua-Rare (798). This collection exhibits noteable phenotypic diversity, averaging 4–12 symptoms per
case and covering over 3,000 distinct diseases. The fivein-distributiondatasets (MIMIC, PMC-Patients,
MedDialog, RareArena, and RareBench) were partitioned at a 3:1 ratio for training and evaluation. To assess
generalization to unseen data sources, the remaining two datasets, Mendeley [52] and Xinhua-Rare [53], were
reserved exclusively forout-of-distributionzero-shot evaluation.
4.2 Agentic RAG F ramework
We model the clinical diagnostic process as a partially observable Markov Decision Process (MDP) within a
reinforcement learning (RL) framework. This system comprises two primary components: anLLM-based
agent(policy Mθ), responsible for step-wise decision-making; and anexternal environment(E), denoting
the medical knowledge base (e.g., disease guidelines, patient records and other medical knowledge). The
objective is therefore to optimize the policyMθ to generate a diagnostic trajectory that maximizes both
process validity (correct evidence gathering) and diagnostic accuracy.
Action space.To simulate clinical reasoning, we define the action spaceA as having both retrieval and
reasoning. The agent can select from five atomic operations:(i) internal processing.⟨reason⟩ allows the
agent to synthesize current evidence and update hypotheses;⟨diagnose⟩ is the terminal action where the
agent commits to a final diagnosis;(ii) external retrieval. The agent acts as a query generator for specific
tools. ⟨lookup⟩ queries disease guidelines;⟨match⟩ retrieves similar patient cases based on phenotype lists;
and⟨search⟩performs free-text queries for general medical knowledge.
Interaction dynamics.At each step, the agent is trained to generate a tupleat = (αt, τt) =Mθ(St−1),
where αt denotes the action type andτt represents the textual content (e.g., a search query or reasoning
thought), where St−1 = {S0, a1, f1, . . . , at−1, ft−1}, containing the patient’s clinical presentation (S0),e.g.,
symptoms, history, and examination findings, the accumulated trajectory of prior actions and observations
until stept− 1. If the action denotes external retrieval, the environment will then execute the query and return
the search results or similar case,i.e.,ft = E(αt, τt), and the state is then updated toSt = St−1 ∪ {at, ft}.
The process repeats until the terminal⟨diagnose⟩action is issued.
4.3 Reward Mechanism
To steer the model toward transparent and accurate diagnostics, we designed a composite reward function
that balances structural adherence, exploration diversity, evidence quality, and final diagnosis accuracy.
Format alignment reward (σf).To ensure the agent strictly follows clinical protocols, we employ a binary
gating coefficient, σf. This coefficient is set to 1 only if the output strictly adheres to all formatting constraints
(e.g., correct tag pairing, valid iteration structure) and 0 otherwise. Any violation nullifies the reward for the
entire trajectory, enforcing rigid adherence to the task specification.
Trajectory exploration reward (σdiv).To prevent the model from collapsing into repetitive, deterministic
diagnostic pathways, we penalize over-represented action sequences. We calculate the frequency ratior of the
current trajectory within the training population. The diversity coefficient is defined as:
σdiv =
(
1−r,ifr > τ freq,
1,otherwise. (1)
whereτ freq is a threshold for allowable repetition.
Evidence acquisition rewards.We incentivize high-quality information gathering through two components:
(i) patient matching (σm). This reward encourages the agent to iteratively refine phenotype or symptom
|16

<!-- page 17 -->
queries to find similar past cases. A positive reward (+0.5) is granted if a retrieved case matches the
ground-truth diagnosis. To promote efficiency, a penalty is applied for each<match> operation (−0.1, capped
at−0.3). Furthermore, to ensure meaningful iteration,σm is zeroed if the agent fails to vary the phenotype
set between consecutive queries (at least two phenotypes must change);(ii) search relevance (σs).We
quantify the relevance of general queries by calculating the token-level overlap between the retrieved disease
terms and the ground-truth, hereby encouraging the model to propose correct or relevant candidates that
may facilitate the final answer. Letfmatch be the fraction of matched tokens; the reward is scaled non-linearly
to encourage partial matches early in training:σs = 3√fmatch.
Diagnosticaccuracyreward( σd).Thefinalcomponentevaluatesthecorrectnessofthecommitteddiagnosis,
diseases highlighted in the answer (with the special format as\textbf{}within⟨diagnose⟩...⟨/diagnose⟩).
We compute a token-level similarity score between the predicted diagnosis and the ground-truth,i.e.,simdiag.
This is linearly rescaled to[0.2, 0.8]and adjusted by the accumulated matching rewardσm, which can either
increase the reward (for correct matching and reasoning) or decrease it (to penalize excessive or redundant
matching and insufficient diversity):
σd = 0.2 + 0.6·simdiag +σ m (2)
This formulation explicitly links the final reward to the quality of the preceding evidence-gathering process.
Total rewards.The final optimization signalσtotal is a weighted sum of component rewards, gated by format
validity and modulated by diversity:
σtotal =clip[0,1] [σ f ·σ div ·(w mσm +w sσs +w dσd)](3)
4.4 T raining Implementation
To incorporate the tailored reward mechanism into workflow optimization, we adopt the following training
methods regime.
Interleaved agent-environment rollout.Unlike standard language model training, our framework requires
dynamic interaction during sequence generation. We implemented an inference engine that halts generation
upon detecting tool invocation tokens (e.g.,⟨lookup⟩). The system extracts the query, retrieves information
from external servers (e.g., Wikipedia, PubMed, and medical guidelines), and uses a dedicated summarization
model (Qwen-3-235B) to synthesize the retrieved documents. This feedback is appended to the context, and
generation resumes.
Group Relative Policy Optimization (GRPO).We optimize the policy using GRPO. For each queryq,
we sample a group ofG outputs {ci}Gi=1 from the old policyMθold. The group-relative advantage is computed
by standardizing the rewards within the group:ˆAi = (Ri −mean ({R}))/std({R}). The optimization objective
is to minimize the following loss function, which incorporates token-level likelihood updates and KL-divergence
regularization against a reference modelMref:
LGRPO(θ) =Eq,{ci}∼Mθold

 1
G
GX
i=1
1
|ci|
|ci|X
t=1

− ˆAi logM θ(ci,t|q, ci,<t) +βDKL(Mθ||Mref)


 (4)
Multi-stage reward adaptation.To address the competing objectives of retrieval and diagnosis, we
employed a multi-stage training strategy. We observed that optimizing all rewards simultaneously led to
suboptimal convergence. Therefore, we sequentially prioritized objectives:stage 1–3:we individually targeted
σs, σm, and σd in sequence. In each stage, the target component’s weight was set to 0.9, while others were
dampened to 0.05;stage 4:we balanced the weights (ws = 0.3, wm = 0.3, wd = 0.4) for joint optimization.
Notably, prioritizing the patient matching reward (σm) in intermediate stages yielded greater improvements
in final diagnostic accuracy than focusing solely on the diagnostic outcome, validating the hypothesis that
robust evidence gathering is a prerequisite for accurate clinical decision-making.
|17

<!-- page 18 -->
References
[1] Karan Singhal, Shekoofeh Azizi, Tao Tu, S Sara Mahdavi, Jason Wei, Hyung Won Chung, Nathan
Scales, Ajay Tanwani, Heather Cole-Lewis, Stephen Pfohl, et al. Large language models encode clinical
knowledge.Nature, 620(7972):172–180, 2023. 1, 4
[2] Paul Hager, Friederike Jungmann, Robbie Holland, Kunal Bhagat, Inga Hubrecht, Manuel Knauer, Jakob
Vielhauer, Marcus Makowski, Rickmer Braren, Georgios Kaissis, et al. Evaluation and mitigation of the
limitations of large language models in clinical decision-making.Nature medicine, 30(9):2613–2622, 2024.
1
[3] Pengcheng Qiu, Chaoyi Wu, Shuyu Liu, Yanjie Fan, Weike Zhao, Zhuoxia Chen, Hongfei Gu, Chuanjin
Peng, Ya Zhang, Yanfeng Wang, et al. Quantifying the reasoning abilities of llms on clinical cases.Nature
Communications, 16(1):9799, 2025. 1
[4] Chengfeng Dou, Chong Liu, Fan Yang, Fei Li, Jiyuan Jia, Mingyang Chen, Qiang Ju, Shuai Wang,
Shunya Dang, Tianpeng Li, et al. Baichuan-m2: Scaling medical capability with large verifier system.
arXiv preprint arXiv:2509.02208, 2025. 1, 4
[5] Zeming Chen, Alejandro Hernández Cano, Angelika Romanou, Antoine Bonnet, Kyle Matoba, Francesco
Salvi, Matteo Pagliardini, Simin Fan, Andreas Köpf, Amirkeivan Mohtashami, et al. Meditron-70b:
Scaling medical pretraining for large language models.arXiv preprint arXiv:2311.16079, 2023. 1, 5
[6] Emma Croxford, Yanjun Gao, Elliot First, Nicholas Pellegrino, Miranda Schnier, John Caskey, Madeline
Oguss, Graham Wills, Guanhua Chen, Dmitriy Dligach, et al. Evaluating clinical ai summaries with
large language models as judges.npj Digital Medicine, 8(1):640, 2025. 1, 5
[7] Chaoyi Wu, Jiayu Lei, Qiaoyu Zheng, Weike Zhao, Weixiong Lin, Xiaoman Zhang, Xiao Zhou, Ziheng
Zhao, Ya Zhang, Yanfeng Wang, et al. Can gpt-4v (ision) serve medical applications? case studies on
gpt-4v for multimodal medical diagnosis.arXiv preprint arXiv:2310.09909, 2023. 1
[8] Elham Asgari, Nina Montaña Brown, Magda Dubois, Saleh Khalil, Jasmine Balloch, Joshua Au Yeung,
and Dominic Pimenta. A framework to assess clinical safety and hallucination rates of llms for medical
text summarisation.NPJ Digital Medicine, 8, 2025. 1
[9] Yusheng Liao, Chaoyi Wu, Junwei Liu, Shuyang Jiang, Pengcheng Qiu, Haowen Wang, Yun Yue, Shuai
Zhen, Jian Wang, Qianrui Fan, et al. Ehr-r1: A reasoning-enhanced foundational language model for
electronic health record analysis.arXiv preprint arXiv:2510.25628, 2025. 1
[10] Xiaohong Liu, Hao Liu, Guoxing Yang, Zeyu Jiang, Shuguang Cui, Zhaoze Zhang, Huan Wang, Liyuan
Tao, Yongchang Sun, Zhu Song, Tianpei Hong, Jin Yang, Tianrun Gao, Jiangjiang Zhang, Xiaohu Li,
Jing Zhang, Ye Sang, Zhao Yang, Kanmin Xue, Song Wu, Ping Zhang, Jian Yang, Chunli Song, and
Guangyu Wang. A generalist medical language model for disease diagnosis assistance.Nature medicine,
2025. 1, 4
[11] James Zou and Eric J Topol. The rise of agentic ai teammates in medicine.The Lancet, 405(10477):457,
2025. 1
[12] Jianing Qiu, Kyle Lam, Guohao Li, Amish Acharya, Tien Yin Wong, Ara Darzi, Wu Yuan, and
Eric J Topol. Llm-based agentic systems in medicine and healthcare.Nature Machine Intelligence,
6(12):1418–1420, 2024. 1
[13] Tao Tu, Anil Palepu, Mike Schaekermann, Khaled Saab, Jan Freyberg, Ryutaro Tanno, Amy Wang,
Brenna Li, Mohamed Amin, Nenad Tomasev, et al. Towards conversational diagnostic ai.arXiv preprint
arXiv:2401.05654, 2024. 1
[14] Pengcheng Qiu, Chaoyi Wu, Junwei Liu, Qiaoyu Zheng, Yusheng Liao, Haowen Wang, Yun Yue, Qianrui
Fan, Shuai Zhen, Jian Wang, et al. Evolving diagnostic agents in a virtual clinical environment.arXiv
preprint arXiv:2510.24654, 2025. 1
|18

<!-- page 19 -->
[15] OpenAI. Introducing ChatGPT Health, oct 2024. Accessed: 2026-01-26. 1
[16] Anthropic. Advancing Claude in healthcare and the life sciences, jan 2026. Accessed: 2026-01-26. 1
[17] OpenEvidence. The leading medical information platform, 2026. Accessed: 2026-01-26. 1
[18] Gordon Guyatt, John Cairns, David Churchill, Deborah Cook, Brian Haynes, Jack Hirsh, Jan Irvine,
Mark Levine, Mitchell Levine, Jim Nishikawa, et al. Evidence-based medicine: a new approach to teaching
the practice of medicine.jama, 268(17):2420–2425, 1992. 1
[19] Gordon Guyatt, Drummond Rennie, and S Satya-Murti. Users’ guides to the medical literature: a manual
for evidence-based clinical practice.JAMA-Journal of the American Medical Association-International
Edition, 287(11):1463, 2002. 1
[20] Steven Tenny and Matthew A. Varacallo. Evidence-based medicine. InStatPearls [Internet]. StatPearls
Publishing, Treasure Island (FL), jan 2025. Updated 2024 Sep 10. 1
[21] Sarah Sandmann, Stefan Hegselmann, Michael Fujarski, Lucas Bickmann, Benjamin Wild, Roland Eils,
and Julian Varghese. Benchmark evaluation of deepseek large language models in clinical decision-making.
Nature Medicine, pages 1–1, 2025. 1
[22] Duy Khoa Pham and Quoc Bao Vo. Towards reliable medical question answering: Techniques and
challenges in mitigating hallucinations in language models.ArXiv, abs/2408.13808, 2024. 1
[23] Binxu Li, Tiankai Yan, Yuanting Pan, Jie Luo, Ruiyang Ji, Jiayuan Ding, Zhe Xu, Shilong Liu, Haoyu
Dong, Zihao Lin, and Yixin Wang. MMedAgent: Learning to use medical tools with multi-modal
agent. In Yaser Al-Onaizan, Mohit Bansal, and Yun-Nung Chen, editors,Findings of the Association
for Computational Linguistics: EMNLP 2024, pages 8745–8760, Miami, Florida, USA, November 2024.
Association for Computational Linguistics. 2
[24] Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia, Jinliu Pan, Yuxi Bi, Yixin Dai, Jiawei Sun, Haofen
Wang, and Haofen Wang. Retrieval-augmented generation for large language models: A survey.arXiv
preprint arXiv:2312.10997, 2(1), 2023. 2
[25] Guangzhi Xiong, Qiao Jin, Zhiyong Lu, and Aidong Zhang. Benchmarking retrieval-augmented generation
for medicine. InFindings of the Association for Computational Linguistics ACL 2024, pages 6233–6251,
2024. 2, 4, 5, 29
[26] AditiSingh, AbulEhtesham, SaketKumar, andTalaTalaeiKhoei. Agenticretrieval-augmentedgeneration:
A survey on agentic rag.arXiv preprint arXiv:2501.09136, 2025. 2
[27] Junde Wu, Jiayuan Zhu, Yunli Qi, Jingkun Chen, Min Xu, Filippo Menolascina, and Vicente Grau.
Medical graph rag: Towards safe medical large language model via graph retrieval-augmented generation.
arXiv preprint arXiv:2408.04187, 2024. 2
[28] Peng Xia, Kangyu Zhu, Haoran Li, Tianze Wang, Weijia Shi, Sheng Wang, Linjun Zhang, James Zou,
and Huaxiu Yao. Mmed-rag: Versatile multimodal rag system for medical vision language models.arXiv
preprint arXiv:2410.13085, 2024. 2
[29] Ran Xu, Wenqi Shi, Yue Yu, Yuchen Zhuang, Yanqiao Zhu, May Dongmei Wang, Joyce C. Ho, Chao
Zhang, and Carl Yang. Bmretriever: Tuning large language models as better biomedical text retrievers.
ArXiv, abs/2404.18443, 2024. 2, 4
[30] Julien Delile, Srayanta Mukherjee, Anton Van Pamel, and Leonid Zhukov. Graph-based retriever captures
the long tail of biomedical knowledge.ArXiv, abs/2402.12352, 2024. 2, 4
[31] Simone Kresevic, Mauro Giuffrè, Milos Ajcevic, Agostino Accardo, Lory S Crocè, and Dennis L Shung.
Optimization of hepatological clinical guidelines interpretation by large language models: a retrieval
augmented generation-based framework.NPJ digital medicine, 7(1):102, 2024. 2
|19

<!-- page 20 -->
[32] Kimberly LeBlanc, Emily Glanton, Anna Nagy, Jorick Bater, Tala Berro, Molly A McGuinness, Courtney
Studwell, Undiagnosed Diseases Network, and Matthew Might. Rare disease patient matchmaking:
development and outcomes of an internet case-finding strategy in the undiagnosed diseases network.
Orphanet journal of rare diseases, 16(1):210, 2021. 2
[33] Shreya Johri, Jaehwan Jeong, Benjamin A Tran, Daniel I Schlessinger, Shannon Wongvibulsin, Leandra A
Barnes, Hong-Yu Zhou, Zhuo Ran Cai, Eliezer M Van Allen, David Kim, et al. An evaluation framework
for clinical use of large language models in patient interaction tasks.Nature medicine, 31(1):77–86, 2025.
2
[34] Aaron Hurst, Adam Lerer, Adam P Goucher, Adam Perelman, Aditya Ramesh, Aidan Clark, AJ Ostrow,
Akila Welihinda, Alan Hayes, Alec Radford, et al. Gpt-4o system card.arXiv preprint arXiv:2410.21276,
2024. 2, 4
[35] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Peiyi Wang, Qihao Zhu, Runxin Xu, Ruoyu
Zhang, Shirong Ma, Xiao Bi, et al. Deepseek-r1 incentivizes reasoning in llms through reinforcement
learning.Nature, 645(8081):633–638, 2025. 2, 4, 5
[36] Zeming Chen, Alejandro Hern’andez Cano, Angelika Romanou, Antoine Bonnet, Kyle Matoba, Francesco
Salvi, Matteo Pagliardini, Simin Fan, Andreas Kopf, Amirkeivan Mohtashami, Alexandre Sallinen,
Alireza Sakhaeirad, Vinitra Swamy, Igor Krawczuk, Deniz Bayazit, Axel Marmet, Syrielle Montariol,
Mary-Anne Hartley, Martin Jaggi, and Antoine Bosselut. Meditron-70b: Scaling medical pretraining for
large language models.ArXiv, abs/2311.16079, 2023. 2, 4
[37] Andrew Sellergren, Sahar Kazemzadeh, Tiam Jaroensri, Atilla Kiraly, Madeleine Traverse, Timo
Kohlberger, Shawn Xu, Fayaz Jamil, Cían Hughes, Charles Lau, et al. Medgemma technical report.
arXiv preprint arXiv:2507.05201, 2025. 2, 4
[38] Xi Chen, Huahui Yi, Mingke You, WeiZhi Liu, Li Wang, Hairui Li, Xue Zhang, Yingman Guo, Lei
Fan, Gang Chen, et al. Enhancing diagnostic capability with multi-agents conversational large language
models.NPJ digital medicine, 8(1):159, 2025. 2, 5
[39] Junying Chen, Chi Gui, Anningzhe Gao, Ke Ji, Xidong Wang, Xiang Wan, and Benyou Wang. Cod,
towards an interpretable medical agent using chain of diagnosis. InFindings of the Association for
Computational Linguistics: ACL 2025, pages 14345–14368, 2025. 2, 5
[40] Yichun Feng, Jiawei Wang, Lu Zhou, and Yixue Li. Doctoragent-rl: A multi-agent collaborative
reinforcement learning system for multi-turn clinical dialogue.arXiv preprint arXiv:2505.19630, 2025. 2,
5
[41] Li Wang, Xi Chen, XiangWen Deng, Hao Wen, MingKe You, WeiZhi Liu, Qi Li, and Jian Li. Prompt
engineering in consistency and reliability with the evidence-based guideline for llms.NPJ digital medicine,
7(1):41, 2024. 4
[42] Hanlin Ding, Wenjie Xia, Yujia Zhou, Lei Wei, Yipeng Feng, Zi Wang, Xuming Song, Rutao Li, Qixing
Mao, Bing Chen, et al. Evaluation and practical application of prompt-driven chatgpts for emr generation.
npj Digital Medicine, 8(1):77, 2025. 4
[43] Xuanzhong Chen, Xiaohao Mao, Qihan Guo, Lun Wang, Shuyang Zhang, and Ting Chen. Rarebench:
Can llms serve as rare diseases specialists?Proceedings of the 30th ACM SIGKDD Conference on
Knowledge Discovery and Data Mining, 2024. 4, 5, 14, 29
[44] Chaoyi Wu, Pengcheng Qiu, Jinxin Liu, Hongfei Gu, Na Li, Ya Zhang, Yanfeng Wang, and Weidi Xie.
Towards evaluating and building versatile large language models for medicine.npj Digital Medicine,
8(1):58, 2025. 4
[45] Chaoyi Wu, Weixiong Lin, Xiaoman Zhang, Ya Zhang, Weidi Xie, and Yanfeng Wang. Pmc-llama:
toward building open-source language models for medicine.Journal of the American Medical Informatics
Association, 31(9):1833–1843, 2024. 4
|20

<!-- page 21 -->
[46] Qwen An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan Li,
Dayiheng Liu, Fei Huang, Guanting Dong, Haoran Wei, Huan Lin, Jian Yang, Jianhong Tu, Jianwei
Zhang, Jianxin Yang, Jiaxin Yang, Jingren Zhou, Junyang Lin, Kai Dang, Keming Lu, Keqin Bao, Kexin
Yang, Le Yu, Mei Li, Mingfeng Xue, Pei Zhang, Qin Zhu, Rui Men, Runji Lin, Tianhao Li, Tingyu Xia,
Xingzhang Ren, Xuancheng Ren, Yang Fan, Yang Su, Yi-Chao Zhang, Yunyang Wan, Yuqi Liu, Zeyu
Cui, Zhenru Zhang, Zihan Qiu, Shanghaoran Quan, and Zekun Wang. Qwen2.5 technical report.ArXiv,
abs/2412.15115, 2024. 4
[47] Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha
Letman, Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan, et al. The llama 3 herd of models.arXiv
e-prints, pages arXiv–2407, 2024. 4
[48] Qiao Jin, Won Kim, Qingyu Chen, Donald C. Comeau, Lana Yeganova, John Wilbur, and Zhiyong Lu.
Biocpt: Contrastive pre-trained transformers with large-scale pubmed search logs for zero-shot biomedical
information retrieval.Bioinformatics, 39 11, 2023. 4
[49] Alistair E. W. Johnson, Lucas Bulgarelli, Lu Shen, Alvin Gayles, Ayad Shammout, Steven Horng, Tom J.
Pollard, Benjamin Moody, Brian Gow, Li wei H. Lehman, Leo Anthony Celi, and Roger G. Mark.
Mimic-iv, a freely accessible electronic health record dataset.Scientific Data, 10, 2023. 5, 14, 27
[50] Zhengyun Zhao, Qiao Jin, and Sheng Yu. Pmc-patients: A large-scale dataset of patient notes and
relations extracted from case reports in pubmed central.ArXiv, abs/2202.13876, 2022. 5, 14, 28
[51] Shu Chen, Zeqian Ju, Xiangyu Dong, Hongchao Fang, Sicheng Wang, Yue Yang, Jiaqi Zeng, Ruisi Zhang,
Ruoyu Zhang, Meng Zhou, Penghui Zhu, and Pengtao Xie. Meddialog: A large-scale medical dialogue
dataset.ArXiv, abs/2004.03329, 2020. 5, 14, 28
[52] Abdullah Al Shafi, Rowzatul Zannat, Abdul Muntakim, and Mahmudul Hasan. A structured dataset of
disease-symptom associations to improve diagnostic accuracy.ArXiv, abs/2506.13610, 2025. 5, 14, 16, 29
[53] Weike Zhao, Chaoyi Wu, Yanjie Fan, Xiaoman Zhang, Pengcheng Qiu, Yuze Sun, Xiao Zhou, Yanfeng
Wang, Ya Zhang, Yongguo Yu, Kun Sun, and Weidi Xie. An agentic system for rare disease diagnosis
with traceable reasoning.ArXiv, abs/2506.20430, 2025. 5, 14, 16, 29
[54] Zoe Piran, Niv Cohen, Yedid Hoshen, and Mor Nitzan. Disentanglement of single-cell data with biolord.
Nature Biotechnology, 42(11):1678–1683, 2024. 14
[55] Naomi Miller, Eve-Marie Lacroix, and Joyce Backus. Medlineplus: building and maintaining the national
library of medicine’s consumer health web service.Bulletin of the Medical Library Association, 88 1:11–7,
2000. 15
|21

<!-- page 22 -->
5 Extended Data
Basic Info
Clinical Presentatin
Symptoms
HPOs
Confirmed Diagnosis
Real Patient Record
Age: 51, Gender: Male
Patient presented with fatigue and 
recurrent infections ...
Alcoholism, Bowel diverticulosis, ...
HP:0030955, HP:0005222, ...
Acute myeloid leukemia, ...
Alexander Disease
Overview
Acute Myeloid Leukemia (AML) is 
a type of cancer that affects the 
blood and bone marrow ...
Symptom
l Fatigue...
l Frequent infections...
l Easy bruising or bleeding...
Causes
The exact cause of AML is often 
unknown, but certain genetic and 
environmental factors may ...
Acute Myeloid Leukemia
Overview
Acute Myeloid Leukemia (AML) is 
a type of cancer that affects the 
blood and bone marrow ...
Symptom
l Fatigue...
l Frequent infections...
l Easy bruising or bleeding ...
Causes
The exact cause of AML is often 
unknown, but certain genetic and 
environmental factors may ...
...
common disease: 12,088
symptoms: 31,837
relations: 142,141
ICD codes (10 dec): 3180 
HPO codes: 4970
rare disease: 4,283
symptoms: 8,600
relations: 114,961
ORPHA codes: 4283 
HPO codes: 8595
Basic Info
Clinical Presentatin
Symptoms
HPOs
Confirmed Diagnosis
Filtered Patient Record
Age: 51, Gender: Male
Patient presented with fatigue and 
recurrent infections ...
Alcoholism, Bowel diverticulosis, ...
HP:0030955, HP:0005222, ...
Acute myeloid leukemia, ...
MIMIC-
IV
PMC-
Patients
Med-
Dialog
Rare-
Arena
Rare-
Bench
Total Records Disease Num Male Femal 
155,442 34189 53.62 % 46.38 %
Wiki 
Docs
Tokens 
per Doc
Pubmed 
Docs
Tokens 
per Doc
Textbook 
Docs
Tokens 
per Doc
3.31M 117 23.9M 164 125,847 152
Blood, Heart and CirculationBones, Joints and Muscles
Unknown, 15.3%
Blood, Heart and Circulation, 15.0%
Brain and Nerves, 
14.9%
Digestive System, 
11.8%
Im
m
une System
, 
11.4%
Skin, Hair and Nails, 10.1%Lungs and Breathing, 6.4%Endocrine System, 6.1%
Other System, 
21.6%
Brain and NervesDigestive SystemEar, Nose and ThroatEndocrine SystemEyes and VisionImmune SystemKidneys and Urinary SystemLungs and BreathingMouth and TeethSkin, Hair and NailsFemale Reproductive SystemMale Reproductive SystemUnknown
ICD-10 Coverage from Code First Letter A to Z
official number our coverage
ORPHA Coverage among Specialists
official number our coverage
low 
correlation
disease
medium 
correlation
high correlation
symptom difference
Outlier Distribution 
of Patient Records
Specialists Distribution
Source Distribution for Disease Guideline
1 source, 37.6%
3 sources, 24.0%
 4 sources, 15.8%
5 or more sources,
 6.8%
2 sources, 15.6%
Highlight Information Sources
WebMD NCBI MSD MANUALS
NHS MedlinePlus MAYO CLNICL
...Orphanet NORD
...
Multi-source Dataset
Total Case:
24,142 
Common Disease 
Rare Disease 
73.1%
26.9%
In-distrubution (ID)
In-distrubution (ID)
OOD
OOD
MIMIC-Common
PM
C-Patients
MedDialog
MIMIC-RareMendeley
RareArena
RareBench
Xinhua
1320
2775
3038
85
710
2576
121
324
7.63
7.92
6.08
4.98 11.76
8.33
11.91
4.19
EHR data from clinical 
center in Israel, 7257 cases
Patient summary from 
PubMed, 6421 cases
Coversational data from 
web platform, 3206 cases
Disease-symptom data from 
literature, 757 cases
EHR data from clinical 
center in Israel, 2184 cases
Patient summary from 
PubMed, 3242 cases
Part from literature 
and part from 
clinical center in 
German, 277 cases
EHR data from 
Xinhua hospital 
in China, 
798 cases
unique disease number
in dataset
Average symptom/phenotype
per patient record
a. Statistics on Disease Information Guideline
b. Statistics on Patient Record Database
c. Statistics on Clinical Knowledge Collection
d. Statistics on Training / Evaluation Dataset
Extended Data Figure 1| Data statistics. a.Left: Overview of items and their relationships in the disease guideline.
Middle: ICD coverage for common diseases and Orpha coverage for rare diseases. Right: Distribution of disease information
sources, highlighting major public resources.b.Top: Summary statistics of patient records. Bottom: Distribution of outliers,
illustrating discrepancies between real patient disease-symptom associations and guideline expectations; Breakdown of confirmed
patient diagnoses by specialty.c.Summary statistics of the clinical knowledge collection.d.Detailed statistics of the seven-center
datasets used for training and evaluation.
|22

<!-- page 23 -->
a. Action Trajectory Statistics on Common Disease Diagnosis 
before RL Training
Our DeepDxSearch
b. Action Trajectory Statistics on Rare Disease Diagnosis 
62.8%
8.7%
9.9%
7.5%
35.2% 26.0%
9.0%
8.6%
40.1% 13.4%
16.5%
8.0%
7.8%
20.4%
12.6%20.0%
21.1%
7.7%
c. Action Flow during Diagnostic Reasoning on Common Disease
before RL Training
Our DeepDxSearch
before RL Training before RL Training
Our DeepDxSearch Our DeepDxSearch
d. Action Flow during Diagnostic Reasoning on Rare Disease
lookup match search diagnose lookup match search diagnose
reasoning steps
reasoning steps
reasoning steps
reasoning steps
e. Transition Probability of Each Action on Common Disease Diagnosis e. Transition Probability of Each Action on Rare Disease Diagnosis
before RL Training before RL TrainingOur DeepDxSearch Our DeepDxSearch
L: <lookup>
M: <match>
S: <search>
D: <diagnose>
L: <lookup>
M: <match>
S: <search>
D: <diagnose>
L: <lookup>
M: <match>
S: <search>
D: <diagnose>
L: <lookup>
M: <match>
S: <search>
D: <diagnose>
Extended Data Figure 2 | Analysis of reasoning dynamics before and after Deep-DxSearch training.a, b.Statistical
comparison of action trajectories for common and rare disease diagnosis. The baseline model (top) exhibits significant algorithmic
rigidity, with the fixed sequence “L,M,S,D” (<lookup>→<match>→<search>→<diagnose> ) accounting for 62.8% and 40.1%
of cases, respectively. In contrast, Deep-DxSearch (bottom) demonstrates increased trajectory diversity (e.g., unique trajectory
types increased from 22 to 37 for common diseases), indicating a shift from repetitive heuristics to customized diagnostic paths.
c, d.Visualization of action flows illustrating the logical progression. The flows confirm a transition from linear, deterministic
execution to adaptive, branching investigation suited to case complexity.e, f.Action-to-action transition probability matrices.
Post-training matrices reveal the emergence of recursive behaviors (e.g.,<search>→<search> for self-correction) and a smoothed
probability distribution in rare diseases, suggesting that the agent’s decisions are conditioned on evolving context rather than
fixed rules.
|23

<!-- page 24 -->
Extended Data Table 1| Impact of embedding-based de-duplication on diagnostic accuracy.We conducted a
rigorous ablation study by filtering cases from the retrieval corpus that exceeded specific cosine similarity thresholds (τ) relative
to the query case, utilizing both BioLORD and OpenAI embeddings to measure similarity.Rem. %denotes the percentage of
the retrieval corpus retained after filtering.Observations:(1) The removal of highly similar cases (τ≥ 0.90) impacts < 2%of
the corpus and causes negligible performance variance. (2) Diagnostic accuracy remains robust even at moderate thresholds
(τ = 0.80), where the top ∼13–17% of similar cases are excluded; this confirms that the model’s performance drives from
synthesizing evidence across a distribution of relevant cases rather than memorizing a specific “near-duplicate.” (3) A significant
performance decline is only observed at aggressive thresholds (τ <0.75) where the corpus is severely decimated (retention falls
below 20%), indicating the loss of essential medical evidence rather than the removal of leakage.
Thres.
Common Disease Diagnosis Rare Disease Diagnosis
Rem. MIMIC-C PMC-Pat. MedDialog Rem. MIMIC-R RareArena RareBench
% Acc@1 Acc@5 Acc@1 Acc@5 Acc@1 Acc@5 % Acc@1 Acc@5 Acc@1 Acc@5 Acc@1 Acc@5
BioLORD Embedding
1.00 100.0 31.03 41.62 43.51 52.16 47.27 58.44 100.0 34.86 46.69 31.93 41.20 71.44 81.22
0.95 99.9 31.16 41.71 43.33 51.80 47.27 59.77 99.2 34.43 46.32 30.85 40.79 67.59 78.14
0.90 99.0 30.92 42.39 42.84 51.66 46.55 59.39 98.8 33.01 44.77 30.36 41.15 64.31 74.38
0.85 94.8 30.03 39.97 41.11 50.86 45.26 58.10 97.0 32.03 44.59 29.16 39.42 61.27 71.55
0.80 83.1 28.43 37.51 40.32 49.17 44.59 57.48 90.9 29.45 40.26 27.41 36.03 60.17 70.82
0.75 63.1 25.47 32.14 36.82 46.24 41.92 54.33 73.6 26.72 37.65 26.18 34.99 59.46 69.20
0.70 39.4 23.88 31.70 32.67 44.51 39.52 50.96 44.0 22.60 32.32 23.42 33.16 56.27 65.18
OpenAI Embedding
1.00 100.0 31.03 41.62 43.51 52.16 47.27 58.44 100.0 34.86 46.69 31.93 41.20 71.44 81.22
0.95 99.2 30.88 41.79 43.25 51.71 46.75 57.98 100.0 34.39 64.41 31.17 39.03 70.42 79.96
0.90 98.8 30.10 41.68 43.12 51.58 46.60 57.82 99.8 34.95 64.43 31.01 39.05 67.25 75.71
0.85 96.9 29.85 41.35 42.75 41.15 46.15 57.30 97.7 34.30 63.85 31.65 38.67 64.42 73.85
0.80 87.2 28.60 39.92 41.45 49.83 44.71 55.85 84.8 30.61 59.75 27.15 35.45 60.12 70.53
0.75 55.2 25.80 36.24 38.22 47.58 40.35 50.60 51.3 24.17 48.29 24.86 31.62 54.43 64.27
0.70 19.8 19.45 28.20 29.19 38.80 32.54 41.15 19.2 15.80 42.60 20.20 25.80 48.10 58.50
Extended Data Table 2| Action Space Ablation: Performance vs. Efficiency Trade-off.We report the latencyafter
removing each component and the specific time reduction (in parentheses). Performance impact is measured by the cumulative
drop in Top-1 Accuracy on Rare Diseases compared to the Full Pipeline.
System State Component Removed Acc@1 Drop Time Cost (Reduction) Efficiency Analysis
Full PipelineNone - 31.78s (-) Optimal accuracy baseline.
w/o<search> Knowledge Searcher & Summa-
rizer
-8.33%† 19.23s (-12.55s) High Cost:Processing
unstructured text is time-
consuming but vital for
robustness.
w/o<lookup>Disease Guideline -1.88% 16.37s (-2.86s) Low Cost:Fast execution;
structures the search space.
w/o<match>Patient Record Database-17.46%10.15s (-6.22s) High Value:Critical for accu-
racy; offers best ROI on latency.
w/o<reason>Policy Reward-22.14%10.15s (Base) Foundation:Core LLM infer-
ence without tool support.
† Combined drop from removing the Document Summarizer (-5.61%) and Knowledge Searcher (-2.72%).
|24

<!-- page 25 -->
A Supplementary
A.1 F ramework Instruction
System Prompt
You are an AI assistant specializing in diagnosing diseases based on phenotypes or symptoms.
Task Description:
Your task is to analyze patient clinical presentation including phenotypes or symptoms and make a final disease
diagnosis through systematic medical reasoning using the available tools.
Available Tools:
1. Disease Information Guideline Lookup Tool:Use the <lookup> tag to query typical phenotypes or
symptoms of specific diseases.
Format:<lookup> disease1, disease2... </lookup>
The system returns common phenotypes for each disease enclosed in a<guide>tag.
2. Patient Record Database Match Tool:Use the<match> tag to submit a list of phenotypes. The system
returns similar known cases, including diseases and their corresponding symptoms, enclosed in a<refer> tag.
Format:<match> phenotype1, phenotype2, phenotype3... </match>
3. Medical Knowledge Corpus Search Tool:Use the<search> tag to retrieve knowledge from Wikipedia,
PMC, or textbooks using free-text queries (do not use commas within each question).
Format: <search> |WIKI| query1, query2... </search> or <search> |PMC| query1, query2...
</search>or<search> |BOOK| query1, query2... </search>
Specify the source using the prefix|WIKI|, |PMC|, or |BOOK|. The system returns the retrieved content in a
<result>tag.
Allowed Actions:
1.<reason> </reason>: Active action. Use for the analysis process or reasoning chain between actions.
2.<lookup> </lookup>: Active action. Use to look up up to 10 diseases within one<lookup>tag.
3.<guide> </guide>: Passive action. Returned by the system after a<lookup>action.
4.<match> </match>: Active action. Use to match a series of patient cases related to the query phenotypes.
5.<refer> </refer>: Passive action. Returned by the system after a<match>action.
6.<search> </search> : Active action. Use to search knowledge from only one source, with up to three queries
(separated by commas) per<search>tag.
7.<result> </result>: Passive action. Returned by the system after a<search>action.
8.<diagnose> </diagnose> : Active action. Analyze all reference information and synthesize to make the final
disease diagnosis.
Format Requirements:
•<reason>must appear between two active actions.
•<lookup>may appear at most once. The content should only include diseases, not symptoms or phenotypes.
•<match> may appear up to three times. The content should only include symptoms or phenotypes, not diseases.
•<search>may appear at most twice. The content must follow the|Source| query1, query2format, with up
to three queries at a time.
• The <diagnose> tag is mandatory at the end. Provide up to five possible disease diagnoses, enclosed in LaTeX
bold format:\textbf{Disease1},\textbf{Disease2}, etc.
•No text may appear outside of the specified tags.
Phenotype Query Refinement Guide:
If repeating the<match> step for more patient case references, refine the query phenotypes by one or more of the
following:
•Adding related phenotypes commonly seen in suspected disease categories
•Replacing phenotypes with alternative medical terminology
•Including potential complications or associated features
•Adding earlier or later stage manifestations
•Using symptoms from retrieved cases as references
Diagnostic Workflow:
The diagnostic workflow is flexible. There is no fixed order for using the<lookup>, <match>, or <search> tools; use
them as appropriate. Ensure your disease diagnoses are enclosed with\textbf{} within the <diagnose> tag, with a
maximum of five diagnoses.
|25

<!-- page 26 -->
A.2 Case Demonstration
To further clarify the problem formulation, we illustrate an exact case about a 58-year-old man with a 6-month
history of progressive muscle weakness and neurological symptoms, and is ultimately confirmed asSystemic
Lupus Erythematosus (SLE). The case was collected from RareArena, accompanied by the traceable
diagnostic reasoning generated by Deep-DxSearch:
Case Illustration: Diagnostic Process of A Patient with Complex Neuromuscular Disorder
Clinical Presentation Input:A 58-year-old male presents with a 6-month history of progressive muscle weakness
and neurological symptoms. He initially noticed double vision and drooping of his left eyelid (ptosis) which gradually
worsened. Over the following months, he developed numbness and tingling sensations in both hands and feet, along
with profound fatigue that significantly impacted his daily activities. The muscle weakness progressed from proximal
muscles to involve distal extremities, eventually rendering him unable to walk independently. He has experienced
unintentional weight loss of 15 pounds and a persistent chronic cough. Physical examination reveals facial weakness,
pronounced proximal muscle weakness affecting shoulders and hips, muscle atrophy in the extremities, diminished deep
tendon reflexes, and distal sensory impairment to vibration and position sense. Laboratory findings show proteinuria
on urinalysis and elevated erythrocyte sedimentation rate. Lumbar puncture demonstrates elevated protein levels
in cerebrospinal fluid. Muscle biopsy reveals inflammatory myopathy with endomysial fibrosis, regenerating muscle
fibers, and scattered ragged red fibers on modified Gomori trichrome stain...
Traceable Diagnostic Reasoning Output of Deep-DxSearch:
<reason> The patient presents with a combination of cranial and peripheral neuropathies, muscle weakness, and other
systemic symptoms. Key symptoms include ptosis, numbness and tingling, fatigue, and proximal muscle weakness.
There are also abnormalities in reflexes, proteinuria, and elevated protein in cerebrospinal fluid. The differential to
consider includes diseases that can affect both muscles and the nervous system, such as inflammatory myopathies,
autoimmune diseases, and metabolic myopathies including mitochondrial disorders. The presence of ragged red fibers
on muscle biopsy suggestive of mitochondrial myopathy. I will firstly lookup diseases I suspect.</reason>
<lookup>inflammatory myopathy, autoimmune disease, mitochondrial myopathy...</lookup>
<guide> **inflammatory myopathy**: proximal muscle weakness, elevated muscle enzymes (CK, aldolase), muscle
pain and tenderness, characteristic rashes in dermatomyositis, dysphagia, and interstitial lung disease. Major types
include dermatomyositis, polymyositis, and inclusion body myositis...
**autoimmune disease**: fatigue, fever, joint pain, organ-specific manifestations, positive autoantibodies (ANA,
anti-dsDNA, RF), and multi-system involvement affecting skin, joints, kidneys, and nervous system...
**mitochondrial myopathy**: progressive muscle weakness, exercise intolerance, ptosis, external ophthalmoplegia,
proximal muscle weakness, and characteristic ragged red fibers on muscle biopsy...
...</guide>
<reason> The search results suggest three main categories to consider. Inflammatory myopathies could explain
the proximal muscle weakness, muscle atrophy, and elevated CSF protein through inflammatory muscle disease
with potential CNS involvement. Autoimmune diseases can cause multi-system manifestations including neurologic
symptoms, proteinuria, and muscle weakness through immune-mediated tissue damage. Mitochondrial myopathy is
particularly compelling given the presence of ragged red fibers, ptosis, and progressive muscle weakness, though the
inflammatory features and systemic involvement suggest a mixed or overlapping pathology...</reason>
<match> ptosis, numbness and tingling, fatigue, proximal muscle weakness, muscle weakness, numbness, tingling,
fatigue, abnormal erythrocyte sedimentation rate, elevated protein in cerebrospinal fluid, muscle atrophy, decreased
reflexes, distal sensory impairment</match>
<refer> Phenotype: Bilateral ptosis, proximal muscle weakness, limb-girdle muscle weakness, decreased tendon
reflexes, reduced lower limb muscle strength; tingling sensation, distal upper limb weakness, elevated cerebrospinal
fluid protein. Confirmed disease: [Guillain-Barré syndrome]
Phenotype: Proximal muscle weakness, distal muscle weakness, peripheral sensorimotor neuropathy, elevated cere-
brospinal fluid protein, pain, numbness, tingling, progressive motor decline. Confirmed disease: [Chronic inflammatory
demyelinating polyneuropathy]
|26

<!-- page 27 -->
Phenotype: Paresthesia, muscular weakness, foot drop, distal lower limb weakness, reduced sensation, areflexia, elevated
erythrocyte sedimentation rate, elevated C-reactive protein level. Confirmed disease: [Eosinophilic Granulomatosis
with Polyangiitis]
Phenotype: Polymyositis, muscle weakness, cardiac involvement in inflammatory myopathy, interstitial lung disease,
elevation of serum creatine phosphokinase. Confirmed disease: [Polymyositis]
...</refer>
<reason> The phenotypes in the reference cases suggest several diseases that could fit the patient’s symptoms.
Guillain-Barré syndrome and chronic inflammatory demyelinating polyneuropathy could explain the neuropathic
features and CSF abnormalities. Eosinophilic granulomatosis with polyangiitis can cause peripheral neuropathy and
muscle weakness with systemic inflammation... However, some typical patterns can not be well-explained and worth
further retrieval...</reason>
<match> muscle weakness, numbness, tingling, fatigue, proteinuria, elevated protein in cerebrospinal fluid, decreased
reflexes, distal sensory impairment, inflammatory myopathy, eosinophilic granulomatosis with polyangiitis</match>
<refer> Phenotype: Tingling sensation, distal upper limb weakness, normal reflexes, normal sensory examination,
elevated cerebrospinal fluid protein. Confirmed disease: [Acute Inflammatory Demyelinating Polyneuropathy]
Phenotype: Proximal muscle weakness, distal muscle weakness, peripheral sensorimotor neuropathy, elevated cere-
brospinal fluid protein, oligoclonal bands, pain, numbness, tingling. Confirmed disease: [Chronic inflammatory
demyelinating polyneuropathy]
Phenotype: Fever, myalgia, weight loss, fatigue, anorexia, arthralgia, anemia, elevated C-reactive protein, proteinuria,
inflammatory myopathy, polyserositis. Confirmed disease: [Systemic Lupus Erythematosus]
...</refer>
<reason> The matching cases from the second search further refine our differential diagnosis. The conditions
consistently appearing include inflammatory demyelinating neuropathies, systemic autoimmune diseases with muscle
involvement, and endocrine-related myopathies. The combination of peripheral neuropathy, muscle weakness, and
systemic inflammation points toward autoimmune etiologies. Let’s search for more specific information about the
relationship between these conditions and the patient’s key symptoms.</reason>
<lookup>dermatomyositis, systemic lupus erythematosus, ...</lookup>
<guide> **dermatomyositis**: Characterized by proximal muscle weakness, characteristic skin rashes (heliotrope rash,
Gottron’s papules), elevated muscle enzymes, dysphagia, and potential for malignancy association...
**systemic lupus erythematosus**: SLE can present with inflammatory myopathy in 5-10% of cases, featuring muscle
weakness, elevated CK, myalgia, along with other SLE manifestations like proteinuria, neurologic involvement, and
positive autoantibodies...
...</guide>
<search> |PubMed| relationship between ptosis and inflammatory myopathies, |PubMed| SLE neurologic manifestations
with ptosis, ...</search>
<result> Ptosis in inflammatory myopathies can occur through several mechanisms: direct extraocular muscle
involvement in dermatomyositis/polymyositis, cranial nerve involvement in systemic vasculitis, or neuromuscular
junction dysfunction. SLE can cause ptosis through cranial neuropathy, CNS lupus affecting brainstem nuclei, or
concurrent myasthenia gravis (increased association).
...</result>
<diagnose> The following diseases should be of primary concern and warrant further investigation:Dermatomyositis,
Systemic Lupus Erythematosus,Mitochondrial Myopathy...</diagnose>
A.3 Details in Data Processing per Resource
We utilized a diverse set of clinical and biomedical resources to construct the training and evaluation datasets,
as well as the retrieval corpus (Supplementary Fig. 1). Below, we describe each source in terms of its origin,
processing steps, and specific use within our framework, with their license presented in Supplementary Tab. 1.
MIMIC-IV[ 49]. This public dataset contains 331,794 de-identified discharge summaries from 145,915
patients admitted to Beth Israel Deaconess Medical Center. We first categorize these cases into common and
rare diseases based on ICD codes and primary diagnoses, following the disease classification Stage (Stage 1 in
Sec. 4.1). This process yields 318,976 common and 12,818 rare disease cases. To ensure data integrity, we
utilize GPT-4o to evaluate case quality, excluding entries with “low-quality” attributes, such as those lacking
|27

<!-- page 28 -->
PMC-Patients
N = 250,294 cases
N = 87,298 cases
MedDialog
N = 257454 cases
N = 162995 cases
N = 56,054 cases
Exclude Step1: 
Not clear presentation 
N = 31,244 cases
Exclude Step2: 
Not a common disease 
N = 9,620 cases
N = 247,834 cases
Exclude Step: 
Not clear presentation
Not a common disease 
N = 162,996 cases
MIMIC-IV
N = 331,794 cases
common
or rare
N = 318,976 cases N = 12,818 cases
common rare
N = 52,078 cases N = 9,395 cases
Exclude Step: 
Not clear presentation 
RareArena
N = 49,760 cases
N = 49,760 cases
RareBench
N = 1,122 cases
N = 1,122 cases
Cleaned Patient Record Collection (N = 178,029)
Dataset for 
Training and Evaluation
N = 22,587 cases
quality
assessment
common = 16,884
rare = 5,703 Patient Record Database
N = 155,442 cases
common = 100,868
rare = 54,574
Xinhua Hosp.
352,424 cases
Mendeley
N = 757 cases
Dataset for 
Evaluation Only
N = 1,555 cases
N = 162995 cases
N = 41,450 cases
Exclude Step: 
Not clear presentation
Not a rare disease 
quality assessment
N = 5,820 cases
Disease Information
Guideline
N = 16,371 cases
ICD10Data Orphanet
N = 11,074 diseases
N = 4,283 pairs
tree-structure mapping
N = 12,088 diseases
select common diseases
based on ICD code,
considering only the part
of the ICD code before the
first decimal place.
Healthcase Web
disease knowledge
search and summarize
Clinical Knowledge
Collection
N = 27.34 million docs 
Wikipedia
PubMed
TextBook
Datasets
Medical
Retrieval
Corpus
N = 247,834 cases
Supplementary Figure 1| Data processing procedure.The datasets for training and evaluation are derived from eight
data sources and are split into training, evaluation, and evaluation-only sets. The medical retrieval corpus is constructed partially
from these datasets as well as additional authoritative online resources.
a clear causal link between the clinical presentation and the final diagnosis (Stage 2 in Sec. 4.1). After this
filtering, 52,078 common and 9,395 rare disease cases remain. Following the standards of extraction and
stratification (Stage 3 in Sec. 4.1)in, we identify 7,257 cases for the common disease diagnosis task and 2,184
for the rare disease task. The remaining 44,821 common and 7,211 rare cases are integrated into the patient
record database used by Deep-DxSearch.
PMC-Patients[ 50]. This dataset comprises 250,294 patient profiles derived from 167,000 public summaries
in PubMed Central. We first employ GPT-4o to assess the quality of these cases, excluding 162,995 entries
identified as “low-quality.” (Stage 2). Of the remaining 87,298 cases, we categorize them (Stage 1) and
retain only those associated with common diseases, resulting in 56,054 cases. Following our extraction and
stratification pipeline (Stage 3), we select 6,421 cases for the common disease diagnosis task, while the
remaining 49,633 cases are incorporated into the patient record database for Deep-DxSearch.
MedDialog[ 51]. This dataset contains clinical consultations from both Chinese- and English-speaking
online platforms. We utilize the English subset, which initially comprises 257,454 cases. By applying the
aforementioned pipeline to exclude rare diseases (Stage 1) and identify “low-quality” entries (Stage 2), we
remove 247,839 cases, leaving 9,620 cases associated with common diseases. Following the diagnostic data
processing pipeline (Stage 3), 3,206 of these cases are designated for the training and testing tasks. The
remaining 6,414 cases are integrated into the patient record database for Deep-DxSearch.
|28

<!-- page 29 -->
RareArena 3. Derived from PMC-Patients, this dataset contains approximately 50,000 patient records
covering over 4,000 diseases. As these cases are pre-curated for rare disease tasks, we bypass the processing
stage 1 & 2. However, we apply the extraction and stratification pipeline, which explicitly identifies 3,242 cases
for training and evaluation. The remaining 46,518 cases are incorporated into the patient record database.
RareBench[ 43]. This benchmark targets rare disease diagnosis and includes both public and private
components. We utilize 1,122 cases from the public sources (RAMEDIS, MME, HMS, and LIRICAL). Given
this dataset provides structured phenotype-diagnosis fields and explicitly targets rare diseases, we do not
apply the additional quality assessment or filtering pipeline. From this collection, we randomly select 798 cases
for training and evaluation, while the remaining 324 cases are integrated into the patient record database.
Mendeley[ 52]. Released in June 2025, this structured resource details binary associations between 85
common diseases and 172 symptoms derived from peer-reviewed literature and reputable databases. We utilize
this dataset for zero-shot evaluation; its release date postdates the training cutoffs of the models, ensuring no
prior exposure and allowing for an assessment of generalization to new data. Unlike the previously described
datasets, we bypass the additional GPT-4o quality assessment here, as the highly structured curation of this
resource inherently minimizes noise.
Xinhua Hosp[53]. This in-house dataset comprises rare disease diagnostic records fromXinhua Hospital
Affiliated To Shanghai Jiao Tong University School of Medicinespanning 2014 to 2025, totaling 352,424
entries. We apply the GPT-4o quality assessment to exclude “low-quality” entries (Stage 2), followed by the
extraction and stratification pipeline (Stage 3), which yields a total of 5,820 validated cases. From this subset,
we randomly sample 798 cases for evaluation. Distinct from the public datasets, the remaining cases are not
integrated into the patient record database during training; instead, they function exclusively as an extra
retrieval source during zero-shot testing.
ICD10Data. We extracted disease names and codes from the official ICD-10-CM classification, yielding
12,088 common and 4,283 rare diseases. This taxonomy was used to construct our disease information guide.
Orphanet. We obtained 11,074 Orpha codes, including phenotype probability distributions for 4,283 rare
diseases. These were integrated into the structured knowledge base to support phenotype-driven reasoning.
Healthcare Websites. We curated disease descriptions, symptoms, and other clinical features from online
medical sources (e.g., NCBI, WebMD, NIH, Mayo Clinic). Using deepseek-v3, we summarized and standardized
142,141 disease–symptoms/phenotypes pairs for inclusion in the structured guideline.
PubMed, Wikipedia, and Textbooks. Following the MedRAG protocol [25], we aggregated 23.9 million
PubMed abstracts and 3.31 million Wikipedia medical entries and 18 medical textbooks to form a broad
clinical knowledge base. They were further chunked and indexed into database to facilitate efficient retrieval.
Supplementary Table 1|Legal audit of training & evaluation datasets.
Dataset License Type Permission for LLM Training
MIMIC-IV PhysioNet DUA v1.5.0 (Creden-
tialed)
Authorized.DUA permits derived models; compliant with
PhysioNet LLM guidelines.
PMC-PatientsCC BY / CC BY-SA Authorized.Part of the Open Access Subset specifically for
text mining.
RareBenchApache 2.0 Authorized.Permissive license allowing modification and
derivative works.
RareArenaCC BY-NC-SA 4.0Authorized.Permits non-commercial derivative works.
Mendeley (Bangla)CC BY 4.0Authorized.Permits unrestricted use with attribution.
MedDialogAcademic Research Use Fair Use.Used strictly for non-commercial academic valida-
tion.
3https://github.com/zhao-zy15/RareArena
|29

<!-- page 30 -->
A.4 Details in Retrieval Methods
To maximize the efficacy and performance of the interaction with our proposed medical retrieval corpus, we
treat each retrieval action and the observation of the action as tool and input arguments. Here we detaied the
formulation of these tools including the Phenotype Parser, Patient Matcher, knowledge Searcher and MedDoc
Summarizer.
Phenotype Parser.This tool is designed for the retriving from the diseae information guideline. We use
BM25 search algorithm to build this tool for phenotype parsing with the input of a list of diseases. To
optimize the response time, we process it batch by batch for searching process acceleration. Specifically, take
D = {d1, d2, ..., dm} as input wheredi denotes the ith disease waiting for searching, then the general process
could be denoted as:
TPP(D) =
(  
d,
(
P( ˆd),ifBM25(d, ˆd)≥τ
no reference,otherwise
!  d∈ D, ˆd= arg maxd′∈Mdisease BM25(d, d′)) (5)
Here, BM25_Match(d,M disease)denotes the best-matching disease ˆd for a queryd in the reference corpus
Mdisease using the standard BM25 algorithm, where the BM25 score between a tokenized queryq and a
candidate disease named′ is defined as
BM25(q, d′) =X
t∈q
IDF(t)· f(t, d′) (k1 + 1)
f(t, d′) +k1(1−b+b |d′|avgdl)
with f (t, d′)being the frequency of tokent in d′, |d′| the number of tokens ind′, avgdl the average length of
all disease names in the corpus, andk1, b standard hyperparameters (e.g.,k1 = 1.5, b = 0.75). The inverse
document frequency is computed as
IDF(t) = log
 N−n(t) + 0.5
n(t) + 0.5 + 1

,
where N is the total number of diseases andn(t)is the number of diseases containing tokent. For each
d∈ D, if the maximum BM25 scoreBM25(d, ˆd)exceeds a threshold τ, we return the topk (e.g., k = 10)
high-frequency phenotypes for the matched disease, denoted asP(ˆd); otherwise, we return “no reference”.
Patient Matcher.This tool is designed to interact with the patient record database When taking symptoms
or phenotypes as input, matching to patients in similar situations can provide valuable references for current
case diagnosis. Given that different patients may describe symptoms differently, lexical searching is not
adopted. Instead, we use BioLORD embeddings to calculate semantic similarity between cases. Specifically,
each phenotype or symptoms in a patient record is encoded as a feature vectore(s)using the BioLORD
encoder. For a case i with set Pi = {pi,1, pi,2, . . . , pi,ni }, we represent its overall case embedding as the
transformation of the symptom embeddings:
Sim(Pq,P i) = 1|Pq|
|Pq|X
j=1
max
1≤k≤|Pi|
cos (e(pq,j ),e(p i,k))(6)
where Pq = {pq,1, . . . , pq,nq } is the query case,Pi = {pi,1, . . . , pi,ni } is the i-th case in the database, and
cos(a, b)denotes the cosine similarity between two embedding vectors. For each query symptompq,j, we find
its maximal similarity to all symptoms in the candidate case, and then average these maxima across all query
symptoms.
|30

<!-- page 31 -->
The Patient Matcher toolTPM returns the top-Ncases with the highest similarity scores:
TPM(Pq) = TopNi (Sim(Pq,P i))(7)
whereTopN i(·)selects theNmost similar cases from the database.
Knowledge Searcher.This tool is designed to interact with medical knowledge collection. To deploy
these corpora as an efficient retrieval service accessible to Large Language Models (LLMs), we developed
an asynchronous web server using the Python-based FastAPI framework, served by Uvicorn. The system
implements two mainstream retrieval paradigms: sparse retrieval, based on keyword frequency (BM25), and
dense retrieval, based on semantic similarity. For sparse retrieval, we leveraged the Pyserini library to query a
pre-constructed Lucene index. For dense retrieval, we first utilized the Transformers library to load pre-trained
text embedding models (e.g., E5, BGE) to encode all text chunks into high-dimensional vectors. Subsequently,
we employed the FAISS library to build an index for these vectors, enabling millisecond-level similarity
searches across a massive vector space by leveraging its GPU acceleration capabilities. The server’s core logic
is encapsulated within an Encoder class and multiple Retriever classes; the former handles text vectorization,
while the latter executes the specific retrieval operations (either BM25 or Dense) based on the provided
configuration. It calls a batch_search method to perform real-time query encoding and retrieves the top-k
most relevant documents from the corresponding FAISS or Lucene index, returning the final results in JSON
format. The entire service is initiated via a command-line script, which allows for flexible configuration of key
parameters such as index and corpus paths, the choice of retrieval model, and the number of documents to
return (top-k). This design results in a highly configurable, scalable, and high-performance retrieval backend.
MedDoc Summarizer.To mitigate context length constraints when environment feedback exceeds maximum
limits, we employed a document summarizer to condense information into a controllable length. Specifically,
we utilizedQwen-3-235Bas the summarizer, deployed within our multi-source environment using theSGLang
framework for efficient batch inference. This inference infrastructure was hosted on four NVIDIA H200 GPUs
within the Deep-DxSearch training cluster. The summarization instruction prompt is provided below:
System Prompt:
You are a medical document summarization assistant. Given a search query and a retrieved document,
your task is to summarize the document to directly and concisely answer the query.
• Extract the most relevant facts or statements from the document that directly answer the
query. If more than 10 points are relevant, keep only the 10 most important.
•Your answer should be brief, focused, and contain no extra explanation.
•Format your answer as a JSON string, e.g.,"answer": "...".
•If no relevant information can be found, respond with"answer": "no reference".
Agent:
Source: {source} | Query: {query}
A.5 Prompt for Reasoning Quality Assessment
To quantitatively evaluate the diagnostic capabilities, we employed advanced LLMs, specifically DeepSeek-R1
and Meditron, as evaluator agents. The prompt presented below was designed to instruct these evaluators to
assess the entire diagnostic reasoning process of the target models for a given patient case, strictly adhering
to the proposed five-dimensional scoring framework.
Role & Objective:You are an expert Medical Evaluator. Your task is to evaluate the clinical
reasoning capabilities of an AI model based on a specific patient case and a ground truth diagnosis.
You must strictly adhere to the following 5-dimensional framework.
|31

<!-- page 32 -->
Evaluation Criteria (Scale 1-4):
1. Overall Correctness (Diagnostic Accuracy)
• Score 1 (Poor):The diagnosis is incorrect, or the model provides dangerous/contraindicated
recommendations.
• Score 2 (Fair):Identifies the general disease category or system but misses the specific
pathology; includes unreasonable differentials.
• Score 3 (Good):Correct diagnosis is present but ranked low in the candidate list, or the list
contains significant distractors.
• Score 4 (Excellent):Precisely identifies the ground truth as the primary diagnosis and
successfully excludes reasonable differentials.
2. Clinical Utility (Actionability)
• Score 1 (Poor):Response lacks actionable insight, is disorganized, or increases the physician’s
cognitive load.
• Score 2 (Fair):Provides generic, “textbook-style” information not specifically tailored to the
patient’s unique case presentation.
• Score 3 (Good):Integrates case-specific details, providing valuable reference points that aid
the diagnostic process.
• Score 4 (Excellent):Achieves a “Consultant” level of insight, offering the correct diagnosis
alongside profound analysis and management recommendations.
3. Reasoning Consistency (Logical Flow)
•Score 1 (Poor):Logic is chaotic, exhibiting non-sequiturs or significant logical fallacies.
• Score 2 (Fair):Relies on superficial keyword matching without comprehensive clinical synthesis
or analysis.
• Score 3 (Good):Logic is clear, establishing reasonable causal links between presenting
symptoms and potential diseases.
• Score 4 (Excellent):Demonstrates complex clinical reasoning (e.g., diagnosis by exclusion,
multi-system synthesis) with robust logical coherence.
4. Reference Info Relevance (Signal-to-Noise Ratio)
• Score 1 (Poor):Discussion is severely off-topic, focusing on irrelevant organ systems or
non-medical content.
• Score 2 (Fair):Output contains excessive irrelevant background knowledge or generic, non-
substantive text.
• Score 3 (Good):Content is primarily focused on the specific case with minimal redundancy.
• Score 4 (Excellent):Highly pertinent; every step is tightly aligned with the diagnostic needs
of the current case (High Signal-to-Noise Ratio).
5. Hallucination Severity (Faithfulness)
• Score 1 (Severe):Fabricates symptoms, physical signs, or laboratory results not present in
the patient record (Fatal Errors).
• Score 2 (Moderate):Confuses medical concepts or misattributes information (e.g., citing
incorrect guidelines).
• Score 3 (Minor):Slight deviations in details (e.g., severity, frequency) that do not fundamen-
tally alter the diagnostic direction.
• Score 4 (None):Completely faithful to the case description; all cited medical knowledge and
patient data are accurate.
Output Requirements:
•You must output the result strictly as aJSON object. Do not include any conversational text.
• The JSON object must contain the following keys:overall_correctness, clinical_utility,
reasoning_consistency,reference_relevance,hallucination_severity.
|32

<!-- page 33 -->
• Each key must contain a "score" (integer 1-4) and a "justification" (concise explanation
referencing the criteria).
JSON Example:
{
"overall_correctness": {
"score": 3,
"justification": "Correct diagnosis is present but ranked low..."
},
"clinical_utility": {
"score": 2,
"justification": "Provides generic info not tailored to the patient..."
},
...
}
A.6 T op-N Accuracy Calculation Protocol
Given the inherent variability of natural language generation, establishing a rigorous performance metric is
essential for reproducible clinical evaluation. We implemented a standardizedtwo-stage protocolcomprising
deterministic extraction followed by rule-enhanced strict matching. This approach ensures that reported
Top-N accuracy metrics reflect genuine diagnostic capability, decoupling clinical reasoning performance from
formatting variability or semantic ambiguity.
A.6.1 Deterministic Extraction via Format Enforcement
In contrast to standard generative settings where answers may be dispersed within unstructured conversational
text, our framework imposes a rigorous structural constraint reinforced during training via the format reward
(σf). The model is required to encapsulate the final diagnostic conclusion within<diagnose> tags and explicitly
delineate specific disease entities using LATEX-style bold formatting (\textbf{}). For instance, a valid output
must strictly adhere to the schema:<diagnose> ... \textbf{Disease A} ... </diagnose> . We parse
the content enclosed within these bold delimiters to generate an ordered candidate listC = [c1, c2, . . . , ck],
treating any text outside these tags as auxiliary reasoning context excluded from metric calculation. Adherence
is strictly enforced; any response failing to satisfy these formatting constraints is assigned a score of zero for
that instance.
A.6.2 Rule-Enhanced Strict Matching
To evaluate the correspondence between a candidate diagnosisci and the ground-truthg, we employ a strict
matching protocol that rejects vague semantic similarities while accommodating clinically valid specificity
refinements. The process begins with standard string normalization for both the candidate and ground-truth,
including case-folding and the removal of punctuation and whitespace.
Permissible clinical variations.We acknowledge that a candidate diagnosis may be clinically correct even
if it includes specific modifiers absent in a more generic ground-truth. Therefore, a candidateci is considered
a match if it consists of the ground-truth stringg modified exclusively by terms from a predefined set of
permissible clinical variations. These variations span five axes:chronicity and course(e.g., acute, recurrent,
progressive);severity and state(e.g., mild, malignant, latent);etiology and origin(e.g., idiopathic, congenital,
iatrogenic);laterality and localization(e.g., bilateral, focal, systemic); andtyping and staging(e.g., Type I,
Stage 4). Formally, ifg is a substring ofci, and the set difference consisting of the remaining words belongs
solely to these allowable categories, the prediction is counted as correct.
Exclusion of fuzzy matches.To maintain the highest evaluation standards, we enforce exact character
matching for the core disease entity, deliberately excluding probabilistic semantic metrics such as BERTScore
|33

<!-- page 34 -->
or edit-distance measures like Levenshtein distance. This strict protocol penalizes orthographic variations (e.g.,
“Haemophilia” vs. “Hemophilia”) and synonymous terminology (e.g., “Hepatic Steatosis” vs. “Fatty Liver”)
unless explicitly linked within the source taxonomy. While our training objective utilizes partial rewards to
facilitate optimization, the testing protocol remains binary and stringent, ensuring that high Top-N accuracy
reflects precise adherence to standardized medical terminology.
A.7 System prompt for baseline models
For vanilla model with direct diagnosis inference, we use the following prompt:
System Prompt:
You are a disease diagnosis assistant. Your task is to make diagnosis based on the given symtoms
or phenotypes. The user input is a list of symptoms of phenotypes. Your answer should only be
diseases without other explanations enclosed within LaTeX bold format:Disease1,Disease2, etc.
Please make up to 5 diagnoses.
For training-free RAG, we use the same prompt as detailed in Supp. A.1.
|34
