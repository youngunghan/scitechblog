---
title: "[Troubleshooting] Fixing Broken LaTeX Rendering in Jekyll Chirpy"
date: 2025-12-01 16:30:00 +0900
categories: [Blogging, Troubleshooting]
tags: [jekyll, chirpy, latex, mathjax, automation, python]
description: "Resolving the issue where MathJax formulas display as raw text by automating the front matter configuration."
image:
  path: assets/img/posts/troubleshooting/latex_thumbnail.png
  alt: LaTeX Rendering Issue Thumbnail
math: true
---

## Introduction

After migrating my algorithm posts to Jekyll Chirpy, I noticed a glaring issue. Complex mathematical formulas, which are essential for explaining time complexity like $O(N \log N)$ or recurrence relations, were displaying as **raw text**.

Instead of a beautifully rendered formula, I saw:
`$O(N \log N)$`

This post documents why this happened and how I automated the fix for over 30 posts using a Python script.

## The Problem

I use LaTeX syntax (wrapped in `$`) for mathematical expressions in my Markdown files. 
For example:

```markdown
The time complexity is $O(N \log N)$.
```

I expected the theme to automatically render this using **MathJax** or **KaTeX**. However, it rendered literally as `$O(N \log N)$`.

## Root Cause Analysis

The Jekyll Chirpy theme is optimized for performance. To avoid loading heavy JavaScript libraries like MathJax on every page, it only loads them **on demand**.

The trigger for loading MathJax is a specific variable in the **Front Matter**:

```yaml
---
title: "My Post"
math: true  # <--- This was missing!
---
```

Since my migrated posts didn't have this line, the theme assumed they were plain text posts and didn't load the math rendering engine.

## The Solution

The manual fix is simple: add `math: true` to the front matter of every post containing math.
However, I have dozens of algorithm posts. Doing this manually is tedious and error-prone.

### Automation with Python

I wrote a Python script to:
1.  Scan all Markdown files in `_posts/`.
2.  Detect if they contain LaTeX delimiters (`$`, `\(`, `\[`).
3.  Check if `math: true` is missing.
4.  Automatically insert `math: true` into the front matter.

Here is the script `enable_math.py`:

```python
import glob
import re

def enable_math_in_files():
    # Find all markdown files in _posts
    files = glob.glob("_posts/*.md")
    
    for file_path in files:
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Check if file contains math delimiters
        if not ("$" in content or "\\(" in content or "\\[" in content):
            continue
            
        # Check if math: true is already present
        if "math: true" in content:
            continue
            
        # Insert math: true before the second ---
        match = re.search(r'^---\s*$', content, re.MULTILINE) # First ---
        if match:
            end_match = re.search(r'^---\s*$', content[match.end():], re.MULTILINE) # Second ---
            if end_match:
                insert_pos = match.end() + end_match.start()
                
                new_content = content[:insert_pos] + "math: true\n" + content[insert_pos:]
                
                with open(file_path, 'w') as f:
                    f.write(new_content)
                print(f"Enabled math in {file_path}")

if __name__ == "__main__":
    enable_math_in_files()
```

### Result

Running this script instantly fixed 13 posts that were missing the configuration, including:
- `[BOJ] 11401. 이항 계수 3` (Heavy math content)
- `[BOJ] 1920. 수 찾기` (Time complexity analysis)

Now, $O(N \log N)$ renders perfectly!

## Conclusion

If your LaTeX formulas aren't rendering in Jekyll Chirpy:
1.  Check if `math: true` is in your Front Matter.
2.  Don't waste time editing files manually—script it!

This small automation saved me a lot of repetitive work and ensured no post was left behind.
