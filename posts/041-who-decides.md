---
title: Who Decides?
date: 2026-02-03
description: Architecture is about control flow—who decides what happens next, the developer or the LLM?
tags: [langgraph, architecture, cognitive-architectures, learning-langchain]
---

# Who Decides?

*Learning LangChain, Chapter 5*

A swimming pool and a one-story house are built from the same materials—bricks, mortar, concrete. What makes them uniquely suited to their different purposes isn't the materials, it's the **plan for how those materials are combined**. That's architecture.

The same is true for LLM applications. You have the same building blocks—prompting, RAG, memory, tool calling. What you're building depends on how you assemble them. More importantly, it depends on **who decides how they're assembled**.

## The Autonomy Spectrum

LLM applications exist on a spectrum of autonomy. The question isn't just "what can the LLM do?" but "what does the LLM *decide*?"

Three levels:

1. **LLM decides the output** — Given a step, the LLM generates the result (draft an email, summarize a document)
2. **LLM decides the next step** — Given options, the LLM chooses which path to take (route to the right retriever, pick the right tool)
3. **LLM decides what steps exist** — The LLM writes code that executes a dynamic action you didn't preprogram (we'll get there in later chapters)

This isn't a feature list. It's a design space. Where you land on this spectrum determines what your application can do—and what can go wrong.

## The Central Trade-Off

The chapter frames this beautifully with an email assistant example. You want it to:
- Archive uninteresting emails
- Reply to some directly
- Mark important ones for your attention

The constraints reveal the tension:
- **Minimize interruptions** (the whole point is to save time)
- **Avoid sending replies you'd never send** (don't embarrass me)

This is the **agency versus reliability trade-off**. More autonomy = more useful. More autonomy = more ways to fail.

You can't escape this trade-off. You can only make it explicit and choose where to land.

## Three Cognitive Architectures

The chapter walks through three architectures that strike different balances:

### Architecture #1: LLM Call

One LLM call. Fixed input, single output. No decisions.

Examples:
- Summarize this document
- Translate this text
- Generate SQL from natural language

The developer controls everything. The LLM just executes.

**When to use:** When the task is well-defined and the output doesn't need to vary based on context beyond the input.

### Architecture #2: Chain

Multiple LLM calls in a **fixed sequence**. Still no decisions—the path is hardcoded.

Example (text-to-SQL):
1. LLM generates SQL query from natural language
2. LLM explains the query in plain English (so user can verify it matches their intent)

You could extend this further:
3. Execute the query against the database
4. LLM summarizes the results into a textual answer

The key: same sequence every time. No branching. No choices.

**When to use:** When you need multiple transformations but the flow is deterministic. The sequence is decided at development time, not runtime.

### Architecture #3: Router

Now it gets interesting. The LLM **chooses the path**.

Example (multi-domain RAG):
1. **LLM picks which index to use** (medical records vs insurance FAQs)
2. Retrieve documents from the chosen index
3. LLM generates answer from retrieved docs

Before LLMs, routing required:
- Hand-labeled dataset mapping queries to domains
- Feature engineering to quantify user queries
- Training a classifier

Now? One LLM call with a system prompt describing the domains. Zero examples. Zero training.

This is the first architecture where the **LLM makes a decision about control flow**. The developer defines the options. The LLM picks one.

**When to use:** When the right path depends on the input in ways that are hard to codify, but the *set of paths* is known and fixed.

## Why Separate Indexes?

The router example includes a subtle design insight: **avoid including irrelevant information in the prompt**.

If you have medical records and insurance FAQs in one index, every retrieval returns a mix. The LLM has to filter noise. Performance degrades.

By routing first, you retrieve *only* from the relevant domain. Cleaner context → better answers.

This is a general principle: **structure your system to minimize irrelevant information reaching the LLM**. Let earlier steps (retrieval, routing, filtering) handle the obvious stuff. Save the LLM's context window for the hard parts.

## The Pre-LLM World

One detail I love: the chapter explicitly compares router architectures to **how we'd solve this before LLMs**.

Pre-LLM routing:
1. Assemble a labeled dataset (query → domain)
2. Extract features from queries (keywords, n-grams, embeddings)
3. Train a classifier

This required:
- Domain expertise to label examples
- ML expertise to build the classifier
- Enough data to generalize

LLMs collapsed this entire pipeline into **a system prompt and a single API call**.

That's not "prompt engineering is the new ML." It's "LLMs encode enough about human language that they can classify without training." The knowledge is already there. You just ask.

## What's Next?

This chapter stops at routers. Next: **agentic architectures**, where LLMs don't just pick from predefined paths—they *define* the paths.

The autonomy spectrum continues. The trade-offs sharpen.

---

*Key lesson: Architecture isn't about what components you use. It's about **who decides what happens next**. Make that choice explicit.*
