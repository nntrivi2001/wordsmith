---
name: strand-weave-pattern
purpose: Check three-strand balance during chapter planning to avoid monotonous pacing
---

<context>
This file is used for plot strand balance control. Claude already knows multi-strand narrative techniques; this only supplements the wordsmith-specific three-strand weaving mechanism and the tracker structure in state.json.
Note: This file is the shared single source of truth; copying or modifying it in individual Skill's references is prohibited. To update, modify this file.
</context>

<instructions>

## Vietnamese Writing Patterns

> Adapted from STYLE_GUIDE_VN.md for strand balance in Vietnamese wordsmiths.

### VN.1 Pronoun Usage in Three-Strand Context

| Pronoun | Usage | Example |
|---------|-------|---------|
| **tao / mày** | Quest strand — close teammates during battle planning | *"Tao cá là mày chưa từng..."* |
| **hắn / nó** | Quest strand — antagonists, enemies | *"Hắn ta dám..."* |
| **tôi / ngài** | Constellation strand — formal world-building dialogue | *"Ngài có thể giúp tôi..."* |
| **bọn tao / tụi mày** | Fire strand — group interactions, romantic tension | *"Tụi mày có thể sống..."* |

**Key pattern:** Quest strand (55-65% ratio) uses casual pronouns among allies. Constellation strand (world-building) shifts to formal ngài/tôi. Fire strand (romance) mixes casual with formal depending on relationship stage.

### VN.2 Short Punchy Sentences for Quest Scenes

```
"Jack xông ra!"
"Rồi cậu cười."
"Một con Goblin rơi xuống."
```

**Weaving rule:** Quest-dominant chapters keep sentences short (2-4 words) for combat beats. Save long descriptive sentences for Fire or Constellation strands.

### VN.3 Show-Don't-Tell in Fire (Romance) Strand

**Instead of:** "Cô ấy rất giận."

**Write:** "Rosa nghiến răng, nắm chặt tay lại đến trắng bóc. Mắt cô nổ đom đóm."

**Emotion triggers for Fire strand:**
| Emotion | Physical Expression |
|---------|--------------------|
| Giận (Anger) | nghiến răng, nổ gân, mặt đỏ |
| Sợ (Fear) | run bần bật, mặt tái mét |
| Buồn (Sadness) | nước mắt, cười méo, thở dài |
| Bất ngờ (Surprise) | tròn mắt, há hốc, giật mình |

### VN.4 Chapter Cliffhanger Patterns

- **Câu bỏ dở:** "Bảy ngày…C"
- **Twist bất ngờ:** "Là nó. Thanatos."
- **Hành động dở dang:** "Nhưng khi Tanaka ngồi dậy..."

**For strand weaving:** End Quest-dominant chapters on action cliffhangers. End Fire-dominant chapters on emotional ambiguity. End Constellation-dominant chapters on mystery/reveal hooks.

### VN.5 Transition Techniques Between Strands

| Technique | Use Case |
|-----------|----------|
| `***` (ba dấu sao) | Major scene change between strands |
| `—0o0—` | Small scene transitions (UH style) |
| "Sáu năm trước..." | Flashback (switch to earlier strand) |
| "Buổi sáng hôm đó..." | Day change within same strand |

### VN.6 Formality Levels for Strand Voice Consistency

| Level | Pronouns | Strand Context |
|-------|----------|----------------|
| Highest | ngài, tôi | Constellation — royal/nobility scenes |
| High | tôi, ông, bà | Constellation — official/formal worldbuilding |
| Equal | mày, tao | Quest (allies) / Fire (close characters) |
| Low | thằng/kẻ | Quest — enemy/antagonist speech |

**Note:** Friends become "thằng chó" when emotions flare in Quest scenes. Romance scenes between Fire characters use casual pronouns with physical expressiveness rather than formal register.

---

## Three-Strand Definitions and Ratios

| Strand | Ratio | Definition | Typical Plot |
|------|------|------|----------|
| **Quest (Main Storyline)** | 55–65% | Core tasks, leveling, battles, treasure | Sect tournament, secret realm, breakthrough, revenge face-slapping |
| **Fire (Romance Line)** | 20–30% | Emotional relationship development (romance / friendship / master-disciple) | First meeting / flirting, hero saves beauty, relationship confirmed |
| **Constellation (World-building Line)** | 10–20% | Setting expansion, revealing new factions / locations, faction relationships, social networks | Hidden factions revealed, new continent introduced, protagonist's origin hinted |

