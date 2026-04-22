---
name: foreshadowing
purpose: Loaded when urgently analyzing and managing foreshadowing
---

<context>
This file is for foreshadowing management reference. Claude already knows general narrative foreshadowing techniques; this only supplements web novel-specific foreshadowing layers, recovery cycles, and urgency calculations.

**Vietnamese Webnovel Patterns**:
- Foreshadowing in VN wordsmiths often uses "duyên" (fate/destiny) connections
- Xuanhuan (Fantasy) foreshadowing frequently involves dragon-related mythology
- Isekai/Game genre commonly uses "thẻ trạng thái" (status card) system hints
- Cliffhanger patterns: "...", "—0o0—" separator, cliffhanger endings
- Harem/Romance foreshadowing: early hints at character interests and rivalries
</context>

<instructions>

## Foreshadowing Layer Classification

| Layer | Recovery Cycle | Weight | Examples |
|-------|---------------|--------|----------|
| **Core** | 50-300 chapters | 3.0x | Protagonist's identity, ultimate enemy, cheat ability origin |
| **Sub-line** | 30-100 chapters | 2.0x | Supporting character motivation, mysterious item, sect secrets |
| **Decorative** | 10-30 chapters | 1.0x | Scene details, small habits, passerby mentions |

## Urgency Calculation

```
Urgency = (Chapters elapsed / Target chapter) x Layer weight
```

**Status determination**:
- Critical: Exceeded target chapter OR Core foreshadow >50 chapters unrecovered
- Warning: >80% target OR Sub-line >80 chapters unrecovered
- Normal: Within planned range

## Foreshadowing Planting Techniques

| Technique | Method | Example |
|----------|--------|---------|
| Casual plant | Naturally mention during normal plot | While browsing books in library, see "Devouring Heaven Divine Art" legend |
| Dialogue plant | Reveal through character dialogue | "Your constitution is very special..." |
| Detail plant | Inconspicuous detail | Broken temple statue is missing one arm |
| Dream plant | Hint future through dreams | Dream of blood-colored world and blurry figure |

## Foreshadowing Recovery Methods

| Method | Applicable Layer | Effect |
|--------|-----------------|--------|
| Direct reveal | Shallow | Quick explanation |
| Layer-by-layer reveal | Middle | Gradually reveal truth |
| Unexpected reversal | Deep | Create surprise shock |

## Foreshadowing Density Suggestions

| Work Length | Shallow | Middle | Deep |
|------------|--------|--------|------|
| Short (100K words) | 5-10 | 2-3 | 1 |
| Medium (500K words) | 20-30 | 5-10 | 2-3 |
| Long (2M+ words) | 50+ | 20+ | 5-10 |

**Principle**: No more than 5 simultaneous foreshadowing lines

## Taboos

