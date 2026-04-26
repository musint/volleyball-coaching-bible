---
type: ops-doc
kind: match-prep
audience: coach
sources: [aoc-2020-stone-liskevych-using-video, aoc-2017-rose-pennstate-prep, aoc-2024-kiraly-stats-matter-most]
---

# Match-Prep Video Review Workflow

## Purpose

Convert post-match (or post-practice) film into a small set of teaching clips and adjustment cues, then deliver them to the team in a meeting structure that fits a club / HS / college calendar. The aim is not to watch more film — it is to watch *less* film, more deliberately. [[jim-stone]] and Terry Liskevych split video use into three buckets: scouting, match analysis, and teaching ([[aoc-2020-stone-liskevych-using-video]]). This workflow operationalizes the second and third for a head coach who already runs [[match-prep]] and wants the film loop to compound week over week.

## Inputs

- **Match film** uploaded same-day to Hudl, Synergy Sports, VolleyMetrics, BallerTV, or equivalent. Cloud-only is fine; on-device backups recommended for travel tournaments.
- **In-match stat sheet** from [[match-prep-stat-collection-sheet]] (rotation-by-rotation passing, hitting, serving, FBSO).
- **Pre-match plan** from [[match-prep-scouting-form]] and [[match-prep-opponent-tendency-form]] — needed to grade what worked and what got rewritten in-match.
- **Coach notes** scribbled between sets / on the bench.
- **Roster + jersey numbers** for tagging (one-time setup per season).

## Form

### Tagging conventions (skill + outcome + player)

Use a three-axis tag for every clip you keep. Hudl and VolleyMetrics both support compound tags; the convention works in any platform.

| Axis | Values | Notes |
|---|---|---|
| Skill | `serve` / `pass` / `set` / `hit` / `block` / `dig` / `transition` / `oos` | Match the [[match-prep]] skill enum |
| Outcome | `+` (point won) / `-` (point lost) / `0` (neutral) / `err` (unforced error) | `+` and `err` are the highest-leverage clips |
| Player | jersey# (e.g. `7`, `12`) or position code (`s`, `oh1`, `oh2`, `mb1`, `mb2`, `opp`, `l`) | Both is fine: `7-oh1` |

Compound tag examples: `pass-+-12`, `hit-err-7`, `block-+-mb1`, `oos-+-team`. Add a fourth axis (`rotation-1` … `rotation-6`) when you scout opponents — it lets you slice opponent serve-receive by rotation later.

### Per-match review steps

1. **Same-night triage (15 min, coach alone).** Skim film at 1.5x. Tag only the clips you might show: every `err`, every `+` from a player you're trying to develop, every rally where the *plan* (defense, blocking call, serve target) succeeded or failed. Target 12–20 clips, not 60.
2. **Stat-vs-film reconciliation (10 min).** Open the [[match-prep-stat-collection-sheet]]. Find the worst-FBSO rotation and the worst-passing rotation; pull the film for each. The numbers tell you *where* to look; the film tells you *why*.
3. **Clip-list build (15 min).** Bucket the tagged clips into three folders: **Wins** (≤4 clips, what worked), **Errors** (≤6, unforced errors with a fixable cause), **Adjustments** (≤4, decisions worth re-litigating — defensive base, set selection, serve target).
4. **Position-group splits (5 min).** Re-tag each clip with the position group(s) it belongs in: `pin` (OH+opp), `middle` (mb), `back-row` (l + ds), `setter`. A single clip can land in two groups.

### Review-meeting structure

Default meeting length: **35 minutes**. Run on the next practice day, before warm-up, in a film room or any space with a TV / projector. If you have to choose between video and court time, court wins — keep the meeting tight.

| Block | Duration | Format | Content |
|---|---|---|---|
| Team-level intro | 5 min | All players + staff | Set the frame. One sentence on what worked, one on what didn't, one on what tonight's practice fixes. Show 2–3 *Wins* clips only. |
| Position-group split | 10 min | Three rooms / corners | Pins with OH coach; middles with MB / blocking coach; back-row with DC / libero. Each group reviews 3–5 clips from its position-tagged list. Setters either join pins or get a fourth split if you have the bodies. |
| Team-level adjustment | 5 min | All back together | Show the *Adjustments* clips. State the change for the next match (defensive base, serve target, set distribution). Not a debate — a decision. |
| Q&A / captains' floor | 5 min | All players + staff | Captains lead. Coach answers, doesn't lecture. |
| Walk to court | 10 min | — | The film loops into the practice plan immediately — first drill block targets the worst rotation. ([[aoc-2017-rose-pennstate-prep]] frame: analysis exists to feed the next session.) |

### Cadence

- **In-season:** one review meeting per match, within 48 hours, on the next practice day. Skip if a tournament weekend gives you three matches in two days — batch into one Monday meeting instead.
- **Tournament weekends:** between-pool film is *coaches only* — no player meetings between matches. Save the player-facing review for the Monday after.
- **Self-scout review:** every 4–6 weeks, swap the opponent focus for a self-scout meeting using the same structure. Watch yourselves the way an opponent would.

## Sources

- [[aoc-2020-stone-liskevych-using-video]]
- [[aoc-2017-rose-pennstate-prep]]
- [[aoc-2024-kiraly-stats-matter-most]]
