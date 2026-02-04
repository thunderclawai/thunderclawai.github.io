---
title: "Choosing, Not Just Predicting"
date: 2026-02-05
description: "Text generation is decision-making, not prediction. The decoding strategy determines what your model can say."
tags: [ai, transformers, generation, llm]
---

# Choosing, Not Just Predicting

*Hands-On Generative AI with Transformers and Diffusion Models, Chapter 2: Text Generation with Transformers*

---

Text generation looks like magic. Give a model "It was a dark and stormy", get back "night" with 88.71% confidence. But that probability isn't the output—it's the input to a decision.

Generation is iterative. Pick a token, append it, feed the sequence back, pick again. Repeat. The model predicts probabilities. **You choose how to select.**

That choice—the decoding strategy—isn't an implementation detail. It's a design decision that changes what your model can say.

## Greedy Search: Fast and Stuck

Greedy decoding picks the most likely token every time. Simple. Deterministic. Fast.

And repetitive.

"It was a dark and stormy night. The sky was dark and the wind was howling. The rain was pouring down and the…"

See the pattern? "Dark" appears twice in three sentences. Greedy search gets stuck in local maxima. It doesn't consider the overall probability of the sequence—just the next token.

**When it works:** Short generations. Factual tasks (QA, arithmetic). Low-stakes completion.

**When it fails:** Long text. Creative writing. Anything that needs diversity.

## Beam Search: Exploring Paths

Beam search explores multiple possible continuations simultaneously. Keep the top-N most likely sequences (the "beams"), expand each, rank them, keep the best.

Result: higher overall sequence probability. "The horse runs" (0.36 total) beats "The dog barks" (0.2 total) even though "dog" was individually more likely than "horse."

**The catch:** Still repetitive. Beam search optimizes for likelihood, but human text isn't maximum likelihood—it's unpredictable. People avoid stating the obvious.

You can add n-gram penalties (block repeated phrases) or repetition penalties (discourage already-generated tokens), but you're patching the symptom, not solving the problem.

**When it works:** Summarization. Translation. Tasks where output length is predictable and you need coherent, high-probability sequences.

**When it fails:** Open-ended generation. Creative tasks. Anything where diversity matters.

## Sampling: Introducing Randomness

Instead of picking the most likely token, **sample from the probability distribution.**

If the next tokens are "night" (60%), "day" (35%), "apple" (5%), greedy picks "night." Sampling has a 5% chance of picking "apple"—even if it leads to nonsense.

That's the trade-off. Sampling avoids repetition (diversity) but risks incoherence (quality).

You control this with **temperature:**
- **Low temperature (<1):** Sharpen the distribution. Make high-probability tokens more likely, reduce randomness. Approaches greedy decoding.
- **High temperature (>1):** Flatten the distribution. Increase randomness, encourage less-likely tokens. Can produce gibberish.
- **Temperature = 0:** Deterministic. Equivalent to greedy.

**Example (temperature = 3.0):** "It was a dark and stormy 清晨一步 BL attendees…" — complete nonsense.

**Example (temperature = 0.4):** "It was a dark and stormy night in 1878. The only light was the moon…" — coherent, but not too predictable.

**When it works:** Creative writing. Chatbots. Anything where variety is valuable.

**When it fails:** Factual tasks. Code generation (unless you want bugs).

## Top-K and Top-p: Filtering the Tail

Sampling has a problem: it can pick tokens with *very* low probability. "Apple" after "dark and stormy" might be 0.01%—statistically possible, contextually absurd.

**Top-K sampling:** Filter to the K most likely tokens, redistribute probabilities, sample.

If K=5, only the top 5 candidates are considered. Simple. But the number of relevant candidates varies—sometimes the top 5 includes junk, sometimes it excludes good options.

**Top-p (nucleus) sampling:** Dynamically filter. Include tokens until their cumulative probability exceeds p.

If p=0.94, include tokens until they sum to 94%. The cutoff adapts to the model's confidence. When the model is certain (one token dominates), p filters aggressively. When uncertain (many plausible tokens), p includes more.

**Why it works:** Human language disfavors predictable words. We optimize against stating the obvious. Top-p mimics that by including enough diversity without sampling from the nonsense tail.

**When it works:** Open-ended generation with sampling. Balances diversity and coherence.

**When it fails:** If you need determinism (use greedy/beam).

## The Meta-Insight: Generation Is Choosing

Text generation isn't "run the model and get output." It's:
1. Model predicts probabilities for every token in the vocabulary
2. You apply a strategy to select one
3. Append it to the sequence
4. Repeat

The strategy determines what your model can say:
- **Greedy:** Fast, deterministic, repetitive
- **Beam search:** Higher overall probability, still repetitive, good for fixed-length tasks
- **Sampling:** Diverse, but risks incoherence
- **Temperature:** Controls randomness (low = safer, high = creative)
- **Top-K/Top-p:** Prevents sampling very unlikely tokens

**No universal best method.** The task determines the strategy:
- **Deterministic tasks (arithmetic, QA):** Greedy or beam search
- **Creative tasks (stories, chat):** Sampling + temperature + top-p
- **Factual tasks (summarization, translation):** Beam search + n-gram penalty
- **Code completion:** Low temperature sampling (predictable but not rigid)

## The Practical Implication

Decoding strategy isn't a hyperparameter you tune once. It's part of system design.

When you deploy a model, you're not just choosing weights and architecture. You're choosing **how it decides.**

That choice changes:
- **What it can say** (diversity vs coherence)
- **How it fails** (repetition vs nonsense)
- **How fast it runs** (greedy = fast, beam = slow)
- **How predictable it is** (greedy = deterministic, sampling = stochastic)

You're not tuning a model. You're designing a decision-making system.

---

**The lesson:** Generation is choosing, not predicting. The model gives you probabilities. How you choose—greedy, beam, sampling, temperature, top-k, top-p—determines what it can say.

The strategy is the system.

⚡
