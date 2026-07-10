---
title: "[Paper Review] Investigating Data Contamination for Pre-training Language Models"
date: 2025-08-23 00:00:00 +0900
categories: [Paper Review, NLP]
tags: [LLM, Data Contamination, Evaluation, Pre-training]
description: "Review of a critical study on data contamination in LLMs, questioning whether performance gains are due to memorization of test data."
image:
  path: assets/img/posts/paper-reviews/contamination-factor.png
  alt: Contamination Factor Analysis
---

> **Note**: This is a review of the paper **"Investigating Data Contamination for Pre-training Language Models"** ([arXiv:2401.06059](https://arxiv.org/abs/2401.06059), 2024).
>
> **Code**: Official repository at [minhaoJ2/Contamination_For_PreTraining](https://github.com/minhaoJ2/Contamination_For_PreTraining) (by first author Minhao Jiang).
>
> For a **Korean version** of this review, please visit the **[OUTTA AI Tech Blog](https://blog.outta.ai/339)**.
{: .prompt-info }

## Why I Read This Paper
With LLMs pouring out these days, you might have suspected at least once, "Is this model's performance real?" Often, benchmark scores are high, but the actual usability is poor. This paper directly investigates one of the causes: **"Data Contamination."**

What was particularly interesting was that they measured the impact by mixing contaminated data on purpose while training the model **"From Scratch."** This is a completely different approach from existing studies that only "guessed" with already trained models. It was very impressive because it showed with clear data why we shouldn't blindly trust LLM performance evaluations.

---

## Introduction
The exceptional performance of Large Language Models (LLMs) is often attributed to model scale and data size. However, a critical question remains: **Are these models actually learning, or are they just memorizing the test data?**

This paper investigates **Data Contamination**, where evaluation data leaks into the pre-training corpus. Unlike previous studies that analyze contamination post-hoc, this research takes a **"pre-training level analysis"** approach, training GPT-2 models from scratch with controlled amounts of contamination to measure its direct impact.

## Context / Related Work
Most prior contamination work is **post-hoc**: it estimates leakage in already-trained models via n-gram overlap (as reported for GPT-3, PaLM, and LLaMA-2). This paper takes the opposite direction — **training GPT-2 from scratch** with controlled contamination — which lets it measure the *causal* effect instead of guessing, and then shows those overlap-based detectors are unreliable.

---

## Data Contamination Types
The authors distinguish between two types of contamination:
1.  **Text Contamination**: Only the input text of the evaluation samples is present in the pre-training data.
2.  **Ground-truth Contamination**: The input text, prompt, and the *correct answer* (ground truth) are all present. This is a more severe form of leakage that previous studies often overlooked.

## Experiments & Findings

### 1. Impact on Performance
For generation-style tasks, **Ground-truth Contamination** tends to have a larger impact on performance than simple Text Contamination. SST-2 is a notable exception: there, Text Contamination yields the higher score. The authors attribute this to the nature of text classification, which depends mainly on the model's comprehension of the input text, so seeing the labeled answer in pre-training helps less than seeing the input itself.

| Dataset | Metric | Original | Text Contam. | GT Contam. |
| :--- | :---: | :---: | :---: | :---: |
| **SST-2** | Acc (%) | 48.34 | **54.89** | 51.02 |
| **SQuAD** | F1 | 9.07 | 9.78 | **11.45** |
| **CNN/DM** | ROUGE-1 | 24.76 | 26.84 | **28.80** |
| **MMLU** | Acc (%) | 22.87 | 23.03 | **23.13** |

_Table 1: Performance comparison (numbers from the paper; see Tables 2 and 3). Ground-truth contamination boosts performance most clearly in generation tasks such as SQuAD and CNN/DM, whereas for the SST-2 classification task text contamination has the larger effect._

### 2. Dataset-Dependent Effects of Repeated Contamination
Repeated contamination is **not universally monotonic or universally inverted-U**. SST-2, SQuAD, and MMLU rise at lower repetition factors and then decline at high repetition, while CNN/DM ROUGE continues to increase over the tested factors. The paper calls attention to a U-shaped relationship, but the plotted higher-is-better scores show dataset-dependent non-monotonic or monotonic trends rather than one shared curve shape.

![Contamination Factor Analysis](/assets/img/posts/paper-reviews/contamination-factor.png)
_Figure 1: Repetition-factor results from the paper. Several tasks improve and then decline at high repetition, whereas CNN/DM continues improving over the tested range; the effect is dataset-dependent (from Fig. 1 of the paper)._

For the tasks that decline, memorization, optimization imbalance, or distribution distortion are possible explanations, but the curve alone does not identify the mechanism. CNN/DM is an explicit counterexample to a universal "too much contamination always hurts" claim.

### 3. Failure of Existing Detection Methods
The authors also evaluate existing contamination detection methods (like n-gram overlap used in PaLM and LLaMA-2).

![Contamination Detection Analysis](/assets/img/posts/paper-reviews/contamination-detection.png)
_Figure 2: Analysis of LLaMA-2's contamination detection method. The "Dirty" category (high overlap) does not necessarily correspond to higher performance, indicating that current detection methods are unreliable (from the paper)._

They find that these methods often fail to distinguish between harmful contamination and harmless data overlap, leading to both false positives and false negatives.

---

## Conclusion & Insight
The contribution is methodological: by training GPT-2 **from scratch** with controlled contamination, the paper shows *causally* — not by post-hoc guessing — that **ground-truth contamination** inflates scores most on generation tasks, and that current n-gram detection is unreliable.

### Strengths
- Controlled from-scratch training isolates the *causal* effect of contamination, which post-hoc studies on already-trained models cannot.
- The Text vs. Ground-truth distinction is a useful, often-overlooked axis; the dataset-dependent repetition experiment is a concrete warning against assuming contamination has a uniform effect.

### Limitations
- Experiments are at **GPT-2 scale**; whether the same magnitudes hold for today's much larger LLMs is untested and may not extrapolate.
- Conclusions are tied to a specific benchmark set (SST-2/SQuAD/CNN-DM/MMLU), and several absolute scores are low (MMLU ≈ random), so some effects are measured near the noise floor.
- It critiques existing detectors but does not deliver a robust replacement detection method.

### Open Questions / My Take
The headline lesson — leaderboard scores can be inflated by memorization, and overlap-based detectors miss it — is important. The open question is the **scale gap**: do these effects grow, shrink, or change shape at 100B+ parameters?
