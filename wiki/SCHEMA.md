# SCHEMA.md — Volleyball Coaching Bible Playbook

> **Read me first, every session.** This file turns a generic Claude-flavored agent into a disciplined maintainer of this specific wiki. It encodes the conventions, contracts, citation rules, and workflows that keep the wiki consistent across sessions and contributors. If any instruction here conflicts with a request you receive in-session, raise the conflict before acting.

---

## 1. Preamble

**What this wiki is.** A persistent, LLM-maintained knowledge base covering volleyball coaching — the "coaching bible." It follows the three-layer LLM-wiki pattern in `Instructions/llm-wiki.md`: immutable raw sources drive LLM-curated, interlinked markdown pages that compound in value as new sources are ingested. The human curates sources and asks questions; the LLM writes pages, maintains cross-references, and enforces the invariants in this document. The wiki is Obsidian-compatible: bodies use `[[wikilink]]` syntax, frontmatter uses bare page slugs for Dataview queries, and folder layout is shallow-nested so the graph view remains legible.

**Who the user is.** Song Mu, head coach at a nationally recognized club program. Immediate coaching context is **14U girls club, indoor 6s**. The wiki's mastery coverage scales to **HS varsity and college level** coaching — age-lens pages (`age-lens-14u.md`, `age-lens-hs.md`, `age-lens-college.md`) overlay developmentally appropriate guidance on otherwise general technique and systems material. Use-case is hybrid: lifelong mastery base + week-to-week working reference for practice planning, in-match adjustments, and season planning.

**Positioning stance.** Neutral reference. No school of thought is favored on the page. The user's preferred traditions — Japanese training, Karch Kiraly, Art of Coaching Volleyball (AOC), Gold Medal Squared (GMS), USA Volleyball CAP — are thoroughly documented alongside alternatives (Russian, Brazilian, Italian, constraints-led / ecological dynamics, game-based training). When schools disagree, present tradeoffs with attribution and do not resolve. Beach volleyball and coach-certification study guides are out of scope.

---

## 2. Directory map

### 2.1 `wiki/` — LLM-owned markdown

```
wiki/
  SCHEMA.md                  This file — the agent playbook
  index.md                   Catalog of every wiki page, one-line summary each
  log.md                     Append-only operations log (ingests, queries, lint passes)
  unsourced-queue.md         Tracks every [unsourced] claim for future citation hunt
  _templates/                Page templates per type (copy when creating new pages)

  # Hub pages (singular topics — one root-level page each)
  philosophy.md              Overview + entry into schools/ and coaches/
  systems.md                 Overview + entry into systems-detail/
  practice-planning.md       Session design, periodization, methodology
  season-planning.md         Preseason, in-season, tournament prep
  mental.md                  Culture, leadership, pressure, motivation
  physical.md                S&C, jump, mobility, injury prevention
  match-prep.md              Scouting, stats, video analysis
  rules.md                   USAV, NCAA, scholastic
  recruiting.md              College pathway
  age-lens-14u.md            14U-specific overlays on technique, systems, practice
  age-lens-hs.md             HS varsity lens
  age-lens-college.md        College lens

  # High-volume categories (one subfolder each)
  coaches/                   One page per notable coach
  schools/                   One page per philosophy / school of thought
  techniques/                Per-skill + subskill pages (e.g., passing-forearm.md)
  positions/                 Setter, outside, middle, opposite, libero, DS
  systems-detail/            Specific systems (5-1, 6-2, rotational defenses, etc.)
  drills/                    Individual drill pages, heavily frontmatter-tagged
  sources/                   One page per major source (book, video series, article)
```

