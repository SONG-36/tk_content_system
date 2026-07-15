from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from create_optimization_case import create_case
from generate_regression_plan import generate_plan
from validate_change_scope import validate_scope
from validate_optimization_case import validate_case


def defect_text(
    *,
    severity: str = "S1_CRITICAL",
    status: str = "REPRODUCED",
    complete_output: str = "Full GPT output",
    builder_retest: str = "NOT_RUN",
    change_request_id: str = "CR-DEF-001",
) -> str:
    return f"""# DEF-001

```yaml
defect:
  defect_id: "DEF-001"
  title: "Home cleaning routed as automotive"
  reporter: "tester"
  reported_at: "2026-07-15T00:00:00Z"
  severity: "{severity}"
  status: "{status}"

  environment:
    custom_gpt_version: "V2.6-BASELINE"
    instructions_version: "MAIN_INSTRUCTIONS 7195 chars"
    knowledge_version: "Knowledge 01-18"
    builder_environment: "Preview"

  evidence:
    test_case_id: "R-07"
    original_prompt: "Home cleaning product prompt"
    complete_output: "{complete_output}"
    expected_result: "home_cleaning"
    actual_result: "automotive_cleaning"
    screenshots: []
    generated_files: []
    conversation_reference: "manual-session"
    reproduction_count: 1

  reproduction:
    reproducible: true
    attempts: 1
    reproduction_steps: ["Run original prompt"]

  diagnosis:
    defect_type: "CATEGORY_ROUTER"
    suspected_layer: "Category Router"
    confirmed_root_cause: "Router over-defaulted to automotive"
    responsible_source_files: ["workflows/Category_Router.md"]
    affected_generated_files: ["custom_gpt_package/multi_category_gpt/01_KNOWLEDGE_UPLOAD/11_Category_and_Main_Router.md"]

  resolution:
    change_request_id: "{change_request_id}"
    branch: "fix/DEF-001-routing"
    pull_request: ""
    fixed_version: ""
    repository_validation: "NOT_RUN"
    builder_retest: "{builder_retest}"
```
"""


def change_request_text(
    *,
    responsible_layer: str = "CATEGORY_ROUTER",
    source_files: str = '["workflows/Category_Router.md"]',
    generated_files: str = '["custom_gpt_package/multi_category_gpt/01_KNOWLEDGE_UPLOAD/11_Category_and_Main_Router.md"]',
    protected_files: str = "[]",
    owner_required: str = "false",
    owner_ref: str = "",
    intended: str = "Route home cleaning to home_cleaning.",
) -> str:
    return f"""# CR-DEF-001

```yaml
change_request:
  change_id: "CR-DEF-001"
  defect_ids: ["DEF-001"]

  root_cause:
    responsible_layer: "{responsible_layer}"
    description: "Smallest responsible layer"

  scope:
    source_files_to_modify: {source_files}
    generated_files_expected_to_change: {generated_files}
    protected_files: {protected_files}
    prohibited_changes: []
    owner_approval_required: {owner_required}
    owner_approval_reference: "{owner_ref}"

  intended_behavior: "{intended}"
  prohibited_behavior: "Do not weaken Product Truth."

  risk:
    truth_risk: "medium"
    safety_risk: "low"
    cross_category_risk: "medium"
    builder_impact: "requires retest"

  validation:
    targeted_tests: ["R-07"]
    full_repository_validation_required: true
    builder_retest_required: true
    original_failure_prompt_required: true
```
"""


