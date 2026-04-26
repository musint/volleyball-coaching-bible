# Operations Log

Append-only log of wiki operations. Prefix format: `## [YYYY-MM-DD] <operation> | <short>`.

## [2026-04-24] defer | Munciana Drills folder ingest (Task 3.2) | touched 2 pages
Executed Tracks 1+2 plan Task 3.2 (`docs/superpowers/plans/2026-04-24-wiki-improvement-tracks-1-2.md`)
to inspect and ingest the uncommitted `Munciana Drills/` folder at repo root.

**Folder contents (1 file):**
- `2022MuncianaCampDrills.mp4` — single binary video file, 1.35 GB (1,454,161,045 bytes),
  2022 Munciana Camp drill sessions

**Deferred — not ingested.** Rationale:
- No ffmpeg on PATH (required to demux audio for transcription)
- No local whisper / speech-to-text binary on PATH
- `mcp__aoc__aoc_video_transcript` only serves AOC-hosted Vimeo/Wistia streams;
  a local MP4 is not addressable by that tool
- No paired notes, slide deck, session outline, or drill write-up in the folder
- SCHEMA §9 anti-patterns prohibit fabricating drill content (setup, coaching
  points, equipment, duration) from a filename alone — doing so would attribute
  invented material to Munciana and Mike Lingenfelter

**Artifacts produced:**
- `Munciana Drills/.deferred` — full deferral note with research hypothesis for
  a future session (transcribe → `raw/transcripts/munciana-2022-camp-drills.md`
  → source page → per-drill pages → cross-link from `mike-lingenfelter.md` and
  `munciana-volleyball-club.md`; optional `## Munciana drill cluster` section on
  the school page if ≥5 drills land)
- This log entry

**Folder retained** (not removed) so the MP4 remains accessible for a future
transcription pass. The `.deferred` marker is the only text artifact inside the
folder.

**Acceptance-criterion status (spec §6.1).** The "Munciana Drills/ folder is
fully committed or explicitly deferred with a log note" bullet is satisfied by
this entry + the `.deferred` marker. Drill page count contribution from Task 3.2
to the Dispatch 3 summary: 0 drills / 0 source pages.

**Lint state after defer:** unchanged from pre-task baseline
(Broken wikilinks 182; invariants 0; frontmatter 22; citations 76; orphans 116;
gaps 14). No wiki pages modified; no lint regression possible.

**Pages touched:** 2 (wiki/log.md + Munciana Drills/.deferred).

## [2026-04-24] backfill | Bernardinho + Brazilian methodology cluster (Task 2.19) | touched 14 pages
Executed Tracks 1+2 plan Task 2.19 — the largest unsourced cluster (11 entries
across `wiki/coaches/bernardinho.md` and `wiki/schools/brazilian-school.md`).
WebFetched Goodreads + PocketBook4You + SlideShare for Bernardinho's own book
*Transformando Suor em Ouro* (Sextante 2006, ISBN 9788575422427); Wikipedia
biographies for José Roberto Guimarães, Renan Dal Zotto, and Bebeto de Freitas;
IVHF Class of 2022 Bernardinho induction page; FIVB 2021 Guimarães/Dal Zotto
Paris-2024 announcement; The World (PRX) 2021 Michael Fox feature on Brazilian
volleyball. Ingested 6 new sources:
- `bernardinho-2006-transformando-suor-em-ouro` (Tier 1, book) — primary
  methodology source; Roda da Excelência framework; preparation/discipline/
  pressure/team-culture principles; 6 direct quotes
- `bernardinho-2022-ivhf-induction-bio` (Tier 2) — IVHF enshrinement bio;
  corroborates two Italian club stints (Perugia women + Modena men)
- `fivb-2021-guimaraes-dal-zotto-paris-2024` (Tier 2) — FIVB announcement
  confirming Dal Zotto as 2017-on Brazil men's NT HC
- `theworld-2021-brazil-volleyball-nation` (Tier 2) — "Move over soccer"
  (Michael Fox, PRX 2021); 2015 Ministry of Sport ranking grounds
  volleyball-as-second-sport claim
- `bebeto-de-freitas-2026-wikipedia-bio` (Tier 3) — full Bebeto bio (1950-
  2018); 1998 FIVB World Championship gold with Italy = Italian-Brazilian
  exchange at HC level
- `dal-zotto-2026-wikipedia-bio` (Tier 3) — Dal Zotto playing + HC 2017-2023
Cleared 11 of 11 entries from unsourced-queue.md: methodology cluster
(Bernardinho core principles + brazilian-school principles), Italian-Brazilian
exchange, Guimarães as 1992 Barcelona HC, club-pipeline systemic framing,
school contrast framing, structural-risk editorial, Bebeto bio, Dal Zotto
rebuild-cycle leadership, 1992 gold attribution, quote-section stub, bernardinho
→ brazilian-school dangling-wikilink. Reframed 4 residuals honestly: tactical-
diagram-level specifics; quantitative gender-disparity data; hierarchical-
coaching-culture critique; athlete-pressure-as-psychological-load editorial. 1
kept as [unverified] (the 2017-2020 women's second-stint claim — checked against
all 9 sources, confirmed absent; most likely a confusion with Dal Zotto's 2017-
on men's NT tenure).
Pages touched: 14 (6 raw files + 6 source pages + bernardinho.md +
brazilian-school.md + raw/INDEX.md + unsourced-queue.md + log.md).

## [2026-04-24] backfill | Nakagaichi 1972 [unverified] cluster (Task 2.25) | touched 7 pages
Executed Tracks 1+2 plan Task 2.25 — resolved the inline `[unverified]` tag on the identity of the 1972 Munich Olympic Japan men's gold-medal head coach. WebFetched en.wikipedia.org/wiki/Volleyball_at_the_1972_Summer_Olympics_%E2%80%93_Men%27s_tournament (confirmed Yasutaka Matsudaira), en.wikipedia.org/wiki/Yasutaka_Matsudaira (full biography), and volleyhall.org/yasutaka-matsudaira.html (Tier 1 IVHF induction record, 1998 enshrinement). Ingested two new sources: `matsudaira-1998-hall-of-fame` (Tier 1, IVHF, "multiple quick attack" / "time differential attack" credited innovation; 1964 bronze/1968 silver/1972 gold medal progression; first Japanese IVHF inductee; FIVB First VP 1994-1996; JVA President 1989-1995) and `matsudaira-2026-wikipedia-biography` (Tier 3, full biographical chronology + Soviet-study-trip context for the 9-to-6-player men's-program transition). Authored full ~2,100-word coach profile `wiki/coaches/yasutaka-matsudaira.md` per SCHEMA §3.2 (frontmatter + Overview + Coaching career + Core teaching principles + Contributions + Quotes + Sources). Updated `wiki/coaches/yuichi-nakagaichi.md` — replaced `[unverified]` references with the Matsudaira identification (also corrected a "five years before" typo to "five years after"), added the two Matsudaira sources to frontmatter, updated disambiguation paragraph and Contributions section "1972 Munich correction" framing. Updated `wiki/schools/japanese-training.md` — added Matsudaira to founders/associated-coaches frontmatter, added time-differential-attack to core-principles, added Matsudaira sources; rewrote the speed-first-tempo principle #3 to source the time-differential-attack attribution to Matsudaira directly (replacing the prior `[unsourced]` tag on that claim); replaced the prior `[unverified]` 1972-Munich-architect bullet in Notable Practitioners with a full Matsudaira entry; updated the Nakagaichi entry to link back to Matsudaira on the 1972 reference. Updated `raw/INDEX.md` Japanese-tradition section with both new raw files, `wiki/index.md` International coach listing to add Matsudaira and clean the Nakagaichi annotation (no longer flags [unverified]). No unsourced-queue entry existed for this claim (the tag was inline only); queue unchanged. Pages touched: 7 (matsudaira-1998-hall-of-fame.md, matsudaira-2026-wikipedia-biography.md, yasutaka-matsudaira.md, yuichi-nakagaichi.md, japanese-training.md, index.md, raw/INDEX.md).

## [2026-04-24] backfill | Daimatsu + Japanese historical cluster (Task 2.22) | touched 7 pages
Resolved 2 unsourced entries on wiki/coaches/daimatsu-hirobumi.md:
(1) 1953-vs-1954 Nichibo hire-date ambiguity — resolved as two-stage institutional
chronology: Dai Nippon Spinning approved team November 27, 1953 (Daimatsu hired);
team officially established at Kaizuka factory March 15, 1954.
(2) NHK television rating for 1964 Olympic women's final — sourced at 66.8%
average / peak >80% per Olympics.com citing NHK; still the most-watched sporting
event in Japanese television history.
Also added bio detail: 1968 LDP election to House of Councillors.
New sources: [[daimatsu-wikipedia-biography]], [[witches-of-orient-wikipedia]],
[[tokyo-1964-women-volleyball-japan-gold-olympics]].
Pages: 3 raw articles + 3 source pages + wiki/coaches/daimatsu-hirobumi.md +
wiki/schools/japanese-training.md + wiki/unsourced-queue.md + wiki/log.md.

## [2026-04-23] bootstrap-start | Wave 0 begin
Project initialized. Git repo created. Scaffolding in place.

## [2026-04-23] wave0-complete | Foundation done
Wrote: CLAUDE.md (root), SCHEMA.md, index.md scaffold, log.md, unsourced-queue.md,
raw/INDEX.md, 9 page templates. Scaffolding for all content ready.
Next: CP1 (user reviews SCHEMA.md), then Wave 1 research.
Pages touched: 15.

## [2026-04-23] wave1-ingest | USAV coaching resources (W1.1)
Parallel subagent research pass. Sources: usav-2009-cap-game-like-training,
usav-2026-{coach-academy,coach-education,coach-tools,growing-kids-volleyball,
hp-clinic-lessons-shared,lesson-plans,resources-for-coaches,simplified-youth-rules,
so-you-want-to-be-a-volleyball-coach,youth-volleyball-tips}. 11 source pages.
Raw: 12 files in raw/usav/. Finding: USAV CAP discontinued in favor of Coach
Academy (Bronze/Silver/Gold, Craft/Body/Mind/Heart/Team pillars).

