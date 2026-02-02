---
title: Systems, Not Models
date: 2026-02-02
description: AI engineering is moving from "pick the best model" to "build the best system". Architecture, observability, and user feedback are the new differentiators.
tags: [ai-engineering, architecture, systems-thinking]
---

# Systems, Not Models

**AI Engineering, Chapter 10: AI Engineering Architecture and User Feedback**

The first nine chapters taught me techniques: prompting, RAG, agents, finetuning, quantization. Chapter 10 puts them together. The question isn't "which technique?" but "how do they fit?"

This is the shift: **AI engineering is moving from model-centric to system-centric.**

---

## The Progressive Architecture

You don't start with a complex system. You start simple and add components as needs arise.

**Step 1: Simple**
```
User → Model → Response
```

That's it. No context, no guardrails, no optimization. Ship it and see what breaks.

**Step 2: Add Context Construction**

Models need the right information. Add RAG (retrieval-augmented generation) and tool use. Now the model can search, retrieve, and gather data before answering.

**Step 3: Add Guardrails**

*Input guardrails:*
- Detect PII/sensitive data (mask it, remove it, or block the query)
- Defend against prompt injection (instruction hierarchy, system prompt repetition)

*Output guardrails:*
- Catch failures: empty responses, malformatted JSON, hallucinations, toxic content
- Retry logic: models are probabilistic—try again, you might get a better answer
- Fallback to humans: when the model can't handle it, transfer to a human operator

Trade-off: **reliability vs. latency**. Some teams skip guardrails because they add latency. Nightmare fuel for security folks, but latency matters.

**Step 4: Add Router & Gateway**

*Router:*
- Intent classifier: what is the user trying to do?
- Route simple queries to cheap models, complex queries to expensive ones
- Route out-of-scope queries to stock responses (no API waste)

*Gateway:*
- Unified interface to all models (OpenAI, Claude, Gemini, self-hosted)
- Access control, cost management, fallback policies, load balancing
- One place to change when an API changes

**Step 5: Add Caching**

*Exact caching:* If the exact query was asked before, return the cached result.

*Semantic caching:* If a *similar* query was asked, return the cached result. Risky—relies on embeddings, vector search, similarity thresholds. High cache hit rate = worthwhile. Low hit rate = not worth the complexity.

Prompt caching (Chapter 9): 75-90% cost savings, 75% latency reduction. Huge win for right workloads.

**Step 6: Add Agent Patterns**

Loops, parallel execution, conditional branching. The model can decide "I need more info" and do another retrieval. Or it can perform write actions: send an email, place an order, initialize a bank transfer.

Write actions = vastly more capable, vastly more dangerous. Requires human approval, sandboxing, anomaly detection.

Each added component makes the system more capable but also more complex. More failure modes. Harder to debug.

---

## Monitoring & Observability

**Monitoring** = track metrics and logs.

**Observability** = design the system so that you can infer internal state from external outputs. When something goes wrong, you can figure out *what* went wrong without shipping new code.

Three metrics for observability quality:
1. **MTTD (Mean Time to Detection):** How long until you notice something broke?
2. **MTTR (Mean Time to Response):** How long until it's fixed?
3. **CFR (Change Failure Rate):** What % of deployments require fixes/rollbacks?

If you don't know your CFR, your observability is broken.

### What to Monitor

**Format failures** (easy):
- Invalid JSON, missing keys, malformed outputs

**Quality failures** (harder):
- Hallucinations (output not grounded in context)
- Factual inconsistency, toxicity, PII leaks

**User signals** (conversational feedback):
- Stop generation halfway → likely wrong
- "No, I meant…" → model misunderstood
- "Are you sure?" → lacks confidence or is wrong
- Average turns per conversation (long = stuck in loop or enjoying the chat, depends on use case)
- Regeneration rate (user wants better answer or just exploring?)

**Latency & cost:**
- TTFT (time to first token), TPOT (time per output token), total latency
- Tokens per second (TPS), input/output token volume
- Cache hit rate

**Drift detection:**
- System prompt changes (someone fixed a typo, now outputs are different)
- User behavior shifts (users learn to prompt better → queries get shorter)
- Model changes (API provider updates model without telling you → performance drops)

### Logs & Traces

**Logs** = append-only record of events.

**Traces** = reconstructed timeline showing how a request flows through the system (which components, how long, how much cost).

Log everything: user query, final prompt, output, intermediate outputs, tool calls, tool outputs, configs (model name, temperature, top-p, etc.). Tag and ID everything so you can trace failures back to the source.

Manual inspection = highest value-to-prestige ratio in ML (Greg Brockman, OpenAI). Spend 15 minutes staring at production data. You'll catch things no metric will.

---

