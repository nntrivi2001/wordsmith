---
name: system-data-flow-redirect
purpose: Redirect to the authoritative version
---

<context>
This file has been migrated to a unified location to avoid synchronization issues across multiple versions.
</context>

<instructions>

## Authoritative Version Location

`${CLAUDE_PLUGIN_ROOT}/skills/wordsmith-query/references/system-data-flow.md`

## Loading Method

```bash
cat "${CLAUDE_PLUGIN_ROOT}/skills/wordsmith-query/references/system-data-flow.md"
```

## Quick Reference

### Directory Structure
```
Project Root/
├── MainText/           # Chapter files
├── Outline/            # Volume outlines/Chapter outlines
├── Settings/           # Worldbuilding/Power systems/Character sheets
└── .webnovel/
    ├── state.json          # Authoritative state
    ├── workflow_state.json # Workflow checkpoint
    ├── index.db            # SQLite index
    └── archive/            # Archived data
```

### Current Core Architecture Changes
- **Dual Agent Architecture**: Context Agent (read) + Data Agent (write)
- **No XML Tags**: Pure manuscript writing, Data Agent AI auto-extracts entities
- **SQLite Storage**: entities/aliases/state_changes migrated to index.db
- **Streamlined state.json**: Keep under 5KB, main content includes progress/protagonist_state/strand_tracker/disambiguation

### Vietnamese Webnovel Writing Conventions

When writing or reviewing Vietnamese webnovel content, apply these patterns from STYLE_GUIDE_VN.md:

#### Pronoun Usage (Han Viet Roots)
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

#### Sentence Structure
- **Action scenes**: Short punchy sentences (3-8 words), dồn dập rhythm
- **Inner monologue**: Longer sentences with literary register
- **Combat dialogue**: Short, cutting each other off
- **Emotional scenes**: Descriptive with metaphors and sensory details

#### Punctuation Patterns
| Mark | Context | Meaning |
|------|---------|---------|
| `...` | Skepticism/hesitation | Skepticism, hesitation, cliffhanger |
| `—` | Dialogue/thought | Direct speech, inner thoughts |
| `!` | Strong emotion | Shouting, action impact |
| `***` | Scene break | Major scene transitions |
| `—0o0—` | Minor break | Within-chapter transitions (UH style) |

#### Formality Levels

| Mức độ | Ngôi xưng | Ngữ cảnh |
|--------|-----------|----------|
| Cao nhất | ngài, tôi | Vua, quý tộc, nghi lễ |
| Cao | tôi, ông, bà | Người lạ, công việc |
| Bình đẳng | mày, tao | Bạn bè thân, đồng đội |
| Thấp | thằng/kẻ (khiếm khuyết) | Đối thủ, khinh bỉ |

**Lưu ý quan trọng:**
- Ngôn ngữ bạn bè thân: "mày/tao" nhưng khi giận chuyển sang "thằng chó"
- Nhân vật yếu thường bị xưng "nó" thay vì "hắn"

### Slang và Vernacular Patterns

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

### Logic Linking Words

| Từ nối | Chức năng | Ví dụ |
|--------|-----------|-------|
| vì | Nguyên nhân | "Vì những lý do không ai biết..." |
| nhưng | Đối lập | "Tuy nhiên, nhưng mà" |
| mà | Liên kết | "Đó là cách... mà cũng là..." |
| tuy nhiên | Đối lập nhẹ | "Tuy nhiên, với những gì..." |
| nên | Kết quả trực tiếp | "Nên cô tạm thời được giải phóng..." |

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

</instructions>
