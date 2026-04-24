# Wiki Improvement — Tracks 1 + 2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the wiki from a dense reference library into a working coaching tool while simultaneously closing integrity gaps — via 7 skill hubs, ~25 Dataview retrofits, 15 practice-plan templates, 15 secondary-coach profiles, ~40 unsourced-queue backfills, lint automation, and residual cleanup.

**Architecture:** Three parallel-agent dispatches sandwiched around lint checkpoints. Dispatch 1 lands the content scaffolding (hubs + coaches + retrofits + lint tooling); Dispatch 2 lands the operational layer and integrity work (practice plans + research backfills); Dispatch 3 resolves residuals. Each new page type follows the existing SCHEMA.md contracts; practice-plan becomes page type #10 with a new SCHEMA entry. Execution pattern matches the Wave 2–5 bootstrap: multiple parallel subagents per dispatch, with a lint checkpoint between dispatches verifying invariants and broken-link counts.

**Tech Stack:** Markdown + YAML frontmatter (Obsidian-compatible), Python 3 + pyyaml (for the lint script), bash pre-commit hook, git. No new dependencies beyond pyyaml for lint tooling.

**Spec source:** `docs/superpowers/specs/2026-04-24-wiki-improvement-tracks-1-2-design.md`

---

## File structure

### New files (content)
- `wiki/passing.md`, `wiki/setting.md`, `wiki/hitting.md`, `wiki/blocking.md`, `wiki/serving.md`, `wiki/defense.md`, `wiki/transition.md` — 7 skill hubs
- `wiki/coaches/<slug>.md` × 15 — secondary coach profiles
- `wiki/practice-plans/<slug>.md` × 15 — new page type
- `wiki/schools/<slug>.md` × 2–4 — institutional stubs surfaced by coach profiles (e.g., `munciana-volleyball-club.md`, `iowa-state-volleyball.md`, `ohio-state-volleyball.md` as needed)
- `wiki/sources/<slug>.md` × variable — sources ingested during backfill research

### New files (tooling)
- `tools/lint.py` — Python lint script
- `tools/install-hooks.sh` — one-liner to install the pre-commit hook for new clones
- `.git/hooks/pre-commit` — shell hook that runs lint and blocks on broken-link regression
- `wiki/lint-report.md` — auto-generated report

### Modified files
- `wiki/SCHEMA.md` — add `practice-plan` as page type #10; add Dataview install note to §2.2; add enums
- `wiki/index.md` — add Skill hubs section, Practice plans section, expand Coaches section
- `wiki/log.md` — per-dispatch entries
- `wiki/unsourced-queue.md` — entries cleared by §4.2 backfills
- ~25 existing hub/age-lens/position pages — Dataview retrofits inserted
- Misc existing pages — replace `[unsourced]` tags with citations, stub creation for missing institutional slugs

### Shared brief templates (used repeatedly across tasks)
Defined once at the bottom of each dispatch section so individual tasks can reference them rather than inlining.

---

## Dispatch 1 — Content scaffolding + tooling

Launched as a single parallel dispatch of ~24 agents. Each task below produces an isolated artifact committed independently.

---

### Task 1.1: Author `tools/lint.py` and install pre-commit hook

**Files:**
- Create: `tools/lint.py`
- Create: `tools/install-hooks.sh`
- Create: `.git/hooks/pre-commit` (installed by the script)
- Create: `tools/test_lint.py`
- Create: `wiki/lint-report.md` (first run)

- [ ] **Step 1: Write the failing test file**

Create `tools/test_lint.py`:

```python
"""Tests for tools/lint.py. Run: python -m pytest tools/test_lint.py -v"""
import os
import tempfile
import shutil
import subprocess
from pathlib import Path

LINT = Path(__file__).parent / "lint.py"

def _run(wiki_root, extra_args=None):
    args = ["python", str(LINT), "--wiki", str(wiki_root)]
    if extra_args:
        args.extend(extra_args)
    result = subprocess.run(args, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def _scaffold(tmpdir, pages):
    """pages is {relative_path: content}"""
    for rel, content in pages.items():
        p = Path(tmpdir) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

def test_broken_wikilink_detected(tmp_path):
    _scaffold(tmp_path, {
        "wiki/hub.md": "---\ntype: hub\narea: x\nsubtopics: []\n---\n# Hub\nLink to [[missing-page]].\n",
    })
    code, out, _ = _run(tmp_path)
    assert code != 0
    assert "missing-page" in out
    assert "broken wikilink" in out.lower()

def test_no_broken_wikilinks_passes(tmp_path):
    _scaffold(tmp_path, {
        "wiki/a.md": "---\ntype: hub\narea: x\nsubtopics: []\n---\n# A\nLinks to [[b]].\n",
        "wiki/b.md": "---\ntype: hub\narea: y\nsubtopics: []\n---\n# B\n",
    })
    code, _, _ = _run(tmp_path)
    assert code == 0

def test_drill_must_have_source_and_technique(tmp_path):
    _scaffold(tmp_path, {
        "wiki/drills/bad.md": "---\ntype: drill\nname: Bad\nprimary-skill: passing\nphase: skill\nteam-size-min: 2\nteam-size-max: 4\nduration-min: 5\nlevels: [14u]\nequipment: []\ntechniques: []\nsources: []\n---\n# Bad\n",
    })
    code, out, _ = _run(tmp_path)
    assert code != 0
    assert "drill" in out.lower() and ("source" in out.lower() or "technique" in out.lower())

def test_coach_must_have_school_and_source(tmp_path):
    _scaffold(tmp_path, {
        "wiki/coaches/nobody.md": "---\ntype: coach\nname: Nobody\ncountry: USA\nera: modern\nroles: []\nschools: []\nsources: []\n---\n# Nobody\n",
    })
    code, out, _ = _run(tmp_path)
    assert code != 0
    assert "coach" in out.lower()

def test_report_file_written(tmp_path):
    _scaffold(tmp_path, {
        "wiki/a.md": "---\ntype: hub\narea: x\nsubtopics: []\n---\n# A\n",
    })
    _run(tmp_path, ["--report", str(tmp_path / "report.md")])
    assert (tmp_path / "report.md").exists()
```

- [ ] **Step 2: Run test to verify it fails**

```
python -m pytest tools/test_lint.py -v
```

Expected: all tests FAIL (lint.py does not exist yet).

- [ ] **Step 3: Implement `tools/lint.py`**

Create `tools/lint.py`:

```python
"""Volleyball Coaching Bible — wiki lint.

Runs SCHEMA §5.3 checks:
  1. Orphan scan
  2. Cross-link invariants (SCHEMA §6)
  3. Broken wikilinks
  4. Unsourced-queue consistency
  5. Frontmatter validation
  6. Stale-claim scan (methodology pages > 5y since newest source)
  7. Concept-gap detection

Usage:
  python tools/lint.py [--wiki PATH] [--report PATH]

Exits non-zero on:
  - Broken wikilink count > baseline in prior report (regression)
  - Cross-link invariant violations
  - Frontmatter validation failures
"""
import argparse
import datetime
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml required. Install: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

WIKILINK_RE = re.compile(r"\[\[([a-z0-9][a-z0-9\-]*)\]\]")
INLINE_CITE_RE = re.compile(r"(?<!\w)\[([a-z0-9][a-z0-9\-]*)\](?!\()")
UNSOURCED_RE = re.compile(r"\[unsourced\]|\[unverified\]|\[transcript-unavailable\]|\[translation-needed\]")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

REQUIRED_FIELDS = {
    "hub": ["type", "area"],
    "coach": ["type", "name", "country", "era", "roles", "schools", "sources"],
    "school": ["type", "name", "origin", "sources"],
    "technique": ["type", "skill", "subskill", "sources"],
    "position": ["type", "position", "role"],
    "system": ["type", "category", "name", "sources"],
    "drill": ["type", "name", "primary-skill", "techniques", "phase", "team-size-min",
              "team-size-max", "duration-min", "levels", "equipment", "sources"],
    "source": ["type", "source-type", "title", "author", "year", "citation-key", "trust-tier"],
    "age-lens": ["type", "label", "scope", "sources"],
    "practice-plan": ["type", "level", "duration-min", "focus", "season-phase", "drills", "sources"],
}

ENUM_VALUES = {
    "phase": {"warm-up", "skill", "strategic", "competition", "conditioning"},
    "source-type": {"book", "video-series", "podcast", "article", "interview", "clinic", "social-post"},
    "trust-tier": {1, 2, 3},
    "skill": {"passing", "setting", "hitting", "blocking", "serving", "defense", "transition"},
    "category": {"offense", "defense", "serve-receive", "blocking", "transition"},
    "complexity": {"low", "medium", "high"},
    "position": {"setter", "outside-hitter", "middle-blocker", "opposite", "libero", "defensive-specialist"},
    "level": {"14u", "hs", "college"},
    "focus": {"passing", "setting", "hitting", "blocking", "serving", "defense", "transition",
              "serve-receive", "out-of-system", "match-prep", "player-development", "composite"},
    "season-phase": {"preseason", "mid-season", "pre-tournament", "taper", "tryout",
                     "postseason", "match-day"},
}

METHODOLOGY_TYPES = {"school", "hub", "age-lens"}
STALE_YEARS = 5


def parse_page(path: Path):
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    meta = {}
    body = text
    if m:
        try:
            meta = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError:
            meta = {"__invalid_yaml__": True}
        body = text[m.end():]
    return meta, body, text


def collect_pages(wiki: Path):
    """Return dict slug -> {path, meta, body, text, inbound_count, outbound_links}"""
    pages = {}
    for md in wiki.rglob("*.md"):
        slug = md.stem
        if slug in pages:
            # filename collision — record both (lint rule: basenames must be globally unique per SCHEMA)
            pages[slug + "__dup__" + str(len(pages))] = {"path": md, "duplicate_of": slug}
            continue
        meta, body, text = parse_page(md)
        pages[slug] = {
            "path": md,
            "meta": meta if isinstance(meta, dict) else {},
            "body": body,
            "text": text,
        }
    # inbound counting
    for slug, p in pages.items():
        out = set(WIKILINK_RE.findall(p.get("body", "")))
        p["outbound"] = out
    inbound = defaultdict(int)
    for slug, p in pages.items():
        for target in p.get("outbound", ()):
            inbound[target] += 1
    for slug, p in pages.items():
        p["inbound"] = inbound.get(slug, 0)
    return pages


def check_broken_wikilinks(pages):
    findings = []
    slug_set = set(s for s in pages if "__dup__" not in s)
    for slug, p in pages.items():
        if "__dup__" in slug:
            continue
        for target in sorted(p["outbound"]):
            if target not in slug_set:
                findings.append((str(p["path"]), target))
    return findings


def check_cross_link_invariants(pages):
    violations = []
    for slug, p in pages.items():
        if "__dup__" in slug:
            continue
        m = p["meta"]
        t = m.get("type")
        if t == "drill":
            if not m.get("sources") or not m.get("techniques"):
                violations.append((str(p["path"]), "drill missing sources or techniques"))
        elif t == "coach":
            if not m.get("sources") or not m.get("schools"):
                violations.append((str(p["path"]), "coach missing sources or schools"))
        elif t == "technique":
            sp = m.get("schools-perspectives") or {}
            # only contested techniques need schools-perspectives; we don't know which so skip
            pass
    return violations


def check_frontmatter(pages):
    failures = []
    for slug, p in pages.items():
        if "__dup__" in slug:
            continue
        m = p["meta"]
        if m.get("__invalid_yaml__"):
            failures.append((str(p["path"]), "invalid YAML frontmatter"))
            continue
        t = m.get("type")
        if not t:
            # index, log, SCHEMA, lint-report, unsourced-queue: no type by design
            if slug not in {"index", "log", "SCHEMA", "lint-report", "unsourced-queue"}:
                failures.append((str(p["path"]), f"missing 'type' field"))
            continue
        required = REQUIRED_FIELDS.get(t)
        if required is None:
            failures.append((str(p["path"]), f"unknown type '{t}'"))
            continue
        for field in required:
            if field not in m:
                failures.append((str(p["path"]), f"missing required field '{field}' for type '{t}'"))
        # enum validation on common fields
        for field in ("phase", "source-type", "trust-tier", "skill", "complexity", "position",
                      "level", "focus", "season-phase"):
            if field in m and field in ENUM_VALUES:
                val = m[field]
                if val not in ENUM_VALUES[field]:
                    failures.append((str(p["path"]), f"invalid enum value '{val}' for '{field}'"))
        if t == "system" and "category" in m:
            if m["category"] not in ENUM_VALUES["category"]:
                failures.append((str(p["path"]), f"invalid system category '{m['category']}'"))
    return failures


def check_citation_keys(pages):
    """Every inline [citation-key] must resolve to a source page's citation-key field."""
    source_keys = set()
    for slug, p in pages.items():
        if "__dup__" in slug:
            continue
        if p["meta"].get("type") == "source":
            ck = p["meta"].get("citation-key")
            if ck:
                source_keys.add(ck)
    unresolved = []
    for slug, p in pages.items():
        if "__dup__" in slug:
            continue
        for ck in INLINE_CITE_RE.findall(p["body"]):
            if ck in {"unsourced", "unverified", "transcript-unavailable", "translation-needed"}:
                continue
            if ck not in source_keys:
                unresolved.append((str(p["path"]), ck))
    return unresolved


def check_orphans(pages):
    orphans = []
    for slug, p in pages.items():
        if "__dup__" in slug:
            continue
        if p["inbound"] == 0:
            t = p["meta"].get("type")
            if t in {"hub", None}:
                continue  # hubs are entry points; index/log/SCHEMA have no type
            if slug in {"index", "log", "SCHEMA", "lint-report", "unsourced-queue"}:
                continue
            orphans.append((str(p["path"]), t or "(untyped)"))
    return orphans


def check_stale_claims(pages):
    stale = []
    today_year = datetime.date.today().year
    for slug, p in pages.items():
        if "__dup__" in slug:
            continue
        t = p["meta"].get("type")
        if t not in METHODOLOGY_TYPES:
            continue
        src_slugs = p["meta"].get("sources") or []
        if not isinstance(src_slugs, list):
            continue
        newest = None
        for s in src_slugs:
            src_page = pages.get(s)
            if not src_page:
                continue
            y = src_page["meta"].get("year")
            if isinstance(y, int) and (newest is None or y > newest):
                newest = y
        if newest is not None and today_year - newest > STALE_YEARS:
            stale.append((str(p["path"]), f"newest source year {newest}"))
    return stale


def check_concept_gaps(pages):
    """Terms that appear as [[wikilinks]] on >=3 pages but have no matching page."""
    slug_set = set(s for s in pages if "__dup__" not in s)
    reference_counts = defaultdict(int)
    for slug, p in pages.items():
        if "__dup__" in slug:
            continue
        for target in p["outbound"]:
            if target not in slug_set:
                reference_counts[target] += 1
    return [(t, c) for t, c in reference_counts.items() if c >= 3]


def check_unsourced_consistency(pages, queue_path: Path):
    if not queue_path.exists():
        return []
    queue_text = queue_path.read_text(encoding="utf-8")
    issues = []
    for slug, p in pages.items():
        if "__dup__" in slug:
            continue
        if UNSOURCED_RE.search(p["body"]):
            page_rel = "wiki/" + p["path"].relative_to(p["path"].parent.parent).as_posix()
            # weak consistency: does the queue mention this page path?
            if str(p["path"].name) not in queue_text and page_rel not in queue_text:
                issues.append((str(p["path"]), "has [unsourced] tag but no matching queue entry"))
    return issues


def read_prior_broken_count(report_path: Path):
    if not report_path.exists():
        return None
    text = report_path.read_text(encoding="utf-8")
    m = re.search(r"Broken wikilinks:\s*(\d+)", text)
    return int(m.group(1)) if m else None


def render_report(findings, report_path: Path):
    lines = [f"# Wiki Lint Report", f"", f"Generated: {datetime.datetime.now().isoformat(timespec='seconds')}", ""]
    for section, items, header in findings:
        lines.append(f"## {section}")
        lines.append(f"{header}: {len(items)}")
        lines.append("")
        for item in items[:40]:
            lines.append(f"- {item}")
        if len(items) > 40:
            lines.append(f"- ...and {len(items) - 40} more")
        lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--wiki", default=".", help="Project root (containing wiki/)")
    ap.add_argument("--report", default=None, help="Report output path (default: wiki/lint-report.md)")
    ap.add_argument("--strict", action="store_true", help="Non-zero exit on any check failure")
    args = ap.parse_args(argv)

    root = Path(args.wiki)
    wiki = root / "wiki"
    report_path = Path(args.report) if args.report else wiki / "lint-report.md"
    queue_path = wiki / "unsourced-queue.md"

    if not wiki.exists():
        print(f"No wiki/ at {wiki}", file=sys.stderr)
        return 2

    pages = collect_pages(wiki)
    broken = check_broken_wikilinks(pages)
    invariants = check_cross_link_invariants(pages)
    frontmatter = check_frontmatter(pages)
    citations = check_citation_keys(pages)
    orphans = check_orphans(pages)
    stale = check_stale_claims(pages)
    gaps = check_concept_gaps(pages)
    queue_issues = check_unsourced_consistency(pages, queue_path)

    findings = [
        ("Broken wikilinks", [f"{p}: [[{t}]]" for p, t in broken], "Broken wikilinks"),
        ("Cross-link invariant violations", [f"{p}: {why}" for p, why in invariants], "Violations"),
        ("Frontmatter failures", [f"{p}: {why}" for p, why in frontmatter], "Failures"),
        ("Unresolved citation keys", [f"{p}: [{ck}]" for p, ck in citations], "Unresolved"),
        ("Orphan pages", [f"{p} (type={t})" for p, t in orphans], "Orphans"),
        ("Stale methodology pages", [f"{p} ({why})" for p, why in stale], "Stale"),
        ("Concept gaps", [f"[[{t}]] (referenced {c}x)" for t, c in gaps], "Gaps"),
        ("Unsourced-queue consistency", [f"{p}: {why}" for p, why in queue_issues], "Issues"),
    ]

    render_report(findings, report_path)

    prior = read_prior_broken_count(report_path.with_name(report_path.name + ".baseline")) or None
    current = len(broken)

    # Exit logic
    if invariants or frontmatter or citations:
        print(f"Broken wikilinks: {current}; invariants={len(invariants)}; frontmatter={len(frontmatter)}; citations={len(citations)}")
        return 1
    if prior is not None and current > prior:
        print(f"Broken wikilinks regressed: {current} > {prior}")
        return 1
    if args.strict and (orphans or queue_issues):
        return 1
    print(f"Lint OK. Broken wikilinks: {current}; orphans: {len(orphans)}; gaps: {len(gaps)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run test to verify it passes**

```
python -m pytest tools/test_lint.py -v
```

Expected: all 5 tests PASS.

- [ ] **Step 5: Run the lint on the real wiki and capture the report baseline**

```
python tools/lint.py
```

Expected: report lands at `wiki/lint-report.md`. Record the current broken-wikilink count (expect ~116).

```
cp wiki/lint-report.md wiki/lint-report.md.baseline
```

- [ ] **Step 6: Create the install-hooks script**

Create `tools/install-hooks.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT=$(git rev-parse --show-toplevel)
HOOK="$REPO_ROOT/.git/hooks/pre-commit"
cat > "$HOOK" <<'EOF'
#!/usr/bin/env bash
# Block commit if broken-wikilink count regresses.
set -euo pipefail
REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"
if ! command -v python >/dev/null 2>&1; then
  echo "pre-commit: python not found; skipping lint"
  exit 0
fi
if ! python tools/lint.py >/dev/null 2>&1; then
  EXIT=$?
  echo "pre-commit: wiki lint failed (exit $EXIT). See wiki/lint-report.md."
  exit $EXIT
fi
exit 0
EOF
chmod +x "$HOOK"
echo "Installed $HOOK"
```

- [ ] **Step 7: Install and verify the hook**

```
bash tools/install-hooks.sh
```

Expected: `Installed .../pre-commit`.

Test it with a known-safe no-op commit:

```
git commit --allow-empty -m "chore: verify pre-commit hook installed"
```

Expected: commit succeeds (lint passes on current state).

- [ ] **Step 8: Commit**

```
git add tools/lint.py tools/test_lint.py tools/install-hooks.sh wiki/lint-report.md wiki/lint-report.md.baseline
git commit -m "$(cat <<'EOF'
feat(tools): add wiki lint script, pre-commit hook, install helper

