# Operations Log

Append-only log of wiki operations. Prefix format: `## [YYYY-MM-DD] <operation> | <short>`.

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
    wiki/sources/. Dangling [[wikilinks]] left for W2.2+ targets
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
- 15 dangling [[wikilinks]] in coach profiles to future coach pages
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