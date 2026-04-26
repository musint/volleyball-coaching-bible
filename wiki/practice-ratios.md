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

# Practice Ratios by Age & Season Phase

## Overview

Practice ratios — how much of a session is blocked / skill-isolation work versus small-group game-like competitive work versus 6v6 live full-format play — sit at the operational core of practice planning. Every coach is making this allocation decision, explicitly or by drill-design habit. The methodology layer is in `[[block-vs-random-practice]]`: the contextual-interference effect, the ecological-dynamics critique, and per-school positions. The per-age developmental layer is in the `[[10s]]` through `[[18s]]` age-guides plus the `[[age-lens-14u]]` / `[[age-lens-hs]]` / `[[age-lens-college]]` band overlays. The season-arc layer is in `[[season-planning]]` and the macrocycle pages. This page is the synthesis: a 10-row × 5-column matrix that says *for athletes of age X in season-phase Y, practice runs roughly Z% blocked / W% small-group / V% 6v6*, with per-age narrative paragraphs and transition criteria that name the signs to advance to the next phase's ratios.

The matrix cells are **coach-judgment synthesis grounded in the existing wiki's evidence base** — USAV age-appropriate guidelines, the contextual-interference literature [shea-1979-contextual-interference], GMS's "as quickly as the learner allows" framing [gms-nd-structure-practice], the existing 14U lens's static recommendation. They are *defensible defaults*, not RCT-derived constants. Treat the cells as starting points; ±10pp adjustments are normal for team-stage variation, season-topology, and roster maturity.

The page uses a **three-bucket structure** (blocked / small-group game-like / 6v6 live) and a **five-phase progression** (preseason / mid-season / late-season / pre-tournament-peak / taper-match-day). The non-monotonic taper — blocked bumps back up, live drops — is intentional and reflects what NCAA-program tapers actually do.

## Bucket definitions

These need to be operationally crisp — coaches will use them to count minutes during practice planning.

**Bucket 1 — Blocked / skill-isolation work.** Same-skill repetition with a controlled, predictable feed (coach-toss, partner-toss, tee, line). Limited or no opposing intent. The athlete knows what's coming. Drill examples from the existing wiki catalog: `[[butterfly-passing]]` when coach-fed, `[[serve-targets]]`, `[[target-setting]]`, `[[block-footwork-ladder]]`, `[[two-line-passing]]`, `[[approach-and-swing]]` against coach-tossed sets, `[[front-back-sets]]`, individual position work. Maps to the SCHEMA `phase: skill` enum. Purpose: pattern installation, technique repair, low-cognitive-load cue reinforcement. Methodology profile: high in-session fluency, low retention/transfer if held too long [shea-1979-contextual-interference].

**Bucket 2 — Small-group game-like / competitive.** Sub-6v6 formats with opposing intent and scoring: 1v1, 2v2, 3v3, 4v4 over-the-net; queen-of-the-court variants; wash-drill formats with scoring; mini-game scrimmage. Random in schedule (between-skill interleaving from a live cue source) but at lower rotation-tracking load than 6v6. Drill examples: `[[serve-receive-3v3]]`, `[[queen-of-the-court]]`, `[[queen-of-the-court-passing]]`, `[[wash-drill]]` at small scale, `[[munciana-biggie-smalls]]`, `[[munciana-prove-it]]`, `[[cooperative-25-goal]]`. Maps to SCHEMA `phase: strategic` or `phase: competition` at smaller scale. Purpose: this is where the contextual-interference benefit lives at the highest density per minute — methodologically the richest bucket [magill-1990-contextual-interference-review].

**Bucket 3 — Live / full-format match play.** Twelve-player game-like situations: 6v6 wash-style scoring drills, side-out drills, free-ball-to-offense at 6v6, half-game and full-game scrimmage, simulated matches with referee, transition-rally drills at 6v6 scale. **Important:** for 12s and older, bucket 3 is 6v6 (the actual match format). For 10s and 11s where USAV's modified format is 4v4, bucket 3 is 4v4 simulation — the bucket means "the actual live match format being played," not literally six-against-six [usav-2026-simplified-youth-rules]. Drill examples: `[[gold-medal-scrimmage]]`, `[[six-player-defense]]`, `[[transition-rally]]`, `[[wash-drill]]` at 6v6 scale. Maps to SCHEMA `phase: competition` at full scale. Purpose: full information-coupling, system execution under rotation-tracking load, decision-making at match-realistic complexity.

