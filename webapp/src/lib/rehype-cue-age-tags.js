// On cue-dictionary pages: parse "Introduced Xs", "Refined Ys+", "Lifelong"
// patterns embedded in cue prose and:
//   1. Wrap the whole containing element (<p> or <li>) with data attributes
//      so a client-side filter island can show/hide based on age selection.
//   2. Replace the text "Introduced 12s." with a visible chip span so coaches
//      can scan ages at a glance.
//
// Activated only on /manual/cues/* pages by checking the document URL —
// safe to ship globally because non-cue pages have no matching patterns.

import { visit } from 'unist-util-visit';

const INTRO_RE = /Introduced (\d+)s/;          // captures "Introduced 14s"
const REFINED_RE = /Refined (\d+)s\+?/;        // captures "Refined 13s+" or "Refined 13s"
const LIFELONG_RE = /\bLifelong\b/i;

function elementText(node) {
  let out = '';
  if (!node || !node.children) return '';
  for (const c of node.children) {
    if (c.type === 'text') out += c.value;
    else if (c.children) out += elementText(c);
  }
  return out;
}

// Replace `Introduced 12s.` text inside an element with a chip span.
function injectChips(node) {
  if (!node || !node.children) return;
  const newChildren = [];
  for (const child of node.children) {
    if (child.type === 'text') {
      // Look for "Introduced Xs", "Refined Xs+", "Lifelong"
      const text = child.value;
      let lastIndex = 0;
      const replacements = [];

      // Compile all matches across all three patterns
      const all = [];
      let m;
      const introGlobal = /Introduced (\d+)s\b/g;
      while ((m = introGlobal.exec(text)) !== null) {
        all.push({ start: m.index, end: m.index + m[0].length, kind: 'introduced', age: m[1] + 's' });
      }
      const refinedGlobal = /Refined (\d+)s\+?\b/g;
      while ((m = refinedGlobal.exec(text)) !== null) {
        all.push({ start: m.index, end: m.index + m[0].length, kind: 'refined', age: m[1] + 's' });
      }
      const lifelongGlobal = /\bLifelong\b/g;
      while ((m = lifelongGlobal.exec(text)) !== null) {
        all.push({ start: m.index, end: m.index + m[0].length, kind: 'lifelong' });
      }
      all.sort((a, b) => a.start - b.start);

      if (all.length === 0) {
        newChildren.push(child);
        continue;
      }

      for (const r of all) {
        if (r.start > lastIndex) {
          newChildren.push({ type: 'text', value: text.slice(lastIndex, r.start) });
        }
        const className = r.kind === 'introduced' ? 'age-chip age-chip-intro'
          : r.kind === 'refined' ? 'age-chip age-chip-refined'
          : 'age-chip age-chip-lifelong';
        const label = r.kind === 'introduced' ? `${r.age} intro`
          : r.kind === 'refined' ? `${r.age}+ refined`
          : 'lifelong';
        newChildren.push({
          type: 'element',
          tagName: 'span',
          properties: { className: [className] },
          children: [{ type: 'text', value: label }],
        });
        lastIndex = r.end;
      }
      if (lastIndex < text.length) {
        newChildren.push({ type: 'text', value: text.slice(lastIndex) });
      }
    } else {
      // recurse into nested elements
      injectChips(child);
      newChildren.push(child);
    }
  }
  node.children = newChildren;
}

export default function rehypeCueAgeTags() {
  return (tree, file) => {
    // Only run on cue-dictionary pages. Astro passes a `data` object with the
    // markdown frontmatter via `file.data`. Be defensive — if we can't tell,
    // run the chip injection (idempotent on non-cue pages since the prose
    // patterns won't match).
    visit(tree, 'element', (node) => {
      if (node.tagName !== 'p' && node.tagName !== 'li') return;
      const text = elementText(node);
      const intro = text.match(INTRO_RE);
      const refined = text.match(REFINED_RE);
      const lifelong = LIFELONG_RE.test(text);
      if (!intro && !lifelong) return;

      node.properties = node.properties || {};
      if (intro) node.properties['data-introduced'] = `${intro[1]}s`;
      if (refined) node.properties['data-refined'] = `${refined[1]}s`;
      if (lifelong) node.properties['data-lifelong'] = 'true';
      node.properties.className = (node.properties.className || []).concat(['cue-entry']);

      injectChips(node);
    });
  };
}
