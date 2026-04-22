---
name: wordsmith-review
description: Reviews Vietnamese webnovel chapter quality with checker agents and generates reports. Use when the user asks for a chapter review or runs /wordsmith-review. Scoring and patterns follow STYLE_GUIDE_VN.md.
allowed-tools: Read Grep Write Edit Bash Task AskUserQuestion
---

# Quality Review Skill

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

## Vietnamese Review Methodology

This skill evaluates Vietnamese webnovel content per STYLE_GUIDE_VN.md patterns:

### Review Dimensions (aligned with VN webnovel quality)
- **Cool-point density**: Action punch ("Ầm!", "Chết tiệt!"), emotional beats, status card reveals
- **Setting consistency**: Pronoun usage (mày/tao vs tôi/ngài), formality levels maintained
- **Pacing control**: Sentence length variation - fast for action, slow for emotional scenes
- **Character portrayal**: Distinct character voices, body language over telling emotions
- **Continuity**: Consistent pronoun references, timeline logic, "within-chapter time span" alignment
- **Reader pull**: Cliffhanger effectiveness, hook placement per chapter end requirements

### Common Vietnamese Quality Issues
- Pronoun mixing (using formal "tôi" between close friends)
- Telling emotions instead of showing physical tells
- Flat status card descriptions lacking character reaction
- Missing chapter-end hook or unclosed questions
- Action scenes with overly long sentences

### 8 Error Types to Check (from User Feedback)

When reviewing, flag any of these 8 error types:

| # | Error Type | What to Check | Examples |
|---|------------|---------------|----------|
| 1 | **Units** | Metric vs traditional | mét, cm, km, kg (NOT trượng, dặm, tấc, thốn, ly) |
| 2 | **Punctuation** | Em-dash usage | Use `—` NOT `——` (double em-dash) |
| 3 | **Sentence Structure** | Subject + predicate required | No fragments like "Được. Thở được." |
| 4 | **Scene Break Markers** | Correct markers | `***` (major), `—0o0—` (minor), NOT `---` or `*` |
| 5 | **Ellipsis** | Three connected dots | `...` NOT `. . .` |
| 6 | **Vocabulary Accuracy** | Contextually correct words | "từng đứa" (people), not "từng đồng" (money) |
| 7 | **Descriptive Specificity** | Concrete descriptions | Add subjects, make vivid |
| 8 | **Natural Vietnamese Rhythm** | Avoid English/Chinese structures | Natural word order, not calques |

See `references/common-mistakes.md` for detailed SAI/ĐÚNG examples.

## Project Root Guard (must confirm first)

- The Claude Code "workspace root" is not necessarily equal to the "book project root." A common structure: workspace is `D:\wk\xiaoshuo`, book project is `D:\wk\xiaoshuo\FanrenCapitalTheory`.
- Must first resolve the true book project root (which must contain `.webnovel/state.json`); all subsequent read/write paths are relative to that directory.

Environment setup (before executing bash commands):
```bash
export WORKSPACE_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"

if [ -z "${CLAUDE_PLUGIN_ROOT}" ] || [ ! -d "${CLAUDE_PLUGIN_ROOT}/skills/wordsmith-review" ]; then
  echo "ERROR: CLAUDE_PLUGIN_ROOT is not set or directory is missing: ${CLAUDE_PLUGIN_ROOT}/skills/wordsmith-review" >&2
  exit 1
fi
export SKILL_ROOT="${CLAUDE_PLUGIN_ROOT}/skills/wordsmith-review"

if [ -z "${CLAUDE_PLUGIN_ROOT}" ] || [ ! -d "${CLAUDE_PLUGIN_ROOT}/scripts" ]; then
  echo "ERROR: CLAUDE_PLUGIN_ROOT is not set or directory is missing: ${CLAUDE_PLUGIN_ROOT}/scripts" >&2
  exit 1
fi
export SCRIPTS_DIR="${CLAUDE_PLUGIN_ROOT}/scripts"

export PROJECT_ROOT="$(python "${SCRIPTS_DIR}/webnovel.py" --project-root "${WORKSPACE_ROOT}" where)"
```

## 0.5 Workflow Breakpoint (best-effort — must not block the main flow)

> Goal: allow `/wordsmith-resume` to recover based on the real breakpoint. Even if `workflow_manager` errors, only **record a warning** — the review continues.

Recommended (bash):
```bash
python "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" workflow start-task --command wordsmith-review --chapter {end} || true
```

Step mapping (must align with `workflow_manager.py get_pending_steps("wordsmith-review")`):
- Step 1: Load references
- Step 2: Load project state
- Step 3: Call checkers in parallel
- Step 4: Generate review report
- Step 5: Save review metrics to index.db
- Step 6: Write review record back to state.json
- Step 7: Handle critical issues (AskUserQuestion)
- Step 8: Wrap up (complete task)

