---
title: "VS Code Markdown PDF Extension: Tips and Gotchas"
date: 2025-12-24 14:30:00 +0900
categories: [Development, VS Code]
tags: [vscode, markdown, pdf, mermaid, extension, troubleshooting]
description: "Practical tips for using the Markdown PDF extension in VS Code, including common pitfalls with Mermaid diagrams."
image:
  path: assets/img/posts/troubleshooting/vscode_markdown_pdf_thumbnail.png
  alt: VS Code Markdown PDF Tips
author: seoultech
---

## Introduction

The **Markdown PDF** extension for VS Code is a convenient way to export Markdown documents to PDF, HTML, or images. However, it has some quirks, especially when working with Mermaid diagrams. This post covers practical tips and common gotchas.

## Basic Setup

### Installation

1. Open VS Code Extensions (Ctrl+Shift+X)
2. Search for "Markdown PDF" by yzane
3. Install and reload VS Code

### Export Options

- `Markdown PDF: Export (pdf)` - Standard PDF export
- `Markdown PDF: Export (html)` - HTML with embedded styles
- `Markdown PDF: Export (png/jpeg)` - Image export

## Mermaid Diagram Support

The extension supports Mermaid diagrams (version 11.x as of this writing). However, syntax that works in GitHub or other renderers may fail here.

### Gotcha #1: Reserved Keywords

Certain words are reserved in Mermaid's parser:

```markdown
<!--  Causes Syntax Error -->
A -->|"AND"| B
A -->|"OR"| B

<!--  Works -->
A -->|"_AND_"| B
A -->|"_OR_"| B
```

Use underscores to escape: `_AND_`, `_OR_`

### Gotcha #2: HTML Tag Interpretation

Content in angle brackets (`<>`) may be interpreted as HTML:

```markdown
<!--  Error: Looks like HTML tag -->
A -->|"response: <row>"| B
A -->|"data: <unchanged>"| B

<!--  Works: Add non-English characters -->
A -->|"response: <해당row>"| B
A -->|"data: <변경없음>"| B
```

### Gotcha #3: Actual HTML Tag Names

Be especially careful with real HTML tag names:

```markdown
<!--  ALWAYS fails -->
<meta>
<div>
<span>

<!--  Replace with alternatives -->
<메타>
<구역>
<범위>
```

## Styling Tips

### Custom CSS

Create a custom CSS file for consistent styling:

```css
/* markdown-pdf.css */
body {
  font-family: 'Noto Sans KR', sans-serif;
  line-height: 1.6;
}

code {
  background-color: #f5f5f5;
  padding: 2px 6px;
  border-radius: 4px;
}

pre {
  background-color: #2d2d2d;
  color: #f8f8f2;
  padding: 16px;
  border-radius: 8px;
}
```

Configure in `settings.json`:

```json
{
  "markdown-pdf.styles": [
    "/path/to/markdown-pdf.css"
  ]
}
```

### Page Layout

```json
{
  "markdown-pdf.format": "A4",
  "markdown-pdf.margin.top": "20mm",
  "markdown-pdf.margin.bottom": "20mm",
  "markdown-pdf.margin.left": "15mm",
  "markdown-pdf.margin.right": "15mm"
}
```

## Troubleshooting

### Problem: Diagrams Not Rendering

**Symptom:** Mermaid code blocks show as raw text.

**Solution:** Check if the extension is up to date. Restart VS Code after updating.

### Problem: Korean Text Broken

**Symptom:** Korean characters appear as boxes or question marks.

**Solution:** Specify a font that supports Korean:

```json
{
  "markdown-pdf.styles": [
    "https://fonts.googleapis.com/css2?family=Noto+Sans+KR&display=swap"
  ]
}
```

### Problem: Export Takes Forever

**Symptom:** PDF export hangs on large documents.

**Solution:** 
1. Split into multiple files
2. Reduce diagram complexity
3. Close other VS Code extensions temporarily

## Best Practices

### 1. Test Incrementally

Export after every few changes to catch issues early.

### 2. Keep Diagrams Simple

Markdown PDF uses a headless browser internally. Complex diagrams with many nodes can cause timeouts.

### 3. Avoid Special Characters in Labels

Characters that have meaning in HTML/Mermaid can cause issues:
- `<`, `>` - Use `&lt;`, `&gt;` or Korean alternatives
- `"` inside labels - Escape with backslash
- `|` - Use sparingly, can conflict with Mermaid syntax

### 4. Use Preview First

Before exporting to PDF, use VS Code's built-in Markdown preview (Ctrl+Shift+V) to catch obvious rendering issues.

## Conclusion

Markdown PDF is powerful but has quirks, especially with Mermaid diagrams. Key takeaways:

1. **Escape reserved keywords**: `_AND_`, `_OR_`
2. **Avoid English-only angle brackets**: `<english>` → `<한글>`
3. **Watch for HTML tag names**: `<meta>`, `<div>`, etc.
4. **Configure Korean fonts** for proper rendering

With these tips, you can produce professional PDF documentation directly from Markdown!
