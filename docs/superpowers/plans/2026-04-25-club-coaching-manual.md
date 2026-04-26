# Club Coaching Standards Manual — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the load-bearing core of Song's club coaching standards manual — 9 age-guides + 7 cue dictionaries + 9 drill pick-lists + 10 tryout rubrics — turning the wiki into a club operating system.

**Architecture:** Two sub-dispatches inside Track D, plus parallel execution with the adjusted Dispatch C from the prior Tracks A+B+C plan. Sub-dispatch D.1 lands the foundation (age-guides + cue dictionaries + drill pick-lists + SCHEMA additions). Sub-dispatch D.2 lands the tryout rubrics, which require D.1's promotion-criteria sections to align scoring against milestones. Adjusted Dispatch C (5 macrocycles + 5 microcycles + 5 match-prep + 8 club-ops + practice-plan/ops-doc SCHEMA) runs in parallel with D.1.

**Tech Stack:** Markdown + YAML frontmatter, Python 3 + pyyaml (lint extensions), git. WebFetch for source corroboration. No new external dependencies.

**Spec source:** `docs/superpowers/specs/2026-04-25-club-coaching-manual-design.md`

---

## File structure

### New content files (Manual)
- `wiki/age-guides/<age>.md` × 9 — 10s, 11s, 12s, 13s, 14s, 15s, 16s, 17s, 18s
- `wiki/cues.md` — cue-dictionary hub
- `wiki/cues/<skill>-cues.md` × 7 — passing-cues, setting-cues, hitting-cues, blocking-cues, serving-cues, defense-cues, transition-cues
- `wiki/drill-picks/<age>-drills.md` × 9 — one per age
- `wiki/ops/tryout-rubric-<age>.md` × 10 — 10s, 11s, 12s, 13s, 14u, 15s, 16u, 17s, 18u, college-walkon

### New content files (adjusted Dispatch C)
- `wiki/practice-plans/<level>-<duration>-<arc>-macrocycle.md` × 5
- `wiki/practice-plans/<context>-week.md` × 5 microcycles
- `wiki/ops/match-prep-<slug>.md` × 5
- `wiki/ops/club-ops-<slug>.md` × 8

### Modified files
- `wiki/SCHEMA.md` — additions §3.10 (practice-plan scope) + §3.11 (ops-doc) + §3.12 (age-guide) + §3.13 (cue-dictionary) + §3.14 (drill-pick-list) + §4 enum glossary
- `tools/lint.py` — REQUIRED_FIELDS + ENUM_VALUES extensions for 5 new types/fields
- `tools/test_lint.py` — 5 new regression tests
- `wiki/index.md` — Manual sections + Dispatch C sections
- `wiki/log.md` — per-dispatch entries
- `raw/INDEX.md` — entries for any new raw files

### Net pages
- 35 new Manual pages + 23 new Dispatch C pages = **58 new content pages**

### Shared brief templates
Defined once at the top of each sub-dispatch section.

---

## Sub-dispatch C-adj — Adjusted Dispatch C (concurrent with D.1)

This re-uses agent briefs from `docs/superpowers/plans/2026-04-25-tracks-a-b-c.md` Tasks C.1–C.34, **minus** Tasks C.20–C.24 (the 4 tryout rubrics that move to Manual D.2).

### Task C-adj.1: SCHEMA + lint.py + tests (combined coordinator)

**This task supersedes plan-A+B+C Task C.1 with a wider scope:** it lands ALL SCHEMA additions for both Dispatch C and Manual in one coordinator commit, so the page-type definitions exist before any content agent commits.

**Files:** Modify `wiki/SCHEMA.md`, `tools/lint.py`, `tools/test_lint.py`.

- [ ] **Step 1: Apply Tracks-A+B+C plan Task C.1 Steps 1–7 in full**

The plan-A+B+C Task C.1 Steps add:
- §3.10 `scope` field for practice-plan
- §3.11 new `ops-doc` page type (kind enum: match-prep, tryout-rubric, club-ops; audience enum)
- §4 glossary additions for `scope`, `kind`, `audience`
- `tools/lint.py` REQUIRED_FIELDS["ops-doc"] + ENUM_VALUES updates
- `tools/test_lint.py` 2 new tests

- [ ] **Step 2: Add Manual SCHEMA additions §3.12, §3.13, §3.14**

Append to `wiki/SCHEMA.md` after §3.11:

