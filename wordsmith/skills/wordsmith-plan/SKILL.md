---
name: wordsmith-plan
description: Builds volume and chapter outlines for Vietnamese wordsmiths from the total outline, inherits creative constraints, and prepares writing-ready chapter plans. Use when the user asks for outlining or runs /wordsmith-plan. Strand/Cool-point methodology follows STYLE_GUIDE_VN.md patterns.
---

# Outline Planning

## IMPORTANT: Before Executing — Read STYLE_GUIDE_VN.md First

**You MUST read `../../STYLE_GUIDE_VN.md` before starting any task.**

The STYLE_GUIDE_VN.md contains authoritative Vietnamese writing patterns that MUST be applied:
- Section 11: QUY TẮC CỤ THỂ (Units, Punctuation, Sentence Structure)
- Section 13: PATTERN ANALYSIS TỪ 4 NGUỒN TRUYỆN (Primary source: Ta Dung Nhin Vo Lam Toang)

**8 Error Types to Avoid (from user feedback):**
1. Units: Use mét/cm/km/kg (NOT trượng, dặm, tấc, thốn, ly)
2. Vocabulary: Match context ("đứa" not "đồng" for people)
3. Punctuation: Use — (single) NOT —— (double) for dialogue
4. Sentence structure: Must have subject + predicate (NO fragmented sentences)
5. Spelling: "ken két" not "kẽ kẽy"
6. Connectors: Use và/nhưng/nên/vì/sau đó/rồi/thì/mà
7. Subject: Descriptions MUST have explicit subject
8. Natural Vietnamese: Use natural words, not machine-translated Sino-Vietnamese

**Key Patterns from Ta Dung Nhin Vo Lam Toang:**
- Dialogue: "Nội dung" + (action tag) — no ——
- Inner thoughts: Third-person narrative without quotes, use "cậu" for self
- Scene breaks: --- for major, *— Hết Chương X —* for chapter end
- First-person: "cậu/mình" in internal monologue, "tao/mày" for close relationships
- Slang: "vãi", "cứt", "bro", "(@ v @)" acceptable in GenZ contexts

## Vietnamese Methodology

Vietnamese wordsmith planning follows STYLE_GUIDE_VN.md patterns:

### Strand Distribution (VN Webnovel)
- **Quest Strand** (55-65%): Mainline progress - breakthrough, complete mission, obtain treasure
- **Fire Strand** (20-30%): Emotional/relationships - female lead interaction, master-disciple conflict, team dynamics  
- **Constellation Strand** (10-20%): Worldbuilding/mysteries - ancient secrets, villain schemes, world truth reveals

### Cool-Point Density (VN Style)
- **Regular chapters**: 1-2 small cool points (intensity 2-3) - action punch, status reveal
- **Key chapters**: 2-3 cool points, at least 1 medium (intensity 4-5) - emotional beats, relationship shifts
- **Climax chapters**: 3-4 cool points, at least 1 large (intensity 6-7) - major revelations, victories

### Chapter-End Hook Types (per VN pattern)
- Suspense hook: Raise questions, create crisis
- Promise hook: Preview rewards, hint at turning point
- Emotional hook: Relationship changes, character crisis
- Cliffhanger: Incomplete action, twist revelation, "—0o0—" mid-break

### Genre-Specific Planning (Isekai/Xuanhuan)
- Status card system: Include "thẻ trạng thái" reveals at appropriate beats
- Level-up triggers: Plan 5% recovery chance moments
- Combat chapters: Identify → Giám định (check status) → Evaluate → Tactical decision → Action → Result

Purpose: refine the master outline into volume + chapter outlines. Do not redesign the global story.
Setting policy: First build the setting baseline from master outline + worldview based on init output; then after volume outline is complete, incrementally add to the existing setting files.

## Project Root Guard
- Claude Code's "workspace root directory" does not necessarily equal "book project root". Common structure: workspace is `D:/wk/novels`, book project is `D:/wk/novels/mortal-capital-theory`.
- Must first resolve `PROJECT_ROOT` to the actual book project root (must contain `.wordsmith/state.json`), all subsequent read/write paths are relative to this directory.

