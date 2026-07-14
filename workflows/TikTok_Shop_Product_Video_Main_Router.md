# TikTok Shop Product Video Main Router

## Purpose

This is the formal multi-category top-level router.

It sits above the automotive sub-router and decides:

- which category pack to load
- which product pack to load
- whether support is routed, generic supported, partial, or unsupported

---

## Canonical Flow

```text
User Input
-> Category Router
-> Core Viral Analysis
-> Selected Category Pack
-> Selected Product Pack
-> Script Generation
-> Professional Shooting
-> Shot Production Planning
-> REAL_SHOOT / STOCK / AI_GENERATION / HYBRID
-> Seedance Director when routed
-> mark AI Generation Quality Review as REQUIRED / NOT_RUN until generated media exists
-> Commercial Script Scoring
```

---

## Router Layers

### Layer 1: Category Routing

Use `workflows/Category_Router.md` first.

Inside GPT Builder, resolve runtime Knowledge by Builder filenames such as `11_Category_and_Main_Router.md`, not by repository paths.

### Layer 2: Category Logic

Load:

- automotive category pack
- home-cleaning skeleton
- beauty-care skeleton

based on the routing result.

### Layer 3: Product Logic

If a complete product pack exists:

- load it

If only a skeleton or no product pack exists:

- declare `PARTIAL` or `UNSUPPORTED`
- declare `GENERIC_SUPPORTED` where category knowledge can support a conservative generic plan
- do not fabricate expert support

### Layer 4: Production And AI Routing

Use:

- `knowledge/08_Shot_Production_Planning_Framework.md`
- `knowledge/09_Seedance_Generation_Director.md`
- `knowledge/10_AI_Generation_Quality_Review.md`

only after category and product context are known.

Knowledge 10 must not return `PASS` for prompts or storyboards. It executes only after actual generated AI material exists.

---

## Automotive Sub-Chain

```text
Category Router
-> automotive_cleaning
-> Car Cleaning Router
-> Optional Product Pack
```

### Car Vacuum Path

```text
automotive_cleaning
-> car_vacuum
-> Car Vacuum Product Pack
-> Core 01–10
```

---

## Safety And Truth Rule

If the category or product pack is incomplete:

- do not generate unsupported hard claims
- do not generate unsupported safety assurances
- do not auto-upgrade to production-ready guidance
