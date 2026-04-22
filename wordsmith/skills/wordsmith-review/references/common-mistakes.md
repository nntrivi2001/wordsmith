---
name: common-mistakes
purpose: Quick self-check during quality review, identifying common errors
---

<context>
This file is for chapter quality quick self-check. Claude already knows general writing errors; this only lists web novel-specific common problems.
</context>

<instructions>

## Quick Self-Check Checklist

| Check Item | Pass Standard | Violation Consequence |
|------------|--------------|----------------------|
| Combat power reasonable | Protagonist strength less than or equal to state.json | Breaks combat system |
| Cool point exists | At least 1 cool point/chapter | Reader loss |
| Entity recognized | New entities can be auto-extracted by Data Agent | Settings chaos |
| Character consistency | Dialogue/behavior matches character design | OOC breaks immersion |
| Rhythm balanced | No 5+ consecutive chapters same Strand | Aesthetic fatigue |
| Foreshadowing tracked | Foreshadowing can be identified and recorded | Foreshadowing forgotten |

</instructions>

<examples>

<example>
<input>Error: Protagonist at Foundation Building layer 3, defeats Golden Core enemy</input>
<output>
**Combat power collapse**

Fix: If must cross-realm battle, need:
- Cheat/secret technique boost
- Opponent injured/weakened
- Environment advantage/trap assistance
</output>
</example>

<example>
<input>Error: Entire chapter protagonist traveling, no conflict no cool point</input>
<output>
**Cool point missing**

Fix: Arrange during travel:
- Encounter events (bandits/monsters/fortuitous encounters)
- Run into characters (partners/enemies/female lead)
- Discover hidden locations/treasures
</output>
</example>

<example>
<input>Error: Suddenly appear "Purple Cloud Sect," no such faction in settings</input>
<output>
**Unauthorized invention**

Fix:
- Ensure new faction has clear name and description
- Data Agent will auto-extract and ask if should be added to settings
</output>
</example>

<example>
<input>Error: Protagonist personality "reserved and calm," suddenly loses temper out of control</input>
<output>
**Character OOC**

Fix:
- Reference character card personality
- If change needed, must have foreshadowing (touch bottom line/major stimulus)
- Mark reason for personality change
</output>
</example>

<example>
<input>Error: Antagonist dialogue all "You ant!" "How dare you!"</input>
<output>
**Dialogue stereotyped**

Fix:
- C-level antagonists can be stereotyped
- B-level and above should have IQ and personality
- Mockery should be natural and informative
</output>
</example>

</examples>

<errors>
Combat power collapse (cross-realm kill with no reason) = Check state.json, reasonably set opponent
Cool point missing (whole chapter no conflict) = At least 1 cool point, transition chapters also need one
Unauthorized invention (new entity description vague) = Ensure new entities have clear name and description
Character OOC (personality sudden change no foreshadowing) = Reference character card, need foreshadowing for changes
Rhythm monotonous (10 consecutive chapters pure combat) = Check strand_tracker, switch Strand
Foreshadowing forgotten (>100 chapters unrecovered) = Core foreshadowing recovered within 50 chapters
Dialogue stereotyped (antagonist only shouts slogans) = B-level+ antagonists need IQ
</errors>

---

## Vietnamese Webnovel Quality Checklist (8 Error Types)

Use this checklist when reviewing Vietnamese wordsmith content. Flag any violations.

### 1. Units (Đơn vị đo lường)

**Rule**: Use metric units: mét, cm, km, kg. Do NOT use traditional Chinese/Vietnamese units.

**SAI (Wrong)**:
- "Hắn đi được năm trượng" → Use "mét"
- "Cách đó mười dặm" → Use "km"
- "Cây sào ba thốn" → Use "cm"

**ĐÚNG (Correct)**:
- "Hắn đi được năm mét"
- "Cách đó mười kilômét"
- "Cây sào ba centimét"

**Common violations**: trượng, dặm, tấc, thốn, ly, phân

---

### 2. Punctuation (Dấu câu)

**Rule**: Use em-dash `—` (U+2014) for dialogue and inner thoughts. NOT double em-dash `——`.

**SAI (Wrong)**:
- `"——Tao sẽ giết mày ——"` (double em-dash)
- `"——Được rồi——"` (double em-dash)
- `"——Có chuyện gì vậy?——"`

**ĐÚNG (Correct)**:
- `"—Tao sẽ giết mày."` (single em-dash)
- `"—Được rồi."` (single em-dash)
- `"—Có chuyện gì vậy?"`

**Common violations**: `——` anywhere in text; using `—` at end of dialogue without closing punctuation

---

### 3. Sentence Structure (Cấu trúc câu)

**Rule**: Every sentence must have subject + predicate. No fragmented sentences.

**SAI (Wrong)**:
- "Được. Thở được." (fragment, no subject)
- "Chạy. Nhanh." (fragment, no subject)
- "Im lặng." (fragment, no subject)
- "Đứng đó. Không nhúc nhích."

**ĐÚNG (Correct)**:
- "Hắn gật đầu. Hắn thở được."
- "Hắn chạy nhanh."
- "Anh ta im lặng."
- "Nó đứng đó, không nhúc nhích."

