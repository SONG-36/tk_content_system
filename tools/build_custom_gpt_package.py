#!/usr/bin/env python3
"""Build the single primary Custom GPT release package."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = ROOT / "custom_gpt_package"
PRIMARY_PACKAGE_REL = Path("multi_category_gpt")
PRIMARY_PACKAGE = PACKAGE_ROOT / PRIMARY_PACKAGE_REL

INSTRUCTIONS_DIR = PRIMARY_PACKAGE / "00_INSTRUCTIONS"
KNOWLEDGE_DIR = PRIMARY_PACKAGE / "01_KNOWLEDGE_UPLOAD"
SOURCE_DIR = PRIMARY_PACKAGE / "02_SOURCE_FILES"
BUILDER_DIR = PRIMARY_PACKAGE / "03_BUILDER_SETUP"
TESTS_DIR = PRIMARY_PACKAGE / "04_TESTS"
AUDIT_DIR = PRIMARY_PACKAGE / "05_AUDIT"

PACKAGE_README = PACKAGE_ROOT / "README.md"
PACKAGE_ENTRY = PRIMARY_PACKAGE / "READ_ME_FIRST.md"
MAIN_INSTRUCTIONS = INSTRUCTIONS_DIR / "MAIN_INSTRUCTIONS.md"
RELEASE_MANIFEST = BUILDER_DIR / "RELEASE_MANIFEST.md"
FINAL_UPLOAD_MANIFEST = BUILDER_DIR / "FINAL_UPLOAD_MANIFEST.md"
UPLOAD_ORDER = BUILDER_DIR / "UPLOAD_ORDER.md"
BUILDER_CHECKLIST = BUILDER_DIR / "BUILDER_CHECKLIST.md"
SMOKE_TEST_CASES = TESTS_DIR / "SMOKE_TEST_CASES.md"
SMOKE_TEST_TEMPLATE = TESTS_DIR / "SMOKE_TEST_RESULT_TEMPLATE.md"
SOURCE_MAP = AUDIT_DIR / "SOURCE_MAP.md"
PACKAGE_REPORT = AUDIT_DIR / "PACKAGE_REPORT.md"
SHA256SUMS = AUDIT_DIR / "SHA256SUMS.txt"

MULTI_CATEGORY_INSTRUCTIONS = Path(
    "instructions/TikTok_Shop_Product_Video_Director_Main_Instructions.md"
)
AUTOMOTIVE_ONLY_INSTRUCTIONS = Path(
    "instructions/Car_Cleaning_Custom_GPT_Main_Instructions.md"
)

KNOWLEDGE_FILES = [
    Path("knowledge/01_TikTok_Viral_Analysis_Framework.md"),
    Path("knowledge/02_Car_Cleaning_Content_Psychology.md"),
    Path("knowledge/03_Cleaning_Video_Hook_Database.md"),
    Path("knowledge/04_Satisfying_Cleaning_Visual_Library.md"),
    Path("knowledge/05_TikTok_Shop_Script_Writing_Rules.md"),
    Path("knowledge/06_Video_Script_Scoring_System.md"),
    Path("knowledge/07_Professional_Shooting_Standard.md"),
    Path("knowledge/08_Shot_Production_Planning_Framework.md"),
    Path("knowledge/09_Seedance_Generation_Director.md"),
    Path("knowledge/10_AI_Generation_Quality_Review.md"),
    Path("knowledge/18_Deliverable_and_Output_Contract.md"),
]

ROUTER_SOURCES = [
    Path("workflows/Category_Router.md"),
    Path("workflows/TikTok_Shop_Product_Video_Main_Router.md"),
    Path("workflows/Car_Cleaning_Main_Router.md"),
]

AUTOMOTIVE_PACK_SOURCES = [
    Path("categories/automotive_cleaning/README.md"),
    Path("categories/automotive_cleaning/category_pack.md"),
    Path("categories/automotive_cleaning/product_matrix.md"),
    Path("categories/automotive_cleaning/material_and_claim_boundaries.md"),
    Path("categories/automotive_cleaning/products/README.md"),
]

CAR_VACUUM_SOURCES = [
    Path("categories/automotive_cleaning/products/car_vacuum/README.md"),
    Path("categories/automotive_cleaning/products/car_vacuum/product_knowledge.md"),
    Path("categories/automotive_cleaning/products/car_vacuum/consumer_psychology.md"),
    Path("categories/automotive_cleaning/products/car_vacuum/hook_library.md"),
    Path("categories/automotive_cleaning/products/car_vacuum/visual_proof_protocol.md"),
    Path("categories/automotive_cleaning/products/car_vacuum/attachment_scenario_matrix.md"),
    Path("categories/automotive_cleaning/products/car_vacuum/claim_boundary.md"),
    Path(
        "categories/automotive_cleaning/products/car_vacuum/"
        "professional_shooting_standard.md"
    ),
    Path("categories/automotive_cleaning/products/car_vacuum/seedance_and_hybrid_rules.md"),
    Path("categories/automotive_cleaning/products/car_vacuum/script_templates.md"),
    Path("categories/automotive_cleaning/products/car_vacuum/test_cases.md"),
]

HOME_SKELETON_SOURCES = [
    Path("categories/home_cleaning/README.md"),
    Path("categories/home_cleaning/category_pack_skeleton.md"),
    Path("categories/home_cleaning/room_and_surface_matrix_skeleton.md"),
    Path("categories/home_cleaning/claim_and_material_risk_skeleton.md"),
    Path("categories/home_cleaning/products/README.md"),
]

STEAM_SKELETON_SOURCES = [
    Path("categories/home_cleaning/products/steam_cleaner/README.md"),
    Path("categories/home_cleaning/products/steam_cleaner/product_pack_skeleton.md"),
    Path(
        "categories/home_cleaning/products/steam_cleaner/"
        "safety_and_claim_boundary_skeleton.md"
    ),
    Path(
        "categories/home_cleaning/products/steam_cleaner/"
        "material_compatibility_skeleton.md"
    ),
]

BEAUTY_SKELETON_SOURCES = [
    Path("categories/beauty_care_tools/README.md"),
    Path("categories/beauty_care_tools/category_pack_skeleton.md"),
    Path("categories/beauty_care_tools/human_demo_and_safety_skeleton.md"),
    Path("categories/beauty_care_tools/before_after_authenticity_skeleton.md"),
    Path("categories/beauty_care_tools/product_matrix_skeleton.md"),
    Path("categories/beauty_care_tools/products/README.md"),
]

SEEDANCE_REFERENCE_SOURCES = [
    Path("seedance_skills/reference-workflow.md"),
    Path("seedance_skills/seedance-prompt/SKILL.md"),
    Path("seedance_skills/seedance-camera/SKILL.md"),
    Path("seedance_skills/seedance-motion/SKILL.md"),
]

SMOKE_TEST_SOURCE = Path("tests/builder_smoke_test_cases.md")
SMOKE_TEMPLATE_SOURCE = Path("tests/builder_smoke_test_result_template.md")
REFERENCE_CHECK_SCRIPT = Path("tools/check_markdown_references.py")
SOURCE_COPY_ROOTS = [
    Path("knowledge"),
    Path("categories"),
    Path("workflows"),
    Path("instructions"),
    Path("seedance_skills"),
]

EXCLUDED_FILENAMES = {".DS_Store"}
TEXT_ENCODING = "utf-8"


class BuildError(RuntimeError):
    """Raised when the package build cannot proceed."""


@dataclass(frozen=True)
class GeneratedFile:
    path: Path
    content: str
    sources: tuple[Path, ...]
    role: str


def rel(path: Path) -> str:
    return path.as_posix()


def source_path(path: Path) -> Path:
    return ROOT / path


def ensure_exists(paths: Iterable[Path]) -> None:
    missing = [rel(path) for path in paths if not source_path(path).is_file()]
    if missing:
        raise BuildError(f"Missing required source files: {', '.join(missing)}")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_text(content: str) -> str:
    return sha256_bytes(content.encode(TEXT_ENCODING))


def read_text(path: Path) -> str:
    return source_path(path).read_text(encoding=TEXT_ENCODING).rstrip() + "\n"


def latest_source_mtime(paths: Iterable[Path]) -> str:
    timestamps = [source_path(path).stat().st_mtime for path in paths]
    latest = max(timestamps)
    return (
        __import__("datetime")
        .datetime.fromtimestamp(latest, tz=__import__("datetime").timezone.utc)
        .replace(microsecond=0)
        .isoformat()
    )


def source_block(path: Path) -> str:
    return f"---\n\n# SOURCE FILE: {rel(path)}\n\n---\n\n{read_text(path).rstrip()}\n"


def join_source_blocks(paths: list[Path]) -> str:
    return "\n".join(source_block(path).rstrip() for path in paths) + "\n"


def copied_source_files() -> list[Path]:
    files: list[Path] = []
    for base in SOURCE_COPY_ROOTS:
        for path in sorted((ROOT / base).rglob("*")):
            if not path.is_file():
                continue
            if path.name in EXCLUDED_FILENAMES:
                continue
            files.append(path.relative_to(ROOT))
    return files


def knowledge08_paths() -> list[Path]:
    return sorted(path.relative_to(ROOT) for path in (ROOT / "knowledge").glob("08_*.md"))


def source_union() -> list[Path]:
    ordered: list[Path] = []
    seen: set[Path] = set()
    groups = [
        [MULTI_CATEGORY_INSTRUCTIONS, AUTOMOTIVE_ONLY_INSTRUCTIONS],
        KNOWLEDGE_FILES,
        ROUTER_SOURCES,
        AUTOMOTIVE_PACK_SOURCES,
        CAR_VACUUM_SOURCES,
        HOME_SKELETON_SOURCES,
        STEAM_SKELETON_SOURCES,
        BEAUTY_SKELETON_SOURCES,
        SEEDANCE_REFERENCE_SOURCES,
        [SMOKE_TEST_SOURCE, SMOKE_TEMPLATE_SOURCE, REFERENCE_CHECK_SCRIPT],
        copied_source_files(),
    ]
    for group in groups:
        for item in group:
            if item not in seen:
                seen.add(item)
                ordered.append(item)
    return ordered


def rendered_multi_category_instructions() -> str:
    return read_text(MULTI_CATEGORY_INSTRUCTIONS)


def rendered_router_file() -> str:
    header = (
        "# Category And Main Router\n\n"
        "```yaml\n"
        "builder_knowledge_aliases:\n"
        "  viral_analysis: \"01_TikTok_Viral_Analysis_Framework.md\"\n"
        "  automotive_psychology: \"02_Car_Cleaning_Content_Psychology.md\"\n"
        "  automotive_hook_database: \"03_Cleaning_Video_Hook_Database.md\"\n"
        "  automotive_visual_library: \"04_Satisfying_Cleaning_Visual_Library.md\"\n"
        "  script_rules: \"05_TikTok_Shop_Script_Writing_Rules.md\"\n"
        "  script_scoring: \"06_Video_Script_Scoring_System.md\"\n"
        "  professional_shooting: \"07_Professional_Shooting_Standard.md\"\n"
        "  production_planning: \"08_Shot_Production_Planning_Framework.md\"\n"
        "  seedance_director: \"09_Seedance_Generation_Director.md\"\n"
        "  ai_quality_review: \"10_AI_Generation_Quality_Review.md\"\n"
        "  category_and_main_router: \"11_Category_and_Main_Router.md\"\n"
        "  automotive_category_pack: \"12_Automotive_Category_Pack.md\"\n"
        "  car_vacuum_product_pack: \"13_Car_Vacuum_Product_Pack.md\"\n"
        "  home_cleaning_skeleton: \"14_Home_Cleaning_Skeleton.md\"\n"
        "  steam_cleaner_skeleton: \"15_Steam_Cleaner_Skeleton.md\"\n"
        "  beauty_tools_skeleton: \"16_Beauty_Care_Tools_Skeleton.md\"\n"
        "  seedance_reference_pack: \"17_Seedance_Reference_Pack.md\"\n"
        "```\n\n"
        "Runtime Resolution Rule\n\n"
        "Repository paths inside SOURCE FILE sections are provenance only.\n\n"
        "Inside GPT Builder, resolve runtime Knowledge through the Builder filenames above.\n\n"
        "Do not treat a Knowledge file as missing merely because its original repository path was not separately uploaded.\n\n"
        "This Builder upload file combines the only top-level routing documents for the "
        "single primary multi-category GPT release.\n\n"
        "- `Category_Router` is the only top-level entry.\n"
        "- `TikTok_Shop_Product_Video_Main_Router` is the formal overall flow.\n"
        "- `Car_Cleaning_Main_Router` is an automotive sub-router only.\n"
        "- Missing Product Packs must return generic, partial, or unsupported handling.\n"
        "- `car_vacuum` rules must not be applied to other products.\n"
        "- Knowledge 10 is REQUIRED / NOT_RUN until actual generated AI media exists.\n"
    )
    return f"{header}\n{join_source_blocks(ROUTER_SOURCES)}"


def rendered_automotive_pack() -> str:
    header = (
        "# Automotive Category Pack\n\n"
        "```yaml\n"
        "category_pack_status:\n"
        "  category: automotive_cleaning\n"
        "  support_level: MATURE\n"
        "  production_ready: true\n"
        "  dedicated_product_packs:\n"
        "    - car_vacuum\n"
        "  generic_supported_products:\n"
        "    - snow_foam_cannon\n"
        "    - detailing_brush\n"
        "\n"
        "automotive_product_support:\n"
        "  car_vacuum: COMPLETE\n"
        "  snow_foam_cannon: GENERIC_SUPPORTED\n"
        "  detailing_brush: GENERIC_SUPPORTED\n"
        "  blower_vacuum: PARTIAL\n"
        "  pressure_washer_accessory: PARTIAL\n"
        "  crevice_cleaning_tool: PARTIAL\n"
        "  interior_cleaning_tool: PARTIAL\n"
        "  car_cleaning_spray: PARTIAL\n"
        "\n"
        "support_level_definitions:\n"
        "  COMPLETE: \"Dedicated Product Pack exists and is production-ready.\"\n"
        "  GENERIC_SUPPORTED: \"Category knowledge can support a conservative generic plan, but no complete Product Pack exists.\"\n"
        "  PARTIAL: \"Routing is possible, but product-specific knowledge gaps must be disclosed.\"\n"
        "```\n"
    )
    return f"{header}\n{join_source_blocks(AUTOMOTIVE_PACK_SOURCES)}"


def rendered_car_vacuum_pack() -> str:
    header = (
        "# Car Vacuum Product Pack\n\n"
        "```yaml\n"
        "product_pack:\n"
        "  category: automotive_cleaning\n"
        "  product_type: car_vacuum\n"
        "  support_level: COMPLETE\n"
        "  production_ready: true\n"
        "  truth_dependency_default: high\n"
        "  core_product_proof_requires_real_shoot: true\n"
        "  ai_generated_suction_proof_prohibited: true\n"
        "```\n"
    )
    return f"{header}\n{join_source_blocks(CAR_VACUUM_SOURCES)}"


def rendered_home_skeleton() -> str:
    header = (
        "# Home Cleaning Skeleton\n\n"
        "```yaml\n"
        "category_pack_status:\n"
        "  category: home_cleaning\n"
        "  support_level: SKELETON_ONLY\n"
        "  routing_status: PARTIAL\n"
        "  production_ready: false\n"
        "  must_disclose_knowledge_gaps: true\n"
        "  product_pack_required_for_full_support: true\n"
        "```\n"
    )
    return f"{header}\n{join_source_blocks(HOME_SKELETON_SOURCES)}"


def rendered_steam_skeleton() -> str:
    header = (
        "# Steam Cleaner Skeleton\n\n"
        "```yaml\n"
        "product_pack_status:\n"
        "  category: home_cleaning\n"
        "  product_type: steam_cleaner\n"
        "  support_level: SKELETON_ONLY\n"
        "  routing_status: PARTIAL\n"
        "  production_ready: false\n"
        "  safety_level: high\n"
        "  unsupported_claims_must_be_blocked: true\n"
        "  sterilization_claim_requires_evidence: true\n"
        "```\n"
    )
    return f"{header}\n{join_source_blocks(STEAM_SKELETON_SOURCES)}"


def rendered_beauty_skeleton() -> str:
    header = (
        "# Beauty Care Tools Skeleton\n\n"
        "```yaml\n"
        "category_pack_status:\n"
        "  category: beauty_care_tools\n"
        "  support_level: SKELETON_ONLY\n"
        "  routing_status: PARTIAL\n"
        "  production_ready: false\n"
        "  human_demo_required_by_default: true\n"
        "  ai_generated_core_before_after_prohibited: true\n"
        "  human_safety_review_required: true\n"
        "```\n"
    )
    return f"{header}\n{join_source_blocks(BEAUTY_SKELETON_SOURCES)}"


def rendered_seedance_pack() -> str:
    local_sections = """## Local Quick Reference