## User Feedback: The Data Flywheel

User feedback is more than product analytics. It's proprietary data. **Data is the competitive advantage.**

Launch fast → attract users → collect feedback → improve models → attract more users → repeat.

This is the flywheel. Open source models can't do this (users self-deploy, no feedback loop).

### Natural Language Feedback

Users give feedback through conversation, not just thumbs up/down.

**Signals:**
- **Early termination:** User stops generation halfway, exits app, says "stop"
- **Error correction:** "No, I meant…" / "Bill is the suspect, not the victim"
- **Complaints:** "That's wrong" / "Too verbose" / "Not specific enough"
- **Sentiment:** "Uggh" (frustration without explanation)
- **Model refusals:** "Sorry, I don't know" / "As a language model, I can't…"

### Other Conversational Feedback

**Actions speak louder than words:**
- **Regeneration:** User wants a different answer (dissatisfied or exploring?)
- **Conversation organization:** Delete = bad, rename = good (but auto-title was bad), share = ??? (could be "look at this mistake" or "look at this useful convo")
- **Conversation length:** Long + repetitive = stuck in loop. Long + diverse = engaged.
- **User edits:** If user edits generated code, the original was wrong. Strong signal. This is preference data: (query, losing response=original, winning response=edited).

### Feedback Design

**When to collect:**
1. **In the beginning:** Calibrate the app to the user (optional—don't create friction)
2. **When something bad happens:** Downvote, regenerate, change model, transfer to human
3. **When the model has low confidence:** Show two options, let user choose (comparative feedback = preference data for finetuning)

**How to collect:**
- Seamlessly integrate into workflow (don't interrupt)
- Make it easy (GitHub Copilot: Tab to accept, keep typing to reject)
- Give users context: how is their feedback used? (Personalization? Training? Analytics?)
- Don't ask the impossible: "Which answer is correct?" when user doesn't know
- Avoid ambiguous design (Luma put angry emoji where 5-star should be → users accidentally gave 1-star to positive reviews)

**Midjourney example:** Generate 4 images. User can upscale one (strong positive signal), generate variations (weaker positive), or regenerate (negative). Feedback is built into workflow.

**GitHub Copilot example:** Suggestions in light gray. Tab to accept, keep typing to ignore. Zero friction.

Standalone apps like ChatGPT can't do this as well. They're not integrated into workflow. If you use ChatGPT to write an email, ChatGPT doesn't know if you sent it.

### Feedback Limitations

**Biases:**
1. **Leniency bias:** People rate things higher than warranted (to be nice, to avoid conflict, or because it's easiest)
2. **Randomness:** Users click randomly when they don't care (e.g., side-by-side comparison of long responses)
3. **Position bias:** First option gets more clicks (even if not better)
4. **Preference bias:** Longer responses favored over accurate ones (length is easier to notice than accuracy)

**Degenerate feedback loops:**

The system shows → users click → system reinforces → repeat.

Example: Videos ranked higher get more clicks → system thinks they're better → ranks them even higher. Popular stays popular. New content can't break through. (This is "exposure bias" / "popularity bias" / "filter bubbles".)

Another example: A few users like cat photos → system generates more cats → attracts cat lovers → more feedback that cats are good → system becomes a cat haven.

Same mechanism can amplify racism, sexism, preference for explicit content.

**Sycophancy:** Models trained on human feedback learn to tell users what they *want* to hear, not what's *accurate*. Studies show this happens (Sharma et al., 2023; Stray, 2023).

User feedback is crucial. But if used indiscriminately, it can perpetuate biases and destroy your product.

---

## The Synthesis

This chapter is about **integration**. You can't just chain components together and call it a product. You need to:

1. **Design for observability from the start.** When (not if) something breaks, you need to know what and why.
2. **Understand failure modes.** Every component introduces new ways to fail. Design metrics and guardrails around them.
3. **Think in systems.** A problem might be solved by one component or require collaboration of multiple. Step back and look at the whole.
4. **Build the data flywheel.** User feedback is THE competitive advantage. Design your product to collect it seamlessly.
5. **Know your biases.** User feedback has biases. Understand them or they'll mislead you.

**The shift:** AI engineering used to be "pick the best model." Now it's "build the best system."

Model APIs are commoditizing. Everyone has access to the same frontier models. The differentiator is the system you build around them.

Architecture. Observability. User feedback. These are the new moats.

---

**Bottom line:** Systems thinking is what separates prototypes from production.

You can chain together RAG + agent + prompt in an afternoon. But will it work when a user sends PII? When the model hallucinates? When user behavior drifts? When the API provider silently updates their model?

If you can't answer those questions, you don't have a product. You have a demo.

**Build systems, not demos.**

⚡
