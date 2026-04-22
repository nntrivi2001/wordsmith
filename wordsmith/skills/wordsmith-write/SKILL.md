---
name: wordsmith-write
description: Writes webnovel chapters in Vietnamese style (default 2000-2500 words). Use when the user asks to write a chapter or runs /wordsmith-write. Runs context, drafting, review, polish, and data extraction. Built-in Contract follows Vietnamese webnovel patterns per STYLE_GUIDE_VN.md.
allowed-tools: Read Write Edit Grep Bash Task
---

# Chapter Writing (Structured Workflow)

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

## Vietnamese Writing Methodology

This skill produces Vietnamese webnovel content following STYLE_GUIDE_VN.md patterns:

### Core Vietnamese Patterns
- **Pronoun system**: Use "mày/tao" between close characters, "tôi/ngài" with strangers, "hắn" for third-person male antagonists
- **Sentence rhythm**: Short punchy sentences for action (1-5 words), longer descriptive sentences for emotions/sensory details
- **Show-don't-tell**: Instead of "cô ấy rất giận" → "Rosa nghiến răng, nắm chặt tay lại đến trắng bóc. Mắt cô nổ đom đóm."
- **Colloquial vs Literary**: Dialogue uses colloquial ("làm gì", "đâu", "vậy"), inner narration uses literary forms
- **Inverted syntax**: Available for archaic/noble character voice ("Ra ngoài hắn ta đi")

### Genre-Specific (Isekai/Xuanhuan) Patterns
- Status card system (thẻ trạng thái): Display stats with Vietnamese formatting
- Level-up pacing: 5% recovery chance on level-up (adjustable)
- Combat flow: Identify enemy → Check status (Giám định) → Evaluate strength → Tactical decision → Action → Result + loot/exp

### Chapter Structure per VN Style
- Opening: Action hook ("Bốp! Choang!"), dialogue hook, status card intro, or descriptive scene
- Body: Mixed sentence lengths, dialogue + narration, "***" for major scene breaks
- End: Cliffhanger using incomplete action, twist revelation, or "—0o0—" mid-scene break

## Goals

- Produce publishable chapters through a stable workflow: prioritize `Chapters/Chapter{NNNN}-{title_safe}.md`, fall back to `Chapters/Chapter{NNNN}.md` when untitled.
- Default chapter word count target: 2000-2500 words (follows user or outline agreement when explicitly overridden).
- Ensure review, polish, and data writeback form a complete closed loop, avoiding "write and discard context."
- Output structured data directly consumable by subsequent chapters: `review_metrics`, `summaries`, `chapter_meta`.

## Execution Principles

1. Verify input completeness before entering the writing workflow; block immediately if critical inputs are missing.
2. Review and data writeback are hard steps; `--fast`/`--minimal` only allows degradation of optional steps.
3. Reference materials are loaded strictly on-demand per step, not all at once.
4. Step 2B and Step 4 have separate responsibilities: 2B only handles style translation, 4 only handles issue fixing and quality control.
5. On any step failure, prioritize minimal rollback rather than rerunning the entire workflow.

## Mode Definitions

- `/wordsmith-write`：Step 1 → 2A → 2B → 3 → 4 → 5 → 6
- `/wordsmith-write --fast`：Step 1 → 2A → 3 → 4 → 5 → 6 (skip 2B)
- `/wordsmith-write --minimal`：Step 1 → 2A → 3 (only 3 basic reviews) → 4 → 5 → 6

Minimum deliverables (all modes):
- `Chapters/Chapter{NNNN}-{title_safe}.md` or `Chapters/Chapter{NNNN}.md`
- `index.db.review_metrics` new record (including `overall_score`)
- `.webnovel/summaries/ch{NNNN}.md`
- `.webnovel/state.json` progress and `chapter_meta` updates

### Workflow Hard Constraints (Prohibited Items)

- **No parallel execution**: Do not merge two Steps into one action (e.g., doing 2A and 3 simultaneously).
- **No step skipping**: Do not skip Steps not marked as skippable in the mode definition.
- **No temporary renaming**: Do not rewrite a Step's output to a non-standard filename or format.
- **No self-created modes**: `--fast`/`--minimal` only allows trimming steps as defined above; do not create hybrid modes, "half-steps" or "simplified versions."
- **No self-review substitution**: Step 3 review must be executed by a Task subagent; the main workflow must not inline falsified review conclusions.
- **No source code probing**: Script invocation methods are based on command examples in this document and the data-agent document; when commands fail, check logs to locate issues, do not dig into source code for invocation methods.

