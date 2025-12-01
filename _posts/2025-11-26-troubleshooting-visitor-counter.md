---
title: "Troubleshooting Visitor Counter Integration in Jekyll Chirpy"
date: 2025-11-26 17:00:00 +0900
categories: [Development, Jekyll]
tags: [jekyll, chirpy, visitor-counter, troubleshooting, busuanzi, ci-cd]
author: seoultech
image:
  path: /scitechblog/assets/img/posts/visitor-counter/final-counter.png
  alt: Final Visitor Counter Design
---

## Introduction

After migrating to the Jekyll Chirpy theme, one of the first requested features was a **Visitor Counter**. While it seems like a simple addition, integrating it seamlessly into the theme while maintaining stability and passing CI/CD checks required several iterations of troubleshooting. This post documents that journey.

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

## Problem 2: CI/CD Build Failures

### Symptom
After adding the Busuanzi script, the GitHub Actions deployment workflow failed:

```
HTML-Proofer found errors:
  *  linking to internal hash #busuanzi_value_site_pv
  *  ...
```

### Root Cause
The script was added using a protocol-relative URL:
```html
<script src="//busuanzi.ibruce.info/..."></script>
```
The `htmlproofer` tool used in the CI pipeline (with `--disable-external` flag) was confused by the `//` prefix, potentially treating it as an internal link or failing to validate it properly.

### Solution
We explicitly specified the HTTPS protocol to ensure it's treated as a valid external resource:

```html
<!-- Before -->
<script src="//busuanzi.ibruce.info/..."></script>

<!-- After -->
<script src="https://busuanzi.ibruce.info/..."></script>
```

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

## Problem 4: UX/UI Refinement

### Symptom
The initial design used a simple eye icon (`👁️`) and text, which felt outdated ("not cool") and lacked clarity.

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

## Conclusion

What started as a simple badge addition turned into a lesson in **layout mechanics**, **CI/CD constraints**, and **UI design**. The result is a stable, aesthetically pleasing visitor counter that integrates perfectly with the Chirpy theme's dark mode.

**Key Takeaway:** When modifying a strict theme like Chirpy, always check the underlying Sass for layout constraints and verify your changes against the CI/CD pipeline.
