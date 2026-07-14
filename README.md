# TikTok Shop Product Video Knowledge System

## Project Positioning

This repository is a document-first production system for TikTok Shop product-video planning.

Current architecture:

- `core/`: reusable logic
- `categories/`: category packs
- `categories/.../products/`: product packs
- `knowledge/`: backward-compatible formal knowledge files
- `workflows/`: routing and handoff rules
- `instructions/`: GPT instruction drafts
- `tests/`: document-level test cases

No external API integration is included in this repo.

---

## Current Maturity

### Maturest Category

- `automotive_cleaning`

### Complete Product Pack

- `car_vacuum`

### Skeleton-Only Areas

- `home_cleaning`
- `home_cleaning/products/steam_cleaner`
- `beauty_care_tools`

These skeletons are not full production knowledge.

---

## Architecture

### Core

Reusable logic such as:

- viral analysis
- commercial script generation
- commercial script scoring
- production planning
- Seedance package generation
- AI quality review

### Category Pack

Adds:

- category psychology
- category proof logic
- category claim boundaries
- category safety assumptions

### Product Pack

Adds:

- product structure
- product jobs to be done
- product proof protocols
- product-specific claim boundaries
- product-specific shooting rules

---

## Routers

### Multi-Category

- `workflows/Category_Router.md`
- `workflows/TikTok_Shop_Product_Video_Main_Router.md`

### Automotive Sub-Router

- `workflows/Car_Cleaning_Main_Router.md`

---

## Seedance Position

Seedance sits after production planning.

Formal chain:

`Category Router -> Category Pack -> Product Pack -> 08 Production Planning -> 09 Seedance Director -> 10 AI Review -> 06 Commercial Scoring`

Seedance does not replace:

- product truth
- product proof
- before/after authenticity

---

## Automotive Cleaning Support

Automotive cleaning remains the highest-confidence category.

The car-vacuum pack supports:

- dedicated hooks
- proof protocols
- claim boundaries
- professional shooting rules
- hybrid and Seedance boundaries

---

## How To Add A Category Pack

1. Create `categories/<category>/README.md`.
2. Add a category-pack file and status marker.
3. Define what is reusable from core and what is category-specific.
4. Update `workflows/Category_Router.md`.
5. Add tests under `tests/`.

## How To Add A Product Pack

1. Create `categories/<category>/products/<product_type>/`.
2. Add product knowledge, psychology, proof, claim, shooting, AI boundary, and test files.
3. Update the category product matrix.
4. Update `workflows/Category_Router.md`.
5. Add product-pack tests.

---

## Document-Level Tests

This repo currently uses document-based test cases.

Key files:

- `tests/test_category_router.md`
- `tests/test_car_vacuum_product_pack.md`
- `tests/test_incomplete_category_fallback.md`
- `tests/test_cross_category_guardrails.md`

Useful local checks:

```bash
git diff --check
rg -n "routing_status|expected_status|expected_result|FAIL_GUARDRAIL" tests categories workflows instructions version
rg -n "SKELETON_ONLY|PARTIAL|UNSUPPORTED" categories workflows instructions version
```

---

## Custom GPT Release Package

The project now has one primary release package:

- `custom_gpt_package/multi_category_gpt/`

Run:

```bash
python3 tools/build_custom_gpt_package.py
```

Current release posture:

- the final product is one multi-category GPT
- automotive cleaning is a mature internal category, not a separate primary GPT
- `car_vacuum` is the only complete Product Pack
- home cleaning, steam cleaner, and beauty care remain skeleton or partial support
- generated package files should not be edited by hand

## Release And Validation

### Build The Primary Package

```bash
python3 tools/build_custom_gpt_package.py
python3 tools/build_custom_gpt_package.py --check
```

### Primary Package Paths

- `custom_gpt_package/README.md`
- `custom_gpt_package/multi_category_gpt/READ_ME_FIRST.md`
- `custom_gpt_package/multi_category_gpt/03_BUILDER_SETUP/RELEASE_MANIFEST.md`

### Check Git Changes

```bash
git status --short
git diff --check
git ls-files --others --exclude-standard
```

### Run Internal Reference Check

```bash
python3 tools/check_markdown_references.py
```

### Run Document-Level Tests

Review:

- `tests/test_category_router.md`
- `tests/test_car_vacuum_product_pack.md`
- `tests/test_incomplete_category_fallback.md`
- `tests/test_cross_category_guardrails.md`

### Manual GPT Builder Upload

1. Open `custom_gpt_package/multi_category_gpt/READ_ME_FIRST.md`.
2. Paste `00_INSTRUCTIONS/MAIN_INSTRUCTIONS.md` into GPT Builder.
3. Upload `01_KNOWLEDGE_UPLOAD/` in the documented order.
4. Do not upload `02_SOURCE_FILES/`, `04_TESTS/`, `05_AUDIT/`, `archive/`, `research/`, or `.DS_Store`.

### Builder Smoke Test Recording

Use:

- `custom_gpt_package/multi_category_gpt/04_TESTS/SMOKE_TEST_CASES.md`
- `custom_gpt_package/multi_category_gpt/04_TESTS/SMOKE_TEST_RESULT_TEMPLATE.md`

### Skeleton Limits

- Home Cleaning is not production-ready.
- Steam Cleaner is high-risk and skeleton-only.
- Beauty Care Tools is skeleton-only.
- Missing product packs must surface `PARTIAL` or `UNSUPPORTED`.

---

## Current Limitation

This repo does not currently include:

- Seedance API calls
- GPT Builder live configuration
- executable production automation
