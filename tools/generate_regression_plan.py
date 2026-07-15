#!/usr/bin/env python3
"""Generate a targeted regression plan from REGRESSION_MATRIX.md."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SECTION_BY_DEFECT_TYPE = {
    "CATEGORY_ROUTER": ["Category Router"],
    "SUPPORT_LEVEL": ["Category Router", "Steam", "Beauty"],
    "PRODUCT_PACK": ["Product Truth"],
    "PRODUCT_TRUTH": ["Product Truth"],
    "PRODUCTION_TYPE": ["Product Truth", "Seedance"],
    "SEEDANCE_PACKAGE": ["Seedance"],
    "AI_REVIEW": ["Seedance"],
    "DELIVERY": ["Delivery"],
    "STEAM": ["Steam"],
    "BEAUTY": ["Beauty"],
    "BACKEND_ACTION": [],
}

TYPE_LABELS = {
    "automated_repository_test": "targeted repository tests",
    "manual_document_review": "manual reviews",
    "builder_preview_test": "Builder Preview tests",
    "future_backend_test": "future backend tests",
}

FULL_VALIDATION_COMMANDS = [
    "python3 tools/validate_main_instructions.py",
    "python3 tools/validate_knowledge_01_17.py",
    "python3 tools/validate_knowledge_18.py",
    "python3 tools/validate_knowledge_01_18.py",
    "python3 tools/check_markdown_references.py",
    "python3 tools/build_custom_gpt_package.py --check",
    "git diff --check",
]


def section_text(markdown: str, section: str) -> str:
    pattern = re.compile(rf"^## {re.escape(section)}\n(?P<body>[\s\S]*?)(?=^## |\Z)", re.M)
    match = pattern.search(markdown)
    return match.group("body") if match else ""


def rows_for_section(markdown: str, section: str) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for line in section_text(markdown, section).splitlines():
        if not line.startswith("|") or "---" in line or "test_type" in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) >= 3:
            rows.append((cells[0], cells[1], cells[2]))
    return rows


def generate_plan(defect_type: str, matrix_path: Path) -> str:
    normalized = defect_type.upper()
    markdown = matrix_path.read_text(encoding="utf-8")
    sections = SECTION_BY_DEFECT_TYPE.get(normalized, [normalized.replace("_", " ").title()])
    grouped: dict[str, list[str]] = {label: [] for label in TYPE_LABELS.values()}

    for section in sections:
        for test_id, test_type, target in rows_for_section(markdown, section):
            label = TYPE_LABELS.get(test_type)
            if label:
                grouped[label].append(f"- {test_id}: {target}")

    if normalized == "BACKEND_ACTION":
        grouped["future backend tests"].append(
            "- BACKEND-ACTION: run backend tests and OpenAPI validation when backend scope applies."
        )

    lines = [f"# Regression Plan: {normalized}", ""]
    for label in TYPE_LABELS.values():
        lines.append(f"## {label}")
        lines.extend(grouped[label] or ["- None from current matrix."])
        lines.append("")

    lines.append("## full validation commands")
    lines.extend(f"- `{command}`" for command in FULL_VALIDATION_COMMANDS)
    lines.append("")
    lines.append("This plan has not executed any test.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--defect-type", required=True)
    parser.add_argument(
        "--matrix",
        type=Path,
        default=Path("optimization/REGRESSION_MATRIX.md"),
    )
    args = parser.parse_args()
    print(generate_plan(args.defect_type, args.matrix))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