**Outside the three buckets:** warm-up, cool-down, and non-decision conditioning sit *outside* the percentages. Treated as off-clock when computing matrix cells. A 120-min session with 15-min warm-up + 5-min cool-down has 100 min of in-bucket time; the percentages apply to the 100 min only. This mirrors how coaches actually plan and avoids the percentages drifting from session to session because of warm-up length variation.

**Edge-call rules** (named explicitly to avoid bucket-classification mistakes):

- *Pepper.* Live-feed but two-player and uncompetitive without scoring → bucket 1 (warm-up sub-category) by default; bucket 2 if scored as `[[partner-pepper-warmup]]` competition.
- *Wash drills.* Bucket 2 if 2v2/3v3, bucket 3 if 6v6 — same drill family lands in different buckets based on player count.
- *Position-specific individual work* (setter footwork, libero reads, hitter arm mechanics). Always bucket 1.
- *Coach-fed but live-decision drills* (e.g., coach-tossed defensive ball where the digger has to read direction). Bucket 1 if the read is trivial; bucket 2 if the read is a real perceptual problem and the drill is scored. The default classification errs toward bucket 1 since information-coupling is degraded vs. live.

## Master matrix

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

**Pattern claims to notice:**

1. **Blocked drops as athletes age.** Preseason blocked falls from ~40-45% at 10s-12s to ~25% at college. Drops because patterns stabilize and blocked work shifts from "install the platform" to "fix the specific drift in athletes A, B, C."

2. **12s is the pattern-install-heaviest year.** The 6v6 introduction at 12s adds team-system install (rotations, overlap rules, position assignments, three-attacker coverage) on top of skill installation. Preseason blocked peaks at 45% — the highest in the matrix — to support the double load.

3. **Small-group plateaus high at younger ages, ramps down at older.** 10s/11s sit at 50-55% small-group across the season because USAV's "grills" philosophy puts most of practice in scored small-side games and their actual match format is methodologically a small-group format anyway [usav-2026-youth-volleyball-tips]. By college, small-group drops to 15-25% because most live work has graduated to 6v6.

4. **Live-full-format ramps both across ages and across the season.** College pre-tournament-peak hits 75% live — the highest concentration in the matrix — and reflects what NCAA programs actually do in conference week.

5. **Taper is non-monotonic.** Blocked bumps back up by ~10pp from pre-tournament-peak to taper, live drops by ~10-15pp. The mechanism: in the last 24-72 hours, blocked polish-rep work (`[[serve-targets]]`, `[[pass-set-hit]]` at chosen tempos) gets contact freshness without the fatigue cost of full live competition.

The 11s-14s blocked percentages are intentionally 5pp higher than a "pure-random methodology" reading would prescribe. Three reasons: (a) the contextual-interference literature's most-misquoted caveat is that CI benefits *require a stable movement solution to interleave* — learners in the cognitive stage need blocked work first [magill-1990-contextual-interference-review]; (b) GMS's "as quickly as the learner allows" framing — for an 11s learning the platform, that's meaningfully slower than for a 17s [gms-nd-structure-practice]; (c) practice-budget arithmetic — a 90-min 12s session can't realistically install platform + hand-hinge + approach + float-serve mechanics across a roster AND have 30 min of 6v6.

## Per-age trajectories

Ten paragraphs translate the matrix rows into coaching guidance. Each paragraph names the row's defining shape, walks the trajectory across the five phases, calls out the age-specific quirk that drives the shape, and anchors drill-format choices to the existing wiki catalog.

### 10s

10s is where the matrix shape diverges most from the older ages. Preseason **40/55/5** has bucket 3 (4v4 modified format, not 6v6) at near-zero because USAV's developmental philosophy keeps formal competition minimal at this age — the 5pp is for end-of-practice 4v4 grills, not real bracket play [usav-2026-simplified-youth-rules]. The dominant pattern across the row is **bucket 2 holding stable at 50-55%** through every phase: `[[partner-pepper-warmup]]`, scored `[[serve-targets]]`, mini-grills, Newkirk's 15-drill youth sampler [aoc-2021-youth-15-drills] are the meat of the year. Bucket 1 stays at 25-40% for movement-discovery and brief platform-introduction moments — short segments, frequent rotation, kids prefer games over drills [usav-2026-youth-volleyball-tips]. Pre-tournament-peak (if it applies — many 10s programs have no peak event) lifts 4v4 simulation to 25%. Taper at this age is more a volume cut than a ratio shift; the 35/50/15 column is for programs with a real culminating tournament. Coaches running rec or developmental 10s should treat the row as ceiling, not floor.

