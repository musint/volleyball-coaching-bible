// Volleyball court diagram SVG generator.
//
// Renders a top-down view of a half-court with one side of opponent's court
// shown faded, an attack-direction arrow, and player positions labeled with
// roles. Used by remark-court-diagram.js to embed diagrams inline in wiki
// markdown via fenced ```court-diagram``` code blocks.
//
// Geometry: viewBox 900x1200 (width x height in mm).
// - y=0..300: opponent side (faded; shows attacker + arrow)
// - y=300: net
// - y=300..1200: defense side (your team's half-court)
// - y=600: 3m attack line
// - y=1200: end line
// - x=0..900: court width (9m)

// Court dimensions
const W = 900;
const H = 1200;
const NET_Y = 300;
const LINE_3M_Y = NET_Y + 300; // 3m past net = y=600
const END_Y = H;

// Color palette tied to the site's theme.
const C = {
  courtFill: '#fef9e7', // cream
  courtFillFaded: '#fafaf9', // stone-50
  line: '#92400e', // amber-800
  net: '#1c1917', // stone-900
  blocker: '#ef4444', // red-500
  blockerOff: '#fca5a5', // red-300 (off-blocker, pulls)
  defender: '#2563eb', // blue-600
  defenderAnchor: '#1d4ed8', // blue-700 (the 6m middle anchor — distinguished)
  libero: '#facc15', // yellow-400
  liberoBorder: '#a16207', // yellow-700
  attackArrow: '#dc2626', // red-600
  attackerOpponent: '#7f1d1d', // red-900 (faded opponent)
  textDark: '#1c1917', // stone-900
  textMuted: '#78716c', // stone-500
};

// Player roles used across configs.
// Each role: { id, x, y, label (1-2 chars), color, borderColor, role-name }
function makePlayer(id, x, y, label, color, role, opts = {}) {
  return {
    id,
    x,
    y,
    label,
    color,
    borderColor: opts.borderColor || color,
    role,
    accent: opts.accent || false, // for the libero or anchor — gets a halo/star
  };
}

