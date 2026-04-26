// Strip [citation-key] inline references from rendered HTML, post-markdown.
// Runs at the HAST stage so it sees the final plain-text view of all the
// markdown-reference-style edge cases. Honesty tags ([unsourced], etc.) are
// preserved as visible markers.

import { visit } from 'unist-util-visit';

const HONESTY_TAGS = new Set([
  'unsourced',
  'unverified',
  'transcript-unavailable',
  'translation-needed',
]);

const CITATION_RE = /\s*\[([a-z0-9][a-z0-9-]*)\]/g;

export default function rehypeStripCitations() {
  return (tree) => {
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
  };
}
