#!/usr/bin/env python3
"""Validate the generated Custom GPT Knowledge 01-17 upload set."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "custom_gpt_package/multi_category_gpt/01_KNOWLEDGE_UPLOAD"

EXPECTED = [
    "01_TikTok_Viral_Analysis_Framework.md",
    "02_Car_Cleaning_Content_Psychology.md",
    "03_Cleaning_Video_Hook_Database.md",
    "04_Satisfying_Cleaning_Visual_Library.md",
    "05_TikTok_Shop_Script_Writing_Rules.md",
    "06_Video_Script_Scoring_System.md",
    "07_Professional_Shooting_Standard.md",
    "08_Shot_Production_Planning_Framework.md",
    "09_Seedance_Generation_Director.md",
    "10_AI_Generation_Quality_Review.md",
    "11_Category_and_Main_Router.md",
    "12_Automotive_Category_Pack.md",
    "13_Car_Vacuum_Product_Pack.md",
    "14_Home_Cleaning_Skeleton.md",
    "15_Steam_Cleaner_Skeleton.md",
    "16_Beauty_Care_Tools_Skeleton.md",
    "17_Seedance_Reference_Pack.md",
]

FORBIDDEN_SHARED_ROLE_TERMS = [
    "Car Cleaning AI Director",
    "Car Cleaning Shot Production Planner",
    "Car Cleaning Commercial Shots",
    "Car Cleaning Commercial Assets",
    "Car Cleaning Video Production Director Standard",
]

SUPPORT_MATRIX_LINES = [
    "car_vacuum: COMPLETE",
    "snow_foam_cannon: GENERIC_SUPPORTED",
    "detailing_brush: GENERIC_SUPPORTED",
    "blower_vacuum: PARTIAL",
    "pressure_washer_accessory: PARTIAL",
    "crevice_cleaning_tool: PARTIAL",
    "interior_cleaning_tool: PARTIAL",
    "car_cleaning_spray: PARTIAL",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(name: str) -> str:
    path = BASE / name
    if not path.is_file():
        fail(f"missing {path}")
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        fail(f"empty {path}")
    return text


def require(text: str, needle: str, context: str) -> None:
    if needle not in text:
        fail(f"{context} missing {needle!r}")


def main() -> int:
    if not BASE.is_dir():
        fail(f"missing directory {BASE}")

    files = sorted(
        p.name
        for p in BASE.glob("*.md")
        if p.name[:2].isdigit() and 1 <= int(p.name[:2]) <= 17
    )
    if files != EXPECTED:
        fail(f"expected 17 exact files, got {files}")

    k08_files = [name for name in files if name.startswith("08_")]
    if k08_files != ["08_Shot_Production_Planning_Framework.md"]:
        fail(f"invalid Knowledge 08 files: {k08_files}")
    if any("Decision_Framework" in name for name in files):
        fail("old Decision Framework present in upload set")

    for name in [
        "01_TikTok_Viral_Analysis_Framework.md",
        "05_TikTok_Shop_Script_Writing_Rules.md",
        "06_Video_Script_Scoring_System.md",
        "07_Professional_Shooting_Standard.md",
        "08_Shot_Production_Planning_Framework.md",
        "09_Seedance_Generation_Director.md",
        "10_AI_Generation_Quality_Review.md",
    ]:
        top = "\n".join(read(name).splitlines()[:90])
        for term in FORBIDDEN_SHARED_ROLE_TERMS:
            if term in top:
                fail(f"{name} shared role/status still contains {term!r}")

    for name in [
        "02_Car_Cleaning_Content_Psychology.md",
        "03_Cleaning_Video_Hook_Database.md",
        "04_Satisfying_Cleaning_Visual_Library.md",
    ]:
        text = read(name)
        require(text, "category: automotive_cleaning", name)
        require(text, "Cross-Category", name)

    k11 = read("11_Category_and_Main_Router.md")
    for needle in [
        "builder_knowledge_aliases",
        "Runtime Resolution Rule",
        "GENERIC_SUPPORTED",
        "Task Router",
        "Car Cleaning Main Router",
        "NOT_RUN",
    ]:
        require(k11, needle, "Knowledge 11")
    if "separate primary release" in k11 and "not a separate primary release" not in k11:
        fail("Knowledge 11 may still mark automotive GPT as primary release")

    k12 = read("12_Automotive_Category_Pack.md")
    for line in SUPPORT_MATRIX_LINES:
        if k12.count(line) < 1:
            fail(f"Knowledge 12 missing matrix line {line}")
    for product in [line.split(":")[0] for line in SUPPORT_MATRIX_LINES]:
        statuses = set(re.findall(rf"\b{re.escape(product)}:\s+([A-Z_]+)", k12))
        if len(statuses) != 1:
            fail(f"Knowledge 12 conflicting statuses for {product}: {sorted(statuses)}")

    k13 = read("13_Car_Vacuum_Product_Pack.md")
    for needle in [
        "support_level: COMPLETE",
        "production_ready: true",
        "core_product_proof_requires_real_shoot: true",
        "ai_generated_suction_proof_prohibited: true",
        "Only accessories verified in the actual SKU",
    ]:
        require(k13, needle, "Knowledge 13")

    skeleton_requirements = {
        "14_Home_Cleaning_Skeleton.md": [
            "support_level: SKELETON_ONLY",
            "routing_status: PARTIAL",
            "production_ready: false",
        ],
        "15_Steam_Cleaner_Skeleton.md": [
            "support_level: SKELETON_ONLY",
            "routing_status: PARTIAL",
            "production_ready: false",
            "safety_level: high",
        ],
        "16_Beauty_Care_Tools_Skeleton.md": [
            "support_level: SKELETON_ONLY",
            "routing_status: PARTIAL",
            "production_ready: false",
            "human_demo_required_by_default: true",
        ],
    }
    for name, needles in skeleton_requirements.items():
        text = read(name)
        for needle in needles:
            require(text, needle, name)
        if "support_level: COMPLETE" in text or "production_ready: true" in text:
            fail(f"{name} contains complete/production-ready marker")

    for name in [
        "08_Shot_Production_Planning_Framework.md",
        "09_Seedance_Generation_Director.md",
        "10_AI_Generation_Quality_Review.md",
        "11_Category_and_Main_Router.md",
    ]:
        require(read(name), "NOT_RUN", name)

    for name in [
        "08_Shot_Production_Planning_Framework.md",
        "09_Seedance_Generation_Director.md",
        "10_AI_Generation_Quality_Review.md",
    ]:
        text = read(name)
        forbidden = [
            "Prompt can receive PASS",
            "Prompt may receive PASS",
            "Storyboard can receive PASS",
            "Storyboard may receive PASS",
        ]
        if any(phrase in text for phrase in forbidden):
            fail(f"{name} may allow prompt/storyboard PASS")

    k17 = read("17_Seedance_Reference_Pack.md")
    unresolved = re.findall(r"\[(ref|skill):[^\]]+\]", k17)
    if unresolved:
        fail(f"Knowledge 17 unresolved runtime tokens: {len(unresolved)}")
    for needle in [
        "self_contained: true",
        "unresolved_ref_tokens: 0",
        "unresolved_skill_tokens: 0",
        "Local Quick Reference",
        "Local Continuation Contract",
    ]:
        require(k17, needle, "Knowledge 17")

    print("PASS: Knowledge 01-17 validation succeeded")
    print("expected_files: 17")
    print("actual_files: 17")
    print("unresolved_ref_tokens: 0")
    print("unresolved_skill_tokens: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
