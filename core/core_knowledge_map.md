# Core Knowledge Map

## Purpose

This file explains how the existing `knowledge/01-10` set maps into the new:

- `core`
- `category pack`
- `product pack`

architecture without breaking backward compatibility.

---

## Reusability Audit

| File | Current Role | Reusability | Notes |
| --- | --- | --- | --- |
| `knowledge/01_TikTok_Viral_Analysis_Framework.md` | Viral analysis | `CORE_REUSABLE` | Structure is broadly reusable across categories. |
| `knowledge/02_Car_Cleaning_Content_Psychology.md` | Automotive cleaning psychology | `AUTOMOTIVE_CATEGORY_SCOPED` | Strong car-cleaning language. |
| `knowledge/03_Cleaning_Video_Hook_Database.md` | Cleaning hooks | `PARTIALLY_REUSABLE` | Hook mechanics can transfer, examples are automotive-cleaning heavy. |
| `knowledge/04_Satisfying_Cleaning_Visual_Library.md` | Cleaning visual proof | `PARTIALLY_REUSABLE` | Proof logic transfers, scenarios remain cleaning-specific. |
| `knowledge/05_TikTok_Shop_Script_Writing_Rules.md` | Script generation | `CORE_REUSABLE_WITH_CATEGORY_INPUTS` | Should be fed with category/product packs. |
| `knowledge/06_Video_Script_Scoring_System.md` | Commercial scoring | `CORE_REUSABLE` | Applies to all categories with proper inputs. |
| `knowledge/07_Professional_Shooting_Standard.md` | Automotive-oriented shooting standard | `PARTIALLY_REUSABLE` | Shot schema is reusable, examples remain car-cleaning oriented. |
| `knowledge/08_Shot_Production_Planning_Framework.md` | Production planning and AI routing | `CORE_REUSABLE` | Truth-first logic is category-agnostic. |
| `knowledge/09_Seedance_Generation_Director.md` | Seedance package generation | `CORE_REUSABLE_WITH_TRUTH_BOUNDARY` | Reusable only after category/product truth rules are loaded. |
| `knowledge/10_AI_Generation_Quality_Review.md` | AI asset review | `CORE_REUSABLE` | Reusable with category-specific failure checks. |

---

## Current Category-Limited Areas

Strong automotive-cleaning language currently exists in:

- `knowledge/02_Car_Cleaning_Content_Psychology.md`
- `knowledge/03_Cleaning_Video_Hook_Database.md`
- `knowledge/04_Satisfying_Cleaning_Visual_Library.md`
- `knowledge/07_Professional_Shooting_Standard.md`
- `instructions/Car_Cleaning_Custom_GPT_Main_Instructions.md`
- `workflows/Car_Cleaning_Main_Router.md`

---

## Migration Rule

Until a dedicated generalized replacement exists:

- keep legacy files active
- do not remove them
- use `categories/automotive_cleaning/` to document their scoped meaning
- use `workflows/Category_Router.md` to stop accidental cross-category reuse