**Common violations**: Single-word sentences; action fragments without actor; staccato pacing that breaks immersion

---

### 4. Scene Break Markers (Dấu ngắt cảnh)

**Rule**: Major scene breaks use `***`. Minor scene breaks use `—0o0—`. NOT `---`, NOT single `*`.

**SAI (Wrong)**:
- `---` (triple hyphen, looks like em-dash)
- `*` (single asterisk, looks like emphasis)
- `----` (quadruple hyphen)
- `* * *` (spaced asterisks)

**ĐÚNG (Correct)**:
- `***` (major break: between arcs, time jumps, POV changes)
- `—0o0—` (minor break: within scene, small transition)

**Usage**:
```
Chapter ends with protagonist facing enemy.
*** (major break)
Next chapter opens with protagonist waking up in hospital.
vs
Scene shifts from bedroom to kitchen.
—0o0— (minor break)
```

---

### 5. Ellipsis (Dấu ba chấm)

**Rule**: Use `...` (three connected dots). NOT `. . .` (spaced dots).

**SAI (Wrong)**:
- `"Chờ đã . . ."`
- `"Bảy ngày . . ."`
- `"Khoan đã . . . có gì đó"`

**ĐÚNG (Correct)**:
- `"Chờ đã..."`
- `"Bảy ngày..."`
- `"Khoan đã... có gì đó"`

**Common violations**: Spaced dots anywhere; mixing with other punctuation (`. . .!`)

---

### 6. Vocabulary Accuracy (Độ chính xác từ vựng)

**Rule**: Use contextually correct words. Vietnamese has many synonyms; pick the right one.

**SAI (Wrong)**:
- "Tao sẽ tính sổ từng đồng một" (wrong context - "đồng" = money, should be "đứa" = people)
- "Con dao đâm vào bụng hắn ta" (wrong measure word)
- "Hắn cầm một cây kiếm dài một tấc" (using traditional unit)

**ĐÚNG (Correct)**:
- "Tao sẽ tính sổ từng đứa một" (correct - "đứa" for people)
- "Hắn cầm một cây kiếm dài ba mươi centimét"
- "Lưỡi dao sáng loáng cắm vào tường"

**Common violations**: Mixing up measure words (đồng/đứa/con/cây); using traditional units in modern settings; wrong idioms

---

### 7. Descriptive Specificity (Tính cụ thể của mô tả)

**Rule**: Add subjects to descriptions. Make descriptions concrete and visual.

**SAI (Wrong)**:
- "Lạnh lẽo." (too vague)
- "Nhanh." (too vague - what is fast?)
- "Một bóng đen xuất hiện." (who is the shadow?)
- "Tiếng động." (what sound?)

**ĐÚNG (Correct)**:
- "Anh ta cảm thấy lạnh lẽo run rẩy."
- "Hắn lao nhanh như cơn gió."
- "Một bóng người mặc áo choàng đen xuất hiện trong góc phòng."
- "Tiếng kiếm va nhau звениh trong không khí."

**Common violations**: Adjective-only sentences; passive descriptions without actor; generic nouns without specification

---

### 8. Natural Vietnamese Rhythm (Nhịp điệu tự nhiên tiếng Việt)

**Rule**: Don't copy English/Chinese sentence structures directly. Adapt to Vietnamese patterns.

**SAI (Wrong)**:
- "Anh ta (subject) đã (aux) từ từ (adv) đi (verb) về (dir) phía (prep) căn (n) phòng (n) của (prep) anh ta (pron)." (calque from English)
- "Cô ấy (subject) được (passive) cho là (reporting) đã (aux) nói (verb) rằng (conj)..." (calque from English)
- "Hắn (subject) bước (verb) ra (dir) ngoài (loc) đường (n)." (word-by-word translation)

**ĐÚNG (Correct)**:
- "Anh ta đi về phía căn phòng."
- "Cô ấy nói rằng..."
- "Hắn bước ra đường."

**Common violations**:
- Prepositional phrases at beginning of sentences
- Excessive passive constructions ("được...bởi...")
- Stacked modifiers before nouns
- Direct translation of English relative clauses

**Vietnamese natural order**:
- Subject + Verb + Object/Complement
- Time words at beginning
- Place words after verb
- Descriptive phrases before nouns (but keep readable)

---

## Quick Reference: SAI vs ĐÚNG Examples

| Error Type | SAI | ĐÚNG |
|-----------|-----|------|
| Units | "năm trượng" | "năm mét" |
| Punctuation | `"——Giết——"` | `"—Giết."` |
| Sentence | "Chạy nhanh." | "Hắn chạy nhanh." |
| Scene break | `---` | `***` or `—0o0—` |
| Ellipsis | `. . .` | `...` |
| Vocabulary | "tính sổ từng đồng" | "tính sổ từng đứa" |
| Descriptive | "Lạnh." | "Anh ta run lạnh." |
| Rhythm | "Anh ta đã từ từ đi về phía căn phòng của anh ta." | "Anh ta đi về phía căn phòng." |
