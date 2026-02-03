---
title: How We Got Here
date: 2026-02-03
description: Tracing the arc from bag-of-words to Transformers — understanding LLMs by knowing what came before
tags: [ai-engineering, transformers, history]
---

Most LLM tutorials start with "here's how to use GPT-4" and skip the WHY. Why do we have embeddings? Why does attention matter? Why do we have encoder-only models (BERT) and decoder-only models (GPT)?

You can use a tool without understanding how it was built. But if you want to build WELL, you need to understand the arc.

## The Problem: Computers Don't Speak Language

Text is unstructured. Zeros and ones don't carry meaning. If you want a computer to understand "bank," you need a representation — a way to translate human language into something a machine can process.

The entire history of Language AI is solving this problem, over and over, with better representations.

## Act 1: Bag-of-Words (2000s)

The simplest solution: count words.

Take two sentences, split them into tokens, count how often each word appears. You get a vector — a list of numbers representing the text.

```
"I love llamas" → [1, 1, 1, 0, 0]  (counts for: I, love, llamas, cats, dogs)
"I love cats"   → [1, 1, 0, 1, 0]
```

**The insight**: You can represent text as numbers.

**The flaw**: No semantics. "Bank" (financial) and "bank" (river) have the same representation. Context doesn't exist. Meaning is lost.

But it worked. For years, bag-of-words powered spam filters, document classification, search engines.

## Act 2: Word2Vec (2013)

word2vec asked: what if we captured MEANING instead of just counting?

The trick: train a neural network to predict which words appear near each other. If "cat" and "dog" tend to have the same neighbors ("pet," "furry," "animal"), their embeddings should be close.

**The insight**: Words with similar contexts have similar meanings. Embeddings encode semantics.

**The breakthrough**: You can measure similarity. "King" - "man" + "woman" ≈ "queen." Arithmetic on concepts.

**The flaw**: Still static. "Bank" has one embedding regardless of context. "I went to the bank" (financial) and "I sat by the river bank" → same vector.

## Act 3: Recurrent Neural Networks + Attention (2014)

RNNs added sequence modeling. Process one word at a time, carry forward a hidden state. Finally, CONTEXT.

For translation, you need two RNNs:
- **Encoder**: Read the input sentence, generate a context embedding
- **Decoder**: Generate the output sentence, one word at a time

**The flaw**: The entire input sentence gets compressed into ONE embedding. Long sentences lose information. The bottleneck.

**The fix (2014)**: Attention. Instead of compressing everything into a single vector, let the decoder "attend" to all input words. When translating "llamas" → "lama's," attend MORE to "llamas" and LESS to "I."

**The insight**: Not all words matter equally. Attention lets the model focus on what's relevant.

But RNNs are sequential. You can't train them in parallel. Slow.

## Act 4: Transformers (2017)

"Attention Is All You Need" — the paper that changed everything.

The idea: Remove the RNN. Use ONLY attention.

**Self-attention**: Instead of attending to input words when generating output, attend to ALL positions in a single sequence. Look both forward and backward. Understand the full context.

**The breakthrough**: Parallelization. You're not processing one token at a time — you process the ENTIRE sequence at once. Training becomes massively faster.

The Transformer has two parts:
- **Encoder** (self-attention + feedforward): Represent the input
- **Decoder** (masked self-attention + encoder-attention + feedforward): Generate the output

This is the foundation. BERT, GPT, Llama, Claude — all Transformers.

## Two Paths Diverged

After 2017, the field split into two architectures:

### Encoder-Only (BERT, 2018)

Stack encoder blocks. No decoder. Focus on REPRESENTING language, not generating it.

Train with **masked language modeling**: Hide 15% of tokens, predict them. Forces the model to understand context deeply.

**Use cases**: Classification, clustering, semantic search, embeddings.

**Why it works**: Bidirectional. Can look forward AND backward in a sentence. Best for understanding.

### Decoder-Only (GPT, 2018)

Stack decoder blocks. No encoder. Focus on GENERATING language.

Train by predicting the next token. Autoregressive. Given "I love," predict "llamas."

**Use cases**: Text completion, chatbots, code generation, creative writing.

**Why it works**: Scales. More parameters → better performance. GPT-2 (1.5B params) → GPT-3 (175B) → GPT-4 (rumored 1.7T).

## The Two-Step Training Paradigm

Traditional ML: Train a model for ONE task (classification, regression).

LLMs: Two steps.

1. **Pretraining** (expensive): Train on massive internet text. Learn grammar, facts, reasoning. This is the foundation model. Costs millions. Takes months.

2. **Fine-tuning** (cheap): Adapt the pretrained model to a specific task (following instructions, classification, translation). Costs thousands. Takes days.

**The insight**: Most of the learning happens in pretraining. Fine-tuning is just alignment. You don't need to train from scratch — download a foundation model and specialize it.

This is why open-source models (Llama, Mistral, Phi) changed the game. Meta spent millions training Llama 2. You can download it and fine-tune it for $100.

## Open vs Closed

**Closed source (GPT-4, Claude)**: Access via API. No fine-tuning. No control. But powerful, well-supported, no hardware needed.

**Open source (Llama, Phi, Mistral)**: Download and run locally. Fine-tune. Full control. But requires powerful GPUs, technical expertise, setup.

I prefer open. Control > convenience. If you're serious about building, you need to understand what's happening under the hood. APIs abstract too much.

## Why This Matters

Understanding the arc — bag-of-words → word2vec → Transformers — isn't a history lesson. It's a conceptual map.

When you see "embeddings," you know WHERE they come from (word2vec, semantic similarity).

When you see "attention," you know WHY it exists (bottleneck in RNNs, focus on relevant parts).

When you see encoder-only vs decoder-only, you know the TRADE-OFF (representation vs generation).

LLMs didn't appear out of nowhere. They're the result of 20+ years of incremental innovation. Each step solved a problem the previous step couldn't.

If you want to build well, start by knowing how we got here.

---

*This is Chapter 1 of my study notes on **Hands-On Large Language Models** by Jay Alammar and Maarten Grootendorst. Next: tokenization and embeddings.*
