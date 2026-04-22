---
name: workflow-resume
purpose: Loaded when resuming tasks, guiding interruption recovery process
---

<context>
This file is for interrupted task recovery. Claude already knows error handling flow; this only supplements web novel creation workflow-specific Step difficulty grading and recovery strategies.
</context>

<instructions>

## Step Interruption Difficulty Grading

| Step | Name | Impact | Difficulty | Default Strategy |
|------|------|--------|-------------|-------------------|
| Step 1 | Context Agent | No side effects (read-only) | 1 star | Directly re-execute |
| Step 1.5 | Chapter design | Structure not solidified | 1 star | Redesign |
| Step 2A | Generate rough draft | Half-finished chapter file | 2 stars | **Delete half-finished product**, restart from Step 1 |
| Step 2B | Style adaptation | Partially rewritten content | 2 stars | Continue adaptation or return to 2A |
| Step 3 | Review | Review incomplete | 3 stars | User decides: re-review or skip |
| Step 4 | Net-novel polishing | Partially polished file | 2 stars | Continue polishing or delete and rewrite |
| Step 5 | Data Agent | Entities not fully extracted | 2 stars | Re-run (idempotent) |
| Step 6 | Git backup | Not committed | 3 stars | Check staging area, decide commit/rollback |

## Recovery Flow

### Phase 1: Detect Interruption Status

```bash
python "${SCRIPTS_DIR}/webnovel.py" --project-root "$PROJECT_ROOT" workflow detect
```

### Phase 2: Ask User

**Must display**:
- Task command and parameters
- Interruption time and location
- Completed steps
- Recovery options and risk level

### Phase 3: Execute Recovery

**Option A (recommended)**: Delete half-finished product and restart
```bash
python "${SCRIPTS_DIR}/webnovel.py" --project-root "$PROJECT_ROOT" workflow cleanup --chapter {N} --confirm
python "${SCRIPTS_DIR}/webnovel.py" --project-root "$PROJECT_ROOT" workflow clear
/wordsmith-write {N}
```

**Option B**: Roll back to previous chapter
```bash
git reset --hard ch{N-1:04d}
python "${SCRIPTS_DIR}/webnovel.py" --project-root "$PROJECT_ROOT" workflow clear
```

## Why Delete Instead of Continue?

1. **Quality assurance**: Half-finished product may contain incomplete sentences, broken logic
2. **Context loss**: New session can't remember previous creative thinking
3. **Prevent hallucinations**: Continuing easily creates contradictions
4. **Cost controllable**: Regenerate less than Fix half-finished + review

## Vietnamese Recovery Context

When resuming, apply Vietnamese writing patterns from STYLE_GUIDE_VN.md:

### Step 2A - Content Generation Patterns

#### Sentence Structure
- **Action scenes**: Short, punchy sentences (3-8 words)
  - "Jack xông ra!" / "Ầm!" / "Chết tiệt!"
- **Emotional/ descriptive scenes**: Longer sentences with metaphors
  - "Loài rồng từng là biểu tượng thiêng liêng của sức mạnh và lòng kiêu hãnh."
- **Combat pacing**: Alternate short-long-short for tension

#### Pronoun & Formality
| Level | Pronouns | When to use |
|-------|----------|-------------|
| Casual | mày/tao | Friends, teammates, close characters |
| Formal | tôi/ngài | Strangers, authority, ceremonies |
| Archaic | ta | Noble characters, formal rituals |
| Contempt | thằng/kẻ | Enemies, insults |

**Key pattern**: Protagonists (Rosa, Jack) use "tao-mày" with each other but "tôi-ngài" with strangers

#### Cliffhanger Endings
- Incomplete sentences: "Bảy ngày…C"
- Twist reveals: "Là nó. Thanatos."
- Action dangling: "Nhưng khi Tanaka ngồi dậy..."
- Separators: "—0o0—"

### Step 2B - Style Adaptation

#### Colloquial vs Literary Register
| Colloquial | Literary | Context |
|------------|----------|---------|
| đi đường | đường đi | Order difference |
| làm gì | làm chi | Asking purpose |
| sao | như thế nào | Asking how |
| vậy | như vậy / thế | Way of saying |

**Pattern**: Dialogue = colloquial; Narration inner thoughts = literary

#### Emotional Expression (Show-Don't-Tell)
| Emotion | Physical Signs |
|---------|----------------|
| Giận (anger) | nghiến răng, nổ gân, mắt nổ đom đóm |
| Sợ (fear) | run bần bật, mặt tái mét, đứng không vững |
| Buồn (sad) | nước mắt lã chã, cười méo, thở dài |
| Bất ngờ (surprise) | tròn mắt, há hốc mồm, giật mình |
| Tức giận cực độ | hét lên, khặc ặc, cười điên cuồng |