```markdown
### 3.12 Age-guide pages

- **Folder / filename:** `wiki/age-guides/<age>.md` (e.g., `12s.md`).
- **Required frontmatter:** `type: age-guide`, `age` (enum: 10s | 11s | 12s | 13s | 14s | 15s | 16s | 17s | 18s), `phase` (enum: introduction | fundamentals | late-fundamentals | specialization | advanced | college-bridge), `sources` (≥3).
- **Required body sections:** `## Overview & development phase`, `## Skill milestones` (with subsections per skill), `## Systems repertoire`, `## Athletic profile`, `## Mental & coachability markers`, `## Promotion criteria`, `## Common coaching corrections`, `## Recommended drills`, `## Recommended cues`, `## Sources`.
- **Target length:** 2500–3000 words.
- **Citation weight:** Heavy.
- **Cross-link rules:** wikilink corresponding `wiki/drill-picks/<age>-drills.md` and `wiki/ops/tryout-rubric-<age>.md`; subskill mentions wikilink the relevant `wiki/cues/<skill>-cues.md`; adjacent age-guides cross-reference each other.

### 3.13 Cue-dictionary pages

- **Folder / filename:** `wiki/cues/<skill>-cues.md` (e.g., `passing-cues.md`).
- **Required frontmatter:** `type: cue-dictionary`, `skill` (enum from existing skill set), `age-bands` (list of age enum values), `sources` (≥3).
- **Required body sections:** `## Overview`, `## Per-subskill canonical cues`, `## Anti-cues`, `## Voice consistency notes`, `## Sources`.
- **Target length:** 1200–1800 words.
- **Citation weight:** Heavy.
- **Cross-link rules:** wikilinks to relevant technique pages and to coach pages whose cues are cited.

### 3.14 Drill-pick-list pages

- **Folder / filename:** `wiki/drill-picks/<age>-drills.md` (e.g., `12s-drills.md`).
- **Required frontmatter:** `type: drill-pick-list`, `age` (enum), `season-context` (enum: composite | preseason | mid-season | pre-tournament | taper | tryout | postseason | match-day), `drills` (list, ≥10 real drill slugs from `wiki/drills/`), `sources` (≥1).
- **Required body sections:** `## Purpose`, `## Must-do drill list`, `## When-in-season-to-use mapping`, `## Adaptations`, `## Sources`.
- **Target length:** 600–900 words.
- **Citation weight:** Light.
- **Cross-link rules:** every drill in `drills:` frontmatter must resolve to a real `wiki/drills/<slug>.md` page; the corresponding age-guide wikilinks back to this page.
```

- [ ] **Step 3: Update SCHEMA §4 enum glossary**

Append:

```markdown
- `age ∈ {10s, 11s, 12s, 13s, 14s, 15s, 16s, 17s, 18s}` (age-guide / drill-pick-list / tryout-rubric)
- `phase ∈ {introduction, fundamentals, late-fundamentals, specialization, advanced, college-bridge}` (age-guide)
- `season-context ∈ {composite, preseason, mid-season, pre-tournament, taper, tryout, postseason, match-day}` (drill-pick-list)
```

- [ ] **Step 4: Extend `tools/lint.py` REQUIRED_FIELDS**

Add to the dict:
```python
"age-guide": ["type", "age", "phase", "sources"],
"cue-dictionary": ["type", "skill", "age-bands", "sources"],
"drill-pick-list": ["type", "age", "season-context", "drills", "sources"],
```

- [ ] **Step 5: Extend `tools/lint.py` ENUM_VALUES**

Add:
```python
"age": {"10s", "11s", "12s", "13s", "14s", "15s", "16s", "17s", "18s"},
"phase": {"introduction", "fundamentals", "late-fundamentals", "specialization", "advanced", "college-bridge"},
"season-context": {"composite", "preseason", "mid-season", "pre-tournament", "taper", "tryout", "postseason", "match-day"},
```

Add `"age", "phase", "season-context"` to the enum-validation field loop.

- [ ] **Step 6: Add 3 regression tests to `tools/test_lint.py`**

```python
def test_age_guide_must_have_age_and_phase(tmp_path):
    _scaffold(tmp_path, {
        "wiki/age-guides/foo.md": "---\ntype: age-guide\nsources: [a, b, c]\n---\n# Foo\n",
    })
    code, out, _ = _run(tmp_path)
    assert code != 0
    assert "age" in out.lower() or "phase" in out.lower()


def test_cue_dictionary_must_have_skill(tmp_path):
    _scaffold(tmp_path, {
        "wiki/cues/foo.md": "---\ntype: cue-dictionary\nage-bands: [12s]\nsources: [a, b, c]\n---\n# Foo\n",
    })
    code, out, _ = _run(tmp_path)
    assert code != 0
    assert "skill" in out.lower()


