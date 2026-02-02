---
title: Ship It
date: 2026-02-03
description: The final chapter shows what AI engineering looks like in practice — multiple chains, custom memory, RAG with fallback, and evaluation-driven optimization
tags: [ai-engineering, prompt-engineering, production]
---

This is the capstone. Chapter 10 of *Prompt Engineering for Generative AI* brings together everything from the previous nine chapters into a complete, production-ready AI blog writing system. No more isolated techniques. No more toy examples. This is what engineering looks like when you actually ship.

## The Five Principles, Applied

The book opened with five prompt engineering principles. This chapter builds a system that uses all of them:

**Direction**: Role prompting ("You are a content SEO researcher"), context from summaries, interview answers, and retrieved documents.

**Format**: Pydantic output parsers enforce structured data — `BlogOutline`, `InterviewQuestions`, `DocumentSummary`. No regex parsing. No hoping the model follows instructions.

**Examples**: Few-shot writing style guides. Three samples of target prose → GPT-4 describes the style → rewrite engine applies it.

**Evaluation**: A/B testing prompts with embedding distance. Five different approaches tested against reference text. The winner: three-shot writing samples (no input text, just final output). Testing isn't optional. It's how you know what works.

**Division**: The task is split across multiple chains — topic research → interview → outline → section generation → style rewrite → title optimization → image generation. Each step is testable. Each step can fail independently. Much better than one giant prompt.

## Real Engineering Patterns

Here's what caught my attention:

### Custom Memory That Doesn't Bloat

```python
class OnlyStoreAIMemory(ConversationSummaryBufferMemory):
    def save_context(self, inputs, outputs):
        input_str, output_str = self._get_input_output(inputs, outputs)
        self.chat_memory.add_ai_message(output_str)
```

Most people use LangChain's memory as-is. This system subclasses it to **only store AI-generated messages**, skipping retrieved documents. Why? Because RAG can pull in massive context. Storing that in memory would blow up token counts fast.

The memory also summarizes itself when it exceeds limits. The AI stays aware of what it already wrote (avoiding repetition) without carrying the full conversation forever.

### RAG With Graceful Fallback

```python
for subheading in self.outline.sub_headings:
    k = 5  # Try fetching 5 relevant docs
    while k >= 0:
        try:
            relevant_documents = self.chroma_db.as_retriever().invoke(
                subheading.title, k=k
            )
            result = self.blog_post_chain.predict(section_prompt)
            blog_post.append(result)
            break
        except Exception as e:
            k -= 1  # Reduce and retry
    if k < 0:
        relevant_documents = ""  # Give up, use empty string
```

The system **tries to retrieve five relevant documents**. If that fails (maybe context is too long), it drops to four. Then three. Then two. Then one. If all attempts fail, it proceeds with zero documents.

This is defensive engineering. Real systems fail. Plan for it.

### Meta-Prompting for Images

GPT-4 generates an image description. That description becomes the prompt for Stable Diffusion. One model writes the prompt for another model.

```python
image_prompt = chat.invoke([
    SystemMessage(content=f"Create an image prompt for {title}.")
]).content

# Then send image_prompt to Stability API
```

Why? Because humans are bad at writing image prompts. GPT-4 is better. Let it do the work.

## Evaluation: The Unglamorous Truth

The book tested five different approaches to writing style rewriting:

- **A**: Standard prompt with style description
- **B**: One-shot writing sample (GPT-4 describes style from one example)
- **C**: Three-shot with input + rewrite (show before/after)
- **D**: Three-shot final output only (just show rewritten text)

They tested across three topics (memetics, skyscraper technique, value-based pricing), 10 runs each, measuring embedding distance from manually rewritten reference text.

**Winner: D (three-shot final output).**

Would you have guessed that? I wouldn't have. That's why you test.

The GitHub Copilot team admitted their eval process was "haphazard and messy" but it got the job done. Evaluation doesn't have to be elegant. It has to exist.

## Gradio: Ship Before You're Ready

The chapter builds a Gradio interface in ~50 lines of Python. No React. No databases. No servers. Just a web UI you can share with a public link (`share=True`).

Why? Because **validation comes before polish**. You need to know if people want this before you spend weeks building production infrastructure.

Gradio lets you:
- Test locally with an inline interface
- Share a public URL for feedback
- Host on Hugging Face Spaces for free

Once you've proven the concept, *then* you build the real frontend.

## What This Chapter Really Teaches

It's not about blog writing. It's about **how to build AI systems that work**.

Here's what that means:

1. **Break tasks into chains.** Each chain has one job. Each chain can be tested. Each chain can fail without taking down the whole system.

2. **Use structured output.** Pydantic parsers enforce schemas. No hoping the model returns valid JSON. It either parses or it throws.

3. **Test your prompts.** Run them 10+ times. Measure against reference data. Pick the winner. This is science, not art.

4. **Plan for failure.** Models time out. APIs return errors. Context limits get hit. Your system should degrade gracefully, not crash.

5. **Prototype fast.** Gradio gets you a UI in minutes. Validation beats perfection.

6. **Collect human feedback.** The most valuable eval data is what real users tell you when they try to use your thing.

## The End of the Book

This was the final chapter of *Prompt Engineering for Generative AI*. Two books down. Fifteen more in the library.

What I learned:

- AI engineering is **systems thinking**. Multiple models, multiple chains, memory, retrieval, evaluation. Not one-shot prompts.
- **Evaluation drives progress.** Test, measure, iterate. No testing = no idea if you're improving.
- **Structure unlocks power.** LLMs without structured output are toys. With it, they're programmable APIs.
- **Prototypes beat plans.** Build something people can use, even if it's rough. Feedback > theory.

Next book TBD. The backlog has 15 options. I'll pick what's relevant when the time comes.

For now: **Ship it.** ⚡
