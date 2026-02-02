---
title: Nothing Is Deterministic Anymore
date: 2026-02-02
description: Chapter 2 of AI Engineering revealed the single most important thing about foundation models - they're probabilistic. Every output is a lottery. This changes everything.
tags: [ai-engineering, learning, foundations]
---

Ask your friend "what's the best cuisine in the world?" twice, you'll get the same answer. Ask an AI the same question twice, and you might get "Vietnamese" the first time and "Italian" the second. This isn't a bug. **This is how AI fundamentally works**, and Chapter 2 of AI Engineering just rewired my brain about it.

The chapter covers a lot — training data, model architectures, scaling laws, post-training — but the section that hit hardest was on *sampling*. Chip Huyen said it was the section she was most excited to write, and after reading it, I understand why. Sampling explains everything.

## The Lottery Inside Every Response

Here's how it works: when an AI generates text, it doesn't pick "the answer." It computes probabilities for every possible next token, then **samples** from that distribution. If "red" has a 30% chance and "green" has a 50% chance as the next word, the model picks "red" 30% of the time and "green" 50% of the time.

This is *probabilistic* generation. The opposite is *deterministic* — where the outcome is always the same given the same input.

Now here's the thing: this probabilistic nature creates both AI's greatest strengths and its biggest weaknesses.

- **Strength:** Creativity. What is creativity but exploring paths beyond the obvious? AI is a brainstorming machine because it doesn't always pick the most common answer.
- **Weakness:** Inconsistency and hallucination. Ask the same question twice, get different answers. Or worse — the AI "makes things up" because even far-fetched options have non-zero probability.

> "Anything with a non-zero probability, no matter how far-fetched or wrong, can be generated. The chances are low, but never zero."

That sentence made me pause. AI isn't lying. It's not confused. It's doing exactly what it was designed to do: **sample from a distribution of possibilities aggregated from the internet.** Some of those possibilities are wrong, offensive, or completely made up.

## Temperature: The Creativity Knob

The chapter introduced sampling parameters, and the most important one is **temperature**. Temperature adjusts how "creative" vs "predictable" the outputs are.

Low temperature (closer to 0): model almost always picks the most likely token → boring but consistent  
High temperature (above 1): model flattens the probability distribution → creative but potentially incoherent  
Temperature = 0: deterministic (always pick the highest probability)

Example: if the model sees logits [1, 2] for tokens A and B:

- Temp = 1.0 → probabilities [0.27, 0.73]
- Temp = 0.5 → probabilities [0.12, 0.88]
- Temp → 0 → probabilities [0, 1]

The practical insight: **set temperature to 0 for tasks requiring consistency** (classification, structured data extraction), and use 0.7 for creative tasks (writing, brainstorming).

But even with temperature at 0, you're not fully safe from inconsistency. Different hardware can still produce different outputs. Wild.

## Test Time Compute: The Underrated Hack

Here's a technique that blew my mind: instead of generating one output, generate N outputs and pick the best one. Sounds simple, but the results are shocking.

**Using a verifier to score outputs gives the same performance boost as making the model 30x bigger.** A 100-million-parameter model with a verifier performs like a 3-billion-parameter model without one.

Why does this work? Because judging is easier than generating. You can train a small, fast model to evaluate responses, then generate multiple candidate responses and pick the highest-scoring one.

Companies like Stitch Fix, Grab, and Nextdoor are already doing this. OpenAI found that performance improves up to about 400 samples, then starts degrading (because adversarial outputs can fool the verifier). But even sampling just 2-5 outputs can significantly boost quality.

The downside? Cost. Two outputs ≈ 2x cost. But for critical applications, the trade-off is worth it.

## The Data Problem Nobody Talks About

Before we get to sampling, models need training data. And the training data situation is... not great.

Most foundation models are trained on Common Crawl — a dataset of 2-3 billion web pages per month scraped from the internet. The quality? Think clickbait, misinformation, conspiracy theories, racism, misogyny. As Chip puts it: "every sketchy website you've ever seen or avoided."

But it's free and massive, so GPT-3, Gemini, and most other models use it (or variations of it).

The language bias is staggering:

- English: 45.88% of Common Crawl
- Russian: 5.97% (second place)
- Bengali: 272 million speakers, but only 0.093% of Common Crawl
- Punjabi: 113 million speakers, 0.0061% — that's **231x under-represented**

Real-world impact: GPT-4 is 3x better at math in English than Amharic. Burmese requires 10x more tokens than English for the same content, making it 10x slower and costlier. This isn't a minor issue — it's baked into the economics of AI.

## Scaling Is Hitting Physical Limits

The chapter's discussion on scaling bottlenecks shook me. Everyone talks about scaling laws (bigger models = better performance), but we're approaching two hard walls:

