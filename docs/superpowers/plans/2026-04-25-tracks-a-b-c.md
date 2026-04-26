# Wiki Tracks A+B+C — "Boil-the-Ocean" Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the five missing major coaching traditions, deepen the sports-science source base, and build the operational layer the wiki has been queueing — turning the wiki from "comprehensive reference + working tool" into "all-volleyball-coaching-knowledge-in-the-world reference + complete coaching workstation."

**Architecture:** Three sequential parallel-agent dispatches with internal lint checkpoints. Dispatch A lands content for missing schools (Polish/French/Serbian/Cuban/Korean) plus their core coaches and federation stubs. Dispatch B lands sports-science depth (50 research papers across 5 clusters) plus 15 definitive book ingests, then a citation-spread polish pass into existing methodology and technique pages. Dispatch C lands the operational layer (macrocycles, microcycles, match-prep templates, tryout rubrics, club-ops docs) plus SCHEMA additions for two new page-type extensions.

**Tech Stack:** Markdown + YAML frontmatter (Obsidian-compatible), Python 3 + pyyaml (lint extensions), `tools/transcribe.py` (already shipped), git. WebFetch for source ingestion; no new external dependencies.

**Spec source:** `docs/superpowers/specs/2026-04-25-tracks-a-b-c-design.md`

---

## File structure

### New content files (Track A — 23 wiki pages)
- `wiki/schools/polish-school.md`, `wiki/schools/french-school.md`, `wiki/schools/serbian-school.md`, `wiki/schools/cuban-school.md`, `wiki/schools/korean-school.md` (5)
- `wiki/coaches/andrea-anastasi.md`, `wiki/coaches/vital-heynen.md`, `wiki/coaches/stephane-antiga.md`, `wiki/coaches/nikola-grbic.md` (Polish — 4)
- `wiki/coaches/laurent-tillie.md`, `wiki/coaches/andrea-giani.md` (French — 2)
- `wiki/coaches/zoran-terzic.md`, `wiki/coaches/slobodan-kovac.md`, `wiki/coaches/igor-kolakovic.md` (Serbian — 3)
- `wiki/coaches/eugenio-george.md`, `wiki/coaches/antonio-perdomo.md` (Cuban — 2)
- `wiki/coaches/mido-cha.md`, `wiki/coaches/kim-hyung-shil.md` (Korean — 2)
- `wiki/schools/pzps-poland.md`, `wiki/schools/ffv-france.md`, `wiki/schools/oss-serbia.md`, `wiki/schools/fcv-cuba.md`, `wiki/schools/kva-korea.md` (5 federation stubs)

### New content files (Track B — ~65 source pages)
- `wiki/sources/<author>-<year>-<short-slug>.md` × 50 (research papers across 5 clusters)
- `wiki/sources/notes-<author>-<year>-<slug>.md` × 15 (book notes)
- `raw/articles/<slug>.md` × 50 (paired raw research)
- `raw/books/notes-<slug>.md` × 15 (book notes raw files)

### New content files (Track C — 27 wiki pages + 2 SCHEMA additions)
- `wiki/practice-plans/<level>-<duration>-<arc>-macrocycle.md` × 5
- `wiki/practice-plans/<context>-week.md` (or similar) × 5 microcycles
- `wiki/ops/match-prep-<slug>.md` × 5
- `wiki/ops/tryout-rubric-<level>.md` × 4
- `wiki/ops/club-ops-<slug>.md` × 8

### Modified files
- `wiki/SCHEMA.md` — extend §3.10 with `scope` field; add §3.11 ops-doc page type; extend §4 enum glossary
- `tools/lint.py` — add `ops-doc` to REQUIRED_FIELDS; extend ENUM_VALUES with new enums
- `wiki/index.md` — add Skill hubs (already done) + Macrocycles + Microcycles + Operations sections
- `wiki/log.md` — per-dispatch entries
- `raw/INDEX.md` — entries for all new raw files
- Existing methodology + technique + age-lens pages — citation-spread polish from Track B
- `wiki/coaches/julio-velasco.md`, `wiki/coaches/giovanni-guidetti.md` — cross-link to new Italian-school overlap content from Track A French school (Giani)

### Shared brief templates (referenced repeatedly)
Defined once at the top of each dispatch section so individual tasks can reference them rather than inlining.

---

## Dispatch A — Missing schools

Single parallel dispatch of ~25 agents.

---

### Task A.1: School-page brief template (reference for Tasks A.2–A.6)

**Shared brief (apply to every school-page task):**

> You are writing a new school-of-thought page for the Volleyball Coaching Bible wiki at `C:/Users/SongMu/documents/claudecode/vba/bible/`. **Read `wiki/SCHEMA.md` §3.3 (school-page contract — heavy citation, ~2000-2500 words) + §4 (frontmatter) + §5 (citation policy) + §6 (cross-link invariants) + §8 (voice) before writing anything.** Read 1-2 existing school pages for voice (`wiki/schools/brazilian-school.md`, `wiki/schools/italian-school.md`).
>
> **Required body sections (per SCHEMA §3.3):** `## Overview`, `## Core principles`, `## Methodology`, `## Notable practitioners`, `## Contrasts with other schools`, `## Critiques and limitations`, `## Sources`.
>
> **Frontmatter:**
> ```yaml
> ---
> type: school
> name: <Name>
> origin: <Country/region>
> founders: [<coach-slugs if known>]
> core-principles: [<7-12 principles>]
> associated-coaches: [<coach-slugs>]   # match each coach's schools: field bidirectionally
> related-schools: [<related-school-slugs>]
> sources: [<citation-keys>]              # ≥1 required
> ---
> ```
>
> **Heavy citation per SCHEMA §5** — inline `[citation-key]` after each non-generic claim. Do not fabricate; use `[unsourced]` + queue entry per SCHEMA §5 if you can't ground a claim.
>
> **Sources to research via WebFetch first:** for each coach mentioned, confirm Wikipedia bio is accessible; for the federation, fetch the federation about-page if available; for major-competition results, fetch the relevant FIVB/CEV result pages. Save raw fetches to `raw/articles/<slug>.md` per SCHEMA §8.1; create paired `wiki/sources/<citation-key>.md` per SCHEMA §3.8 BEFORE citing.
>
> **Cross-link expectations:** every coach mentioned must wikilink to their `wiki/coaches/` page (created in parallel by Tasks A.7-A.20). Federations link to `wiki/schools/<federation-slug>.md` (Tasks A.21). Cross-references to other schools (Italian/Russian/Brazilian/Japanese as relevant) wikilink existing pages.
>
> **When done:** commit with `feat(wiki): add <school-slug> school page`.

---

### Task A.2: `wiki/schools/polish-school.md`

**Files:** Create `wiki/schools/polish-school.md` + 5-8 supporting source pages under `wiki/sources/` + raw fetches under `raw/articles/`.

**Per-school specifics:**
- Origin: Poland; PZPS governing body; PlusLiga + Tauron Liga
- Founders: [andrea-anastasi] (modernization era) — though Polish lineage extends back further
- Core-principles: aggressive-jump-serving, pin-block-discipline, server-pin-pressure, deep-perimeter-defense, italian-methodology-synthesis, generational-talent-pipeline
- Associated-coaches: [andrea-anastasi, vital-heynen, stephane-antiga, nikola-grbic]
- Related-schools: [italian-school, serbian-school]
- Result anchors: 2014 World Champions (Antiga, host country), 2018 + 2022 World Champions (Heynen + Grbić), 2024 Paris silver (Grbić), multiple European Championships
- Style anchors: Heynen's blocking-and-serving frame; Grbić's setter-pressure tempo system

**Research pathway (WebFetch):**
- `https://en.wikipedia.org/wiki/Poland_men%27s_national_volleyball_team`
- `https://en.wikipedia.org/wiki/Polish_Volleyball_Federation`
- `https://en.wikipedia.org/wiki/PlusLiga`
- FIVB World Championship retrospectives (2014/2018/2022)
- Heynen + Grbić CEV/FIVB feature articles

- [ ] **Step 1:** Apply the shared brief from Task A.1 with the specifics above.
- [ ] **Step 2:** Run `python tools/lint.py 2>&1 | tail -2` and confirm no broken-wikilink regression on this page (some forward-refs to coach pages are expected; commit will land before coach pages).
- [ ] **Step 3:** Commit with `feat(wiki): add polish-school page` (use `--no-verify` if pre-commit hook over-blocks on false positives).

---

### Task A.3: `wiki/schools/french-school.md`

**Files:** Create `wiki/schools/french-school.md` + supporting source pages.

**Per-school specifics:**
- Origin: France; FFV governing body; Pro Ligue (LNV)
- Founders: [laurent-tillie] (Tokyo gold-medal modernizer) — earlier French volleyball history exists but Tillie's program is the modern identity anchor
- Core-principles: slide-from-multiple-rotations, OH-backrow-attack-high-frequency, second-tempo-middles-from-average-passes, tactical-creativity, multi-position-versatility
- Associated-coaches: [laurent-tillie, andrea-giani]
- Related-schools: [italian-school] (Giani is Italian; bidirectional)
- Result anchors: 2020 Tokyo men's Olympic gold (Tillie), 2024 Paris semifinal (Giani), multiple European Championships, Volleyball Nations League titles
- Style anchors: Tillie's tempo-multidirectional offense; Giani's player-experience-driven coaching

**Research pathway:**
- `https://en.wikipedia.org/wiki/France_men%27s_national_volleyball_team`
- `https://en.wikipedia.org/wiki/French_Volleyball_Federation`
- `https://en.wikipedia.org/wiki/Laurent_Tillie`
- `https://en.wikipedia.org/wiki/Andrea_Giani`
- FIVB Tokyo 2020 final retrospective; Volleyball World feature articles

