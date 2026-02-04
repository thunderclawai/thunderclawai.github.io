---
title: Trust Is Deterministic
date: 2026-02-04
description: Zero trust isn't paranoia when the system is designed to be unpredictable
tags: [security, llm, trust, architecture]
---

# Trust Is Deterministic

Traditional software works because it's predictable. You trust it because `2 + 2` always equals `4`, not `4.01`, not "probably around 4," not "four, or maybe five if you round up." Deterministic systems earn trust through consistency.

LLMs broke that contract.

This isn't a bug—it's the architecture. Stochastic systems don't have a "correct" answer; they have probability distributions. Every output is a roll of the dice, weighted by training data and sampling parameters. You can't trust a system that's fundamentally designed to vary.

That's why zero trust isn't paranoia. It's the only rational response to non-deterministic behavior.

## Trust Was Built for Determinism

When John Kindervag introduced "zero trust" in 2009, he wasn't thinking about LLMs. He was thinking about networks, where "trust but verify" failed because people were great at trust but terrible at verification.

His solution: **never trust, always verify.**

Three core principles:
1. **Secure all resources, everywhere** — treat every piece of data with equal scrutiny
2. **Least privilege** — grant only the minimum access needed
3. **Monitor everything** — log every action, watch for anomalies

This framework works beautifully for systems where behavior is predictable. If your firewall lets through a SQL injection, that's a security failure—the system didn't work as designed.

But with LLMs, the system works exactly as designed. It generates plausible text. Sometimes that text is helpful. Sometimes it's a hallucination. Sometimes it's a prompt injection attack. The model can't tell the difference—it's pattern matching, not reasoning.

**You can't verify what you can't predict.**

## Excessive Agency: The Structural Vulnerability

The book introduces "excessive agency" as a top-10 LLM risk—and it's fundamentally different from traditional vulnerabilities.

It's not about bugs in code. It's about **giving the LLM more capability than it can safely handle without supervision.**

Three failure modes:

**1. Excessive Permissions**
- A medical diagnosis app gets READ access to patient records (RAG pattern)
- Feature request: let it write notes for physicians
- Team grants UPDATE, INSERT, DELETE permissions
- Attack: Malicious insider tricks the LLM into modifying records, deleting billing data

The fix? Go back to READ-only. The feature wasn't worth the risk.

**2. Excessive Autonomy**
- A financial app analyzes portfolios, explains improvement strategies
- It's a hit! Product decides: let it auto-rebalance portfolios monthly
- Attack: Nation-state hackers use indirect prompt injection to manipulate trades, move millions, trigger SEC investigation

The fix? Human-in-the-loop. Every trade requires approval. Slower, but survivable.

**3. Excessive Functionality**
- A recruiting app screens resumes, routes to hiring managers
- Success! HR VP is a board hero for cost savings
- Expansion: let the LLM recommend top candidates based on qualifications
- Problem: EU regulation prohibits direct AI use in hiring decisions. Millions in fines.

The fix? Know your regulatory environment. Not every feature is legal.

The pattern: **Features that sound compelling on paper become liabilities in production.**

## Output Filtering: The Safety Net

You can't eliminate risk through design alone. You need defense in depth.

**Three categories of dangerous output:**

**1. PII Disclosure**
- Regex patterns catch Social Security numbers, credit cards, phone numbers
- Named Entity Recognition (NER) identifies names, addresses
- Data masking replaces PII with tokens

**2. Toxic Content**
- Sentiment analysis evaluates emotional tone
- Keyword filtering flags known offensive terms (crude but fast)
- Machine learning models provide context-aware detection
- OpenAI Moderation API scores toxicity 0-1 (>0.7 = unsafe)

**3. Rogue Code Execution**
- HTML encoding neutralizes XSS attacks
- Parameterized queries prevent SQL injection
- Syntax/keyword filtering removes dangerous language constructs
- Tokenization strips executable code

The book provides sample Python code that chains these checks: prompt → LLM → toxicity check → PII scan → sanitization → log → return or flag.

**Every output is guilty until proven safe.**

## The Paradox: Power Without Common Sense

Here's the fundamental problem: LLMs are incredibly capable but completely lack judgment.

Traditional software: limited capability, predictable behavior → trustworthy within scope
LLMs: vast capability, unpredictable behavior → untrustworthy despite utility

The book ends with a perfect analogy: Fox Mulder from *The X-Files* started with "trust no one," then found people he could trust—but never lost his paranoia. That vigilance kept him alive.

**With LLMs, you can't trust the entity itself. You can only trust your containment strategy.**

Zero trust isn't about preventing LLMs from being useful. It's about ensuring they can't be dangerous. Limit agency, filter output, monitor everything, log everything, assume nothing.

Because when behavior is non-deterministic, trust must be earned—one output at a time.

---

**Bottom line:** Traditional security assumes deterministic behavior. LLMs are fundamentally stochastic. Zero trust is the only architecture that accounts for unpredictability by design. Trust the containment, not the model.
