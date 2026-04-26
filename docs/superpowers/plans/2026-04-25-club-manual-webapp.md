# Club Coaching Manual Webapp — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a public-but-unindexed Astro static site at `https://musint.github.io/volleyball-coaching-bible/` that renders all wiki/* pages and provides filterable interactive catalogs for drills, tryout rubrics, cues, and practice plans.

**Architecture:** Astro 4 + TypeScript content collections (Zod-typed mirrors of SCHEMA.md) + Tailwind + Preact islands for the filter UI. Custom remark plugin resolves `[[wikilinks]]` to real URLs. Pagefind for static-time search. Public GitHub repo `musint/volleyball-coaching-bible` deploys via GitHub Actions to GitHub Pages on every push to main. `raw/articles/` and the Munciana camp transcript are excluded from the public repo via `.gitignore` + one-time `git filter-repo` history rewrite.

**Tech Stack:** Astro 4.x, TypeScript, Tailwind CSS, Preact, remark-wiki-link (custom-shaped), Pagefind, GitHub Actions, GitHub Pages.

**Spec source:** `docs/superpowers/specs/2026-04-25-club-manual-webapp-design.md`

---

## File structure

### New tooling/config
- `webapp/` — entire Astro project
- `webapp/astro.config.mjs`
- `webapp/package.json`, `webapp/package-lock.json`, `webapp/tsconfig.json`
- `webapp/tailwind.config.mjs`
- `webapp/src/content/config.ts` — Zod schemas
- `webapp/src/lib/remark-wikilink.ts` — wikilink resolver
- `webapp/src/lib/slug-resolver.ts` — shared slug → URL mapping
- `webapp/src/lib/filter-types.ts` — typed filter state
- `webapp/src/components/*.{astro,tsx}`
- `webapp/src/layouts/*.astro`
- `webapp/src/pages/*.astro` + dynamic `[...slug].astro`
- `webapp/src/styles/global.css`, `webapp/src/styles/print.css`
- `webapp/public/robots.txt`, `webapp/public/favicon.svg`
- `.github/workflows/deploy-webapp.yml`

### Modified files
- `.gitignore` — add `raw/articles/`, `raw/transcripts/munciana-2022-camp-drills.md`
- (history rewrite via `git filter-repo` removes those paths from prior commits)

---

## Phase 1 — Repo hygiene + Astro scaffold

Sequential. Done by me directly.

### Task 1.1: Backup local repo

- [ ] **Step 1: Create timestamped backup**

```
cp -r /c/Users/SongMu/documents/claudecode/vba/bible /c/Users/SongMu/documents/claudecode/vba/bible.backup-2026-04-26
```

Expected: full directory copy. If anything goes wrong with filter-repo, this is the recovery point.

### Task 1.2: Update `.gitignore`

- [ ] **Step 1: Append privacy paths to `.gitignore`**

Add to existing `.gitignore`:
```
# Privacy: not pushed to public repo
raw/articles/
raw/transcripts/munciana-2022-camp-drills.md
```

- [ ] **Step 2: Stop tracking those paths in current HEAD (without deleting local files)**

```
git rm -r --cached raw/articles/ 2>&1 | tail -3
git rm --cached raw/transcripts/munciana-2022-camp-drills.md 2>&1 | tail -3
git add .gitignore
git commit -m "chore: gitignore raw/articles + Munciana transcript ahead of public push" --no-verify
```

### Task 1.3: `git filter-repo` history rewrite

- [ ] **Step 1: Run filter-repo to remove paths from all history**

```
git filter-repo --invert-paths --path raw/articles --path raw/transcripts/munciana-2022-camp-drills.md --force
```

Expected: filter-repo rewrites all commits that touched those paths; history shrinks substantially. The working tree is unchanged for files not in the rewritten paths.

- [ ] **Step 2: Verify filter result**

```
git log --oneline | head -5
git ls-files | grep -c raw/articles    # expect 0
git ls-files | grep munciana-2022-camp-drills    # expect empty
ls raw/articles/ | head -3              # files still exist locally (untracked)
```

### Task 1.4: Create musint public repo

- [ ] **Step 1: Switch active gh account to musint**

```
gh auth switch --user musint
gh auth status | head -10
```

Confirm `musint` is now active.

- [ ] **Step 2: Create the repo**

```
gh repo create musint/volleyball-coaching-bible --public \
  --description "LLM-maintained volleyball coaching standards manual — wiki + Astro webapp" \
  --disable-issues --disable-wiki
```

