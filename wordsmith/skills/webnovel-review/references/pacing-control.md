---
name: pacing-control
purpose: Loaded when reviewing rhythm, diagnosing water-floating and dragging issues
---

<context>
This file is for rhythm review and water-floating diagnosis. Claude already knows narrative rhythm techniques; this only supplements web novel-specific information density standards and fast-paced writing.
</context>

<instructions>

## Information Density Standard

**Core metric**: At least 1 substantial plot point per 1000 words

**Substantial plot point definition**:
- Protagonist obtains new information/clues/abilities
- Interpersonal relationship changes (likability 10, hatred 10)
- Combat power improvement/breakthrough/learns new move
- Plot twist (new conflict/new goal/new crisis)
- Foreshadowing planted or recovered
- Pure scenery description (unless strongly plot-related)
- Repeated inner monologue
- Meaningless dialogue (small talk greetings)

**Scoring standards**:

| Information Density | Cool Point Quantity | Invalid Content | Judgment |
|-------------------|--------------------|-----------------|----------|
| < 800 words/point | 2 or more | None | Excellent 90-100 |
| 800-1000 words/point | 1 | Very little | Good 70-89 |
| 1000-1500 words/point | 1 | Some | Pass 50-69 |
| > 1500 words/point | 0 | Lots | Fail, need rewrite |

## Fast Rhythm vs Slow Rhythm

| Dimension | Slow rhythm (traditional novel) | Fast rhythm (web novel) |
|-----------|-------------------------------|-------------------------|
| Cultivation | 3 chapters describe cultivation process | 3 lines to explain, 4th line breakthrough |
| Foreshadow | 5000 words foreshadow antagonist | 500 words foreshadow, direct conflict |
| Decision | Protagonist agonizes for 2 chapters | Protagonist agonizes for 2 paragraphs, immediately acts |
| Dungeon | 20 chapters complete | 5-8 chapters complete |

## Chapter Structure Template

**Standard chapter (3000-5000 words)**:
```
Opening 300-500 words: Connect to last chapter + set scene
Setup 800-1200 words: Introduce this chapter's core conflict
Development 1000-1500 words: Advance plot + cool point prelude
Climax 500-800 words: This chapter's cool point explosion
Ending 300-500 words: Afterglow + introduce next chapter suspense
```

**Transition chapter (avoid water-floating)**:
```
Review 200-300 words: Last stage's gains
New goal 500-700 words: Establish next plan
Preparation 1000-1500 words: Prepare for next arc
Small conflict 500-800 words: Insert small cool point (must have!)
Suspense 200-300 words: Lead to next arc
```

## Genre-Specific Rhythm Standards

| Genre | Cool Point Density | Information Density | Foreshadow Tolerance |
|-------|-------------------|--------------------|---------------------|
| Fantasy Cultivation | 1 major cool point every 5-8 chapters | 500-1000 words/point | Medium |
| Urban Shuangwen | 1 major cool point every 3-5 chapters | 400-800 words/point | Low |
| Mystery Reasoning | 1 major cool point every 10-15 chapters | 600-1200 words/point | High |
| Zhihu Short | At least 1 small cool point per chapter | 300-500 words/point | Extremely low |

</instructions>

<examples>

<example>
<input>Cultivation breakthrough chapter - Original 1200 words, 1 plot point</input>
<output>
**Water-floating version** (1200 words, 1 plot point):
Lin Tian sits cross-legged, starts operating technique... (500 words detailed description)
Spiritual energy slowly enters body... (300 words process description)
Time passes second by second... (200 words)
Finally breaks through! (50 words)
Information density = 1200 words/point = Severely dragged

**Streamlined version** (90 words, 3 plot points):
Lin Tian sits cross-legged, Devouring System frantically absorbs Thunder Fruit energy.
Three hours later—"Boom!" Foundation Building layer 8!
Lin Tian opens eyes, clenches fist, air screams.
Outside comes exclamation: "Broke through in three days?"
Information density = 30 words/point = Tight rhythm
</output>
</example>

