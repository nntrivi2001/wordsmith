---
name: webnovel-init
description: Deep-initialize a webnovel project. Collects complete creative information through phased interaction, and generates a project skeleton and constraint files ready for planning and writing.
allowed-tools: Read Write Edit Grep Bash Task AskUserQuestion WebSearch WebFetch
---

# Project Initialization (Deep Mode)

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

## Objective

- Collect sufficient information through structured interaction to avoid "generate first, rework later."
- Produce a deployable project skeleton: `.webnovel/state.json`, `Settings/*`, `Outline/master.md`, `.webnovel/idea_bank.json`.
- Ensure that subsequent `/webnovel-plan` and `/webnovel-write` can run directly.

## Execution Principles

1. Collect first, generate later; do not execute `init_project.py` until the sufficiency gate is passed.
2. Ask questions in waves - each round only asks for information that is "currently missing and will block the next step."
3. `Read/Grep/Bash/Task/AskUserQuestion/WebSearch/WebFetch` may be invoked to assist with collection.
4. Do not repeat questions for information the user has already provided; when information conflicts, let the user decide.
5. Deep mode prioritizes completeness - it is acceptable to be slower, but critical fields must never be omitted.

## Reference Loading Levels (strict, lazy)

Use tiered loading to avoid dumping all material at once:

- L0: No references are pre-loaded before the task is confirmed.
- L1: Each phase loads only the "required reading" files for that phase.
- L2: Extended references are loaded only when the genre, golden finger, or creative constraint trigger condition is met.
- L3: Market-trend and time-sensitive materials are loaded only when the user explicitly requests them.

Path conventions:
- `references/...` relative to the current skill directory (`${CLAUDE_PLUGIN_ROOT}/skills/webnovel-init/references/...`).
- `templates/...` relative to the plugin root directory (`${CLAUDE_PLUGIN_ROOT}/templates/...`).
- `../../STYLE_GUIDE_VN.md` for Vietnamese writing methodology patterns.

Default loading manifest:
- L1 (before startup): `references/genre-tropes.md`
- L2 (on demand):
  - Genre template: `templates/genres/{genre}.md`
  - Golden finger: `../../templates/golden-finger-templates.md`
  - World-building: `references/worldbuilding/faction-systems.md`
  - Creative constraints: loaded by trigger per the per-file reference list below
- L3 (explicit request):
  - `references/creativity/market-trends-2026.md`
  - Vietnamese writing patterns: `../../STYLE_GUIDE_VN.md`

## References (Per-File Reference List)

### Root Directory

- `references/genre-tropes.md`
  - Purpose: Step 1 genre normalization and genre-trait prompting.
  - Trigger: Required reading for all projects.
- `references/system-data-flow.md`
  - Purpose: Consistency check between initialization output and the downstream `/plan` and `/write` data flow.
  - Trigger: Required reading for the Step 0 pre-check.

### worldbuilding

- `references/worldbuilding/character-design.md`
  - Purpose: Step 2 supplementary questions for character dimensions (goal, flaw, motivation, contrast).
  - Trigger: Load when the user's character information is abstract or flat.
- `references/worldbuilding/faction-systems.md`
  - Purpose: Step 4 faction landscape and organizational hierarchy design.
  - Trigger: Loaded by default in Step 4.
- `references/worldbuilding/power-systems.md`
  - Purpose: Step 4 power system types and boundary definitions.
  - Trigger: Load when the genre involves cultivation / fantasy / high martial arts / supernatural powers.
- `references/worldbuilding/setting-consistency.md`
  - Purpose: Step 6 setting conflict check before the consistency recap.
  - Trigger: Loaded by default in Step 6.
- `references/worldbuilding/world-rules.md`
  - Purpose: Step 4 world rules and forbidden-item collation.
  - Trigger: Loaded by default in Step 4.

### creativity

- `references/creativity/creativity-constraints.md`
  - Purpose: Step 5 creative constraint pack master schema.
  - Trigger: Required reading in Step 5.
- `references/creativity/category-constraint-packs.md`
  - Purpose: Step 5 constraint pack template selection by platform/genre.
  - Trigger: Required reading in Step 5.
- `references/creativity/creative-combination.md`
  - Purpose: Hybrid genre (A+B) fusion rules.
  - Trigger: Load when the user selects a hybrid genre.
- `references/creativity/inspiration-collection.md`
  - Purpose: Provides selling-point/hook candidates when the user is stuck.
  - Trigger: Load when Step 1 or Step 5 stalls.