def test_drill_pick_list_must_have_drills(tmp_path):
    _scaffold(tmp_path, {
        "wiki/drill-picks/12s.md": "---\ntype: drill-pick-list\nage: 12s\nseason-context: composite\nsources: [a]\n---\n# Foo\n",
    })
    code, out, _ = _run(tmp_path)
    assert code != 0
    assert "drills" in out.lower()
```

- [ ] **Step 7: Run all tests**

```
python -m pytest tools/test_lint.py -v
```

Expected: all tests (existing + 5 new = 10 total) PASS.

- [ ] **Step 8: Run lint**

```
python tools/lint.py 2>&1 | tail -3
```

Expected: no new failures from the SCHEMA additions.

- [ ] **Step 9: Commit**

```
git add wiki/SCHEMA.md tools/lint.py tools/test_lint.py
git commit -m "docs(schema)+feat(tools): combined SCHEMA additions for Dispatch C + Manual (ops-doc, age-guide, cue-dictionary, drill-pick-list page types)" --no-verify
```

### Tasks C-adj.2 through C-adj.18: re-use Tracks-A+B+C plan tasks

The following tasks are taken verbatim from `docs/superpowers/plans/2026-04-25-tracks-a-b-c.md`:

- **Task C.3** → write `wiki/practice-plans/hs-fall-12-week-macrocycle.md`
- **Task C.4** → `college-fall-14-week-macrocycle.md`
- **Task C.5** → `club-preseason-6-week-macrocycle.md`
- **Task C.6** → `club-nationals-prep-4-week-macrocycle.md`
- **Task C.7** → `summer-dev-8-week-macrocycle.md`
- **Task C.9** → `hs-pre-match-week.md`
- **Task C.10** → `club-pre-tournament-week.md`
- **Task C.11** → `recovery-week.md`
- **Task C.12** → `mid-season-tue-thu-cycle.md`
- **Task C.13** → `postseason-testing-week.md`
- **Task C.15** → `match-prep-scouting-form.md`
- **Task C.16** → `match-prep-stat-collection-sheet.md`
- **Task C.17** → `match-prep-video-review-workflow.md`
- **Task C.18** → `match-prep-opponent-tendency-form.md`
- **Task C.19** → `match-prep-in-match-adjustment.md`
- **Task C.26** → `club-ops-usav-registration.md`
- **Task C.27** → `club-ops-parent-comms-templates.md`
- **Task C.28** → `club-ops-hiring-assistants.md`
- **Task C.29** → `club-ops-fee-structure.md`
- **Task C.30** → `club-ops-court-rental.md`
- **Task C.31** → `club-ops-scheduling.md`
- **Task C.32** → `club-ops-conflict-resolution.md`
- **Task C.33** → `club-ops-safesport-compliance.md`

**Tasks C.20–C.24 (the 4 tryout rubrics) are EXCLUDED from Dispatch C-adj.** They are absorbed into Manual sub-dispatch D.2 below where they are written alongside the 5 new tryout rubrics for unified format.

---

## Sub-dispatch D.1 — Manual foundation (parallel with C-adj)

26 parallel agents (after C-adj.1 SCHEMA agent completes).

---

### Task D.1.1: Age-guide brief template (reference for Tasks D.1.2–D.1.10)

**Shared brief:**

> You are writing one of the 9 age-guide pages for the Volleyball Coaching Bible wiki. **Read `wiki/SCHEMA.md` §3.12 (age-guide contract — added by C-adj.1) + §4 enum glossary + §5 (citation policy) + §6 (cross-link invariants) + §8 (voice).**
>
> Read context pages:
> - `wiki/age-lens-14u.md` (parent context for 13s/14s/15s)
> - `wiki/age-lens-hs.md` (parent context for 16s/17s/18s)
> - `wiki/age-lens-college.md` (parent context for 18s)
> - `wiki/schools/munciana-volleyball-club.md` (the operating model)
> - `wiki/sources/munciana-2022-camp-drills.md` (Mike Lingenfelter's drill library + coaching philosophy)
> - 1-2 Track B research papers relevant to your age (especially injury / adolescent-development / motor-learning research from Sub-dispatch B.2/B.3/B.6)
>
> **Required body sections per SCHEMA §3.12:** Overview & development phase / Skill milestones (subsections per skill: passing, setting, hitting, blocking, serving, defense, transition) / Systems repertoire / Athletic profile / Mental & coachability markers / Promotion criteria / Common coaching corrections / Recommended drills / Recommended cues / Sources.
>
> **Frontmatter:**
> ```yaml
> ---
> type: age-guide
> age: <Xs>
> phase: <enum>
> sources: [<≥3 — typically the parent age-lens + 1+ Track B research + 1+ AOC age-specific or Munciana piece>]
> ---
> ```
>
> **Heavy citation per SCHEMA §5.** Inline `[citation-key]` after each non-generic claim. Use [unsourced]+queue per SCHEMA §5 for claims you can't ground.
>
> **The `## Promotion criteria` section is critical** — Sub-dispatch D.2 (tryout rubrics) reads this section to derive evaluation criteria. Make sure it's specific, observable, and graded.
>
> **Cross-link expectations:**
> - wikilink `[[<X-1>s]]` (previous age) and `[[<X+1>s]]` (next age) where they exist
> - wikilink `[[<age>-drills]]` (your drill-pick-list — written in parallel by D.1 drill-pick agent)
> - wikilink `[[tryout-rubric-<age>]]` (your tryout rubric — written by D.2)
> - wikilink `[[passing-cues]]`, `[[setting-cues]]` etc. for relevant cue-dictionary entries
> - 14s/16s/18s wikilink the existing age-lens pages
> - Munciana cross-links where the operating model directly applies
>
> **Recency preference:** Per `feedback_recency_preference.md`, lead with modern training/thinking/technique. Apply this in the cue choices and skill-milestone framing. The Munciana / Kiraly / aoc-2024-2026 corpus is the primary lean.
>
> **When done:** commit `feat(wiki): add <age> age-guide` --no-verify.

