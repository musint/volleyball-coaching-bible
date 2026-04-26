// Astro content collections backed by the wiki/ markdown tree.
// Each collection has a Zod schema mirroring SCHEMA.md frontmatter contracts,
// plus a glob loader pointing at the relevant wiki/ subfolder.

import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Astro's glob loader wants a `base` URL (file://) — relative paths from the
// content config file via import.meta.url. Wiki lives at ../wiki/ relative
// to webapp/src/content.config.ts (i.e. webapp/../wiki/).
const WIKI = new URL('../../wiki/', import.meta.url);
const sub = (p: string) => new URL(p, WIKI);

const SKILLS = z.enum(['passing','setting','hitting','blocking','serving','defense','transition']);
const LEVELS = z.enum(['14u','hs','college']);
const AGES = z.enum(['10s','11s','12s','13s','14s','15s','16s','17s','18s']);

// Several legacy frontmatter fields are typed loosely (year can be int or string,
// trust-tier same, sources arrays sometimes contain nested arrays from earlier
// agent runs). We absorb that variation rather than fighting it.
const looseStrArr = z.array(z.union([z.string(), z.array(z.string())])).default([]);

export const collections = {
  drill: defineCollection({
    loader: glob({ pattern: '*.md', base: sub('drills/') }),
    schema: z.object({
      type: z.literal('drill'),
      name: z.string(),
      'primary-skill': SKILLS,
      'secondary-skills': z.array(z.string()).default([]),
      techniques: z.array(z.string()).min(1),
      phase: z.enum(['warm-up','skill','strategic','competition','conditioning']),
      'team-size-min': z.number().int(),
      'team-size-max': z.number().int(),
      'duration-min': z.number().int(),
      levels: z.array(z.string()),  // canonical enum is LEVELS but real data includes "professional" etc
      equipment: z.array(z.string()).default([]),
      sources: z.array(z.string()).min(1),
      'video-url': z.string().nullable().optional(),
      variations: z.array(z.string()).default([]),
    }),
  }),

  ageGuide: defineCollection({
    loader: glob({ pattern: '*.md', base: sub('age-guides/') }),
    schema: z.object({
      type: z.literal('age-guide'),
      age: AGES,
      phase: z.enum(['introduction','fundamentals','late-fundamentals','specialization','advanced','college-bridge']),
      sources: z.array(z.string()).min(1),
    }),
  }),

  cueDictionary: defineCollection({
    loader: glob({ pattern: '*.md', base: sub('cues/') }),
    schema: z.object({
      type: z.literal('cue-dictionary'),
      skill: SKILLS,
      'age-bands': z.array(AGES),
      sources: z.array(z.string()).min(1),
    }),
  }),

  drillPickList: defineCollection({
    loader: glob({ pattern: '*.md', base: sub('drill-picks/') }),
    schema: z.object({
      type: z.literal('drill-pick-list'),
      age: AGES,
      'season-context': z.enum(['composite','preseason','mid-season','pre-tournament','taper','tryout','postseason','match-day']),
      drills: z.array(z.string()).min(3),
      sources: z.array(z.string()).min(1),
    }),
  }),

  opsDoc: defineCollection({
    loader: glob({ pattern: '*.md', base: sub('ops/') }),
    schema: z.object({
      type: z.literal('ops-doc'),
      kind: z.enum(['match-prep','tryout-rubric','club-ops']),
      // audience is dual-purpose: ops-doc reader role
      // (coach|parent|club-director|front-office) and/or manual-layer
      // audience (womens-indoor-6s|mens-indoor-6s|...). Accept either form.
      audience: z.union([z.string(), z.array(z.string())]).optional(),
      level: LEVELS.optional(),
      sources: z.array(z.string()).min(1),
    }).passthrough(),
  }),

  practicePlan: defineCollection({
    loader: glob({ pattern: '*.md', base: sub('practice-plans/') }),
    schema: z.object({
      type: z.literal('practice-plan'),
      scope: z.enum(['single-session','week','macrocycle']).default('single-session'),
      level: LEVELS,
      'duration-min': z.number().int().optional(),
      focus: z.string(),
      'season-phase': z.string(),
      drills: z.array(z.string()).min(1),
      sources: z.array(z.string()).min(1),
    }).passthrough(),
  }),

  coach: defineCollection({
    loader: glob({ pattern: '*.md', base: sub('coaches/') }),
    schema: z.object({
      type: z.literal('coach'),
      name: z.string(),
      country: z.string(),
      era: z.string(),
      roles: z.array(z.string()).default([]),
      schools: z.array(z.string()).min(1),
      tags: z.array(z.string()).default([]),
      sources: looseStrArr,
    }).passthrough(),
  }),

  school: defineCollection({
    loader: glob({ pattern: '*.md', base: sub('schools/') }),
    schema: z.object({
      type: z.literal('school'),
      name: z.string(),
      origin: z.string(),
      founders: z.array(z.string()).default([]),
      'core-principles': z.array(z.string()).default([]),
      'associated-coaches': z.array(z.string()).default([]),
      'related-schools': z.array(z.string()).default([]),
      sources: z.array(z.string()).default([]),  // institutional stubs may have empty sources
    }).passthrough(),
  }),

  technique: defineCollection({
    loader: glob({ pattern: '*.md', base: sub('techniques/') }),
    schema: z.object({
      type: z.literal('technique'),
      skill: SKILLS,
      subskill: z.string(),
      positions: z.array(z.string()).default([]),
      'related-drills': z.array(z.string()).default([]),
      'related-techniques': z.array(z.string()).default([]),
      'schools-perspectives': z.record(z.string(), z.string()).optional(),
      sources: z.array(z.string()).min(1),
    }).passthrough(),
  }),

  system: defineCollection({
    loader: glob({ pattern: '*.md', base: sub('systems-detail/') }),
    schema: z.object({
      type: z.literal('system'),
      category: z.enum(['offense','defense','serve-receive','blocking','transition']),
      name: z.string(),
      'age-appropriateness': z.array(z.string()).default([]),
      complexity: z.enum(['low','medium','high']),
      'when-to-use': z.string(),
      alternatives: z.array(z.string()).default([]),
      sources: z.array(z.string()).min(1),
    }).passthrough(),
  }),

  source: defineCollection({
    loader: glob({ pattern: '*.md', base: sub('sources/') }),
    schema: z.object({
      type: z.literal('source'),
      title: z.string(),
      'citation-key': z.string(),
    }).passthrough(),  // 597+ source pages have varied legacy frontmatter shapes; preserve all without strict validation
  }),

  position: defineCollection({
    loader: glob({ pattern: '*.md', base: sub('positions/') }),
    schema: z.object({
      type: z.literal('position'),
      position: z.enum(['setter','outside-hitter','middle-blocker','opposite','libero','defensive-specialist']),
      role: z.string(),
      'physical-profile': z.string().optional(),
      'key-skills': z.array(z.string()).default([]),
      'common-drills': z.array(z.string()).default([]),
      'related-coaches': z.array(z.string()).default([]),
    }).passthrough(),
  }),

  ageLens: defineCollection({
    loader: glob({ pattern: 'age-lens-*.md', base: WIKI }),
    schema: z.object({
      type: z.literal('age-lens'),
      label: z.string(),
      scope: z.string(),
      emphasis: z.array(z.string()).default([]),
      'age-ceilings': z.array(z.string()).default([]),
      sources: z.array(z.string()).min(1),
    }).passthrough(),
  }),

  hub: defineCollection({
    loader: glob({
      pattern: ['philosophy.md','systems.md','practice-planning.md','season-planning.md',
               'mental.md','physical.md','match-prep.md','rules.md','recruiting.md',
               'passing.md','setting.md','hitting.md','blocking.md','serving.md',
               'defense.md','transition.md','cues.md','mental-skills-curriculum.md',
               'practice-ratios.md'],
      base: WIKI,
    }),
    schema: z.object({
      type: z.literal('hub'),
      area: z.string(),
      subtopics: z.array(z.string()).default([]),
    }).passthrough(),
  }),
};
