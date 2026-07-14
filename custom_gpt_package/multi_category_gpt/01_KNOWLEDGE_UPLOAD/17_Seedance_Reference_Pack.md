# Seedance Reference Pack

```yaml
runtime_dependency_status:
  self_contained: true
  unresolved_ref_tokens: 0
  unresolved_skill_tokens: 0
  authoritative_truth_router: "08_Shot_Production_Planning_Framework.md"
  authoritative_seedance_package: "09_Seedance_Generation_Director.md"
```

This file is uploaded only for the multi-category GPT when Seedance-oriented reference-role syntax must be available inside Builder context.

Knowledge 17 provides prompt, reference, camera and motion language.

It does not decide whether AI is allowed.

Knowledge 08 controls production-type and truth routing.
Knowledge 09 controls the final Seedance Production Package.
Category and Product Packs control product truth and safety.


## Local Quick Reference

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

---

# SOURCE FILE: seedance_skills/reference-workflow.md

---

# Reference Workflow

## Reference Tag Syntax

Seedance 2.0 binds uploaded assets with an `@`-mention typed directly in the prompt: type `@` in the prompt field to pick an uploaded file, or write the tag inline. Tags are assigned by type and upload order.

- Images: `@Image1`–`@Image9` (Chinese surfaces: `@图片1`–`@图片9`)
- Videos: `@Video1`–`@Video3` (Chinese surfaces: `@视频1`–`@视频3`)
- Audio: `@Audio1`–`@Audio3` (Chinese surfaces: `@音频1`–`@音频3`)

Write each tag with the job it does, never on its own: `@Image1 as the first frame`, `follow @Video1 for camera movement`, `@Audio1 for background music`. Keep tags literal — do not translate `@Image1` into another language, renumber it, or rewrite it as a bracketed `[Image1]`; the platform's `@`-parser does not recognize the bracket form, so a mistyped tag silently fails to bind its reference.

## Asset Role Map

Before writing prompt prose, assign every uploaded asset a role. Role mapping prevents accidental transfer of identity, logos, scene ownership, or incompatible camera and motion instructions.

| Asset | Good Roles | Avoid |
|---|---|---|
| Image | identity, product, pose, costume, environment, first frame, last frame | asking it to define unseen motion |
| Video | motion, camera, pacing, blocking, timing, gesture rhythm | copying protected identity, logo, or scene ownership |
| Audio | rhythm, tempo, mood, ambience, delivery tone, music texture | assuming voice, song, or likeness authorization |
| Text brief | action, genre, camera plan, constraints | replacing concrete reference roles with vague mood words |

## Rules

- Preserve reference tags exactly.
- Give every reference one primary role before writing style language.
- Do not ask one reference to control incompatible roles unless the tradeoff is explicit.
- Use owned, licensed, public-domain, or clearly authorized references.
- Write what should transfer and what should not transfer.
- When authorization is unclear, transfer broad motion, tempo, mood, or production function rather than protected identity.
- Treat multimodal reference generation, video edit, video extend, and first/last-frame generation as separate tasks. They can share assets, but the prompt should name the active workflow.
- If audio and video references compete, make the video silent when audio timing must dominate, or state that the video controls camera/motion only and `@Audio1` controls tempo.
- In sequences, separate canonical references from accepted continuity sources: canonical identity/product references control immutable design, while accepted previous footage controls transient opening state.
- Never let a motion reference overwrite continuity locks, completed beats, reserved beats, or exact reference tags.

## Workflow-Specific Patterns

| Workflow | Use this wording | Avoid |
|---|---|---|
| Multimodal reference | `@Image1 controls product identity; @Video1 controls camera rhythm; @Audio1 controls tempo only.` | `Use all references for style.` |
| Video edit | `@Video1 is the source clip; preserve composition and timing, change only [lighting/background/VFX].` | Regenerating the whole concept from scratch. |
| Video extend | `@Video1 is the previous clip; continue the same shot for [duration] and preserve last-frame continuity.` | Starting a new scene with no continuity anchor. |
| First/last frame | `@Image1 is first frame; @Image2 is final visual target; generate the continuous transition only.` | Asking the last frame to be only "mood." |
| Audio reference | `@Audio1 controls tempo and energy; do not copy protected voice, song, or performance identity.` | Treating audio as authorization proof. |

## Role Examples