### Step 3 - Review Checklist

#### Pronoun Consistency
- Check characters maintain consistent formality levels
- Verify pronoun shifts match emotional state (normal → angry = shift to thằng khốn/con nhóc)
- Protagonists: "tao-mày" between each other, "tôi-ngài" with others

#### Punctuation Review
- **Dấu gạch ngang (—)**: Inner thoughts, dialogue attribution, explanations
  - "—Cô ấy thật yếu đuối..."
  - "Anh ta — kẻ phản bội — đã chết."
- **Dấu ba chấm (...)**: Hesitation, cliffhanger, prolonged thought
- **Dấu chấm than (!)**: Shouting, impact, "JACKKKK!!!!"

#### Show-Don't-Tell Verification
- Replace "Cô ấy rất giận" with: "Rosa nghiến răng, nắm chặt tay lại đến trắng bóc. Mắt cô nổ đom đóm."

### Step 4 - Polishing Patterns

#### Pacing
- **Fast-paced (combat)**: Short sentences, strong verbs, sound effects
  - "Ầm!" / "Bắn!" / "Chết tiệt!"
- **Slow-paced (emotional/scenic)**: Long descriptive sentences
  - "Mùa xuân đến và Ardisia sẽ nở - loài hoa dại thân thảo mọc dày đặc..."

#### Scene Transitions
| Method | Usage |
|--------|-------|
| `***` | Major scene change, time shift |
| `—0o0—` | Minor scene within UH |
| "Sáu năm trước..." | Flashback |
| "Buổi sáng hôm đó..." | Day change |

#### Sound Effects (Vietnamese)
- Ầm! (impact)
- Bắn! (shooting)
- Choang! (clashing)
- Bốp! (slap/hit)
- "JACKKKK!!!!" (shouting)

### Genre-Specific (Isekai/Gaming)

#### Status Card Format
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

#### Combat Flow
1. See enemy → Giám định (check status)
2. Assess strength
3. Tactics
4. Action
5. Result + loot/exp

### Special Recovery Notes

| Scenario | Vietnamese Pattern Implication |
|----------|-------------------------------|
| Over 24 hours | Context lost; restart with fresh pacing patterns |
| Half-finished combat scene | Verify short sentences maintained throughout |
| Romance scene incomplete | Check speech register transitions (mày/tao → tôi/ngài for tension) |
| Status card scene | Ensure field labels match VN format (Cấp, Mana, Sức khỏe) |

## Special Scenarios

| Scenario | Strategy |
|----------|----------|
| Over 24 hours | Recommend rollback (context completely lost) |
| Over 1 hour | Recommend restart |
| Multiple half-finished products | Delete all, restart from stable state |
| workflow_state.json doesn't exist | Heuristic detection state.json vs files |

</instructions>

<examples>

<example>
<input>Step 2A interruption (most common)</input>
<output>
Detected interrupted task:

Task: /wordsmith-write 7
Interruption location: Step 2A - Chapter content generation in progress

Completed:
  Step 1: Context Agent collected context

Incomplete:
  Step 2A: Generate chapter content (written 1500 words)
  Step 3-6: Not started

Recovery options:
A) Delete half-finished product, restart from Step 1 (recommended) 1 star
B) Roll back to Ch6, give up all Ch7 progress

Please choose (A/B):
</output>
</example>

<example>
<input>Step 3 interruption (review)</input>
<output>
Recovery options:
A) Re-execute review
   - Call 6 reviewers
   - Generate review report
   - Continue Step 4 polishing

B) Skip review, directly polish (recommended)
   - Don't generate review report
   - Can use /wordsmith-review for supplementary review later

Please choose (A/B):
</output>
</example>

<example>
<input>Step 4 interruption (polishing)</input>
<output>
Recovery options:
A) Continue polishing (recommended) 1 star
   - Open and continue polishing actual chapter file (prioritize `MainText/Chapter0007-Chapter-Title.md`)
   - Save file
   - Continue Step 5 (Data Agent)

B) Delete polished draft, restart from Step 2A
   - Delete actual chapter file (prioritize `MainText/Chapter0007-Chapter-Title.md`)
   - Regenerate chapter content

Please choose (A/B):
</output>
</example>

</examples>

<errors>
Intelligently continue half-finished product = Delete and regenerate
Auto-decide recovery strategy = Must get user confirmation
Skip interruption detection = Run workflow_manager.py detect first
Fix state.json without verification = Check field-by-field consistency
</errors>
