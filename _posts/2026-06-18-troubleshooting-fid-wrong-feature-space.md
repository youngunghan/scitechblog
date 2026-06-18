---
title: "[Troubleshooting] Your FID of 0.24 Isn't Near-Perfect — It's the Wrong Feature Space"
date: 2026-06-18 09:00:00 +0900
categories: [AI, Troubleshooting]
tags: [fid, gan, model-evaluation, generative-models, torchmetrics, pytorch]
description: "A text-to-image GAN reported FID 0.2423 and it looked near-perfect. It wasn't: pytorch-ignite's default FID scores in a 1000-d logit space, not the standard 2048-d pool3. The same model's real FID was ~165, and the two scales don't convert."
author: seoultech
image:
  path: assets/img/posts/fid-feature-space/ignite-vs-2048.png
  alt: "The same model and images scored by two FID feature spaces: ignite's 1000-d default versus the standard 2048-d pool3"
math: true
mermaid: true
---

## Introduction

I inherited an evaluation notebook for a text-to-image GAN. It reported **FID 0.2423** and **IS 1.86**, and since FID is lower-is-better, 0.24 reads like a near-perfect generator.

That is precisely the problem. State-of-the-art face GANs (StyleGAN2 on FFHQ) land around **FID 3**; a mediocre one sits at 30–80. An FID of 0.24 would mean the generated and real distributions are *almost identical* — superhuman, from a model whose samples were visibly blurry. A number that good is almost never a great model; it is almost always a broken metric.

It was. This post walks through why **pytorch-ignite's default FID** returns a tiny, non-comparable number, proves it on our own model (same images, two feature spaces, a ~900× gap), flags a second bug that compounds it, and shows the fix.

> **Setup.** The model is a multi-stage CLIP-guided GAN trained on an MM-CelebA-HQ subset, on a single RTX 4060 Ti (8 GB). The dataset is licensed, so no generated faces are shown here — only metric values and plots, which are what this post is about anyway.
{: .prompt-info }

## The Symptom: An Impossibly Good FID

- **Expected:** an FID in the literature range (single digits for excellent, tens for mediocre) that tracks sample quality.
- **Actual:** **FID 0.2423**, while the samples were clearly low quality.
- **Reproduction:** the notebook computed FID with pytorch-ignite's metric, constructed with no feature extractor:

```python
from ignite.metrics import FID

fid_metric = FID(device=idist.device())   # the bug is hidden in this default
```

- **Environment:** `pytorch-ignite`, InceptionV3 weights downloaded by ignite, single CUDA device.

A score of 0.24 implies the two Gaussians FID compares are nearly coincident. The samples said otherwise. So the question is not "why is the model so good" — it is "what is this number actually measuring."

## Root Cause: ignite's Default FID Uses 1000-d Logits, Not 2048-d pool3

FID is the Fréchet distance between two Gaussians fit to **Inception features**:

$$\text{FID} = \lVert \mu_r - \mu_f \rVert^2 + \operatorname{Tr}\!\left(\Sigma_r + \Sigma_f - 2\left(\Sigma_r \Sigma_f\right)^{1/2}\right)$$

The subtlety lives in the word *features*. The canonical FID (Heusel et al., 2017) uses the **2048-dimensional `pool3`** activations of InceptionV3. But "Inception features" is a choice, and ignite makes a different one by default: with no `feature_extractor` argument, `FID(device=...)` falls back to ignite's `InceptionModel` wrapper, whose default output is the **1000-dimensional classification logits** (`num_features=1000`).

A Fréchet distance computed in a 1000-d softmax-logit space and one computed in the 2048-d pool3 space are simply **different metrics**. The logit space is lower-dimensional, differently scaled, and concentrated, so the distances come out 100–1000× smaller — and comparable to *nothing* in the literature.

```mermaid
flowchart LR
    I["Generated / real image"] --> N["InceptionV3"]
    N --> L["1000-d logits<br/>(ignite FID default)"]
    N --> P["2048-d pool3<br/>(standard FID)"]
    L --> A["FID approx 0.18<br/>not comparable"]
    P --> B["FID approx 165<br/>literature scale"]
```

The kicker: the pytorch-ignite GAN-evaluation tutorial the notebook was based on **does** build a custom 2048-d wrapper around InceptionV3 and passes it as `feature_extractor=...`. The notebook copied the `FID(...)` call but dropped the wrapper, silently inheriting the 1000-d default.

## Proof: Same Model, Two Scales (and No Conversion)

To show this is the metric and not the model, I took our shipped best checkpoint, generated one fake **per test caption** (510 test images), and scored the *same* fakes and reals two ways — ignite's default and the standard 2048-d FID:

| Inputs | ignite default (1000-d logits) | standard (2048-d pool3) |
|--------|:---:|:---:|
| fakes vs real | **0.181** | **164.9** |
| real vs real (sanity) | −0.000 | — |

![Bar chart on a log axis: the same model and images score 0.181 under ignite's 1000-d default and 164.9 under the standard 2048-d pool3 FID](/assets/img/posts/fid-feature-space/ignite-vs-2048.png)
_Same generator, same 510 image pairs — only the Inception feature space differs. The 1000-d default reports 0.181; the standard 2048-d FID reports 164.9 (a 910× gap). The real-vs-real control is ≈ 0, as it should be._

Two things to read off this:

1. **0.18 is the same tiny scale as the original 0.2423.** The notebook's "near-perfect" number was this 1000-d artifact all along; the real FID of this model is ~165 — high, because the model is genuinely weak.
2. **You cannot convert one into the other.** There is no fixed multiplier: on an earlier run, the 2048-d / 1000-d ratio was **1343×** at one epoch and **1870×** at another. The ratio depends on the model, so a 1000-d FID carries no recoverable information about the standard FID. You have to recompute from images.

## A Second Bug: All Fakes From One Prompt

Even with the right extractor, the notebook's comparison was invalid. Its `generate_images_batch(128)` produced all 128 fakes from a **single fixed caption**, then compared them against real images spanning the whole test set. That pits a one-point fake distribution against a broad real distribution (with a real/fake value-range mismatch on top). FID is a distribution-to-distribution distance; the fakes have to be drawn from the **same caption distribution** as the reals, or the number is meaningless before the feature space even enters the picture.

## The Fix: Standard 2048-d FID, Fakes Per Caption

Use `torchmetrics`, which defaults to the 2048-d pool3 features, accumulate over the whole test set, and condition each fake on its real caption:

```python
import torch
from torchmetrics.image.fid import FrechetInceptionDistance

fid = FrechetInceptionDistance(normalize=False).to(device)  # 2048-d pool3; expects uint8 [0,255]
to_u8 = lambda x: (x.clamp(0, 1) * 255).to(torch.uint8)

with torch.no_grad():
    for real, captions in test_loader:                       # real in [0,1]
        fid.update(to_u8(real.to(device)), real=True)
        z = torch.randn(captions.size(0), noise_dim, device=device)
        fake = (generator(captions.to(device), z).clamp(-1, 1) + 1) / 2   # tanh [-1,1] -> [0,1]
        fid.update(to_u8(fake), real=False)
    # end for
# end with
print(f"standard FID = {fid.compute().item():.2f}")
```

A couple of details that bite people: pass `normalize=False` and feed **uint8** `[0, 255]` (as above), *or* pass `normalize=True` and feed **float** `[0, 1]` — mixing them (uint8 into `normalize=True`) silently corrupts the score. And `FrechetInceptionDistance` resizes to 299×299 internally, so don't pre-resize.

On our model this returns **164.9** — a high number, but the *real* one. And unlike the 1000-d artifact, it behaves like FID should: it falls as the model improves and rises as it degrades, so it is usable for checkpoint selection and ablations.

**Lesson:** the metric object's defaults are part of the metric. If you didn't choose the feature extractor, you don't know what you measured.

## Conclusion / Key Takeaways

1. **The feature space is part of FID.** Confirm you are on the 2048-d `pool3` features; a metric library's *default* extractor is not guaranteed to be the standard one (ignite's default is the 1000-d logits).
2. **A suspiciously tiny FID is a misconfigured extractor, not a great model.** Sanity-check against literature ranges (~3 excellent, tens mediocre) and a real-vs-real control (≈ 0).
3. **Fix the comparison before the extractor.** Generate fakes from the real caption distribution and match input ranges, or the number is invalid no matter which features you use.

## Resources

- **FID** — Heusel et al., *GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium*, NeurIPS 2017 ([arXiv:1706.08500](https://arxiv.org/abs/1706.08500))
- **torchmetrics** — [`FrechetInceptionDistance`](https://lightning.ai/docs/torchmetrics/stable/image/frechet_inception_distance.html) (2048-d pool3 by default)
- **pytorch-ignite** — [`FID` metric](https://pytorch.org/ignite/generated/ignite.metrics.FID.html) and the GAN-evaluation tutorial that builds the custom 2048-d extractor
- **Next in this series** — before interpreting the training curves, map the model being measured: ["MS-CLIP-GAN Architecture: How a CLIP-Guided Multi-Stage GAN Is Wired"]({% post_url 2026-06-18-ms-clip-gan-architecture %}).
