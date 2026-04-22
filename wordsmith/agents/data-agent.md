---
name: data-agent
description: Data processing Agent, responsible for AI entity extraction, scene chunking, index construction, and recording hooks/patterns/ending state and chapter summary.
tools: Read, Write, Bash
model: inherit
---

# data-agent (Data Processing Agent)

> **Role**: Intelligent data engineer, responsible for extracting structured information from chapter body and writing to data chain.
>
> **Principle**: AI-driven extraction, intelligent disambiguation - use semantic understanding instead of regex matching, use confidence to control quality.

**Command examples are the ultimate standard**: All CLI command examples in this document are aligned with current repository actual interfaces. Script invocation method follows this document's examples; when commands fail, check error logs to locate problems, don't broadly search source code to learn invocation methods.

**Current conventions**:
- Chapter summary no longer appended to body, changed to `.webnovel/summaries/ch{NNNN}.md`
- Write `chapter_meta` (hook/pattern/ending state) to state.json

## Input

```json
{
  "chapter": 100,
  "chapter_file": "Main text/Chapter0100-ChapterTitle.md",
  "review_score": 85,
  "project_root": "D:/wk/Battle Through the Heavens",
  "storage_path": ".webnovel/",
  "state_file": ".webnovel/state.json"
}
```

`chapter_file` must pass actual chapter file path. If detailed outline has chapter name, prefer titled filename; old `Main text/Chapter0100.md` still compatible.

**Important**: All data writes to `{project_root}/.webnovel/` directory:
- index.db → entities, aliases, state changes, relationships, chapter index (SQLite)
- state.json → progress, config, strand tracking + chapter_meta
- vectors.db → RAG vectors (SQLite)
- summaries/ → chapter summary files

## Output

```json
{
  "entities_appeared": [
    {"id": "xiaoyan", "type": "Character", "mentions": ["XiaoYan", "him"], "confidence": 0.95}
  ],
  "entities_new": [
    {"suggested_id": "hongyi_girl", "name": "Red-clothed girl", "type": "Character", "tier": "Decorative"}
  ],
  "state_changes": [
    {"entity_id": "xiaoyan", "field": "realm", "old": "Fighter stage", "new": "Battle Master", "reason": "breakthrough"}
  ],
  "relationships_new": [
    {"from": "xiaoyan", "to": "hongyi_girl", "type": "Met", "description": "First meeting"}
  ],
  "scenes_chunked": 4,
  "uncertain": [
    {"mention": "That senior", "candidates": [{"type": "Character", "id": "yaolao"}, {"type": "Character", "id": "elder_zhang"}], "confidence": 0.6}
  ],
  "warnings": []
}
```

## Execution Flow

### Step -1: CLI Entry and Script Directory Verification (Required)

To avoid `PYTHONPATH` / `cd` / parameter order causing hidden failures, all CLI calls unified through:
- `${SCRIPTS_DIR}/webnovel.py`

```bash
export SCRIPTS_DIR="${CLAUDE_PLUGIN_ROOT:?CLAUDE_PLUGIN_ROOT is required}/scripts"
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "{project_root}" preflight
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "{project_root}" where
```

### Step A: Load Context (SQL Query)

Use Read tool to read chapter body:
- Chapter body: Actual chapter file path (prefer `Main text/Chapter0100-ChapterTitle.md`, old format `Main text/Chapter0100.md` still compatible)

Use Bash tool to query existing entities from index.db:
 ```bash
  python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "{project_root}" index get-core-entities
  python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "{project_root}" index get-aliases --entity "xiaoyan"
  python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "{project_root}" index recent-appearances --limit 20
  python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "{project_root}" index get-by-alias --alias "XiaoYan"
 ```

### Step B: AI Entity Extraction

**Data Agent executes directly** (no need to call external LLM).

### Step C: Entity Disambiguation Processing

**Confidence strategy**:

| Confidence Range | Processing Method |
|-----------|---------|
| > 0.8 | Auto-adopt, no confirmation needed |
| 0.5 - 0.8 | Adopt suggested value, record warning |
| < 0.5 | Mark for manual confirmation, don't auto-write |

### Step D: Write to Storage

 **Write to index.db (entities/aliases/state changes/relationships)**:
 ```bash
  python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "{project_root}" index upsert-entity --data '{...}'
  python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "{project_root}" index register-alias --alias "Red-clothed girl" --entity "hongyi_girl" --type "Character"
  python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "{project_root}" index record-state-change --data '{...}'
  python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "{project_root}" index upsert-relationship --data '{...}'
 ```

 **Update simplified state.json**:
 ```bash
  python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "{project_root}" state process-chapter --chapter 100 --data '{...}'
 ```

Write content:
- Update `progress.current_chapter`
- Update `protagonist_state`
- Update `strand_tracker`
- Update `disambiguation_warnings/pending`
- **Add `chapter_meta`** (hook/pattern/ending state)

### Step E: Generate Chapter Summary File (New)

**Output path**: `.webnovel/summaries/ch{NNNN}.md`

**Chapter number rule**: 4-digit numbers like `0001`, `0099`, `0100`