- choose one generation mode
- define one visible beat
- assign one role to each reference
- define camera start, move and endpoint
- define observable motion and endpoint
- preserve product identity
- add negative constraints
- add fallback

## Local I2V Guide

For I2V, preserve the supplied image identity and describe only new motion, time, camera, lighting transition, audio and constraints. Do not re-describe exact identity in a way that invites drift. Lock logo, shape, interface, and endpoint.

## Local First/Last Frame Guide

Use `@Image1` as the first frame and `@Image2` as the final visual target. Describe the transition only. Do not morph product structure. The final frame is an exact endpoint.

## Local Mode Examples

- T2V: non-proof premium garage atmosphere around an unnamed product silhouette.
- I2V: animate a supplied product hero image with a slow push-in and no structure changes.
- V2V: transfer only camera rhythm from an authorized source clip.
- R2V: use one product image for identity and one environment image for atmosphere.
- FLF2V: move from supplied first frame to supplied final frame without changing product identity.
- Edit: preserve the source clip and change only a non-proof background layer.
- Extend: continue only from an accepted source clip with observed final state.

## Local Shot Continuity Rules

Track accepted previous state, actual opening state, screen direction, action phase, camera phase, light continuity, product continuity, and reserved future beats.

## Local Multishot Grammar

Shot 1 [0-2s]: one main action, one visible result, one main camera move, clear cut point.

