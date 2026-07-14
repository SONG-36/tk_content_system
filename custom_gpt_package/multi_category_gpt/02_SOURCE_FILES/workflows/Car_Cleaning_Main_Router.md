# Car Cleaning Main Router

## Purpose

This file defines the automotive-cleaning sub-router.

- It is retained as the automotive sub-router inside the single multi-category GPT.
- It is not a separate primary release.
- In the multi-category architecture, it sits below `workflows/Category_Router.md`.

---

## Canonical Flow

`Category Router`
-> `automotive_cleaning`
-> optional product-pack selection
-> `01 Viral Analysis`
-> `02 Psychology`
-> `03 Hook`
-> `04 Visual Mechanism`
-> `05 Script Generation`
-> `07 Professional Shooting`
-> `08 Shot Production Planning`
-> branch by production type
-> `09 Seedance Director` only for AI_GENERATION/HYBRID routed to Seedance
-> mark `10 AI Generation Quality Review` as REQUIRED / NOT_RUN until actual AI media exists
-> `06 Commercial Script Evaluation`

Written as branches:

```text
Category Router
-> automotive_cleaning
-> optional product pack
-> 01 Viral Analysis
-> 02 Psychology
-> 03 Hook
-> 04 Visual Mechanism
-> 05 Script Generation
-> 07 Professional Shooting
-> 08 Shot Production Planning
    -> REAL_SHOOT: Real Production Brief
    -> STOCK_ASSET: Stock Asset Brief
    -> AI_GENERATION + Seedance: 09 Seedance Director, 10 REQUIRED / NOT_RUN
    -> HYBRID + Seedance: Real Production Brief + 09 Seedance Director, 10 REQUIRED / NOT_RUN
-> 10 AI Generation Quality Review only after generated media exists
-> 06 Commercial Script Evaluation
```

---

## Routing Rules

### 1. Upstream Strategy

- Category selection must already resolve to `automotive_cleaning`.
- If `product_type=car_vacuum`, load the dedicated car-vacuum product pack.
- `01` explains why the benchmark content works.
- `02` defines user psychology and purchase drivers.
- `03` selects hook mechanisms.
- `04` selects visual proof and satisfying mechanisms.
- `05` generates three commercial script versions.
- `07` upgrades each script into professional shot language.

### 2. Production Planning

- `08` is the production gate.
- `08` must decide `REAL_SHOOT | AI_GENERATION | HYBRID | STOCK_ASSET`.
- `08` must decide truth dependency before any AI routing.

### 3. Seedance Routing

- `REAL_SHOOT` does not enter `09`.
- `STOCK_ASSET` does not enter `09`.
- `AI_GENERATION + selected_model=Seedance` must enter `09`.
- `HYBRID + selected_model=Seedance` must output both a real brief and `09` input.

### 4. AI Review

- `10` reviews generated material consistency, truth, continuity, and usability.
- `10` is required before AI-generated footage is accepted.
- Prompt-only or storyboard-only outputs must keep `ai_quality_review_status=NOT_RUN`.

### 5. Commercial Review

- `06` reviews hook, visual, product value, conversion, and production feasibility.
- `06` does not replace `10`.
- `10` does not replace `06`.

### 6. Product-Pack Rule

- `car_vacuum` should use the dedicated product pack.
- other automotive products without a dedicated pack should remain in category-level support and declare `PARTIAL` or `GENERIC_SUPPORTED`.

---

## Per-Branch Outputs

### `REAL_SHOOT`

Output:

- real production brief
- required assets
- fallback

### `STOCK_ASSET`

Output:

- stock usage purpose
- stock search queries
- license requirements
- fallback

### `AI_GENERATION + Seedance`

Output:

- `seedance_input` from `08`
- `seedance_production_package` from `09`
- `ai_quality_review_status=NOT_RUN` until actual generated media exists

### `HYBRID + Seedance`

Output:

- real production brief
- `seedance_input` from `08`
- `seedance_production_package` from `09`
- `ai_quality_review_status=NOT_RUN` until actual generated media exists

---

## Final Acceptance Rule

Do not accept final output unless:

- the commercial script can pass `06`
- every AI-generated shot can pass `10`
- no product-truth shot is left as unsupported pure AI
