#!/usr/bin/env python3
"""Check internal markdown path references in this repository.

Rules:
- standard-library only
- read-only
- non-zero exit on missing internal references
- ignores external URLs
- ignores placeholder/template paths that contain '<', '>', or '*'
- scans for repo-relative paths using known top-level prefixes
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


TOP_LEVEL_PREFIXES = (
    "archive/",
    "categories/",
    "core/",
    "instructions/",
    "knowledge/",
    "release_manifests/",
    "research/",
    "seedance_skills/",
    "tests/",
    "tools/",
    "version/",
    "workflows/",
)


PATH_PATTERN = re.compile(
    r"(?P<path>(?:archive|categories|core|instructions|knowledge|release_manifests|"
    r"research|seedance_skills|tests|tools|version|workflows)"
    r"/[A-Za-z0-9_./<>*=-]+\.md)"
)


def iter_markdown_files(root: Path) -> list[Path]:
    files = []
    for path in root.rglob("*.md"):
        rel = path.relative_to(root).as_posix()
        if rel.startswith(".git/") or rel.startswith("source/"):
            continue
        files.append(path)
    return sorted(files)


def normalize_candidate(raw: str) -> str:
    candidate = raw.strip("`'\"()[]{}.,:;")
    candidate = candidate.split("=", 1)[-1] if "=" in candidate and candidate.startswith("selected_") else candidate
    return candidate


def should_ignore(candidate: str) -> bool:
    if "://" in candidate:
        return True
    if any(char in candidate for char in "<>*"):
        return True
    return not candidate.startswith(TOP_LEVEL_PREFIXES)


def check_references(root: Path) -> tuple[list[str], dict[str, list[tuple[str, int]]]]:
    missing: list[str] = []
    found_refs: dict[str, list[tuple[str, int]]] = {}

    for md_file in iter_markdown_files(root):
        rel_file = md_file.relative_to(root).as_posix()
        for lineno, line in enumerate(md_file.read_text(encoding="utf-8").splitlines(), start=1):
            for match in PATH_PATTERN.finditer(line):
                candidate = normalize_candidate(match.group("path"))
                if should_ignore(candidate):
                    continue
                target = root / candidate
                found_refs.setdefault(candidate, []).append((rel_file, lineno))
                if not target.exists():
                    missing.append(f"{rel_file}:{lineno} -> {candidate}")

    return missing, found_refs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root to scan. Defaults to current directory.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    missing, refs = check_references(root)

    print("Scanned markdown files:", len(iter_markdown_files(root)))
    print("Unique internal references:", len(refs))
    if missing:
        print("Missing references:")
        for entry in missing:
            print(entry)
        return 1

    print("No missing internal markdown references found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
