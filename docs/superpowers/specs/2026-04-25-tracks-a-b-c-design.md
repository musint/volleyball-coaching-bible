# Wiki Tracks A+B+C — "Boil-the-Ocean" Design Spec

**Date:** 2026-04-25
**Owner:** Song Mu (song.mu@discordapp.com)
**Predecessor specs:** `docs/superpowers/specs/2026-04-22-volleyball-coaching-bible-design.md` (bootstrap), `docs/superpowers/specs/2026-04-24-wiki-improvement-tracks-1-2-design.md` (usability + integrity)

---

## 1. Context

### 1.1 Why this work

After Tracks 1+2 (2026-04-24) and the Munciana camp ingest (2026-04-25), the wiki has 33 schools, 43 coaches, 632 sources, 101 drills, 15 practice plans, and zero broken wikilinks. It is a working coaching tool. But Song's question on 2026-04-25 was: *"Anything I might be missing if I want it to be the boil-the-ocean version of all volleyball coaching knowledge in the world?"*

Honest gap audit found 17 missing dimensions. Three were chosen as the next big push:

- **Track A — Five missing major coaching traditions.** Polish, French, Serbian, Cuban, Korean. The Polish men's NT is currently #1 in the world; France won the 2020 Tokyo men's gold; Serbia, Cuba, and Korea each have decades of dominant results. Their absence is the single most visible structural gap in the wiki's claim to comprehensive coverage.
- **Track B — Sports-science depth + definitive-book ingest.** Only 7 research papers and 7 book notes ingested across the entire wiki. Methodology and technique pages are undersourced. Adding ~50 papers + ~15 books gives every existing page a stronger citation base for the rest of the wiki's life.
- **Track C — Operational layer (Track 3 territory).** 15 single-session practice plans exist; no microcycle weeks, no macrocycle season-arcs, no match-prep templates, no tryout rubrics, no club operations docs. The wiki is a reference but is not yet a complete *workstation* for running a competitive club program week-to-week.

### 1.2 Stance

Boil the ocean. Ship all three tracks in one session via three sequential parallel dispatches. Internal lint checkpoints between dispatches; no human-gate breakpoints between A, B, and C unless something fails hard.

### 1.3 Positioning

Unchanged from prior specs. Neutral reference. Preferred-tradition material (Kiraly/AOC/GMS/USAV/Japanese) remains first-among-equals in coverage depth; no school is favored on any page; contested topics present tradeoffs without resolution.

---

## 2. Scope

### 2.1 Deliverable matrix

| Track | New wiki content pages | New source pages | New tooling |
|---|---:|---:|---:|
| A | 23 (5 schools + 13 coaches + 5 federation stubs) | ~50 | — |
| B | 0 (citations spread into existing pages) | ~65 (50 research + 15 books) | — |
| C | 27 (5 macro + 5 micro + 5 match-prep + 4 tryout + 8 ops) | ~5 | SCHEMA additions only |
| **Total** | **~50 new wiki content pages** | **~120 new sources** | **2 SCHEMA additions** |

Plus a citation-spread polish pass on existing methodology and technique pages after Track B lands.

### 2.2 Non-goals (explicit YAGNI)

