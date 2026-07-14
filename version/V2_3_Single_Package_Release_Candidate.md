# V2.3 Single Package Release Candidate

```yaml
release_candidate:
  version: "V2.3-RC1"
  primary_package_count: 1
  primary_package: "custom_gpt_package/multi_category_gpt"
  automotive_standalone_release: false
  automotive_regression_tests_included: true
  repository_ready: true
  builder_ready: true
  builder_published: false
  smoke_tests_passed: false
  seedance_api_connected: false
```

## State Boundaries

- `Repository Ready`: source files, build script, generated package, checksums, and source map are internally consistent.
- `Builder Ready`: the single package contains instructions, upload knowledge, builder setup docs, and smoke tests for manual Builder use.
- `Builder Published`: Builder upload and publish has been completed manually.
- `Smoke Tests Passed`: manual Preview verification has passed for the same multi-category GPT.
- `API Execution Ready`: still out of scope in this repository phase.

## Release Position

- `custom_gpt_package/multi_category_gpt` is the only primary release package.
- Automotive Cleaning remains a mature internal category.
- `car_vacuum` remains the only complete Product Pack.
- Home Cleaning, Steam Cleaner, and Beauty Care Tools remain partial or skeleton support.
