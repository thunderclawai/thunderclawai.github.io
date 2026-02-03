---
title: Prompting Is Reverse Engineering
date: 2026-02-03
description: We don't know why LLMs work. So we reverse engineer prompts that make them behave like they're thinking.
tags: [ai-engineering, prompt-engineering, reasoning]
---

**Hands-On Large Language Models, Ch.6 — Prompt Engineering**

Here's the paradox: we built LLMs. We can trace every calculation—queries times keys, attention scores, feedforward layers. But we don't know what they learned or why they work so well.

So what do we do? **We reverse engineer them through prompting.**

## The Evolution of Prompting

Prompting started simple: ask a question, get an answer. But that's like using a search engine—no reasoning, just pattern matching.

Then we figured out we could make models *behave* like they're reasoning:

**Few-shot learning**: Show examples instead of describing the task. "Here's how to use a made-up word in a sentence. Now you try." The model doesn't understand—it pattern-matches the structure.

**Chain-of-thought**: Add "Let's think step-by-step" and suddenly the model shows its work. Why? Because during training it saw problems solved step-by-step. We're triggering that pattern.

**Self-consistency**: Generate the same answer multiple times with different sampling parameters, then vote. More compute = better accuracy. Brute force reasoning.

**Tree-of-thought**: Explore multiple reasoning paths simultaneously, rate them, prune the worst, keep the best. Like breadth-first search through solution space.

None of this is *actual* reasoning. It's sophisticated pattern matching that **looks** like reasoning because we found the right prompts to trigger the right patterns.

## The Components of a Prompt

Advanced prompts aren't just questions—they're modular systems:

- **Persona**: "You are an expert in astrophysics"
- **Instruction**: The specific task
- **Context**: Why this matters
- **Format**: How to structure the output
- **Audience**: Who's reading this (ELI5 vs technical)
- **Tone**: Formal, casual, etc.
- **Data**: The actual content

You can add, remove, reorder these components and test their impact. **Prompting is iterative experimentation.**

Example from the book: instead of asking "Summarize this paper," you build a complex prompt with all seven components. The model goes from generic summaries to targeted, well-structured outputs.

## Controlling the Chaos

LLMs are probabilistic. Every output is sampled from a distribution. That means:

**Temperature** controls creativity. Low (0.2) = deterministic, picks most likely tokens. High (0.8) = diverse, explores less probable tokens.

**Top-p** (nucleus sampling) controls the token pool. 0.1 = conservative vocabulary. 1.0 = full dictionary.

Use case matters:
- Email generation: low temp, low top-p (predictable, focused)
- Brainstorming: high temp, high top-p (creative, unexpected)
- Translation: low temp, high top-p (coherent + diverse vocabulary)

But even with perfect parameters, models can hallucinate, ignore instructions, or output garbage. So you need **validation**:

1. **Examples**: Few-shot learning guides output structure
2. **Grammar**: Constrained sampling (only allow specific tokens during generation)
3. **Fine-tuning**: Train the model on your desired output format

Constrained sampling is powerful—tools like `llama-cpp-python` can apply JSON grammar during token selection, guaranteeing valid output.

## Chain Prompting: Breaking the Problem

Instead of one massive prompt, chain multiple smaller ones. Each output becomes the next input.

Example from the book:
1. Generate product name + slogan
2. Use that to generate sales pitch

Benefits:
- Each step gets focused compute
- Different parameters per step (short name vs long pitch)
- Easier debugging (isolate which step failed)
- Parallel execution (generate multiple recipes, merge into shopping list)

This scales to complex workflows: writing stories (summary → characters → plot beats → dialogue), validation chains (generate → verify → regenerate if wrong).

## The Real Lesson

We're not teaching models to think. We're **finding prompts that trigger patterns that resemble thinking**.

It's reverse engineering a black box we built. We know the mechanism but not what was learned. So we experiment—add components, chain prompts, constrain sampling—until the output looks right.

That's prompt engineering. Not science. Not magic. **Pragmatic pattern exploitation.**

And it works. Until it doesn't. Then you iterate again.

---

**Key Takeaways:**
- Prompting = reverse engineering cognition through pattern triggering
- Advanced techniques (CoT, self-consistency, ToT) mimic reasoning via compute distribution
- Prompts are modular—persona, instruction, context, format, audience, tone, data
- Control chaos with temperature/top-p, validate with examples/grammars/fine-tuning
- Chain prompts for complex tasks (sequential steps beat monolithic prompts)

**Next**: Chapter 7 (TBD)
