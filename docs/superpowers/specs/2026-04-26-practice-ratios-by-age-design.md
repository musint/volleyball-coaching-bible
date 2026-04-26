# Practice Ratios by Age & Season Phase — Design Spec

**Date:** 2026-04-26
**Owner:** Song Mu (song.mu@discordapp.com)
**Predecessor specs:**
- `docs/superpowers/specs/2026-04-22-volleyball-coaching-bible-design.md` (bootstrap)
- `docs/superpowers/specs/2026-04-25-club-coaching-manual-design.md` (Module 1 age-guides established)

---

## 1. Context

### 1.1 Why this work

Song asked for guidance, per age group, on how much **blocked training vs. live game play** should be recommended — *especially as the season progresses*. Two-dimensional gap: age × season-phase → blocked-vs-live ratio.

The wiki has the methodology layer (`wiki/schools/block-vs-random-practice.md` covers the contextual-interference effect, ecological-dynamics critique, and per-school positions). It has the per-age developmental layer (9 age-guides + 3 age-lens pages). It has the season-arc layer (5 macrocycle pages + 5 microcycle pages). What it does *not* have is the synthesis: a coach landing on `14s.md` cannot read off "in late-season, what should my blocked / small-group / 6v6 ratio be?" The information is scattered across the methodology page, the per-age guide, and the macrocycle template.

The deliverable closes that gap with a synthesis page (the master matrix + per-age narratives + phase-transition criteria) and self-sufficient sections on every age-guide and age-lens that link back.

### 1.2 Stance

The matrix cells are **coach-judgment synthesis grounded in the existing wiki's evidence base** — USAV age-appropriate guidelines, the CI literature (Shea & Morgan 1979 forward), GMS's "as quickly as the learner allows" framing, and the existing 14U lens's static recommendation. They are *defensible defaults*, not RCT-derived constants. The page text states this honestly upfront.

Bucket structure is **three buckets**, not the user's original binary "blocked vs. live": (1) blocked / skill-isolation, (2) small-group game-like / competitive, (3) 6v6 live full-format. The methodologically interesting middle bucket is where the contextual-interference benefit lives at highest density per minute.

Season phases are **five**: preseason / mid-season / late-season / pre-tournament-peak / taper-match-day. The non-monotonic taper (blocked bumps back up, live drops) is intentional and reflects what NCAA-program tapers actually do.

### 1.3 Approach

**Hybrid (Approach C from the brainstorm).** One synthesis page (`wiki/practice-ratios.md`) holds the master matrix and the canonical narrative. Each age-guide and age-lens carries a self-sufficient section that links back. Per-page sections are complementary in framing rather than identical in text — different angle on the same row, plus drill anchors, plus link out — to comply with SCHEMA §9 anti-pattern (no content duplication).

---

## 2. Scope

### 2.1 Deliverables

| Item | Count | Notes |
|---|---:|---|
| New synthesis page (`wiki/practice-ratios.md`) | 1 | Hub page-type per SCHEMA §3.1; ~3500-4500 words |
| Age-guide section additions | 9 | One per age 10s through 18s |
| Age-lens section replacements/additions | 3 | 14U / HS / college |
| `practice-planning.md` hub line update | 1 | Existing "Practice ratios" subtopic line |
| `wiki/index.md` entry | 1 | Under Hub pages |
| `wiki/log.md` append | 1 | Per SCHEMA §8.1 ingest workflow conventions |
| **Total** | **16** | 1 new file + 15 edits |

### 2.2 Non-goals

- New source pages (all ~22 cited sources already exist as `wiki/sources/<slug>.md`; verified no new source-page creation required).
- Macrocycle / microcycle / practice-plan page rewrites (existing pages already encode their own phase-specific ratios; this spec creates the cross-cutting reference, not a rewrite of every plan).
- Methodology re-argument (`wiki/schools/block-vs-random-practice.md` already carries the evidence-base argument; this spec applies it operationally).
- Bucket-4 carve-out (warm-up + cool-down sit *outside* the three-bucket percentages by design; included as page text, not a column).
- Postseason / off-season column (deferred — pattern at that phase is individual development, not team-wide ratio shifting; can be a Manual v2 addition).
- Position-specific matrices (a setter's blocked time is structurally different from a libero's, but team-level ratios are the right unit for practice planning).

---

## 3. Page contract — `wiki/practice-ratios.md`