## Reference Loading Levels (strict, lazy)

- L0: Before entering the corresponding step, do not load any reference files.
- L1: Each step only loads "required" files for that step.
- L2: Load "conditionally required/optional" files only when triggering conditions are met.

Path conventions:
- `references/...` is relative to the current skill directory.
- `../../references/...` points to globally shared references.

## References (File-by-File Index)

### Root Directory

- `references/step-3-review-gate.md`
  - Purpose: Step 3 review invocation template, aggregation format, database JSON specification.
  - Trigger: Step 3 required read.
- `references/step-5-debt-switch.md`
  - Purpose: Step 5 debt interest switch rules (default off).
  - Trigger: Step 5 required read.
- `../../references/shared/core-constraints.md`
  - Purpose: Step 2A writing hard constraints (outline is law / settings are physics / inventions need recognition).
  - Trigger: Step 2A required read.
- `references/polish-guide.md`
  - Purpose: Step 4 issue fixing, Anti-AI and No-Poison rules.
  - Trigger: Step 4 required read.
- `references/writing/typesetting.md`
  - Purpose: Step 4 mobile reading typesetting and pre-publish checklist.
  - Trigger: Step 4 required read.
- `references/style-adapter.md`
  - Purpose: Step 2B style translation rules; does not alter plot facts.
  - Trigger: Step 2B required read when executed (`--fast`/`--minimal` skip).
- `references/style-variants.md`
  - Purpose: Step 1 (built-in Contract) opening/hook/rhythm variants and repetition risk control.
  - Trigger: Step 1 loads when differentiated design is needed.
- `../../references/reading-power-taxonomy.md`
  - Purpose: Step 1 (built-in Contract) hook, thrill point, micro-redemption taxonomy.
  - Trigger: Step 1 loads when reader-pull design is needed.
- `../../references/genre-profiles.md`
  - Purpose: Step 1 (built-in Contract) rhythm thresholds and hook preferences by genre.
  - Trigger: Step 1 loads when `state.project.genre` is known.
- `references/writing/genre-hook-payoff-library.md`
  - Purpose: Quick library for esports/livestream/Cthulhu genre hooks and micro-redemptions.
  - Trigger: Step 1 required read when genre matches `esports/livestream/cosmic-horror`.

### writing (Issue-Directed Additional Reading)

- `references/writing/combat-scenes.md`
  - Trigger: Combat chapters or review hits "combat readability/camera confusion."
- `references/writing/dialogue-writing.md`
  - Trigger: Review hits OOC, dialogue instruction style, poor dialogue recognition.
- `references/writing/emotion-psychology.md`
  - Trigger: Abrupt emotional transitions, motivation gaps, weak empathy.
- `references/writing/scene-description.md`
  - Trigger: Vague scenes, unclear spatial orientation, abrupt scene cuts.
- `references/writing/desire-description.md`
  - Trigger: Weak protagonist goal, insufficient desire drive.

## Tool Strategy (On-Demand)

- `Read/Grep`: Read `state.json`, outline, chapter body, and reference files.
- `Bash`: Run `extract_chapter_context.py`, `index_manager`, `workflow_manager`.
- `Task`: Invoke `context-agent`, review subagent, `data-agent` for parallel execution.

## Interaction Workflow

### Step 0: Pre-Check and Minimal Context Loading

Required actions:
- Parse the actual book project root (book project_root): must contain `.webnovel/state.json`.
- Validate core inputs: `Outline/Master.md`, `${CLAUDE_PLUGIN_ROOT}/scripts/extract_chapter_context.py` exist.
- Normalize variables:
  - `WORKSPACE_ROOT`: Claude Code workspace root (may be the parent directory of the book project, e.g., `D:\wk\xiaoshuo`)
  - `PROJECT_ROOT`: Actual book project root (must contain `.webnovel/state.json`, e.g., `D:/wk/novels/mortal-capital-theory`)
  - `SKILL_ROOT`: Skill directory (fixed `${CLAUDE_PLUGIN_ROOT}/skills/wordsmith-write`)
  - `SCRIPTS_DIR`: Scripts directory (fixed `${CLAUDE_PLUGIN_ROOT}/scripts`)
  - `chapter_num`: Current chapter number (integer)
  - `chapter_padded`: Four-digit chapter number (e.g., `0007`)