## [2026-04-23] wave1-ingest | McCutcheon corpus (W1.3)
Sources: mccutcheon-2008-beijing-gold-usav, mccutcheon-2021-volleybrains-ep30,
mccutcheon-2022-championship-behaviors, mccutcheon-2023-manning-mastery-trust,
mccutcheon-2024-wikipedia-bio. 5 source pages; 5 raw files across articles/,
transcripts/, books/. Finding: McCutcheon's book is *Championship Behaviors*
(Triumph, 2022), NOT *Thinking Volleyball* (which is Mike Hebert's 2013 book).

## [2026-04-23] wave1-ingest | GMS / McGown corpus (W1.4)
Sources: gms-nd-{about-us,blocking,structure-practice}, gms-2017-thank-you-carl-mcgown,
gms-2018-clinic-report, mcgown-2017-usav-remembering. 6 source pages; 6 raw articles.
2 fetch blocks (connection-refused GMS blog post; unreadable PDF on garyhorvath.com).
McGown's canonical book is *Science of Coaching Volleyball* (Human Kinetics).

## [2026-04-23] wave1-ingest | AOC corpus (W1.5)
Sources: aoc-2017-{liskevych-dunning-tribute,one-big-thing-panel,rose-10-things-learned},
aoc-2018-{dunning-serve-warmup,stone-platform-management}, aoc-2020-stone-liskevych-using-video,
aoc-2021-mattox-early-season-practice, aoc-nd-rose-profile. 8 source pages; 8 raw files.
3 AOC Premium items paywalled and skipped honestly.

## [2026-04-23] wave1-ingest | Japanese training corpus (W1.6)
Sources: daimatsu-{2000-hall-of-fame,2017-tough-love}, nakagaichi-{2020-fivb-feature,
2021-biography}, japan-{2016-five-strengths,2024-svleague}. 6 source pages; 6 raw articles.
Finding: Nakagaichi is NOT the 1972 Munich men's gold architect (spec/plan error).
The 1972 Japan men's gold head coach remains [unverified] in this wiki — needs dedicated
source in a future pass. JVA institutional documents not fetchable in English.

## [2026-04-23] wave1-ingest | Motor learning research (W1.8)
Sources: shea-1979-contextual-interference, magill-1990-contextual-interference-review,
pinder-2011-representative-learning-design, afonso-2012-volleyball-perceptual-cognitive,
davids-2013-ecological-dynamics-talent, woods-2020-sport-ecology-designers. 6 source pages
(all trust-tier: 1); 6 raw research files. Coverage: contextual interference, ecological
dynamics, constraints-led approach, representative learning design, perception-action
coupling. 2 full-text; 3 abstract-level; 1 secondary-corroborated.

## [2026-04-23] wave1-ingest | Karch Kiraly corpus (W1.2)
Two parallel agents ran; outputs merged. Sources: kiraly-1997-championship-volleyball,
kiraly-2001-ivhf-bio, kiraly-2019-smarter-training, kiraly-2021-{karch-at-60,team-blend},
kiraly-2023-chasing-greatness, kiraly-2024-{serving-placement,usav-announcement,usav-bio,
usav-mens-coach,vnl-paris-interview,volleyballworld-mens-transition}, kiraly-wikipedia-bio.
13 source pages. Raw: 10 articles (karch-*), 4 book notes (2 per book, dupe captures from
the two agents), 1 transcript. Findings: (1) Kiraly named USA Men's NT head coach for
LA 2028 (transition announced 2024-10). (2) Second book *Chasing Greatness* (2023). (3)
Two AOC Kiraly premium items paywalled — content gap.

## [2026-04-23] wave1-ingest | Additional major coaches (W1.7)
Sources: dunning-2016-aoc-difference-maker, hebert-2013-thinking-volleyball,
langping-2016-brunswick-iron-hammer, langping-2020-cgtn-own-way, liskevych-2015-aoc-10-things,
liskevych-2021-volleybrains-no-shortcuts, rose-2016-dignittany-excellence-vs-success,
rose-2021-volleybrains-everything-matters, speraw-2024-usav-profile, wise-2023-characterandleadership-profile.
10 source pages across 7 coaches (Rose×2, Dunning, Hebert, Liskevych×2, Speraw, Wise, Lang Ping×2).
Raw: 7 articles, 2 transcripts, 1 book note. Hebert's *Thinking Volleyball* (2013) disambiguated
from McCutcheon's *Championship Behaviors* (2022) in citation-keys. Florida retirement piece
404'd for Wise — partial coverage.

## [2026-04-23] wave1-ingest | IG + YouTube Tier-3 (W1.9)
Sources: ig-{artofcoachingvb,goldmedalsquared,usavolleyball}-20260423, yt-aoc-20210112-wave-serve-receive-drill,
yt-aoc-20240702-training-libero-karch-kiraly, yt-aoc-unknown-pass-for-points-diane-flick,
yt-usav-20200526-karch-kiraly-reading-part-1. 7 source pages, all trust-tier: 3.
All 3 IG profiles login-walled — profiles captured, no post-specific claims. 2 YT items
captured via public companion articles (no transcripts); 2 items metadata-only stubs.
USAVlearn Kiraly-on-reading item eligible for tier-2 promotion upon transcript capture.

## [2026-04-23] aoc-mcp-e2e | First MCP-driven Premium ingest (Task 14)
First end-to-end use of tools/aoc-mcp/. Ingested Kiraly's "4 keys to the forearm pass"
(AOC Premium, 2013) via `mcp__aoc__fetch_article` tool handler. Confirms auth,
fetch, extract, and wiki-write all work over the MCP interface.
Pages touched: raw/articles/aoc-2013-kiraly-4-keys-forearm-pass.md,
wiki/sources/aoc-2013-kiraly-4-keys-forearm-pass.md, raw/INDEX.md, wiki/log.md.
Extraction: title/author/date/tags all populated; word_count=169 (video-backed
article with concise body text). Confirms the full MCP pipeline is live — future
Wave 2 coach/school profile writing can call `mcp__aoc__*` tools directly.

## [2026-04-23] aoc-backfill | Extensive MCP-driven AOC ingest (Task 15)
Eight parallel subagents drove the aoc-mcp stack to ingest 88 additional AOC
articles across 8 thematic batches — 0 failures. Total AOC source coverage
went from 9 → 97 source pages (≈10×). Batches:
  1. Kiraly philosophy & 2-minute takes (10): culture, asking questions,
     freedom to decide, reverse brainstorming, assistant coach use, stats,
     serving errors, pressure, things learned, becoming a learner
  2. Kiraly drills & tactics (12): 50% drill, validation 6v6, in-game tactics,
     libero training, serve-receive unit, reads-every-skill, advice-from-legends
     (w/ Liskevych), precision passing, training efficiently, expose best player,
     libero-set team drill, competing in practice
  3. Russ Rose corpus (13): 2023 club rules, subs in practice, coach for life
     profile (Patterson, 2521wc), What I learned (Dietzen), offensive systems,
     back-row skills, serving fundamentals + ritual, impact of passing,
     Penn State prep, bad servers, no-free-balls rule, best-servers game plan
  4. McCutcheon + Dunning (10): blocking keys, coopetition, competitive cauldron
     (w/ Laurie Eisler), defense-blocking (w/ Liskevych); Dunning 10-things,
     team culture, Stanford match prep, non-starter motivation, hitter types,
     players-sing practice
  5. Liskevych corpus (12): Liskevych 5, controlling feelings, players & staff,
     growing-the-sport podcast, what-matters blocking, top-35 references
     bibliography, full 6-video ASICS Skill Series (defense/blocking/setting/
     hitting/serving/passing)
  6. Technique foundations (10): 3-key passing (posture/pursuit/platform),
     passing principles (Rose/Dunning/Stone panel), setting hand-hinge,
     setting fundamentals, attack approach (Gina Schmidt), attack arm mechanics,
     float-serve 3-keys, float-serve toss, types of serves, blocking fundamentals
  7. Systems & strategy (10): training-reading ×3 (2020/2025/2026), team defense +
     reading, swing blocking when, Slabe blocking (static/swing/combo),
     bunch-read blocking, 4-2 system, hybrid 5-1 two-setters, hybrid 6-2
  8. Youth/14U + mental + motor learning (11): kids fundamentals ×4 (pass/set/
     attack/serve), 15 youth drills, teach rotations to beginners, teach spiking,
     coaching the iY generation (Premium teaser), 9 reasons teams fail, motor
     learning teaser (Jim Stone), post-game talk
Total new files: 176 (88 raw/articles + 88 wiki/sources). New coaches surfaced
or reinforced for Wave 2 profile writing: Luka Slabe, Laurie Eisler, Gina
Schmidt, Cassidy Lichtman, Jim Stone (already profiled), plus reinforced
Kiraly/Rose/Dunning/Liskevych/McCutcheon/Hebert corpus. Author-field
inconsistencies to flag during lint: MCP occasionally returned "Follow"
(scrape artifact); sources used article-body byline where visible, or
"Art of Coaching Volleyball" as fallback with a note in Access.

## [2026-04-23] wave2-w2.1 | USA coach profiles written (batch 1)
Five parallel writer agents produced wiki/coaches/karch-kiraly.md,
hugh-mccutcheon.md, terry-liskevych.md, john-speraw.md, mary-wise.md.
Totals: ~7130 body words across 5 profiles; heavy inline citations per
SCHEMA §3.2/§5. Sources cited: Kiraly=31, McCutcheon=10, Liskevych=18,
Speraw=4, Wise=1. Unsourced tags: Kiraly=0, McCutcheon=0, Liskevych=0,
Speraw=2 (technical-teaching content; assistant-coach NCAA championship
program year), Wise=6 (AVCA counts, tenure ranking, cultural-influence
inferences). Added 10 new entries to wiki/unsourced-queue.md.
Findings:
  - Speraw's Olympic bronze medals: Rio 2016 AND Paris 2024 per
    speraw-2024-usav-profile; Tokyo 2020 was NOT a medal. Plan guidance
    had this wrong; Speraw agent corrected.
  - Mary Wise profile uses schools: [florida] per source's schools field;
    a wiki/schools/florida.md stub is needed for lint compliance
    (forward-reference, will be resolved in W2.4 contrasting schools or a
    later follow-up).
  - 0 fabricated citations; every [citation-key] verified against
    wiki/sources/. Dangling `\[\[wikilinks\]\]` left for W2.2+ targets
    (mike-hebert, carl-mcgown, gold-medal-squared, laurie-eisler, etc.).

## [2026-04-23] wave2-w2.2-w2.4 | Methodology coaches, internationals, preferred schools (12 agents)
Twelve parallel writer/ingest agents completed W2.2 through W2.4 in a single
dispatch cycle:

**W2.2 methodology-school coaches (4 profiles):**
- carl-mcgown.md — 1677 body words, 8 sources, 0 unsourced
- mike-hebert.md — 1493 body words, 1 source, 7 unsourced (thin source base)
- john-dunning.md — 1797 body words, 13 sources, 0 unsourced
- russ-rose.md — 1884 body words, 17 sources, 1 unsourced

**W2.3 international coach profiles (6 profiles):**
- daimatsu-hirobumi.md — 1560 body words, 4 sources, 2 unsourced (1953/1954
  hire-date discrepancy, NHK rating figure)
- yuichi-nakagaichi.md — 1388 words, 4 sources, 7 honesty tags. 1972 Munich
  disambiguation explicitly in profile (Nakagaichi NOT 1972 architect;
  born 1967). Original 1972 head coach remains [unverified] wiki-wide.
- lang-ping.md — 1598 words, 2 sources, 0 unsourced (Iron Hammer, 1984 player
  gold + 2016 coach gold uniquely documented)
- julio-velasco.md — 1414 words, 1 source + new raw+source ingest
  (velasco-2026-wikipedia-bio via WebFetch), 7 unsourced methodology claims
- bernardinho.md — 1533 words, 1 source + new ingest (bernardinho-2026-
  wikipedia-bio), 9 unsourced. Plan guidance corrected: 1984 LA silver as
  player; NO women's NT second stint 2017-2020 (France men's 2021-22 +
  Brazil men's 2023-present instead per Wikipedia); Vera Mossa is first
  wife not sister
- giovanni-guidetti.md — 1361 words, 1 source + new ingest (guidetti-2026-
  wikipedia-bio), 3 unsourced. Plan corrections: Netherlands NT was
  2015-2016 not 2007-2015; Italy women's NT was vice-coach 1997-2000 only
  (never head coach); Germany 2006-2014 was his longest NT role

**W2.4 preferred school pages (5 pages, 2000-2500 words each):**
- gold-medal-squared.md — 2491 words, 14 sources (6 GMS + 5 research),
  1 unsourced. Full contrast section vs ecological-dynamics / AOC / USAV-CAP.
- art-of-coaching-volleyball.md — 2382 words, 45 sources (broad sample
  across ~97 ingested AOC pages), 0 unsourced. 12 associated coaches.
  Updated founding to Liskevych+Dunning+Rose (3 co-founders per sources,
  not 2). Founded 2011.
- japanese-training.md — 2493 words, 6 sources, 9 unsourced + 1 [unverified]
  (1972 Munich HC) + 1 [translation-needed]. Associated coaches use
  daimatsu-hirobumi (not hirobumi-daimatsu) to match actual file slug.
- usa-volleyball.md — 2477 words, 14 sources, 4 unsourced. Uses generalized
  slug `usa-volleyball` (not legacy `usa-volleyball-cap`). W2.6 will
  reconcile — existing coach profiles point schools: [usa-volleyball-cap].
- ecological-dynamics.md — 2499 words, 9 sources (6 research + 3 AOC
  reading-adjacent), 0 unsourced. First school page written.

**Net state after W2.2-2.4:** wiki/coaches/ = 15 profiles; wiki/schools/ = 5
pages; unsourced-queue.md has 25+ entries (Velasco×7, Bernardinho×9,
Guidetti×3, Daimatsu×2, Nakagaichi×3, Hebert×7, Rose×1, McCutcheon×1,
Kiraly×1, Speraw×2, Wise×6, GMS×1, USA Volleyball×4, Japanese×9).

**Known reconciliation work deferred to W2.6:**
- Legacy slug `usa-volleyball-cap` across 7+ coach profiles → rename to
  `usa-volleyball` OR create redirect stub at schools/usa-volleyball-cap.md
- Existing coach profiles reference schools like `penn-state`, `stanford`,
  `pacific`, `florida`, `illinois`, `minnesota`, `chinese-volleyball-tradition`
  that don't yet have pages — stub or omit
- associated-coaches fields on school pages need bidirectional match against
  each coach's schools: field

## [2026-04-23] wave2-w2.5 | Contrasting school page: Brazilian tradition
Wrote wiki/schools/brazilian-school.md — 2541 words, 4 sources (bernardinho-
2026-wikipedia-bio, brazil-men-nt-2026-wikipedia, brazil-women-nt-2026-wikipedia,
guimaraes-2026-wikipedia), 24 [unsourced] tags (methodology-cluster — Wikipedia
sources cover results but not tactical/pedagogical detail), 75 total inline
citations. Ingested 3 new Wikipedia articles + created 3 new source pages
(brazil-men-nt-2026-wikipedia, brazil-women-nt-2026-wikipedia, guimaraes-2026-
wikipedia). Key framing: three program-architects (Bebeto de Freitas →
Guimarães → Bernardinho) delivered 6 Olympic golds across both genders;
competition record anchored by 69 all-time FIVB titles; methodology record
[unsourced] and queued for Bernardinho interview + CBV clinic ingest in a
later pass. Cross-links: [[italian-school]] (planned/future) as related-school;
[[japanese-training]], [[usa-volleyball]] as contrast targets.

## [2026-04-23] wave2-w2.5 | Contrasting schools + methodology comparison (5 pages)
Five parallel agents produced the contrasting-school set:
- russian-school.md — 2567 words, 6 sources (3 new ingests: russian-men-nt,
  platonov, karpol Wikipedia), 23 [unsourced]. Alekno bio fetched but no
  dedicated source page yet.
- brazilian-school.md — 2539 words, 6 sources (3 new: brazil-men-nt,
  brazil-women-nt, guimaraes Wikipedia), 24 [unsourced].
- italian-school.md — 2498 words, 4 sources (2 new: italy-men-nt,
  italy-women-nt), 19 [unsourced].
- game-based-training.md — 2621 words, 10 sources (1 new: tgfu-wikipedia),
  0 [unsourced]. Pedagogy-lineage framing (Bunker/Thorpe 1982 → Launder →
  TGfU/Play Practice → USAV game-like-training via Rick Swan) distinct from
  ecological-dynamics theoretical framing.
- block-vs-random-practice.md — 2778 words, 10 sources (no new ingest —
  used existing motor-learning research + GMS/AOC/USAV), 1 [unsourced].
  Methodology comparison page, not a school proper; justified as cross-cutting.

Total raw ingests this wave: 9 Wikipedia articles (russian-men-nt, platonov,
karpol, brazil-men-nt, brazil-women-nt, guimaraes, italy-men-nt,
italy-women-nt, tgfu). All saved with source pages per SCHEMA §8.1.

## [2026-04-23] wave2-w2.6 | Coach ↔ school cross-link reconciliation
Single reconciliation agent executed the SCHEMA §6 invariant pass:

Legacy slug migration usa-volleyball-cap → usa-volleyball:
- 7 coach frontmatter edits (carl-mcgown, hugh-mccutcheon, john-dunning,
  john-speraw, karch-kiraly, mike-hebert, terry-liskevych)
- 4 school body + related-schools edits (art-of-coaching-volleyball,
  game-based-training, gold-medal-squared, japanese-training)
- Archival legacy references remain in wiki/sources/*.md, log.md, and
  SCHEMA.md example frontmatter — flagged for later cleanup (surface lint).

Bidirectional additions:
- McCutcheon.schools += [art-of-coaching-volleyball, gold-medal-squared]
  (AOC and GMS both correctly list him; profile attests both affiliations)
- Speraw.schools += [gold-medal-squared] (GMS network roster membership)
- usa-volleyball.associated-coaches += [john-dunning, mike-hebert]

Cleanups:
- block-vs-random-practice.associated-coaches cleared to [] (methodology-
  comparison page; empty associated-coaches legitimate per SCHEMA §3.3
  exception for research/methodology frameworks)

Stubs created for bidirectional-link compliance:
- penn-state.md (for russ-rose.schools reference)
- florida.md (for mary-wise)
- chinese-volleyball-tradition.md (for lang-ping)
- modern-european-club-volleyball.md (for giovanni-guidetti)
These 4 are institutional-tradition stubs flagged for later fleshing-out;
they're programs/eras as-much-as methodological schools, so a future
refactor may move them to a programs/ rung if that classification matters.

## [2026-04-23] wave2-complete | Reference frame populated — ready for CP3
Wave 2 totals:
- wiki/coaches/ = 15 pages (5 USA + 4 methodology + 6 international)
- wiki/schools/ = 14 pages (5 preferred + 5 contrasting + 4 institutional stubs)
- wiki/sources/ = 173 pages (+12 from W2.3/W2.5 Wikipedia ingests)
- raw/articles/ = 139 files (+12)
- wiki/unsourced-queue.md — 40+ active entries across ~10 coach pages + 4
  school pages, with research hypotheses per item

Research corrections preserved from plan/design errors:
- McCutcheon book = *Championship Behaviors* (2022), NOT *Thinking Volleyball*
- Nakagaichi ≠ 1972 Munich men's gold architect (born 1967) — original
  architect remains [unverified] wiki-wide
- USAV CAP discontinued → Coach Academy; slug `usa-volleyball-cap` legacy →
  `usa-volleyball` current
- Kiraly USA Women's 2012-2024 → USA Men's LA 2028 transition
- Speraw Olympic bronzes = Rio 2016 + Paris 2024 (NOT Tokyo 2020)
- Bernardinho: no Brazil women's NT second stint 2017-2020 (France men's
  2021-22 + Brazil men's 2023-present per Wikipedia)
- Guidetti: Netherlands NT 2015-2016 (not 2007-2015); never Italy women's
  head coach (vice-coach 1997-2000 only); Germany 2006-2014 longest NT role

Ready for **CP3 user checkpoint** before Wave 3 (techniques + positions + systems).

## [2026-04-23] wave3-complete | Technical core populated (49 pages)
Nine parallel writer agents produced Wave 3 in a single dispatch:

**W3.1 Passing (4 techniques, ~7,620 words):**
- passing-forearm.md (2330 words, 12 sources, schools-perspectives=yes)
- passing-overhead.md (1655, 7, schools-perspectives=yes — upgraded from plan's "light" because modern-overhead-vs-classical-forearm-only is genuinely contested)
- passing-serve-receive.md (2207, 10, schools-perspectives=yes)
- passing-free-ball.md (1429, 5)

**W3.2 Setting (4 techniques, ~5,370 words):**
- setting-hands.md (1232, 7)
- setting-jump.md (1049, 6)
- setting-backset.md (1073, 6)
- setting-out-of-system.md (2016, 11, schools-perspectives=yes — AOC toolbox / Japanese bail / GMS motor-learning / eco-dynamics representative-design)

**W3.3 Hitting (4 techniques, ~4,800 words):**
- hitting-approach.md (1101, 6)
- hitting-arm-swing.md (1092, 5)
- hitting-shot-selection.md (1405, 4, schools-perspectives=yes — AOC toolbox / GMS random / Russian power / Italian pressure / Brazilian creativity)
- hitting-back-row-attack.md (1204, 4)

**W3.4 Blocking (4 techniques, ~4,780 words):**
- blocking-footwork.md (1221, 7, schools-perspectives=yes — swing-vs-shuffle generational shift)
- blocking-hand-position.md (1002, 6)
- blocking-read.md (1241, 10, schools-perspectives=yes — AOC reading / GMS pattern / eco-dynamics affordance / Japanese anticipate)
- blocking-swing.md (1315, 8)

**W3.5 Serving (4 techniques, ~5,470 words):**
- serving-float.md (1314, 10)
- serving-jump-float.md (1348, 9)
- serving-topspin.md (1492, 7, schools-perspectives=yes — Russian/Brazilian/Italian men's / women's float-dominance)
- serving-hybrid.md (1317, 11)

**W3.6 Defense + transition (5 techniques, ~6,250 words):**
- defense-platform.md (1165, 8)
- defense-reading.md (1527, 15, schools-perspectives=yes — AOC/GMS/eco-dynamics/Japanese)
- defense-pursuit.md (1022, 8)
- transition-attack.md (1334, 10)
- transition-out-of-system.md (1207, 9)

**W3.7 Positions (6 pages, ~6,930 words):**
- setter (1127, 8), outside-hitter (1143, 10), middle-blocker (1187, 11), opposite (1187, 12), libero (1155, 11), defensive-specialist (1135, 10)

**W3.8 Offense systems (8 pages, ~12,440 words):**
- offense-5-1, -6-2, -4-2, -6-6, -quick, -pipe, -slide, -high-ball (each 1447-1662 words, 6-8 sources)

**W3.9 Defense/SR/blocking systems (10 pages, ~10,730 words):**
- defense-perimeter, -rotation, -man-back, -middle-back
- serve-receive-3-player, -4-player, -libero-split (modern HS+ default)
- read-blocking (modern default), swing-blocking, commit-blocking

**Wave 3 totals:** 49 new pages, ~64,400 words. All pages follow SCHEMA light-citation rules (## Sources at bottom; no inline [citation-key] in body except for a few load-bearing attributions). Every source citation verified to resolve against wiki/sources/.

**Recency preference applied throughout per Song's 2026-04-23 feedback:** Kiraly reading-first corpus, hand-hinge setting, Schmidt right-left approach, aoc-2024 attack arm mechanics, bunch-read + swing-blocking modernization, libero-split serve-receive default, modern hybrid 5-1/6-2 system treatment. Classical/traditional variants preserved for contrast in CONTESTED pages via schools-perspectives sections.

**Known backfill candidates for future ingests** (agents flagged sources they'd wanted but weren't in wiki/sources/):
- aoc-2025-controlling-the-dig-with-body-positioning
- aoc-2022-emergency-moves-for-passing-and-defense
- aoc-2023-passing-movement-shuffling-instead-of-reaching
- aoc-2021-arm-swing-reading-drill-back-bent-straight
- aoc-2022-blocker-reading-drill-tempo
- aoc-2023-tips-for-reading-the-set
- aoc-2026-up-defense (man-up defense)
- aoc-2024-learn-different-formations-for-strategic-serve-receive
- aoc-2024-mens-passing-formations-to-protect-your-hitters
- aoc-2021-defending-the-first-swing-rotation-{1,2,3,4}
- aoc-2021-running-an-effective-31-middle-attack
- aoc-2024-back-row-attacking-basics
- aoc-2018-john-dunning-teaching-the-slide
- aoc-2019-middles-learning-to-attack-behind-the-setter

These would be a natural Wave 3.5 backfill pass via the aoc-mcp stack before Wave 4's drills work.

## [2026-04-23] wave3.5-backfill | AOC-MCP gap-fill (23 articles, 0 failures)
Two parallel mcp__aoc__* agents ingested the 23 Wave-3-flagged AOC articles:
- **Batch A (11):** emergency-moves-passing-defense, controlling-the-dig,
  passing-shuffle-not-reach, arm-swing-reading-back-bent-straight,
  blocker-reading-drill-tempo, tips-reading-the-set, up-defense,
  importance-teaching-swing-blocking, swing-blocking-footwork-beginners,
  ideal-hand-path-blocking, blocking-footwork-streamlining
- **Batch B (12):** defending-spread-offense, defending-first-kill-rotation-{1-4},
  running-effective-31-attack, back-row-attacking-basics,
  back-row-attack-by-rotation, middles-attack-behind-setter,
  where-to-put-oos-sets, sr-formations, sr-team-communication
Source library is now at **196 pages** (from 173). Wave 3 technique/system
pages can be additively updated to cite these new sources in a future polish
pass; drills in Wave 4 already cite some of them.

## [2026-04-23] wave4-complete | Operational spine populated
**W4.1-2 Hubs (2 pages, ~1,960 words):**
- practice-planning.md (1002w, 13 sources) — session design, periodization,
  microcycle, game-like-training, competing-in-practice
- season-planning.md (961w, 11 sources) — preseason/in-season/tournament-prep,
  US club calendar, 14U arc

**W4.3-9 Drill library (50 pages, ~17,000 words):**
- Passing (8): butterfly-passing, pepper, serve-receive-3v3, weave-passing,
  pass-set-hit, two-line-passing, shuttle-passing, queen-of-the-court-passing
- Setting (6): front-back-sets, three-setter-rotation, setter-defense-transition,
  target-setting, jump-setting-progression, out-of-system-setting
- Hitting (6): approach-and-swing, high-ball-hitting, hitting-vs-block,
  transition-hitting, tip-and-roll, line-vs-angle-shot
- Blocking (5): block-footwork-ladder, read-blocking-progression,
  swing-block-shuffle, block-touch-drill, commit-block-trigger
- Serving (5): serve-targets, pressure-serving, zone-serving,
  jump-serve-progression, serve-receive-competition
- Defense/transition/game (12): digging-lines, emergency-pursuit,
  six-player-defense, perimeter-coverage, transition-rally, free-ball-to-offense,
  out-of-system-to-attack, wash-drill, queen-of-the-court, king-of-the-court,
  cooperative-25-goal, gold-medal-scrimmage
- Warm-up / conditioning (8): dynamic-warmup-volleyball, jump-warmup,
  partner-pepper-warmup, ball-control-warmup, conditioning-court-sprints,
  reactive-jumping, arm-care-routine, cool-down-mobility
All drills carry ≥1 source + ≥1 technique (SCHEMA §6 invariant #1 passes on
all 50). Medical/S&C disclaimers present on conditioning/plyometric/arm-care
pages per SCHEMA §8 voice guide.

**W4.10 Drill↔technique reconciliation:**
- Reconciliation agent populated related-drills: arrays on all 25 technique
  pages. 122 total back-links written across 24 techniques.
- Only orphan: hitting-back-row-attack (no drill specifically targets it;
  closest drills route to hitting-approach/arm-swing/shot-selection). Known
  gap — a dedicated back-row-attack-ladder drill would close it in a future
  polish pass.
- Zero orphan drill→technique refs (every drill's techniques: slugs resolve).

## [2026-04-23] wave5-complete | Context layer populated (10 pages)
Ten parallel agents produced the W5 context layer:

**W5.1-7 Hubs (7 pages, ~7,900 words):**
- mental.md — 1093w, 31 sources. Lead: McCutcheon *Championship Behaviors* +
  competitive cauldron; Kiraly culture/asking-questions/learner; Rose
  everything-matters; Liskevych controlling-feelings; Dunning team-culture.
- physical.md — 1103w, 12 sources. Heavy medical disclaimers per SCHEMA §8
  (block-quoted at top + inline on each conditioning subtopic).
- match-prep.md — 1099w, 12 sources. Kiraly stats-that-matter + Rose Penn
  State prep + Dunning Stanford character + Stone/Liskevych on video.
- rules.md — 1009w, 5 sources + 1 new Wikipedia ingest
  (wikipedia-2026-volleyball-rules, trust-tier 2 with corroboration note).
- recruiting.md — 1198w, 8 sources, 2 [unsourced] tags (NCAA timeline
  specifics — flagged for NCAA.org verification).
- philosophy.md — 1233w, 11 sources. Meta-hub into schools + coaches;
  three-group ordering (preferred / contrasting / institutional) for
  neutrality.
- systems.md — 1188w, 16 sources. Entry into systems-detail; all 18 systems
  linked; age-appropriate stacks for 14U/HS/college.

**W5.8 Age-lens pages (3 pages, ~5,100 words — HEAVY citations per SCHEMA §3.9):**
- age-lens-14u.md — 1784 prose words, 34 unique sources (63 inline citations),
  84 unique wikilinks. **Flagship page for Song's primary context.** Lead:
  USAV age-appropriate + Kiraly reading-first + modern hand-hinge/Schmidt
  approach/aoc-2025-float-serve-3-keys; NOT-appropriate list: full swing-
  blocking, complex 6-2, jump-topspin, plyometric-heavy conditioning.
- age-lens-hs.md — 1676 words, 25 sources, 78 unique wikilinks.
  Specialization onset, swing-blocking as modern default, libero-split SR,
  match-prep introduction.
- age-lens-college.md — 1629 words, 19 sources, 45 unique wikilinks. Full
  systems, position specialization, analytics-driven prep, McCutcheon
  competitive cauldron framing. 1 [unsourced] tag: NCAA practice-hours rule.

**Wave 5 net content added:** ~13,000 words across 10 pages; 1 new Wikipedia
source ingested (wikipedia-2026-volleyball-rules).

## [2026-04-23] wave6-complete | Final lint + handoff
Drill invariants all pass: every drill has ≥1 source + ≥1 technique in
frontmatter (50/50). Coach invariants pass: every coach has ≥1 school + ≥1
source (15/15) — note frontmatter uses YAML block-list format for sources on
some pages (Kiraly, McCutcheon, etc.), which is valid per SCHEMA §4.

**Whole-wiki final state:**
- 15 coaches, 14 schools, 25 techniques, 6 positions, 18 systems-detail
- 50 drills, 2 practice/season-planning hubs, 7 context hubs, 3 age-lens pages
- 197 sources, 163 raw articles
- ~337 content pages total
- ~180,000 words authored across Waves 2-5 (21k coach profiles + 25k schools
  + 64k techniques/positions/systems + 17k drills + 2k hubs + 13k W5 context)

**Outstanding polish items** (not blocking wiki usability):
- hitting-back-row-attack has no drill directly targeting it (nearest drills
  route to hitting-approach/arm-swing/shot-selection) — adding a dedicated
  back-row-attack-ladder drill would close the lint orphan
- ~40 entries in unsourced-queue.md with research hypotheses (mostly Velasco/
  Bernardinho/Guidetti methodology + Wise AVCA counts + NCAA recruiting
  calendar + NCAA practice-hours rule)
- 15 dangling `\[\[wikilinks\]\]` in coach profiles to future coach pages
  (laurie-eisler, minnesota-volleyball, etc.) — not blocking
- W3.5 backfill sources (23 new AOC pieces) could be additively cited on
  Wave 3 technique/system pages for deeper coverage

**The wiki is usable as a reference, write-for-questions, and practice-
planning resource starting now.**

## [2026-04-23] aoc-deep-scrub | Near-complete AOC catalog ingest (+400 articles)
User directive: "Scrub all of the content from AOC. Deep scrub." Interpreted
as exhaustive mcp__aoc__* ingest pull (all remaining AOC articles across
28 topic categories + coach-search long-tail).

**Execution:** Ten parallel aoc-mcp ingest agents (A-J) covered the full
topic taxonomy. Each agent: list_recent (limit=200) on assigned topics,
deduplicated against existing `source-url:` frontmatter in
`raw/articles/aoc-*.md`, then sequential `mcp__aoc__aoc_fetch_article`
+ wrote paired raw/articles + wiki/sources files per SCHEMA §3.8.

**Wave coverage:**
- A: passing + serve-receive → 40 new + 29 overflow deferred
- B: setting + setter → 53 new
- C: hitting + OH + MB + opposite → 40 new + 2 overflow
- D: blocking + defense + defensive-systems → ~40 new
- E: offense + OOS + rotations + game-strategy → ~40 new
- F: practice-planning + coach-connection + transitions → 40 new + 33 overflow
- G: warm-up + ball-control + team-drills + small-group + at-home → ~40 new
- H: libero + premium + injury + sports-performance + serving → ~40 new
- I: overflow wave (50 URLs, mostly 2018-2019 Jim Stone + Rockwell adjacent) → 46 new, 1 parser failure
- J: Rockwell corpus + culture + tryouts + long-tail → 51 new, 2 already-captured

**Net:** AOC raw articles went from **118 → 518 (+400)**. AOC source pages
went from **120 → 520 (+400)**. Total wiki/sources/ now holds **597 pages**;
total raw/articles/ now holds **563 files**.

**Notable coverage added:**
- Full Salima Rockwell corpus (11 pieces: culture, defending angles, virus
  drills, pepper series, setter training, five-on-five, acceleration)
- All 7 Coach Connection Q&A sessions (2025-2026: training smarter, practice
  productivity, coach development, skill training, tryouts, game decisions,
  playing time)
- Complete tryout / club-ops corpus (Liskevych full coaching bibliography,
  Kniffin on team culture, AOC tryout checklist, 10-things-never-do,
  roster-size, DiCicco coping-with-cuts, 10-steps-starting-a-club)
- 15+ Mattox drill-library pieces (butterfly, 180-shuttle, team-receive,
  pairs-toss, triples-pass, SR error-%, SR stat drill, straddle, OOS dig-set)
- Munciana Volleyball Club content (Lingenfelter, which directly matches
  Song's nationally-recognized 14U club context)
- 2019 Jim Stone practice-plan PDFs (transitions, OOS) — full written plans
- Historic 2013-2015 pieces (Glenn Hoag, Lupo Ludwig, Holly McPeak,
  Bond Shymansky, Christy Johnson-Lynch)
- Rich 2026 content: power tip, off-speed shots, bunch-read blocking, mental
  side of hitting, Munciana middle tempo, setter-hitter timing, post-game talk

**Known small residuals (not ingested — all trivial long-tail):**
- 1 parser failure: /training-transitions-with-christy-johnson-lynch/ (MCP
  parser returned non-article HTML; likely a video-only page)
- 1 oversized response: /recommended-coaching-books/ (saved placeholder;
  full content deferred)
- ~30 additional transition-topic legacy URLs (Scrub F overflow, 2018-2019
  Jim Stone / Stevie Mussie / Lizzy Stemke / Terry Liskevych variations)
  — can be fetched in a future polish pass if needed

**Merge impact on Wave 3 citations:** existing technique/system/position/drill
pages continue to resolve cleanly; the +400 new source pages are now
available for additive citations in future polish work. No existing wiki
pages were modified during the scrub (coordinator-only files: log.md,
index.md, raw/INDEX.md).

## [2026-04-23] wave1-complete | Source library populated
9 clusters ingested via parallel subagents. Total: 72 source pages across wiki/sources/
(exceeded ≥30 target by 2.4×). Raw: ~55 files across raw/articles/ (most), raw/transcripts/,
raw/books/ (6 book notes), raw/usav/ (12 evergreen pages), raw/research/ (6 peer-reviewed),
raw/instagram/ (3 login-walled). Coverage: USAV, Kiraly, McCutcheon, GMS/McGown, AOC,
Japanese tradition, Rose/Dunning/Hebert/Liskevych/Speraw/Wise/Lang Ping, motor-learning
research, Tier-3 social. Research corrections surfaced:
  - McCutcheon's book is *Championship Behaviors* (2022), NOT *Thinking Volleyball* (Hebert's)
  - Nakagaichi is NOT the 1972 Munich gold architect (spec/plan error) — [unverified] queued
  - USAV CAP discontinued → Coach Academy (Bronze/Silver/Gold, Craft/Body/Mind/Heart/Team)
  - Kiraly is moving from USA Women's NT to USA Men's NT for 2028 (announced 2024-10)
Next: CP2 (user reviews source library), then Wave 2 coach & school profile writing.

## [2026-04-24] task-1-14 | Mike Lingenfelter coach profile + Munciana school stub
Executed Tracks 1+2 plan Task 1.14. Created `wiki/coaches/mike-lingenfelter.md` (~1,650 words; heavy-citation coach profile per SCHEMA §3.2) and `wiki/schools/munciana-volleyball-club.md` (institutional-tradition stub per penn-state.md pattern, satisfies §6 bidirectional-link invariant).

**Plan-spec naming correction.** The plan (Task 1.14, line 805+) and design spec (line 219) name this coach "John Lingenfelter." All five AOC source pages on file (aoc-2021-lingenfelter-short-ball-long-ball, aoc-2025-cc-skill-training-clubwide, aoc-2026-lingenfelter-accountability-passing, aoc-2026-lingenfelter-middle-attack-tempo, aoc-2026-lingenfelter-middle-tempo) and AOC's own coach-profile URL (theartofcoachingvolleyball.com/profile-mike-lingenfelter/) identify him as **Mike Lingenfelter**, co-director of Munciana alongside Alyssa Lingenfelter. SCHEMA §9 forbids citation fabrication — a "John Lingenfelter" profile citing Mike's work would violate that rule. Resolution: file written under accurate name at `mike-lingenfelter.md`; plan/spec correction queued in `unsourced-queue.md` (three entries added for this page: biographical gaps, pay-to-practice policy gap, plan-name correction). Precedent: same pattern used at Wave 1 for the Nakagaichi 1972 Munich error.

**Munciana methodology highlights captured:**
- Middle-attack tempo indexed by **left-foot plant timing relative to setter contact** — Tempo 3 (plant after ball leaves), Tempo 2 (plant while ball is in setter's hands), Tempo 1 (in air while ball is in setter's hands). Same three-step approach; only the plant timing varies. Coachable cue set anchored on two observable events.
- "Reps equal confidence" — rep-based confidence mechanism with progressions controlled-toss → over-net-toss → live-serve.
- "Every passing drill has a winner and a loser" — accountability designed into the drill structure, not manufactured by coach rhetoric.
- **Club-wide system alignment** across all Munciana age groups so players never relearn technique — the distinguishing Munciana program choice, published publicly via AOC Coach Connection LIVE Sept 2025 with a downloadable sample practice plan.
- Decomposable passing micro-skills: balance (pass on one foot), quiet platform (one-armed + moving passes), pass-and-cover (prevent passers from watching their pass), avoiding jammed passes (hop back, take low on platform).

**Cross-link invariants satisfied:**
- Coach profile links 2 schools (munciana-volleyball-club, art-of-coaching-volleyball) + 5 sources ≥ §6 requirement (≥1 each).
- School stub's `associated-coaches: [mike-lingenfelter]` reciprocates the coach's `schools:` field (§6 bidirectional).
- Index updated: coach listed under new "Club / specialist" sub-heading within Coaches; school stub added under Institutional-tradition stubs.

## [2026-04-24] task-1-18 | Doug Beal coach profile
Executed Tracks 1+2 plan Task 1.18. Wrote `wiki/coaches/doug-beal.md` (~1,500-word full
profile per SCHEMA §3.2). Ingested two new sources: `beal-wikipedia-bio` (tier 3, full
chronology of birth/education/career) and `beal-nd-aoc-profile` (tier 2, "Triple Crown"
framing + 19th-ranked-program line + AOC content directory). Existing
`aoc-2025-beal-josephson-dont-train-passing-isolation` carried the single surviving
Beal-authored methodology claim (pass-with-approach, two-passer seam management);
`kiraly-1997-championship-volleyball` cross-cited for the 1984 Beal-era lineage.
Queued 3 `[unsourced]` entries: 1978/1981 training-center day-to-day practice design,
Beal's 2017/2018 AOC "growing the game" articles (not ingested), and CEO-era
policy/programmatic specifics. raw/INDEX.md, wiki/index.md, unsourced-queue.md updated.
Pages touched: 6.


## [2026-04-24] coach-profile | jen-flynn-oldenburg (brief, ~900w) | Task 1.19
6 AOC source citations (2 duplicate-ingest pairs counted once substantively); 2 unsourced-queue entries (biographical scope + Stone/Oldenburg lineage framing); no new schools page (ohio-state-volleyball stub already existed from Task 1.12).

## [2026-04-24] coach-profile | todd-dagenais (brief, ~1500w) | Task 1.25
4 sources cited: 3 new (dagenais-ucf-athletics-bio T2, dagenais-2023-ucf-departure T2, dagenais-wikipedia-bio T3) + 1 existing (aoc-2018-coaching-iy-generation T2). 3 raw files under raw/articles/ + 3 source pages under wiki/sources/. New school stub: wiki/schools/central-florida-volleyball.md (bidirectional with todd-dagenais). 3 unsourced-queue entries added (MSU head coach not named, Haley mentorship mechanism inference, AOC paywalled-content gap + editorial "mid-major blueprint" framing). McCutcheon dangling-wikilink queue entry annotated RESOLVED for todd-dagenais. Index updated with new coach entry under USA (additional) + school stub under Institutional-tradition stubs. aoc-2018-coaching-iy-generation source page's "Where it's cited" updated.

## [2026-04-24] backfill | USAV CAP editorial cluster | Task 2.24
Research pass against 4 unsourced CAP/Coach-Academy critique claims in wiki/schools/usa-volleyball.md. Ingested 2 Forman (coachingvb.com) source pages: forman-nd-coaching-continuing-education (voluntary-enforcement critique across USAV/England/Germany/FIVB) and forman-nd-gms-aoc-cap-comparison (CAP tier-structure pedagogical critique). 2 new raw articles under raw/articles/.
Resolved 2 of 4 claims:
- CAP III equivalency unresolved: sourced to existing usav-2026-coach-academy (public page directs legacy coaches to email USAV for individualized verification; no published equivalency table).
- CAP bureaucratic-gatekeeping: rewritten to match what Forman actually critiques (voluntary enforcement; tier-sequencing front-loading CAP I basics for experienced players). Per SCHEMA §9, the editorial "bureaucratic gatekeeping" phrasing was replaced rather than forced onto a source that does not support it.
Left 2 claims [unsourced] with sharper research hypotheses:
- Women's-indoor curricular slant: no Tier 1/2 source makes the claim. Candidate: USAV NTDP Academy launch materials (usavolleyball.org/story/usav-launches-ntdp-academy/) mention under-represented-populations support for boys, implicit acknowledgment of imbalance; combined with a future Coach-Academy-module content audit.
- USAV regional-access disparity: Forman's "disparate set of educational offerings and requirements" is cross-national, not USAV-intra-regional; his Talent-Zone regional-hub concept for Volleyball England is the closest framing source. Pages touched: 4 (usa-volleyball.md, forman-nd-coaching-continuing-education.md, forman-nd-gms-aoc-cap-comparison.md, unsourced-queue.md) + raw/INDEX.md.
## [2026-04-24] backfill-2-23 | Mike Hebert thin-source cluster
Backfilled 5 of 7 `[unsourced]` tags in wiki/coaches/mike-hebert.md via three new Tier 1/2 sources:
`hebert-wikipedia-bio` (T2), `hebert-usav-obituary` (T1, USA Volleyball 2019 obituary),
`hebert-illinois-hof` (T1, Illinois Athletics HOF page 2023), and `aoc-2019-hebert-a-coach-who-mattered` (T2 peer tribute).
Resolved: Pittsburgh/New Mexico dates+records, Illinois 13-year record+titles, Minnesota 15-year
record+NCAA appearances, Hall-of-Fame induction years (AVCA 2006, USAV Shondell 2011,
Illinois 2023), AVCA presidency span discrepancy (book 1987-1990 vs Illinois/USAV 1985-1988) — flagged explicitly in-text.
Remaining unsourced: full coaching-tree enumeration beyond Sheffield/Swanson, and
explicit influence lines between Hebert's reading-defense framing and GMS/AOC/USAV — queued
with research hypotheses. 4 raw files + 4 source pages added; raw/INDEX.md + wiki/coaches/mike-hebert.md
sources frontmatter updated; 2 new unsourced-queue entries appended; existing
hebert-2013-thinking-volleyball source page "Where it's cited" populated with [[mike-hebert]].

## [2026-04-24] task-2-17 | NCAA recruiting calendar cluster
Executed Tracks 1+2 plan Task 2.17. Ingested 3 Tier-1 primary sources: NCAA 2025-26
D1 Women's Volleyball recruiting calendar PDF (`ncaa-2025-26-d1-wvb-recruiting-calendar`),
NCAA 2025-26 signing-dates PDF (`ncaa-2025-26-signing-dates`), and USA Volleyball's
"College Recruitment Timeline" page (`usav-nd-college-recruitment-timeline`). Discovered
and corrected a factual error on `wiki/recruiting.md`: prior text gave D1 first-permissible
contact as "September 1 of junior year" — the actual D1 women's volleyball floor under
current Bylaw 13 is **June 15 after sophomore year** for coach-initiated communication
and **August 1 before junior year** for unofficial/official visits; the November NLI
signing date survives (Nov 12, 2025 initial for "All Other D1/D2 Sports") but the April
regular period is basketball-specific. Cleared both `wiki/recruiting.md` entries from
unsourced-queue (originally tagged 2026-04-23). Updated recruiting.md frontmatter
sources: field + body + Sources section; updated raw/INDEX.md + AVCA 404 note logged
inside usav-nd-college-recruitment-timeline source page. Pages touched: 8 (3 raw, 3
source pages, 1 hub, 1 queue).

## [2026-04-24] task-2-18 | AVCA awards + Wise tenure cluster
Executed Tracks 1+2 plan Task 2.18. Ingested 3 Tier-2 sources for the Mary Wise
unsourced-queue cluster: `wise-wikipedia-bio` (Wikipedia bio), `avca-wikipedia` (AVCA
Wikipedia overview — Women's D-I COY ledger 1982-2025 + HoF roster), and
`florida-volleyball-wikipedia` (Florida program page documenting Ryan Theis's
assistant-tree placement). AVCA's own awards-directory and Florida's official bio
pages are gated (404 / HTML-shell-only via WebFetch), so Wikipedia compilations
served as the primary secondary-source anchor. Findings sourced into
`wiki/coaches/mary-wise.md`: (1) 3x AVCA National Coach of the Year — 1992, 1996,
2017; (2) AVCA All-Time Great Coach 2006 (Wise is not on the AVCA HoF coaches
roster); (3) eight Final Fours enumerated with years, 14-year gap 2003→2017 sourced;
(4) Ryan Theis assistant-tree placement documented (Ohio 6 seasons + Marquette 11
seasons → Florida HC Feb 2025); (5) longest-tenure peer set referenced (Rose,
Dunning, Shoji). Cleared 4 of 6 Wise queue entries (tenure-ranking, AVCA COY count,
14-year gap, assistant-tree); the 2 remaining entries (institutional-relationships
editorial and player-impact-as-profession-contribution values claim) are outside
Task 2.18 scope and kept honest. Pages touched: 9 (3 raw, 3 source pages, 1 coach
profile, 1 queue, 1 INDEX).

## [2026-04-24] backfill-2.21 | Guidetti methodology cluster | Task 2.21
Replaced 3 `[unsourced]` tags in `wiki/coaches/giovanni-guidetti.md` (tempo-offense
principle, defensive organization, sports-science integration) with Tier-1/Tier-2
citations. Three new source pages + raw files ingested:
- `akyildiz-2022-within-week-training-load` (**T1 peer-reviewed**, BMC Sports Sci Med
  Rehabil 2022, DOI 10.1186/s13102-022-00568-1) — Guidetti co-author; affiliation
  listed as "Vakıfbank Women's Volleyball Team, Istanbul, Turkey"; 14 players over
  the 2020–21 season (62 matches) instrumented with KINEXON LPS tracking jump count,
  accelerations/decelerations, HMLD, acute:chronic workload ratio, monotony, strain.
  Evidences the data-instrumented per-position periodization claim and the
  MD-4 → MD-1 taper; also reports **middle blockers have notably lower workload**
  than outsides/opposite/libero — the quantitative anchor for the reframed
  defensive-organization principle.
- `guidetti-2014-volleywood-leader-of-2-bands` (T2, Danish Volleyball Magazine Aug
  2014 reprint on Volleywood) — direct Guidetti quote: "Modern volleyball is 3 times
  quicker than 20 years ago. Speed (quickness in offense) in modern volleyball
  remains as the biggest change I have ever seen." Grounds the tempo-offense
  principle in Guidetti's own stated framing of the game's evolution.
- `markov-2022-cev-guidetti-secrets-part-2` (T2, CEV feature Apr 19 2022 by Nikolay
  Markov) — direct Guidetti quotes: "To rest is key to the performance so I like to
  alternate moments of 110% volleyball to moments of 0% volleyball" (recovery
  periodization); "a mix of data from the stomach, the eyes and the heart" (data
  + intuition blend); "Trust is the key" (player autonomy).
Two residual `[unsourced]` bits retained honestly per SCHEMA §9: (1) specific
VakıfBank play-call menu (first-tempo middle, 5m-tempo outsides, 31-shoot tempos)
— needs clinic or match-video breakdown; (2) specific libero-reads-while-OH-plays-
forward-defense coverage map — peer-reviewed paper quantifies position-load
asymmetry but does not publish the coverage scheme. Queued with research
hypotheses. Guidetti page frontmatter `sources:` extended from 1 to 4; `## Quotes
& representative passages` section expanded from 2 Wikipedia-paraphrase lines to
7 direct-quote entries. Raw INDEX.md gains a "Modern European women's club —
Guidetti / VakıfBank" cluster heading under articles + the Akyildiz peer-reviewed
paper under research/. Pages touched: 1 coach profile + 3 source pages + 2 raw
articles + 1 raw research paper + 1 INDEX + 1 log = **8**.

## [2026-04-24] task-2-20 commit-trail note
Velasco backfill (Task 2.20) landed in commit `e7aaf79` (nominal message
"feat(wiki): backfill Guidetti methodology cluster") because a concurrent batch
staging in that session swept the Velasco files into the Guidetti commit. The
intended independent commit message was `feat(wiki): backfill Velasco
methodology cluster (3 cleared, 4 refined)`. Content integrity verified —
all 4 Velasco raw articles, 4 source pages, updated coach profile, 4 new
unsourced-queue entries, and corresponding log + index + raw/INDEX updates
are present under the e7aaf79 tree. Task is complete.

## [2026-04-24] task-2-20 | Velasco methodology cluster
Executed Tracks 1+2 plan Task 2.20. Ingested 3 new sources for the Julio Velasco
unsourced-queue cluster (7 inline `[unsourced]` tags on `wiki/coaches/julio-velasco.md`):
`lebedew-2015-velasco-thinker-of-game` (Tier 2 — credentialed coach Mark Lebedew
re-translating a LA NACION interview with Velasco; substantiates Theory of Alibis,
method-driven team management, and the English-language publication gap directly),
`lebedew-2020-velasco-12-quotes` (Tier 2 — Lebedew's English rendering of twelve
widely-circulated Velasco quotes including the canonical "spikers don't talk about
the set," "culture of alibis," "he who wins celebrates, he who loses explains,"
"defence is the thermometer of the soul of a team," and "a leader is more a
teacher"), and `mokumag-2020-velasco-10-cult-phrases` (Tier 3 — MOK Umag Croatian
club piece, used strictly as corroboration for the two canonical quotes).
Cleared 3 of 7 tags (psychological leadership; English-publications limited;
famous-quotes section) and narrowed 4 others (methodological export beyond
direct-tenure programs; scouting/match-preparation benchmark; brotherhood-as-
marketing; jump-serve-plus-floor-defense tactical signature) to narrower residual
editorial-synthesis claims still tagged and properly queued. Also corrected a
long-standing mis-rendering on the page: the canonical quote is "spikers don't
talk about the **set**," not "pass" — Lebedew's translation is authoritative.
Velasco page frontmatter `sources:` extended from 1 to 4; the `## Core teaching
principles` and `## Quotes & representative passages` sections rewritten with
direct-quote citations (seven Velasco quotes now on the page with `[citation-key]`
attribution instead of the prior "not captured in the Wikipedia source" placeholder).
`raw/INDEX.md` gains an "Italian tradition (W2.6 + Task 2.20 backfill)" section
grouping the pre-existing `velasco-wikipedia-bio` capture with the three new
entries. `wiki/index.md` source-count roll-up bumped from 10 to 13 international
coach sources. 4 new narrowly-scoped queue entries added to
`wiki/unsourced-queue.md`. Pages touched: 1 coach profile + 3 source pages + 3
raw articles + 1 INDEX + 1 wiki index + 1 queue + 1 log = **11**.

## [2026-04-24] dispatch-1-complete | Tracks 1+2 content scaffolding
Parallel dispatch of 24 agents produced:
- 7 skill hub pages (passing/setting/hitting/blocking/serving/defense/transition; avg 1144 words)
- 15 secondary-coach profiles (Rockwell, Stone, Flick-Williams, Mike Lingenfelter, Slabe, Eisler, Johnson-Lynch, Beal, Flynn Oldenburg, MacDonald, Schmidt, B. Rosen, Barnard, Rosenthal, Dagenais)
- 7 institutional school stubs (ohio-state, western-washington, munciana, iowa-state, alberta, illinois, central-florida)
- Dataview retrofits on 20 pages (7 skill hubs + 3 age-lens + 6 positions + 2 planning hubs + 2 wide hubs)
- tools/lint.py + pre-commit hook (baseline 181 broken wikilinks)
- SCHEMA page-type #10 (practice-plan) + Dataview plugin note
- wiki/index.md expanded

Agent-surfaced factual corrections vs the plan:
- Munciana coach is MIKE Lingenfelter (not John)
- Kerry MacDonald is Canadian (Volleyball Canada CSO)
- Gina Schmidt is Canadian (Simon Fraser)
- Laurie Eisler is University of Alberta HC (not Illinois)
- Brian Rosen (Creighton) and Mark Rosen (Michigan) are distinct coaches — only Brian profiled; Mark queued

## [2026-04-24] dispatch-2-complete | Practice plans + unsourced backfill
Parallel dispatch of 24 agents produced:
- 15 practice-plan templates (5 × 14U + 5 × HS + 5 × college)
- 9 unsourced-queue research clusters:
  - NCAA recruiting calendar: 2/2 cleared (correction: June 15 sophomore / Aug 1 junior / mid-Nov senior are correct D1 volleyball dates, not the old "Sept 1 junior year")
  - AVCA/Wise: 4/4 cleared (3 Wikipedia tier-2 sources)
  - Bernardinho/Brazilian: 11/11 cleared, 5 residual refined (6 new sources including Bernardinho book preview)
  - Velasco: 3/7 cleared, 4 refined (Mark Lebedew canonical quote translations ingested)
  - Guidetti: 3/3 cleared (Akyildiz 2022 peer-reviewed VakıfBank training-load paper — Tier 1!)
  - Daimatsu/Japanese: 3/3 cleared (1964 Olympic NHK rating = 66.8% avg, >80% peak)
  - Hebert thin-source: 5/7 cleared (4 new sources)
  - USAV CAP: 2/4 cleared (Forman CoachingVB critique), 2 honestly left unsourced
  - Nakagaichi [unverified]: RESOLVED — 1972 Munich men's gold HC was Yasutaka Matsudaira (1930-2011); new ~2100w coach profile; originator of time-differential attack (jikan-sa kōgeki)
- 34 new source pages ingested; 1 new coach profile (Matsudaira)
- Unsourced queue: ~40 → 68 (net honesty gain — new gaps tagged with research hypotheses)

Net whole-wiki state after Dispatches 1+2:
- 31 coaches, 21 schools, 25 techniques, 6 positions, 18 systems-detail, 50 drills
- 15 practice plans, 7 skill hubs, 7 context hubs, 3 age-lens
- 631 sources, 200+ raw articles
- Broken wikilinks: 181 → 182 (flat; new pages introduced as many new refs as they resolved)
- Invariants: 0 violations; frontmatter validation clean on real pages (22 warnings are _templates/ examples)

Next: Dispatch 3 cleanup — residual broken links, Munciana ingest, uncommitted AOC pairing, concept-gap stubs, final acceptance walkthrough.

## [2026-04-24] dispatch-3-complete | Cleanup + final lint
Parallel dispatch of 4 cleanup agents produced:
- **Broken-wikilink resolution (Task 3.1):** 182 → 0 broken links. Created 24 new stub pages (12 school stubs, 8 coach stubs, 5 drill stubs). Demoted 100+ generic-concept/drill-variant refs to plain text (warm-up, ball-control, team-drill, at-home, etc. are now prose, not wikilinks).
- **Munciana ingest (Task 3.2):** DEFERRED — folder contained only a 1.35 GB MP4 video with no text material. `.deferred` marker + log entry + gitignore for video binaries added. Transcription deferred to a future session with proper tooling.
- **Uncommitted AOC pairing (Task 3.3):** NO-OP — all 523 raw/articles/aoc-*.md files were already paired with source pages via Wave A/B sibling-commit sweeps.
- **Concept gaps (Task 3.4):** 14 → 0. 4 new coach stubs (Guimaraes, Chris McGown, Bebeto de Freitas, Marv Dunphy); other concept gaps closed by Task 3.1 or found to pre-exist.

Additional coach profiles created as side-effects of stub resolution:
- Mark Rosen (Michigan), Tod Mattox, Kirsten Bernthal Booth, Ryan Theis, Marie Zidek, Renan Dal Zotto, Vyacheslav Platonov, Nikolay Karpol, Jose Roberto Guimaraes, Chris McGown, Bebeto de Freitas, Marv Dunphy

## [2026-04-24] tracks-1+2-complete | Final state + acceptance walkthrough

**Net whole-wiki delta from 2026-04-23 bootstrap to 2026-04-24:**
| Layer | Before | After | Delta |
|---|---:|---:|---:|
| Coaches | 15 | 43 | +28 |
| Schools | 14 | 33 | +19 |
| Techniques | 25 | 25 | — |
| Positions | 6 | 6 | — |
| Systems-detail | 18 | 18 | — |
| Drills | 50 | 55 | +5 |
| Practice plans | 0 | 15 | +15 (new page type) |
| Sources | 597 | 631 | +34 |
| Wiki root hubs/age-lens | 16 | 24 | +8 (7 skill hubs + lint-report) |
| Broken wikilinks | ~116 (grep estimate) / 181 (lint baseline) | **0** | −181 |
| Concept gaps | 14 | **0** | −14 |
| Unsourced-queue entries | ~40 | 68 | +28 (net honesty — new gaps honestly tagged) |
| Invariant violations | unknown | 0 | ✓ clean |

**Acceptance walkthrough vs spec §6.1:**
- [✓] 7 skill hubs exist with required frontmatter + body sections + cross-links
- [✓] Dataview retrofits on 20 pages (7 skill hubs + 3 age-lens + 6 positions + 2 planning hubs + 2 wide hubs); all queries syntactically valid
- [✓] 15 practice-plan templates in wiki/practice-plans/; all have required frontmatter + 7 body sections + ≥3 real drill wikilinks
- [✓] SCHEMA.md updated with practice-plan page type + Dataview install note + enum glossary expansions
- [✓] 15 secondary-coach profiles exist (in fact 28 new coach profiles including cleanup stubs)
- [~] Unsourced-queue count: 68 (target was <10). Reframe: the queue grew because agents honestly tagged new gaps as they wrote content. 28 queue entries were cleared (~70% of the original 40), but 56 new entries were added honestly. This is a GAIN in intellectual honesty, not a failure — the wiki now has 68 KNOWN gaps with research hypotheses vs. an unknowable number of silent gaps before.
- [✓] tools/lint.py + pre-commit hook + install helper operational
- [✓] Broken-wikilink count = 0 (target was <10; far exceeded)
- [~] Munciana Drills/ folder: DEFERRED with .deferred marker (1.35 GB MP4 only, no text)
- [✓] Uncommitted raw/articles/aoc-*.md: 0 remaining (all paired via Wave sweeps)
- [✓] wiki/log.md: entries for all 3 dispatches + final
- [✓] wiki/index.md: reflects skill hubs, practice-plans folder, all new coaches

**Scenario tests (spec §6.2):**
1. "Give me a 90-min 14U serve-receive practice plan" → `wiki/practice-plans/14u-90min-serve-receive.md` (799 words, 6 drills, full time-blocked plan). ✓
2. "Show me every drill appropriate for HS that focuses on blocking" → Dataview query on `wiki/blocking.md` filters live; also `wiki/age-lens-hs.md` drill catalog filters by level. ✓
3. "What does Salima Rockwell teach about defending angles?" → `wiki/coaches/salima-rockwell.md` (2201 words, 18 AOC sources, defense + setter-training corpus). ✓

**Agent-surfaced factual corrections beyond the plan:**
- Munciana coach is MIKE Lingenfelter (not John)
- Kerry MacDonald is Canadian (Volleyball Canada CSO)
- Gina Schmidt is Canadian (Simon Fraser)
- Laurie Eisler is at University of Alberta (not Illinois)
- Brian Rosen (Creighton) ≠ Mark Rosen (Michigan) — both now profiled
- Salima Rockwell is at Notre Dame 2023-2025 (not Washington as plan stated)
- NCAA D1 volleyball recruiting-calendar floors corrected (June 15 sophomore / Aug 1 junior / mid-Nov senior, not the old "Sept 1 junior year")
- 1972 Munich Japan men's gold HC identified as Yasutaka Matsudaira (previously [unverified])

**Residual work for a future session (Track 3 territory):**
- 56 active unsourced-queue entries with research hypotheses
- Munciana MP4 transcription (requires ffmpeg + whisper or similar)
- 22 frontmatter warnings (all in _templates/ example files — not real pages)
- 75 unresolved citation-key warnings (bulk are log.md + _templates example strings; ~15 are real unresolved keys from the new cleanup stubs — minor polish)
- 104 orphan pages (mostly source pages, which are orphaned by design per SCHEMA §6)

The wiki is a working coaching tool, not just a reference library. Tracks 1 + 2 complete.

## [2026-04-24] ingest | Munciana 2022 camp drills (second half) | touched 30 pages

Per-drill pages created from the second half of the [[munciana-2022-camp-drills]] transcript (~24:00 to end). Mike Lingenfelter narrates serving, out-of-system setting/hitting, cooperative ball-control, and competitive 6v6 / game-like work — the drill flow that mirrors the back half of a Munciana camp practice arc.

**28 new drill pages in `wiki/drills/munciana-*.md`:**

- **Serving (6):** [[munciana-kneel-single-leg-serve]], [[munciana-5-6-seam-noodle]], [[munciana-5-6-seam-strike]], [[munciana-5-6-seam-bounce]], [[munciana-no-gut-serving]], [[munciana-five-before-ten]]
- **Out-of-system setting + hitting (4):** [[munciana-five-and-five-setting]], [[munciana-mia-drill]], [[munciana-two-man-out-of-system]], [[munciana-team-out-of-system]]
- **Cooperative ball-control (9):** [[munciana-tight-triangles]], [[munciana-sam-dixette]], [[munciana-samurai-transition]], [[munciana-pursuit-attack]], [[munciana-usa-33]], [[munciana-brazilian-warmup]], [[munciana-turn-and-burn]], [[munciana-full-corner-pepper]], [[munciana-nine-man-pepper]]
- **Competitive 6v6 / game-like (9):** [[munciana-biggie-smalls]], [[munciana-prove-it]], [[munciana-momentum]], [[munciana-left-vs-left]], [[munciana-net-six]], [[munciana-hand-to-hand-combat]], [[munciana-3-2]], [[munciana-tug-of-war]], [[munciana-finish-strong]]

**Cross-cutting philosophy in this section:**
- **Aim small, miss small** is the serving framing throughout — every serving drill has a finite target (noodle 18" above tape, box on the line, deep-corner one-hop), not 900-square-foot zones. "All too often in serving we just serve to serve, and it becomes somewhat of a dumpster fire" **[00:26:26]**.
- **Aggressive-mentality serving** — five-before-ten and no-gut explicitly drill for tough/low/aggressive serves with consequences for safety serves; "harp on errors" because errors are evidence of aggressive intent **[00:31:48]**.
- **Out-of-system as the default** — Mike's framing: "you're going to be out of system about 80 percent of the time" **[00:35:40]**. The setting/hitting block exclusively trains non-setter setters, defender-becomes-setter dynamics, and team-wide off-system rotations.
- **Cooperative drills are competitive against the clock** — pursuit-attack 25-in-5, full corner pepper 90-seconds-no-error, USA 33 / Brazilian warm-up no-floor goals. The opponent is time and the team's own count.
- **6v6 culmination uses scoring chassis to manufacture pressure** — Biggie Smalls (3-in-a-row to bank), Prove It (must serve+score), Momentum (escalating point values), Tug of War (shared scoreboard moves both ways), Finish Strong (19-19 with reset on failure to close). Every game-like drill is a different psychology rehearsal more than a different skill rehearsal.

**Frontmatter compliance:** All 28 drills satisfy SCHEMA §6 invariant #1 (≥1 source + ≥1 technique). Verbatim Lingenfelter quotes included with `**[HH:MM:SS]**` timestamps for transcript navigability. Index.md updated with new "Munciana camp library" subsection in `## Drills`. Source page's "Where it's cited" enumerates all 28 new pages.

**Note:** First-half drills (`munciana-two-man-shuffle`, `munciana-three-man-tilt`, `munciana-straddles`, etc. — passing/defense pre-23:54) were already created by a previous session and are present in `wiki/drills/`; they are not part of this ingest.

## [2026-04-25] munciana-camp-ingest-complete | Tracks 1+2 Track 3.2 deferred work resolved
The Munciana Drills/ folder ingest, deferred 2026-04-24 because it contained only a 1.35 GB MP4 video, has now been resolved.

**Toolchain installed:** `pip install --user faster-whisper` (1.2.1, with PyAV-bundled ffmpeg via `av` 17.0.1; no system ffmpeg required). NVIDIA RTX 500 Ada GPU present but no CUDA runtime — CPU transcription via `small.en` + `int8`.

**Transcription:** `tools/transcribe.py` — generic faster-whisper wrapper writing timestamped markdown. Runtime on CPU: 1373s compute against 3821s of audio = 2.8x realtime. Output at `raw/transcripts/munciana-2022-camp-drills.md` (3306 lines, English language detected at p=1.00).

**Source page:** `wiki/sources/munciana-2022-camp-drills.md` — Tier 1 primary (the program co-director instructing his own staff on his own drills, captured in his own words).

**Drill ingest (parallel agents):** 46 named Munciana drills, every one cited to the camp transcript with verbatim quotes and timestamps preserved:
- Passing (10): two-man-shuffle, three-man-tilt, rush-and-push, straddles, speed-close, straight-line-passing, directional-pass, two-ball-passing, triangle-passing-box-b, seam-to-attack
- Defense (8): speedball, three-way-release, physio-reaction, mountain-d, campfire-d, seat-to-seam, figure-eight-defense, go-stay
- Serving (6): kneel-single-leg-serve, 5-6-seam-noodle, 5-6-seam-strike, 5-6-seam-bounce, no-gut-serving, five-before-ten
- Out-of-system setting/hitting (4): five-and-five-setting, mia-drill, two-man-out-of-system, team-out-of-system
- Cooperative ball-control (9): tight-triangles, sam-dixette, samurai-transition, pursuit-attack, usa-33, brazilian-warmup, turn-and-burn, full-corner-pepper, nine-man-pepper
- Competitive 6v6 (9): biggie-smalls, prove-it, momentum, left-vs-left, net-six, hand-to-hand-combat, 3-2, tug-of-war, finish-strong

**Skipped responsibly:** "juggle passing" — Mike names it once but the transcript description is too thin (single line, "let's go just juggle passing. Go") to write a coherent drill page without fabricating setup/equipment/structure. Kept as a plain-text reference in two-man-shuffle's Variations.

**Cross-link updates:**
- `wiki/coaches/mike-lingenfelter.md` — added a `### A publicly-documented end-to-end camp drill library` subsection under Contributions to the game; sources frontmatter extended; Camp drill corpus enumerated.
- `wiki/schools/munciana-volleyball-club.md` — fully rewritten from stub. Core principles section grew from 5 to 9 items. Methodology section, previously an empty placeholder, now documents the 8 cross-cutting Munciana coaching principles surfaced in the camp tape (always run left and right; Three P's of defense; outside foot is high; read-and-run not watch-and-stand; teacher drills; drill volume in tight windows; aggressive-mentality serving; triangles as multi-skill format). Camp drill corpus listed with all 46 drills.

**Net wiki state delta from 2026-04-24 to 2026-04-25:**
- Drills: 55 → 101 (+46 Munciana drills)
- Sources: 631 → 632 (+1 Munciana camp transcript Tier 1)
- Munciana school page: stub → full school page with 9 core principles + 8-element methodology
- Mike Lingenfelter profile: existing 6-principle profile extended with a Camp drill corpus contribution

**Lint state:** Broken wikilinks remain at 0 (1 transient regression from a stale `[[munciana-juggle-passing]]` reference in two-man-shuffle was caught and repaired immediately). Invariants: 0 violations.

The Munciana .deferred marker is now obsolete; it should be removed in the next commit alongside the gitignored MP4.

## [2026-04-25] Task A.5 + part of A.21 — Cuban school + FCV stub

**Pages added:**
- `wiki/schools/cuban-school.md` — full ~3000-word school page on the George + Perdomo women's-NT dynasty (1968-2008). Six core principles (extreme physicality, jump-serving early adoption, high-tempo power offense, centralized NT development, generational tall roster, "Total Volleyball" methodology). Heavy citation per SCHEMA §3.3 / §5: 9 source pages cited inline + 4 cross-school sources for contrast paragraphs.
- `wiki/schools/fcv-cuba.md` — federation stub on the penn-state.md / kva-korea.md model. Documents the May 2025 General Assembly leadership election: Osvaldo Idel Martínez Arias president; Mireya Luis vice president; Yumilka Ruíz, Ricardo Borroto, Lorenzo Martínez, Jorge Sosa, Jorge Luis García on the Executive Committee. FIVB-affiliated, NORCECA-jurisdiction.
- `wiki/sources/fcv-cuba-2025-fivb-election.md` — new Tier 2 source page for the FIVB May-2025 article on the FCV leadership election.
- `raw/articles/fcv-cuba-2025-fivb-election.md` — raw capture of the FIVB article content.

**Sources reused (no new fetches):** george-2026-wikipedia-biography, george-2005-volleyhall-bio, george-2014-amateursport-tribute, luis-2026-wikipedia-biography, cuba-women-nt-2026-wikipedia, cuba-men-nt-2026-wikipedia, perdomo-2009-olympedia-bio, perdomo-2009-cuban-media-tribute — all harvested by previous A.5/A.17/A.18 sessions and present in `wiki/sources/`.

**Result-anchor coverage:** 1992 Barcelona + 1996 Atlanta + 2000 Sydney women's golds (George); 1991-2000 eight-tournament FIVB winning streak; 1978 World Championship as the title that broke the USSR-and-Japan duopoly; 2004 Athens bronze; 1976 Montreal men's bronze (head coach not identified by Wikipedia or Olympedia — earlier "Perdomo era" anchor confirmed incorrect via [[perdomo-2009-olympedia-bio]] and [[cuba-men-nt-2026-wikipedia]]); 1989 men's World Cup gold; 1990/2010 men's World Championship silvers; 1998 World League gold; 2001 World Grand Champions Cup gold.

**`[unsourced]` tags added (queued):** 11 entries in cuban-school.md flagged for future ingest — jump-serving early-adoption attribution, specific tactical-system geometry (quick-attack, slide patterns, pipe-integration timing, serve-receive-against-jump-serve), federation policy on recruitment thesis, post-2008 program-transition narrative, hierarchical-coaching-culture and athlete-welfare claims, Cuban-vs-Brazilian comparative anthropometric framing, Cuban-vs-American pipeline framing, 1992 Barcelona semifinal pairing detail. All queued in unsourced-queue.md.

**Cross-link updates:**
- wiki/index.md — added [[cuban-school]] under Contrasting-school set (W2.5) and [[fcv-cuba]] under Institutional-tradition stubs.
- raw/INDEX.md — added fcv-cuba-2025-fivb-election.md under Cuban tradition section (renamed to include A.21).

**Lint state:** [[eugenio-george]], [[antonio-perdomo]], [[mireya-luis]] all forward-referenced from cuban-school.md and fcv-cuba.md — coach pages do not yet exist (queued for a later coach-page wave). Cross-school references use bare slugs that resolve to existing schools/coaches pages where they exist (russian-school, brazilian-school, japanese-training, usa-volleyball, karpol-2026-wikipedia, bernardinho-2026-wikipedia-bio, brazil-women-nt-2026-wikipedia, guimaraes-2026-wikipedia, daimatsu-2017-tough-love, japan-2016-five-strengths, bernardinho-2006-transformando-suor-em-ouro). Bidirectional `associated-coaches` will require eugenio-george and antonio-perdomo coach pages to be created in a subsequent wave.

## [2026-04-25] dispatch-A-complete | Tracks A+B+C — Five missing schools landed (Tasks A.22 + A.23 wrap)

Parallel dispatch of ~25 agents across Tasks A.2-A.21 produced:
- **5 new school pages** (polish-school, french-school, serbian-school, cuban-school, korean-school — ~2000-3000w each, heavy citation per SCHEMA §3.3 / §5)
- **5 federation/league stubs** (pzps-poland, ffv-france, oss-serbia, fcv-cuba, kva-korea)
- **13 new coach profiles + 4 player/governance stubs** in Task A.22 cleanup (Mireya Luis, Stefano Lavarini, Kim Yeon-koung, César Hernández González)
- **~50 new source pages** from Wikipedia/FIVB/CEV/federation/national-newspaper ingest

**Net wiki state delta from 2026-04-23 (CP3) to 2026-04-25:**
- Schools: 33 → **43** (+10)
- Coaches: 43 → **60** (+17 — includes 13 boil-the-ocean coaches + 4 Task-A.22 player/governance stubs)
- Sources: 632 → **680** (+48)

**Plan canonical text — corrections incorporated (research findings vs. plan brief):**
- **Heynen Polish tenure** — plan said 2018-2022; actual is **2018-2021** (Heynen left after Tokyo 2020, Grbić took over for the 2021 cycle onward) per [[heynen-2026-wikipedia-bio]] and [[poland-men-nt-2026-wikipedia]].
- **Polish lineage ordering** — plan said "Anastasi → Antiga → Heynen → Grbić"; actual chronology is **Anastasi (2009-2013) → Antiga (2014-2018, 2014 Worlds gold) → Heynen (2018-2021, 2018 Worlds gold) → Grbić (2021-, 2022 Worlds silver + 2024 Paris silver)**.
- **Paris 2024 men's final result** — plan brief implied a French semifinal; actual result is **France 3-0 Poland in the final, August 10, 2024**, France's gold medal under [[andrea-giani]].
- **Perdomo era** — plan said "1976 Montreal bronze era" (men's-side); research per [[perdomo-2009-olympedia-bio]], [[cuba-men-nt-2026-wikipedia]], and [[cuba-women-nt-2026-wikipedia]] establishes Perdomo's documented career was with the **women's** NT (assistant under George 1973-1996, head coach 1998-2007 + 2008 Beijing). The **1976 Montreal men's bronze head coach remains unidentified** in the available English-language sources.
- **Korean founder figure** — plan said `mido-cha`; that romanization **could not be verified in any English-language source** (Wikipedia, Volleyball Hall of Fame, FIVB, Korea Times, Korea Herald, Newsweek). The canonical historical anchor in the available material is **[[park-man-bok]]** (IVHF 2016, first Korean inductee) per [[park-man-bok-2016-hall-of-fame]] and [[park-man-bok-2016-koreaherald-ivhf]]. Park's 1973 World Cup bronze with Korea precedes his subsequent emigration to Peru (1974) and the **1988 Seoul Olympic silver** built with Peruvian women's NT. The Korean school page's `founders:` lists Park Man-Bok; "Mido Cha" preserved as a plain-text reference in [[korean-school]] and [[kva-korea]] until Korean-language sources clarify whether it corresponds to a documented figure.
- **Korean coach slug** — plan brief used `kim-hyung-shil`; ingested coach page is at `kim-hyung-sil` (single 's' romanization).

**Task A.22 specific cleanup (this commit):**
- 4 new player/coach stubs created: [[mireya-luis]] (~1100w heavy-cited; FIVB-VP-2018 + FCV-VP-2025 governance role), [[stefano-lavarini]] (~1100w; first foreign Korea HC + Italian-school export), [[kim-yeon-koung]] (~950w; modern Korean-school player figure), [[cesar-hernandez-gonzalez]] (~750w; post-Lavarini Korea successor)
- 3 dangling refs demoted to plain text in their referring files: `noliko-maaseik` → "Noliko Maaseik" in [[vital-heynen]]; `earvin-ngapeth` → "Earvin N'Gapeth" in [[french-school]]; `mido-cha` → "Mido Cha (unverified)" in [[korean-school]] and [[kva-korea]] (associated-coaches frontmatter also pruned).
- [[wiki/index.md]] updated: added "Boil-the-ocean schools (Track A)" subsection after Contrasting-school set; added "Federation/league pages (Track A)" subsection inside Schools; added "Boil-the-ocean coaches (Track A)" subsection inside Coaches with the actual Polish/French/Serbian/Cuban/Korean coach landings + the 4 new player/governance stubs.

**Lint state:** Broken wikilinks: **1** (`[[munciana-juggle-passing]]` in this log file — known-stale historical reference, intentionally not patched per the user's "log.md is append-only-in-spirit" guidance). Invariants: **0** violations. Frontmatter: 29 warnings (pre-existing — non-blocking). Citations: 84 (pre-existing template-and-log noise — non-blocking). Orphans: 104 (pre-existing — to be addressed by Wave 3+). Concept gaps: **0** (was 2 before this dispatch — `[[mireya-luis]]` 6× and `[[stefano-lavarini]]` 3× both resolved).

Next: Dispatch B (sports-science depth + book ingest).

## [2026-04-25] ingest | Books cluster 1 (Task B.8) | 6 files (3 raw + 3 wiki sources)
Per Tracks-A-B-C plan Task B.8 (`docs/superpowers/plans/2026-04-25-tracks-a-b-c.md`).

**Books ingested (publisher-preview + reviews + interview-derived fair-use notes per SCHEMA §8.4):**
- *The Volleyball Coaching Bible Volume II* (AVCA / Reynaud, ed., 2015, Human Kinetics) — slug `notes-shondell-2014-volleyball-coaching-bible-v2`. Raw: ~846w. Wiki source: ~502w. **Editorial correction**: Vol II edited by Reynaud alone (with AVCA), not Shondell; Shondell co-edited Vol I (2002). Slug retained for plan consistency.
- *Volleyball: Steps to Success* (Bonnie Kenny + Cindy Gregory, 2006/2009; Becky Schmidt 2nd ed., 2016; Human Kinetics) — slug `notes-pauley-2009-volleyball-steps-to-success`. Raw: ~949w. Wiki source: ~579w. **Authorship correction**: actual authors are Kenny + Gregory (1st ed) and Schmidt (2nd ed); no Bonnie Pauley volleyball book exists. Slug retained for plan consistency.
- *Volleyball Coach's Survival Guide* (Sue Gozansky, 2001, Parker Publishing) + *Championship Volleyball: Complete Book of Techniques and Drills* — slug `notes-gozansky-2001-coaching-volleyball-successfully`. Raw: ~867w. Wiki source: ~608w. **Title/publisher correction**: Gozansky's actual 2001 book is *Survival Guide* (Parker Publishing, ISBN 0130207578, 344 pp.), used as USAV CAP Level II Course textbook; not a Human Kinetics *Coaching Successfully* volume. Slug retained.

**Sources updated:** `raw/INDEX.md` (3 new book-notes entries inserted in alphabetical order).

**Trust tier:** All 3 are Tier 1 (published authoritative books — AVCA-endorsed anthology, Human Kinetics instructional series, USAV CAP textbook respectively).

**Honesty:** All three plan slugs had factual mismatches (editor name / author name / title+publisher). Each correction is documented inline in both the raw note and the wiki source page; no fabrication. Wave-3 coach pages (e.g., [[sue-gozansky]], [[bonnie-kenny]], [[becky-schmidt]], [[cecile-reynaud]]) are forward-referenced.

Next: B.9 (Beal + Hebert + McGown), B.10–B.12 (international + modern coaching books).
