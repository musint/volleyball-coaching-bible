# Wiki Improvement — Tracks 1 + 2 Design Spec

**Date:** 2026-04-24
**Owner:** Song Mu (song.mu@discordapp.com)
**Pattern source:** `Instructions/llm-wiki.md`
**Predecessor spec:** `docs/superpowers/specs/2026-04-22-volleyball-coaching-bible-design.md`

---

## 1. Context

### 1.1 Why this work

The wiki cleared its Wave 0–6 bootstrap (design spec §6) and sits at roughly 400 content pages, 180,000 words, 597 source pages, and exhaustive AOC coverage. Technique and age-lens pages are flagship-quality and the three-layer architecture is holding.

Two distinct improvement axes remain before the wiki is maximally useful:

1. **Usability axis** — the wiki today is a dense *library*; it is not yet a *working tool* you reach for to plan Tuesday's practice in ten minutes. Missing skill-level navigation, unused Dataview hooks, and the absence of concrete practice-plan templates keep every weekly question as a cold synthesis pass.
2. **Integrity axis** — a mini-lint pass on 2026-04-24 found 116 broken wikilinks, ~15 heavily-cited secondary coaches without profiles, ~40 unresolved `[unsourced]` claims, no automated lint, and a cluster of uncommitted `raw/` material from earlier scrubs.

This spec covers both axes in one project. Track 1 addresses usability; Track 2 addresses integrity. They ship together because the work is independent and parallelizable, and because the wiki is healthiest when structural growth (Track 1) and cleanup (Track 2) happen in the same session.

### 1.2 Who this serves

- **Primary user:** Song Mu, 14U girls club head coach at a nationally-recognized program, using the wiki week-to-week for practice planning, in-match adjustments, and season planning.
- **Coverage obligation:** HS varsity and college materials exist at mastery depth for the wiki's long-horizon role, not as Song's immediate week-to-week context.

### 1.3 Positioning stance

Unchanged from the bootstrap design spec §1.3: neutral reference. Preferred-tradition material (Kiraly, AOC, GMS, USAV, Japanese) remains first-among-equals in coverage depth; no school is favored on any page; contested topics present tradeoffs without resolution.

---

## 2. Scope

### 2.1 Deliverable matrix

| Bucket | Count | Nature |
|---|---:|---|
| Skill hub pages | 7 | New (hub type) |
| Dataview retrofits | ~25 | Edits to existing pages |
| Practice-plan templates | 15 | New page type (net-new) |
| Secondary-coach profiles | 15 | New (coach type) |
| Unsourced-queue backfills | ~40 | Research + edits |
| Lint script + pre-commit hook | 1 | New tooling |
| Residual broken-link + uncommitted cleanup | varies | Edits + git |

Net: ~37 new content pages, ~25 Dataview retrofits, ~40 sourced claims cleared, 1 automation script, plus cleanup.

### 2.2 Non-goals (explicit YAGNI)

Tracks 1+2 do **not** include:

- A web frontend. Obsidian remains the reader.
- A live practice-planning app. Practice-plan templates are markdown files authored once, not a dynamic composer.
- Beach volleyball or coach-certification study guides (out of scope per bootstrap §1.4).
- Track 3 (deep 14U operational layer: season arc, tryout doc, parent comms, scouting templates, Munciana drill cluster). Track 3 is scoped separately and should follow as a third spec after Tracks 1+2 complete.
- Automated ingestion pipelines. Ingestion stays agent-driven per SCHEMA §8.1.
- Rewrites of existing Wave 2–5 content. Edits to existing pages are limited to (a) Dataview insertion, (b) `[unsourced]` replacement with citations, (c) minor cross-link additions surfaced by lint.

---

## 3. Track 1 — Usability axis

### 3.1 Skill hub pages (7)

**Motivation.** `[[passing]]`, `[[setting]]`, `[[hitting]]`, `[[blocking]]`, `[[serving]]`, `[[defense]]`, `[[transition]]` are referenced 10–18 times each in existing pages but no page exists at those slugs. These are the highest-traffic structural gaps in the wiki graph.