Environment setup (before bash command execution):
```bash
export WORKSPACE_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
export SCRIPTS_DIR="${CLAUDE_PLUGIN_ROOT:?CLAUDE_PLUGIN_ROOT is required}/scripts"
export SKILL_ROOT="${CLAUDE_PLUGIN_ROOT:?CLAUDE_PLUGIN_ROOT is required}/skills/wordsmith-write"

python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${WORKSPACE_ROOT}" preflight
export PROJECT_ROOT="$(python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${WORKSPACE_ROOT}" where)"
```

**Hard threshold**: `preflight` must succeed. It uniformly validates `SKILL_ROOT`/`SCRIPTS_DIR` derived from `CLAUDE_PLUGIN_ROOT`, `webnovel.py`, `extract_chapter_context.py`, and parsed `PROJECT_ROOT`. Any failure immediately blocks and prompts to fix missing items first.

Output:
- List of "ready inputs" and "missing inputs"; if missing, block and prompt to complete first.

### Step 0.5: Workflow Breakpoint Recording (best-effort, non-blocking)

```bash
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" workflow start-task --command wordsmith-write --chapter {chapter_num} || true
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" workflow start-step --step-id "Step 1" --step-name "Context Agent" || true
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" workflow complete-step --step-id "Step 1" --artifacts '{"ok":true}' || true
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" workflow complete-task --artifacts '{"ok":true}' || true
```

Requirements:
- `--step-id` only allows: `Step 1` / `Step 2A` / `Step 2B` / `Step 3` / `Step 4` / `Step 5` / `Step 6`.
- Any recording failure only logs a warning, does not block writing.
- After each Step completes, `complete-step` must also be called (failure does not block).

### Step 1: Context Agent (built-in Context Contract, generates direct-write execution package)

Invoke Task with `context-agent`, parameters:
- `chapter`
- `project_root`
- `storage_path=.webnovel/`
- `state_file=.webnovel/state.json`

Hard requirements:
- If `state` or outline is unavailable, immediately block and return missing items.
- Output must simultaneously include:
  - 7-section mission brief (goal/conflict/continuation/character/scene constraints/foreshadowing/reader-pull);
  - Context Contract all fields (goal/resistance/cost/chapter changes/unclosed issues/opening type/emotional rhythm/information density/transition chapter judgment/reader-pull design);
  - "Writing execution package" directly consumable by Step 2A (chapter beats, immutable facts list, prohibited items, final checklist).
- When mission brief and contract conflict, the stricter of "outline and setting constraints" prevails.

Output:
- Single "creative execution package" (mission brief + Context Contract + direct-write prompt), directly consumable by Step 2A, not split into a separate Step 1.5.

### Step 2A: Body Drafting

Must load before execution:
```bash
cat "${SKILL_ROOT}/../../references/shared/core-constraints.md"
```

Hard requirements:
- Output only pure body text to the chapter file; if detailed outline already has a chapter title, prioritize `Chapters/Chapter{chapter_padded}-{title_safe}.md`, otherwise fall back to `Chapters/Chapter{chapter_padded}.md`.
- Default execution at 2000-2500 words; if outline marks it as a critical combat chapter/climax chapter/volume-end chapter or user explicitly specifies, follow outline/user priority.
- No placeholder body text (e.g., `[TODO]`, `[pending]`).
- Preserve continuity: if the previous chapter has a clear hook, this chapter must respond (may partially redeem).