### 3.1 Page type and frontmatter

**Page type:** `hub` per SCHEMA §3.1.

```yaml
---
type: hub
area: practice-planning
subtopics:
  - bucket-definitions
  - season-progression
  - age-progression
  - transition-criteria
  - methodology-evidence-base
---
```

### 3.2 Body sections

1. `## Overview` (~250 words) — what the page is, the 3-bucket frame, the 5-phase frame, the synthesis-not-RCT-constants disclosure.
2. `## Bucket definitions` (~600 words) — operational definitions of blocked / small-group / 6v6 with example drills and edge-call rules.
3. `## Master matrix` (~150 words intro + the 10×5 table).
4. `## Per-age trajectories` (~1700-2000 words; ten 150-200-word paragraphs).
5. `## Phase-transition criteria` (~600 words; five transitions including cyclical-club structure).
6. `## Schools of thought` (~500 words; six school positions).
7. `## Getting started` (~150 words; read order).
8. `## Related areas` (~80 words; wikilinks).
9. `## Sources` (~22 source-page wikilinks).

**Total target:** ~3500-4500 words.

### 3.3 Bucket definitions

**Bucket 1 — Blocked / skill-isolation work.**
Same-skill repetition with controlled feed (coach-toss, partner-toss, tee, line). Limited or no opposing intent. The athlete knows what's coming.
- Drill examples: `[[butterfly-passing]]` (coach-fed), `[[serve-targets]]`, `[[target-setting]]`, `[[block-footwork-ladder]]`, `[[two-line-passing]]`, `[[approach-and-swing]]` against coach-toss, `[[front-back-sets]]`, individual position work.
- Maps to SCHEMA `phase: skill` enum.
- Purpose: pattern installation, technique repair, low-cognitive-load cue reinforcement.
- Methodology profile: high in-session fluency, low retention/transfer if held too long.

**Bucket 2 — Small-group game-like / competitive.**
Sub-6v6 formats with opposing intent and scoring: 1v1, 2v2, 3v3, 4v4 over-the-net; queen-of-the-court variants; wash-drill formats with scoring; mini-game scrimmage.
- Drill examples: `[[serve-receive-3v3]]`, `[[queen-of-the-court]]`, `[[queen-of-the-court-passing]]`, `[[wash-drill]]` at small scale, `[[munciana-biggie-smalls]]`, `[[munciana-prove-it]]`, `[[cooperative-25-goal]]`.
- Maps to SCHEMA `phase: strategic` or `phase: competition` at smaller scale.
- Purpose: highest-density contextual-interference benefit per minute — the methodologically richest bucket.

**Bucket 3 — Live / full-format match play.**
Twelve-player game-like situations: 6v6 wash-style scoring drills, side-out drills, free-ball-to-offense at 6v6, half-game and full-game scrimmage, simulated matches.
- For 12s+: 6v6 (the actual match format).
- For 10s/11s: 4v4 (the USAV modified match format for those ages).
- For younger / different-format play: the bucket means "the actual match format being played."
- Drill examples: `[[gold-medal-scrimmage]]`, `[[six-player-defense]]`, `[[transition-rally]]`, `[[wash-drill]]` at 6v6 scale, simulated bracket matches.
- Maps to SCHEMA `phase: competition` at full scale.
- Purpose: full information-coupling, system execution under rotation-tracking load, decision-making at match-realistic complexity.

**Outside the three buckets:** warm-up + cool-down + non-decision conditioning. Treated as off-clock when computing percentages. A 120-min session with 15-min warm-up + 5-min cool-down = 100 min of in-bucket time. Mirrors how coaches actually plan and avoids percentages drifting from warm-up length variation.

**Edge calls (named explicitly in the page):**
- *Pepper.* Live-feed but two-player and uncompetitive without scoring → bucket 1 (warm-up sub-category) by default; bucket 2 if scored as `[[partner-pepper-warmup]]` competition.
- *Wash drills.* Bucket 2 if 2v2/3v3, bucket 3 if 6v6 — same drill family lands in different buckets based on player count.
- *Position-specific individual work* (setter footwork, libero reads, hitter arm mechanics). Always bucket 1.
- *Coach-fed but live-decision drills.* Bucket 1 if the read is trivial; bucket 2 if the read is a real perceptual problem and the drill is scored. Errs toward bucket 1 since information-coupling is degraded vs. live.

