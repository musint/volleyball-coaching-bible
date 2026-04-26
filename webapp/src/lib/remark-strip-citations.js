// Strip inline [citation-key] markers from rendered markdown.
// Keeps honesty tags ([unsourced], [unverified], etc.) since those are intentional
// flags that signal claims still needing a source.
//
// Runs AFTER remark-wikilink so it never sees [[wikilink]] patterns — those
// are already converted to link AST nodes by the time we walk text nodes.

import { visit } from 'unist-util-visit';

const HONESTY_TAGS = new Set([
  'unsourced',
  'unverified',
  'transcript-unavailable',
  'translation-needed',
]);

// Match [identifier] where identifier is lowercase alphanumeric+hyphens.
// Negative lookahead prevents matching markdown link syntax `[text](url)` and
// the inner half of a wikilink `]]`.
const CITATION_RE = /\s*\[([a-z0-9][a-z0-9-]*)\](?!\(|\[|\])/g;

export default function remarkStripCitations() {
  return (tree) => {
    // Step 1: when the markdown has adjacent `[text][ref]` patterns, remark
    // parses them as `linkReference` nodes (treating the second pair as a
    // reference link with no matching `[ref]: url` definition). Convert those
    // back to plain text nodes with the brackets restored, so step 2 can
    // strip them via the citation regex.
    visit(tree, 'linkReference', (node, index, parent) => {
      if (!parent || index === undefined || index === null) return;
      const inner = (node.children || [])
        .map((c) => (c.type === 'text' ? c.value : ''))
        .join('');
      parent.children.splice(index, 1, { type: 'text', value: `[${inner}]` });
      return ['skip', index];
    });

    // Step 2: strip `[citation-key]` patterns from all text nodes. Honesty tags
    // are preserved as visible markers.
    visit(tree, 'text', (node) => {
      let text = node.value;
      text = text.replace(CITATION_RE, (_match, key) => {
        if (HONESTY_TAGS.has(key)) return ` [${key}]`;
        return '';
      });
      text = text.replace(/[ \t]+([.,;:!?])/g, '$1');
      text = text.replace(/[ \t]{2,}/g, ' ');
      node.value = text;
    });

    // Step 3: drop any orphaned link-reference definitions (`[id]: url`) at
    // the root level. The wiki doesn't use real reference definitions, but if
    // any sneak through they'd render as empty link-targets.
    if (Array.isArray(tree.children)) {
      tree.children = tree.children.filter((c) => c.type !== 'definition');
    }
  };
}