<example>
<input>Traveling transition scene</input>
<output>
**Water-floating version** (800 words):
Lin Tian walks on mountain road, looking at trees on both sides... (inner monologue 300 words)
On the road encounters a rabbit... (observes rabbit 200 words)
Several clouds float over... (describe weather 300 words)

**Streamlined version** (80 words):
Lin Tian traveled for three days, finally arrived at Blood Evil Secret Realm entrance. Just stepping into the secret realm, a dangerous aura hits face.
</output>
</example>

<example>
<input>Detected 500 consecutive words with no plot advancement</input>
<output>
**Severe dragging marker**

Correction options:
A) Delete that paragraph
B) Compress to 1-2 sentences
C) Insert micro-conflict (passerby provokes/accident)
</output>
</example>

</examples>

<errors>
Information density > 1500 words/point = Compress or add plot points
Whole chapter no cool point = At least insert 1 small cool point
Foreshadow exceeds 2000 words still no conflict = Immediately accelerate
Transition chapter pure transition no conflict = Must have small cool point
Consecutive 500 words pure description = Delete or compress
</errors>

---

## Appendix: Vietnamese Webnovel Rhythm Patterns

### Vietnamese Sentence Structure (from STYLE_GUIDE_VN.md)

**Short punchy sentences (action/fight scenes):**
```
"Jack xông ra!" (BNsr Chương 1)
"Bắn!"
"Chết tiệt!"
```

**Long descriptive sentences (emotional/sensory):**
```
"Lâu đài Chyrse một buổi chiều lặng tuyết buồn tẻ lãng mạn..."
"Có một nụ cười làm tuyết tan."
```

### Vietnamese Punctuation for Pacing

| Punctuation | Usage | Example |
|------------|-------|---------|
| `...` | Prolonged thought, cliffhanger | `"Bảy ngày…"` |
| `—` | Dialogue, inner thoughts | `"—Cô ấy đi rồi."` |
| `!` | Action impact, shouting | `"JACKKKK!!!!"` |
| `***` | Major scene transition | Between arcs |

### Fast vs Slow Rhythm (Vietnamese Style)

**Fast-paced examples:**
```
"Hắn nghiến răng; tay vẫn giơ kiếm."
"Kiếm chạm kiếm tóe lửa. Jack bị hất văng về phía sau, lại lao lên."
```

**Slow-paced examples:**
```
"Mùa xuân đến và Ardisia sẽ nở - loài hoa dại thân thảo mọc dày đặc..."
"Erever như tờ giấy mỏng manh điểm xuyến những ngọn thông xanh sẫm..."
```

### Emotion-to-Physical Expression Mapping

| Emotion | Vietnamese Signs |
|---------|------------------|
| Giận (Anger) | nghiến răng, nổ gân, mắt nổ đom đóm, hét lên |
| Sợ (Fear) | run bần bật, mặt tái mét, đứng không vững |
| Buồn (Sadness) | nước mắt lã chã, cười méo, thở dài |
| Bất ngờ (Surprise) | tròn mắt, há hốc mồm, giật mình |

### Dialogue Voice vs Narration Voice (VN Style)

**Dialogue voice:** Short, direct, colloquial (đời thường)
**Narration voice:** Longer, descriptive, literary (văn chương)

### Clue Hiding Patterns (for Mystery)

When placing clues in Vietnamese webnovel context:
- Use short declarative sentences for obvious clues
- Use descriptive narration for hidden clues
- End chapters with `...` or unfinished actions for suspense
- Use `"—0o0—"` for small scene transitions

---

## Pacing Violations from the 8 Error Types

These errors directly impact rhythm and pacing quality:

### 1. Sentence Structure Breaks Pacing

