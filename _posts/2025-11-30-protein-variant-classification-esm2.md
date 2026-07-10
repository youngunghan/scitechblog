---
title: "Building a Protein Variant Classifier with ESM2 and Multi-GPU Training"
description: "Building a protein variant classifier with ESM2: clinical metric selection, a difference-vector architecture, class imbalance, and multi-GPU DDP."
date: 2025-11-30 00:00:00 +0900
categories: [AI, Bioinformatics]
tags: [esm2, pytorch, multi-gpu, class-imbalance, protein-language-model]
author: seoultech
image:
  path: assets/img/posts/protein-classifier/cover_v3.png
  alt: Protein Structure with Highlighted Mutation Analysis
math: true
---

## Introduction

In the field of clinical genomics, accurately predicting whether a specific genetic variant is pathogenic (disease-causing) or benign is a critical challenge. Recently, I worked on a project to develop a deep learning model that classifies protein variants as either **Gain-of-Function (GOF)** or **Loss-of-Function (LOF)** using **ESM2 (Evolutionary Scale Modeling)**, a state-of-the-art protein language model.

This post covers **two related but distinct tasks** with **different label spaces**, so it is worth separating them up front to avoid conflating their labels:

- **Task A — Pathogenic-variant prioritization & metric selection.** A binary `pathogenic (LABEL=1)` vs `benign (LABEL=0)` problem, used to evaluate and choose among existing pathogenicity predictors. (Covered in Challenge 1.)
- **Task B — GOF/LOF classifier training.** A separate binary `GOF` vs `LOF` problem over the variants of interest, where we train our own ESM2-based model. (Covered in Challenges 2-4.)

The two tasks share a class-imbalance theme but do **not** share labels: a "positive" in Task A is a pathogenic variant, whereas a "positive" in Task B is the minority GOF class.

## Challenge 1 (Task A): Metric Selection for Clinical Use

Before diving into the model, I had to evaluate existing pathogenicity predictors. The dataset contains **107 patients**, each with multiple variants where only a few are pathogenic (LABEL=1).

### The Problem: Class Imbalance

The data is highly imbalanced—most variants are benign (LABEL=0), only a few are pathogenic (LABEL=1). This makes metric selection critical.

| Metric | Formula | Problem with Imbalanced Data |
|--------|---------|------------------------------|
| **Accuracy** | (TP+TN) / Total | Predicting all as benign gives high accuracy |
| **AUROC** | Area under TPR-FPR curve | Can look good even with poor precision |

### Why AUROC Alone Is Not Enough

AUROC measures discrimination across *all thresholds*. A model with AUROC=0.94 sounds great, but:
- At what threshold does it achieve good **Precision** and **Recall**?
- In clinical diagnostics, **False Negatives are dangerous** (missing a pathogenic variant)

### Metrics for Clinical Pathogenicity Prediction

For this problem, I focused on both **classification metrics** and **ranking metrics**:

#### Classification Metrics (Binary)

| Metric | Formula | Clinical Importance |
|--------|---------|---------------------|
| **Recall (Sensitivity)** | $\frac{TP}{TP + FN}$ | Must be high: we cannot miss pathogenic variants |
| **Precision (PPV)** | $\frac{TP}{TP + FP}$ | Reduces unnecessary follow-up tests |
| **F1 Score** | $\frac{2 \times Precision \times Recall}{Precision + Recall}$ | Balances both for imbalanced data |

#### Ranking Metric (Patient-Centric)

Since each patient has multiple variants and we want the pathogenic variant to be ranked high:

