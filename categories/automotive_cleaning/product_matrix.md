# Automotive Cleaning Product Matrix

| Product Type | Product Pack Status | Strong Hooks | Strong Proof | Truth Dependency |
| --- | --- | --- | --- | --- |
| car_vacuum | COMPLETE | Hidden Dirt / Product Test | Dirt Collection / Transparent Bin | High |
| snow_foam_cannon | GENERIC_SUPPORTED | Transformation | Foam Coverage / Real Rinse | High |
| detailing_brush | GENERIC_SUPPORTED | Hidden Dirt | Dirt Extraction | High |
| Blower Vacuum | PARTIAL | Difficult Area / Product Test | Dust Movement / Collection | High |
| Pressure Washer Accessory | PARTIAL | Visual Impact | Real Water Contact / Real Rinse | High |
| Crevice Cleaning Tool | PARTIAL | Hidden Dirt | Real Reach / Real Contact | High |
| Interior Cleaning Tool | PARTIAL | Problem Reveal | Real Touch / Real Removal | High |
| car_cleaning_spray | PARTIAL | Before/After | Surface Transformation | High |

---

## Interpretation Rules

- `COMPLETE` means a dedicated product pack exists.
- `GENERIC_SUPPORTED` means the category pack plus core rules can support basic work.
- `PARTIAL` means routing may continue, but unsupported gaps must be declared.

If a product pack is not complete:

- do not route to a different product pack
- do not fabricate product-specific claim logic
