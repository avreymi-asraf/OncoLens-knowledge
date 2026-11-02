# Lexicon: Agentic RAG and Agentic RL

*An English–Hebrew dictionary of the concepts behind this knowledge base.*
*Created 2026-11-02 · built from the cortex (`cortex/`) and the four ingested sources, plus web research on origins.*

Each entry gives:

- **Hebrew**: how the word is said in Israeli tech speech, written in Hebrew letters, then a Latin transliteration with the **stressed syllable in bold**. Where a native Hebrew term exists, it is given with niqqud.
- **Origin**: where the word comes from, and where it got its technical meaning.
- **Meaning**: what it means here.
- **Usage**: how it shows up in the sources, with an English and a Hebrew example sentence.
- **In this KB**: links to cortex nodes, where they exist.

> **A note on Hebrew terms.** In Israeli industry most of these words are said in English
> ("טוקן", "פרומפט", "ראג"). Hebrew equivalents exist for many of them, and they appear in
> academic writing, the press and courses. I could not reach the Academy of the Hebrew Language's
> term database while writing this, so the Hebrew equivalents below are **common usage**, not
> official Academy rulings, unless stated otherwise.

> **Pronunciation key.** `ג'` = *j* (as in *jet*), `צ'` = *ch* (as in *chat*), `ז'` = *zh* (as in *vision*),
> `ח`/`כ` = *kh* (as in *Bach*), `ו'`/`וו` = *w*. Israeli speakers usually stress English loanwords on the
> first syllable, as in English.

---

## Contents