### 3.4 Master matrix

Format per cell: **blocked / small-group / live-full-format** as percentages summing to 100, applied to in-bucket time (warm-up/cool-down excluded).

| Age | Preseason | Mid-season | Late-season | Pre-tournament-peak | Taper / match-day |
|---|---|---|---|---|---|
| **10s** (4v4) | 40 / 55 / 5 | 30 / 55 / 15 | 25 / 55 / 20 | 25 / 50 / 25 | 35 / 50 / 15 |
| **11s** (4v4) | 40 / 55 / 5 | 30 / 55 / 15 | 30 / 50 / 20 | 25 / 45 / 30 | 35 / 50 / 15 |
| **12s** (6v6) | 45 / 40 / 15 | 35 / 40 / 25 | 30 / 40 / 30 | 25 / 35 / 40 | 35 / 35 / 30 |
| **13s** | 40 / 40 / 20 | 30 / 40 / 30 | 30 / 35 / 35 | 25 / 30 / 45 | 35 / 30 / 35 |
| **14s** | 40 / 35 / 25 | 30 / 35 / 35 | 25 / 35 / 40 | 20 / 30 / 50 | 30 / 30 / 40 |
| **15s** | 30 / 35 / 35 | 25 / 30 / 45 | 20 / 30 / 50 | 15 / 25 / 60 | 25 / 25 / 50 |
| **16s** | 30 / 30 / 40 | 20 / 30 / 50 | 15 / 30 / 55 | 10 / 25 / 65 | 20 / 25 / 55 |
| **17s** | 25 / 30 / 45 | 20 / 25 / 55 | 15 / 25 / 60 | 10 / 20 / 70 | 20 / 20 / 60 |
| **18s** | 25 / 25 / 50 | 20 / 25 / 55 | 15 / 25 / 60 | 10 / 20 / 70 | 20 / 20 / 60 |
| **College** | 25 / 25 / 50 | 20 / 25 / 55 | 15 / 20 / 65 | 10 / 15 / 75 | 15 / 15 / 70 |

**Pattern claims the page text will name:**

1. **Blocked drops as athletes age** — preseason blocked falls from ~40-45% at 10s-12s to ~25% at college. Drops because patterns stabilize and blocked work shifts from "install the platform" to "fix the specific drift."
2. **12s is the pattern-install-heaviest year** — 6v6 introduction adds team-system install (rotations, position assignments, three-attacker coverage) on top of skill install. Preseason peaks at 45 blocked.
3. **Small-group plateaus high at younger ages, ramps down at older.** 10s/11s sit at 50-55% small-group across the season; college drops to 15-25% as 6v6 takes over.
4. **Live-full-format ramps both across ages and across the season.** College pre-tournament-peak hits 75% live — the highest concentration in the matrix and what NCAA programs actually run in conference week.
5. **Taper is non-monotonic.** Blocked bumps back up by ~10pp from pre-tournament-peak to taper, live drops by ~10-15pp. Mechanism: blocked polish-rep work (serve targets, pass-set-hit at chosen tempos) gets contact freshness without the fatigue cost of full live competition.

**Methodological justification of the 11-14s bump (Section 3.5):** the matrix's blocked percentages at 11s-14s are 5pp higher than a "pure-random methodology" reading would prescribe. Three reasons in the page text:
- CI literature's most-misquoted caveat (Magill & Hall 1990): CI benefits *require a stable movement solution to interleave*; learners in the cognitive stage need blocked work first.
- GMS's actual position read carefully: "as quickly as the learner allows" — for an 11s learning the platform, that's meaningfully slower than for a 17s.
- Practice-budget arithmetic: a 90-min 12s session can't realistically install platform + hand-hinge + approach + float-serve mechanics across a roster AND have 30 min of 6v6 — install density per skill drops below pattern-stability threshold.

The 5pp comes from bucket 3, not bucket 2: bucket 3 at younger ages has high error rate, more standing around, more rotation chaos, and lower meaningful-touch density per minute than bucket 2.

### 3.5 Per-age trajectory paragraph template

Each of the 10 paragraphs follows:
1. One sentence naming the row's defining shape.
2. Two-to-three sentences walking the trajectory across the five phases, citing the percentages.
3. One sentence on the age-specific quirk driving the shape.
4. Drill-format anchors per phase as wikilinks.

