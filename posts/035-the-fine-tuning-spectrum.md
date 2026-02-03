---
title: The Fine-Tuning Spectrum
date: 2026-02-03
description: Fine-tuning isn't binary. It's a design space with trade-offs.
tags: [ai-engineering, fine-tuning, setfit, bert, practical-ml]
---

Fine-tuning isn't a yes/no decision. It's a spectrum of choices, each with different trade-offs between data requirements, compute costs, and performance.

Most tutorials present fine-tuning as "freeze the model or train it all." Reality is more nuanced.

## Four Approaches

### 1. Full Fine-Tuning

Train the entire pretrained model + classification head together. Both learn from each other during backpropagation.

**Result**: F1 = 0.85 on Rotten Tomatoes sentiment (8,500 training examples)

**Trade-off**: Best performance, but slowest training and requires the most data.

### 2. Frozen Layers

Freeze the pretrained model, only train the classification head.

**Result**: F1 = 0.63 (same dataset, same architecture, only the classification head updates)

**Trade-off**: Much faster training, but 26% performance drop. The model can't adapt its representations to your task.

**Insight**: Representations matter. When you freeze BERT, you're stuck with Wikipedia-trained embeddings. Your classification head tries to work with what it's given, but it's handicapped.

### 3. Few-Shot with SetFit

What if you don't have 8,500 labeled examples? What if you only have 32?

SetFit uses contrastive learning on generated sentence pairs:
1. Generate positive pairs (same class) and negative pairs (different classes)
2. Fine-tune a SentenceTransformer model on these pairs
3. Train a logistic regression classifier on the resulting embeddings

**Result**: F1 = 0.84 with only 32 labeled documents (16 per class)

**Trade-off**: Comparable performance to full fine-tuning with 265x less labeled data. The catch: you need good sentence embeddings to start with.

**Insight**: Contrastive learning is ridiculously data-efficient. 32 examples → 1,280 training pairs (20 pairs per sample × 2 for positive/negative). You're not training on 32 examples, you're training on synthetic variations.

### 4. Continued Pretraining

The three-step approach: Pretrain → Continue pretraining on domain data → Fine-tune on task.

Standard BERT is trained on Wikipedia. But what if your task is medical diagnosis? Or legal document analysis? Or movie reviews with domain-specific slang?

Continue pretraining with masked language modeling on your domain corpus before fine-tuning for classification.

**Trade-off**: Adds training time, but adapts the model's vocabulary and representations to your domain. General BERT → BioBERT → Fine-tuned medical classifier.

**Insight**: Representations encode what the model saw during training. If it never saw "myocardial infarction" or "tort liability" or "jump scare," its embeddings won't capture those concepts well. Continued pretraining fixes this.

## The Decision Tree

**Have 10K+ labeled examples + compute budget?**  
→ Full fine-tuning

**Have <100 labeled examples per class?**  
→ SetFit (few-shot)

**Domain-specific vocabulary?**  
→ Continued pretraining → fine-tuning

**Need fast iteration?**  
→ Frozen layers (accept performance hit for speed)

**No labeled data at all?**  
→ Zero-shot classification (SetFit can generate synthetic examples from label names)

## Named-Entity Recognition: Token-Level Classification

Most classification is document-level: "Is this review positive or negative?"

NER is token-level: "Which words are people? Organizations? Locations?"

**Challenge**: Tokenizers split words into subwords. "Homer" → ["home", "##r"]. You can't label both as B-PER (beginning of person entity) or they'll look like two separate people.

**Solution**: First subtoken gets B (beginning), following subtokens get I (inside). "Dean Palmer" → ["Dean/B-PER", "Palmer/I-PER"].

**Insight**: When you fine-tune, you're not just learning class boundaries. You're learning alignment between your task's granularity and the model's tokenization.

## What This Means for Engineering

Fine-tuning isn't a single technique. It's a design space.

The naive approach: "Should I fine-tune or not?"

The engineering approach: "What constraints do I have, and which fine-tuning strategy fits?"

- **Data constraint** → Few-shot methods (SetFit)
- **Compute constraint** → Freeze layers, accept trade-off
- **Domain constraint** → Continued pretraining
- **Performance constraint** → Full fine-tuning

Every technique has a place. The mistake is treating one as universally correct.

---

**Source**: Chapter 11, *Hands-On Large Language Models* (O'Reilly)
