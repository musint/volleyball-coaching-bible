# Club Coaching Standards Manual — Design Spec

**Date:** 2026-04-25
**Owner:** Song Mu (song.mu@discordapp.com)
**Predecessor specs:**
- `docs/superpowers/specs/2026-04-22-volleyball-coaching-bible-design.md` (bootstrap)
- `docs/superpowers/specs/2026-04-24-wiki-improvement-tracks-1-2-design.md` (usability + integrity)
- `docs/superpowers/specs/2026-04-25-tracks-a-b-c-design.md` (boil-the-ocean tracks)

---

## 1. Context

### 1.1 Why this work

Song is the head coach of a nationally-recognized 14U girls club program. After Tracks A+B+C lands the comprehensive coaching reference, he wants a unified **Club Coaching Standards Manual** — the load-bearing artifact that turns the wiki into a *club operating system* his coaches can use to run consistent skill training across age groups (10s through 18s) the way Munciana does.

The model is Munciana's club-wide system alignment (documented at `wiki/schools/munciana-volleyball-club.md` from the 2026-04-25 ingest): every age group runs the same skill-training and systems vocabulary, so players never have to relearn technique as they move up. The Manual operationalizes that strategy for Song's own club.

The manual answers four questions, per age:

1. **What skills should a player at this age master?** (skill milestones)
2. **What cues do all our coaches use to teach those skills?** (cue dictionary)
3. **Which drills do we use to train them?** (drill pick-list)
4. **How do we evaluate them at tryouts?** (tryout rubric)

### 1.2 Stance

**Load-bearing core only** (Option B from the 2026-04-25 brainstorm). Nine age-level guides, seven cue dictionaries, nine drill pick-lists, nine tryout rubrics (replacing the four currently scoped in Dispatch C). Cross-cutting club docs — philosophy, parent comms, coach onboarding, athlete self-development guides — are deferred to a future Manual v2 spec.

### 1.3 Sequencing relative to Dispatch C

Dispatch C from the Tracks A+B+C spec is **adjusted**: it ships its non-rubric items (5 macrocycles + 5 microcycles + 5 match-prep templates + 8 club-ops docs + SCHEMA `practice-plan` extension + `ops-doc` page type addition). The 4 originally-scoped tryout rubrics (14U/16U/18U/college walk-on) **move to this Manual project** so all 9 ages get rubrics in unified format aligned with Module 1 milestones.

### 1.4 Positioning

Unchanged. Neutral reference. The manual is *opinionated about the club's choices* (which is the point of a club standards manual) but transparent about which choices are universal volleyball wisdom (cite the wiki) and which are club-specific calls (note as such).

---

## 2. Scope

### 2.1 Deliverable matrix

| Module | New pages | Source backing |
|---|---:|---|
| 1. Age-guides (10s through 18s) | 9 | Wiki age-lens + Track B research + Track A schools |
| 2. Cue dictionary (per skill) | 7 + 1 hub = 8 | Wiki techniques + AOC corpus + Munciana camp |
| 3. Drill pick-list per age | 9 | Wiki drills (101-drill library) + Munciana camp |
| 4. Tryout rubrics (all 9 ages) | 9 | Module 1 milestones (rubric criteria align) |
| **Total** | **35** | All cross-referenced to existing wiki content |

Plus SCHEMA additions, lint.py extension, and `wiki/index.md` updates.

### 2.2 Non-goals (deferred to Manual v2)

