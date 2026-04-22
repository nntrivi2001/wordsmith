---
name: system-data-flow
purpose: Loaded when initializing projects and querying status, to understand data structure
---

<context>
This file is for project data structure reference. Claude knows general file organization; this only supplements web novel workflow-specific directory conventions and script responsibilities.
</context>

<instructions>

## Directory Conventions

```
Project Root/
├── MainText/           # Chapter files (Chapter0001.md or Vol1/Chapter001-Title.md)
├── Outline/            # Volume outlines/Chapter outlines/Scene outlines
├── Settings/           # Worldbuilding/Power systems/Character cards/Item cards
└── .webnovel/
    ├── state.json          # Streamlined state (< 5KB): progress/protagonist/strand_tracker/disambiguation
    ├── index.db            # SQLite main storage: entities/aliases/relationships/state_changes/chapters/scenes
    ├── workflow_state.json # Workflow checkpoint (used for /webnovel-resume)
    ├── vectors.db          # RAG vector database
    ├── summaries/          # Chapter summaries (chNNNN.md)
    └── archive/            # Archived data (inactive characters/recovered foreshadowing)
```

## Architecture Change Explanation

**Core change**: Solve state.json bloat problem (token explosion after 20 chapters)

| Data Type | Old Storage Location | Current Storage Location |
|----------|---------------------|------------------------|
| entities_v3 | state.json | **index.db** (entities table) |
| alias_index | state.json | **index.db** (aliases table) |
| state_changes | state.json | **index.db** (state_changes table) |
| structured_relationships | state.json | **index.db** (relationships table) |
| progress | state.json | state.json (retained) |
| protagonist_state | state.json | state.json (retained) |
| strand_tracker | state.json | state.json (retained) |
| disambiguation_* | state.json | state.json (retained) |

## Dual Agent Architecture

```
Before writing: Context Agent reads data = Assembles context package
        = Read streamlined data from state.json (progress/config)
        = SQL query index.db as needed (core entities/on-demand entities)

During writing: Writer uses context package to generate pure manuscript (no XML tags)

After writing: Data Agent processes data chain = AI extracts entities = Writes to data chain
        = Write to index.db (entities/aliases/state changes/relationships)
        = Update state.json (progress/protagonist snapshot + chapter_meta)
        = Write summaries/chNNNN.md (chapter summary)

Context Agent (read) = index.db + state.json = Data Agent (write)
```

## Script/Module Responsibilities Quick Reference

### Core Scripts

| Script | Input | Output |
|--------|-------|--------|
| `init_project.py` | Project info | Generate `.webnovel/state.json` + initialize `index.db` |
| `update_state.py` | Parameters | Atomically update `state.json` fields (progress/protagonist/strand_tracker) |
| `backup_manager.py` | Chapter number | Auto Git backup |
| `status_reporter.py` | None | Generate health report/foreshadowing urgency |
| `archive_manager.py` | None | Archive inactive data |
| `data_modules/migrate_state_to_sqlite.py` | Project path | Migrate old state.json to SQLite |

### data_modules

| Module | Responsibility |
|--------|----------------|
| `state_manager.py` | Entity state management (streamlined state.json + SQLite sync) |
| `sql_state_manager.py` | SQLite state management (replaces JSON writes) |
| `index_manager.py` | SQLite index management (entities/aliases/relationships/state changes/chapters/scenes) |
| `entity_linker.py` | Alias registration and disambiguation |
| `rag_adapter.py` | Vector embedding and semantic retrieval |
| `style_sampler.py` | Style sample extraction and management |
| `api_client.py` | LLM API call wrapper |
| `config.py` | Configuration management |

## Per-Chapter Data Chain

```
1. Context Agent assembles creative task book
   = Read state.json (streamlined: progress/config)
   = SQL query index.db (core entities/on-demand entities)
   = RAG retrieval (related scenes)

2. Step 1.5 Chapter design
   = Select opening/hook/cool point pattern (avoid last 3 chapters)

3. Writer generates chapter content
   = 2A rough draft (pure text)
   = 2B style adaptation (optional)

4. Review (6 Agents in parallel)
   = Cool point/consistency/rhythm/OOC/coherence/continuation check
   = Output review report

5. Net-novel polishing
   = Fix issues based on review report
   = Strengthen taste rules

6. Data Agent processes data chain
   = AI entity extraction (replaces XML tag parsing)
   = Entity disambiguation (confidence strategy)
   = Write to index.db (entities/aliases/state changes/relationships)
   = Update state.json (progress/protagonist snapshot + chapter_meta)
   = Write summaries/chNNNN.md (chapter summary)
   = Vector embedding (RAG)
   = Style sample evaluation

7. Git backup (mandatory)
```

> `update_state.py` is used for manual/scripted updates to `progress`/`protagonist_state`/`strand_tracker` fields; the main flow usually advances progress synchronously when Data Agent processes the data chain.

