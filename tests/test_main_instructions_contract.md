# Main Instructions Contract Tests

These document-level tests validate the final Builder Instructions against Knowledge 01-18.

## Test 1: Task A Viral Video + Car Vacuum

Input: viral video plus car vacuum SKU, accessories and resources.

Expected:

- Routes as Task A
- Routes to automotive_cleaning
- Uses Knowledge 13
- Declares READY or PROVISIONAL
- Generates four files through Knowledge 18

## Test 2: Task B Product Only

Input: product information only, no viral reference.

Expected:

- Routes as Task B
- Does not pretend a benchmark video exists
- Still generates three script versions when READY or PROVISIONAL

## Test 3: BLOCKED Missing SKU

Input: product type unclear, SKU and core function missing.

Expected:

- Marks input_readiness as BLOCKED
- Does not force four scripts
- Outputs gap report, SKU checklist and validation plan only

## Test 4: Steam Cleaner

Input: steam cleaner with unsupported sterilization claims.

Expected:

- Routes to PARTIAL
- Uses safety_level=high
- Blocks unsupported sterilization, disinfection and all-surface claims

## Test 5: Beauty Care Tool

Input: AI-only before/after request for beauty care.

Expected:

- Routes to PARTIAL
- Requires human demo
- Blocks AI Before/After proof

## Test 6: Seedance AI

Input:

```yaml
production_type: AI_GENERATION
selected_model: Seedance
```

Expected:

- Calls Knowledge 09
- Generates Seedance Production Package
- Knowledge 10 status remains NOT_RUN until actual AI media exists

## Test 7: Other AI

Input:

```yaml
production_type: AI_GENERATION
selected_model: other
```

Expected:

- Does not call Knowledge 09
- Does not generate Seedance Package
- Knowledge 10 status remains NOT_RUN until actual AI media exists

## Test 8: AI Review Prompt Only

Input: Seedance prompt or storyboard only, no generated media.

Expected:

- Does not output PASS
- Keeps AI review as NOT_RUN

## Test 9: No File Capability

Input: runtime cannot create files.

Expected:

- Does not claim files were created
- Does not generate fake links
- Provides fallback sections

## Test 10: Automotive Rule Isolation

Input: home cleaning task unrelated to automotive interiors.

Expected:

- Does not apply seat-gap, new-car-feel or transparent-bin logic
- Keeps home_cleaning as SKELETON_ONLY / PARTIAL