### 11s

11s sits at the same 4v4 modified format as 10s but with skill development pulling ahead. Preseason **40/55/5** mirrors the 10s shape — heavy install but with the platform and contact mechanics now stable enough to graduate beyond catch-and-set. Mid-season balances at **30/55/15** as 4v4 grills become the practice meat: `[[serve-receive-3v3]]`, `[[queen-of-the-court-passing]]`, `[[wash-drill]]` at 3v3 take more time. Late-season **30/50/20** holds the small-group bucket high while 4v4 simulation creeps up. Pre-tournament-peak **25/45/30** is the live-format ceiling for 11s — most peak events at this age still cap at 4v4 brackets [usav-2026-simplified-youth-rules]. Taper **35/50/15** pulls blocked back up for serve-target work and contact freshness. Pattern install dominates at this age because skills like the float-serve toss are still being acquired; long-blocked sessions are counter-productive but short focused blocked moments throughout practice are essential [aoc-2024-kids-serving-fundamentals].

### 12s

12s is the pattern-install-heaviest year of the program — the format jumps to 6v6 and a wave of new system-level concepts (rotations, overlap rules, position assignments, three-attacker coverage) lands on top of skill installation. Preseason **45/40/15** runs the highest blocked percentage in the matrix to support that double load: `[[butterfly-passing]]`, `[[front-back-sets]]`, `[[approach-and-swing]]` blocked work installing the team-wide vocabulary [aoc-2024-kids-attacking-fundamentals]. Mid-season **35/40/25** transitions install-to-execute as 6v6 wash patterns earn more time. Late-season **30/40/30** balances the buckets evenly for the first time as 6v6 becomes routine. Pre-tournament-peak **25/35/40** is the live-dominant moment of the 12s year. Taper **35/35/30** bumps blocked back to the same level as mid-season — at 12s, polish-rep blocked work is more useful at taper than for older ages because patterns are still consolidating, so contact freshness via blocked reps reinforces the pattern instead of just maintaining it.

### 13s

13s is the 6v6 systems-stabilization year — patterns installed at 12s become durable enough to interleave at the room temperature of competition. Preseason **40/40/20** runs lower blocked than 12s because the team isn't installing 6v6 from scratch (returning 13s athletes carry the system over from 12s). Mid-season **30/40/30** is the most balanced row in the matrix — equal thirds across the three buckets, reflecting that 13s is methodologically the year where the contextual-interference benefit becomes most accessible at the team level [shea-1979-contextual-interference]. Late-season **30/35/35** drifts toward 6v6 dominance. Pre-tournament-peak **25/30/45** matches 14s's preseason ratio — the asymmetric 13s peak is roughly equivalent to 14s baseline. Taper **35/30/35** preserves polish-rep blocked work as a contact-freshness lever. Drill-format anchors cluster around `[[wash-drill]]`, `[[transition-rally]]`, `[[gold-medal-scrimmage]]` for 6v6 and `[[queen-of-the-court]]` plus competing-in-practice formats for small-group [aoc-2023-kiraly-competing-in-practice].

### 14s

The 14s row sits at the developmental hinge: forearm-pass platform and setting hand-hinge are stable enough to interleave, but 5-1 position commitment and complex 6-2 are still ahead. Preseason runs **40/35/25** — heavy install with the platform-and-hands work that, if missed at 13-14, is hard to recover at 17 [aoc-2024-setting-hand-hinge]. Mid-season balances at **30/35/35** as the team's repertoire stabilizes; small-group work skews competitive — `[[queen-of-the-court]]`, `[[wash-drill]]` 3v3 variants, `[[cooperative-25-goal]]`. Late season climbs to **25/35/40** with `[[gold-medal-scrimmage]]` and `[[transition-rally]]` formats taking more 6v6 time as rotations track without prompting. Pre-tournament-peak hits **20/30/50** — the highest 6v6 density of the 14s year, with simulated bracket play and `[[pressure-serving]]`. Taper trims volume but bumps blocked back to **30/30/40** — `[[serve-targets]]`, controlled `[[pass-set-hit]]`, contact freshness without competition fatigue. The growth-spurt reality means the platform is on a moving target through this year; revisit blocked install reps mid-season for athletes who grew 2+ inches over the holidays.

