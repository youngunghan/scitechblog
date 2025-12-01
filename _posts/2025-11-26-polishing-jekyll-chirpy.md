---
title: "Polishing Jekyll Chirpy: Fixing UI Glitches and Content Visibility"
date: 2025-11-26 18:00:00 +0900
categories: [Development, Jekyll]
tags: [jekyll, chirpy, troubleshooting, ui-ux, markdown]
author: seoultech
image:
  path: /scitechblog/assets/img/posts/polishing/badges-fix.png
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
*Tip: Always double-check your `date` field and the `timezone` setting in `_config.yml`.*

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

```html
<img src="..." alt="Python"/>
&nbsp;
<img src="..." alt="C"/>
```

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

## Conclusion

Building a polished tech blog is an iterative process. "It works on my machine" is rarely the end of the story. These small fixes—ensuring content visibility, refining layout, and managing regressions—are what separate a template from a professional-looking site.
