// Wrap every markdown table in a horizontal-scroll container so wide tables
// (tryout rubrics are 6 columns) stay usable on phones. Tables with 4+ columns
// also get `table-wide`, which pins the first column while the rest scroll —
// on a rubric that keeps the criterion name visible while a coach swipes
// across the 1-5 anchors.
import { visit } from 'unist-util-visit';

export default function rehypeWrapTables() {
  return (tree) => {
    visit(tree, 'element', (node, index, parent) => {
      if (node.tagName !== 'table' || !parent || index === null) return;
      if (parent.tagName === 'div' && parent.properties?.className?.includes('table-scroll')) return;

      let cols = 0;
      visit(node, 'element', (row) => {
        if (row.tagName !== 'tr') return;
        const n = row.children.filter(
          (c) => c.type === 'element' && (c.tagName === 'th' || c.tagName === 'td')
        ).length;
        if (n > cols) cols = n;
      });

      const className = ['table-scroll'];
      if (cols >= 4) {
        node.properties = node.properties || {};
        const existing = node.properties.className;
        node.properties.className = Array.isArray(existing)
          ? [...existing, 'table-wide']
          : existing ? [existing, 'table-wide'] : ['table-wide'];
      }

      parent.children[index] = {
        type: 'element',
        tagName: 'div',
        properties: { className },
        children: [node],
      };
    });
  };
}
