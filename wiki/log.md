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