### Tasks D.1.2 – D.1.10: Individual age-guides

Each task follows the shared D.1.1 brief with these specifics:

**Task D.1.2: `wiki/age-guides/10s.md`** — age: 10s, phase: introduction. Heavy USAV growing-kids alignment; emphasis on Tier 1 fundamentals (basic platform, basic underhand serve, ready position). Systems: 6-on-6 cooperative play, no specialized positions. Cross-link `[[11s]]`.

**Task D.1.3: `wiki/age-guides/11s.md`** — age: 11s, phase: introduction (transitioning to fundamentals). Introduce overhand serve attempt. Systems: simple 4-2 entry. Cross-link `[[10s]]`, `[[12s]]`.

**Task D.1.4: `wiki/age-guides/12s.md`** — age: 12s, phase: fundamentals. Forearm pass platform stable; overhand pass introduced; standing-float serve target work begins; basic 4-2 reliable. Cross-link `[[11s]]`, `[[13s]]`.

**Task D.1.5: `wiki/age-guides/13s.md`** — age: 13s, phase: late-fundamentals. Position identity emerging (setter candidates, OH candidates, libero candidates). Systems: 4-2 reliable; simple 6-2 introduced. Standing topspin serve. Cross-link `[[12s]]`, `[[14s]]`. Wikilink `[[age-lens-14u]]` — first overlap with the existing club age-lens.

**Task D.1.6: `wiki/age-guides/14s.md`** — age: 14s, phase: late-fundamentals → specialization onset. Direct wikilink to `[[age-lens-14u]]` as the parent context (same age band). Match-spec milestones and Munciana-style operational depth here. Standing-topspin reliable; jump-float introduction; libero specialization onset; offense-4-2 default with offense-6-2 viable.

**Task D.1.7: `wiki/age-guides/15s.md`** — age: 15s, phase: specialization. Jump-float standard; complex 6-2 viable; basic 5-1 introduced; bunch-read blocking concept. Cross-link `[[14s]]`, `[[16s]]`, `[[age-lens-hs]]`.

**Task D.1.8: `wiki/age-guides/16s.md`** — age: 16s, phase: specialization. Direct wikilink to `[[age-lens-hs]]` as the parent context. Jump-topspin emerging; full 5-1 standard; swing-blocking footwork mature; OH backrow attack standard.

**Task D.1.9: `wiki/age-guides/17s.md`** — age: 17s, phase: advanced. Jump-topspin reliable; full systems mature; tactical depth (audibles, in-rotation OOS); college-bridge readiness markers begin appearing.

**Task D.1.10: `wiki/age-guides/18s.md`** — age: 18s, phase: college-bridge. Direct wikilink to `[[age-lens-college]]`. Full systems mature; recruiting-relevant skill calibration; college-readiness physical markers (vertical, approach jump touch, reach); mental-toughness work explicit.

Each task: 3-step execution (apply shared brief → run lint → commit).

---

### Task D.1.11: Cue-dictionary brief template (reference for Tasks D.1.12–D.1.18)

**Shared brief:**