Environment setup (before bash command execution):
```bash
export WORKSPACE_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"

if [ -z "${CLAUDE_PLUGIN_ROOT}" ] || [ ! -d "${CLAUDE_PLUGIN_ROOT}/skills/wordsmith-plan" ]; then
  echo "ERROR: CLAUDE_PLUGIN_ROOT not set or directory missing: ${CLAUDE_PLUGIN_ROOT}/skills/wordsmith-plan" >&2
  exit 1
fi
export SKILL_ROOT="${CLAUDE_PLUGIN_ROOT}/skills/wordsmith-plan"

if [ -z "${CLAUDE_PLUGIN_ROOT}" ] || [ ! -d "${CLAUDE_PLUGIN_ROOT}/scripts" ]; then
  echo "ERROR: CLAUDE_PLUGIN_ROOT not set or directory missing: ${CLAUDE_PLUGIN_ROOT}/scripts" >&2
  exit 1
fi
export SCRIPTS_DIR="${CLAUDE_PLUGIN_ROOT}/scripts"

export PROJECT_ROOT="$(python "${SCRIPTS_DIR}/wordsmith.py" --project-root "${WORKSPACE_ROOT}" where)"
```

## References (Step-by-Step Navigation)

- Step 3 (required reading, beat table template): [Outline-volume-beat-table.md](../../templates/output/Outline-volume-beat-table.md)
- Step 4.5 (required reading, timeline template): [Outline-volume-timeline.md](../../templates/output/Outline-volume-timeline.md)
- Step 4 (required reading, genre configuration): [genre-profiles.md](../../references/genre-profiles.md)
- Step 4 (required reading, Strand rhythm): [strand-weave-pattern.md](../../references/shared/strand-weave-pattern.md)
- Step 4 (optional, if cool-point structure needs refinement): [cool-points-guide.md](../../references/shared/cool-points-guide.md)
- Step 5/6 (optional, conflict intensity layering): [conflict-design.md](references/outlining/conflict-design.md)
- Step 5 (optional, if hooks/rhythm need detailed breakdown): [reading-power-taxonomy.md](../../references/reading-power-taxonomy.md)
- Step 6 (optional, chapter micro-structure refinement): [chapter-planning.md](references/outlining/chapter-planning.md)
- Step 4/5 (optional, esports/livestream/Cthulhu): [genre-volume-pacing.md](references/outlining/genre-volume-pacing.md)
- Archive (not in main flow): `references/outlining/outline-structure.md`, `references/outlining/plot-frameworks.md`

## Reference Loading Levels (strict, lazy)

Use progressive disclosure and load only what current step requires:
- L0: No references before scope/volume is confirmed.
- L1: Before each step, load only the "required reading" items in **References (Step-by-Step Navigation)**.
- L2: Load optional items only when the trigger condition applies.

## Workflow
1. Load project data.
2. Build setting baseline from master outline + worldview (in-place incremental).
3. Select volume and confirm scope.
4. Generate volume beat sheet.
4.5. Generate volume timeline.
5. Generate volume skeleton.
6. Generate chapter outlines in batches.
7. Enrich existing setting files from volume outline (in-place incremental).
8. Validate + save + update state.

## 1) Load project data
```bash
cat "$PROJECT_ROOT/.wordsmith/state.json"
cat "$PROJECT_ROOT/Outline/Master.md"
```

Optional (only if they exist):
- `Settings/Protagonists.md`
- `Settings/FemaleLead.md`
- `Settings/Villains.md`
- `Settings/Worldview.md`
- `Settings/PowerSystem.md`
- `Settings/ProtagonistCard.md`
- `.wordsmith/idea_bank.json` (inherit constraints)

If the master outline file lacks volume ranges / core conflict / climax, ask the user to fill those before proceeding.

## 2) Build setting baseline from master outline + worldview
Goal: Without overturning existing content, bring the setting files from "skeleton template" to "plannable and writable" baseline state.

Input sources:
- `Outline/Master.md`
- `Settings/Worldview.md`
- `Settings/PowerSystem.md`
- `Settings/ProtagonistCard.md`
- `Settings/Villains.md`

Execution rules (mandatory):
- Only do incremental additions, do not clear or rewrite entire files.
- Prioritize filling "executable fields": character positioning, faction relationships, ability boundaries, cost rules, villain hierarchy mapping.
- If master outline conflicts with existing settings, list conflicts first and block, wait for user arbitration before making changes.

