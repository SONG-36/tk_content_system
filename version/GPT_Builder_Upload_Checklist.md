# GPT Builder Upload Checklist

Historical repository-side checklist from the pre-single-package phase.

For the current formal release flow, use:

- `custom_gpt_package/multi_category_gpt/03_BUILDER_SETUP/BUILDER_CHECKLIST.md`
- `custom_gpt_package/multi_category_gpt/03_BUILDER_SETUP/UPLOAD_ORDER.md`

## Scope

This checklist is for manual GPT Builder verification.

- It does not claim the live Builder is already synced.
- It should be checked manually during upload or release.

---

## 1. Instructions Check

- [ ] Correct release manifest selected before upload
- [ ] Correct GPT package selected: automotive-only or multi-category
- [ ] Instructions include Seedance routing rules
- [ ] Instructions distinguish Knowledge 06 and Knowledge 10
- [ ] Instructions keep high-truth shots out of pure AI generation
- [ ] Instructions require `08 -> 09 -> 10` when Seedance routing is active
- [ ] Multi-category GPT uses `instructions/TikTok_Shop_Product_Video_Director_Main_Instructions.md`
- [ ] Automotive GPT may use `instructions/Car_Cleaning_Custom_GPT_Main_Instructions.md`

---

## 2. Core And Router Upload Check

- [ ] `workflows/Category_Router.md` uploaded for multi-category GPT
- [ ] `workflows/TikTok_Shop_Product_Video_Main_Router.md` uploaded for multi-category GPT
- [ ] `workflows/Car_Cleaning_Main_Router.md` uploaded only when automotive sub-router is needed
- [ ] Knowledge `01` uploaded
- [ ] Knowledge `05` uploaded
- [ ] Knowledge `06` uploaded
- [ ] Knowledge `08` uploaded
- [ ] Knowledge `09` uploaded
- [ ] Knowledge `10` uploaded
- [ ] `seedance_skills/reference-workflow.md` uploaded if reference-role syntax is needed in Builder context

---

## 3. Category And Product Pack Upload Check

- [ ] Automotive category pack uploaded when automotive support is needed
- [ ] Car Vacuum Product Pack uploaded when `car_vacuum` support is needed
- [ ] Home-cleaning skeletons are not misrepresented as complete production knowledge
- [ ] Beauty-care skeletons are not misrepresented as complete production knowledge
- [ ] Steam cleaner skeleton is not misrepresented as production-ready

---

## 4. Exclusion Check

- [ ] `archive/08_Shot_Production_Decision_Framework.md` not uploaded
- [ ] `research/` files not uploaded as formal Knowledge
- [ ] Raw Seedance `SKILL.md` files are not uploaded as duplicate formal Knowledge unless there is a deliberate Builder strategy for them
- [ ] `*_skeleton.md` files are not described as fully supported product knowledge

---

## 5. Routing Check

- [ ] Category Router uploaded
- [ ] `car_vacuum` resolves to automotive_cleaning + car_vacuum product pack
- [ ] incomplete home-cleaning products return `PARTIAL` or `UNSUPPORTED`
- [ ] beauty-care tools require human-demo logic
- [ ] steam cleaner routes with `safety_level=high`
- [ ] `REAL_SHOOT` bypasses Seedance
- [ ] `STOCK_ASSET` bypasses Seedance
- [ ] `AI_GENERATION + selected_model=Seedance` routes to Knowledge 09
- [ ] `HYBRID + selected_model=Seedance` outputs both real brief and Knowledge 09 input
- [ ] high-truth shots cannot remain pure AI generation

---

## 6. Output Contract Check

- [ ] Knowledge 08 outputs production type, truth dependency, selected model, routing flag, and fallback
- [ ] Knowledge 09 outputs full Seedance Production Package
- [ ] Knowledge 10 outputs review status and regeneration or switch instructions
- [ ] Builder prompts do not allow Seedance to fake core product proof
- [ ] Output contains `knowledge_routing_summary`
- [ ] `PARTIAL` and `UNSUPPORTED` states display unsupported gaps instead of fake expertise

---

## 7. Release Check

- [ ] Router files match the uploaded instructions
- [ ] Upload order matches `version/V2_1_Category_Expansion_Structure.md`
- [ ] Selected manifest matches the actual upload set
- [ ] `tests/builder_smoke_test_cases.md` is ready for manual verification
- [ ] `tests/builder_smoke_test_result_template.md` is ready for result capture
- [ ] Manual smoke test covers automotive cleaning
- [ ] Manual smoke test covers `car_vacuum`
- [ ] Manual smoke test covers home-cleaning skeleton behavior
- [ ] Manual smoke test covers beauty-care skeleton behavior
- [ ] Manual smoke test covers steam-cleaner skeleton behavior
- [ ] Incomplete categories do not produce fake professional conclusions
