---
name: webnovel-resume
description: Recovers interrupted webnovel tasks with precise workflow state tracking. Detects interruption point and provides safe recovery options. Activates when user wants to resume or /webnovel-resume.
allowed-tools: Read Bash AskUserQuestion
---

# Task Resume Skill

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

## Project Root Guard (must confirm first)

- The Claude Code "workspace root" is not necessarily equal to the "book project root." A common structure: workspace is `D:\wk\xiaoshuo`, book project is `D:\wk\xiaoshuo\FanrenCapitalTheory`.
- Must first resolve the true book project root (which must contain `.webnovel/state.json`); all subsequent read/write paths are relative to that directory.

Environment setup (before executing bash commands):
```bash
export WORKSPACE_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"

if [ -z "${CLAUDE_PLUGIN_ROOT}" ] || [ ! -d "${CLAUDE_PLUGIN_ROOT}/skills/webnovel-resume" ]; then
  echo "ERROR: CLAUDE_PLUGIN_ROOT is not set or directory is missing: ${CLAUDE_PLUGIN_ROOT}/skills/webnovel-resume" >&2
  exit 1
fi
export SKILL_ROOT="${CLAUDE_PLUGIN_ROOT}/skills/webnovel-resume"

if [ -z "${CLAUDE_PLUGIN_ROOT}" ] || [ ! -d "${CLAUDE_PLUGIN_ROOT}/scripts" ]; then
  echo "ERROR: CLAUDE_PLUGIN_ROOT is not set or directory is missing: ${CLAUDE_PLUGIN_ROOT}/scripts" >&2
  exit 1
fi
export SCRIPTS_DIR="${CLAUDE_PLUGIN_ROOT}/scripts"

export PROJECT_ROOT="$(python "${SCRIPTS_DIR}/webnovel.py" --project-root "${WORKSPACE_ROOT}" where)"
```

## Workflow Checklist

Copy and track progress:

```
Task Resume Progress:
- [ ] Step 1: Load resume protocol (cat "${SKILL_ROOT}/references/workflow-resume.md")
- [ ] Step 2: Load data specification (cat "${SKILL_ROOT}/references/system-data-flow.md")
- [ ] Step 3: Confirm sufficient context
- [ ] Step 4: Detect interruption state
- [ ] Step 5: Display recovery options (AskUserQuestion)
- [ ] Step 6: Execute recovery
- [ ] Step 7: Continue task (optional)
```

---

## Reference Loading Levels (strict, lazy)

- L0: Do not load any references until an interrupted-recovery need is confirmed.
- L1: Load only the resume protocol main file.
- L2: Load the data specification only when checking state field consistency / recovery strategy.

### L1 (minimum)
- [workflow-resume.md](references/workflow-resume.md)

### L2 (conditional)
- [system-data-flow.md](references/system-data-flow.md) (only when state fields or recovery strategy need to be verified)
- Vietnamese writing patterns: [STYLE_GUIDE_VN.md](../../STYLE_GUIDE_VN.md)

## Step 1: Load Resume Protocol (required)

```bash
cat "${SKILL_ROOT}/references/workflow-resume.md"
```

**Core principles** (apply after reading):
- **No smart continuation**: High risk of context loss
- **Must detect before recovering**: Do not guess the interruption point
- **Must confirm with user**: Do not auto-recover

## Step 2: Load Data Specification

```bash
cat "${SKILL_ROOT}/references/system-data-flow.md"
```

## Step 3: Confirm Sufficient Context

**Checklist**:
- [ ] Resume protocol understood
- [ ] Step difficulty levels known
- [ ] State structure understood
- [ ] "Delete and restart" vs "smart continuation" principles clarified

**If anything is missing → return to the corresponding Step**

## Step Difficulty Levels (from workflow-resume.md)

| Step | Difficulty | Recovery Strategy |
|------|-----------|------------------|
| Step 1 | ⭐ | Re-execute directly |
| Step 1.5 | ⭐ | Redesign |
| Step 2A | ⭐⭐ | Delete partial work, start over |
| Step 2B | ⭐⭐ | Continue adaptation or return to 2A |
| Step 3 | ⭐⭐⭐ | User decides: re-review or skip |
| Step 4 | ⭐⭐ | Continue polishing or delete and rewrite |
| Step 5 | ⭐⭐ | Re-run (idempotent) |
| Step 6 | ⭐⭐⭐ | Check staging area, decide commit/rollback |

## Step 4: Detect Interruption State

```bash
python "${SCRIPTS_DIR}/webnovel.py" --project-root "$PROJECT_ROOT" workflow detect
```

**Output scenarios**:
- No interruption → end the flow, notify the user
- Interruption detected → continue to Step 5

## Step 5: Display Recovery Options (required)

**Show the user**:
- Task command and arguments
- Interruption time and elapsed time since
- Completed steps
- Current (interrupted) step
- Remaining steps
- Recovery options with risk levels

**Example output**:

```
🔴 Interrupted task detected:

Task: /webnovel-write 7
Interrupted at: Step 2 - Chapter content generation in progress

Completed:
  ✅ Step 1: Context loading

Not completed:
  ⏸️ Step 2: Chapter content (1500 words written)
  ⏹️ Steps 3-7: Not started

Recovery options:
A) Delete partial work, restart from Step 1 (recommended)
B) Roll back to Ch6, discard all progress on Ch7

Please choose (A/B):
```

## Step 6: Execute Recovery

**Option A — Delete and restart** (recommended):
```bash
python "${SCRIPTS_DIR}/webnovel.py" --project-root "$PROJECT_ROOT" workflow cleanup --chapter {N} --confirm
python "${SCRIPTS_DIR}/webnovel.py" --project-root "$PROJECT_ROOT" workflow clear
```

**Option B — Git rollback**:
```bash
git -C "$PROJECT_ROOT" reset --hard ch{N-1:04d}
python "${SCRIPTS_DIR}/webnovel.py" --project-root "$PROJECT_ROOT" workflow clear
```

## Step 7: Continue Task (optional)

If the user chooses to continue immediately:
```bash
/{original_command} {original_args}
```

---

## Special Scenarios

### Step 6 Interruption (high cost)

```
Recovery options:
A) Re-execute dual-chapter review (cost: ~$0.15) ⚠️
B) Skip review, continue to next chapter (can review later)
```

### Step 4 Interruption (partial state)

```
⚠️ state.json may be partially updated

A) Inspect and repair state.json
B) Roll back to previous chapter (safe)
```

### Long Interruption (>1 hour)

```
⚠️ Interruption exceeds 1 hour

High risk of context loss
Recommended to restart rather than continue
```

---

## Prohibitions

- ❌ Smart continuation of partial content
- ❌ Auto-selecting a recovery strategy
- ❌ Skipping interruption detection
- ❌ Patching state.json without validation