## state.json Streamlined Structure

```json
{
  "project_info": {"title": "", "genre": ""},
  "progress": {"current_chapter": N, "total_words": W, "current_volume": 1},
  "protagonist_state": {
    "name": "",
    "power": {"realm": "", "layer": 1, "bottleneck": ""},
    "location": {"current": "", "last_chapter": 0},
    "golden_finger": {"name": "", "level": 1, "skills": []}
  },
  "strand_tracker": {
    "last_quest_chapter": 0,
    "last_fire_chapter": 0,
    "last_constellation_chapter": 0,
    "current_dominant": "quest",
    "chapters_since_switch": 0,
    "history": []
  },
  "relationships": {},
  "plot_threads": {"active_threads": [], "foreshadowing": []},
  "world_settings": {},
  "disambiguation_warnings": [],
  "disambiguation_pending": [],
  "review_checkpoints": [],
  "chapter_meta": {},
  "_migrated_to_sqlite": true
}
```

> **Current structure explanation**: entities_v3, alias_index, state_changes, structured_relationships have migrated to index.db, no longer stored in state.json.

## index.db Table Structure

```sql
-- Entity table
CREATE TABLE entities (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,           -- Character/Location/Item/Faction/Technique
    canonical_name TEXT NOT NULL,
    tier TEXT DEFAULT 'decorative',     -- Core/Important/Minor/Decorative
    desc TEXT,
    current_json TEXT,            -- JSON: {realm, location, ...}
    first_appearance INTEGER,
    last_appearance INTEGER,
    is_protagonist INTEGER DEFAULT 0,
    is_archived INTEGER DEFAULT 0
);

-- Alias table (one-to-many)
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
    chapter INTEGER NOT NULL
);

-- Relationships table
CREATE TABLE relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_entity TEXT NOT NULL,
    to_entity TEXT NOT NULL,
    type TEXT NOT NULL,
    description TEXT,
    chapter INTEGER NOT NULL,
    UNIQUE(from_entity, to_entity, type)
);

-- Original tables (retained)
CREATE TABLE chapters (...);
CREATE TABLE scenes (...);
CREATE TABLE appearances (...);
```

## Data Agent AI Extraction Flow

Current main flow no longer requires XML tags, Data Agent intelligently extracts:

1. **Entity recognition**: Identify characters/locations/items/factions from text semantics
2. **Entity matching**: Prioritize matching existing entities (through alias_index)
3. **Disambiguation handling**:
   - Confidence > 0.8: Auto adopt
   - Confidence 0.5-0.8: Adopt but record warning
   - Confidence < 0.5: Mark pending manual confirmation
4. **State change recognition**: Realm breakthroughs/location moves/relationship changes
5. **Write to storage**: Directly write to index.db (entities/aliases/relationships/state changes)

## Foreshadow Field Standards

| Field | Standard Values | Compatible Values (Historical) |
|-------|-----------------|------------------------------|
| status | unrecovered / recovered | unrecovered/in-progress/active/pending |

**Recommended fields**: content, status, planted_chapter, target_chapter, tier

## alias_index Format (One-to-Many)

```json
{
  "Lin Tian": [{"type": "Character", "id": "lintian"}],
  "Tianyun Sect": [
    {"type": "Location", "id": "loc_tianyunzong"},
    {"type": "Faction", "id": "faction_tianyunzong"}
  ]
}
```

Same alias can map to multiple entities; disambiguate according to type or context.

## Formality Levels

| Mức độ | Ngôi xưng | Ngữ cảnh |
|--------|-----------|----------|
| Cao nhất | ngài, tôi | Vua, quý tộc, nghi lễ |
| Cao | tôi, ông, bà | Người lạ, công việc |
| Bình đẳng | mày, tao | Bạn bè thân, đồng đội |
| Thấp | thằng/kẻ (khiếm khuyết) | Đối thủ, khinh bỉ |

**Lưu ý quan trọng:**
- Ngôn ngữ bạn bè thân: "mày/tao" nhưng khi giận chuyển sang "thằng chó"
- Nhân vật yếu thường bị xưng "nó" thay vì "hắn"

## Slang và Vernacular Patterns

| Slang | Ý nghĩa | Ví dụ |
|-------|---------|-------|
| thằng chó | Chửi thề mạnh | *"Thằng chó đó mà dám..."* (UH Chương 3) |
| khốn | Khinh bỉ | *"Đồ khốn nạn!"* |
| chó đẻ | Mắng thô bạo | *"Chết mẹ mày đi!"* (UH Chương 4) |
| hớt hải | Vội vàng | *"Tanaka hớt hải hỏi"* (UH Chương 2) |
| lèm nhèm | Yếu đuối | *"Đứa nhèm nhèm"* |