**Fragmented sentences** (Error Type 3) disrupt reading flow:
```
SAI: "Chạy. Nhanh. Tránh né."
ĐÚNG: "Hắn chạy nhanh, tránh né từng đường kiếm."
```
**Rule**: Use complete sentences with subject + predicate. Fragments feel staccato and amateurish.

---

### 2. Improper Scene Breaks Kill Momentum

**Wrong markers** (Error Type 4) confuse readers:
```
SAI: "---" used for major break (looks like em-dash in prose)
ĐÚNG: "***" for major, "—0o0—" for minor
```
**Rule**: Major breaks (`***`) between arcs. Minor breaks (`—0o0—`) within scenes. Wrong markers break immersion.

---

### 3. Punctuation Errors Slow Reading

**Double em-dash** (Error Type 2) looks amateur:
```
SAI: "——Mày nghĩ mày là ai——"
ĐÚNG: "—Mày nghĩ mày là ai?"
```
**Rule**: Single `—` for dialogue. Double `——` is only for ornamental use (rare).

---

### 4. Vocabulary Errors Create Confusion

**Wrong word choice** (Error Type 6) breaks reader trust:
```
SAI: "Tao sẽ tính sổ từng đồng một" (sounds like accounting)
ĐÚNG: "Tao sẽ tính sổ từng đứa một" (sounds like revenge)
```
**Rule**: Match vocabulary to context. Readers notice wrong word choices.

---

### 5. Vague Descriptions Drag Pacing

**Generic descriptions** (Error Type 7) cause readers to skim:
```
SAI: "Một tiếng động vang lên."
ĐÚNG: "Thanh kiếm звениh khi chạm vào khiên."
```
**Rule**: Be specific. Concrete details create mental imagery faster than vague summaries.

---

### 6. Non-Natural Rhythm Feels Translated

**English/Chinese sentence order** (Error Type 8) feels stilted in Vietnamese:
```
SAI: "Anh ta đã từ từ và cẩn thận đi về phía căn phòng của anh ta."
ĐÚNG: "Anh ta lon ton đi vào phòng."
```
**Rule**: Use natural Vietnamese word order. Transliterated structures slow readers down.

---

## Fast-Paced Vietnamese Patterns (Correct Implementation)

### Action Scenes (use Error Type 3 + 7 + 8)
```
Hắn lao tới. Kiếm chém xuống.
Bùm! Đối phương văng ra, máu bắn tung tóe.
Hắn không dừng, lao tiếp.
```
- Short sentences with subject + verb
- Onomatopoeia (Bùm!, Ầm!, Chát!)
- No unnecessary adjectives

### Emotional Scenes (use Error Type 5 + 7)
```
"Ngày hôm đó... trời mưa to..."
"Anh ấy đứng đó, mưa ướt áo, mắt đỏ hoe."
```
- Ellipsis for pauses
- Concrete sensory details
- Subject included in descriptions

### Dialogue Pacing (use Error Type 2 + 6)
```
"—Mày là ai?"
"—Tao là kẻ sẽ giết mày."
```
- Single em-dash
- Short exchanges
- Vocabulary matches character voice

---

## Scene Transition Pacing Standards

| Transition Type | Marker | Pacing | Example |
|----------------|--------|--------|---------|
| Major arc break | `***` | Full stop, new chapter feel | Between volumes |
| Minor scene shift | `—0o0—` | Brief pause | POV change, location change within scene |
| Time skip (small) | `...` | Ellipsis in narration | "Ba ngày sau..." |
| Time skip (major) | `***` | Scene break with time indicator | "***Ba tháng sau***" |

---

## Rhythm Diagnosis Questions

When checking pacing, ask:
1. Are sentences complete with subject + predicate? (Error Type 3)
2. Are scene breaks marked correctly? (Error Type 4)
3. Is punctuation correct (em-dash not double)? (Error Type 2)
4. Are descriptions concrete, not vague? (Error Type 7)
5. Is sentence rhythm natural Vietnamese, not translated? (Error Type 8)