Minimum baseline requirements:
- `Settings/Worldview.md`: World rule boundaries, social structure, key location purposes.
- `Settings/PowerSystem.md`: Realm chain/ability limits/costs and cooldowns.
- `Settings/ProtagonistCard.md`: Desires, flaws, initial resources and limitations.
- `Settings/Villains.md`: Small/medium/large villain hierarchy and protagonist mirror relationship.

## 3) Select volume
- Offer choices from the master outline (volume name + chapter range).
- Confirm any special requirement (tone, POV emphasis, romance, etc.).
If the master outline lacks volume names/chapter ranges/core conflicts/volume-end climax, first ask supplementary questions and update it, then continue.

## 4) Generate volume beat sheet
Goal: First lock down this volume's "promise → escalating crisis → mid-volume reversal → lowest point → big payoff + new hook" to avoid mid-volume drift.

Load template:
```bash
cat "${SKILL_ROOT}/../../templates/output/Outline-volume-beat-table.md"
```

Must satisfy (hard requirements):
- **Mid-volume reversal (required)**: Cannot be left empty; if none exists, write `none (reason:...)`
- **Crisis chain**: At least 3 escalations (rows 1-3 in table cannot be empty)
- **Volume-end new hook**: Must be able to land on "the unclosed issue at end of last chapter"

Write output:
```bash
@'
{beat_sheet_content}
'@ | Set-Content -Encoding UTF8 "$PROJECT_ROOT/Outline/Volume_{volume_id}-beat-table.md"
```

Completion criteria:
- `Outline/Volume_{volume_id}-beat-table.md` exists and is not empty
- Step 4/5 can directly reference Catalyst / mid-volume reversal / lowest point / big payoff / new hook to anchor rhythm

## 4.5) Generate volume timeline

Goal: Establish a timeline baseline for this volume, ensure logical consistency of time progression between chapters, avoid time-jump problems like "disaster in Chapter 1, fighting in Chapter 2".

Load template:
```bash
cat "${SKILL_ROOT}/../../templates/output/Outline-volume-timeline.md"
```

Must satisfy (hard requirements):
- **Time baseline (required)**: Clearly state the time system used in this volume (post-apocalypse Day X / immortal calendar date / modern date)
- **Volume time span (required)**: The time range covered by this volume
- **Key countdown events**: If there are time-limited events (supplies exhausted / tournament start / deadline), must list and mark D-N

Write output:
```bash
@'
{timeline_content}
'@ | Set-Content -Encoding UTF8 "$PROJECT_ROOT/Outline/Volume_{volume_id}-timeline.md"
```

Completion criteria:
- `Outline/Volume_{volume_id}-timeline.md` exists and is not empty
- Time baseline and volume span are clearly stated
- If countdown events exist, they are listed in the table

## 5) Generate volume skeleton
Load genre profile and apply standards:
```bash
cat "${SKILL_ROOT}/../../references/genre-profiles.md"
cat "${SKILL_ROOT}/../../references/shared/strand-weave-pattern.md"
```

Optional (only if cool-point structure needs refinement):
```bash
cat "${SKILL_ROOT}/../../references/shared/cool-points-guide.md"
```

Optional (only if volume-level conflict chain and intensity layering needs reinforcement):
```bash
cat "${SKILL_ROOT}/references/outlining/conflict-design.md"
```

Load beat sheet (must exist):
```bash
cat "$PROJECT_ROOT/Outline/Volume_{volume_id}-beat-table.md"
```

Extract for current genre:
- Strand ratio (Quest/Fire/Constellation)
- Cool-point density standards (minimum/recommended per chapter)
- Hook type preferences

### Strand Weave Planning Strategy
Based on genre profile, distribute chapters:
- **Quest Strand** (mainline progress): 55-65% of chapters
  - Clear goals, visible progress, measurable milestones
  - Examples: breakthrough, complete mission, obtain treasure
- **Fire Strand** (emotion/relationships): 20-30% of chapters
  - Character relationship changes, emotional conflicts, team dynamics
  - Examples: interact with female lead, master-disciple conflict, brotherly betrayal
