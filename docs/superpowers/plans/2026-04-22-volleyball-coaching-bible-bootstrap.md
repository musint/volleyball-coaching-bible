# Volleyball Coaching Bible — Bootstrap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bootstrap a comprehensive, Obsidian-compatible LLM wiki covering volleyball coaching — the "coaching bible" — in one continuous sprint across 6 waves, producing ~160–200 interlinked markdown pages with proper sourcing.

**Architecture:** Three-layer LLM wiki: `raw/` (immutable sources) + `wiki/` (LLM-maintained markdown) + `SCHEMA.md` + root `CLAUDE.md` (agent playbook). Shallow-nested hybrid folder structure (hub pages at root, subfolders for high-volume categories). Obsidian-native link syntax in page bodies; bare-slug link fields in YAML frontmatter for Dataview compatibility. Heavy citations for philosophy/methodology pages, light citations for technique/drill pages. 4 user checkpoints at strategic review gates.

**Tech Stack:** Markdown + YAML frontmatter · Obsidian (reader + graph view + Dataview plugin for frontmatter queries) · Git for version history · Claude Code tools for research & writing: WebSearch, WebFetch, Read, Write, Edit, Grep, Glob, Bash. No custom CLI tooling in bootstrap (per §7.4 non-goals).

**Spec reference:** `docs/superpowers/specs/2026-04-22-volleyball-coaching-bible-design.md`

**Work philosophy:** Every page writes a `log.md` entry. Every new entity (coach, drill, technique, source) gets a page before being cross-linked. Every claim gets a citation or `[unsourced]` tag. No fabrication. Commit after every task.

---

## Operating conventions (read before executing any task)

### Commit-message format
```
<wave>: <short description>

Wave N / Task N.N — <what was produced>
Pages touched: <list of modified/created files>
```
Example: `wave1: add Karch Kiraly source pages · W1.3 — karch research ingest · Pages: sources/kiraly-1997-*, sources/kiraly-aoc-interview-2022, raw/articles/karch-*.md`

### Citation-key convention
Format: `<author-lastname>-<year>-<short-slug>` (e.g., `kiraly-1997-championship-volleyball`, `mccutcheon-2022-thinking-vb-interview`). For organizational sources: `<org>-<year>-<slug>` (e.g., `usav-2024-coaching-education`). For social posts: `<platform>-<handle>-<YYYYMMDD>` (e.g., `ig-usavolleyball-20260315`).

### Lint invariants (validated in Wave 6, and informally by the writing agent)
1. Every drill links ≥1 source + ≥1 technique (via `sources` and `techniques` frontmatter fields)
2. Every coach profile links ≥1 school + ≥1 source
3. Every contested technique has ≥2 `schools-perspectives` entries
4. Every source page exists before being cited anywhere
5. Zero orphan pages (every page reachable from a hub)
6. Every inline `[citation-key]` resolves to a `sources/` page's `citation-key` field

### Source trust tier (enforced in page frontmatter)
- **Tier 1:** published books by credentialed coaches, USA Volleyball official, peer-reviewed research — cite freely
- **Tier 2:** AOC, GMS, Net Live, VolleyballMag, FIVB, JVA, AVCA Convention clinics — cite with affiliation
- **Tier 3:** IG/TikTok/YouTube non-credentialed, forums — corroborate with Tier 1/2 before citing; attribute clearly

### Unsourced claim policy
Any claim without a source → inline `[unsourced]` tag AND entry in `wiki/unsourced-queue.md` with the page, claim, and a research hypothesis (where to look to source it later).

### Research-fidelity rules (per §5.4 of spec)
- **Books:** summarize with chapter/page refs; PDFs only if user-provided. Otherwise `raw/books/notes-<slug>.md` from fair-use material (previews, interviews, reviews, syllabi).
- **YouTube:** fetch captions → `raw/transcripts/<slug>.md` with URL + timestamps. No captions → summarize from description, tag `[transcript-unavailable]`.
- **Instagram:** screenshot + caption text + handle + date → `raw/instagram/<slug>.md`. Treat as ephemeral.
- **Articles:** clipped markdown → `raw/articles/<slug>.md`.

### User checkpoints (4 total)
- **CP1** (end of Wave 0): review `SCHEMA.md` before any content is written
- **CP2** (end of Wave 1): review source library — right coaches/schools represented?
- **CP3** (end of Wave 2): review coach/school profiles for positioning accuracy
- **CP4** (end of Wave 6): review full wiki

**At each checkpoint, the agent stops and waits for explicit user approval before proceeding.**

---

## Pre-Wave: Project initialization

### Task 0.1: Initialize git repository

**Files:**
- Create: `C:/Users/SongMu/documents/claudecode/vba/bible/.gitignore`

- [ ] **Step 1: Initialize git**

Run from project root:
```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible" && git init && git branch -M main
```
Expected: `Initialized empty Git repository in .../bible/.git/`

- [ ] **Step 2: Create .gitignore**

Write `C:/Users/SongMu/documents/claudecode/vba/bible/.gitignore`:
```
# Obsidian workspace (personal to each user's Obsidian install)
.obsidian/workspace*
.obsidian/cache
.obsidian/plugins/*/data.json

# OS
.DS_Store
Thumbs.db
desktop.ini

# Editor
.vscode/
*.swp
*.tmp

# Owned book PDFs that shouldn't be committed to shared repos
# (user may redistribute this repo; copyrighted PDFs stay local)
raw/books/*.pdf
```

- [ ] **Step 3: Commit**
```bash
git add .gitignore && git commit -m "chore: initialize git repo with .gitignore"
```

### Task 0.2: Create directory scaffolding

**Files:**
- Create: directory tree under `wiki/` and `raw/`

- [ ] **Step 1: Create folders**
```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible" && mkdir -p \
  wiki/coaches wiki/schools wiki/techniques wiki/positions wiki/systems-detail wiki/drills wiki/sources \
  raw/books raw/articles raw/transcripts raw/instagram raw/usav raw/research raw/images
```
Expected: no output, directories created.

- [ ] **Step 2: Verify**
```bash
find "C:/Users/SongMu/documents/claudecode/vba/bible/wiki" "C:/Users/SongMu/documents/claudecode/vba/bible/raw" -type d | sort
```
Expected: 17 directories total (wiki + 7 subfolders, raw + 7 subfolders + top-level wiki & raw).

- [ ] **Step 3: Add `.gitkeep` to each empty folder** so git tracks them
```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible" && \
  find wiki raw -type d -empty -exec touch {}/.gitkeep \;
```

- [ ] **Step 4: Commit**
```bash
git add wiki raw && git commit -m "chore: create wiki and raw directory scaffolding"
```

---

## Wave 0 — Foundation (playbook + templates)

Writes the schema and templates. No research content yet. Ends with CP1.

### Task W0.1: Write root `CLAUDE.md` pointer

**Files:**
- Create: `C:/Users/SongMu/documents/claudecode/vba/bible/CLAUDE.md`

- [ ] **Step 1: Write pointer file**

Content:
```markdown
# Volleyball Coaching Bible — Project Instructions

This project is an LLM-maintained wiki covering volleyball coaching.

**Before doing anything else in this project, read `wiki/SCHEMA.md`.**
It contains the conventions, page contracts, workflows, and anti-patterns
that keep this wiki consistent across sessions.

The pattern this wiki follows is documented at `Instructions/llm-wiki.md`.
The design spec is at `docs/superpowers/specs/2026-04-22-volleyball-coaching-bible-design.md`.

## User profile (brief)
Head coach, 14U girls club (nationally recognized program), indoor 6s.
Mastery coverage also scales to HS varsity and college levels.

## Quick navigation
- `wiki/index.md` — catalog of every wiki page
- `wiki/log.md` — chronological log of ingests, queries, lint passes
- `wiki/unsourced-queue.md` — claims needing citation backfill
- `raw/` — immutable source material; never edit these
- `wiki/` — LLM-maintained content; edit freely per SCHEMA.md rules
```

- [ ] **Step 2: Commit**
```bash
git add CLAUDE.md && git commit -m "wave0: add root CLAUDE.md pointer · W0.1"
```

### Task W0.2: Write `wiki/SCHEMA.md`

This is the single most important file in the wiki — the playbook every future session reads.

**Files:**
- Create: `C:/Users/SongMu/documents/claudecode/vba/bible/wiki/SCHEMA.md`

- [ ] **Step 1: Write SCHEMA.md in full**

The file must contain **10 sections** per spec §4.1. Each section content is specified below.

**Section 1 — Preamble.** 3 paragraphs covering: (a) what this wiki is (volleyball coaching bible, LLM-maintained, pattern from `Instructions/llm-wiki.md`), (b) who the user is (head coach, 14U girls national club, indoor 6s, scaling to HS/college), (c) positioning stance (neutral reference, preferred schools documented but not favored: Karch/GMS/AOC/Japanese/USAV).

**Section 2 — Directory map.** Exact tree of `wiki/` and `raw/` from spec §2.1 and §2.2, each folder annotated with one-line purpose.

**Section 3 — Page types reference.** For each of the 9 page types, a subsection containing:
- Folder + filename pattern (from spec §3.1 table)
- Required frontmatter fields (from spec §3.2)
- Optional frontmatter fields
- Required body sections with target word counts (from spec §3.3)
- Cross-link rules specific to this type

**Section 4 — Frontmatter contracts.** Paste the 9 frontmatter examples from spec §3.2 verbatim. Add enum value glossary at end:
- `phase ∈ {warm-up, skill, strategic, competition, conditioning}`
- `source-type ∈ {book, video-series, podcast, article, interview, clinic, social-post}`
- `trust-tier ∈ {1, 2, 3}`
- `skill ∈ {passing, setting, hitting, blocking, serving, defense, transition}`
- `system.category ∈ {offense, defense, serve-receive, blocking, transition}`
- `complexity ∈ {low, medium, high}`

**Section 5 — Citation rules.** Per spec §3.4: heavy (inline `[citation-key]` + `## Bibliography`) for philosophy/schools/coach-profiles/methodology-sections; light (just `## Sources`) for technique/drill/position/system pages; hub pages light. Inline format: `[citation-key]` keyed to the `citation-key` field of the relevant `sources/` page. Unresolvable keys fail lint. **Unsourced claims** get `[unsourced]` tag AND entry in `wiki/unsourced-queue.md`.

**Section 6 — Cross-link invariants.** Enumerate the 6 rules from spec §3.5 verbatim. State: "lint validates these; agent enforces pre-commit."

**Section 7 — Source trust tiers.** Copy spec §4.2 verbatim.

**Section 8 — Voice & style guide.** Copy spec §4.3 verbatim.

**Section 9 — Anti-patterns.** Copy spec §4.4 verbatim.

**Section 10 — Session-start checklist.** The 4-step drill every new session runs:
1. Read this file (`SCHEMA.md`) top-to-bottom
2. Read `index.md` to see the catalog
3. Tail last 10 lines of `log.md` to see recent activity: `tail -n 20 wiki/log.md`
4. If a specific area is being worked, read that area's hub page before touching sub-pages

