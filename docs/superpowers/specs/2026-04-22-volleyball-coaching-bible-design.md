# Volleyball Coaching Bible — LLM Wiki Design Spec

**Date:** 2026-04-22
**Owner:** Song Mu (song.mu@discordapp.com)
**Pattern source:** `Instructions/llm-wiki.md`
**Reference implementation:** `C:/Users/SongMu/documents/claudecode/DataRepository/wiki/` (Discord organizational wiki)

---

## 1. Context

### 1.1 What this is

A persistent, LLM-maintained knowledge wiki covering volleyball coaching — the "coaching bible." Built on the LLM-wiki pattern in `Instructions/llm-wiki.md`: raw sources drive LLM-curated, interlinked markdown pages that compound in value as new sources are ingested. Humans curate sources and ask questions; the LLM writes, cross-references, and maintains the wiki.

### 1.2 Who it's for

- **Owner / primary reader:** Song Mu, head coach at a nationally recognized club program
- **Immediate coaching context:** 14U girls club, indoor 6s
- **Mastery coverage scales to:** HS varsity and college level coaching
- **Use case:** Hybrid — lifelong mastery base + week-to-week working reference (practice planning, in-match adjustments, season planning)

### 1.3 Positioning stance

**Neutral reference.** No school of thought favored. Preferred philosophies (Japanese training, Karch Kiraly, Art of Coaching Volleyball, Gold Medal Squared, USA Volleyball) are well-documented among the rest. Where schools disagree, present tradeoffs; do not pick sides.

### 1.4 Topic scope

**In scope:**
1. Technique (passing, setting, hitting, blocking, serving, defense, transition)
2. Systems (rotations, defensive/offensive systems, serve-receive, blocking systems)
3. Practice design & methodology
4. Drill library
5. Philosophies / schools / coach profiles
6. Season & practice planning
7. Physical training (S&C, jump, mobility, injury prevention)
8. Mental / psychology (culture, leadership, pressure)
9. Match prep & scouting
10. Position-specific coaching (S, OH, MB, OPP, L, DS)
11. Age-group specifics (14U, HS varsity, college lenses)
12. Recruiting & college track
13. Rules / administration (USAV, NCAA, scholastic)
14. Sources & references (dedicated pages per book/video/podcast)

**Out of scope:** beach volleyball, coach certification study guides.

---

## 2. Architecture

Three-layer architecture from the LLM-wiki playbook, made concrete.

### 2.1 Layer 1 — Raw sources (immutable)

Location: `C:/Users/SongMu/documents/claudecode/vba/bible/raw/`

```
raw/
  books/                   PDFs of owned books + per-book notes files when PDFs unavailable
  articles/                Blog posts, features, interviews — web-clipped to markdown
  transcripts/             YouTube/podcast transcripts with source URL + timestamps
  instagram/               Screenshots + captions (IG is ephemeral; snapshot it)
  usav/                    USA Volleyball curriculum, coaching toolbox PDFs, rule docs
  research/                Peer-reviewed papers on motor learning, skill acquisition, ecological dynamics
  images/                  Figures, court diagrams, photos referenced from wiki pages
  INDEX.md                 One-line catalog of every raw source with citation-key
```

**Copyright rule:** the wiki builder will not source or download copyrighted books without rights. Legally acquired PDFs the owner places in `raw/books/` are fair-use summarizable. Otherwise, we cite books using publisher previews, author interviews, clinic recordings, syllabi, reviews — all legal fair-use material.

### 2.2 Layer 2 — The wiki (LLM-owned, Obsidian-compatible)

Location: `C:/Users/SongMu/documents/claudecode/vba/bible/wiki/`

Shallow-nested hybrid: folders only where volume demands. Hub pages at root for singular/overview topics.

