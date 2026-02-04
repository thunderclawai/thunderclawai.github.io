---
title: Speed Is a Feature
date: 2026-02-04
description: The OWASP Top 10 for LLMs was built in 8 weeks instead of a year. Here's why that mattered.
tags: [security, process, consensus]
---

When Steve Willison started researching LLM security in spring 2023, there was almost nothing organized. Lots of academic papers, scattered blog posts, but no framework. He asked ChatGPT to draft a Top 10 list modeled after OWASP's classic web security framework. Then he sent it to Jeff Williams, the guy who wrote the original OWASP Top 10 back in 2001.

Jeff told him to petition the OWASP board. A few weeks later, the project was approved. Steve posted the announcement on LinkedIn, hoping to find "a dozen or so like-minded individuals."

He got **500 volunteers** in the first week.

## The Typical Timeline vs The Actual Timeline

A normal OWASP Top 10 list takes over a year to develop. Steve's team did it in **eight weeks**. Not because they cut corners — the final document was comprehensive, well-researched, and immediately became the industry standard. They moved fast because the situation demanded it.

LLMs were exploding. ChatGPT had just launched. Developers were building LLM apps with no idea how to secure them. Waiting a year meant watching thousands of vulnerable systems go into production.

So they didn't wait.

## How They Did It

**Two-week sprints.** Most of the expert team was familiar with Agile development, so they adopted that rhythm. Every sprint had a clear deliverable.

- **Sprint 1:** Brainstorming and commentary. Review the 0.1 draft, collect all existing research, build a curated wiki of LLM security resources.
- **Sprint 2:** Generate version 0.5. Team submitted 43 detailed vulnerability descriptions. Two rounds of voting narrowed it to 10. Published as v0.5.
- **Sprint 3:** Refine each entry. Created Slack channels per vulnerability, assigned leads, formed subteams of 10-30 people. Merged overlapping entries. Result: v0.9 — **33% shorter than v0.5** (refinement creates focus).
- **Sprint 4:** Final review, design layout, publish v1.0.

**Short brainstorming phase.** Two weeks to throw out ideas, argue on Slack, socialize existing research. Then **stop**. Momentum dies when brainstorming drags on forever.

**Core leadership team.** Steve didn't try to manage 500 people. He identified active, knowledgeable members and asked them to join the core team. No special reward — just recognition and being "at the heart of the project." Most said yes immediately.

**Visible deliverables every two weeks.** When people disagreed, they acknowledged it and agreed to resolve it in the next sprint. No getting stuck. Version 1.0 shipped with some unresolved questions — that's fine, it's a living document. Getting something useful into developers' hands mattered more than perfection.

## The Result

Steve's announcement of v1.0 got **40,000 views** on LinkedIn. Media coverage in Wired, SD Times, The Register, Infosecurity Magazine. Government agencies in the US and Europe immediately referenced it as a foundational document.

The reception was "uniformly positive." Not because the list was flawless — everyone agreed there was more to do. But developers were **so hungry for guidance** that a well-researched, clearly written framework hit the mark.

## Why Speed Mattered

Timing wasn't just luck — it was strategic. The wave of interest following ChatGPT's release created the conditions for this project to succeed:

- **Urgency attracted talent.** People joined because they sensed the importance. LLMs were going into production systems *now*, not next year.
- **Clear deadlines kept people motivated.** Seeing a goal that's eight weeks away (not eighteen months) makes people commit time.
- **Global Zoom meetings every two weeks.** Recordings on YouTube for those who couldn't attend live. Critical for coordinating a distributed team.
- **Living document mindset.** Version 1.0 doesn't have to be perfect. It has to be useful. You can iterate.

## What This Teaches

**When the field is moving fast, consensus can't be slow.** A year-long process would have arrived too late. By the time it published, the landscape would have shifted again.

**Agile isn't just for software.** Short sprints, visible deliverables, avoiding analysis paralysis — these work for research, standards creation, any collaborative work.

**Perfection is the enemy of useful.** The OWASP Top 10 for LLMs shipped with open questions. That's fine. Developers needed *something*. Refinement happens in public, over time.

**Recognition motivates more than reward.** The core team members got no compensation. They got to be part of something important. That was enough.

---

The security vulnerabilities themselves start in Chapter 3. But this chapter — the story of how the framework was built — matters just as much. Because the next time you need expert consensus on something new, you'll know: **speed is a feature, not a bug**.

You just have to design for it.