Then a subsection "Workflows" with the 4 numbered workflows copied verbatim from spec §5 (ingest / query / lint / research).

- [ ] **Step 2: Self-validate SCHEMA.md**

Run to confirm all 10 sections exist:
```bash
grep -c "^## " "C:/Users/SongMu/documents/claudecode/vba/bible/wiki/SCHEMA.md"
```
Expected: at least 10 (one per section plus any subsections).

- [ ] **Step 3: Commit**
```bash
git add wiki/SCHEMA.md && git commit -m "wave0: write SCHEMA.md playbook · W0.2"
```

### Task W0.3: Write operational files (empty scaffolds)

**Files:**
- Create: `wiki/index.md`, `wiki/log.md`, `wiki/unsourced-queue.md`, `raw/INDEX.md`

- [ ] **Step 1: Write `wiki/index.md`** (scaffold only — populated in Wave 6)

Content:
```markdown
# Wiki Index

Catalog of every page in the wiki. Updated by the LLM on every ingest.
One-line summary per page; see the page itself for detail.

## Operational
- [SCHEMA.md](SCHEMA.md) — agent playbook: conventions, workflows, anti-patterns
- [log.md](log.md) — chronological operations log
- [unsourced-queue.md](unsourced-queue.md) — claims awaiting citation backfill

## Hub pages
*(populated in Waves 4–5)*

## Coaches
*(populated in Wave 2)*

## Schools / philosophies
*(populated in Wave 2)*

## Techniques
*(populated in Wave 3)*

## Positions
*(populated in Wave 3)*

## Systems
*(populated in Wave 3)*

## Drills
*(populated in Wave 4)*

## Sources
*(populated in Wave 1)*
```

- [ ] **Step 2: Write `wiki/log.md`**

Content:
```markdown
# Operations Log

Append-only log of wiki operations. Prefix format: `## [YYYY-MM-DD] <operation> | <short>`.

## [2026-04-22] bootstrap-start | Wave 0 begin
Project initialized. Git repo created. Scaffolding in place.
```

- [ ] **Step 3: Write `wiki/unsourced-queue.md`**

Content:
```markdown
# Unsourced Claim Queue

Every claim in the wiki tagged `[unsourced]` has an entry here. Lint replenishes
this list. Research passes hunt down primary sources and clear entries.

## Format
```
### <page-path>
- **Claim:** <exact sentence>
- **Why unsourced:** <brief reason — couldn't find Tier 1/2 evidence, specific claim beyond sources reviewed, etc.>
- **Research hypothesis:** <where to look — specific book chapter, interview, paper, author to track down>
- **Added:** YYYY-MM-DD
```

## Entries
*(populated as claims accumulate)*
```

- [ ] **Step 4: Write `raw/INDEX.md`**

Content:
```markdown
# Raw Source Index

One-line catalog of every file in `raw/`. Updated on every ingest.
Format: `- <path> — <source-title> — <citation-key>`

## books/
*(populated in Wave 1)*

## articles/
*(populated in Wave 1)*

## transcripts/
*(populated in Wave 1)*

## instagram/
*(populated in Wave 1)*

## usav/
*(populated in Wave 1)*

## research/
*(populated in Wave 1)*

## images/
*(populated as needed)*
```

- [ ] **Step 5: Commit**
```bash
git add wiki/index.md wiki/log.md wiki/unsourced-queue.md raw/INDEX.md && \
  git commit -m "wave0: scaffold operational files · W0.3"
```

### Task W0.4: Write page templates

Templates live in `wiki/_templates/` so future ingest/content-creation agents copy them. Obsidian's Templater plugin can use them directly.

**Files:**
- Create: `wiki/_templates/coach.md`, `wiki/_templates/school.md`, `wiki/_templates/technique.md`, `wiki/_templates/position.md`, `wiki/_templates/system.md`, `wiki/_templates/drill.md`, `wiki/_templates/source.md`, `wiki/_templates/age-lens.md`, `wiki/_templates/hub.md`

- [ ] **Step 1: Create `_templates/` directory**
```bash
mkdir -p "C:/Users/SongMu/documents/claudecode/vba/bible/wiki/_templates"
```

- [ ] **Step 2: Write coach template**

`wiki/_templates/coach.md`:
```markdown
---
type: coach
name: <Full Name>
country: <country>
era: <e.g., 1980s-present>
roles: [<role1>, <role2>]  # e.g., player, coach, commentator, author
schools: [<slug>]           # ≥1 required — slugs of schools/ pages
tags: []
sources: [<citation-key>]   # ≥1 required
---

# <Full Name>

## Overview
<2-3 sentences: who they are, what they're known for.>

## Coaching career
<Career timeline: teams coached, era, major results.>

## Core teaching principles
<3-5 principles they're known for. Inline `[citation-key]` after each claim.>

## Contributions to the game
<Innovations, publications, influence on other coaches/schools.>

## Quotes & representative passages
<Direct quotes where possible, each attributed with `[citation-key]`.>

## Sources
- [[<citation-key-1>]] — <title>
- [[<citation-key-2>]] — <title>
```

- [ ] **Step 3: Write school template**

`wiki/_templates/school.md`:
```markdown
---
type: school
name: <School Name>
origin: <country or institution>
founders: [<slug>]
core-principles: [<principle1>, <principle2>]
associated-coaches: [<slug>, <slug>]
related-schools: [<slug>]
sources: [<citation-key>]
---

# <School Name>

## Overview
<2-3 paragraphs introducing the school: what it is, what problem it addresses, era.>

## Core principles
<Bulleted list of 4-8 principles, each with `[citation-key]`.>

## Methodology
<How this school translates principles into practice design, drills, season planning.>

## Notable practitioners
<Coaches, teams, programs using this approach. Link to coach pages.>

## Contrasts with other schools
<How this school diverges from others. Attribute differences. Do not pick sides.>

## Critiques and limitations
<Fair criticisms raised in the literature. Attribute.>

## Sources
- [[<citation-key-1>]] — <title>
```

- [ ] **Step 4: Write technique template**

`wiki/_templates/technique.md`:
```markdown
---
type: technique
skill: <skill>                    # passing|setting|hitting|blocking|serving|defense|transition
subskill: <subskill>
positions: [<slug>, <slug>]
related-drills: [<slug>, <slug>]
related-techniques: [<slug>]
schools-perspectives:              # ≥2 required IF topic contested
  <school-slug>: "<concise statement of that school's approach>"
  <school-slug>: "<concise statement of that school's approach>"
sources: [<citation-key>]
---

# <Technique Name>

## Overview
<What is this skill/subskill. Where in the game it matters. 2-3 sentences.>

## Teaching progressions
<Step-by-step teaching progression: beginner → intermediate → advanced.
Light citations (`## Sources` at bottom; no inline) per citation policy.>

## Common errors
<Bulleted list of common errors + how to correct each.>

## Schools-perspectives
<Expanded discussion of how different schools teach this. Include only if
topic is genuinely contested. Mirror the frontmatter field but with more detail.>

## Related drills
- [[<drill-slug>]] — <short description>
- [[<drill-slug>]] — <short description>

## Sources
- [[<citation-key-1>]]
- [[<citation-key-2>]]
```

- [ ] **Step 5: Write position template**

`wiki/_templates/position.md`:
```markdown
---
type: position
position: <slug>                  # setter | outside-hitter | middle-blocker | opposite | libero | defensive-specialist
role: <role>
physical-profile: "<1-2 sentences>"
key-skills: [<technique-slug>]
common-drills: [<drill-slug>]
related-coaches: [<coach-slug>]
---

# <Position Name>

## Role and responsibilities
<What this position does in and out of system.>

## Physical profile
<Typical size, athleticism, strengths.>

## Key skills
<Which techniques this position must master. Link to technique pages.>

## Common drills
<Which drills develop this position. Link to drill pages.>

## Position-specific coaching points
<Teaching emphasis, decision-making, reads, communication.>

## Progression by level
<What a 14U player at this position focuses on vs. HS vs. college. Link to age-lens pages.>

## Sources
- [[<citation-key>]]
```

- [ ] **Step 6: Write system template**

`wiki/_templates/system.md`:
```markdown
---
type: system
category: <category>              # offense | defense | serve-receive | blocking | transition
name: <System Name>
age-appropriateness: [<level>]
complexity: <low|medium|high>
when-to-use: "<1-2 sentences>"
alternatives: [<system-slug>]
sources: [<citation-key>]
---

# <System Name>

## Overview
<What this system is, when it's used.>

## Personnel requirements
<Who you need — specialists, specific skills, setter profile, etc.>

## Diagram or text description of alignment
<Court positions. ASCII or linked image in `raw/images/`.>

## Strengths
<What this system is good at.>

## Weaknesses
<What this system struggles with.>

## When to use / when not to use
<Decision criteria.>

## Alternatives and adjustments
<When to switch to a different system; how to adapt this one under constraints.>

## Sources
- [[<citation-key>]]
```

- [ ] **Step 7: Write drill template**

`wiki/_templates/drill.md`:
```markdown
---
type: drill
name: <Drill Name>
primary-skill: <skill>
secondary-skills: [<skill>, <skill>]
techniques: [<technique-slug>]    # ≥1 required
phase: <phase>                    # warm-up|skill|strategic|competition|conditioning
team-size-min: <int>
team-size-max: <int>
duration-min: <int>
levels: [<level>]
equipment: [<item>]
sources: [<citation-key>]         # ≥1 required
video-url: <url or empty>
variations: [<drill-slug>]
---

# <Drill Name>

## Setup
<Court layout, equipment, player positions. Diagram if helpful.>

## Execution
<Step-by-step description of how the drill runs.>

## Coaching points
<What to watch for, what feedback to give, what reps to insist on.>

## Variations
<Variations that alter difficulty, focus, or phase.>

## Adaptations by level
<14U / HS / college differences in setup, tempo, or success criteria.>

## Sources
- [[<citation-key>]]
```

- [ ] **Step 8: Write source template**

`wiki/_templates/source.md`:
```markdown
---
type: source
source-type: <type>               # book|video-series|podcast|article|interview|clinic|social-post
title: "<title>"
author: "<author>"
year: <year>
citation-key: <slug-per-convention>
raw-file: raw/<category>/<filename>
url: <url or empty>
topics: [<topic>]
featured-coaches: [<coach-slug>]
schools: [<school-slug>]
trust-tier: <1|2|3>
---

# <title>

## Summary
<2-3 paragraph summary of what this source covers and why it matters.>

## Key claims / ideas
<Bulleted list of the source's most important contributions. Each point can be
cross-linked from wiki pages via `[<citation-key>]`.>

## Topics covered
<Longer topical breakdown.>

## Where it's cited
*(populated as wiki pages cite this source; Dataview can regenerate)*