**Length target:** 150-200 words per paragraph.

**Driving-quirk callouts per row:**
- 10s — USAV-modified format (4v4); cooperative-game / movement-discovery default
- 11s — 4v4 still; pattern install dominates skill development
- 12s — 6v6 introduction year; pattern-install-heaviest year of the program
- 13s — 6v6 systems stabilizing; skills consolidating
- 14s — fundamentals consolidation; growth-spurt reality on a moving target
- 15s — specialization onset rewrites blocked time
- 16s — position commitment, jump-topspin install, swing-blocking transition
- 17s — recruiting cycle, pre-college readiness, advanced systems
- 18s — college bridge, full elite system execution
- College — NCAA hours-rules cap, conference-week / NCAA-bracket peak; concurrent S&C considerations

**Sample paragraphs (14s, 10s, college) included as Appendix A** of this spec for the writing phase to anchor against.

### 3.6 Phase-transition criteria

For each transition the page lists *signs the team is ready to graduate to the next phase's ratios*, not a fixed timeline.

- **Preseason → mid-season:** patterns stable enough to interleave. Markers: athletes execute proper mechanics in blocked work without prompting; team executes base offense without rotation reminders; first competition has happened; pass quality 2+ on ~60% of serves received. Time-based fallback: 3-4 weeks HS, 2-4 weeks club, ~2 weeks college.
- **Mid-season → late-season:** team-wide install demand gone, only specific repair remains. Markers: blocked-time content shifts from "install" to "fix athletes A/B/C"; tournament density accumulated; cumulative-fatigue markers appear (Hooper-Index drift up, weekly-CMJ drift down) [[rebelo-2024-training-stress-fatigue-wellbeing]] [[sanders-2025-early-season-jump-load-d1-volleyball]].
- **Late-season → pre-tournament-peak:** event-driven, 7-14 days before targeted event; roster locked; opponent intel arrived.
- **Pre-tournament-peak → taper-match-day:** 24-72 hours before; volume reduction priority; ratio bumps blocked back up.
- **Cyclical structure for club volleyball:** the matrix is not run linearly once per year for 14U/club. Cycle is preseason → mid-season → late-season → repeated mini-peak / mini-taper every 2-3 weeks → final-tournament peak. HS = one big linear arc with one peak. College = two peaks (conference + NCAA).

### 3.7 Schools of thought

Six positions, one short paragraph each:
- `[[gold-medal-squared]]` — random-leaning, "as quickly as the learner allows"
- `[[art-of-coaching-volleyball]]` — eclectic; Mattox argues heavy fundamentals, Rose argues competitive intent in every bucket
- `[[usa-volleyball]]` — "grills not drills" tilts toward bucket 2 at younger ages
- `[[ecological-dynamics]]` — bucket dichotomy is under-specified; what matters is information-coupling fidelity
- `[[japanese-training]]` — historically high blocked volume; modern Japan modernizing toward bucket 2/3
- `[[game-based-training]]` — TGfU inversion: tactical context first, blocked work as need reveals it

### 3.8 Citation strategy

Hub default per SCHEMA §5 is *light*. This hub carries methodology-grade synthesis, so practice is **medium-heavy**:

- Inline `[citation-key]` on key methodology claims, USAV philosophy quotes, evidence-cited age-specific markers.
- *No inline citations on matrix cells* — they are coach-judgment synthesis, not source-derivable claims. Page text states this honestly upfront.
- Per-age trajectory paragraphs cite where claims are sourced.
- `## Sources` at bottom lists all referenced source pages as wikilinks.

---

## 4. Per-page integration contracts

### 4.1 Age-guide sections (`wiki/age-guides/<age>.md`, 9 files)

**Location:** new section between existing `## Recommended drills` and `## Recommended cues` sections.

**Section heading:** `## Practice ratio across the season`

**Length target:** 120-150 words per section.

**Template (filled with 14s example):**

