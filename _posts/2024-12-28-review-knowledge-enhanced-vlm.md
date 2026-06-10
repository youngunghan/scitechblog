---
title: "[Paper Review] Knowledge-enhanced Visual-Language Pre-training on Chest Radiology Images"
date: 2024-12-28 00:00:00 +0900
categories: [Paper Review, Medical AI]
tags: [VLM, Medical Imaging, Pre-training, Knowledge Graph]
description: "Review of Knowledge-enhanced Auto Diagnosis (KAD), a model that integrates medical domain knowledge into vision-language pre-training."
image:
  path: assets/img/posts/paper-reviews/kad-overview.png
  alt: KAD Overview
---

> **Note**: This is a review of the paper **"Knowledge-enhanced Visual-Language Pre-training on Chest Radiology Images"** (Nature Communications 2023, [arXiv:2302.14042](https://arxiv.org/abs/2302.14042)).
>
> For a **Korean version** of this review, please visit the **[OUTTA AI Tech Blog](https://blog.outta.ai/103)**.
{: .prompt-info }

## Why I Read This Paper
There have been many attempts to apply Vision-Language Models (VLMs) to the medical AI field, but simply aligning images with text, like CLIP, has clear limitations. In medical data, the relationships between specialized terms (e.g., "Pneumonia", "Pneumothorax")—the Knowledge Graph—are crucial.

This paper (KAD) tackles the question, **"How can we inject the domain knowledge possessed by doctors into the model?"** by taking a direct approach using the UMLS, a massive medical knowledge graph. The result that its **zero-shot performance matched or exceeded the average of three radiologists (by F1 and MCC) on the five CheXpert competition pathologies** was particularly impressive, making it a must-read for any medical AI researcher.

---

## Introduction
Recent vision-language models (e.g., CLIP) have shown great success in general domains. However, in the medical domain, simply aligning images with raw textual reports is insufficient due to the fine-grained nature of medical tasks and the need for specialized domain knowledge.

This paper introduces **Knowledge-enhanced Auto Diagnosis (KAD)**, a novel framework that integrates structured medical knowledge into vision-language pre-training. KAD leverages the **Unified Medical Language System (UMLS)** to guide the learning of visual representations, enabling the model to better understand complex medical concepts and relationships.

![KAD Overview](/assets/img/posts/paper-reviews/kad-overview.png)
_Figure 1: Overview of the KAD framework. It consists of a knowledge encoder trained on a medical knowledge graph and a vision-language pre-training stage that aligns chest X-rays with extracted clinical entities (from Fig. 1 of the paper)._

## Methods

### a. Knowledge Base & Encoder
The authors construct a knowledge base using UMLS, which contains medical concepts (entities) and their relationships (triplets).
-   **Knowledge Graph**: Represents concepts and their relations (e.g., "Pneumonia" is a finding in "Lung").
-   **Knowledge Encoder**: A text encoder (based on PubMedBERT) is pre-trained on this knowledge graph using contrastive learning. This ensures that the text embeddings capture the semantic relationships defined in the medical ontology.

### b. Image-Text Contrastive Learning
The core of KAD is the alignment of chest X-ray images with radiology reports.
-   **Image Encoder**: Uses ResNet-50 or ViT to extract visual features.
-   **Entity Extraction**: Instead of using raw reports, the model extracts clinical entities and relations using tools like RadGraph or heuristic rules. This filters out noise and focuses on medically relevant information.
-   **Disease Query Network (DQN)**: A Transformer-based module that takes a disease name as a query and interacts with the image features to predict the presence of the pathology.

### c. Training Objectives
The model is trained with two main losses:
1.  **Contrastive Loss**: Aligns the image embeddings with the text embeddings of the extracted entities.
2.  **DQN Loss**: A binary cross-entropy loss that optimizes the Disease Query Network for pathology classification.

## Results

### Performance on Seen Classes
On the **PadChest** dataset, KAD's zero-shot diagnosis significantly outperforms the fully supervised CheXNet on five of the seven evaluated pathologies. The paper reports CheXNet's per-pathology AUCs only graphically (Fig. 2a), so the table below lists KAD's exact AUCs (with 95% confidence intervals) and notes the qualitative comparison against CheXNet (see the paper's Fig. 2a for the exact CheXNet AUCs).

| Pathology | KAD AUC (95% CI) | vs. CheXNet |
| :--- | :---: | :---: |
| **Atelectasis** | 0.809 (0.796–0.822) | KAD higher |
| **Cardiomegaly** | 0.916 (0.913–0.919) | KAD higher |
| **Consolidation** | 0.910 (0.896–0.924) | KAD higher |
| **Edema** | 0.966 (0.958–0.974) | KAD higher |
| **Pneumonia** | 0.835 (0.829–0.842) | KAD higher |

_Table 1: KAD zero-shot AUC scores on the PadChest dataset. KAD significantly outperforms the fully supervised CheXNet on five of the seven pathologies (see paper Fig. 2a for the exact CheXNet AUCs)._

### Generalization to Unseen Classes
A key strength of KAD is its zero-shot and few-shot capabilities.
-   **Zero-shot**: KAD achieves impressive performance on unseen pathologies. On the CheXpert benchmark specifically, its zero-shot predictions match or exceed the average of three expert radiologists on the five competition pathologies (measured by F1 and MCC), though this is a result on that particular benchmark rather than a blanket claim across all settings.
-   **Data Efficiency**: In fine-tuning settings with only 1% of labeled data, KAD significantly outperforms existing state-of-the-art models.

![KAD Qualitative Results](/assets/img/posts/paper-reviews/kad-results-qualitative.png)
_Figure 2: Qualitative results showing the attention maps generated by KAD. The model accurately localizes the pathology (red regions) corresponding to the ground truth (red boxes), providing explainability (from the paper)._

---

## Conclusion & Insight
KAD's contribution is injecting a structured medical **knowledge graph (UMLS)** into vision-language pre-training, yielding strong zero-shot diagnosis — even for long-tail diseases — and attention maps that localize pathology.

### Strengths
- Knowledge-guided pre-training gives competitive zero-shot AUCs and high data efficiency (strong with only 1% labels), valuable where labeled medical data is scarce.
- The Disease Query Network's attention maps add a degree of explainability that pure image–text alignment (CLIP) lacks.

### Limitations
- Scope is **chest X-rays** only; transfer to other modalities/organs is untested here, and the pipeline depends on the quality of UMLS and the RadGraph entity extractor.
- The "matches/exceeds three radiologists" result is specific to the five CheXpert competition pathologies (by F1/MCC) — not a general clinical claim.
- AUC and attention-overlap are not clinical evidence: real trust needs prospective validation, calibration, and workflow study.

### Open Questions / My Take
The transferable idea is that **high-quality domain knowledge can substitute for data volume**. Open questions: how much do results hinge on the specific ontology/extractor, and does attention-based explainability actually change clinician decisions? Future medical VLM work will likely focus on integrating high-quality domain knowledge, not just scaling data.