1. [Foundations: AI and language models](#1-foundations-ai-and-language-models)
2. [Retrieval and search](#2-retrieval-and-search)
3. [RAG and its variants](#3-rag-and-its-variants)
4. [Agents and tools](#4-agents-and-tools)
5. [Graphs and orchestration](#5-graphs-and-orchestration)
6. [Prompt programming and DSPy](#6-prompt-programming-and-dspy)
7. [Reinforcement learning](#7-reinforcement-learning)
8. [Agentic RL in practice](#8-agentic-rl-in-practice)
9. [Evaluation and benchmarks](#9-evaluation-and-benchmarks)
10. [Frameworks, libraries and models](#10-frameworks-libraries-and-models)
11. [Quick Hebrew–English table](#11-quick-hebrewenglish-table)
12. [Sources](#12-sources)

---

## 1. Foundations: AI and language models

### Artificial intelligence (AI)
- **Hebrew:** בִּינָה מְלָאכוּתִית (*bi**na** m'la-khu**tit***); in speech often אֵיי-אַיי (***ey**-ay*).
- **Origin:** Coined by John McCarthy in the 1955 proposal for the 1956 Dartmouth summer workshop. *Artificial* is from Latin *artificium*, "craft" (*ars* "skill" + *facere* "make"); *intelligence* is from Latin *intellegere*, "to understand", literally "to choose between" (*inter* + *legere*). The Hebrew *bina* is from the root ב־י־ן, "to discern, understand", the same root as *bein*, "between". So both the Latin and the Hebrew build "intelligence" from the idea of telling things apart. *M'lakhutit* is from *m'lakha*, "craft, work".
- **Meaning:** The field of building systems that carry out tasks that need human-like judgement, such as perception, language, planning and learning.
- **Usage:** The umbrella term. Everything below is a part of it.
  - *"The agent is an AI system that decides when to search."*
  - *"בינה מלאכותית היא תחום־העל של כל המושגים כאן."*

### Machine learning (ML)
- **Hebrew:** לְמִידַת מְכוֹנָה (*l'mi**dat** m'kho**na***); in speech אֶם-אֶל (***em**-el*).
- **Origin:** Popularised by Arthur Samuel (IBM) around 1959, in his work on a checkers program that improved by playing itself.
- **Meaning:** Getting a system's behaviour from data and feedback instead of from hand-written rules.
- **Usage:** *"RL is one branch of machine learning."* / *"למידת חיזוק היא ענף של למידת מכונה."*

### Language model (LM)
- **Hebrew:** מוֹדֶל שָׂפָה (*mo**del** sa**fa***); in speech אֶל-אֶם (***el**-em*).
- **Origin:** *Model* is from Latin *modulus*, "small measure", via Italian *modello*. Statistical language models go back to Claude Shannon's 1948 n-gram experiments. The phrase *language model* became standard in IBM's speech-recognition research in the 1970s and 1980s.
- **Meaning:** A model that assigns probabilities to sequences of tokens, which in practice means predicting the next token.
- **Usage:** DSPy calls the configured model the "LM": `dspy.LM(...)`. In the multi-hop source, the *student LM* is Llama-3.1-8B and the *teacher LM* is GPT-4o.
  - *"מודל השפה מנבא את האסימון הבא."*

### Large language model (LLM)
- **Hebrew:** מוֹדֶל שָׂפָה גָּדוֹל (*mo**del** sa**fa** ga**dol***); in speech אֶל-אֶל-אֶם (*el-el-**em***).
- **Origin:** Came into wide use between 2018 and 2023 (BERT, GPT-2, GPT-3) for transformer language models with billions of parameters. Hebrew Wikipedia notes that the term has no formal definition.
- **Meaning:** A very large transformer language model trained on huge amounts of text, which can follow instructions, write, reason and call tools.
- **Usage:** *"The LLM decides whether to call the retriever."* / *"ה־LLM מחליט אם לקרוא לכלי האחזור."*
- **In this KB:** [[claims/the-model-deciding-whether-to-call-the-retriever-makes-rag-agentic-rather-than-a-fixed-pipeline]]

### Transformer
- **Hebrew:** טְרַנְסְפוֹרְמֶר (*trans-**for**-mer*). The literal Hebrew is שַׁנַּאי (*sha-**nai***, an electrical transformer), but nobody uses it for the model.
- **Origin:** Latin *transformare*, "to change shape". As a model architecture, it comes from Vaswani et al. (Google, 2017), *"Attention Is All You Need"*.
- **Meaning:** A neural-network architecture built on *attention*, which lets every token weigh every other token. Almost every LLM is a transformer.
- **Usage:** *"Qwen2.5 is a decoder-only transformer."*

### Parameter
- **Hebrew:** פָּרָמֶטֶר (*pa-**ra**-me-ter*); also פָּרָמֶטֶר in plain Hebrew. Plural פָּרָמֶטְרִים.
- **Origin:** Greek *para* "beside" + *metron* "measure". It was used in mathematics from the 17th century.
- **Meaning:** One learned number (a weight) inside a model. "8B" means 8 billion parameters.
- **Usage:** *"Llama-3.1-8B"* = 8 billion parameters. / *"מודל עם שמונה מיליארד פרמטרים."*

### Token
- **Hebrew:** אֲסִימוֹן (*a-si-**mon***); in speech טוֹקֶן (***to**-ken*), plural טוֹקֶנִים (*to-ke-**nim***).
- **Origin:** Old English *tācen*, "sign, symbol" (related to *teach*). In computing, a *token* was first the smallest unit a compiler reads. The Hebrew *asimon* has a parallel story. It comes from Greek *asēmon*, "unmarked [metal]", meaning uncoined silver. It appears in the Mishnah, and in modern Hebrew it meant the old payphone token. Both words mean "a small unit that stands for something".
- **Meaning:** The basic unit a language model reads and writes: a word, part of a word, or a symbol. Usage, cost and context limits are counted in tokens.
- **Usage:** VerlTool's training has to keep tokens consistent across multi-turn rollouts.
  - *"Tool outputs are tokenized separately from the model's actions."*
  - *"כל תשובה של הכלי הופכת לרצף אסימונים."*
- **In this KB:** [[claims/tokenizing-actions-and-observations-separately-keeps-multi-turn-rollouts-token-consistent]]

### Tokenizer / tokenization
- **Hebrew:** טוֹקֶנַייזֶר (*to-ke-**nai**-zer*); in Hebrew מְאַסְמֵן (*m'as-**men***), the act אִסְמוּן (*is-**mun***). These are rare; the English word dominates.
- **Origin:** *Token* + *-ize*. The best-known algorithm, BPE (byte-pair encoding), started as a data-compression method (Philip Gage, 1994). Sennrich et al. adapted it for NLP in 2016.
- **Meaning:** The component that splits text into tokens and maps each one to an integer ID, and turns IDs back into text.
- **Usage:** The VerlTool paper shows that tokenizing *action + observation* together can give different tokens than tokenizing each one separately and joining them. This breaks on-policy training.
  - *"מאסמנים כל קטע בנפרד ומשרשרים את רצפי ה־ID."*
- **In this KB:** [[claims/tokenizing-actions-and-observations-separately-keeps-multi-turn-rollouts-token-consistent]]

### Embedding
- **Hebrew:** אֶמְבֶּדִינְג (*em-**be**-ding*); in Hebrew שִׁכּוּן (*shi-**kun***, the mathematics term) or הַטְמָעָה (*hat-ma-**'a***, common in ML writing).
- **Origin:** *Embed*, "fix firmly in a surrounding mass" (from *bed*), 18th century. In mathematics, an *embedding* places one structure inside another. In NLP, it took off with Bengio et al. (2003) and word2vec (Mikolov et al., 2013).
- **Meaning:** A list of numbers (a vector) that represents a piece of text, so that texts with similar meanings land close to each other.
- **Usage:** *"The documents are embedded and stored in a vector store."* / *"מטמיעים את המסמכים ושומרים אותם במאגר וקטורים."*

### Vector
- **Hebrew:** וֶקְטוֹר (***vek**-tor*). Plural וֶקְטוֹרִים.
- **Origin:** Latin *vector*, "carrier", from *vehere*, "to carry" (as in *vehicle*). William Rowan Hamilton used it in mathematics in the 1840s.
- **Meaning:** An ordered list of numbers, here a point in embedding space.
- **Usage:** *"Each chunk becomes a 768-dimensional vector."*

### Semantic similarity / cosine similarity
- **Hebrew:** דִּמְיוֹן סֵמַנְטִי (*dim-**yon** se-**man**-ti*); דִּמְיוֹן קוֹסִינוּס (*dim-**yon** ko-**si**-nus*).
- **Origin:** *Semantic* is from Greek *sēmantikos*, "significant", from *sēma*, "sign". Michel Bréal coined French *sémantique* in 1883. *Cosine* is from Latin *complementi sinus*, "sine of the complement". *Sinus* ("fold, bay") is itself a mistranslation of the Arabic *jayb*, which came from Sanskrit *jīvā*, "bowstring".
- **Meaning:** How close two texts are in meaning, usually measured as the cosine of the angle between their embedding vectors (1 = same direction, 0 = unrelated).
- **Usage:** The Hugging Face source points out that a *question* and the *answer document* can be far apart in similarity because one is phrased as a question and the other as a statement.
  - *"הדמיון הסמנטי בין השאלה לבין המסמך נמוך, אף שהמסמך עונה עליה."*
- **In this KB:** [[claims/using-the-user-question-as-the-similarity-reference-can-miss-answer-documents-written-in-affirmative-form]]

### Prompt
- **Hebrew:** פְּרוֹמְפְּט (*promt*, one syllable; plural פְּרוֹמְפְּטִים, *promp-**tim***); in Hebrew הַנְחָיָה (*han-kha-**ya***), plural הַנְחָיוֹת.
- **Origin:** Latin *promptus*, "brought forth, ready", from *promere*, "to bring out". In the theatre, a *prompter* fed actors their forgotten lines. In computing, the *command prompt* invited the user to type. The Hebrew *hanchaya* is from the root נ־ח־ה, "to lead, guide" (as in Psalm 23:3, *yancheni*, "He leads me").
- **Meaning:** The text given to a model as input: instructions, examples, context and the question.
- **Usage:** *"The grader prompt tells the model to treat retrieved text as data."* / *"בהנחיה של המדרג כתוב שהטקסט שנשלף הוא מידע בלבד."*
- **In this KB:** [[claims/retrieved-text-should-be-treated-as-data-only-in-grader-and-generator-prompts]]

### Prompt engineering
- **Hebrew:** פְּרוֹמְפְּט אֶנְגִ'ינִירִינְג (*promt en-ji-**ni**-ring*); in Hebrew הַנְדָּסַת הַנְחָיוֹת (*han-da-**sat** han-kha-**yot***).
- **Origin:** Came into use around 2020 and 2021, after GPT-3 showed that wording changes results a great deal. *Engineering* is from Latin *ingenium*, "cleverness, innate talent".
- **Meaning:** Writing and refining prompts by hand to get better outputs. DSPy's position is that this should be done by an *optimizer*, not by hand.
- **Usage:** *"Instead of prompt engineering by hand, MIPROv2 searched over instructions."*
- **In this KB:** [[claims/the-retriever-tool-prompt-tells-the-agent-to-query-in-affirmative-form-with-several-semantically-different-queries]]

### Context window
- **Hebrew:** חַלּוֹן הֶקְשֵׁר (*kha-**lon** hek-**sher***); in speech קוֹנְטֶקְסְט (***kon**-tekst*).
- **Origin:** Latin *contextus*, "woven together" (*con* + *texere*, "to weave", as in *textile*). The Hebrew *heksher* is from ק־ש־ר, "to tie".
- **Meaning:** The maximum number of tokens a model can see at once: the prompt, the retrieved documents, the tool outputs and its own replies.
- **Usage:** *"Retrieved chunks must fit in the context window."*

### Hallucination
- **Hebrew:** הָלוּצִינַצְיָה (*ha-lu-tsi-**nats**-ya*) or הָלוּסִינֵיישֶׁן (*ha-lu-si-**ney**-shen*); in Hebrew הֲזָיָה (*ha-za-**ya***).
- **Origin:** Latin *(h)allucinari*, "to wander in mind, dream". In computer vision, *face hallucination* (Baker and Kanade, 2000) was a positive term for inventing plausible detail. In neural machine translation and LLMs (from about 2018), it became negative: fluent but false output. The Hebrew *hazaya* is from the root ה־ז־ה. Isaiah 56:10 has *hozim shokhvim*, "dreaming, lying down".
- **Meaning:** A model stating something fluent and confident that is not supported by facts or by its sources.
- **Usage:** Rewriting the question and retrying retrieval is a way to avoid hallucinating after a weak first search.
  - *"בלי אחזור טוב, המודל נוטה להזיות."*
- **In this KB:** [[claims/rewriting-the-question-and-retrying-retrieval-lets-an-agent-recover-from-a-weak-first-retrieval]]

### Zero-shot / few-shot
- **Hebrew:** זִירוֹ-שׁוֹט, פְיוּ-שׁוֹט (***zi**-ro shot, **fyu** shot*); in Hebrew לְלֹא דֻּגְמָאוֹת / עִם דֻּגְמָאוֹת סְפוּרוֹת (*l'lo dug-ma-**ot*** / *im dug-ma-**ot** s'fu-**rot***).
- **Origin:** A *shot* is an attempt (from shooting). *Zero-data learning* (Larochelle et al., 2008) and *zero-shot learning* (Palatucci et al., 2009) came from computer vision. The GPT-3 paper (2020) made *few-shot prompting* everyday language.
- **Meaning:** Zero-shot: the model gets only instructions. Few-shot: the prompt also includes a few worked examples ("demonstrations").
- **Usage:** DSPy's optimizers choose few-shot demonstrations automatically.

### Fine-tuning / supervised fine-tuning (SFT)
- **Hebrew:** פַיין-טְיוּנִינְג (*fain-**tyu**-ning*), אֶס-אֶף-טִי (*es-ef-**ti***); in Hebrew כִּוְנוּן עָדִין (*kiv-**nun** a-**din***).
- **Origin:** A metaphor from tuning a radio or an instrument. *Tune* is a variant of *tone*, from Greek *tonos*, "stretching, pitch".
- **Meaning:** Further training of a pretrained model on a narrower dataset. SFT uses example input-output pairs, and usually comes before RL.
- **Usage:** *"Agentic RL usually starts from an SFT or instruct checkpoint."*

---

## 2. Retrieval and search

### Retrieval / information retrieval (IR)
- **Hebrew:** רִיטְרִיבַל (*ri-**tri**-val*); in Hebrew אִחְזוּר (*ikh-**zur***), אִחְזוּר מֵידָע (*ikh-**zur** mei-**da***), or שְׁלִיפָה (*sh'li-**fa***).
- **Origin:** Old French *retrover*, "to find again" (*re* + *trover*, "to find"). Hunting dogs "retrieve" game. Calvin Mooers coined *information retrieval* around 1950. The Hebrew *ikhzur* is from א־ח־ז, "to grasp, hold". *Shlifa* is from ש־ל־ף, "to draw out", as in drawing a sword: "וְלֹא שָׁלַף הַנַּעַר חַרְבּוֹ" (Judges 8:20).
- **Meaning:** Finding the documents in a collection that are relevant to a query.
- **Usage:** *"Vanilla RAG does one retrieval step."* / *"RAG בסיסי מבצע שלב אחזור אחד בלבד."*
- **In this KB:** [[claims/vanilla-rag-performs-only-one-retrieval-step-so-bad-retrieval-yields-bad-generation]]

### Retriever
- **Hebrew:** רִיטְרִיבֶר (*ri-**tri**-ver*); in Hebrew מְאַחְזֵר (*m'akh-**zer***) or רְכִיב אִחְזוּר.
- **Origin:** As above. *Retriever* has named a dog breed since the 19th century, which is why "retriever" packages sometimes have a dog for a logo.
- **Meaning:** The component that takes a query and returns the top-k documents. In agentic RAG, the retriever is wrapped as a **tool** that the model can call.
- **Usage:** LangGraph: `retriever_tool`; smolagents: `RetrieverTool`.
  - *"הסוכן קורא למאחזר כשהוא צריך מידע."*

### Corpus / knowledge base
- **Hebrew:** קוֹרְפּוּס (***kor**-pus*); מַאֲגַר יֶדַע (*ma-'a-**gar** ye-**da***), in speech נוֹלֶדְג' בֵּייס (***no**-lej beys*).
- **Origin:** Latin *corpus*, "body", as in *Corpus Juris Civilis*, "the body of civil law". The Hebrew *ma'agar* is from א־ג־ר, "to gather, store" (Proverbs 6:8, "אָגְרָה בַקָּצִיר מַאֲכָלָהּ", the ant "gathers her food in the harvest").
- **Meaning:** The whole document collection that retrieval searches. In the DSPy source, this is Wikipedia 2017 abstracts. In the Hugging Face source, it is the Hugging Face documentation.

### Chunk / chunking
- **Hebrew:** צַ'אנְק (*chank*), צַ'אנְקִים; in Hebrew מִקְטָע (*mik-**ta***), the act מִקְטוּעַ / חִתּוּךְ לְמִקְטָעִים.
- **Origin:** A 17th-century variant of *chuck*, "a lump" (of wood or meat).
- **Meaning:** A piece of a document small enough to embed and to fit in the prompt. Chunking is splitting documents into chunks, often with some overlap.
- **Usage:** Both web sources split documents with a text splitter before indexing.

### Index
- **Hebrew:** אִינְדֶּקְס (***in**-deks*); in Hebrew מַפְתֵּחַ (*maf-**te**-akh*) or אִנְדֶּקְס.
- **Origin:** Latin *index*, "forefinger, pointer", from *indicare*, "to point out".
- **Meaning:** A data structure built ahead of time so that search is fast: an inverted index for keyword search, or a vector index for embeddings.
- **Usage:** `bm25s.BM25()` followed by `retriever.index(...)` in the DSPy source.

### Vector store / vector database
- **Hebrew:** וֶקְטוֹר סְטוֹר (***vek**-tor stor*); in Hebrew מַאֲגַר וֶקְטוֹרִים (*ma-'a-**gar** vek-to-**rim***).
- **Meaning:** A database for storing embeddings and finding the nearest ones to a query vector. Examples: FAISS, Chroma, and LangChain's `InMemoryVectorStore`.

### BM25 / BM25S
- **Hebrew:** בִּי-אֶם-עֶשְׂרִים-וְחָמֵשׁ (*bi-em es-**rim** v'kha-**mesh***), or in English *bi-em **twen**-ty five*.
- **Origin:** BM stands for *Best Matching*, and 25 is the number of the formula variant. It was developed for the **Okapi** retrieval system at City University London (Stephen Robertson, Karen Spärck Jones and colleagues) in the 1990s, which is why it is often called *Okapi BM25*. It builds on IDF (inverse document frequency), introduced by Spärck Jones in 1972. *BM25S* is a fast Python implementation by Xing Han Lù (2024).
- **Meaning:** A keyword ("sparse", lexical) ranking function. It scores documents by how often query words appear in them, weighted by how rare the words are, with a correction for document length.
- **Usage:** The DSPy multi-hop program searches Wikipedia abstracts with BM25S.
- **In this KB:** [[claims/an-unoptimized-two-module-multi-hop-program-on-llama-3-1-8b-reaches-only-31-percent-top5-recall-on-hover]]

### Dense vs. sparse retrieval
- **Hebrew:** אִחְזוּר צָפוּף / אִחְזוּר דָּלִיל (*ikh-**zur** tsa-**fuf*** / *ikh-**zur** da-**lil***); in speech דֶּנְס / סְפַּארְס.
- **Meaning:** *Sparse* retrieval matches words (BM25, TF-IDF). The vectors are mostly zeros, one slot per vocabulary word. *Dense* retrieval matches meaning, using embeddings in which every slot has a value. Hybrid systems combine the two.

### Semantic search
- **Hebrew:** חִפּוּשׂ סֵמַנְטִי (*khi-**pus** se-**man**-ti*).
- **Meaning:** Search by meaning (dense embeddings) rather than by exact words.
- **Usage:** *"Instead of using the user query directly as the reference in semantic search, the agent writes its own reference sentence."* (Hugging Face source)

### Top-k
- **Hebrew:** טוֹפּ-קֵיי (*top **kei***); טוֹפּ-חָמֵשׁ for top-5.
- **Meaning:** The k highest-scoring results that a retriever returns.

### Recall / precision
- **Hebrew:** רִיקוֹל (***ri**-kol*), פְּרִיסִיזְיָה / פְּרֶסִיזְ'ן (*pre-**si**-zhen*); in Hebrew כִּסּוּי or רְגִישׁוּת (*ki-**sui*** / *r'gi-**shut***) for recall, and דִּיּוּק (*di-**yuk***) for precision.
- **Origin:** Latin *re-* + *calare*, "to call back"; Latin *praecisio*, "a cutting off". The two measures were formalised in information-retrieval evaluation in the 1950s and 1960s (Kent et al., and the Cranfield experiments).
- **Meaning:** *Recall* is the share of all relevant documents that were found. *Precision* is the share of returned documents that are relevant. **Top-5 recall** is the share of gold documents found among the top 5.
- **Usage:** In the DSPy source, top-5 recall on HoVer went from about 31% to about 59% after optimization.
  - *"הכיסוי בחמש התוצאות הראשונות כמעט הוכפל."*
- **In this KB:** [[claims/joint-prompt-optimization-with-miprov2-roughly-doubles-multi-hop-retrieval-recall-from-31-to-59-percent]]

### Re-ranking
- **Hebrew:** רִי-רֵנְקִינְג (*ri-**ren**-king*); in Hebrew דֵּרוּג מֵחָדָשׁ (*de-**rug** me-kha-**dash***).
- **Meaning:** A second, more expensive model (often a cross-encoder) re-scores a short candidate list from the first retriever.

### Query
- **Hebrew:** קְוֶוְרִי (***kve**-ri*); in Hebrew שְׁאִילְתָּה (*sh'il-**ta***), plural שְׁאִילְתּוֹת.
- **Origin:** Latin *quaere*, "ask!" (imperative of *quaerere*). It was written in the margins of texts to mark a doubtful point and became an English noun in the 17th century. The Hebrew *she'ilta* is an Aramaic-form word from ש־א־ל, "to ask". It is best known from the *She'iltot* of Rav Achai Gaon (8th century), and was reused in computing for database queries.
- **Meaning:** The text sent to a search system. In agentic RAG, the model writes its own queries.
- **Usage:** *"The agent formulates its own retrieval query."* / *"הסוכן מנסח בעצמו את השאילתה."*

### Query reformulation / query rewriting
- **Hebrew:** רִיפוֹרְמוּלַצְיָה (*ri-for-mu-**lats**-ya*); in Hebrew נִסּוּחַ מֵחָדָשׁ שֶׁל הַשְּׁאִילְתָּה (*ni-**su**-akh me-kha-**dash***), or שִׁכְתּוּב שְׁאִילְתָּה (*shikh-**tuv** sh'il-**ta***).
- **Meaning:** Changing the user's question into a better search query: clearer, phrased as a statement, broken into parts, or split into several variants.
- **Usage:** LangGraph's `rewrite_question` node runs when the documents are graded as irrelevant.
- **In this KB:** [[claims/rewriting-the-question-and-retrying-retrieval-lets-an-agent-recover-from-a-weak-first-retrieval]], [[claims/the-retriever-tool-prompt-tells-the-agent-to-query-in-affirmative-form-with-several-semantically-different-queries]]

### HyDE (Hypothetical Document Embeddings)
- **Hebrew:** הַייד (*haid*, like the English name *Hyde*).
- **Origin:** Gao, Ma, Lin and Callan (2022), *"Precise Zero-Shot Dense Retrieval without Relevance Labels"* (arXiv 2212.10496). The acronym is a pun on Stevenson's *Dr Jekyll and Mr Hyde*. *Hypothetical* is from Greek *hypothesis*, "a placing under, a foundation".
- **Meaning:** The model first writes a *fake* answer document, then searches with *that* document's embedding. A made-up answer tends to sit closer to real answers than the question does.
- **Usage:** The Hugging Face agent behaves "as in HyDE" when it writes affirmative queries.
- **In this KB:** [[claims/a-rag-agent-formulates-its-own-retrieval-query-and-re-retrieves-recovering-hyde-and-self-query-behaviour]]

### Self-query
- **Hebrew:** סֶלְף-קְוֶוְרִי (*self **kve**-ri*); in Hebrew שְׁאִילְתָּה עַצְמִית.
- **Origin:** Named after LangChain's `SelfQueryRetriever`.
- **Meaning:** The model turns a natural-language request into a structured query, such as search text plus a **metadata filter** (for example `year > 2020`), and runs it itself.
- **Usage:** The Hugging Face source names self-query as one of the behaviours an agent gets "for free".

### Metadata
- **Hebrew:** מֶטָא-דָּאטָה (*me-ta-**da**-ta*); in Hebrew מֶטָא־נְתוּנִים (*me-ta n'tu-**nim***).
- **Origin:** Greek *meta*, "after, beyond" + Latin *data*, "things given". The term is usually credited to Philip Bagley (1968).
- **Meaning:** Data about data: a document's source, date, author or section, used for filtering.

### Multi-hop
- **Hebrew:** מוּלְטִי-הוֹפּ (*mul-ti **hop***); in Hebrew רַב־שְׁלַבִּי or רַב־דִּלּוּגִי (*rav-sh'la-**bi***, *rav-di-lu-**gi***).
- **Origin:** *Hop* is Old English *hoppian*, "to leap". In networking, a *hop* is one leg of a packet's route. In QA, it means one step of reasoning across documents.
- **Meaning:** A question that can only be answered by chaining several documents. The answer to step 1 (a **bridge entity**) is needed to search for step 2.
- **Usage:** HoVer claims need up to 4 hops. The DSPy program runs a fixed number of hops, adding notes after each one.
  - *"בכל דילוג המודל כותב שאילתה חדשה על סמך הרשימות שנצברו."*
- **In this KB:** [[concepts/multi-hop-retrieval-with-note-accumulation]]

### Bridge entity / query decomposition
- **Hebrew:** יֵשׁוּת גִּשְׁרִית (*ye-**shut** gish-**rit***), פֵּרוּק שְׁאִילְתָּה (*pe-**ruk** sh'il-**ta***).
- **Meaning:** A *bridge entity* is the unknown middle link in a chain, for example "the author of the book". *Query decomposition* is breaking a complex question into sub-questions, starting with the bridge.
- **Usage:** The optimized DSPy query generator, with no notes yet, first asks who the author of *Up Against It* is.
- **In this KB:** [[claims/optimized-query-generator-decomposes-a-multi-hop-claim-by-asking-for-the-first-unknown-entity-when-notes-are-empty]]

---

## 3. RAG and its variants

### RAG (Retrieval-Augmented Generation)
- **Hebrew:** רָאג (*rag*, rhymes with "jog") or spelled out אַר-אֵיי-גִ'י (*ar-ey-**ji***); in Hebrew יְצִירָה מֻעֲשֶׁרֶת אִחְזוּר (*y'tsi-**ra** mu-'e-**she**-ret ikh-**zur***), a descriptive phrase with no fixed standard.
- **Origin:** Lewis et al. (Facebook AI Research, UCL and NYU), 2020, *"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"*. *Augment* is from Latin *augere*, "to increase". Patrick Lewis has said publicly that they would have picked a nicer name had they known it would catch on, since *rag* also means a scrap of cloth.
- **Meaning:** Before generating an answer, the system retrieves relevant documents and adds them to the prompt. The model answers *from* that context, which reduces hallucination and allows citations.
- **Usage:** *"RAG grounds the answer in retrieved documents."* / *"ב־RAG התשובה מעוגנת במסמכים שנשלפו."*

### Vanilla RAG
- **Hebrew:** וָנִילָה רָאג (*va-**ni**-la rag*); in Hebrew RAG בְּסִיסִי (*b'si-**si***).
- **Origin:** *Vanilla*, "plain, default", from vanilla as the default ice-cream flavour. The word comes from Spanish *vainilla*, "little pod", from Latin *vagina*, "sheath".
- **Meaning:** A fixed pipeline: one retrieval with the user's question, then one generation. There is no retry or check.
- **Usage:** The Hugging Face source: one retrieval step, so a bad retrieval means a bad answer.
- **In this KB:** [[claims/vanilla-rag-performs-only-one-retrieval-step-so-bad-retrieval-yields-bad-generation]]

### Agentic RAG
- **Hebrew:** אֵייגֶ'נְטִיק רָאג (*ey-**jen**-tik rag*); in Hebrew RAG סוֹכְנוּתִי (*sokh-nu-**ti***).
- **Meaning:** RAG in which an **agent** (an LLM with a retriever *tool*) decides *whether*, *what* and *how many times* to retrieve. It can rewrite queries, grade results and loop.
- **Usage:** In the Hugging Face evaluation, agentic RAG scored 86.9% and standard RAG 73.1% on an LLM-judged documentation QA set.
- **In this KB:** [[claims/the-model-deciding-whether-to-call-the-retriever-makes-rag-agentic-rather-than-a-fixed-pipeline]], [[claims/agentic-rag-scored-86-9-percent-versus-73-1-percent-for-standard-rag-on-an-llm-judged-hugging-face-docs-qa-set]], [[concepts/agentic-rag-retrieve-grade-rewrite-loop]]

### Relevance grading / grader
- **Hebrew:** גְּרֵיידֶר (***grey**-der*); in Hebrew מְדָרֵג (*m'da-**reg***), the act דֵּרוּג רֵלֵוַנְטִיּוּת (*de-**rug** re-le-van-ti-**yut***).
- **Origin:** Latin *gradus*, "step". The Hebrew *dirug* is from ד־ר־ג, "step, degree", the same idea.
- **Meaning:** An LLM call that judges whether the retrieved documents are relevant, often as a binary *yes/no* score. It sends the graph either to *answer* or to *rewrite*.
- **Usage:** LangGraph `grade_documents` returns `"generate_answer"` or `"rewrite_question"`.
- **In this KB:** [[claims/a-relevance-grader-after-retrieval-routes-the-agent-to-answer-or-to-question-rewrite]]

### Corrective RAG (CRAG) / Self-RAG
- **Hebrew:** קוֹרֶקְטִיב רָאג, סֶלְף רָאג; in Hebrew RAG מְתַקֵּן / RAG רַפְלֶקְטִיבִי.
- **Origin:** Self-RAG: Asai et al. (2023). CRAG: Yan et al. (2024). Both add a self-check step after retrieval.
- **Meaning:** RAG variants that grade their own retrieval (and sometimes their answer) and correct course with another search, a web search or a rewrite. The LangGraph grade-and-rewrite loop is a small version of this idea.

### Grounding
- **Hebrew:** גְּרָאוּנְדִּינְג (***grawn**-ding*); in Hebrew עִגּוּן (*i-**gun***).
- **Origin:** *Ground*, Old English *grund*, "bottom, foundation". The Hebrew *igun* is from ע־ג־ן, "anchor".
- **Meaning:** Tying every statement to evidence. (In this KB, every claim must have a `derived_from` quote. That is grounding applied to the knowledge base itself.)

### Prompt injection
- **Hebrew:** פְּרוֹמְפְּט אִינְגֶ'קְשֶׁן (*promt in-**jek**-shen*); in Hebrew הַזְרָקַת הַנְחָיוֹת (*haz-ra-**kat** han-kha-**yot***).
- **Origin:** Coined by Simon Willison in September 2022, by analogy with *SQL injection*. *Inject* is from Latin *inicere*, "to throw in".
- **Meaning:** Text inside the data (such as a retrieved web page) that tries to act as instructions to the model ("ignore previous instructions...").
- **Usage:** The LangGraph source's grader and generator prompts say to treat retrieved content as data only.
- **In this KB:** [[claims/retrieved-text-should-be-treated-as-data-only-in-grader-and-generator-prompts]]

---

## 4. Agents and tools

### Agent
- **Hebrew:** אֵייגֶ'נְט (***ey**-jent*), plural אֵייגֶ'נְטִים; in Hebrew סוֹכֵן (*so-**khen***), plural סוֹכְנִים; also סוֹכֵן תְּבוּנִי (*so-**khen** t'vu-**ni***, "intelligent agent").
- **Origin:** Latin *agens*, "one who does", from *agere*, "to drive, act". The Hebrew *sokhen* is biblical, meaning a steward or attendant: "לֶךְ בֹּא אֶל הַסֹּכֵן הַזֶּה, עַל שֶׁבְנָא אֲשֶׁר עַל הַבָּיִת" (Isaiah 22:15), and Abishag was a *sokhenet* to King David (1 Kings 1:2). It already meant "one who acts on another's behalf", which is exactly the AI sense.
- **Meaning:** An LLM in a loop that observes, decides, acts (often by calling tools), sees the result and continues until it reaches the goal.
- **Usage:** *"smolagents' ToolCallingAgent"*. / *"הסוכן מחליט בעצמו מתי לחפש."*
- **In this KB:** [[claims/a-rag-agent-formulates-its-own-retrieval-query-and-re-retrieves-recovering-hyde-and-self-query-behaviour]]

### Agentic
- **Hebrew:** אֵייגֶ'נְטִי / אֵייגֶ'נְטִיק (*ey-**jen**-ti*, *ey-**jen**-tik*); in Hebrew סוֹכְנוּתִי (*sokh-nu-**ti***).
- **Origin:** Psychology used it first: Stanley Milgram's *agentic state* (1974) and Albert Bandura's *agentic perspective* (late 1980s onward). It became AI jargon in 2023 and 2024.
- **Meaning:** Having agency: the model chooses its own actions instead of following a fixed pipeline.
- **Usage:** "agentic RAG", "agentic RL".

### Tool / tool calling / function calling
- **Hebrew:** טוּל (*tul*), טוּל קוֹלִינְג (*tul **ko**-ling*), פַאנְקְשֶׁן קוֹלִינְג; in Hebrew כְּלִי (*k'li*), קְרִיאָה לְכְלִי (*k'ri-**a** lik-**li***).
- **Origin:** *Tool* is Old English *tōl*, "instrument", related to *tawian*, "to prepare". OpenAI's API popularised *function calling* in June 2023; "tool calling" is the general name now. The Hebrew *k'li* is biblical ("כְּלִי יוֹצֵר", "vessel, instrument").
- **Meaning:** An external function the model can call by writing a structured request (name + arguments). The system runs it and feeds the result back. Examples: search, code execution, SQL, image operations.
- **Usage:** LangGraph `bind_tools`; in VerlTool, tools run on a unified tool server.
  - *"המודל מחזיר tool_calls, והגרף מריץ את כלי האחזור."*
- **In this KB:** [[claims/the-model-deciding-whether-to-call-the-retriever-makes-rag-agentic-rather-than-a-fixed-pipeline]], [[claims/a-unified-tool-server-framework-reaches-task-specific-baseline-performance-across-six-agentic-rl-domains]]

### ReAct
- **Hebrew:** רִיאַקְט (*ri-**akt***).
- **Origin:** Yao et al. (2022), from *Reason + Act*.
- **Meaning:** A prompting pattern that alternates *Thought → Action → Observation*. It is the basis of most tool-calling agents.

### Action / observation
- **Hebrew:** אַקְשֶׁן, אוֹבְּזֶרְבֵיישֶׁן; in Hebrew פְּעֻלָּה (*p'u-**la***), תַּצְפִּית (*tats-**pit***).
- **Origin:** Latin *actio*, from *agere*; Latin *observare*, "to watch over". The Hebrew *tatspit* is from צ־פ־ה, "to look out" (as in *tsofeh*, "a watchman").
- **Meaning:** In agentic RL, *actions* are tokens the model writes (including tool calls). *Observations* are tokens that come back from the tool or environment.
- **Usage:** VerlTool writes a trajectory as τ = {a₀, o₀, …, aₙ}. Observation tokens are masked out of the loss.
- **In this KB:** [[claims/tool-observation-tokens-are-off-policy-and-masked-from-the-grpo-loss]]

### Trajectory
- **Hebrew:** טְרָגֶ'קְטוֹרְיָה (*tra-jek-**tor**-ya*); in Hebrew מַסְלוּל (*mas-**lul***), plural מַסְלוּלִים.
- **Origin:** Latin *traiectus*, "thrown across" (*trans* + *iacere*, "to throw"), first used for the path of a projectile. The Hebrew *maslul* is from ס־ל־ל, "to pave a road" (Isaiah 62:10, "סֹלּוּ סֹלּוּ הַמְסִלָּה", "build up, build up the highway").
- **Meaning:** The full recorded sequence of one episode: actions, observations and the final reward.
- **In this KB:** [[concepts/agentic-reinforcement-learning-with-tool-use]]

### Environment / state
- **Hebrew:** אֶנְבַיירוֹנְמֶנְט, סְטֵייט; in Hebrew סְבִיבָה (*s'vi-**va***), מַצָּב (*ma-**tsav***).
- **Meaning:** In RL, the *environment* is everything outside the agent that responds to its actions. The *state* is the current situation. In LangGraph, `State` is the shared object (for example the message list) that the nodes read and update.

### Sandbox
- **Hebrew:** סֶנְדְבּוֹקְס (***send**-boks*); in Hebrew אַרְגַּז חוֹל (*ar-**gaz** khol*), סְבִיבָה מְבֻדֶּדֶת.
- **Origin:** A children's sandbox, a safe place to play. It has been used in computer security since the 1990s.
- **Meaning:** An isolated environment where tool calls such as code execution run without being able to harm the host.

---

## 5. Graphs and orchestration

### Graph / node / edge
- **Hebrew:** גְּרָף (*graf*), נוֹד (*nod*), אֶדְג' (*ej*); in Hebrew גְּרָף, צֹמֶת (***tso**-met*), קֶשֶׁת (***ke**-shet*, directed edge) / צֵלָע (*tse-**la***, undirected edge).
- **Origin:** *Graph* was coined by J. J. Sylvester (1878), from "graphic notation" in chemistry, from Greek *graphein*, "to write". *Node* is from Latin *nodus*, "knot". *Edge* is Old English *ecg*, "blade's edge". The Hebrew *keshet* (bow, arc) and *tsomet* (junction) are the standard terms in Hebrew graph theory.
- **Meaning:** In LangGraph, nodes are steps (functions or LLM calls) and edges are the allowed transitions.
- **Usage:** `workflow.add_node("grade_documents", ...)`.
- **In this KB:** [[concepts/agentic-rag-retrieve-grade-rewrite-loop]]

### Conditional edge
- **Hebrew:** קוֹנְדִּישֶׁנָל אֶדְג'; in Hebrew קֶשֶׁת מוּתְנֵית (***ke**-shet mut-**neit***).
- **Meaning:** An edge whose target is chosen at run time by a function, for example "tool call → retrieve, otherwise → END" or "relevant → answer, otherwise → rewrite".
- **In this KB:** [[claims/a-relevance-grader-after-retrieval-routes-the-agent-to-answer-or-to-question-rewrite]]

### Orchestration
- **Hebrew:** אוֹרְקֶסְטְרַצְיָה (*or-kes-**trats**-ya*); in Hebrew תִּזְמוּר (*tiz-**mur***).
- **Origin:** Greek *orkhēstra*, the space in front of the stage where the chorus danced. The Hebrew *tizmur* is from ז־מ־ר, "to sing, make music".
- **Meaning:** Coordinating several model calls, tools and agents in a controlled flow.

### Pipeline
- **Hebrew:** פַּייפְּלַיין (*paip-**lain***); in Hebrew צַנֶּרֶת (*tsa-**ne**-ret*).
- **Meaning:** A fixed sequence of steps. In agentic systems, the contrast is with a loop where the model chooses the next step.

---

## 6. Prompt programming and DSPy

### Signature (DSPy)
- **Hebrew:** סִיגְנַצֶ'ר (***sig**-na-cher*); in Hebrew חֲתִימָה (*kha-ti-**ma***).
- **Origin:** Latin *signare*, "to mark". It is borrowed from a programming *function signature* (input and output types).
- **Meaning:** A declaration of what a model call takes and returns, for example `"claim, notes -> query"`, with no prompt text written by hand.
- **Usage:** `dspy.ChainOfThought("claim, notes -> query")`.

### Module (DSPy)
- **Hebrew:** מוֹדוּל (*mo-**dul***); in Hebrew רְכִיב (*r'khiv*).
- **Origin:** Latin *modulus*, "small measure".
- **Meaning:** A composable unit of an LM program, such as `Predict` or `ChainOfThought`, or your own class. The multi-hop `Hop` module has two sub-modules: `generate_query` and `append_notes`.

### Chain of thought (CoT)
- **Hebrew:** צֵ'יין אוֹף ת'וֹט, סִי-אוֹ-טִי; in Hebrew שַׁרְשֶׁרֶת מַחֲשָׁבָה (*shar-**she**-ret ma-kha-sha-**va***).
- **Origin:** Wei et al. (Google, 2022).
- **Meaning:** Getting the model to write intermediate reasoning before the answer.

### Optimizer (formerly "teleprompter")
- **Hebrew:** אוֹפְּטִימַייזֶר (*op-ti-**mai**-zer*); in Hebrew מְמַטֵּב (*m'ma-**tev***), the act מִטּוּב (*mi-**tuv***).
- **Origin:** Latin *optimus*, "best". DSPy first called its optimizers **teleprompters**, a pun on the TV device that shows lines to presenters ("prompting from a distance", Greek *tēle*, "far"). The Hebrew *mitav* is from ט־ו־ב, "good", like the Latin.
- **Meaning:** An algorithm that improves an LM program automatically by searching over instructions and few-shot examples, scored by a metric.

### MIPROv2
- **Hebrew:** מִיפְּרוֹ וִי-טוּ (***mip**-ro vi-**tu***).
- **Origin:** Opsahl-Ong et al. (2024), *"Optimizing Instructions and Demonstrations for Multi-Stage Language Model Programs"*. It is usually expanded as *Multiprompt Instruction PRoposal Optimizer*.
- **Meaning:** A DSPy optimizer that bootstraps examples, proposes candidate instructions for every module, then uses Bayesian optimization to pick the best combination.
- **Usage:** `dspy.MIPROv2(metric=top5_recall, auto="medium")`. In the source, it took top-5 recall from 31% to 59% in about 35 minutes for about $5.
- **In this KB:** [[claims/joint-prompt-optimization-with-miprov2-roughly-doubles-multi-hop-retrieval-recall-from-31-to-59-percent]]

### Bootstrapping
- **Hebrew:** בּוּטְסְטְרַפִּינְג (***but**-stra-ping*); in Hebrew אִתְחוּל עַצְמִי (*it-**khul** ats-**mi***).
- **Origin:** "To pull oneself up by one's bootstraps", a 19th-century joke about an impossible feat. Computing uses it for *booting*, and statistics for resampling (Efron, 1979).
- **Meaning:** In DSPy, running the program on training inputs, keeping the runs that pass the metric, and reusing them as few-shot demonstrations.

### Teacher / student model
- **Hebrew:** טִיצֶ'ר / סְטוּדֶנְט; in Hebrew מוֹדֶל מוֹרֶה / מוֹדֶל תַּלְמִיד (*mo-**re*** / *tal-**mid***).
- **Origin:** From *knowledge distillation* (Hinton, Vinyals and Dean, 2015).
- **Meaning:** A strong model (the teacher, for example GPT-4o) helps produce examples or instructions that a small model (the student, for example Llama-3.1-8B) then uses.
- **Usage:** The DSPy source: a teacher is not strictly needed, but it makes the result less sensitive to the optimizer's starting setup.
- **In this KB:** [[claims/a-small-model-can-typically-teach-itself-multi-hop-tasks-in-dspy-and-a-larger-teacher-only-adds-robustness]]

### Metric
- **Hebrew:** מֶטְרִיקָה (*met-**ri**-ka*); in Hebrew מַדָּד (*ma-**dad***).
- **Origin:** Greek *metron*, "measure". The Hebrew *madad* is from מ־ד־ד, "to measure".
- **Meaning:** A function that scores an output. Optimizers maximise it. Example: `top5_recall`.

### Tracing
- **Hebrew:** טְרֵיסִינְג (***trey**-sing*); in Hebrew מַעֲקָב (*ma-'a-**kav***).
- **Meaning:** Recording every LM call, input, output and timing in a run, for debugging. The DSPy source uses MLflow tracing.

---

## 7. Reinforcement learning

### Reinforcement learning (RL)
- **Hebrew:** רִיאִינְפוֹרְסְמֶנְט לֶרְנִינְג, mostly אַר-אֶל (*ar-**el***); in Hebrew לְמִידַת חִזּוּק (*l'mi-**dat** khi-**zuk***).
- **Origin:** *Reinforcement* comes from behavioural psychology: the 1927 English translation of Pavlov's work on conditioning, and later B. F. Skinner's operant conditioning. *Reinforce* is from French *renforcer*, "to strengthen". The computational field was shaped by Sutton and Barto (*Reinforcement Learning: An Introduction*, 1998). Hebrew psychology also uses *khizuk* (חִיזּוּק חִיּוּבִי, "positive reinforcement"), from ח־ז־ק, "strong".
- **Meaning:** Learning by trial and error: an agent acts, gets a reward, and updates its policy to get more reward.
- **Usage:** *"VerlTool is a framework for agentic RL with tool use."*
- **In this KB:** [[concepts/agentic-reinforcement-learning-with-tool-use]]

### Reward
- **Hebrew:** רִיוֹוֹרְד (*ri-**word***); in Hebrew תִּגְמוּל (*tig-**mul***).
- **Origin:** Anglo-Norman *rewarder*, "to regard, look at", a variant of *regard*. The sense "to repay" came later. The Hebrew *tigmul* is from ג־מ־ל, "to repay, deal out" (Psalm 116:12, "מָה אָשִׁיב לַה' כָּל תַּגְמוּלוֹהִי עָלָי", "What shall I render to the Lord for all His bounties toward me?").
- **Meaning:** The scalar signal that says how good an outcome was. Agentic RL usually uses *verifiable* rewards: whether the answer is correct, whether the code passes the tests.
- **In this KB:** [[claims/tool-use-vanishes-during-rl-without-suitable-reward-design]]

### Policy
- **Hebrew:** פּוֹלִיסִי (***po**-li-si*); in Hebrew מְדִינִיּוּת (*m'di-ni-**yut***).
- **Origin:** Greek *politeia*, "citizenship, government", via Old French *policie*. In RL, it means "a rule for choosing actions" (Bellman's dynamic programming, 1950s).
- **Meaning:** The mapping from a state to an action, or a probability distribution over actions. In LLM RL, the policy *is* the language model.

### On-policy / off-policy
- **Hebrew:** אוֹן-פּוֹלִיסִי / אוֹף-פּוֹלִיסִי; in Hebrew עַל־פִּי הַמְּדִינִיּוּת / מִחוּץ לַמְּדִינִיּוּת.
- **Meaning:** *On-policy* data was produced by the current policy itself. *Off-policy* data came from somewhere else: an older policy, another model, or the environment.
- **Usage:** VerlTool: tool observation tokens were not produced by the model, so they are off-policy and are masked from the loss.
- **In this KB:** [[claims/tool-observation-tokens-are-off-policy-and-masked-from-the-grpo-loss]]

### RLHF / RLVR
- **Hebrew:** אַר-אֶל-אֵייצ'-אֶף, אַר-אֶל-וִי-אַר; in Hebrew לְמִידַת חִזּוּק מִמָּשׁוֹב אֱנוֹשִׁי / עִם תִּגְמוּלִים נִתָּנִים לְאִמּוּת.
- **Origin:** RLHF: Christiano et al. (2017), and InstructGPT (Ouyang et al., 2022). The term *RLVR* (RL with Verifiable Rewards) was introduced with Tülu 3 (Lambert et al., AI2, 2024).
- **Meaning:** RLHF learns from human preference judgements, usually through a reward model. RLVR uses rewards a program can check, such as a math answer or unit tests. Agentic RL (ARLT) is multi-turn RLVR with tools.
- **In this KB:** [[concepts/agentic-reinforcement-learning-with-tool-use]]

### PPO (Proximal Policy Optimization)
- **Hebrew:** פִּי-פִּי-אוֹ (*pi-pi-**o***).
- **Origin:** Schulman et al. (OpenAI, 2017). *Proximal* is from Latin *proximus*, "nearest". It keeps each update *close to* the previous policy.
- **Meaning:** A policy-gradient algorithm that clips updates so the policy doesn't change too much in one step. It needs a learned value model (critic).

### GRPO (Group Relative Policy Optimization)
- **Hebrew:** גִ'י-אַר-פִּי-אוֹ (*ji-ar-pi-**o***).
- **Origin:** Shao et al. (DeepSeek, 2024), *DeepSeekMath*.
- **Meaning:** A PPO variant with no critic. For each prompt it samples a *group* of answers and scores each one *relative to* the group average (the advantage). It is the most common algorithm for RLVR today.
- **Usage:** VerlTool trains with GRPO and masks observation tokens.
- **In this KB:** [[claims/tool-observation-tokens-are-off-policy-and-masked-from-the-grpo-loss]]

### Advantage
- **Hebrew:** אַדְוַונְטֶג' (*ad-**van**-tej*); in Hebrew יִתְרוֹן (*yit-**ron***).
- **Origin:** Old French *avantage*, from *avant*, "before". The *advantage function* is from Leemon Baird (1993). The Hebrew *yitron* is from י־ת־ר, "surplus" (a key word in Ecclesiastes: "מַה יִּתְרוֹן לָאָדָם", "What profit has a man").
- **Meaning:** How much better an action was than expected. Positive advantages are reinforced; negative ones are suppressed.

### Loss / loss masking
- **Hebrew:** לוֹס (*los*), לוֹס מַסְקִינְג; in Hebrew פּוּנְקְצְיַת הֶפְסֵד (*hef-**sed***), מִסּוּךְ הַהֶפְסֵד (*mi-**sukh***).
- **Origin:** Old English *los*, "destruction". The Hebrew *misukh* is from מָסָךְ, "screen, curtain".
- **Meaning:** *Loss* is the number training minimises. *Masking* sets some tokens' contribution to zero, so the model is not trained to "write" text it never generated, such as tool outputs.
- **In this KB:** [[claims/tool-observation-tokens-are-off-policy-and-masked-from-the-grpo-loss]]

### KL divergence
- **Hebrew:** קֵיי-אֶל דַּיְוֶרְגֶ'נְס (*kei-el dai-**ver**-jens*); in Hebrew סְטִיַּת קוּלְבֶּק–לַיְבְּלֶר (*s'ti-**yat** kul-bek lai-bler*).
- **Origin:** Solomon Kullback and Richard Leibler (1951).
- **Meaning:** A measure of how different two probability distributions are. In RL it is often added as a penalty to keep the policy close to a reference model.

### Gradient
- **Hebrew:** גְּרַדְיֶנְט (*grad-**yent***); in Hebrew גְּרַדְיֶנְט or שִׁפּוּעַ (*shi-**pu**-a*, "slope").
- **Origin:** Latin *gradiens*, "stepping", from *gradi*, "to step".
- **Meaning:** The direction in which a small change of the parameters increases the loss the most. Training steps the other way.

---

## 8. Agentic RL in practice

### Rollout
- **Hebrew:** רוֹלְאָאוּט (*rol-**a**-ut*), plural רוֹלְאָאוּטִים; no fixed Hebrew term. Descriptive phrases: הַרְצַת מַסְלוּל (*har-**tsat** mas-**lul***), גִּלְגּוּל.
- **Origin:** In RL, the word comes from Tesauro and Galperin's 1996 "rollout" algorithm for backgammon. It plays a position out to the end many times with simulated dice rolls. Backgammon players already used "rollout" for this kind of analysis. The image of dice being "rolled out" fits, but I could not find a source that confirms it as the origin.
- **Meaning:** Running the current policy to generate full trajectories. In agentic RL, this includes the tool calls.
- **Usage:** *"Rollout is the bottleneck when tools are slow."* / *"שלב הרולאאוט הוא צוואר הבקבוק כשהכלים איטיים."*

### Asynchronous rollout
- **Hebrew:** רוֹלְאָאוּט אֵסִינְכְרוֹנִי (*a-sin-**khro**-ni*); in Hebrew הַרָצָה לֹא־מְסֻנְכֶּרֶנֶת.
- **Origin:** Greek *a-* "not" + *syn* "together" + *chronos* "time".
- **Meaning:** Each trajectory moves forward on its own (generate → call tool → continue) instead of the whole batch waiting for the slowest tool call. This removes GPU idle "bubbles".
- **Usage:** VerlTool reports a 1.2× to 2× speedup.
- **In this KB:** [[claims/asynchronous-per-trajectory-rollout-speeds-up-agentic-rl-rollouts-by-1-2-to-2x]]

### Multi-turn
- **Hebrew:** מוּלְטִי-טֶרְן (*mul-ti **tern***); in Hebrew רַב־סִבּוּבִי (*rav si-bu-**vi***).
- **Meaning:** A trajectory with several model ↔ tool exchanges, as opposed to a single prompt → answer.

### Reward design / tool-use collapse
- **Hebrew:** רִיוֹוֹרְד דִּיזַיין; in Hebrew תִּכְנוּן תִּגְמוּל (*tikh-**nun** tig-**mul***), קְרִיסַת שִׁמּוּשׁ בַּכְּלִים (*k'ri-**sat** shi-**mush***).
- **Meaning:** If the reward doesn't make tool use pay off, RL can teach the model to stop calling tools altogether. VerlTool saw this in visual reasoning.
- **In this KB:** [[claims/tool-use-vanishes-during-rl-without-suitable-reward-design]]

### Tool-call frequency dynamics
- **Hebrew:** תְּדִירוּת קְרִיאוֹת לְכֵלִים (*t'di-**rut** k'ri-**ot***).
- **Meaning:** During RL, calls to tools whose output the model can memorise (such as a fixed SQL schema) become rarer. Calls to tools whose output it can't memorise (such as live web search) become more frequent.
- **In this KB:** [[claims/tool-call-frequency-during-rl-falls-for-memorizable-tool-outputs-and-rises-for-unmemorizable-ones]]

### Reward hacking
- **Hebrew:** רִיוֹוֹרְד הָאקִינְג (*ri-word **ha**-king*); in Hebrew פְּרִיצַת תִּגְמוּל / נִצּוּל הַתִּגְמוּל.
- **Origin:** *Hack* is Old English *haccian*, "to cut", later "a clever trick" (MIT slang in the 1950s).
- **Meaning:** The policy finds a way to get high reward without doing the intended task, for example by gaming the checker.

### GPU / throughput
- **Hebrew:** גִ'י-פִּי-יוּ (*ji-pi-**yu***); in Hebrew מְעַבֵּד גְּרָפִי, תְּפוּקָה (*t'fu-**ka***).
- **Meaning:** The hardware that runs training and inference, and how much work it gets through per second. Idle GPU time while waiting for tools is the waste that async rollout reduces.

---

## 9. Evaluation and benchmarks

### Benchmark
- **Hebrew:** בֶּנְצ'מַארְק (***bench**-mark*); in Hebrew מַדַּד יְחוּס (*ma-**dad** y'khus*) or מְבַחַן הַשְׁוָאָה.
- **Origin:** Surveyors cut a mark into stone where an angle-iron (a "bench") could be placed for a levelling rod. It came to mean "a fixed reference point" (19th century).
- **Meaning:** A standard dataset and metric for comparing systems.

### LLM-as-a-judge
- **Hebrew:** אֶל-אֶל-אֶם אֶז אֶ-גָ'אג'; in Hebrew מוֹדֶל שָׂפָה כְּשׁוֹפֵט (*k'sho-**fet***).
- **Origin:** Zheng et al. (2023), *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*.
- **Meaning:** Using a strong LLM to grade answers against a reference or a rubric.
- **Usage:** The Hugging Face agentic-RAG comparison was LLM-judged.
- **In this KB:** [[claims/agentic-rag-scored-86-9-percent-versus-73-1-percent-for-standard-rag-on-an-llm-judged-hugging-face-docs-qa-set]]

### HoVer
- **Hebrew:** הוֹבֶר (***ho**-ver*).
- **Origin:** Jiang et al. (2020), *"HoVer: A Dataset for Many-Hop Fact Extraction and Claim Verification"* (Findings of EMNLP 2020). The name combines *hop* and *verification*.
- **Meaning:** Complex claims that must be checked against several Wikipedia articles. In the DSPy source, the task is to retrieve all the gold page titles.
- **In this KB:** [[concepts/multi-hop-retrieval-with-note-accumulation]]

### GAIA
- **Hebrew:** גַּאיָה (***ga**-ya*).
- **Origin:** Mialon et al. (Meta and Hugging Face, 2023), a benchmark for *General AI Assistants*. The name is also the Greek earth goddess *Gaia*.
- **Meaning:** Real-world assistant questions that need web browsing, tools and several steps. It is one of the VerlTool domains (DeepSearch).

### SWE-bench
- **Hebrew:** סְוִוי-בֶּנְץ' (*swi-bench*) or אֶס-דַּבְּל-יוּ-אִי בֶּנְץ'.
- **Origin:** Jimenez et al. (Princeton, 2023). SWE = *software engineering*.
- **Meaning:** Real GitHub issues that the agent must fix so that the repository's tests pass. It is one of the VerlTool domains.

### Wikipedia
- **Hebrew:** וִיקִיפֶּדְיָה (*vi-ki-**ped**-ya*).
- **Origin:** Hawaiian *wiki*, "quick" (Ward Cunningham's 1995 WikiWikiWeb, named after the Wiki Wiki airport shuttle in Honolulu) + *encyclopedia*. That word is from Greek *enkyklios paideia*, "rounded education".
- **Meaning:** The corpus for HoVer and the DSPy example (2017 abstracts).

### SQL
- **Hebrew:** אֶס-קְיוּ-אֶל (*es-kyu-**el***) or סִיקְוֶול (***si**-kvel*).
- **Origin:** Chamberlin and Boyce (IBM, 1974) called it **SEQUEL**, *Structured English Query Language*. A trademark conflict forced the shorter *SQL*, which is why both pronunciations are still around.
- **Meaning:** The database query language. Text-to-SQL is one of VerlTool's tool domains.

---

## 10. Frameworks, libraries and models

### LangChain / LangGraph
- **Hebrew:** לֶנְגְצֵ'יין (***leng**-chein*), לֶנְגְגְרָף (***leng**-graf*).
- **Origin:** LangChain was started by Harrison Chase in October 2022: "chaining" LLM calls together ("Lang" from *language*). LangGraph (2024) is its library for stateful graphs: nodes, edges and loops.
- **Usage:** The custom RAG agent source is built in LangGraph (`StateGraph`, `ToolNode`, `tools_condition`).

### Hugging Face / smolagents
- **Hebrew:** הָאגִינְג פֵיְיס (***ha**-ging feys*), סְמוֹל-אֵייגֶ'נְטְס (*smol **ey**-jents*).
- **Origin:** Hugging Face (founded 2016) is named after the 🤗 emoji. *smolagents* (2024–25) uses internet slang *smol*, "small", for a deliberately minimal agent library.
- **Usage:** The query-reformulation source builds a `ToolCallingAgent` with a `RetrieverTool`.

### DSPy
- **Hebrew:** דִּי-אֶס-פַּיי (*di-es-**pai***).
- **Origin:** Omar Khattab and colleagues at Stanford NLP. It began as *Demonstrate–Search–Predict* (2022) and is now expanded as *Declarative Self-improving Python* (2023 onward).
- **Meaning:** A framework for *programming* LM pipelines with signatures and modules, then *compiling* (optimizing) their prompts against a metric.
- **In this KB:** [[concepts/multi-hop-retrieval-with-note-accumulation]]

### MLflow
- **Hebrew:** אֶם-אֶל-פְלוֹאוּ (*em-el-**flo**-u*).
- **Origin:** Databricks, 2018.
- **Meaning:** A platform for tracking experiments. The DSPy source uses it to trace each hop of the program.

### verl / VerlTool
- **Hebrew:** וֶרְל (*verl*), וֶרְל-טוּל (*verl-**tul***).
- **Origin:** *verl* is "Volcano Engine Reinforcement Learning", ByteDance's open-source RL library for LLMs and the public version of the HybridFlow paper (EuroSys 2025). Volcano Engine is ByteDance's cloud division. *VerlTool* (2025) extends verl into a framework for agentic RL with tool use (ARLT). It has a unified tool server and asynchronous rollouts.
- **In this KB:** [[concepts/agentic-reinforcement-learning-with-tool-use]], [[claims/a-unified-tool-server-framework-reaches-task-specific-baseline-performance-across-six-agentic-rl-domains]]

### Llama / Qwen / GPT-4o
- **Hebrew:** לָאמָה (***la**-ma*), צְ'וֶון (*chwen*, often said קְוֶון, *kwen*), גִ'י-פִּי-טִי פוֹר-אוֹ (*ji-pi-ti for-**o***).
- **Origin:** *Llama* (Meta, 2023) started as LLaMA, *Large Language Model Meta AI*. *Qwen* (Alibaba) is short for 通义千问 *Tōngyì Qiānwèn*, roughly "a thousand questions of universal truth"; Alibaba's own pronunciation is "chwen". *GPT* = *Generative Pre-trained Transformer*. The "o" in 4o stands for *omni*.
- **Usage:** Llama-3.1-8B is the student in the DSPy source. GPT-4o is the teacher. Qwen2.5 is the tokenizer example and base model in VerlTool.

---

## 11. Quick Hebrew–English table

| English | Said in Israeli tech speech | Hebrew equivalent |
|---|---|---|
| artificial intelligence | אֵיי-אַיי | בִּינָה מְלָאכוּתִית |
| machine learning | אֶם-אֶל | לְמִידַת מְכוֹנָה |
| language model | אֶל-אֶם / מוֹדֶל | מוֹדֶל שָׂפָה |
| token | טוֹקֶן | אֲסִימוֹן |
| embedding | אֶמְבֶּדִינְג | הַטְמָעָה / שִׁכּוּן |
| prompt | פְּרוֹמְפְּט | הַנְחָיָה |
| context window | קוֹנְטֶקְסְט | חַלּוֹן הֶקְשֵׁר |
| hallucination | הָלוּצִינַצְיָה | הֲזָיָה |
| fine-tuning | פַיין-טְיוּנִינְג | כִּוְנוּן עָדִין |
| retrieval | רִיטְרִיבַל | אִחְזוּר / שְׁלִיפָה |
| retriever | רִיטְרִיבֶר | מְאַחְזֵר |
| corpus / knowledge base | קוֹרְפּוּס / נוֹלֶדְג' בֵּייס | מַאֲגַר יֶדַע |
| chunk | צַ'אנְק | מִקְטָע |
| index | אִינְדֶּקְס | מַפְתֵּחַ |
| query | קְוֶוְרִי | שְׁאִילְתָּה |
| query rewriting | רִיפוֹרְמוּלַצְיָה | שִׁכְתּוּב שְׁאִילְתָּה |
| recall / precision | רִיקוֹל / פְּרֶסִיזְ'ן | כִּסּוּי / דִּיּוּק |
| multi-hop | מוּלְטִי-הוֹפּ | רַב־שְׁלַבִּי |
| grader | גְּרֵיידֶר | מְדָרֵג |
| grounding | גְּרָאוּנְדִּינְג | עִגּוּן |
| prompt injection | פְּרוֹמְפְּט אִינְגֶ'קְשֶׁן | הַזְרָקַת הַנְחָיוֹת |
| agent | אֵייגֶ'נְט | סוֹכֵן |
| agentic | אֵייגֶ'נְטִי | סוֹכְנוּתִי |
| tool / tool call | טוּל / טוּל קוֹל | כְּלִי / קְרִיאָה לְכְלִי |
| action / observation | אַקְשֶׁן / אוֹבְּזֶרְבֵיישֶׁן | פְּעֻלָּה / תַּצְפִּית |
| trajectory | טְרָגֶ'קְטוֹרְיָה | מַסְלוּל |
| graph / node / edge | גְּרָף / נוֹד / אֶדְג' | גְּרָף / צֹמֶת / קֶשֶׁת |
| orchestration | אוֹרְקֶסְטְרַצְיָה | תִּזְמוּר |
| pipeline | פַּייפְּלַיין | צַנֶּרֶת |
| optimizer | אוֹפְּטִימַייזֶר | מְמַטֵּב |
| metric | מֶטְרִיקָה | מַדָּד |
| reinforcement learning | אַר-אֶל | לְמִידַת חִזּוּק |
| reward | רִיוֹוֹרְד | תִּגְמוּל |
| policy | פּוֹלִיסִי | מְדִינִיּוּת |
| advantage | אַדְוַונְטֶג' | יִתְרוֹן |
| loss | לוֹס | הֶפְסֵד |
| rollout | רוֹלְאָאוּט | (no fixed term) הַרְצַת מַסְלוּל |
| benchmark | בֶּנְצ'מַארְק | מַדַּד יְחוּס |

---

## 12. Sources

**This knowledge base** (all four ingested sources):
- `sources/text/VERLTOOL TOWARDS HOLISTIC AGENTIC.md`: VerlTool, ARLT, GRPO, async rollout, observation masking.
- `sources/text/agentic-rag-turbocharge-your-rag-with-query-reformulation-and-self-query.md`: HyDE, self-query, vanilla vs. agentic RAG.
- `sources/text/build-a-custom-rag-agent-with-langgraph-docs-by-langchain.md`: LangGraph, grading, rewriting, conditional edges.
- `sources/text/multi-hop-rag-dspy.md`: DSPy, HoVer, BM25S, MIPROv2, teacher/student.

**Original papers named in the entries:** Lewis et al. 2020 (RAG); Gao et al. 2022 (HyDE, arXiv 2212.10496); Yao et al. 2022 (ReAct); Wei et al. 2022 (CoT); Vaswani et al. 2017 (Transformer); Schulman et al. 2017 (PPO); Shao et al. 2024 (GRPO / DeepSeekMath); Lambert et al. 2024 (Tülu 3 / RLVR); Christiano et al. 2017 and Ouyang et al. 2022 (RLHF); Jiang et al. 2020 (HoVer); Mialon et al. 2023 (GAIA); Jimenez et al. 2023 (SWE-bench); Opsahl-Ong et al. 2024 (MIPRO); Khattab et al. 2022–23 (DSPy); Zheng et al. 2023 (LLM-as-a-judge); Tesauro and Galperin 1996 (rollout); Kullback and Leibler 1951; Robertson et al. (Okapi BM25); Spärck Jones 1972 (IDF); Sheng et al. 2025 (HybridFlow / verl).

**Web lookups made while writing:**
- [HoVer paper, ACL Anthology](https://aclweb.org/anthology/2020.findings-emnlp.442.pdf)
- [TD-Gammon (rollouts), Wikipedia](https://en.wikipedia.org/wiki/TD-Gammon)
- [Tesauro and Galperin, *On-line policy improvement using Monte-Carlo search* (NIPS 1996)](https://papers.nips.cc/paper/1292-why-did-td-gammon-work)
- [HybridFlow / verl, ByteDance Seed](https://seed.bytedance.com/zh/public_papers/hybridflow-a-flexible-and-efficient-rlhf-framework)
- [Large language model, Hebrew Wikipedia](https://he.wikipedia.org/wiki/%D7%9E%D7%95%D7%93%D7%9C_%D7%A9%D7%A4%D7%94_%D7%92%D7%93%D7%95%D7%9C) (token = אסימון; no formal definition of LLM)
- [Intelligent agent (סוכן תבוני), Hamichlol](https://www.hamichlol.org.il/%D7%A1%D7%95%D7%9B%D7%9F_%D7%AA%D7%91%D7%95%D7%A0%D7%99)

**Caveats**
- Hebrew equivalents are common usage. The Academy of the Hebrew Language's term database could not be reached (HTTP 403), so none of them is marked as an official ruling.
- Some origins are traditional accounts that I could not confirm from a primary source: the dice explanation for *rollout*, Bagley as the coiner of *metadata*, and the exact expansion of *MIPRO*. Each entry says so where it applies.
