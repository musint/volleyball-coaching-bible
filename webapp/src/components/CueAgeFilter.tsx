/** @jsxImportSource preact */
import { useEffect, useState } from 'preact/hooks';

const AGES = ['10s','11s','12s','13s','14s','15s','16s','17s','18s'];

function ageNum(a: string): number {
  return parseInt(a, 10);
}

export default function CueAgeFilter() {
  const [selected, setSelected] = useState<string | null>(null);

  // Parse from URL on first paint
  useEffect(() => {
    const q = new URLSearchParams(window.location.search);
    const a = q.get('age');
    if (a && AGES.includes(a)) setSelected(a);
  }, []);

  // Sync to URL on change
  useEffect(() => {
    const q = new URLSearchParams(window.location.search);
    if (selected) q.set('age', selected);
    else q.delete('age');
    const s = q.toString();
    history.replaceState(null, '', s ? `?${s}` : window.location.pathname);
  }, [selected]);

  // Apply filter to cue entries via DOM
  useEffect(() => {
    const entries = document.querySelectorAll<HTMLElement>('.cue-entry');
    if (!selected) {
      entries.forEach(e => { e.style.display = ''; e.classList.remove('cue-dim'); });
      return;
    }
    const wantNum = ageNum(selected);
    entries.forEach(e => {
      const intro = e.getAttribute('data-introduced');
      const lifelong = e.getAttribute('data-lifelong') === 'true';
      const introNum = intro ? ageNum(intro) : null;
      // Show cue if: lifelong, OR introduced at-or-before selected age.
      const visible = lifelong || (introNum !== null && introNum <= wantNum);
      e.style.display = visible ? '' : 'none';
    });
  }, [selected]);

  return (
    <div class="not-prose mb-6 p-4 rounded-lg border-2 border-orange-200 bg-orange-50/60 no-print">
      <div class="flex flex-wrap items-baseline gap-2 mb-2">
        <span class="font-serif font-bold text-stone-900">Show cues for age:</span>
        <span class="text-xs text-stone-500">
          {selected
            ? <>cues introduced at <strong>{selected}</strong> or earlier (plus lifelong cues)</>
            : <>showing all cues</>}
        </span>
      </div>
      <div class="flex flex-wrap gap-1">
        <button
          onClick={() => setSelected(null)}
          class={`px-3 py-1 text-sm rounded border ${selected === null ? 'bg-stone-700 text-white border-stone-700' : 'bg-white border-stone-300 text-stone-700 hover:bg-stone-100'}`}
        >All ages</button>
        {AGES.map(a => (
          <button
            onClick={() => setSelected(a)}
            class={`px-3 py-1 text-sm rounded border ${selected === a ? 'bg-orange-600 text-white border-orange-600' : 'bg-white border-stone-300 text-stone-700 hover:bg-orange-50 hover:border-orange-300'}`}
          >{a}</button>
        ))}
      </div>
    </div>
  );
}