## Access
- Raw file: `<raw-file>`
- URL: <url>
- Trust tier: <1|2|3> — <one-line rationale>
```

- [ ] **Step 9: Write age-lens template**

`wiki/_templates/age-lens.md`:
```markdown
---
type: age-lens
label: <label>                    # 14u | hs | college | etc.
scope: "<1 sentence>"
emphasis: [<emphasis>]
age-ceilings:
  - "<technique or system NOT appropriate at this level>"
sources: [<citation-key>]
---

# Age Lens: <label>

## Scope
<Which demographic this lens applies to.>

## Development priorities
<What this age group needs to develop first, second, third.>

## Appropriate techniques & systems
<Which techniques/systems from the wiki are age-appropriate. Link.>

## NOT appropriate at this level
<What's developmentally too advanced, why.>

## Practice design adaptations
<How practice looks different for this age: duration, focus, complexity.>

## Season-planning adaptations
<How season planning differs for this age.>

## Sources
- [[<citation-key>]]
```

- [ ] **Step 10: Write hub template**

`wiki/_templates/hub.md`:
```markdown
---
type: hub
area: <area>
subtopics: [<topic>]
---

# <Area Name>

## Overview
<What this area covers. 1-2 paragraphs orienting the reader.>

## Major subtopics
<Bulleted list linking to pages in this area.>

## Schools of thought
<Where different schools approach this area differently. Link to school pages.>

## Getting started
<For the coach new to this area: where to begin reading. Link in reading order.>

## Related areas
<Cross-link to other hub pages where relevant.>

## Sources
*(this is a navigational page; body claims should be light. Anything non-navigational belongs on a subordinate page.)*
```

- [ ] **Step 11: Commit**
```bash
git add wiki/_templates/ && git commit -m "wave0: add page templates · W0.4"
```

### Task W0.5: Append Wave 0 log entry

**Files:**
- Modify: `wiki/log.md`

- [ ] **Step 1: Append log entry**

Append to `wiki/log.md`:
```markdown

## [2026-04-22] wave0-complete | Foundation done
Wrote: CLAUDE.md (root), SCHEMA.md, index.md scaffold, log.md, unsourced-queue.md,
raw/INDEX.md, 9 page templates. Scaffolding for all content ready.
Next: CP1 (user reviews SCHEMA.md), then Wave 1 research.
Pages touched: 15.
```

- [ ] **Step 2: Commit**
```bash
git add wiki/log.md && git commit -m "wave0: log end of Wave 0 · W0.5"
```

### Task W0.6 (CHECKPOINT 1): User reviews SCHEMA.md

- [ ] **Step 1: Present to user**

Message: "**CP1:** Wave 0 complete. SCHEMA.md is written. Before I start Wave 1 research, please review `wiki/SCHEMA.md`. Specifically: do the page-type contracts, citation rules, trust tiers, and voice guide match what you want? Approve or request changes."

- [ ] **Step 2: Wait for user approval**

Do not proceed to Wave 1 until user explicitly approves. If user requests changes, make them, re-commit (`git commit -m "wave0: SCHEMA.md revisions from CP1"`), and re-present.

---

## Wave 1 — Source research & `raw/` library population

Deep web research pass. Ingests ~30–50 sources into `raw/` and writes corresponding `sources/<key>.md` pages.

**Wave 1 task structure pattern** (applied to every source cluster):
1. **Research** — WebSearch for the cluster's topics; identify sources by trust tier
2. **Fetch** — WebFetch each URL; convert to markdown; save to appropriate `raw/` subfolder with slugged filename
3. **Source page** — create `sources/<citation-key>.md` from template, fully populated frontmatter including `trust-tier` and `raw-file`
4. **raw/INDEX.md update** — append a line per raw file
5. **log.md entry** — single line for the cluster
6. **Commit**

### Task W1.1: USA Volleyball coaching resources

USAV public coaching education materials are Tier 1. Priority targets: CAP (Coaching Accreditation Program) public-facing content, coaching toolbox, age-appropriate guidance (a cornerstone of the 14U lens), IMPACT course description.

**Files:**
- Create: ≥4 entries in `raw/usav/`, ≥4 source pages in `wiki/sources/`

- [ ] **Step 1: Research**

WebSearch queries (run each, note Tier 1 URLs):
- `USA Volleyball coaching education CAP program`
- `USA Volleyball age-appropriate guidelines`
- `USA Volleyball IMPACT coaching course`
- `USAV coaching toolbox`
- `USA Volleyball skills guide youth volleyball`

- [ ] **Step 2: Fetch into `raw/usav/`**

For each Tier 1 URL found in step 1:
- WebFetch URL
- Save as `raw/usav/<slug>.md` with YAML front-note:
  ```yaml
  ---
  source-url: <url>
  fetched: 2026-04-22
  ---
  # Original title
  <fetched content>
  ```

Target: at least 4 files in `raw/usav/`.

- [ ] **Step 3: Write source pages**

For each raw file, create `wiki/sources/usav-<year>-<slug>.md` from `_templates/source.md`. Fill frontmatter completely. Fill Summary and Key claims sections from the raw content.

- [ ] **Step 4: Update `raw/INDEX.md`**

Under `## usav/`, append one line per file:
```
- raw/usav/<filename> — <source-title> — usav-<year>-<slug>
```

- [ ] **Step 5: Log entry**

Append to `wiki/log.md`:
```markdown

## [2026-04-22] wave1-ingest | USAV coaching resources (W1.1)
Sources: <list citation-keys>. Raw: ≥4 files in raw/usav/.
Pages touched: <count>.
```

- [ ] **Step 6: Commit**
```bash
git add raw/usav/ wiki/sources/usav-*.md raw/INDEX.md wiki/log.md && \
  git commit -m "wave1: ingest USAV coaching resources · W1.1"
```

### Task W1.2: Karch Kiraly corpus

Karch is a user-preferred author. Coverage must be substantial. Targets: his book(s), major interviews, USA Women's NT coaching content, clinic talks, AOC/USAV podcasts featuring him.

**Files:**
- Create: ≥5 entries across `raw/articles/`, `raw/transcripts/`, possibly `raw/books/notes-*.md`
- Create: ≥5 source pages in `wiki/sources/`

- [ ] **Step 1: Research**

WebSearch queries:
- `Karch Kiraly championship volleyball book`
- `Karch Kiraly coaching interview`
- `Karch Kiraly USA women's volleyball coaching philosophy`
- `Karch Kiraly beach to indoor transition`
- `Karch Kiraly AVCA Convention talk`
- `Karch Kiraly USAV coaching video`

Tag each found source with trust tier.

- [ ] **Step 2: Fetch articles and transcripts**

For each Tier 1/2 URL:
- Articles → `raw/articles/karch-<year>-<slug>.md`
- YouTube → fetch transcript (via WebFetch on the video URL; captures captions if exposed) → `raw/transcripts/karch-<year>-<slug>.md` with source URL + any timestamps
- If book preview (Google Books / Amazon Look Inside) → summarize in `raw/books/notes-kiraly-championship-volleyball.md` with chapter/page refs where visible. If user has dropped the PDF in `raw/books/`, note its path and extract more liberally.

- [ ] **Step 3: Write source pages**

For each raw file, create `wiki/sources/kiraly-<year>-<slug>.md` from template. Full frontmatter; `featured-coaches: [karch-kiraly]` (even though that page doesn't exist yet — it will be created in Wave 2 and the pre-existing forward-reference is fine per SCHEMA rule "source page must exist before citation"; the coach page doesn't exist yet but the source page does).

- [ ] **Step 4: Update `raw/INDEX.md` + log**

Append raw lines under appropriate sections. Append `wiki/log.md` entry.

- [ ] **Step 5: Commit**
```bash
git add raw/ wiki/sources/kiraly-*.md wiki/log.md && \
  git commit -m "wave1: ingest Karch Kiraly corpus · W1.2"
```

### Task W1.3: Hugh McCutcheon corpus

Same pattern as W1.2. Targets: "Thinking Volleyball" (fair-use from previews/reviews/interviews), USA Women's/Men's NT coaching content, University of Minnesota coaching, AOC podcast appearances.

**Files:**
- Create: ≥4 raw files, ≥4 source pages

- [ ] **Step 1: Research**

WebSearch:
- `Hugh McCutcheon Thinking Volleyball book summary`
- `Hugh McCutcheon coaching philosophy interview`
- `Hugh McCutcheon USA volleyball head coach`
- `Hugh McCutcheon Minnesota volleyball coaching`
- `Hugh McCutcheon AVCA coaching development`

- [ ] **Step 2: Fetch** (same pattern as W1.2)

- [ ] **Step 3: Write source pages** (`sources/mccutcheon-*.md`)

- [ ] **Step 4: Update `raw/INDEX.md` + log**

- [ ] **Step 5: Commit**
```bash
git add raw/ wiki/sources/mccutcheon-*.md wiki/log.md raw/INDEX.md && \
  git commit -m "wave1: ingest Hugh McCutcheon corpus · W1.3"
```

### Task W1.4: Gold Medal Squared / Carl McGown corpus