Step recording template (bash — failure does not block):
```bash
python "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" workflow start-step --step-id "Step 1" --step-name "Load references" || true
python "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" workflow complete-step --step-id "Step 1" --artifacts '{"ok":true}' || true
```

## Review depth

- **Core (default)**: consistency / continuity / ooc / reader-pull
- **Full (key chapters / user request)**: core + high-point + pacing

## Step 1: Load References (on demand)

## References (by step navigation)

- Step 1 (required reading, hard constraints): [core-constraints.md](../../references/shared/core-constraints.md)
- Step 1 (optional, Full or pacing/cool-point issues): [cool-points-guide.md](../../references/shared/cool-points-guide.md)
- Step 1 (optional, Full or pacing/cool-point issues): [strand-weave-pattern.md](../../references/shared/strand-weave-pattern.md)
- Step 1 (optional, only when rework suggestions are needed): [common-mistakes.md](references/common-mistakes.md)
- Step 1 (optional, only when rework suggestions are needed): [pacing-control.md](references/pacing-control.md)

## Reference Loading Levels (strict, lazy)

- L0: Determine review depth (Core / Full) first, then load references.
- L1: Load only "required reading" items from the References section.
- L2: Load "optional" items from the References section only when needed for issue diagnosis.

**Required reading**:
```bash
cat "${SKILL_ROOT}/../../references/shared/core-constraints.md"
```

**Recommended (Full or when needed)**:
```bash
cat "${SKILL_ROOT}/../../references/shared/cool-points-guide.md"
cat "${SKILL_ROOT}/../../references/shared/strand-weave-pattern.md"
```

**Optional**:
```bash
cat "${SKILL_ROOT}/references/common-mistakes.md"
cat "${SKILL_ROOT}/references/pacing-control.md"
```

## Step 2: Load Project State (if it exists)

```bash
cat "$PROJECT_ROOT/.webnovel/state.json"
```

## Step 3: Call Checkers in Parallel (Task)

**Invocation constraints**:
- Must call review subagents via the `Task` tool; the main flow must not inline fake review conclusions.
- Generate the overall assessment and priority ranking only after all subagent results have returned.

**Core**:
- `consistency-checker`
- `continuity-checker`
- `ooc-checker`
- `reader-pull-checker`

**Full additions**:
- `high-point-checker`
- `pacing-checker`

## Step 4: Generate Review Report

Save to: `review-reports/ch{start}-{end}-review.md`

**Report structure (condensed)**:
```markdown
# Chapter {start}-{end} Quality Review Report

## Overall Score
- Cool-point density / Setting consistency / Pacing / Character portrayal / Continuity / Reader pull
- Overall assessment and grade

## Revision Priority
- 🔴 High priority (must fix)
- 🟠 Medium priority (recommended fix)
- 🟡 Low priority (optional improvement)

## Improvement Suggestions
- Actionable fix suggestions
```

**Review metrics JSON (for trend tracking)**:
```json
{
  "start_chapter": {start},
  "end_chapter": {end},
  "overall_score": 48,
  "dimension_scores": {
    "cool_point_density": 8,
    "setting_consistency": 7,
    "pacing_control": 7,
    "character_portrayal": 8,
    "continuity": 9,
    "reader_pull": 9
  },
  "severity_counts": {"critical": 1, "high": 2, "medium": 3, "low": 1},
  "critical_issues": ["Setting self-contradiction"],
  "report_file": "review-reports/ch{start}-{end}-review.md",
  "notes": ""
}
```

Note: Only the review metrics JSON is generated here; persisting to the database is done in Step 5.

## Step 5: Save Review Metrics to index.db (required)

```bash
python "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" index save-review-metrics --data '@review_metrics.json'
```

## Step 6: Write Review Record Back to state.json (required)

Write the review report record back to `state.json.review_checkpoints` for subsequent tracking and tracing (depends on `update_state.py --add-review`):
```bash
python "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" update-state -- --add-review "{start}-{end}" "review-reports/ch{start}-{end}-review.md"
```

## Step 7: Handle Critical Issues

If critical issues are found (`severity_counts.critical > 0` or `critical_issues` is non-empty), **must use AskUserQuestion** to ask the user:
- A) Fix immediately (recommended)
- B) Save the report only, handle later

If the user chooses A:
- Output a "rework checklist" (each critical issue → locate → minimal fix action → notes)
- If the user explicitly authorizes direct modification of the chapter files, use `Edit` to apply the minimal fix to the corresponding chapter file, and suggest re-running `/wordsmith-review` to verify

If the user chooses B:
- Do not modify the chapter files; only retain the review report and metrics record, then end this review session

## Step 8: Wrap Up (Complete Task)

```bash
python "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" workflow start-step --step-id "Step 8" --step-name "Wrap up" || true
python "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" workflow complete-step --step-id "Step 8" --artifacts '{"ok":true}' || true
python "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" workflow complete-task --artifacts '{"ok":true}' || true
```
