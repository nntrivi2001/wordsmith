# Entity Management Specification

> **Scope**: All entity types (characters / locations / items / factions / skills)
> **Core Goal**: AI-driven entity extraction, alias management, and version tracking
>
> **Vietnamese Pattern Reference**: For naming conventions and character voice patterns, see `STYLE_GUIDE_VN.md` Section 1 (pronouns, formality levels) and Section 7 (narrative voice).

---

## Current Specification Changes

1. **SQLite Storage**: Entities, aliases, state changes, and relationships migrated to `index.db`
2. **Streamlined state.json**: Retains only progress, protagonist state, and pacing tracking (< 5 KB)
3. **AI Extraction**: Data Agent extracts entities from raw prose via semantic analysis
4. **Confidence-based Disambiguation**: > 0.8 auto-accepted, 0.5–0.8 flagged with warning, < 0.5 requires manual confirmation
5. **Dual Agent Architecture**: Context Agent (read) + Data Agent (write)

> **Note**: XML tags are still available for manual annotation scenarios, but are no longer required by the main workflow.

---

## 1. Storage Architecture

### 1.1 Data Distribution

| Data Type | Storage Location | Description |
|---------|---------|------|
| Entities | index.db | SQLite `entities` table |
| Aliases | index.db | SQLite `aliases` table (one-to-many) |
| State Changes | index.db | SQLite `state_changes` table |
| Relationships | index.db | SQLite `relationships` table |
| Chapter Index | index.db | SQLite `chapters` table |
| Scene Index | index.db | SQLite `scenes` table |
| Progress / Config | state.json | Compact JSON (< 5 KB) |
| Protagonist State | state.json | `protagonist_state` snapshot |
| Pacing Tracking | state.json | `strand_tracker` |

### 1.2 index.db Schema

```sql
-- Entities table
CREATE TABLE entities (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,  -- character/location/item/faction/skill
    canonical_name TEXT NOT NULL,
    tier TEXT DEFAULT 'decorative',  -- core/important/minor/decorative
    desc TEXT,
    current_json TEXT,  -- current state in JSON format
    first_appearance INTEGER,
    last_appearance INTEGER,
    is_protagonist INTEGER DEFAULT 0,
    created_at TEXT,
    updated_at TEXT
);

-- Aliases table (one-to-many)
CREATE TABLE aliases (
    alias TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    PRIMARY KEY (alias, entity_id, entity_type)
);

-- State changes table
CREATE TABLE state_changes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id TEXT NOT NULL,
    field TEXT NOT NULL,
    old_value TEXT,
    new_value TEXT,
    reason TEXT,
    chapter INTEGER,
    created_at TEXT
);

-- Relationships table
CREATE TABLE relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_entity TEXT NOT NULL,
    to_entity TEXT NOT NULL,
    type TEXT NOT NULL,
    description TEXT,
    chapter INTEGER,
    created_at TEXT,
    UNIQUE(from_entity, to_entity, type)
);
```

### 1.3 Entity Type Characteristics

| Entity Type | Alias Complexity | Attribute Changes | Hierarchical |
|---------|-----------|---------|---------|
| Character | High (many forms of address) | High (realm / location / relationship) | No |
| Location | Medium (abbreviation / full name) | Low (status changes) | Yes (province > city > district) |
| Item | Low (few alternate names) | Medium (upgrade / transfer) | No |
| Faction | Medium (abbreviation / alias) | Medium (rank / territory) | Yes (HQ > branch) |
| Skill | Low (aliases rare) | Medium (upgrade) | No |

---

## 2. Processing Workflow

### 2.1 Data Agent Automatic Extraction

```
Chapter Text
    ↓
Data Agent (AI Semantic Analysis)
    ↓
┌─────────────────────────────────────────────────────────────┐
│ 1. Identify appearing entities                              │
│    - Match existing entities (via aliases table)            │
│    - Identify new entities, generate suggested_id           │
│                                                          │
│ 2. Confidence evaluation                                   │
│    ├─ > 0.8: Auto-accept                                   │
│    ├─ 0.5-0.8: Accept with warning                         │
│    └─ < 0.5: Mark for manual confirmation                  │
│                                                          │
│ 3. Write to index.db                                       │
│    - entities table: new entities / update appearance      │
│    - aliases table: register new aliases                   │
│    - state_changes table: record attribute changes          │
│    - relationships table: record new relationships          │
│                                                          │
│ 4. Update state.json (streamlined)                         │
│    - protagonist_state: protagonist status snapshot         │
│    - strand_tracker: pacing tracking                       │
│    - disambiguation_warnings/pending: disambiguation records│
└─────────────────────────────────────────────────────────────┘
    ↓
index.db Update Complete
```

### 2.2 Query Interface

```bash
# Query entity
python "${SCRIPTS_DIR}/webnovel.py" --project-root "$PROJECT_ROOT" index get-entity --id "xiaoyan"

# Query core entities
python "${SCRIPTS_DIR}/webnovel.py" --project-root "$PROJECT_ROOT" index get-core-entities

# Find by alias
python "${SCRIPTS_DIR}/webnovel.py" --project-root "$PROJECT_ROOT" index get-by-alias --alias "xiaoyan"

# Query state change history
python "${SCRIPTS_DIR}/webnovel.py" --project-root "$PROJECT_ROOT" index get-state-changes --entity "xiaoyan"

# Query relationships
python "${SCRIPTS_DIR}/webnovel.py" --project-root "$PROJECT_ROOT" index get-relationships --entity "xiaoyan"
```

---

## 3. Tag System (Optional)

> The main workflow now uses Data Agent automatic extraction. The following tags are only for **manual annotation scenarios**.

