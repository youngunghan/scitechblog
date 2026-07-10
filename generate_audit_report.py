#!/usr/bin/env python3
"""Generate a lightweight Markdown audit of blog post structure."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError as error:
    raise SystemExit("PyYAML is required: python -m pip install pyyaml") from error


FRONT_MATTER_RE = re.compile(r"\A---\s*\r?\n(.*?)\r?\n---\s*$", re.DOTALL | re.MULTILINE)


def parse_front_matter(path: Path) -> dict | None:
    content = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(content)
    if match is None:
        return None

    try:
        front_matter = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None

    return front_matter if isinstance(front_matter, dict) else None


def check_structure(path: Path) -> list[str]:
    content = path.read_text(encoding="utf-8")
    filename = path.name.lower()

    if any(term in filename for term in ("algo", "leetcode", "boj")):
        required = ["## Problem", "## Solution", "## Complexity"]
    elif "review" in filename:
        required = ["## Introduction", "## Conclusion"]
    else:
        required = ["## Introduction", "## Conclusion"]

    return [heading for heading in required if heading not in content and heading[1:] not in content]


def markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def generate_report(posts_dir: Path) -> str:
    lines = [
        "# Blog Post Quality Audit Report",
        "",
        "## 1. Blog Post Characteristics & Standards",
        "",
        "### Common Standards (All Posts)",
        "- **Front Matter**: Title, Date, Categories, Tags, Image (Relative path).",
        "- **Structure**: Clear headers, Intro/Conclusion.",
        "",
        "### Category Standards",
        "- **Algorithm**: Problem, Approach, Solution, Complexity.",
        "- **Review**: Abstract, Method, Experiments.",
        "- **Troubleshooting**: Problem, Root Cause, Solution.",
        "",
        "---",
        "",
        "## 2. Evaluation Results",
        "",
        "| Date | File | Category | Image Path | Structure | Status |",
        "|------|------|----------|------------|-----------|--------|",
    ]

    for path in sorted(posts_dir.glob("*.md")):
        front_matter = parse_front_matter(path)
        date = path.name[:10]

        if front_matter is None:
            lines.append(f"| {date} | `{path.name}` | N/A | Invalid YAML | N/A | Fail |")
            continue

        categories = front_matter.get("categories", [])
        category = ", ".join(map(str, categories)) if isinstance(categories, list) else str(categories)
        image = front_matter.get("image")

        if not image:
            image_status = "Missing"
        elif isinstance(image, dict):
            image_path = str(image.get("path", ""))
            if image_path.startswith("/"):
                image_status = "Absolute path"
            elif not image_path.startswith("assets/img/"):
                image_status = f"Unusual path (`{image_path}`)"
            else:
                image_status = "Valid"
        else:
            image_status = "Invalid format"

        missing = check_structure(path)
        structure_status = f"Missing: {', '.join(missing)}" if missing else "Valid"

        if image_status in {"Missing", "Absolute path", "Invalid format"}:
            status = "Fail"
        elif image_status.startswith("Unusual") or missing:
            status = "Warning"
        else:
            status = "Pass"

        lines.append(
            f"| {date} | `{path.name}` | {markdown_cell(category)} | "
            f"{markdown_cell(image_status)} | {markdown_cell(structure_status)} | {status} |"
        )

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--posts-dir", type=Path, default=Path("_posts"))
    parser.add_argument("--output", type=Path, help="Write to this path instead of stdout.")
    args = parser.parse_args()

    report = generate_report(args.posts_dir)
    if args.output is None:
        sys.stdout.write(report)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