Chinese-thinking writing constraints (hard rules):
- **No "English first, then Chinese"**: Do not first organize content using English engineering skeleton (e.g., ABCDE paragraphing, Summary/Conclusion frameworks), then translate to Chinese.
- **Chinese narrative units take priority**: Use "action, reaction, cost, emotion, scene, relationship displacement" as basic narrative units; do not use English structural labels to drive body generation.
- **No English conclusion phrasing**: Body text, review notes, polish notes, change summaries, and final reports must not contain English conclusion headings such as Overall / PASS / FAIL / Summary / Conclusion.
- **English only for machine identifiers**: CLI flags (`--fast`), checker IDs (`consistency-checker`), DB field names (`anti_ai_force_check`), JSON key names, and other immutable interface names remain in English; all others use simplified Chinese.

Output:
- Chapter draft (can proceed to Step 2B or Step 3).

### Step 2B: Style Adaptation (`--fast`/`--minimal` skip)

Must load before execution:
```bash
cat "${SKILL_ROOT}/references/style-adapter.md"
```

Hard requirements:
- Only do expression-layer translation; do not alter plot facts, event sequence, character behavior outcomes, or setting rules.
- Targeted rewriting of "template tone, exposition tone, mechanical tone" to leave problem-fixing space for Step 4.

Output:
- Stylized body text (overwrites original chapter file).

### Step 3: Review (auto routing, must be executed by Task subagent)

Must load before execution:
```bash
cat "${SKILL_ROOT}/references/step-3-review-gate.md"
```

Invocation constraints:
- Must use `Task` to invoke the review subagent; main workflow must not falsify review conclusions.
- Can launch reviews in parallel, aggregate `issues/severity/overall_score` uniformly.
- Default uses `auto` routing: dynamically selects reviewers based on "this chapter's execution contract + body signals + outline labels."

Core reviewers (always execute):
- `consistency-checker`
- `continuity-checker`
- `ooc-checker`

Conditional reviewers (execute when `auto` hits):
- `reader-pull-checker`
- `high-point-checker`
- `pacing-checker`

Mode descriptions:
- Standard/`--fast`: Core 3 + conditional reviewers hit by auto
- `--minimal`: Only runs core 3 (ignores conditional reviewers)

Review metrics must be saved to database (required):
```bash
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" index save-review-metrics --data "@${PROJECT_ROOT}/.webnovel/tmp/review_metrics.json"
```

review_metrics field constraints (current workflow agreement only passes the following fields):
```json
{
  "start_chapter": 100,
  "end_chapter": 100,
  "overall_score": 85.0,
  "dimension_scores": {"thrill_density": 8.5, "setting_consistency": 8.0, "rhythm_control": 7.8, "character_portrayal": 8.2, "coherence": 9.0, "reader_pull": 8.7},
  "severity_counts": {"critical": 0, "high": 1, "medium": 2, "low": 0},
  "critical_issues": ["issue_description"],
  "report_file": "review_report/ch100-100_review_report.md",
  "notes": "single_string; selected_checkers / timeline_gate / anti_ai_force_check and other extended info compressed into single-line text written to this field"
}
```
- `notes` in the current execution contract must be a single string; do not pass objects or arrays.
- Current workflow does not additionally pass other top-level fields; script side does not add new hard validation here.

Hard requirements:
- `--minimal` must also produce `overall_score`.
- Cannot proceed to Step 5 if `review_metrics` not saved to database.

### Step 4: Polish (issue fixing priority)

Must load before execution:
```bash
cat "${SKILL_ROOT}/references/polish-guide.md"
cat "${SKILL_ROOT}/references/writing/typesetting.md"
```

Execution order:
1. Fix `critical` (required)
2. Fix `high` (if cannot fix, record deviation)
3. Handle `medium/low` (choose by benefit)
4. Execute Anti-AI and No-Poison full-text final check (must output `anti_ai_force_check: pass/fail`)

Output:
- Polished body text (overwrites chapter file)
- Change summary (must include: fixed items, retained items, deviation, `anti_ai_force_check`)

### Step 5: Data Agent (state and index writeback)

Use Task to invoke `data-agent`, parameters:
- `chapter`
- `chapter_file` must pass actual chapter file path; if detailed outline already has chapter title, prioritize passing `Chapters/Chapter{chapter_padded}-{title_safe}.md`, otherwise pass `Chapters/Chapter{chapter_padded}.md`
- `review_score=Step 3 overall_score`
- `project_root`
- `storage_path=.webnovel/`
- `state_file=.webnovel/state.json`

