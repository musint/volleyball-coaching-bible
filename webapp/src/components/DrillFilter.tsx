/** @jsxImportSource preact */
import { useMemo, useState, useEffect } from 'preact/hooks';

interface Drill {
  slug: string;
  name: string;
  primary: string;
  secondary: string[];
  techniques: string[];
  phase: string;
  durationMin: number;
  teamMin: number;
  teamMax: number;
  levels: string[];
  equipment: string[];
  href: string;
}

interface Props {
  drills: Drill[];
  base: string;
}

const SKILLS = ['passing','setting','hitting','blocking','serving','defense','transition'];
const PHASES = ['warm-up','skill','strategic','competition','conditioning'];
const LEVELS = ['14u','hs','college','professional'];

function parseHash(): Record<string, string> {
  if (typeof window === 'undefined') return {};
  const q = new URLSearchParams(window.location.search);
  const r: Record<string, string> = {};
  for (const [k, v] of q.entries()) r[k] = v;
  return r;
}

function setHash(state: Record<string, string>) {
  if (typeof window === 'undefined') return;
  const q = new URLSearchParams();
  for (const [k, v] of Object.entries(state)) {
    if (v) q.set(k, v);
  }
  const s = q.toString();
  history.replaceState(null, '', s ? `?${s}` : window.location.pathname);
}

