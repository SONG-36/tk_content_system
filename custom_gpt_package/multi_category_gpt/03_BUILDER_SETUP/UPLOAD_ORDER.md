# Upload Order

This package defines the only formal GPT release flow for the project.

Status: Builder Ready.

`00_INSTRUCTIONS/MAIN_INSTRUCTIONS.md` is finalized for Builder and is 7195 characters, below the 8000 character limit.

1. Paste `00_INSTRUCTIONS/MAIN_INSTRUCTIONS.md` into GPT Builder -> Instructions.
2. Upload Knowledge `01` through `10`.
3. Upload `01_KNOWLEDGE_UPLOAD/11_Category_and_Main_Router.md`.
4. Upload `01_KNOWLEDGE_UPLOAD/12_Automotive_Category_Pack.md`.
5. Upload `01_KNOWLEDGE_UPLOAD/13_Car_Vacuum_Product_Pack.md`.
6. Upload `01_KNOWLEDGE_UPLOAD/14_Home_Cleaning_Skeleton.md`.
7. Upload `01_KNOWLEDGE_UPLOAD/15_Steam_Cleaner_Skeleton.md`.
8. Upload `01_KNOWLEDGE_UPLOAD/16_Beauty_Care_Tools_Skeleton.md`.
9. Upload `01_KNOWLEDGE_UPLOAD/17_Seedance_Reference_Pack.md`.
10. Upload `01_KNOWLEDGE_UPLOAD/18_Deliverable_and_Output_Contract.md`.
11. Save the GPT configuration.
12. Run Preview smoke tests.
13. Record results.
14. Publish only after passing manual review.

Knowledge 18 defines final delivery format, file naming, script headers, shot contracts, Seedance package output, AI review timing, and file generation honesty. It does not replace category routing, Product Truth/Safety rules, Knowledge 08 production planning, Knowledge 09 Seedance direction, Knowledge 10 AI review, or Knowledge 06 scoring.

## Do Not Upload

- `00_INSTRUCTIONS/MAIN_INSTRUCTIONS.md` as ordinary Knowledge
- automotive-only instructions
- automotive standalone manifest
- `02_SOURCE_FILES/`
- `04_TESTS/`
- `05_AUDIT/`
- `archive/`
- `research/`
- `tests/`
- `tools/`
- `version/`
- `release_manifests/`
- V1 legacy docs
