# Club Coaching Manual Webapp — Design Spec

**Date:** 2026-04-25 (initiated; deploy-execution date 2026-04-26)
**Owner:** Song Mu
**Predecessor specs:** `docs/superpowers/specs/2026-04-25-club-coaching-manual-design.md` (the Manual content this webapp renders)

---

## 1. Context

### 1.1 Why this work

The Club Coaching Standards Manual (~1100 wiki pages including 9 age-guides, 8 cue dictionaries, 9 drill pick-lists, 10 tryout rubrics, 25 practice plans, 23 ops docs) currently lives as Obsidian-readable markdown. Song's coaching staff needs a webapp form factor: mobile-friendly, filterable, printable, and shareable via URL — so that an assistant coach can pull up the 14s tryout rubric on a phone during tryouts and a head coach can find a 12-minute mid-season blocking drill in 10 seconds during practice planning.

### 1.2 Stance

**Option B + Audience 2** (per 2026-04-25 brainstorm):
- Documentation rendering of every wiki page **plus** filterable interactive catalogs for drills and rubrics (the load-bearing utility for staff use)
- Public-but-unindexed (anyone with the link can read; `/robots.txt` blocks search engines)
- Hosted on **GitHub Pages** under the `musint` GitHub account
- Site URL: `https://musint.github.io/volleyball-coaching-bible/`

### 1.3 Wiki repo as source of truth

The webapp reads `wiki/` directly. No content duplication. Edits in Obsidian → `git push` → Vercel-style auto-rebuild via GitHub Actions → live in ~60–90 seconds.

---

## 2. Scope

### 2.1 Deliverable matrix

| Bucket | Output | Notes |
|---|---|---|
| Astro project | `webapp/` directory (config, src, package.json) | Reads from `../wiki/` |
| TypeScript content collections | One Zod schema per page type from SCHEMA.md | Drills, age-guides, cue-dicts, drill-picks, tryout-rubrics, practice-plans, ops-docs, coaches, schools, techniques, systems, sources |
| Wikilink resolution | remark plugin converting `[[slug]]` → `<a href="/<resolved>">` | Build-time |
| Page templates | DefaultLayout + ManualLayout + PrintLayout | Mobile-first |
| Drill catalog | Filterable React/Preact island | Multi-axis: skill, phase, levels, duration, team-size |
| Tryout-rubric viewer | Per-age 8×5 grid + Print button + Copy-as-CSV | Print stylesheet → 1 page |
| Cue dictionary lookup | Skill × subskill table with age-band toggles | Pure HTML + small JS |
| Search | Pagefind static-built index | Site-wide |
| GitHub Actions deploy | `.github/workflows/deploy-webapp.yml` | Build + deploy on push to main |
| Repo hygiene | `.gitignore` + `git filter-repo` history rewrite | Excludes `raw/articles/` + Munciana transcript |
| GH Pages config | Pages from Actions; custom-domain optional later | `https://musint.github.io/volleyball-coaching-bible/` |

### 2.2 Non-goals (deferred to v2)

- **Practice-plan composer** (drag drills onto a 90-min canvas) — Option C territory
- **Authentication / private user accounts** — public-but-unindexed is the v1 access model
- **Athlete- or parent-facing portals** with role-based content masking
- **PWA / offline support** — nice-to-have; v2
- **Comments / collaboration** — out of scope
- **Internal API for live updates** — v2 if usage demands it; v1 rebuilds on `git push`
- **Custom domain** — start at `musint.github.io/volleyball-coaching-bible/`; can add custom domain later via repo settings without redeploy

---

## 3. Tech stack