```
wiki/
  index.md                    Catalog of every page, one-line summary each
  log.md                      Append-only operation log
  SCHEMA.md                   The agent playbook (see §4)
  unsourced-queue.md          Tracks all [unsourced] claims for future citation hunt

  # Hub pages (singular topics — one page each)
  philosophy.md               Overview + entry into schools/ and coaches/
  systems.md                  Overview + entry into systems-detail/
  practice-planning.md        Session design, periodization, methodology
  season-planning.md          Preseason, in-season, tournament prep
  mental.md                   Culture, leadership, pressure, motivation
  physical.md                 S&C, jump, mobility, injury prevention
  match-prep.md               Scouting, stats, video analysis
  rules.md                    USAV, NCAA, scholastic
  recruiting.md               College pathway (since user is at national club)
  age-lens-14u.md             14U-specific overlays on technique, systems, practice
  age-lens-hs.md              HS varsity lens
  age-lens-college.md         College lens

  # Subfolders for high-volume categories
  coaches/                    One page per notable coach (12–15 at bootstrap)
  schools/                    One page per philosophy / school of thought
  techniques/                 Per-skill + subskill pages
  positions/                  S, OH, MB, OPP, L, DS
  systems-detail/             Specific system pages (5-1, read-blocking, etc.)
  drills/                     Individual drill pages, heavily frontmatter-tagged
  sources/                    One page per major source (book, podcast, video series, article cluster)
```

### 2.3 Layer 3 — The schema (agent playbook)

Two-tier:

- **`C:/Users/SongMu/documents/claudecode/vba/bible/CLAUDE.md`** — project-root pointer auto-discovered by Claude Code at session start. Brief: "this is a volleyball-coaching LLM wiki; read `wiki/SCHEMA.md` before doing anything."
- **`wiki/SCHEMA.md`** — the full operational playbook (see §4). Lives inside the wiki folder so if the wiki moves or is copied, the schema travels with it.

---

## 3. Page taxonomy & frontmatter schema

### 3.1 Nine page types

| Type | Folder | Filename pattern | Example |
|------|--------|------------------|---------|
| Hub | `wiki/` root | `topic.md` | `practice-planning.md` |
| Coach profile | `coaches/` | `firstname-lastname.md` | `karch-kiraly.md` |
| School / philosophy | `schools/` | `slug.md` | `gold-medal-squared.md` |
| Technique | `techniques/` | `skill-subskill.md` | `passing-forearm.md` |
| Position | `positions/` | `position.md` | `setter.md` |
| System | `systems-detail/` | `category-name.md` | `offense-5-1.md` |
| Drill | `drills/` | `slug.md` | `butterfly-passing.md` |
| Source | `sources/` | `author-year-shorttitle.md` | `kiraly-1997-championship-volleyball.md` |
| Age-lens | `wiki/` root | `age-lens-<label>.md` | `age-lens-14u.md` |

Basenames remain globally unique, so Obsidian `[[wikilinks]]` resolve with basename only.

### 3.2 Frontmatter contracts

All pages use YAML frontmatter. Required fields listed; optional fields permitted.

**Link-field convention:** link fields (e.g., `sources`, `schools`, `related-drills`) store **bare page slugs** (the filename without `.md`). This keeps YAML valid and works cleanly with Dataview. In-body references use `[[wikilink]]` form. SCHEMA.md specifies this convention and the lint validator enforces it.

**Hub page**
```yaml
---
type: hub
area: practice-planning
subtopics: [periodization, session-design, microcycle-planning, practice-ratios]
---
```

**Coach profile**
```yaml
---
type: coach
name: Karch Kiraly
country: USA
era: 1980s-present
roles: [player, coach, usa-women-national-team]
schools: [usa-volleyball-cap]                          # ≥1 required
tags: [hall-of-fame, three-time-olympic-champion]
sources: [kiraly-1997-championship-volleyball]         # ≥1 required
---
```

**School / philosophy**
```yaml
---
type: school
name: Gold Medal Squared
origin: USA
founders: [carl-mcgown]
core-principles: [motor-learning, random-practice, feedback-timing]
associated-coaches: [carl-mcgown, mike-hebert, chris-mccray]
related-schools: [ecological-dynamics]
sources: [mcgown-2013-gms-principles]
---
```

