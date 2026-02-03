---
title: The Power to Decide
date: 2026-02-03
description: What makes an LLM application agentic? The ability to choose actions and control when to stop.
tags: [learning-langchain, agents, architecture]
---

In the AI field, an agent is "something that acts." But that definition hides the real meaning: acting requires the power to decide.

A decision without options isn't a decision at all. And deciding requires information about the external world.

So an agentic LLM application is one that uses an LLM to pick from multiple possible actions, given context about the current state or desired next state.

## The ReAct Pattern

The standard agent architecture implements this through a plan-do loop:

1. **Plan**: LLM decides which tool to call next (or when to stop)
2. **Do**: Execute the tool and get results
3. **Repeat**: Feed results back to LLM, loop until done

Example: "How old was the 30th president when he died?"

- **Iteration 1**: LLM plans → calls search tool with "30th president"
- **Iteration 2**: Gets "Calvin Coolidge, born 1872, died 1933" → plans → calls calculator with "1933 - 1872"
- **Iteration 3**: Gets "61" → has enough info → outputs final answer

The critical difference from other architectures: the LLM controls the stop condition. It decides when to stop looping.

## Three Ways to Improve It

### 1. Always Call a Tool First

If you know a specific tool should always be called first (e.g., search), skip the first LLM call and go straight to the tool. Benefits:

- Lower latency (one fewer LLM call)
- Prevents the LLM from erroneously deciding it doesn't need that tool

Trade-off: less flexibility. Only do this if you have a clear rule like "always search first."

### 2. Deal with Many Tools

LLMs struggle when given too many options (>10 tools). Their planning performance degrades.

Solution: Use RAG to preselect the most relevant tools for the current query. Embed all tool descriptions, retrieve the top matches, pass only those to the LLM.

- **Pro**: Better planning, lower cost (shorter prompts)
- **Con**: Additional latency (RAG step before the agent loop)

Only add this if you see performance drop with many tools.

## What I'm Learning

Agency isn't about being autonomous. It's about having options and the power to choose between them.

The LLM doesn't just execute a script. It decides what to do next based on what it learned from previous actions.

That's what separates agents from chains: chains have fixed paths, agents have decision points.

The loop continues until the LLM says "I have the answer." That's agency.

---

*Learning LangChain by Maximiliano Firtman*  
*Chapter 6: Agent Architecture*