| Situation | Strong map |
|---|---|
| Product ad | `@Image1 controls product identity; @Audio1 controls tempo only.` |
| Motion transfer | `@Video1 controls side-step choreography only; do not transfer performer, costume, room, or logo.` |
| Style reference | `@Image2 controls warm bar atmosphere only; product identity remains from @Image1.` |
| First-last frame | `@Image1 is first frame; @Image2 is target end frame; transition occurs through light sweep, not product deformation.` |
| Edit/extend | `@Video1 is the source clip; preserve subject and camera path, replace only the failed lighting beat from 3s to 5s.` |

## Motion Transfer

Field-observed technique; test before promising results. Probably the most under-used reference capability: a donor video drives choreography or camera rhythm while an image keeps identity.

- Pair one donor `@Video1` with one identity anchor `@Image1`, and write the exclusion explicitly: `@Video1 controls the choreography only - nothing of its appearance, performer, costume, room, or logo transfers.`
- Pick donor clips with one clear action, a clean silhouette, and a steady camera. Busy multi-person footage transfers noise, not motion.
- Mute the donor clip before upload unless its sound should drive timing; if it keeps sound, state which reference owns the clock.
- Transfers well: choreography, gesture timing, camera rhythm, blocking. Transfers poorly: fine hand detail, multi-person sync, facial performance.
- Use only owned, licensed, stock, mocap, rehearsal, or self-recorded donor footage; real-person donors transfer general motion only, never likeness.

## Template

`@Image1 controls product identity. @Video1 controls camera pace only. @Audio1 controls tempo only. Preserve the subject from @Image1; do not copy characters, logos, music, voice, or environment from @Video1/@Audio1.`

## Sequence Transfer Template

`[Video 1] is the accepted previous clip and controls only the actual opening state, camera phase, motion phase, ambience, and environment arrangement. @Image 1 controls canonical identity. Preserve both tags exactly. Do not copy unrelated identity, costume, logo, or future action from any reference.`
---

# SOURCE FILE: seedance_skills/seedance-prompt/SKILL.md

---

---
name: seedance-prompt
description: "This skill should be used when the user asks to write, improve, translate, compress, or debug a Seedance 2.0 video prompt; mentions T2V, I2V, V2V, R2V, camera direction, prompt quality, or provides reference assets for a production-ready prompt."
license: MIT
user-invocable: true
tags:
  - prompt-engineering
  - video-generation
  - seedance-20
metadata:
  version: "6.6.0"
  updated: "2026-07-04"
  parent: "seedance-20"
  author: "Iamemily2050 (@iamemily2050)"
  repository: "https://github.com/Emily2040/seedance-2.0"
  openclaw:
    emoji: "🎬"
    homepage: "https://github.com/Emily2040/seedance-2.0"
---

# seedance-prompt

Build production-ready Seedance prompts from clear concepts or supplied reference assets. Treat the prompt as a short shooting brief: it must say what changes on screen, what the camera does, what the light and sound contribute, and what must stay stable. Keep final prompts under the platform prompt budget and remove filler before delivery.

Load `the Local Quick Reference section in this Knowledge` for the checklist, `the Reference Workflow section included earlier in this Knowledge` for multimodal references, `the Local I2V Guide section in this Knowledge` for image-to-video, `the Local First/Last Frame Guide section in this Knowledge` for first/last-frame work, `the Local Mode Examples section in this Knowledge` when examples are useful, `the Local Shot Continuity Rules section in this Knowledge` for multi-shot professional plans, `the Local Multishot Grammar section in this Knowledge` for shot-label grammar, the shots-times-seconds budget, and cut placement inside one generation, and `clear professional camera terminology in the requested language` for Chinese/Russian/Japanese/Korean/Spanish or mixed-language prompts. When sequence state is present, load `the Local Prompt Compiler section in this Knowledge` and compile only the current clip contract.

## Intent

This is the translator between a scene that exists in someone's head and one that exists on screen. The user has already imagined it; the job is to lose as little as possible in transit. Success is a first generation close enough that they can react instead of explain. Each revision inherits everything the story has already decided and changes only what the reaction asked for - a draft is a conversation, not a restart.

## Director Formula

Before filling slots, decide the one thing the shot is doing. Load `the Local Directing Engine section in this Knowledge`, read the scene, name a single intention, and let that intention choose the camera, lighting, blocking, performance, and sound together so they reinforce instead of compete. The formula below is the container for a coherent setup, not a checklist of independent decorations; if a project voice is already set, keep this shot inside it.

