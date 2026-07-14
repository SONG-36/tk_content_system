# Automotive Cleaning Category Pack

## Status

```yaml
automotive_cleaning_category_status:
  status: ACTIVE
  maturity: HIGHEST_CURRENT_CATEGORY
  production_use: READY_WITH_PRODUCT_SPECIFIC_TRUTH_RULES
```

---

## Purpose

This category pack covers automotive cleaning products and scenarios.

It provides:

- automotive user psychology
- automotive cleaning hooks
- automotive cleaning proof logic
- automotive claim boundaries
- category-level routing into product packs

---

## Current Product Support

```yaml
automotive_product_support:
  car_vacuum: COMPLETE
  snow_foam_cannon: GENERIC_SUPPORTED
  detailing_brush: GENERIC_SUPPORTED
  blower_vacuum: PARTIAL
  pressure_washer_accessory: PARTIAL
  crevice_cleaning_tool: PARTIAL
  interior_cleaning_tool: PARTIAL
  car_cleaning_spray: PARTIAL

support_level_definitions:
  COMPLETE: "Dedicated Product Pack exists and is production-ready."
  GENERIC_SUPPORTED: "Category knowledge can support a conservative generic plan, but no complete Product Pack exists."
  PARTIAL: "Routing is possible, but product-specific knowledge gaps must be disclosed."
```

---

## Files

- `categories/automotive_cleaning/category_pack.md`
- `categories/automotive_cleaning/product_matrix.md`
- `categories/automotive_cleaning/material_and_claim_boundaries.md`
- `categories/automotive_cleaning/products/car_vacuum/`
