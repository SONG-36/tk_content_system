# Car Vacuum Claim Boundary

## Claim Levels

### Level A: Directly Demonstrable

- product powers on
- an attachment enters a shown gap
- transparent dust bin shows collected debris
- attachments can be installed
- one-hand holding is possible

### Level B: Controlled-Test Claims

- picking up sand, hair, or heavier debris
- runtime
- noise
- filtration performance
- blower performance
- multi-scene consistency

### Level C: Do Not State Without Evidence

- strongest suction in the market
- suction never fades
- completely silent
- works for all vehicles and all scenarios
- supports liquid pickup unless explicitly supported
- medical-grade HEPA unless certified
- removes all pet hair in one pass
- cleaner than professional detailing
- never clogs
- absolute battery safety
- compatible with all chargers
- runtime that differs from verified product evidence

---

## Review Schema

```yaml
claim_review:
  proposed_claim: ""
  claim_level: "A | B | C"
  evidence_required: []
  approved_wording: ""
  prohibited_wording: ""
  production_proof_required: true
```

---

## Output Rule

If evidence is missing:

- downgrade wording
- remove absolute language
- avoid comparative superlatives
