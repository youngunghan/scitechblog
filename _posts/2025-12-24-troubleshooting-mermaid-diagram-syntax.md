---
title: "[Troubleshooting] Mermaid Diagram Syntax Errors in Markdown PDF Export"
date: 2025-12-24 13:15:00 +0900
categories: [Development, Troubleshooting]
tags: [mermaid, markdown, pdf, vscode, flowchart, html, syntax-error]
description: "Resolving mysterious Mermaid syntax errors caused by HTML tag interpretation in angle brackets."
image:
  path: assets/img/posts/troubleshooting/mermaid_thumbnail.png
  alt: Mermaid Diagram Troubleshooting
author: seoultech
mermaid: true
---

## Introduction

While documenting API test scenarios with Mermaid flowcharts, I encountered a frustrating issue. Some diagrams rendered perfectly, while others showed the dreaded error:

```text
Syntax error in text
mermaid version 11.12.2
```

The bizarre part? The diagrams looked **identical in structure**. This post documents the root causes and solutions for several hidden pitfalls in Mermaid diagram syntax.

## Problem 1: `AND` and `OR` Breaking Edge Labels

### Symptom

I was creating search API diagrams with conditional queries:

```text
flowchart LR
    Tester([Tester])
    API[Search API]
    
    Tester -->|"q=[cond1, AND, cond2]"| API
```

This resulted in a syntax error, while similar diagrams using `IS`, `IN`, `NOT` worked fine:

```text
flowchart LR
    Tester([Tester])
    API[Search API]
    
    Tester -->|"q=[col, IS, val]"| API
```

### Root Cause

This isn't a documented Mermaid feature, so treat the following as an empirical observation rather than a rule. In practice, `AND` and `OR` sitting bare inside an edge label seem to trigger a parsing conflict — likely an interaction with the surrounding brackets and commas in the label text — and even wrapping the label in quotes (`"..."`) doesn't always avoid it.

> Note: `AND` and `OR` are *not* documented reserved operators in Mermaid flowcharts; this is just a workaround for the parsing conflict above. (Mermaid *does* reserve keywords — lowercase `end`, `subgraph`, `graph`, `style`, `class`, `classDef`, `linkStyle`, `click`, etc. — with `end` being the most notorious for silently breaking flowcharts.)
{: .prompt-info }

### Solution

Add underscores around the offending words so they no longer trip the parser:

```markdown
<!-- Before (Error) -->
q=[cond1, AND, cond2]
q=[cond1, OR, cond2]

<!-- After (Works) -->
q=[cond1, _AND_, cond2]  
q=[cond1, _OR_, cond2]   
```

Alternatively, you can use symbols like `+` and `/`:

```markdown
q=cond1 + cond2   <!-- AND -->
q=cond1 / cond2   <!-- OR -->
```

The most portable fix, though, is to rephrase the whole edge label so the operator words never appear (e.g. `q: cond1 + cond2` or `q: all conditions`).

**Lesson:** Bare `AND`/`OR` inside an edge label can trip Mermaid's parser — rephrase the label or wrap the words (`_AND_`, or symbols `+`/`/`) so the operator words never appear raw.

## Problem 2: Angle Brackets Interpreted as HTML Tags

### Symptom

Some response messages with angle brackets failed:

```text
flowchart LR
    A[API]
    T([Tester])
    
    A -.->|"200(rows=<row>)"| T
    A -.->|"200(rows=<unchanged>)"| T
```

But these worked:

```text
flowchart LR
    A[API]
    T([Tester])
    
    A -.->|"200(rows=<1개>)"| T
    A -.->|"200(rows=<원래값>)"| T
```

### Root Cause Analysis

| Pattern | Result | Reason |
|---------|--------|--------|
| `<row>` |  Error | Looks like HTML `<row>` tag |
| `<unchanged>` |  Error | Looks like HTML `<unchanged>` tag |
| `<1개>` |  Works | Contains number, not a valid tag |
| `<원래값>` |  Works | Contains Korean, not a valid tag |

The Markdown PDF exporter (or underlying HTML renderer) interprets **English-only content in angle brackets** as potential HTML tags, breaking the Mermaid parser.

### Solution

The recommended general fix is to stop the renderer from seeing the angle brackets as a tag in the first place. There are three robust approaches, in order of preference:

1. **Escape the brackets as HTML entities** — replace `<` with `&lt;` and `>` with `&gt;` so they render as literal characters. This works because our Markdown-PDF/Puppeteer pipeline decodes the HTML entity before rendering; note that Mermaid's *own* [flowchart docs](https://mermaid.js.org/syntax/flowchart.html) escape special characters with `#`-prefixed codes (e.g. `#lt;`/`#gt;`), not `&`-entities:

   ```markdown
   <!-- Before (Error) -->
   rows=<row>
   rows=<unchanged>

   <!-- After (Works) -->
   rows=&lt;row&gt;
   rows=&lt;unchanged&gt;
   ```

2. **Wrap/quote the label text** so the brackets stay inside a quoted string, e.g. `|"200(rows=&lt;row&gt;)"|`, keeping the quotes already used in these edge labels.

3. **Remove the angle brackets** entirely if they are purely decorative, e.g. `rows=row` or `rows=[row]`.

As a secondary quick hack, you can also break the HTML tag pattern by adding a non-English character (Korean, a number, or a symbol) so the content no longer looks like a valid tag:

```markdown
<!-- Quick hack -->
rows=<해당row>
rows=<변경없음>
```

This works because the renderer only treats English-only content between `<` and `>` as a potential tag, but escaping is the more portable fix.

**Lesson:** An HTML-based renderer reads `<english>` in a label as a tag — escape the brackets as `&lt;`/`&gt;` (the portable fix); adding a Korean character or number is only a quick hack.

## Problem 3: The Infamous `<meta>` Tag

### Symptom

This diagram consistently failed in my Markdown-PDF (Puppeteer/HTML) export pipeline, even with Korean characters nearby:

```text
flowchart LR
    ML[Meta Listing API]
    T([Tester])
    
    ML -.->|"200(rows=<meta값유지>)"| T
```

### Root Cause

`<meta>` is a **valid HTML tag**! 

```html
<meta charset="UTF-8">
```

Even though `<meta값유지>` contains Korean, the parser sees `<meta` and interprets it as the start of an HTML meta tag, causing a parsing failure.

### Solution

Because `<meta>` is a real tag, the Korean-character trick alone won't save you here — `<meta값유지>` still starts with `<meta`. Escape the brackets instead:

```markdown
<!-- Before (Error) -->
rows=<meta값유지>

<!-- After (Works) -->
rows=&lt;meta값유지&gt;
```

As a secondary quick hack, you can rename the token so the literal string `meta` no longer appears right after `<`, for example using its Korean equivalent:

```markdown
<!-- Quick hack -->
rows=<메타값유지>
```

**Lesson:** For a real HTML tag name (`<meta>`, `<div>`, `<span>`), the non-English trick fails — the parser keys on the leading tag name, so always escape (`&lt;meta&gt;`).

## Summary: Mermaid + HTML Parsing Gotchas

| Issue | Trigger | Solution |
|-------|---------|----------|
| Edge-label parsing conflict | `AND`, `OR` in message labels | Use `+`, `/` or `_AND_`, `_OR_` |
| HTML Tag Interpretation | `<english>` patterns | Escape as `&lt;row&gt;`, quote the label, or drop the brackets (quick hack: add Korean/numbers, `<한글english>`) |
| Actual HTML Tags | `<meta>`, `<div>`, `<span>`, etc. | Escape as `&lt;meta&gt;` (quick hack: rename, e.g. `<메타>`) |

## Conclusion

Mermaid is powerful for documentation, but its integration with HTML-based renderers (like VS Code's Markdown PDF extension) introduces hidden parsing conflicts.

**Key Takeaways:**
1. Avoid bare `AND`/`OR` inside message labels (they aren't reserved words — Mermaid's reserved keywords are `end`, `subgraph`, `graph`, `style`, `class`, etc. — but the bare tokens still trip the parser).
2. For angle brackets in labels, escape them as HTML entities (`&lt;row&gt;`), keep the label quoted, or remove the brackets — the entity escape is what works in our Markdown-PDF/Puppeteer pipeline. (Mermaid's own [flowchart docs](https://mermaid.js.org/syntax/flowchart.html) escape special characters with `#`-prefixed codes like `#lt;`/`#gt;`, not `&`-entities.)
3. Be especially careful with real HTML tag names like `<meta>`, `<div>`, `<span>`; escaping handles these too.

When in doubt, escape the brackets. As a quick hack you can add a Korean character or number to break the pattern, but `&lt;`/`&gt;` is the more reliable fix.