// Five defense systems supported initially. Each config returns:
// { title, subtitle, players[], attackOrigin (x,y), attackTarget (x,y), notes? }
export const DEFENSE_CONFIGS = {
  // 1. Middle-Middle, libero-at-LB (user's preferred install)
  'middle-middle-libero-lb': {
    title: 'Middle-Middle Defense — Libero at LB',
    subtitle: 'Trinsey/GMS scheme · libero at zone 5 (line) · MB anchor at 6m middle',
    players: [
      makePlayer('LF', 200, NET_Y + 30, 'LF', C.blocker, 'Block (line side)'),
      makePlayer('MF', 450, NET_Y + 30, 'MF', C.blocker, 'Block (middle)'),
      makePlayer('RF', 750, LINE_3M_Y, 'RF', C.blockerOff, 'Off-blocker — pulls to short cross/tip'),
      makePlayer('LB', 200, NET_Y + 550, 'L', C.libero, 'Libero — line, deep-line cuts', { borderColor: C.liberoBorder, accent: true }),
      makePlayer('MB', 450, NET_Y + 600, 'MB', C.defenderAnchor, '6m middle anchor (Trinsey 90-95% zone)', { accent: true }),
      makePlayer('RB', 750, NET_Y + 600, 'RB', C.defender, 'Cross side, deep cross + over-the-block'),
    ],
    attackOrigin: { x: 750, y: 180 },
    attackTarget: { x: 200, y: NET_Y + 550 },
    attackerLabel: 'OH',
  },

  // 2. Middle-Middle, libero-at-MB (Trinsey-canonical alternative)
  'middle-middle-libero-mb': {
    title: 'Middle-Middle Defense — Libero at MB',
    subtitle: 'Trinsey-canonical · libero anchors 6m middle directly',
    players: [
      makePlayer('LF', 200, NET_Y + 30, 'LF', C.blocker, 'Block (line side)'),
      makePlayer('MF', 450, NET_Y + 30, 'MF', C.blocker, 'Block (middle)'),
      makePlayer('RF', 750, LINE_3M_Y, 'RF', C.blockerOff, 'Off-blocker — pulls to short cross/tip'),
      makePlayer('LB', 200, NET_Y + 550, 'LB', C.defender, 'Line, deep-line cuts'),
      makePlayer('MB', 450, NET_Y + 600, 'L', C.libero, 'Libero — 6m middle anchor', { borderColor: C.liberoBorder, accent: true }),
      makePlayer('RB', 750, NET_Y + 600, 'RB', C.defender, 'Cross side, deep cross'),
    ],
    attackOrigin: { x: 750, y: 180 },
    attackTarget: { x: 450, y: NET_Y + 600 },
    attackerLabel: 'OH',
  },

  // 3. Middle-Back (libero deep at end line — modern HS+/college default)
  'middle-back': {
    title: 'Middle-Back Defense',
    subtitle: 'Libero deep at zone 6 (~8-9m, end line) · reads block seam · shifts seam-to-seam',
    players: [
      makePlayer('LF', 200, NET_Y + 30, 'LF', C.blocker, 'Block (line side)'),
      makePlayer('MF', 450, NET_Y + 30, 'MF', C.blocker, 'Block (middle)'),
      makePlayer('RF', 750, LINE_3M_Y, 'RF', C.blockerOff, 'Off-blocker — pulls to short cross/tip'),
      makePlayer('LB', 200, NET_Y + 700, 'LB', C.defender, 'Line, deep'),
      makePlayer('MB', 450, NET_Y + 800, 'L', C.libero, 'Libero — deep middle, reads seam', { borderColor: C.liberoBorder, accent: true }),
      makePlayer('RB', 750, NET_Y + 700, 'RB', C.defender, 'Cross deep, over-the-block'),
    ],
    attackOrigin: { x: 750, y: 180 },
    attackTarget: { x: 450, y: NET_Y + 800 },
    attackerLabel: 'OH',
  },

  // 4. Perimeter (all 5 non-blocking defenders along edges)
  perimeter: {
    title: 'Perimeter Defense',
    subtitle: 'Landmarks-based · all defenders along the court edges · simplest to install',
    players: [
      makePlayer('LF', 200, NET_Y + 30, 'LF', C.blocker, 'Block (line side)'),
      makePlayer('MF', 450, NET_Y + 30, 'MF', C.blocker, 'Block (middle)'),
      makePlayer('RF', 750, LINE_3M_Y - 20, 'RF', C.blockerOff, 'Off-blocker — short cross / tip cover'),
      makePlayer('LB', 130, NET_Y + 750, 'LB', C.defender, 'Deep line corner (zone 5)'),
      makePlayer('MB', 450, NET_Y + 820, 'L', C.libero, 'Libero — deep middle (zone 6)', { borderColor: C.liberoBorder, accent: true }),
      makePlayer('RB', 770, NET_Y + 750, 'RB', C.defender, 'Deep cross corner (zone 1)'),
    ],
    attackOrigin: { x: 750, y: 180 },
    attackTarget: { x: 130, y: NET_Y + 750 },
    attackerLabel: 'OH',
  },

  // 5. Up Defense / 6-Up / Setter-Up (Russ Rose's published variant — defender at 3m line)
  'up-defense': {
    title: 'Up Defense (6-Up / Setter-Up)',
    subtitle: 'Russ Rose · back-row defender pulled to 3m line behind block · tip-priority',
    players: [
      makePlayer('LF', 200, NET_Y + 30, 'LF', C.blocker, 'Block (line side)'),
      makePlayer('MF', 450, NET_Y + 30, 'MF', C.blocker, 'Block (middle)'),
      makePlayer('RF', 750, LINE_3M_Y - 20, 'RF', C.blockerOff, 'Off-blocker — short cross'),
      makePlayer('LB', 200, NET_Y + 700, 'LB', C.defender, 'Line, deep'),
      makePlayer('UP', 450, LINE_3M_Y - 20, 'UP', C.defenderAnchor, 'Up defender (libero or other) — 3m line behind block', { accent: true }),
      makePlayer('RB', 750, NET_Y + 700, 'RB', C.defender, 'Cross, deep'),
    ],
    attackOrigin: { x: 750, y: 180 },
    attackTarget: { x: 450, y: LINE_3M_Y },
    attackerLabel: 'OH',
  },
};

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function arrowMarker() {
  return `<defs>
    <marker id="court-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="${C.attackArrow}" />
    </marker>
    <pattern id="court-net" x="0" y="0" width="14" height="14" patternUnits="userSpaceOnUse">
      <rect x="0" y="0" width="14" height="14" fill="white" />
      <line x1="0" y1="0" x2="14" y2="14" stroke="${C.net}" stroke-width="1.2" />
    </pattern>
    <filter id="court-shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="4" stdDeviation="3" flood-opacity="0.18" />
    </filter>
  </defs>`;
}

function courtBackground() {
  return `
    <!-- opponent half (faded) -->
    <rect x="0" y="0" width="${W}" height="${NET_Y}" fill="${C.courtFillFaded}" />
    <!-- defense half -->
    <rect x="0" y="${NET_Y}" width="${W}" height="${H - NET_Y}" fill="${C.courtFill}" />
    <!-- 3m attack line -->
    <line x1="0" y1="${LINE_3M_Y}" x2="${W}" y2="${LINE_3M_Y}" stroke="${C.line}" stroke-width="3" stroke-dasharray="0" />
    <!-- end line -->
    <line x1="0" y1="${END_Y}" x2="${W}" y2="${END_Y}" stroke="${C.line}" stroke-width="3" />
    <!-- side lines (defense half) -->
    <line x1="0" y1="${NET_Y}" x2="0" y2="${END_Y}" stroke="${C.line}" stroke-width="3" />
    <line x1="${W}" y1="${NET_Y}" x2="${W}" y2="${END_Y}" stroke="${C.line}" stroke-width="3" />
    <!-- side lines (opponent strip; lighter) -->
    <line x1="0" y1="0" x2="0" y2="${NET_Y}" stroke="${C.line}" stroke-width="2" stroke-opacity="0.4" />
    <line x1="${W}" y1="0" x2="${W}" y2="${NET_Y}" stroke="${C.line}" stroke-width="2" stroke-opacity="0.4" />
    <!-- top of opponent strip (their endline edge — partial) -->
    <line x1="0" y1="0" x2="${W}" y2="0" stroke="${C.line}" stroke-width="2" stroke-opacity="0.4" />
    <!-- net band -->
    <rect x="0" y="${NET_Y - 14}" width="${W}" height="28" fill="url(#court-net)" stroke="${C.net}" stroke-width="2" />`;
}

