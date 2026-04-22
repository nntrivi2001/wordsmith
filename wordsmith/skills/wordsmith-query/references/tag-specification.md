---
name: tag-specification
purpose: XML tag format reference
---

<context>
This file is for XML tag format reference.

**Current convention**:
- XML tags are **no longer required** when writing chapters
- Data Agent automatically extracts entities from pure manuscript text, writes to index.db
- Tags are only used for **manual annotation** scenes (such as explicitly marking important entities, supplementing missed extractions)
- If you choose to use tags, please follow the specifications below

**Vietnamese Entity Patterns**:
- Character names: "Rosa", "Jack" (BNsr), "Tanaka Akashi", "Endou", "Tekuzu" (UH)
- Pronoun usage and speech registers (see below)
- Faction names reflect Xuanhuan/isekai genre: "Môn phái", "Hội", "Đội"
- Location names: "Erever", "Chyrse" (BNsr fantasy realm), "Abandoned laboratory west of city" (UH modern)
- Item/skill names: "Time Rewind", "Space Anchor", "Cơ Địa Của Kẻ Vô Dụng"

**Vietnamese Pronoun & Speech Register Patterns**:

| Pronoun | Register | Context | Example |
|---------|----------|---------|---------|
| **hắn** | 3rd male | Action, provoking | *"Hắn ta dám..."* (BNsr Chương 4) |
| **tao** | Equal/friends | Strong, confident | *"Tao cá là mày chưa từng..."* (UH Chương 4) |
| **mày** | Equal/friends | Casual address | *"Mày nghĩ tao sợ mày à!"* (UH Chương 1) |
| **tụi mày** | Group | Addressing multiple | *"Tụi mày có thể sống..."* (BNsr Chương 5) |
| **bọn tao** | Our group | Protagonist's party | *"Bọn tao sẽ không để mày..."* (BNsr Chương 5) |
| **ta** | Archaic/ritual | Noble, formal | *"Ta là Vincent..."* (BNsr Chương 3) |
| **ngài** | Honorific | Addressing authority | *"Ngài có thể để tôi..."* (UH Chương 1) |
| **tôi** | Polite | Formal, social | *"Tôi muốn gia nhập..."* (UH Chương 2) |

**Pattern: Pronoun shifts indicate emotional state**
- Normal: "mày/mày" between close characters
- Angry: Switch to "thằng khốn", "con nhóc", "thằng chó"
- Protagonists (Rosa, Jack) use "tao-mày" with each other but "tôi-ngài" with strangers
- Weak characters often called "nó" instead of "hắn"

**Formality Levels**:
| Level | Pronouns | Context |
|-------|----------|---------|
| Highest | ngài, tôi | King, nobility, ceremonies |
| High | tôi, ông, bà | Strangers, business |
| Equal | mày, tao | Close friends, teammates |
| Low | thằng/kẻ (defective) | Enemies, contempt |

**Colloquial vs Literary Register**:
| Colloquial | Literary | Meaning |
|------------|----------|---------|
| đi đường | đường đi | Same meaning, different order |
| làm gì | làm chi | Asking purpose |
| sao | như thế nào | Asking how |
| vậy | như vậy / thế | Way of saying |

**Slang & Vernacular Patterns**:
| Slang | Meaning | Example |
|-------|---------|---------|
| thằng chó | Strong swear | *"Thằng chó đó mà dám..."* (UH Chương 3) |
| khốn | Contempt | *"Đồ khốn nạn!"* |
| chó đẻ | Rough insult | *"Chết mẹ mày đi!"* (UH Chương 4) |
| hớt hải | Hurriedly | *"Tanaka hớt hải hỏi"* (UH Chương 2) |
| lèm nhèm | Weak | *"Đứa nhèm nhèm"* |
| cơm | Money (slang) | Used in character's inner thoughts |

**Pattern: When furious, combine swear words**
- "Mẹ nó! Chết tiệt! Thằng khốn!"
- Inner thoughts use normal language, less vulgar than spoken
</context>

<instructions>

## Tag Overview

| Tag | Purpose | Required Attributes |
|-----|---------|--------------------|
| `<entity>` | Create/update entities (character/location/item/faction/technique) | type, name |
| `<entity-alias>` | Register entity alias/title | id/ref, alias |
| `<entity-update>` | Update entity attributes (supports set/unset/add/remove/inc + history tracking) | id/ref, `<set>` etc. |
| `<skill>` | Cheat ability | name, level, desc, cooldown |
| `<foreshadow>` | Foreshadow planting | content, tier |
| `<relationship>` | Character relationship | char1, char2, type |
| `<deviation>` | Outline deviation marking | reason |

## Attribute Details

### tier (Layer)
- **Core**: Affects main plot, must be tracked
- **Sub-line**: Enriches plot, should be tracked
- **Decorative**: Adds realism, optional tracking

### type (Entity Type)
Character / Location / Item / Faction / Technique

### id / ref (Entity Reference)
- **id (recommended)**: Stable unique identifier (facilitates subsequent updates/alias additions)
- **ref**: Use previously appeared name/alias reference (auto-resolved through index.db aliases table)
- **type (optional)**: Used for disambiguation when ref is ambiguous (e.g., same name different people); if still ambiguous must use `id`

### `<entity-update>` Sub-operations
- **set**: `<set key="k" value="v" reason="optional"/>`
- **unset**: `<unset key="k" reason="optional"/>`
- **add**: `<add key="k" value="v" reason="optional"/>` (array append, auto dedup)
- **remove**: `<remove key="k" value="v" reason="optional"/>` (array removal)
- **inc**: `<inc key="k" delta="1" reason="optional"/>` (numeric increment, default +1)

