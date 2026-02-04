---
title: Data From Elsewhere Still Helps
date: 2026-02-05
description: Multilingual training improves performance across all languages, even the ones you have data for.
tags: [transformers, multilingual, ner, cross-lingual-transfer]
---

# Data From Elsewhere Still Helps

**Source:** Natural Language Processing with Transformers (Revised Edition), Chapter 4  
**Task:** Named Entity Recognition across German, French, Italian, English  
**Model:** XLM-RoBERTa (pretrained on 100 languages)

Counterintuitive result: training on German + French improves German performance compared to training on German alone.

You'd expect the opposite—adding French data should dilute the German signal. But multilingual training forces the model to learn more robust, language-agnostic representations.

## The Experiments

Fine-tune XLM-RoBERTa on a Swiss corpus (German 63%, French 23%, Italian 8%, English 6%). Test three strategies:

1. **Monolingual** — Fine-tune on German (12,580 examples), zero-shot transfer to others
2. **Target language** — Fine-tune directly on each language's data
3. **Multilingual** — Fine-tune on all languages together

Results (F1 scores on test sets):

| Strategy | German | French | Italian | English |
|----------|--------|--------|---------|---------|
| German only | 0.868 | 0.714 | 0.692 | 0.589 |
| Each language | 0.868 | 0.851 | 0.819 | 0.707 |
| All languages | **0.868** | **0.865** | **0.858** | **0.787** |

The multilingual model **matches or beats** monolingual training on every language.

French gets +15 points over zero-shot transfer (expected).  
Italian gets +16 points despite never being in the German-only model.  
German **doesn't degrade** despite adding 3 other languages to training.

## Why It Works

XLM-RoBERTa was pretrained on 100 languages with masked language modeling. It already has multilingual representations—fine-tuning on multiple languages reinforces the cross-lingual signal instead of overriding it with language-specific patterns.

Training on German alone makes the model German-specific.  
Training on German + French makes the model learn "what's common across languages" (entity patterns, context clues, boundary markers).  
That general knowledge transfers better to Italian and English.

## When Zero-Shot Makes Sense

Fine-tuning on French with only 250 examples: **F1 = 0.137** (way worse than zero-shot 0.714).  
With 750 examples: zero-shot and fine-tuning converge.  
With 4,000 examples: fine-tuning hits 0.850 (matches German performance).

**Rule of thumb:** If you have <750 labeled examples in the target language, zero-shot transfer from a high-resource language beats fine-tuning on scarce data.

If you have 750+ examples, fine-tune directly.  
If you have data in multiple languages, **always train on all of them**.

## The Distance Problem

Zero-shot transfer from German:
- French (Romance): -15 points
- Italian (Romance): -18 points  
- English (Germanic): -28 points

Surprising—English is Germanic like German, but performs worst. Why?

Language families matter less than **training data distribution**. XLM-RoBERTa was pretrained on Wikipedia + Common Crawl. German Wikipedia articles have different structure/content than English ones. French and Italian Wikipedia are more similar to German in how they write about entities (geography, organizations, parenthetical clarifications).

The lesson: **linguistic similarity ≠ transfer performance**. Check your data distributions.

## Token Classification Is Different

Sequence classification (Chapter 2): one label for the whole sequence.  
Token classification (NER): one label **per token**.

Challenges:
1. **Subword splitting** — "Einwohnern" → ["▁Einwohner", "n"]. Which gets the B-LOC label?  
   **Solution:** First subword gets the label, others are masked with -100 (ignored in loss).

2. **IOB2 format** — B-PER (beginning), I-PER (inside), O (outside). Consecutive tokens in the same entity get I- tags.  
   **Example:** "Jeff Dean" → [B-PER, I-PER]

3. **Special tokens** — `<s>` and `</s>` (XLM-R) also get -100 labels (not part of named entities).

SentencePiece tokenizer (250K vocab) handles all 100 languages with one model. Uses Unicode characters directly, preserves whitespace with `▁` character (U+2581). Language-agnostic—no language-specific pretokenization.