- `references/creativity/selling-points.md`
  - Purpose: Step 5 selling-point generation and filtering.
  - Trigger: Required reading in Step 5.
- `references/creativity/market-positioning.md`
  - Purpose: Target-reader/platform positioning and unified commercial semantics.
  - Trigger: Load when the user mentions a platform or commercial goal in Step 1.
- `references/creativity/market-trends-2026.md`
  - Purpose: Time-sensitive market trend reference.
  - Trigger: Load only when the user explicitly requests "reference current trends."
- `references/creativity/anti-trope-xianxia.md`
  - Purpose: Anti-trope library (cultivation / fantasy / high martial arts / western fantasy).
  - Trigger: Load when the genre matches the corresponding mapping.
- `references/creativity/anti-trope-urban.md`
  - Purpose: Anti-trope library (urban / historical).
  - Trigger: Load when the genre matches the corresponding mapping.
- `references/creativity/anti-trope-game.md`
  - Purpose: Anti-trope library (game / sci-fi / apocalypse).
  - Trigger: Load when the genre matches the corresponding mapping.
- `references/creativity/anti-trope-rules-mystery.md`
  - Purpose: Anti-trope library (rule-horror / mystery / supernatural / Cthulhu).
  - Trigger: Load when the genre matches the corresponding mapping.

## Tool Strategy (on demand)

- `Read/Grep`: Read project context and reference files (`README.md`, `CLAUDE.md`, `templates/genres/*`, `references/*`).
- `Bash`: Execute `init_project.py`, file existence checks, minimal validation commands.
- `Task`: Split parallel sub-tasks (e.g. genre mapping, constraint pack candidate generation, file validation).
- `AskUserQuestion`: Used for key conflict adjudication, candidate selection, and final confirmation.
- `WebSearch`: Search for the latest market trends, platform directions, and genre data (domain filtering supported).
- `WebFetch`: Fetch content from confirmed source pages for fact verification.
- External search trigger conditions:
  - The user explicitly requests reference to market trends or platform directions;
  - Creative constraints require "time-sensitive evidence";
  - There is obvious uncertainty about genre information.

## Interaction Flow (Deep)

### Step 0: Pre-check and Context Loading

Environment setup (before executing bash commands):
```bash
export WORKSPACE_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"

if [ -z "${CLAUDE_PLUGIN_ROOT}" ] || [ ! -d "${CLAUDE_PLUGIN_ROOT}/scripts" ]; then
  echo "ERROR: CLAUDE_PLUGIN_ROOT is not set or directory is missing: ${CLAUDE_PLUGIN_ROOT}/scripts" >&2
  exit 1
fi
export SCRIPTS_DIR="${CLAUDE_PLUGIN_ROOT}/scripts"
```

Required actions:
- Confirm the current directory is writable.
- Resolve the scripts directory and confirm the entry point exists (plugin directory only):
  - Fixed path: `${CLAUDE_PLUGIN_ROOT}/scripts`
  - Entry script: `${SCRIPTS_DIR}/webnovel.py`
- Recommended: print the resolved result to avoid writing to the wrong directory:
  - `python "${SCRIPTS_DIR}/webnovel.py" --project-root "${WORKSPACE_ROOT}" where`
- Load minimum references:
  - `references/system-data-flow.md` (for verifying the link between init output and plan/write input)
  - `references/genre-tropes.md`
  - `templates/genres/` (read on demand only after the user selects a genre)

Output:
- A "known information list" and "items to collect" list before entering Deep collection.

### Step 1: Story Core and Commercial Positioning

Required collection:
- Title (a working title is acceptable)
- Genre (A+B hybrid genres supported)
- Target scale (total word count or total chapters)
- One-line story pitch
- Core conflict
- Target reader / platform

Genre set (for normalization and mapping):
- Cultivation/Fantasy: Cultivation | System cultivation | High martial arts | Western fantasy | Infinite loop | Apocalypse | Sci-fi
- Urban/Modern: Urban supernatural | Urban slice-of-life | Urban concept | Realistic fiction | Dark themes | E-sports | Livestream
- Romance: Ancient/Historical romance | Palace intrigue | Sweet campus romance | Wealthy CEO romance | Workplace romance | Republican-era romance | Fantasy romance | Modern romance concepts | Female-oriented mystery | Dramatic romance | Stand-in romance | Large family | Slice-of-life/farming | Historical period
- Special genres: Rule-based horror | Mystery concepts | Mystery/supernatural | Historical ancient | Historical concepts | Game/sports | Wartime/spy thriller | Zhihu short story | Cthulhu

