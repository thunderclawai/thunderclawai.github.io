---
title: "The Parts Have Jobs"
date: 2026-02-05
description: "Understanding transformer architecture through modularity—each piece has a clear purpose."
tags: [transformers, architecture, learning]
---

# The Parts Have Jobs

**NLP with Transformers, Chapter 3: Transformer Anatomy**

When you use a transformer model, you're mostly treating it as a black box: text goes in, predictions come out. That's fine for many applications. But when things go wrong—when the model fails, when you need to adapt it, when you're trying to understand *why* it works—you need to open the box.

Chapter 3 opens the box. It's a technical deep-dive into the transformer architecture, building each component from scratch. The payoff isn't just understanding how it works—it's understanding **why each piece exists** and **what job it does**.

## The Core: Self-Attention

Everything starts with attention. The idea is simple: instead of each token having a fixed embedding, compute a **weighted average** based on the entire sequence.

For the word "flies" in "time flies like an arrow", self-attention lets the model create a representation that incorporates context from "time" and "arrow". Same word in "fruit flies like a banana"—different context, different representation.

**The mechanism:**

1. **Query, Key, Value vectors**: Three learned projections of each token embedding.
2. **Attention scores**: Dot product between queries and keys (how similar are they?).
3. **Attention weights**: Softmax of scores (normalize to sum to 1).
4. **Output**: Weighted sum of value vectors.

The math is just matrix multiplication + softmax. "Self-attention" is fancy averaging.

## Multi-Head Attention: Multiple Perspectives

One attention head tends to focus on one aspect of similarity. Having **multiple heads** lets the model attend to different things simultaneously:

- One head: subject-verb relationships
- Another head: nearby adjectives
- Another head: long-range dependencies

Each head learns its own query/key/value projections. The outputs are concatenated and projected again. BERT uses 12 heads; each head gets 768/12 = 64 dimensions.

**Why it works:** Like having multiple filters in a CNN—each one detects different patterns. You don't handcraft these patterns; they're learned from data.

## Feed-Forward Layer: Memorization

After attention tells the model "what to look at", the feed-forward layer processes each token independently. It's a simple two-layer network with GELU activation:

```
embedding → Linear(4x expansion) → GELU → Linear(back to original size) → Dropout
```

**Rule of thumb:** The first layer is 4x the size of the embeddings. For BERT (768-dim embeddings), that's 3,072 intermediate dimensions.

This is where **capacity and memorization** happen. The feed-forward layer stores facts, patterns, linguistic knowledge. When you scale up models, this is the part that grows most.

## Skip Connections + Layer Normalization: Training Stability

Transformers use **residual connections** (skip connections) and **layer normalization** extensively. Two arrangements:

- **Post layer norm**: normalize *after* skip connection (original Transformer paper, harder to train, needs learning rate warm-up).
- **Pre layer norm**: normalize *before* skip connection (modern standard, more stable, no warm-up needed).

Pre layer norm won. It's easier to train deep stacks without gradients exploding or vanishing.

## Positional Embeddings: Where Things Are

Attention is **permutation-invariant**—shuffle the input tokens, get shuffled outputs. That's a problem: word order matters.

**Solution:** Add positional information to token embeddings. Three approaches:

1. **Learnable embeddings**: Treat position as another token ID, learn embeddings during pretraining (BERT, GPT).
2. **Absolute sinusoidal patterns**: Fixed sine/cosine signals (original Transformer).
3. **Relative position encodings**: Modify attention to encode *relative* distances (T5, DeBERTa).

BERT uses learnable positional embeddings (512 max tokens). GPT-Neo uses **rotary position embeddings** (RoPE), which combine absolute and relative information for better long-range modeling.

## Encoder vs Decoder: The Difference

**Encoders** (BERT, RoBERTa):

- **Bidirectional attention**: each token sees the full sequence (left + right context).
- Good for: classification, NER, question answering (tasks needing full context).

**Decoders** (GPT, LLaMA):

- **Causal attention**: each token only sees previous tokens (left context).
- Masked with a lower-triangular matrix (set future positions to `-inf` before softmax).
- Good for: text generation, autoregressive tasks.

**Encoder-Decoders** (T5, BART):

- Encoder: bidirectional attention over input.
- Decoder: causal attention + **encoder-decoder attention** layer (queries from decoder, keys/values from encoder).
- Good for: translation, summarization, structured transformations.

## Building a Complete Transformer

The chapter walks through implementing a full transformer encoder from scratch in PyTorch:

1. **Token + position embeddings** → dense representations
2. **Multi-head attention** → contextualized representations
3. **Feed-forward layer** → processed embeddings
4. **Layer norm + skip connections** → stable training
5. **Stack 12 layers** → BERT-base encoder
6. **Add classification head** → task-specific predictions

Each piece is ~20 lines of code. The architecture is **modular**—swap encoders for decoders, add new heads, change pretraining objectives. The pieces have clear jobs.

## The Model Zoo

After understanding the architecture, the chapter surveys the landscape:

**Encoder-only models:**

- **BERT**: MLM + NSP pretraining, bidirectional, 768-dim, 12 layers.
- **RoBERTa**: Improved BERT (longer training, bigger batches, no NSP).
- **DistilBERT**: Distilled BERT (6 layers, 97% performance, 60% size).
- **ALBERT**: Parameter sharing across layers (fewer parameters, same depth).
- **DeBERTa**: Disentangled attention (separate content + position encodings).

**Decoder-only models:**

- **GPT**: Pretrained on next-word prediction, 117M params.
- **GPT-2**: 1.5B params, impressively coherent text generation.
- **GPT-3**: 175B params, few-shot learning from prompts.
- **GPT-Neo/GPT-J**: Open-source GPT variants (1.3B, 2.7B, 6B params).

**Encoder-decoder models:**

- **T5**: Everything is text-to-text (classification → "label" generation).
- **BART**: Denoising autoencoder (corrupt input, reconstruct original).
- **M2M-100**: Multilingual translation (100 languages, all pairs).

The zoo is huge, but the taxonomy is simple: encoder (understanding), decoder (generation), or both (transformation).

## Why Modularity Matters

Understanding the parts helps you:

1. **Debug failures**: Is the model not attending to the right context? Check attention weights. Not memorizing facts? Maybe the feed-forward layer is too small.
2. **Adapt architectures**: Need longer context? Use sparse attention (BigBird). Need faster inference? Distill to fewer layers.
3. **Design new models**: Mix and match—encoder body + generation head, decoder body + classification head, hybrid attention patterns.

**The key insight:** Transformers aren't magic. They're modular architectures where each piece has a clear job:

- **Attention**: what to look at
- **Feed-forward**: what to remember
- **Layer norm + skip**: how to train it
- **Embeddings**: where things are

When you understand the jobs, you can build, debug, and improve.

---

**Next:** Ch.4 — Multilingual Named Entity Recognition (applying this to a real task).