- **Constellation Strand** (world/mysteries): 10-20% of chapters
  - Worldbuilding reveals, foreshadowing, mystery advancement
  - Examples: discover ancient secret, reveal villain's scheme, world truth

**Weaving pattern** (recommended):
- Switch dominant Strand every 3-5 chapters
- Climax chapters can have multiple Strands intertwined
- Last 3-5 chapters of volume focus on Quest Strand

For esports/livestream/Cthulhu, apply dedicated volume pacing template:
```bash
cat "${SKILL_ROOT}/references/outlining/genre-volume-pacing.md"
```

### Cool-Point Density Planning Strategy
Based on genre profile:
- **Regular chapters**: 1-2 small cool points (intensity 2-3)
- **Key chapters**: 2-3 cool points, at least 1 medium cool point (intensity 4-5)
- **Climax chapters**: 3-4 cool points, at least 1 large cool point (intensity 6-7)

**Distribution rule**:
- At least 1 key chapter every 5-8 chapters
- At least 1 climax chapter per volume (usually at volume end)

### Constraint Trigger Planning Strategy
If idea_bank.json exists:
```bash
cat "$PROJECT_ROOT/.wordsmith/idea_bank.json"
```

Calculate trigger frequency:
- **Anti-trope rules**: Trigger once every N chapters
  - N = max(5, total chapters / 10)
  - Example: 50-chapter volume → trigger every 5 chapters
  - Example: 100-chapter volume → trigger every 10 chapters
- **Hard constraints**: Throughout the entire volume, reflected in chapter goals/cool-point design
- **Protagonist flaws**: At least 2 times as conflict source per volume
- **Villain mirror**: Villain-appearing chapters must reflect mirror contrast

Use this template and fill from master outline + idea_bank:

```markdown
# Volume {volume_id}: {volume_name}

> Chapter range: Chapter {start} - {end}
> Core conflict: {conflict}
> Volume-end climax: {climax}

## Volume Summary
{2-3 paragraph overview}

## Key Characters and Villains
- Main appearing characters:
- Villain hierarchy:

## Strand Weave Planning
| Chapter Range | Dominant Strand | Content Summary |
|-------------|----------------|-----------------|

## Cool-Point Density Planning
| Chapter | Cool-Point Type | Specific Content | Intensity |
|---------|----------------|------------------|-----------|

## Foreshadowing Planning
| Chapter | Operation | Foreshadowing Content |
|---------|-----------|----------------------|

## Constraint Trigger Planning (if applicable)
- Anti-trope rules: Trigger once every N chapters
- Hard constraints: Throughout entire volume
```

## 6) Generate chapter outlines (batched)
Batching rule:
- ≤20 chapters: 1 batch
- 21–40 chapters: 2 batches
- 41–60 chapters: 3 batches
- >60 chapters: 4+ batches

Optional (only if hooks/rhythm need detailed breakdown):
```bash
cat "${SKILL_ROOT}/../../references/reading-power-taxonomy.md"
```

Optional (only if chapter micro-structure/title strategy needs refinement):
```bash
cat "${SKILL_ROOT}/references/outlining/chapter-planning.md"
```

### Chapter generation strategy
For each chapter, determine:

**1. Strand assignment** (follow volume skeleton distribution)
- Quest: Mainline mission progress, goal achievement, ability improvement
- Fire: Character relationships, emotional conflicts, team dynamics
- Constellation: World reveals, foreshadowing, mystery advancement

**2. Cool-point design** (based on Strand and position)
- Quest Strand → Achievement cool-points (face-slapping, comeback, breakthrough)
- Fire Strand → Emotional cool-points (recognition, protection, confession)
- Constellation Strand → Revelation cool-points (truth, prophecy, identity)

