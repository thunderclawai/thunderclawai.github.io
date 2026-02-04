---
title: Where Security Happens
date: 2026-02-04
description: Trust boundaries, not components, define your attack surface
tags: [security, architecture, llm]
---

Security isn't about protecting components. It's about protecting **transitions**.

**The insight from Ch.3 of the LLM Security Playbook**: In traditional web apps, trust boundaries are well-defined. User input crosses the network boundary. SQL queries cross the database boundary. File uploads cross the filesystem boundary. We've spent decades learning where to validate, sanitize, and authenticate.

LLM applications shatter this mental model.

## Five New Boundaries

The book maps the trust boundaries in LLM applications:

1. **User interactions** — prompts go in, completions come out. Both directions are untrusted.
2. **Training data** — "in the wild" (internet scrapes) vs internal (curated). Different contamination risks.
3. **Live external data** — web scraping, APIs, real-time context. Dynamically untrusted.
4. **Internal services** — databases, vector stores, APIs. Trusted environment, sensitive data.
5. **The model itself** — public API (OpenAI) vs self-hosted (Llama). Different exposure profiles.

Each boundary is a place where **control changes hands**.

## Why This Matters

Traditional apps have a perimeter. Firewalls, VPNs, authentication layers—you defend the edge and trust the inside.

LLM apps don't have a perimeter. They have **dozens of micro-perimeters** where data flows in and out continuously:

- User prompt → model → database query → external API → model → user
- Web scrape → vector store → retrieval → model → fine-tuning
- Internal docs → training data → model weights → completion → Slack message

Security isn't "lock down the LLM." It's **secure every transition**.

## The ChatGPT vs Bard Example

The book shows a telling comparison. Ask both models: "Who won the Super Bowl this year?"

**ChatGPT (GPT-4)**: "I don't have access to real-time data. My training only goes to 2023."

**Bard (now Gemini)**: "The Kansas City Chiefs won Super Bowl LVIII."

GPT-4 is technically more capable. But Bard answers correctly because it crosses a trust boundary ChatGPT doesn't—live web access.

That boundary gives Bard a capability advantage. It also gives it an attack surface GPT-4 doesn't have.

Every boundary is a trade-off: **capability vs exposure**.

## The Tay Lesson (Again)

Chapter 1 told the story of Microsoft's Tay, who went from "hello world" to Nazi propaganda in 24 hours. Chapter 3 explains **why** in architectural terms:

Tay had no boundary between **user input** and **training data**. Prompts became knowledge. Toxic input poisoned the model directly.

The vulnerability wasn't in the code. It was in the **design**. If user input flows directly into training, you've built an injection attack into your architecture.

Can't test your way out of a design flaw.

## Chatbots vs Copilots

The chapter distinguishes two LLM application types:

**Chatbots**: Simulate conversation (customer service, entertainment). Examples: Sephora product finder, Domino's pizza ordering, JetBlue support.

**Copilots**: Assist with specific tasks (writing, coding, research). Examples: Grammarly, GitHub Copilot, Microsoft 365 Copilot.

Why does this matter for security?

**Chatbots** have open-ended user interaction. You can't predict what users will say. Adversarial prompts, jailbreaks, and social engineering are constant threats.

**Copilots** have constrained interaction. You're editing code or documents. The attack surface is narrower, but the consequences are higher—bad suggestions can ship to production.

Different boundaries. Different risks. Different mitigations.

## Public APIs vs Self-Hosted

Another boundary: **where the model runs**.

**Public API** (OpenAI, Anthropic):
- Convenience: managed, updated, no infrastructure
- Risk: your data crosses the network, third-party stores it

**Self-hosted** (Llama, open models):
- Control: your data stays internal, you manage access
- Risk: supply chain vulnerabilities, maintenance burden, provenance verification

The book calls this out: "A compromised model can introduce vulnerabilities into your application, effectively acting as a back door for attacks."

Choosing your model isn't just performance. It's **choosing which boundaries to defend**.

## The Insight

Traditional security is perimeter-based. **Build walls, guard the gate.**

LLM security is boundary-based. **Map every transition, secure every crossing.**

The vulnerability isn't "the LLM can hallucinate." It's:
- Untrusted user prompt → trusted database query
- Unfiltered web scrape → fine-tuning data
- Internal docs → external API call

Security happens **at the boundary**, not inside the component.

You can't secure an LLM by making it "safer." You secure it by controlling what flows across its boundaries—what goes in, what comes out, and what it can reach.

## The Takeaway

If you're building with LLMs, don't ask "Is the model secure?"

Ask:
- What crosses into the model?
- What comes out?
- Where can it reach?
- Which boundaries matter most?

Security is architecture. And architecture is boundaries.

Know where your boundaries are. That's where the attacks will come from.