- Plant but don't recover (reader expectations disappointed)
- Force to wrap up (obviously last-minute patch)
- Foreshadowing too obvious (obvious at a glance)
- Too many foreshadowing (readers can't remember)

</instructions>

<examples>

<example>
<input>Design protagonist identity foreshadowing (core layer)</input>
<output>
**Chapter 1 plant**: Protagonist's father mysteriously disappears
**Chapter 50 clue**: Find letter father left, mentions Northern Region
**Chapter 100 clue**: Find father's traces in Northern Region
**Chapter 200 recovery**: Father appears, actually sealed a demonic god!

**Recovery method**: Layer-by-layer reveal
**Planting techniques**: Dialogue plant (mother's dying words) + Detail plant (jade pendant father left)

**Vietnamese Pattern (BNsr - "Biên niên sử rồng")**:
- Core identity reveals often wrapped in "duyên" (fate) narrative
- Dragon-related mythology creates deep foreshadowing (rồng cái, rồng đực)
- Use "tự do" (freedom) motif for protagonist arc foreshadowing
- Core reveals wrapped in "phước duyên" (blessed fate) or "mệnh lệnh" (destined mandate)
- Use "Pandora" as plot device for mystery delivery

**Pronoun pattern for dramatic reveals**:
- Normal speech: "mày/tao" between close characters
- Dramatic reveals: Shift to "ta/ngài" for formal weight
- Angry reveals: "thằng khốn", "con nhóc" - indicates enemy/antagonist
</output>
</example>

<example>
<input>Foreshadowing urgency analysis</input>
<output>
**Current chapter**: 80
**Foreshadow F-001**: Mysterious jade pendant (core, target=50)
  Urgency = (80/50) x 3.0 = 4.8
  Status: Critical (exceeded target!)

**Foreshadow F-002**: Junior sister's identity (sub-line, target=100)
  Urgency = (80/100) x 2.0 = 1.6
  Status: Warning (>80%)

**Foreshadow F-003**: Broken temple detail (decorative, target=120)
  Urgency = (80/120) x 1.0 = 0.67
  Status: Normal

**Pattern note**: In Xuanhuan (VN fantasy), core layer often involves "phước duyên" (blessed fate) or "mệnh lệnh" (destined mandate)

**Sentence structure for tension building**:
- Critical status: Use short, punchy sentences (1-2 words)
  - "Bảy ngày…" (BNsr Chương 1 cliffhanger)
  - "Là nó. Thanatos."
- Warning status: Mix short and medium sentences, increase pacing
- Normal status: Can use longer descriptive passages
</output>
</example>

<example>
<input>Hidden clue design</input>
<output>
**Chapter 10**: Protagonist encounters beggar old man, gives him a pill
**Chapter 30**: Protagonist encounters this old man again, old man smiles without speaking
**Chapter 50**: At critical moment, old man rescues
**Chapter 100**: Old man identity revealed—ancient great one!

**Technique**: Each appearance leaves suspense but doesn't explain

**Vietnamese Isekai Pattern (UH - "Useless hero from another world")**:
- Status card system hints: early "Giám định" (Appraisal) reveals hidden potential
- Underdog-to-stronger foreshadowing: "Kẻ Vô Dụng" (Useless One) archetype
- Training/combat pacing foreshadowing via "cấp" (level) and "mana" descriptions
- Harem hints: multiple female characters showing early interest/protection
- Status card format:

```
[Tên nhân vật]
(Tình trạng: ...)
-Chủng loài:
-Tuổi:
-Chức nghiệp:
-Cấp:
Mana: X/Y
-Kĩ năng:
+[Tên] (Cấp X) (Độc nhất nếu có)
```

**Harem foreshadowing triggers**:
- Multiple female characters show early interest in weak protagonist
- "Honoka: quan tâm Tanaka"
- "Kagura: bảo vệ khi bị bắt nạt"
- "Yuki: lạnh lùng nhưng can thiệp khi cần"
- Jealousy and comparison between female characters
</output>
</example>

<example>
<input>Romance foreshadowing (VN wordsmith style)</input>
<output>
**Layer**: Sub-line (30-100 chapters)

**Plant examples**:
- "Nụ cười làm tuyết tan" (smile that melts snow) - emotional connection foreshadow
- "Cái lưỡi câu" (fishing hook) metaphor - love that hooks heart
- "Sợi dây câu" (fishing line) - connection that cannot be escaped
- Character notices small habit early, becomes important later

**Technique**: Show-Don't-Tell
- Instead of "she will love him", show her protecting him when others mock
- Build through body language: "nghiến răng", "nước mắt", "cười méo"

**Vietnamese emotional triggers**:
| Emotion | Physical Expression |
|---------|---------------------|
| Giận (anger) | nghiến răng, nổ gân, mắt nổ đom đóm |
| Sợ (fear) | run bần bật, mặt tái mét, đứng không vững |
| Buồn (sad) | nước mắt lã chã, cười méo, thở dài |
| Bất ngờ (surprise) | tròn mắt, há hốc mồm, giật mình |
| Tức giận cực độ | hét lên, khặc ặc, cười điên cuồng |
| Xúc động | nghẹn bứ, run lên, khóc nức nở |

**Cliffhanger patterns from BNsr**:
- "...", "—0o0—" separator, cliffhanger endings
- "Bảy ngày…C" - sentence left incomplete
- "Là nó. Thanatos." - twist reveal
- Action left dangling: "Nhưng khi Tanaka ngồi dậy..."

**Romance building through speech register shifts**:
- Friends use "mày/tao" with each other
- When romantic tension rises, speech becomes more formal ("tôi/ngài")
- During confession: shift to literary register
</output>
</example>

<example>
<input>Dragon mythology foreshadowing (Xuanhuan)</input>
<output>
**Layer**: Core (50-300 chapters)

**Plant techniques using VN dragon mythology**:
- Early mentions of "rồng cái" (female dragon) and "rồng đực" (male dragon)
- Dragon-related artifacts appear mundane but later prove significant
- "Erever" - place name with dragon significance, appears in descriptive passages
- Dragon as symbol of power and pride ("sức mạnh và lòng kiêu hãnh")

**Example structure**:
- Chapter 1-10: Subtle dragon references in world-building
  - "Loài rồng từng là biểu tượng thiêng liêng của sức mạnh và lòng kiêu hãnh"
- Chapter 30-50: Character encounters dragon-related artifact
- Chapter 100-200: Dragon mythology deepens, reveals "rồng cái" connection
- Chapter 200+: Major dragon revelation, core identity tied to dragon lineage

**Metaphor patterns**:
- "lửa đỏ" + rồng = power, danger
- "tuyết tan" = warm emotion, love breaking coldness
- "bóng ma" = loss, haunting
- "cái lưỡi câu" = painful love
</output>
</example>

</examples>

<errors>
Plant but don't recover (readers angry) = Establish foreshadowing list, regularly recover
Force to wrap up (far-fetched) = The earlier you plant, the more reasonable the recovery must be
Foreshadowing too obvious = Should be implicit, not too direct
10+ simultaneous foreshadowing = No more than 5 simultaneous
Core foreshadowing >50 chapters unrecovered = Check urgency, recover in time
</errors>
