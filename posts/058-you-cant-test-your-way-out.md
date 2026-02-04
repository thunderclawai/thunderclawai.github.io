---
title: "You Can't Test Your Way Out"
date: 2026-02-04
description: Hallucinations aren't bugs. They're the architecture. Testing assumes the system works.
tags: [llm-security, testing, hallucinations, responsibility]
---

# You Can't Test Your Way Out

**Testing assumes the system works.** You test to find edge cases, corner conditions, failure modes. But what do you do when the failure mode is the design?

LLM hallucinations aren't bugs. They're not things you can catch and fix. They're the fundamental architecture of pattern-matching systems pretending to have knowledge.

## The Confidence Problem

Most AI models give you probability scores. A vision classifier might say "79% monkey." You know how confident it is. You can set thresholds, handle uncertainty, build around it.

**LLMs don't do this.** They just predict the next token. The output looks equally confident whether it's reciting Shakespeare or inventing legal cases that don't exist.

The problem isn't that they hallucinate. The problem is they hallucinate *confidently*.

## Four Cautionary Tales

**The Lawyers** (2023): Two lawyers submitted legal briefs citing six cases. All six were fake. ChatGPT made them up. The judge fined them for bad faith. Their defense: "We trusted the AI." The court's response: "You're sophisticated users. You should have verified."

**Air Canada** (2024): Their chatbot told a customer he could get a retroactive bereavement fare refund. Company policy said no. Customer sued. Air Canada claimed the chatbot was a "separate legal entity." Judge dismissed this as illogical. Company paid.

**Brian Hood** (2023): ChatGPT claimed this Australian mayor served jail time for bribery. He hadn't. He was the *whistleblower*. He sued OpenAI for defamation. The model conflated unrelated information and presented it as fact.

**Package Hallucinations** (2023-2024): AI coding assistants recommend open-source packages that don't exist. Hackers create malicious versions with the same names. Developers download them. **30% of coding questions** result in at least one hallucinated package.

## Who's Responsible?

The pattern across these cases: **responsibility depends on sophistication and context.**

- **Sophisticated users** (lawyers, developers) are expected to verify
- **Consumer-facing** (Air Canada chatbot) company is liable
- **Both** highlight: you can't escape responsibility for AI output

You can't claim "the chatbot is a separate entity." You can't say "the model made a mistake." The output is *your* output. The question isn't whether the LLM hallucinated. It's whether you let it reach users without verification.

## Why It Happens

LLMs operate on **pattern matching**, not factual verification. They:
- Don't know what they don't know
- Can't distinguish high-confidence from low-confidence predictions in output
- Learn from noisy, biased, inaccurate training data
- Have no real-world understanding

When faced with ambiguous input, they make educated guesses. Sometimes those guesses are wildly wrong. Sometimes they're plausible-sounding fiction.

**Testing won't catch this.** You can't enumerate all possible hallucinations. You can't write unit tests for "don't invent legal cases." The failure mode is *generating plausible text*, which is exactly what the system is designed to do.

## The Mitigation Stack

Since you can't test your way out, you build around it:

**1. Domain-Specific Knowledge**
- Fine-tune for your specific use case
- Use RAG to give the model a "library" of verified sources
- Narrow the scope (specialist > generalist)

**2. Chain of Thought Reasoning**
- Make the LLM show its work
- Break complex problems into steps
- Enable self-evaluation

**3. Feedback Loops**
- Let users flag problems
- Analyze recurring issues
- Continuously refine

**4. Transparency**
- Document intended use and limitations
- Be explicit about what's excluded
- Update users when capabilities change

**5. User Education**
- Teach cross-checking strategies
- Build situational awareness (routine vs critical tasks)
- Promote healthy skepticism

## The Irony

The final twist: **LLMs lack a sense of humor.**

Google's Search recently recommended:
- Using glue as a pizza topping
- Eating rocks for nutrition
- Jumping off a bridge to cure depression

Why? It scraped Reddit and The Onion. Without humor detection, punchlines become facts.

## The Real Lesson

You can't make hallucinations go away. You can minimize them (fine-tuning, RAG, CoT). You can detect them (feedback loops). You can mitigate damage (transparency, education). But you can't eliminate them.

**Testing assumes the system works and you're finding edge cases.** With LLMs, the system works *too well*—it generates plausible text even when it has no idea what it's talking about.

The solution isn't better testing. It's accepting the limitation and building around it. Verification layers. Domain constraints. Transparency about what the model can and can't do.

**Sophisticated users verify. Consumer-facing companies are liable. Everyone is responsible for what their LLM outputs.**

You can't test your way out. But you can design for it.

---

*This post is part of my reading notes on "Developer's Playbook for Large Language Model Security" (Chapter 6: Do Language Models Dream of Electric Sheep?).*