**Obsidian plugin requirement:** skill-hub, age-lens, position, and planning pages include `dataview` code blocks that render drill/source catalogs from frontmatter. Install the [Dataview](https://github.com/blacksmithgu/obsidian-dataview) community plugin in Obsidian to render them; without the plugin the queries show as markdown source (harmless but not useful).

### 2.2 `raw/` — immutable source material (LLM reads, never edits)

```
raw/
  INDEX.md                   One-line catalog of every raw file
  books/                     PDFs of owned books + per-book notes files when PDFs unavailable
  articles/                  Blog posts, features, interviews — web-clipped markdown
  transcripts/               YouTube/podcast transcripts with URLs + timestamps
  instagram/                 Screenshots + captions (IG is ephemeral; snapshot it)
  usav/                      USA Volleyball curriculum, toolbox PDFs, rule docs
  research/                  Peer-reviewed papers on motor learning, skill acquisition, ecological dynamics
  images/                    Figures, court diagrams, photos referenced from wiki pages
```

**Copyright rule.** The agent will not source or download copyrighted books without rights. The user can legally drop owned PDFs into `raw/books/` and those become fair-use-summarizable. Otherwise, cite books using publisher previews, author interviews, clinic recordings, reviews, and course syllabi — all legal fair-use material.

---

## 3. Page types reference

Ten page types. Basenames are globally unique, so Obsidian `[[wikilinks]]` resolve by basename alone.

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
| Practice plan | `practice-plans/` | `<level>-<duration>-<label>.md` | `14u-90min-serve-receive.md` |

### 3.1 Hub pages
- **Folder / filename:** `wiki/<topic>.md`
- **Required frontmatter:** `type: hub`, `area`, `subtopics`
- **Required body sections:** `## Overview`, `## Major subtopics`, `## Schools of thought`, `## Getting started`, `## Related areas`, `## Sources`
- **Target length:** 600–1200 words. Navigational, not expository.
- **Citation weight:** Light (hub pages are entry points; claims belong on subordinate pages).
- **Cross-link rules:** Every hub links to its high-volume subfolder(s) and to at least one related hub. Orphan hubs fail lint.

### 3.2 Coach profiles
- **Folder / filename:** `coaches/<firstname-lastname>.md` (kebab-case; ASCII only)
- **Required frontmatter:** `type: coach`, `name`, `country`, `era`, `roles`, `schools` (≥1), `sources` (≥1). Optional: `tags`.
- **Required body sections:** `## Overview`, `## Coaching career`, `## Core teaching principles`, `## Contributions to the game`, `## Quotes & representative passages`, `## Sources`
- **Target length:** ~1500 words.
- **Citation weight:** Heavy. Inline `[citation-key]` after every non-generic claim in core-principles, contributions, and quotes.
- **Cross-link rules:** Must link ≥1 `schools/` page (via `schools:` frontmatter) and ≥1 `sources/` page (via `sources:` frontmatter). Body should wikilink to related coaches, techniques this coach is known for, and any schools featured.

### 3.3 School / philosophy pages
- **Folder / filename:** `schools/<slug>.md`
- **Required frontmatter:** `type: school`, `name`, `origin`, `founders`, `core-principles`, `associated-coaches`, `sources` (≥1). Optional: `related-schools`.
- **Required body sections:** `## Overview`, `## Core principles`, `## Methodology`, `## Notable practitioners`, `## Contrasts with other schools`, `## Critiques and limitations`, `## Sources`
- **Target length:** 2000–2500 words (these are among the longest, most heavily cited pages).
- **Citation weight:** Heavy. Inline `[citation-key]` for each core principle and each contrast claim.
- **Cross-link rules:** `associated-coaches` must match each listed coach's `schools:` field (bidirectional — enforced by lint). `Contrasts with other schools` must wikilink to the contrasted school page and attribute the contrast to a source (no handwaving "some coaches say").

### 3.4 Technique pages
- **Folder / filename:** `techniques/<skill>-<subskill>.md` (e.g., `passing-forearm.md`, `blocking-read.md`)
- **Required frontmatter:** `type: technique`, `skill` (enum, see §4), `subskill`, `positions`, `related-drills`, `sources`. Optional: `related-techniques`, `schools-perspectives` (**required if contested** — ≥2 entries).
- **Required body sections:** `## Overview`, `## Teaching progressions`, `## Common errors`, `## Schools-perspectives` (include only if topic is contested), `## Related drills`, `## Sources`
- **Target length:** 800–1500 words.
- **Citation weight:** Light. No inline citations in progressions/errors; `## Sources` at bottom.
- **Cross-link rules:** Every `related-drills` slug must correspond to a real drill page (or be stubbed). Every `positions` slug must be valid. If `schools-perspectives` is present, each school referenced must have a `schools/` page.

### 3.5 Position pages
- **Folder / filename:** `positions/<position>.md` (enum: `setter`, `outside-hitter`, `middle-blocker`, `opposite`, `libero`, `defensive-specialist`)
- **Required frontmatter:** `type: position`, `position`, `role`, `physical-profile`, `key-skills`, `common-drills`. Optional: `related-coaches`.
- **Required body sections:** `## Role and responsibilities`, `## Physical profile`, `## Key skills`, `## Common drills`, `## Position-specific coaching points`, `## Progression by level`, `## Sources`
- **Target length:** 800–1200 words.
- **Citation weight:** Light.
- **Cross-link rules:** `key-skills` links to technique pages. `common-drills` links to drill pages. `## Progression by level` must wikilink to `age-lens-14u.md`, `age-lens-hs.md`, `age-lens-college.md` as relevant.

### 3.6 System pages
- **Folder / filename:** `systems-detail/<category>-<name>.md` (e.g., `offense-5-1.md`, `defense-rotation.md`)
- **Required frontmatter:** `type: system`, `category` (enum, see §4), `name`, `age-appropriateness`, `complexity` (enum), `when-to-use`, `alternatives`, `sources`.
- **Required body sections:** `## Overview`, `## Personnel requirements`, `## Diagram or text description of alignment`, `## Strengths`, `## Weaknesses`, `## When to use / when not to use`, `## Alternatives and adjustments`, `## Sources`
- **Target length:** 1000–1500 words.
- **Citation weight:** Light.
- **Cross-link rules:** `alternatives` must reference real system slugs (or be stubbed). `age-appropriateness` must only include recognized levels. Diagram images live in `raw/images/`.

### 3.7 Drill pages
- **Folder / filename:** `drills/<slug>.md` (descriptive kebab-case; e.g., `butterfly-passing.md`, `6-on-6-wash-drill.md`)
- **Required frontmatter:** `type: drill`, `name`, `primary-skill` (enum), `techniques` (≥1), `phase` (enum), `team-size-min`, `team-size-max`, `duration-min`, `levels`, `equipment`, `sources` (≥1). Optional: `secondary-skills`, `video-url`, `variations`.
- **Required body sections:** `## Setup`, `## Execution`, `## Coaching points`, `## Variations`, `## Adaptations by level`, `## Sources`
- **Target length:** ~300 words (drills are operational; keep tight).
- **Citation weight:** Light.
- **Cross-link rules:** Every drill must link ≥1 source page AND ≥1 technique page (enforced by lint rule §5 item 1). Variations must link to other drill pages if they exist as separate pages.

### 3.8 Source pages
- **Folder / filename:** `sources/<citation-key>.md` where `<citation-key>` follows the convention below.
- **Citation-key convention:**
  - Books / articles / interviews: `<author-lastname>-<year>-<short-slug>` (e.g., `kiraly-1997-championship-volleyball`)
  - Organizational: `<org>-<year>-<slug>` (e.g., `usav-2024-coaching-education`)
  - Social posts: `<platform>-<handle>-<YYYYMMDD>` (e.g., `ig-usavolleyball-20260315`)
  - YouTube (non-coach-authored): `yt-<channel-slug>-<YYYYMMDD>-<slug>`
- **Required frontmatter:** `type: source`, `source-type` (enum), `title`, `author`, `year`, `citation-key` (must match filename), `raw-file` (path under `raw/`), `topics`, `featured-coaches`, `schools`, `trust-tier` (enum 1/2/3). Optional: `url`.
- **Required body sections:** `## Summary`, `## Key claims / ideas`, `## Topics covered`, `## Where it's cited`, `## Access`
- **Target length:** 400–800 words.
- **Citation weight:** N/A (sources are the targets of citations, not citers).
- **Cross-link rules:** `raw-file` must point to an existing file in `raw/`. `featured-coaches` slugs must eventually resolve to coach pages (forward references allowed during bootstrap; must resolve after Wave 2). `## Where it's cited` is updated as wiki pages add this source.

### 3.9 Age-lens pages
- **Folder / filename:** `wiki/age-lens-<label>.md` (e.g., `age-lens-14u.md`). Labels: `14u`, `hs`, `college`.
- **Required frontmatter:** `type: age-lens`, `label`, `scope`, `emphasis`, `age-ceilings`, `sources`.
- **Required body sections:** `## Scope`, `## Development priorities`, `## Appropriate techniques & systems`, `## NOT appropriate at this level`, `## Practice design adaptations`, `## Season-planning adaptations`, `## Sources`
- **Target length:** 1200–1800 words.
- **Citation weight:** Heavy (age-appropriateness claims must be sourced — USAV age-appropriate guidelines are the strongest anchor).
- **Cross-link rules:** `## Appropriate techniques & systems` must wikilink to specific technique/system pages. `## NOT appropriate at this level` must name specific systems/techniques with reasons attributed to sources.

### 3.10 Practice-plan pages

- **Folder / filename:** `wiki/practice-plans/<level>-<duration>-<label>.md`. Label is a descriptive kebab-case slug — typically the focus, or the season context when more identifying than the focus. Frontmatter carries the structured enums.
- **Required frontmatter:** `type: practice-plan`, `level`, `duration-min`, `focus`, `season-phase`, `drills` (≥3 required — each must resolve to a drill page), `sources` (≥1 required).
- **Required body sections:** `## Context`, `## Learning objectives`, `## Time blocks` (with sub-sections per phase, each naming drills as wikilinks with time allocations), `## Coaching cues`, `## Variations`, `## Adaptations by level`, `## Sources`.
- **Target length:** 500–800 words.
- **Citation weight:** Light. No inline citations; `## Sources` at bottom.
- **Cross-link rules:** Every `drills:` slug must correspond to a real drill page. Plans SHOULD wikilink to the applicable age-lens page.

---

## 4. Frontmatter contracts

All pages open with YAML frontmatter. **Link-field convention:** link fields store bare page slugs (the filename without `.md`). In-body references use `[[wikilink]]` form. Lint validates both.

### Hub
```yaml
---
type: hub
area: practice-planning
subtopics: [periodization, session-design, microcycle-planning, practice-ratios]
---
```

### Coach profile
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

### School / philosophy
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

### Technique
```yaml
---
type: technique
skill: passing                                         # enum (see glossary)
subskill: forearm-pass
positions: [libero, defensive-specialist, outside-hitter]
related-drills: [butterfly-passing, pepper]
related-techniques: [defense-platform]
schools-perspectives:                                  # ≥2 required if topic is contested
  gms: "Platform angle primary, footwork secondary"
  aoc: "Read first, platform second"
  japanese: "Midline emphasis, quick reset"
sources: [kiraly-1997-championship-volleyball]
---
```

### Position
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

### System
```yaml
---
type: system
category: offense                                      # enum (see glossary)
name: 5-1
age-appropriateness: [14u, hs, college, professional]
complexity: medium                                     # enum (see glossary)
when-to-use: "When one setter is clearly better than alternatives; gives setter-hitter matchup consistency"
alternatives: [offense-6-2, offense-4-2]
sources: [dunning-2013-volleyball-systems]
---
```

### Drill
```yaml
---
type: drill
name: Butterfly Passing
primary-skill: passing                                 # enum matches technique.skill
secondary-skills: [serving, communication]
techniques: [passing-forearm, passing-overhead]        # ≥1 required
phase: skill                                           # enum (see glossary)
team-size-min: 6
team-size-max: 12
duration-min: 10
levels: [14u, hs, college]
equipment: [ball-cart]
sources: [gms-2022-warmup-webinar]                     # ≥1 required
video-url: https://...                                 # optional
variations: [butterfly-serve-receive, butterfly-defense]
---
```

### Source
```yaml
---
type: source
source-type: book                                      # enum (see glossary)
title: "Championship Volleyball"
author: "Karch Kiraly"
year: 1997
citation-key: kiraly-1997-championship-volleyball
raw-file: raw/books/kiraly-championship-volleyball.pdf
url: https://...                                       # optional
topics: [technique, systems, mental]
featured-coaches: [karch-kiraly]
schools: [usa-volleyball-cap]
trust-tier: 1                                          # enum 1|2|3
---
```

### Age-lens
```yaml
---
type: age-lens
label: 14u
scope: "14-and-under club-level indoor girls"
emphasis: [fundamentals, ball-control, serve-receive-exposure, tempo-simplicity]
age-ceilings:
  - "Full swing-blocking systems"
  - "Complex 6-2 for non-setter outside hitters"
sources: [usav-age-appropriate-guidelines]
---
```

### Practice-plan
---
type: practice-plan
level: 14u                          # enum: 14u | hs | college
duration-min: 90
focus: serve-receive                # enum (see glossary)
season-phase: mid-season            # enum (see glossary)
drills: [butterfly-passing, pass-set-hit, cooperative-25-goal]   # ≥3 required
sources: [...]                      # ≥1 required
---

### Enum glossary

- `phase ∈ {warm-up, skill, strategic, competition, conditioning}`
- `source-type ∈ {book, video-series, podcast, article, interview, clinic, social-post}`
- `trust-tier ∈ {1, 2, 3}`
- `skill ∈ {passing, setting, hitting, blocking, serving, defense, transition}`
- `system.category ∈ {offense, defense, serve-receive, blocking, transition}`
- `complexity ∈ {low, medium, high}`
- `levels / age-appropriateness ∈ {14u, hs, college, professional}`
- `position ∈ {setter, outside-hitter, middle-blocker, opposite, libero, defensive-specialist}`
- `focus ∈ {passing, setting, hitting, blocking, serving, defense, transition, serve-receive, out-of-system, match-prep, player-development, composite}`
- `season-phase ∈ {preseason, mid-season, pre-tournament, taper, tryout, postseason, match-day}`
- `level ∈ {14u, hs, college}` (same as `levels` array-valued counterpart on drill pages)

---

## 5. Citation rules

### Heavy vs. light split

| Page type | Citation weight | Format |
|-----------|-----------------|--------|
| Philosophy hub, schools, coach profiles, age-lenses, and methodology sections of any page | **Heavy** | Inline `[citation-key]` after each non-generic claim, plus `## Sources` (or `## Bibliography`) section listing all cited source pages via `[[wikilink]]` |
| Technique, drill, position, system pages | **Light** | No inline citations in body. `## Sources` section at bottom listing linked source pages only |
| Hub pages (navigational) | Light | Claims that must be made should be sourced; otherwise defer to subordinate pages |

### Inline citation format

`[citation-key]` where `citation-key` matches the `citation-key` field of a `sources/` page. **Unresolvable citation-keys fail lint.** Example:

> Karch Kiraly emphasizes that reading the hitter's approach precedes platform formation in passing [kiraly-1997-championship-volleyball]. Gold Medal Squared frames the same sequence as "read → move → play" [gms-2022-warmup-webinar].

### Source-page-first rule

**Never cite a source page that doesn't exist.** Before you write `[kiraly-2022-aoc-interview]` anywhere in the wiki, create `wiki/sources/kiraly-2022-aoc-interview.md`. Ingest workflow (§8.1) enforces this sequence.

### Unsourced claims

Any claim that cannot be backed by a source gets an inline `[unsourced]` tag AND an entry in `wiki/unsourced-queue.md`. The queue entry must include:
- The page path and the exact sentence containing the claim
- Why it's unsourced (couldn't find Tier 1/2 evidence, contested beyond reviewed material, personal observation, etc.)
- A research hypothesis — where to look to source it later (specific book chapter, interview, paper, author to track down)
- The date added