function attackVisual(config) {
  const { attackOrigin, attackTarget, attackerLabel } = config;
  if (!attackOrigin || !attackTarget) return '';
  // Render the attacker on the opponent side
  return `
    <!-- opponent attacker (faded context) -->
    <circle cx="${attackOrigin.x}" cy="${attackOrigin.y}" r="32" fill="${C.attackerOpponent}" opacity="0.6" />
    <text x="${attackOrigin.x}" y="${attackOrigin.y + 6}" text-anchor="middle" font-family="ui-sans-serif, system-ui, sans-serif" font-size="22" font-weight="700" fill="white">${escapeHtml(attackerLabel || 'OH')}</text>
    <!-- attack direction arrow -->
    <line x1="${attackOrigin.x}" y1="${attackOrigin.y + 24}" x2="${attackTarget.x}" y2="${attackTarget.y - 28}" stroke="${C.attackArrow}" stroke-width="6" stroke-linecap="round" stroke-dasharray="14 8" marker-end="url(#court-arrow)" opacity="0.85" />`;
}

function playerCircle(p) {
  const r = 36;
  const labelY = p.y + 8;
  // Halo for accent players (libero, anchor)
  const halo = p.accent
    ? `<circle cx="${p.x}" cy="${p.y}" r="${r + 7}" fill="none" stroke="${p.borderColor}" stroke-width="2" stroke-opacity="0.5" />`
    : '';
  return `
    <g filter="url(#court-shadow)">
      ${halo}
      <circle cx="${p.x}" cy="${p.y}" r="${r}" fill="${p.color}" stroke="${p.borderColor}" stroke-width="3" />
      <text x="${p.x}" y="${labelY}" text-anchor="middle" font-family="ui-sans-serif, system-ui, sans-serif" font-size="22" font-weight="700" fill="white">${escapeHtml(p.label)}</text>
    </g>`;
}

function legendRow(config) {
  // Build the role legend below the court
  const rows = config.players.map((p) => {
    return `
      <li style="display:flex;align-items:center;gap:0.5rem;padding:0.25rem 0;">
        <span style="display:inline-block;width:1.25rem;height:1.25rem;border-radius:9999px;background:${p.color};border:2px solid ${p.borderColor};flex-shrink:0;"></span>
        <span style="font-weight:600;color:#1c1917;min-width:2.25rem;">${escapeHtml(p.label)}</span>
        <span style="color:#57534e;font-size:0.875rem;">${escapeHtml(p.role)}</span>
      </li>`;
  });
  return `<ul style="list-style:none;padding:0;margin:0.5rem 0 0 0;font-family:ui-sans-serif, system-ui, sans-serif;font-size:0.9375rem;">${rows.join('')}</ul>`;
}

export function buildDefenseSvg(systemId) {
  const config = DEFENSE_CONFIGS[systemId];
  if (!config) {
    return `<div style="padding:1rem;background:#fef2f2;border:1px solid #fecaca;border-radius:0.5rem;color:#991b1b;font-family:ui-sans-serif,system-ui,sans-serif;">Court diagram: unknown system "${escapeHtml(systemId)}". Known systems: ${Object.keys(DEFENSE_CONFIGS).map(escapeHtml).join(', ')}.</div>`;
  }

  const svg = `<svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="${escapeHtml(config.title)}" style="width:100%;height:auto;display:block;max-width:480px;margin:0 auto;">
${arrowMarker()}
${courtBackground()}
${attackVisual(config)}
${config.players.map(playerCircle).join('\n')}
</svg>`;

  // Wrap in a styled container with title, subtitle, and legend.
  return `<figure style="margin:1.5rem 0;padding:1rem 1.25rem;border:1px solid #e7e5e4;border-radius:0.75rem;background:#fafaf9;">
  <figcaption style="margin:0 0 0.5rem 0;font-family:ui-serif,Georgia,serif;">
    <strong style="display:block;font-size:1.0625rem;color:#1c1917;">${escapeHtml(config.title)}</strong>
    <span style="display:block;font-size:0.875rem;color:#57534e;margin-top:0.125rem;">${escapeHtml(config.subtitle)}</span>
  </figcaption>
  ${svg}
  ${legendRow(config)}
</figure>`;
}

// Convenience: list of supported systems for documentation.
export const SUPPORTED_SYSTEMS = Object.keys(DEFENSE_CONFIGS);
