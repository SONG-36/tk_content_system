# Optimization Framework

This directory implements the manual workflow approved in
`optimization/POST_TEST_OPTIMIZATION_WORKFLOW.md`.

It supports contributors using VS Code, Codex, and GitHub to move a real
Custom GPT defect through:

```text
发现问题 -> 创建 Defect -> 复现 -> 创建 Change Request -> 新分支修复
-> 定向回归 -> 全量验证 -> Pull Request -> Owner 合并
-> Builder 更新 -> Preview 重测 -> CLOSED
```

## Fast Path

1. Confirm the issue is a defect, not a feature request.
2. Create a defect file from `optimization/defects/DEFECT_TEMPLATE.md`.
3. Capture full evidence: Prompt, complete output, expected result, actual
   result, screenshots/files, reproduction count, and test case ID.
4. Reproduce the issue. If it cannot be reproduced, keep status
   `NEEDS_REPRODUCTION` and do not modify Knowledge.
5. Use `optimization/DEFECT_ROUTING_MATRIX.md` to find the smallest responsible
   layer.
6. Create a change request from
   `optimization/change_requests/CHANGE_REQUEST_TEMPLATE.md`.
7. Create a Git branch: `fix/<defect-id>-<description>`.
8. Make the smallest repository change.
9. Run targeted regression from `optimization/REGRESSION_MATRIX.md`.
10. Run full Repository Validation.
11. Open a Pull Request using `.github/PULL_REQUEST_TEMPLATE.md`.
12. Project Owner reviews, merges, updates Builder, runs Preview retest, and
    closes the defect only after Builder retest passes.

## Tools

The Python tools are helpers only. They do not replace Maintainer or Project
Owner judgment.

```bash
python3 tools/create_optimization_case.py --help
python3 tools/validate_optimization_case.py --help
python3 tools/validate_change_scope.py --help
python3 tools/generate_regression_plan.py --help
```

Example:

```bash
python3 tools/create_optimization_case.py \
  --defect-id DEF-001 \
  --title "Home cleaning routed as automotive" \
  --severity S1_CRITICAL
```

The tools never run `git add`, `git commit`, or `git push`.

## Boundaries

- Repository Validation is not Builder Validation.
- `MERGED` is not `CLOSED`.
- `REPOSITORY_VALIDATED` is not `BUILDER_RETESTED`.
- Backend Action defects belong in `backend/` unless the GPT Action contract or
  GPT routing itself is wrong.
- Generated Builder package files must not be edited instead of their source of
  truth.

## Source of Truth

The workflow source of truth is:

- `optimization/POST_TEST_OPTIMIZATION_WORKFLOW.md`

If a template or tool conflicts with that document, the workflow document wins.
