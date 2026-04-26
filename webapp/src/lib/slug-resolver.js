// Build-time slug → URL map for wikilink resolution.
// Walks the wiki/ tree once at config-load time and produces a flat lookup.
// Runs from astro.config.mjs which loads before content collections, so we
// scan the filesystem directly rather than going through the content API.

import { readdirSync, statSync } from 'node:fs';
import { join, relative, basename } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = fileURLToPath(new URL('.', import.meta.url));
const WIKI_ROOT = join(HERE, '..', '..', '..', 'wiki');

// Maps each top-level wiki/ folder to a URL prefix. Anything not in this map
// either lives at the root (hubs/age-lens) or is excluded.
const FOLDER_TO_PREFIX = {
  'drills': '/drills',
  'age-guides': '/manual/ages',
  'cues': '/manual/cues',
  'drill-picks': '/manual/drill-picks',
  'ops': '/ops',
  'practice-plans': '/manual/practice-plans',
  'coaches': '/coaches',
  'schools': '/schools',
  'techniques': '/techniques',
  'systems-detail': '/systems',
  'sources': '/sources',
  'positions': '/positions',
};

// Files at wiki/ root we want to expose at /<slug>/
const ROOT_INCLUDE_PATTERNS = [
  /^age-lens-(14u|hs|college)\.md$/,
  /^(philosophy|systems|practice-planning|season-planning|mental|physical|match-prep|rules|recruiting|passing|setting|hitting|blocking|serving|defense|transition|cues|mental-skills-curriculum|practice-ratios)\.md$/,
];

const ROOT_EXCLUDE = new Set(['SCHEMA.md', 'index.md', 'log.md', 'unsourced-queue.md', 'lint-report.md', 'lint-report.md.baseline']);

function walkMarkdown(dir, results = []) {
  let entries;
  try {
    entries = readdirSync(dir);
  } catch {
    return results;
  }
  for (const name of entries) {
    if (name.startsWith('.') || name === '_templates') continue;
    const full = join(dir, name);
    const stat = statSync(full);
    if (stat.isDirectory()) {
      walkMarkdown(full, results);
    } else if (name.endsWith('.md')) {
      results.push(full);
    }
  }
  return results;
}

export async function buildSlugMap(base) {
  const map = {};
  const files = walkMarkdown(WIKI_ROOT);
  for (const file of files) {
    const rel = relative(WIKI_ROOT, file).split('\\').join('/'); // normalize Windows paths
    const slug = basename(file, '.md');
    let href = null;

    if (rel.includes('/')) {
      const folder = rel.split('/')[0];
      const prefix = FOLDER_TO_PREFIX[folder];
      if (!prefix) continue;
      href = `${base}${prefix}/${slug}/`;
    } else {
      // root file
      if (ROOT_EXCLUDE.has(rel)) continue;
      const matches = ROOT_INCLUDE_PATTERNS.some(re => re.test(rel));
      if (!matches) continue;
      href = `${base}/${slug}/`;
    }

    if (href && !map[slug]) {
      map[slug] = { href };
    }
  }
  return map;
}