## Con Duong Ba Chu Strand-Specific Pacing

### Quest Strand (55-65%) — Fast Pacing

**Sentence rhythm:** 70-80% short (1-5 words), 20-30% long
**Trigger types:** Action punches ("Ậm!", "Chết tiệt!"), combat impacts, overlevel counter
**Density target:** High (1.0x multiplier)

**Pattern from "Ta Dung Nhin Võ Lâm Toang":**
```
"Hắn xông ra."
"Kiếm chém xuống."
"Bốp!"
"Máu bắn."
```

**Rules:**
- Keep sentences punchy during combat
- Alternate short impact with brief explanation
- End on action beat or cliffhanger question

### Fire Strand (20-30%) — Slow Pacing

**Sentence rhythm:** 20-30% short, 70-80% long
**Trigger types:** Emotional beats, internal monologue, relationship development
**Density target:** Medium (0.8x multiplier)

**Pattern:**
- Internal monologue with colloquial language
- Physical manifestations (nghiến răng, nắm chặt tay, mắt đỏ)
- Longer descriptive sentences for emotional depth

**Rules:**
- Use "mày/tao" for close characters, "tôi/ngài" for formal moments
- Include physical emotional expression
- End on emotional ambiguity or relationship tension

### Constellation Strand (10-20%) — Medium Pacing

**Sentence rhythm:** 40-50% short, 50-60% long
**Trigger types:** Status reveals, authority challenges, world-building reveals
**Density target:** Medium (0.9x multiplier)

**Pattern:**
- Status card display ("Giám Định!", thẻ trạng thái)
- Formal register (ngài/tôi) for nobility/power scenes
- Mystery hooks and foreshadowing

**Rules:**
- Use formal pronouns for faction leaders, nobles
- Include system/status UI elements for confirmation
- End on mystery or revelation hook

### Strand Transition Patterns

| Transition | Technique | Example |
|------------|-----------|---------|
| Quest → Fire | Emotional pivot | Combat ends → character reflects |
| Fire → Constellation | Context expansion | Romance scene → faction politics intrude |
| Constellation → Quest | Action trigger | Revelation → immediate threat emerges |

### Con Duong Ba Chu Chapter Structure

**Opening (slow):** Descriptive scene-setting, 50-100 words
```
"Một buổi sáng lạnh. Tuyết phủ trắng thung lũng. Hắn đứng trước cổng sect..."
```

**Rising (accelerate):** Action builds, sentences shorten
**Peak (fast):** Cool-point delivery, 1-5 word sentences
```
"Ầm!"
"Hắn văng ra."
"Đứt hết."
```

**Release (decelerate):** Aftermath, longer descriptive
**Hook (slow):** Cliffhanger, single dramatic sentence, creates curiosity

**Cliffhanger patterns from Con Duong Ba Chu:**
- Single dramatic sentence without resolution
- Subverts expectation
- No period at end (implied continuation)
- Examples: "Hắn ta nhìn thẳng vào mắt tôi. Đó là...", "Cô ấy biết. Nhưng mà..."

## Weaving Rules (Low Flexibility — Must Be Executed)

| Rule | Warning Condition | Recommended Action |
|------|----------|----------|
| Quest does not exceed 5 consecutive chapters | `chapters_since_switch >= 5` | Switch to Fire or Constellation |
| Fire does not exceed 10 chapters without appearing | `current - last_fire > 10` | Arrange romance (small sweet moment / jealousy) |
| Constellation does not exceed 15 chapters without appearing | `current - last_constellation > 15` | Reveal new setting / faction / foreshadowing |

## strand_tracker Structure in state.json

```json
{
  "strand_tracker": {
    "last_quest_chapter": 45,
    "last_fire_chapter": 43,
    "last_constellation_chapter": 40,
    "current_dominant": "quest",
    "chapters_since_switch": 3,
    "history": [{"chapter": 46, "dominant": "quest"}, ...]
  }
}
```

Compatibility note:
- `history[].dominant` is the current standard field (written by update_state.py)
- If an older project has `history[].strand`, it should be read with compatibility mapping to `dominant`

## First 30-Chapter Weaving Template

