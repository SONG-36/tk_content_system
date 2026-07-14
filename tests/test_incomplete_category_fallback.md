# Test Incomplete Category Fallback

## Cases

```yaml
- id: "fallback_01"
  scenario: "Home electric scrubber without product pack"
  expected_status: "PARTIAL"
  expected_gap_behavior: "declare unsupported knowledge gaps"

- id: "fallback_02"
  scenario: "Steam cleaner with 100 percent sterilization claim"
  expected_status: "BLOCK"
  expected_gap_behavior: "require evidence"

- id: "fallback_03"
  scenario: "Beauty tool requests AI before and after proof"
  expected_status: "BLOCK"
  expected_fallback: "REAL_SHOOT or explicit unsupported warning"
```

---

## Pass Rule

Pass if incomplete categories never present themselves as production-ready expert systems.
