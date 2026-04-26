// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';
import preact from '@astrojs/preact';
import remarkWikilink from './src/lib/remark-wikilink.js';
import remarkHideSources from './src/lib/remark-hide-sources.js';
import rehypeStripCitations from './src/lib/rehype-strip-citations.js';
import rehypeCueAgeTags from './src/lib/rehype-cue-age-tags.js';
import { buildSlugMap } from './src/lib/slug-resolver.js';

const BASE = '/volleyball-coaching-bible';
const SITE = 'https://musint.github.io';

const slugMap = await buildSlugMap(BASE);

export default defineConfig({
  site: SITE,
  base: BASE,
  output: 'static',
  trailingSlash: 'always',
  vite: {
    plugins: [tailwindcss()],
  },
  integrations: [sitemap(), preact()],
  markdown: {
    // remark plugins operate on the markdown AST (mdast); rehype runs on the
    // HTML AST (hast) after markdown → HTML conversion. Citation stripping
    // runs at the rehype stage because mdast's linkReference handling makes
    // adjacent `[a][b]` patterns ambiguous; by hast time, everything is
    // resolved to text + element nodes we can walk uniformly.
    remarkPlugins: [
      [remarkWikilink, { base: BASE, slugMap }],
      remarkHideSources,
    ],
    rehypePlugins: [
      rehypeStripCitations,
      rehypeCueAgeTags,
    ],
  },
});
