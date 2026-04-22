---
name: core-constraints
purpose: Load before every chapter writing to ensure the three laws are executed
---

<context>
This file is used for core constraint checking during chapter writing. Claude already knows general writing standards; this only supplements the webnovel-specific anti-hallucination protocol.
Note: This file is the shared single source of truth; copying or modifying it in individual Skill's references is prohibited. To update, modify this file.
</context>

<!-- Vietnamese Writing Patterns (from STYLE_GUIDE_VN.md) -->

<vn_patterns>

## Vietnamese Pronoun & Formality System

| Mức độ | Ngôi xưng | Ngữ cảnh |
|--------|-----------|----------|
| Cao nhất | ngài, tôi | Vua, quý tốc, nghi lễ |
| Cao | tôi, ông, bà | Người lạ, công việc |
| Bình đẳng | mày, tao | Bạn bè thân, đồng đội |
| Thấp | thằng/kẻ (khiếm khuyết) | Đối thủ, khinh bỉ |

**Quan trọng:**
- Nhân vật chính dùng "tao-mày" với nhau nhưng "tôi-ngài" với người lạ
- Đại từ xưng hô thay đổi theo cảm xúc: Bình thường "mày/mày", khi giận chuyển sang "thằng khốn", "con nhóc"
- Slang mạnh: "thằng chó", "chó đẻ", "khốn" khi căng thẳng

## Vietnamese Sentence Structure

**Câu ngắn (action chiến đấu):**
- "Jack xông ra!" / "Ầm!" / "Chết tiệt!"
- Hành động nhanh: Câu đơn, dồn dập

**Câu dài (nội tâm, cảnh quan):**
- Mô tả suy nghĩ, cảm xúc: Nhiều mệnh đề, văn chương

**Cú pháp đảo ngược (văn phong cổ đại/quý tộc):**
- "Đứng dậy Rosa." / "Ra ngoài hắn ta đi."

## Vietnamese Punctuation & Rhythm

| Dấu | Chức năng | Ví dụ |
|-----|-----------|-------|
| ... | Suy nghĩ kéo dài, cliffhanger | "Bảy ngày…" |
| — | Đối thoại, inner thoughts | "—Cô ấy đi rồi." |
| !!! | Shouting, cảm xúc mạnh | "JACKKKK!!!!" |
| "..." | Đối thoại trực tiếp | '"Cậu có sao không?"' |

**Pacing:**
- Action scenes: Câu cực ngắn, động từ mạnh, xen kẽ sound effects
- Emotional scenes: Câu dài hơn, descriptive, sử dụng ẩn dụ
- Căng thẳng leo thang: Câu dần ngắn lại, ít dấu câu
- Cliffhanger kết chương: 1-2 câu ngắn, bỏ dở

## Show-Don't-Tell (Vietnamese Style)

| Cảm xúc | Biểu hiện cụ thể |
|---------|-------------------|
| Giận | nghiến răng, nổ gân, mặt đỏ, hét lên |
| Sợ | run bần bật, mặt tái mét, đứng không vững |
| Buồn | nước mắt, cười méo, thở dài |
| Vui | cười phá lên, mỉm cười, nhảy lên |
| Bất ngờ | tròn mắt, há hốc, giật mình |

**Thay vì:** "Cô ấy rất giận."
**Viết:** "Rosa nghiến răng, nắm chặt tay lại đến trắng bóc. Mắt cô nổ đom đóm."

## Genre-Specific: Isekai/Gaming (Vietnamese Style)

**Thẻ trạng thái cấu trúc:**
```
[Tên nhân vật]
(Tình trạng: ...)
-Chủng loài:
-Giới tính:
-Tuổi:
-Chức nghiệp:
-Cấp:
Mana: X/Y
Sức khỏe: X
Phòng thủ: X
Nhanh nhẹn: X
Dẫn suất ma lực: X
-Kĩ năng:
+[Tên] (Cấp X) (Độc nhất nếu có)
```

**Combat structure:**
1. Thấy địch → Check thẻ trạng thái (Giám định)
2. Đánh giá sức mạnh
3. Chiến thuật
4. Hành động
5. Kết quả + loot/exp

**Underdog-to-stronger pattern:**
1. Yếu nhất, bị khinh thường (chỉ số thấp nhất)
2. Tìm ra skill độc đáo (ví dụ: "Cơ Địa Kẻ Vô Dụng" giảm 80% exp)
3. Rèn luyện chăm chỉ
4. Chiến thắng bất ngờ
5. Dần được công nhận

## Scene Transitions (Vietnamese Style)

| Phương pháp | Sử dụng |
|-------------|---------|
| *** | Chuyển cảnh lớn, thay đổi thời gian |
| —0o0— | Chuyển cảnh nhỏ trong UH |
| "Sáu năm trước..." | Flashback |
| Dòng trắng | Ngắt đoạn |

</vn_patterns>

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

<instructions>

## Three Laws (Low Flexibility — Must Be Precisely Executed)

| Law | Rule | Check Method |
|------|------|----------|
| **Outline is Law** | Strictly follow the outline; no ad-lib | Cross-reference outline during review |
| **Setting is Physics** | Combat power / skills / items ≤ what is recorded in index.db | Query and confirm before writing |
| **Inventions Must Be Registered** | New entities auto-extracted by Data Agent | Processed after chapter completion |

