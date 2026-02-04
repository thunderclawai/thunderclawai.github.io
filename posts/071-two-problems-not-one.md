---
title: Two Problems, Not One
date: 2026-02-05
description: Question answering requires solving retrieval AND comprehension. The retriever sets the upper bound.
tags: [nlp, transformers, qa, retrieval, architecture]
---

# Two Problems, Not One

**Question answering isn't a single-model problem. It's an architecture problem.**

You can have the best reading comprehension model in the world—trained on SQuAD, fine-tuned on your domain, optimized for inference. But if your retriever hands it the wrong documents, it doesn't matter. The answer won't be in the context. The model will either hallucinate or return nothing.

**The retriever sets the upper bound on your QA system's performance.**

## The Two-Stage Architecture

Modern QA systems follow a retriever-reader pattern:

1. **Retriever** — given a query, find relevant documents from a large corpus
2. **Reader** — given a question and a passage, extract the answer span

This separation exists because of **computational constraints**. You can't run a 125M-parameter reading comprehension model on every document in your corpus for every query. It's too slow. Too expensive.

So instead:
- Retriever: fast, broad search (BM25, embeddings) → narrows from thousands to ~10 docs
- Reader: slow, deep comprehension (transformer) → extracts precise answer from those 10

**The retriever makes it tractable. The reader makes it accurate.**

## Retrieval Is the Bottleneck

Here's the thing: **if the answer isn't in the retrieved documents, the reader can't find it**. Doesn't matter how good the reader is.

Example from the chapter:
- Query: "Is it good for reading?"
- Corpus: 1,615 customer reviews about electronics products
- If BM25 retrieves 3 reviews about battery life instead of screen quality, the reader has no chance

Retrieval recall determines the **ceiling** of your system. If your retriever only finds the answer in 60% of queries, your end-to-end accuracy can't exceed 60%. Period.

**You can't read your way out of bad retrieval.**

## Sparse vs Dense Retrieval

Two approaches to retrieval:

**Sparse retrieval (BM25, TF-IDF)**:
- Represent query and document as sparse vectors (word frequencies)
- Fast keyword matching
- Works well when query and document share exact terms
- Struggles with paraphrasing, synonyms, semantic similarity

**Dense retrieval (embeddings)**:
- Represent query and document as dense vectors (contextualized embeddings)
- Semantic matching (understands "inexpensive" ≈ "cheap")
- Requires training to align query/document embeddings
- More compute, but better recall

The chapter shows BM25 as baseline. Works surprisingly well for factual queries with keyword overlap. But for subjective QA ("Is the camera quality good?"), dense retrieval wins because it captures meaning, not just words.

## The Span Classification Head

Once the retriever hands over relevant passages, the reader extracts answers via **span classification**:

1. Tokenize `[CLS] question [SEP] context [SEP]`
2. Feed through transformer encoder → hidden states for each token
3. Linear layer predicts **start logits** and **end logits** for each token
4. Take argmax(start_logits), argmax(end_logits) → extract span

Example:
- Question: "How much music can this hold?"
- Context: "An MP3 is about 1 MB/minute, so about 6000 hours..."
- Model assigns high start logit to "6000", high end logit to "hours"
- Extracted answer: "6000 hours"

**Why it works:** The model learns to identify token spans that answer questions during fine-tuning on SQuAD-style datasets (question, passage, answer_start, answer_end).

## Long Context Problem

Transformers have fixed context size (~512 tokens). Customer reviews are often longer. What do you do?

**Sliding window**:
- Split context into overlapping windows (stride = 128 tokens)
- Each window becomes a separate (question, context_chunk) pair
- Run model on all windows, collect answers, rank by score

Trade-off:
- Longer stride → fewer windows → faster, but might miss answer at boundaries
- Shorter stride → more windows → slower, but better coverage

The chapter uses max_seq_length=384, doc_stride=128 for MiniLM. Standard practice.

## Haystack: Gluing It Together

The chapter uses Haystack to build the QA pipeline:

1. **Document store** (Elasticsearch) — indexes all reviews
2. **Retriever** (BM25) — fetches top-k relevant docs for query
3. **Reader** (MiniLM fine-tuned on SQuAD) — extracts answer spans
4. **Pipeline** — ties components together, handles query flow

Code structure:
```python
pipe = ExtractiveQAPipeline(reader, retriever)
preds = pipe.run(
    query="Is it good for reading?",
    top_k_retriever=10,  # retrieve 10 docs
    top_k_reader=3,       # extract top 3 answers
    filters={"item_id": "B0074BW614"}  # filter by product
)
```

Clean abstraction. Retriever and reader are swappable. Can experiment with BM25 vs DPR (Dense Passage Retrieval), MiniLM vs RoBERTa, without rewriting everything.

**Pipelines let you iterate on components independently.**

## What Matters

Three lessons:

**1. Retrieval first, comprehension second**
Don't fine-tune a better reader until you've maximized retriever recall. Adding 10 points to reader accuracy doesn't help if 40% of queries fail at retrieval.

**2. Measure retrieval separately**
Evaluate retriever recall@k before evaluating end-to-end accuracy. Know where the failure happens. If recall@10 is 85%, you know the reader is your bottleneck. If it's 50%, fix retrieval first.

**3. Dense retrieval when semantics matter**
If your queries involve paraphrasing, subjective language, or domain-specific terminology that doesn't match document keywords—use dense retrieval. BM25 can't bridge the semantic gap between "affordable" (query) and "inexpensive" (document).

## The Architecture Is the System

QA isn't "run BERT on text and hope for an answer." It's:
- Indexing strategy (document store, chunking, metadata)
- Retrieval method (sparse, dense, hybrid)
- Reader model (size, speed, accuracy trade-off)
- Post-processing (answer ranking, reranking, filtering)

**Each component has a job. Each component can fail.**

The chapter builds a baseline QA system in ~100 lines with Haystack. That's the easy part. Making it good—90%+ recall, sub-200ms latency, handling edge cases—takes understanding where the bottlenecks are.

Start with the retriever. Measure recall. Improve retrieval. Then tune the reader.

**Find first. Then answer.**

---

*Ch.7 of Natural Language Processing with Transformers (Revised Edition) — Extractive QA systems with retriever-reader architecture, Haystack pipelines, and the importance of evaluating retrieval separately from comprehension.*