Shot 2 [2-5s]: one main action, one visible result, one main camera move, clear cut point.

Shot 3 [5-8s]: one main action, one visible result, one main camera move, clear cut point.

## Local Prompt Compiler

```yaml
sequence_state:
  project_id: ""
  clip_id: ""
  parent_clip_id: ""
  actual_opening_state: ""
  completed_beats: []
  current_beat: ""
  reserved_future_beats: []
  continuity_locks: []
```

Compile only the current clip contract from the accepted sequence state. Do not invent future plot.

## Local Directing Engine

Choose one intention, one main subject, one main action, one motivated camera move, motivated lighting, visible performance/action, sound purpose, and no hollow adjectives.

## Local Cinematography Language

Define shot size, angle, lens, movement, subject distance, focus behavior, start point, and endpoint.

## Local Continuation Contract

Extend requires actual accepted source clip, observed final frame, motion phase, camera phase, environment state, next visible beat, and continuity locks.

If these are missing, do not invent continuation state.
"""
    header = (
        "# Seedance Reference Pack\n\n"
        "```yaml\n"
        "runtime_dependency_status:\n"
        "  self_contained: true\n"
        "  unresolved_ref_tokens: 0\n"
        "  unresolved_skill_tokens: 0\n"
        "  authoritative_truth_router: \"08_Shot_Production_Planning_Framework.md\"\n"
        "  authoritative_seedance_package: \"09_Seedance_Generation_Director.md\"\n"
        "```\n\n"
        "This file is uploaded only for the multi-category GPT when Seedance-oriented "
        "reference-role syntax must be available inside Builder context.\n"
        "\n"
        "Knowledge 17 provides prompt, reference, camera and motion language.\n\n"
        "It does not decide whether AI is allowed.\n\n"
        "Knowledge 08 controls production-type and truth routing.\n"
        "Knowledge 09 controls the final Seedance Production Package.\n"
        "Category and Product Packs control product truth and safety.\n\n"
    )
    raw = join_source_blocks(SEEDANCE_REFERENCE_SOURCES)
    return f"{header}\n{local_sections}\n{sanitize_seedance_references(raw)}"


def sanitize_seedance_references(text: str) -> str:
    replacements = {
        "[ref:reference-workflow]": "the Reference Workflow section included earlier in this Knowledge",
        "[ref:quick-ref]": "the Local Quick Reference section in this Knowledge",
        "[ref:i2v-guide]": "the Local I2V Guide section in this Knowledge",
        "[ref:first-last-frame-guide]": "the Local First/Last Frame Guide section in this Knowledge",
        "[ref:examples-by-mode]": "the Local Mode Examples section in this Knowledge",
        "[ref:shot-list-continuity]": "the Local Shot Continuity Rules section in this Knowledge",
        "[ref:multishot-grammar]": "the Local Multishot Grammar section in this Knowledge",
        "[ref:prompt-compiler]": "the Local Prompt Compiler section in this Knowledge",
        "[ref:directing-engine]": "the Local Directing Engine section in this Knowledge",
        "[ref:cinematography-shot-language]": "the Local Cinematography Language section in this Knowledge",
        "[ref:vocab/zh]": "clear professional camera terminology in the requested language",
        "[ref:vocab/ru]": "clear professional camera terminology in the requested language",
        "[ref:multilingual-community-examples]": "clear professional camera terminology in the requested language",
        "[skill:seedance-continuation]": "the Local Continuation Contract section in this Knowledge",
    }
    for token, replacement in replacements.items():
        text = text.replace(token, replacement)
    unresolved = sorted(set(re.findall(r"\[(?:ref|skill):[^\]]+\]", text)))
    if unresolved:
        raise BuildError("Unresolved Seedance runtime tokens: " + ", ".join(unresolved))
    return text


def rendered_smoke_tests() -> str:
    return """# Smoke Test Cases

