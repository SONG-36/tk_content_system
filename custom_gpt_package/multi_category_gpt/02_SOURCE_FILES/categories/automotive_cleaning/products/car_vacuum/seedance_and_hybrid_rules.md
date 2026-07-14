# Car Vacuum Seedance And Hybrid Rules

## Must Be `REAL_SHOOT`

- real suction proof
- dirt intake
- pet hair removal
- crumb collection
- transparent dust-bin result
- product buttons, ports, and attachments
- attachment installation
- before/after proof
- runtime, noise, or performance tests

---

## Allowed `AI_GENERATION`

- non-proof luxury interior hook
- premium garage environment
- pure atmosphere transition
- abstract dust-anxiety visual
- opening visual that does not prove product ability

AI may only carry non-proof Hook, premium environment, lighting, transition, and supporting atmosphere.

---

## Allowed `HYBRID`

- real product plus AI premium car interior
- real hand and product plus non-proof environment enhancement
- real hero product plus AI lighting or background
- real cleaning action surrounded by non-proof atmosphere enhancement

---

## Hybrid Boundary

```yaml
hybrid_layer_definition:
  real_layer:
    - product
    - attachments
    - human_hand
    - product_contact
    - dirt_intake
    - result_proof
  ai_layer:
    - background_environment
    - non-functional atmosphere
    - lighting_enhancement
    - non-proof transition
  proof_layer_owner: "REAL_SHOOT"
  ai_must_not_rewrite:
    - actual product
    - actual SKU structure
    - actual proof
    - accessories
    - buttons
    - logo
```

---

## Prohibited

- Seedance generating core debris-intake proof
- AI changing attachment structure
- AI adding nonexistent accessories
- AI generating wrong logo or wrong buttons
- AI making untouched dirt disappear
- AI generating fake before/after

## Template Priority

Car Vacuum script templates provide product-specific structure only.

They must not override:

- Knowledge 07 professional shot requirements
- Knowledge 08 production type decisions
- Knowledge 10 AI review timing