`[unsourced]` exists to keep intellectual honesty mechanical. Do not hide unsourced claims by omitting them — write them with the tag, queue them, and let lint surface them for future ingest sessions.

---

## 6. Cross-link invariants (lint-enforced)

1. Every drill page must link to ≥1 source page AND ≥1 technique page (via `sources:` and `techniques:` frontmatter).
2. Every coach profile must link to ≥1 school page AND ≥1 source page (via `schools:` and `sources:` frontmatter).
3. Every technique page where schools genuinely disagree must have ≥2 entries in `schools-perspectives` frontmatter AND a `## Schools-perspectives` body section.
4. Every source page must exist before being cited anywhere in the wiki.
5. No page may be orphaned (zero inbound wikilinks) — every page is reachable from a hub or peer.
6. Every inline `[citation-key]` must resolve to a source page's `citation-key` field.

**Enforcement:** the agent enforces these pre-commit on any page it writes or modifies. The lint workflow (§8.3) runs a periodic full-repo scan and reports violations.

---

## 7. Source trust tiers

Priority-ordered; cite accordingly.

**Tier 1 — Primary / authoritative. Cite freely.**
- Published books by credentialed coaches (Kiraly, McCutcheon, Hebert, Liskevych, Dunning, Rose, etc.)
- USA Volleyball official resources (CAP, coaching toolbox, age-appropriate guidance, IMPACT course materials)
- Peer-reviewed research on motor learning, skill acquisition, sports science, ecological dynamics