```markdown
## Practice ratio across the season

The blocked / small-group / 6v6 mix for 14s runs **40/35/25 → 30/35/35 → 25/35/40
→ 20/30/50 → 30/30/40** across preseason, mid-season, late-season, pre-tournament-peak,
and taper respectively. The 14s-specific shape: heavy pattern install through the
platform and hand-hinge install window; the small-group bucket holds steady at
30-35% year-round as the methodologically-richest practice density [shea-1979-contextual-interference];
bucket 1 dips to 20% at peak and bumps back to 30% at taper for polish-rep contact
freshness without fatigue. Drill-format anchors: `[[butterfly-passing]]`,
`[[pass-set-hit]]`, `[[serve-targets]]` (blocked); `[[queen-of-the-court]]`,
`[[wash-drill]]`, `[[cooperative-25-goal]]` (small-group); `[[gold-medal-scrimmage]]`,
`[[transition-rally]]` (6v6). See `[[practice-ratios]]` for the full age × season
matrix, bucket definitions, methodology basis, and adjacent-age-band trajectories.
```

**Citation requirement:** at least 1 inline citation per section (heavy-citation contract for age-guide pages per SCHEMA §5). Default citation: `[shea-1979-contextual-interference]` for the small-group / CI claim, plus one age-appropriate methodology citation.

