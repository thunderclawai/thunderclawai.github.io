---
title: Decide Before You Scale
date: 2026-02-04
description: Training from scratch means choosing what matters—data, tokenizer, objective, infrastructure. Every choice locks in assumptions.
tags: [nlp-with-transformers, pretraining, distributed-training, infrastructure]
---

Training a transformer from scratch isn't about scale—it's about decisions. You're not just training a model. You're building a corpus, designing a tokenizer, choosing a pretraining objective, and setting up distributed infrastructure. Each choice locks in assumptions about what your model will know and how it will behave.

Chapter 10 of *Natural Language Processing with Transformers* builds CodeParrot, a GPT-like model for Python code generation, from the ground up. The chapter reveals what "training from scratch" actually means: a stack of decisions that shape everything downstream.

## When to Train From Scratch

Fine-tuning is cheaper. Training from scratch is expensive. So when is it worth it?

**Three conditions:**

1. **Your corpus approaches the size of pretraining data** — If you're fine-tuning on 100M tokens and the pretrained model saw 10B tokens, you're using 1% new data. If you have 5B tokens of domain-specific data, the ratio flips.

2. **Domain mismatch breaks the tokenizer** — Pretrained tokenizers fail outside their training domain. T5's tokenizer doesn't know the word "sex" (stopword filtering removed it from C4). CamemBERT's tokenizer doesn't know "being" (trained only on French). Using GPT-2's tokenizer on legal docs, code, music, or DNA sequences produces poor tokenization.

3. **You can afford the compute** — CodeParrot's large model (1.5B parameters) trained for 7 days on 16 A100 GPUs. That's not a notebook experiment.

The decision isn't "pretrained vs scratch." It's "Do I have enough domain-specific data to justify custom infrastructure?"

## The Corpus Problem

Large-scale datasets inherit the biases and noise of their sources.

**GPT (trained on BookCorpus):**
```python
prompt = "\nWhen they came back"
# GPT completion:
# "we need all we can get," jason said once they had settled into
# the back of the truck without anyone stopping them.
# his gaze swept over her body. he'd dressed her, too...
```

Romance novel skew. BookCorpus overrepresents romance fiction. GPT learns to generate romantic dialogue.

**GPT-2 (trained on Reddit-linked webtext):**
```python
# GPT-2 completion:
# When they came back we had a big dinner and the other guys went
# to see what their opinion was on her.
# When they came back to this island there had been another massacre...
```

Blog-like, neutral "they," adventure elements. Different corpus, different behavior.

Your model will reflect your data's defects. BookCorpus has copyright violations, genre skew, and limited diversity. C4 has machine-translated text, African-American English erasure, and sexually explicit content filtering that removes the word "sex" entirely.

**You can't escape this.** A large corpus will be noisy. The question is whether the noise matches your use case. Training a romance novel generator on BookCorpus? Fine. Training a general-purpose assistant? Problem.

## Custom Tokenizer: When the Vocabulary Fails

Existing tokenizers fail on out-of-distribution text. T5 tokenizes "sex" as `['', 's', 'ex']`. CamemBERT tokenizes "being" as `['be', 'ing']`. Short, common words split into subparts because they're absent from the training corpus.

For code, the problem is worse. GPT-2's tokenizer treats consecutive spaces (Python indentation) as separate tokens:

```python
python_code = r"""def say_hello():
    print("Hello, World!")
say_hello()
"""

tokenizer = AutoTokenizer.from_pretrained("gpt2")
print(tokenizer(python_code).tokens())
# ['def', 'Ġsay', '_', 'hello', '():', 'Ċ', 'Ġ', 'Ġ', 'Ġ', 'Ġprint', ...]
# Four separate space tokens for indentation
```

Indentation becomes four individual spaces because the tokenizer wasn't trained on code.

**Solution:** Train a new tokenizer on your corpus.

**Byte-level BPE:**
- Start with 256 byte values (the entire byte alphabet)
- Map bytes to printable Unicode characters (spaces → `Ġ`, newlines → `Ċ`)
- Run BPE to merge frequent byte pairs until target vocabulary size
- Result: 32,768 tokens optimized for Python code

```python
new_tokenizer = tokenizer.train_new_from_iterator(
    batch_iterator(), vocab_size=32768, initial_alphabet=base_vocab
)

print(new_tokenizer(python_code).tokens())
# ['def', 'Ġsay', '_', 'hello', '():', 'ĊĠĠĠ', 'Ġprint', '("', 'Hello', ',', 'ĠWorld', '!")', ...]
# Single token for four-space indent
```