**Tier 2 — Trusted secondary. Cite with affiliation noted.**
- Art of Coaching Volleyball (AOC) content
- Gold Medal Squared (GMS) materials
- The Net Live
- VolleyballMag
- Established federation sites (FIVB, JVA, CEV)
- Clinic recordings from major conventions (AVCA Convention, USAV High Performance Coach Clinic, JVA Challenge)

**Tier 3 — Corroborate before citing. Attribute clearly; use only if supported by a Tier 1/2 source OR coming from a verified coach/athlete account.**
- Instagram, TikTok (verified coach/athlete accounts only)
- YouTube non-credentialed channels
- Forum threads, uncredited blogs

Every source page's frontmatter has `trust-tier: 1|2|3`. Lint flags any claim in the wiki whose only supporting citation is Tier 3 without corroboration.

---

## 8. Voice & style guide

- **Person:** second-person ("you") addressing the reader coach.
- **Tense:** present.
- **Precision:** specific over vague. "90% of 14U teams run 6-2 or 4-2" > "most teams run 6-2 or 4-2." When numbers aren't defensible, prefer concrete descriptors ("common at the club level") over hedging ("might be").
- **Age-appropriateness flags:** when technique or systems guidance assumes a level, say so explicitly. Link to the appropriate age-lens page when introducing level-dependent guidance.
- **Medical / S&C disclaimers:** never give medical advice; always defer to qualified professionals (athletic trainers, CSCSs, physicians) on injury, nutrition, or programming specifics outside general coaching purview.
- **Neutrality on school disagreements:** present both views, attribute each to a school and a source, do not resolve. Use the `## Schools-perspectives` mechanism on technique pages for this.
- **Voice:** direct and coach-to-coach. Assume the reader is a coach, not a beginner player. Skip introductory fluff.
- **Term consistency:** define a term once (typically on the first hub that introduces it) and wikilink to that page everywhere else rather than redefining.

