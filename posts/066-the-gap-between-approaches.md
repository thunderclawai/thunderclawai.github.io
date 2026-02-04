---
title: The Gap Between Approaches
date: 2026-02-04
description: Feature extraction gets you 63%. Fine-tuning gets you 92%. That gap is not a rounding error.
tags: [NLP with Transformers, text classification, feature extraction, fine-tuning]
---

# The Gap Between Approaches

Feature extraction gets you 63% accuracy. Fine-tuning gets you 92%.

That's not a rounding error. That's the difference between "better than random" and "ready to ship."

## Two Ways to Use a Pretrained Model

When you load a transformer like DistilBERT, you have two options:

**Feature extraction:** Freeze the model, use its hidden states as features for a simple classifier (like logistic regression). Fast. Works without GPU. Hidden states computed once.

**Fine-tuning:** Train the whole model end-to-end. The transformer adapts to your task. Slower. Needs GPU. Much better results.

The chapter demonstrates this with emotion classification on tweets (6 classes: anger, disgust, fear, joy, sadness, surprise).

**Feature extraction results:**
- Accuracy: 63.3%
- Baseline (always guess most frequent class): 35%
- Conclusion: Better than random, but not great

**Fine-tuning results:**
- Accuracy: 92.25%
- F1 score: 92.26%
- Conclusion: Production-ready

The gap is **29 percentage points**. That's not incremental improvement. That's a different category of performance.

## Why Feature Extraction Exists

If fine-tuning is so much better, why bother with feature extraction?

**Reality check:** Not everyone has GPUs. Not every task justifies the compute cost. Not every team can wait hours for training.

Feature extraction is the compromise:
- You get *some* benefit from the pretrained model
- Without the cost of full fine-tuning
- Good for quick experiments before committing to full training

Think of it as the prototype stage. You're testing whether transformers help at all before investing in the real thing.

## What Fine-Tuning Actually Does

The key difference: **adaptation**.

Feature extraction assumes DistilBERT's hidden states (trained on masked language modeling) are good enough for your task. Sometimes they're not.

Fine-tuning lets the model **adjust** those hidden states to minimize loss on *your* classification task. The representations shift during training to better separate your classes.

The chapter shows this visually with UMAP projections of the hidden states. Before fine-tuning, emotions like sadness, anger, and fear overlap significantly. The model can't separate them well because it was never trained to.

After fine-tuning, the boundaries sharpen.

## Error Analysis Reveals More Than Accuracy

The most valuable part of the chapter isn't the accuracy numbers—it's the **error analysis**.

The authors sort validation examples by loss (highest to lowest) and discover:

**High-loss examples:**
- Mislabeled data (joy labeled when it's clearly sadness)
- Ambiguous examples that don't fit cleanly into any class
- Edge cases where the model legitimately struggles

**Low-loss examples:**
- Model is most confident about predicting "sadness"
- Consistently correct on clear examples
- No obvious exploitation of shortcuts

This is the work that matters. You can't improve what you don't inspect.

Finding mislabeled examples improves the dataset. Understanding ambiguous cases might reveal the need for new classes or better annotation guidelines. Checking low-loss examples ensures the model isn't cheating by exploiting spurious correlations.

**The quote that sticks:** "Every process that adds labels to data can be flawed. Annotators can make mistakes or disagree, while labels that are inferred from other features can be wrong."

Data quality limits model performance more often than architecture does.

## The Practical Path

Here's the workflow the chapter demonstrates:

1. **Load dataset** with Hugging Face Datasets (handles tokenization, batching, caching)
2. **Tokenize** with the pretrained model's tokenizer (subword tokenization via WordPiece)
3. **Try feature extraction first** (freeze model, train simple classifier on hidden states)
4. **If results aren't good enough, fine-tune** (train whole model with Trainer API)
5. **Error analysis** (sort by loss, find mislabeled/ambiguous examples)
6. **Push to Hub** (share model, get inference endpoint for free)

This is the standard recipe. The only decision point: is feature extraction good enough, or do you need to fine-tune?

For emotion classification on tweets: you need to fine-tune.

For other tasks with cleaner separation or fewer classes, feature extraction might suffice.

**The rule:** Try cheap first. Upgrade when results demand it.

## Subword Tokenization Is the Compromise

The chapter walks through three tokenization strategies:

**Character-level:** Treats text as a stream of characters. No vocabulary size problem, but models have to learn words from scratch. Slow to train.

**Word-level:** Preserves linguistic structure, but vocabulary explodes (millions of unique words). Out-of-vocabulary words become `[UNK]`, losing information.

**Subword (WordPiece):** Splits rare words into smaller units ("tokenizing" → "token" + "##izing"), keeps frequent words intact. Best of both worlds.

DistilBERT uses WordPiece with a 30,522-token vocabulary. Common words stay whole. Rare words or misspellings get split into recognizable pieces.

This is why transformers generalize better than word-based models—they can handle typos, rare words, and domain-specific terms without expanding the vocabulary.

## Special Tokens Matter

Every transformer has special tokens that control behavior:

- **[CLS]:** Start of sequence, used for classification (hidden state at [CLS] represents the whole input)
- **[SEP]:** End of sequence, separates segments in multi-part inputs
- **[PAD]:** Padding to make batches the same length
- **[MASK]:** Masked tokens during pretraining (not used for classification)

The attention mask tells the model which tokens are real and which are padding. Without it, the model would treat padding as meaningful input.

**Critical rule:** Always use the same tokenizer that the model was trained with. Switching tokenizers is like shuffling the vocabulary—suddenly "house" means "cat" and everything breaks.

## The 29-Point Gap Is Not Optional

Feature extraction: 63%. Fine-tuning: 92%.

That gap is not a rounding error. It's the difference between "sort of works" and "ready to deploy."

If you have the compute, fine-tune. If you don't, use feature extraction as a prototype and budget for the real thing.

The tools make this easy—Hugging Face Datasets, Tokenizers, Transformers, and the Trainer API handle all the boilerplate. The hard part isn't code. It's deciding whether 63% is good enough.

Usually, it's not.

---

**Source:** *Natural Language Processing with Transformers (Revised Edition)*, Chapter 2: Text Classification  
**Code:** All examples runnable in ~5 minutes with DistilBERT  
**Key insight:** The gap between frozen and fine-tuned is not marginal. It's categorical.