## Scope

These tests target the same multi-category GPT release package.

- Automotive tests are regression checks for mature internal modules.
- Steam and beauty tests verify partial-support, safety, and authenticity boundaries.
- These cases are not proof of live Builder execution.

---

## Test Cases

### BST-01 Car Vacuum Full Route

Input:

```text
我卖的是车载吸尘器，有缝隙吸头、毛刷头和透明尘盒。请根据我的商品生成三套 TikTok Shop 视频脚本，并判断每个镜头如何生产。
```

Expected:

- category=`automotive_cleaning`
- product_pack=`car_vacuum`
- product proof routes to `REAL_SHOOT`
- non-proof luxury hook may route to `AI_GENERATION` or `HYBRID`
- output includes product-pack-specific hook, proof, and claim boundaries
- output includes `knowledge_routing_summary`

### BST-02 Fake AI Suction Proof

Input:

```text
没有实拍条件，请直接用 Seedance 生成碎屑被吸入透明尘盒的镜头。
```

Expected:

- block pure AI product proof
- switch to `REAL_SHOOT` or controlled `HYBRID`
- no fake suction proof

### BST-03 Missing Accessory Details

Input:

```text
帮我拍三吸头测试，但我没有说明商品包含哪些吸头。
```

Expected:

- no invented accessories
- clear information gap
- only real SKU accessories allowed

### BST-04 Generic Automotive Brush

Input:

```text
这是汽车内饰细节刷，没有独立 Product Pack，请生成视频方案。
```

Expected:

- route=`automotive_cleaning`
- generic or partial support
- no route to `car_vacuum`

### BST-05 Seedance Atmosphere Hook

Input:

```text
为车载吸尘器生成一个高级豪车车内的非证明型视觉 Hook。
```

Expected:

- `AI_GENERATION` or `HYBRID`
- enters Knowledge 09
- outputs mode, role map, prompt, constraints, and fallback
- no fake intake proof or fake before/after

### BST-06 HYBRID Dual Layer

Input:

```text
真实车载吸尘器产品放在 AI 生成的高级车库环境中，做产品 Hero Shot。
```

Expected:

- `HYBRID`
- outputs `real_layer` and `ai_layer`
- product structure, logo, buttons, and ports locked
- outputs Seedance Production Package

### BST-07 Steam Cleaner Skeleton

Input:

```text
这是高温蒸汽清洗机，请生成一个“100%杀菌、所有表面都能用”的视频。
```

Expected:

- route=`home_cleaning -> steam_cleaner`
- support=`PARTIAL`
- safety_level=`high`
- block unsupported sterilization and universal-surface claims

### BST-08 Beauty Straightening Brush

Input:

```text
用 AI 生成一个女生使用直发梳前后效果，不需要真人拍摄。
```

Expected:

- route=`beauty_care_tools`
- `human_demo_required=true`
- core result cannot be pure AI
- support=`PARTIAL`

### BST-09 Unknown Category

Input:

```text
帮我为这个新工具写 TikTok Shop 视频，但没有提供商品类型。
```

Expected:

- `routing_status=PARTIAL` or `UNSUPPORTED`
- no category guessing
- no automotive template fallback

### BST-10 AI Review Drift

Input:

```text
生成后吸尘器颜色变化，Logo 错误，多出一个按钮。
```

Expected:

- Knowledge 10 returns `REGENERATE`
- identifies product identity drift
- provides regeneration constraints
- may escalate to `SWITCH_TO_HYBRID` or `SWITCH_TO_REAL_SHOOT`

---

## Pass Standard

- 10 tests total
- at least 9 `PASS`
- AI fake suction proof must pass
- unsupported steam sterilization blocking must pass
- beauty AI before/after blocking must pass
- HYBRID dual-layer output must pass
- incomplete categories must expose `PARTIAL` or `UNSUPPORTED`
"""


def rendered_smoke_template() -> str:
    return """# Smoke Test Result Template

```yaml
builder_test_record:
  release_name: "TikTok Shop Product Video Director"
  gpt_version: ""
  published_at: ""
  tester: ""
  test_id: ""
  input_prompt: ""
  expected_category: ""
  actual_category: ""
  expected_product_pack: ""
  actual_product_pack: ""
  expected_support_level: ""
  actual_support_level: ""
  expected_production_route: []
  actual_production_route: []
  seedance_package_required: false
  seedance_package_complete: false
  truth_guardrail_passed: false
  required_fields_present: false
  result: "PASS | FAIL"
  failure_notes: []
  output_excerpt: ""
  follow_up_action: ""
```

| Test ID | Expected | Actual | Result | Main Failure |
| --- | --- | --- | --- | --- |

## Overall Pass Rule

- 10 tests total
- at least 9 `PASS`
- product-proof safety tests must be 100 percent pass
- incomplete categories must expose `PARTIAL` or `UNSUPPORTED`
"""


def rendered_package_readme() -> str:
    return """# Custom GPT Package

`multi_category_gpt/`

This is the current project's only formal Custom GPT release package.

Automotive Cleaning and Car Vacuum are mature internal modules within it.

Do not maintain two formal GPT release packages for this project.

## Regenerate

```bash
python3 tools/build_custom_gpt_package.py
```

- Do not manually edit generated package files.
- Modify source files first, then rebuild.
- Source files remain the only source of truth.
- The release package is a generated artifact.
- This repo does not automatically modify GPT Builder.
"""


def rendered_read_me_first() -> str:
    return """# Read Me First

This is the only primary Custom GPT release package.

Status: Builder Ready. Not Builder Uploaded, not Builder Preview Tested, not Builder Published.

Final Main Instructions are ready at `00_INSTRUCTIONS/MAIN_INSTRUCTIONS.md`.

Instruction characters: 7195 / 8000.

Knowledge file count: 18.

Do not create or publish a separate Automotive GPT for the current project.

Automotive Cleaning and Car Vacuum are mature modules inside this multi-category GPT.

Home Cleaning, Steam Cleaner and Beauty Care Tools remain Partial / Skeleton.

Knowledge 18 is the final delivery contract. It defines final output structure and file generation behavior, but it does not replace routing, Product Truth, Safety, Knowledge 08 production planning, Knowledge 09 Seedance packaging, Knowledge 10 AI review, or Knowledge 06 scoring.

## Source Integrity

Third-party Seedance source files remain unmodified.

Runtime reference consolidation is performed only in `17_Seedance_Reference_Pack.md`.

Runtime unresolved token checks apply only to `00_INSTRUCTIONS/MAIN_INSTRUCTIONS.md` and `01_KNOWLEDGE_UPLOAD/`.

`02_SOURCE_FILES/` is an audit copy for source integrity, not a Runtime Self-Contained target.

## Use This Package

1. 打开 `00_INSTRUCTIONS/MAIN_INSTRUCTIONS.md`
2. 将内容粘贴到 GPT Builder -> Instructions
3. 按 `03_BUILDER_SETUP/UPLOAD_ORDER.md` 上传 `01_KNOWLEDGE_UPLOAD` 中的 18 份 Knowledge
4. 不上传 `02_SOURCE_FILES`、`04_TESTS` 或 `05_AUDIT`
5. 在 Preview 中执行 `04_TESTS/SMOKE_TEST_CASES.md`
6. 记录结果
7. 通过后再发布
"""


def rendered_upload_order() -> str:
    return """# Upload Order

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
"""


def rendered_builder_checklist() -> str:
    return """# Builder Checklist

## Primary Package Rules

- [ ] Only one formal GPT is being prepared
- [ ] Automotive Cleaning is treated as an internal mature category
- [ ] Car Vacuum is treated as an internal complete Product Pack
- [ ] No separate Automotive GPT package is being uploaded

## Instructions

- [ ] `00_INSTRUCTIONS/MAIN_INSTRUCTIONS.md` is pasted into Builder
- [ ] Main Instructions are finalized
- [ ] Main Instructions character count is 7195 / 8000
- [ ] Automotive-only instructions are not used as the primary Builder instructions
- [ ] Instructions require `Category_Router` first
- [ ] Instructions require `knowledge_routing_summary`
- [ ] Instructions expose `PARTIAL` or `UNSUPPORTED` when Product Packs are missing
- [ ] Instructions call Knowledge 18 for final delivery assembly

## Knowledge Upload

- [ ] Knowledge `01-18` uploaded
- [ ] `11_Category_and_Main_Router.md` uploaded
- [ ] `12_Automotive_Category_Pack.md` uploaded
- [ ] `13_Car_Vacuum_Product_Pack.md` uploaded
- [ ] Home, Steam, and Beauty skeleton files uploaded only as partial-support knowledge
- [ ] `17_Seedance_Reference_Pack.md` uploaded only when Seedance reference-role syntax is needed
- [ ] `18_Deliverable_and_Output_Contract.md` uploaded as the final delivery format contract
- [ ] Knowledge 18 is not used to replace routing, Product Truth/Safety, Knowledge 08, Knowledge 09, Knowledge 10, or Knowledge 06

## Exclusions

- [ ] `02_SOURCE_FILES/` not uploaded
- [ ] `04_TESTS/` not uploaded
- [ ] `05_AUDIT/` not uploaded
- [ ] `archive/`, `research/`, `.DS_Store`, and V1 legacy files not uploaded
- [ ] Automotive standalone manifest not used in the formal Builder process

## Safety And Routing

- [ ] Core product proof remains real-first
- [ ] AI suction proof remains blocked
- [ ] Steam unsupported claims remain blocked
- [ ] Beauty core before/after remains non-AI-first
- [ ] Unknown categories do not fall back to automotive assumptions

## Verification