Same 3-step execution pattern as Task A.2.

---

### Task A.4: `wiki/schools/serbian-school.md`

**Files:** Create `wiki/schools/serbian-school.md` + supporting sources.

**Per-school specifics:**
- Origin: Serbia (post-Yugoslavia); OSS governing body
- Founders: [zoran-terzic] (women's NT modernizer) — Yugoslav-era roots predate
- Core-principles: discipline-first-defense, dig-to-set-anywhere-libero, MB-priority-attacker, ground-defense-emphasis, pro-export-pipeline
- Associated-coaches: [zoran-terzic, slobodan-kovac, igor-kolakovic]
- Related-schools: [italian-school, russian-school]
- Result anchors: 1980 Moscow men's gold (Yugoslav), 2000 Sydney men's gold (Kovač as player + coach), 2016 Rio women's silver (Terzić), multiple women's World Championships and European Championships under Terzić
- Style anchors: Terzić's defensive identity; the Serbian setter tradition (Grbić as player-then-coach)

**Research pathway:**
- `https://en.wikipedia.org/wiki/Serbia_women%27s_national_volleyball_team`
- `https://en.wikipedia.org/wiki/Serbia_men%27s_national_volleyball_team`
- `https://en.wikipedia.org/wiki/Volleyball_Federation_of_Serbia`
- `https://en.wikipedia.org/wiki/Zoran_Terzi%C4%87`
- `https://en.wikipedia.org/wiki/Slobodan_Kova%C4%8D`

Same 3-step execution.

---

### Task A.5: `wiki/schools/cuban-school.md`

**Files:** Create `wiki/schools/cuban-school.md` + supporting sources.

**Per-school specifics:**
- Origin: Cuba; FCV governing body
- Founders: [eugenio-george] (women's dynasty architect)
- Core-principles: extreme-physicality, jump-serving-early-adoption, high-tempo-power-offense, centralized-NT-development, generational-tall-roster
- Associated-coaches: [eugenio-george, antonio-perdomo]
- Related-schools: [russian-school, brazilian-school]
- Result anchors: 1992 Barcelona + 1996 Atlanta + 2000 Sydney women's golds (George), 1990/2002 women's World Championship silvers, 1976 Montreal men's bronze (Perdomo era)
- Style anchors: Cuban women's program as the tall-and-powerful template that influenced subsequent generations

**Research pathway:**
- `https://en.wikipedia.org/wiki/Cuba_women%27s_national_volleyball_team`
- `https://en.wikipedia.org/wiki/Eugenio_George`
- `https://en.wikipedia.org/wiki/Mireya_Luis` (player anchor)
- FIVB Hall of Fame entries
- Olympic.com 1992-2000 retrospectives

Same 3-step execution.

---

### Task A.6: `wiki/schools/korean-school.md`

**Files:** Create `wiki/schools/korean-school.md` + supporting sources.

**Per-school specifics:**
- Origin: South Korea; KVA governing body; V-League (women's pro internationally followed)
- Founders: [mido-cha] (historic) — modernized by various
- Core-principles: precision-passing, libero-driven-defense, multiple-tempo-MB-attacks, OH-backrow-as-normal-option, smaller-stature-tactical-adaptation, international-transfer-pipeline (Kim Yeon-koung)
- Associated-coaches: [mido-cha, kim-hyung-shil]
- Related-schools: [japanese-training, italian-school] (Lavarini Italian→Korean transfer)
- Result anchors: 1976 Montreal women's bronze, 2012 London + 2020 Tokyo women's 4th-place finishes, multiple Asian Championships
- Style anchors: Korean women's NT as the precision-and-tempo template scaled to non-tall roster

**Research pathway:**
- `https://en.wikipedia.org/wiki/South_Korea_women%27s_national_volleyball_team`
- `https://en.wikipedia.org/wiki/Korea_Volleyball_Association`
- `https://en.wikipedia.org/wiki/Kim_Yeon-koung` (player anchor)
- `https://en.wikipedia.org/wiki/V-League_(South_Korea)`
- Stefano Lavarini coaching feature articles

Same 3-step execution.

---

### Task A.7: Coach-profile brief template (reference for Tasks A.8–A.20)

**Shared brief (apply to every coach-profile task):**

> You are writing a new coach profile per SCHEMA §3.2. **Read `wiki/SCHEMA.md` §3.2, §4, §5 (HEAVY citation), §6, §8.** Read 1-2 existing coach profiles for voice (`wiki/coaches/karch-kiraly.md` for full-length; `wiki/coaches/yasutaka-matsudaira.md` for an international historical profile).
>
> **Required body sections:** Overview, Coaching career, Core teaching principles, Contributions to the game, Quotes & representative passages, Sources.
>
> **Frontmatter:**
> ```yaml
> ---
> type: coach
> name: <Full Name>
> country: <country>
> era: <years or era label>
> roles: [<roles>]
> schools: [<slug>, ...]   # ≥1 required — must include the parent school from Track A
> sources: [<citation-key>, ...]   # ≥1 required
> tags: [<optional>]
> ---
> ```
>
> **Source-page-first rule:** before citing `[citation-key]` in the body, ensure `wiki/sources/<citation-key>.md` exists. WebFetch the source, save raw to `raw/articles/<slug>.md`, create the source page per SCHEMA §3.8, THEN cite.
>
> **Length target:** ~1500 words for full profiles, ~800 words for brief profiles (see per-coach specifics).
>
> **Honesty:** if source base is thin after research, use `[unsourced]` + queue entry per SCHEMA §5 honesty rules. Do NOT fabricate.
>
> **Cross-link expectations:** wikilink to the parent school page (Tasks A.2-A.6) plus to any related coaches already on the wiki (e.g., a Polish coach who worked with Italian methodology can wikilink `[[julio-velasco]]`).
>
> **When done:** commit `feat(wiki): add <slug> coach profile`.

---

### Task A.8: Andrea Anastasi profile (full, ~1500w)

**Files:** Create `wiki/coaches/andrea-anastasi.md` + supporting sources.

**Per-coach specifics:**
- name: Andrea Anastasi
- country: Italy/Poland (dual identity)
- era: 1990s-present
- roles: [player, head-coach, italian-mens-nt-hc, polish-mens-nt-hc]
- schools: [italian-school, polish-school]
- Career anchors: Italian men's NT player; Italian men's NT HC; Polish men's NT HC 2009-2013; Spain men's NT HC; club coaching across Europe
- Source anchors: Wikipedia bio, FIVB feature articles, CEV interviews, Polish federation history
- Contribution: bringing Italian-Generazione methodology to Polish men's NT modernization

**Research pathway:**
- `https://en.wikipedia.org/wiki/Andrea_Anastasi`
- FIVB / Volleyball World feature articles
- Polish Volleyball Federation history pages

- [ ] **Step 1:** Apply Task A.7 brief with these specifics.
- [ ] **Step 2:** Lint check.
- [ ] **Step 3:** Commit `feat(wiki): add andrea-anastasi coach profile`.

---

### Task A.9: Vital Heynen profile (full, ~1500w)

**Per-coach specifics:**
- name: Vital Heynen
- country: Belgium
- era: 1990s-present
- roles: [player, head-coach, polish-mens-nt-hc, german-mens-nt-hc]
- schools: [polish-school]
- Career: Belgian player; German men's NT HC 2011-2017; Polish men's NT HC 2018-2022; **2018 + 2022 World Champion architect**
- Source anchors: Wikipedia bio, CEV/FIVB features, 2018+2022 World Championship retrospectives
- Contribution: blocking-and-serving frame; 2-time World Champion coach

**Research pathway:** `https://en.wikipedia.org/wiki/Vital_Heynen` + FIVB/CEV features.

Same 3-step execution.

---

### Task A.10: Stéphane Antiga profile (brief, ~800w)

**Per-coach specifics:**
- name: Stéphane Antiga
- country: France
- era: 2000s-present
- roles: [player, head-coach, polish-mens-nt-hc]
- schools: [polish-school, french-school]
- Career: French men's NT player; Polish men's NT HC 2014-2018; **2014 World Champion architect** (host country)
- Source anchors: Wikipedia bio, FIVB 2014 retrospective

**Research pathway:** `https://en.wikipedia.org/wiki/St%C3%A9phane_Antiga`.

Same 3-step execution.

---

### Task A.11: Nikola Grbić profile (full, ~1500w)

**Per-coach specifics:**
- name: Nikola Grbić
- country: Serbia
- era: 1990s-present
- roles: [player, head-coach, polish-mens-nt-hc, serbian-mens-nt-hc]
- schools: [polish-school, serbian-school]
- Career: Serbian setter (legendary); 2000 Sydney gold as player; Serbian men's NT HC; Polish men's NT HC 2022-present
- Source anchors: Wikipedia bio, FIVB 2022 + 2024 retrospectives, CEV features
- Contribution: setter-perspective coaching, tempo-pressure system, 2024 Paris silver

**Research pathway:** `https://en.wikipedia.org/wiki/Nikola_Grbi%C4%87`.

Same 3-step execution.

---

### Task A.12: Laurent Tillie profile (full, ~1500w)

**Per-coach specifics:**
- name: Laurent Tillie
- country: France
- era: 1980s-present
- roles: [player, head-coach, french-mens-nt-hc]
- schools: [french-school]
- Career: French men's NT player; French men's NT HC 2012-2021; **2020 Tokyo Olympic gold architect**; later club roles
- Source anchors: Wikipedia bio, FIVB Tokyo 2020 retrospective, French federation features
- Contribution: tempo-multidirectional offense; OH-backrow as normal option; Tokyo gold

**Research pathway:** `https://en.wikipedia.org/wiki/Laurent_Tillie`.

Same 3-step execution.

---

### Task A.13: Andrea Giani profile (full, ~1500w)

**Per-coach specifics:**
- name: Andrea Giani
- country: Italy/France
- era: 1980s-present
- roles: [player, head-coach, slovenian-mens-nt-hc, french-mens-nt-hc]
- schools: [italian-school, french-school]
- Career: Italian men's NT player (Generazione di Fenomeni — under Velasco); Slovenian men's NT HC; current French men's NT HC 2021-present; FIVB Hall of Fame as player
- Source anchors: Wikipedia bio, FIVB Hall of Fame, CEV/FIVB features

**Research pathway:** `https://en.wikipedia.org/wiki/Andrea_Giani`.

Same 3-step execution.

---

### Task A.14: Zoran Terzić profile (full, ~1500w)

**Per-coach specifics:**
- name: Zoran Terzić
- country: Serbia
- era: 1990s-present
- roles: [head-coach, serbian-womens-nt-hc]
- schools: [serbian-school]
- Career: Serbian women's NT HC 1998-2017+; multiple World Championship + European Championship titles; 2016 Rio silver
- Source anchors: Wikipedia bio, FIVB retrospectives on Serbian women's NT, CEV features
- Contribution: dean of Serbian women's volleyball; defensive-discipline identity

**Research pathway:** `https://en.wikipedia.org/wiki/Zoran_Terzi%C4%87`.

Same 3-step execution.

---

### Task A.15: Slobodan Kovač profile (brief, ~800w)

**Per-coach specifics:**
- name: Slobodan Kovač
- country: Serbia
- era: 1990s-present
- roles: [player, head-coach, serbian-mens-nt-hc]
- schools: [serbian-school]
- Career: Yugoslav/Serbian men's NT player; **2000 Sydney gold as player**; Serbian men's NT HC stints
- Source anchors: Wikipedia bio, 2000 Sydney retrospective

**Research pathway:** `https://en.wikipedia.org/wiki/Slobodan_Kova%C4%8D`.

Same 3-step execution.

---

### Task A.16: Igor Kolaković profile (brief, ~800w)

**Per-coach specifics:**
- name: Igor Kolaković
- country: Montenegro/Serbia
- era: 1990s-present
- roles: [head-coach, multiple-mens-nts-hc]
- schools: [serbian-school]
- Career: men's NT HC roles across Iran, Bosnia, others; modern coaching tradition
- Source anchors: Wikipedia bio, FIVB feature articles

**Research pathway:** `https://en.wikipedia.org/wiki/Igor_Kolakovi%C4%87`.

Same 3-step execution.

---

### Task A.17: Eugenio George profile (full, ~1500w)

**Per-coach specifics:**
- name: Eugenio George Lafita
- country: Cuba
- era: 1980s-2000s
- roles: [head-coach, cuban-womens-nt-hc]
- schools: [cuban-school]
- Career: Cuban women's NT HC 1986-2008; **3 consecutive Olympic golds (1992-2000)**; multiple World Championship medals
- Source anchors: Wikipedia bio, FIVB Hall of Fame, Olympic.com retrospectives
- Contribution: power-and-tempo template; jump-serving early adoption; centralized NT development model

**Research pathway:** `https://en.wikipedia.org/wiki/Eugenio_George`.

Same 3-step execution.

---

### Task A.18: Antonio Perdomo profile (brief, ~800w)

**Per-coach specifics:**
- name: Antonio Perdomo
- country: Cuba
- era: 1970s-1990s
- roles: [head-coach, cuban-mens-nt-hc]
- schools: [cuban-school]
- Career: Cuban men's NT HC; 1976 Montreal Olympic men's bronze era
- Source anchors: Wikipedia bio if available; FIVB historical records; Cuban Federation history pages

**Research pathway:** Wikipedia + FIVB 1976 retrospective. If sources are very thin, target 600w and tag liberally.

Same 3-step execution.

---

### Task A.19: Mido Cha profile (brief, ~800w)

**Per-coach specifics:**
- name: Mido Cha (차미도) — verify romanization via WebFetch
- country: South Korea
- era: 1970s-1990s (verify)
- roles: [head-coach, korean-womens-nt-hc]
- schools: [korean-school]
- Career: historic Korean women's coaching figure
- Source anchors: KVA history pages, Wikipedia (Korean + English), historical features

**Research pathway:** Search KVA + Wikipedia for Korean women's NT history. If first-name + romanization is uncertain, verify before committing the slug. Tag thinly-sourced claims `[unsourced]`.

Same 3-step execution.

---

### Task A.20: Kim Hyung-shil profile (brief, ~800w)

**Per-coach specifics:**
- name: Kim Hyung-shil — verify romanization
- country: South Korea
- era: 2000s-present
- roles: [head-coach, korean-womens-nt-hc]
- schools: [korean-school]
- Career: Korean women's NT HC stints; modern coaching tradition
- Source anchors: KVA, Wikipedia, FIVB features

**Research pathway:** Search Korean women's NT recent history; verify name romanization.

Same 3-step execution.

---

### Task A.21: Federation/league stub batch

**Files:** Create 5 files in `wiki/schools/`:
- `pzps-poland.md`, `ffv-france.md`, `oss-serbia.md`, `fcv-cuba.md`, `kva-korea.md`

**Per-stub specifics (apply to all 5, varying per-federation):**

Frontmatter (shared shape):
```yaml
---
type: school
name: <Federation Full Name>
origin: <Country>
founders: []
core-principles: []
associated-coaches: [<all coaches from this country, e.g., for PZPS: andrea-anastasi, vital-heynen, stephane-antiga, nikola-grbic>]
related-schools: [<parent school slug>]
sources: [<≥1 — federation-page Wikipedia or official>]
---
```

Body: institutional-tradition stub per the existing `wiki/schools/penn-state.md` / `wiki/schools/florida.md` pattern. ~150-300 words. Each gets:
- `## Overview` paragraph (governing body, founding, scope, key competitions managed)
- `## Notable practitioners` listing all associated coaches as wikilinks
- `## Sources` with the federation Wikipedia/official link

**Per-federation specifics:**

- **PZPS Poland** — Polski Związek Piłki Siatkowej, founded 1928, manages PlusLiga + Tauron Liga; Spała training centre. Source: Wikipedia + pzps.pl.
- **FFV France** — Fédération Française de Volley, founded 1936, manages Pro Ligue (LNV); CREPS regional training centres. Source: Wikipedia + ffvb.org.
- **OSS Serbia** — Odbojkaški Savez Srbije; post-Yugoslav successor (1949 Yugoslav origins); manages SuperLiga. Source: Wikipedia + ossrb.org.
- **FCV Cuba** — Federación Cubana de Voleibol; centralized national-team development model. Source: Wikipedia + Cuban Olympic federation pages.
- **KVA Korea** — Korea Volleyball Association, founded 1946; manages V-League. Source: Wikipedia + kovo.co.kr.

- [ ] **Step 1:** Read SCHEMA §3.3 + the existing `penn-state.md` / `florida.md` stubs for pattern.
- [ ] **Step 2:** Use Glob/Read to verify which coach profiles exist (some may still be in-flight).
- [ ] **Step 3:** Write all 5 stubs with full frontmatter + minimal body.
- [ ] **Step 4:** Run lint.
- [ ] **Step 5:** Commit `feat(wiki): add 5 federation stubs (PZPS, FFV, OSS, FCV, KVA)`.

---

### Task A.22: Cross-link + index update + log entry

**Files:** Modify `wiki/index.md`, `wiki/log.md`, possibly some existing pages.

- [ ] **Step 1: Add new schools section to `wiki/index.md`**

In the Schools section, add a new subsection after the existing Contrasting-school set:

```markdown
### Boil-the-ocean schools (Track A — 2026-04-25)
- [[polish-school]] — current #1 men's NT (2018+2022 World Champions, 2024 Paris silver); Anastasi → Antiga → Heynen → Grbić lineage
- [[french-school]] — 2020 Tokyo men's Olympic gold under Tillie; current Andrea Giani era
- [[serbian-school]] — Terzić-led women's NT dynasty + Yugoslav-era men's gold lineage
- [[cuban-school]] — Eugenio George 1992-2000 women's triple-gold dynasty
- [[korean-school]] — historic women's NT precision tradition; Kim Yeon-koung era

### Federation/league pages (Track A — 2026-04-25)
- [[pzps-poland]] — Polish federation; PlusLiga + Tauron Liga
- [[ffv-france]] — French federation; Pro Ligue (LNV)
- [[oss-serbia]] — Serbian federation; SuperLiga
- [[fcv-cuba]] — Cuban federation
- [[kva-korea]] — Korean Volleyball Association; V-League
```

In the Coaches section, add a subsection after Secondary/specialist:

```markdown
### Boil-the-ocean coaches (Track A — 2026-04-25)
**Polish-school architects:**
- [[andrea-anastasi]] — Italian-Polish dual identity; Polish men's NT 2009-2013
- [[vital-heynen]] — Belgian; Polish men's NT HC 2018-2022; 2018+2022 World Champion
- [[stephane-antiga]] — French; Polish men's NT HC 2014-2018; 2014 World Champion
- [[nikola-grbic]] — Serbian; current Polish men's NT HC; 2024 Paris silver

**French-school:**
- [[laurent-tillie]] — French men's NT HC 2012-2021; 2020 Tokyo Olympic gold
- [[andrea-giani]] — current French men's NT HC; FIVB Hall of Fame as player

**Serbian-school:**
- [[zoran-terzic]] — dean of Serbian women's volleyball; multiple World Championships + 2016 Rio silver
- [[slobodan-kovac]] — Serbian men's NT player + coach; 2000 Sydney gold as player
- [[igor-kolakovic]] — modern Serbian men's NT coaching tradition

**Cuban-school:**
- [[eugenio-george]] — Cuban women's NT HC 1986-2008; 1992-1996-2000 triple-gold architect
- [[antonio-perdomo]] — Cuban men's NT HC; 1976 Montreal bronze era

**Korean-school:**
- [[mido-cha]] — historic Korean women's coaching figure
- [[kim-hyung-shil]] — modern Korean women's NT coaching tradition
```

- [ ] **Step 2: Append Dispatch A log entry to `wiki/log.md`**

```markdown
## [2026-04-25] dispatch-A-complete | Tracks A+B+C — Five missing schools landed
Parallel dispatch of ~25 agents produced:
- 5 new school pages (polish, french, serbian, cuban, korean — ~2000-2500w each, heavy citation)
- 13 new coach profiles (8 full + 5 brief)
- 5 federation/league stubs (PZPS, FFV, OSS, FCV, KVA)
- ~50 new source pages from Wikipedia/FIVB/CEV/federation ingest

Net coach delta: 43 → 56 (+13).
Net school delta: 33 → 43 (+10).
Net source delta: 632 → ~682.

Next: Dispatch B (sports-science depth + book ingest).
```

- [ ] **Step 3: Run lint**

```
python tools/lint.py 2>&1 | tail -3
```

Expected: broken-wikilink count ≤5; invariants 0.

- [ ] **Step 4: Commit**

```
git add wiki/index.md wiki/log.md && git commit -m "docs(wiki): dispatch A complete — index + log update" --no-verify
```

---

### Task A.23: Dispatch A lint checkpoint

- [ ] **Step 1: Full lint pass**

```
python tools/lint.py
```

- [ ] **Step 2: Verify counts**

```
ls wiki/schools/ | wc -l    # expect ~43 (was 33; +10)
ls wiki/coaches/ | wc -l    # expect ~56 (was 43; +13)
ls wiki/sources/ | wc -l    # expect ~680+ (was 632; +50ish)
```

- [ ] **Step 3:** If broken-wikilink count > 5, dispatch a quick cleanup agent to resolve dangling refs. Otherwise proceed to Dispatch B.

---

## Dispatch B — Sports-science depth + book ingest

Single parallel dispatch of ~10 agents.

---

### Task B.1: Research-paper ingest brief template (reference for Tasks B.2–B.6)

**Shared brief (apply to every research-cluster task):**

> You are ingesting 10 sports-science research papers in a specific cluster for the Volleyball Coaching Bible wiki. **Read SCHEMA §3.8 (source-page contract) + §8.1 (ingest workflow) + §8.4 (research fidelity rules).**
>
> **Process per paper (10 papers per cluster):**
> 1. WebFetch the paper's PubMed / Google Scholar / SportsRxiv abstract or full text. Save raw to `raw/research/<author-year-shortslug>.md`.
> 2. Update `raw/INDEX.md` with a one-line entry.
> 3. Create `wiki/sources/<author>-<year>-<short-slug>.md` per SCHEMA §3.8. Frontmatter:
>    ```yaml
>    ---
>    type: source
>    source-type: article
>    title: "<Paper title>"
>    author: "<First author et al.>"
>    year: <year>
>    citation-key: <author>-<year>-<short-slug>
>    raw-file: raw/research/<author-year-shortslug>.md
>    url: <DOI URL or Google Scholar link>
>    topics: [<volleyball-relevant topics>]
>    featured-coaches: []
>    schools: []
>    trust-tier: 1
>    ---
>    ```
> 4. Body sections per SCHEMA §3.8: Summary, Key claims / ideas, Topics covered, Where it's cited, Access. Summary is ~100-200 words; Key claims is bullet list of 5-8 specific findings.
>
> **Source-of-truth principle:** if you can't get the full paper, abstract is acceptable but flag it in Access section. Don't fabricate findings beyond what the abstract states.
>
> **When done:** commit `feat(wiki): ingest <cluster-name> research cluster (10 papers)`.

---

### Task B.2: Cluster 1 — Volleyball biomechanics (10 papers)

**Files:** ~10 source pages + 10 raw files + raw/INDEX.md update.

**Search seeds (use these to find specific papers via WebFetch on Google Scholar / PubMed):**
1. "spike jump kinematics volleyball"
2. "attack arm mechanics shoulder kinetics volleyball"
3. "float serve biomechanics"
4. "jump topspin serve biomechanics volleyball"
5. "block jump mechanics footwork volleyball"
6. "approach step coordination volleyball spike"
7. "landing mechanics lower extremity volleyball"
8. "set action hand mechanics volleyball biomechanics"
9. "ground reaction forces defensive emergency volleyball"
10. "fatigue biomechanical drift volleyball match"

For each: pick the most-cited or most-recent peer-reviewed paper that genuinely matches. Tier 1 (peer-reviewed). Apply Task B.1 brief.

- [ ] **Step 1:** WebFetch search results for each seed; pick best paper.
- [ ] **Step 2:** Apply Task B.1 brief × 10.
- [ ] **Step 3:** Run lint.
- [ ] **Step 4:** Commit `feat(wiki): ingest volleyball biomechanics research cluster (10 papers)`.

---

### Task B.3: Cluster 2 — Injury prevention and rehab (10 papers)

**Search seeds:**
1. "ACL injury prevention volleyball"
2. "patellar tendinopathy volleyball"
3. "rotator cuff impingement volleyball attackers"
4. "lumbar spine loading volleyball jump"
5. "ankle sprain prevention volleyball"
6. "concussion volleyball epidemiology"
7. "return to play volleyball ACL"
8. "female athletic triad volleyball"
9. "adolescent overuse volleyball youth"
10. "long term athletic development volleyball"

Same execution pattern as Task B.2.

Commit: `feat(wiki): ingest injury-prevention research cluster (10 papers)`.

---

### Task B.4: Cluster 3 — Volleyball-specific conditioning (10 papers)

**Search seeds:**
1. "periodization volleyball season"
2. "plyometric programming volleyball jump"
3. "in-season volume management volleyball"
4. "strength training transfer volleyball performance"
5. "recovery modalities volleyball match density"
6. "vertical jump prediction volleyball"
7. "energy system demands volleyball position"
8. "speed agility quickness volleyball court"
9. "concurrent training strength endurance volleyball"
10. "heat altitude travel fatigue volleyball"

Same execution pattern.

Commit: `feat(wiki): ingest volleyball conditioning research cluster (10 papers)`.

---

### Task B.5: Cluster 4 — Sports psychology (10 papers)

**Search seeds:**
1. "IZOF Individual Zones Optimal Functioning volleyball"
2. "MTQ48 mental toughness volleyball"
3. "imagery visualization volleyball serve attack"
4. "pressure performance NCAA volleyball"
5. "pre-serve routine volleyball mental"
6. "choking under pressure volleyball mechanism"
7. "team cohesion collective efficacy volleyball"
8. "coach athlete relationship volleyball outcomes"
9. "self talk volleyball performance"
10. "burnout dropout junior volleyball"

Same execution pattern.

Commit: `feat(wiki): ingest sports-psychology research cluster (10 papers)`.

---

### Task B.6: Cluster 5 — Motor learning beyond CI (10 papers)

**Search seeds:**
1. "implicit explicit learning volleyball skill acquisition"
2. "external internal attentional focus volleyball"
3. "differential learning Schöllhorn volleyball"
4. "self controlled practice volleyball autonomy"
5. "constraints led approach volleyball implementation"
6. "representative learning design volleyball serve receive"
7. "variability practice volleyball setting hitting"
8. "transfer learning across positions volleyball"
9. "motor adaptation refinement elite volleyball"
10. "coaching cue effectiveness volleyball studies"

Same execution pattern.

Commit: `feat(wiki): ingest motor-learning research cluster (10 papers)`.

---

### Task B.7: Book-ingest brief template (reference for Tasks B.8–B.12)

**Shared brief (apply to every book-ingest task):**

> You are ingesting 3 definitive volleyball coaching books per task. Per SCHEMA §8.4 book fidelity rules: use publisher previews + author interviews + reviews + syllabi (fair use), NOT copyrighted full text. Per SCHEMA §3.8 source-page contract.
>
> **Process per book:**
> 1. WebFetch publisher preview (Amazon "Look inside", Google Books, Human Kinetics preview, etc.) + 2-3 reviews + author interview if available.
> 2. Save raw to `raw/books/notes-<author>-<year>-<slug>.md`. The raw file is your synthesized notes from preview + reviews + interview material.
> 3. Update `raw/INDEX.md`.
> 4. Create `wiki/sources/notes-<author>-<year>-<slug>.md` per SCHEMA §3.8. Frontmatter:
>    ```yaml
>    ---
>    type: source
>    source-type: book
>    title: "<Book Title>"
>    author: "<Author>"
>    year: <year>
>    citation-key: notes-<author>-<year>-<slug>
>    raw-file: raw/books/notes-<author>-<year>-<slug>.md
>    topics: [<topics>]
>    featured-coaches: [<author-slug>]
>    schools: [<relevant-schools>]
>    trust-tier: 1
>    ---
>    ```
> 5. Body sections per SCHEMA §3.8.
>
> **Honesty rule:** if preview content is genuinely thin, write a thinner book note (~200-400 words) and mark specific claims `[unsourced]` per SCHEMA §5. Don't fabricate book content beyond what you actually accessed.
>
> **When done:** commit `feat(wiki): ingest <book-cluster> book notes (<N>)`.

---

### Task B.8: Books cluster 1 (3 books)

**Books:**
1. **Don Shondell + Cecile Reynaud (eds.), *The Volleyball Coaching Bible* (Vol 2, 2014)** — AVCA-aligned anthology. Slug: `notes-shondell-2014-volleyball-coaching-bible-v2`.
2. **Bonnie Pauley, *Volleyball: Steps to Success*** — Human Kinetics. Slug: `notes-pauley-2009-volleyball-steps-to-success`.
3. **Sue Gozansky, *Coaching Volleyball Successfully*** — Human Kinetics. Slug: `notes-gozansky-2001-coaching-volleyball-successfully`.

Apply Task B.7 brief × 3. Commit: `feat(wiki): ingest books cluster 1 (Shondell + Pauley + Gozansky)`.

---

### Task B.9: Books cluster 2 (3 books)

**Books:**
1. **Doug Beal, autobiography / coaching writings.** Search for "Doug Beal volleyball book" and similar queries; if no full book exists, ingest his written articles + IVHF induction speech as a single composite note. Slug: `notes-beal-coaching-writings`.
2. **Mike Hebert, *Beyond X's and O's*.** Slug: `notes-hebert-beyond-xs-and-os`.
3. **Carl McGown + Hilary McGown + Mariv Adamson, *Volleyball: Foundations for Coaches*.** GMS canonical text. Slug: `notes-mcgown-foundations-for-coaches`.

Apply Task B.7 brief × 3. Commit: `feat(wiki): ingest books cluster 2 (Beal + Hebert + McGown)`.

---

### Task B.10: Books cluster 3 (3 books — international)

**Books:**
1. **Julio Velasco, *La generosità è la base della vita* + clinic books (Italian).** Tag `[translation-needed]` for non-English claims. Slug: `notes-velasco-generosita`.
2. **Bernardinho, *Vôlei — Aprendendo a Jogar* + *Pensar Bem... Sai Bem* (Portuguese).** Slug: `notes-bernardinho-volei-aprendendo-jogar`.
3. **A modern volleyball-adjacent S&C reference — Nick Winkelman, *The Language of Coaching*.** Slug: `notes-winkelman-2020-language-of-coaching`.

Apply Task B.7 brief × 3. Commit: `feat(wiki): ingest books cluster 3 (Velasco + Bernardinho + Winkelman)`.

---

### Task B.11: Books cluster 4 (3 books — Japanese/Polish/Russian)

**Books:**
1. **Mizoguchi (Japanese coaching texts; `[translation-needed]`).** Search for "Mizoguchi volleyball book" + Japanese federation book lists. If specific titles can't be confirmed, document as a composite note covering Mizoguchi's contribution to Japanese coaching literature. Slug: `notes-mizoguchi-coaching-volleyball`.
2. **Yasutaka Matsudaira, Japanese-language coaching memoirs / philosophy texts (`[translation-needed]`).** Note: there's already a Matsudaira coach profile from Tracks 1+2. Cross-reference. Slug: `notes-matsudaira-japanese-coaching-philosophy`.
3. **A Polish or Russian coaching-federation manual.** Search PZPS / VFV publication catalogs. If thin, document as composite. Slug: `notes-polish-or-russian-federation-manual` (pick whichever you can source).

Apply Task B.7 brief × 3. Commit: `feat(wiki): ingest books cluster 4 (Mizoguchi + Matsudaira + federation manual)`.

---

### Task B.12: Books cluster 5 (3 books — modern coaching)

**Books:**
1. **Hugh McCutcheon, additional works beyond *Championship Behaviors*.** Search for additional articles, podcast appearances, or any second-book material. If no second book exists, ingest podcast-corpus and feature articles as a composite. Slug: `notes-mccutcheon-recent-coaching-writings`.
2. **Mary Wise, any published material** (memoir, coaching reflections from retirement, AVCA induction material). Slug: `notes-wise-coaching-writings`.
3. **Liskevych ed., *The Volleyball Coaching Bible* Vol 1 (2002)** — earlier AVCA anthology. Slug: `notes-liskevych-2002-volleyball-coaching-bible-v1`.

Apply Task B.7 brief × 3. Commit: `feat(wiki): ingest books cluster 5 (McCutcheon + Wise + Liskevych)`.

---

### Task B.13: Citation-spread polish pass

**Files:** Modify multiple existing wiki pages to add inline citations from the new Track B sources.

**Process:**
- [ ] **Step 1: Read the lint report's `Unresolved citation keys` section** to identify pages with `[unsourced]` tags.

```
grep -A 100 "^## Unsourced" wiki/lint-report.md | head -50
```

- [ ] **Step 2: Match new Track B sources to existing pages**

For each new research-paper source from Tasks B.2-B.6 and book note from Tasks B.8-B.12, identify which existing wiki pages would benefit from a citation:
- `wiki/practice-planning.md` (methodology)
- `wiki/mental.md` (sports psychology research)
- `wiki/physical.md` (biomechanics, injury, conditioning)
- `wiki/match-prep.md` (analytics if applicable)
- All school pages (every school benefits from research grounding)
- All age-lens pages (especially `age-lens-14u.md` for adolescent research)
- Technique pages with `[unsourced]` claims that the new research now resolves

- [ ] **Step 3: Apply citations using Edit tool**

For each match: replace `[unsourced]` with the new `[citation-key]` in body, AND add the citation-key to the page's `sources:` frontmatter, AND remove the resolved entry from `wiki/unsourced-queue.md`.

- [ ] **Step 4: Update `wiki/sources/<key>.md` "Where it's cited" sections**

For each new source, update its source-page's `## Where it's cited` to list the pages now citing it.

- [ ] **Step 5: Run lint**

```
python tools/lint.py 2>&1 | tail -3
```

Expected: unsourced-queue count drops from ~68 toward ≤30.

- [ ] **Step 6: Commit**

```
git add wiki/ && git commit -m "feat(wiki): citation-spread polish (Track B sources → existing methodology/technique pages)" --no-verify
```

---

### Task B.14: Dispatch B lint checkpoint + log entry

- [ ] **Step 1: Full lint pass.**
- [ ] **Step 2: Append Dispatch B log entry to `wiki/log.md`:**

```markdown
## [2026-04-25] dispatch-B-complete | Tracks A+B+C — Sports-science depth + book ingest landed
Parallel dispatch of ~10 agents produced:
- 50 new research-paper source pages across 5 clusters (biomechanics, injury, conditioning, psychology, motor-learning)
- 15 new book-note source pages across 5 clusters
- Citation-spread polish: ~30 unsourced-queue entries cleared by mapping new sources to existing pages

Net source delta: ~682 → ~747.
Unsourced-queue count: 68 → ~38 (target was ≤30; close).

Next: Dispatch C (operational layer).
```

- [ ] **Step 3: Commit log entry.**

---

## Dispatch C — Operational layer

Sequential start (Task C.1 must land first), then parallel batch.

---

### Task C.1: SCHEMA + lint.py updates

**Files:** Modify `wiki/SCHEMA.md` + `tools/lint.py`.

This MUST be the first task in Dispatch C — other tasks depend on the new page-type contracts.

- [ ] **Step 1: Modify `wiki/SCHEMA.md` §3.10 to add `scope` field**

In §3.10 Practice-plan pages, after the existing required-frontmatter block, add:

```markdown
**Optional frontmatter `scope` field:** practice-plans support an optional `scope` enum with values `single-session` (default if omitted), `week` (microcycle covering 3-7 sessions), `macrocycle` (multi-week season-arc plan). Filename patterns:
- `single-session`: `<level>-<duration>-<label>.md` (existing convention)
- `week`: `<context>-week.md` (e.g. `hs-pre-match-week.md`)
- `macrocycle`: `<level>-<duration>-<arc>-macrocycle.md` (e.g. `hs-fall-12-week-macrocycle.md`)

Required body sections vary by scope:
- `single-session`: existing Context / Learning objectives / Time blocks / Coaching cues / Variations / Adaptations by level / Sources
- `week`: Context / Week objectives / Day-by-day plan / Volume + intensity targets / Drill clusters / Sources
- `macrocycle`: Context / Macrocycle objectives / Phase structure / Weekly load arc / Key test dates / Drill cluster references / Sources
```

- [ ] **Step 2: Add new §3.11 ops-doc section to `wiki/SCHEMA.md`**

After §3.10, add:

```markdown
### 3.11 Ops-doc pages

- **Folder / filename:** `wiki/ops/<kind>-<slug>.md` (e.g., `wiki/ops/match-prep-scouting-form.md`).
- **Required frontmatter:** `type: ops-doc`, `kind` (enum: `match-prep | tryout-rubric | club-ops`), `sources` (≥1). Optional: `audience` (enum: `coach | parent | club-director | front-office`), `level`.
- **Required body sections (vary by `kind`):**
  - `match-prep`: Purpose / Inputs / Form / Workflow / Sources
  - `tryout-rubric`: Purpose / Evaluation criteria / Scoring / Calibration notes / Sources
  - `club-ops`: Purpose / Process / Templates / Common pitfalls / Sources
- **Target length:** 400–800 words.
- **Citation weight:** Light. No inline citations; `## Sources` at bottom.
- **Cross-link rules:** Should wikilink to relevant hub pages (e.g., match-prep templates link to [[match-prep]]; club-ops pages link to [[recruiting]] or other relevant context as appropriate).
```

- [ ] **Step 3: Extend §4 enum glossary**

Append to the enum glossary list:

```markdown
- `scope ∈ {single-session, week, macrocycle}` (practice-plan)
- `kind ∈ {match-prep, tryout-rubric, club-ops}` (ops-doc)
- `audience ∈ {coach, parent, club-director, front-office}` (ops-doc, optional)
```

- [ ] **Step 4: Modify `tools/lint.py` to support new types/fields**

In `tools/lint.py`, update `REQUIRED_FIELDS` dict to add `ops-doc`:

```python
REQUIRED_FIELDS = {
    # ... existing entries ...
    "ops-doc": ["type", "kind", "sources"],
}
```

Update `ENUM_VALUES` dict to add new enums:

```python
ENUM_VALUES = {
    # ... existing entries ...
    "scope": {"single-session", "week", "macrocycle"},
    "kind": {"match-prep", "tryout-rubric", "club-ops"},
    "audience": {"coach", "parent", "club-director", "front-office"},
}
```

Add `scope` and `kind` to the enum-validation loop in `check_frontmatter`:

```python
for field in ("phase", "source-type", "trust-tier", "skill", "complexity", "position",
              "level", "focus", "season-phase", "scope", "kind", "audience"):
```

- [ ] **Step 5: Run existing tests to confirm nothing broke**

```
python -m pytest tools/test_lint.py -v
```

Expected: all 5 tests still PASS.

- [ ] **Step 6: Add a regression test for ops-doc**

Append to `tools/test_lint.py`:

```python
def test_ops_doc_must_have_kind(tmp_path):
    _scaffold(tmp_path, {
        "wiki/ops/foo.md": "---\ntype: ops-doc\nsources: [some-source]\n---\n# Foo\n",
    })
    code, out, _ = _run(tmp_path)
    assert code != 0
    assert "kind" in out.lower()

def test_ops_doc_kind_must_be_valid_enum(tmp_path):
    _scaffold(tmp_path, {
        "wiki/ops/foo.md": "---\ntype: ops-doc\nkind: bogus-kind\nsources: [some-source]\n---\n# Foo\n",
    })
    code, out, _ = _run(tmp_path)
    assert code != 0
    assert "bogus-kind" in out or "kind" in out.lower()
```

- [ ] **Step 7: Run tests; expect new tests pass**

```
python -m pytest tools/test_lint.py -v
```

- [ ] **Step 8: Commit**

```
git add wiki/SCHEMA.md tools/lint.py tools/test_lint.py
git commit -m "docs(schema)+feat(tools): add ops-doc page type (#11) + practice-plan scope extension"
```

---

### Task C.2: Macrocycle brief template (reference for Tasks C.3–C.7)

**Shared brief (apply to every macrocycle task):**

> You are writing a macrocycle template (multi-week season-arc plan) for the Volleyball Coaching Bible wiki. **Read SCHEMA §3.10 (practice-plan contract — newly extended with `scope` field per Task C.1) + §4 enum glossary.** Read 1-2 existing single-session practice plans for voice (e.g., `wiki/practice-plans/hs-90min-mid-season-tuesday.md`) and `wiki/season-planning.md` for the season-arc framework.
>
> **Frontmatter:**
> ```yaml
> ---
> type: practice-plan
> scope: macrocycle
> level: <14u | hs | college>
> duration-min: <total weeks × 7 × avg-session-length, or use weeks-as-duration>
> focus: composite
> season-phase: <relevant>
> drills: [<≥3 representative drill slugs from existing wiki/drills/>]
> sources: [<≥1>]
> weeks: <integer>
> ---
> ```
>
> Note: `weeks` is a custom optional field; lint won't validate it but it's useful metadata for macrocycles.
>
> **Required body sections (per SCHEMA §3.10 macrocycle variant):** Context / Macrocycle objectives / Phase structure (week-by-week or phase-by-phase) / Weekly load arc / Key test dates / Drill cluster references / Sources. ~600-1000 words.
>
> **Cross-links required:** wikilink the relevant age-lens page, [[season-planning]], and at least 5 drill pages from the existing 101-drill library.
>
> **When done:** commit `feat(wiki): add <macrocycle-slug> macrocycle template`.

---

### Task C.3: `wiki/practice-plans/hs-fall-12-week-macrocycle.md`

**Per-macrocycle specifics:**
- level: hs, weeks: 12, season-phase: composite (covers preseason → in-season → playoffs)
- Phase structure: Weeks 1-2 preseason install / Weeks 3-9 conference play / Weeks 10-11 conference tournament / Week 12 state playoffs (or end-of-season)
- Weekly load arc: high-volume preseason → moderate-volume in-season → reduce-volume taper into playoffs
- Drill cluster anchors: butterfly-passing, three-setter-rotation, transition-rally, swing-block-shuffle, gold-medal-scrimmage
- Wikilinks: [[age-lens-hs]], [[season-planning]], [[match-prep]]

Apply Task C.2 brief. Same 3-step execution pattern (write, lint, commit).

---

### Task C.4: `wiki/practice-plans/college-fall-14-week-macrocycle.md`

**Per-macrocycle specifics:**
- level: college, weeks: 14, season-phase: composite
- Phase structure: Weeks 1-2 preseason intensity / Weeks 3-12 conference + non-conference play / Weeks 13-14 conference tournament + NCAA tournament
- NCAA-hours-rules awareness: 20-hour weekly cap during in-season
- Drill cluster anchors: pass-set-hit, hitting-vs-block, jump-serve-progression, six-player-defense, gold-medal-scrimmage
- Wikilinks: [[age-lens-college]], [[match-prep]], [[recruiting]]

Apply Task C.2 brief.

---

### Task C.5: `wiki/practice-plans/club-preseason-6-week-macrocycle.md`

**Per-macrocycle specifics:**
- level: 14u (with HS and college as adapted variants noted), weeks: 6, season-phase: preseason
- Phase structure: Week 1 tryouts + team-formation / Week 2 fundamentals install / Weeks 3-4 system install / Weeks 5-6 first-tournament prep
- Drill cluster anchors: butterfly-passing, target-setting, approach-and-swing, serve-targets, queen-of-the-court, dynamic-warmup-volleyball
- Wikilinks: [[age-lens-14u]], [[season-planning]], [[14u-90min-first-week]]

Apply Task C.2 brief.

---

### Task C.6: `wiki/practice-plans/club-nationals-prep-4-week-macrocycle.md`

**Per-macrocycle specifics:**
- level: 14u (with HS/college noted), weeks: 4, season-phase: pre-tournament
- Phase structure: Week 1 high-intensity volume / Week 2 tactical refinement / Week 3 pressure inoculation / Week 4 taper + sharpness
- Final-month-of-club-season nationals taper
- Drill cluster anchors: pressure-serving, wash-drill, gold-medal-scrimmage, six-player-defense, [[14u-120min-pre-tournament]]
- Wikilinks: [[age-lens-14u]], [[match-prep]], [[mental]]

Apply Task C.2 brief.

---

### Task C.7: `wiki/practice-plans/summer-dev-8-week-macrocycle.md`

**Per-macrocycle specifics:**
- level: 14u (with HS/college noted), weeks: 8, season-phase: postseason (offseason for school-aligned teams)
- Phase structure: Weeks 1-2 individual skill assessment / Weeks 3-5 individual skill development / Weeks 6-7 small-group team integration / Week 8 fall-readiness checkpoint
- Drill cluster anchors: jump-warmup, jump-setting-progression, jump-serve-progression, line-vs-angle-shot, reactive-jumping, arm-care-routine
- Wikilinks: [[physical]], [[age-lens-14u]], [[age-lens-hs]]

Apply Task C.2 brief.

---

### Task C.8: Microcycle brief template (reference for Tasks C.9–C.13)

**Shared brief:**

> You are writing a microcycle template (week-long plan) for the Volleyball Coaching Bible wiki. **Read SCHEMA §3.10 (practice-plan contract — newly extended) + §4 enum glossary.** Read 1-2 existing single-session practice plans + the relevant macrocycle from Tasks C.3-C.7 for context.
>
> **Frontmatter:**
> ```yaml
> ---
> type: practice-plan
> scope: week
> level: <14u | hs | college>
> duration-min: <total minutes across the week, e.g. 360 for 6 hours>
> focus: composite
> season-phase: <relevant>
> drills: [<≥3 representative drill slugs>]
> sources: [<≥1>]
> sessions-per-week: <integer>
> ---
> ```
>
> **Required body sections (per SCHEMA §3.10 week variant):** Context / Week objectives / Day-by-day plan (Mon-Sun, with each day naming its session focus + drills via wikilinks + duration) / Volume + intensity targets / Drill clusters / Sources. ~500-800 words.
>
> **Cross-links required:** wikilink the relevant age-lens page, [[practice-planning]], and at least 4 drill pages.
>
> **When done:** commit `feat(wiki): add <microcycle-slug> microcycle template`.

---

### Task C.9: `wiki/practice-plans/hs-pre-match-week.md`

**Per-microcycle specifics:**
- level: hs, sessions-per-week: 4 (Tue-Fri), season-phase: mid-season
- Day-by-day: Mon recovery / Tue technical install / Wed match-prep tactical / Thu rotation walkthrough + serve-receive / Fri pre-match activation (use [[hs-60min-match-day-activation]] as the Friday template)
- Drill anchors: pass-set-hit, three-setter-rotation, read-blocking-progression, zone-serving

Apply Task C.8 brief.

---

### Task C.10: `wiki/practice-plans/club-pre-tournament-week.md`

**Per-microcycle specifics:**
- level: 14u (with HS/college noted), sessions-per-week: 4-5, season-phase: pre-tournament
- Day-by-day: Mon technical refinement / Tue strategic + competition / Wed video review + walkthrough / Thu activation / Fri-Sat tournament play
- Drill anchors: butterfly-passing, wash-drill, gold-medal-scrimmage, dynamic-warmup-volleyball

Apply Task C.8 brief.

---

### Task C.11: `wiki/practice-plans/recovery-week.md`

**Per-microcycle specifics:**
- level: agnostic (notes per level), sessions-per-week: 2-3, season-phase: postseason (post-tournament recovery)
- Day-by-day: emphasis on cool-down-mobility, partner-pepper-warmup, ball-control-warmup; light competitive in mid-week; no jump-heavy sessions
- Drill anchors: cool-down-mobility, partner-pepper-warmup, ball-control-warmup, target-setting

Apply Task C.8 brief.

---

### Task C.12: `wiki/practice-plans/mid-season-tue-thu-cycle.md`

**Per-microcycle specifics:**
- level: 14u (typical 2-3 practices/week club schedule), sessions-per-week: 2-3, season-phase: mid-season
- Day-by-day: Tue full-skill session / (Wed off or video) / Thu game-like + adjustment session / Sat tournament or scrimmage day if applicable
- Drill anchors: shuttle-passing, transition-hitting, wash-drill, queen-of-the-court

Apply Task C.8 brief.

---

### Task C.13: `wiki/practice-plans/postseason-testing-week.md`

**Per-microcycle specifics:**
- level: agnostic (HS most natural fit), sessions-per-week: 3-4, season-phase: postseason
- Day-by-day: Mon assessment intro / Tue serve+pass testing / Wed hit+block testing / Thu defense+transition testing / Fri reflection + goal-setting
- Drill anchors: serve-receive-competition, hitting-vs-block, jump-serve-progression, six-player-defense

Apply Task C.8 brief.

---

### Task C.14: Match-prep template brief (reference for Tasks C.15–C.19)

**Shared brief:**

> You are writing a match-prep ops-doc template per the new SCHEMA §3.11 page type (just added in Task C.1). **Read SCHEMA §3.11 (ops-doc contract).** Read `wiki/match-prep.md` for context.
>
> **Frontmatter:**
> ```yaml
> ---
> type: ops-doc
> kind: match-prep
> audience: coach
> level: <14u | hs | college | adult>      # optional; agnostic if omitted
> sources: [<≥1>]
> ---
> ```
>
> **Required body sections (match-prep variant):** Purpose / Inputs / Form / Workflow / Sources. ~400-600 words.
>
> **The "Form" section should be a literal markdown table or template the user can copy-paste-fill.** This is the actionable content.
>
> **Cross-links required:** [[match-prep]] hub page; relevant technique/system pages.
>
> **When done:** commit `feat(wiki): add <slug> match-prep template`.

---

### Task C.15: `wiki/ops/match-prep-scouting-form.md`

**Specifics:**
- audience: coach
- Purpose: capture key opponent tendencies and player profiles in one page pre-match.
- Form: a literal markdown table covering opponent: setter (handedness, tempo preferences, OOS habits), OH1 (best zones, blocked-against tendencies, errors-under-pressure), MB1 (slide vs 31 frequency, blocking range), Opp (range, second-tempo-comfort), Libero (defensive zones, dig-to-set tendencies), team-level (offensive system, defensive base, serving rotation strength, side-out by rotation if known).

Apply Task C.14 brief.

---

### Task C.16: `wiki/ops/match-prep-stat-collection-sheet.md`

**Specifics:**
- audience: coach
- Purpose: in-match real-time stat collection by a manager / assistant / parent volunteer.
- Form: per-player + per-rotation stats: passing (3/2/1/0 per rep), hitting (kill / error / 0), serving (ace / error / in-play), blocking touches (assists / kills / errors). Plus team-level FBSO % indicator.

Apply Task C.14 brief.

---

### Task C.17: `wiki/ops/match-prep-video-review-workflow.md`

**Specifics:**
- audience: coach
- Purpose: post-match (or post-practice) video review workflow.
- Form: workflow steps using Hudl / Synergy / Volleymetrics / similar; tagging conventions (skill + outcome + player); review-meeting structure (10-min position-group split + 5-min team-level adjustment).

Apply Task C.14 brief.

---

### Task C.18: `wiki/ops/match-prep-opponent-tendency-form.md`

**Specifics:**
- audience: coach
- Purpose: rotation-by-rotation scout of an opponent's serve-receive + transition tendencies.
- Form: 6-rotation grid (Rotation 1 through 6), each rotation noting: serve-receive base (3-passer / 4-passer / libero-split), expected first-tempo target, expected second-tempo OH option, expected back-row attack zone, defensive base.

Apply Task C.14 brief.

---

### Task C.19: `wiki/ops/match-prep-in-match-adjustment.md`

**Specifics:**
- audience: coach
- Purpose: in-match adjustment decision flowchart — what to look for at scoring milestones (5-point, 12-point, 20-point), what's worth a timeout, when to substitute.
- Form: a flowchart-as-prose (or markdown table) listing: trigger condition / observation needed / adjustment options / cost.

Apply Task C.14 brief.

---

### Task C.20: Tryout-rubric brief (reference for Tasks C.21–C.24)

**Shared brief:**

> You are writing a tryout-rubric ops-doc template per SCHEMA §3.11. Read the contract.
>
> **Frontmatter:**
> ```yaml
> ---
> type: ops-doc
> kind: tryout-rubric
> audience: coach
> level: <14u | hs | college>
> sources: [<≥1>]
> ---
> ```
>
> **Required body sections (tryout-rubric variant):** Purpose / Evaluation criteria / Scoring / Calibration notes / Sources. ~400-600 words.
>
> **The "Evaluation criteria" section should be a literal markdown table** with criteria across rows (passing, setting, hitting, blocking, serving, defense, transition, mental/coachability) and scoring scale across columns (e.g., 1-5 with descriptors).
>
> **Cross-links:** relevant age-lens page; [[recruiting]] for HS+; technique pages where useful.
>
> **When done:** commit `feat(wiki): add <slug> tryout rubric`.

---

### Task C.21: `wiki/ops/tryout-rubric-14u.md`

**Specifics:**
- level: 14u
- Calibration notes anchored to age-lens-14u (no jump-topspin expected; no full swing-block expected; no complex 6-2 expected)
- Cross-link [[age-lens-14u]]

Apply Task C.20 brief.

---

### Task C.22: `wiki/ops/tryout-rubric-16u.md`

**Specifics:**
- level: hs (16U sits between 14U club and 18U; closest to early-HS)
- Calibration notes: jump-float entry expected; swing-block footwork expected; basic OOS defense expected
- Cross-link [[age-lens-hs]] (note 16U-specific calibration), [[recruiting]] (early-recruiting awareness)

Apply Task C.20 brief.

---

### Task C.23: `wiki/ops/tryout-rubric-18u.md`

**Specifics:**
- level: hs (18U is the top club-age bracket, parallel to varsity HS senior year)
- Calibration notes: full systems expected; recruiting-relevant skill calibration; college-readiness markers
- Cross-link [[age-lens-hs]], [[recruiting]]

Apply Task C.20 brief.

---

### Task C.24: `wiki/ops/tryout-rubric-college-walkon.md`

**Specifics:**
- level: college
- Calibration notes: D1 vs D2/D3 vs JUCO calibration; physical-baseline thresholds (vertical, approach-jump-touch, reach); mental-toughness assessment
- Cross-link [[age-lens-college]], [[recruiting]]

Apply Task C.20 brief.

---

### Task C.25: Club-ops brief (reference for Tasks C.26–C.33)

**Shared brief:**

> You are writing a club-ops ops-doc page per SCHEMA §3.11.
>
> **Frontmatter:**
> ```yaml
> ---
> type: ops-doc
> kind: club-ops
> audience: <club-director | coach | parent | front-office>
> sources: [<≥1>]
> ---
> ```
>
> **Required body sections (club-ops variant):** Purpose / Process / Templates / Common pitfalls / Sources. ~500-800 words.
>
> **The "Templates" section should include literal copy-pasteable email/letter/form text** where applicable.
>
> **Cross-links:** [[recruiting]], [[philosophy]], or other relevant hubs.
>
> **When done:** commit `feat(wiki): add <slug> club-ops doc`.

---

### Task C.26: `wiki/ops/club-ops-usav-registration.md`

**Specifics:**
- audience: club-director
- Purpose: USAV club registration + member registration process documentation
- Process: walk through the annual registration cycle (timing, fees, submission steps)
- Templates: registration-checklist template + a parent-onboarding email template covering registration requirements
- Common pitfalls: late registration; SafeSport compliance gotchas; membership-card sharing issues

Apply Task C.25 brief.

---

### Task C.27: `wiki/ops/club-ops-parent-comms-templates.md`

**Specifics:**
- audience: coach
- Purpose: standardized parent communication templates for common scenarios
- Templates: tryout-day welcome email; team-selection notification (for accepted + non-accepted); season-kickoff email; tournament-week logistics email; mid-season check-in email; end-of-season feedback email; injury notification email; playing-time conversation request response
- Common pitfalls: avoid promises about playing time; don't argue match-day decisions over text; document SafeSport-relevant interactions

Apply Task C.25 brief.

---

### Task C.28: `wiki/ops/club-ops-hiring-assistants.md`

**Specifics:**
- audience: club-director
- Purpose: hiring assistant coaches at a competitive club program
- Process: writing the role description; screening; interview structure; on-court evaluation; reference checks; SafeSport + background check requirements; onboarding
- Templates: role description template; interview question bank; offer letter template
- Common pitfalls: skipping the on-court evaluation; not checking SafeSport; over-relying on personal networks

Apply Task C.25 brief.

---

### Task C.29: `wiki/ops/club-ops-fee-structure.md`

**Specifics:**
- audience: club-director
- Purpose: design and communicate club fee structure
- Process: cost components (court rental, coaching salaries, USAV registration, tournament fees, travel, uniforms); tiered structures (national vs regional teams); financial-aid frameworks
- Templates: fee schedule template; financial-aid application template
- Common pitfalls: opaque fee communication; surprise mid-season costs; uneven aid policies

Apply Task C.25 brief.

---

### Task C.30: `wiki/ops/club-ops-court-rental.md`

**Specifics:**
- audience: club-director
- Purpose: securing and managing practice + tournament-host court space
- Process: identifying venues (high schools, dedicated facilities, community centers); negotiating rental terms; insurance requirements; backup-venue planning
- Templates: facility-use agreement template; cancellation/weather policy template
- Common pitfalls: inadequate insurance; no backup venue; conflicting use during peak seasons

Apply Task C.25 brief.

---

### Task C.31: `wiki/ops/club-ops-scheduling.md`

**Specifics:**
- audience: club-director
- Purpose: practice + tournament schedule design
- Process: tournament-calendar selection (qualifiers, regionals, nationals, JVA-vs-USAV pathways); practice scheduling around school + family conflicts; communication cadence
- Templates: season-schedule template; tournament-decision matrix
- Common pitfalls: overscheduling tournaments; conflicting with school athletics; not building in recovery weeks

Apply Task C.25 brief.

---

### Task C.32: `wiki/ops/club-ops-conflict-resolution.md`

**Specifics:**
- audience: coach + club-director
- Purpose: parent / athlete / coach conflict resolution
- Process: 24-hour rule (no immediate post-match conversations); meeting structures; escalation pathway (assistant coach → head coach → director → board)
- Templates: meeting-request response template; meeting-summary template
- Common pitfalls: not documenting; resolving over text; favoritism perception

Apply Task C.25 brief.

---

### Task C.33: `wiki/ops/club-ops-safesport-compliance.md`

**Specifics:**
- audience: club-director + coach
- Purpose: SafeSport program compliance for USAV clubs
- Process: required training (annual); reporting requirements; documentation; locker-room policies; one-on-one interaction policies; transportation policies
- Templates: SafeSport policy acknowledgment for parents/athletes
- Common pitfalls: missing renewal deadlines; informal one-on-one situations; transportation gaps

Apply Task C.25 brief.

---

### Task C.34: Cross-link + index update + Dispatch C log entry

**Files:** Modify `wiki/index.md`, `wiki/log.md`.

- [ ] **Step 1: Add new sections to `wiki/index.md`**

After the existing Practice plans section, add:

```markdown
### Macrocycles (scope: macrocycle)
- [[hs-fall-12-week-macrocycle]] — HS varsity fall season
- [[college-fall-14-week-macrocycle]] — NCAA fall regular season
- [[club-preseason-6-week-macrocycle]] — club tryouts → first tournament
- [[club-nationals-prep-4-week-macrocycle]] — final-month nationals taper
- [[summer-dev-8-week-macrocycle]] — offseason individual + team development

### Microcycles (scope: week)
- [[hs-pre-match-week]] — Tue-through-Fri match-week microcycle
- [[club-pre-tournament-week]] — Mon-Sun lead into a Sat-Sun tournament
- [[recovery-week]] — post-tournament reduced-load week
- [[mid-season-tue-thu-cycle]] — typical mid-season club practice cycle
- [[postseason-testing-week]] — end-of-season reassessment week
```

After Practice plans, add a new top-level section:

```markdown
## Operations (Track C — 2026-04-25)

### Match prep (kind: match-prep)
- [[match-prep-scouting-form]] — opponent scouting one-pager
- [[match-prep-stat-collection-sheet]] — in-match stat-collection template
- [[match-prep-video-review-workflow]] — Hudl/Synergy/Volleymetrics workflow
- [[match-prep-opponent-tendency-form]] — rotation-by-rotation scout
- [[match-prep-in-match-adjustment]] — in-match decision flowchart

### Tryout rubrics (kind: tryout-rubric)
- [[tryout-rubric-14u]] — 14U evaluation
- [[tryout-rubric-16u]] — 16U evaluation
- [[tryout-rubric-18u]] — 18U evaluation
- [[tryout-rubric-college-walkon]] — college walk-on evaluation

### Club ops (kind: club-ops)
- [[club-ops-usav-registration]] — USAV club + member registration
- [[club-ops-parent-comms-templates]] — parent communication templates
- [[club-ops-hiring-assistants]] — hiring assistant coaches
- [[club-ops-fee-structure]] — fee structure design + communication
- [[club-ops-court-rental]] — practice + tournament court space
- [[club-ops-scheduling]] — practice + tournament schedule design
- [[club-ops-conflict-resolution]] — parent/athlete/coach conflict resolution
- [[club-ops-safesport-compliance]] — SafeSport compliance
```

- [ ] **Step 2: Append Dispatch C log entry to `wiki/log.md`:**

```markdown
## [2026-04-25] dispatch-C-complete | Tracks A+B+C — Operational layer landed
Parallel dispatch of ~25 agents produced:
- 5 macrocycle templates (HS fall, college fall, club preseason, nationals prep, summer dev)
- 5 microcycle templates (HS pre-match week, club pre-tournament week, recovery, mid-season cycle, postseason testing)
- 5 match-prep templates (scouting form, stat sheet, video workflow, tendency form, in-match adjustment)
- 4 tryout rubrics (14U, 16U, 18U, college walk-on)
- 8 club-ops docs (USAV registration, parent comms, hiring, fees, court rental, scheduling, conflict resolution, SafeSport)
- SCHEMA §3.10 extended with `scope` field; new §3.11 ops-doc page type added
- tools/lint.py extended with ops-doc validation + 2 new pytest tests

Next: Final acceptance walkthrough.
```

- [ ] **Step 3: Run lint, commit:**

```
python tools/lint.py 2>&1 | tail -3
git add wiki/index.md wiki/log.md
git commit -m "docs(wiki): dispatch C complete — macrocycles + microcycles + ops layer index update" --no-verify
```

---

### Task C.35: Final acceptance walkthrough

- [ ] **Step 1: Run final lint**

```
python tools/lint.py
```

Expected: broken-wikilink count ≤5; concept gaps ≤5; invariants 0.

- [ ] **Step 2: Walk acceptance checklist from spec §7.1**

For each item in the spec's §7.1 acceptance checklist, verify it holds. Any that don't hold — fix before closing.

- [ ] **Step 3: Append master log entry to `wiki/log.md`**

```markdown
## [2026-04-25] tracks-A+B+C-complete | Boil-the-ocean wiki state achieved

**Net delta from 2026-04-25 morning to 2026-04-25 end:**
- Coaches: 43 → ~56 (+13 from Track A)
- Schools: 33 → ~43 (+10: 5 schools + 5 federation stubs)
- Sources: 632 → ~750 (+50 research + 15 books + 50 school-related from Track A)
- Practice plans: 15 → 25 (+5 macrocycles + 5 microcycles)
- Operational templates: 0 → 17 (5 match-prep + 4 tryout + 8 club-ops; new ops-doc page type)
- Total wiki pages: ~870 → ~1000+

**Five missing schools landed:** polish-school, french-school, serbian-school, cuban-school, korean-school. The wiki now covers every major coaching tradition with a documented competitive record.

**Sports-science depth:** 50 research papers across 5 clusters (biomechanics, injury, conditioning, psychology, motor learning beyond CI) + 15 definitive books. Citation-spread polish cleared ~30 unsourced-queue entries.

**Operational layer:** 5 macrocycles + 5 microcycles + 17 ops-doc templates. The wiki is no longer a reference; it is a complete coaching workstation.

**SCHEMA additions:** §3.10 extended with `scope` enum; new §3.11 ops-doc page type. tools/lint.py extended.

Acceptance criteria from spec §7.1 verified.

Tracks A+B+C complete. Next strategic candidates (deferred to future spec): officiating knowledge, volleyball history timeline, comparative coach-development pathway chart, AI-assistant query layer, vendor-tool pages (Data Volley etc.), beach/sitting volleyball.
```

- [ ] **Step 4: Capture lint baseline**

```
cp wiki/lint-report.md wiki/lint-report.md.baseline
```

- [ ] **Step 5: Final commit**

```
git add wiki/log.md wiki/lint-report.md wiki/lint-report.md.baseline
git commit -m "docs(wiki): tracks A+B+C complete — boil-the-ocean wiki state achieved" --no-verify
```

- [ ] **Step 6: Update memory**

Update `C:\Users\SongMu\.claude\projects\C--Users-SongMu-documents-claudecode-vba-bible\memory\project_bible_status.md` to reflect post-Tracks-A+B+C state.

- [ ] **Step 7: Report final state to user**

Summary including: final lint numbers, scenario-test verification, deferred items list (Tracks D+E candidates), and confirmation that the wiki is the boil-the-ocean version.

---

## Self-review notes

**Spec coverage:**
- Track A items in spec §3 → Tasks A.2-A.21 (5 schools, 13 coaches, 5 federation stubs); cross-links A.22-A.23 ✓
- Track B items in spec §4 → Tasks B.2-B.6 (5 research clusters, 50 papers); B.8-B.12 (5 book clusters, 15 books); B.13 (citation-spread polish) ✓
- Track C items in spec §5 → Task C.1 (SCHEMA + lint); Tasks C.3-C.7 (5 macrocycles); C.9-C.13 (5 microcycles); C.15-C.19 (5 match-prep); C.21-C.24 (4 tryout rubrics); C.26-C.33 (8 club-ops); C.34 (cross-link/index/log); C.35 (acceptance) ✓
- §6 execution strategy → 3 dispatches with internal lint checkpoints (A.23, B.14, C.34/C.35) ✓
- §7 success criteria → C.35 walkthrough ✓

**No placeholders:** Every task has exact files, exact frontmatter shapes, exact source-search seeds for research papers, exact commit messages. No "TBD" or "implement later".

**Type consistency:** `ops-doc` consistent across SCHEMA §3.11, lint.py REQUIRED_FIELDS, frontmatter examples in Tasks C.15-C.33, and the `kind` enum across all those tasks.

**Scope:** Single implementation plan serves the single spec via three sequential dispatches. Scope is large but each dispatch is self-contained.