export default function DrillFilter({ drills }: Props) {
  const init = parseHash();
  const [skills, setSkills] = useState<string[]>(init.skills ? init.skills.split(',') : []);
  const [phases, setPhases] = useState<string[]>(init.phases ? init.phases.split(',') : []);
  const [levels, setLevels] = useState<string[]>(init.levels ? init.levels.split(',') : []);
  const [maxDuration, setMaxDuration] = useState<number>(init.maxDuration ? +init.maxDuration : 0);
  const [search, setSearch] = useState<string>(init.q ?? '');
  const [sort, setSort] = useState<string>(init.sort ?? 'name');

  // Sync filter state to URL
  useEffect(() => {
    setHash({
      skills: skills.join(','),
      phases: phases.join(','),
      levels: levels.join(','),
      maxDuration: maxDuration ? String(maxDuration) : '',
      q: search,
      sort: sort === 'name' ? '' : sort,
    });
  }, [skills, phases, levels, maxDuration, search, sort]);

  const filtered = useMemo(() => {
    let result = drills.filter(d => {
      if (skills.length && !skills.includes(d.primary)) return false;
      if (phases.length && !phases.includes(d.phase)) return false;
      if (levels.length && !d.levels.some(l => levels.includes(l))) return false;
      if (maxDuration > 0 && d.durationMin > maxDuration) return false;
      if (search) {
        const q = search.toLowerCase();
        if (!d.name.toLowerCase().includes(q) &&
            !d.slug.toLowerCase().includes(q) &&
            !d.techniques.some(t => t.includes(q))) return false;
      }
      return true;
    });
    if (sort === 'duration') result = [...result].sort((a, b) => a.durationMin - b.durationMin);
    else if (sort === 'phase') result = [...result].sort((a, b) =>
      PHASES.indexOf(a.phase) - PHASES.indexOf(b.phase) || a.name.localeCompare(b.name));
    else result = [...result].sort((a, b) => a.name.localeCompare(b.name));
    return result;
  }, [drills, skills, phases, levels, maxDuration, search, sort]);

  function toggle(arr: string[], value: string, setter: (v: string[]) => void) {
    if (arr.includes(value)) setter(arr.filter(x => x !== value));
    else setter([...arr, value]);
  }

  function reset() {
    setSkills([]); setPhases([]); setLevels([]); setMaxDuration(0); setSearch(''); setSort('name');
  }

  return (
    <div class="grid md:grid-cols-[16rem_1fr] gap-6">
      {/* Filter sidebar */}
      <aside class="bg-stone-50 border border-stone-200 rounded-lg p-4 text-sm md:sticky md:top-20 md:self-start no-print">
        <div class="flex justify-between items-center mb-3">
          <h2 class="font-serif font-bold">Filters</h2>
          {(skills.length || phases.length || levels.length || maxDuration || search || sort !== 'name') ? (
            <button onClick={reset} class="text-xs text-orange-700 hover:underline">Reset</button>
          ) : null}
        </div>

        <div class="mb-4">
          <label class="block text-xs font-semibold text-stone-500 uppercase tracking-wider mb-1">Search</label>
          <input
            type="text"
            value={search}
            onInput={(e) => setSearch((e.currentTarget as HTMLInputElement).value)}
            placeholder="butterfly, pepper, …"
            class="w-full border border-stone-300 rounded px-2 py-1 text-sm"
          />
        </div>

        <div class="mb-4">
          <label class="block text-xs font-semibold text-stone-500 uppercase tracking-wider mb-1">Primary skill</label>
          <div class="flex flex-wrap gap-1">
            {SKILLS.map(s => (
              <button
                onClick={() => toggle(skills, s, setSkills)}
                class={`px-2 py-1 text-xs rounded border ${skills.includes(s) ? 'bg-orange-600 text-white border-orange-600' : 'bg-white border-stone-300 text-stone-700 hover:bg-stone-100'}`}
              >{s}</button>
            ))}
          </div>
        </div>

        <div class="mb-4">
          <label class="block text-xs font-semibold text-stone-500 uppercase tracking-wider mb-1">Phase</label>
          <div class="flex flex-wrap gap-1">
            {PHASES.map(p => (
              <button
                onClick={() => toggle(phases, p, setPhases)}
                class={`px-2 py-1 text-xs rounded border ${phases.includes(p) ? 'bg-orange-600 text-white border-orange-600' : 'bg-white border-stone-300 text-stone-700 hover:bg-stone-100'}`}
              >{p}</button>
            ))}
          </div>
        </div>

        <div class="mb-4">
          <label class="block text-xs font-semibold text-stone-500 uppercase tracking-wider mb-1">Age level</label>
          <div class="flex flex-wrap gap-1">
            {LEVELS.map(l => (
              <button
                onClick={() => toggle(levels, l, setLevels)}
                class={`px-2 py-1 text-xs rounded border ${levels.includes(l) ? 'bg-orange-600 text-white border-orange-600' : 'bg-white border-stone-300 text-stone-700 hover:bg-stone-100'}`}
              >{l}</button>
            ))}
          </div>
        </div>

        <div class="mb-4">
          <label class="block text-xs font-semibold text-stone-500 uppercase tracking-wider mb-1">
            Max duration {maxDuration > 0 && <span class="text-stone-700">({maxDuration} min)</span>}
          </label>
          <input
            type="range"
            min="0"
            max="60"
            step="5"
            value={maxDuration}
            onInput={(e) => setMaxDuration(+(e.currentTarget as HTMLInputElement).value)}
            class="w-full"
          />
          <div class="flex justify-between text-xs text-stone-500"><span>any</span><span>60min</span></div>
        </div>

        <div>
          <label class="block text-xs font-semibold text-stone-500 uppercase tracking-wider mb-1">Sort</label>
          <select value={sort} onChange={(e) => setSort((e.currentTarget as HTMLSelectElement).value)}
                  class="w-full border border-stone-300 rounded px-2 py-1 text-sm">
            <option value="name">Name (A→Z)</option>
            <option value="duration">Duration (short→long)</option>
            <option value="phase">Phase</option>
          </select>
        </div>
      </aside>

      {/* Result table */}
      <div>
        <div class="text-sm text-stone-600 mb-3">
          Showing <strong>{filtered.length}</strong> of {drills.length} drills.
        </div>
        <div class="overflow-x-auto rounded border border-stone-200">
          <table class="min-w-full text-sm">
            <thead class="bg-stone-100 text-stone-700">
              <tr>
                <th class="text-left px-3 py-2">Drill</th>
                <th class="text-left px-3 py-2">Skill</th>
                <th class="text-left px-3 py-2">Phase</th>
                <th class="text-left px-3 py-2">Min</th>
                <th class="text-left px-3 py-2">Team</th>
                <th class="text-left px-3 py-2 hidden md:table-cell">Levels</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map(d => (
                <tr class="border-t border-stone-200 hover:bg-orange-50">
                  <td class="px-3 py-2"><a href={d.href} class="text-orange-700 font-medium no-underline hover:underline">{d.name}</a></td>
                  <td class="px-3 py-2 text-stone-700">{d.primary}</td>
                  <td class="px-3 py-2 text-stone-600">{d.phase}</td>
                  <td class="px-3 py-2 tabular-nums">{d.durationMin}</td>
                  <td class="px-3 py-2 text-stone-600">{d.teamMin}–{d.teamMax}</td>
                  <td class="px-3 py-2 hidden md:table-cell text-stone-500 text-xs">{d.levels.join(', ')}</td>
                </tr>
              ))}
              {filtered.length === 0 && (
                <tr><td colSpan={6} class="px-3 py-6 text-center text-stone-500">No drills match. <button onClick={reset} class="text-orange-700 hover:underline">Reset filters</button></td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
