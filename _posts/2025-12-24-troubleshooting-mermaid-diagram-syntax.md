---
title: "[Troubleshooting] Mermaid Diagram Syntax Errors in Markdown PDF Export"
date: 2025-12-24 13:15:00 +0900
categories: [Development, Troubleshooting]
tags: [mermaid, markdown, pdf, vscode, flowchart, html, syntax-error]
description: "Diagnosing exporter-specific Mermaid errors by separating Mermaid grammar, edge-label syntax, HTML-like text, and Markdown/PDF preprocessing."
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

The diagrams looked nearly identical. A later re-check also showed why troubleshooting notes must distinguish an observed workaround from a proven parser rule: several inputs that failed in that Markdown-PDF setup parse successfully in a current Mermaid renderer.

## Problem 1: Do Not Blame `AND` / `OR` Without a Minimal Reproduction

### Symptom

I was creating search API diagrams with conditional queries. A solid edge rendered, but a similarly labeled dotted edge failed in the PDF export:

```text
flowchart LR
    Tester([Tester])
    API[Search API]
    
    Tester -->|"q=[cond1, AND, cond2]"| API
    API -.->|"200(rows=row)"| Tester
```

The tempting conclusion was that `AND` caused the failure. That conclusion does not survive re-testing: `AND` and `OR` are ordinary quoted label text, and both lines above parse in a current Mermaid renderer. The dotted form combines `-.->` with a pipe label, which current Mermaid also accepts.

### Root Cause

Mermaid's documentation presents these canonical forms for text on solid and dotted links:

```text
flowchart LR
    A -->|"solid label"| B
    B -. "dotted label" .-> C
```

### Solution

For a portable minimal reproduction, keep the query text quoted and normalize the dotted link to the documented form:

```text
flowchart LR
    Tester([Tester])
    API[Search API]

    Tester -->|"q=[cond1, AND, cond2]"| API
    API -. "200(rows=row)" .-> Tester
```

Lowercase `end` is a documented flowchart hazard, but `AND` and `OR` are not reserved flowchart operators. If both the original and normalized snippets render in Mermaid Live/current Mermaid but only one fails in PDF export, the remaining suspect is the extension's bundled Mermaid version or its Markdown/HTML preprocessing. Record those versions before calling the issue a Mermaid grammar bug.

**Lesson:** Use `A -. "label" .-> B` as the documented diagnostic form, but do not claim the alternative arrow or ordinary label words are invalid when a current parser accepts them.

## Problem 2: Angle Brackets Interpreted as HTML Tags

### Symptom

Some response messages with angle brackets failed:

```text
flowchart LR
    A[API]
    T([Tester])
    
    A -. "200(rows=<row>)" .-> T
    A -. "200(rows=<unchanged>)" .-> T
```

### Root Cause Analysis

Angle brackets pass through three layers here: Markdown, Mermaid, and the exporter's HTML renderer. Current Mermaid accepts the quoted `<row>` example, so the historical failure is not enough to establish a Mermaid grammar rule. A Markdown/PDF wrapper can still transform or sanitize HTML-like label content before Mermaid receives it. Whether Korean or a number happened to make one example render was exporter-specific behavior, not a portable parsing rule.

### Solution

The recommended general fix is to stop the renderer from seeing literal angle brackets. There are two robust approaches:

1. **Use Mermaid's entity-code form** — replace `<` with `#lt;` and `>` with `#gt;`, following the [flowchart documentation](https://mermaid.js.org/syntax/flowchart.html):

   ```text
   <!-- Before (Error) -->
   rows=<row>
   rows=<unchanged>

   <!-- After (Works) -->
   rows=#lt;row#gt;
   rows=#lt;unchanged#gt;
   ```

2. **Remove the angle brackets** if they are only notation, for example `rows=row` or `rows=[row]`.

Keep the complete edge label quoted as well: `A -. "200(rows=#lt;row#gt;)" .-> T`. Quoting protects spaces and punctuation; entity codes protect the angle brackets. They solve different parts of the parse.

**Lesson:** Do not rely on character-language tricks. Quote the label and encode literal angle brackets with Mermaid entity codes, or remove the brackets.

## Problem 3: The Infamous `<meta>` Tag

### Symptom

This diagram consistently failed in my Markdown-PDF (Puppeteer/HTML) export pipeline, even with Korean characters nearby:

```text
flowchart LR
    ML[Meta Listing API]
    T([Tester])
    
    ML -. "200(rows=<meta-value>)" .-> T
```

### Root Cause

`meta` is also an HTML tag name. A current Mermaid parser accepts the quoted example, but an HTML-preprocessing path may still interpret `<meta...>` as markup before Mermaid sees it.

```html
<meta charset="UTF-8">
```

Even though `<meta값유지>` contains Korean, the exporter's preprocessing may have treated `<meta` as the start of an HTML meta tag before Mermaid parsed the diagram. The historical failure alone does not prove which preprocessing layer did so.

### Solution

Encode the brackets rather than trying to alter the characters after `meta`:

```text
<!-- Before (Error) -->
rows=<meta-value>

<!-- After (Works) -->
rows=#lt;meta-value#gt;
```

**Lesson:** For HTML tag names such as `meta`, `div`, and `span`, always encode the brackets or avoid angle-bracket notation.

## Summary: Mermaid + HTML Parsing Gotchas

| Issue | Trigger | Solution |
|-------|---------|----------|
| Exporter-specific edge failure | A renderer rejects a form current Mermaid accepts | Normalize to `A -. "label" .-> B`, then compare Mermaid vs exporter versions |
| Literal angle brackets | A Markdown/HTML wrapper rewrites `<row>` | Quote the label and encode as `#lt;row#gt;`, or drop the brackets |
| Actual HTML tag names | `<meta>`, `<div>`, `<span>`, etc. | Encode the brackets; do not rely on renaming tricks |

## Conclusion

Mermaid is powerful for documentation, but its integration with HTML-based renderers (like VS Code's Markdown PDF extension) introduces hidden parsing conflicts.

**Key Takeaways:**
1. Use Mermaid's documented edge form before blaming label words: `A -->|"text"| B` for a solid edge and `A -. "text" .-> B` for a dotted edge.
2. Quote labels that contain punctuation or spaces, and encode angle brackets as `#lt;` / `#gt;` when they must be displayed literally.
3. Be especially careful with HTML tag names such as `meta`, `div`, and `span`; encoding handles these too.

When in doubt, reduce the diagram to one documented edge, test it in the same Mermaid version and in the PDF exporter, then add encoded label text back. That separates Mermaid grammar from host preprocessing instead of turning a one-off workaround into a false language rule.