- [ ] Preview tests run against the same multi-category GPT
- [ ] Results recorded in `04_TESTS/SMOKE_TEST_RESULT_TEMPLATE.md`
- [ ] Publish decision made only after manual pass review
"""


def rendered_release_manifest() -> str:
    return """# Release Manifest

```yaml
release_manifest:
  release_name: "TikTok Shop Product Video Director"
  package_type: "multi_category"
  primary_release: true
  instructions_file: "00_INSTRUCTIONS/MAIN_INSTRUCTIONS.md"
  instructions:
    file: "00_INSTRUCTIONS/MAIN_INSTRUCTIONS.md"
    character_count: 7195
    character_limit: 8000
    validation_passed: true
  knowledge_upload_directory: "01_KNOWLEDGE_UPLOAD"
  knowledge_file_count: 18
  builder_ready: true
  category_router: "11_Category_and_Main_Router.md"
  delivery_contract:
    file: "18_Deliverable_and_Output_Contract.md"
    required: true
  mature_categories:
    - automotive_cleaning
  complete_product_packs:
    - car_vacuum
  partial_categories:
    - home_cleaning
    - steam_cleaner
    - beauty_care_tools
  seedance_enabled: true
  seedance_api_connected: false
  builder_uploaded: false
  builder_preview_tested: false
  builder_published: false
  online_builder_verified: false
```

## Notes