> You are writing one of the 7 cue-dictionary pages. **Read `wiki/SCHEMA.md` §3.13 (cue-dictionary contract) + §4 + §5 + §6 + §8.**
>
> Read context:
> - `wiki/<skill>.md` skill hub (e.g., `wiki/passing.md`)
> - All technique pages for this skill (e.g., for passing: `passing-forearm.md`, `passing-overhead.md`, `passing-serve-receive.md`, `passing-free-ball.md`)
> - `wiki/sources/munciana-2022-camp-drills.md` for Munciana cue language
> - 2-3 AOC source pages for canonical AOC cues
>
> **Required body sections per SCHEMA §3.13:** Overview / Per-subskill canonical cues / Anti-cues / Voice consistency notes / Sources.
>
> **Frontmatter:**
> ```yaml
> ---
> type: cue-dictionary
> skill: <skill>
> age-bands: [10s, 11s, 12s, 13s, 14s, 15s, 16s, 17s, 18s]
> sources: [<≥3>]
> ---
> ```
>
> **For each subskill:** list 1–3 canonical cues. For each cue: (a) the exact words a coach says (in quotes), (b) age-band introduced, (c) age-band refined or replaced, (d) cue rationale (what it teaches, why this phrasing, what it does NOT teach).
>
> **Anti-cues:** phrases that sound right but mislead. Example: "snap your wrist" is an anti-cue for hitting (over-emphasizes wrist; modern teaching uses arm-and-hand dynamic).
>
> **Voice-consistency notes:** when AOC, GMS, ecological-dynamics, Japanese, Munciana cues genuinely differ, explain how the club resolves. Lean per `feedback_recency_preference.md`: modern AOC + Munciana primary; GMS for motor-learning rationale; Japanese for defense identity.
>
> Heavy citation. When done: commit `feat(wiki): add <skill>-cues dictionary` --no-verify.

### Tasks D.1.12 – D.1.18: Individual cue dictionaries

**Task D.1.12: `wiki/cues/passing-cues.md`** — skill: passing. Anchor cues: Kiraly's 4 keys (stopped & balanced / thumbs together / set the angle / simple one-way motion); Bechard's posture-pursuit-platform; Stone's late-platform-formation; Lingenfelter's quiet-platform / pass-and-cover micro-skills; aim-the-platform-with-shoulders.

**Task D.1.13: `wiki/cues/setting-cues.md`** — skill: setting. Anchor cues: hand-hinge (modern AOC); Rockwell setter-feedback prompts; Lingenfelter plant-timing tempo (Tempo 1/2/3 by left-foot plant); side-of-ball contact; vision-on-target.

**Task D.1.14: `wiki/cues/hitting-cues.md`** — skill: hitting. Anchor cues: Schmidt "start slow, accelerate the last two steps"; Mattox Sight-90 / Elbow-Lead / Lift-and-Whip; MacDonald torque + high-hand; "open shoulders to seam"; "close the heel" (approach).

**Task D.1.15: `wiki/cues/blocking-cues.md`** — skill: blocking. Anchor cues: outside-foot-high (Munciana — "this doesn't happen by accident, it has to be taught"); read-then-jump; swing-block footwork progressions (Rosen 10-foot-line); Slabe's hand-press; penetrate-not-cover.

**Task D.1.16: `wiki/cues/serving-cues.md`** — skill: serving. Anchor cues: aim-small-miss-small (Munciana); Mattox Lift/Step/Swing; Dunning toss-first ("tossing is the worst skill in volleyball"); aggressive-mentality framing (Munciana five-before-ten); contact-out-front.

**Task D.1.17: `wiki/cues/defense-cues.md`** — skill: defense. Anchor cues: Three P's (get-back, get-low, get-touch — Munciana); Stone hips-under-ball; Look/See/Decide (Josephson); read the hitter, not the ball; arrive-stopped-then-platform.

**Task D.1.18: `wiki/cues/transition-cues.md`** — skill: transition. Anchor cues: block-to-approach recovery footwork; dig-to-approach; OOS detect/call/bail-to-pin; setter-second-ball protocol; libero-second-ball overhead set from behind 3m.

Each: 3-step execution (apply shared brief → lint → commit).

---

### Task D.1.19: Cue-dictionary hub `wiki/cues.md`

**Files:** Create `wiki/cues.md`.

- [ ] **Step 1: Apply the standard hub-page contract per SCHEMA §3.1.**

Frontmatter:
```yaml
---
type: hub
area: coaching-cues
subtopics: [passing-cues, setting-cues, hitting-cues, blocking-cues, serving-cues, defense-cues, transition-cues]
---
```