Interaction approach:
- Allow the user to describe freely first, then do a second structured confirmation.
- If the user is stuck, offer 2-4 candidate directions to choose from.

### Step 2: Character Skeleton and Relationship Conflict

Required collection:
- Protagonist name
- Protagonist desire (what they want)
- Protagonist flaw (a flaw that will cost them something)
- Protagonist structure (single protagonist / multiple protagonists)
- Romance configuration (none / single heroine / multiple heroines)
- Antagonist tiers (minor / mid / major) and mirror-opposition one-liner

Optional collection:
- Protagonist archetype tag (growth type / revenge type / prodigy type, etc.)
- Multiple-protagonist role division

### Step 3: Golden Finger and Payoff Mechanism

Required collection:
- Golden finger type (may be "no golden finger")
- Name / system name (leave blank if none)
- Style (hardcore / comedic / dark / restrained, etc.)
- Visibility (who knows about it)
- Irreversible cost (must have a cost, or explicitly state "none + reason")
- Growth pacing (slow burn / medium / fast)

Conditionally required collection:
- If system-type: system personality, leveling pacing
- If reincarnation: time of rebirth, memory completeness
- If inheritance / artifact spirit: assistance limits and action restrictions

### Step 4: World-building and Power Rules

Required collection:
- World scale (single city / multi-region / continent / multi-realm)
- Power system type
- Faction landscape
- Social class and resource distribution

Genre-related collection:
- Currency system and exchange rules
- Sect / organization hierarchy
- Cultivation chain and sub-realms

### Step 5: Creative Constraint Pack (Differentiation Core)

Process:
1. Load anti-trope library based on genre mapping (at most 2 primary relevant libraries).
2. Generate 2-3 creative packs, each containing:
   - One-line selling point
   - 1 anti-trope rule
   - 2-3 hard constraints
   - Protagonist flaw drive (one-liner)
   - Antagonist mirror (one-liner)
   - Opening hook
3. Three-question filter:
   - Why must this genre be written this way?
   - Would a conventional protagonist cause it to collapse?
   - Can the selling point be explained in one sentence without copying a template?
4. Display the five-dimension scoring (see `references/creativity/creativity-constraints.md`, section `8.1 Five-Dimension Scoring`) to assist user decision-making.
5. The user selects the final option, or rejects it with a reason.

Notes:
- If the user requests "align with the current market," external search may be triggered and the timestamp must be noted.

### Step 6: Consistency Recap and Final Confirmation

Must output a "initialization summary draft" for user confirmation:
- Story core (genre / one-line story / core conflict)
- Protagonist core (desire / flaw)
- Golden finger core (ability and cost)
- World core (scale / power / factions)
- Creative constraint core (anti-trope + hard constraints)

Confirmation rules:
- Do not execute generation until the user explicitly confirms.
- If the user only modifies part of it, return to the corresponding Step for minimal re-collection.

## Internal Data Model (Initialization Collection Object)

```json
{
  "project": {
    "title": "",
    "genre": "",
    "target_words": 0,
    "target_chapters": 0,
    "one_liner": "",
    "core_conflict": "",
    "target_reader": "",
    "platform": ""
  },
  "protagonist": {
    "name": "",
    "desire": "",
    "flaw": "",
    "archetype": "",
    "structure": "single-protagonist"
  },
  "relationship": {
    "heroine_config": "",
    "heroine_names": [],
    "heroine_role": "",
    "co_protagonists": [],
    "co_protagonist_roles": [],
    "antagonist_tiers": {},
    "antagonist_level": "",
    "antagonist_mirror": ""
  },
  "golden_finger": {
    "type": "",
    "name": "",
    "style": "",
    "visibility": "",
    "irreversible_cost": "",
    "growth_rhythm": ""
  },
  "world": {
    "scale": "",
    "factions": "",
    "power_system_type": "",
    "social_class": "",
    "resource_distribution": "",
    "currency_system": "",
    "currency_exchange": "",
    "sect_hierarchy": "",
    "cultivation_chain": "",
    "cultivation_subtiers": ""
  },
  "constraints": {
    "anti_trope": "",
    "hard_constraints": [],
    "core_selling_points": [],
    "opening_hook": ""
  }
}
```

## Sufficiency Gate (must pass)

Do not execute `init_project.py` until all of the following conditions are met:

