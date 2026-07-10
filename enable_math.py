#!/usr/bin/env python3
"""Enable MathJax only for posts containing math outside code spans/blocks."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


FRONT_MATTER_RE = re.compile(
    r"\A---[ \t]*\r?\n(?P<front>.*?)(?P<closing>^---[ \t]*\r?$)",
    re.DOTALL | re.MULTILINE,
)
INLINE_MATH_RE = re.compile(
    r"(?<![\\$])\$(?![\s$])(?:\\.|[^$\n])+?(?<![\s\\])\$(?!\$)"
)
DISPLAY_MATH_RE = re.compile(r"(?<!\\)\$\$.+?(?<!\\)\$\$", re.DOTALL)


def strip_inline_code(line: str) -> str:
    """Remove Markdown code spans while preserving surrounding prose."""
    output: list[str] = []
    index = 0

    while index < len(line):
        if line[index] != "`":
            output.append(line[index])
            index += 1
            continue

        delimiter_end = index
        while delimiter_end < len(line) and line[delimiter_end] == "`":
            delimiter_end += 1
        delimiter = line[index:delimiter_end]
        closing = line.find(delimiter, delimiter_end)

        if closing == -1:
            break
        index = closing + len(delimiter)

    return "".join(output)


def prose_without_code(markdown: str) -> str:
    """Return Markdown prose with fenced and inline code removed."""
    output: list[str] = []
    fence_char: str | None = None
    fence_length = 0

    for line in markdown.splitlines(keepends=True):
        marker = re.match(r" {0,3}(`{3,}|~{3,})", line)

        if fence_char is None and marker:
            fence_char = marker.group(1)[0]
            fence_length = len(marker.group(1))
            continue

        if fence_char is not None:
            closing = rf" {{0,3}}{re.escape(fence_char)}{{{fence_length},}}[ \t]*(?:\r?\n)?$"
            if re.match(closing, line):
                fence_char = None
                fence_length = 0
            continue

        output.append(strip_inline_code(line))

    return "".join(output)


def contains_math(markdown: str) -> bool:
    prose = prose_without_code(markdown)
    return bool(
        "\\(" in prose
        or "\\[" in prose
        or DISPLAY_MATH_RE.search(prose)
        or INLINE_MATH_RE.search(prose)
    )


def enable_math(path: Path, *, check: bool = False) -> bool:
    content = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(content)

    if match is None:
        print(f"Skipping {path}: no complete YAML front matter")
        return False

    if re.search(r"(?m)^\s*math:\s*true(?:\s*#.*)?$", match.group("front")):
        return False

    if not contains_math(content[match.end() :]):
        return False

    if check:
        print(f"Needs math: true: {path}")
        return True

    insert_at = match.start("closing")
    path.write_text(content[:insert_at] + "math: true\n" + content[insert_at:], encoding="utf-8")
    print(f"Enabled math in {path}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--posts-dir", type=Path, default=Path("_posts"))
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report posts that need math enabled without modifying them.",
    )
    args = parser.parse_args()

    changed = sum(enable_math(path, check=args.check) for path in sorted(args.posts_dir.glob("*.md")))
    return 1 if args.check and changed else 0


if __name__ == "__main__":
    raise SystemExit(main())
