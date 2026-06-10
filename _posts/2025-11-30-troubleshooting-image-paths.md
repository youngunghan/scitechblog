---
title: "[Troubleshooting] Jekyll Blog Image Path & HTMLProofer Errors (Double Baseurl)"
date: 2025-11-30 11:30:00 +0900
categories: [Blogging, Troubleshooting]
tags: [jekyll, chirpy, htmlproofer, github-pages, ci-cd]
description: "Resolving the 'internal image does not exist' error caused by double baseurl duplication in Jekyll Chirpy theme."
image:
  path: assets/img/posts/troubleshooting/thumbnail.png
  alt: Troubleshooting Log
---

## Introduction

While migrating my algorithm solutions to this Jekyll (Chirpy theme) blog, I encountered a persistent error in the CI/CD pipeline. `htmlproofer`, which checks for broken links and images, kept failing with a strange error:

```text
internal image /scitechblog/scitechblog/assets/img/posts/algo/leetcode.png does not exist
```

Notice the **double baseurl** (`/scitechblog/scitechblog/`). This post documents the troubleshooting process, the root cause, and the solution.

> **Environment:** Jekyll 4.3 · jekyll-theme-chirpy 7.4 · html-proofer 5.0 · Ruby 3.3 (this blog's pinned GitHub Pages build). The exact path behavior is tied to the theme/`baseurl` handling in these versions.
{: .prompt-info }

## The Problem

My blog is hosted on GitHub Pages with a project url: `https://youngunghan.github.io/scitechblog`.
Therefore, the `baseurl` is set to `/scitechblog` in `_config.yml`.

When I added images to my posts, I initially tried two approaches:

1.  **Absolute Path in Markdown**: `path: /scitechblog/assets/img/...`
2.  **Relative Path + HTML Logic**: `path: /assets/img/...` and using `relative_url` filter in Liquid.

Both approaches resulted in the same error: **Double Baseurl**.
The generated HTML looked like this:
`<img src="/scitechblog/scitechblog/assets/img/..." ...>`

This meant that the `baseurl` was effectively being applied twice: the path already carried `/scitechblog`, and then it was prepended a second time. In other words, the duplication came from *also* adding `baseurl` manually to a path that already included it.

## Root Cause Analysis

I investigated the `_layouts/home.html` file, which renders the post previews.

```liquid
<!-- _layouts/home.html (Simplified) -->
{% assign src = post.image.path %}
<img src="{{ src }}" ...>
```

At first glance, it looks like raw output. However, the Jekyll Chirpy theme (and its plugins) has hidden logic to handle asset paths.

First, a note on how this is *supposed* to work. Per the [Jekyll filters docs](https://jekyllrb.com/docs/liquid/filters/), the `relative_url` filter **prepends `baseurl` to the input path**. On a GitHub Pages subpath site like this one, `{{ path | relative_url }}` is the standard, correct way to build asset URLs — you give it a root-relative path and it adds `/scitechblog` for you. So `relative_url` is not the villain here; the problem is supplying it (or the theme's own path handling) a path that *already* contains `baseurl`.

1.  **Theme Logic**: The theme already builds asset URLs with `baseurl` prepended.
2.  **Conflict**: When I manually added `/scitechblog` in the Markdown front matter, the path already carried the `baseurl`. When the theme then prepended `baseurl` again, the result was `/scitechblog/scitechblog/...`.
3.  **Double application**: The same thing happens if you run `relative_url` on a path that already starts with `baseurl` — it is correct on a clean root-relative path, but doubles up when the input already includes `/scitechblog`.

## The Solution

The solution was counter-intuitive: **Do less.**

I reverted all my "fixes" in the HTML and Markdown files.

### 1. Revert HTML
I restored `_layouts/home.html` to its original state, removing any `relative_url` filters or manual `baseurl` appending logic.

### 2. Clean Markdown Paths
I updated all Markdown files to use **relative paths without a leading slash**:

```yaml
image:
  path: assets/img/posts/algo/leetcode.png
```

### 3. Layout Adjustment (Fork-Specific Workaround)
However, simply using relative paths caused issues on pagination pages (e.g., `/page2/`) with my forked layout. In my fork's `_layouts/home.html`, the path handling only added `baseurl` cleanly when the input was a leading-slash, root-relative path.

So, scoped to *this* layout, I reverted the manual `baseurl` and instead forced a leading-slash path in my forked `_layouts/home.html`:

```liquid
<!-- _layouts/home.html -->
{% assign src = '/' | append: src | replace: '//', '/' %}
<img src="{{ src }}" ...>
```

This normalizes the input to `/assets/img/...`, after which the layout's path handling prepends `/scitechblog` once, giving the correct `/scitechblog/assets/img/...`.

Note this is a workaround for my particular fork's layout/plugin combination, not a general Jekyll rule. The canonical approach on a subpath site is still to feed a clean root-relative path to `relative_url` (`{{ src | relative_url }}`) and let it add `baseurl` — exactly once.

## Comparison: Original vs. Fork

I created this blog by forking [jekyll-theme-chirpy](https://github.com/cotes2020/jekyll-theme-chirpy).

-   **Original Repo**: Designed to be generic. It expects users to follow standard Jekyll conventions (relative paths for assets).
-   **My Fork**: In my attempt to customize and "fix" things for my specific `baseurl`, I broke the standard behavior.

**Key Takeaway**: When using a robust theme like Chirpy, trust its default behavior first. Manually forcing paths often leads to conflicts with built-in plugins.

## Conclusion

If you encounter "double baseurl" errors in Jekyll:
1.  Check if you are manually adding `baseurl` in Markdown.
2.  Remember `relative_url` is correct — it prepends `baseurl` for you. The bug is applying it (or any baseurl logic) to a path that *already* includes `baseurl`.
3.  Feed a single clean root-relative path to `relative_url` and let it add `baseurl` exactly once.

Now, my CI/CD pipeline passes with **0 errors** (at the time of this fix)!