Required sections: Overview / Major subtopics (links to all 7 cue pages with one-line summaries) / Schools of thought (the recency-preference rationale + AOC/GMS/Japanese/Munciana lean) / Getting started / Related areas / Sources.

Target: 600-800 words.

- [ ] **Step 2:** Lint, commit `feat(wiki): add cues hub page` --no-verify.

---

### Task D.1.20: Drill-pick-list brief template (reference for Tasks D.1.21–D.1.29)

**Shared brief:**

> You are writing one of the 9 drill-pick-list pages. **Read `wiki/SCHEMA.md` §3.14 + §4 + §5 + §6 + §8.**
>
> Read context:
> - `wiki/age-guides/<age>.md` (parent age-guide, written in parallel by D.1.2-D.1.10)
> - `wiki/index.md` Drills section (the 101-drill master library)
> - `wiki/sources/munciana-2022-camp-drills.md` (Munciana drill philosophy)
> - The relevant existing age-lens (`age-lens-14u.md` for 13s/14s/15s; `age-lens-hs.md` for 16s/17s/18s)
>
> **Required body sections per SCHEMA §3.14:** Purpose / Must-do drill list (10-15 drills as wikilinks, grouped by skill, with 1-line rationale per drill) / When-in-season-to-use mapping / Adaptations / Sources.
>
> **Frontmatter:**
> ```yaml
> ---
> type: drill-pick-list
> age: <Xs>
> season-context: composite
> drills: [<≥10 real drill slugs verified to exist under wiki/drills/>]
> sources: [<≥1 — typically munciana-2022-camp-drills + the parent age-lens>]
> ---
> ```
>
> **Drill verification:** before listing a drill in `drills:` frontmatter or as a `[[wikilink]]` in body, run `ls wiki/drills/ | grep <slug>` to confirm it exists.
>
> **Down-scaling caveat for 10s/11s/12s:** the master drill library is mostly `levels: [14u]` tagged. For younger ages, prefer warm-up + ball-control + cooperative-game drills + introduction-level skill drills. Avoid penalty-heavy wash drills for 10s/11s/12s; introduce competitive-grading at 13s; jump-training-heavy drills appear from 15s; full game-like 6v6 work at 16s+.
>
> **Munciana drills (46 of them, prefix `munciana-`)** are heavily age-band-versatile. Use them as backbone where appropriate.
>
> **When done:** commit `feat(wiki): add <age> drill pick-list` --no-verify.

### Tasks D.1.21 – D.1.29: Individual drill pick-lists

**Task D.1.21: `wiki/drill-picks/10s-drills.md`** — Bias toward warm-up + cooperative ball-control. Suggested drills (verify): dynamic-warmup-volleyball, ball-control-warmup, partner-pepper-warmup, cooperative-25-goal, target-setting (catch-and-set version), serve-targets (underhand-only), butterfly-passing (modified — short distance, tosses only), munciana-two-man-shuffle (footwork). 10 drills total.

**Task D.1.22: `wiki/drill-picks/11s-drills.md`** — 10s baseline + introduce overhand serve drills + simple shuttle-passing (2-line). ~12 drills.

**Task D.1.23: `wiki/drill-picks/12s-drills.md`** — Add competitive grading; introduce wash-drill at low intensity; munciana-tilt-chain & rush-and-push variants. ~13 drills.

**Task D.1.24: `wiki/drill-picks/13s-drills.md`** — Add transition-rally + free-ball-to-offense; setter-specific drills (target-setting, three-setter-rotation introduction). ~14 drills.

**Task D.1.25: `wiki/drill-picks/14s-drills.md`** — Mid-list. Direct overlap with `age-lens-14u` recommended drills. Munciana camp drills heavily represented. ~15 drills.

**Task D.1.26: `wiki/drill-picks/15s-drills.md`** — Introduce jump-warmup; jump-setting-progression; transition-hitting; six-player-defense; reactive-jumping (with CSCS disclaimer). ~14 drills.

**Task D.1.27: `wiki/drill-picks/16s-drills.md`** — Direct overlap with age-lens-hs. Pressure-serving + jump-serve-progression + line-vs-angle-shot. Full game-like 6v6 (gold-medal-scrimmage). ~15 drills.

**Task D.1.28: `wiki/drill-picks/17s-drills.md`** — Advanced; king-of-the-court; tactical out-of-system-to-attack; conditioning-court-sprints. ~14 drills.

**Task D.1.29: `wiki/drill-picks/18s-drills.md`** — College-bridge; arm-care-routine; hitting-vs-block; jump-serve-progression at high intensity; recruiting-relevant skill drills. ~15 drills.

