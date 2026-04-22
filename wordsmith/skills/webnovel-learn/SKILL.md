---
name: webnovel-learn
description: Extract successful writing patterns from the current session and write them to project_memory.json
allowed-tools: Read Write Bash
---

# /webnovel-learn

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

- Must be executed from the project root directory (`.webnovel/state.json` must exist)
- If the file does not exist in the current directory, ask the user for the project path and `cd` into it
- After entering, set the variable: `$PROJECT_ROOT = (Resolve-Path ".").Path`

## Objective
- Extract reusable writing patterns (hooks / pacing / dialogue / micro-payoffs, etc.)
- Append them to `.webnovel/project_memory.json`

## Vietnamese Style Patterns

When extracting patterns for Vietnamese webnovels, apply these STYLE_GUIDE_VN.md conventions:

### Vocabulary & Nuances

#### Pronoun System (Đại từ xưng hô)
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
- Protagonists use "tao-mày" with each other but "tôi-ngài" with strangers
- Weak characters often called "nó" instead of "hắn"

#### Formality Levels
| Level | Pronouns | Context |
|-------|----------|---------|
| Highest | ngài, tôi | King, nobility, ceremonies |
| High | tôi, ông, bà | Strangers, business |
| Equal | mày, tao | Close friends, teammates |
| Low | thằng/kẻ (defective) | Enemies, contempt |

#### Colloquial vs Literary Register
| Colloquial | Literary | Meaning |
|------------|----------|---------|
| đi đường | đường đi | Same meaning, different order |
| làm gì | làm chi | Asking purpose |
| sao | như thế nào | Asking how |
| vậy | như vậy / thế | Way of saying |

**Pattern**:
- Normal characters use colloquial language
- Inner thoughts or scenic descriptions use literary
- Short dialogue = colloquial; monologue = literary

#### Slang & Vernacular
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

### Sentence Structure

#### Simple vs Compound Sentences
**Simple (action fast pace)**:
```
"Jack xông ra!" (BNsr Chương 1)
"Rồi cậu cười." (BNsr Chương 3)
"Một con Goblin rơi xuống." (UH Chương 4)
```

**Compound (thoughts, scenery)**:
```
"Loài rồng từng là biểu tượng thiêng liêng của sức mạnh và lòng kiêu hãnh."
"Cô - đứa con gái lớn lên bằng thịt sống, cắn nhau với lũ rồng con..."
```

**Pattern**:
- Combat: Short, rapid-fire
- Inner thoughts: Long, multi-clause
- Tense dialogue: Short, cutting across each other

#### Inverted Syntax
**Normal**: Rosa đứng dậy.
**Inverted**: Đứng dậy Rosa. (Literary)

**Normal**: Hắn ta đi ra ngoài.
**Inverted**: Ra ngoài hắn ta đi. (Archaic)

**Usage**:
- Archaic/noble speech: "Này thưa công tước..."
- Poetry/emotion: "Buồn bã cô bước đi..."
- Emphasis: "Chết đi! Chết mẹ mày đi!"

### Rhetorical Devices

#### Ellipsis (...)
| Context | Meaning |
|---------|---------|
| Prolonged thought | "Cô ấy đang nghĩ... về những ký ức..." |
| Hesitation | "Ờ... để tớ nghĩ lại..." |
| Cliffhanger | "Bảy ngày…" (BNsr Chương 1) |
| Interrupted | "Không... không phải tôi..." |

#### Em dash (—)
| Context | Usage |
|---------|-------|
| Dialogue | "—Ngài có thể giúp tôi không?" |
| Inner thoughts | "—Cô ấy thật yếu đuối..." |
| Explanation | "Anh ấy — kẻ đã chết — vẫn còn ở đây..." |
| Emphasis | "Sao tự nhiên lại cười — điên à?" |

### Pacing Patterns

#### Fast-paced (Action/Combat)
```
BNsr Chương 1:
"Kiếm chạm kiếm tóe lửa. Jack bị hất văng về phía sau, lại lao lên.
-Đánh trả đi - anh rít lên.
-Nghe em nói đã!"
```

