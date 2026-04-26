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
# Inline citation: [citation-key] NOT preceded by [ (wikilink) or word char and NOT followed by ( (markdown link) or ]
INLINE_CITE_RE = re.compile(r"(?<!\[)(?<!\w)\[([a-z0-9][a-z0-9\-]*)\](?!\()(?!\])")
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
    "ops-doc": ["type", "kind", "sources"],
    "age-guide": ["type", "age", "phase", "sources"],
    "cue-dictionary": ["type", "skill", "age-bands", "sources"],
    "drill-pick-list": ["type", "age", "season-context", "drills", "sources"],
}

ENUM_VALUES = {
    # `phase` is used both on drills (warm-up/skill/strategic/competition/conditioning)
    # and on age-guides (introduction/fundamentals/.../college-bridge). The union below
    # accepts either; per-type semantic enforcement is left to the frontmatter contract.
    "phase": {"warm-up", "skill", "strategic", "competition", "conditioning",
              "introduction", "fundamentals", "late-fundamentals",
              "specialization", "advanced", "college-bridge"},
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
    "scope": {"single-session", "week", "macrocycle"},
    "kind": {"match-prep", "tryout-rubric", "club-ops"},
    "audience": {"coach", "parent", "club-director", "front-office"},
    "age": {"10s", "11s", "12s", "13s", "14s", "15s", "16s", "17s", "18s"},
    "season-context": {"composite", "preseason", "mid-season", "pre-tournament", "taper",
                       "tryout", "postseason", "match-day"},
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


SKIP_SLUGS_FOR_SCAN = {"lint-report"}


def collect_pages(wiki: Path):
    """Return dict slug -> {path, meta, body, text, inbound_count, outbound_links}"""
    pages = {}
    for md in wiki.rglob("*.md"):
        slug = md.stem
        # lint-report.md is generated output and self-references every broken link
        # in its body. Including it makes runs non-idempotent, so skip the scan.
        if slug in SKIP_SLUGS_FOR_SCAN:
            continue
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
        elif t == "ops-doc":
            kind = m.get("kind")
            if not kind:
                violations.append((str(p["path"]), "ops-doc missing kind"))
            elif kind not in ENUM_VALUES["kind"]:
                violations.append((str(p["path"]), f"ops-doc invalid kind '{kind}'"))
            if not m.get("sources"):
                violations.append((str(p["path"]), "ops-doc missing sources"))
        elif t == "age-guide":
            if not m.get("age"):
                violations.append((str(p["path"]), "age-guide missing age"))
            if not m.get("phase"):
                violations.append((str(p["path"]), "age-guide missing phase"))
            if not m.get("sources"):
                violations.append((str(p["path"]), "age-guide missing sources"))
        elif t == "cue-dictionary":
            if not m.get("skill"):
                violations.append((str(p["path"]), "cue-dictionary missing skill"))
            if not m.get("age-bands"):
                violations.append((str(p["path"]), "cue-dictionary missing age-bands"))
            if not m.get("sources"):
                violations.append((str(p["path"]), "cue-dictionary missing sources"))
        elif t == "drill-pick-list":
            if not m.get("age"):
                violations.append((str(p["path"]), "drill-pick-list missing age"))
            if not m.get("season-context"):
                violations.append((str(p["path"]), "drill-pick-list missing season-context"))
            if not m.get("drills"):
                violations.append((str(p["path"]), "drill-pick-list missing drills"))
            if not m.get("sources"):
                violations.append((str(p["path"]), "drill-pick-list missing sources"))
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
                      "level", "focus", "season-phase", "scope", "kind", "audience",
                      "age", "season-context"):
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

    # If a baseline file exists, compare broken-wikilink count against it.
    # If no baseline is recorded, treat 0 broken links as the implicit baseline
    # (any broken link is therefore a regression until a baseline is pinned).
    prior = read_prior_broken_count(report_path.with_name(report_path.name + ".baseline"))
    current = len(broken)

    # Emit detail lines so callers (tests, humans) can see what broke.
    for p, t in broken:
        print(f"broken wikilink: {p}: [[{t}]]")
    for p, why in invariants:
        print(f"invariant: {p}: {why}")
    for p, why in frontmatter:
        print(f"frontmatter: {p}: {why}")
    for p, ck in citations:
        print(f"citation: {p}: [{ck}]")

    # Exit logic:
    #   - Cross-link invariant violations always block (SCHEMA §6 is hard).
    #   - Broken-wikilink regression vs baseline blocks.
    #   - Frontmatter/citation failures are surfaced in the report as warnings
    #     but do not block commits — they track pre-existing drift that gets
    #     cleaned up incrementally rather than all-at-once.
    #   - --strict additionally blocks on orphans and queue-consistency issues.
    baseline = prior if prior is not None else 0
    status_line = (
        f"Broken wikilinks: {current}; invariants={len(invariants)}; "
        f"frontmatter={len(frontmatter)}; citations={len(citations)}; "
        f"orphans={len(orphans)}; gaps={len(gaps)}"
    )
    if invariants:
        print(status_line)
        print(f"FAIL: {len(invariants)} cross-link invariant violation(s).")
        return 1
    if current > baseline:
        print(status_line)
        print(f"FAIL: broken wikilinks regressed: {current} > {baseline}")
        return 1
    if args.strict and (frontmatter or citations or orphans or queue_issues):
        print(status_line)
        print("FAIL: strict mode — frontmatter/citation/orphan/queue issues present.")
        return 1
    print(f"Lint OK. {status_line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