Use `Subject + Action + Scene + Camera + Lighting/Style + Audio + Constraints`. Put the subject and primary action first because early clauses set the shot hierarchy. Do not force every slot if a reference asset already shows the information; for I2V, describe only the motion, camera, timing, transformation, audio, and preservation constraints that the still image cannot show.

| Slot | Use for | Prompt-ready pattern |
|---|---|---|
| Subject | The anchor the model must track. | `Original ceramic perfume bottle on black acrylic, label preserved exactly` |
| Action | The visible change. | `condensation beads form and slide down the glass over five seconds` |
| Scene | Only what is not already in references. | `quiet rain-lit kitchen counter, shallow depth of field` |
| Camera | One primary move with endpoint. | `slow dolly-in from medium product shot to macro label detail` |
| Light and style | Physical light plus safe visual language. | `warm practical key from frame left, cool blue rim, clean commercial realism` |
| Audio | Ambient bed, SFX, dialogue, or silence. | `Sound: low room tone, soft glass chime on final frame` |
| Constraints | Preservation and exclusions. | `do not alter logo, shape, label, or cap geometry` |

## Mode Gate

Choose the mode before drafting. **T2V** needs subject, action, scene, camera, light, style, and constraints because nothing is visible yet. **I2V** starts from `@Image1` and adds only motion, time, camera, lighting transition, audio, and preservation. **V2V** should map `@Video1` to source clip, camera move, action rhythm, blocking, edit target, or extension anchor rather than accidentally transferring identity. **R2V** must list every reference role and state what must not transfer. **FLF2V** uses `@Image1` as first frame and `@Image2` as last frame, then describes only the continuous transition.

| Mode | Drafting priority | Common mistake | Repair |
|---|---|---|---|
| T2V | Build the whole shot in compact layers. | Too many events in one clip. | Keep one visible beat and one endpoint. |
| I2V | Preserve visible identity; add motion. | Re-describing the image until the product or face drifts. | Say `preserve @Image1 exactly`; add only dynamic changes. |
| V2V | Transfer motion, camera, or timing. | Copying unauthorized likeness or scene details. | Use owned/licensed/authorized references and restrict transfer role. |
| R2V | Assign separate roles to each asset. | One reference asked to control identity, pose, scene, and style. | Split roles or prioritize the most important role. |
| FLF2V | Move from first frame to last frame. | Treating the last frame as vague mood instead of endpoint. | State `@Image2` is the final visual target. |
| Edit | Preserve the source clip while changing one layer. | Rewriting the whole scene and losing continuity. | Say `@Video1 is the source clip; change only...` |
| Extend | Continue from accepted source footage only. | Starting from a planned ending or inventing the clip state. | Route to `the Local Continuation Contract section in this Knowledge` and use the observed end state. |

## Sequence Boundary

The generic prompt skill must not independently invent continuation state. If the user asks to continue, extend, make part two, or use a previous clip, route to `the Local Continuation Contract section in this Knowledge` unless the accepted clip/final frame and observed end state are already present in the sequence state.

For sequence prompts, preserve `project_id`, `clip_id`, `parent_clip_id`, continuity locks, exact reference tags, the actual opening state, completed beat exclusions, and reserved future beats. The final prompt remains natural language and covers only the current clip.

## Prompt Build Process

First, identify the single visible beat: reveal, arrival, decision, transformation, contact, pursuit, or disappearance, and name the one intention it serves. Next, assign reference roles before adding adjectives. Then write a compact first draft in the director formula order, keeping camera, light, performance, and sound aimed at that intention. Finally, run a self-check and the directing coherence test from `the Local Directing Engine section in this Knowledge`: one main subject, one main action, one motivated main camera move, physically motivated lighting, performance written as a visible gesture rather than an emotion word, assigned character tags, sound intent, and no hollow boosters.

## Compression Rules

When the prompt is too long, cut in this order: duplicate style adjectives, generic quality words, background details visible in references, secondary camera moves, secondary actions, and speculative emotional labels. Keep preservation constraints, action timing, and role maps. If a user requests a bilingual or mixed-language prompt, use language mixing only for clarity: reference roles, dialogue language, technical camera terms, and safe production constraints. Do not use another language to hide unsafe intent.

## Output Contract

Return:

1. Mode: T2V, I2V, V2V, R2V, FLF2V, edit, or extend.
2. Reference role map, if any.
3. Final prompt under the verified active-surface prompt budget.
4. Optional Chinese compressed version when useful.
5. Shot-list or delivery note when the prompt belongs to a professional sequence.
6. Safety or copyright note when relevant.

