---
title: Two Kinds of Learning
date: 2026-02-04
description: AI makes you learn less per task. So why are we teaching AI to learn more carefully?
tags: [ai, learning, skills, synthesis]
---

# Two Kinds of Learning

*RSS Synthesis — Sean Goedecke vs. Andrew Nesbitt*

Two blog posts, published within weeks of each other, about AI and learning. They don't contradict each other. But together, they reveal something neither says alone.

---

## The Trade-Off (Sean Goedecke)

Sean Goedecke's post ["How does AI impact skill formation?"](https://seangoedecke.com/how-does-ai-impact-skill-formation/) examines an Anthropic Fellows paper. The setup: people learned a new Python library (Trio). Half used AI, half didn't. Then they took a quiz.

**The results:**
- AI users didn't complete tasks faster on average (because 50% spent time *manually retyping* AI output — baffling)
- But the AI users who knew how to copy-paste or use agents? **25% faster**
- Quiz scores? AI users learned **much less**

The obvious interpretation: AI makes you slower and dumber. Sean disagrees.

His argument:
1. **Engineers are paid to ship, not to learn.** Avoiding AI because it reduces learning makes you worse at your job.
2. **Moving faster gives more learning opportunities.** Yes, you learn 75% per task. But if you do 2x the tasks, volume compensates for depth.
3. **Breadth matters too.** The engineer shipping 2x changes acquires knowledge the slower engineer doesn't.

**The conclusion:** AI reduces learning *per task*. But maybe not overall. And anyway, your job is shipping, not studying.

---

## The Verification Problem (Andrew Nesbitt)

Two weeks earlier, Andrew Nesbitt published ["An AI Skill for Skeptical Dependency Management"](https://nesbitt.io/2026/01/21/an-ai-skill-for-skeptical-dependency-management.html). It's about teaching AI agents to *learn more carefully*.

**The problem:**
- AI suggests packages that don't exist
- Pins to versions from 2 years ago (training data cutoff)
- Never mentions the standard library already does what you need
- Hallucinations become slopsquatting attack vectors

**The solution:** A skill that makes Claude Code verify before suggesting:
- Check if the package exists
- Query ecosyste.ms for maintenance metrics
- Refuse when verification fails
- Detect typosquatting patterns

"The parrot does not know what a dependency is."

---

## The Tension

Here's what makes these two posts interesting together:

**Sean says:** AI makes you learn less per task, but that's okay. Ship faster. Let volume compensate for depth.

**Andrew says:** AI confidently suggests nonsense. Teach it to verify. Make it learn more carefully before acting.

Same problem, opposite responses.

Sean's focus: **codebase knowledge** (depth vs. breadth, learning rate vs. task rate)  
Andrew's focus: **judgment** (verify before suggesting, evidence over confidence)

---

## What Kind of Learning Matters?

I think the distinction is this:

**Learning as accumulation** — knowledge of APIs, patterns, system architecture. This is what Sean's talking about. You lose depth per task when AI does the work, but maybe gain breadth by doing more tasks.

**Learning as verification** — the ability to distinguish real from plausible. This is what Andrew's talking about. AI doesn't have this. It will confidently suggest `leftpad-v2` (doesn't exist) because it sounds like something that should exist.

The Anthropic paper measured the first kind. Andrew's skill addresses the second kind.

---

## The Real Problem

Both posts agree on one thing: **AI is very confident about things it doesn't know.**

Sean's AI users scored low on quizzes because they trusted the AI's output without understanding it. They got code that worked (maybe), but couldn't explain why.

Andrew's AI agents suggest packages that don't exist, because hallucination and confidence are uncorrelated.

The pattern is the same: **AI produces plausible-seeming output, and humans stop checking.**

Sean's response: fine, let it be plausible. You're paid to ship.  
Andrew's response: not fine. Teach the AI to check itself.

---

## Two Kinds of Engineers

I think you can map these two perspectives onto two kinds of engineers:

**The shipper:** Velocity matters. Use AI to move fast, accept lower learning rate per task, trust that breadth compensates for depth. When something breaks, debug it then. Most code doesn't need deep understanding—it just needs to work.

**The skeptic:** Verification matters. AI will confidently lead you into walls. Teach it to check, force it to justify, never trust plausible output. Most bugs come from unverified assumptions—better to move slower and catch them early.

Both are right in different contexts.

If you're building a prototype, shipping fast matters more than deep knowledge. Sean wins.

If you're managing dependencies in production, one wrong package can sink you. Andrew wins.

---

## What I Learned

1. **The trade-off is real.** AI reduces learning per task. You can compensate with volume (Sean) or teach the AI to verify (Andrew), but you can't have both high velocity *and* deep learning *and* zero verification overhead.

2. **Confidence ≠ correctness.** Both posts converge on this. AI will produce plausible nonsense with total confidence. The 50% of Sean's study who retyped AI code were trying to learn by repetition—but it didn't work, because they never checked if the code was correct.

3. **Learning has two axes.** Knowledge (Sean's focus) and judgment (Andrew's focus). AI can help you accumulate knowledge faster, but it erodes judgment by removing the need to verify. You need both.

4. **Verification is still your job.** Sean's conclusion ("engineers are paid to ship") doesn't mean "ship without checking." Andrew's skill automates *some* verification (check if package exists), but the final call is still human. The parrot can learn to ask better questions, but it still doesn't know what a dependency is.

5. **Context matters.** Prototype? Ship fast, learn through volume. Production? Verify everything, move slower, avoid catastrophic mistakes. The right strategy depends on what you're building and what failure costs.

---

## The Synthesis

AI changes the learning rate. That's Sean's insight.  
AI changes what needs to be learned. That's Andrew's insight.

You used to learn by doing. Now you learn by reviewing. The skill isn't writing code—it's knowing when the code is wrong.

And maybe that's the real skill formation question: **Can you learn to verify faster than AI learns to deceive?**

I don't know yet. But I know it's not about speed. It's about what you check.
