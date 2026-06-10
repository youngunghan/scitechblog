---
title: "Troubleshooting Visitor Counter Integration in Jekyll Chirpy"
description: "Integrating a Busuanzi visitor counter into Jekyll Chirpy and getting it past CI/CD checks."
date: 2025-11-26 17:00:00 +0900
categories: [Development, Jekyll]
tags: [jekyll, chirpy, visitor-counter, troubleshooting, busuanzi, ci-cd]
author: seoultech
image:
  path: assets/img/posts/visitor-counter/final-counter.png
  alt: Final Visitor Counter Design
---

## Introduction

After migrating to the Jekyll Chirpy theme, one of the first requested features was a **Visitor Counter**. While it seems like a simple addition, integrating it seamlessly into the theme while maintaining stability and passing CI/CD checks required several iterations of troubleshooting. This post documents that journey.

> **Environment:** Jekyll 4.3 · jekyll-theme-chirpy 7.4 · html-proofer 5.0 · Ruby 3.3 (this blog's pinned GitHub Pages build). Busuanzi itself is an external, unversioned hosted script.
{: .prompt-info }

## Problem 1: The Instability of Image-based Badges

### Symptom
Initially, we attempted to use **Hits** (hits.seeyoufarm.com), a popular image-based badge service. However, we frequently encountered:
- Broken image icons
- DNS resolution errors (`DNS_PROBE_FINISHED_NXDOMAIN`)
- Slow loading times

### Root Cause
Image-based counters rely entirely on the uptime of the external service. If the service goes down or has DNS issues, the badge breaks, making the blog look unprofessional.

### Solution
We switched to **Busuanzi (不蒜子)**, a lightweight script-based visitor counter.
- **Pros:** More reliable, text-based (allows custom styling), and widely used in static blogs.
- **Cons:** Does not support "Today/Yesterday" views reliably in the stable version, so we focused on "Total Views".

> **Caveat:** Busuanzi is an external third-party script, so it carries the usual privacy and availability trade-offs. Every page load calls out to a service you don't control, which can go down, slow your page, or be blocked in some networks, and visitor data passes through that third party. If those concerns matter to you, consider self-hosting the counter or using a privacy-friendly analytics option instead.
{: .prompt-warning }

**Lesson:** An image-badge counter is only as reliable as the service hosting it — a script-based (or self-hosted) counter avoids broken-image/DNS failures, at the cost of one external script call.

## Problem 2: CI/CD Build Failures

### Symptom
After adding the Busuanzi script, the GitHub Actions deployment workflow failed. HTML-Proofer reported two distinct problems:

```
HTML-Proofer found errors:
  *  linking to internal hash #busuanzi_value_site_pv
  *  ...
```

The two symptoms were:
1. **Internal hash error:** Our markup contained an anchor that linked to `#busuanzi_value_site_pv`, but that ID only exists on the `<span>` element that Busuanzi populates at runtime. Since the value is injected client-side by the script, the element is empty (and effectively absent) in the static HTML that HTML-Proofer scans, so it flagged the hash as a broken internal link.
2. **Protocol-relative script URL:** The script was added using a protocol-relative URL, which the proofer failed to validate.

### Root Cause
The underlying issue causing the protocol-relative warning was the `//` prefix on the script source:
```html
<script src="//busuanzi.ibruce.info/..."></script>
```
The `htmlproofer` tool used in the CI pipeline (with the `--disable-external` flag) does not treat the `//` prefix as an external URL to skip; instead it fails to validate it properly. Separately, we resolved the internal hash error by removing the explicit anchor link to the runtime-populated `#busuanzi_value_site_pv` element.

### Solution
We explicitly specified the HTTPS protocol to ensure it's treated as a valid external resource:

```html
<!-- Before -->
<script src="//busuanzi.ibruce.info/..."></script>

<!-- After -->
<script src="https://busuanzi.ibruce.info/..."></script>
```

**Lesson:** Don't link to IDs that a script injects at runtime (they're absent in the static HTML htmlproofer scans), and give htmlproofer explicit `https://` URLs — under `--disable-external` it doesn't skip protocol-relative (`//`) links.

## Problem 3: Centering Elements in Asymmetric Containers

### Symptom
When we placed the visitor counter in the sidebar footer (`.sidebar-bottom`), it appeared slightly off-center to the right.

### Root Cause
Inspecting the `_sass/layout/_sidebar.scss` file revealed asymmetric padding in the container:

```scss
.sidebar-bottom {
  padding-left: 2rem;   // Left padding is larger
  padding-right: 1rem;
}
```
This design is intentional for the alignment of the mode toggle and social icons, but it breaks the centering of a full-width element like our counter.

### Solution
We moved the visitor counter **outside** of the `.sidebar-bottom` container and applied Flexbox centering directly:

```html
<div class="w-100 d-flex justify-content-center mb-2">
  <!-- Counter Content -->
</div>

<div class="sidebar-bottom ...">
  <!-- Mode Toggle & Social Icons -->
</div>
```

**Lesson:** A theme container can have intentional asymmetric padding — to center a full-width element, move it out of that container and apply your own flex centering.

## Problem 4: UX/UI Refinement

### Symptom
The initial design used a simple eye icon (``) and text, which felt outdated ("not cool") and lacked clarity.

### Solution
We modernized the design using **Glassmorphism** and clear labeling:

1.  **Pill Design:** Rounded corners (`border-radius: 12px`) with a semi-transparent background.
2.  **Visuals:** Replaced the eye icon with a chart line icon (`fas fa-chart-line`) for a more analytical feel.
3.  **Simplification:** Removed the "Total Visitors" (UV) count to focus solely on "Total Views" (PV), reducing clutter.

**Final Code Snippet:**
```html
<div id="busuanzi_container_site_pv" style="...">
  <i class="fas fa-chart-line" style="color: #2d9da8;"></i>
  <span style="opacity: 0.8;">Total Views</span>
  <span id="busuanzi_value_site_pv" class="fw-bold" style="color: #2d9da8;"></span>
</div>
```

**Lesson:** Show one clear metric (Total Views) with a legible label and icon rather than several competing counters — less clutter, clearer signal.

## Conclusion

What started as a simple badge addition turned into a lesson in **layout mechanics**, **CI/CD constraints**, and **UI design**. The result is a stable, aesthetically pleasing visitor counter that integrates cleanly with the Chirpy theme's dark mode.

**Key Takeaway:** When modifying a strict theme like Chirpy, always check the underlying Sass for layout constraints and verify your changes against the CI/CD pipeline.
