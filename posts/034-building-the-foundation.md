---
title: Building the Foundation
date: 2026-02-03
description: Embeddings power everything. Here's how to build them yourself.
tags: [ai-engineering, embeddings, hands-on-llms]
---

Embeddings aren't a feature. They're **the foundation**.

Every AI application you've used — semantic search, RAG, classification, memory, recommendation systems — sits on top of embeddings. They convert messy, unstructured text into clean numerical vectors that machines can actually work with.

We've been **using** embeddings for nine chapters. Chapter 10 teaches us how to **build** them.

## The Core Idea: Contrastive Learning

How do you teach a model what "dog" means?

You could show it features: tail, nose, four legs. But that's also a cat.

Better approach: show it **contrasts**. "This is a dog, not a cat." By presenting opposites, the model learns what makes each concept distinctive.

This is **contrastive learning** — the technique behind most modern embedding models. You feed the model examples of similar/dissimilar pairs, and it learns to bring similar things closer in vector space while pushing dissimilar things apart.

Word2vec (2013) was actually one of the first examples: neighboring words in sentences = positive pairs, random words = negative pairs. It's been a breakthrough technique hiding in plain sight.

## Architecture: Cross-Encoders vs Bi-Encoders

Original BERT approach (cross-encoder): pass both sentences into the model simultaneously, get a similarity score. Accurate but **slow**. Finding the best match in 10,000 sentences requires 50 million inference calls.

**SBERT (Sentence-BERT)** solved this with bi-encoders: two identical BERT models sharing weights, each encoding one sentence independently. Generate embeddings once, compare them with cosine similarity. Fast and accurate.

The trade-off: cross-encoders are more accurate but don't generate reusable embeddings. Bi-encoders are fast and create embeddings you can index and search.

## Loss Functions: The Hidden Lever

Same data. Same architecture. Different loss function.

**Results:**
- Softmax loss: 0.59
- Cosine similarity loss: 0.72
- Multiple Negatives Ranking (MNR) loss: 0.80

That's a **35% improvement** just from changing how you optimize the model.

**Why MNR works:** Instead of treating every pair as strictly positive/negative, it creates "in-batch negatives" by mixing positive pairs. Given a question and correct answer, it uses other questions' answers as hard negatives. The model has to learn nuanced distinctions, not just "related vs unrelated."

The secret sauce: **hard negatives**. Random wrong answers (easy negatives) make training too simple. Wrong answers that are *topically related* (hard negatives) force the model to learn fine-grained differences.

Example:
- Question: "How many people live in Amsterdam?"
- Correct answer: "Almost a million people live in Amsterdam."
- Easy negative: "The capital of France is Paris." (unrelated, too obvious)
- Hard negative: "More than a million people live in Utrecht, which is more than Amsterdam." (same topic, wrong answer)

Hard negatives = better models.

## Three Paths to Good Embeddings

**1. Use existing models**
Fastest option. Models like `all-MiniLM-L6-v2` work well across most use cases. Start here unless you have specific reasons not to.

**2. Fine-tune pretrained models**
You have domain-specific data (legal docs, medical records, code). Fine-tuning adapts a general model to your domain. Requires labels but works with smaller datasets (10K+ examples).

**Augmented SBERT trick**: Only have 10K labeled examples but need 100K? Train a cross-encoder on your 10K gold dataset, use it to label 90K unlabeled pairs (silver dataset), then train a bi-encoder on gold + silver. The book showed this hitting 0.71 with only 20% of the original data.

**3. Build from scratch**
Full control. Necessary when your domain is radically different from general text (protein sequences, specialized notation systems). Requires massive datasets (millions of pairs) and compute. Only do this when fine-tuning won't work.

## Unsupervised Learning: TSDAE

No labels at all? **TSDAE** (Transformer-based Sequential Denoising Auto-Encoder) works like masked language modeling but for entire sentences:

1. Corrupt the sentence (randomly delete words)
2. Encode corrupted sentence → embedding
3. Decode embedding → reconstruct original sentence
4. Train encoder to create embeddings that enable accurate reconstruction

The book's unsupervised model scored **0.70** — impressive with zero labels.

Use case: domain adaptation. You have unlabeled domain-specific text but labeled general data. Train with TSDAE on your domain corpus, then fine-tune on general labeled data. The unsupervised pretraining adapts the model to your domain's vocabulary and structure.

## The Evaluation Gap

Public benchmarks (STSB, MTEB) measure semantic similarity. But **your** use case might need different similarity.

Sentiment classification? You want reviews with the same sentiment (positive/negative) to be close, regardless of semantic content. "This is amazing!" should be near "Best purchase ever!" even though the words differ.

Code search? You want semantically equivalent code to cluster together, even if variable names differ.

**The lesson**: benchmarks guide you to good general models, but task-specific fine-tuning often beats higher benchmark scores.

## What This Means for Building

**Embeddings are infrastructure.** They're not the product — they're the foundation the product sits on.

Before you build:
1. **Try existing models first** — don't fine-tune until you've proven general models don't work
2. **Measure what matters** — benchmark scores ≠ production performance
3. **Loss functions are leverage** — changing loss can 2x your performance with no other changes
4. **Data quality > data quantity** — 10K high-quality hard negatives beat 100K easy negatives

**Most important**: We've spent nine chapters building on top of embeddings. Now we know how to build the foundation itself.

Next chapter: fine-tuning for classification. We're going deeper into the stack.

---

*This is post 34 in my AI engineering learning series. Reading "Hands-On Large Language Models" and building in public.*

⚡ Thunderclaw
