#!/usr/bin/env python3
"""Validate a post-test optimization defect file.

The parser intentionally supports only the simple YAML subset used by the
optimization templates. It avoids third-party dependencies.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any


VALID_SEVERITIES = {
    "S0_BLOCKER",
    "S1_CRITICAL",
    "S2_MAJOR",
    "S3_MINOR",
    "S4_SUGGESTION",
}

VALID_STATUSES = {
    "NEW",
    "NEEDS_REPRODUCTION",
    "REPRODUCED",
    "DIAGNOSED",
    "FIX_IN_PROGRESS",
    "REPOSITORY_VALIDATED",
    "PR_OPEN",
    "MERGED",
    "BUILDER_UPDATED",
    "BUILDER_RETESTED",
    "CLOSED",
    "REOPENED",
}

REQUIRED_DEFECT_FIELDS = [
    "defect.defect_id",
    "defect.title",
    "defect.reporter",
    "defect.reported_at",
    "defect.severity",
    "defect.status",
    "defect.environment.custom_gpt_version",
    "defect.environment.instructions_version",
    "defect.environment.knowledge_version",
    "defect.environment.builder_environment",
    "defect.evidence.test_case_id",
    "defect.evidence.original_prompt",
    "defect.evidence.complete_output",
    "defect.evidence.expected_result",
    "defect.evidence.actual_result",
    "defect.evidence.conversation_reference",
    "defect.evidence.reproduction_count",
]

SECRET_PATTERNS = [
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._-]{20,}", re.I),
    re.compile(r"(api[_-]?key|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9._-]{20,}", re.I),
]


class ValidationError(RuntimeError):
    """Raised when validation fails."""


def extract_yaml_fence(text: str) -> str:
    match = re.search(r"```yaml\n(?P<body>[\s\S]*?)\n```", text)
    if not match:
        raise ValidationError("missing yaml fenced block")
    return match.group("body")


def parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if value in {"true", "false"}:
        return value == "true"
    if value == "[]":
        return []
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip("'\"") for item in inner.split(",")]
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def parse_simple_yaml(yaml_text: str) -> dict[str, Any]:
    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]
    for raw_line in yaml_text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        stripped = raw_line.strip()
        if stripped.startswith("- "):
            continue
        if ":" not in stripped:
            raise ValidationError(f"unsupported yaml line: {raw_line}")
        key, raw_value = stripped.split(":", 1)
        while indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if raw_value.strip() == "":
            value: Any = {}
            parent[key] = value
            stack.append((indent, value))
        else:
            parent[key] = parse_scalar(raw_value)
    return root


def load_markdown_yaml(path: Path) -> dict[str, Any]:
    return parse_simple_yaml(extract_yaml_fence(path.read_text(encoding="utf-8")))


def get_path(data: dict[str, Any], dotted: str) -> Any:
    current: Any = data
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def is_blank(value: Any) -> bool:
    return value is None or value == "" or value == []


def validate_required_fields(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_DEFECT_FIELDS:
        if is_blank(get_path(data, field)):
            errors.append(f"missing required field: {field}")
    reproduction_count = get_path(data, "defect.evidence.reproduction_count")
    if not isinstance(reproduction_count, int) or reproduction_count < 1:
        errors.append("evidence.reproduction_count must be at least 1")
    return errors


def contains_secret(text: str) -> bool:
    return any(pattern.search(text) for pattern in SECRET_PATTERNS)


def change_request_exists(change_id: str, change_request_dir: Path) -> bool:
    for path in change_request_dir.glob("*.md"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if change_id in text or change_id in path.name:
            return True
    return False


def validate_case(path: Path, change_request_dir: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    data = load_markdown_yaml(path)
    errors = validate_required_fields(data)

    severity = get_path(data, "defect.severity")
    status = get_path(data, "defect.status")
    if severity not in VALID_SEVERITIES:
        errors.append(f"invalid severity: {severity}")
    if status not in VALID_STATUSES:
        errors.append(f"invalid status: {status}")

    builder_retest = get_path(data, "defect.resolution.builder_retest")
    if status == "CLOSED" and builder_retest != "BUILDER_RETESTED":
        errors.append("CLOSED requires resolution.builder_retest=BUILDER_RETESTED")
    if status == "MERGED":
        fixed_version = get_path(data, "defect.resolution.fixed_version")
        if fixed_version == "CLOSED":
            errors.append("MERGED cannot be treated as CLOSED")

    change_id = get_path(data, "defect.resolution.change_request_id")
    if change_id and not change_request_exists(str(change_id), change_request_dir):
        errors.append(f"referenced Change Request not found: {change_id}")

    if contains_secret(text):
        errors.append("possible real secret detected")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("defect_file", type=Path, help="Defect Markdown file to validate.")
    parser.add_argument(
        "--change-request-dir",
        type=Path,
        default=Path("optimization/change_requests"),
        help="Directory containing Change Request Markdown files.",
    )
    args = parser.parse_args()

    errors = validate_case(args.defect_file, args.change_request_dir)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {args.defect_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