### 15s

15s is when specialization onset rewrites blocked time. Patterns are stable enough that team-wide install demand falls sharply; what blocked work remains is position-specific (setter footwork, libero ball-control, MB approach timing, OH arm-swing repair), not roster-wide platform install. Preseason **30/35/35** drops blocked 10pp from 14s as a result — the biggest age-to-age step in the matrix. Mid-season **25/30/45** brings 6v6 to majority share. Late-season **20/30/50** continues the live-dominant trajectory. Pre-tournament-peak **15/25/60** is the install-window's lower bound — the 15s row's blocked floor isn't lower than this without compromising per-position repair work. Taper **25/25/50** pulls back toward balanced ratios with volume cut doing most of the freshness work. The 15s year is when swing-blocking gets installed in earnest as the default scheme [aoc-2026-swing-blocking-footwork-beginners] and when 5-1 offense replaces 6-2 for teams with a clearly-dominant setter [aoc-2022-4-2-system].

### 16s

16s is the position-commitment year — most athletes have a primary role that frames the year's blocked-time content (specific position-skill repair). Preseason **30/30/40** holds blocked at 30% but 6v6 jumps to 40% as the live-dominant pole takes hold. Mid-season **20/30/50** has 6v6 at half of practice. Late-season **15/30/55** drifts further toward live dominance with `[[wash-drill]]` at 6v6 and `[[gold-medal-scrimmage]]` carrying most time. Pre-tournament-peak **10/25/65** is the 16s ceiling at 65% live; small-group bucket holds at 25% as the high-density CI window [shea-1979-contextual-interference]. Taper **20/25/55** pulls blocked back to 20% for serve-target and pass-set-hit polish-rep work. The 16s year is when jump-topspin serving becomes appropriate for athletes with the physical tools [aoc-2020-types-of-serves] and when bunch-read blocking variants enter the repertoire — both add to per-position blocked-content load even as roster-wide blocked time shrinks.

### 17s

17s sits inside the recruiting cycle and pre-college readiness window — practice content tilts heavily toward the system-execution and analytics-light awareness college coaches will look for in film. Preseason **25/30/45** matches 16s mid-season — by 17s, the install pace has dropped enough that preseason and mid-season at 16s look similar. Mid-season **20/25/55** runs majority-6v6 with opponent-specific tactical work taking more time. Late-season **15/25/60** continues the live-dominant trajectory; small-group bucket trims toward 25% as 6v6 absorbs more time. Pre-tournament-peak **10/20/70** is one of the highest live percentages outside of college. Taper **20/20/60** holds. The 17s year's small-group bucket is methodologically the most valuable per-minute block of practice — at this age, 25% of practice in `[[wash-drill]]` 3v3 or competing-in-practice formats is where the high-density CI gains land [shea-1979-contextual-interference] [gms-nd-structure-practice].

### 18s

18s is the college-bridge year — full elite-level system execution with athletes capable of absorbing live volume that would overwhelm 14s/15s rosters. Preseason **25/25/50** matches 17s but with a tighter small-group bucket reflecting the smaller marginal return on 4v4/3v3 for athletes who've been doing it for years. Mid-season **20/25/55** mirrors 17s exactly. Late-season **15/25/60** continues. Pre-tournament-peak **10/20/70** holds at 70% live — the same as 17s, since both ages are at or near the live-dominant ceiling that practice-budget arithmetic allows below college. Taper **20/20/60** holds. The 18s tournament structure (JVA, USAV, AAU nationals) is when the cyclical-club structure shows up most clearly: practice ratios cycle through the late-season → pre-tournament → taper sequence repeatedly across April-June bid events. Coaches running the 18s plan must explicitly account for the cycle-stacking; treating each event as a discrete linear arc misses the load accumulation [pires-2021-burnout-coping-volleyball-season].

### College

