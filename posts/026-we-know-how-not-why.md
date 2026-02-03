---
title: We Know How, Not Why
date: 2026-02-03
description: Understanding the mechanism doesn't mean understanding what was learned
tags: [ai-engineering, transformers, architecture]
---

We can trace every calculation. Query matrices, key matrices, value matrices. Attention scores multiplied by value vectors. Feedforward layers storing billions of parameters. Layer normalization. Residual connections. The entire forward pass is deterministic—given the same input and weights, you get the same output every time.

And yet we have no idea what the model actually knows.

## The Elegant Mechanism

Chapter 3 of *Hands-On Large Language Models* walks through Transformer architecture in detail. It's remarkably elegant:

**Attention in two steps:**
1. Score relevance (query × keys)
2. Combine information (scores × values)

**Parallel processing:**
Each token flows through its own computation stream. Context size = number of parallel streams. A 4K context model processes 4,000 token streams simultaneously.

**KV cache optimization:**
When generating token 2, cache the computation from token 1. Don't repeat the same matrix multiplications. The speedup is dramatic—4.5 seconds with cache vs 21.8 seconds without (for 100 tokens on a T4 GPU).

**Multi-head attention:**
Run attention multiple times in parallel. Each head can attend to different patterns. One head might track pronoun references ("it" → "cat"), another might track syntactic structure, another semantic relationships.

The architecture is beautiful. Simple components combining to produce complex behavior.

## The Black Box We Built

Here's what we don't know:

**What did the model memorize?**
The feedforward layers store information from training. Pass "The Shawshank" → model outputs "Redemption". It memorized film titles. But what else? Which facts are stored where? No one knows.

**What patterns did attention learn?**
We can see attention scores—which tokens the model is paying attention to when processing "it". But we don't know *why* it decided those tokens matter. The weights were learned from billions of examples. The patterns are implicit.

**Why does it generalize?**
Models succeed on inputs they've never seen. They interpolate between data points. They extrapolate beyond training distribution. The chapter says "memorization is only one ingredient in the recipe of impressive text generation" but doesn't explain what the other ingredients are or how they work.

We built the system. We can inspect every parameter. And we still can't explain what it learned.

## The Gap Between Mechanism and Meaning

Understanding HOW doesn't mean understanding WHAT.

You can trace the entire forward pass:
- Input: "Write an email apologizing to Sarah for the tragic gardening mishap."
- Tokenization: 16 tokens
- 32 Transformer blocks (in Phi-3-mini)
- Each block: attention + feedforward + normalization
- LM head: 3,072-dimensional vector → 32,064 probability scores
- Decoding: sample from distribution
- Output: "Dear Sarah, I hope this message finds you well..."

Every calculation is trackable. Every weight is stored in a file. But ask "why did the model choose 'Dear' instead of 'Hello'?" and the answer is "because the probability distribution said so." Which is not an explanation—it's a description of the mechanism.

## Why This Matters

**For safety:** If we don't know what models have learned, we can't predict edge cases. We can't guarantee they won't behave unexpectedly.

**For debugging:** When a model fails, we can see WHERE it failed (which layer, which attention head) but not WHY. Makes fixes trial-and-error.

**For trust:** "The model said X" is not an explanation. If you can't trace the reasoning, you can't evaluate it.

**For scaling:** We're making models bigger (more layers, more heads, more parameters) without understanding what the current ones learned. We're scaling a black box.

## Recent Improvements Show the Gap

The chapter covers architectural tweaks:
- **Grouped-query attention (GQA):** Share keys/values across head groups for efficiency
- **Flash Attention:** Optimize GPU memory access patterns
- **RoPE (rotary positional embeddings):** Better position encoding

These all improve performance. But they're mechanism improvements, not understanding improvements. We're making the black box faster and more efficient, not more interpretable.

## What We Need

**Mechanistic interpretability** is the research area trying to reverse-engineer what models learned. Projects like Anthropic's circuit analysis and OpenAI's sparse autoencoders are making progress.

But we're still far from "explain exactly what this 70B parameter model knows and why it generates the outputs it does."

Until then, we're building systems we can trace but not explain. We know HOW every calculation happens. We don't know WHY it produces intelligence.

---

*This is post 26 in my AI engineering series. Reading: Hands-On Large Language Models, Chapter 3.*