**Pattern đặc biệt:**
- Khi tâm trạng điên tiết: kết hợp nhiều từ tục: "Mẹ nó! Chết tiệt! Thằng khốn!"
- Nội tâm suy nghĩ dùng ngôn ngữ bình thường, ít tục tĩu hơn lời nói

## Vietnamese Webnovel Writing Conventions

When writing or reviewing Vietnamese webnovel content, apply these patterns from STYLE_GUIDE_VN.md:

### Pronoun Usage (Han Viet Roots)
| Pronoun | Gender/Context | Example |
|---------|----------------|---------|
| **hắn** | Third person male | *"Hắn ta dám..."* |
| **tao** | Equal/friends (strong personality) | *"Tao cá là mày chưa từng..."* |
| **mày** | Equal/friends | *"Mày nghĩ tao sợ mày à!"* |
| **tụi mày** | Plural (multiple people) | *"Tụi mày có thể sống..."* |
| **bọn tao** | Our group (main characters) | *"Bọn tao sẽ không để mày..."* |
| **ta** | Archaic/noble speech | *"Ta là Vincent..."* |
| **ngài** | Honorific (authority figures) | *"Ngài có thể để tôi..."* |
| **tôi** | Formal/polite | *"Tôi muốn gia nhập..."* |

**Pattern**: Pronouns shift with emotions. Normal: "mày/mày", Angry: "thằng khốn", "con nhóc"

### Sentence Structure
- **Action scenes**: Short punchy sentences (3-8 words), dồn dập rhythm
- **Inner monologue**: Longer sentences with literary register
- **Combat dialogue**: Short, cutting each other off
- **Emotional scenes**: Descriptive with metaphors and sensory details

### Colloquial vs Literary Register
| Đời thường | Văn chương | Ghi chú |
|------------|------------|----------|
| đi đường | đường đi | Cùng nghĩa, khác trật tự |
| làm gì | làm chi | Hỏi mục đích |
| đâu | ở đâu | Nơi chốn |
| vậy | như vậy / thế | Cách nói |

### Show-Don't-Tell Emotion Patterns
| Cảm xúc | Biểu hiện cụ thể |
|---------|-------------------|
| Sợ | "run bần bật", "mặt tái mét", "đứng không vững" |
| Giận | "nghiến răng", "nổ gân", "mắt nổ đom đóm" |
| Tức giận cực độ | "hét lên", "khặc ặc", "cười điên cuồng" |
| Buồn | "nước mắt lã chã", "cười méo", "thở dài" |
| Bất ngờ | "tròn mắt", "há hốc mồm", "giật mình" |

### Punctuation Patterns
| Mark | Context | Meaning |
|------|---------|---------|
| `...` | Skepticism/hesitation | Skepticism, hesitation, cliffhanger |
| `—` | Dialogue/thought | Direct speech, inner thoughts |
| `!` | Strong emotion | Shouting, action impact |
| `***` | Scene break | Major scene transitions |
| `—0o0—` | Minor break | Within-chapter transitions (UH style) |

### Chapter Structure Hooks
| Type | Example | Source |
|------|---------|--------|
| Action opening | *"Bốp! Choang!"* | BNsr Chương 1 |
| Status card | *"Thẻ trạng thái!"* | UH Chương 1 |
| Quote opening | *'"Hẳn các vị ở đây..."'* | UH Chương 1 |
| Descriptive | *"Bão. Tuyết. Cái lạnh..."* | BNsr Chương 2 |
| Flashback | *"Khi còn nhỏ tôi đã..."* | BNsr Chương 1 |

### Cliffhanger Patterns
- Incomplete sentences: "Bảy ngày…"
- Plot twist reveals: "Là nó. Thanatos."
- Action dangling: "Nhưng khi Tanaka ngồi dậy..."
- Separator ending: "—0o0—" then chapter end

### Genre-Specific (Isekai/Gaming)
**Status card format (Vietnamese labels)**:
```
Tanaka Akashi
(Tình trạng: Suy dinh dưỡng)
-Chủng loài: Con người
-Tuổi: 17
-Chức nghiệp: Kẻ Vô Dụng
-Cấp: 1
Mana: 5/5
Sức khỏe: 3
-Kĩ năng:
+Cơ Địa Của Kẻ Vô Dụng (Độc nhất)
```

**Combat structure**: See enemy → Check status (Giám định) → Evaluate → Tactical → Action → Result + loot/exp

### Logic Linking Words
| Từ nối | Chức năng | Ví dụ |
|--------|-----------|-------|
| vì | Nguyên nhân | "Vì những lý do không ai biết..." |
| nhưng | Đối lập | "Tuy nhiên, nhưng mà" |
| mà | Liên kết | "Đó là cách... mà cũng là..." |
| tuy nhiên | Đối lập nhẹ | "Tuy nhiên, với những gì..." |
| nên | Kết quả trực tiếp | "Nên cô tạm thời được giải phóng..." |

</instructions>