**Top-level field whitelist** (can directly update entity top-level rather than current): `tier`, `desc`, `canonical_name`, `importance`, `status`, `parent`

> **Suggestion**: `<entity>` strongly recommended to add `desc` and `tier`, otherwise subsequent retrieval and consistency checks will suffer.

## Placement Rules

- **Recommended**: Unified placement at chapter end (easy to manage)
- **Allowed**: End of paragraph where entity first appears
- **Required**: Tags on their own line, not interspersed in body text

### Hidden approach (Recommended)

```markdown
Body content...

<!--
<entity type="Character" id="luchen" name="Lu Chen" desc="Protagonist, spatiotemporal ability awakens" tier="core"/>
<entity-alias id="luchen" alias="Captain Lu" context="After joining special task force"/>
<entity-update id="luchen"><set key="realm" value="F-rank Awakened" reason="Awakening complete"/></entity-update>
<skill name="Time Rewind" level="1" desc="Return to 10 seconds ago" cooldown="24 hours"/>
<foreshadow content="Mysterious old man's jade pendant" tier="core" target="50"/>
<relationship char1_id="luchen" char2_id="liwe" type="ally" intensity="60" desc="Initial cooperation"/>
-->
```

</instructions>

<examples>

<example>
<input>Mark new character</input>
<output>
```xml
<entity type="Character" id="luchen" name="Lu Chen" desc="Protagonist, spatiotemporal ability awakens, university student" tier="core"/>
<entity type="Character" id="liwe" name="Li Wei" desc="Female lead, mysterious background school beauty" tier="core"/>
<entity type="Character" name="Coffee shop owner" desc="Seems ordinary but actually powerful" tier="decorative"/>
```
</output>
</example>

<example>
<input>Mark character with Vietnamese naming pattern</input>
<output>
```xml
<!-- VN Xuanhuan style: Character with title/alias system -->
<entity type="Character" id="rosa" name="Rosa" desc="Con gái lớn lên bằng thịt sống, cắn nhau với lũ rồng con" tier="core"/>
<entity type="Character" id="jack" name="Jack" desc="Main protagonist, uses kiếm (sword),追求自由 (seeking freedom)" tier="core"/>

<!-- VN Isekai style: Status card system characters -->
<entity type="Character" id="tanaka" name="Tanaka Akashi" desc="Kẻ Vô Dụng, cấp 1, stats thấp nhất" tier="core"/>
<entity type="Character" id="endou" name="Endou" desc="Student, seems weak but hidden power" tier="sub-line"/>
```
</output>
</example>

<example>
<input>Register new title/alias</input>
<output>
```xml
<entity-alias id="luchen" alias="Captain Lu" context="After joining special task force"/>
<entity-alias ref="Lu Chen" alias="The Heir" context="After system confirms identity"/>
```
</output>
</example>

<example>
<input>Update entity attributes (realm/location/status/affiliation, etc.)</input>
<output>
```xml
<entity-update id="luchen">
  <set key="realm" value="E-rank Controller" reason="Breakthrough during crisis"/>
  <set key="location" value="Abandoned laboratory west of city"/>
</entity-update>
```
</output>
</example>

<example>
<input>Mark new skill</input>
<output>
```xml
<skill name="Time Rewind" level="1" desc="Return to state 10 seconds ago" cooldown="24 hours"/>
<skill name="Space Anchor" level="2" desc="Set teleport anchor, can teleport back instantly" cooldown="1 hour"/>
<skill name="Time Perception" level="1" desc="Passive skill, foresee 3 seconds of danger" cooldown="None"/>
```
</output>
</example>

<example>
<input>Mark skill with VN gaming pattern (Isekai/Game genre)</input>
<output>
```xml
<!-- UH style: Gaming system skills -->
<skill name="Cơ Địa Của Kẻ Vô Dụng" level="1" desc="Giảm 80% exp để lên cấp, thật vô dụng... hay là đặc biệt?" cooldown="N/A"/>
<skill name="Dịch Chuyển Ngẫu Nhiên" level="1" desc="Di chuyển ngẫu nhiên đến vị trí bất kỳ trong phạm vi 10m" cooldown="5 phút"/>
<skill name="Giám Định" level="1" desc="Xem thông tin trạng thái của mục tiêu" cooldown="1 phút"/>

<!-- Xuanhuan style: Martial arts/technique -->
<skill name="Devouring Heaven Divine Art" level="???" desc="Công pháp thượng cổ, hiện đang trong trạng thái sealed" cooldown="Unknown"/>
```
</output>
</example>

<example>
<input>Plant foreshadow</input>
<output>
```xml
<foreshadow content="Mysterious old man's jade pendant starts glowing" tier="core" target="50" location="Abandoned laboratory"/>
<foreshadow content="Li Wei's strange tattoo on wrist" tier="sub-line" target="30" characters="Li Wei,Lu Chen"/>
<foreshadow content="Coffee shop owner's meaningful gaze" tier="decorative"/>
```
</output>
</example>

<example>
<input>Mark outline deviation</input>
<output>
```xml
<deviation reason="Temporary inspiration, increased Li Wei and Lu Chen emotional interaction, foreshadowing for later romance line"/>
<deviation reason="Originally planned breakthrough this chapter, but rhythm too fast, delayed to next chapter"/>
```
</output>
</example>

</examples>

<errors>
`<entity type='character' .../>` = Use double quotes `type="character"`
`<entity type="character" ...>` = Self-close `.../>` or complete `</entity>`
`<Entity type="character" .../>` = Lowercase tag name `<entity`
`[NEW_ENTITY: character, Lu Chen, ...]` = Use XML format
`<entity-update ref="xxx"></entity-update>` = Must include at least one `<set key="..." value="..."/>`
</errors>