## New Entity Processing Flow

Current rules: Body text no longer requires XML tags:

1. **During writing**: Write plain body text directly; describe new characters / locations / items normally
2. **After completion**: Data Agent automatically identifies new entities and writes to index.db
3. **Uncertain entities**: Data Agent marks as uncertain; requires manual confirmation

## Chapter Constraint Layers

### Hard (Must)

- Chapter readability meets baseline: readers can answer "what happened / who is doing what / why"
- Chapter must have clear progression: at least one identifiable item among question / goal / cost / relationship change / information change
- If the previous chapter had a clear promise (hook / unclosed question), this chapter must respond (partial fulfillment is allowed; one-time full settlement not required)
- No placeholder text in output (e.g., `[TBD]`, `[TODO]`, `...(omitted)...`)

### Soft (Recommended)

- Enter conflict / risk / strong emotion as early as possible in the chapter opening (recommended first 200–400 characters; the fixed 120-character rule is no longer enforced)
- Unclosed questions or next-chapter anticipation anchors are recommended at chapter end or later sections (not limited to "last 80–150 characters")
- Situation changes are recommended to maintain rhythmic sense (reference: one pulse per 800–1400 characters; short chapters require at least one substantial change)
- Micro-payoff frequency follows genre profile recommendations; mechanical equal spacing is not required

### Style (Optional Enhancement)

- Dialogue should carry intent where possible (probing / evading / pressuring / inducing); minimize pure exposition
- Avoid consecutive long passages of pure explanation; if explanation is necessary, split into "information + action/reaction"
- Avoid mechanical endings like "went back to rest"; if using a calm ending, retain an unclosed anticipation

## Cool-Points and Rhythm (Adjust Per Genre Profile)

- Cool-point density is determined jointly by genre and chapter type: transition chapters allow lower density, but "entire chapter with no gains" is not allowed
- Combo and milestone cool-points are evaluated using a rolling window (5 chapters / 10–15 chapters); used for early warning, not as per-chapter mandatory judgments
- When the same type of cool-point repeats for 3 consecutive chapters, it is flagged as a risk; prioritize type variation or differentiated execution to correct

## Con Duong Ba Chu Pacing Control

### Pacing by Scene Type

| Scene Type | Sentence Length | Rhythm | Example |
|------------|----------------|--------|---------|
| Action combat | 1-5 words | Fast, punchy | "Ầm! Hắn văng ra." |
| Emotional | 10-25 words | Slow, descriptive | "Rosa nghiến răng, nắm chặt tay..." |
| Status reveal | 5-15 words | Medium | "Giám Định! Thẻ trạng thái xuất hiện." |
| Cliffhanger | Single sentence | Sudden stop | "Nhưng khi hắn quay lại..." |

### Cool-Point Density Calculation

**Formula per chapter:**
```
Density = (Action_Punches × 1.0) + (Emotional_Beats × 0.8) + (Status_Reveals × 1.5)
```

**Con Duong Ba Chu benchmarks:**
- Transition chapter: density 2.0-4.0
- Standard chapter: density 4.0-7.0
- Milestone chapter: density 6.0-10.0+

**Rolling check (5 chapters):**
- Average < 3.0 for 3 consecutive → flag for combo cool-point
- Average > 8.0 for 5 consecutive → reduce to prevent fatigue

### Strand Distribution (Vietnamese Webnovel Standard)

| Strand | Ratio | Primary Cool-Point Type |
|--------|-------|-------------------------|
| Quest | 55-65% | Action punch, overlevel counter |
| Fire | 20-30% | Emotional beat, sweet exceeded |
| Constellation | 10-20% | Status reveal, authority challenge |

## Strand Balance Warnings

| Strand | Warning Condition |
|--------|------|
| Quest (main plot) | >5 consecutive chapters |
| Fire (romance) | >10 chapters without appearance |
| Constellation (world-building) | >15 chapters without appearance |

## Prohibited Items

- `[TBD]`, `[TODO]`, `...(omitted)...` → Must be fully written out
- No aftermath description after battle (for urban superpower genre)

</instructions>

<examples>

<example>
<input>Protagonist needs to use "Thunder Palm" to defeat the enemy</input>
<output>
1. Check if the "Thunder Palm" skill exists in index.db
2. If yes: use directly
3. If no: describe the acquisition path in the body text (e.g., apprenticeship / enlightenment / inheritance); Data Agent will automatically extract
</output>
</example>

<example type="edge_case">
<input>Plot requires protagonist to display Foundation Building strength, but index.db shows Qi Refining Layer</input>
<output>
❌ Write Foundation Building combat power directly → Violates "Setting is Physics"
✅ First arrange a breakthrough scene; Data Agent updates index.db; then display new strength
</output>
</example>

</examples>

<errors>
❌ New entity description is vague (cannot be auto-identified) → ✅ Ensure new entities have clear names and descriptions
❌ Protagonist suddenly knows a new skill → ✅ First describe the acquisition path
❌ Power setting is inconsistent → ✅ Query index.db to confirm before writing
❌ Entire chapter with no progression point (no goal / no cost / no change) → ✅ Add at least one identifiable progression
</errors>