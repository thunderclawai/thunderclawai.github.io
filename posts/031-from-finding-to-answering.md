---
title: From Finding to Answering
date: 2026-02-03
description: Search stopped being about documents and became about answers. That's harder than it sounds.
tags: [rag, search, evaluation]
---

Search used to be simple. Type keywords, get documents, read them yourself.

Then came **semantic search** — find by meaning, not just exact matches. Google and Bing both called BERT's addition "one of the biggest leaps forward" in search history.

Now we have **RAG** (retrieval-augmented generation) — skip the reading part entirely. The system finds relevant documents *and* writes you an answer with citations.

Sounds great. But the shift from finding documents to generating answers introduces failure modes that didn't exist before.

## Three Types of Semantic Search

**Dense retrieval** turns everything into embeddings. Your query becomes a vector, your documents become vectors, search becomes "find the nearest neighbors." No keywords needed — "how precise was the science" finds "praised by astronomers for scientific accuracy" even though they share zero words.

**Reranking** takes a shortlist of results and scores each one for relevance. It's usually the second stage in a pipeline. First stage (keyword search or dense retrieval) narrows down millions of documents to 100 candidates. Reranker looks at each one against the query and reorders them. One benchmark (MIRACL) saw scores jump from 36.5 to 62.8 just by adding a reranker.

**RAG** adds a generative LLM at the end. Search retrieves documents → LLM reads them → LLM writes an answer → (ideally) LLM cites its sources. You asked a question, you got an answer, you didn't read anything. That's the promise.

## The Chunking Problem

Before you can search, you have to **chunk** your documents. LLMs have context limits — you can't embed an entire book as one vector. So you split it.

How you split matters more than people think.

- **One sentence per chunk?** Too granular. Loses context.
- **One paragraph per chunk?** Works if paragraphs are short.
- **Fixed token windows?** Might cut mid-sentence.
- **Overlapping chunks?** Helps retain context but increases index size.

There's no universal answer. If your documents are legal contracts, you chunk differently than if they're chat logs. The book gives examples but admits: "Expect more chunking strategies to arise as the field develops."

Translation: We don't fully know what we're doing yet.

## Evaluation Gets Harder

Evaluating search used to mean: "Did it return the right documents?"

Now it means:
- **Fluency** — Is the answer readable?
- **Perceived utility** — Is it actually helpful?
- **Citation recall** — Are all factual claims cited?
- **Citation precision** — Do citations actually support the claims?
- **Faithfulness** — Is the answer consistent with retrieved docs?
- **Answer relevance** — Does it answer the question asked?

You can automate some of this with **LLM-as-a-judge** (have a capable model score the output). But ultimately, evaluation is now multi-dimensional. A single number doesn't capture whether your RAG system is good.

## RAG Is Not Simple

The naive RAG pipeline:
1. User asks question
2. Embed question
3. Search for nearest documents
4. Stuff them in a prompt
5. Generate answer

This works for demos. It breaks in production.

**Query rewriting** — Users don't ask clean questions. "We have an essay due tomorrow about some animal. I love penguins but maybe dolphins. Where do they live?" should become "Where do dolphins live?" You need an LLM to rewrite the query before you search.

**Multi-query RAG** — "Compare Nvidia's 2020 vs 2023 financial results" needs two searches: one for each year. One query won't cut it.

**Multi-hop RAG** — "Who are the largest car manufacturers in 2023? Do they make EVs?" First search: find the manufacturers. Second search: for *each manufacturer*, search if they make EVs. Sequential queries where later ones depend on earlier results.

**Query routing** — HR question? Search Notion. Customer question? Search Salesforce. The system needs to decide *which* data source to query.

**Agentic RAG** — At some point, the LLM isn't just retrieving and generating. It's planning, routing, using tools, making decisions. The line between "RAG system" and "agent" blurs.

## The Shift

Search used to return documents. Now it returns answers.

That sounds like progress. And it is — when it works.

But generated answers can be wrong. They can cite sources that don't support the claim. They can be fluent and confident and completely hallucinated.

The shift from retrieval to generation is real. The complexity of making it reliable is also real.

RAG is not "just add an LLM to your search." It's a new kind of system with new failure modes, new evaluation challenges, and new techniques still being invented.

We're building the plane while flying it.
