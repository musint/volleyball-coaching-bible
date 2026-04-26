// Drop the "## Sources" / "## Bibliography" section from rendered markdown.
// The wiki carries source lists at the bottom of every page for citation
// integrity — useful for archival reading, noise for the webapp reader.

export default function remarkHideSources() {
  return (tree) => {
    if (!tree.children) return;
    let cutoff = -1;
    for (let i = 0; i < tree.children.length; i++) {
      const node = tree.children[i];
      if (node.type !== 'heading' || node.depth !== 2) continue;
      const text = (node.children?.[0]?.value || '').trim().toLowerCase();
      if (text === 'sources' || text === 'bibliography' || text === 'where it\'s cited') {
        cutoff = i;
        break;
      }
    }
    if (cutoff >= 0) {
      tree.children = tree.children.slice(0, cutoff);
    }
  };
}
