---
name: style-adapter
purpose: Step 2B dedicated prompt, rewriting rough draft into web novel style
---

**Chinese Priority Principle**: This step's rewrite instructions, rewrite log, and change summary all use Simplified Chinese. English is only retained on CLI flags, checker id, JSON key names, and other unchangeable machine identifiers.

**Boundary with Step 4 (polish-guide)**:
- **Step 2B (this step)**: Pure style conversion — sentence rewriting, abstract to concrete, web novel taste
- **Step 4**: Problem fixing — based on review report fixing critical/high issues + AI trace detection

> Note: Step 4 will not repeat Step 2B's sentence conversion; the two steps each have their focus.

## Input
- Rough draft body (Step 2A output)
- Chapter type (battle/dialogue/transition/breakthrough)
- Hook requirements (type + intensity)

## Output
- Web novel body (word count ±10%)
- Rewrite log (record major adjustments)

Default word count target:
- Regular chapters default 2000-2500 words (unless outline or user specifies otherwise).

## Prohibited Changes (red lines)
- Plot direction
- Event sequence
- Character behavior results
- Settings/ability descriptions
- Foreshadowing content

## Hard Constraints (must)
- Long sentences (>40 characters) split, avoid consecutive long sentences pressing read
- Abstract judgment converted to action/reaction/cost
- Delete "summary narration" and large blocks of pure explanation
- Chapter has at least 1 clear advancing point (information/action/relationship/situation one)

## Soft Suggestions (prioritize execution)
- Opening enters conflict/risk/strong emotion early (suggest first 200-400 characters)
- Later paragraph or chapter end sets unclosed issue/next chapter motivation (no fixed character count window)
- Micro-delivery arrangement 1-3 times per chapter type, avoid mechanical equidistant spacing
- Each chapter priority appears 1 "quantifiable change" (status/resource/relationship/risk any one)
- Hook type priority "choice hook/crisis hook," but allow genre switching
- Dialogue maintains "intention conflict," reduce ineffective small talk

## Genre-Specific Style Weighting (new)
- **Fantasy/Cultivation/High Martial Arts**: Higher proportion of action and results, term explanation postponed.
- **Urban/Livestream/Esports**: Faster information rhythm, strengthen "feedback-reaction-counter" three-sequence.
- **Romance/Body Double/Soap**: Emotional arc front-loaded, key scenes must have relationship displacement.
- **Mystery/Rules/Cthulhu**: Clue delivery must be recoverable, fear comes from rules not word stacking.

## AI Trace Quick Replacement (new)
- Change "he is very angry" to "action+physiological+decision" three-sequence expression.
- Change "in summary" to direct conclusion action, do not do meta-narration.
- When 3 consecutive same-structure sentences, change at least one to short sentence burst point.

## Vietnamese Anti-AI Patterns

### Pronoun System (Đại từ xưng hô)
| Tình huống | Dùng | Tránh |
|------------|------|-------|
| Bạn bè thân | mày, tao | hắn, nó (khi đang nói chuyện) |
| Khi giận dữ | thằng khốn, con nhóc | hắn ta (quá bình thản) |
| Quý tộc/cổ đại | ta, ngài | mày, tao |
| Lạnh lùng/khinh bỉ | nó, thằng đó | tên đó (quá bình thường) |

### Sentence Variety (Đa dạng câu)
- **Action nhanh**: Câu đơn ngắn "Jack xông ra!", "Một con Goblin rơi xuống."
- **Mô tả nội tâm**: Câu ghép dài với nhiều mệnh đề
- **Hội thoại căng thẳng**: Câu ngắn cắt ngang, có dấu chấm than

### Colloquial vs Literary (Đời thường vs Văn chương)
| Đời thường | Văn chương |
|------------|------------|
| làm gì | làm chi |
| đâu | ở đâu |
| vậy | như vậy / thế |

### Emotion Expression (Biểu hiện cảm xúc)
| Cảm xúc | Thay vì nói... | Hãy viết... |
|---------|----------------|-------------|
| Giận | Hắn rất giận | Nghiến răng, nắm tay trắng bóc, mắt nổ đom đóm |
| Sợ | Hắn sợ hãi | Run bần bật, mặt tái mét, đứng không vững |
| Buồn | Hắn buồn lắm | Nước mắt lã chã, cười méo, thở dài |
| Bất ngờ | Hắn rất ngạc nhiên | Tròn mắt, há hốc mồm, giật mình |

### Slang & Intensity (Tiếng lóng)
- Khi căng thẳng cao độ: kết hợp nhiều từ tục "Thằng chó! Chết mẹ mày đi!"
- Inner monologue dùng ngôn ngữ bình thường, ít tục tĩu hơn lời nói

## Checkpoints (post-rewrite verification)
| Check Item | Standard | Failed Processing |
|-----------|----------|-------------------|
| Opening conflict | Suggest entering conflict/risk/strong emotion in first 200-400 characters | Add conflict introduction paragraph |
| Expectation anchor | Later paragraph or chapter end has unclosed issue/next chapter motivation | Add "unclosed issue" |
| Micro-delivery rhythm | Has 1-3 micro-deliveries, and not mechanical equidistant | Merge or reposition delivery points |
| Long sentence ratio | Sentences >40 characters <10% | Split long sentences |
| Explanation paragraphs | No consecutive >200 character pure explanation | Break up or delete |

## Chapter Type Adaptation (by outline, not by word count)
- **Regular advancing chapter (default 2000-2500 words)**: Execute all hard constraints + soft suggestions prioritized
- **Transition chapter (determined by outline)**:
  - Conflict introduction can relax to first 400 characters
  - Micro-delivery can reduce to 0-1 times, but still needs 1 clear advancing point
  - Expectation anchor intensity can be weak
  - Transition chapter identity determined by chapter outline/volume outline, prohibited from using word count threshold determination

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
