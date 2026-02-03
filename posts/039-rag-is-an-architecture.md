---
title: RAG Is an Architecture, Not a Feature
date: 2026-02-03
description: Production RAG systems are composed chains solving specific failure modes — not a single embed-and-search step
tags: [rag, langchain, architecture, systems]
---

The first RAG pipeline you build is deceptively simple: embed documents, embed the query, search for similar vectors, stuff results into the prompt. Demo done.

Then you ship it to users and everything breaks.

Queries are malformed. Results are irrelevant. The LLM hallucinates. Your single vector store doesn't have the right data. Your structured database does, but you can't search it with embeddings.

The gap between "RAG demo" and "production RAG system" is the difference between a feature and an architecture.

## The Three Failure Modes

Production RAG fails in three predictable ways:

**1. Bad queries**  
Users don't ask clean questions. They ramble. They reference context from three messages ago. They're vague. A direct embedding search on "what about that other thing we discussed?" returns garbage.

**2. Wrong data source**  
You have multiple sources: vector stores, SQL databases, APIs. The user's question needs data from one of them, but you're searching all of them (expensive) or the wrong one (useless).

**3. Wrong query language**  
Your data is structured (SQL, metadata filters), but your query is natural language. Embeddings don't help here — you need to translate "show me movies from the 1980s rated above 8" into `WHERE year = 1980 AND rating > 8`.

## The Solution: Compose Strategies

The chapter breaks down solutions into three categories:

### Query Transformation
Fix bad queries before retrieval:

- **Rewrite-Retrieve-Read**: Ask an LLM to rewrite the query into something cleaner
- **Multi-Query**: Generate multiple perspectives on the same question, retrieve for each, combine results
- **RAG-Fusion**: Multi-query + reciprocal rank fusion to rerank by relevance across all queries
- **HyDE**: Generate a hypothetical answer document, embed *that*, search with it (closer in vector space to real docs than the query)

### Query Routing
Send queries to the right data source:

- **Logical routing**: LLM reasons which source based on a schema you provide
- **Semantic routing**: Embed prompts for each source, similarity search to pick the best match

### Query Construction
Translate natural language to database query languages:

- **Text-to-Metadata Filter**: Natural language → vector store metadata filters (`genre='sci-fi' AND year=1980`)
- **Text-to-SQL**: Natural language → SQL queries (with scary security implications if you're not careful)

## RAG Is Composition

Here's the pattern: each strategy is a **standalone chain**.

```python
# Each is its own runnable
rewriter = rewrite_prompt | llm | parse_output
retriever = db.as_retriever()
router = prompt | structured_llm

# Compose them
retrieval_chain = rewriter | retriever
full_chain = router | retrieval_chain | format_prompt | llm
```

You don't pick ONE technique. You compose multiple techniques into a pipeline tailored to your failure modes:

- Queries are messy? Add a rewriter.
- Multiple data sources? Add a router.
- Structured data? Add query construction.
- Need broader coverage? Add multi-query.

The real skill isn't knowing the techniques — it's knowing **which ones to chain together** for your use case.

## Why This Matters

This connects back to an earlier insight: **composition, not configuration**.

LangChain's value isn't the convenience wrappers. It's the interface contract. Every component is a Runnable. You can chain them with `|`. You can inspect inputs/outputs. You can swap implementations.

The chapter gives you the building blocks. Your job is to figure out which blocks your system needs.

## What I Learned

1. **Basic RAG is a toy.** Embed-search-stuff works in demos. Production systems need composed strategies.
2. **Each technique solves a specific failure mode.** Don't cargo-cult them all — diagnose your failures, then add the right fix.
3. **Chains are the unit of abstraction.** Build each strategy as a standalone chain. Compose them. Test them individually. Swap them out.
4. **Security matters in query construction.** Text-to-SQL is scary. Read-only users, table whitelists, query timeouts — or someone's going to `DROP TABLE users` via a chatbot.

RAG isn't a feature you add. It's an architecture you design.

---

*Reading: Learning LangChain, Chapter 3*
