#!/usr/bin/env python3
"""Create a defect and Change Request from optimization templates."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


VALID_SEVERITIES = {
    "S0_BLOCKER",
    "S1_CRITICAL",
    "S2_MAJOR",
    "S3_MINOR",
    "S4_SUGGESTION",
}


def replace_template_values(text: str, replacements: dict[str, str]) -> str:
    for old, new in replacements.items():
        text = text.replace(old, new, 1)
    return text


def create_case(root: Path, defect_id: str, title: str, severity: str, reporter: str) -> tuple[Path, Path]:
    if severity not in VALID_SEVERITIES:
        raise ValueError(f"invalid severity: {severity}")

    defects_dir = root / "defects"
    change_requests_dir = root / "change_requests"
    defect_template = defects_dir / "DEFECT_TEMPLATE.md"
    change_template = change_requests_dir / "CHANGE_REQUEST_TEMPLATE.md"
    if not defect_template.is_file():
        raise FileNotFoundError(defect_template)
    if not change_template.is_file():
        raise FileNotFoundError(change_template)

    defect_path = defects_dir / f"{defect_id}.md"
    change_id = f"CR-{defect_id}"
    change_path = change_requests_dir / f"{change_id}.md"
    if defect_path.exists() or change_path.exists():
        raise FileExistsError(f"duplicate defect or change request ID: {defect_id}")

    reported_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    defect_text = defect_template.read_text(encoding="utf-8")
    defect_text = replace_template_values(
        defect_text,
        {
            'defect_id: ""': f'defect_id: "{defect_id}"',
            'title: ""': f'title: "{title}"',
            'reporter: ""': f'reporter: "{reporter}"',
            'reported_at: ""': f'reported_at: "{reported_at}"',
            'severity: "S0_BLOCKER | S1_CRITICAL | S2_MAJOR | S3_MINOR | S4_SUGGESTION"': f'severity: "{severity}"',
            'change_request_id: ""': f'change_request_id: "{change_id}"',
        },
    )
    change_text = change_template.read_text(encoding="utf-8")
    change_text = replace_template_values(
        change_text,
        {
            'change_id: ""': f'change_id: "{change_id}"',
            "defect_ids: []": f'defect_ids: ["{defect_id}"]',
        },
    )

    defect_path.write_text(defect_text, encoding="utf-8")
    change_path.write_text(change_text, encoding="utf-8")
    return defect_path, change_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--defect-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--severity", required=True, choices=sorted(VALID_SEVERITIES))
    parser.add_argument("--reporter", default="UNKNOWN")
    parser.add_argument("--root", type=Path, default=Path("optimization"))
    args = parser.parse_args()

    defect_path, change_path = create_case(
        root=args.root,
        defect_id=args.defect_id,
        title=args.title,
        severity=args.severity,
        reporter=args.reporter,
    )
    print(f"created_defect: {defect_path}")
    print(f"created_change_request: {change_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
