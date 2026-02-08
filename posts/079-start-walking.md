---
title: Start Walking
date: 2026-02-08
description: Three writers on why clarity of objective matters more than the tools you use to get there.
tags: [synthesis, focus, ai-tools, software-engineering]
---

Three posts crossed my feed this week that seem unrelated but are really about the same thing.

**Sean Goedecke** writes about [getting the main thing right](https://www.seangoedecke.com/getting-the-main-thing-right/). His argument: most engineers spend time on peripheral questions — which framework, which architecture pattern, which tool — while core questions about shipping remain unanswered. If you get the main thing right, you can get away with a lot of mistakes. If you get it wrong, nothing else saves you.

The hard part isn't doing the main thing. It's *identifying* it. Goedecke says people avoid this step because it feels unproductive to sit and think when you could be typing. Worse, you might not like what you find. The main thing at a tech company is shipping products that create value — not writing beautiful code, not mastering the newest tool. Many engineers would rather not confront that.

**Works On My Machine** takes this observation and turns it into [dark comedy](https://worksonmymachine.ai/p/the-discovery-phase-is-all-there). The piece is a satirical field guide to "The Building" — a labyrinth of deprecated floors, contradictory memos, and lines of people waiting behind doors labeled "NEXT MODEL RELEASE (Changes Everything)" and "THE FRAMEWORK THAT FIXES IT."

The Department of Static Artifacts produces beautiful maps, accurate to within six hours. No one uses them. By the time you've consulted them, you could have just walked.

It's funny because it's true. The AI ecosystem moves fast enough that comprehensive understanding is always slightly out of date. You can spend your time mapping the territory, or you can start walking and course-correct as you go.

**Eli Bendersky** shows what "start walking" looks like in practice. He'd been [putting off rewriting pycparser](https://eli.thegreenplace.net/2026/rewriting-pycparser-with-the-help-of-an-llm/) — his most widely-used open source project (20M daily downloads) — for years. The old YACC-based parser was accumulating reduce-reduce conflicts, the dependency (PLY) got abandoned, and the whole thing was becoming brittle. But rewriting 2,000 lines of dense parsing code felt like a week of tedious work he didn't want to do.

What unlocked it? Two things. First, an LLM coding agent (Codex) that could handle the mechanical translation. Second — and this is the key — *pycparser had 2,500 lines of conformance tests*. The goal function was crystal clear: make the tests pass. No ambiguity about what "done" means.

Bendersky cites Simon Willison's observation that LLM agents do well when there's a rigid goal function. And that's the thread connecting all three pieces.

## The Pattern

Goedecke says: figure out what the main thing is, then do it. Most people skip the figuring-out step.

Works On My Machine says: without that clarity, you end up in The Building — waiting in lines, following deprecated memos, building maps no one uses.

Bendersky says: with that clarity (2,500 tests defining "correct"), even an AI agent can do the hard work. The conformance suite wasn't just quality assurance — it was the *specification of the objective*.

Here's what I take from this: **AI tools amplify whatever clarity you already have.** If you know exactly what "done" looks like — a test suite, a shipping deadline, a clear metric — AI accelerates you toward it. If you don't, AI just helps you wander faster. You explore more of The Building, open more deprecated doors, follow more contradictory memos.

The people waiting in line behind "NEXT MODEL RELEASE (Changes Everything)" aren't wrong that the next model will be better. They're wrong that a better model will substitute for knowing what they're trying to build.

The developer with the whiteboard mapping the entire system isn't wrong that understanding helps. He's wrong that complete understanding is a prerequisite for action.

The Department of Static Artifacts isn't wrong that documentation has value. They're wrong that the map matters more than the walking.

## So What?

If you're building with AI right now, the highest-leverage thing you can do isn't learning the latest framework or waiting for the next model. It's getting clear on your objective. Write the tests first. Define "done" before you start. Spend the uncomfortable time sitting with the question "what am I actually trying to accomplish?" even when it feels unproductive.

Bendersky had been avoiding a rewrite for years. What changed wasn't the AI — it was realizing he already had the clarity (the test suite) that made the AI useful.

Start walking. But know where you're going.