```
Chapters 1–5:   Quest ×5 (fast main plot launch)
Chapter 6:      Fire (first encounter with female lead)
Chapters 7–10:  Quest ×4 (sect tournament)
Chapter 11:     Fire (hero saves beauty)
Chapters 12–14: Quest ×3 (secret realm treasure hunt)
Chapter 15:     Constellation (reveals "Sacred Land" existence)
Chapters 16–19: Quest ×4 (defeat strong enemy)
Chapter 20:     Fire (relationship confirmed)
Chapters 21–24: Quest ×4 (breakthrough in cultivation)
Chapter 25:     Constellation (protagonist origin clue discovered)
Chapters 26–30: Quest ×5 (volume climax)
```

## Vietnamese Webnovel Style Supplement

Based on STYLE_GUIDE_VN.md patterns:

### 12.1 Vocabulary & Nuances

**Pronoun Usage (Đại từ xưng hô):**
| Vietnamese | Context | Example |
|------------|---------|---------|
| Tao / Mày | Equal peers, close friends | *"Tao cá là mày chưa từng..."* |
| Hắn / Nó | Third person (male/female) | *"Hắn ta dám..."* / *"Cô ấy — nó — vẫn còn..."* |
| Ngài / Tôi | Formal, respectful | *"Ngài có thể giúp tôi..."* |

**Pattern:** Pronouns shift with emotion - calm uses "mày", angry switches to "thằng khốn", "con nhóc".

### 12.2 Sentence Structure Patterns

**Short punchy sentences (Action scenes):**
```
"Jack xông ra!"
"Rồi cậu cười."
"Một con Goblin rơi xuống."
```

**Long descriptive sentences (Emotion/sensory):**
```
BNsr Chương 2:
"Lâu đài Chyrse một buổi chiều lặng tuyết buồn tẻ lãng mạn..."
```

**Pacing pattern:**
- Fast-paced (hành động, chiến đấu): Short sentences, strong verbs
- Slow-paced (cảm xúc, nội tâm, cảnh quan): Long descriptive sentences

### 12.3 Show-Don't-Tell in Romance

**Instead of:** "Cô ấy rất giận."

**Write:** "Rosa nghiến răng, nắm chặt tay lại đến trắng bóc. Mắt cô nổ đom đóm."

**Emotion triggers:**
| Emotion | Physical expression |
|---------|---------------------|
| Giận (Anger) | nghiến răng, nổ gân, mặt đỏ, hét lên |
| Sợ (Fear) | run bần bật, mặt tái mét, đứng không vững |
| Buồn (Sadness) | nước mắt, cười méo, thở dài |
| Bất ngờ (Surprise) | tròn mắt, há hốc, giật mình |

### 12.4 Chapter Structure

**Opening Hooks:**
| Type | Example |
|------|---------|
| Action | "Bốp! Choang!" |
| Quote | '"Hẳn các vị ở đây..."' |
| Descriptive | "Bão. Tuyết. Cái lạnh cắt da cắt thịt." |
| Status card | "Thẻ trạng thái..." (UH style) |

**Cliffhanger patterns:**
- Câu bỏ dở: "Bảy ngày…C"
- Twist bất ngờ: "Là nó. Thanatos."
- Action dở dang: "Nhưng khi Tanaka ngồi dậy..."

### 12.5 Transition Techniques

| Technique | When to use |
|-----------|-------------|
| *** (ba dấu sao) | Major scene changes, time jumps |
| —0o0— | Small scene transitions (UH style) |
| "Sáu năm trước..." | Flashbacks |
| "Buổi sáng hôm đó..." | Day change |

### 12.6 Formality Levels

| Level | Pronouns | Context |
|-------|----------|---------|
| Cao nhất (Highest) | ngài, tôi | Royalty, nobility, ceremonies |
| Cao (High) | tôi, ông, bà | Strangers, business |
| Bình đẳng (Equal) | mày, tao | Close friends, teammates |
| Thấp (Low) | thằng/kẻ | Enemies, contempt |

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

## Colloquial vs Literary Register

| Đời thường | Văn chương | Ghi chú |
|------------|------------|----------|
| đi đường | đường đi | Cùng nghĩa, khác trật tự |
| làm gì | làm chi | Hỏi mục đích |
| đâu | ở đâu | Nơi chốn |
| vậy | như vậy / thế | Cách nói |

**Pattern:**
- Nhân vật bình thường dùng ngôn ngữ đời thường
- Khi suy nghĩ nội tâm hoặc mô tả cảnh quan thường dùng văn chương
- Đoạn hội thoại ngắn gọn, đời thường; đoạn độc thoại dùng văn chương hơn

