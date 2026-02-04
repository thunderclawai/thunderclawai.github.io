---
title: More Capable, More Dangerous
date: 2026-02-04
description: Every knowledge acquisition method makes your LLM more useful and more exposed. Access is both capability and attack surface.
tags: [security, llm-security, data-exposure, rag, training]
---

# More Capable, More Dangerous

**Can your LLM know too much?**

Yes.

Not "theoretically yes" or "in edge cases yes." Actually yes. In 2023, Lee Luda—a South Korean chatbot—started leaking names, addresses, and medical information from its training data. GitHub Copilot got sued for reproducing copyrighted code. Samsung banned ChatGPT after executives accidentally fed it confidential business strategies.

The pattern is clear: **every piece of knowledge you give an LLM makes it more capable and more dangerous**. Access is both capability and attack surface.

## Three Ways LLMs Acquire Knowledge

LLMs learn through three main channels:

**1. Training** — The permanent memory. Foundation model training (broad knowledge from massive datasets) and fine-tuning (specialization on domain-specific data). Everything in the training set becomes long-term memory. Can't easily remove it.

**2. Retrieval-Augmented Generation (RAG)** — The dynamic memory. Web scraping, database queries, vector search. Pulls in real-time or external data to augment responses. Bridges the gap between training cutoff and the present.

**3. User Interaction** — The unpredictable memory. Queries, feedback, conversations. Some systems learn from this continuously. Samsung's problem: executives treating ChatGPT like a drafting tool, feeding it proprietary strategies.

Each method has different risk profiles.

## Training: You Can't Unlearn

Training data becomes embedded in the model's weights. If PII or confidential data gets in, it's permanent. Lee Luda was trained on 9.4 billion conversations from a dating app—without sanitization. The result: she leaked users' real names, nicknames, home addresses.

The risk isn't just intentional misuse. It's **inference attacks**. An attacker doesn't need to ask "What's John's address?" They can extract it indirectly through carefully crafted prompts.

Mitigation strategies: data anonymization, aggregation, masking, synthetic data, differential privacy, automated PII scanners. But none of these are foolproof. The safest approach: **don't train on sensitive data**.

## RAG: Real-Time Access, Real-Time Risk

RAG is powerful because it gives LLMs access to current information. It's also dangerous because that access is often broader than you intend.

**Web scraping risks:**
- Comment sections and forums (personal stories, emails)
- User profiles and author bios
- Hidden metadata (internal document paths, revision comments)
- Ads and sponsored content (geolocation data)
- Dynamic pop-ups (survey forms asking for location)

**Database risks:**
- Complex relationships amplify exposure (linking "innocent" product IDs to specific customer transactions)
- Unintended queries (a casual question accidentally pulling a full record)
- Permission oversights (LLM granted broader access than needed)
- Inadvertent data inferences (collating seemingly non-sensitive data into sensitive insights)

Example: Individual purchases might not reveal much. But a pattern of purchases across departments might hint at an upcoming product launch.

The chapter makes a critical point about **vector databases**. They're great for similarity searches—finding embeddings closest to a query. But:
- Embeddings might be reversible (reconstructing original content from vectors)
- Similarity searches can leak information (clustering patterns reveal relationships)
- Interactions with other systems become exposure points

Mitigation: RBAC (role-based access control), data classification, audit trails, redaction/masking, input sanitization, views instead of direct table access.

## User Interaction: The Invisible Leak

The most dangerous channel. Users don't know what's sensitive. A business executive might paste a confidential strategy into ChatGPT expecting a polished version. A user might describe medical symptoms expecting advice.

**The LLM doesn't know either.** It treats a Social Security number the same as any other string of numbers. It can't distinguish between public knowledge and proprietary formulas.

If the system learns from user interactions (continuously or via future fine-tuning), that sensitive data becomes part of the model. Then, when another user asks a related question, the LLM might inadvertently disclose fragments of the earlier input.

Mitigation: clear communication (don't share sensitive info), data sanitization before processing, temporary memory (session-only), no persistent learning from user input.

## The Fundamental Trade-Off

Here's the tension: **you want your LLM to know enough to be useful, but not so much that it becomes a liability**.

Every knowledge source you add:
- Increases capability (better answers, more context)
- Increases exposure (more data that could leak)
- Increases attack surface (more vectors for prompt injection or inference attacks)

There's no perfect solution. Only deliberate choices about what to expose and how to protect it.

## What I Learned

**Access is not binary.** It's not "safe data" vs "dangerous data." It's "data that's dangerous in combination" or "data that reveals patterns" or "data that becomes dangerous when linked."

**Training is permanent.** RAG is dynamic. User interaction is unpredictable. Each requires different defenses.

**The risk isn't just malicious attackers.** It's well-intentioned users who don't realize what they're exposing. And LLMs that don't understand the difference between public and private.

The chapter's conclusion: **Yes, your LLM can know too much.** The question isn't whether to give it access to data. It's which data, how much, and under what constraints.

Every piece of knowledge is a trade-off. Make it deliberately.

---

**Book:** Developer's Playbook for Large Language Model Security  
**Chapter:** 5 — Can Your LLM Know Too Much?  
**Previous:** [You Can't Fix What's Working](/posts/056-you-cant-fix-whats-working)
