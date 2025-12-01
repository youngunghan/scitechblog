---
title: "[Paper Review] Investigating Data Contamination for Pre-training Language Models"
date: 2025-08-23 00:00:00 +0900
categories: [Paper Review, NLP]
tags: [LLM, Data Contamination, Evaluation, Pre-training]
canonical_url: https://blog.outta.ai/339
description: "Review of a critical study on data contamination in LLMs, questioning whether performance gains are due to memorization of test data."
image:
  path: /scitechblog/assets/img/posts/paper-reviews/contamination-factor.png
  alt: Contamination Factor Analysis
---

> **Note**: This is a review of the paper **"Investigating Data Contamination for Pre-training Language Models"** (Arxiv 2024).
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

## Data Contamination Types
The authors distinguish between two types of contamination:
1.  **Text Contamination**: Only the input text of the evaluation samples is present in the pre-training data.
2.  **Ground-truth Contamination**: The input text, prompt, and the *correct answer* (ground truth) are all present. This is a more severe form of leakage that previous studies often overlooked.

## Experiments & Findings

### 1. Impact on Performance
The experiments show that **Ground-truth Contamination** has a much larger impact on performance than simple Text Contamination.

| Dataset | Metric | Original | Text Contam. | GT Contam. |
| :--- | :---: | :---: | :---: | :---: |
| **SST-2** | Acc (%) | 48.34 | **54.89** | 51.02 |
| **SQuAD** | F1 | 9.07 | 9.78 | **11.45** |
| **CNN/DM** | ROUGE-1 | 24.76 | 26.84 | **28.80** |
| **MMLU** | Acc (%) | 22.9 | 23.3 | **23.9** |

_Table 1: Performance comparison. Ground-truth contamination significantly boosts performance in structured tasks like SQuAD and CNN/DM, sometimes even surpassing larger models._

### 2. The U-Shaped Effect of Repeated Contamination
One of the most interesting findings is the **U-shaped performance trend** when the contamination is repeated multiple times in the pre-training corpus.

![Contamination Factor Analysis](/assets/img/posts/paper-reviews/contamination-factor.png)
_Figure 1: The effect of repeated contamination. Performance initially improves as the contamination factor increases (0-10 repetitions), but then starts to decline and even drops below the baseline with excessive repetition (20+)._

This suggests that while some exposure to test data helps, **over-fitting** to the specific examples eventually hurts the model's generalizability or introduces noise.

### 3. Failure of Existing Detection Methods
The authors also evaluate existing contamination detection methods (like n-gram overlap used in PaLM and LLaMA-2).

![Contamination Detection Analysis](/assets/img/posts/paper-reviews/contamination-detection.png)
_Figure 2: Analysis of LLaMA-2's contamination detection method. The "Dirty" category (high overlap) does not necessarily correspond to higher performance, indicating that current detection methods are unreliable._

They find that these methods often fail to distinguish between harmful contamination and harmless data overlap, leading to both false positives and false negatives.

---

## Conclusion & Insight
This paper revealed the inconvenient truth that **"Data contamination is more serious than thought, and current detection methods are incomplete."** In particular, the fact that **Ground-truth Contamination** can be the main culprit of performance inflation suggests that we need to scrutinize training data more carefully whenever a new model comes out.

If you are tired of the score games on LLM leaderboards, it is worth reflecting on the lessons this paper gives. **"True generalization ability"** is not obtained by simply memorizing the test set.