Before finalizing, run an anti-slop pass and remove vague quality boosters.
---

# SOURCE FILE: seedance_skills/seedance-camera/SKILL.md

---

---
name: seedance-camera
description: "This skill should be used when the user asks for camera movement, shot scale, lens feel, framing, one-take direction, dolly, pan, tilt, push-in, handheld, aerial, macro, or camera-transfer guidance for Seedance 2.0."
license: MIT
user-invocable: true
tags:
  - camera
  - cinematography
  - seedance-20
metadata:
  version: "6.6.0"
  updated: "2026-07-04"
  parent: "seedance-20"
  author: "Iamemily2050 (@iamemily2050)"
  repository: "https://github.com/Emily2040/seedance-2.0"
  openclaw:
    emoji: "🎬"
    homepage: "https://github.com/Emily2040/seedance-2.0"
---

# seedance-camera

Use one clear camera idea per short clip unless the user asks for a multi-shot sequence. The best camera direction has a start frame, movement, speed, subject relationship, and endpoint. Avoid stacking moves that fight each other, such as drone rise, dolly-in, handheld shake, and orbit in the same five-second shot.

Load `the Local Quick Reference section in this Knowledge` for prompt assembly, `the Local Cinematography Language section in this Knowledge` for professional shot contracts, `the Local Directing Engine section in this Knowledge` to derive the move from the scene's one intention so it reinforces light, performance, and sound instead of competing, and `clear professional camera terminology in the requested language` or `clear professional camera terminology in the requested language` when camera wording must be multilingual.

## Intent

When a user asks about camera, they are really asking where the viewer's body stands and what the viewer is made to feel from there. Camera grammar is empathy mechanics: a push-in is leaning closer, a locked frame is holding your breath. Choose the move that puts the audience where the user's feeling lives.

## Camera Contract

State: shot scale, angle, movement, speed, subject relationship, and endpoint. A prompt-ready camera phrase should be physically possible and tied to the subject's action.

| Need | Strong phrase | Avoid |
|---|---|---|
| Emotional realization | `slow dolly-in from medium close-up to tight close-up as Character A lowers the envelope` | `dramatic cinematic zoom` |
| Product reveal | `controlled slider move from silhouette to front three-quarter hero angle, ending on the label` | `dynamic product camera` |
| Scale | `low-angle crane up from boots to skyline, ending behind the character's shoulder` | `epic wide moving shot` |
| Instability | `subtle handheld shoulder camera, small breathing sway, subject kept centered` | `shaky chaotic camera everywhere` |
| Precision detail | `locked macro shot, focus stays on the watch gears while the second hand clicks once` | `cool close-up details` |

## Lens and Framing Anchors

Use lens anchors only when they improve direction: `24mm wide lens for spatial energy`, `35mm natural street perspective`, `50mm portrait compression`, `85mm shallow close-up`, or `macro lens for material detail`. Pair lens words with subject distance and motion; do not stack lens numbers as decoration.

## Move Selection

Use **locked-off** shots for lip-sync, product identity, and delicate VFX. Use **dolly-in** for discovery or realization. Use **tracking** for travel, pursuit, and product motion. Use **orbit** only when the subject can remain clear from all sides. Use **crane or drone** for scale, arrival, or reveal. Use **handheld** only when realism matters more than precision.

## Continuity Rules

For multi-character scenes, anchor the camera to named tags: `camera holds Character A in foreground while Character B crosses behind`. For I2V, preserve the image composition unless the user explicitly wants a reframing. For reference video, state whether `@Video1` transfers camera movement, action rhythm, or blocking; do not let it transfer identity unless authorized.

For complex camera movement, a video reference often works better than a long verbal stack. Use `@Video1 controls camera rhythm only; do not transfer performer, room, logo, or identity`.

## Conflict Rule

If the user gives several incompatible moves, choose one primary camera move and put the rest into optional variants. If the shot needs multiple beats, recommend splitting into separate clips or a time-segmented prompt.

## Sequence State

When sequence state is present, inherit the observed camera phase, screen direction, current clip scope, continuity locks, exact reference tags, and reserved future beats before choosing a move. A continuation camera phrase must begin from the accepted source frame or observed end state; do not restart a pan, focus pull, or tracking move unless an intentional next shot declares the reset.

## Output Contract