**Per-age customization required:**
- The percentage chain reflects that age's row in the matrix.
- The "shape" sentence reflects that age's driving quirk (per §3.5).
- Drill anchors are pulled from drills appropriate to that age (cross-reference `wiki/drill-picks/<age>-drills.md` for the age's existing drill pick-list).

### 4.2 Age-lens sections

**`wiki/age-lens-14u.md`** — replace the existing line at line 80:
> A reasonable shape: 30–40% ball-control, 20–30% small-group competitive (1v1, 2v2, 3v3), 20–30% 6v6 scrimmage, 10% warm-up/cool-down.

with:

```markdown
**Drill-mix ratio.** The blocked / small-group / 6v6 mix runs **40/35/25 → 30/35/35
→ 25/35/40 → 20/30/50 → 30/30/40** across preseason / mid-season / late-season /
pre-tournament-peak / taper at 14U. Heavy install transitions to 6v6-dominant by peak;
small-group — `[[wash-drill]]`, `[[queen-of-the-court]]`, `[[cooperative-25-goal]]` —
holds at ~35% through the year as the highest-density CI window
[shea-1979-contextual-interference][gms-nd-structure-practice]. Warm-up + cool-down
sits outside these percentages, typically 10-15 min off the top of a 90-min session.
See `[[practice-ratios]]` for the full matrix, bucket definitions, and phase-transition
criteria. Note: 14U families running primarily-13s rosters should reference 13s row
directly (lower 6v6 percentages, similar small-group).
```

**`wiki/age-lens-hs.md`** — add or replace equivalent under "Practice design adaptations": use the **16s row as the default** (most representative of HS varsity rosters) with explicit notes that freshman programs lean toward the 15s row's slightly more blocked-heavy mix, and senior-heavy programs (year 4 athletes preparing for college) lean toward the 17s row.

**`wiki/age-lens-college.md`** — add or replace equivalent: the college row directly with NCAA hours-rules callout — rotation moves, not bucket allocation.

**Length target:** 80-110 words per replacement.

### 4.3 `practice-planning.md` hub line update

**Before:**
> **Practice ratios** — the mix of blocked vs. random, technical vs. tactical, individual vs. team. The modern default skews heavily random-and-tactical once fundamentals are stable. See [[block-vs-random-practice]].

**After:**
> **Practice ratios** — the mix of blocked / small-group game-like / 6v6 live across age and season phase. See `[[practice-ratios]]` for the full age × season matrix, and `[[block-vs-random-practice]]` for the methodology basis underneath the matrix.

### 4.4 `wiki/index.md` entry

**Add under "Hub pages":**
> - `[[practice-ratios]]` (W-R) — age × season-phase matrix of blocked / small-group / 6v6 percentages with per-age trajectories and phase-transition criteria

(Wave label `W-R` is suggestive; can be assigned to whatever wave naming the index uses at commit time, or left bare like other recently-added pages.)

### 4.5 `wiki/log.md` entry

**Append:**
```markdown
## [2026-04-26] new-page | practice-ratios.md | age × season-phase matrix synthesis
- Created `wiki/practice-ratios.md` (hub, ~3500-4500 words): 10×5 master matrix
  (blocked / small-group / 6v6 percentages), per-age trajectory paragraphs,
  phase-transition criteria, schools-of-thought roundup.
- Updated 9 age-guides (10s-18s) with `## Practice ratio across the season` section.
- Updated 3 age-lens pages (14U/HS/college) replacing static drill-mix-ratio lines
  with phase-progression mini-paragraphs.
- Updated `practice-planning.md` "Practice ratios" subtopic line to wikilink the new page.
- No new source pages needed; cited ~22 existing sources.
- Touched 14 files + 1 new file = 15 files.
```

---

## 5. Cross-link invariant compliance (SCHEMA §6)

| Invariant | Status |
|---|---|
| #1: Drill pages link ≥1 source + ≥1 technique | N/A — not editing drill pages |
| #2: Coach pages link ≥1 school + ≥1 source | N/A |
| #3: Contested-technique schools-perspectives | N/A |
| #4: Source pages exist before citation | ✓ All 22 cited sources verified to exist |
| #5: No orphaned pages | ✓ New hub has 13+ inbound wikilinks (practice-planning + 9 age-guides + 3 age-lens) plus index/log |
| #6: All inline citation-keys resolve | ✓ All citation-keys in cited list verified to exist |

**Frontmatter validation:**
- `type: hub` — valid enum ✓
- `area: practice-planning` — already used by `practice-planning.md` ✓
- `subtopics:` — list valid ✓

---

## 6. Source pages cited (all verified to exist)

Methodology core:
- `[[shea-1979-contextual-interference]]`
- `[[magill-1990-contextual-interference-review]]`
- `[[pinder-2011-representative-learning-design]]`
- `[[woods-2020-sport-ecology-designers]]`
- `[[gms-nd-structure-practice]]`

USAV / school-philosophy:
- `[[usav-2009-cap-game-like-training]]`
- `[[usav-2026-youth-volleyball-tips]]`
- `[[usav-2026-growing-kids-volleyball]]`
- `[[usav-2026-simplified-youth-rules]]`
- `[[usav-2026-coach-academy]]`

Practice / season planning:
- `[[aoc-2024-kiraly-training-efficiently]]`
- `[[aoc-2024-motor-learning]]`
- `[[aoc-2021-mattox-early-season-practice]]`
- `[[aoc-2023-rose-club-rules]]`
- `[[mccutcheon-2022-championship-behaviors]]`
- `[[aoc-2024-setting-hand-hinge]]` (cited in 14s sample for hand-hinge install-window claim)
- `[[aoc-2021-youth-15-drills]]` (cited in 10s sample for Newkirk's youth sampler)

Volleyball-specific evidence (recent):
- `[[qu-2025-contextual-interference-volleyball-serve]]`
- `[[apidogo-2021-differential-learning-volleyball]]`
- `[[caldeira-2023-functional-movement-variability]]`
- `[[moy-2024-constraints-led-volleyball-serve]]`

Season-load / fatigue / season-arc:
- `[[pires-2021-burnout-coping-volleyball-season]]`
- `[[sanders-2025-early-season-jump-load-d1-volleyball]]`
- `[[rebelo-2024-training-stress-fatigue-wellbeing]]`
- `[[wang-2024-concurrent-training-strength-endurance]]`

---

## 7. Implementation sequence

The implementation plan (created via `superpowers:writing-plans` after this spec is approved) will follow this execution order to allow each commit to be self-contained and reviewable:

1. **Write `wiki/practice-ratios.md`** — full hub page with master matrix, all 10 per-age trajectory paragraphs, phase-transition criteria, schools-of-thought, getting-started, related-areas, sources.
2. **Update `practice-planning.md`** hub line.
3. **Update `wiki/index.md`** with new hub entry.
4. **Add age-guide sections** — 9 separate edits (10s.md through 18s.md).
5. **Replace age-lens drill-mix-ratio lines** — 3 edits (14U / HS / college).
6. **Append `wiki/log.md`** entry.
7. **Lint pass** — verify no orphaned pages, no broken citation-keys, all wikilinks resolve.
8. **Single git commit** with SCHEMA §8.1-style message: `add: practice-ratios hub · age × season-phase matrix · touched 14 pages + 1 new`.

---

## 8. Risks & open questions

### 8.1 Risks

- **Static cells become wrong as the wiki accumulates new evidence.** Mitigation: state the synthesis-not-constants disclosure prominently; cells are design-time defaults updateable as new evidence lands. The `wiki/log.md` history will show when cells last changed.
- **Coach reads percentages as prescriptive.** Mitigation: page text explicitly says ±10pp adjustments are normal for team-stage variation; phase-transition criteria provide signs-not-timelines for advancing.
- **Per-page sections drift from the master.** Mitigation: master is single source of truth; lint pass on commit verifies each age-guide's cited row matches master. If a future cell change happens, the lint failure flags out-of-sync per-page sections.
- **Bucket boundaries are fuzzy in practice.** Mitigation: edge calls explicitly named in the bucket-definitions section (pepper, wash drills, position-specific work, coach-fed live-decision drills).

### 8.2 Open questions deferred to implementation phase

- Final wave-label assignment in `wiki/index.md` (cosmetic — pick whatever the index uses at commit time).
- Whether to add a small "How to plan a 90-min practice from this matrix" worked-example callout (decide at writing time based on whether it's repetition of macrocycle pages or genuinely value-additive).
- Whether to re-flow `season-planning.md` to wikilink the new page (low-priority follow-up; the practice-planning hub already does this).

---

## Appendix A — Sample per-age paragraphs (for the writing phase)

### A.1 14s (the user's primary)

> The 14s row sits at the developmental hinge: forearm-pass platform and setting hand-hinge are stable enough to interleave, but 5-1 position commitment and complex 6-2 are still ahead. Preseason runs **40/35/25** — heavy install with the platform-and-hands work that, if missed at 13-14, is hard to recover at 17 [aoc-2024-setting-hand-hinge]. Mid-season balances at **30/35/35** as the team's repertoire stabilizes; small-group work skews competitive — `[[queen-of-the-court]]`, `[[wash-drill]]` 3v3 variants, `[[cooperative-25-goal]]`. Late season climbs to **25/35/40** with `[[gold-medal-scrimmage]]` and `[[transition-rally]]` formats taking more 6v6 time as rotations track without prompting. Pre-tournament-peak hits **20/30/50** — the highest 6v6 density of the 14s year, with simulated bracket play and `[[pressure-serving]]`. Taper trims volume but bumps blocked back to **30/30/40** — `[[serve-targets]]`, controlled `[[pass-set-hit]]`, contact freshness without competition fatigue. The growth-spurt reality means the platform is on a moving target through this year; revisit blocked install reps mid-season for athletes who grew 2+ inches over the holidays.

### A.2 10s (youngest extreme)

> 10s is where the matrix shape diverges most from the older ages. Preseason **40/55/5** has bucket 3 (4v4 modified format, not 6v6) at near-zero because USAV's developmental philosophy keeps formal competition minimal at this age — the 5pp is for end-of-practice 4v4 grills, not real bracket play. The dominant pattern across the row is **bucket 2 holding stable at 50-55%** through every phase: `[[partner-pepper-warmup]]`, scored `[[serve-targets]]`, mini-grills, Newkirk's 15-drill youth sampler [aoc-2021-youth-15-drills] are the meat of the year. Bucket 1 stays at 25-40% for movement-discovery and brief platform-introduction moments — short segments, frequent rotation, kids prefer games over drills [usav-2026-youth-volleyball-tips]. Pre-tournament-peak (if it applies — many 10s programs have no peak event) lifts 4v4 simulation to 25%. Taper at this age is more a volume cut than a ratio shift; the 35/50/15 column is for programs with a real culminating tournament. Coaches running rec or developmental 10s should treat the row as ceiling, not floor.

### A.3 College (oldest extreme)

> College sits at the matrix's live-dominant pole because by the time athletes are on a roster, patterns are largely stable and the marginal return on blocked-time has dropped. Preseason **25/25/50** reflects NCAA fall camp: system install with experienced returners, blocked work concentrated on individual position-specific repair (setter footwork, libero second-ball reads, hitter arm mechanics) rather than team-wide platform install. Mid-season **20/25/55** is the conference-block default, with `[[wash-drill]]` and `[[gold-medal-scrimmage]]` carrying most of practice. Late-season **15/20/65** drops blocked further as opponent-specific tactical work takes over and small-group time gets squeezed by tournament density. Pre-tournament-peak **10/15/75** is the conference-tournament or NCAA-bracket week — the live-dominant ceiling of the program. Taper **15/15/70** holds the live percentage tighter than younger ages because elite athletes can absorb live volume better, so the volume cut does the work and the ratio barely moves. NCAA hours rules cap the total minutes; rotation is what moves, not bucket allocation. Concurrent S&C considerations apply [wang-2024-concurrent-training-strength-endurance].

---

**End of spec.**
