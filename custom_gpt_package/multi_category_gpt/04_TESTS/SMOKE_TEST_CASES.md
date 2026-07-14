# Smoke Test Cases

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