**Technique**
```yaml
---
type: technique
skill: passing                                         # enum: passing|setting|hitting|blocking|serving|defense|transition
subskill: forearm-pass
positions: [libero, defensive-specialist, outside-hitter]
related-drills: [butterfly-passing, pepper]
related-techniques: [defense-platform]
schools-perspectives:                                  # ≥2 required if topic is contested across schools
  gms: "Platform angle primary, footwork secondary"
  aoc: "Read first, platform second"
  japanese: "Midline emphasis, quick reset"
sources: [kiraly-1997-championship-volleyball]
---
```

**Position**
```yaml
---
type: position
position: setter
role: primary-ball-handler
physical-profile: "Typically 5'10\"+ for collegiate; quickness > pure height"
key-skills: [setting-hands, setting-jump, defense-platform, serving]
common-drills: [front-back-sets, three-setter-rotation]
related-coaches: [russ-rose, hugh-mccutcheon]
---
```

**System**
```yaml
---
type: system
category: offense                                      # enum: offense|defense|serve-receive|blocking|transition
name: 5-1
age-appropriateness: [14u, hs, college, professional]
complexity: medium                                     # enum: low|medium|high
when-to-use: "When one setter is clearly better than alternatives; gives setter-hitter matchup consistency"
alternatives: [offense-6-2, offense-4-2]
sources: [dunning-2013-volleyball-systems]
---
```

**Drill** (the most Dataview-filterable type)
```yaml
---
type: drill
name: Butterfly Passing
primary-skill: passing                                 # enum matches technique.skill
secondary-skills: [serving, communication]
techniques: [passing-forearm, passing-overhead]        # ≥1 required — links to technique pages
phase: skill                                           # enum: warm-up|skill|strategic|competition|conditioning
team-size-min: 6
team-size-max: 12
duration-min: 10
levels: [14u, hs, college]                             # age-appropriateness
equipment: [ball-cart]
sources: [gms-2022-warmup-webinar]                     # ≥1 required
video-url: https://...                                 # optional
variations: [butterfly-serve-receive, butterfly-defense]
---
```

**Source** (the citation target)
```yaml
---
type: source
source-type: book                                      # enum: book|video-series|podcast|article|interview|clinic|social-post
title: "Championship Volleyball"
author: "Karch Kiraly"
year: 1997
citation-key: kiraly-1997
raw-file: raw/books/kiraly-championship-volleyball.pdf # or notes file path
url: https://...                                       # if web-based
topics: [technique, systems, mental]
featured-coaches: [karch-kiraly]
schools: [usa-volleyball-cap]
trust-tier: 1                                          # enum: 1|2|3 per trust tier policy
---
```

**Age-lens**
```yaml
---
type: age-lens
label: 14u
scope: "14-and-under club-level indoor girls"
emphasis: [fundamentals, ball-control, serve-receive-exposure, tempo-simplicity]
age-ceilings:                                          # things that are NOT age-appropriate
  - "Full swing-blocking systems"
  - "Complex 6-2 for non-setter outside hitters"
sources: [usav-age-appropriate-guidelines]
---
```

### 3.3 Required body sections per page type

Each page type has required markdown sections below the frontmatter. `SCHEMA.md` specifies the full list. Examples:

- **Technique**: `## Overview`, `## Teaching progressions`, `## Common errors`, `## Schools-perspectives`, `## Related drills`, `## Sources`
- **Coach profile**: `## Overview`, `## Coaching career`, `## Core teaching principles`, `## Contributions to the game`, `## Quotes & representative passages` (with citations), `## Sources`
- **Drill**: `## Setup`, `## Execution`, `## Coaching points`, `## Variations`, `## Adaptations by level`, `## Sources`
- **School / philosophy**: `## Overview`, `## Core principles`, `## Methodology`, `## Notable practitioners`, `## Contrasts with other schools`, `## Critiques and limitations`, `## Sources`

Target lengths: drill ≈ 300 words; technique ≈ 800–1500 words; coach profile ≈ 1500 words; school / philosophy page ≈ 2000–2500 words.