**Placement.** At `wiki/` root, peers of the other hubs (`practice-planning.md`, `systems.md`, `philosophy.md`, etc.). They sit *between* the area-level hubs and the per-subskill technique pages: `passing.md` sits above `passing-forearm.md`, `passing-overhead.md`, `passing-serve-receive.md`, `passing-free-ball.md`.

**Type.** Hub page type per SCHEMA §3.1 — no new page type needed.

**Required body sections** (per SCHEMA §3.1): Overview, Major subtopics (= the subskill technique pages), Schools of thought (where schools disagree on this skill), Getting started, Related areas, Sources. Target length 600–1200 words.

**Frontmatter:**
```yaml
---
type: hub
area: passing   # or setting/hitting/etc.
subtopics: [passing-forearm, passing-overhead, passing-serve-receive, passing-free-ball]
---
```

**Cross-link expectations.** Each hub wikilinks to (a) each of its subskill technique pages, (b) the position pages that most rely on the skill, (c) the related drills category cluster, (d) the age-lens pages, (e) any school pages with distinctive methodology on this skill. No inline citations in bodies (hub pages are navigational per SCHEMA §5); `## Sources` at bottom lists the sources that inform the overview.

**Broken-link impact.** The 7 hubs resolve 70–90 of the current 116 broken wikilinks as a direct side effect of their creation.

### 3.2 Dataview retrofits (~25 pages)

**Motivation.** Every drill carries Dataview-ready frontmatter (`primary-skill`, `phase`, `levels`, `duration-min`, `team-size-min`, `team-size-max`, `techniques`, `equipment`) and so does every technique, coach, school, and source. Zero Dataview queries currently exist. The single largest UX multiplier in the wiki is sitting unused.

**Retrofit targets.**

- **7 skill hub pages** (from §3.1): auto-rendered drill catalog filtered by skill.
- **3 age-lens pages** (`age-lens-14u.md`, `age-lens-hs.md`, `age-lens-college.md`): auto-rendered drill catalog filtered by `contains(levels, "<label>")`.
- **6 position pages**: drill catalog filtered by the position's `key-skills`.
- **2 planning hubs** (`practice-planning.md`, `season-planning.md`): drill index grouped by phase; source index grouped by topic.
- **2 wide hubs** (`philosophy.md`, `systems.md`): contested-technique table; age-appropriate system-stack table.
- **1 `schools/` cross-page** (optional, add if trivial): contest-matrix of which schools disagree on which techniques.

**Representative query (on `passing.md`):**
```dataview
TABLE phase, levels, duration-min, team-size-min + "-" + team-size-max AS size
FROM "wiki/drills"
WHERE primary-skill = "passing" OR contains(techniques, "passing-forearm") OR contains(techniques, "passing-overhead")
SORT phase ASC, duration-min ASC
```

**Representative query (on `age-lens-14u.md`):**
```dataview
TABLE primary-skill, phase, duration-min, team-size-min + "-" + team-size-max AS size
FROM "wiki/drills"
WHERE contains(levels, "14u")
SORT primary-skill ASC, duration-min ASC
```

**Representative query (on `practice-planning.md`, grouped):**
```dataview
TABLE rows.file.link AS drills, rows.duration-min AS duration
FROM "wiki/drills"
GROUP BY phase
SORT phase ASC
```

**Obsidian dependency.** Dataview rendering requires the Dataview community plugin. Update SCHEMA §2.2 with a one-line install note. Queries degrade gracefully to their markdown source when Dataview is absent, so the pages remain readable without the plugin.

**Pattern.** Each retrofit adds a `## Drill catalog` or `## Sources index` subsection above `## Sources`, containing the query in a fenced code block. Existing page content is left intact.

### 3.3 Practice-plan templates (15)

**Motivation.** 50 drill pages exist, 3 age-lens pages exist, 2 planning hubs exist — but zero concrete practice-plan templates. Every request like "give me a 90-minute 14U serve-receive practice" becomes a cold synthesis. Templates turn the wiki from "library you read" into "tool you reach for on Tuesday."

**New page type.** `practice-plan` becomes page type #10 in SCHEMA §3. New folder `wiki/practice-plans/`.

