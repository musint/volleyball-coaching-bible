// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';
import preact from '@astrojs/preact';
import remarkWikilink from './src/lib/remark-wikilink.js';
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
    remarkPlugins: [[remarkWikilink, { base: BASE, slugMap }]],
  },
});