### 3.4 Citation policy (heavy / light split)

| Page types | Citation weight | Format |
|------------|-----------------|--------|
| Philosophy, schools, coach profiles, methodology sections of any page | **Heavy** | Inline `[citation-key]` after claims, plus `## Bibliography` section auto-linked to `sources/` pages |
| Technique, drill, position, system pages | **Light** | No inline citations. `## Sources` section at bottom listing linked source pages only |
| Hub pages | Light (they're navigational) | Just list sources of claimed facts |

Inline citation format: `[citation-key]` where `citation-key` matches the `citation-key` field in the relevant `sources/` page's frontmatter. Unresolvable citation-keys fail lint.

**Unsourced claims:** any claim that cannot be backed by a source gets an inline `[unsourced]` tag AND an entry in `wiki/unsourced-queue.md`. This keeps intellectual honesty mechanical and gives lint a worklist.

### 3.5 Cross-link invariants (enforced by lint)

1. Every drill page must link to ≥1 source page and ≥1 technique page.
2. Every coach profile must link to ≥1 school page and ≥1 source page.
3. Every technique page where schools genuinely disagree must have ≥2 entries in `schools-perspectives`.
4. Every source page must exist before being cited anywhere.
5. No page may be orphaned (zero inbound links) — every page is reachable from a hub or peer.
6. Every `[citation-key]` must resolve to a source page's `citation-key`.

---

## 4. `SCHEMA.md` — the agent playbook

`SCHEMA.md` is the CLAUDE.md-for-the-wiki. Every future session reads it first. Its job: turn any Claude-flavored agent into a disciplined maintainer of this specific wiki.

### 4.1 Contents outline (10 sections)

1. **Preamble** — what this wiki is, who the user is, positioning stance, source preferences.
2. **Directory map** — `wiki/` and `raw/` tree with one-line descriptions per folder.
3. **Page types reference** — for each of the 9 page types: folder, filename pattern, required frontmatter, required body sections, target length, linking norms.
4. **Frontmatter contracts** — full spec per type, including enum values (e.g., `phase ∈ {warm-up, skill, strategic, competition, conditioning}`).
5. **Citation rules** — heavy/light policy per page type, inline format, bibliography template, source-page-first rule.
6. **Cross-link invariants** — the 6 lint-enforced rules from §3.5.
7. **Source trust tiers** — see §4.2 below.
8. **Voice & style guide** — see §4.3 below.
9. **Anti-patterns** — see §4.4 below.
10. **Session-start checklist** — the 4-step drill every new session runs: read `SCHEMA.md`, scan `index.md`, tail last 10 lines of `log.md`, read the relevant area hub page.

### 4.2 Source trust tiers

Priority-ordered; cite accordingly.

**Tier 1 — Primary / authoritative.** Cite freely.
- Published books by credentialed coaches (Kiraly, McCutcheon, Hebert, Liskevych, Dunning, Rose, etc.)
- USA Volleyball official resources (CAP, coaching toolbox, age-appropriate guidance)
- Peer-reviewed research on motor learning, skill acquisition, sports science

**Tier 2 — Trusted secondary.** Cite with affiliation noted.
- Art of Coaching Volleyball content
- Gold Medal Squared materials
- The Net Live
- VolleyballMag
- Established federation sites (FIVB, JVA, CEV)
- Clinic recordings from major conventions (AVCA Convention, USAV High Performance Coach Clinic)

**Tier 3 — Corroborate before citing.** Attribute clearly; use only if supported by a Tier 1/2 source OR coming from a verified coach/athlete account.
- Instagram, TikTok (verified coach/athlete accounts only)
- YouTube non-credentialed channels
- Forum threads, uncredited blogs

### 4.3 Voice & style guide

- **Person:** second-person ("you") addressing the reader coach
- **Tense:** present
- **Precision:** specific over vague. "90% of 14U teams run 6-2 or 4-2" > "most teams run 6-2 or 4-2"
- **Age-appropriateness flags:** when technique/systems guidance assumes a level, say so explicitly
- **Medical / S&C disclaimers:** never give medical advice; always defer to qualified professionals (ATs, CSCSs, physicians)
- **Neutrality on school disagreements:** present both views, attribute, do not resolve

### 4.4 Anti-patterns (explicit "don'ts")

- **Never fabricate citations.** If a claim can't be sourced, tag `[unsourced]` and queue.
- **Never pick sides** on school disagreements. Present tradeoffs.
- **Never duplicate content** across pages — cross-link instead.
- **Never write content in `index.md` or `log.md`.** `index.md` is a catalog; `log.md` is chronological operations only.
- **Never cite a source page that doesn't exist.** Create the source page first.

---

## 5. Operational workflows

Four workflows live in `SCHEMA.md`. Each is a numbered checklist the agent follows on invocation.

### 5.1 Ingest (new source → wiki)

1. User drops file in `raw/<category>/` **or** provides URL. If URL: fetch, convert to markdown, save to appropriate `raw/` subfolder with a slugged filename. Update `raw/INDEX.md`.
2. Read the source end-to-end.
3. Brief with user: 2–3 key takeaways, anything surprising, anything that contradicts existing wiki claims.
4. Create/update `sources/<citation-key>.md` with full frontmatter (including `trust-tier`).
5. Identify every affected page (coaches, schools, techniques, drills, systems, hubs). A single rich source typically touches 10–15 pages.
6. For each affected page:
   - Add to `sources` frontmatter
   - Add inline `[citation-key]` where claims are supported (per citation policy)
   - Add a `## Contradictions` callout if this source disagrees with an existing claim
   - Create stub pages for any new entity (new coach, new drill, new technique) introduced
7. Update `index.md` to reflect new pages and re-categorizations.
8. Append to `log.md`: `## [YYYY-MM-DD] ingest | <title> | touched N pages`.
9. Clear any now-resolved entries from `unsourced-queue.md`.

### 5.2 Query (user asks a question)

1. Read `index.md`; identify candidate pages.
2. Read those pages.
3. If answer requires info outside wiki: offer to research + ingest, OR answer best-effort with `[unsourced]` tags queued.
4. Synthesize answer with citations (honoring heavy/light citation policy).
5. If answer is substantive (a comparison, practice plan, synthesis) → **offer to file as a new wiki page** so explorations compound.
6. Append to `log.md`: `## [YYYY-MM-DD] query | <short description>`.

### 5.3 Lint (periodic health-check)

Run on demand. Produces a findings report; user triages fixes.

1. **Orphan scan** — pages with no inbound links
2. **Cross-link invariant check** — violations of the 6 rules in §3.5
3. **Unsourced queue triage** — prioritize replacing highest-impact `[unsourced]` tags
4. **Stale-claim scan** — methodology pages whose newest source is > 5 years old
5. **Frontmatter validation** — required fields, valid enums, resolvable citation-keys
6. **Concept-gap detection** — terms mentioned across ≥3 pages with no dedicated page
7. **Contradiction reconciliation** — review outstanding `## Contradictions` callouts with user
8. Report; user decides what to fix now vs. queue

### 5.4 Research (bootstrap + gap-filling)

**Priority order for a given topic:**

1. Check `raw/` first — we may already have it
2. Tier 1 sources (books, USAV, peer-reviewed research)
3. Tier 2 (AOC, GMS, The Net Live, VolleyballMag, FIVB, JVA)
4. Tier 3 (Instagram, YouTube non-credentialed, forums — corroborate with Tier 1/2 before citing)

**Per-source fidelity rules:**

- **Books:** summarize with chapter/page refs. If PDF owned by user, save to `raw/books/`. Otherwise `raw/books/notes-<slug>.md` summary built from fair-use sources (previews, interviews, reviews).
- **YouTube:** fetch captions → save to `raw/transcripts/<slug>.md` with URL + key timestamps. If no captions, summarize from description/clips and tag `[transcript-unavailable]`.
- **Instagram:** screenshot + caption text + account handle + post date to `raw/instagram/<slug>.md`. Treat as ephemeral.
- **Articles:** Obsidian-Web-Clipper-style markdown to `raw/articles/<slug>.md`.

**Conflict handling:** document both views, attribute, don't resolve (per §1.3 positioning and §4.4 anti-patterns).

---

## 6. Bootstrap research sprint plan

### 6.1 Cadence

**One continuous sprint** across 6 waves. The user checks in at 4 checkpoints. Session count depends on how rich the research gets, but the goal is a "launch version" where the wiki feels real from day one.

### 6.2 Deliverable targets (bootstrap done = all met)

| Category | Target |
|----------|-------:|
| Operational files (`index.md`, `log.md`, `SCHEMA.md`, `unsourced-queue.md`, root `CLAUDE.md`) | 5 |
| Hub + age-lens pages (root-level singular pages) | 12 |
| Coach profiles | 12–15 |
| School / philosophy pages | 8–10 |
| Technique pages | 25–30 |
| Position pages | 6 |
| Systems pages | 15–20 |
| Drills (seed library) | 50 |
| Source pages | 30–50 |
| **Total** | **~160–200** |

### 6.3 Wave structure

**Wave 0 — Foundation** *(one chunk at start)*
Write `SCHEMA.md`, root `CLAUDE.md`, full folder structure, empty operational files, page templates. No content yet, but the playbook is in place.

**Wave 1 — Source research & `raw/` library population**
Deep web research pass. Gather + ingest to `raw/`:
- USA Volleyball public coaching resources (CAP materials, coaching toolbox, age-appropriate guidance)
- Karch Kiraly — articles, interviews, USAV videos, clinic transcripts; user-owned PDFs if available
- Hugh McCutcheon — publicly available *Thinking Volleyball* material, USA+Minnesota coaching content
- Gold Medal Squared — Carl McGown writing, GMS webinar transcripts, public articles
- Art of Coaching Volleyball — article catalog, podcast transcripts, video topic inventory
- Japanese training — Nakagaichi writings, Daimatsu historical, V.League coaches, JVA materials, modern Japanese technical articles
- Additional major coaches — Russ Rose, John Dunning, Mike Hebert, Terry Liskevych, John Speraw, Mary Wise
- Instagram + YouTube — verified coach/athlete accounts (screenshots + transcripts for Tier 3 material)

Output: 30–50 source pages + `raw/` populated.

**Wave 2 — Reference frame (coaches + schools)**
Build all coach profiles and school/philosophy pages from Wave 1 sources. Heavy citations throughout.

**Wave 3 — Technical core (techniques + positions + systems)**
Build technique, position, systems-detail pages. Each pulls multiple `schools-perspectives` where topics diverge.

**Wave 4 — Operational spine (practice-planning + drills)**
Practice-planning hub, season-planning hub, drill library (50-drill seed), practice-plan templates. Drill pages heavily frontmatter-tagged for Dataview filtering.

**Wave 5 — Context layer (mental + physical + match-prep + rules + recruiting + age-lenses)**
Fill remaining hubs and all three age-lens pages (14U, HS, college).

**Wave 6 — Index, lint, handoff**
Full `index.md` catalog, first lint pass, `unsourced-queue.md` seeded, `log.md` entries for all waves, session-end summary.

### 6.4 Checkpoints (user review gates)

- **End of Wave 0:** user reviews `SCHEMA.md` before content starts
- **End of Wave 1:** user reviews the source library — are the right coaches/schools represented?
- **End of Wave 2:** user reviews coach/school profiles for positioning accuracy (highest fingerprint content)
- **End of Wave 6:** user reviews the full wiki

### 6.5 Copyright caveats

- The agent will **not** source or download copyrighted books without rights. The user can legally drop owned PDFs into `raw/books/` and those become fair-use-summarizable.
- Publisher previews, author interviews, clinic recordings, book reviews, and course syllabi provide extensive legal material to cite against even when full book texts are unavailable.
- `raw/transcripts/` materials should capture source URL + key timestamps for every YouTube/podcast excerpt.
- `raw/instagram/` materials are treated as ephemeral and always snapshot before citing.

---

## 7. Success criteria

### 7.1 Bootstrap "done" checklist (acceptance)

Bootstrap is complete when all of these are true:

- [ ] §6.2 deliverable targets met (~160–200 pages across the taxonomy)
- [ ] `SCHEMA.md`, `CLAUDE.md`, `index.md`, `log.md`, `unsourced-queue.md` all populated
- [ ] Every page's frontmatter validates against its type contract
- [ ] Cross-link invariants (§3.5) all hold
- [ ] Zero orphan pages
- [ ] Every wiki claim has either a citation or an `[unsourced]` tag
- [ ] `unsourced-queue.md` lists every `[unsourced]` claim
- [ ] `log.md` has an entry for Waves 0–6 with touched-page counts
- [ ] Obsidian opens `wiki/` cleanly — wikilinks resolve, graph view is rich, no broken-link reports
- [ ] `sources/` has ≥30 pages, and `raw/` has real material behind each (no phantom citations)

### 7.2 End-of-bootstrap scenario tests

Three real queries that validate the wiki is useful — the day after bootstrap:

1. **"Build me a 90-minute 14U practice focused on serve-receive, skill phase, with both GMS and Japanese perspectives represented."**
   Expected: a plan citing ≥5 drill pages, references to `gold-medal-squared.md` and `japanese-training.md`, respects 14U age-lens guidance.

2. **"How does Karch teach blocking vs. how GMS teaches it?"**
   Expected: a comparison pulling from `coaches/karch-kiraly.md`, `schools/gold-medal-squared.md`, `techniques/blocking-footwork.md`, `systems-detail/read-blocking.md`, `systems-detail/swing-blocking.md` — with citations.

3. **"What's the evidence for random vs. blocked practice in volleyball skill acquisition?"**
   Expected: synthesis from `schools/ecological-dynamics.md`, relevant motor-learning research in `raw/research/`, and coaching articles citing the literature.

Any test that returns thin or uncited answers → gap goes to `unsourced-queue.md`, Wave 1 gets topped up.

### 7.3 Living-wiki success signals (3–6 months out)

- Ingesting a new source reliably touches 10+ pages (the maintenance graph is working)
- Questions return cited wiki answers rather than ad-hoc web synthesis
- Lint surfaces actual gaps/contradictions, not false positives
- User reaches for the wiki before Google
- Wiki gets richer every use, not staler

### 7.4 Explicit non-goals (YAGNI)

Bootstrap does **not** include:

- Custom CLI tooling (qmd, lint scripts) — defer until scale demands; SCHEMA.md + Obsidian Dataview cover early needs
- Beach volleyball
- Coach certification study guides
- A web frontend — Obsidian is the reader
- Automated ingestion pipelines — ingest stays conversational, agent-driven, one source at a time
- Player/team management or stats tracking — this is a coaching knowledge wiki, not a team CMS

---

## 8. Open items & acknowledged caveats

1. **User-owned book PDFs:** the user will decide case-by-case whether to drop owned book PDFs into `raw/books/`. Bootstrap proceeds with fair-use citation methods regardless; any owned PDFs raise depth where provided.
2. **Instagram/YouTube snapshot dependence:** material found live may move or disappear. Wave 1 captures snapshots, but some Tier 3 citations will inevitably rot over time and require re-sourcing in future lint passes.
3. **Japanese-language sources:** primary Japanese-language material (JVA, Japanese coaching texts) may require translation during ingest. Bootstrap prioritizes English-language writing about Japanese training methodology; native-language deep dives are a later expansion.
4. **Version control:** the project directory is not currently a git repo (per environment report). Recommend initializing `git` at `vba/bible/` before bootstrap begins so Waves 0–6 produce visible commit history. This is a bootstrap-prep step for the implementation plan.

---

## 9. Next step

Hand off to the writing-plans skill to produce a wave-by-wave implementation plan with concrete task lists, acceptance checks per wave, and checkpoint prompts for user review.
