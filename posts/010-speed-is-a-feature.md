---
title: Speed Is a Feature
date: 2026-02-02
description: Why inference optimization matters more than you think — and how to make models faster and cheaper.
tags: [ai-engineering, inference, optimization]
---

# Speed Is a Feature

Training gets the headlines. Inference pays the bills.

A shocking stat from Ch.9: **inference accounts for up to 90% of machine learning costs** for deployed AI systems. You train once. You serve forever. And every millisecond matters.

## The Real Bottleneck

Not all slowness is the same. There are two computational bottlenecks:

**Compute-bound:** Limited by FLOP/s. How many operations can your chip execute per second? Image generation (Stable Diffusion) lives here.

**Memory bandwidth-bound:** Limited by data transfer speed. How fast can you move weights from memory to compute units? LLM decoding lives here.

LLM inference has **two phases** with different profiles:

- **Prefill:** Process all input tokens at once. Compute-bound. This determines TTFT (time to first token).
- **Decode:** Generate one token at a time. Memory bandwidth-bound. This determines TPOT (time per output token).

Because they have different bottlenecks, modern inference servers **run prefill and decode on separate machines**. Prefill machines need high FLOP/s. Decode machines need high bandwidth.

## Metrics That Matter

**TTFT (Time to First Token):** How fast does the first token appear? Users expect instant responses for chat (< 200 ms). Document analysis can tolerate seconds.

**TPOT (Time per Output Token):** How fast are subsequent tokens generated? Human reading speed is ~120 ms/token. Faster than that is overkill for streaming.

**Throughput:** Output tokens per second across all users. Directly linked to cost. If your hardware costs $2/hour and generates 100 tokens/s, that's **$5.56 per million tokens**.

**MFU (Model FLOP/s Utilization):** Are you using your expensive chip efficiently? Training typically hits 30-50% MFU. Inference is lower (decoding is bandwidth-bound, not compute-bound).

**MBU (Model Bandwidth Utilization):** For memory-bound workloads, this matters more. Formula: `(params × bytes × tokens/s) / theoretical_bandwidth`. A 7B FP16 model at 100 tokens/s uses 700 GB/s bandwidth.

**The trade-off:** Latency vs throughput. Batching improves throughput but increases latency. LinkedIn reports **2-3x throughput gains** if you're willing to sacrifice TTFT/TPOT.

## The Fastest Wins

### 1. Quantization

32-bit → 4-bit = **8x memory reduction**. No code changes. Works everywhere. QLoRA finetuned a 65B model on a single 48 GB GPU.

BitNet b1.58 uses **1.58 bits per parameter** and matches 16-bit Llama 2 quality. We're approaching the information-theoretic floor of 1 bit.

### 2. Speculative Decoding

Use a small draft model to generate K tokens. Main model verifies them in parallel (verification is faster than generation). Accept the longest valid subsequence.

If acceptance rate is high, you get **K+1 tokens per loop** instead of 1. DeepMind reduced Chinchilla-70B latency by **>50%** with a 4B draft model.

Works because:
- Verification is parallelizable (prefill-like)
- Some tokens are easier to predict (high acceptance rate)
- Decoding is memory-bound (unused FLOP/s capacity)

Frameworks like vLLM, TensorRT-LLM, and llama.cpp support it out of the box.

### 3. Prompt Caching

Cache overlapping prompt segments (system prompts, long documents, conversation history) and reuse across queries.

**Impact:**
- **75-90% cost savings** (longer cached context = higher savings)
- **75% latency reduction** for multi-turn conversations
- If your system prompt is 1,000 tokens and you handle 1M calls/day, you save **1 billion input tokens/day**

Anthropic and Google Gemini both offer this. No code changes needed.

## The KV Cache Explosion

The attention mechanism's dirty secret: generating each new token requires attending to **all previous tokens**. To avoid recomputing, we cache key-value vectors. This cache grows **quadratically** with sequence length.

**Example:** Llama 2 13B with batch size 32, sequence length 2,048 needs **54 GB KV cache** (without optimization). That's more than the model weights!

For a 500B model with batch 512 and context 2,048: **3 TB KV cache**. Three times the model size.

### Solutions

**Redesign attention:**
- Multi-query attention: Share key-value pairs across query heads
- Grouped-query attention: Share within groups (Llama 3 uses this)
- Cross-layer attention: Share key-value vectors across adjacent layers
- Local windowed attention: Attend only to nearby tokens

Character.AI reduced KV cache **20x** with these techniques, making memory no longer a bottleneck for large batch sizes.

**Optimize the cache:**
- **PagedAttention** (vLLM): Split KV cache into non-contiguous blocks, reduce fragmentation
- KV cache quantization: Store in lower precision
- Adaptive compression: Drop less important tokens

**Write better kernels:**
- **FlashAttention:** Fused kernel optimized for NVIDIA GPUs. Faster attention without changing the mechanism.

## Service-Level Wins

These don't change the model — just how you serve it.

### Continuous Batching

**Static batching:** Wait until batch is full. First request waits for last.
**Dynamic batching:** Process batch after time window or when full. Better latency.
**Continuous batching:** Return completed responses immediately, add new requests in their place. Like a bus that picks up new passengers after dropping off old ones.

vLLM pioneered this. Now standard across inference frameworks.

### Decoupling Prefill and Decode

Run prefill (compute-bound) and decode (memory-bound) on **different machines**. They compete for resources if on the same GPU.

Ratio depends on workload. Long inputs + prioritize TTFT = 2:1 to 4:1 prefill:decode ratio.

### Parallelism

**Replica parallelism:** Run multiple copies of the model. Simplest way to handle more load.

**Tensor parallelism:** Split tensors across machines. Required for models too large for one GPU. Reduces latency but adds communication overhead.

**Pipeline parallelism:** Split model into stages, each on different machine. Good for throughput (training), bad for latency (inference).

## What Actually Works

PyTorch team optimized Llama-7B on A100-80GB:

1. `torch.compile` → modest throughput gain
2. INT8 quantization → bigger gain
3. INT4 quantization → even bigger
4. Speculative decoding → massive boost

**Across use cases, the wins are:**
- **Quantization** (works everywhere, easy to implement)
- **Tensor parallelism** (enables large models, reduces latency)
- **Replica parallelism** (straightforward to implement)
- **Attention optimization** (huge for transformers)
- **Prompt caching** (75-90% savings for the right workloads)

## Why This Matters

Faster inference isn't just about cost. It unlocks **new use cases**.

Real-time code completion requires < 100 ms latency. Conversational AI needs instant first tokens. Agentic workflows with multi-step reasoning need high throughput.

The bottleneck isn't models anymore. It's **serving them efficiently**.

---

**Reading:** AI Engineering, Ch.9 — "Inference Optimization"

**Key insight:** Speed is a feature. The faster and cheaper you can serve models, the more ambitious your applications can be. Inference optimization is where engineering skill translates directly into user experience and economics.

Next up: Ch.10 — AI Engineering Architecture and User Feedback.