- Club philosophy / culture / values document
- Parent-facing expectations doc per age
- Coach onboarding doc (how a new assistant learns the system)
- Athlete self-development guides per age
- Mentorship structure within the club
- Decision frameworks for coaches (sub timing, timeout timing — captured by Dispatch C's match-prep in-match-adjustment template, sufficient for v1)
- Boys'/men's club coaching layer (same skills, different demographics — defer)
- Beach / sitting volleyball (out of scope per bootstrap)

These deferrals are not rejection — they are sequencing.

---

## 3. Page types & contracts

### 3.1 Age-guide pages (Module 1, new page type)

**Folder / filename:** `wiki/age-guides/<age>.md` (e.g., `12s.md`)

**Frontmatter:**
```yaml
---
type: age-guide
age: 12s                                  # enum: 10s, 11s, 12s, 13s, 14s, 15s, 16s, 17s, 18s
phase: late-fundamentals                  # enum: introduction, fundamentals, late-fundamentals, specialization, advanced, college-bridge
sources: [<≥3 — typically the related age-lens page + Track B research + AOC age-specific pieces>]
---
```

**Required body sections:**
1. `## Overview & development phase` — what age this serves, where it sits in the club's developmental arc, what changes from the prior age-guide
2. `## Skill milestones` — subsections per skill (passing / setting / hitting / blocking / serving / defense / transition); each subsection lists the specific technical milestones a player at this age should be able to demonstrate
3. `## Systems repertoire` — what offensive/defensive/SR/blocking systems are appropriate at this age (with wikilinks to `systems-detail/`)
4. `## Athletic profile` — physical markers (vertical, approach jump touch, range), with explicit medical-disclaimer language for jump-training and conditioning
5. `## Mental & coachability markers` — what cognitive/emotional development to expect, what to coach toward
6. `## Promotion criteria` — what a player needs to demonstrate before promoting to the next age-guide (this becomes the corresponding tryout rubric's evaluation criteria)
7. `## Common coaching corrections` — at this age, what fails most and how to fix it
8. `## Recommended drills` — short paragraph + wikilink to the drill-pick-list for this age (Module 3)
9. `## Recommended cues` — wikilinks to the cue dictionary (Module 2) for the relevant subskills
10. `## Sources`

**Target length:** 2500-3000 words.

**Citation weight:** Heavy. Inline `[citation-key]` after each non-generic claim. The Track B sports-science research strengthens claims about jump training, ACL prevention, motor-learning expectations, and adolescent development. Wiki age-lens pages (14U/HS/college) are the parent context for ages they overlap.

**Cross-link rules:**
- Each age-guide wikilinks to the corresponding `wiki/drill-picks/<age>-drills.md`
- Each age-guide wikilinks to the corresponding `wiki/ops/tryout-rubric-<age>.md`
- Subskill mentions wikilink to `wiki/cues/<skill>-cues.md`
- Adjacent age-guides cross-reference each other (`12s.md` links `[[11s]]` and `[[13s]]`)
- 14s/16s/18s wikilink the existing age-lens pages (14U, HS for 16s as it overlaps, college for 18s as the bridge)

### 3.2 Cue-dictionary pages (Module 2, new page type)

**Folder / filename:** `wiki/cues/<skill>-cues.md` (e.g., `passing-cues.md`)

**Frontmatter:**
```yaml
---
type: cue-dictionary
skill: passing                            # enum from existing skill set: passing, setting, hitting, blocking, serving, defense, transition
age-bands: [10s, 11s, 12s, 13s, 14s, 15s, 16s, 17s, 18s]
sources: [<≥3>]
---
```

**Required body sections:**
1. `## Overview` — why these are the canonical club cues; what makes a good cue
2. `## Per-subskill canonical cues` — subsections per subskill (e.g., for passing: forearm, overhead, serve-receive, free-ball). Each subsection lists 1–3 canonical cues; for each cue: (a) the exact words a coach says, (b) the age-band when introduced, (c) the age-band when refined or replaced, (d) the cue rationale (what it teaches, why this phrasing, what it does NOT teach)
3. `## Anti-cues` — phrases that sound right but mislead; what a coach should say *instead*
4. `## Voice consistency notes` — when two cues from different schools conflict (e.g., AOC "set the angle" vs GMS "small-arm movement"), how the club resolves
5. `## Sources`

**Target length:** 1200–1800 words.

**Citation weight:** Heavy.

**Cross-link rules:** wikilinks to relevant technique pages and to coach pages whose cues are cited (Kiraly, Stone, Liskevych, Lingenfelter, etc.).

### 3.3 Cue-dictionary hub (Module 2)

**File:** `wiki/cues.md` (single hub page)

**Frontmatter:**
```yaml
---
type: hub
area: coaching-cues
subtopics: [passing-cues, setting-cues, hitting-cues, blocking-cues, serving-cues, defense-cues, transition-cues]
---
```

Standard hub-page contract. Acts as entry point to the 7 cue-dictionary pages. ~600-800 words.

### 3.4 Drill-pick-list pages (Module 3, new page type)

**Folder / filename:** `wiki/drill-picks/<age>-drills.md` (e.g., `12s-drills.md`)

**Frontmatter:**
```yaml
---
type: drill-pick-list
age: 12s                                  # enum
season-context: composite                 # or specific phase
drills: [<≥10 drill slugs from existing wiki/drills/>]
sources: [<≥1 — typically munciana-2022-camp-drills + the parent age-lens + AOC age-specific pieces>]
---
```

**Required body sections:**
1. `## Purpose` — why these specific drills for this age
2. `## Must-do drill list` — 10–15 drills as wikilinks, grouped by skill (passing/setting/hitting/blocking/serving/defense/transition), with 1-line rationale per drill (why this drill at this age)
3. `## When-in-season-to-use mapping` — which drills are preseason install vs in-season repetition vs pre-tournament sharpening
4. `## Adaptations` — what changes if you have less time, fewer players, more advanced players
5. `## Sources`

**Target length:** 600–900 words.

**Citation weight:** Light.

**Cross-link rules:** every drill in `drills:` frontmatter must resolve to a real `wiki/drills/<slug>.md` page. The corresponding age-guide wikilinks back to this page.

### 3.5 Tryout-rubric pages (Module 4, extension of existing `ops-doc` type from Dispatch C)

Uses the existing `ops-doc` `kind: tryout-rubric` page type defined in Dispatch C's SCHEMA §3.11. Manual contributes 9 rubrics covering 10s/11s/12s/13s/14s/15s/16s/17s/18s.

**Each rubric's evaluation criteria mirror the corresponding age-guide's `## Promotion criteria` section** — that's the unifying-principle: the milestones a 12s player needs to graduate are the criteria a 13s tryout evaluates against.

The college-walk-on rubric originally scoped in Dispatch C is preserved as a separate `wiki/ops/tryout-rubric-college-walkon.md` page (it's an outlier, not part of the 9-age progression). It is built alongside the 9 ages here for unified format.

**Total tryout rubrics shipped by Manual: 10** (9 ages + 1 college walk-on).

---

## 4. SCHEMA additions

- **§3.12 (new) `age-guide` page type** — full contract per §3.1 above
- **§3.13 (new) `cue-dictionary` page type** — full contract per §3.2 above
- **§3.14 (new) `drill-pick-list` page type** — full contract per §3.4 above
- **§4 enum glossary additions:**
  - `age ∈ {10s, 11s, 12s, 13s, 14s, 15s, 16s, 17s, 18s}` (age-guide / drill-pick-list / tryout-rubric)
  - `phase ∈ {introduction, fundamentals, late-fundamentals, specialization, advanced, college-bridge}` (age-guide)
  - `season-context ∈ {composite, preseason, mid-season, pre-tournament, taper, tryout, postseason, match-day}` (drill-pick-list — reuses practice-plan's season-phase enum plus `composite`)
- **`tools/lint.py`** — extend `REQUIRED_FIELDS` and `ENUM_VALUES` to validate the three new page types
- **`tools/test_lint.py`** — add 3 regression tests (one per new page type)

These build on Dispatch C's SCHEMA additions for `ops-doc` and `practice-plan.scope`, which are prerequisites.

---

## 5. Module-by-module deliverables

### 5.1 Module 1 — Age-guides (9 pages)

One agent per age. Each agent reads the parent age-lens (14U for 13s/14s/15s; HS for 16s/17s/18s; reasonable extrapolation for 10s/11s/12s using USAV growing-kids guidance), Track B injury + adolescent-development research, and Munciana methodology.

**Per-age phase mapping (preliminary, agents may refine):**
- 10s: introduction
- 11s: introduction → fundamentals transition
- 12s: fundamentals
- 13s: late-fundamentals
- 14s: late-fundamentals → specialization onset
- 15s: specialization
- 16s: specialization
- 17s: advanced
- 18s: college-bridge

### 5.2 Module 2 — Cue dictionaries (7 + 1 hub)

One agent per skill (7 agents) writing canonical cues:
- `passing-cues.md` — Kiraly's 4 keys; Bechard's posture-pursuit-platform; Stone's late-platform-formation; Lingenfelter's quiet-platform / pass-and-cover micro-skills
- `setting-cues.md` — hand-hinge framing; Rockwell's setter-training corpus; Lingenfelter's plant-timing tempo (Tempo 1/2/3)
- `hitting-cues.md` — Schmidt's "start slow, accelerate the last two steps"; Mattox's Sight-90 / Elbow-Lead / Lift-and-Whip; MacDonald's torque + high-hand
- `blocking-cues.md` — outside-foot-high (Munciana); read-then-jump; swing-block footwork progressions; Slabe's hand-press
- `serving-cues.md` — aim small, miss small (Munciana); Mattox Lift/Step/Swing; Dunning toss-first; aggressive mentality
- `defense-cues.md` — Three P's (get-back, get-low, get-touch) (Munciana); Stone hips-under-ball; Look/See/Decide
- `transition-cues.md` — block-to-approach recovery; dig-to-approach; OOS detect/call/bail-to-pin

One agent for `wiki/cues.md` hub (or this hub is written by the cross-link coordinator at the end).

### 5.3 Module 3 — Drill-pick-lists (9 pages)

One agent per age. Each agent picks 10–15 drills from the existing 101-drill library tagged appropriate for that age (`levels:` frontmatter contains the appropriate level — 14u/hs/college mapped against the fine-grained age). Munciana camp drills (46 of them) are heavily represented since the 2022 camp library is age-band-versatile.

For 10s/11s/12s: the existing drill library is mostly tagged `levels: [14u]` because 14U is the youngest level documented. The drill-pick-list agents must infer down-scaling — the 10s pick-list should bias toward warm-up + ball-control + simple cooperative-game drills; introduce competitive-grading drills at 13s; jump-training-heavy drills appear from 15s; full game-like drills at 16s+. Simply listing `[14u]`-tagged drills for 10s would mis-scale.

### 5.4 Module 4 — Tryout rubrics (9 + 1 = 10 pages)

One agent per age (9) plus one for college walk-on. Each agent reads the corresponding age-guide's `## Promotion criteria` section (already produced by Module 1 agents in the same dispatch — agents must coordinate or this becomes a dependency to sequence) and translates those criteria into a 1–5 (or 1–4) scoring rubric per skill.

**Sequencing within Manual dispatch:** Module 1 agents must complete `## Promotion criteria` sections before Module 4 agents start, OR Module 4 agents accept a brief from this spec that anchors the rubric criteria to Module 1's planned structure. Practical solution: Module 1 agents produce a brief "promotion criteria summary" YAML block at the top of their output for Module 4 to consume, OR Module 4 launches in a second sub-dispatch after Module 1 lands.

For execution: launch Module 1 first (parallel 9 agents), then Module 4 (parallel 10 agents) as a second sub-dispatch.

### 5.5 Index updates

`wiki/index.md` adds:

```markdown
## Club Coaching Standards Manual (Track D — 2026-04-25)

### Age-guides (10s through 18s)
- [[10s]] — introduction phase
- [[11s]] — introduction → fundamentals
- [[12s]] — fundamentals
- [[13s]] — late-fundamentals
- [[14s]] — late-fundamentals → specialization onset
- [[15s]] — specialization
- [[16s]] — specialization
- [[17s]] — advanced
- [[18s]] — college-bridge

### Cue dictionary
- [[cues]] — hub
- [[passing-cues]], [[setting-cues]], [[hitting-cues]], [[blocking-cues]], [[serving-cues]], [[defense-cues]], [[transition-cues]]

### Drill pick-lists
- [[10s-drills]], [[11s-drills]], [[12s-drills]], [[13s-drills]], [[14s-drills]], [[15s-drills]], [[16s-drills]], [[17s-drills]], [[18s-drills]]

### Tryout rubrics (per age)
(in Operations section): tryout-rubric-10s, -11s, -12s, -13s, -14u, -15s, -16u, -17s, -18u, -college-walkon
```

---

## 6. Execution strategy

### 6.1 Two sub-dispatches within Track D (Manual)

**Sub-dispatch D.1 — Module 1 + Module 2 + Module 3 + SCHEMA (parallel ~26 agents):**
- 9 × age-guide writers (Module 1)
- 7 × cue-dictionary writers (Module 2)
- 1 × cue-dictionary hub writer
- 9 × drill-pick-list writers (Module 3)
- 1 × SCHEMA + lint.py + test_lint.py update agent

**Sub-dispatch D.2 — Module 4 tryout rubrics (parallel ~10 agents) + cross-link coordinator:**
- 10 × tryout-rubric writers (one per age + college walk-on), each reading the corresponding age-guide's promotion criteria
- 1 × index/log/cross-link coordinator (after rubrics land)

Lint checkpoint between D.1 and D.2; final acceptance walkthrough after D.2.

### 6.2 Dispatch C concurrent execution

Dispatch C is **adjusted** to ship its non-rubric items only:
- 5 macrocycle templates
- 5 microcycle templates
- 5 match-prep templates
- 8 club-ops docs
- SCHEMA `practice-plan.scope` extension + new `ops-doc` page type

Dispatch C's 4 originally-scoped tryout rubrics (14U/16U/18U/college walk-on) are removed from Dispatch C and become part of Manual sub-dispatch D.2.

Dispatch C runs in parallel with Manual sub-dispatch D.1 (different files, no conflicts). Manual sub-dispatch D.2 runs after BOTH Dispatch C and D.1 complete (D.2 needs Dispatch C's `ops-doc` page type definition AND D.1's age-guide promotion criteria).

Effective sequence:
1. Dispatch C and Manual D.1 in parallel (~30 + ~26 = 56 agents — split into two parallel waves to keep dispatch sizes manageable)
2. Lint checkpoint
3. Manual D.2 (tryout rubrics)
4. Final acceptance walkthrough

### 6.3 Cross-track coordination

Each writer agent gets explicit guidance: read SCHEMA, read existing wiki content (especially Munciana methodology + Track A/B sources), use real source-page slugs that exist on disk, never fabricate citations.

---

## 7. Success criteria

### 7.1 Acceptance checklist

Manual complete when all of these hold:

**Module 1 (Age-guides):**
- [ ] 9 pages exist at `wiki/age-guides/<age>.md`
- [ ] Each has required frontmatter + 10 body sections
- [ ] Each has heavy citation density (≥10 inline citations per page)
- [ ] Each has `## Promotion criteria` populated (drives Module 4)
- [ ] Each cross-references its drill-pick-list and the relevant cue-dictionary entries

**Module 2 (Cue dictionaries):**
- [ ] 7 skill-cue-dictionary pages exist at `wiki/cues/<skill>-cues.md`
- [ ] 1 hub page exists at `wiki/cues.md`
- [ ] Each cue page has subsections per subskill with 1–3 canonical cues + age-band + rationale per cue
- [ ] Each cue page has an `## Anti-cues` section

**Module 3 (Drill pick-lists):**
- [ ] 9 pages exist at `wiki/drill-picks/<age>-drills.md`
- [ ] Each has 10–15 wikilinked drills, all resolving to real `wiki/drills/` pages
- [ ] Each has age-down-scaling rationale where the master drill library is `[14u]`-tagged

**Module 4 (Tryout rubrics):**
- [ ] 10 pages exist at `wiki/ops/tryout-rubric-<age>.md` (9 ages + college-walkon)
- [ ] Each has evaluation criteria aligned with the corresponding age-guide's promotion criteria
- [ ] Scoring scale documented; calibration notes present

**Cross-cutting:**
- [ ] SCHEMA.md updated with §3.12 + §3.13 + §3.14 + enum additions
- [ ] tools/lint.py extended; tools/test_lint.py has 3 new regression tests passing
- [ ] wiki/index.md reflects all new sections
- [ ] wiki/log.md has Track D dispatch entries
- [ ] Broken-wikilink count ≤10 in final lint
- [ ] Invariant violations: 0
- [ ] Memory updated

### 7.2 Scenario tests

Three real questions the Manual must answer cleanly:

1. **"What does my 14s player need to demonstrate before I promote her to 15s?"** — Answer comes verbatim from `wiki/age-guides/14s.md` `## Promotion criteria`.
2. **"What's the canonical Munciana-style cue for forearm passing at 12s?"** — Answer comes from `wiki/cues/passing-cues.md` "12s introduces / 13s refines" cue entry.
3. **"What 10 drills should I run with my 13s team this preseason?"** — Answer comes from `wiki/drill-picks/13s-drills.md` "Must-do drill list" section, with `season-context: preseason` filter applied.

### 7.3 Living-manual signals

- A new assistant coach can read their age-guide + their age's drill-pick-list + the relevant cue dictionaries in one practice-prep session and walk on the court using club-canonical vocabulary
- Tryouts at every age use the corresponding rubric; calibration is documented; cross-evaluator scoring agreement is mechanizable
- Athlete promotions are evaluated against documented criteria, not against ad-hoc coach impressions
- The wiki's graph view shows age-guides as a connected ladder (10s → 11s → 12s → ... → 18s) with cross-links into cue dictionaries and drill pick-lists at each level

---

## 8. Open items & caveats

1. **Down-scaling drill picks for 10s/11s/12s.** The master drill library is `[14u]`-tagged at the youngest. Module 3 agents must scale down rather than just filter. Risk: agents over-include 14U-appropriate-only drills for 10s. Mitigation: explicit guidance in agent briefs to prefer warm-up / ball-control / cooperative-game drills for younger ages and not introduce penalty-heavy or jump-heavy drills below 13s.
2. **Module 4 rubric criteria depend on Module 1 promotion-criteria sections.** Sequencing risk if Module 4 launches before Module 1 finishes. Mitigation: D.2 runs after D.1, not in parallel.
3. **Cue-dictionary contestation.** Module 2 must take a club-side on cue choices where schools genuinely disagree (per §3.2 voice-consistency notes section). Risk: agents pick arbitrarily. Mitigation: agent briefs name the club's lean (modern AOC + Munciana primary; GMS for motor-learning rationale; Japanese for defense identity) per the existing `feedback_recency_preference` memory.
4. **Promotion criteria as objective evaluation.** Some milestones are quantitative (vertical, approach jump touch); most are qualitative (platform-stability under live serve). Rubric calibration relies on coach judgment. The Manual provides a calibration framework, not an algorithm.
5. **Boys'/men's club applicability.** The Manual is written assuming girls'-club context (Song's environment). Cross-applicability to boys'/men's clubs is largely transferable but the 18s → college-bridge phase differs (men's college timing + skill expectations differ). Out of scope for v1.
6. **Manual v2 backlog.** Cross-cutting club philosophy, parent comms, coach onboarding, athlete self-development guides, mentorship structure are deferred. They are real and valuable; sequencing puts them after the load-bearing core lands.

---

## 9. Next step

Hand off to the writing-plans skill to produce a sub-dispatch-by-sub-dispatch implementation plan with concrete agent briefing templates, acceptance checks, and the parallel-execution coordination details.