Tier 2 with some Tier 1 (McGown's published work). Focus on motor learning, random practice, feedback timing.

**Files:**
- Create: ≥4 raw files, ≥4 source pages

- [ ] **Step 1: Research**

WebSearch:
- `Gold Medal Squared coaching philosophy`
- `Carl McGown volleyball coaching motor learning`
- `GMS random practice blocked practice`
- `Gold Medal Squared Mike Hebert coaching`
- `GMS coaches clinic webinar`

- [ ] **Step 2: Fetch** (articles → `raw/articles/`, transcripts → `raw/transcripts/`)

- [ ] **Step 3: Write source pages** (`sources/gms-*.md`, `sources/mcgown-*.md`)

- [ ] **Step 4: Update `raw/INDEX.md` + log**

- [ ] **Step 5: Commit**
```bash
git add raw/ wiki/sources/gms-*.md wiki/sources/mcgown-*.md wiki/log.md raw/INDEX.md && \
  git commit -m "wave1: ingest GMS / McGown corpus · W1.4"
```

### Task W1.5: Art of Coaching Volleyball corpus

Tier 2. AOC publishes an enormous content library: article archive, podcast episodes, video catalog. Prioritize articles by notable coaches (Russ Rose, John Dunning, etc. that AOC hosts).

**Files:**
- Create: ≥5 raw files, ≥5 source pages

- [ ] **Step 1: Research**

WebSearch:
- `Art of Coaching Volleyball articles`
- `Art of Coaching Volleyball podcast`
- `AOC volleyball John Dunning teaching`
- `AOC volleyball Russ Rose`
- `AOC volleyball practice planning articles`

- [ ] **Step 2: Fetch** (articles → `raw/articles/`; podcast transcripts → `raw/transcripts/`)

- [ ] **Step 3: Write source pages** (`sources/aoc-*.md`)

- [ ] **Step 4: Update `raw/INDEX.md` + log**

- [ ] **Step 5: Commit**
```bash
git add raw/ wiki/sources/aoc-*.md wiki/log.md raw/INDEX.md && \
  git commit -m "wave1: ingest AOC corpus · W1.5"
```

### Task W1.6: Japanese training corpus

User-preferred tradition with heavy historical and modern content. Targets: Nakagaichi writings (if available in English), Daimatsu historical (1964 Women's NT), V.League modern coaches, JVA coaching materials.

**Files:**
- Create: ≥4 raw files, ≥4 source pages

- [ ] **Step 1: Research**

WebSearch:
- `Japanese volleyball training philosophy method`
- `Yuichi Nakagaichi volleyball coaching`
- `Daimatsu Hirobumi 1964 Japan women's volleyball`
- `V.League Japan coaching methodology`
- `JVA Japan Volleyball Association coaching education`
- `Japanese volleyball defense technique`

- [ ] **Step 2: Fetch**

English-language material primarily. If high-value Japanese-language material surfaces, capture with a `[translation-needed]` note in the source page.

- [ ] **Step 3: Write source pages** (`sources/<author>-<year>-*.md` or `sources/jva-<year>-*.md`)

- [ ] **Step 4: Update `raw/INDEX.md` + log**

- [ ] **Step 5: Commit**
```bash
git add raw/ wiki/sources/ wiki/log.md raw/INDEX.md && \
  git commit -m "wave1: ingest Japanese training corpus · W1.6"
```

### Task W1.7: Additional major coaches corpus

Covers coaches mentioned in spec §6.3 not already covered: Russ Rose, John Dunning, Mike Hebert, Terry Liskevych, John Speraw, Mary Wise, Lang Ping (Chinese but Japanese-influenced).

**Files:**
- Create: ≥6 raw files, ≥6 source pages (≥1 per coach)

- [ ] **Step 1: Research**

For each of: Rose, Dunning, Hebert, Liskevych, Speraw, Wise, Lang Ping, run:
- `<coach name> volleyball coaching philosophy book interview`
- `<coach name> practice planning teaching`

- [ ] **Step 2: Fetch** (articles → `raw/articles/`, transcripts → `raw/transcripts/`, book notes → `raw/books/notes-*.md`)

- [ ] **Step 3: Write source pages**

One `sources/<lastname>-<year>-*.md` per coach minimum; more if multiple strong sources exist.

- [ ] **Step 4: Update `raw/INDEX.md` + log**

- [ ] **Step 5: Commit**
```bash
git add raw/ wiki/sources/ wiki/log.md raw/INDEX.md && \
  git commit -m "wave1: ingest additional major coaches corpus · W1.7"
```

### Task W1.8: Motor learning / skill acquisition research

Tier 1 academic sources. Critical for backing up claims in `schools/ecological-dynamics.md`, `schools/constraints-led-approach.md`, technique pages' methodology sections.

**Files:**
- Create: ≥3 files in `raw/research/`, ≥3 source pages

- [ ] **Step 1: Research**

WebSearch (prefer open-access or abstract-available):
- `motor learning random vs blocked practice volleyball`
- `ecological dynamics skill acquisition sports`
- `constraints-led approach coaching`
- `contextual interference effect motor skill volleyball`
- `representative learning design team sport`

Also scan: Google Scholar, Research Gate (abstracts OK for citation).

- [ ] **Step 2: Fetch**

Abstracts and open-access PDFs → `raw/research/<firstauthor>-<year>-<slug>.md`. Full papers only if open-access; for paywalled, abstract is sufficient for Tier 1 citation support.

- [ ] **Step 3: Write source pages** (`sources/<firstauthor>-<year>-<slug>.md` with `trust-tier: 1`)

- [ ] **Step 4: Update `raw/INDEX.md` + log**

- [ ] **Step 5: Commit**
```bash
git add raw/research/ wiki/sources/ wiki/log.md raw/INDEX.md && \
  git commit -m "wave1: ingest motor learning research · W1.8"
```

### Task W1.9: Instagram + YouTube capture (Tier 3)

Snapshots of high-signal modern coaching content from verified accounts. Ephemeral material; handle per spec §5.4.

**Files:**
- Create: files in `raw/instagram/` and `raw/transcripts/`, corresponding source pages

- [ ] **Step 1: Identify targets**

WebSearch / direct IG/YouTube browse for verified accounts:
- @usavolleyball, @aocvolleyball, @goldmedalsquaredvolleyball, @karch_kiraly (if public)
- Coach-athletes with teaching content: @joelembiid... actually verify actual VB accounts. Use WebSearch: `best volleyball coaching instagram accounts 2026`, `volleyball youtube channels coaches`

- [ ] **Step 2: Capture**

For IG: screenshot + caption text to `raw/instagram/<handle>-<YYYYMMDD>-<slug>.md`:
```markdown
---
handle: "@<handle>"
post-date: YYYY-MM-DD
post-url: <url>
captured: 2026-04-22
---
# Caption
<full caption text>

# Description of image/video content
<brief description>

# Screenshot reference
raw/images/ig-<handle>-<YYYYMMDD>-<slug>.png
```

For YouTube: captions → `raw/transcripts/<channel>-<slug>.md` with URL + timestamps.

- [ ] **Step 3: Write source pages**

For each social post or YouTube video, `sources/ig-<handle>-<YYYYMMDD>.md` or `sources/yt-<channel>-<slug>.md` with `trust-tier: 3` and corroboration notes.

- [ ] **Step 4: Update `raw/INDEX.md` + log**

- [ ] **Step 5: Commit**
```bash
git add raw/instagram/ raw/transcripts/ wiki/sources/ wiki/log.md raw/INDEX.md && \
  git commit -m "wave1: ingest IG + YouTube tier-3 corpus · W1.9"
```

### Task W1.10: Wave 1 summary + CP2 prep

- [ ] **Step 1: Count source pages**

Run:
```bash
ls "C:/Users/SongMu/documents/claudecode/vba/bible/wiki/sources/" | wc -l
```
Expected: ≥30 (spec target).

If < 30, identify which clusters are under-represented and add more sources (re-run relevant tasks W1.1–W1.9 with additional queries).

- [ ] **Step 2: Summarize in log**

Append `wiki/log.md`:
```markdown

## [2026-04-22] wave1-complete | Source library populated
Source pages: <count>. Raw files: <count>.
Coverage summary: <clusters covered, sources per cluster>.
Next: CP2 user review.
```

- [ ] **Step 3: Commit**
```bash
git add wiki/log.md && git commit -m "wave1: summary and CP2 prep · W1.10"
```

### Task W1.11 (CHECKPOINT 2): User reviews source library

- [ ] **Step 1: Present to user**

Message to user:
"**CP2:** Wave 1 complete. Source library populated.
- Sources pages: `<count>` in `wiki/sources/`
- Raw files: `<count>` in `raw/`
- Coverage summary: `<clusters covered>`

Please review `wiki/sources/` (file listing) and a few representative `sources/*.md` pages. Specifically: are the right coaches/schools represented? Any obvious source I missed? Any source I included that you don't think should be primary reference?

Approve or request additions/removals before Wave 2 begins (where I start writing coach/school profiles from this material)."

- [ ] **Step 2: Wait for user approval**

If additions requested: revisit relevant W1.* tasks to add sources. If removals requested: delete source pages + raw files, amend commit or add revert commit.

---

## Wave 2 — Reference frame (coaches + schools)

Build coach profiles and school/philosophy pages using Wave 1 sources. Heavy citations throughout. Each page produces cross-links to existing source pages; new entity references can be stubs.

**Wave 2 task pattern** (applied to each coach and each school):
1. Identify sources in `wiki/sources/` that feature/discuss this entity
2. Copy `_templates/<type>.md` to target path
3. Fill frontmatter completely (link to `schools/` + `sources/` per invariants)
4. Draft body — heavy inline `[citation-key]` citations
5. Validate: ≥1 school + ≥1 source linked (for coaches); ≥1 source (for schools); all `[citation-key]` resolve
6. Update `index.md` — add entry under `## Coaches` or `## Schools`
7. Log.md entry
8. Commit

### Task W2.1: Write coach profiles — USA-centric (batch 1)

**Target coaches (5 profiles):** Karch Kiraly, Hugh McCutcheon, Terry Liskevych, John Speraw, Mary Wise.

**Files:**
- Create: `wiki/coaches/karch-kiraly.md`, `wiki/coaches/hugh-mccutcheon.md`, `wiki/coaches/terry-liskevych.md`, `wiki/coaches/john-speraw.md`, `wiki/coaches/mary-wise.md`

For each coach, execute these steps (5 iterations of the same pattern):

- [ ] **Step 1 (per coach): Collect sources**

Grep `wiki/sources/` for entries where the coach appears in `featured-coaches:`:
```bash
grep -lE "featured-coaches:.*\b<lastname>\b" "C:/Users/SongMu/documents/claudecode/vba/bible/wiki/sources/"
```
Target: ≥3 sources per coach.

- [ ] **Step 2 (per coach): Write profile**

Copy `_templates/coach.md` to `wiki/coaches/<firstname-lastname>.md`. Fill:
- Frontmatter: `name`, `country`, `era`, `roles`, `schools:` (at least 1 — most US coaches link `usa-volleyball-cap`), `tags`, `sources: [<citation-keys>]`
- Body sections per template. Each claim in "Core teaching principles," "Contributions to the game," and "Quotes" gets inline `[citation-key]`. Target page length: ~1500 words.

Content guidance per coach:
- **Karch:** beach→indoor transition, reading the game, mental toughness, platform simplification
- **McCutcheon:** Thinking Volleyball framework, mental model of play, USA men's '08 / USA women's '12 approaches, U Minn era
- **Liskevych:** AOC co-founder, Liberos handbook author, USA women's '84–'96 era
- **Speraw:** current USA men's NT, UCLA, defensive systems, player development
- **Wise:** Florida SEC dynasty, culture-building, long-tenure consistency

- [ ] **Step 3 (per coach): Validate**

For each `wiki/coaches/<slug>.md`:
```bash
# Check frontmatter link invariants
grep -E "^schools:" wiki/coaches/<slug>.md  # must show ≥1 slug
grep -E "^sources:" wiki/coaches/<slug>.md  # must show ≥1 slug
# Check that every inline [citation-key] resolves
grep -oE "\[[a-z0-9-]+\]" wiki/coaches/<slug>.md | sort -u
# For each captured key, verify a source page exists:
ls wiki/sources/<key>.md
```
Expected: no missing source pages, no unresolvable citations.

- [ ] **Step 4 (after all 5 profiles): Update `index.md`**

Under `## Coaches` in `wiki/index.md`:
```markdown
- [[karch-kiraly]] — three-time Olympic gold medalist, current USA women's NT head coach
- [[hugh-mccutcheon]] — author of *Thinking Volleyball*, USA men's '08 Olympic gold, USA women's '12 silver
- [[terry-liskevych]] — AOC co-founder, USA women's NT '84–'96, *The Volleyball Coaching Bible* editor
- [[john-speraw]] — current USA men's NT head coach, UCLA
- [[mary-wise]] — Florida head coach 1991–present, SEC dynasty builder
```

- [ ] **Step 5: Log + commit**

Append log, commit:
```bash
git add wiki/coaches/ wiki/index.md wiki/log.md && \
  git commit -m "wave2: coach profiles (USA batch 1) · W2.1 · 5 profiles"
```

### Task W2.2: Write coach profiles — methodology-school coaches (batch 2)

**Target coaches (4 profiles):** Carl McGown (GMS founder), Mike Hebert, John Dunning, Russ Rose.

Same pattern as W2.1. Content guidance:
- **McGown:** GMS founding, motor learning evangelism, BYU era
- **Hebert:** Illinois/Minnesota/New Mexico, *Thinking Volleyball* (shares title with McCutcheon book; disambiguate), GMS affiliation
- **Dunning:** Pacific/Stanford dynasty, system-centric coaching
- **Rose:** Penn State, seven NCAA titles, program culture

- [ ] **Step 1–3: Per coach (5 iterations pattern from W2.1)**

- [ ] **Step 4: Update `index.md`**

Add entries under `## Coaches`.

- [ ] **Step 5: Commit**
```bash
git add wiki/coaches/ wiki/index.md wiki/log.md && \
  git commit -m "wave2: coach profiles (methodology batch 2) · W2.2 · 4 profiles"
```

### Task W2.3: Write coach profiles — international (batch 3)

**Target coaches (3–6 profiles):** Yuichi Nakagaichi, Daimatsu Hirobumi, Lang Ping (Jenny Lang), Julio Velasco (Italian school), Bernardo Rezende "Bernardinho" (Brazilian), Giovanni Guidetti (modern Italian/Dutch/Turkish).

Same pattern as W2.1. Content guidance:
- **Nakagaichi:** Japan men's '72 Olympic gold architect, technical precision
- **Daimatsu:** 1964 Women's Olympic gold, "Witches of the Orient," training intensity
- **Lang Ping:** China women's legend as player & coach, 2016 Rio Olympic gold coach
- **Velasco:** Italian men's 1980s–90s dynasty, modern methodology innovator
- **Bernardinho:** Brazilian men's/women's multiple Olympic golds, modern offensive systems
- **Guidetti:** modern pro coach, Turkish/Dutch/Italian national teams

- [ ] **Step 1–3: Per coach iterations**

- [ ] **Step 4: Update `index.md`**

- [ ] **Step 5: Commit**
```bash
git add wiki/coaches/ wiki/index.md wiki/log.md && \
  git commit -m "wave2: coach profiles (international batch 3) · W2.3 · N profiles"
```

### Task W2.4: Write school / philosophy pages — preferred-school set

**Target pages (4–5 profiles):** `gold-medal-squared.md`, `art-of-coaching-volleyball.md`, `japanese-training.md`, `usa-volleyball-cap.md`, `ecological-dynamics.md`.

These are user-preferred schools; heaviest citations, most detailed treatment (2000–2500 words each per spec §3.3).

**Files:**
- Create: `wiki/schools/gold-medal-squared.md`, `wiki/schools/art-of-coaching-volleyball.md`, `wiki/schools/japanese-training.md`, `wiki/schools/usa-volleyball-cap.md`, `wiki/schools/ecological-dynamics.md`

For each school (5 iterations):

- [ ] **Step 1 (per school): Collect sources**

Grep `wiki/sources/` for entries linking this school:
```bash
grep -lE "schools:.*\b<school-slug>\b" wiki/sources/
```

- [ ] **Step 2 (per school): Write page**

Copy `_templates/school.md` to `wiki/schools/<slug>.md`. Fill frontmatter and all required body sections. Content guidance:

- **gold-medal-squared.md:** motor learning, random practice > blocked, immediate feedback, McGown's frame; cite GMS sources + research
- **art-of-coaching-volleyball.md:** Liskevych + Dunning founding, pedagogical breadth, coach-development emphasis; cite AOC sources
- **japanese-training.md:** precision, discipline, defensive emphasis, dig-up-everything mindset, historical roots (Daimatsu → modern); cite Japanese + JVA sources
- **usa-volleyball-cap.md:** CAP curriculum structure, age-appropriate model, IMPACT foundation; cite USAV sources
- **ecological-dynamics.md:** constraints-led, representative learning, perception-action coupling; cite research + related AOC/GMS articles

- [ ] **Step 3 (per school): Validate**

Confirm ≥1 source link; confirm "Contrasts with other schools" section fairly presents alternatives (per spec §1.3 neutrality).

- [ ] **Step 4: Update `index.md`**

Add entries under `## Schools / philosophies`.

- [ ] **Step 5: Commit**
```bash
git add wiki/schools/ wiki/index.md wiki/log.md && \
  git commit -m "wave2: preferred schools (GMS/AOC/Japanese/USAV/EcoDyn) · W2.4 · 5 pages"
```

### Task W2.5: Write school / philosophy pages — contrasting-school set

**Target pages (3–5 profiles):** `russian-school.md`, `brazilian-school.md`, `italian-school.md`, `constraints-led-approach.md`, `game-based-training.md`, `block-vs-random-practice.md` (methodology page).

Same pattern as W2.4. Content:
- **russian-school.md:** Platonov, Karpol, systems-heavy, physical dominance
- **brazilian-school.md:** Bernardinho era, skill+creativity, modern offensive systems
- **italian-school.md:** Velasco-era methodological innovation, Guidetti continuation
- **constraints-led-approach.md:** task/individual/environmental constraints; contrast with traditional progressions
- **game-based-training.md:** Play Practice roots, volleyball-specific application (overlaps with ecological-dynamics but distinct enough to warrant own page)
- **block-vs-random-practice.md:** methodology comparison page rather than a school — justified because it's cross-cutting

- [ ] **Step 1–3: Per school iterations**

- [ ] **Step 4: Update `index.md`**

- [ ] **Step 5: Commit**
```bash
git add wiki/schools/ wiki/index.md wiki/log.md && \
  git commit -m "wave2: contrasting schools + methodology pages · W2.5 · N pages"
```

### Task W2.6: Cross-link coaches ↔ schools

Ensure every coach profile's `schools:` field matches what schools' `associated-coaches:` lists. Bidirectional integrity.

- [ ] **Step 1: Generate coach→school map**

Bash:
```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible"
for f in wiki/coaches/*.md; do
  coach=$(basename "$f" .md)
  schools=$(grep -E "^schools:" "$f" | sed 's/schools: //; s/\[//; s/\]//')
  echo "$coach → $schools"
done
```

- [ ] **Step 2: Generate school→coach map**
```bash
for f in wiki/schools/*.md; do
  school=$(basename "$f" .md)
  coaches=$(grep -E "^associated-coaches:" "$f" | sed 's/associated-coaches: //; s/\[//; s/\]//')
  echo "$school → $coaches"
done
```

- [ ] **Step 3: Reconcile**

For every coach→school link, verify the school's `associated-coaches` includes that coach. If missing, add. Write a small fix-script OR hand-edit.

- [ ] **Step 4: Commit**
```bash
git add wiki/coaches/ wiki/schools/ && \
  git commit -m "wave2: reconcile coach↔school cross-links · W2.6"
```

### Task W2.7: Wave 2 summary + CP3 prep

- [ ] **Step 1: Count + validate**
```bash
echo "Coach profiles: $(ls wiki/coaches/*.md | wc -l)"
echo "School pages:   $(ls wiki/schools/*.md | wc -l)"
```
Target: 12–15 coach profiles, 8–10 school pages.

- [ ] **Step 2: Log + commit**

Append log:
```markdown

## [2026-04-22] wave2-complete | Reference frame populated
Coach profiles: <count>. School pages: <count>.
Cross-links reconciled. Ready for CP3.
```

```bash
git add wiki/log.md && git commit -m "wave2: summary · W2.7"
```

### Task W2.8 (CHECKPOINT 3): User reviews coach/school profiles

- [ ] **Step 1: Present to user**

Message: "**CP3:** Wave 2 complete. `wiki/coaches/` has `<count>` profiles; `wiki/schools/` has `<count>` pages.

These are the highest-fingerprint pages in the wiki — they encode how the wiki characterizes each tradition. Please spot-check 3–4 coach profiles and 3–4 school pages, especially those on the preferred schools (GMS, AOC, Japanese, USAV-CAP). Specifically: is the positioning neutral but accurate? Are contested points presented fairly? Are there any characterizations you'd contest?

Approve or request revisions before Wave 3 (technical core: techniques, positions, systems)."

- [ ] **Step 2: Wait for user approval**

Revise as requested. Commit revisions before proceeding.

---

## Wave 3 — Technical core (techniques + positions + systems)

Build technique, position, systems-detail pages. Each page links to coach/school/source pages created in Wave 2.

### Task W3.1: Passing techniques

**Files:**
- Create: `wiki/techniques/passing-forearm.md`, `wiki/techniques/passing-overhead.md`, `wiki/techniques/passing-serve-receive.md`, `wiki/techniques/passing-free-ball.md`

For each (4 iterations):

- [ ] **Step 1 (per page): Copy template**

`cp wiki/_templates/technique.md wiki/techniques/<slug>.md`

- [ ] **Step 2 (per page): Fill frontmatter**

Set `skill: passing`, appropriate `subskill`, `positions:` (who uses this), `related-drills:` (leave empty; Wave 4 will backfill), `related-techniques:`, and — if contested — `schools-perspectives:` with ≥2 schools.

Example for `passing-forearm.md`:
```yaml
---
type: technique
skill: passing
subskill: forearm
positions: [libero, defensive-specialist, outside-hitter]
related-drills: []  # filled in Wave 4
related-techniques: [defense-platform]
schools-perspectives:
  gms: "Platform angle primary, footwork secondary; random practice drives pattern recognition"
  aoc: "Read server's contact first, then platform"
  japanese: "Midline emphasis, quick reset; attention to body position over arm angle"
sources: [kiraly-1997-championship-volleyball, mccutcheon-2022-thinking-volleyball-interview, gms-2020-passing-fundamentals]
---
```

- [ ] **Step 3 (per page): Fill body**

Per template: `## Overview`, `## Teaching progressions`, `## Common errors`, `## Schools-perspectives`, `## Related drills`, `## Sources`. Light citation policy (no inline; `## Sources` section only).

- [ ] **Step 4 (per page): Validate**

Check frontmatter validity (required fields present, slugs resolve) and body has all 6 sections.

- [ ] **Step 5: Update `index.md`**

Under `## Techniques` add 4 entries.

- [ ] **Step 6: Commit**
```bash
git add wiki/techniques/passing-*.md wiki/index.md wiki/log.md && \
  git commit -m "wave3: passing techniques · W3.1 · 4 pages"
```

### Task W3.2: Setting techniques

**Files:** `setting-hands.md`, `setting-jump.md`, `setting-backset.md`, `setting-out-of-system.md`

Same pattern as W3.1.

- [ ] **Step 1–5 (4 iterations per pattern)**

- [ ] **Step 6: Commit**
```bash
git add wiki/techniques/setting-*.md wiki/index.md wiki/log.md && \
  git commit -m "wave3: setting techniques · W3.2 · 4 pages"
```

### Task W3.3: Hitting techniques

**Files:** `hitting-approach.md`, `hitting-arm-swing.md`, `hitting-shot-selection.md`, `hitting-back-row-attack.md`

Same pattern.

- [ ] **Step 1–5**

- [ ] **Step 6: Commit**
```bash
git add wiki/techniques/hitting-*.md wiki/index.md wiki/log.md && \
  git commit -m "wave3: hitting techniques · W3.3 · 4 pages"
```

### Task W3.4: Blocking techniques

**Files:** `blocking-footwork.md`, `blocking-hand-position.md`, `blocking-read.md`, `blocking-swing.md`

Note: `blocking-read.md` and `blocking-swing.md` are *technique* pages for the mechanical footwork/timing; the *system* pages (`read-blocking.md`, `swing-blocking.md`) in W3.8 cover the team-level implementation.

- [ ] **Step 1–5**

- [ ] **Step 6: Commit**
```bash
git add wiki/techniques/blocking-*.md wiki/index.md wiki/log.md && \
  git commit -m "wave3: blocking techniques · W3.4 · 4 pages"
```

### Task W3.5: Serving techniques

**Files:** `serving-float.md`, `serving-jump-float.md`, `serving-topspin.md`, `serving-hybrid.md`

Same pattern.

- [ ] **Step 6: Commit**
```bash
git add wiki/techniques/serving-*.md wiki/index.md wiki/log.md && \
  git commit -m "wave3: serving techniques · W3.5 · 4 pages"
```

### Task W3.6: Defense + transition techniques

**Files:** `defense-platform.md`, `defense-reading.md`, `defense-pursuit.md`, `transition-attack.md`, `transition-out-of-system.md`

5 pages, same pattern.

- [ ] **Step 6: Commit**
```bash
git add wiki/techniques/defense-*.md wiki/techniques/transition-*.md wiki/index.md wiki/log.md && \
  git commit -m "wave3: defense + transition techniques · W3.6 · 5 pages"
```

### Task W3.7: Position pages

**Files:** `wiki/positions/setter.md`, `outside-hitter.md`, `middle-blocker.md`, `opposite.md`, `libero.md`, `defensive-specialist.md`

For each (6 iterations):

- [ ] **Step 1 (per position): Copy template**

`cp wiki/_templates/position.md wiki/positions/<slug>.md`

- [ ] **Step 2 (per position): Fill frontmatter**

Example for `setter.md`:
```yaml
---
type: position
position: setter
role: primary-ball-handler
physical-profile: "Typically 5'10\"+ at collegiate level; quickness and hand-speed over pure height"
key-skills: [setting-hands, setting-jump, setting-backset, defense-platform, serving-float, blocking-footwork]
common-drills: []  # filled in Wave 4
related-coaches: [russ-rose, hugh-mccutcheon]
---
```

- [ ] **Step 3 (per position): Fill body**

Per template sections: Role, Physical profile, Key skills, Common drills, Position-specific coaching points, Progression by level, Sources. Link to age-lens pages (`age-lens-14u.md`, etc.) — those are Wave 5 so links are forward-references but will resolve when created.

- [ ] **Step 4 (per position): Validate**

- [ ] **Step 5: Update `index.md`**

- [ ] **Step 6: Commit**
```bash
git add wiki/positions/ wiki/index.md wiki/log.md && \
  git commit -m "wave3: position pages · W3.7 · 6 pages"
```

### Task W3.8: Systems pages — offense

**Files:** `wiki/systems-detail/offense-5-1.md`, `offense-6-2.md`, `offense-4-2.md`, `offense-6-6.md` (youth), `offense-quick.md`, `offense-pipe.md`, `offense-slide.md`, `offense-high-ball.md`

For each (8 iterations):

- [ ] **Step 1–5 per pattern**

- [ ] **Step 6: Commit**
```bash
git add wiki/systems-detail/offense-*.md wiki/index.md wiki/log.md && \
  git commit -m "wave3: offense systems · W3.8 · 8 pages"
```

### Task W3.9: Systems pages — defense, serve-receive, blocking

**Files:**
- Defense: `defense-perimeter.md`, `defense-rotation.md`, `defense-man-back.md`, `defense-middle-back.md`
- Serve-receive: `serve-receive-3-player.md`, `serve-receive-4-player.md`, `serve-receive-libero-split.md`
- Blocking: `read-blocking.md`, `swing-blocking.md`, `commit-blocking.md`

10 pages, same pattern.

- [ ] **Step 6: Commit**
```bash
git add wiki/systems-detail/ wiki/index.md wiki/log.md && \
  git commit -m "wave3: defense/SR/blocking systems · W3.9 · 10 pages"
```

### Task W3.10: Wave 3 summary

- [ ] **Step 1: Count + validate**
```bash
echo "Techniques: $(ls wiki/techniques/*.md | wc -l)"
echo "Positions:  $(ls wiki/positions/*.md | wc -l)"
echo "Systems:    $(ls wiki/systems-detail/*.md | wc -l)"
```
Target: 25–30 techniques, 6 positions, 15–20 systems.

- [ ] **Step 2: Log + commit**
```markdown

## [2026-04-22] wave3-complete | Technical core populated
Techniques: <count>. Positions: <count>. Systems: <count>.
Ready for Wave 4 (operational: practice/drills).
```
```bash
git add wiki/log.md && git commit -m "wave3: summary · W3.10"
```

---

## Wave 4 — Operational spine (practice-planning + drills)

### Task W4.1: Write `practice-planning.md` hub

**Files:**
- Create: `wiki/practice-planning.md`

- [ ] **Step 1: Copy template**

`cp wiki/_templates/hub.md wiki/practice-planning.md`

- [ ] **Step 2: Fill frontmatter**

```yaml
---
type: hub
area: practice-planning
subtopics: [session-design, periodization, microcycle, practice-ratios, game-like-training]
---
```

- [ ] **Step 3: Fill body**

Sections: Overview (methodology landscape: GMS random-practice lean, ecological-dynamics constraints lens, Japanese repetition-with-purpose), Major subtopics (linked subtopic pages to be created here or as stubs), Schools of thought (link `schools/`), Getting started (reading order for a new coach), Related areas (`season-planning.md`, `age-lens-*.md`).

- [ ] **Step 4: Create subtopic pages** (if needed as separate pages; otherwise sections within this hub suffice — choose based on length. If any subtopic exceeds ~500 words, split into its own `wiki/practice-planning-<subtopic>.md`)

- [ ] **Step 5: Update `index.md` + commit**
```bash
git add wiki/practice-planning*.md wiki/index.md wiki/log.md && \
  git commit -m "wave4: practice-planning hub · W4.1"
```

### Task W4.2: Write `season-planning.md` hub

Same pattern as W4.1. Subtopics: preseason, in-season, peaking/tournament prep, tapering, periodization by level.

**Files:** `wiki/season-planning.md`

- [ ] **Step 1–5 per pattern**

- [ ] **Step 6: Commit**
```bash
git add wiki/season-planning*.md wiki/index.md wiki/log.md && \
  git commit -m "wave4: season-planning hub · W4.2"
```

### Task W4.3: Drill library — passing-focused batch

**Files:** ~8 drill pages in `wiki/drills/` where `primary-skill: passing`.

Candidate drills (from standard volleyball pedagogy; each gets its own page):
- `butterfly-passing.md` — Butterfly Passing
- `pepper.md` — Pepper
- `serve-receive-3v3.md` — 3v3 Serve-Receive
- `weave-passing.md` — Weave Passing (continuous-motion)
- `pass-set-hit.md` — Pass-Set-Hit triplet
- `two-line-passing.md` — Two-Line Passing
- `shuttle-passing.md` — Shuttle
- `queen-of-the-court-passing.md` — Queen of the Court (passing variant)

For each (8 iterations):

- [ ] **Step 1 (per drill): Copy template**

`cp wiki/_templates/drill.md wiki/drills/<slug>.md`

- [ ] **Step 2 (per drill): Fill frontmatter**

Required fields: `primary-skill`, `techniques: [<slug>]` (≥1), `phase`, `team-size-min/max`, `duration-min`, `levels`, `equipment`, `sources: [<key>]` (≥1), `variations`.

- [ ] **Step 3 (per drill): Fill body**

Sections: Setup, Execution, Coaching points, Variations, Adaptations by level, Sources.

- [ ] **Step 4 (per drill): Validate invariants**

```bash
grep -E "^sources:" wiki/drills/<slug>.md    # ≥1 key
grep -E "^techniques:" wiki/drills/<slug>.md # ≥1 slug
```

- [ ] **Step 5 (after batch): Back-link technique pages**

For each drill, add its slug to the `related-drills:` frontmatter of the linked technique pages.

- [ ] **Step 6: Update `index.md`**

Under `## Drills` add 8 entries.

- [ ] **Step 7: Commit**
```bash
git add wiki/drills/ wiki/techniques/ wiki/index.md wiki/log.md && \
  git commit -m "wave4: drills — passing batch · W4.3 · 8 drills"
```

### Task W4.4: Drill library — setting batch (~6 drills)

Candidates: `front-back-sets.md`, `three-setter-rotation.md`, `setter-defense-transition.md`, `target-setting.md`, `jump-setting-progression.md`, `out-of-system-setting.md`.

Same pattern as W4.3.

- [ ] **Step 7: Commit**
```bash
git add wiki/drills/ wiki/techniques/ wiki/index.md wiki/log.md && \
  git commit -m "wave4: drills — setting batch · W4.4 · 6 drills"
```

### Task W4.5: Drill library — hitting batch (~6 drills)

Candidates: `approach-and-swing.md`, `high-ball-hitting.md`, `hitting-vs-block.md`, `transition-hitting.md`, `tip-and-roll.md`, `line-vs-angle-shot.md`.

Same pattern.

- [ ] **Step 7: Commit**
```bash
git add wiki/drills/ wiki/techniques/ wiki/index.md wiki/log.md && \
  git commit -m "wave4: drills — hitting batch · W4.5 · 6 drills"
```

### Task W4.6: Drill library — blocking batch (~5 drills)

Candidates: `block-footwork-ladder.md`, `read-blocking-progression.md`, `swing-block-shuffle.md`, `block-touch-drill.md`, `commit-block-trigger.md`.

Same pattern.

- [ ] **Step 7: Commit**
```bash
git add wiki/drills/ wiki/techniques/ wiki/index.md wiki/log.md && \
  git commit -m "wave4: drills — blocking batch · W4.6 · 5 drills"
```

### Task W4.7: Drill library — serving batch (~5 drills)

Candidates: `serve-targets.md`, `pressure-serving.md`, `zone-serving.md`, `jump-serve-progression.md`, `serve-receive-competition.md`.

Same pattern.

- [ ] **Step 7: Commit**
```bash
git add wiki/drills/ wiki/techniques/ wiki/index.md wiki/log.md && \
  git commit -m "wave4: drills — serving batch · W4.7 · 5 drills"
```

### Task W4.8: Drill library — defense + transition + game batch (~12 drills)

Candidates:
- Defense: `digging-lines.md`, `emergency-pursuit.md`, `six-player-defense.md`, `perimeter-coverage.md`
- Transition: `transition-rally.md`, `free-ball-to-offense.md`, `out-of-system-to-attack.md`
- Game/competition phase: `wash-drill.md`, `queen-of-the-court.md`, `king-of-the-court.md`, `cooperative-25-goal.md`, `gold-medal-scrimmage.md`

Same pattern.

- [ ] **Step 7: Commit**
```bash
git add wiki/drills/ wiki/techniques/ wiki/index.md wiki/log.md && \
  git commit -m "wave4: drills — defense/transition/game batch · W4.8 · 12 drills"
```

### Task W4.9: Drill library — warm-up + conditioning batch (~8 drills)

Candidates: `dynamic-warmup-volleyball.md`, `jump-warmup.md`, `partner-pepper-warmup.md`, `ball-control-warmup.md`, `conditioning-court-sprints.md`, `reactive-jumping.md`, `arm-care-routine.md`, `cool-down-mobility.md`.

Same pattern.

- [ ] **Step 7: Commit**
```bash
git add wiki/drills/ wiki/index.md wiki/log.md && \
  git commit -m "wave4: drills — warmup/conditioning batch · W4.9 · 8 drills"
```

### Task W4.10: Drill-library count check

- [ ] **Step 1: Count**
```bash
ls wiki/drills/*.md | wc -l
```
Expected: ≥50 drills (spec target). If short, add more to the under-represented batch.

- [ ] **Step 2: Verify invariants across library**
```bash
for f in wiki/drills/*.md; do
  if ! grep -qE "^sources: \[.+\]" "$f"; then echo "MISSING sources: $f"; fi
  if ! grep -qE "^techniques: \[.+\]" "$f"; then echo "MISSING techniques: $f"; fi
done
```
Expected: no output (all drills have sources + techniques).

- [ ] **Step 3: Log + commit**
```markdown

## [2026-04-22] wave4-complete | Operational spine populated
Drills: <count>. Hubs: practice-planning, season-planning.
All drills link ≥1 source and ≥1 technique. Ready for Wave 5 (context layer).
```
```bash
git add wiki/log.md && git commit -m "wave4: summary · W4.10"
```

---

## Wave 5 — Context layer (mental + physical + match-prep + rules + recruiting + age-lenses)

### Task W5.1: Write `mental.md` hub

**Files:** `wiki/mental.md`

- [ ] **Step 1: Copy template + fill**

Subtopics: team-culture, pressure/performance, leadership (player + coach), motivation, mental-toughness, communication, dealing with adversity. Cite GMS + McCutcheon's *Thinking Volleyball* framing heavily.

- [ ] **Step 2: Commit**
```bash
git add wiki/mental.md wiki/index.md wiki/log.md && \
  git commit -m "wave5: mental hub · W5.1"
```

### Task W5.2: Write `physical.md` hub

**Files:** `wiki/physical.md`

- [ ] **Step 1: Copy template + fill**

Subtopics: S&C foundations, jump training, mobility/flexibility, injury prevention (with explicit non-advice disclaimer), load management, sport-specific conditioning.

- [ ] **Step 2: Commit**
```bash
git add wiki/physical.md wiki/index.md wiki/log.md && \
  git commit -m "wave5: physical hub · W5.2"
```

### Task W5.3: Write `match-prep.md` hub

**Files:** `wiki/match-prep.md`

- [ ] **Step 1: Copy template + fill**

Subtopics: opponent scouting, self-scouting, stat tracking (USAV/VolleyMetrics basics), video-prep workflow, in-match adjustments.

- [ ] **Step 2: Commit**
```bash
git add wiki/match-prep.md wiki/index.md wiki/log.md && \
  git commit -m "wave5: match-prep hub · W5.3"
```

### Task W5.4: Write `rules.md` hub

**Files:** `wiki/rules.md`

- [ ] **Step 1: Copy template + fill**

Subtopics: USAV Indoor rules essentials, NCAA rule differences, scholastic rule variants, libero replacement rules, tournament format (single-day, pool → bracket, rally score, best-of-N). Cite USAV and NCAA rule PDFs (Wave 1 should have surfaced these).

- [ ] **Step 2: Commit**
```bash
git add wiki/rules.md wiki/index.md wiki/log.md && \
  git commit -m "wave5: rules hub · W5.4"
```

### Task W5.5: Write `recruiting.md` hub

**Files:** `wiki/recruiting.md`

- [ ] **Step 1: Copy template + fill**

Subtopics: college pathway (D1/D2/D3/NAIA/JUCO), NCAA recruiting timeline (critical because 14U players at national clubs begin exposure early), tournaments that matter (AAU Nationals, JVA Championships, USAV Girls' Junior Nationals), film standards, coach communication norms, camp-clinic strategy, academic-fit factors.

- [ ] **Step 2: Commit**
```bash
git add wiki/recruiting.md wiki/index.md wiki/log.md && \
  git commit -m "wave5: recruiting hub · W5.5"
```

### Task W5.6: Write `philosophy.md` hub

**Files:** `wiki/philosophy.md`

- [ ] **Step 1: Copy template + fill**

This hub is the entry into `schools/` and `coaches/`. Body: Overview (what "philosophy" means for coaching — pedagogy + worldview), Major traditions (link each school), Major coaches (link each coach profile), How schools disagree (meta-level view of key divergences — random vs. blocked, read vs. swing block, precision vs. improvisation), Getting started (reading order for a coach new to the meta-view).

- [ ] **Step 2: Commit**
```bash
git add wiki/philosophy.md wiki/index.md wiki/log.md && \
  git commit -m "wave5: philosophy hub · W5.6"
```

### Task W5.7: Write `systems.md` hub

**Files:** `wiki/systems.md`

- [ ] **Step 1: Copy template + fill**

Entry into `systems-detail/`. Overview of categories (offense, defense, serve-receive, blocking), age-appropriate system selection, how systems layer (e.g., 5-1 + read-blocking + perimeter-defense is a common collegiate stack).

- [ ] **Step 2: Commit**
```bash
git add wiki/systems.md wiki/index.md wiki/log.md && \
  git commit -m "wave5: systems hub · W5.7"
```

### Task W5.8: Write age-lens pages

**Files:** `wiki/age-lens-14u.md`, `wiki/age-lens-hs.md`, `wiki/age-lens-college.md`

For each (3 iterations):

- [ ] **Step 1 (per age-lens): Copy + fill**

Per `_templates/age-lens.md`. Critical for the user's 14U context.

- `age-lens-14u.md` — scope: 14-and-under club, emphasis on fundamentals + ball control, tempo-simplicity, NOT appropriate: full swing-block systems, complex 6-2 for non-setter OHs. Cite USAV age-appropriate guidelines.
- `age-lens-hs.md` — scope: HS varsity, emphasis on system execution, specialization, competition. Physical training appropriate.
- `age-lens-college.md` — scope: D1/D2/D3 college, full systems, position specialization, elite conditioning, recruiting-to-retention arc.

- [ ] **Step 2 (per age-lens): Fill body**

All template sections. Extensive cross-links to techniques, systems, drills, practice-planning — each with age-specific commentary.

- [ ] **Step 3: Commit**
```bash
git add wiki/age-lens-*.md wiki/index.md wiki/log.md && \
  git commit -m "wave5: age-lens pages · W5.8 · 3 pages"
```

### Task W5.9: Wave 5 summary

- [ ] **Step 1: Count root-level pages**
```bash
ls wiki/*.md | wc -l
```
Expected: 13+ (4 operational: index.md, log.md, SCHEMA.md, unsourced-queue.md + 9 hubs + 3 age-lens + possibly philosophy.md + systems.md = 18 files).

- [ ] **Step 2: Log + commit**
```markdown

## [2026-04-22] wave5-complete | Context layer populated
Hubs written. Age-lenses in place. Ready for Wave 6 (index, lint, handoff).
```
```bash
git add wiki/log.md && git commit -m "wave5: summary · W5.9"
```

---

## Wave 6 — Index, lint, handoff

### Task W6.1: Populate `index.md` completely

Catalog every page in the wiki with a one-line summary.

**Files:**
- Modify: `wiki/index.md`

- [ ] **Step 1: Generate entries per category**

For each category, list every page with a one-line summary. Bash helpers:

```bash
# Coaches
for f in wiki/coaches/*.md; do
  slug=$(basename "$f" .md)
  name=$(grep "^name:" "$f" | sed 's/name: //; s/"//g')
  echo "- [[$slug]] — $name"
done

# Schools
for f in wiki/schools/*.md; do
  slug=$(basename "$f" .md)
  name=$(grep "^name:" "$f" | sed 's/name: //; s/"//g')
  echo "- [[$slug]] — $name"
done

# (Repeat for techniques, positions, systems-detail, drills, sources)
```

Paste results under the appropriate `##` section in `wiki/index.md`.

- [ ] **Step 2: Hand-edit one-liners for clarity**

Auto-generated one-liners from `name:` fields are weak. Rewrite each to be informative in one line. Example: `[[karch-kiraly]] — three-time Olympic gold medalist (beach + indoor), current USA women's NT head coach, author of *Championship Volleyball*`.

- [ ] **Step 3: Commit**
```bash
git add wiki/index.md && git commit -m "wave6: populate full index · W6.1"
```

### Task W6.2: Lint pass 1 — frontmatter validation

- [ ] **Step 1: Validate each page type has required fields**

Script that checks required fields per type:

```bash
cd "C:/Users/SongMu/documents/claudecode/vba/bible"
errors=0
for f in wiki/coaches/*.md; do
  for field in type name country era roles schools sources; do
    if ! grep -qE "^$field:" "$f"; then
      echo "MISSING $field in $f"; errors=$((errors+1))
    fi
  done
done
for f in wiki/schools/*.md; do
  for field in type name origin core-principles sources; do
    if ! grep -qE "^$field:" "$f"; then
      echo "MISSING $field in $f"; errors=$((errors+1))
    fi
  done
done
for f in wiki/techniques/*.md; do
  for field in type skill subskill positions sources; do
    if ! grep -qE "^$field:" "$f"; then
      echo "MISSING $field in $f"; errors=$((errors+1))
    fi
  done
done
for f in wiki/drills/*.md; do
  for field in type name primary-skill techniques phase sources; do
    if ! grep -qE "^$field:" "$f"; then
      echo "MISSING $field in $f"; errors=$((errors+1))
    fi
  done
done
for f in wiki/sources/*.md; do
  for field in type source-type title author year citation-key trust-tier; do
    if ! grep -qE "^$field:" "$f"; then
      echo "MISSING $field in $f"; errors=$((errors+1))
    fi
  done
done
echo "Total errors: $errors"
```

Expected: 0 errors.

- [ ] **Step 2: Fix any missing fields** (hand-edit)

- [ ] **Step 3: Commit**
```bash
git add wiki/ && git commit -m "wave6: lint pass 1 — frontmatter validation · W6.2"
```

### Task W6.3: Lint pass 2 — cross-link invariants

- [ ] **Step 1: Check drill → source + technique invariant (rule 1)**

```bash
for f in wiki/drills/*.md; do
  s=$(grep -E "^sources:" "$f" | grep -oE "\[[^]]+\]" | tr -d '[]')
  t=$(grep -E "^techniques:" "$f" | grep -oE "\[[^]]+\]" | tr -d '[]')
  if [ -z "$s" ]; then echo "DRILL no source: $f"; fi
  if [ -z "$t" ]; then echo "DRILL no technique: $f"; fi
done
```

- [ ] **Step 2: Check coach → school + source (rule 2)**

```bash
for f in wiki/coaches/*.md; do
  s=$(grep -E "^schools:" "$f" | grep -oE "\[[^]]+\]" | tr -d '[]')
  src=$(grep -E "^sources:" "$f" | grep -oE "\[[^]]+\]" | tr -d '[]')
  if [ -z "$s" ]; then echo "COACH no school: $f"; fi
  if [ -z "$src" ]; then echo "COACH no source: $f"; fi
done
```

- [ ] **Step 3: Check citation-key resolution (rule 6)**

```bash
# Collect all citation-keys defined in sources/
declare -A keys
for f in wiki/sources/*.md; do
  k=$(grep "^citation-key:" "$f" | sed 's/citation-key: //')
  keys[$k]=1
done
# Find all [citation-key] references in wiki/ body text
grep -rnoE "\[[a-z0-9-]+\]" wiki/ --include="*.md" | while read line; do
  key=$(echo "$line" | grep -oE "\[[a-z0-9-]+\]" | tr -d '[]')
  # Skip common false positives: [unsourced], [transcript-unavailable], [translation-needed]
  case "$key" in
    unsourced|transcript-unavailable|translation-needed) continue ;;
  esac
  if [ -z "${keys[$key]}" ]; then echo "UNRESOLVED citation: $line"; fi
done
```

- [ ] **Step 4: Check orphan pages (rule 5)**

```bash
# For each wiki page, count inbound [[wikilinks]]
for f in wiki/**/*.md wiki/*.md; do
  slug=$(basename "$f" .md)
  if [ "$slug" = "index" ] || [ "$slug" = "log" ] || [ "$slug" = "SCHEMA" ] || [ "$slug" = "unsourced-queue" ]; then continue; fi
  count=$(grep -r "\[\[$slug\]\]\|\[\[$slug|" wiki/ --include="*.md" | grep -v "$f" | wc -l)
  if [ "$count" -eq 0 ]; then echo "ORPHAN: $f"; fi
done
```

- [ ] **Step 5: Fix violations**

For each violation, patch the offending page to add the missing link or source.

- [ ] **Step 6: Commit**
```bash
git add wiki/ && git commit -m "wave6: lint pass 2 — cross-link invariants · W6.3"
```

### Task W6.4: Lint pass 3 — source-page-exists-before-citation (rule 4)

- [ ] **Step 1: Check every frontmatter `sources:` entry resolves to a source page**

```bash
for f in $(find wiki -name "*.md" -not -path "wiki/sources/*"); do
  # Extract source slugs from sources: frontmatter field
  srcs=$(grep -A1 "^sources:" "$f" | tr -d '[]' | tr ',' '\n' | sed 's/^ *//; s/^- *//' | grep -v "^$\|^sources:")
  for s in $srcs; do
    if [ ! -f "wiki/sources/$s.md" ]; then
      echo "MISSING source page: $s referenced in $f"
    fi
  done
done
```

- [ ] **Step 2: Fix**

Create any missing source pages. If a citation was fabricated (no real source), replace with `[unsourced]` and add to queue.

- [ ] **Step 3: Commit**
```bash
git add wiki/ && git commit -m "wave6: lint pass 3 — source existence · W6.4"
```

### Task W6.5: Populate `unsourced-queue.md`

- [ ] **Step 1: Collect all `[unsourced]` tags**

```bash
grep -rnH "\[unsourced\]" wiki/ --include="*.md"
```

- [ ] **Step 2: For each hit, add entry to `unsourced-queue.md`**

Per-hit entry format (from W0.3 template):
```markdown
### wiki/<path>.md
- **Claim:** <sentence containing [unsourced]>
- **Why unsourced:** <best hypothesis — couldn't find Tier 1/2, specific claim, etc.>
- **Research hypothesis:** <specific source/author/paper to hunt>
- **Added:** 2026-04-22
```

- [ ] **Step 3: Commit**
```bash
git add wiki/unsourced-queue.md && git commit -m "wave6: seed unsourced-queue · W6.5"
```

### Task W6.6: Run scenario tests (spec §7.2)

- [ ] **Step 1: Test 1 — 14U serve-receive practice plan**

In the project, simulate the query: *"Build me a 90-minute 14U practice focused on serve-receive, skill phase, with both GMS and Japanese perspectives represented."*

Execute:
```bash
# Verify expected pages exist to answer the question
ls wiki/age-lens-14u.md wiki/schools/gold-medal-squared.md wiki/schools/japanese-training.md wiki/practice-planning.md
# Verify ≥5 drills with phase=skill and primary-skill=passing exist and are 14U-appropriate
grep -l "primary-skill: passing" wiki/drills/*.md | while read f; do
  if grep -qE "^phase: skill" "$f" && grep -qE "levels:.*14u" "$f"; then echo "OK: $f"; fi
done | wc -l
```
Expected: ≥5 drills.

- [ ] **Step 2: Test 2 — Karch vs. GMS blocking comparison**

```bash
ls wiki/coaches/karch-kiraly.md wiki/schools/gold-medal-squared.md wiki/techniques/blocking-footwork.md wiki/systems-detail/read-blocking.md wiki/systems-detail/swing-blocking.md
```
Expected: all files exist.

Manually spot-check that both schools' views on blocking are represented with citations.

- [ ] **Step 3: Test 3 — random vs. blocked practice evidence**

```bash
ls wiki/schools/ecological-dynamics.md wiki/schools/block-vs-random-practice.md raw/research/
```
Expected: school pages exist, `raw/research/` has Tier 1 motor-learning papers.

- [ ] **Step 4: Record findings**

If any test surfaces gaps, add to `wiki/unsourced-queue.md` and flag for user at CP4.

- [ ] **Step 5: Commit**
```bash
git add wiki/unsourced-queue.md && git commit -m "wave6: scenario tests + gap tracking · W6.6"
```

### Task W6.7: Wave 6 summary + log finalization

- [ ] **Step 1: Count all wiki pages**

```bash
find wiki -name "*.md" -not -path "wiki/_templates/*" | wc -l
```
Expected: 160–200 per spec §6.2.

- [ ] **Step 2: Final log entry**

Append:
```markdown

## [2026-04-22] wave6-complete | Bootstrap done
Total wiki pages: <count>.
Lint: all invariants passing.
Scenario tests: <pass/gaps-noted>.
Unsourced queue: <N> entries pending future research passes.

The wiki is ready for day-one use. Handoff to user for CP4 review.
```

- [ ] **Step 3: Commit**
```bash
git add wiki/log.md && git commit -m "wave6: summary and bootstrap completion · W6.7"
```

### Task W6.8 (CHECKPOINT 4): User reviews full wiki

- [ ] **Step 1: Present summary to user**

Message:
"**CP4:** Bootstrap complete. Wiki stats:
- Total pages: `<count>`
- Coaches: `<count>` · Schools: `<count>` · Techniques: `<count>` · Positions: `<count>` · Systems: `<count>` · Drills: `<count>` · Sources: `<count>`
- Hubs: `<list>` · Age-lenses: 14U, HS, college
- Unsourced-queue entries: `<N>` (for later research passes)
- Scenario tests: `<pass/gaps-noted with specifics>`

Ready for review. Please open the wiki in Obsidian (point the vault at `wiki/`). Suggested tour:

1. Read `index.md`
2. Read `SCHEMA.md` (refresh)
3. Spend 10 minutes following wikilinks from `philosophy.md` → a few coach profiles → a few school pages
4. Spot-check 3–4 technique pages and 3–4 drills
5. Read `age-lens-14u.md` thoroughly (your primary daily context)
6. Check graph view for structural health

Flag anything that needs revision. Sign off = bootstrap accepted and wiki goes into living-maintenance mode."

- [ ] **Step 2: Wait for user approval**

Revisions per feedback. Commit revisions with `wave6: post-CP4 revisions`.

- [ ] **Step 3: Final commit**

After CP4 approval:
```bash
git add -A && git commit -m "chore: bootstrap complete · CP4 approved · wiki live"
```

---

## Self-review notes (author's pre-handoff pass)

**Spec coverage check:**
- §1 context & scope → captured in plan header and CLAUDE.md (W0.1)
- §2 architecture → Pre-Wave 0.2 scaffolding + W0.1 pointer + W0.2 SCHEMA
- §3 page taxonomy & frontmatter → W0.2 SCHEMA + W0.4 templates + per-page tasks Waves 2–5
- §4 SCHEMA.md contents → W0.2 spec out in full
- §5 workflows → W0.2 (copied into SCHEMA §10) + used operationally in Wave 1 ingest, W6.2–W6.5 lint
- §6.1 continuous sprint → tasks chained linearly, checkpoints at CP1/CP2/CP3/CP4
- §6.2 deliverable targets → Wave-end count-checks in W1.10, W2.7, W3.10, W4.10, W5.9, W6.7
- §6.3 wave structure → Waves 0–6 mapped to tasks
- §6.4 user checkpoints → W0.6, W1.11, W2.8, W6.8
- §6.5 copyright caveats → referenced in W1.2 (books) and consistent across raw/books/ handling
- §7.1 done checklist → validated across W6.2–W6.7
- §7.2 scenario tests → W6.6
- §7.3 living-wiki signals → meta; lives in SCHEMA and post-CP4 mode
- §7.4 non-goals → respected (no custom CLI, no beach, no certs, no webapp)

**Open items from §8:**
- Git init: covered in Task 0.1 (first task of plan)
- User-owned books: handling documented in W1.2 step 2
- Japanese translation: flagged in W1.6 step 2
- Version control: ensured via Task 0.1

**Known risks:**
1. Web research in Wave 1 depends on WebFetch/WebSearch availability and rate limits. If Wave 1 cannot produce 30+ sources, the user can be asked to contribute known-good URLs as a short unblocking step.
2. YouTube caption fetching may require manual intervention if WebFetch can't extract captions directly. In that case, substitute with video description + clip notes and tag `[transcript-unavailable]`.
3. Scenario tests in W6.6 are structural (file-existence + frontmatter checks) rather than LLM-answer-quality tests. A deeper test would require user in the loop — this is intentional and covered by CP4 user review.

---

**Plan length:** 8 task groups (Pre + Waves 0–6), ~60 discrete tasks with bite-sized steps inside each. Total expected commits: ~60–70.

**End of implementation plan.**