class OptimizationFrameworkTests(unittest.TestCase):
    def write(self, path: Path, text: str) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_valid_defect_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            defect = self.write(root / "defects" / "DEF-001.md", defect_text())
            self.write(root / "change_requests" / "CR-DEF-001.md", change_request_text())

            self.assertEqual(validate_case(defect, root / "change_requests"), [])

    def test_invalid_severity_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            defect = self.write(
                root / "defects" / "DEF-001.md",
                defect_text(severity="CRITICAL"),
            )
            self.write(root / "change_requests" / "CR-DEF-001.md", change_request_text())

            self.assertTrue(any("invalid severity" in e for e in validate_case(defect, root / "change_requests")))

    def test_invalid_status_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            defect = self.write(
                root / "defects" / "DEF-001.md",
                defect_text(status="DONE"),
            )
            self.write(root / "change_requests" / "CR-DEF-001.md", change_request_text())

            self.assertTrue(any("invalid status" in e for e in validate_case(defect, root / "change_requests")))

    def test_closed_without_builder_retested_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            defect = self.write(
                root / "defects" / "DEF-001.md",
                defect_text(status="CLOSED", builder_retest="NOT_RUN"),
            )
            self.write(root / "change_requests" / "CR-DEF-001.md", change_request_text())

            self.assertTrue(any("CLOSED requires" in e for e in validate_case(defect, root / "change_requests")))

    def test_duplicate_defect_id_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "optimization"
            shutil.copytree(ROOT / "optimization" / "defects", root / "defects")
            shutil.copytree(ROOT / "optimization" / "change_requests", root / "change_requests")
            create_case(root, "DEF-001", "First", "S2_MAJOR", "tester")

            with self.assertRaises(FileExistsError):
                create_case(root, "DEF-001", "Second", "S2_MAJOR", "tester")

    def test_missing_evidence_field_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            defect = self.write(
                root / "defects" / "DEF-001.md",
                defect_text(complete_output=""),
            )
            self.write(root / "change_requests" / "CR-DEF-001.md", change_request_text())

            self.assertTrue(any("complete_output" in e for e in validate_case(defect, root / "change_requests")))

    def test_backend_defect_without_reason_cannot_modify_knowledge(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            change = self.write(
                root / "change_requests" / "CR-DEF-001.md",
                change_request_text(
                    responsible_layer="BACKEND_ACTION",
                    source_files='["knowledge/18_Deliverable_and_Output_Contract.md"]',
                    generated_files="[]",
                    protected_files='["knowledge/18_Deliverable_and_Output_Contract.md"]',
                    owner_required="true",
                    owner_ref="owner-approved",
                    intended="Fix backend response handling.",
                ),
            )

            self.assertTrue(any("Backend Action" in e for e in validate_scope(change)))

    def test_generated_file_without_source_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            change = self.write(
                root / "change_requests" / "CR-DEF-001.md",
                change_request_text(source_files="[]"),
            )

            self.assertTrue(any("generated files" in e for e in validate_scope(change)))

    def test_skeleton_upgrade_to_complete_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            change = self.write(
                root / "change_requests" / "CR-DEF-001.md",
                change_request_text(
                    intended="Upgrade SKELETON_ONLY support to COMPLETE for steam cleaner.",
                ),
            )

            self.assertTrue(any("COMPLETE" in e for e in validate_scope(change)))

    def test_regression_plan_outputs_category_router_tests(self) -> None:
        plan = generate_plan("CATEGORY_ROUTER", ROOT / "optimization" / "REGRESSION_MATRIX.md")

        self.assertIn("R-01", plan)
        self.assertIn("Builder Preview tests", plan)
        self.assertIn("full validation commands", plan)
        self.assertIn("This plan has not executed any test.", plan)

    def test_tools_do_not_execute_git_writes(self) -> None:
        for path in [
            ROOT / "tools" / "create_optimization_case.py",
            ROOT / "tools" / "validate_optimization_case.py",
            ROOT / "tools" / "validate_change_scope.py",
            ROOT / "tools" / "generate_regression_plan.py",
        ]:
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("git add", text)
            self.assertNotIn("git commit", text)
            self.assertNotIn("git push", text)
            self.assertNotIn("subprocess.run(['git'", text)


if __name__ == "__main__":
    unittest.main()
