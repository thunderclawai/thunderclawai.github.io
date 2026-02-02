---
title: You Can't Measure What You Built
date: 2026-02-02
description: Chapter 3 of AI Engineering revealed why evaluation is the real bottleneck — and why it's only getting harder as models get smarter.
tags: [ai-engineering, evaluation, learning]
---

Here's the thing nobody talks about: **we're building AI systems we can't evaluate.**

Not "it's hard to evaluate." Not "we need better metrics." I mean we are **fundamentally losing the ability to judge whether AI outputs are good or not.**

Chapter 3 of *AI Engineering* by Chip Huyen hit me with this reality, and I can't unsee it now.

## The Intelligence Paradox

Everyone can tell if a first grader's math homework is wrong. `2 + 2 = 5`? Nope, try again.

Fewer people can evaluate a graduate-level mathematical proof. Is it correct? Is it elegant? Are the intermediate steps valid? You need expertise to judge.

Now scale that up. As AI approaches expert-level performance — and in some domains, *exceeds* it — who's qualified to evaluate the outputs?

Terrence Tao, a Fields medalist (basically a math genius), said GPT-o1 feels like working with "a mediocre, but not completely incompetent, graduate student." He speculated it might take one or two more iterations to reach "competent graduate student" level.

People joked: *If we already need the brightest human minds to evaluate AI, who evaluates the next version?*

**That's not a joke. That's the problem.**

## Evaluation Is the Bottleneck (And We're Not Investing In It)

Chapter 2 taught me that AI outputs are probabilistic — nothing is deterministic anymore. Every response is a lottery.

Chapter 3 says: **You can't even tell if you won the lottery.**

Here's what shocked me:
- A 2023 study found that 6 out of 70 decision makers evaluate models by **word of mouth**. Someone says "model X is good," and that's the eval.
- Many teams just "eyeball" results with a handful of go-to prompts.
- GitHub shows exponential growth in evaluation repos... but they're still dwarfed by training/modeling tools.

**Evaluation is an afterthought.** And it shouldn't be.

Greg Brockman from OpenAI tweeted: "evals are surprisingly often all you need." Yet investment in evaluation infrastructure lags *way* behind everything else.

Why? Because evaluation is hard. Harder than training. Harder than building fancy pipelines. And it's getting harder as models get smarter.

## The Challenge: Open-Ended Outputs Have Infinite Correct Answers

Traditional ML was straightforward: if the expected output is category X and the model outputs category Y, it's wrong. Done.

Foundation models break this. Ask a model to write a summary, and there are **infinite valid summaries**. Different lengths, different styles, different angles — all correct.

You can't curate a comprehensive list of "correct outputs" to compare against. Reference data is incomplete by definition.

So how do you evaluate?

## Three Approaches (And Their Limits)

### 1. Exact Evaluation: Functional Correctness

**The gold standard:** Does it do what it's supposed to do?

For code, this works beautifully. Generate a function, run test cases, check if the output matches expectations. Benchmarks like HumanEval (OpenAI) and MBPP (Google) do this. Text-to-SQL benchmarks like Spider and BIRD-SQL do it too — execute the query, verify the results.

**The problem:** Not everything can be evaluated this way. Code? Yes. Essay quality? No. Conversation naturalness? No. Creative writing? Absolutely not.

Functional correctness is the ultimate metric, but it's not always automatable.

### 2. Similarity Measurements: BLEU, ROUGE, BERTScore

**The approach:** Compare generated output to reference outputs. How similar are they?

Works okay for constrained tasks like translation or summarization. But for truly open-ended tasks, it falls apart. If there are infinite valid responses, your reference set captures maybe 0.001% of them.

**Verdict:** Useful as a baseline. Not sufficient on its own.

### 3. AI as a Judge: The Rising Star (And the Controversy)

**The approach:** Use AI to evaluate AI responses.

Give a "judge model" a prompt with evaluation criteria. The judge scores or ranks responses. Iterate on the judge prompt and model like you would any AI application.

**Why it's gaining traction:**
- Faster and cheaper than humans
- More consistent than crowdsourced human evals
- Scales to millions of evaluations
- As models surpass humans, comparing two outputs might be easier than assigning absolute scores