| Metric | Formula | Clinical Importance |
|--------|---------|---------------------|
| **Hit@K** | $\frac{\text{# eligible patients with a pathogenic variant at rank }\le K}{\text{# eligible patients}}$ | Measures how often at least one pathogenic variant appears in the top K ranks |

The formal definition:

$$
\text{Hit@K} = \frac{1}{N} \sum_{i=1}^{N} \mathbb{1}[\exists v \in P_i:\operatorname{rank}(v) \leq K]
$$

Where:
- $N$ = number of patients
- $P_i$ = the set of known pathogenic variants for patient $i$
- $\operatorname{rank}(v)$ = descending score rank, using the minimum rank for tied scores
- $\mathbb{1}[\cdot]$ = indicator function (1 if true, 0 if false)

This patient-level binary success rate is **Hit@K**, not variant-level recall. The distinction matters when a patient has multiple pathogenic variants. Ties at the K boundary are included rather than broken by input row order, so a tie can produce more than K returned rows.

### Why Recall Is Critical

In a validated clinical workflow, a **False Negative** (ranking a truly pathogenic variant too low) may:
- delay follow-up or confirmatory analysis,
- reduce the chance that a relevant variant is reviewed promptly.

The downstream effect depends on disease, evidence, review workflow, variant actionability, and clinician judgment; this classifier does not directly prescribe treatment. Recall or Hit@K should therefore be emphasized alongside precision and workload, not maximized without a deployment-specific trade-off analysis.

### Evaluation Framework

I evaluated each predictor (A, B, C) with both classification and ranking metrics:

```python
from sklearn.metrics import (
    precision_recall_curve,
    precision_recall_fscore_support,
    roc_auc_score,
)
import numpy as np
import pandas as pd

def select_f1_threshold(y_true_val: np.ndarray, y_scores_val: np.ndarray) -> float:
    """Choose an operating threshold on validation data only."""
    precisions, recalls, thresholds = precision_recall_curve(y_true_val, y_scores_val)
    f1_scores = 2 * precisions[:-1] * recalls[:-1] / (
        precisions[:-1] + recalls[:-1] + 1e-8
    )
    return float(thresholds[np.argmax(f1_scores)])
# end def

def evaluate_predictor(
    y_true_test: np.ndarray,
    y_scores_test: np.ndarray,
    threshold: float,
) -> dict:
    """Evaluate a validation-selected threshold on untouched test data."""
    y_pred = (y_scores_test >= threshold).astype(int)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true_test,
        y_pred,
        average="binary",
        zero_division=0,
    )
    return {
        "auroc": roc_auc_score(y_true_test, y_scores_test),
        "f1": f1,
        "recall": recall,
        "precision": precision,
        "threshold": threshold,
    }
# end def

def compute_top_k_hit(df: pd.DataFrame, score_col: str, k: int) -> float:
    """Compute tie-inclusive patient-level Hit@K."""
    if k <= 0:
        raise ValueError("k must be positive")

    patient_hits = []
    for _, group in df.groupby("Patient_ID"):
        if not group["LABEL"].eq(1).any():
            continue
        ranks = group[score_col].rank(method="min", ascending=False)
        patient_hits.append(bool((group["LABEL"].eq(1) & ranks.le(k)).any()))
    # end for
    if not patient_hits:
        raise ValueError("no patients with a pathogenic variant")
    return float(np.mean(patient_hits))
# end def
```

The threshold-selection and test-evaluation calls must use different patients (or, at minimum, a group-disjoint split). Selecting the best F1 and reporting it on the same 107 patients is an exploratory upper estimate, not a deployable operating point.

### Results

#### Classification Metrics (Exploratory Same-Set Threshold Scan)

The original comparison below selected each predictor's best-F1 threshold on the same 107-patient dataset used for reporting. It is useful for hypothesis generation, but it is optimistically biased; a clinical claim requires a patient-disjoint validation set for threshold selection and an untouched test cohort for the final table.

| Predictor | AUROC | Best F1 | Recall @ Best F1 | Precision @ Best F1 |
|-----------|-------|---------|------------------|---------------------|
| A | **0.94** | 0.42 | 0.65 | 0.31 |
| B | 0.88 | **0.58** | **0.82** | 0.45 |
| C | 0.91 | 0.51 | 0.71 | 0.40 |

#### Ranking Metrics (Patient-Centric, Tie-Inclusive)

| Predictor | Hit@1 | Hit@5 |
|-----------|--------------|--------------|
| A | 12% | 35% |
| B | **24%** | **52%** |
| C | 18% | 41% |

**Key Findings**:
1. Predictor A had the highest AUROC but the worst F1, Recall, and Hit@K metrics
2. Predictor B achieved **82% exploratory Recall** and **52% Hit@5** on this dataset, meaning at least one known pathogenic variant ranked within the top five for 52% of eligible patients

**Exploratory decision**: **Predictor B** is the candidate to carry into a disjoint validation because it had:
1. Highest Recall (minimizes missed pathogenic variants)
2. Best F1 Score (balanced performance on imbalanced data)
3. Best Hit@5 (at least one pathogenic variant is within the top five ranks for 52% of patients)

This table does **not** establish a clinical operating point: the threshold was tuned and evaluated on the same cohort, confidence intervals are absent, and Hit@K does not measure how many pathogenic variants were missed when a patient has more than one.

**Lesson:** In medical AI with class imbalance, evaluate using multiple metrics that reflect clinical consequences—not just AUROC.


## Challenge 2 (Task B): Modeling Protein Variants with ESM2

The core task was to classify variants using `esm2_t33_650M_UR50D`.

### Existing vs. Proposed Approach

A standard approach in this domain often involves feeding the mutant sequence directly into the model to predict its property.

![Baseline Architecture](/assets/img/posts/protein-classifier/baseline_architecture.png)
_Figure 1: Standard Baseline Approach. The model only sees the mutant sequence, making it difficult to learn the specific impact of the mutation relative to the wild-type._

However, simply feeding the mutant sequence isn't enough. The model needs to understand *what changed*. I designed the input to explicitly capture the difference:

```
Input = Concat(E_wt, E_mut, E_mut - E_wt)
```

- **E_wt**: Embedding of the Wild-Type sequence
- **E_mut**: Embedding of the Mutant sequence
- **Difference**: The vector representing the direction of change (Mutant - Wild-Type)

This "Difference Vector" was a key design choice in my experiments for distinguishing between LOF (function loss) and GOF (function gain).

![Model Architecture](/assets/img/posts/protein-classifier/architecture.png)
_Figure 2: Our Proposed Architecture. By explicitly feeding the difference vector (Mutant - WT), the model can directly focus on the functional shift caused by the variant._

### Code Snippet: Model Architecture

```python
import torch
import torch.nn as nn
from transformers import EsmModel

class ESM2VariantClassifier(nn.Module):
    def __init__(self, model_name="facebook/esm2_t33_650M_UR50D"):
        super().__init__()
        self.esm = EsmModel.from_pretrained(model_name)
        # Freeze backbone for efficiency
        for param in self.esm.parameters():
            param.requires_grad = False
            
        hidden_size = self.esm.config.hidden_size
        
        self.classifier = nn.Sequential(
            nn.Linear(hidden_size * 3, 512), # 3x input size due to concatenation
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 2)
        )

    def forward(self, wt_ids, wt_mask, mut_ids, mut_mask):
        wt_out = self.esm(input_ids=wt_ids, attention_mask=wt_mask)
        mut_out = self.esm(input_ids=mut_ids, attention_mask=mut_mask)
        
        wt_cls = wt_out.last_hidden_state[:, 0, :]
        mut_cls = mut_out.last_hidden_state[:, 0, :]
        
        diff = mut_cls - wt_cls
        combined = torch.cat((wt_cls, mut_cls, diff), dim=1)
        
        return self.classifier(combined)
```

Here I pool each sequence using the CLS token (`last_hidden_state[:, 0, :]`); a common alternative is mean-pooling the hidden states over the non-special (non-CLS/EOS/padding) tokens, which can yield a more stable whole-sequence representation when the CLS token is not specifically trained as a summary.

## Challenge 3 (Task B): Extreme Class Imbalance

This imbalance is on Task B's GOF/LOF label space (distinct from the pathogenic/benign labels of Task A). The dataset had a **9:1 imbalance** (90% LOF, 10% GOF). A standard model would simply predict "LOF" for everything and achieve 90% accuracy, which is useless.

### Solution: Weighted Loss
I used `CrossEntropyLoss` with class weights inversely proportional to the class frequencies.

```python
import torch
import torch.nn as nn

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# LOF (0): 90%, GOF (1): 10%
class_weights = torch.tensor([0.1, 0.9]).to(device)
criterion = nn.CrossEntropyLoss(weight=class_weights)
```

This forces the model to pay 9x more attention to the minority GOF class, preventing it from being ignored.

## Challenge 4 (Task B): Distributed Training on A100s

To utilize 4x NVIDIA A100 GPUs, I used PyTorch's **DistributedDataParallel (DDP)**.

Key implementation details:
1.  **`DistributedSampler`**: Ensures each GPU gets a different slice of data.
2.  **`init_process_group`**: Sets up communication between GPUs.
3.  **`torchrun`**: The launcher utility to manage processes.

One useful pre-cluster check is a **CPU smoke test** of the data/model path. It is not a single-GPU DDP test: in the later public implementation, selecting `gloo` explicitly forces the device to CPU. The real 4xA100 run used `nccl`, which [PyTorch recommends](https://docs.pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html) for distributed GPU training.

The original coursework used a different private training script. A later public reimplementation is available at commit [`6b8bcd5`](https://github.com/youngunghan/protein-variant-classifier/tree/6b8bcd57a4964f1f788f96fb934ae485986c5f25); its runnable one-process distributed CPU smoke path is:

```bash
# Current public implementation: one-process distributed CPU smoke test
git checkout 6b8bcd57a4964f1f788f96fb934ae485986c5f25
torchrun --standalone --nproc_per_node=1 code/train_esm_classifier.py \
    --backend gloo --use_mock_data --epochs 1 --batch_size 2 \
    --max_len 64 --output_dir /tmp/pvc-ddp-smoke
```

The current script reads `LOCAL_RANK` from `torchrun`, and its `gloo` branch deliberately selects CPU. This checks process-group and DDP plumbing, but it is not validation of CUDA/NCCL behavior or the historical four-GPU result.

## What Didn't Work / Limitations

This was a small-scale study, so the results are a proof of concept rather than a validated clinical tool:

- **Tiny, reused evaluation set.** Task A's predictor comparison uses 107 patients with only a few pathogenic variants each, and the best-F1 threshold was selected on the same cohort used for reporting. The AUROC/F1/Hit@K gaps therefore carry both wide uncertainty and selection bias; no confidence intervals or significance tests are reported.
- **Frozen backbone.** ESM2 is used purely as a feature extractor (backbone frozen, only the head trained), which caps how much variant-specific signal the model can capture; fine-tuning or LoRA was not compared.
- **Static class weighting only.** The 9:1 GOF/LOF imbalance is handled with fixed inverse-frequency weights; resampling, focal loss, and threshold calibration were not benchmarked against it.
- **Pooling not ablated.** CLS-token pooling is used; as noted above, mean-pooling may give a more stable representation, but the two were not compared head-to-head.
- **No external validation.** Generalization to other cohorts and a leakage-safe held-out split (so variants from the same patient don't span train/test) are not established here.

## Conclusion

This project reinforced the importance of domain-specific feature engineering (Difference Vector) and robust engineering practices (DDP, Weighted Loss) when working with biological data. By combining pre-trained PLMs with thoughtful architecture, we can build powerful tools for genomic analysis.

> **Setup (for reproducibility).** Model: `facebook/esm2_t33_650M_UR50D` (HuggingFace `transformers`, backbone frozen). Hardware: 4× NVIDIA A100, PyTorch `DistributedDataParallel` (`nccl`) launched with `torchrun`. Data: 107 patients (Task A); ~9:1 LOF/GOF split (Task B). The original coursework checkout remains private; the linked public repository is a later implementation, not provenance for every historical command or result.
{: .prompt-info }