1. Title and genre (may be hybrid) are confirmed.
2. Target scale is calculable (at least one of word count or chapter count).
3. Protagonist name + desire + flaw are complete.
4. World scale + power system type are complete.
5. Golden finger type is confirmed (allowing "no golden finger").
6. Creative constraints are confirmed:
   - At least 1 anti-trope rule
   - At least 2 hard constraints
   - Or the user has explicitly declined and the reason is recorded.

## Project Directory Safety Rules (required)

- `project_root` must be generated by sanitizing the title (remove illegal characters, spaces to `-`).
- If the sanitized result is empty or starts with `.`, automatically prefix with `proj-`.
- Project files must not be generated inside the plugin directory (`${CLAUDE_PLUGIN_ROOT}`).

## Execute Generation

### 1) Run the Initialization Script

```bash
python "${SCRIPTS_DIR}/webnovel.py" init \
  "{project_root}" \
  "{title}" \
  "{genre}" \
  --protagonist-name "{protagonist_name}" \
  --target-words {target_words} \
  --target-chapters {target_chapters} \
  --golden-finger-name "{gf_name}" \
  --golden-finger-type "{gf_type}" \
  --golden-finger-style "{gf_style}" \
  --core-selling-points "{core_points}" \
  --protagonist-structure "{protagonist_structure}" \
  --heroine-config "{heroine_config}" \
  --heroine-names "{heroine_names}" \
  --heroine-role "{heroine_role}" \
  --co-protagonists "{co_protagonists}" \
  --co-protagonist-roles "{co_protagonist_roles}" \
  --antagonist-tiers "{antagonist_tiers}" \
  --world-scale "{world_scale}" \
  --factions "{factions}" \
  --power-system-type "{power_system_type}" \
  --social-class "{social_class}" \
  --resource-distribution "{resource_distribution}" \
  --gf-visibility "{gf_visibility}" \
  --gf-irreversible-cost "{gf_irreversible_cost}" \
  --currency-system "{currency_system}" \
  --currency-exchange "{currency_exchange}" \
  --sect-hierarchy "{sect_hierarchy}" \
  --cultivation-chain "{cultivation_chain}" \
  --cultivation-subtiers "{cultivation_subtiers}" \
  --protagonist-desire "{protagonist_desire}" \
  --protagonist-flaw "{protagonist_flaw}" \
  --protagonist-archetype "{protagonist_archetype}" \
  --antagonist-level "{antagonist_level}" \
  --target-reader "{target_reader}" \
  --platform "{platform}"
```

### 2) Write `idea_bank.json`

Write to `.webnovel/idea_bank.json`:

```json
{
  "selected_idea": {
    "title": "",
    "one_liner": "",
    "anti_trope": "",
    "hard_constraints": []
  },
  "constraints_inherited": {
    "anti_trope": "",
    "hard_constraints": [],
    "protagonist_flaw": "",
    "antagonist_mirror": "",
    "opening_hook": ""
  }
}
```

### 3) Patch Master Outline

Must fill in:
- One-line story
- Core main plot thread / core hidden thread
- Creative constraints (anti-trope, hard constraints, protagonist flaw, antagonist mirror)
- Antagonist tiers
- Key catharsis milestones (2-3 items)

## Validation and Delivery

Run checks:

```bash
test -f "{project_root}/.webnovel/state.json"
find "{project_root}/Settings" -maxdepth 1 -type f -name "*.md"
test -f "{project_root}/Outline/master.md"
test -f "{project_root}/.webnovel/idea_bank.json"
```

Success criteria:
- `state.json` exists and key fields are non-empty (title / genre / target_words / target_chapters).
- Core settings files exist: `worldview.md`, `power-system.md`, `protagonist-profile.md`, `golden-finger-design.md`.
- `master.md` has the core plot thread and constraint fields filled in.
- `idea_bank.json` has been written and matches the final selected option.

## Failure Handling (Minimal Rollback)

Trigger conditions:
- A critical file is missing;
- A critical field in the master outline is missing;
- Constraints are enabled but `idea_bank.json` is missing or its content is inconsistent.

Recovery flow:
1. Fill only the missing fields; do not re-ask everything from scratch.
2. Re-run only the minimal steps:
   - File missing -> re-run `init_project.py`;
   - Master outline missing fields -> patch the master outline only;
   - `idea_bank` inconsistent -> rewrite that file only.
3. Re-validate; finish only after all checks pass.
