#!/usr/bin/env python3
"""Validate the final GPT Builder Main Instructions."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INSTRUCTIONS = (
    ROOT / "custom_gpt_package/multi_category_gpt/00_INSTRUCTIONS/MAIN_INSTRUCTIONS.md"
)


REQUIRED_TOKENS = [
    "TikTok Shop Product Video Director",
    "Product truth and safety override visual ambition",
    "Task A",
    "Task B",
    "Task C",
    "Task D",
    "Task E",
    "Knowledge 11",
    "Knowledge 18",
    "automotive_cleaning",
    "home_cleaning",
    "beauty_care_tools",
    "car_vacuum COMPLETE",
    "SKELETON_ONLY",
    "READY",
    "PROVISIONAL",
    "BLOCKED",
    "REAL_SHOOT",
    "AI_GENERATION",
    "HYBRID",
    "STOCK_ASSET",
    "selected_model=Seedance",
    "selected_model=other",
    "NOT_RUN",
    "REGENERATE",
    "SWITCH_TO_HYBRID",
    "SWITCH_TO_REAL_SHOOT",
    "<name>_analysis.md",
    "<name>_script_01_replicate.md",
    "<name>_script_02_low_cost.md",
    "<name>_script_03_conversion.md",
    "无文件能力不得虚构",
    "Hook 30",
    "Visual Satisfaction 20",
    "Product Value 20",
    "Conversion 15",
    "Production Feasibility 10",
    "Innovation 5",
]

PROHIBITED_PATTERNS = [
    (re.compile(r"\[(?:ref|skill):[^\]]+\]"), "unresolved ref/skill token"),
    (re.compile(r"Mandatory Final Shot Contract", re.I), "full shot contract duplicated"),
    (re.compile(r"^shot:\s*$", re.M), "shot schema duplicated"),
    (re.compile(r"^resource_alignment:\s*$", re.M), "resource schema duplicated"),
    (re.compile(r"^product_truth_review:\s*$", re.M), "product truth schema duplicated"),
    (re.compile(r"^seedance_production_package:\s*$", re.M), "Seedance schema duplicated"),
    (re.compile(r"^script_evaluation:\s*$", re.M), "script evaluation schema duplicated"),
    (re.compile(r"/Users/|custom_gpt_package/|knowledge/|workflows/|categories/"), "local repository path used as runtime requirement"),
]


def fail(message: str) -> int:
    print(f"FAIL: {message}", file=sys.stderr)
    return 1


def main() -> int:
    if not INSTRUCTIONS.is_file():
        return fail(f"missing file: {INSTRUCTIONS.relative_to(ROOT)}")
    text = INSTRUCTIONS.read_text(encoding="utf-8")
    if not text.strip():
        return fail("Main Instructions is empty")

    character_count = len(text)
    if character_count >= 8000:
        return fail(f"character count must be below 8000, found {character_count}")

    missing = [token for token in REQUIRED_TOKENS if token not in text]
    if missing:
        return fail("missing required tokens: " + ", ".join(missing))

    for pattern, reason in PROHIBITED_PATTERNS:
        if pattern.search(text):
            return fail(reason)

    print("PASS: Main Instructions validation succeeded")
    print(f"instruction_characters: {character_count}")
    print(f"instruction_bytes: {len(text.encode('utf-8'))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