College sits at the matrix's live-dominant pole because by the time athletes are on a roster, patterns are largely stable and the marginal return on blocked-time has dropped. Preseason **25/25/50** reflects NCAA fall camp: system install with experienced returners, blocked work concentrated on individual position-specific repair (setter footwork, libero second-ball reads, hitter arm mechanics) rather than team-wide platform install. Mid-season **20/25/55** is the conference-block default, with `[[wash-drill]]` and `[[gold-medal-scrimmage]]` carrying most of practice. Late-season **15/20/65** drops blocked further as opponent-specific tactical work takes over and small-group time gets squeezed by tournament density. Pre-tournament-peak **10/15/75** is the conference-tournament or NCAA-bracket week — the live-dominant ceiling of the program. Taper **15/15/70** holds the live percentage tighter than younger ages because elite athletes can absorb live volume better, so the volume cut does the work and the ratio barely moves. NCAA hours rules cap the total minutes; rotation is what moves, not bucket allocation. Concurrent S&C considerations apply [wang-2024-concurrent-training-strength-endurance].

## Phase-transition criteria

The matrix gives static cells per phase; this section answers *when* a coach should advance from preseason ratios into mid-season ratios and so on. The criteria are *signs the team is ready to graduate*, not a fixed timeline.

**Preseason → mid-season.** Patterns are stable enough to interleave. Markers: athletes consistently demonstrate proper platform / hand-hinge / approach mechanics in blocked work without prompting; team executes its base offense (4-2, 6-2, or 5-1) without rotation reminders; first competition has happened (intra-squad scrimmage or external scrimmage); pass quality reaches 2+ on roughly 60% of serves received. Time-based fallback when the markers don't yield a clear signal: 3-4 weeks for HS preseason, 2-4 weeks for club preseason, ~2 weeks for NCAA fall camp (camp-driven).

**Mid-season → late-season.** Team-wide install demand has gone away; only specific repair remains. Markers: the coach's blocked-time content shifts from "install the platform" to "fix the platform-drift in athletes A, B, C"; tournament density has accumulated (3-4 events for club; week 4+ for HS); cumulative-fatigue markers appear in the team's monitoring stack — Hooper Index drift up, weekly countermovement-jump drift down [rebelo-2024-training-stress-fatigue-wellbeing] [sanders-2025-early-season-jump-load-d1-volleyball]. Coach attention shifts from "build the team" to "fix the things that lost us match X."

**Late-season → pre-tournament-peak.** Event-driven, not time-driven. Markers: 7-14 days before the targeted event (regional, state, nationals, conference tournament); roster is locked; opponent intel has arrived (scout video, prior-meeting data); practice content switches to opponent-specific simulation [mccutcheon-2022-championship-behaviors].

**Pre-tournament-peak → taper-match-day.** 24-72 hours before competition. Markers: last meaningful tactical install is complete; volume reduction takes priority over content shift; ratio bumps blocked back up for polish-rep contact freshness without fatigue cost.

**Cyclical structure for club volleyball.** For 14U/club, the matrix is not run linearly once per year — the cycle is preseason → mid-season → late-season → repeated mini-peak → mini-taper every 2-3 weeks for tournament weekends → final-tournament peak. The "late-season" phase governs the baseline practice ratio between tournaments; pre-tournament-peak governs Tuesday-Thursday before each event; taper governs the Friday before. HS volleyball runs as one big linear arc with one peak (state tournament). College has two peaks within a season: conference tournament + NCAA bracket. The cyclical structure is the dominant feature of club planning [aoc-2023-rose-club-rules].

## Schools of thought

Six positions on practice ratios across the methodology landscape:

- **`[[gold-medal-squared]]`** — random-leaning, motor-learning-orthodox. McGown's "first we have to teach them how to move, then we need to teach them how to see" framing allows an early blocked phase but treats extended blocked practice as a design failure once patterns stabilize. The GMS read of the matrix would compress bucket 1 faster than the matrix shows — but accepts that cognitive-stage learners need real blocked work [gms-nd-structure-practice].

- **`[[art-of-coaching-volleyball]]`** — pedagogically eclectic. Internally pluralistic on this question. Mattox's early-season-practice piece argues for heavy fundamentals work in preseason — more bucket 1 than the matrix's mid-season cells [aoc-2021-mattox-early-season-practice]. Rose's "everything matters" frame pushes competitive intent in every bucket; the operational consequence is that even bucket 1 work scores reps, makes them count, and treats them as competition [aoc-2023-rose-club-rules]. AOC's honest summary: the bucket dichotomy matters less than cue quality, progression, and competitive intent.