Python 3 + pyyaml; 5 pytest unit tests. Checks SCHEMA §5.3 items
(orphans, cross-link invariants, broken wikilinks, frontmatter
validation, citation-key resolution, stale-claim scan, concept-gap
detection, unsourced-queue consistency). Renders wiki/lint-report.md.
Baseline captured at 116 broken wikilinks for regression detection.
Pre-commit hook blocks commits that increase broken-wikilink count.
EOF
)"
```

---

### Task 1.2: Skill-hub brief template (reference for Tasks 1.3–1.9)

**This is a shared brief. Tasks 1.3–1.9 each reference it with per-hub specifics.**

**Agent type:** general-purpose, medium thoroughness.

**Shared brief (apply to every skill-hub task):**

> You are writing a new skill-level hub page for the Volleyball Coaching Bible wiki at `C:/Users/SongMu/documents/claudecode/vba/bible/`. **Read `wiki/SCHEMA.md` top-to-bottom before writing anything** — it defines the hub-page contract (§3.1, §4), citation policy (§5), cross-link invariants (§6), and voice (§8).
>
> Skill hubs sit between area-level hubs (`practice-planning.md`, `systems.md`, `philosophy.md`) and per-subskill technique pages. They are navigational, not expository — 600–1200 words.
>
> **Required body sections:** Overview, Major subtopics, Schools of thought, Getting started, Related areas, Sources.
>
> **Frontmatter:**
> ```yaml
> ---
> type: hub
> area: <skill>
> subtopics: [<subskill-slug-1>, <subskill-slug-2>, ...]
> ---
> ```
>
> **Cross-link budget (must all appear as `[[wikilinks]]` in the body):**
> - Every subskill technique page for this skill (e.g. passing.md must link `[[passing-forearm]]`, `[[passing-overhead]]`, `[[passing-serve-receive]]`, `[[passing-free-ball]]`)
> - The positions that most rely on this skill
> - The related drills category (a short paragraph enumerating drill wikilinks is fine; no full catalog — Dataview retrofit will handle that)
> - All three age-lens pages (`age-lens-14u`, `age-lens-hs`, `age-lens-college`)
> - Schools with distinctive methodology on this skill (e.g. GMS, AOC, ecological-dynamics, Japanese-training when relevant)
>
> **Citation weight:** Light per SCHEMA §5. No inline `[citation-key]` in body. `## Sources` at bottom lists 6–12 linked source pages.
>
> **Voice:** second-person present, per SCHEMA §8. Direct, coach-to-coach.
>
> **Do NOT invent content.** Only use source-page slugs that exist under `wiki/sources/`. Before citing, run `ls wiki/sources/ | grep <author>` to confirm the source exists.
>
> **When done:** commit with `feat(wiki): add <skill> skill-hub page`.

---

### Task 1.3: `wiki/passing.md` skill hub

**Files:** Create `wiki/passing.md`

**Per-hub specifics:**
- `subtopics`: `[passing-forearm, passing-overhead, passing-serve-receive, passing-free-ball]`
- Related positions: libero, defensive-specialist, outside-hitter, all back-row
- Contested methodology: AOC reads-first vs GMS motor-learning vs ecological-dynamics constraints-led vs Japanese midline/precision (see `passing-forearm.md` for the existing four-way framing — mirror that framing at the skill-level)
- Source anchors: aoc-2013-kiraly-4-keys-forearm-pass, aoc-2023-kiraly-precision-passing, aoc-2025-passing-posture-pursuit-platform, aoc-2024-kids-passing-fundamentals, kiraly-1997-championship-volleyball, gms-2018-clinic-report, pinder-2011-representative-learning-design, shea-1979-contextual-interference

- [ ] **Step 1:** Follow the shared brief from Task 1.2 with the specifics above.
- [ ] **Step 2:** Run `python tools/lint.py` and confirm broken-wikilink count went down.
- [ ] **Step 3:** Commit.

---

### Task 1.4: `wiki/setting.md` skill hub

**Files:** Create `wiki/setting.md`

**Per-hub specifics:**
- `subtopics`: `[setting-hands, setting-jump, setting-backset, setting-out-of-system]`
- Related positions: setter (primary), libero (second-ball)
- Contested methodology: AOC toolbox / Japanese bail / GMS motor-learning / eco-dynamics (same framing as `setting-out-of-system.md`)
- Source anchors: aoc-2024-setting-hand-hinge, aoc-2020-setting-fundamentals, kiraly-1997-championship-volleyball, aoc-2018-rose-offensive-systems, aoc-2015-rockwell-training-setters, aoc-2014-dunning-hitter-setter-connection

Same 3-step execution pattern as Task 1.3.

---

### Task 1.5: `wiki/hitting.md` skill hub

**Files:** Create `wiki/hitting.md`

**Per-hub specifics:**
- `subtopics`: `[hitting-approach, hitting-arm-swing, hitting-shot-selection, hitting-back-row-attack]`
- Related positions: outside-hitter, opposite, middle-blocker
- Contested methodology: AOC toolbox / GMS random / Russian power / Italian pressure / Brazilian creativity (same framing as `hitting-shot-selection.md`)
- Source anchors: aoc-2024-attack-approach, aoc-2024-attack-arm-mechanics, aoc-2021-teach-spiking, aoc-2014-dunning-hitter-setter-connection, kiraly-1997-championship-volleyball

Same 3-step execution pattern.

---

### Task 1.6: `wiki/blocking.md` skill hub

**Files:** Create `wiki/blocking.md`

**Per-hub specifics:**
- `subtopics`: `[blocking-footwork, blocking-hand-position, blocking-read, blocking-swing]`
- Related positions: middle-blocker (primary), opposite, outside-hitter
- Contested methodology: swing-vs-shuffle generational shift; AOC reading / GMS pattern / eco-dynamics affordance / Japanese anticipate (same framing as `blocking-footwork.md` and `blocking-read.md`)
- Source anchors: gms-nd-blocking, aoc-2024-importance-teaching-swing-blocking, aoc-2026-swing-blocking-footwork-beginners, aoc-2023-swing-blocking-when, aoc-2015-liskevych-mccutcheon-defense-blocking, aoc-2015-mccutcheon-blocking-keys, aoc-2026-bunch-read-blocking

Same 3-step execution pattern.

---

### Task 1.7: `wiki/serving.md` skill hub

**Files:** Create `wiki/serving.md`

**Per-hub specifics:**
- `subtopics`: `[serving-float, serving-jump-float, serving-topspin, serving-hybrid]`
- Related positions: all (every position serves)
- Contested methodology: modern women's float-dominance vs men's jump-topspin (same framing as `serving-topspin.md`)
- Source anchors: aoc-2025-float-serve-3-keys, aoc-2024-float-serve-toss, aoc-2020-types-of-serves, aoc-2024-kiraly-serving-placement, aoc-2024-kids-serving-fundamentals, aoc-2015-rose-serving-fundamentals

Same 3-step execution pattern.

---

### Task 1.8: `wiki/defense.md` skill hub

**Files:** Create `wiki/defense.md`

**Per-hub specifics:**
- `subtopics`: `[defense-platform, defense-reading, defense-pursuit]` (note: this is the individual-defense skill hub, not the team-defense systems hub — those live in `systems-detail/`)
- Related positions: libero (primary), defensive-specialist, all back-row
- Contested methodology: AOC reads-first / GMS pattern / eco-dynamics affordance / Japanese dig-everything (same framing as `defense-reading.md`)
- Source anchors: aoc-2025-training-reading-look-see-decide, aoc-2025-controlling-the-dig, aoc-2017-liskevych-asics-defense, aoc-2015-liskevych-mccutcheon-defense-blocking, aoc-2022-emergency-moves-passing-defense, aoc-2016-rockwell-defending-angle

Same 3-step execution pattern.

---

### Task 1.9: `wiki/transition.md` skill hub

**Files:** Create `wiki/transition.md`

**Per-hub specifics:**
- `subtopics`: `[transition-attack, transition-out-of-system]`
- Related positions: outside-hitter, opposite (block-to-approach), middle-blocker (block-to-approach), setter (OOS setting)
- Contested methodology: modern default (all schools agree transition is foundational) — section can cover differences in *how* transition is drilled rather than *whether* it's important
- Source anchors: aoc-2013-hoag-transition-drills, aoc-2014-johnson-lynch-passing-setting-transition, aoc-2015-shymansky-oh-transition-footwork, aoc-2013-lupo-ludwig-box-block-transition, aoc-2013-lupo-ludwig-free-ball-transition, aoc-2016-rosen-training-transition-in-out-system

Same 3-step execution pattern.

---

### Task 1.10: Secondary-coach brief template (reference for Tasks 1.11–1.25)

**Shared brief (apply to every secondary-coach-profile task):**

> You are writing a new coach profile for the Volleyball Coaching Bible wiki at `C:/Users/SongMu/documents/claudecode/vba/bible/`. **Read `wiki/SCHEMA.md`** — coach-profile contract is §3.2, frontmatter in §4, citation policy in §5 (heavy citation: inline `[citation-key]` after every non-generic claim), cross-link invariants §6 (≥1 school + ≥1 source), voice in §8.
>
> Also read one or two existing coach profiles (e.g. `wiki/coaches/karch-kiraly.md` for a full-length example, `wiki/coaches/daimatsu-hirobumi.md` for a historical example) to match house voice.
>
> **Required body sections:** Overview, Coaching career, Core teaching principles, Contributions to the game, Quotes & representative passages, Sources.
>
> **Frontmatter (fill in from the per-coach data provided):**
> ```yaml
> ---
> type: coach
> name: <Full Name>
> country: <country>
> era: <years or era label>
> roles: [<roles>]
> schools: [<slug>, ...]   # ≥1 required
> sources: [<citation-key>, ...]  # ≥1 required
> tags: [<optional>]
> ---
> ```
>
> **Source sourcing:** Only cite source pages that already exist under `wiki/sources/`. Before citing `[xyz]`, confirm `wiki/sources/xyz.md` exists. If the source base is thin, keep the profile proportionally shorter (target length below) and use `[unsourced]` per SCHEMA §5 honesty rules for claims you cannot ground — add a queue entry to `wiki/unsourced-queue.md` per SCHEMA §5 format.
>
> **Target length:** ~1500 words for high-source profiles; ~800 words for thin-source profiles (per-coach spec tells you which).
>
> **School linkage:** Every coach MUST link ≥1 school page. If the coach's primary institutional affiliation doesn't have a school page yet (e.g. `iowa-state-volleyball`, `ohio-state-volleyball`, `central-florida-volleyball`, `munciana-volleyball-club`), create a short institutional-tradition stub in `wiki/schools/` (match the format of the existing stubs like `penn-state.md`, `florida.md`) as part of this task.
>
> **Quotes section:** Even if thin, try to include at least one representative passage from the available AOC articles with proper `[citation-key]` attribution. If no direct quotes are available, write a flagged stub paragraph and queue the gap.
>
> **When done:** commit with `feat(wiki): add <firstname-lastname> coach profile`.