**Astro 4.x** with:
- `@astrojs/mdx` for richer markdown if needed (optional)
- `@astrojs/sitemap` for `sitemap.xml` (we'll exclude search engines via `robots.txt` but still build the sitemap for direct nav)
- `@astrojs/preact` (or React) for interactive islands
- `tailwindcss` for styling
- Content collections (Astro built-in) typed via Zod schemas mirroring SCHEMA.md
- `remark-wiki-link` (or custom remark plugin) for `[[slug]]` resolution
- `pagefind` for static-time search indexing
- TypeScript end-to-end

**Hosting:** GitHub Pages via Actions (`actions/deploy-pages@v4`).

**No backend.** Pure static site. Frontmatter-driven catalogs ship as JSON loaded by the filter island.

### 3.1 Why Astro vs alternatives

- **VitePress** — Vue-only, less flexible for the interactive filter component
- **Next.js** — overkill for a static content site; SSR/ISR features unused
- **Eleventy** — pre-2024-era; Astro is strictly better for typed content + islands
- **MkDocs Material** — purpose-built for docs but inflexible; harder to add the drill-catalog filter UI
- **Docusaurus** — React-based, fine, but Astro's content collections + islands model is cleaner for our use case

---

## 4. Architecture

### 4.1 Content pipeline

```
wiki/                              ← source of truth (unchanged)
  age-guides/*.md
  cues/*.md, cues.md
  drill-picks/*.md
  drills/*.md
  ops/*.md
  practice-plans/*.md
  schools/*.md, coaches/*.md, ...

webapp/
  astro.config.mjs                 ← site: 'https://musint.github.io', base: '/volleyball-coaching-bible/'
  src/
    content/
      config.ts                    ← Zod schemas per page type
    pages/
      [...slug].astro              ← catch-all, resolves any wiki/*.md URL
      index.astro                  ← landing
      manual/index.astro
      drills/index.astro           ← filterable catalog
      drills/[skill].astro         ← skill-pre-filtered
      coaches/index.astro
      schools/index.astro
      search.astro                 ← Pagefind UI
    components/
      DrillCatalog.astro           ← server-rendered table + island controls
      FilterSidebar.tsx            ← client-side island (Preact)
      AgeLadder.astro              ← 10s → 18s nav
      CueLookup.astro
      WikilinkRenderer.astro       ← consumes remark-resolved links
      PromotionCriteria.astro
      RubricGrid.astro
      PrintButton.astro
    layouts/
      DefaultLayout.astro
      ManualLayout.astro
      PrintLayout.astro
    styles/
      global.css                   ← Tailwind base + custom
      print.css                    ← media print rules
    lib/
      slug-resolver.ts             ← shared wikilink resolution
      filter-types.ts              ← typed filter state
  public/
    favicon.svg
    robots.txt                     ← Disallow: /
  package.json
  tsconfig.json
  .github/workflows/
    deploy-webapp.yml              ← build + deploy on push to main
```

### 4.2 Content collection schemas

Each SCHEMA.md page type gets a Zod schema in `webapp/src/content/config.ts`. Example:

```ts
import { defineCollection, z } from 'astro:content';

const drill = defineCollection({
  type: 'content',
  schema: z.object({
    type: z.literal('drill'),
    name: z.string(),
    'primary-skill': z.enum(['passing','setting','hitting','blocking','serving','defense','transition']),
    'secondary-skills': z.array(z.string()).optional(),
    techniques: z.array(z.string()).min(1),
    phase: z.enum(['warm-up','skill','strategic','competition','conditioning']),
    'team-size-min': z.number().int(),
    'team-size-max': z.number().int(),
    'duration-min': z.number().int(),
    levels: z.array(z.enum(['14u','hs','college'])),
    equipment: z.array(z.string()),
    sources: z.array(z.string()).min(1),
  }),
});

const ageGuide = defineCollection({ /* ... */ });
const cueDictionary = defineCollection({ /* ... */ });
const drillPickList = defineCollection({ /* ... */ });
const opsDoc = defineCollection({ /* ... */ });
const practicePlan = defineCollection({ /* ... */ });
const coach = defineCollection({ /* ... */ });
const school = defineCollection({ /* ... */ });
const technique = defineCollection({ /* ... */ });
const system = defineCollection({ /* ... */ });
const source = defineCollection({ /* ... */ });

export const collections = {
  drill, ageGuide, cueDictionary, drillPickList,
  opsDoc, practicePlan, coach, school, technique, system, source,
};
```

Each collection's content directory is configured in the same file to point at the corresponding `wiki/<folder>/`.

### 4.3 Wikilink resolution

Custom remark plugin in `webapp/src/lib/remark-wikilink.ts` walks the AST. For each `[[slug]]`:
1. Look up the slug across all collections (drills, coaches, schools, age-guides, cues, ops, practice-plans, techniques, systems, sources)
2. If found, replace with `<a href="/<base>/<resolved-path>">`
3. If not found, render as plain text + add a build-time warning (does not fail the build; matches lint's "broken wikilink" behavior)

Slug → URL mapping: every page lives at a stable URL derived from its file path under `wiki/`. E.g., `wiki/age-guides/14s.md` → `/volleyball-coaching-bible/age-guides/14s/`.

### 4.4 Drill catalog (the headline feature)

**`/drills/`** route:
- Server-rendered HTML table of all 101 drills with frontmatter columns (name, skill, phase, duration, levels, team-size)
- Astro Island (`FilterSidebar.tsx`, Preact) hydrates on the client
- Filter state stored in URL query params for bookmarkable filters: `?skill=passing&phase=skill&levels=14u&maxDuration=10`
- Filter axes: primary-skill (multi-select), secondary-skills (multi-select), phase (multi-select), levels (multi-select), duration min/max sliders, team-size range, equipment (multi-select), sources (multi-select)
- Sort options: alphabetical, duration ascending, phase ordering
- Click a drill row → drill detail page at `/drills/<slug>/`

**`/drills/<skill>/`** routes (auto-generated): pre-filtered views like `/drills/passing/`, `/drills/blocking/`. Same filter UI, just with `skill` pre-selected.

### 4.5 Tryout-rubric viewer

**`/manual/tryouts/<age>/`** route per rubric (10s through 18u + college-walkon):
- Renders the 8×5 evaluation grid as a styled HTML table with subtle row alternation
- "Print this rubric" button triggers `window.print()` with the print stylesheet → single-page output
- "Copy as CSV" button serializes the rubric for clipboard paste into a stat-tracker
- Cross-link to corresponding age-guide for context

### 4.6 Cue dictionary lookup

**`/manual/cues/`** hub + per-skill `/manual/cues/<skill>/` pages:
- Skill hub lists all 7 skill cue dictionaries with one-line summaries
- Per-skill page renders all subskills with their canonical cues + age-band tags
- Toggle filter: "show only cues introduced at <age>" — quickly scopes the page to "what should I be saying at 12s?"

### 4.7 Practice-plan rendering

**`/manual/practice-plans/<slug>/`** routes:
- Macrocycles, microcycles, single-session plans all render with structured time-block sections
- Drill wikilinks expand to inline drill-card on hover/tap (drill name + setup snippet + duration)
- Print stylesheet → printable plan that fits a single 8.5×11 sheet

### 4.8 Search

Pagefind. Static-time index built from all rendered pages. `/search/` route hosts the search UI. Returns ranked results with frontmatter-tag faceting.

---

## 5. Navigation + page structure

### 5.1 Top nav (desktop)

`Home / Manual / Library / Drills / Coaches / Schools / Search`

### 5.2 Mobile bottom tabs

`Manual / Drills / Coaches / Search` (the four highest-frequency entry points)

### 5.3 Manual section structure

Sticky sidebar with the four-question loop:
```
Manual
├── Age-guides (10s → 18s ladder)
├── Cue dictionary (7 skills + hub)
├── Drill pick-lists (per-age)
├── Tryout rubrics (per-age + college walk-on)
├── Practice plans
│   ├── Macrocycles (5)
│   ├── Microcycles (5)
│   └── Single-session (15)
└── Operations
    ├── Match prep (5)
    └── Club ops (8)
```

### 5.4 Library section structure

```
Library
├── Skill hubs (passing, setting, hitting, blocking, serving, defense, transition)
├── Techniques (25 pages, organized by skill)
├── Positions (6 pages)
├── Systems (18 pages, organized by category)
├── Hubs (philosophy, practice-planning, season-planning, mental, physical, match-prep, rules, recruiting)
└── Age-lenses (14U, HS, college — the older/coarser version of age-guides; cross-link)
```

### 5.5 Coaches + Schools

Grid layout grouped by country/tradition. Click → coach/school page.

---

## 6. Build + deploy

### 6.1 Local dev

```bash
cd webapp
npm install
npm run dev   # http://localhost:4321/volleyball-coaching-bible/
```

Hot reload on edits to either the webapp/ source or the wiki/ markdown.

### 6.2 GitHub Actions deploy

`.github/workflows/deploy-webapp.yml`:

```yaml
name: Deploy webapp to GitHub Pages
on:
  push:
    branches: [main]
    paths:
      - 'webapp/**'
      - 'wiki/**'
      - '.github/workflows/deploy-webapp.yml'
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: pages
  cancel-in-progress: false
jobs:
  build:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: webapp
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
          cache-dependency-path: webapp/package-lock.json
      - run: npm ci
      - run: npm run build
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: webapp/dist
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

### 6.3 GitHub Pages settings

Repo settings → Pages → Source: **GitHub Actions** (not "Deploy from a branch"). The workflow above handles everything.

### 6.4 Robots / indexing

`webapp/public/robots.txt`:
```
User-agent: *
Disallow: /
```

This keeps the site public-but-unindexed. Anyone with the URL can read; search engines won't return it as a result.

---

## 7. Repo hygiene

### 7.1 Privacy-sensitive paths to exclude

- `raw/articles/` — ~600 extracted article texts (mostly AOC). Public exposure of verbatim article text exceeds typical fair-use comfort
- `raw/transcripts/munciana-2022-camp-drills.md` — Mike Lingenfelter's internal staff training video transcript; private
- `Munciana Drills/` (already gitignored — 1.35 GB MP4)

### 7.2 Mechanics

1. Backup the local repo to `vba/bible.backup/` (full `cp -r`)
2. Update `.gitignore` to add `raw/articles/` and `raw/transcripts/munciana-2022-camp-drills.md`
3. Run `git filter-repo --invert-paths --path raw/articles --path raw/transcripts/munciana-2022-camp-drills.md --force` to remove from history
4. Verify the rewrite produced sane history
5. Create the public repo: `gh repo create musint/volleyball-coaching-bible --public --description "LLM-maintained volleyball coaching standards manual" --source . --remote origin --disable-issues --disable-wiki`
6. Push: `git push -u origin main`
7. Configure GH Pages source = GitHub Actions
8. Verify deployment lands at `https://musint.github.io/volleyball-coaching-bible/`

### 7.3 Going forward

`raw/articles/` and the Munciana transcript stay local-only. The wiki references them via `raw-file:` frontmatter, but the rendered site doesn't need them — only the metadata + the interpreted content (which lives in `wiki/sources/`).

---

## 8. Success criteria

### 8.1 Acceptance checklist

Webapp v1 complete when:

- [ ] `webapp/` directory exists with Astro project + Tailwind + Preact
- [ ] Content collections schemas exist for all 11 page types from SCHEMA.md
- [ ] Wikilink remark plugin resolves `[[slug]]` to real URLs (or graceful fallback)
- [ ] Catch-all `[...slug].astro` renders any wiki page at its derived URL
- [ ] Drill catalog at `/drills/` filters by skill / phase / levels / duration / team-size with URL state
- [ ] Tryout rubric pages render the 8×5 grid + print button
- [ ] Cue dictionary pages render with age-band toggles
- [ ] Practice-plan pages render with drill cross-links
- [ ] Pagefind search lands at `/search/`
- [ ] Mobile responsive (Tailwind breakpoints; verified on 375px width)
- [ ] Print stylesheet works for tryout rubrics + practice plans
- [ ] `/robots.txt` blocks search engines
- [ ] `git filter-repo` cleans `raw/articles/` and `raw/transcripts/munciana-2022-camp-drills.md` from history
- [ ] `musint/volleyball-coaching-bible` public repo exists
- [ ] GitHub Actions workflow deploys on push
- [ ] Live site responds at `https://musint.github.io/volleyball-coaching-bible/`
- [ ] All scenario tests in §8.2 pass

### 8.2 Scenario tests

Three real workflows the webapp must handle cleanly:

1. **"Find a 12-minute mid-season blocking drill suitable for 14U"** — Open `/drills/`, filter `phase=skill, primary-skill=blocking, levels=14u, maxDuration=12`, get a result table in <2 seconds.
2. **"Print the 16U tryout rubric for tomorrow"** — Open `/manual/tryouts/16u/`, click Print, get a clean 1-page printable rubric.
3. **"What's the canonical Munciana cue for forearm passing at 12s?"** — Search "forearm pass cue 12s" in `/search/`, land on `/manual/cues/passing/`, see the 12s-banded cue immediately.

### 8.3 Performance budget

- First Contentful Paint < 1.5s on 4G mobile
- Initial HTML payload < 50KB per page
- Pagefind index < 500KB total (lazy-chunked)
- No render-blocking JS on the catch-all content pages
- Filter island hydrates < 200ms

---

## 9. Open items & caveats

1. **Custom domain.** Defaults to `musint.github.io/volleyball-coaching-bible/`. A custom domain (e.g., `coachingbible.com` or similar) can be added later via the repo's `CNAME` file + DNS without redeploy.
2. **`raw/research/`, `raw/usav/`, `raw/instagram/`, `raw/books/` are pushed publicly.** They contain abstracts, public USAV materials, login-walled IG profile snapshots, and the user's synthesized book notes — all judged safe. If any of these turn out to be more sensitive than expected, we add them to `.gitignore` + run `filter-repo` again.
3. **Sitemap exclusion.** The Astro sitemap plugin generates `sitemap-index.xml` regardless of `robots.txt`. Acceptable since direct URLs are already public; just won't be discovered via search.
4. **Future v2 candidates.** Practice-plan composer (drag-and-drop drills onto a 90-min canvas); athlete-facing or parent-facing portal with role-based content; PWA / offline support; comments/collaboration.
5. **Lint-on-build.** The webapp build does not run the wiki lint script. We could add it as a pre-build step in the GH Actions workflow to fail deploys on broken wikilinks; deferred.
6. **Pagefind on filtered routes.** Pagefind indexes the rendered HTML, so the catch-all content pages are searchable but the dynamic filter results inside `/drills/` aren't (since they're constructed client-side). The drill *pages* themselves are searchable; that covers the use case.

---

## 10. Next step

Hand off to the writing-plans skill to produce a task-by-task implementation plan covering: repo hygiene → Astro scaffolding → content collections → wikilink plugin → drill catalog → cue dictionary + tryout viewer + practice-plan renderer → search → mobile + print stylesheets → GitHub Actions deploy → live verification.