### 3.1 Create New Entity (`<entity>`)

```xml
<entity type="character" id="lintian" name="Lin Tian" desc="Protagonist, awakens devouring golden finger" tier="core">
  <alias>trash</alias>
  <alias>that youth</alias>
</entity>

<entity type="location" id="tianyunzong" name="Tian Yun Sect" desc="One of the three major sects in the Eastern Domain" tier="core">
  <alias>sect</alias>
</entity>
```

### 3.2 Add Alias (`<entity-alias>`)

```xml
<entity-alias id="lintian" alias="Sect Master Lin" context="After becoming Tian Yun Sect Master"/>
<entity-alias ref="Lin Tian" alias="Immortal Warrior" context="After receiving Immortal Warrior title"/>
```

### 3.3 Update Attributes (`<entity-update>`)

```xml
<entity-update id="lintian">
  <set key="realm" value="Foundation Building Stage Layer 1" reason="Breakthrough in Blood Evil Secret Realm"/>
  <set key="location" value="Tian Yun Sect"/>
</entity-update>
```

**Operation Types**:

| Operation | Syntax | Description |
|------|------|------|
| set | `<set key="k" value="v"/>` | Set attribute value |
| unset | `<unset key="k"/>` | Delete attribute |
| add | `<add key="k" value="v"/>` | Add element to array |
| remove | `<remove key="k" value="v"/>` | Remove element from array |
| inc | `<inc key="k" delta="1"/>` | Increment numeric value |

---

## 4. ID Generation Rules

```python
def generate_entity_id(entity_type: str, name: str, existing_ids: set) -> str:
    """
    Generate unique entity ID

    Rules:
    1. Prefer pinyin (remove spaces, lowercase)
    2. If conflict, append numeric suffix
    3. Type prefix: item→item_, faction→faction_, skill→skill_, location→loc_
    """
    prefix_map = {
        "item": "item_",
        "faction": "faction_",
        "skill": "skill_",
        "location": "loc_"
        # character has no prefix
    }

    pinyin = ''.join(lazy_pinyin(name))
    base_id = prefix_map.get(entity_type, '') + pinyin.lower()

    final_id = base_id
    counter = 1
    while final_id in existing_ids:
        final_id = f"{base_id}_{counter}"
        counter += 1

    return final_id
```

---

## 5. Error Handling

### 5.1 Alias Conflicts

The current structure allows **one-to-many aliases**: the same alias can point to multiple entities.

When `ref="alias"` matches multiple entities and cannot be disambiguated, an error is raised:

```
⚠️ Alias ambiguity: 'sect_master' matches 2 entities. Please use an id or add a type attribute.

Solutions:
  1. Use a stable id: <entity-update id="...">...</entity-update>
  2. Add type attribute (only disambiguates across types; same-type name collisions still require id)
```

### 5.2 Confidence Handling

| Confidence Range | Handling |
|-----------|---------|
| > 0.8 | Auto-accepted, no confirmation needed |
| 0.5 – 0.8 | Accepted with a recorded warning |
| < 0.5 | Flagged for manual confirmation; not auto-written |

---

## 6. Migration Notes

Migrating from the old structure to the current structure:

```bash
# Run migration script
python "${SCRIPTS_DIR}/webnovel.py" --project-root "$PROJECT_ROOT" migrate -- --backup

# Verify migration results
python "${SCRIPTS_DIR}/webnovel.py" --project-root "$PROJECT_ROOT" index stats
```

After migration:
- `index.db` contains all entities, aliases, state changes, and relationships
- `state.json` retains only progress, protagonist state, and pacing tracking
- Legacy fields `entities_v3` and `alias_index` are cleaned up

---

## 7. Summary

### 7.1 Core Improvements in the Current Structure

1. **SQLite Storage**: Solves the `state.json` bloat problem
2. **Compact JSON**: `state.json` stays under 5 KB
3. **One-to-Many Aliases**: The same alias can map to multiple entities
4. **AI Auto-Extraction**: Data Agent semantic analysis replaces XML tags

### 7.2 Data Flow

```
Chapter Text → Data Agent → index.db (entities / aliases / relationships / state changes)
                          → state.json (progress / protagonist state / pacing)
                          → vectors.db (scene vectors)
                                  ↓
                          Context Agent → Next Chapter Context
```

---

## Vietnamese Writing Patterns (STYLE_GUIDE_VN.md Section 13)

### From Ta Dung Nhin Vo Lam Toang (Primary Source):
- Dialogue: "Nội dung" + action tag, no ——
- Inner thoughts: third-person narrative, "cậu" for self-reference
- Scene breaks: --- for major, *— Hết Chương —* for end
- First-person: cậu/mình in thoughts, tao/mày with close people
- Slang: vãi, cứt, bro (@ v @) in GenZ contexts

### Sentence Structure:
- Must have Subject + Predicate
- Connectors: và, nhưng, nên, vì, sau đó, rồi, thì, mà
- No fragmented sentences

### 8 Error Types:
1. Units: mét/cm/km/kg (NOT trượng/dặm/tấc/thốn/ly)
2. Vocabulary: match context
3. Punctuation: — single (NOT —— double)
4. Sentence: complete with subject+predicate
5. Spelling: ken két not kẽ kẽy
6. Connectors: required
7. Subject: explicit in descriptions
8. Natural Vietnamese words

### Cool-Point Placement:
- Every 500-800 words
- Fast-paced: 70-80% short sentences (1-7 words)
- Slow-paced: 70-80% long sentences (15+ words)

### Cliffhanger Patterns:
- Incomplete action ending
- System notification: "Keng!" + message
- Twist revelation
- Question left unanswered