## Building Custom Models

XLM-RoBERTa has the same architecture as RoBERTa (BERT variant). The chapter builds `XLMRobertaForTokenClassification` from scratch to show how custom task-specific heads work.

**Architecture:**
- **Body** = `RobertaModel` (12 transformer layers, pretrained weights)
- **Head** = dropout + linear layer (maps hidden states → 7 NER tags)

```python
class XLMRobertaForTokenClassification(RobertaPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        self.roberta = RobertaModel(config, add_pooling_layer=False)
        self.dropout = nn.Dropout(config.hidden_dropout_prob)
        self.classifier = nn.Linear(config.hidden_size, config.num_labels)
        self.init_weights()  # Load pretrained body, random head
```

Inheriting from `RobertaPreTrainedModel` gives you `.from_pretrained()` for free. You don't implement weight loading—just define the forward pass.

Bodies are task-agnostic (same for classification, NER, QA).  
Heads are task-specific (7-class linear layer for NER, 2-class for sentiment).

**Why custom models?** When Hugging Face doesn't have the exact task you need, you can build it in ~50 lines by:
1. Loading a pretrained body
2. Adding your own head
3. Defining the forward pass (body → head → loss calculation)

## Error Analysis Reveals Dataset Issues

The PAN-X dataset uses "silver standard" annotations (automatically generated from Wikipedia, not human-labeled). High-loss examples reveal problems:

- "United Nations Multidimensional Integration Mission in the Central African Republic" labeled as **B-PER** (person).  
  Correct: B-ORG.

- "8. Juli" (8th of July) labeled as **B-ORG** (organization).  
  Correct: O.

Confusion matrix shows **B-ORG ↔ I-ORG** is the most common error (model confuses entity boundaries).

Most common high-loss tokens:
- Whitespace `▁` (high total loss, low mean—just very frequent)
- Prepositions "in", "von", "der" (often near entities, ambiguous)
- Parentheses, slashes (high mean loss—rare but hard to classify)

**Why parentheses are hard:** Wikipedia article titles use them for disambiguation.  
"Hama (Unternehmen)" = Hama (company)  
"Keskkála (Martna)" = Keskkála (geographic clarification)

Automated extraction labeled the parentheses as part of the entity. Humans wouldn't. Silver standard ≠ gold standard.

**What to do:** Inspect high-loss examples before deploying. Reveals bugs (wrong loss calculation, label masking errors) and dataset issues (mislabeled, ambiguous, domain-specific conventions).

## Practical Recommendations

1. **If you have multilingual data, use all of it.** Even if one language has 10x more examples than the others. Multilingual training improves all languages.

2. **Zero-shot transfer is a prototype, not production.** Fine-tune on target language once you have 750+ labeled examples.

3. **Focus cross-lingual transfer within language families.** German → French/Italian works better than German → English (despite linguistic similarity). Check data distributions, not just linguistic trees.

4. **Inspect high-loss examples before deploying.** Sort validation set by loss. Look at top 10-20. You'll find dataset errors, model confusion patterns, and edge cases.

5. **SentencePiece is the reason XLM-R works.** One tokenizer for 100 languages, no language-specific pretokenization, preserves whitespace. The 250K vocab handles rare words by splitting them into subwords.

6. **Bodies + heads separation is powerful.** Pretrained body is task-agnostic. Swap the head to change tasks. Build custom heads for tasks Hugging Face doesn't cover.

## The Core Insight

More data in one language doesn't just help that language.

If the data is multilingual, it helps **all languages** by forcing the model to learn language-independent entity patterns instead of memorizing language-specific surface forms.

Training on German alone: model learns "German names look like X."  
Training on German + French + Italian: model learns "entity boundaries occur when Y."

Y transfers. X doesn't.

The multilingual model isn't just better on average—it's better on **every single language** including the high-resource ones.

Data from elsewhere still helps.
