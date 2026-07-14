#!/usr/bin/env python3
"""Validate the complete Knowledge 01-18 upload set."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
UPLOAD_DIR = ROOT / "custom_gpt_package/multi_category_gpt/01_KNOWLEDGE_UPLOAD"


def fail(message: str) -> int:
    print(f"FAIL: {message}", file=sys.stderr)
    return 1


def run_validator(script: str) -> tuple[int, str, str]:
    result = subprocess.run(
        [sys.executable, str(ROOT / script)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode, result.stdout, result.stderr


def read_upload(name: str) -> str:
    return (UPLOAD_DIR / name).read_text(encoding="utf-8")


def numbered_knowledge_files() -> list[Path]:
    return sorted(
        path
        for path in UPLOAD_DIR.glob("*.md")
        if path.name[:2].isdigit()
    )


def main() -> int:
    code, stdout, stderr = run_validator("tools/validate_knowledge_01_17.py")
    if code != 0:
        sys.stdout.write(stdout)
        sys.stderr.write(stderr)
        return fail("Knowledge 01-17 regression validation failed")

    code, stdout, stderr = run_validator("tools/validate_knowledge_18.py")
    if code != 0:
        sys.stdout.write(stdout)
        sys.stderr.write(stderr)
        return fail("Knowledge 18 validation failed")

    files = numbered_knowledge_files()
    numbers = [int(path.name[:2]) for path in files]
    expected = list(range(1, 19))
    if len(files) != 18:
        return fail(f"expected 18 numbered Knowledge files, found {len(files)}")
    if numbers != expected:
        return fail(f"expected Knowledge numbers {expected}, found {numbers}")

    knowledge08 = [path for path in files if path.name.startswith("08_")]
    if len(knowledge08) != 1:
        return fail("expected exactly one Knowledge 08 upload file")

    decision_framework = [
        path.name for path in files if "Decision_Framework" in path.name
    ]
    if decision_framework:
        return fail("old Decision Framework upload exists: " + ", ".join(decision_framework))

    k17 = read_upload("17_Seedance_Reference_Pack.md")
    unresolved = sorted(set(re.findall(r"\[(?:ref|skill):[^\]]+\]", k17)))
    if unresolved:
        return fail("Knowledge 17 unresolved tokens: " + ", ".join(unresolved))

    k18 = read_upload("18_Deliverable_and_Output_Contract.md")
    for phrase in [
        "Home Cleaning 必须声明 SKELETON_ONLY 和 PARTIAL",
        "Steam Cleaner 必须声明 SKELETON_ONLY、PARTIAL、safety_level=high",
        "Beauty Care Tools 必须声明 SKELETON_ONLY、PARTIAL、human_demo_required=true",
    ]:
        if phrase not in k18:
            return fail("Knowledge 18 skeleton status mismatch: " + phrase)

    for name in [
        "08_Shot_Production_Planning_Framework.md",
        "09_Seedance_Generation_Director.md",
        "10_AI_Generation_Quality_Review.md",
        "18_Deliverable_and_Output_Contract.md",
    ]:
        text = read_upload(name)
        if "NOT_RUN" not in text:
            return fail(f"{name} does not preserve AI Review NOT_RUN timing")

    if k18.count('production_type: "REAL_SHOOT | AI_GENERATION | HYBRID | STOCK_ASSET"') != 1:
        return fail("Production Type enum is missing or duplicated")

    old_ai_enum = 'ai_quality_review_status: "NOT_REQUIRED | NOT_RUN | PASS | FAILED"'
    if old_ai_enum in k18:
        return fail("Knowledge 18 still uses FAILED as a formal AI review status")

    fix_tokens = [
        "BLOCKED is not a completed full-generation state",
        "READY 表示信息足够生成策略、脚本和证明。Task A 或 Task B 必须生成四个文件",
        "PROVISIONAL 表示可以生成保守脚本。Task A 或 Task B 仍生成四个文件",
        "BLOCKED 状态下，Task A 或 Task B 不强制生成四个文件",
        "selected_model=Seedance",
        "selected_model=other 不生成 Seedance Package",
        "Production Type alone does not trigger Knowledge 09",
        "Knowledge 09 is model-specific routing for Seedance",
        "actual file links only",
        "fallback sections",
        "fabricated download links",
        "files_created 必须与实际生成文件数量一致",
    ]
    for token in fix_tokens:
        if token not in k18:
            return fail("Knowledge 18 fix token missing: " + token)

    if "selected_model: \"other\"" not in k18:
        return fail("Knowledge 18 does not define non-Seedance AI model routing")

    print("PASS: Knowledge 01-18 validation succeeded")
    print("knowledge_validation:")
    print("  expected_count: 18")
    print(f"  actual_count: {len(files)}")
    print("  expected_numbers:")
    for number in expected:
        print(f"    - {number}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
