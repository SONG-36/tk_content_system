# V2.2 Release Candidate

This document records the repository-ready dual-manifest checkpoint from the previous phase.

The current primary release path is the single-package flow recorded in `version/V2_3_Single_Package_Release_Candidate.md`.

```yaml
release_candidate:
  version: "V2.2-RC1"
  repository_status: "REPOSITORY_READY_BUILDER_READY_PENDING_MANUAL_UPLOAD"
  automotive_gpt_manifest: "release_manifests/automotive_gpt_manifest.md"
  multi_category_gpt_manifest: "release_manifests/multi_category_gpt_manifest.md"
  tracked_files_complete: true
  static_checks_passed: true
  builder_published: false
  builder_smoke_tests_passed: false
  seedance_api_connected: false
```

## State Boundaries

- `Repository Ready`: repository structure, files, and references are internally consistent.
- `Builder Ready`: upload manifests, smoke tests, and instructions are ready for manual Builder use.
- `Builder Published`: Builder upload and publish has been completed manually.
- `Prompt Production Ready`: manual Builder smoke tests passed.
- `API Execution Ready`: out of scope in this repository stage.

Current state must not be presented as Builder Published.
