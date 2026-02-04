---
title: Attack Cost Asymmetry
date: 2026-02-04
description: When cheap bytes burn expensive GPU cycles, economics becomes the vulnerability
tags: [security, llm, economics, dos]
---

# Attack Cost Asymmetry

Traditional Denial-of-Service (DoS) attacks require effort. You need botnets—networks of compromised devices—to generate enough traffic to overwhelm a target. The Mirai attack on Dyn in 2016 hit 1.2 Tbps by infecting thousands of IoT devices. That's coordination, scale, infrastructure.

LLMs changed the math.

Now an attacker can send a few dozen bytes—"What is one million factorial?"—and force you to burn thousands of GPU cycles. The cost to attack is trivial. The cost to defend is enormous.

**That's not a technical problem. That's an economic vulnerability.**

## The Old Model: Symmetric Effort

Traditional DoS attacks have cost symmetry. Flooding a server with traffic requires bandwidth. Bandwidth costs money. More traffic = more attacker resources.

Three classic attack types:

**1. Volume-Based Attacks**
- Overwhelm with massive traffic (UDP floods, ICMP floods, spoofed packets)
- Consumes bandwidth—the target can't process legitimate requests
- DDoS amplifies this by using botnets to attack from multiple sources

**2. Protocol Attacks**
- Exploit network/transport layer weaknesses
- SYN floods (incomplete TCP handshakes), ping of death (oversized packets), Smurf attacks (ICMP broadcast amplification)
- Small traffic, disproportionate load—but still requires coordination

**3. Application Layer Attacks**
- Target web servers (HTTP floods, Slowloris)
- Fewer resources needed than volume attacks, but still measurable effort

The pattern: **attacking has a cost**. You need infrastructure, coordination, sustained effort. That's a natural rate limit.

## The New Model: Asymmetric Costs

LLMs broke the symmetry.

Three unique vulnerabilities:

**1. Scarce Resource Attacks**
- LLMs require GPUs or specialized AI accelerators—expensive, limited supply
- Attacker sends cheap requests: "Translate this 10,000-word document"
- Defender burns expensive GPU cycles processing each request
- Gap: trivial to send, intensive to process

**2. Context Window Exhaustion**
- The context window is the LLM's "short-term memory"
- Attacker crafts extremely long prompts or forces verbose responses
- Each token generation consumes computational resources
- Filling the context window strains the model's capacity

**3. Unpredictable User Input**
- LLMs are designed to handle varied queries
- Attacker exploits this: "What is the sum of all prime numbers up to one billion?"
- Computationally intensive requests look like legitimate use
- "Write a detailed history of every World Cup match"—generates massive content
- "List every step in producing a smartphone from mining to assembly, including socioeconomic impacts"—deep, multi-domain reasoning

The attacker doesn't need botnets. They don't even need multiple machines. One adversary with modest resources can flood an LLM with requests that **individually** drain resources.

**The architecture designed for deep analysis becomes the vulnerability.**

## Denial-of-Wallet: Economics as Attack Vector

Denial-of-Service disrupts availability. **Denial-of-Wallet (DoW) bankrupts you.**

LLMs are uniquely vulnerable because:
- **High computational costs** — significant processing power per request
- **Scalability of usage** — designed to scale with volume (turns scalability into a liability)
- **API-based access** — programmatically generate high-volume requests
- **Complex pricing models** — based on tokens processed, interaction duration, model type

DoW isn't new—it's been a cloud computing risk since usage-based pricing began. But LLMs amplify it because computational costs are so high.

**Advanced DoW goes further:** Combine prompt injection (Ch.4) with resource hijacking. Attacker jailbreaks the LLM, then uses it to generate phishing emails, crack CAPTCHAs, or mine cryptocurrency—**all at your expense.**

This resembles cryptojacking (illicitly mining crypto on victim's cloud resources), but worse: you're not just paying for compute cycles, you're **legally liable** for what the attacker does with your LLM.

## Model Cloning: IP Theft via Query Flooding

Model cloning is DoS with a different goal: **steal the intellectual property** that went into training your model.

Attack pattern:
1. Flood the LLM with prompts on specific topics
2. Harvest all outputs
3. Use outputs to fine-tune an alternate model
4. Replicate functionality without accessing original architecture or training data

This isn't just service disruption—it's IP theft. The attacker uses your expensive infrastructure to train their cheap knockoff.

**Tactical similarity to DoS/DoW**: exploits resources through extensive querying. **Strategic difference**: covert replication, not disruption.

## The Defense Stack

Traditional defenses assume attack effort scales with damage. LLMs need new strategies.

**1. Domain-Specific Guardrails**
- Fine-tune the model to respond only to domain-specific inquiries
- Ecommerce chatbot answers product questions, deflects "What is one million factorial?"
- Reduces computational waste on irrelevant requests

**2. Input Validation & Sanitization**
- Strict criteria for acceptable input
- Truncate or divide inputs exceeding context window size
- Reject unusually complex structures that trigger excessive processing

**3. Robust Rate Limiting**
- Define and enforce request frequency limits per user/system
- Dynamic adjustments based on system performance and user behavior
- Prevents overwhelm from excessive demands (malicious or legitimate surge)

**4. Resource Use Capping**
- Set limits on tokens processed per request, computation complexity, processing time
- Makes it harder to induce highly resource-intensive tasks
- Maintains predictable, stable system performance

**5. Monitoring & Alerts**
- Track CPU usage, memory consumption, response times, concurrent requests
- Establish baseline patterns, detect anomalies
- Prompt investigation and response

**6. Financial Thresholds & Alerts**
- Establish budget limits for LLM usage
- Configure alerts when thresholds are approached/exceeded
- Critical in pay-per-use models to avoid unexpected costs

## The Economic Reality

The fundamental problem: **LLMs operate in an environment where attack costs are decoupled from defense costs.**

Traditional web services: linear relationship. More traffic → more resources needed on both sides.

LLMs: exponential gap. Cheap input → expensive processing. One adversary can bankrupt a service without infrastructure.

**Mitigation isn't about eliminating the gap—it's about managing it.** You can't make LLMs cheap to run. You can make attacks expensive through rate limiting, validation, guardrails, financial controls.

But the asymmetry remains. Every architectural choice that makes LLMs powerful (deep analysis, flexible input handling, scalable APIs) also makes them vulnerable.

---

**Bottom line:** Traditional DoS attacks require infrastructure. LLM DoS/DoW attacks exploit the cost asymmetry between generating requests and processing them. When attack costs are trivial and defense costs are massive, economics becomes the vulnerability. Mitigation is about managing the gap, not eliminating it.