#### Slow-paced (Emotional/Scenic)
```
BNsr Chương 3:
"Mùa xuân đến và Ardisia sẽ nở - loài hoa dại thân thảo mọc dày đặc hai bên bờ trải lớp thảm hoa trắng muốt. Mùa hè những ngọn thông cháy trụi lại mọc lên cao vút, xanh mướt..."
```

**Pattern**:
- Chapter opening: Long, descriptive for setting
- Combat: Extremely short, strong verbs
- Climax: Alternating short-long-short
- Cliffhanger ending: 1-2 short sentences, incomplete

### Chapter Patterns

#### Opening Hooks
| Type | Example | Source |
|------|---------|--------|
| Action | "Bốp! Choang!" | BNsr Chương 1 |
| Quote | '"Hẳn các vị ở đây..."' | UH Chương 1 |
| Flashback | "Khi còn nhỏ tôi đã..." | BNsr Chương 1 |
| Descriptive | "Bão. Tuyết. Cái lạnh..." | BNsr Chương 2, 3 |
| Status card | "Thẻ trạng thái..." | UH Chương 1 |

#### Cliffhangers
- "Bảy ngày…C" - incomplete sentence
- "Là nó. Thanatos." - twist reveal
- "Nhưng khi Tanaka ngồi dậy..." - action dangling
- "—0o0—" separator then chapter end

#### Scene Transitions
| Method | Usage |
|--------|-------|
| `***` | Major scene change, time shift |
| `—0o0—` | Minor scene within UH |
| Time change | "Sáu năm trước..." |
| Location change | "Ở trong khu rừng, Tanaka tuyệt nhiên..." |

### Show-Don't-Tell Emotional Triggers
| Emotion | Physical Expression |
|---------|---------------------|
| Giận (anger) | nghiến răng, nổ gân, mắt nổ đom đóm |
| Sợ (fear) | run bần bật, mặt tái mét, đứng không vững |
| Buồn (sad) | nước mắt lã chã, cười méo, thở dài |
| Bất ngờ (surprise) | tròn mắt, há hốc mồm, giật mình |
| Tức giận cực độ | hét lên, khặc ặc, cười điên cuồng |
| Xúc động | nghẹn bứ, run lên, khóc nức nở |

### Genre-Specific (Isekai/Gaming)

#### Status Card Format (UH Style)
```
[Tên nhân vật]
(Tình trạng: ...)
-Chủng loài:
-Tuổi:
-Chức nghiệp:
-Cấp:
Mana: X/Y
Sức khỏe: X
-Kĩ năng:
+[Tên] (Cấp X) (Độc nhất nếu có)
```

#### Combat Structure
1. See enemy → Check status (Giám định)
2. Assess strength
3. Tactics
4. Action
5. Result + loot/exp

#### Training Pacing
- Level up when exp sufficient
- Need to hunt monsters to level
- 5% chance recovery on level up (adjustable)

#### Underdog-to-Stronger (Tanaka pattern)
1. Weakest, despised - lowest stats
2. Find unique skill
3. Train hard
4. Surprise victory
5. Gradually get recognized

### Metaphor Patterns (BNsr)
| Metaphor | Meaning |
|----------|---------|
| "lửa đỏ" + rồng | Power, danger |
| "tuyết tan" | Warm emotion, love |
| "bóng ma" | Loss, haunting |
| "cái lưỡi câu" | Painful love |
| "sợi dây câu" | Unbreakable connection |

## Input
```bash
/webnovel-learn "The crisis hook design in this chapter is very effective — suspense is maximized"
```

## Output
```json
{
  "status": "success",
  "learned": {
    "pattern_type": "hook",
    "description": "Crisis hook design: suspense maximized",
    "source_chapter": 100,
    "learned_at": "2026-02-02T12:00:00Z"
  }
}
```

## Execution Flow
1. Read `"$PROJECT_ROOT/.webnovel/state.json"` to get the current chapter number (`progress.current_chapter`)
2. Read `"$PROJECT_ROOT/.webnovel/project_memory.json"`; if it does not exist, initialize with `{"patterns": []}`
3. Parse the user input and classify `pattern_type` (hook / pacing / dialogue / payoff / emotion)
4. Append the record and write the file back

## Constraints
- Do not delete old records — append only
- Avoid completely duplicate descriptions (deduplication is allowed)