---

### Task 1.11: Salima Rockwell profile (full, ~1500w)

**Files:** Create `wiki/coaches/salima-rockwell.md`; optionally stub `wiki/schools/texas-volleyball.md` if needed.

**Per-coach specifics:**
- `name: Salima Rockwell`
- `country: USA`
- `era: 1990s-present`
- `roles: [player, coach, penn-state-alum, assistant-coach, head-coach]` (Penn State player under Russ Rose; Texas/Louisville assistant; Loyola Marymount HC; now at Washington)
- Known schools affiliation: penn-state (alum); usa-volleyball
- Source anchors (confirm each exists under `wiki/sources/`): aoc-2015-rockwell-training-setters, aoc-2015-rockwell-train-setter, aoc-2015-rockwell-five-on-five, aoc-2015-rockwell-pepper-series, aoc-2015-rockwell-cross-court-pepper, aoc-2015-rockwell-virus-variation-vancouver, aoc-2016-rockwell-defending-angle, and any other aoc-*rockwell* pages
- Contributions to highlight: defense teaching (angle defense, pepper progressions, virus variations), setter training (competitive five-on-five with setter-fed first ball), Russ-Rose lineage transmission

Same 3-step execution pattern (write, lint, commit).

---

### Task 1.12: Jim Stone profile (full, ~1500w)

**Files:** Create `wiki/coaches/jim-stone.md`