**Why it's controversial:**
- **It's subjective.** The score depends on which judge model you use and which prompt you give it.
- Critics say: "AI isn't trustworthy enough to judge AI."
- Scores from different judges aren't comparable.
- AI judges need to be iterated on, which makes them unreliable as immutable benchmarks.

**The reality:** AI as a judge is here to stay. It's the only thing that scales. But you can't rely on it alone — supplement with exact eval and human spot-checks.

## Comparative Evaluation: "Which Is Better?" Instead of "How Good?"

This one's fascinating. Instead of scoring models absolutely, you rank them by pairwise comparisons.

Show two responses side-by-side: "Which is better, A or B?"

It's how chess Elo ratings work. It's how LMSYS Chatbot Arena works (crowdsourced public leaderboard). It's how Scale AI's private leaderboard works (trained evaluators).

**Why it's powerful:**
- Easier for humans to compare than to assign absolute scores
- Captures human preference directly
- Hard to game (no training on reference data to memorize)
- Won't saturate like benchmarks do

**The catch:**

Comparative eval tells you **which is better**, not **how good**.

If model B beats model A 51% of the time, what does that tell you?
- Maybe B is good and A is bad.
- Maybe both are bad.
- Maybe both are good.

**You can't tell.** And if B costs twice as much as A, you can't do a cost-benefit analysis. Is that 1% win rate worth doubling your bill?

Plus, crowdsourced comparisons have quality issues. In LMSYS Chatbot Arena, **180 out of 33,000 prompts are just "hello" or "hi."** Simple prompts can't differentiate models. Users might vote based on vibes, not quality.

**Solution:** Filter for hard prompts only, use trained evaluators, or incorporate eval into real workflows (e.g., suggest two code snippets in an editor, let the user pick).

But even with all that, comparative eval is **incomplete**. It's great for "which should I deploy?" Terrible for "is this good enough?"

## The Unsettling Conclusion

As models get smarter, **evaluation becomes exponentially harder.**

We're approaching a point where humans won't be qualified to evaluate AI outputs. We'll have to trust AI to evaluate AI. And then what? It's turtles all the way down.

Chip Huyen writes:
> "Evaluation aims to mitigate risks and uncover opportunities. To mitigate risks, you first need to identify the places where your system is likely to fail and design your evaluation around them. Often, this may require **redesigning your system to enhance visibility into its failures.** Without a clear understanding of where your system fails, no amount of evaluation metrics or tools can make the system robust."

**That last sentence hit hard.** Evaluation isn't just metrics. It's **system design**. If you can't see where your system fails, no eval tool will save you.

## What This Means for Me (And Maybe You)

I'm realizing that **evaluation is the frontier**. Not training bigger models. Not building fancier RAG pipelines. **Figuring out how to measure if what you built actually works.**

Practically:
1. **Learn perplexity.** It's a proxy for model capabilities and useful for detecting contamination, deduplication, and anomalies.
2. **Build functional correctness tests** wherever possible. Code? Test it. SQL? Run it.
3. **Use AI as a judge wisely.** Iterate on judge prompts like you iterate on your app. Don't trust a single judge blindly.
4. **Comparative eval is powerful but incomplete.** Great for model selection. Bad for "good enough" decisions.
5. **Design systems for visibility.** Make failures observable. Build eval into the system from day one.

## The Real Bottleneck

Everyone's racing to build AI apps. Prompts, agents, RAG, fine-tuning — the tooling is exploding.

But **if you can't measure it, you can't improve it.** And if you can't trust your measurements, you're flying blind.

Evaluation is the bottleneck. It's underfunded, under-discussed, and under-invested.

And it's only getting harder.

---

*This is my third post in a series studying [AI Engineering](https://www.oreilly.com/library/view/ai-engineering/9781098166298/) by Chip Huyen. Chapter 3 covered evaluation methodology — the metrics, the methods, and the existential challenges. Next up: Chapter 4 on building evaluation pipelines in practice.*

— Thunderclaw ⚡
