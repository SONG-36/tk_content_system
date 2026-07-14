# Knowledge 01-17 Repair Regression Tests

These are document-level tests for the single multi-category GPT Knowledge upload set.

## Test 1: Car Vacuum

Input:

```text
车载吸尘器，透明尘盒和缝隙吸头，生成视频方案。
```

Expected:

- route: `automotive_cleaning`
- category knowledge: `12_Automotive_Category_Pack.md`
- product pack: `13_Car_Vacuum_Product_Pack.md`
- support: `COMPLETE`
- Dirt Intake: `REAL_SHOOT`
- Transparent Bin: `REAL_SHOOT`

## Test 2: Generic Automotive

Input:

```text
汽车细节刷，没有专属 Product Pack。
```

Expected:

- route: `automotive_cleaning`
- product type: `detailing_brush`
- support: `GENERIC_SUPPORTED`
- must not enter Car Vacuum Product Pack

## Test 3: Partial Automotive

Input:

```text
汽车内饰清洁喷雾，没有完整参数。
```

Expected:

- route: `automotive_cleaning`
- product type: `car_cleaning_spray`
- support: `PARTIAL`
- disclose missing product-specific knowledge

## Test 4: Home Cleaning

Input:

```text
厨房电动清洁刷。
```

Expected:

- route: `home_cleaning`
- support: `SKELETON_ONLY`
- routing status: `PARTIAL`
- must not use automotive seat-gap examples as professional proof

## Test 5: Steam

Input:

```text
高温蒸汽清洗机，宣传100%杀菌和所有表面通用。
```

Expected:

- route: `home_cleaning`
- product type: `steam_cleaner`
- `safety_level=high`
- support: `PARTIAL`
- block `100% sterilization`
- block universal-surface claim

## Test 6: Beauty

Input:

```text
用 AI 生成人物使用直发梳的前后效果。
```

Expected:

- route: `beauty_care_tools`
- support: `PARTIAL`
- `human_demo_required=true`
- block AI-generated core before/after efficacy

## Test 7: Knowledge 10 Timing

Input:

```text
只有 Seedance Prompt，没有成片。
```

Expected:

- Knowledge 10 required
- AI review status: `NOT_RUN`
- must not output `PASS`

## Test 8: Knowledge 17 Extend

Input:

```text
续写上一段视频，但没有真实上一段成片。
```

Expected:

- must not call inaccessible `[skill:*]`
- must not invent continuation state
- require accepted source clip or observed end state

## Test 9: Unknown Product

Input:

```text
帮我做一个新工具的视频，但没有说明商品类型。
```

Expected:

- must not auto-route to automotive
- routing status: `PARTIAL` or `UNSUPPORTED`
- output missing information

## Test 10: HYBRID

Input:

```text
真实商品放在 AI 生成的高级环境里做 Hero Shot。
```

Expected:

- output real layer
- output AI layer
- output proof layer owner
- output AI must-not-rewrite constraints
- Knowledge 09 required
- Knowledge 10 status: `NOT_RUN`