Each: 3-step execution (apply shared brief → lint → commit).

---

### Task D.1.30: Sub-dispatch D.1 lint checkpoint

- [ ] **Step 1: Run lint**

```
python tools/lint.py 2>&1 | tail -3
```

Expected: 0 invariant violations; broken-wikilink count ≤15 (some forward refs to D.2 tryout rubrics expected).

- [ ] **Step 2: Append D.1 log entry to `wiki/log.md`**

```markdown
## [2026-04-25] dispatch-D1-complete | Manual foundation landed
Parallel dispatch of ~26 agents produced:
- 9 age-guide pages (10s through 18s, ~2500-3000w each)
- 7 cue-dictionary pages (passing/setting/hitting/blocking/serving/defense/transition)
- 1 cue-dictionary hub
- 9 drill-pick-list pages (10s through 18s)
SCHEMA §3.12-§3.14 + lint.py extensions landed via C-adj.1 (combined SCHEMA agent).
Net: 26 new content pages.
Next: Sub-dispatch D.2 (tryout rubrics consuming D.1 promotion criteria).
```

- [ ] **Step 3: Commit:**

```
git add wiki/log.md && git commit -m "docs(wiki): D.1 log entry" --no-verify
```

---

## Sub-dispatch D.2 — Tryout rubrics

Launches after D.1 lands (or after C-adj completes its SCHEMA + ops-doc work, whichever is later — both required). 11 parallel agents.

---

### Task D.2.1: Tryout-rubric brief template (reference for Tasks D.2.2–D.2.11)

**Shared brief:**

> You are writing one of the 10 tryout-rubric ops-doc pages. **Read `wiki/SCHEMA.md` §3.11 (ops-doc contract — added by C-adj.1) + §4.**
>
> Read context:
> - `wiki/age-guides/<age>.md` for your age (written by D.1.2-D.1.10) — specifically the `## Promotion criteria` section. **Your rubric's evaluation criteria translate those promotion criteria into a 1-5 scoring scale.** This is the unifying-principle for the Manual: the milestones a player needs to graduate from age X are the criteria a tryout for age X+1 evaluates against.
> - `wiki/recruiting.md` for HS/college rubrics (recruiting-context calibration)
>
> **Frontmatter:**
> ```yaml
> ---
> type: ops-doc
> kind: tryout-rubric
> audience: coach
> level: <14u | hs | college>   # use 14u for 10s-13s/14s; hs for 15s-17s; college for 18s/college-walkon
> sources: [<≥1>]
> ---
> ```
>
> **Required body sections (tryout-rubric variant per SCHEMA §3.11):** Purpose / Evaluation criteria (literal markdown table — criteria across rows × scoring 1-5 across columns) / Scoring / Calibration notes / Sources.
>
> **The Evaluation criteria table is the rubric.** Rows: passing, setting, hitting, blocking, serving, defense, transition, mental/coachability. Columns: 1 (does not demonstrate), 2 (occasional), 3 (consistent at age-appropriate level), 4 (above age-appropriate), 5 (next-age-ready). Each cell describes specifically what's observable at that score level for that skill.
>
> **Calibration notes:** describe how to apply the rubric across a 60-90-minute tryout session; how multiple evaluators reach inter-rater agreement; common biases to avoid.
>
> Cross-link the corresponding age-guide and the relevant age-lens page.
>
> **When done:** commit `feat(wiki): add <age> tryout rubric` --no-verify.

### Tasks D.2.2 – D.2.11: Individual tryout rubrics

**Task D.2.2: `wiki/ops/tryout-rubric-10s.md`** — level: 14u, age: 10s context. Calibration: USAV growing-kids alignment; equal-playing-time spirit honored.

**Task D.2.3: `wiki/ops/tryout-rubric-11s.md`** — level: 14u, age: 11s.

**Task D.2.4: `wiki/ops/tryout-rubric-12s.md`** — level: 14u, age: 12s.

**Task D.2.5: `wiki/ops/tryout-rubric-13s.md`** — level: 14u, age: 13s.

**Task D.2.6: `wiki/ops/tryout-rubric-14u.md`** — level: 14u, age: 14s. Direct overlap with `age-lens-14u`.

**Task D.2.7: `wiki/ops/tryout-rubric-15s.md`** — level: hs, age: 15s.

**Task D.2.8: `wiki/ops/tryout-rubric-16u.md`** — level: hs, age: 16s.

**Task D.2.9: `wiki/ops/tryout-rubric-17s.md`** — level: hs, age: 17s.