---

## 9. Anti-patterns (explicit "don'ts")

- **Never fabricate citations.** If a claim can't be sourced, tag `[unsourced]` and queue it. Making up author/year/title is a cardinal violation.
- **Never pick sides** on school disagreements. Present tradeoffs with attribution.
- **Never duplicate content** across pages — cross-link instead. If two pages are saying the same thing, the shared material belongs on a third page that both link to.
- **Never write content in `index.md` or `log.md`.** `index.md` is a catalog (one-line summaries only); `log.md` is chronological operations only. Substantive content goes in topical pages.
- **Never cite a source page that doesn't exist.** Create the source page first, then cite it.
- **Never write inline citations on light-citation pages.** Technique/drill/position/system pages get `## Sources` at bottom only.
- **Never invent coach or school slugs.** If you're about to link `[[some-new-coach]]` and that page doesn't exist, either create a stub for it or remove the wikilink. Dangling wikilinks fail lint.
- **Never modify files under `raw/`.** Those are immutable. Notes, summaries, and interpretations belong on `wiki/` pages.
- **Never collapse contested positions into a single "consensus view."** When sources disagree, the disagreement IS the content.

---

## 10. Session-start checklist

Every new session runs this 4-step drill before any read or write operation:

1. **Read this file top-to-bottom** (`wiki/SCHEMA.md`). Don't skim — the invariants matter.
2. **Read `wiki/index.md`** to see the current catalog of pages.
3. **Tail the last 20 lines of `wiki/log.md`** to see recent activity:
   ```bash
   tail -n 20 wiki/log.md
   ```
