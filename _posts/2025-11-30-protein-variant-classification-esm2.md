---
title: "Building a Protein Variant Classifier with ESM2 and Multi-GPU Training"
date: 2025-11-30 00:00:00 +0900
categories: [AI, Bioinformatics]
tags: [esm2, pytorch, multi-gpu, class-imbalance, protein-language-model]
author: seoultech
image:
  path: assets/img/posts/protein-classifier/cover_v3.png
  alt: Protein Structure with Highlighted Mutation Analysis
---

## Introduction

In the field of clinical genomics, accurately predicting whether a specific genetic variant is pathogenic (disease-causing) or benign is a critical challenge. Recently, I worked on a project to develop a deep learning model that classifies protein variants as either **Gain-of-Function (GOF)** or **Loss-of-Function (LOF)** using **ESM2 (Evolutionary Scale Modeling)**, a state-of-the-art protein language model.

This post shares the technical challenges I encountered—specifically regarding **class imbalance** and **distributed training on A100 GPUs**—and how I solved them.

## Challenge 1: Metric Selection for Clinical Use

Before diving into the model, I had to evaluate existing pathogenicity predictors. A common pitfall in this domain is relying solely on global metrics like **AUROC**.

While one predictor had the highest AUROC (0.94), further analysis revealed that it wasn't the best for clinical workflows. In a real-world setting, clinicians review variants for a specific patient.

I implemented a **Patient-Centric Ranking** analysis:
1. Group variants by patient.
2. Sort variants by prediction score.
3. Check the rank of the actual pathogenic variant.

**Result:** A different predictor, despite having a lower AUROC, had a **2x higher Top-1 Accuracy**. This means it was twice as likely to place the causal variant at the very top of the list, significantly reducing the time clinicians spend reviewing candidates.

**Lesson:** Always align your evaluation metrics with the actual end-user workflow, not just statistical textbook definitions.

## Challenge 2: Modeling Protein Variants with ESM2

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

This "Difference Vector" proved crucial for distinguishing between LOF (function loss) and GOF (function gain).

![Model Architecture](/assets/img/posts/protein-classifier/architecture.png)
_Figure 2: Our Proposed Architecture. By explicitly feeding the difference vector (Mutant - WT), the model can directly focus on the functional shift caused by the variant._

### Code Snippet: Model Architecture

```python
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

## Challenge 3: Extreme Class Imbalance

The dataset had a **9:1 imbalance** (90% LOF, 10% GOF). A standard model would simply predict "LOF" for everything and achieve 90% accuracy, which is useless.

### Solution: Weighted Loss
I used `CrossEntropyLoss` with class weights inversely proportional to the class frequencies.

```python
# LOF (0): 90%, GOF (1): 10%
class_weights = torch.tensor([0.1, 0.9]).to(device)
criterion = nn.CrossEntropyLoss(weight=class_weights)
```

This forces the model to pay 9x more attention to the minority GOF class, preventing it from being ignored.

## Challenge 4: Distributed Training on A100s

To utilize 4x NVIDIA A100 GPUs, I used PyTorch's **DistributedDataParallel (DDP)**.

Key implementation details:
1.  **`DistributedSampler`**: Ensures each GPU gets a different slice of data.
2.  **`init_process_group`**: Sets up communication between GPUs.
3.  **`torchrun`**: The launcher utility to manage processes.

One interesting hurdle was **verifying DDP logic on a single local GPU**. I learned that you can use the `gloo` backend (CPU-based) with `torchrun --nproc_per_node=1` to simulate the distributed environment locally before deploying to the expensive cluster.

```bash
# Local verification command
torchrun --nproc_per_node=1 train_script.py --backend gloo
```

## Conclusion

This project reinforced the importance of domain-specific feature engineering (Difference Vector) and robust engineering practices (DDP, Weighted Loss) when working with biological data. By combining pre-trained PLMs with thoughtful architecture, we can build powerful tools for genomic analysis.