- Beach volleyball — out of scope per bootstrap §1.4
- Sitting/wheelchair Paralympic volleyball — out of scope per bootstrap §1.4
- Coach-certification study guides for taking certification exams — out of scope per bootstrap §1.4
- A web frontend — Obsidian remains the reader
- A live AI-assistant query layer over the wiki (item #17 in the gap audit) — explicitly deferred; this spec focuses on content not application
- Mark Rosen and Alyssa Lingenfelter profile expansions (queued from Tracks 1+2 cleanup) — handled here only if they surface in Track A coach research (low likelihood)
- Statistics/analytics tooling pages (Data Volley, etc.) — deferred; Track B's research cluster covers analytic *frameworks* in research-paper form but not vendor tools
- Officiating knowledge — deferred (gap audit item #14)
- Volleyball history timeline page — deferred (gap audit item #15)
- Comparative coach-development pathway chart — deferred (gap audit item #14, partial)

These deferrals form the natural Tracks D+E for a future spec.

---

## 3. Track A — Missing schools

### 3.1 The five schools

**Polish school** — `wiki/schools/polish-school.md`
- *Why:* Poland is currently #1 men's NT (2014/2018/2022 World Championships, 2024 Paris silver, multiple European Championships). The Polish coaching identity is a synthesis of Italian methodology (Anastasi era), Belgian-meets-German pragmatism (Heynen), French tactical adaptability (Antiga), and Serbian discipline (Grbić).
- *Origin / institutions:* PZPS (Polski Związek Piłki Siatkowej) governing body; PlusLiga (men's pro), Tauron Liga (women's pro). Spała training center.
- *Core tactical signatures:* aggressive jump-serving floor, server-pin focus on opposing OH1, pin-block discipline, deep-perimeter defensive base.

**French school** — `wiki/schools/french-school.md`
- *Why:* France won the **2020 Tokyo men's Olympic gold** under Laurent Tillie — one of the most significant non-USA/Brazil/Italy results in a generation. Andrea Giani currently HC. The French style is offense-creative, tempo-multidirectional, with deep MB rotation usage.
- *Origin / institutions:* FFV (Fédération Française de Volley); Pro Ligue (LNV). CREPS regional training centers.
- *Core tactical signatures:* slide-from-multiple-rotations as a default, OH backrow attack high-frequency, second-tempo middles even from average passes.

**Serbian school** — `wiki/schools/serbian-school.md`
- *Why:* Zoran Terzić's women's NT (1998-2017+) won multiple World Championship and European Championship titles plus 2016 Rio silver and 2017 Grand Champions Cup gold. Men's NT under Slobodan Kovač and Igor Kolaković has 1980 Moscow + 2000 Sydney golds in lineage and steady recent performance. Nikola Grbić — currently Polish HC — is Serbian by training.
- *Origin / institutions:* OSS (Odbojkaški Savez Srbije, formerly Yugoslav VF). Domestic SuperLiga; significant pro-export pipeline.
- *Core tactical signatures:* discipline-first ground defense, dig-to-set-from-anywhere libero usage, MB-as-priority-attacker tendency.

**Cuban school** — `wiki/schools/cuban-school.md`
- *Why:* The 1992-2008 Cuban women's dynasty under Eugenio George won 3 consecutive Olympic golds (1992 Barcelona, 1996 Atlanta, 2000 Sydney) plus 2 silvers (1990, 2002 World Championships). The Cuban style — extreme physicality, high-tempo offense, jump-serving aggression — shaped the modern women's game more than its later results have been credited.
- *Origin / institutions:* FCV (Federación Cubana de Voleibol). Centralized national-team development with fewer pro-club layers.
- *Core tactical signatures:* power as core advantage, high-second middle attacks, jump-serving early adoption.

**Korean school** — `wiki/schools/korean-school.md`
- *Why:* The Korean women's NT has decades of consistent Olympic and Asian Championship results (1976 Montreal bronze; multiple Asian Championships; 2012 London 4th-place; 2020 Tokyo 4th-place). Distinct tactical lineage emphasizing precision passing and deep-tempo offense scaled to a smaller-stature roster. Stefano Lavarini's stint as women's NT HC (Italian → Korean transfer) added a methodological bridge.
- *Origin / institutions:* KVA (Korea Volleyball Association). V-League (women's pro is internationally followed). Significant international transfer history (Kim Yeon-koung in Turkey/China/Italy).
- *Core tactical signatures:* libero-driven defensive identity, multiple-tempo MB attacks, OH backrow attack as a normal option even on imperfect passes.

### 3.2 Coach profiles (13)

Full profile (~1500w) for primary architects; brief profile (~800w) for secondary figures.

**Polish:**
- Andrea Anastasi (full) — Italian-Polish dual identity; coached Polish men's NT 2009-2013, brought Italian Generazione methodology
- Vital Heynen (full) — Belgian; Polish men's HC 2018-2022; 2018+2022 World Champion architect
- Stéphane Antiga (brief) — French; player-coach transition; Polish men's HC 2014-2018
- Nikola Grbić (full) — Serbian; current Polish men's HC (2022+); 2022+2024 cycle leadership

**French:**
- Laurent Tillie (full) — French men's HC 2012-2021; **2020 Tokyo gold architect**
- Andrea Giani (full) — Italian; current French men's HC (2021+); both player and coach legend

**Serbian:**
- Zoran Terzić (full) — Serbian women's HC 1998-2017+; multiple titles; the dean of Serbian volleyball
- Slobodan Kovač (brief) — Serbian men's HC; played in 2000 Sydney gold-medal run
- Igor Kolaković (brief) — Serbian/Montenegrin; men's NT history; modern coaching

**Cuban:**
- Eugenio George (full) — Cuban women's HC 1980s-2000s; 1992-2000 triple-gold architect
- Antonio Perdomo (brief) — Cuban men's HC; 1976 Montreal bronze; institutional voice

**Korean:**
- Mido Cha (brief) — historic Korean women's coaching figure
- Kim Hyung-shil (brief) — modern Korean women's NT coaching tradition

### 3.3 Federation/league stubs (5)

- `wiki/schools/pzps-poland.md` — Polish governing body; PlusLiga + Tauron Liga
- `wiki/schools/ffv-france.md` — French federation; Pro Ligue (LNV)
- `wiki/schools/oss-serbia.md` — Serbian federation; SuperLiga
- `wiki/schools/fcv-cuba.md` — Cuban federation
- `wiki/schools/kva-korea.md` — Korean Volleyball Association; V-League

These follow the existing institutional-stub pattern (`penn-state.md`, `florida.md`) and exist primarily to satisfy SCHEMA §6 bidirectional cross-link invariants for the new coach profiles.

### 3.4 Sources

Sourced via WebFetch:
- Wikipedia bios (English + native-language where translation feasible) for each coach
- FIVB Hall of Fame / IVHF induction pages where applicable
- CEV / FIVB feature articles (long-form interviews where they exist)
- Federation-page ingests (PZPS, FFV, OSS, FCV, KVA — about-pages and history-pages)
- Major-competition retrospective articles (Olympic, World Championship)
- Selected pro-league articles (PlusLiga, Pro Ligue features)
- Where Italian/Polish/Serbian/Korean-language sources have richer content than English, ingest with `[translation-needed]` tags per SCHEMA §5

Estimate: ~50 new source pages, mix of Tier 1 (FIVB/IVHF) and Tier 2 (CEV/federation/feature articles) and Tier 3 (Wikipedia, with corroboration).

---

## 4. Track B — Sports-science depth + book ingest

### 4.1 Research clusters (50 papers)

**Cluster 1 — Volleyball biomechanics (10 papers).**
- Spike-jump kinematics + force production
- Attack arm mechanics + shoulder kinetics
- Serve biomechanics (float vs jump-topspin vs jump-float)
- Block-jump mechanics + footwork
- Approach-step coordination
- Landing mechanics + lower-extremity loading
- Set-action hand mechanics
- Pass-platform stability under perturbation
- Ground reaction forces during defensive emergency moves
- Fatigue-induced biomechanical drift in long matches

**Cluster 2 — Injury prevention and rehabilitation (10 papers).**
- ACL prevention adapted to volleyball (FIFA 11+ adaptations, PEP variants)
- Patellar tendinopathy in volleyball
- Shoulder impingement and rotator-cuff in attackers
- Lumbar spine loading in jump landings
- Ankle sprain prevention (eversion taping, balance training)
- Concussion in volleyball (relatively rare but documented)
- Post-injury return-to-play protocols
- Female athletic triad in volleyball populations
- Adolescent overuse injuries (volume thresholds for 14U-18U)
- Long-term athletic development frameworks for volleyball

**Cluster 3 — Volleyball-specific conditioning (10 papers).**
- Periodization studies for volleyball
- Plyometric programming + jump-performance gains
- In-season volume management (rep counts, jump tracking)
- Strength training transfer to court performance
- Recovery modalities + match-density tolerance
- Vertical-jump prediction equations for volleyball
- Energy-system demands per position
- Speed-agility-quickness adapted to volleyball court geometry
- Concurrent training (strength + endurance) for volleyball
- Heat / altitude / travel-fatigue management

**Cluster 4 — Sports psychology in volleyball (10 papers).**
- IZOF (Individual Zones of Optimal Functioning) applied to volleyball
- MTQ48 mental toughness in volleyball populations
- Visualization / imagery practices for serve, attack, set
- Pressure-performance research at NCAA + international level
- Routines and pre-serve / pre-attack mental scripts
- Choking under pressure mechanisms in volleyball
- Team cohesion and collective efficacy
- Coach-athlete relationship quality and outcomes
- Self-talk research applied to volleyball
- Burnout / dropout in elite junior volleyball

**Cluster 5 — Motor learning beyond contextual interference (10 papers).**
- Implicit vs explicit learning in volleyball skill acquisition
- External vs internal attentional focus during execution
- Differential learning theory (Schöllhorn) applied to volleyball
- Self-controlled practice and learner autonomy
- Constraints-led approach implementation studies
- Representative learning design in serve-receive
- Variability-of-practice in setting and hitting
- Transfer of learning across positions
- Motor adaptation and refinement in elite players
- Coaching cue effectiveness studies

Sources fetched via Google Scholar + PubMed + SportsRxiv + ResearchGate + open-access volleyball-specific journals (e.g., *Journal of Strength and Conditioning Research*, *International Journal of Sports Physiology and Performance*, *Sports Medicine*).

Each paper becomes a `wiki/sources/<author>-<year>-<short-slug>.md` Tier 1 source page per SCHEMA §3.8.

### 4.2 Book ingest (~15 books)

Via fair-use publisher previews, author interviews, syllabi, and reviews per SCHEMA §8.4.

1. **Don Shondell + Cecile Reynaud (eds.), *The Volleyball Coaching Bible* (Vol 1, 2002; Vol 2, 2014).** AVCA-aligned definitive coaching anthology. Existing Liskevych-as-editor pages may reflect Vol 1; Vol 2 specifically may be uningested.
2. **Bonnie Pauley, *Volleyball: Steps to Success*.** Fundamentals progression; widely-used as a textbook.
3. **Sue Gozansky, *Coaching Volleyball Successfully* (Human Kinetics).** Practical coaching framework.
4. **Doug Beal, autobiography / coaching books.** 1984 LA gold architect's published material.
5. **Mike Hebert, *Beyond X's and O's*.** Hebert's coaching philosophy book beyond the *Thinking Volleyball* tactical book already on file.
6. **Carl McGown + Hilary McGown + Mariv Adamson, *Volleyball: Foundations for Coaches*.** GMS canonical text.
7. **Mary Wise, any published material** (memoir / coaching reflections if available).
8. **Hugh McCutcheon, additional works beyond *Championship Behaviors***.
9. **Julio Velasco, *La generosità è la base della vita* + clinic books (Italian; `[translation-needed]` where helpful).**
10. **Bernardinho, *Vôlei — Aprendendo a Jogar* + *Pensar Bem... Sai Bem* (Portuguese; `[translation-needed]`).**
11. **Mizoguchi (Japanese coaching texts; `[translation-needed]`).**
12. **Yasutaka Matsudaira, Japanese-language coaching memoirs / philosophy texts (`[translation-needed]`).**
13. **Polish coaching federation manuals — PZPS publications.**
14. **Russian coaching manuals — Platonov / Karpol-era VFV publications.**
15. **A modern strength-and-conditioning reference adapted to volleyball** (e.g., Nick Winkelman's *The Language of Coaching* used widely in volleyball S&C circles).

Each becomes a `wiki/sources/notes-<author>-<year>-<slug>.md` source page citing fair-use material; the `raw-file:` field points at a `raw/books/notes-<slug>.md` summary file built from previews + interviews + syllabi + reviews.

### 4.3 Citation-spread polish pass

After Track B sources land, a single coordinator agent does a citation-spread pass: for each new source, identify which existing wiki pages would benefit from inline citations and add them. Targets:

- Methodology hubs (`practice-planning.md`, `mental.md`, `physical.md`)
- All school pages (every school benefits from research grounding)
- Technique pages with `[unsourced]` claims that the new research now resolves
- Age-lens pages (especially `age-lens-14u.md` for the youth-overuse + adolescent-development research)

This pass clears as many entries as possible from `wiki/unsourced-queue.md` using the new sources.

---

## 5. Track C — Operational layer

### 5.1 New page types

**Extension to `practice-plan`:** add `scope` enum field — `single-session | week | macrocycle`. Existing 15 plans become `scope: single-session` automatically (no change required to their content; SCHEMA §3.10 is updated to define the field with `single-session` as the default). Microcycle and macrocycle templates use the new scope values.

**New page type `ops-doc`:** SCHEMA §3.11 covering match-prep templates, tryout rubrics, and club operations docs. Frontmatter:
```yaml
type: ops-doc
kind: match-prep | tryout-rubric | club-ops      # required enum
audience: coach | parent | club-director | front-office   # optional enum
level: 14u | hs | college | adult                # optional
sources: [...]
```

Required body sections vary by `kind` — match-prep gets *Purpose / Inputs / Form / Workflow / Sources*; tryout-rubric gets *Purpose / Evaluation criteria / Scoring / Calibration notes / Sources*; club-ops gets *Purpose / Process / Templates / Common pitfalls / Sources*.

Target length: 400-800 words.

### 5.2 Macrocycles (5 templates, `scope: macrocycle`)

Filename pattern: `<level>-<duration>-<arc>.md` under `wiki/practice-plans/`.

1. `hs-fall-12-week-macrocycle.md` — HS varsity fall season
2. `college-fall-14-week-macrocycle.md` — NCAA fall regular season
3. `club-preseason-6-week-macrocycle.md` — club tryouts → first tournament
4. `club-nationals-prep-4-week-macrocycle.md` — final-month-of-club-season nationals taper
5. `summer-dev-8-week-macrocycle.md` — offseason individual + team development

Each macrocycle: weekly load/intensity/focus arc, peaking strategy, key-test dates, integration with school calendar / college academic calendar / club tournament dates. ~600-1000 words.

### 5.3 Microcycles (5 templates, `scope: week`)

1. `hs-pre-match-week.md` — Tuesday-through-Friday match-week microcycle
2. `club-pre-tournament-week.md` — Mon-Sun lead into a Saturday-Sunday tournament
3. `recovery-week.md` — post-tournament reduced-load recovery week
4. `mid-season-tue-thu-cycle.md` — typical mid-season three-day club practice cycle
5. `postseason-testing-week.md` — end-of-season reassessment and feedback week

Each microcycle: day-by-day session outline, intensity/volume targets per day, drill-cluster suggestions, session-to-session continuity. ~500-800 words.

### 5.4 Match-prep templates (5, `kind: match-prep`)

1. `wiki/ops/match-prep-scouting-form.md` — opponent scouting one-pager
2. `wiki/ops/match-prep-stat-collection-sheet.md` — in-match stat-collection template
3. `wiki/ops/match-prep-video-review-workflow.md` — Hudl/Synergy/Volleymetrics workflow
4. `wiki/ops/match-prep-opponent-tendency-form.md` — rotational + per-hitter scout
5. `wiki/ops/match-prep-in-match-adjustment.md` — in-match decision flowchart

### 5.5 Tryout rubrics (4, `kind: tryout-rubric`)

1. `wiki/ops/tryout-rubric-14u.md`
2. `wiki/ops/tryout-rubric-16u.md`
3. `wiki/ops/tryout-rubric-18u.md`
4. `wiki/ops/tryout-rubric-college-walkon.md`

Each: evaluation criteria per skill (passing/setting/hitting/blocking/serving/defense/transition/mental), scoring scales, calibration notes, common-mistake guidance for evaluators.

### 5.6 Club operations docs (8, `kind: club-ops`)

1. `wiki/ops/club-ops-usav-registration.md`
2. `wiki/ops/club-ops-parent-comms-templates.md`
3. `wiki/ops/club-ops-hiring-assistants.md`
4. `wiki/ops/club-ops-fee-structure.md`
5. `wiki/ops/club-ops-court-rental.md`
6. `wiki/ops/club-ops-scheduling.md`
7. `wiki/ops/club-ops-conflict-resolution.md`
8. `wiki/ops/club-ops-safesport-compliance.md`

Each: purpose, process, downloadable-style templates inline, common pitfalls, sources (USAV materials, club-management blog posts, SafeSport official guidance).

### 5.7 SCHEMA additions

- §3.10 `practice-plan` — add `scope` field with `single-session | week | macrocycle` enum; clarify filename patterns for week/macrocycle variants
- §3.11 (new) `ops-doc` — full page-type definition
- §4 enum glossary — add `scope ∈ {single-session, week, macrocycle}`, `kind ∈ {match-prep, tryout-rubric, club-ops}`, `audience ∈ {coach, parent, club-director, front-office}`
- `tools/lint.py` REQUIRED_FIELDS dict — add `practice-plan` `scope` (optional, default single-session) and new `ops-doc` type with required `kind`

### 5.8 Index updates

`wiki/index.md` gets:
- New "Macrocycles" section under Practice plans
- New "Microcycles" section under Practice plans
- New top-level "Operations" section listing all `ops-doc` pages grouped by kind

---

## 6. Execution strategy

### 6.1 Three sequential dispatches

**Dispatch A — Missing schools (~25 parallel agents):**
- 5 × school writers
- 13 × coach profile writers (mix of full + brief)
- 5 × federation/league stub writers
- 1 × index/log/cross-link coordinator
- 1 × Track A lint coordinator

Wall clock estimate: ~30-40 minutes parallel-agent work.

**Dispatch B — Sports-science + book ingest (~10 parallel agents):**
- 5 × research-cluster ingest agents (one per cluster, 10 papers each)
- 5 × book-ingest agents (3 books each on average)
- 1 × citation-spread polish agent (after research + books land)
- 1 × Track B lint coordinator

Wall clock estimate: ~40-50 minutes — research papers via WebFetch can be slow, books require digesting publisher previews.

**Dispatch C — Operational layer (~25 parallel agents):**
- 5 × macrocycle writers
- 5 × microcycle writers
- 5 × match-prep template writers
- 4 × tryout rubric writers
- 8 × club ops doc writers
- 1 × SCHEMA §3.10 + §3.11 + lint.py update agent
- 1 × index/log/cross-link coordinator

Wall clock estimate: ~30-40 minutes.

### 6.2 Internal checkpoints (no human gate)

After each dispatch:
- Run `python tools/lint.py`
- Confirm broken-wikilink count remains ≤10 (target: 0; minor temporary regressions during dispatch are acceptable since cross-link agent fixes them)
- Confirm invariant violations remain at 0
- Append a per-dispatch log entry to `wiki/log.md`
- Spot-check a sample of new pages for SCHEMA compliance

### 6.3 Final acceptance walkthrough

After Dispatch C:
- Full lint sweep — broken wikilinks ≤ 5; concept gaps ≤ 5; invariants 0
- §7 acceptance checklist walkthrough
- `wiki/log.md` master entry summarizing the three-track effort
- Memory update at `C:\Users\SongMu\.claude\projects\C--Users-SongMu-documents-claudecode-vba-bible\memory\project_bible_status.md` reflecting the new state

---

## 7. Success criteria

### 7.1 Acceptance checklist

Tracks A+B+C complete when all of these hold:

**Track A:**
- [ ] 5 new school pages exist at `wiki/schools/{polish,french,serbian,cuban,korean}-school.md` with required frontmatter + body sections per SCHEMA §3.3
- [ ] 13 new coach profiles exist at `wiki/coaches/<firstname-lastname>.md` per SCHEMA §3.2
- [ ] 5 federation stubs exist at `wiki/schools/{pzps-poland,ffv-france,oss-serbia,fcv-cuba,kva-korea}.md`
- [ ] Every Track A coach has ≥1 school + ≥1 source per SCHEMA §6
- [ ] ~50 new sources exist under `wiki/sources/` paired with `raw/articles/` files

**Track B:**
- [ ] ~50 new research-paper source pages under `wiki/sources/` across 5 clusters
- [ ] ~15 new book-note source pages under `wiki/sources/` (with `notes-` prefix per SCHEMA §3.8 raw-file convention)
- [ ] Citation-spread polish landed across methodology hubs + school pages + age-lens pages
- [ ] `wiki/unsourced-queue.md` count drops from ~68 toward ≤30

**Track C:**
- [ ] 5 macrocycle templates exist with `scope: macrocycle`
- [ ] 5 microcycle templates exist with `scope: week`
- [ ] 5 match-prep templates exist as `ops-doc` with `kind: match-prep`
- [ ] 4 tryout rubrics exist as `ops-doc` with `kind: tryout-rubric`
- [ ] 8 club-ops docs exist as `ops-doc` with `kind: club-ops`
- [ ] SCHEMA.md updated with §3.10 `scope` extension and new §3.11 `ops-doc` page type
- [ ] `tools/lint.py` extended to handle the new fields and page type
- [ ] `wiki/index.md` reflects Macrocycles, Microcycles, Operations sections

**Cross-cutting:**
- [ ] Broken-wikilink count ≤5 in final lint
- [ ] Invariant violations: 0
- [ ] `wiki/log.md` has dispatch entries for A, B, C plus a master entry
- [ ] Memory updated with new state

### 7.2 Scenario tests

Three real queries that must work cleanly post-Tracks-A+B+C:

1. **"How does the Polish men's program approach jump-serving compared to Brazil?"** Expected: synthesis from `wiki/schools/polish-school.md` (Heynen + Grbić era) and `wiki/schools/brazilian-school.md` with citations.
2. **"Build me a 6-week club preseason macrocycle."** Expected: `wiki/practice-plans/club-preseason-6-week-macrocycle.md` returned verbatim.
3. **"Give me a tryout rubric for 14U evaluation, plus parent communication template for tryout-day."** Expected: `wiki/ops/tryout-rubric-14u.md` + `wiki/ops/club-ops-parent-comms-templates.md` returned, with the latter including a tryout-day-specific template.

### 7.3 Living-wiki signals

- The wiki opens cleanly in Obsidian; graph view shows Polish/French/Serbian/Cuban/Korean schools as new well-connected clusters
- A reader testing for "comprehensive coverage" no longer hits an obvious missing-tradition gap on first 5 minutes of browsing
- Citation density on methodology and technique pages noticeably increases
- Operational templates land in a `wiki/ops/` folder that becomes the natural reach-target for "what do I need this week" questions

---

## 8. Open items & caveats

1. **Translation gaps.** Italian, Polish, Portuguese, Japanese, Korean primary sources may be richer than English secondary coverage. Where helpful, ingest with `[translation-needed]` tags per SCHEMA §5; do not skip primary sources just because they're non-English.
2. **Federation-page accessibility.** Some federation pages (especially KVA, FCV) may have limited English-language web presence. Where Wikipedia is the only practical Tier 2 anchor, use it with corroboration from FIVB/CEV records.
3. **Book preview availability.** Some target books may have minimal publisher previews (e.g., older Italian/Russian texts). Where preview is genuinely thin, ingest a thinner book-note based on reviews + interviews, and tag specific claims `[unsourced]` per SCHEMA §5 honesty rules.
4. **Citation-spread polish scope.** The spread pass touches existing methodology and technique pages. To keep diff size manageable, the agent prioritizes high-impact citation insertions (claims that currently lack any citation or that have only Tier 3 backing) over comprehensive recitation.
5. **Track C coverage of beach / sitting.** Operational templates focus on indoor 6s. Cross-references to beach or sitting are not in scope.
6. **Ops-doc kind enum extensibility.** The initial three kinds (`match-prep`, `tryout-rubric`, `club-ops`) cover this spec's deliverables. Future expansion to e.g. `parent-doc`, `front-office-doc`, `season-debrief` is reserved for a later spec.
7. **Tracks D+E.** The deferred items from §2.2 — beach, sitting, certification guides, AI-assistant layer, vendor-tool pages, officiating, history timeline, comparative-pathway chart — form a natural Tracks D+E for after this spec lands.

---

## 9. Next step

Hand off to the writing-plans skill to produce a dispatch-by-dispatch implementation plan with concrete task lists, agent briefing templates, and acceptance checks per dispatch.
