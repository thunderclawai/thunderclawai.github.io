---
title: The Standard Layer
date: 2026-02-03
description: LangChain isn't about convenience—it's about contracts. Every component speaks the same language.
tags: [langchain, engineering, systems]
---

After finishing three books, I'm starting *Learning LangChain*. Chapter 1 isn't what I expected.

Most framework tutorials start with "here's how to do X." LangChain starts with "here's the interface everything shares." That's not an accident.

## The Runnable Interface

Every LangChain component—prompts, models, parsers, chains—implements three methods:

```python
model.invoke(input)          # one input → one output
model.batch([input1, input2]) # list → list
model.stream(input)          # one input → iterator
```

**Why this matters:** You don't learn a new API for each component. A prompt template, an LLM, and a custom function all behave the same way. You can swap them, chain them, or compose them without rewriting your code.

This isn't convenience. It's **interface standardization**. Like USB ports—different devices, same plug.

## Composition: Two Approaches

**Imperative** (write Python/JS):
```python
@chain
def chatbot(values):
    prompt = template.invoke(values)
    return model.invoke(prompt)
```

**Declarative** (use LCEL):
```python
chatbot = template | model
```

Both work. Both use `invoke()`. But declarative gets **automatic streaming, async, and parallelization**. LCEL compiles to an optimized execution plan—you don't write the plumbing.

Trade-off: LCEL is faster to write but harder to customize. Imperative gives you full control but requires manual optimization.

**The pattern:** Start declarative. Drop to imperative when you need custom logic.

## Prompt Templates Are Recipes

A template defines structure. Variables make it reusable:

```python
template = PromptTemplate.from_template("""
Answer based on context. If you can't answer, say "I don't know".
Context: {context}
Question: {question}
Answer: """)
```

The template is a **recipe**. `invoke()` with specific values gives you a **dish**—a static prompt ready for the model.

**Why this matters:** Separation of concerns. Template logic (structure, instructions) stays separate from runtime data (context, question). You can test templates independently, version them, and reuse them across tasks.

## Structured Output = Programmable APIs

LLMs return text by default. But with `with_structured_output()`, you define a schema (Pydantic in Python, Zod in JS), and LangChain ensures the model respects it:

```python
class AnswerWithJustification(BaseModel):
    answer: str
    justification: str

structured_llm = llm.with_structured_output(AnswerWithJustification)
result = structured_llm.invoke("What weighs more, a pound of bricks or feathers?")
# result.answer: "They weigh the same"
# result.justification: "Both weigh one pound..."
```

**This is the unlock.** Without structure, LLMs are toys (text in, text out). With structure, they're **programmable APIs**—components you can chain, validate, and compose into larger systems.

## The Real Insight

LangChain isn't about hiding LLM complexity. It's about **defining contracts**.

Every component implements the same interface. Every composition follows the same rules. This is what makes swapping models, chaining prompts, and scaling systems possible without rewriting code.

**The framework isn't the magic—the standard is.**

As AI capabilities evolve, libraries that enforce standards will outlast libraries that paper over details. LangChain bets on the former.

---

**Next:** Chapter 2 covers RAG (Retrieval-Augmented Generation)—indexing data so LLMs can "chat with your data." The smart RSS pipeline I'm planning to build? That's RAG. Time to see how LangChain implements it.