Return the selected camera phrase, why it fits the shot, conflicts removed, fragile anchors, endpoint, and a prompt-ready integrated sentence.
---

# SOURCE FILE: seedance_skills/seedance-motion/SKILL.md

---

---
name: seedance-motion
description: "This skill should be used when the user asks for body action, choreography, physics, object movement, movement timing, action continuity, stunt direction, or motion-reference mapping in Seedance 2.0."
license: MIT
user-invocable: true
tags:
  - motion
  - choreography
  - physics
  - seedance-20
metadata:
  version: "6.6.0"
  updated: "2026-07-04"
  parent: "seedance-20"
  author: "Iamemily2050 (@iamemily2050)"
  repository: "https://github.com/Emily2040/seedance-2.0"
  openclaw:
    emoji: "🎬"
    homepage: "https://github.com/Emily2040/seedance-2.0"
---

# seedance-motion

Use physical verbs and consequences. Motion should be observable on screen, timed within the clip, and assigned to a subject or object. Prefer one strong action with a visible endpoint over several vague actions competing for attention.

Load `the Reference Workflow section included earlier in this Knowledge` for video-motion references, `the Local Shot Continuity Rules section in this Knowledge` for action handoffs across shots, `the Local Mode Examples section in this Knowledge` for safe edit, extend, and R2V patterns, and `the Local Directing Engine section in this Knowledge` when motion is performance: translate the scene's emotion into one true visible gesture per beat - a playable action with an objective and subtext - instead of an emotion word the model cannot render.

## Intent

Motion is the verb of the user's story - the thing they came to see HAPPEN. The soul here is consequence: motion that begins, lands, and changes something feels lived; motion that loops feels generated. Every action carries the story one beat forward, or it doesn't belong in the clip.

## Motion Contract

State: actor/object, action, force level, timing, physical consequence, continuity requirement, and endpoint.

| Motion type | Strong phrase | Weak phrase |
|---|---|---|
| Subtle acting | `Character A inhales, grips the cup tighter, then sets it down without looking away` | `she feels nervous` |
| Product material | `condensation beads gather, merge, and slide down the bottle neck` | `the product looks refreshing` |
| Choreography | `Character B ducks under the swinging bag, pivots left, and stops in a guarded stance` | `fast action fight scene` |
| Object physics | `paper receipt lifts in the fan breeze, flips once, and lands face-up` | `papers move dynamically` |
| Environmental motion | `rain streaks diagonally across the backlight while puddle ripples spread from footsteps` | `stormy weather atmosphere` |

## Physics-Forward Pattern

Official material claims strong physics; extract it by writing causes and letting the model compute consequences (field-observed emphasis - test before promising results). State mass, force, and material, then name one consequence the camera can see: `the heavy oak door swings shut and the candle flames bend toward it` beats `the door closes dramatically`. Consequences prove the action: weight shows in landing compression, momentum in overshoot and recovery, friction in skid length, wind in what it displaces. One physical cause with two or three visible consequences reads stronger than three separate actions.

## Timing Pattern

Use a three-beat structure for short clips: setup, action, changed end state. Example: `0-2s: candle flame steady; 2-4s: door opens and flame bends; 4-6s: smoke trail curls toward the hallway`. Time segmentation is useful for action, VFX, lip-sync, and product demonstrations, but avoid frame-perfect overload unless the user truly needs it.

When sound drives the motion, pair each visible change with one beat or SFX: `door click at 2s, light pulse on the downbeat, hand releases the cup on the final chime`. Do not ask for many cuts, locations, and micro-actions inside one short clip.

## Reference Motion Rules

For reference footage, use only owned, licensed, public-domain, stock, mocap, rehearsal, or self-recorded material. Map `@Video1` to motion, camera, timing, or blocking, not identity, unless the identity is authorized. If a reference contains a real person, transfer only general motion or camera behavior and explicitly exclude likeness transfer.

## Stability Rules

Hands, faces, logos, and product geometry drift when too many actions occur. Reduce motion around fragile details: lock the camera for lip-sync, keep hands in simple poses, ask product parts to remain rigid, and move light or environment instead of the core identity anchor.

## Sequence State

When sequence state is present, inherit the observed action phase, open motion vector, current clip scope, continuity locks, exact reference tags, and reserved future beats. Do not replay actions marked already happened or completed. Do not perform a reserved beat early; carry unfinished motion from the accepted end state into the next clip.

## Output Contract

Return the motion phrase, timing pattern, reference role map if any, and repaired prompt language.