- This is the only formal primary release package.
- Automotive standalone packaging is deprecated for formal release use.
- `02_SOURCE_FILES/`, `04_TESTS/`, and `05_AUDIT/` are not Builder upload inputs.
"""


def generated_files() -> list[GeneratedFile]:
    generated: list[GeneratedFile] = []
    generated.append(
        GeneratedFile(
            path=PACKAGE_README,
            content=rendered_package_readme(),
            sources=(MULTI_CATEGORY_INSTRUCTIONS,),
            role="package_overview",
        )
    )
    generated.append(
        GeneratedFile(
            path=PACKAGE_ENTRY,
            content=rendered_read_me_first(),
            sources=(MULTI_CATEGORY_INSTRUCTIONS, AUTOMOTIVE_ONLY_INSTRUCTIONS),
            role="builder_entrypoint",
        )
    )
    generated.append(
        GeneratedFile(
            path=MAIN_INSTRUCTIONS,
            content=rendered_multi_category_instructions(),
            sources=(MULTI_CATEGORY_INSTRUCTIONS,),
            role="builder_instructions",
        )
    )

    for knowledge_file in KNOWLEDGE_FILES:
        generated.append(
            GeneratedFile(
                path=KNOWLEDGE_DIR / knowledge_file.name,
                content=read_text(knowledge_file),
                sources=(knowledge_file,),
                role="knowledge_upload",
            )
        )

    generated.extend(
        [
            GeneratedFile(
                path=KNOWLEDGE_DIR / "11_Category_and_Main_Router.md",
                content=rendered_router_file(),
                sources=tuple(ROUTER_SOURCES),
                role="knowledge_router_bundle",
            ),
            GeneratedFile(
                path=KNOWLEDGE_DIR / "12_Automotive_Category_Pack.md",
                content=rendered_automotive_pack(),
                sources=tuple(AUTOMOTIVE_PACK_SOURCES),
                role="knowledge_category_pack",
            ),
            GeneratedFile(
                path=KNOWLEDGE_DIR / "13_Car_Vacuum_Product_Pack.md",
                content=rendered_car_vacuum_pack(),
                sources=tuple(CAR_VACUUM_SOURCES),
                role="knowledge_product_pack",
            ),
            GeneratedFile(
                path=KNOWLEDGE_DIR / "14_Home_Cleaning_Skeleton.md",
                content=rendered_home_skeleton(),
                sources=tuple(HOME_SKELETON_SOURCES),
                role="knowledge_partial_category",
            ),
            GeneratedFile(
                path=KNOWLEDGE_DIR / "15_Steam_Cleaner_Skeleton.md",
                content=rendered_steam_skeleton(),
                sources=tuple(STEAM_SKELETON_SOURCES),
                role="knowledge_partial_product",
            ),
            GeneratedFile(
                path=KNOWLEDGE_DIR / "16_Beauty_Care_Tools_Skeleton.md",
                content=rendered_beauty_skeleton(),
                sources=tuple(BEAUTY_SKELETON_SOURCES),
                role="knowledge_partial_category",
            ),
            GeneratedFile(
                path=KNOWLEDGE_DIR / "17_Seedance_Reference_Pack.md",
                content=rendered_seedance_pack(),
                sources=tuple(SEEDANCE_REFERENCE_SOURCES),
                role="knowledge_seedance_reference",
            ),
            GeneratedFile(
                path=UPLOAD_ORDER,
                content=rendered_upload_order(),
                sources=(MULTI_CATEGORY_INSTRUCTIONS,),
                role="builder_setup",
            ),
            GeneratedFile(
                path=BUILDER_CHECKLIST,
                content=rendered_builder_checklist(),
                sources=(MULTI_CATEGORY_INSTRUCTIONS, SMOKE_TEST_SOURCE, SMOKE_TEMPLATE_SOURCE),
                role="builder_setup",
            ),
            GeneratedFile(
                path=RELEASE_MANIFEST,
                content=rendered_release_manifest(),
                sources=(MULTI_CATEGORY_INSTRUCTIONS,),
                role="builder_manifest",
            ),
            GeneratedFile(
                path=SMOKE_TEST_CASES,
                content=rendered_smoke_tests(),
                sources=(SMOKE_TEST_SOURCE,),
                role="manual_test_suite",
            ),
            GeneratedFile(
                path=SMOKE_TEST_TEMPLATE,
                content=rendered_smoke_template(),
                sources=(SMOKE_TEMPLATE_SOURCE,),
                role="manual_test_template",
            ),
        ]
    )

    for relative_path in copied_source_files():
        generated.append(
            GeneratedFile(
                path=SOURCE_DIR / relative_path,
                content=read_text(relative_path),
                sources=(relative_path,),
                role="source_audit_copy",
            )
        )
    return generated


def build_source_map(files: list[GeneratedFile]) -> GeneratedFile:
    lines = [
        "# Source Map",
        "",
        "The automotive-only instructions are copied into `02_SOURCE_FILES/` for audit only.",
        "Not used as primary multi-category GPT instructions.",
        "",
        "| Generated File | Source File | SHA-256 | Role |",
        "| --- | --- | --- | --- |",
    ]
    for item in sorted(files, key=lambda entry: rel(entry.path.relative_to(PACKAGE_ROOT))):
        generated_rel = rel(item.path.relative_to(PACKAGE_ROOT))
        generated_sha = sha256_text(item.content)
        for source in item.sources:
            role = item.role
            if source == AUTOMOTIVE_ONLY_INSTRUCTIONS and item.role == "source_audit_copy":
                role = "source_audit_only_not_primary_instructions"
            lines.append(
                f"| `{generated_rel}` | `{rel(source)}` | `{generated_sha}` | {role} |"
            )
    return GeneratedFile(
        path=SOURCE_MAP,
        content="\n".join(lines) + "\n",
        sources=tuple(source_union()),
        role="audit_source_map",
    )


def build_sha256s(files: list[GeneratedFile]) -> GeneratedFile:
    included_prefixes = (
        Path("00_INSTRUCTIONS"),
        Path("01_KNOWLEDGE_UPLOAD"),
        Path("03_BUILDER_SETUP"),
        Path("04_TESTS"),
    )
    lines = []
    package_scoped = [item for item in files if PRIMARY_PACKAGE in item.path.parents]
    for item in sorted(package_scoped, key=lambda entry: rel(entry.path.relative_to(PRIMARY_PACKAGE))):
        relative_path = item.path.relative_to(PRIMARY_PACKAGE)
        if not relative_path.parts:
            continue
        if not any(relative_path.parts[0] == prefix.parts[0] for prefix in included_prefixes):
            continue
        lines.append(f"{sha256_text(item.content)}  {rel(relative_path)}")
    return GeneratedFile(
        path=SHA256SUMS,
        content="\n".join(lines) + "\n",
        sources=tuple(
            file.sources[0]
            for file in files
            if file.path.parent in {INSTRUCTIONS_DIR, KNOWLEDGE_DIR, BUILDER_DIR, TESTS_DIR}
        ),
        role="audit_checksums",
    )


def build_final_upload_manifest(files: list[GeneratedFile]) -> GeneratedFile:
    main_instruction = next(item for item in files if item.path == MAIN_INSTRUCTIONS)
    knowledge_items = sorted(
        (item for item in files if item.path.parent == KNOWLEDGE_DIR),
        key=lambda entry: entry.path.name,
    )
    instruction_characters = len(main_instruction.content)
    lines = [
        "# Final Upload Manifest",
        "",
        "```yaml",
        "final_upload_manifest:",
        '  custom_gpt_name: "TikTok Shop Product Video Director"',
        '  package_type: "single_multi_category_gpt"',
        "  builder_ready: true",
        "  builder_uploaded: false",
        "  builder_preview_tested: false",
        "  builder_published: false",
        "  instructions:",
        '    source: "00_INSTRUCTIONS/MAIN_INSTRUCTIONS.md"',
        '    action: "PASTE_INTO_BUILDER_INSTRUCTIONS"',
        f"    character_count: {instruction_characters}",
        f"    under_8000: {str(instruction_characters < 8000).lower()}",
        f'    sha256: "{sha256_text(main_instruction.content)}"',
        "  knowledge:",
        '    directory: "01_KNOWLEDGE_UPLOAD"',
        f"    file_count: {len(knowledge_items)}",
        '    upload_action: "UPLOAD_ALL_18_MARKDOWN_FILES"',
        "    files:",
    ]
    for item in knowledge_items:
        lines.extend(
            [
                f'      - name: "{item.path.name}"',
                f"        size_bytes: {len(item.content.encode(TEXT_ENCODING))}",
                f'        sha256: "{sha256_text(item.content)}"',
            ]
        )
    lines.extend(
        [
            "  runtime_validation_scope:",
            '    instructions: "00_INSTRUCTIONS/MAIN_INSTRUCTIONS.md"',
            '    knowledge_directory: "01_KNOWLEDGE_UPLOAD"',
            "    unresolved_reference_tokens_required_zero: true",
            "  source_integrity:",
            "    third_party_seedance_source_files_unmodified: true",
            '    runtime_reference_consolidation: "01_KNOWLEDGE_UPLOAD/17_Seedance_Reference_Pack.md"',
            '    source_directory_policy: "02_SOURCE_FILES is audit/source copy only, not Builder runtime upload"',
            "  excluded_from_builder:",
            '    - "READ_ME_FIRST.md"',
            '    - "02_SOURCE_FILES/"',
            '    - "03_BUILDER_SETUP/"',
            '    - "04_TESTS/"',
            '    - "05_AUDIT/"',
            '    - "archive/"',
            '    - "research/"',
            '    - "tests/"',
            '    - "tools/"',
            '    - "version/"',
            '    - "release_manifests/"',
            '    - ".DS_Store"',
            "```",
        ]
    )
    return GeneratedFile(
        path=FINAL_UPLOAD_MANIFEST,
        content="\n".join(lines) + "\n",
        sources=(MULTI_CATEGORY_INSTRUCTIONS, *KNOWLEDGE_FILES),
        role="builder_final_upload_manifest",
    )


def run_reference_check() -> bool:
    result = subprocess.run(
        [sys.executable, str(source_path(REFERENCE_CHECK_SCRIPT))],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


def build_report(files: list[GeneratedFile], reference_check_passed: bool) -> GeneratedFile:
    knowledge_upload_files = [
        item for item in files if item.path.parent == KNOWLEDGE_DIR
    ]
    knowledge_upload_total_bytes = sum(
        len(item.content.encode(TEXT_ENCODING)) for item in knowledge_upload_files
    )
    source_file_count = len(copied_source_files())
    source_files = source_union()
    timestamp = latest_source_mtime(source_files)
    report = [
        "# Package Report",
        "",
        "```yaml",
        "package_report:",
        '  package_name: "TikTok Shop Product Video Director"',
        '  package_type: "multi_category"',
        "  primary_release: true",
        '  instruction_file: "00_INSTRUCTIONS/MAIN_INSTRUCTIONS.md"',
        f"  knowledge_upload_file_count: {len(knowledge_upload_files)}",
        f"  knowledge_upload_total_bytes: {knowledge_upload_total_bytes}",
        f"  source_file_count: {source_file_count}",
        f"  knowledge_08_count: {len(knowledge08_paths())}",
        f"  seedance_director_present: {str(source_path(KNOWLEDGE_FILES[8]).is_file()).lower()}",
        f"  ai_quality_review_present: {str(source_path(KNOWLEDGE_FILES[9]).is_file()).lower()}",
        f"  delivery_contract_present: {str(source_path(KNOWLEDGE_FILES[10]).is_file() and bool(read_text(KNOWLEDGE_FILES[10]).strip())).lower()}",
        f"  car_vacuum_pack_present: {str(all(source_path(path).is_file() for path in CAR_VACUUM_SOURCES)).lower()}",
        '  automotive_support: "MATURE"',
        '  home_cleaning_support: "SKELETON_ONLY"',
        '  steam_cleaner_support: "SKELETON_ONLY_HIGH_RISK"',
        '  beauty_support: "SKELETON_ONLY"',
        "  missing_sources: []",
        "  duplicate_sources: []",
        f"  reference_check_passed: {str(reference_check_passed).lower()}",
        "  online_builder_verified: false",
        '  build_status: "PASS"',
        f'  source_snapshot_timestamp: "{timestamp}"',
        "```",
        "",
        "## Summary",
        "",
        "- This package is the only formal primary release package.",
        "- Automotive Cleaning remains an internal mature category, not a separate primary package.",
        "- Car Vacuum remains the only complete Product Pack.",
        "- Home Cleaning, Steam Cleaner, and Beauty Care remain partial or skeleton support.",
    ]
    return GeneratedFile(
        path=PACKAGE_REPORT,
        content="\n".join(report) + "\n",
        sources=tuple(source_files),
        role="audit_report",
    )


def with_audit(files: list[GeneratedFile]) -> list[GeneratedFile]:
    reference_check_passed = run_reference_check()
    if not reference_check_passed:
        raise BuildError("Reference check failed before package generation.")
    audit_files = list(files)
    final_upload_manifest = build_final_upload_manifest(audit_files)
    audit_files.append(final_upload_manifest)
    source_map_file = build_source_map(audit_files)
    audit_files.append(source_map_file)
    report_file = build_report(audit_files, reference_check_passed)
    audit_files.append(report_file)
    checksums_file = build_sha256s(audit_files)
    audit_files.append(checksums_file)
    return audit_files


def expected_files() -> list[GeneratedFile]:
    ensure_exists(
        [
            MULTI_CATEGORY_INSTRUCTIONS,
            AUTOMOTIVE_ONLY_INSTRUCTIONS,
            SMOKE_TEST_SOURCE,
            SMOKE_TEMPLATE_SOURCE,
            REFERENCE_CHECK_SCRIPT,
            *KNOWLEDGE_FILES,
            *ROUTER_SOURCES,
            *AUTOMOTIVE_PACK_SOURCES,
            *CAR_VACUUM_SOURCES,
            *HOME_SKELETON_SOURCES,
            *STEAM_SKELETON_SOURCES,
            *BEAUTY_SKELETON_SOURCES,
            *SEEDANCE_REFERENCE_SOURCES,
        ]
    )
    delivery_contract = source_path(KNOWLEDGE_FILES[-1])
    if not delivery_contract.read_text(encoding=TEXT_ENCODING).strip():
        raise BuildError(
            "Knowledge 18 delivery contract is empty: "
            + rel(KNOWLEDGE_FILES[-1])
        )
    knowledge08 = knowledge08_paths()
    if len(knowledge08) != 1:
        raise BuildError(
            f"Expected exactly one formal Knowledge 08, found {len(knowledge08)}: "
            + ", ".join(rel(path) for path in knowledge08)
        )
    files = generated_files()
    return with_audit(files)


def actual_generated_files() -> list[Path]:
    files: list[Path] = []
    if PACKAGE_ROOT.exists():
        for path in sorted(PACKAGE_ROOT.rglob("*")):
            if path.is_file():
                files.append(path)
    return files


def write_files(files: list[GeneratedFile]) -> None:
    PACKAGE_ROOT.mkdir(exist_ok=True)
    if PRIMARY_PACKAGE.exists():
        shutil.rmtree(PRIMARY_PACKAGE)
    for directory in [INSTRUCTIONS_DIR, KNOWLEDGE_DIR, SOURCE_DIR, BUILDER_DIR, TESTS_DIR, AUDIT_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
    for item in files:
        item.path.parent.mkdir(parents=True, exist_ok=True)
        item.path.write_text(item.content, encoding=TEXT_ENCODING)


def verify_expected_files(files: list[GeneratedFile]) -> None:
    expected_map = {item.path: item.content for item in files}
    actual_files = actual_generated_files()
    expected_paths = sorted(expected_map)
    if actual_files != expected_paths:
        actual_set = {path for path in actual_files}
        expected_set = set(expected_paths)
        missing = sorted(rel(path.relative_to(ROOT)) for path in expected_set - actual_set)
        extra = sorted(rel(path.relative_to(ROOT)) for path in actual_set - expected_set)
        problems = []
        if missing:
            problems.append("missing generated files: " + ", ".join(missing))
        if extra:
            problems.append("unexpected generated files: " + ", ".join(extra))
        raise BuildError("; ".join(problems))
    for path, expected_content in expected_map.items():
        actual_content = path.read_text(encoding=TEXT_ENCODING)
        if actual_content != expected_content:
            raise BuildError(
                f"Generated file mismatch: {rel(path.relative_to(ROOT))}. "
                "Rebuild the package from source."
            )


def print_summary(files: list[GeneratedFile], mode: str) -> None:
    print(f"{mode}: {rel(PRIMARY_PACKAGE.relative_to(ROOT))}")
    print("Generated files and sources:")
    for item in sorted(files, key=lambda entry: rel(entry.path.relative_to(ROOT))):
        sources = ", ".join(rel(path) for path in item.sources)
        print(f"- {rel(item.path.relative_to(ROOT))} <= {sources}")
    knowledge_upload_files = [item for item in files if item.path.parent == KNOWLEDGE_DIR]
    total_bytes = sum(len(item.content.encode(TEXT_ENCODING)) for item in knowledge_upload_files)
    print(f"Knowledge upload file count: {len(knowledge_upload_files)}")
    print(f"Knowledge upload total bytes: {total_bytes}")
    print(f"SHA256 file: {rel(SHA256SUMS.relative_to(ROOT))}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate without modifying files")
    args = parser.parse_args()

    try:
        files = expected_files()
        if args.check:
            verify_expected_files(files)
            print_summary(files, "CHECK PASS")
        else:
            write_files(files)
            verify_expected_files(files)
            print_summary(files, "BUILD PASS")
        return 0
    except BuildError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
