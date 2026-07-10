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
The original incident record does **not** establish the root cause. Jekyll does hide future-dated posts by default, so I initially suspected the front matter date:
```yaml
date: 2025-11-26 ...
```

However, the recorded timestamp was already in the past relative to the relevant build, and the Git history shows the post working after the year was restored to 2025. That evidence does not support a future-date diagnosis. The actual cause could have been an earlier unrecorded front matter state, build cache, branch mismatch, filename/date parsing, or another transient deployment condition.

### Solution
The durable fix is a diagnostic sequence rather than changing the year until the post appears:

```bash
bundle exec jekyll build --trace
bundle exec jekyll doctor
bundle exec jekyll console
# In the console: site.posts.docs.map { |post| [post.date, post.path] }
```

Check the build's branch and commit, YAML parsing, `_posts/YYYY-MM-DD-...` filename, `date` with timezone, `published`/`hidden` flags, and whether `--future` changes the result. Clear `.jekyll-cache` only after preserving the failing state and logs.

**Lesson:** Jekyll's future-date rule is a useful check, not a root cause without timestamp evidence. Record the failing build commit and inspect `site.posts` before assigning causality.

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

## Problem 3: Broken Menu Links in the Legacy WENIVLOG Site

### Symptom
Before the migration was complete, the **WENIVLOG** sidebar menu items (Categories, Tags) stopped working and led to 404 pages. This incident belongs to the legacy source site, not to Chirpy's current navigation implementation.

### Root Cause
This was a classic **regression** in the old WENIVLOG configuration.
1.  We initially fixed paths in WENIVLOG's `local_blogMenu.json` to include its GitHub Pages repository prefix.
2.  During an unrelated rollback, that JSON file reverted to root-relative paths.
3.  A project site hosted below `username.github.io/repo-name` then resolved those paths against the domain root instead of the project subpath.

The current Chirpy repository has no `local_blogMenu.json`. Chirpy builds its sidebar from `_tabs/` front matter and the site's `baseurl`, so searching this repository's history for that legacy JSON fix will not find it.

### Historical Solution
For the WENIVLOG deployment, I re-applied the repository prefix in its JSON configuration:

**Before (broken):**

```json
{ "url": "/categories/" }
```

**After (fixed in WENIVLOG):**

```json
{ "url": "/scitechblog/categories/" }
```

For Jekyll/Chirpy, do not reproduce this with hard-coded JSON links. Set `url` and `baseurl` in `_config.yml`, keep navigation pages in `_tabs/`, and use Jekyll's `relative_url` filter for custom internal links when a template does not already handle the base URL:

{% raw %}
```liquid
{{ '/categories/' | relative_url }}
```
{% endraw %}

**Lesson:** Project-site URLs need base-path-aware generation. The JSON edit was a WENIVLOG-era fix; Chirpy should derive the prefix from `baseurl`.

## Conclusion

Building a polished tech blog is an iterative process — "it works on my machine" is rarely the end of the story. Key takeaways:

1. **Content visibility**: future-dated posts silently vanish — check `date` and `timezone` (or set `future: true`).
2. **Layout**: use CSS/flexbox (not Markdown) for multi-image rows like badges.
3. **Regressions**: distinguish fixes in the legacy platform from the current implementation, and generate subpath-aware URLs from one `baseurl` setting.
