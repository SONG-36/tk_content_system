#!/usr/bin/env python3
"""Validate Knowledge 18 delivery contract."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "knowledge/18_Deliverable_and_Output_Contract.md"
UPLOAD = (
    ROOT
    / "custom_gpt_package/multi_category_gpt/01_KNOWLEDGE_UPLOAD/"
    / "18_Deliverable_and_Output_Contract.md"
)


REQUIRED_SECTIONS = [
    "# 18. Deliverable and Output Contract",
    "## 1. Purpose and Scope",
    "## 2. Authority and Conflict Resolution",
    "## 3. Builder Knowledge Alias Map",
    "## 4. Task Types and Deliverables",
    "## 5. Input Readiness Contract",
    "## 6. Knowledge Routing Summary",
    "## 7. Resource Alignment",
    "## 8. Product Truth Review",
    "## 9. Deliverable 1 - Analysis Report",
    "## 10. Deliverables 2-4 - Three Script Versions",
    "## 11. Mandatory Script Header",
    "## 12. Mandatory Final Shot Contract",
    "## 13. Shot Production Plan",
    "## 14. Seedance Production Package",
    "## 15. AI Quality Review Status",
    "## 16. Product-Pack Extensions",
    "## 17. Script Evaluation",
    "## 18. File Naming",
    "## 19. File Generation Behavior",
    "## 20. Final Chat Response",
    "## 21. Final Quality Gate",
]

REQUIRED_TOKENS = [
    "knowledge_status:",
    'runtime_role: "FINAL_DELIVERY_ASSEMBLER"',
    "GPT Builder Main Instructions",
    "Category and Product truth/safety rules in Knowledge 11-16",
    "delivery_contract: \"18_Deliverable_and_Output_Contract.md\"",
    "<name>_analysis.md",
    "<name>_script_01_replicate.md",
    "<name>_script_02_low_cost.md",
    "<name>_script_03_conversion.md",
    "<name>_script_audit.md",
    "<name>_script_revised.md",
    "<name>_hook_visual_analysis.md",
    "<name>_seedance_production_package.md",
    "input_readiness:",
    "knowledge_routing_summary:",
    "resource_alignment:",
    "product_truth_review:",
    "script_summary:",
    "production_type: \"REAL_SHOOT | AI_GENERATION | HYBRID | STOCK_ASSET\"",
    "shot_production_plan:",
    "seedance_production_package:",
    "ai_quality_review_status:",
    "status: \"NOT_REQUIRED | NOT_RUN | PASS | REGENERATE | SWITCH_TO_HYBRID | SWITCH_TO_REAL_SHOOT\"",
    "car_vacuum_extension:",
    "SKELETON_ONLY",
    "human_demo_required=true",
    "script_evaluation:",
    "file_naming:",
    "File Generation Behavior",
    "Final Quality Gate",
    "BLOCKED is not a completed full-generation state",
    "selected_model=Seedance",
    "selected_model=other 不生成 Seedance Package",
    "actual file links only",
    "fallback section",
    "files_created 必须与实际生成文件数量一致",
    "input_readiness=READY 或 PROVISIONAL 的完整 Task A/B 没有四份交付物或四个 fallback sections",
    "four_file_contract_satisfied_when_required 仅适用于 READY 或 PROVISIONAL",
]

PROHIBITED_PATTERNS = [
    (re.compile(r"\[(?:ref|skill):[^\]]+\]"), "unresolved ref/skill token"),
    (
        re.compile(r'ai_quality_review_status:\s*"NOT_REQUIRED \| NOT_RUN \| PASS \| FAILED"'),
        "FAILED is used as a formal AI Quality Review enum",
    ),
    (
        re.compile(r"(Home Cleaning|Steam Cleaner|Beauty Care Tools)[\s\S]{0,160}COMPLETE"),
        "skeleton category marked COMPLETE",
    ),
    (
        re.compile(r"Prompt\s+(?:can|may|should|must)\s+(?:be\s+)?(?:receive\s+)?PASS", re.I),
        "prompt allowed to PASS AI review",
    ),
    (
        re.compile(r"Storyboard\s+(?:can|may|should|must)\s+(?:be\s+)?(?:receive\s+)?PASS", re.I),
        "storyboard allowed to PASS AI review",
    ),
]


def fail(message: str) -> int:
    print(f"FAIL: {message}", file=sys.stderr)
    return 1


def main() -> int:
    if not SOURCE.is_file():
        return fail(f"missing source file: {SOURCE.relative_to(ROOT)}")
    if not UPLOAD.is_file():
        return fail(f"missing upload file: {UPLOAD.relative_to(ROOT)}")

    source_bytes = SOURCE.read_bytes()
    upload_bytes = UPLOAD.read_bytes()
    if not source_bytes.strip():
        return fail("Knowledge 18 source is empty")
    if not upload_bytes.strip():
        return fail("Knowledge 18 upload copy is empty")
    if source_bytes != upload_bytes:
        return fail("Knowledge 18 source and upload copy differ")

    text = source_bytes.decode("utf-8")
    if not text.startswith("# 18. Deliverable and Output Contract\n"):
        return fail("title is incorrect")

    missing_sections = [section for section in REQUIRED_SECTIONS if section not in text]
    if missing_sections:
        return fail("missing required sections: " + ", ".join(missing_sections))

    missing_tokens = [token for token in REQUIRED_TOKENS if token not in text]
    if missing_tokens:
        return fail("missing required contract tokens: " + ", ".join(missing_tokens))

    for pattern, reason in PROHIBITED_PATTERNS:
        if pattern.search(text):
            return fail(reason)

    if "AI 不得伪造吸力或人体功效" not in text:
        return fail("AI suction/human efficacy fabrication ban is missing")

    old_enum = 'ai_quality_review_status: "NOT_REQUIRED | NOT_RUN | PASS | FAILED"'
    if old_enum in text:
        return fail("old AI Quality Review FAILED enum remains")

    required_branches = [
        "READY 表示信息足够生成策略、脚本和证明。Task A 或 Task B 必须生成四个文件",
        "PROVISIONAL 表示可以生成保守脚本。Task A 或 Task B 仍生成四个文件",
        "BLOCKED 状态下，Task A 或 Task B 不强制生成四个文件",
        "不得生成虚假的证明型脚本",
    ]
    for branch in required_branches:
        if branch not in text:
            return fail("missing input readiness delivery branch: " + branch)

    seedance_gate_tokens = [
        "Production Type alone does not trigger Knowledge 09",
        "Knowledge 09 is model-specific routing for Seedance",
        "selected_model=other 不生成 Seedance Package",
        'knowledge_09_required: false',
        'knowledge_10_review_required: true',
        'ai_quality_review_status: "NOT_RUN"',
    ]
    for token in seedance_gate_tokens:
        if token not in text:
            return fail("missing Seedance model gate token: " + token)

    file_honesty_tokens = [
        "actual file links only",
        "fallback sections",
        "fabricated download links",
        "files_created 必须与实际生成文件数量一致",
        "BLOCKED 状态不得声称四文件完成",
    ]
    for token in file_honesty_tokens:
        if token not in text:
            return fail("missing file generation honesty token: " + token)

    allowed_enum_count = text.count(
        'production_type: "REAL_SHOOT | AI_GENERATION | HYBRID | STOCK_ASSET"'
    )
    if allowed_enum_count != 1:
        return fail("Production Type enum must appear exactly once")

    print("PASS: Knowledge 18 validation succeeded")
    print(f"source_file: {SOURCE.relative_to(ROOT)}")
    print(f"upload_file: {UPLOAD.relative_to(ROOT)}")
    print("source_target_identical: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