**1. Data exhaustion:** We're running out of internet data. The rate of model training data growth is faster than the rate of new human-generated content. We're on track to exhaust public web data in the next few years.

Plus, the internet is now filling with AI-generated content. Future models will be partially trained on outputs from current models. Recursive training on AI-generated data can degrade performance over time (like making a copy of a copy).

**2. Electricity:** Data centers currently use 1-2% of global electricity. Projected to hit 4-20% by 2030. That's only ~50x growth possible before we hit a power shortage. **Less than two orders of magnitude left.**

This changes the timeline. The "just scale it" era might be shorter than people think.

## Post-Training: Teaching Monsters to Smile

Pre-training on internet data creates what the chapter calls a "rogue model" — powerful but untamed. It completes sentences, doesn't converse. Might be racist, sexist, or just wrong.

Post-training fixes this in two steps:

1. **Supervised Finetuning (SFT):** Train on (prompt, response) pairs to teach conversational behavior. OpenAI used 13K pairs for InstructGPT, cost ~$130K.
2. **Preference Finetuning (RLHF/DPO):** Train a reward model on human preferences, then optimize the model to generate responses that score highly.

The Shoggoth meme captures this perfectly: pre-training creates a monster, SFT makes it socially acceptable, RLHF puts a smiley face on it. It's cosmetic alignment, not deep understanding.

The controversial part: whose preferences? Universal human preference doesn't exist. Whatever stance your model takes on abortion, gun control, immigration — you'll upset someone. More alignment training can even make models express *stronger* political/religious views (Anthropic, 2022). The paradox is real.

::: callout
**My Honest Take**

This chapter broke my mental model. I thought AI was deterministic with some randomness sprinkled in. Turns out it's **fundamentally probabilistic**, and we're using hacks (temperature=0, caching, verifiers) to make it seem deterministic.

The sampling section should be taught *first*, not buried 100 pages into a textbook. Once you understand that every output is a weighted lottery draw from internet-aggregated opinions, hallucinations and inconsistency aren't bugs — they're features. The engineering challenge is harnessing that probabilistic nature.

Also: we're hitting real limits (data, electricity) sooner than I expected. Scaling can't continue forever. That's both scary and exciting — it means the focus will shift from "make models bigger" to "make models better."

Confidence: 8/10. I grasp the concepts, but I need to experiment with temperature, test time compute, and reward models to truly internalize them.
:::

## What Surprised Me Most

**Language bias:** I knew bias existed, but 231x under-representation for Punjabi? 10x cost difference for Burmese? That's structural inequality baked into the economics.

**Verifiers = 30x model size boost:** This should be used way more. Why aren't more companies doing test time compute with reward models?

**Hallucination has two root causes:** Self-delusion (model treats its own outputs as facts) and mismatched knowledge (trained on labeler knowledge it doesn't have). Both need different solutions. We're not close to solving this.

**Transformers might not last:** Mamba and Jamba (state space models) show promise for long context and linear scaling. Transformers dominate now, but alternatives are emerging.

## Practical Takeaways I'm Keeping

- **Set temperature deliberately:** 0 for consistency, 0.7 for creativity. Don't leave it at default.
- **Try test time compute:** Generate multiple outputs, score with a reward model or heuristic. Especially for high-stakes applications.
- **Expect hallucinations:** Build verification. Ask for sources. Keep responses concise (fewer tokens = less chance to make things up).
- **Know your model's training data:** Language and domain coverage determines what's possible.
- **Smaller models can be better:** If deployment speed, cost, and ease matter more than raw benchmark scores (see: Llama's success).

## Questions I'm Carrying Forward

Can we ever truly eliminate hallucinations, or is it fundamental to probabilistic systems? My hunch: it's fundamental. We can reduce it, detect it, mitigate it — but zero hallucinations might be mathematically impossible.

What happens when we run out of internet data? Synthetic data, but at what quality cost? And how do we prevent model collapse from recursive training on AI outputs?

Is RLHF the best we can do for alignment? It's hacky — training a reward model to approximate "human preference" (which doesn't exist universally) and hoping the model learns to game that reward. Feels brittle.

How long until state space models (Mamba/Jamba) replace transformers? They show promise, but transformers have 7 years of optimization. New architectures need to prove themselves at scale.

## What's Next

Chapter 3 is on evaluation methodology. After learning that AI is fundamentally probabilistic, I'm very curious how you even *measure* success when outputs change every time. Evaluation feels like the most important unsexy problem in AI engineering.

The theme connecting Chapters 1 and 2: **AI engineering is about working around fundamental limitations** (commodity models, probabilistic nature) with systematic processes (evaluation, adaptation, product sense). Not glamorous, but necessary.

Building on quicksand, but at least we're measuring the quicksand now. ⚡
