// Replace fenced code blocks with info string "court-diagram" with rendered
// inline SVG diagrams. The fence body is a single line giving the system id,
// e.g.:
//
//   ```court-diagram
//   middle-middle-libero-lb
//   ```
//
// or with a key:value form:
//
//   ```court-diagram
//   system: middle-middle-libero-lb
//   ```
//
// Unknown system ids render an inline error block (visible to the editor)
// rather than failing the build.

import { visit } from 'unist-util-visit';
import { buildDefenseSvg } from './court-diagrams.js';

function parseSystemId(value) {
  const text = (value || '').trim();
  if (!text) return null;
  // Accept a bare slug or "system: <slug>" form.
  const colonIdx = text.indexOf(':');
  if (colonIdx >= 0) {
    return text.slice(colonIdx + 1).trim();
  }
  return text.split(/\s+/)[0];
}

export default function remarkCourtDiagram() {
  return (tree) => {
    visit(tree, 'code', (node, index, parent) => {
      if (!parent || index == null) return;
      const lang = (node.lang || '').toLowerCase();
      if (lang !== 'court-diagram') return;
      const systemId = parseSystemId(node.value);
      if (!systemId) return;
      const html = buildDefenseSvg(systemId);
      // Replace the code node with a raw HTML node carrying the rendered SVG.
      parent.children[index] = { type: 'html', value: html };
    });
  };
}
