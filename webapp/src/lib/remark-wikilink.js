// Remark plugin: convert [[slug]] to <a href> using a pre-built slug map.
// Falls back to plain text for unresolvable wikilinks (matches our lint rule —
// broken wikilinks render as text rather than failing the build).

import { visit } from 'unist-util-visit';

const WIKILINK_RE = /\[\[([a-z0-9][a-z0-9\-]*)\]\]/g;

export default function remarkWikilink(opts = {}) {
  const slugMap = opts.slugMap || {};

  return (tree) => {
    visit(tree, 'text', (node, index, parent) => {
      if (!parent || index === undefined || index === null) return;
      const text = node.value;
      WIKILINK_RE.lastIndex = 0;
      if (!WIKILINK_RE.test(text)) return;

      WIKILINK_RE.lastIndex = 0;
      const parts = [];
      let last = 0;
      let m;
      while ((m = WIKILINK_RE.exec(text)) !== null) {
        if (m.index > last) {
          parts.push({ type: 'text', value: text.slice(last, m.index) });
        }
        const slug = m[1];
        const target = slugMap[slug];
        if (target) {
          parts.push({
            type: 'link',
            url: target.href,
            children: [{ type: 'text', value: humanize(slug) }],
          });
        } else {
          // unresolved — render as plain text with brackets so the reader sees it's a wikilink that didn't resolve
          parts.push({ type: 'text', value: m[0] });
        }
        last = WIKILINK_RE.lastIndex;
      }
      if (last < text.length) {
        parts.push({ type: 'text', value: text.slice(last) });
      }
      parent.children.splice(index, 1, ...parts);
      return ['skip', index + parts.length];
    });
  };
}

function humanize(slug) {
  // turn 'karch-kiraly' → 'Karch Kiraly'; keep age slugs like '14s' as-is
  if (/^\d+s$/.test(slug)) return slug;
  if (/-/.test(slug)) {
    return slug.split('-').map(w => w.length > 0 ? w[0].toUpperCase() + w.slice(1) : w).join(' ');
  }
  return slug;
}
