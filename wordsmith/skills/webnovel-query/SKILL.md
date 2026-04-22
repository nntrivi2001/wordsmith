---
name: webnovel-query
description: Queries project settings for characters, powers, factions, items, and foreshadowing. Supports urgency analysis and golden finger status. Activates when user asks about story elements or /webnovel-query.
allowed-tools: Read Grep Bash AskUserQuestion
---

# Information Query Skill

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
- **Prohibited**: reading from or writing project files under the plugin directory `${CLAUDE_PLUGIN_ROOT}/`

Environment setup (before executing bash commands):
```bash
export WORKSPACE_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"

if [ -z "${CLAUDE_PLUGIN_ROOT}" ] || [ ! -d "${CLAUDE_PLUGIN_ROOT}/skills/webnovel-query" ]; then
  echo "ERROR: CLAUDE_PLUGIN_ROOT is not set or directory is missing: ${CLAUDE_PLUGIN_ROOT}/skills/webnovel-query" >&2
  exit 1
fi
export SKILL_ROOT="${CLAUDE_PLUGIN_ROOT}/skills/webnovel-query"

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
Information Query Progress:
- [ ] Step 1: Identify query type
- [ ] Step 2: Load corresponding reference files
- [ ] Step 3: Load project data (state.json)
- [ ] Step 4: Confirm sufficient context
- [ ] Step 5: Execute query
- [ ] Step 6: Format output
```

---

## Reference Loading Levels (strict, lazy)

- L0: Identify query type first; do not pre-load all references.
- L1: All queries load only the basic data-flow specification.
- L2: Load only the topic-specific reference matching the query type.

### L1 (minimum)
- [system-data-flow.md](references/system-data-flow.md)

### L2 (conditional by query type)
- Foreshadowing query: [foreshadowing.md](references/advanced/foreshadowing.md)
- Pacing query: [strand-weave-pattern.md](../../references/shared/strand-weave-pattern.md)
- Tag format query: [tag-specification.md](references/tag-specification.md)
- Vietnamese writing patterns: [STYLE_GUIDE_VN.md](../../STYLE_GUIDE_VN.md)

Do not load two or more L2 files unless the user request clearly spans multiple query types.

## Step 1: Identify Query Type

| Keyword | Query Type | Load |
|---------|-----------|------|
| Character / protagonist / supporting character | Standard query | system-data-flow.md |
| Realm / cultivation stage | Standard query | system-data-flow.md |
| Foreshadowing / urgent foreshadowing | Foreshadowing analysis | foreshadowing.md |
| Golden finger / system | Golden finger status | system-data-flow.md |
| Pacing / Strand | Pacing analysis | strand-weave-pattern.md |
| Tag / entity format | Format query | tag-specification.md |

## Step 2: Load Corresponding Reference Files

**Required for all queries**:
```bash
cat "${SKILL_ROOT}/references/system-data-flow.md"
```

**Additional for foreshadowing queries**:
```bash
cat "${SKILL_ROOT}/references/advanced/foreshadowing.md"
```

**Additional for pacing queries**:
```bash
cat "${SKILL_ROOT}/../../references/shared/strand-weave-pattern.md"
```

**Additional for tag format queries**:
```bash
cat "${SKILL_ROOT}/references/tag-specification.md"
```

## Step 3: Load Project Data

```bash
cat "$PROJECT_ROOT/.webnovel/state.json"
```

## Step 4: Confirm Sufficient Context

**Checklist**:
- [ ] Query type identified
- [ ] Corresponding reference files loaded
- [ ] state.json loaded
- [ ] Know where to search for the answer

**If anything is missing → return to the corresponding Step**

## Step 5: Execute Query

### Standard Query

| Keyword | Search Target |
|---------|--------------|
| Character / protagonist / supporting character | protagonist-card.md, character-library/ |
| Realm / power level | power-system.md |
| Sect / faction | worldbuilding.md |
| Item / treasure | item-library/ |
| Location / secret realm | worldbuilding.md |

### Foreshadowing Urgency Analysis

**Three-tier classification** (from foreshadowing.md):
- **Core foreshadowing**: Main plot — weight 3.0x
- **Sub-plot foreshadowing**: Supporting characters / sub-plots — weight 2.0x
- **Decorative foreshadowing**: Atmosphere / details — weight 1.0x

**Urgency formula**:
```
Urgency = (chapters_elapsed / target_chapter) × tier_weight
```

**Status assessment**:
- 🔴 Critical: past target OR core >20 chapters
- 🟡 Warning: >80% of target OR sub-plot >30 chapters
- 🟢 Normal: within planned range

**Quick analysis**:
```bash
python "${SCRIPTS_DIR}/webnovel.py" --project-root "$PROJECT_ROOT" status -- --focus urgency
```

### Golden Finger Status

Output includes:
- Basic info (name / type / activation chapter)
- Current level and progress
- Unlocked skills and cooldowns
- Preview of skills to unlock
- Upgrade conditions
- Development suggestions

### Strand Pacing Analysis

**Quick analysis**:
```bash
python "${SCRIPTS_DIR}/webnovel.py" --project-root "$PROJECT_ROOT" status -- --focus strand
```

**Check warnings**:
- Quest >5 consecutive chapters
- Fire >10 chapters without appearance
- Constellation >15 chapters without appearance

## Step 6: Format Output

```markdown
# Query Result: {keyword}

## Summary
- **Match type**: {type}
- **Data source**: state.json + settings files + outline
- **Match count**: X items

## Detailed Information

### 1. Runtime State (state.json)
{structured data}
**Source**: `.webnovel/state.json` (lines XX-XX)

### 2. Settings File Match Results
{matched content, with file path and line number}

## Data Consistency Check
{differences between state.json and static files}
```