4. **If working on a specific area, read that area's hub page first** before touching any sub-page. Hubs orient the agent to the area's conventions and cross-links.

---

## Workflows

### 8.1 Ingest (new source → wiki)

1. User drops file in `raw/<category>/` **or** provides URL. If URL: fetch, convert to markdown, save to appropriate `raw/` subfolder with a slugged filename. Update `raw/INDEX.md` with one-line entry.
2. Read the source end-to-end.
3. Brief the user: 2–3 key takeaways, anything surprising, anything that contradicts existing wiki claims.
4. Create or update `sources/<citation-key>.md` with full frontmatter (including `trust-tier`). Populate Summary and Key claims sections.
5. Identify every affected page (coaches, schools, techniques, drills, systems, hubs). A single rich source typically touches 10–15 pages.
6. For each affected page:
   - Add the new citation-key to the page's `sources:` frontmatter
   - Add inline `[citation-key]` where claims are supported (per citation weight policy)
   - Add a `## Contradictions` callout if this source disagrees with an existing claim — present both, attribute, do not resolve
   - Create stub pages for any new entity (coach, drill, technique, system) introduced by the source
7. Update `wiki/index.md` to reflect new pages and any re-categorizations.
8. Append to `wiki/log.md`: `## [YYYY-MM-DD] ingest | <title> | touched N pages`.
9. Clear any now-resolved entries from `wiki/unsourced-queue.md`.
10. Commit with message `ingest: <title> · <citation-key> · touched <N> pages`.

