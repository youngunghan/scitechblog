---
title: "[Troubleshooting] Jekyll Blog Image Path & HTMLProofer Errors (Double Baseurl)"
date: 2025-12-01 11:30:00 +0900
categories: [Blogging, Troubleshooting]
tags: [jekyll, chirpy, htmlproofer, github-pages, ci-cd]
description: "Resolving the 'internal image does not exist' error caused by double baseurl duplication in Jekyll Chirpy theme."
image:
  path: assets/img/posts/visitor-counter/final-counter.png
  alt: Troubleshooting Log
---

## Introduction

While migrating my algorithm solutions to this Jekyll (Chirpy theme) blog, I encountered a persistent error in the CI/CD pipeline. `htmlproofer`, which checks for broken links and images, kept failing with a strange error:

```text
internal image /scitechblog/scitechblog/assets/img/posts/algo/leetcode.png does not exist
```

Notice the **double baseurl** (`/scitechblog/scitechblog/`). This post documents the troubleshooting process, the root cause, and the solution.

## The Problem

My blog is hosted on GitHub Pages with a project url: `https://youngunghan.github.io/scitechblog`.
Therefore, the `baseurl` is set to `/scitechblog` in `_config.yml`.

When I added images to my posts, I initially tried two approaches:

1.  **Absolute Path in Markdown**: `path: /scitechblog/assets/img/...`
2.  **Relative Path + HTML Logic**: `path: /assets/img/...` and using `relative_url` filter in Liquid.

Both approaches resulted in the same error: **Double Baseurl**.
The generated HTML looked like this:
`<img src="/scitechblog/scitechblog/assets/img/..." ...>`

This meant that *something* was prepending the `baseurl` automatically, and my manual attempts were adding it a second time.

## Root Cause Analysis

I investigated the `_layouts/home.html` file, which renders the post previews.

```liquid
<!-- _layouts/home.html (Simplified) -->
{% assign src = post.image.path %}
<img src="{{ src }}" ...>
```

At first glance, it looks like raw output. However, the Jekyll Chirpy theme (and its plugins) has hidden logic to handle asset paths.

1.  **Theme Logic**: The theme is designed to handle `assets/img/...` paths automatically.
2.  **Conflict**: When I manually added `/scitechblog` in the Markdown front matter, the theme *still* prepended the `baseurl`, resulting in `/scitechblog/scitechblog/...`.
3.  **HTML Modification**: Even when I tried to fix it in HTML using `relative_url` filter, it conflicted with the theme's internal processing (likely via `jekyll-relative-links` or similar plugins).

## The Solution

The solution was counter-intuitive: **Do less.**

I reverted all my "fixes" in the HTML and Markdown files.

### 1. Revert HTML
I restored `_layouts/home.html` to its original state, removing any `relative_url` filters or manual `baseurl` appending logic.

### 2. Clean Markdown Paths
I updated all Markdown files to use **relative paths without a leading slash**:

```yaml
# BEFORE (Wrong)
image:
  path: /scitechblog/assets/img/posts/algo/leetcode.png

# AFTER (Correct)
image:
  path: assets/img/posts/algo/leetcode.png
```

By using `assets/img/...`, I allowed the theme to correctly resolve the path to `/scitechblog/assets/img/...` during the build process.

## Comparison: Original vs. Fork

I created this blog by forking [jekyll-theme-chirpy](https://github.com/cotes2020/jekyll-theme-chirpy).

-   **Original Repo**: Designed to be generic. It expects users to follow standard Jekyll conventions (relative paths for assets).
-   **My Fork**: In my attempt to customize and "fix" things for my specific `baseurl`, I broke the standard behavior.

**Key Takeaway**: When using a robust theme like Chirpy, trust its default behavior first. Manually forcing paths often leads to conflicts with built-in plugins.

## Conclusion

If you encounter "double baseurl" errors in Jekyll:
1.  Check if you are manually adding `baseurl` in Markdown.
2.  Check if you are using `relative_url` filter on a path that already has `baseurl`.
3.  Try using simple relative paths (`assets/...`) and let Jekyll handle the rest.

Now, my CI/CD pipeline passes with **0 errors**!