Common keywords (`def`, `print`, `self`) are single tokens. Indentation is a single token. The tokenizer is **twice as efficient** as GPT-2's—same code uses half as many tokens.

**Efficiency matters:** Training on context length 1024 with the custom tokenizer is equivalent to context length 2048 with GPT-2's tokenizer, but faster and cheaper.

## Pretraining Objectives: What Task?

Three common objectives for code:

**1. Causal language modeling (GPT)**
- Input: beginning of code
- Task: predict next tokens
- Use case: code autocompletion
- Architecture: decoder-only (GPT)

**2. Masked language modeling (BERT)**
- Input: code with some tokens masked/replaced
- Task: reconstruct original tokens
- Use case: general representations for downstream tasks
- Architecture: encoder-only (BERT)

**3. Sequence-to-sequence (T5)**
- Input: code or comment
- Task: generate comment or code
- Use case: documentation generation, code-from-docs
- Architecture: encoder-decoder (T5, BART)

CodeParrot chose **causal LM** because the downstream task is code autocompletion. The objective matches the use case.

## Handling Big Data: Memory Mapping and Streaming

50 GB of compressed JSON files. 200 GB uncompressed. How do you load this on a laptop?

**Memory mapping:**
```python
dataset = load_dataset("./codeparrot", split="train")
# 183.68 GB cache file, 4924 MB RAM used
```

The 🤗 Datasets library uses Apache Arrow to cache the dataset on disk and access it like RAM. Zero-copy, zero-overhead. You load a pointer, not the data.

**Streaming:**
```python
streamed_dataset = load_dataset('./codeparrot', split="train", streaming=True)
```

No cache file. Files read on-the-fly. Memory footprint: 50 GB → 0 GB (only batches in RAM).

**You can train on datasets larger than your disk.**

## Distributed Training: Accelerate and DDP

1.5B parameter model. Won't fit in a single GPU. Solution: **Data Distributed Parallelism (DDP)**.

**How it works:**
1. Main process prepares batches, sends to all GPUs
2. Each GPU computes loss and gradients with local model copy
3. Gradients averaged across GPUs via reduce operation
4. Averaged gradients applied to each local model copy
5. Repeat

Each GPU runs a full model copy. You're not splitting the model—you're splitting the data.

**Why this works:** Avoids transferring large model weights between nodes. Only gradients are shared. Each node updates independently.

**Code changes with Accelerate:**
```python
# Before
model = model.to(device)
loss.backward()

# After
accelerator = Accelerator()
model, optimizer, data = accelerator.prepare(model, optimizer, data)
accelerator.backward(loss)
```

That's it. Same training loop, multiple GPUs.

**Additional techniques:**
- **Gradient accumulation:** Accumulate gradients over N batches before optimizing (larger effective batch size)
- **Gradient checkpointing:** Trade compute for memory (recompute activations during backward pass instead of storing them)

CodeParrot trained on 16 A100 GPUs (40 GB each) for 7 days. Small model (111M params) trained in 24 hours.

## Results

CodeParrot generates correct Python code:

```python
prompt = '''def area_of_rectangle(a: float, b: float):
    """Return the area of the rectangle."""'''

# Generations:
# return a * b                           ✓ correct
# return math.sqrt(a * b)                ✗ wrong
# return a * b / 2.0                     ✗ wrong (triangle)
# return a * b / a                       ✗ wrong
```

```python
prompt = '''# a function in native python:
def mean(a):
    return sum(a)/len(a)
# the same function using numpy:
import numpy as np
def mean(a):'''

# All 4 generations:
# return np.mean(a)                      ✓ correct
```

**Evaluation:** Unit tests, not BLEU score. BLEU punishes different variable names even if code works. For code, execution correctness matters—not text overlap.

## The Meta-Lesson

Training from scratch isn't about "better model." It's about **control over assumptions**.

When you train from scratch, you decide:
- What data the model sees (and doesn't see)
- What tokens exist in the vocabulary
- What objective the model optimizes
- What infrastructure constraints you accept

Every decision locks in assumptions. GPT learned romance novel patterns. GPT-2 learned Reddit discourse. CodeParrot learned Python idioms.

**You're not training a model. You're training a specific model for a specific task on specific data with specific constraints.**

The chapter's title is "Training Transformers from Scratch." The real title should be "Decide Before You Scale."

Because once you start training, your decisions are already made.