**Filename pattern.** `<level>-<duration>-<label>.md` — e.g. `14u-90min-serve-receive.md`. The `<label>` is a descriptive kebab-case slug (typically the plan's focus, or the season context when that is more identifying than the focus). The frontmatter carries the structured enum values (`focus`, `season-phase`) so filename-as-label and enum tagging don't collide.

**Frontmatter contract:**
```yaml
---
type: practice-plan
level: 14u                    # enum: 14u | hs | college
duration-min: 90              # integer
focus: serve-receive          # enum: see below
season-phase: mid-season      # enum: preseason | mid-season | pre-tournament | taper | tryout | postseason | match-day
drills: [butterfly-passing, pass-set-hit, cooperative-25-goal]   # ≥3 required — each must resolve to a drill page
sources: [...]                # ≥1 required
---
```

**`focus` enum:** `passing | setting | hitting | blocking | serving | defense | transition | serve-receive | out-of-system | match-prep | player-development | composite`. (The composite value covers plans that split time evenly across multiple skills.)

**Required body sections.**
- `## Context` — one paragraph on what this plan is for, what problem it solves, what kind of team it fits
- `## Learning objectives` — 3–5 bullets, measurable
- `## Time blocks` — the practice itself, with each block naming its drills via `[[wikilink]]` and time allocation:
  - `### Warm-up (N min)` — ball-in-hand, dynamic, jump warm-up if called for
  - `### Skill development (N min)` — blocked + random as appropriate
  - `### Strategic (N min)` — team-tactic installation or review
  - `### Competition (N min)` — scored game-like work
  - `### Cool-down (N min)` — mobility + reflection
  - (Plans may reorder blocks per methodology; e.g., a game-based plan may front-load competition.)
- `## Coaching cues` — 5–8 cue language items, tied to the plan's objectives
- `## Variations` — three knobs for scaling up/down (team size, intensity, time)
- `## Adaptations by level` — what changes if you run this at a higher or lower level
- `## Sources` — linked source pages

Target length: 500–800 words per template.

**Coverage (5 × 14U + 5 × HS + 5 × college = 15).**

*14U:*
1. `14u-90min-serve-receive.md` — serve-receive focus, mid-season
2. `14u-120min-pre-tournament.md` — competition-heavy, pre-tournament
3. `14u-90min-transition.md` — transition-offense focus, mid-season
4. `14u-60min-tryout.md` — evaluation-oriented, tryout
5. `14u-90min-first-week.md` — team-formation + fundamentals install, preseason

*HS:*
6. `hs-120min-preseason-intensity.md` — fall preseason intensity, preseason
7. `hs-90min-mid-season-tuesday.md` — typical Tuesday mid-season microcycle, mid-season
8. `hs-90min-match-prep.md` — pre-Friday match-prep, mid-season
9. `hs-60min-match-day-activation.md` — day-of activation, match-day
10. `hs-120min-postseason-development.md` — post-season player development, postseason

*College:*
11. `college-120min-ncaa-fall-pre-match.md` — pre-match preparation, mid-season
12. `college-90min-in-season-video.md` — video-driven correction, mid-season
13. `college-120min-spring-individual.md` — spring individual development, postseason
14. `college-120min-conference-week.md` — conference-week serve-pass-defend emphasis, pre-tournament
15. `college-90min-taper.md` — taper day before a major match, taper

Each template uses real drill wikilinks from the existing 50-drill library. Every template resolves `≥3 drills` per the frontmatter contract.

### 3.4 SCHEMA.md updates from Track 1

- Add `practice-plan` as page type #10 in §3 (folder, filename, frontmatter, required sections, target length, citation weight = light).
- Add the `practice-plan` frontmatter block to §4.
- Add `level`, `focus`, `season-phase` to the enum glossary in §4.
- Add Dataview plugin install note to §2.2.
- Add Track 1 updates to §10 session-start checklist (no behavior change, just ensuring new page type is discoverable).

### 3.5 `wiki/index.md` updates from Track 1

- Add a `## Skill hubs` section listing the 7 new skill hubs.
- Add a `## Practice plans` section listing the 15 new templates grouped by level.

---

## 4. Track 2 — Integrity axis

### 4.1 Secondary-coach profiles (15)

**Selection principle.** Target the most-cited orphans, weighted toward source richness + direct relevance to Song's 14U club-coaching context.

**High-source, full-length (~1500 words each) — 8 profiles:**
1. **Salima Rockwell** — Penn State alum, Texas/Louisville assistant; AOC defense + setter-training corpus (11+ pieces)
2. **Jim Stone** — author *Defensive Volleyball Drills*; Ohio State; AOC defense/blocking corpus
3. **Diane Flick-Williams** — Western Washington; AOC pass-for-points flagship
4. **John Lingenfelter** — Munciana Volleyball Club; directly matches Song's nationally-recognized club context
5. **Luka Slabe** — AOC static/swing/combo blocking corpus
6. **Laurie Eisler** — Illinois HC; AOC competitive-cauldron feature with McCutcheon
7. **Christy Johnson-Lynch** — Iowa State; AOC transition + setter-training corpus
8. **Doug Beal** — 1984 LA Olympic men's gold HC; historical anchor for US men's program

**Moderate-source, briefer (~800 words each) — 7 profiles:**
9. **Jen Flynn Oldenburg** — Ohio State; AOC piece
10. **Kerry MacDonald** — AOC attack arm mechanics piece
11. **Gina Schmidt** — AOC attack approach 2024 piece
12. **Brian Rosen** — AOC swing-block-beginners progression piece
13. **Mark Barnard** — AOC back-row-attacking-basics piece
14. **Brandon Rosenthal** — AOC rapid-fire drill piece
15. **Todd Dagenais** — referenced in McCutcheon profile (Central Florida HC); biographical-level profile given thin source base

**Universal requirements (all 15).**
- Frontmatter per SCHEMA §3.2 coach profile: `type: coach`, `name`, `country`, `era`, `roles`, `schools` (≥1), `sources` (≥1).
- Body sections per SCHEMA §3.2: Overview, Coaching career, Core teaching principles, Contributions to the game, Quotes & representative passages, Sources.
- Heavy citation per SCHEMA §5.
- Unsourced claims get `[unsourced]` tag + queue entry per SCHEMA §5 rules.
- Each profile adds bidirectional cross-link fixes (e.g. Lingenfelter → `schools: [munciana-volleyball-club]` with a stub page if the school doesn't exist).

**Broken-link impact.** These 15 profiles resolve ~25 of the current 116 broken wikilinks (the coach-name slugs) plus indirectly more via their school stub/creation cascades.

### 4.2 Unsourced-queue backfill (~40 entries)

**Cluster strategy.** Group the 40 entries by research pathway — each cluster becomes one parallel research subagent. Each subagent follows SCHEMA §8.1 ingest: fetch primary → save to `raw/` → create `sources/` page → replace `[unsourced]` tags with `[citation-key]` → clear the queue entry. Any claim that still can't be sourced stays `[unsourced]` with an updated research hypothesis.

**Clusters:**

1. **NCAA recruiting calendar** (2 entries, `wiki/recruiting.md`) → NCAA.org D1 recruiting-calendar page + AVCA recruiting resources + PrepVolleyball explainers
2. **AVCA awards + Wise tenure ranking** (4 entries, `wiki/coaches/mary-wise.md`) → AVCA awards history + Florida official bio + Hall of Fame induction materials
3. **Bernardinho + Guimarães + Brazilian methodology** (11 entries across `wiki/coaches/bernardinho.md` and `wiki/schools/brazilian-school.md`) → Bernardinho's *Transformando Suor em Ouro* publisher preview + AOC/FIVB long-form interviews + CBV features + Brazilian journalism retrospectives
4. **Velasco methodology** (7 entries, `wiki/coaches/julio-velasco.md`) → Velasco clinic recordings + Italian NT features + CEV material
5. **Guidetti methodology** (3 entries, `wiki/coaches/giovanni-guidetti.md`) → VakıfBank + CEV features + modern-European-club material
6. **Daimatsu + Japanese historical** (3 entries, `wiki/coaches/daimatsu-hirobumi.md`) → Roy Tomizawa's *1964 - The Greatest Year in the History of Japan* + Helen Macnaughtan academic work + period Japanese newspapers (via secondary English coverage)
7. **Hebert thin-source base** (7 entries, `wiki/coaches/mike-hebert.md`) → Human Kinetics preview of *Thinking Volleyball* + AVCA bio + Illinois/Minnesota/New Mexico program histories
8. **USAV CAP editorial claims** (4 entries, `wiki/schools/usa-volleyball.md`) → Coach Your Brains Out podcast back-catalog + GMS/AOC CAP commentary + private-coach blogs circa 2020–2024
9. **Nakagaichi 1972 [unverified]** (1 entry across Nakagaichi profile + Japanese-training school) → identify actual 1972 Japan men's gold HC via FIVB records, JVA records, or historical features; update the `[unverified]` tag to a citation or retire the claim

Each cluster's success is measured by `[unsourced]` tags cleared in the target wiki pages AND queue entries cleared in `wiki/unsourced-queue.md`.

### 4.3 Lint automation

**Tool.** `tools/lint.py` — Python 3 script, no external deps beyond pyyaml.

**Checks (the seven SCHEMA §5.3 checks, made concrete):**

1. **Orphan scan** — enumerate wiki pages with zero inbound `[[wikilink]]` references. Source pages with `## Where it's cited` populated don't count as orphans.
2. **Cross-link invariant check** — the six SCHEMA §6 rules:
   - Drill: ≥1 source + ≥1 technique via frontmatter
   - Coach: ≥1 school + ≥1 source
   - Contested technique: ≥2 `schools-perspectives` entries
   - Every source page referenced by a citation must exist
   - No orphan pages
   - Every inline `[citation-key]` resolves to a source page's `citation-key` field
3. **Broken-wikilink count** — `[[slug]]` in any body where `wiki/**/slug.md` does not exist. Report count and first 20 offending links.
4. **Unsourced-queue consistency** — bidirectional: every `[unsourced]` tag in any wiki body has a matching entry in `wiki/unsourced-queue.md` (by page path + exact sentence), and every queue entry still points at a real page and a real sentence.
5. **Frontmatter validation** — required fields per page type, valid enum values, resolvable `citation-key`s in `sources:` arrays.
6. **Stale-claim scan** — for pages of type `school`, `hub`, `age-lens` (the methodology-heavy types): flag if the newest cited source is more than 5 years older than today.
7. **Concept-gap detection** — terms that appear on ≥3 pages as `[[wikilinks]]` but don't have a dedicated page.

**Outputs.**
- **Human-readable report** at `wiki/lint-report.md` — sections per check, counts, first-N offenders with file paths.
- **Exit code** — non-zero if any check fails OR if broken-wikilink count is higher than the previous report.

**Pre-commit hook** at `.git/hooks/pre-commit`:
- Runs lint
- Blocks commit if broken-wikilink count increases relative to `wiki/lint-report.md` baseline
- Does NOT block on other check failures (warn-only) — the checks are advisory except for broken links, which are objectively regressions

**Operator UX.** `python tools/lint.py` full pass any time; output lands in `wiki/lint-report.md` and the terminal. Pre-commit hook runs automatically on every commit.

### 4.4 Residual cleanup

**Remaining broken wikilinks (after §4.1 and §3.1).** Current 116 → after 7 skill hubs (~80 resolved) → after 15 coach profiles (~25 more resolved) → estimate ~15–20 residual. These break into:
- Drill variants referenced in technique bodies (`[[blitz-the-bro]]`, `[[wave-serve-receive]]`, `[[three-person-serve-receive]]`) — evaluate each: if it's a real drill that deserves a page, create one; if it's just a variation name inside an existing drill's `## Variations`, remove the wikilink syntax.
- Institutional slugs referenced in coach profiles (`[[illinois-volleyball]]`, `[[byu]]`, `[[brigham-young-university]]`, `[[china-women-national-team]]`) — create institutional-tradition stubs following the existing `[[penn-state]]`/`[[florida]]`/`[[chinese-volleyball-tradition]]` precedent in `wiki/schools/`.
- Generic-concept slugs (`[[footwork]]`, `[[ball-control]]`, `[[injury-prevention]]`) — decide case-by-case: either create a stub, retire the wikilink, or point it at an existing page.

**Munciana Drills/ folder (uncommitted).** Inspect contents:
- If drill write-ups → ingest via SCHEMA §8.1 ingest workflow into `raw/articles/` or a new `raw/munciana/` subfolder, create `sources/` pages, optionally cluster into a Munciana drill-library landing page. Lingenfelter profile (§4.1) links to whatever lands here.
- If articles/notes → `raw/articles/` with `munciana-` prefix, source-page as appropriate.
- Decision per file; do not bulk-commit without inspection.

**Uncommitted `raw/articles/aoc-*.md` files.** There are 80+ files in `git status` untracked. These appear to be leftover fetches from the 2026-04-23 deep-scrub (§log) that were raw-ingested but may not have paired `wiki/sources/` pages.
- For each: check if `wiki/sources/<matching-slug>.md` exists. If yes → just commit the raw file. If no → create the source page per SCHEMA §3.8.
- If any are duplicates of already-ingested material → delete cleanly with a log note.

**Final commit hygiene.** One commit per bucket with well-structured messages per project git conventions. Example bucket commits:
- `feat(wiki): add 7 skill hub pages (passing/setting/hitting/blocking/serving/defense/transition)`
- `feat(wiki): add 25 Dataview retrofits across hubs, age-lens, positions`
- `feat(wiki): add 15 practice-plan templates (5×14U + 5×HS + 5×college)`
- `feat(wiki): add 15 secondary-coach profiles`
- `feat(wiki): backfill 40 unsourced-queue entries across 9 research clusters`
- `feat(tools): add lint.py + pre-commit hook`
- `chore(wiki): resolve residual broken wikilinks and ingest uncommitted raw/`

---

## 5. Execution strategy

### 5.1 Dispatch plan

**Dispatch 1 — parallel content writers (~24 agents):**
- 7 × skill-hub writer
- 15 × coach-profile writer
- 1 × Dataview retrofit batch (single agent owns the ~25 retrofits since the pattern is mechanical and ordering matters)
- 1 × `tools/lint.py` author

**Dispatch 2 — parallel plans + research (~24 agents):**
- 15 × practice-plan writer (one per template)
- 9 × unsourced-backfill research cluster (one per cluster from §4.2)

**Between dispatches:** run `python tools/lint.py` once the lint script exists (after Dispatch 1). Confirm broken-wikilink count is dropping and invariants are holding. Triage any violations before Dispatch 3.

**Dispatch 3 — cleanup pass:**
- 1 × Munciana folder ingest
- 1 × uncommitted `raw/articles/aoc-*.md` pairing
- 1 × residual broken-wikilink resolution (after the lint report lands)
- 1 × concept-gap stub creation (for any concept-gap the lint surfaces)

**Final:** clean commits per §4.4, checkpoint summary entry in `wiki/log.md`, final lint run with the report attached to the summary.

### 5.2 Checkpoints

- **After Dispatch 1:** confirm skill hubs and coach profiles ship clean; Dataview queries render (I'll test one in Obsidian if accessible, or trust the markdown syntax); lint script passes its own unit tests.
- **After Dispatch 2:** confirm practice-plan templates + unsourced-queue backfill ship; run full lint; report numbers per check.
- **After Dispatch 3:** final lint report, residual count → 0 (or documented exceptions), all commits pushed.

### 5.3 Rollback / containment

- Every dispatch writes to a discrete area of the wiki (new folders, new pages, or additive Dataview blocks). If any individual agent ships junk, its output can be reverted via `git revert` without touching other work.
- The lint pre-commit hook prevents broken-link regressions from landing silently.
- SCHEMA.md and `wiki/index.md` changes are each their own small commit, easy to revert independently.

---

## 6. Success criteria

### 6.1 Acceptance checklist

Tracks 1+2 are complete when all of these hold:

- [ ] 7 new skill hub pages exist at `wiki/` root; each has required frontmatter + required body sections; each wikilinks to its subskill techniques, related positions, and related age-lenses.
- [ ] ~25 Dataview retrofits land across the hubs + age-lens + position pages; each query renders without error in Obsidian with the Dataview plugin enabled.
- [ ] 15 practice-plan templates exist in `wiki/practice-plans/` at the specified filenames; each has required frontmatter, required body sections, and ≥3 real drill wikilinks that resolve.
- [ ] SCHEMA.md is updated with the `practice-plan` page type and the Dataview install note.
- [ ] 15 secondary-coach profiles exist in `wiki/coaches/`; each has ≥1 school + ≥1 source in frontmatter; each has all required body sections.
- [ ] `wiki/unsourced-queue.md` count is < 10 (down from ~40), with remaining entries justified by sources that were chased but unavailable.
- [ ] `tools/lint.py` exists, runs cleanly, produces `wiki/lint-report.md`, and exits non-zero on regression.
- [ ] `.git/hooks/pre-commit` exists and blocks commits that increase broken-wikilink count.
- [ ] Broken-wikilink count is < 10 in the final lint report (down from 116).
- [ ] `Munciana Drills/` folder is fully committed or explicitly deferred with a log note.
- [ ] Uncommitted `raw/articles/aoc-*.md` files are either paired with source pages, deleted as duplicates, or explicitly deferred with a log note.
- [ ] `wiki/log.md` has an entry for each dispatch with touched-page counts.
- [ ] `wiki/index.md` reflects the new skill hubs, practice-plans folder, and new coach profiles.

### 6.2 Scenario tests

Three real queries that must work cleanly once Tracks 1+2 are done:

1. **"Give me a 90-minute 14U serve-receive practice plan."** Expected: return `wiki/practice-plans/14u-90min-serve-receive.md` verbatim or with minor tailoring — not a from-scratch synthesis.
2. **"Show me every drill appropriate for HS that focuses on blocking."** Expected: Dataview-rendered table on `blocking.md` (skill hub) or `age-lens-hs.md` answers instantly.
3. **"What does Salima Rockwell teach about defending angles?"** Expected: `wiki/coaches/salima-rockwell.md` with a Core teaching principles section grounded in her AOC corpus, cited.

Any scenario that doesn't work cleanly on final acceptance adds an entry to a Track 3 followup list.

### 6.3 Living-wiki signals (post-Tracks-1+2)

- Practice-plan prompts return templates, not cold syntheses.
- Skill-hub graph view shows a rich mid-layer between area-hubs and technique pages; no isolated constellations.
- Lint runs as part of every commit; broken-link count trends toward zero.
- Unsourced queue never exceeds 15 entries; clearing it becomes a normal cadence operation.

---

## 7. Open items & caveats

1. **Dataview plugin dependency.** Track 1B retrofits require the Dataview Obsidian plugin. Without it, queries show as their source code — not broken, but not useful. SCHEMA §2.2 will note this; we're not supporting Dataview-free rendering in this spec.
2. **Pre-commit hook portability.** `.git/hooks/pre-commit` is per-clone; new clones need the hook re-installed. A small bootstrap script (`tools/install-hooks.sh`) may land as a nice-to-have; not a blocker.
3. **Nakagaichi 1972 [unverified].** If the actual 1972 Japan men's gold HC can't be sourced in §4.2 cluster 9, the claim stays `[unverified]` and the queue entry stays open. This is a known long-standing gap carried forward honestly.
4. **Munciana folder contents are unknown at spec time.** The folder is uncommitted. Inspection happens during Dispatch 3; ingest decisions are per-file. If Munciana Drills turns out to be a rich cluster (≥10 files), it may warrant a dedicated drill-library landing page, which is a Track 3-adjacent nice-to-have not included here.
5. **Secondary coach depth variance.** The 8 full profiles and 7 briefer profiles is a judgment call on source richness. If a "brief" profile writer finds more source material than expected, the profile should lengthen to the full standard; if an agent runs into a thin source base for a "full" profile, it should tag liberally with `[unsourced]` and queue rather than fabricate.
6. **Track 3 deferred.** The 14U-specific operational layer (season arc, tryout doc, parent comms, scouting templates, Munciana drill cluster) is explicitly a later spec, not in this scope.

---

## 8. Next step

Hand off to the writing-plans skill to produce a dispatch-by-dispatch implementation plan with concrete task lists, acceptance checks per dispatch, and the parallel-agent briefing templates.
