#!/usr/bin/env python3
"""Validate an optimization Change Request scope."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from validate_optimization_case import get_path, load_markdown_yaml


GENERATED_PREFIXES = (
    "custom_gpt_package/multi_category_gpt/00_INSTRUCTIONS/",
    "custom_gpt_package/multi_category_gpt/01_KNOWLEDGE_UPLOAD/",
)

KNOWLEDGE_PREFIXES = (
    "knowledge/",
    "custom_gpt_package/multi_category_gpt/01_KNOWLEDGE_UPLOAD/",
)

PROTECTED_PREFIXES = (
    "custom_gpt_package/multi_category_gpt/00_INSTRUCTIONS/",
    "custom_gpt_package/multi_category_gpt/01_KNOWLEDGE_UPLOAD/",
    "knowledge/",
    "seedance_skills/",
)


def as_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if value in {None, ""}:
        return []
    return [str(value)]


def starts_with_any(path: str, prefixes: tuple[str, ...]) -> bool:
    return any(path.startswith(prefix) for prefix in prefixes)


def validate_scope(path: Path) -> list[str]:
    data = load_markdown_yaml(path)
    errors: list[str] = []

    source_files = as_list(get_path(data, "change_request.scope.source_files_to_modify"))
    generated_files = as_list(
        get_path(data, "change_request.scope.generated_files_expected_to_change")
    )
    protected_files = as_list(get_path(data, "change_request.scope.protected_files"))
    owner_approval_required = bool(
        get_path(data, "change_request.scope.owner_approval_required")
    )
    owner_approval_reference = str(
        get_path(data, "change_request.scope.owner_approval_reference") or ""
    )
    responsible_layer = str(
        get_path(data, "change_request.root_cause.responsible_layer") or ""
    )
    intended_behavior = str(get_path(data, "change_request.intended_behavior") or "")

    if generated_files and not source_files:
        errors.append("generated files changed without source files")
    if any(starts_with_any(item, GENERATED_PREFIXES) for item in source_files):
        errors.append("generated Builder runtime files listed as source files")
    if protected_files and (not owner_approval_required or not owner_approval_reference):
        errors.append("protected files require owner approval reference")

    backend_layer = responsible_layer.upper() == "BACKEND_ACTION"
    modifies_knowledge = any(starts_with_any(item, KNOWLEDGE_PREFIXES) for item in source_files)
    allowed_backend_knowledge_reason = any(
        token in intended_behavior.lower()
        for token in ("api contract", "action payload", "gpt routing", "builder action")
    )
    if backend_layer and modifies_knowledge and not allowed_backend_knowledge_reason:
        errors.append("Backend Action defect cannot modify Knowledge without GPT contract/routing reason")

    if "COMPLETE" in intended_behavior and (
        "SKELETON_ONLY" in intended_behavior or "PARTIAL" in intended_behavior
    ):
        errors.append("skeleton or partial support cannot be silently upgraded to COMPLETE")

    if any(item.startswith("tools/validate_") for item in source_files):
        errors.append("Validator files cannot be removed or weakened as a fix")
    if "delete validator" in intended_behavior.lower() or "weaken validator" in intended_behavior.lower():
        errors.append("Change Request cannot delete or weaken Validator")

    protected_source_files = [item for item in source_files if starts_with_any(item, PROTECTED_PREFIXES)]
    if protected_source_files and (not owner_approval_required or not owner_approval_reference):
        errors.append("protected source file changes require owner approval reference")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("change_request_file", type=Path)
    args = parser.parse_args()

    errors = validate_scope(args.change_request_file)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {args.change_request_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