**Per-coach specifics:**
- `name: Jim Stone`
- `country: USA`
- `era: 1970s-present`
- `roles: [player, head-coach, author, clinician]` (Ohio State women's HC 1984–2009; author *Defensive Volleyball Drills* and other Human Kinetics titles; major AOC voice on defense/blocking/video)
- Known schools affiliation: art-of-coaching-volleyball; usa-volleyball; ohio-state-volleyball (STUB IF NEEDED)
- Source anchors: aoc-2018-stone-platform-management, aoc-2020-stone-liskevych-using-video, aoc-2025-controlling-the-dig, stone-notes-defensive-volleyball-drills (if source page exists; otherwise use the AOC-only set)
- Contributions to highlight: defense platform management (hips-under-ball framework), using video for skill correction, "Controlling the dig with body positioning," and generally bridging competitive coaching to the USAV coach-education pipeline

Same 3-step execution pattern.

---

### Task 1.13: Diane Flick-Williams profile (full, ~1500w)

**Files:** Create `wiki/coaches/diane-flick-williams.md`; stub `wiki/schools/western-washington-volleyball.md` if not present.

**Per-coach specifics:**
- `name: Diane Flick-Williams`
- `country: USA`
- `era: 2000s-present`
- `roles: [player, head-coach, clinician]` (Western Washington HC; Pass for Points AOC flagship)
- Known schools affiliation: art-of-coaching-volleyball; western-washington-volleyball (stub)
- Source anchors: yt-aoc-unknown-pass-for-points-diane-flick, aoc-2024-kiraly-reads-every-skill (if she appears), and any aoc-*flick* pages
- Contributions to highlight: Pass for Points as a competitive passing drill, serve-receive structure, D2 program excellence

Same 3-step execution pattern.

---

### Task 1.14: John Lingenfelter profile (full, ~1500w)

**Files:** Create `wiki/coaches/john-lingenfelter.md`; stub `wiki/schools/munciana-volleyball-club.md`.

**Per-coach specifics:**
- `name: John Lingenfelter`
- `country: USA`
- `era: 2000s-present`
- `roles: [head-coach, club-director, clinician]` (Munciana Volleyball Club — nationally-recognized Indiana club; directly matches Song's coaching context)
- Known schools affiliation: munciana-volleyball-club (STUB THIS WITHIN THIS TASK); art-of-coaching-volleyball
- Source anchors: any aoc-*munciana* or aoc-*lingenfelter* pages (confirm via `ls wiki/sources/ | grep -E "munciana|lingenfelter"`)
- Contributions to highlight: club-building at nationally-recognized level, middle-tempo setter-hitter timing, youth-through-18U pipeline, Munciana practice design

Same 3-step execution pattern.

---

### Task 1.15: Luka Slabe profile (full, ~1500w)

**Files:** Create `wiki/coaches/luka-slabe.md`

**Per-coach specifics:**
- `name: Luka Slabe`
- `country: Slovenia/USA`
- `era: 2000s-present`
- `roles: [player, head-coach, clinician]` (played internationally; coached college & professional; major AOC blocking voice)
- Known schools affiliation: art-of-coaching-volleyball
- Source anchors: any aoc-*slabe* pages (confirm — at least the static/swing/combo blocking piece)
- Contributions to highlight: blocking trichotomy (static/swing/combo), European-to-US methodology bridging, elite-level blocking mechanics

Same 3-step execution pattern.

---

### Task 1.16: Laurie Eisler profile (full, ~1500w)

**Files:** Create `wiki/coaches/laurie-eisler.md`; stub `wiki/schools/illinois-volleyball.md`.

**Per-coach specifics:**
- `name: Laurie Eisler`
- `country: USA`
- `era: 1990s-present`
- `roles: [head-coach, clinician]` (Illinois HC; cauldron philosophy)
- Known schools affiliation: illinois-volleyball (stub); art-of-coaching-volleyball; mike-hebert-lineage (via illinois)
- Source anchors: aoc-2013-mccutcheon-eisler-cauldron, any other aoc-*eisler*
- Contributions to highlight: competitive cauldron practice design with McCutcheon; Big Ten program building; Illinois/Hebert lineage stewardship

Same 3-step execution pattern.

---

### Task 1.17: Christy Johnson-Lynch profile (full, ~1500w)

**Files:** Create `wiki/coaches/christy-johnson-lynch.md`; stub `wiki/schools/iowa-state-volleyball.md`.

**Per-coach specifics:**
- `name: Christy Johnson-Lynch`
- `country: USA`
- `era: 2000s-present`
- `roles: [player, head-coach]` (Nebraska player; Iowa State HC)
- Known schools affiliation: iowa-state-volleyball (stub); art-of-coaching-volleyball
- Source anchors: aoc-2014-johnson-lynch-passing-setting-transition, aoc-2015-johnson-lynch-art-training-transition, aoc-2015-johnson-lynch-setter-transition, and any other aoc-*johnson-lynch*
- Contributions to highlight: transition training (her signature topic in AOC corpus), setter development, non-P5 program elevation

Same 3-step execution pattern.

---

### Task 1.18: Doug Beal profile (full, ~1500w)

**Files:** Create `wiki/coaches/doug-beal.md`

**Per-coach specifics:**
- `name: Doug Beal`
- `country: USA`
- `era: 1970s-2010s`
- `roles: [player, head-coach, usa-men-national-team-head-coach, administrator]` (USA Men's 1984 LA Olympic gold HC; USAV administrator)
- Known schools affiliation: usa-volleyball
- Source anchors: usav-2026-coach-academy or any beal-* pages (confirm); kiraly-1997-championship-volleyball (Kiraly was a Beal-era player; cross-cite appropriate passages)
- Contributions to highlight: architect of the 1984 LA gold; institutional-builder for US men's program; contribution to USAV coach-education lineage

If source base is thin after exhausting the existing sources, this profile may need to drop to ~800w with `[unsourced]` tags for specific methodology claims — follow the shared brief's honesty rules.

Same 3-step execution pattern.

---

### Task 1.19: Jen Flynn Oldenburg profile (brief, ~800w)

**Files:** Create `wiki/coaches/jen-flynn-oldenburg.md`

**Per-coach specifics:**
- `name: Jen Flynn Oldenburg`
- `country: USA`
- `era: 2010s-present`
- `roles: [player, head-coach]` (Ohio State HC)
- Known schools affiliation: ohio-state-volleyball (stub if not already created by Task 1.12); art-of-coaching-volleyball
- Source anchors: any aoc-*flynn-oldenburg* or aoc-*oldenburg* pages
- Contributions to highlight: the AOC piece(s) she's featured in

Same 3-step execution pattern. Target ~800 words reflects thin source base.

---

### Task 1.20: Kerry MacDonald profile (brief, ~800w)

**Files:** Create `wiki/coaches/kerry-macdonald.md`

**Per-coach specifics:**
- `name: Kerry MacDonald`
- `country: USA`
- `era: 2010s-present`
- `roles: [head-coach, clinician]`
- Known schools affiliation: art-of-coaching-volleyball
- Source anchors: aoc-2024-attack-arm-mechanics and any other aoc-*macdonald*
- Contributions to highlight: modern attack arm mechanics (torque + high-hand emphasis), upgrading arm-swing teaching

Same 3-step execution pattern.

---

### Task 1.21: Gina Schmidt profile (brief, ~800w)

**Files:** Create `wiki/coaches/gina-schmidt.md`

**Per-coach specifics:**
- `name: Gina Schmidt`
- `country: USA`
- `era: 2010s-present`
- `roles: [head-coach, clinician]`
- Known schools affiliation: art-of-coaching-volleyball
- Source anchors: aoc-2024-attack-approach and any other aoc-*schmidt*
- Contributions to highlight: modern attack approach (right-left 2-step → 4-step, "start slow, accelerate the last two"), appears prominently on `hitting-approach.md` and `age-lens-14u.md`

Same 3-step execution pattern.

---

### Task 1.22: Brian Rosen profile (brief, ~800w)

**Files:** Create `wiki/coaches/brian-rosen.md`

**Per-coach specifics:**
- `name: Brian Rosen`
- `country: USA`
- `era: 2010s-present`
- `roles: [head-coach, clinician]`
- Known schools affiliation: art-of-coaching-volleyball
- Source anchors: aoc-2026-swing-blocking-footwork-beginners, aoc-2016-rosen-training-transition-in-out-system, and any other aoc-*rosen*
- Contributions to highlight: swing-block beginner progressions (10-foot-line footwork first, jump added later); in/out-of-system transition training

Same 3-step execution pattern.

---

### Task 1.23: Mark Barnard profile (brief, ~800w)

**Files:** Create `wiki/coaches/mark-barnard.md`

**Per-coach specifics:**
- `name: Mark Barnard`
- `country: USA or Australia` (verify via the AOC piece)
- `era: 2010s-present`
- `roles: [head-coach, clinician]`
- Known schools affiliation: art-of-coaching-volleyball
- Source anchors: aoc-2023-back-row-attacking-basics and any other aoc-*barnard*
- Contributions to highlight: back-row attacking fundamentals (setter leads the hitter, takeoff behind 10ft, land in front row)

Same 3-step execution pattern.

---

### Task 1.24: Brandon Rosenthal profile (brief, ~800w)

**Files:** Create `wiki/coaches/brandon-rosenthal.md`

**Per-coach specifics:**
- `name: Brandon Rosenthal`
- `country: USA`
- `era: 2010s-present`
- `roles: [head-coach, clinician]`
- Known schools affiliation: art-of-coaching-volleyball
- Source anchors: aoc-2015-rosenthal-rapid-fire and any other aoc-*rosenthal*
- Contributions to highlight: rapid-fire drill design

Same 3-step execution pattern.

---

### Task 1.25: Todd Dagenais profile (brief, ~800w)

**Files:** Create `wiki/coaches/todd-dagenais.md`; stub `wiki/schools/central-florida-volleyball.md` if needed.

**Per-coach specifics:**
- `name: Todd Dagenais`
- `country: USA`
- `era: 2000s-present`
- `roles: [player, head-coach]` (Central Florida HC; referenced in McCutcheon profile)
- Known schools affiliation: central-florida-volleyball (stub); art-of-coaching-volleyball
- Source anchors: reference mccutcheon-2021-volleybrains-ep30 or mccutcheon-2022-championship-behaviors if he appears; any aoc-*dagenais* pages
- Contributions to highlight: whatever the source base supports; note in `## Quotes` if source base is too thin for direct-quote material

Same 3-step execution pattern. This is the thinnest-source profile — tag `[unsourced]` liberally.

---

### Task 1.26: Dataview retrofit batch

**Files:** Modify in-place.

**Agent type:** general-purpose, single agent owns this task for pattern consistency.

- [ ] **Step 1: Patch skill hubs (7 pages, once created by Tasks 1.3–1.9)**

For each of `wiki/{passing,setting,hitting,blocking,serving,defense,transition}.md`, insert a `## Drill catalog` section above `## Sources`:

Example for `wiki/passing.md`:

````markdown
## Drill catalog

```dataview
TABLE phase, levels, duration-min, team-size-min + "-" + team-size-max AS size
FROM "wiki/drills"
WHERE primary-skill = "passing" OR contains(techniques, "passing-forearm") OR contains(techniques, "passing-overhead") OR contains(techniques, "passing-serve-receive") OR contains(techniques, "passing-free-ball")
SORT phase ASC, duration-min ASC
```
````

Mechanical per-skill mapping:
- passing.md → `primary-skill = "passing"` plus contains checks for all 4 passing-* techniques
- setting.md → `primary-skill = "setting"` plus 4 setting-* techniques
- hitting.md → `primary-skill = "hitting"` plus 4 hitting-* techniques
- blocking.md → `primary-skill = "blocking"` plus 4 blocking-* techniques
- serving.md → `primary-skill = "serving"` plus 4 serving-* techniques
- defense.md → `primary-skill = "defense"` plus defense-* techniques (platform/reading/pursuit)
- transition.md → `primary-skill = "transition"` plus 2 transition-* techniques

- [ ] **Step 2: Patch age-lens pages (3 pages)**

For each of `wiki/age-lens-{14u,hs,college}.md`, insert `## Drill catalog (age-filtered)` above `## Sources`:

````markdown
## Drill catalog (age-filtered)

```dataview
TABLE primary-skill, phase, duration-min, team-size-min + "-" + team-size-max AS size
FROM "wiki/drills"
WHERE contains(levels, "14u")
SORT primary-skill ASC, duration-min ASC
```
````

(Swap `"14u"` for `"hs"` / `"college"` in the respective pages.)

- [ ] **Step 3: Patch position pages (6 pages)**

For each of `wiki/positions/{setter,outside-hitter,middle-blocker,opposite,libero,defensive-specialist}.md`, insert `## Drills for this position` above `## Sources`.

Setter example:

````markdown
## Drills for this position

```dataview
TABLE primary-skill, phase, duration-min
FROM "wiki/drills"
WHERE contains(techniques, "setting-hands") OR contains(techniques, "setting-jump") OR contains(techniques, "setting-backset") OR contains(techniques, "setting-out-of-system")
SORT primary-skill ASC, phase ASC
```
````

Per-position `contains` clauses (from each position's `key-skills:` frontmatter):
- setter → setting-* techniques + `primary-skill = "setting"`
- outside-hitter → hitting-approach, hitting-arm-swing, hitting-shot-selection, hitting-back-row-attack, passing-forearm, passing-serve-receive
- middle-blocker → hitting-approach, hitting-arm-swing (for slides), blocking-footwork, blocking-read, blocking-swing
- opposite → hitting-* techniques, blocking-footwork, blocking-hand-position
- libero → passing-forearm, passing-serve-receive, defense-platform, defense-reading, defense-pursuit
- defensive-specialist → passing-forearm, defense-platform, defense-reading

- [ ] **Step 4: Patch planning hubs (2 pages)**

On `wiki/practice-planning.md`, insert a `## Drill index by phase` section above `## Sources`:

````markdown
## Drill index by phase

```dataview
TABLE rows.file.link AS drills, rows.duration-min AS "durations"
FROM "wiki/drills"
GROUP BY phase
SORT phase ASC
```
````

On `wiki/season-planning.md`, insert `## Drills by season-phase applicability`:

````markdown
## Drills by level

```dataview
TABLE primary-skill, phase, duration-min, join(levels, ", ") AS levels
FROM "wiki/drills"
SORT primary-skill ASC, phase ASC
```
````

- [ ] **Step 5: Patch wide hubs (2 pages)**

On `wiki/philosophy.md`, insert `## Contested techniques` section above `## Sources`:

````markdown
## Contested techniques

```dataview
TABLE skill, subskill
FROM "wiki/techniques"
WHERE schools-perspectives
SORT skill ASC
```
````

On `wiki/systems.md`, insert `## Systems by age-appropriateness`:

````markdown
## Systems by age-appropriateness

```dataview
TABLE category, complexity, join(age-appropriateness, ", ") AS ages
FROM "wiki/systems-detail"
SORT category ASC, complexity ASC
```
````

- [ ] **Step 6: Patch SCHEMA.md §2.2 with Dataview install note**

In `wiki/SCHEMA.md` §2.2, add a single paragraph after the wiki/ tree:

```markdown
**Obsidian plugin requirement:** skill-hub, age-lens, position, and planning pages include `dataview` code blocks that render drill/source catalogs from frontmatter. Install the [Dataview](https://github.com/blacksmithgu/obsidian-dataview) community plugin in Obsidian to render them; without the plugin the queries show as markdown source (harmless but not useful).
```

- [ ] **Step 7: Run lint**

```
python tools/lint.py
```

Expected: pass. Broken wikilinks count has dropped further (skill hubs + coach profiles have already landed).

- [ ] **Step 8: Commit**

```
git add wiki/
git commit -m "feat(wiki): add Dataview retrofits across skill hubs, age-lens, positions, planning"
```

---

### Task 1.27: SCHEMA.md practice-plan page type update

**Files:** Modify `wiki/SCHEMA.md`

- [ ] **Step 1: Extend the page-types table in §3**

Add a row to the table near the top of §3:

```markdown
| Practice plan | `practice-plans/` | `<level>-<duration>-<label>.md` | `14u-90min-serve-receive.md` |
```

- [ ] **Step 2: Add a new subsection §3.10 after §3.9**

Add after age-lens section:

```markdown
### 3.10 Practice-plan pages

- **Folder / filename:** `wiki/practice-plans/<level>-<duration>-<label>.md`. Label is a descriptive kebab-case slug — typically the focus, or the season context when more identifying than the focus. Frontmatter carries the structured enums.
- **Required frontmatter:** `type: practice-plan`, `level`, `duration-min`, `focus`, `season-phase`, `drills` (≥3 required — each must resolve to a drill page), `sources` (≥1 required).
- **Required body sections:** `## Context`, `## Learning objectives`, `## Time blocks` (with sub-sections per phase, each naming drills as wikilinks with time allocations), `## Coaching cues`, `## Variations`, `## Adaptations by level`, `## Sources`.
- **Target length:** 500–800 words.
- **Citation weight:** Light. No inline citations; `## Sources` at bottom.
- **Cross-link rules:** Every `drills:` slug must correspond to a real drill page. Plans SHOULD wikilink to the applicable age-lens page.
```

- [ ] **Step 3: Add `practice-plan` frontmatter block to §4**

Add after the Age-lens block:

```yaml
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
```

- [ ] **Step 4: Extend the enum glossary in §4**

Append:

```markdown
- `focus ∈ {passing, setting, hitting, blocking, serving, defense, transition, serve-receive, out-of-system, match-prep, player-development, composite}`
- `season-phase ∈ {preseason, mid-season, pre-tournament, taper, tryout, postseason, match-day}`
- `level ∈ {14u, hs, college}` (same as `levels` array-valued counterpart on drill pages)
```

- [ ] **Step 5: Commit**

```
git add wiki/SCHEMA.md
git commit -m "docs(schema): add practice-plan page type (type #10) and enum glossary updates"
```

---

### Task 1.28: `wiki/index.md` update for new hubs + coaches + practice-plans folder

**Files:** Modify `wiki/index.md`

- [ ] **Step 1: Add Skill hubs section after Hub pages section**

Insert this section in `wiki/index.md` after the existing `## Hub pages` block:

```markdown
## Skill hubs
- [[passing]] — overview + entry into 4 passing subskills; schools-perspectives meta
- [[setting]] — overview + entry into 4 setting subskills; hand-hinge era
- [[hitting]] — overview + entry into 4 hitting subskills
- [[blocking]] — overview + entry into 4 blocking subskills; swing-vs-shuffle meta
- [[serving]] — overview + entry into 4 serving subskills
- [[defense]] — overview + entry into 3 defense subskills; reading-centric
- [[transition]] — overview + entry into 2 transition subskills
```

- [ ] **Step 2: Expand the Coaches section**

In the existing `## Coaches` section, add a new subsection:

```markdown
### Secondary / specialist (W7)
- [[salima-rockwell]] — Penn State alum → Texas/Louisville assistant → Loyola Marymount/Washington HC; defense + setter training lineage
- [[jim-stone]] — Ohio State women's HC 1984-2009; author *Defensive Volleyball Drills*; AOC defense/blocking voice
- [[diane-flick-williams]] — Western Washington HC; Pass for Points AOC flagship
- [[john-lingenfelter]] — Munciana Volleyball Club; nationally-recognized 14U-to-18U club pipeline
- [[luka-slabe]] — AOC static/swing/combo blocking corpus
- [[laurie-eisler]] — Illinois HC; competitive cauldron with McCutcheon
- [[christy-johnson-lynch]] — Iowa State HC; transition training specialist
- [[doug-beal]] — USA Men's 1984 LA Olympic gold HC; USAV administrator
- [[jen-flynn-oldenburg]] — Ohio State HC
- [[kerry-macdonald]] — modern attack arm mechanics
- [[gina-schmidt]] — modern attack approach
- [[brian-rosen]] — swing-block beginner progressions; in/out-of-system transition
- [[mark-barnard]] — back-row attacking fundamentals
- [[brandon-rosenthal]] — rapid-fire drill
- [[todd-dagenais]] — Central Florida HC
```

- [ ] **Step 3: Add Practice-plans section after Age-lenses**

```markdown
## Practice plans
### 14U
- [[14u-90min-serve-receive]] — serve-receive focus, mid-season
- [[14u-120min-pre-tournament]] — competition-heavy, pre-tournament
- [[14u-90min-transition]] — transition-offense focus, mid-season
- [[14u-60min-tryout]] — evaluation-oriented, tryout
- [[14u-90min-first-week]] — team-formation + fundamentals install, preseason

### HS
- [[hs-120min-preseason-intensity]] — fall preseason intensity
- [[hs-90min-mid-season-tuesday]] — typical mid-season Tuesday microcycle
- [[hs-90min-match-prep]] — pre-Friday match-prep
- [[hs-60min-match-day-activation]] — day-of activation
- [[hs-120min-postseason-development]] — post-season player development

### College
- [[college-120min-ncaa-fall-pre-match]] — pre-match preparation
- [[college-90min-in-season-video]] — video-driven correction
- [[college-120min-spring-individual]] — spring individual development
- [[college-120min-conference-week]] — conference-week serve-pass-defend emphasis
- [[college-90min-taper]] — taper day before a major match
```

- [ ] **Step 4: Commit**

```
git add wiki/index.md
git commit -m "docs(wiki): expand index with skill hubs, secondary coaches, practice-plans"
```

---

### Task 1.29: Dispatch 1 checkpoint — run lint, log entry, review

- [ ] **Step 1: Run full lint**

```
python tools/lint.py
```

Expected: broken-wikilink count drops from 116 baseline to < 40. Orphan count acceptable. Report lands at `wiki/lint-report.md`.

- [ ] **Step 2: Append a log entry to `wiki/log.md`**

```markdown
## [2026-04-24] dispatch-1-complete | Tracks 1+2 content scaffolding
Parallel dispatch of 24 agents produced:
- 7 skill hub pages (passing/setting/hitting/blocking/serving/defense/transition)
- 15 secondary-coach profiles (8 full @~1500w + 7 brief @~800w)
- Dataview retrofits across 25 pages (7 skill hubs + 3 age-lens + 6 positions + 2 planning hubs + 2 wide hubs)
- `tools/lint.py` + pre-commit hook + install helper
- SCHEMA.md page-type #10 (practice-plan) added + Dataview plugin note
- wiki/index.md expanded
Broken-wikilink count dropped from 116 → <N from lint report>.
Next: Dispatch 2 (15 practice-plan templates + 9 unsourced-queue backfill clusters).
```

- [ ] **Step 3: Commit log entry**

```
git add wiki/log.md
git commit -m "docs(wiki): dispatch-1 log entry"
```

---

## Dispatch 2 — Practice plans + research backfill

Another parallel dispatch of ~24 agents.

---

### Task 2.1: Practice-plan brief template (reference for Tasks 2.2–2.16)

**Shared brief:**

> You are writing a new practice-plan template for the Volleyball Coaching Bible wiki at `C:/Users/SongMu/documents/claudecode/vba/bible/`. **Read `wiki/SCHEMA.md` §3.10 for the practice-plan contract** (added in Task 1.27) and §4 for frontmatter. Also read 1–2 drill pages (e.g. `wiki/drills/butterfly-passing.md`) so you know how drills are structured.
>
> **Target length:** 500–800 words.
>
> **Frontmatter:**
> ```yaml
> ---
> type: practice-plan
> level: 14u|hs|college
> duration-min: <integer>
> focus: <enum from SCHEMA §4 glossary>
> season-phase: <enum from SCHEMA §4 glossary>
> drills: [<slug-1>, <slug-2>, <slug-3>, ...]   # ≥3 real drill pages that exist under wiki/drills/
> sources: [<citation-key>, ...]
> ---
> ```
>
> **Required body sections:**
> 1. `## Context` — one paragraph: who is this plan for (level + season context), what problem it solves, when you'd run it.
> 2. `## Learning objectives` — 3–5 measurable bullets.
> 3. `## Time blocks` — the practice itself, structured as:
>    - `### Warm-up (N min)` — ball-in-hand + dynamic + (jump warm-up if intensity warrants)
>    - `### Skill development (N min)`
>    - `### Strategic (N min)`
>    - `### Competition (N min)`
>    - `### Cool-down (N min)`
>    Each block names its drills as `[[wikilink]]` (only use drills that actually exist under `wiki/drills/`) with explicit time allocation and 1–2 sentences of context.
> 4. `## Coaching cues` — 5–8 cue-language items tied to the plan's objectives.
> 5. `## Variations` — three knobs: team size, intensity, duration.
> 6. `## Adaptations by level` — what to change one level up and one level down.
> 7. `## Sources` — linked source pages (`[[citation-key]]` format).
>
> **Drill verification:** before including a drill slug in `drills:` frontmatter or as a body `[[wikilink]]`, run `ls wiki/drills/ | grep <slug>` to confirm it exists. The existing 50-drill library is listed in `wiki/index.md`.
>
> **Reorder blocks when methodology warrants** — e.g., a game-based plan may front-load `### Competition`, then `### Skill development` as targeted-correction time. Ordering is not strict; the 5 phase labels are.
>
> **Cross-link rule:** The plan SHOULD wikilink to its applicable age-lens (e.g. a 14U plan wikilinks `[[age-lens-14u]]` in `## Context` or `## Adaptations`).
>
> **Voice:** second-person, present, concise, per SCHEMA §8.
>
> **When done:** commit with `feat(wiki): add <level>-<duration>-<label> practice plan`.

---

### Tasks 2.2–2.16: Individual practice-plan templates

Each task follows the shared brief with these per-template specifics. Execution pattern for each: (1) apply the shared brief with specifics below, (2) run `python tools/lint.py`, (3) commit.

**Task 2.2: `14u-90min-serve-receive.md`**
- `level: 14u`, `duration-min: 90`, `focus: serve-receive`, `season-phase: mid-season`
- Suggested drills: butterfly-passing, serve-receive-3v3, two-line-passing, serve-receive-competition, cooperative-25-goal, dynamic-warmup-volleyball
- Time shape: 10 warm-up / 30 skill / 25 strategic (SR formations) / 20 competition / 5 cool-down
- Must wikilink `[[age-lens-14u]]`, `[[passing-serve-receive]]`, `[[serve-receive-4-player]]`

**Task 2.3: `14u-120min-pre-tournament.md`**
- `level: 14u`, `duration-min: 120`, `focus: composite`, `season-phase: pre-tournament`
- Suggested drills: dynamic-warmup-volleyball, wash-drill, queen-of-the-court, gold-medal-scrimmage, serve-targets, pressure-serving, six-player-defense
- Time shape: 15 warm-up / 20 skill (targeted weak-spot) / 25 strategic (scout-driven plays) / 55 competition / 5 cool-down

**Task 2.4: `14u-90min-transition.md`**
- `level: 14u`, `duration-min: 90`, `focus: transition`, `season-phase: mid-season`
- Suggested drills: dynamic-warmup-volleyball, pepper, pass-set-hit, transition-rally, free-ball-to-offense, queen-of-the-court
- Time shape: 10 warm-up / 25 skill / 20 strategic / 30 competition / 5 cool-down

**Task 2.5: `14u-60min-tryout.md`**
- `level: 14u`, `duration-min: 60`, `focus: player-development`, `season-phase: tryout`
- Suggested drills: dynamic-warmup-volleyball, two-line-passing, target-setting, approach-and-swing, serve-targets, queen-of-the-court
- Time shape: 10 warm-up / 30 evaluative-skill (rotating stations) / 0 strategic / 15 competition (6v6 or 4v4) / 5 cool-down

**Task 2.6: `14u-90min-first-week.md`**
- `level: 14u`, `duration-min: 90`, `focus: composite`, `season-phase: preseason`
- Suggested drills: dynamic-warmup-volleyball, ball-control-warmup, butterfly-passing, target-setting, serve-targets, cooperative-25-goal
- Time shape: 15 warm-up / 40 skill / 15 strategic (rotation install) / 15 competition (cooperative) / 5 cool-down

**Task 2.7: `hs-120min-preseason-intensity.md`**
- `level: hs`, `duration-min: 120`, `focus: composite`, `season-phase: preseason`
- Suggested drills: dynamic-warmup-volleyball, jump-warmup, weave-passing, three-setter-rotation, hitting-vs-block, swing-block-shuffle, pressure-serving, wash-drill, conditioning-court-sprints, arm-care-routine
- Time shape: 15 warm-up / 35 skill / 25 strategic / 35 competition / 10 cool-down (conditioning + arm care)

**Task 2.8: `hs-90min-mid-season-tuesday.md`**
- `level: hs`, `duration-min: 90`, `focus: composite`, `season-phase: mid-season`
- Suggested drills: dynamic-warmup-volleyball, shuttle-passing, out-of-system-setting, transition-hitting, block-touch-drill, serve-receive-competition, wash-drill
- Time shape: 10 warm-up / 25 skill / 20 strategic / 30 competition / 5 cool-down

**Task 2.9: `hs-90min-match-prep.md`**
- `level: hs`, `duration-min: 90`, `focus: match-prep`, `season-phase: mid-season`
- Suggested drills: dynamic-warmup-volleyball, pass-set-hit, three-setter-rotation, read-blocking-progression, zone-serving, serve-receive-competition, six-player-defense
- Time shape: 10 warm-up / 20 skill (scout-target) / 30 strategic (opponent plays) / 25 competition / 5 cool-down

**Task 2.10: `hs-60min-match-day-activation.md`**
- `level: hs`, `duration-min: 60`, `focus: composite`, `season-phase: match-day`
- Suggested drills: dynamic-warmup-volleyball, ball-control-warmup, partner-pepper-warmup, target-setting, serve-targets, jump-serve-progression (if jump-topspin server), cool-down-mobility
- Time shape: 15 warm-up / 20 skill (light touch) / 10 strategic (rotation walk-through) / 10 competition (short serve-pass-defend) / 5 cool-down

**Task 2.11: `hs-120min-postseason-development.md`**
- `level: hs`, `duration-min: 120`, `focus: player-development`, `season-phase: postseason`
- Suggested drills: dynamic-warmup-volleyball, jump-warmup, weave-passing, jump-setting-progression, line-vs-angle-shot, swing-block-shuffle, jump-serve-progression, king-of-the-court, arm-care-routine
- Time shape: 15 warm-up / 50 skill (skill-building focus) / 15 strategic / 30 competition / 10 cool-down

**Task 2.12: `college-120min-ncaa-fall-pre-match.md`**
- `level: college`, `duration-min: 120`, `focus: match-prep`, `season-phase: mid-season`
- Suggested drills: dynamic-warmup-volleyball, jump-warmup, pass-set-hit, three-setter-rotation, transition-rally, read-blocking-progression, pressure-serving, six-player-defense, gold-medal-scrimmage
- Time shape: 15 warm-up / 20 skill / 30 strategic / 45 competition / 10 cool-down

**Task 2.13: `college-90min-in-season-video.md`**
- `level: college`, `duration-min: 90`, `focus: composite`, `season-phase: mid-season`
- Suggested drills: dynamic-warmup-volleyball, shuttle-passing, target-setting, transition-hitting, block-touch-drill, wash-drill
- Time shape: 10 warm-up / 25 video-tagged skill correction / 15 strategic (video-driven positional work) / 35 competition / 5 cool-down
- Extra: `## Context` must reference the video workflow from `wiki/match-prep.md` and `aoc-2020-stone-liskevych-using-video`

**Task 2.14: `college-120min-spring-individual.md`**
- `level: college`, `duration-min: 120`, `focus: player-development`, `season-phase: postseason`
- Suggested drills: dynamic-warmup-volleyball, jump-warmup, jump-setting-progression, hitting-vs-block, line-vs-angle-shot, swing-block-shuffle, jump-serve-progression, reactive-jumping, arm-care-routine
- Time shape: 15 warm-up / 55 individual skill / 15 strategic / 25 competition (small-sided) / 10 cool-down

**Task 2.15: `college-120min-conference-week.md`**
- `level: college`, `duration-min: 120`, `focus: composite`, `season-phase: pre-tournament`
- Suggested drills: dynamic-warmup-volleyball, jump-warmup, weave-passing, out-of-system-setting, hitting-vs-block, read-blocking-progression, pressure-serving, six-player-defense, wash-drill, king-of-the-court
- Time shape: 15 warm-up / 25 skill / 25 strategic / 45 competition / 10 cool-down

**Task 2.16: `college-90min-taper.md`**
- `level: college`, `duration-min: 90`, `focus: composite`, `season-phase: taper`
- Suggested drills: dynamic-warmup-volleyball, partner-pepper-warmup, target-setting, zone-serving, serve-receive-competition, cool-down-mobility
- Time shape: 15 warm-up / 15 skill (light) / 20 strategic (rotation/signal rehearsal) / 30 competition (controlled) / 10 cool-down

---

### Tasks 2.17–2.25: Unsourced-queue research clusters

**Shared brief for research-cluster tasks:**

> You are executing an unsourced-queue backfill cluster for the Volleyball Coaching Bible wiki. Your job: take a cluster of `[unsourced]` / `[unverified]` tags in specific wiki pages, research the authoritative primary sources, ingest them into `raw/` + `wiki/sources/` per SCHEMA §8.1, replace tags with `[citation-key]` citations, and clear the resolved entries from `wiki/unsourced-queue.md`.
>
> Follow SCHEMA §8.1 ingest workflow strictly:
> 1. Fetch primary source (WebFetch or user-provided). Save to `raw/articles/` or other appropriate subfolder.
> 2. Update `raw/INDEX.md`.
> 3. Create `wiki/sources/<citation-key>.md` per SCHEMA §3.8.
> 4. Update target wiki page(s): add citation-key to `sources:` frontmatter; replace `[unsourced]` with `[citation-key]`.
> 5. Remove resolved entries from `wiki/unsourced-queue.md`.
> 6. If a claim still cannot be sourced after best-effort research, leave the `[unsourced]` tag AND update the queue entry with what you learned (new research hypothesis).
>
> **No fabrication.** If you can't find the source, the claim stays tagged honestly.
>
> **When done:** commit with `feat(wiki): backfill <cluster-name> cluster (<N> entries cleared)`.

**Task 2.17: NCAA recruiting calendar** (2 entries in `wiki/recruiting.md`)
- Fetch: NCAA.org D1 recruiting-calendar volleyball page; AVCA recruiting resources; PrepVolleyball calendar explainer if available
- Target claims: first-permissible-contact dates, visit windows, NLI signing dates

**Task 2.18: AVCA awards + Wise tenure ranking** (4 entries in `wiki/coaches/mary-wise.md`)
- Fetch: AVCA awards history page; Florida volleyball official bio for Wise; AVCA Hall of Fame induction materials
- Target claims: Wise AVCA National Coach of the Year count, tenure ranking, Final Four framing, assistant-tree placement

**Task 2.19: Bernardinho + Brazilian methodology** (11 entries across `wiki/coaches/bernardinho.md` and `wiki/schools/brazilian-school.md`)
- Fetch: Bernardinho's *Transformando Suor em Ouro* publisher preview (Amazon or Google Books) + AOC/FIVB long-form interviews + CBV features + a Bernardinho Wikipedia-linked interview
- Target claims: methodology principles (speed-first, work-ethic, youth pipeline), Italian-Brazilian exchange, Brazilian club-pipeline systemic framing, Guimarães as 1992 Barcelona HC

**Task 2.20: Velasco methodology** (7 entries in `wiki/coaches/julio-velasco.md`)
- Fetch: Velasco clinic recordings (YouTube) with transcripts; FIVB + CEV features; any AOC-Velasco pieces
- Target claims: Generazione di Fenomeni methodology, psychological leadership, tactical preparation

**Task 2.21: Guidetti methodology** (3 entries in `wiki/coaches/giovanni-guidetti.md`)
- Fetch: VakıfBank feature pieces; CEV features; any modern-European-club coaching literature
- Target claims: women's club modernization, national-team vs club methodology differences

**Task 2.22: Daimatsu + Japanese historical** (3 entries in `wiki/coaches/daimatsu-hirobumi.md` + anything related in `wiki/schools/japanese-training.md`)
- Fetch: Roy Tomizawa's *1964 - The Greatest Year in the History of Japan* publisher preview; Helen Macnaughtan academic article on 1964 Japan women's volleyball; 1964 Sports Illustrated article if accessible
- Target claims: Daimatsu hire date (1953 vs 1954), NHK ratings for 1964 Olympic final

**Task 2.23: Hebert thin source base** (7 entries in `wiki/coaches/mike-hebert.md`)
- Fetch: Human Kinetics preview of *Thinking Volleyball* (2013); AVCA bio for Hebert; Illinois/Minnesota/New Mexico volleyball program histories
- Target claims: methodology principles (currently thinly sourced), program-building details, book-derived frameworks

**Task 2.24: USAV CAP editorial claims** (4 entries in `wiki/schools/usa-volleyball.md`)
- Fetch: Coach Your Brains Out podcast episodes discussing USAV CAP/Coach Academy transition; GMS or AOC commentary on USAV curriculum evolution
- Target claims: CAP-as-bureaucratic-gatekeeping framing, coverage-slant toward women's indoor, access disparities

**Task 2.25: Nakagaichi 1972 [unverified]** (1 entry across Nakagaichi profile + Japanese-training school)
- Fetch: FIVB historical records for 1972 Munich men's volleyball gold HC; JVA records; any English-language 1972 Olympic volleyball retrospectives
- Target: identify actual 1972 Japan men's gold HC, create source page, update Nakagaichi profile and Japanese-training page

**Execution for each research task:** (1) apply the shared brief with specifics, (2) commit as `feat(wiki): backfill <cluster> cluster`.

---

### Task 2.26: Dispatch 2 checkpoint — lint + log entry

- [ ] **Step 1: Run lint**

```
python tools/lint.py
```

Expected: broken-wikilink count continues to drop; unsourced-queue count drops from ~40 to < 10.

- [ ] **Step 2: Log entry**

Append to `wiki/log.md`:

```markdown
## [2026-04-24] dispatch-2-complete | Practice plans + unsourced backfill
Parallel dispatch of 24 agents produced:
- 15 practice-plan templates (5 × 14U + 5 × HS + 5 × college)
- 9 unsourced-queue research clusters (~40 entries resolved)
Unsourced-queue count: ~40 → <N from lint report>.
Broken-wikilink count: <from dispatch-1> → <new count>.
Next: Dispatch 3 (residual cleanup — remaining broken links, Munciana ingest, uncommitted AOC pairing, final lint).
```

- [ ] **Step 3: Commit**

```
git add wiki/log.md
git commit -m "docs(wiki): dispatch-2 log entry"
```

---

## Dispatch 3 — Cleanup pass

Mostly sequential; smaller scope than Dispatches 1–2.

---

### Task 3.1: Residual broken-wikilink resolution

**Files:** Modify `wiki/` as needed; create stubs in `wiki/schools/` or `wiki/drills/` as the lint report surfaces.

- [ ] **Step 1: Read the current lint report**

```
cat wiki/lint-report.md
```

Look at the "Broken wikilinks" section. Group remaining broken links by type:
- Drill variants (e.g. `[[blitz-the-bro]]`, `[[wave-serve-receive]]`, `[[three-person-serve-receive]]`)
- Institutional slugs (e.g. `[[illinois-volleyball]]`, `[[byu]]`, `[[china-women-national-team]]`)
- Generic-concept slugs (e.g. `[[footwork]]`, `[[ball-control]]`)

- [ ] **Step 2: For each drill variant — decide and act**

For each drill-like broken wikilink: if it's a real drill that deserves a page, create one following `wiki/_templates/drill.md`. If it's just a variation name that should live inside an existing drill's `## Variations`, edit the referring page to remove the wikilink syntax (keep the name as plain text).

Example resolutions:
- `[[blitz-the-bro]]` — a real USA WNT 6v6 game per the passing-forearm page; create `wiki/drills/blitz-the-bro.md` as a short drill page, or convert to plain text inside a `## Variations` list on a related drill page.
- `[[wave-serve-receive]]` — appears in passing-forearm as a Karin Keeney 10-to-target SR drill. Has a paired source (yt-aoc-20210112-wave-serve-receive-drill). Create `wiki/drills/wave-serve-receive.md` using that source.
- `[[three-person-serve-receive]]` — probably collapses into `wiki/drills/serve-receive-3v3.md`. Replace the wikilink with `[[serve-receive-3v3]]`.

- [ ] **Step 3: For each institutional slug — create an institutional-tradition stub**

Match the pattern of existing stubs (`wiki/schools/penn-state.md`, `wiki/schools/florida.md`). Frontmatter:

```yaml
---
type: school
name: <Program Name>
origin: USA
founders: []
core-principles: []
associated-coaches: [<coach-slugs>]
sources: []
---
# <Program Name>
## Overview
Institutional-tradition stub for bidirectional-link compliance. To flesh out in a future Wave.
```

- [ ] **Step 4: For each generic-concept slug — decide**

For each generic concept referenced 3+ times (e.g. `[[footwork]]`):
- If it deserves its own page, create a hub-style stub
- If it should point at an existing page, edit referring pages to redirect (e.g. `[[footwork]]` → remove wikilink, plain text, or point at most-relevant technique like `[[blocking-footwork]]` depending on context)

- [ ] **Step 5: Run lint, verify residual broken links < 10**

```
python tools/lint.py
```

- [ ] **Step 6: Commit**

```
git add wiki/
git commit -m "chore(wiki): resolve residual broken wikilinks (drill variants, institutional stubs, generic concepts)"
```

---

### Task 3.2: Munciana Drills folder ingest

**Files:** Inspect `Munciana Drills/` (uncommitted); ingest per content.

- [ ] **Step 1: List contents**

```
ls "Munciana Drills/"
```

- [ ] **Step 2: Read each file**

For each file, determine whether it's:
- A drill write-up → convert to `wiki/drills/<slug>.md` per SCHEMA §3.7 drill contract, or to `raw/articles/munciana-<slug>.md` raw + paired source page
- An article/notes → convert to `raw/articles/munciana-<slug>.md` + paired `wiki/sources/<citation-key>.md`
- A draft/incomplete file → flag and defer with a log note; do not force-ingest

- [ ] **Step 3: Ingest each per SCHEMA §8.1**

For each ingested file:
- Save to appropriate `raw/` subfolder
- Update `raw/INDEX.md`
- Create source page (if not a drill)
- Cross-link from `wiki/coaches/john-lingenfelter.md` and `wiki/schools/munciana-volleyball-club.md`

- [ ] **Step 4: Remove the now-empty `Munciana Drills/` folder if fully ingested, or keep with a `.deferred` marker for deferred files**

- [ ] **Step 5: Commit**

```
git add .
git commit -m "feat(wiki): ingest Munciana Drills folder (<N> drill pages / <M> source pages)"
```

---

### Task 3.3: Uncommitted `raw/articles/aoc-*.md` pairing

**Files:** `raw/articles/aoc-*.md` (untracked) + `wiki/sources/aoc-*.md` (as needed).

- [ ] **Step 1: List untracked AOC raw articles**

```
git ls-files --others --exclude-standard raw/articles/ | grep aoc-
```

- [ ] **Step 2: For each untracked raw article, check for paired source page**

```
# Example script:
for f in $(git ls-files --others --exclude-standard raw/articles/ | grep aoc-); do
  slug=$(basename "$f" .md)
  if [ -f "wiki/sources/$slug.md" ]; then
    echo "PAIR OK: $slug"
  else
    echo "MISSING SOURCE: $slug"
  fi
done
```

- [ ] **Step 3: For each MISSING SOURCE, create a `wiki/sources/<slug>.md` page**

Per SCHEMA §3.8 source-page contract. Use the raw article's metadata (author, date, URL) to populate frontmatter.

- [ ] **Step 4: For duplicates (raw files that match already-ingested sources), delete the duplicate raw file cleanly**

- [ ] **Step 5: Update `raw/INDEX.md`** to reflect the pairings.

- [ ] **Step 6: Run lint**

- [ ] **Step 7: Commit**

```
git add raw/ wiki/sources/
git commit -m "chore(wiki): pair uncommitted AOC raw articles with source pages"
```

---

### Task 3.4: Concept-gap stubs (from lint report)

**Files:** Whatever the lint "Concept gaps" section surfaces.

- [ ] **Step 1: Read the lint report concept-gap section**

```
grep -A 100 "^## Concept gaps" wiki/lint-report.md
```

- [ ] **Step 2: For each concept referenced ≥3 times without a page, decide**

Options:
- Create a stub hub/technique/drill page if the concept genuinely deserves its own entry
- Redirect referring pages to an existing page if it's a naming-mismatch (e.g. `[[free-ball-transition]]` → `[[transition-out-of-system]]` or link to `[[passing-free-ball]]`)
- Leave as residual if the concept is best handled as plain prose

- [ ] **Step 3: Apply decisions, run lint, commit**

```
git add wiki/
git commit -m "chore(wiki): address lint-surfaced concept gaps"
```

---

### Task 3.5: Final lint + dispatch-3 log + acceptance checklist

- [ ] **Step 1: Run final lint**

```
python tools/lint.py
```

Expected:
- Broken wikilinks < 10
- Unsourced-queue entries < 10
- No cross-link invariant violations
- Frontmatter all valid

Save the report as the new baseline:

```
cp wiki/lint-report.md wiki/lint-report.md.baseline
```

- [ ] **Step 2: Append a final log entry to `wiki/log.md`**

```markdown
## [2026-04-24] dispatch-3-complete | Cleanup + final lint
- Resolved <N> residual broken wikilinks
- Ingested Munciana Drills/ folder (<N> drill pages / <M> source pages)
- Paired <N> uncommitted AOC raw articles with source pages
- Addressed <N> concept gaps surfaced by lint

Final lint report:
- Broken wikilinks: 116 → <final N>
- Orphans: <N>
- Unsourced queue: 40+ → <final N>
- Stale methodology pages: <N>
- Concept gaps: <N>

Tracks 1+2 complete. Acceptance checklist in
docs/superpowers/specs/2026-04-24-wiki-improvement-tracks-1-2-design.md §6.1
runs green.
```

- [ ] **Step 3: Walk the §6.1 acceptance checklist and confirm each item**

For each line in the acceptance checklist in the spec, verify it holds. Any that don't hold — go back and fix before closing out.

- [ ] **Step 4: Final commit**

```
git add wiki/log.md wiki/lint-report.md wiki/lint-report.md.baseline
git commit -m "$(cat <<'EOF'
chore(wiki): tracks 1+2 complete — final lint + handoff

Final lint report attached. Broken wikilinks 116 → <N>. Unsourced
queue 40+ → <N>. Tracks 1+2 acceptance criteria met per spec §6.1.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 5: Report the final state to the user**

Summarize what shipped, final lint numbers, residual deferred work (if any), and confirm Track 3 (the deferred 14U operational layer) is still queued for a later spec.

---

## Self-review notes

- **Spec coverage:** Every item in spec §2.1 has a task. Skill hubs (Tasks 1.3–1.9), Dataview retrofits (1.26), practice plans (2.2–2.16), coach profiles (1.11–1.25), unsourced backfill (2.17–2.25), lint automation (1.1), residual cleanup (3.1–3.4), Munciana ingest (3.2), uncommitted AOC pairing (3.3). SCHEMA update (1.27). Index update (1.28). Log entries after each dispatch (1.29, 2.26, 3.5). Acceptance walkthrough (3.5).
- **No placeholders:** All steps reference actual files, actual commands, concrete frontmatter snippets and code. No "TBD" / "TODO" / "implement later".
- **Type consistency:** Page types, slug patterns, and frontmatter fields match SCHEMA.md §3/§4 and the design spec §3.3. Dataview query syntax is consistent across retrofits.
- **Scope:** Single implementation plan serves the single spec. No decomposition needed.