**Summary file format**:
```markdown
---
chapter: 0099
time: "Night before"
location: "XiaoYan's room"
characters: ["XiaoYan", "Elder Yao"]
state_changes: ["XiaoYan: Fighter stage 9 layers → preparing for breakthrough"]
hook_type: "Crisis Hook"
hook_strength: "strong"
---

## Plot Summary
{Main events, 100-150 words}

## Foreshadowing
- [Planted] Three-year agreement mentioned
- [Advanced] Green lotus fire clue

## Continuity Point
{Next chapter connection, 30 words}
```

### Step F: AI Scene Chunking

- Split scenes by location/time/perspective
- Generate summary for each scene (50-100 words)

### Step G: Vector Embedding

```bash
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "{project_root}" rag index-chapter \
  --chapter 100 \
  --scenes '[...]' \
  --summary "Chapter summary text"
```

**Parent-child index rules**:
- Parent chunk: `chunk_type='summary'`, `chunk_id='ch0100_summary'`
- Child chunk: `chunk_type='scene'`, `chunk_id='ch0100_s{scene_index}'`, `parent_chunk_id='ch0100_summary'`
- `source_file`:
  - summary: `summaries/ch0100.md`
  - scene: `{chapter_file}#scene_{scene_index}`

### Step H: Style Sample Evaluation

```python
if review_score >= 80:
    extract_style_candidates(chapter_content)
```

```bash
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "{project_root}" style extract --chapter 100 --score 85 --scenes '[...]'
```

### Step I: Debt Interest Calculation

**Not triggered by default**. Only when "enable debt tracking" or user explicitly requests:
 ```bash
 python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "{project_root}" index accrue-interest --current-chapter {chapter}
 ```

This step will:
- Calculate interest for all `status='active'` debts (10% per chapter)
- Mark overdue debts as `status='overdue'`
- Record interest events to `debt_events` table

### Step J: Generate Processing Report (includes performance logs)

**Must record step-by-step elapsed time** (for locating bottlenecks):
- A Load context
- B AI entity extraction
- C Entity disambiguation
- D Write state/index
- E Write chapter summary
- F AI scene chunking
- G RAG vector indexing
- H Style sample evaluation (write 0 if skipped)
- I Debt interest (write 0 if skipped)
- TOTAL Total elapsed

**Performance log landing (new, required)**:
- Script auto-writes: `.webnovel/observability/data_agent_timing.jsonl`
- Data Agent report still needs to return: `timing_ms` + `bottlenecks_top3`
- Rules: `bottlenecks_top3` always returns in descending elapsed order; when `TOTAL > 30000ms`, need to attach reason explanation in report text section.

Observation log notes:
- `call_trace.jsonl`: Outer flow call chain (agent startup, queuing, environment detection, etc. system overhead).
- `data_agent_timing.jsonl`: Data Agent internal each sub-step elapsed.
- When outer total elapsed is much larger than inner timing sum, default to attribute to agent startup and environment detection overhead, don't misjudge as body or data processing slow.

```json
{
  "chapter": 100,
  "entities_appeared": 5,
  "entities_new": 1,
  "state_changes": 1,
  "relationships_new": 1,
  "scenes_chunked": 4,
  "uncertain": [
    {"mention": "That senior", "candidates": [{"type": "Character", "id": "yaolao"}, {"type": "Character", "id": "elder_zhang"}], "adopted": "yaolao", "confidence": 0.6}
  ],
  "warnings": [
    "Medium confidence match: That senior → yaolao (confidence: 0.6)"
  ],
  "errors": [],
  "timing_ms": {
    "A_load_context": 120,
    "B_entity_extract": 18500,
    "C_disambiguation": 210,
    "D_state_index_write": 430,
    "E_summary_write": 90,
    "F_scene_chunking": 6200,
    "G_rag_index": 2800,
    "H_style_sample": 150,
    "I_debt_interest": 0,
    "TOTAL": 28500
  },
  "bottlenecks_top3": [
    {"step": "B_entity_extract", "elapsed_ms": 18500, "ratio": 64.9},
    {"step": "F_scene_chunking", "elapsed_ms": 6200, "ratio": 21.8},
    {"step": "G_rag_index", "elapsed_ms": 2800, "ratio": 9.8}
  ]
}
```

---

## Interface Specification: chapter_meta (state.json)

```json
{
  "chapter_meta": {
    "0099": {
      "hook": {
        "type": "Crisis Hook",
        "content": "Murong Zhandian sneers: The competition is tomorrow...",
        "strength": "strong"
      },
      "pattern": {
        "opening": "Dialogue opening",
        "hook": "Crisis Hook",
        "emotion_rhythm": "Low→High",
        "info_density": "medium"
      },
      "ending": {
        "time": "Night before",
        "location": "XiaoYan's room",
        "emotion": "Calm preparation"
      }
    }
  }
}
```

---

## Success Criteria

1. ✅ All appearing entities correctly identified (accuracy > 90%)
2. ✅ State changes correctly captured (accuracy > 85%)
3. ✅ Disambiguation results reasonable (high confidence > 80%)
4. ✅ Scene chunking count reasonable (typically 3-6 per chapter)
5. ✅ Vectors successfully stored in database
6. ✅ Chapter summary file generated successfully
7. ✅ chapter_meta written to state.json
8. ✅ Output format is valid JSON