## Logic Linking Words

| Từ nối | Chức năng | Ví dụ |
|--------|-----------|-------|
| vì | Nguyên nhân | "Vì những lý do không ai biết..." |
| nhưng | Đối lập | "Tuy nhiên, nhưng mà" |
| mà | Liên kết | "Đó là cách... mà cũng là..." |
| tuy nhiên | Đối lập nhẹ | "Tuy nhiên, với những gì..." |
| thế là | Kết quả | "Thế là chấm hết." |
| nên | Kết quả trực tiếp | "Nên cô tạm thời được giải phóng..." |
| đằng | Mặc dù | "Đằng ấy thì sao?" |
| thậm chí | Nhấn mạnh | "Thậm chí ngay cả..."

## Inverted Syntax Patterns

**Mẫu phổ biến:**
```
Bình thường: Rosa đứng dậy.
Đảo ngược: Đứng dậy Rosa. (Sách vở)

Bình thường: Hắn ta đi ra ngoài.
Đảo ngược: Ra ngoài hắn ta đi. (Cổ xưa)
```

**Sử dụng khi:**
- Văn phong cổ đại/quý tộc: "Này thưa công tước..."
- Thơ ca/mô tả cảm xúc: "Buồn bã cô bước đi..."
- Nhấn mạnh hành động: "Chết đi! Chết mẹ mày đi!"

## Subordinate Clause Patterns

| Loại | Cấu trúc | Ví dụ |
|------|----------|-------|
| Nguyên nhân | vì... nên... | *"Vì mệnh lệnh từ Jack bất ngờ..."* (BNsr Chương 5) |
| Kết quả | ...nên... | *"Nên cô tạm thời được giải phóng..."* |
| Điều kiện | nếu... thì... | *"Nếu một ngày kia rồng chúa quay trở lại..."* |
| Nhượng bộ | tuy... nhưng... | *"Tuy nhiên, dù bản thân có thể..."* |
| Thời gian | khi... thì... | *"Khi còn nhỏ tôi đã nhìn..."* (BNsr Chương 1) |

## Metaphor Patterns (Ẩn dụ)

**So sánh thường gặp:**
| So sánh | Ý nghĩa |
|---------|---------|
| "lửa đỏ" + rồng | Sức mạnh, nguy hiểm |
| "tuyết tan" | Cảm xúc ấm áp, tình yêu |
| "bóng ma" | Sự mất mát, ám ảnh |
| "cái lưỡi câu" | Tình yêu đau đớn |
| "sợi dây câu" | Kết nối không thể thoát |

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

<examples>

<example>
<input>Currently Chapter 46, last_quest=45, last_fire=43, last_constellation=40, current_dominant="quest", chapters_since_switch=3</input>
<output>
**Warning Assessment**:
- Quest 3 consecutive < 5 → No warning yet
- Fire gap 3 < 10 → No warning yet
- Constellation gap 6 < 15 → No warning yet

**Chapter Recommendation**: Quest may continue, but it is recommended to arrange Fire within the next 1–2 chapters to regulate rhythm
</output>
</example>

<example>
<input>Currently Chapter 55, last_fire=42, 13 consecutive chapters without romance</input>
<output>
⚠️ **Warning**: Distance from last romance > 10 chapters!

**Recommendation**: Arrange Fire strand this chapter
- Option A: Female lead appears, small sweet interaction
- Option B: Hero saves beauty scene
- Option C: Jealousy / misunderstanding subplot
</output>
</example>

<example type="edge_case">
<input>First 10 chapters need to quickly establish the main plot; can the romance line be less?</input>
<output>
✅ Yes. First 10 chapters ratio can be adjusted to:
- Quest: 70–80%
- Fire: 10–15%
- Constellation: 5–10%

But Chapters 6–8 must include at least 1 Fire event (first meeting / impression establishment)
</output>
</example>

</examples>

<errors>
❌ 10 consecutive chapters of pure Quest → ✅ Switch after a maximum of 5 chapters
❌ Romance line absent for >10 chapters → ✅ Arrange one every 5–10 chapters
❌ World-building line absent for >15 chapters → ✅ Reveal new setting every 10–15 chapters
❌ Forgot to update strand_tracker after switching strands → ✅ Automatically updated at the end of each chapter
</errors>