Data Agent default sub-steps (all execute):
- A. Load context
- B. AI entity extraction
- C. Entity disambiguation
- D. Write state/index
- E. Write chapter summary
- F. AI scene slicing
- G. RAG vector index (`rag index-chapter --scenes ...`)
- H. Style sample evaluation (`style extract --scenes ...`, only when `review_score >= 80`)
- I. Debt interest (default skip)

`--scenes` source priority (G/H steps share):
1. Prioritize getting from `index.db` scenes records (written by Step F)
2. Next, construct from body by slicing `start_line`/`end_line`
3. Last resort: single-scene degradation (entire chapter as one scene)

Step 5 failure isolation rules:
- If G/H failure cause is `--scenes` missing, scene empty, scene JSON format error: only re-run G/H sub-steps, do not rollback or rerun Step 1-4.
- If A-E failure (state/index/summary write failure): only rerun Step 5, do not rollback passed Step 1-4.
- Do not rerun the entire writing chain due to RAG/style sub-step failures.

Post-execution checks (minimal whitelist):
- `.webnovel/state.json`
- `.webnovel/index.db`
- `.webnovel/summaries/ch{chapter_padded}.md`
- `.webnovel/observability/data_agent_timing.jsonl` (observability log)

Performance requirements:
- Read the latest entry from timing log;
- When `TOTAL > 30000ms`, output the 2-3 slowest sub-steps with reason explanation.

Observability log descriptions:
- `call_trace.jsonl`: Outer workflow call chain (agent startup, queuing, environment probing, etc. system overhead).
- `data_agent_timing.jsonl`: Data Agent internal sub-step timing.
- When outer total time is much greater than inner timing sum, default attribution is agent startup and environment probing overhead; do not misjudge as body text or data processing slow.

Debt interest:
- Default off, only executes when user explicitly requests or tracking is enabled (see `step-5-debt-switch.md`).

### Step 6: Git Backup (can fail but requires explanation)

```bash
git add .
git -c i18n.commitEncoding=UTF-8 commit -m "Chapter {chapter_num}: {title}"
```

Rules:
- Commit timing: execute last after all verification, writeback, and cleanup are complete.
- Commit message default in Chinese, format: `Chapter {chapter_num}: {title}`.
- If commit fails, must give failure reason and range of uncommitted files.

## Completeness Gate (must pass)

Before ending the workflow, the following must be satisfied:

1. Chapter body file exists and is non-empty: `Chapters/Chapter{chapter_padded}-{title_safe}.md` or `Chapters/Chapter{chapter_padded}.md`
2. Step 3 has produced `overall_score` and `review_metrics` successfully saved to database
3. Step 4 has processed all `critical`; unfixed `high` items have deviation records
4. Step 4's `anti_ai_force_check=pass` (based on full-text check; cannot proceed to Step 5 when fail)
5. Step 5 has written back `state.json`, `index.db`, `summaries/ch{chapter_padded}.md`
6. If performance observability is enabled, latest timing record has been read and conclusions output

## Verification and Delivery

Execution checks:

```bash
test -f "${PROJECT_ROOT}/.webnovel/state.json"
test -f "${PROJECT_ROOT}/Chapters/Chapter${chapter_padded}.md"
test -f "${PROJECT_ROOT}/.webnovel/summaries/ch${chapter_padded}.md"
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" index get-recent-review-metrics --limit 1
tail -n 1 "${PROJECT_ROOT}/.webnovel/observability/data_agent_timing.jsonl" || true
```

Success criteria:
- Chapter file, summary file, and state file are all present and readable.
- Review scores are traceable; `overall_score` matches Step 5 input.
- Polishing has not broken outline and setting constraints.

## Failure Handling (Minimal Rollback)

Trigger conditions:
- Chapter file missing or empty;
- Review results not saved to database;
- Data Agent critical deliverables missing;
- Polishing introduced setting conflicts.

Recovery workflow:
1. Only rerun the failed step; do not rollback passed steps.
2. Common minimal fixes:
   - Missing review: only rerun Step 3 and save to database;
   - Polish distortion: restore Step 2A output and redo Step 4;
   - Missing summary/state: only rerun Step 5;
3. Re-execute all "Verification and Delivery" checks; end after passing.
