# Release Gate

```yaml
release_gate:
  target_defects_fixed: true
  targeted_regression_passed: true
  repository_validation_passed: true
  builder_updated: true
  original_failure_cases_retested: true
  core_smoke_tests_passed: true
  open_s0: 0
  open_s1: 0
  open_s2: 0
  product_truth_not_weakened: true
  safety_not_weakened: true
  support_levels_not_silently_upgraded: true
```

## Required Meaning

- `target_defects_fixed`: all defects targeted by the release have a merged fix.
- `targeted_regression_passed`: each defect's targeted regression plan passed.
- `repository_validation_passed`: repository validators and build checks passed.
- `builder_updated`: Project Owner updated GPT Builder test configuration.
- `original_failure_cases_retested`: the exact failing prompts were rerun.
- `core_smoke_tests_passed`: core Builder smoke tests passed in Preview.
- `open_s0`, `open_s1`, `open_s2`: no unresolved blocker, critical, or major defects remain.
- `product_truth_not_weakened`: Product Truth guardrails remain equal or stronger.
- `safety_not_weakened`: safety and claim boundaries remain equal or stronger.
- `support_levels_not_silently_upgraded`: no skeleton or partial category was silently promoted to `COMPLETE`.

## Non-Equivalence Rules

- `MERGED` does not equal `CLOSED`.
- `REPOSITORY_VALIDATED` does not equal `BUILDER_RETESTED`.
- Repository PASS does not equal Builder PASS.

Only the Project Owner can approve release after Builder Preview retest.