- **`[[usa-volleyball]]`** — "grills not drills" tilts heavily toward bucket 2 at younger ages, with bucket 1 reserved for movement-discovery moments. The 2009 CAP "Game-Like Training" article is the cleanest short statement of the practical-random position [usav-2009-cap-game-like-training]. Modern Coach Academy materials extend this with the Bronze/Silver/Gold tiered curriculum, structured around the Craft/Body/Mind/Heart/Team pillars [usav-2026-coach-academy].

- **`[[ecological-dynamics]]`** — the bucket dichotomy is under-specified. What governs transfer is whether practice preserves the **information-movement coupling** of competition. A random-order bucket-2 drill that uses coach-tossed feeds has lost the perceptual sources athletes read in the live game; a blocked bucket-1 drill against a live server preserves them. The criterion is *action fidelity*, stricter than the bucket allocation itself [pinder-2011-representative-learning-design] [woods-2020-sport-ecology-designers].

- **`[[japanese-training]]`** — historically high-blocked. Daimatsu-era *kaiten reshibu* and the precision tradition were repetition-to-standard with the coach defining "the response is now reflex" as the end condition. Contemporary Japanese federation practice has modernized substantially toward bucket 2/3, especially in the SV.League era, but the historical center of gravity sits notably higher in bucket 1 than the GMS or USAV positions.

- **`[[game-based-training]]`** — TGfU inversion. Bunker & Thorpe's 1982 framework starts in tactical context (bucket 2/3) and introduces blocked technique work only as the tactical situation reveals a need for it. The bucket allocation isn't fixed — it's emergent from the modified-game design.

## Getting started

If you're new to this question, read in this order:

1. `[[block-vs-random-practice]]` — the methodology basis. Understand the contextual-interference effect and the ecological-dynamics critique before applying the matrix.
2. The master matrix above — read your age's row across all five season phases.
3. Your age-guide (`[[10s]]` through `[[18s]]`) for the developmental frame.
4. Your age-lens (`[[age-lens-14u]]`, `[[age-lens-hs]]`, `[[age-lens-college]]`) for the band-level overlay.
5. `[[practice-planning]]` and `[[season-planning]]` for the broader practice and season frames.
6. The macrocycle pages — `[[hs-fall-12-week-macrocycle]]`, `[[college-fall-14-week-macrocycle]]`, `[[club-preseason-6-week-macrocycle]]`, `[[club-nationals-prep-4-week-macrocycle]]`, `[[summer-dev-8-week-macrocycle]]` — for week-by-week templates that operationalize these ratios.
7. The microcycle pages — `[[hs-pre-match-week]]`, `[[club-pre-tournament-week]]`, `[[recovery-week]]`, `[[mid-season-tue-thu-cycle]]`, `[[postseason-testing-week]]` — for the week-shape inside each phase.

## Related areas

- `[[practice-planning]]` — the parent hub; practice ratios are a subtopic of practice planning.
- `[[season-planning]]` — the season-arc frame the matrix sits inside.
- `[[block-vs-random-practice]]` — the methodology basis underneath the matrix.
- Age-guides: `[[10s]]`, `[[11s]]`, `[[12s]]`, `[[13s]]`, `[[14s]]`, `[[15s]]`, `[[16s]]`, `[[17s]]`, `[[18s]]`.
- Age-lenses: `[[age-lens-14u]]`, `[[age-lens-hs]]`, `[[age-lens-college]]`.

## Sources

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
- `[[aoc-2023-kiraly-competing-in-practice]]`
- `[[aoc-2024-setting-hand-hinge]]`
- `[[aoc-2021-youth-15-drills]]`
- `[[aoc-2024-kids-attacking-fundamentals]]`
- `[[aoc-2024-kids-serving-fundamentals]]`
- `[[aoc-2026-swing-blocking-footwork-beginners]]`
- `[[aoc-2022-4-2-system]]`
- `[[aoc-2020-types-of-serves]]`

Volleyball-specific evidence (recent):
- `[[qu-2025-contextual-interference-volleyball-serve]]`
- `[[apidogo-2021-differential-learning-volleyball]]`
- `[[caldeira-2023-functional-movement-variability]]`
- `[[moy-2024-constraints-led-volleyball-serve]]`

Season-load / fatigue:
- `[[pires-2021-burnout-coping-volleyball-season]]`
- `[[sanders-2025-early-season-jump-load-d1-volleyball]]`
- `[[rebelo-2024-training-stress-fatigue-wellbeing]]`
- `[[wang-2024-concurrent-training-strength-endurance]]`