**3. Hook design** (based on next chapter's Strand)
- Suspense hook: Raise questions, create crisis
- Promise hook: Preview rewards, hint at turning point
- Emotional hook: Relationship changes, character crisis

**4. Villain hierarchy** (based on volume skeleton)
- None: Daily chapters, cultivation chapters, relationship chapters
- Small: Minor conflict, minor villain, local confrontation
- Medium: Medium villain appears, important conflict, intermediate-stage confrontation
- Large: Large villain appears, core conflict, volume-level climax

**5. Key entities** (new or important)
- New character: Name + one-sentence positioning
- New location: Name + one-sentence description
- New item: Name + function
- New faction: Name + stance

**6. Constraint check** (if idea_bank exists)
- Does it trigger anti-trope rules?
- Does it reflect hard constraints?
- Does it showcase protagonist flaws?
- Does it reflect villain mirror?

Chapter format (include villain hierarchy for context-agent):

```markdown
### Chapter {N}: {title}
- Goal: {within 20 characters}
- Resistance: {within 20 characters}
- Cost: {within 20 characters}
- Time anchor: {post-apocalypse Day X time period/immortal calendar Year X Month X Day/modern date + time period}
- Within-chapter time span: {e.g. 3 hours/half day/1 day}
- Time difference from previous chapter: {e.g. immediate/6 hours/1 day/overnight}
- Countdown status: {Event A D-3 -> D-2 / none}
- Cool-point: {type} - {within 30 characters}
- Strand: {Quest|Fire|Constellation}
- Villain hierarchy: {none/small/medium/large}
- POV/protagonist: {protagonist A/protagonist B/female lead/ensemble}
- Key entities: {new or important appearances}
- Chapter change: {within 30 characters, prioritize quantifiable changes}
- End-of-chapter unclosed question: {within 30 characters}
- Hook: {type} - {within 30 characters}
```

**Time field descriptions**:
- **Time anchor**: The specific time point when this chapter takes place, must be consistent with timeline table
- **Within-chapter time span**: The time length covered by this chapter's content
- **Time difference from previous chapter**: The interval from the end of the previous chapter
  - Immediate: No time gap, directly continues
  - Overnight: Passes night but no more than 12 hours
  - Specific duration: e.g. 6 hours, 1 day, 3 days
- **Countdown status**: If countdown events exist, mark the progress (D-N → D-(N-1))

**Field descriptions**:
- **End-of-chapter unclosed question**: The "unclosed decision/question" that must be preserved at the end of this chapter, used to drive readers to click the next chapter.
  - Rule: Must be consistent with **hook** type/intensity; no mismatch like "hook is very strong but question is very empty".
- **Hook**: The end-of-chapter hook to set up in this chapter (for planning)
  - Example: Suspense hook - mysterious person's identity about to be revealed
  - Meaning: Set up this suspense hook at the end of this chapter
  - Next chapter's context-agent will read chapter_meta[N].hook (actual implemented hook), generate "catch the previous chapter" guidance
  - Hook types reference: Suspense hook | Crisis hook | Promise hook | Emotional hook | Choice hook | Desire hook

Save after each batch:
```bash
@'
{batch_content}
'@ | Add-Content -Encoding UTF8 "$PROJECT_ROOT/Outline/Volume_{volume_id}-detailed-outline.md"
```

## 7) Enrich existing setting files from volume outline
Goal: After volume outline is written, write the new facts from this volume back to "existing setting files" to ensure subsequent writing can read directly.

Input sources:
- `Outline/Volume_{volume_id}-beat-table.md`
- `Outline/Volume_{volume_id}-detailed-outline.md`
- Existing setting files (worldview/power system/character cards/protagonist group/female lead card/villain design)

Write-back strategy (mandatory):
- Only incrementally add relevant paragraphs, do not overwrite entire files.
- New characters: Write to corresponding character card or character group entry (including first appearance chapter, relationships, red lines).
- New factions/locations/rules: Write to worldview or power system corresponding sections.
- New villain hierarchy info: Write to villain design and maintain small/medium/large hierarchy consistency.

Conflict handling (hard rule):
- If volume outline new info conflicts with master outline or confirmed settings, mark `BLOCKER` and stop state update.
- Only after conflict arbitration is completed, allow continuing to update settings and enter save step.

## 8) Validate + save
### Validation checks (must pass all)

**1. Cool-point density check**
- Each chapter ≥1 small cool point (intensity 2-3)
- At least 1 key chapter every 5-8 chapters (intensity 4-5)
- At least 1 climax chapter per volume (intensity 6-7)

**2. Strand ratio check**
Count chapters by Strand and compare with genre profile:
- Quest: Should occupy 55-65%
- Fire: Should occupy 20-30%
- Constellation: Should occupy 10-20%

If deviation > 15%, adjust chapter assignments.

**3. Master outline consistency check**
- Does volume core conflict run through all chapters?
- Is volume-end climax reflected in last 3-5 chapters?
- Do key characters appear as planned?

**4. Constraint trigger frequency check** (if idea_bank exists)
- Anti-trope rules trigger count ≥ total chapters / N (N = max(5, total chapters/10))
- Hard constraints reflected in at least 50% of chapters
- Protagonist flaws at least 2 times as conflict source
- Villain mirror reflected in villain-appearing chapters

**5. Completeness check**
Every chapter must have:
- Goal (within 20 characters)
- Resistance (within 20 characters)
- Cost (within 20 characters)
- Time anchor (required)
- Within-chapter time span (required)
- Time difference from previous chapter (required)
- Countdown status (required if countdown events exist)
- Cool-point (type + within 30 characters description)
- Strand (Quest/Fire/Constellation)
- Villain hierarchy (none/small/medium/large)
- POV/protagonist
- Key entities (at least 1)
- Chapter change (within 30 characters)
- End-of-chapter unclosed question (within 30 characters)
- Hook (type + within 30 characters description)

**6. Timeline consistency check (new)**
- Timeline table file exists: `Outline/Volume_{volume_id}-timeline.md`
- All chapter time anchors are filled in
- Time is monotonically increasing (no going back unless clearly marked as flashback)
- Countdown progresses correctly (D-5 → D-4 → D-3, no skipping)
- Large time jumps (>3 days) must have transition chapter explanation or clear marking

**7. Setting completion check**
- New characters/factions/rules involved in this volume have been written back to existing setting files
- All new entries can be traced back to volume chapter outline chapters
- `BLOCKER` count is 0; if >0, arbitration must be done first, cannot enter state update

Update state (include chapters range):
```bash
python "${SCRIPTS_DIR}/wordsmith.py" --project-root "$PROJECT_ROOT" update-state -- \
  --volume-planned {volume_id} \
  --chapters-range "{start}-{end}"
```

Final check:
- Beat table file written: `Outline/Volume_{volume_id}-beat-table.md`
- Timeline table file written: `Outline/Volume_{volume_id}-timeline.md`
- Chapter outline file written: `Outline/Volume_{volume_id}-detailed-outline.md`
- Settings baseline completed and this volume's incremental additions done (visible in original files)
- Each chapter contains: goal/resistance/cost/time anchor/within-chapter time span/time difference from previous chapter/cool-point/Strand/villain hierarchy/POV/key entities/chapter change/end-of-chapter unclosed question/hook
- Timeline monotonically increasing, countdown progresses correctly
- Consistent with master outline conflicts/climax, constraint trigger frequency reasonable (if idea_bank exists)

### Hard fail conditions (must stop)
- Beat table file does not exist or is empty
- Beat table mid-volume reversal missing (not filled according to "required/none (reason)" rule)
- **Timeline table file does not exist or is empty**
- Chapter outline file does not exist or is empty
- Any chapter lacks: goal/resistance/cost/time anchor/within-chapter time span/time difference from previous chapter/cool-point/Strand/villain hierarchy/POV/key entities/chapter change/end-of-chapter unclosed question/hook
- **Any chapter time fields (time anchor/within-chapter time span/time difference from previous chapter) missing**
- **Time going backward without marking as flashback**
- **Countdown arithmetic conflict (e.g., D-5 directly jumps to D-2)**
- **Significant event occurs with insufficient time gap from previous chapter without reasonable explanation (e.g., establishing faction on post-apocalypse Day 1)**
- Significant conflict with master outline core conflict or volume-end climax
- Setting baseline not completed, or this volume's incremental additions not written back to existing settings
- `BLOCKER` exists unarbitrated
- Constraint trigger frequency insufficient (when idea_bank is enabled)

### Rollback / recovery
If any hard fail triggers:
1. Stop and list the failing items.
2. Re-generate only the failed batch (do not overwrite the whole file).
3. If the last batch is invalid, remove that batch and rewrite it.
4. Only update state after Final check passes.

Next steps:
- Continue planning next volume → /wordsmith-plan
- Start writing → /wordsmith-write