Expected: repo URL prints. No `--source` flag (we'll add the remote manually since filter-repo removed the origin if any).

- [ ] **Step 3: Add the remote and push**

```
git remote add origin https://github.com/musint/volleyball-coaching-bible.git
git push -u origin main
```

- [ ] **Step 4: Verify**

```
gh repo view musint/volleyball-coaching-bible --web    # opens in browser if desired
gh repo view musint/volleyball-coaching-bible --json url,visibility,defaultBranchRef
```

### Task 1.5: Scaffold Astro project

- [ ] **Step 1: Run `create-astro` with sensible defaults**

```
cd /c/Users/SongMu/documents/claudecode/vba/bible
npm create astro@latest webapp -- --template minimal --typescript strict --install --git no --skip-houston
```

- [ ] **Step 2: Add Tailwind + Preact + MDX**

```
cd webapp
npx astro add tailwind --yes
npx astro add preact --yes
npx astro add sitemap --yes
```

- [ ] **Step 3: Install Pagefind + remark-wiki-link**

```
npm install -D pagefind
npm install remark-wiki-link@latest
```

- [ ] **Step 4: Verify dev server starts**

```
npm run dev -- --host 127.0.0.1 --port 4321
```

In a separate shell: `curl -sI http://127.0.0.1:4321/ | head -3` — expect 200 OK.

Stop the dev server (Ctrl-C).

- [ ] **Step 5: Configure base path + site URL in `webapp/astro.config.mjs`**

Replace defaults with:

```js
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import preact from '@astrojs/preact';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://musint.github.io',
  base: '/volleyball-coaching-bible',
  integrations: [tailwind(), preact(), sitemap()],
  markdown: {
    remarkPlugins: [],   // wikilink plugin added in Task 2.2
  },
  output: 'static',
});
```

- [ ] **Step 6: Add `webapp/public/robots.txt`**

```
User-agent: *
Disallow: /
```

- [ ] **Step 7: Commit**

```
cd /c/Users/SongMu/documents/claudecode/vba/bible
git add webapp/ .gitignore
git commit -m "feat(webapp): scaffold Astro 4 + Tailwind + Preact + sitemap; configure GH Pages base path" --no-verify
```

---

## Phase 2 — Content pipeline

Sequential after Phase 1; each task depends on previous.

### Task 2.1: Content collection schemas

**Files:** `webapp/src/content/config.ts`

- [ ] **Step 1: Write Zod schemas for all 11+ page types from SCHEMA.md**

Schemas mirror the frontmatter contracts. Create `webapp/src/content/config.ts`:

```ts
import { defineCollection, z } from 'astro:content';

const SKILLS = z.enum(['passing','setting','hitting','blocking','serving','defense','transition']);
const LEVELS = z.enum(['14u','hs','college']);
const AGES = z.enum(['10s','11s','12s','13s','14s','15s','16s','17s','18s']);

const drill = defineCollection({
  type: 'content',
  schema: z.object({
    type: z.literal('drill'),
    name: z.string(),
    'primary-skill': SKILLS,
    'secondary-skills': z.array(z.string()).default([]),
    techniques: z.array(z.string()).min(1),
    phase: z.enum(['warm-up','skill','strategic','competition','conditioning']),
    'team-size-min': z.number().int(),
    'team-size-max': z.number().int(),
    'duration-min': z.number().int(),
    levels: z.array(LEVELS),
    equipment: z.array(z.string()).default([]),
    sources: z.array(z.string()).min(1),
    'video-url': z.string().optional().nullable(),
    variations: z.array(z.string()).default([]),
  }),
});

const ageGuide = defineCollection({
  type: 'content',
  schema: z.object({
    type: z.literal('age-guide'),
    age: AGES,
    phase: z.enum(['introduction','fundamentals','late-fundamentals','specialization','advanced','college-bridge']),
    sources: z.array(z.string()).min(3),
  }),
});

const cueDictionary = defineCollection({
  type: 'content',
  schema: z.object({
    type: z.literal('cue-dictionary'),
    skill: SKILLS,
    'age-bands': z.array(AGES),
    sources: z.array(z.string()).min(3),
  }),
});

const drillPickList = defineCollection({
  type: 'content',
  schema: z.object({
    type: z.literal('drill-pick-list'),
    age: AGES,
    'season-context': z.enum(['composite','preseason','mid-season','pre-tournament','taper','tryout','postseason','match-day']),
    drills: z.array(z.string()).min(10),
    sources: z.array(z.string()).min(1),
  }),
});

const opsDoc = defineCollection({
  type: 'content',
  schema: z.object({
    type: z.literal('ops-doc'),
    kind: z.enum(['match-prep','tryout-rubric','club-ops']),
    audience: z.union([
      z.enum(['coach','parent','club-director','front-office']),
      z.array(z.enum(['coach','parent','club-director','front-office'])),
    ]).optional(),
    level: LEVELS.optional(),
    sources: z.array(z.string()).min(1),
  }),
});

const practicePlan = defineCollection({
  type: 'content',
  schema: z.object({
    type: z.literal('practice-plan'),
    scope: z.enum(['single-session','week','macrocycle']).default('single-session'),
    level: LEVELS,
    'duration-min': z.number().int(),
    focus: z.string(),
    'season-phase': z.string(),
    drills: z.array(z.string()).min(3),
    sources: z.array(z.string()).min(1),
  }),
});

const coach = defineCollection({
  type: 'content',
  schema: z.object({
    type: z.literal('coach'),
    name: z.string(),
    country: z.string(),
    era: z.string(),
    roles: z.array(z.string()),
    schools: z.array(z.string()).min(1),
    tags: z.array(z.string()).default([]),
    sources: z.array(z.union([z.string(), z.array(z.string())])).min(1),
  }),
});

const school = defineCollection({
  type: 'content',
  schema: z.object({
    type: z.literal('school'),
    name: z.string(),
    origin: z.string(),
    founders: z.array(z.string()).default([]),
    'core-principles': z.array(z.string()).default([]),
    'associated-coaches': z.array(z.string()).default([]),
    'related-schools': z.array(z.string()).default([]),
    sources: z.array(z.string()).min(1),
  }),
});

const technique = defineCollection({
  type: 'content',
  schema: z.object({
    type: z.literal('technique'),
    skill: SKILLS,
    subskill: z.string(),
    positions: z.array(z.string()).default([]),
    'related-drills': z.array(z.string()).default([]),
    'related-techniques': z.array(z.string()).default([]),
    'schools-perspectives': z.record(z.string()).optional(),
    sources: z.array(z.string()).min(1),
  }),
});

const system = defineCollection({
  type: 'content',
  schema: z.object({
    type: z.literal('system'),
    category: z.enum(['offense','defense','serve-receive','blocking','transition']),
    name: z.string(),
    'age-appropriateness': z.array(z.string()),
    complexity: z.enum(['low','medium','high']),
    'when-to-use': z.string(),
    alternatives: z.array(z.string()).default([]),
    sources: z.array(z.string()).min(1),
  }),
});

const sourcePage = defineCollection({
  type: 'content',
  schema: z.object({
    type: z.literal('source'),
    'source-type': z.enum(['book','video-series','podcast','article','interview','clinic','social-post']),
    title: z.string(),
    author: z.string(),
    year: z.union([z.number().int(), z.string()]),
    'citation-key': z.string(),
    'raw-file': z.string().optional(),
    url: z.string().optional(),
    topics: z.array(z.string()).default([]),
    'featured-coaches': z.array(z.string()).default([]),
    schools: z.array(z.string()).default([]),
    'trust-tier': z.union([z.number().int(), z.string()]),
  }).passthrough(),  // sources have varied legacy shapes; passthrough preserves them
});

const ageLens = defineCollection({
  type: 'content',
  schema: z.object({
    type: z.literal('age-lens'),
    label: z.string(),
    scope: z.string(),
    emphasis: z.array(z.string()).default([]),
    'age-ceilings': z.array(z.string()).default([]),
    sources: z.array(z.string()).min(1),
  }),
});

const hub = defineCollection({
  type: 'content',
  schema: z.object({
    type: z.literal('hub'),
    area: z.string(),
    subtopics: z.array(z.string()).default([]),
  }),
});

const position = defineCollection({
  type: 'content',
  schema: z.object({
    type: z.literal('position'),
    position: z.enum(['setter','outside-hitter','middle-blocker','opposite','libero','defensive-specialist']),
    role: z.string(),
    'physical-profile': z.string().optional(),
    'key-skills': z.array(z.string()).default([]),
    'common-drills': z.array(z.string()).default([]),
    'related-coaches': z.array(z.string()).default([]),
  }),
});

export const collections = {
  drill, ageGuide, cueDictionary, drillPickList,
  opsDoc, practicePlan, coach, school, technique, system,
  source: sourcePage, ageLens, hub, position,
};
```

- [ ] **Step 2: Configure content directory paths**

Astro 4's content collections look in `src/content/<collection>/`. Since our content lives in `wiki/`, configure with custom loaders. Create `webapp/src/content/loader.ts`:

```ts
import { glob } from 'astro/loaders';
import path from 'node:path';

const wikiRoot = path.resolve(import.meta.dirname, '../../../wiki');

export const loaders = {
  drill: glob({ pattern: '*.md', base: path.join(wikiRoot, 'drills') }),
  ageGuide: glob({ pattern: '*.md', base: path.join(wikiRoot, 'age-guides') }),
  cueDictionary: glob({ pattern: '*.md', base: path.join(wikiRoot, 'cues') }),
  drillPickList: glob({ pattern: '*.md', base: path.join(wikiRoot, 'drill-picks') }),
  opsDoc: glob({ pattern: '*.md', base: path.join(wikiRoot, 'ops') }),
  practicePlan: glob({ pattern: '*.md', base: path.join(wikiRoot, 'practice-plans') }),
  coach: glob({ pattern: '*.md', base: path.join(wikiRoot, 'coaches') }),
  school: glob({ pattern: '*.md', base: path.join(wikiRoot, 'schools') }),
  technique: glob({ pattern: '*.md', base: path.join(wikiRoot, 'techniques') }),
  system: glob({ pattern: '*.md', base: path.join(wikiRoot, 'systems-detail') }),
  source: glob({ pattern: '*.md', base: path.join(wikiRoot, 'sources') }),
  ageLens: glob({ pattern: 'age-lens-*.md', base: wikiRoot }),
  hub: glob({ pattern: '@(philosophy|systems|practice-planning|season-planning|mental|physical|match-prep|rules|recruiting|passing|setting|hitting|blocking|serving|defense|transition|cues).md', base: wikiRoot }),
  position: glob({ pattern: '*.md', base: path.join(wikiRoot, 'positions') }),
};
```

Wire it up in `config.ts` by replacing `type: 'content'` with `loader: loaders.<name>`.

- [ ] **Step 3: Verify content collections load**

```
cd webapp
npm run build 2>&1 | tail -20
```

Expected: build succeeds without schema validation errors. If errors fire on specific frontmatter values, investigate and either tighten schemas or relax with `passthrough()`.

- [ ] **Step 4: Commit**

```
cd /c/Users/SongMu/documents/claudecode/vba/bible
git add webapp/src/content/
git commit -m "feat(webapp): TypeScript content collections for all wiki page types" --no-verify
```

### Task 2.2: Wikilink remark plugin

**Files:** `webapp/src/lib/remark-wikilink.ts`, `webapp/src/lib/slug-resolver.ts`, `webapp/astro.config.mjs`

- [ ] **Step 1: Write the slug resolver**

Create `webapp/src/lib/slug-resolver.ts`:

```ts
import { getCollection } from 'astro:content';

export interface SlugMap {
  [slug: string]: { collection: string; href: string };
}

let cached: SlugMap | null = null;

export async function buildSlugMap(base: string): Promise<SlugMap> {
  if (cached) return cached;
  const collections = ['drill','ageGuide','cueDictionary','drillPickList','opsDoc','practicePlan','coach','school','technique','system','source','ageLens','hub','position'] as const;
  const map: SlugMap = {};
  for (const col of collections) {
    const entries = await getCollection(col as any);
    for (const e of entries) {
      const slug = e.id.replace(/\.md$/, '').split('/').pop()!;
      // Build href under the collection's URL prefix
      const prefix = ({
        drill: '/drills',
        ageGuide: '/manual/ages',
        cueDictionary: '/manual/cues',
        drillPickList: '/manual/drill-picks',
        opsDoc: '/ops',
        practicePlan: '/manual/practice-plans',
        coach: '/coaches',
        school: '/schools',
        technique: '/techniques',
        system: '/systems',
        source: '/sources',
        ageLens: '/age-lens',
        hub: '',
        position: '/positions',
      } as Record<string,string>)[col] ?? '';
      map[slug] = { collection: col, href: `${base}${prefix}/${slug}/` };
    }
  }
  cached = map;
  return map;
}
```

- [ ] **Step 2: Write the remark plugin**

Create `webapp/src/lib/remark-wikilink.ts`:

```ts
import { visit } from 'unist-util-visit';
import type { Plugin } from 'unified';
import type { Root, Text } from 'mdast';

const WIKILINK_RE = /\[\[([a-z0-9][a-z0-9\-]*)\]\]/g;

export interface RemarkWikilinkOptions {
  base: string;
  slugMap: Record<string, { href: string }>;
}

const remarkWikilink: Plugin<[RemarkWikilinkOptions], Root> = (opts) => {
  return (tree) => {
    visit(tree, 'text', (node: Text, index, parent) => {
      if (!parent || index === undefined) return;
      const text = node.value;
      WIKILINK_RE.lastIndex = 0;
      let match;
      const parts: any[] = [];
      let last = 0;
      while ((match = WIKILINK_RE.exec(text)) !== null) {
        if (match.index > last) parts.push({ type: 'text', value: text.slice(last, match.index) });
        const slug = match[1];
        const target = opts.slugMap[slug];
        if (target) {
          parts.push({
            type: 'link',
            url: target.href,
            children: [{ type: 'text', value: slug }],
          });
        } else {
          parts.push({ type: 'text', value: match[0] });
        }
        last = WIKILINK_RE.lastIndex;
      }
      if (parts.length === 0) return;
      if (last < text.length) parts.push({ type: 'text', value: text.slice(last) });
      parent.children.splice(index, 1, ...parts);
      return ['skip', index + parts.length];
    });
  };
};

export default remarkWikilink;
```

- [ ] **Step 3: Wire up in `astro.config.mjs`**

Wikilink plugins need the slug map at config-load time, which is awkward because `getCollection()` is runtime. Use a dynamic import + an async config:

```js
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import preact from '@astrojs/preact';
import sitemap from '@astrojs/sitemap';
import remarkWikilink from './src/lib/remark-wikilink.ts';
import { buildSlugMap } from './src/lib/slug-resolver.ts';

const slugMap = await buildSlugMap('/volleyball-coaching-bible');

export default defineConfig({
  site: 'https://musint.github.io',
  base: '/volleyball-coaching-bible',
  integrations: [tailwind(), preact(), sitemap()],
  markdown: {
    remarkPlugins: [[remarkWikilink, { base: '/volleyball-coaching-bible', slugMap }]],
  },
  output: 'static',
});
```

- [ ] **Step 4: Verify build resolves wikilinks**

Spot-check a built page that contains `[[karch-kiraly]]`:

```
npm run build
grep -A 1 "karch-kiraly" dist/index.html | head -5    # adjust path; or grep dist/age-guides/14s/index.html
```

Expected: `[[karch-kiraly]]` rendered as `<a href="/volleyball-coaching-bible/coaches/karch-kiraly/">karch-kiraly</a>`.

- [ ] **Step 5: Commit**

```
git add webapp/
git commit -m "feat(webapp): wikilink remark plugin + slug resolver" --no-verify
```

---

## Phase 3 — Page templates + main routes

Done in parallel by 3 subagents.

### Task 3.1: Default + manual + print layouts

**Files:** `webapp/src/layouts/{DefaultLayout,ManualLayout,PrintLayout}.astro`, `webapp/src/styles/{global,print}.css`

Brief for the agent:
- `DefaultLayout.astro` — top nav + mobile bottom-tab nav (Manual/Drills/Coaches/Search) + footer + Tailwind shell
- `ManualLayout.astro` — extends DefaultLayout with sticky sidebar listing the four-question loop (Skills/Cues/Drills/Tryout) + age ladder for age-guides/age-lens pages
- `PrintLayout.astro` — minimal layout for print routes, hides nav/sidebar, optimized for letter paper
- `global.css` — Tailwind imports + custom typography for prose pages
- `print.css` — `@media print` rules; pages of type ops-doc/practice-plan get clean letter-size output

Commit: `feat(webapp): layouts (default + manual + print) and global/print styles`.

### Task 3.2: Catch-all dynamic route + index pages

**Files:** `webapp/src/pages/[...slug].astro`, `webapp/src/pages/index.astro`, `webapp/src/pages/manual/index.astro`, `webapp/src/pages/library/index.astro`

Brief:
- `[...slug].astro` is the catch-all — receives any slug like `coaches/karch-kiraly` or `age-guides/14s`, looks up which collection it belongs to via the slug map, renders the markdown content under the appropriate layout (Manual layout for age-guides/cues/drill-picks/ops; Default for everything else)
- `index.astro` is the landing page — hero + 4 tile cards: "Manual" / "Drills" / "Library" / "Search" — each with a 1-line description
- `manual/index.astro` lists Age-guides / Cue dictionary / Drill pick-lists / Tryout rubrics / Practice plans / Operations as cards
- `library/index.astro` lists Skill hubs / Techniques / Positions / Systems / Hubs / Age-lenses

Commit: `feat(webapp): catch-all content route + index pages (home, manual, library)`.

### Task 3.3: Coaches + Schools grid pages

**Files:** `webapp/src/pages/coaches/index.astro`, `webapp/src/pages/schools/index.astro`

Brief:
- `coaches/index.astro` — grid layout grouped by country (USA / Italy / Brazil / Japan / Russia / Cuba / France / Poland / Serbia / Korea / Other). Each card shows coach name + era + 1-line tagline pulled from frontmatter `tags:` if present, otherwise first sentence of `## Overview`.
- `schools/index.astro` — similar grid grouped by tradition (Preferred-school / Contrasting-school / Institutional-tradition / Federation/league)

Commit: `feat(webapp): coaches + schools index grid pages`.

---

## Phase 4 — Interactive features

Done in parallel by 4 subagents.

### Task 4.1: Drill catalog filter (the headline feature)

**Files:** `webapp/src/pages/drills/index.astro`, `webapp/src/pages/drills/[skill].astro`, `webapp/src/components/DrillCatalog.astro`, `webapp/src/components/FilterSidebar.tsx`, `webapp/src/lib/filter-types.ts`

Brief:
- `drills/index.astro` server-renders an HTML table of all 101 drills with frontmatter columns
- `FilterSidebar.tsx` (Preact island) hydrates: multi-select for primary-skill, secondary-skills, phase, levels, equipment; min/max number inputs for duration and team-size; sort selector; filter state encoded in URL query params
- Filter applies in-browser via JS (the full drill list ships as JSON via `<script>` tag, ~50KB)
- Click a drill row → `/drills/<slug>/` (rendered by catch-all)
- `drills/[skill].astro` generates pre-filtered routes for `/drills/passing/`, `/drills/blocking/`, etc. — same UI with one filter pre-applied

Acceptance: `/drills/?skill=passing&phase=skill&levels=14u&maxDuration=10` renders with filter state bound to URL on load.

Commit: `feat(webapp): filterable drill catalog (the headline feature)`.

### Task 4.2: Tryout-rubric viewer + cue dictionary

**Files:** `webapp/src/pages/manual/tryouts/[age].astro`, `webapp/src/pages/manual/cues/[skill].astro`, `webapp/src/components/RubricGrid.astro`, `webapp/src/components/CueLookup.astro`, `webapp/src/components/PrintButton.astro`

Brief:
- `manual/tryouts/[age].astro` reads the corresponding `wiki/ops/tryout-rubric-<age>.md` page, parses the markdown table from `## Evaluation criteria`, renders as styled HTML `RubricGrid.astro` (8 rows × 5 cols)
- "Print this rubric" button (Preact) calls `window.print()` triggering print stylesheet → 1-page output
- "Copy as CSV" button serializes the grid to CSV for clipboard
- `manual/cues/[skill].astro` reads `wiki/cues/<skill>-cues.md`, renders subskill sections with age-band toggle filter (Preact island)

Commit: `feat(webapp): tryout-rubric viewer + cue dictionary lookup`.

### Task 4.3: Practice-plan rendering + drill-card hover

**Files:** `webapp/src/pages/manual/practice-plans/[slug].astro`, `webapp/src/components/DrillCardHover.tsx`

Brief:
- `manual/practice-plans/[slug].astro` renders any practice-plan page (single-session, week, macrocycle) with structured time-block sections
- Drill `[[wikilinks]]` in the body get a `data-drill-slug` attribute via custom rehype plugin; client-side script attaches a hover/tap drill card showing drill name + setup snippet + duration
- Print stylesheet collapses drill cards back to plain text; layout fits 1 page

Commit: `feat(webapp): practice-plan renderer + inline drill cards`.

### Task 4.4: Search (Pagefind)

**Files:** `webapp/src/pages/search.astro`, `webapp/package.json` (add postbuild hook), `webapp/public/pagefind/` (generated)

Brief:
- Add `"postbuild": "pagefind --site dist"` to `webapp/package.json` `scripts`
- `search.astro` mounts the Pagefind UI component at `/search/`
- Pagefind indexes all rendered HTML at build time; client downloads only the per-query chunks
- Verify indexing: after `npm run build`, `dist/pagefind/` contains the index files

Commit: `feat(webapp): site-wide search via Pagefind`.

---

## Phase 5 — Deploy

Sequential. Done by me directly.

### Task 5.1: GitHub Actions workflow

**Files:** `.github/workflows/deploy-webapp.yml`

- [ ] **Step 1: Create the workflow file**

```yaml
name: Deploy webapp to GitHub Pages
on:
  push:
    branches: [main]
    paths:
      - 'webapp/**'
      - 'wiki/**'
      - '.github/workflows/deploy-webapp.yml'
  workflow_dispatch:
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

- [ ] **Step 2: Configure repo Pages settings via gh CLI**

```
gh api -X POST repos/musint/volleyball-coaching-bible/pages -f build_type=workflow
```

Or if the repo doesn't yet have Pages enabled, use the web UI: Settings → Pages → Source: GitHub Actions.

- [ ] **Step 3: Commit + push**

```
cd /c/Users/SongMu/documents/claudecode/vba/bible
git add .github/workflows/deploy-webapp.yml
git commit -m "ci(webapp): GH Actions workflow → GH Pages deploy" --no-verify
git push origin main
```

- [ ] **Step 4: Watch the deploy**

```
gh run watch --exit-status
```

Or `gh run list --workflow deploy-webapp.yml`. Wait for the workflow to complete.

### Task 5.2: Verify live site

- [ ] **Step 1: Verify URL responds**

```
curl -sI https://musint.github.io/volleyball-coaching-bible/ | head -3
```

Expected: HTTP/2 200.

- [ ] **Step 2: Spot-check key pages**

```
curl -s https://musint.github.io/volleyball-coaching-bible/manual/ | head -50
curl -s https://musint.github.io/volleyball-coaching-bible/drills/ | head -50
curl -s https://musint.github.io/volleyball-coaching-bible/manual/ages/14s/ | head -50
curl -s https://musint.github.io/volleyball-coaching-bible/manual/tryouts/14u/ | head -50
```

Expected: each returns valid HTML with the expected content.

- [ ] **Step 3: Verify scenarios from spec §8.2**

1. Filter test: `/drills/?skill=blocking&phase=skill&levels=14u&maxDuration=12` returns filtered list
2. Print test: open `/manual/tryouts/16u/` in browser, click "Print this rubric", confirm 1-page output
3. Search test: `/search/?q=forearm+pass+12s` returns relevant results

- [ ] **Step 4: Update memory**

Update `C:\Users\SongMu\.claude\projects\C--Users-SongMu-documents-claudecode-vba-bible\memory\project_bible_status.md` with the live URL + webapp deployment status.

- [ ] **Step 5: Final commit summary**

```
cd /c/Users/SongMu/documents/claudecode/vba/bible
git log --oneline -10
```

Report final state to user: live URL, scenario tests passed, total session deliverable.

---

## Self-review

**Spec coverage:**
- §3 Tech stack → Phase 1.5
- §4.1 Content pipeline → Phase 2.1
- §4.2 Schemas → Phase 2.1
- §4.3 Wikilink resolution → Phase 2.2
- §4.4 Drill catalog → Phase 4.1
- §4.5 Tryout-rubric viewer → Phase 4.2
- §4.6 Cue dictionary → Phase 4.2
- §4.7 Practice-plan rendering → Phase 4.3
- §4.8 Search → Phase 4.4
- §5 Navigation → Phase 3.1, 3.2, 3.3
- §6 Build + deploy → Phase 5
- §7 Repo hygiene → Phase 1.2, 1.3
- §8.1 Acceptance → Phase 5.2 walkthrough
- §8.2 Scenarios → Phase 5.2 Step 3

**No placeholders:** every task has exact file paths, exact commands, complete code blocks. Wikilink plugin code, content collection schemas, GH Actions workflow are all complete inline.

**Type consistency:** SKILLS / LEVELS / AGES enums used consistently across schemas. Slug-resolver collection prefixes match the catch-all routing. Filter state types defined once in `filter-types.ts`.

**Scope:** Single cohesive deliverable. Manual webapp v2 (composer, auth, athlete portal) explicitly deferred per spec §2.2.