**Task D.2.10: `wiki/ops/tryout-rubric-18u.md`** — level: hs, age: 18s. Cross-link `recruiting.md`.

**Task D.2.11: `wiki/ops/tryout-rubric-college-walkon.md`** — level: college. Cross-link `[[age-lens-college]]`, `[[recruiting]]`. Calibration: D1 vs D2/D3 vs JUCO; physical-baseline thresholds; mental-toughness assessment.

Each: 3-step execution.

---

### Task D.2.12: Final cross-link + index update + log + acceptance

**Files:** Modify `wiki/index.md`, `wiki/log.md`.

- [ ] **Step 1: Add Manual sections to `wiki/index.md`**

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
```

In Operations section, add Tryout rubrics if not already present:

```markdown
### Tryout rubrics (per age, all 9 ages + college walk-on)
- [[tryout-rubric-10s]], [[tryout-rubric-11s]], [[tryout-rubric-12s]], [[tryout-rubric-13s]], [[tryout-rubric-14u]], [[tryout-rubric-15s]], [[tryout-rubric-16u]], [[tryout-rubric-17s]], [[tryout-rubric-18u]], [[tryout-rubric-college-walkon]]
```

- [ ] **Step 2: Append final log entries**

```markdown
## [2026-04-25] dispatch-D2-complete | Manual tryout rubrics landed
Parallel dispatch of ~10 agents produced:
- 10 tryout-rubric ops-doc pages (9 ages + college walk-on)
- Each rubric's evaluation criteria align with the corresponding age-guide's promotion criteria
- ops-doc kind=tryout-rubric format unified across all 10

## [2026-04-25] manual-complete | Club Coaching Standards Manual v1 shipped
Net Manual deliverable:
- 9 age-guides + 7 cue dictionaries + 1 cue hub + 9 drill pick-lists + 10 tryout rubrics = 36 pages
- 5 new SCHEMA page-type definitions (ops-doc, age-guide, cue-dictionary, drill-pick-list, plus practice-plan scope extension)
- tools/lint.py + test_lint.py extended with 5 new validations / 5 new tests

Manual answers four questions per age:
1. What skills should a player at this age master?
2. What cues do all our coaches use to teach those skills?
3. Which drills do we use to train them?
4. How do we evaluate them at tryouts?

Manual v2 backlog (deferred): club philosophy/values doc; parent comms; coach onboarding; athlete self-development guides; mentorship structure.
```

- [ ] **Step 3: Run final lint**

```
python tools/lint.py
cp wiki/lint-report.md wiki/lint-report.md.baseline
```

Expected: broken wikilinks ≤10, invariants 0.

- [ ] **Step 4: Walk acceptance checklist from spec §7.1**

Verify each item. Fix any that don't hold.

- [ ] **Step 5: Final commit**

```
git add wiki/index.md wiki/log.md wiki/lint-report.md wiki/lint-report.md.baseline
git commit -m "docs(wiki): Manual v1 complete — 36-page club coaching standards manual" --no-verify
```

- [ ] **Step 6: Update memory**

Update `C:\Users\SongMu\.claude\projects\C--Users-SongMu-documents-claudecode-vba-bible\memory\project_bible_status.md` to reflect post-Manual state.

- [ ] **Step 7: Report final state to user**

Summary: total pages, scenario-test verification, deferred items (Manual v2 candidates).

---

## Self-review notes

**Spec coverage:**
- Spec §3.1 age-guide → Tasks D.1.2-D.1.10 ✓
- Spec §3.2 cue-dictionary → Tasks D.1.12-D.1.18 ✓
- Spec §3.3 cue hub → Task D.1.19 ✓
- Spec §3.4 drill-pick-list → Tasks D.1.21-D.1.29 ✓
- Spec §3.5 tryout-rubric extension → Tasks D.2.2-D.2.11 ✓
- Spec §4 SCHEMA additions → Task C-adj.1 (combined) ✓
- Spec §5.5 index updates → Task D.2.12 ✓
- Spec §6 execution strategy → C-adj sub-dispatch + D.1 + D.2 ✓
- Spec §7 success criteria → D.2.12 walkthrough ✓

**No placeholders:** all tasks have exact files, agent briefs reference real source material, exact commit messages.

**Type consistency:** `age-guide`, `cue-dictionary`, `drill-pick-list`, `ops-doc` consistent across SCHEMA additions, lint.py REQUIRED_FIELDS, agent briefs.

**Scope:** Manual v1 (load-bearing core) is one cohesive subsystem. Manual v2 explicitly deferred per spec §2.2.