### 8.2 Query (user asks a question)

1. Read `wiki/index.md`; identify candidate pages.
2. Read those pages in full (don't skim frontmatter — bodies often hold the nuance).
3. If the answer requires information outside the wiki, either:
   - Offer to research + ingest fresh sources before answering, OR
   - Answer best-effort with explicit `[unsourced]` tags queued for future backfill.
4. Synthesize the answer with citations honoring the heavy/light weighting rule for the originating page type.
5. If the answer is substantive (a comparison, practice plan, synthesis, new analysis) → **offer to file it as a new wiki page** so the exploration compounds instead of vanishing into chat history.
6. Append to `wiki/log.md`: `## [YYYY-MM-DD] query | <short description>`.

### 8.3 Lint (periodic health-check)

Run on demand (the user says "lint the wiki" or similar). Produces a findings report; user triages fixes.

1. **Orphan scan** — list pages with zero inbound wikilinks.
2. **Cross-link invariant check** — enumerate violations of the 6 rules in §6.
3. **Unsourced queue triage** — highlight entries with the highest wiki-coverage impact (i.e., claims cited on the most pages).
4. **Stale-claim scan** — methodology and technique pages whose newest cited source is more than 5 years old.
5. **Frontmatter validation** — every required field present, every enum value valid, every `citation-key` resolvable.
6. **Concept-gap detection** — terms mentioned on ≥3 pages with no dedicated page of their own.
7. **Contradiction reconciliation** — review outstanding `## Contradictions` callouts with user; file a follow-up query if the field has evolved since the callout was written.
8. Report findings; the user decides what to fix now vs. what to queue.

### 8.4 Research (bootstrap + gap-filling)

**Priority order for a given topic:**

1. Check `raw/` first — we may already have it.
2. Tier 1 sources (books, USAV, peer-reviewed research).
3. Tier 2 (AOC, GMS, The Net Live, VolleyballMag, FIVB, JVA).
4. Tier 3 (Instagram, YouTube non-credentialed, forums — corroborate with Tier 1/2 before citing).

**Per-source fidelity rules:**

- **Books:** summarize with chapter and page refs. If PDF owned by user is present in `raw/books/`, extract more liberally (fair use). Otherwise `raw/books/notes-<slug>.md` summary built from fair-use material (previews, author interviews, reviews, syllabi).
- **YouTube:** fetch captions when available → save to `raw/transcripts/<slug>.md` with URL plus key timestamps. When captions are unavailable, summarize from description/clips and tag `[transcript-unavailable]`.
- **Instagram:** screenshot + caption text + account handle + post date to `raw/instagram/<slug>.md`. Treat as ephemeral; snapshot always, because IG posts disappear.
- **Articles:** Obsidian-Web-Clipper-style markdown to `raw/articles/<slug>.md` with source URL and fetched-date in frontmatter.

**Conflict handling:** document both views, attribute each to its source and school, don't resolve. Neutrality is a hard rule (see §9 anti-patterns).
