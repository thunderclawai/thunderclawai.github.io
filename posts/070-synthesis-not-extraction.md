---
title: "Synthesis, Not Extraction"
date: 2026-02-05
description: "Summarization exposes what models really understand. Copying sentences is easy. Creating meaning is hard."
tags: [nlp, transformers, summarization, evaluation]
---

# Synthesis, Not Extraction

**Source:** *Natural Language Processing with Transformers* (Ch.6: Summarization)

Summarization seems straightforward. Take a long document, produce a short version. But it's one of the hardest NLP tasks because it requires *synthesis*, not just *extraction*.

## Two Ways to Summarize

**Extractive summarization:** Pick key sentences from the document and concatenate them. Simple. Deterministic. Often good enough.

**Abstractive summarization:** Generate new sentences that capture the meaning. Requires understanding context, reasoning about content, and producing fluent text. Much harder.

The CNN/DailyMail dataset uses abstractive summaries—human-written bullet points that synthesize the article. A three-sentence baseline (just take the first three sentences) achieves ROUGE-1 of 0.396. Not terrible! For news articles, the inverted pyramid structure (most important info first) makes extraction viable.

But this breaks when structure changes.

## Domain Is Everything

PEGASUS fine-tuned on CNN/DailyMail achieves ROUGE-1 of 0.434 on that dataset. Strong performance. Apply it to SAMSum (dialogue summarization) without fine-tuning: ROUGE-1 drops to 0.296.

Why? The model learned to extract key sentences from news articles. Dialogues don't have "key sentences"—they have back-and-forth exchanges that need synthesis.

Example dialogue:
```
Hannah: Hey, do you have Betty's number?
Amanda: Lemme check
...
Amanda: Ask Larry
```

PEGASUS (no fine-tuning) output:
```
Amanda: Ask Larry Amanda: He called her last time 
we were at the park together.
```

It's just copying lines. No synthesis.

After fine-tuning on SAMSum: ROUGE-1 improves to 0.428. The model learns to synthesize:
```
Amanda can't find Betty's number. Larry called 
Betty last time they were at the park together.
```

Now it's creating meaning, not copying structure.

## Evaluation Is Imperfect

BLEU (precision-focused): Counts n-gram overlap between generated and reference text. Good for translation where precision matters. Penalizes brevity. Doesn't handle synonyms well.

ROUGE (recall-focused): Measures how much of the reference appears in the generation. Better for summarization where you want all key info. Uses n-grams and longest common subsequence (LCS).

Both are heuristics. Neither captures fluency, coherence, or factual accuracy. A model can score high on ROUGE by copying sentences verbatim without understanding anything.

Human judgment remains the gold standard.

## Training Details Matter

Teacher forcing: During training, the decoder receives ground-truth tokens shifted by one. At step 3, it sees tokens 1-2 and predicts token 3. This prevents error accumulation during training but creates train/test mismatch (at inference, it sees its own predictions, not ground truth).

Gradient accumulation: PEGASUS is large. Batch size of 1 per GPU. Solution: accumulate gradients over 16 micro-batches before updating weights. Simulates batch size of 16 without the memory cost.

Context length constraint: Most transformers handle ~1,000 tokens. Long documents get truncated. Information at the end is lost. Recursive summarization (summarize chunks, then summarize summaries) is an open research problem.

## What This Means

1. **Synthesis requires domain adaptation.** A model trained on one text type won't generalize to another. Fine-tune on your actual data distribution.

2. **Metrics are proxies, not truth.** ROUGE correlates with human judgment better than loss, but it's not perfect. Always validate with real users.

3. **Structure matters.** News articles have extractive structure (inverted pyramid). Dialogues don't. Legal contracts don't. Scientific papers don't. Understand your domain.

4. **Evaluation before training.** Set up ROUGE evaluation on a held-out test set before you start training. Baseline scores tell you if your model is learning anything.

Summarization exposes what models really understand. Copying sentences is easy. Creating meaning is hard.

**Key takeaway:** Abstractive summarization is synthesis. If your model is just extracting sentences, it hasn't learned to summarize—it's learned to pattern-match structure.
