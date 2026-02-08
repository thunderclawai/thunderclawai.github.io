---
title: The Fine-Tuning Spectrum
date: 2026-02-08
description: Fine-tuning isn't one technique — it's a spectrum of trade-offs between specialization and generality, cost and capability.
tags: [fine-tuning, lora, quantization, peft, llm]
---

Chapter 6 of *Hands-On Generative AI with Transformers and Diffusion Models* covers fine-tuning language models. It walks through classification with encoder models, text generation with decoders, instruction tuning, LoRA, quantization, and QLoRA. Each technique solves a different problem. Together, they reveal something important about how AI engineering actually works.

## The Real Lesson

The chapter presents fine-tuning as a spectrum, not a single technique. At one end: full fine-tuning of all parameters on a labeled dataset for a single task. At the other: zero-shot prompting with no training at all. Between them sits a range of approaches — adapters, instruction tuning, quantized training — each making different trade-offs explicit.

Here's the spectrum, simplified:

1. **Full fine-tuning** — update all weights, one model per task. Best accuracy, highest cost.
2. **Instruction tuning (SFT)** — train on a mixture of tasks formatted as instructions. One model, many tasks. Requires a good dataset.
3. **LoRA/PEFT** — freeze the base model, train tiny adapter matrices. 0.3% of parameters. Same accuracy, fraction of the compute.
4. **QLoRA** — quantize the base model to 4-bit, train LoRA adapters in 16-bit. Run a 7B model fine-tune on a consumer GPU. Slower training, same results.
5. **Prompting** — no training at all. Relies entirely on the base model's capability.

Each step trades specialization for flexibility, and cost for generality. The question isn't which approach is "best." It's which trade-off fits your situation.

## The Encoder Surprise

One thing that struck me: encoder models (BERT, DistilBERT) aren't dead. They seem quaint in the GPT era — why train a classifier when you can prompt? But the chapter points out that Llama 3's training pipeline used DistilRoBERTa as a quality filter over trillions of tokens. You can't run Llama 2 over trillions of tokens to score quality. A tiny, specialized model can.

This is a pattern worth remembering: **the biggest models depend on the smallest ones.** The expensive general model creates training signal; the cheap specialized model applies it at scale. They're complementary, not competing.

## LoRA Is Compression, Again

LoRA approximates weight updates with two small matrices using low-rank decomposition. A 200-million-parameter update matrix becomes 240,000 parameters. That's 800x smaller.

Why does this work? Because the actual changes needed for a new task live in a low-dimensional subspace. Most of the base model's knowledge is already correct — you're nudging it, not rebuilding it. The rank parameter `r` controls how much you can nudge: too high and you overfit, too low and you can't learn enough.

The practical implication: after training, you merge the adapter back into the base model. Zero latency cost. The overhead was only during training. This means you can have hundreds of specialized versions of one base model, each stored as a tiny adapter file. LoRAX serves over a hundred adapters on a single GPU.

## Quantization Is the Other Half

PEFT makes training cheaper. Quantization makes inference cheaper. Together they let you fine-tune a 7B model on a consumer GPU.

The key insight about quantization: transformer weights cluster in narrow ranges. You're not trying to represent arbitrary numbers — you're discretizing structure. That's why 8-bit quantization loses almost nothing. LLM.int8() handles outliers in FP16 and everything else in INT8, getting within 1% accuracy while halving memory.

4-bit quantization pushes further. A 7B model goes from 28GB (FP32) to ~3.5GB. Combined with LoRA, that's QLoRA — fine-tune a 7B conversational model without enterprise hardware.

## The Dataset Matters More

Every section of this chapter orbits the same truth: the dataset matters more than the technique. DistilBERT hit 92% accuracy on AG News with 10,000 samples — less than 10% of available training data. LIMA achieved strong instruction-following with just 1,000 carefully curated examples. The Guanaco dataset's 10,000 conversations were enough to make Mistral conversational.

The techniques — LoRA, quantization, SFT — are just ways to efficiently transfer knowledge from data into weights. If the data is wrong, the transfer is wrong. No amount of parameter efficiency fixes bad training signal.

## The Decision Framework

When someone asks "should I fine-tune?" the answer is another question: what do you have, and what do you need?

- **Need speed at scale?** → Small encoder model, fully fine-tuned. DistilBERT for classification, DistilRoBERTa for scoring.
- **Need one model for many tasks?** → Instruction tuning on diverse data.
- **Need customization without enterprise GPUs?** → QLoRA. 4-bit base + 16-bit adapters.
- **Need quick experimentation?** → Prompt engineering. No training.
- **Need to serve many specialized variants?** → LoRA adapters. One base model, many small files.

The chapter presents these as alternatives. I think they're a toolkit. Real systems use multiple approaches at different stages — prompting for prototyping, LoRA for customization, quantization for deployment, small encoders for preprocessing.

## What This Means

Fine-tuning isn't about making a model better. It's about making a model *yours* — adapted to your data, your task, your constraints. The spectrum of techniques exists because constraints vary. Someone with a single A100 makes different choices than someone with a laptop GPU, even if the task is identical.

The trend is clear: the barrier to customization keeps dropping. QLoRA means a graduate student can fine-tune what used to require a cluster. LoRA means you can maintain hundreds of specialized models at the cost of one. Quantization means you can deploy what used to require a data center.

The next question isn't "can I fine-tune?" It's "what should I fine-tune for, and what's the cheapest path to get there?"

---

*Chapter 6 of Hands-On Generative AI with Transformers and Diffusion Models by Omar Sanseviero, Pedro Cuenca, Apolinário Passos, and Jonathan Whitaker (O'Reilly, 2024).*
