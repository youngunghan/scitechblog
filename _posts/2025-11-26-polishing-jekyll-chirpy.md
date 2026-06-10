---
title: "Polishing Jekyll Chirpy: Fixing UI Glitches and Content Visibility"
description: "Fixing small UI glitches and content-visibility issues while polishing a Jekyll Chirpy blog."
date: 2025-11-26 18:00:00 +0900
categories: [Development, Jekyll]
tags: [jekyll, chirpy, troubleshooting, ui-ux, markdown]
author: seoultech
image:
  path: assets/img/posts/polishing/badges-fix.png
  alt: Badge Layout Fix
---

## Introduction

Beyond the major migration tasks and the visitor counter saga, refining a blog involves solving numerous small but annoying issues. This post details three specific "polishing" problems encountered during the setup of this blog and how they were resolved.

## Problem 1: The "Missing" Blog Post

### Symptom
After writing a detailed migration guide, I pushed the changes to GitHub. The build passed, but the post simply **refused to appear** on the homepage or in the archives. It was as if the file didn't exist.

### Root Cause
Jekyll has a default behavior regarding **future-dated posts**.
The post's front matter had:
```yaml
date: 2025-11-26 ...
```
At the time of deployment, the server time (UTC) or the configured timezone (`Asia/Seoul`) might have been slightly behind this timestamp. Jekyll filters out posts with dates in the future unless explicitly configured otherwise (`future: true`).

### Solution
I corrected the date to ensure it was in the past relative to the build time.

**Lesson:** Jekyll hides future-dated posts by default — keep `date` in the past relative to build time (mind UTC vs your `timezone` in `_config.yml`), or set `future: true`.

## Problem 2: Overlapping Badges in "About" Page

### Symptom
In the "About" page, I wanted to display a row of technical proficiency badges (Shields.io).
Using standard Markdown syntax:
```markdown
![Python](...) ![C](...)
```
Resulted in badges that were either:
- Squashed together with no spacing
- Wrapped unpredictably
- Overlapping vertically on smaller screens

### Root Cause
Markdown's image handling is often too simplistic for complex layouts. It wraps images in paragraph tags but doesn't provide fine-grained control over margins or vertical alignment.

### Solution
I switched to raw HTML to control the layout precisely:
1.  Used `<img>` tags instead of Markdown syntax.
2.  Added non-breaking spaces (`&nbsp;`) for consistent horizontal spacing.
3.  Wrapped them in a `<div>` or `<p>` with specific alignment classes if needed.

**Quick fix:** chain non-breaking spaces between the images.

```html
<img src="..." alt="Python"/>
&nbsp;
<img src="..." alt="C"/>
```

**Recommended:** wrap the badges in a flex container and control spacing with CSS `gap`. This is more consistent and responsive than chaining `&nbsp;`.

```html
<div class="badge-row">
  <img src="..." alt="Python"/>
  <img src="..." alt="C"/>
</div>
```

```css
.badge-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}
```

*Note: Chaining `&nbsp;` works as a quick fix, but CSS/flexbox (e.g. a flex container with `gap`) or Shields.io's own spacing options are generally preferable for consistent, responsive layout.*

**Lesson:** Markdown can't control image layout — for a badge row use a flex container with CSS `gap`; chaining `&nbsp;` is only a quick fix.

## Problem 3: The Broken Menu Links (Regression)

### Symptom
Suddenly, the sidebar menu items (Categories, Tags) stopped working, leading to 404 errors or broken pages.

### Root Cause
This was a classic **regression**.
1.  We initially fixed the paths in `local_blogMenu.json` to include the repository name (`/scitechblog/`).
2.  During a troubleshooting rollback for another issue, this JSON file was reverted to its original state (without the repo name).
3.  The site, hosted on a subpath (`username.github.io/repo-name`), couldn't find the resources at the root path.

### Solution
Re-applied the path fix to the JSON configuration:
```json
// Before (Broken)
"url": "/categories/"

// After (Fixed)
"url": "/scitechblog/categories/"
```

**Lesson:** On a project-subpath GitHub Pages site, resource URLs must include the repo prefix (`/scitechblog/...`); guard config files like this against being reverted during unrelated rollbacks.

## Conclusion

Building a polished tech blog is an iterative process — "it works on my machine" is rarely the end of the story. Key takeaways:

1. **Content visibility**: future-dated posts silently vanish — check `date` and `timezone` (or set `future: true`).
2. **Layout**: use CSS/flexbox (not Markdown) for multi-image rows like badges.
3. **Regressions**: subpath sites need the repo prefix in resource URLs — protect those fixes from unrelated rollbacks.
