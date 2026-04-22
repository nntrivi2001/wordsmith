# Typesetting and Reading Experience (Mobile-First)

> **Purpose**: Let readers "slide through" more smoothly (mobile screen), avoid causing abandonment due to paragraph/dialogue/punctuation issues.

> **Vietnamese wordsmith patterns** from BNsr and UH:
> - Em dash (—) for dialogue and inner thoughts: `"—Cô ấy đi rồi."`
> - Ellipsis (...) for emotional pause: `"Cô ấy nghĩ... về những ký ức..."`
> - Scene cuts: `***` for major transitions, `—0o0—` for minor shifts (UH style)
> - Short punchy sentences for action, longer descriptive for emotional scenes
> - Dialogue: colloquial register (mày/tao between intimate characters)

---

## 1. Paragraph Rules (Most Important)

- **One action/one information per paragraph**: Each paragraph only carries one function (advance/display/emotion/information).
- **Don't make paragraphs too long**: Paragraphs exceeding 5 consecutive lines, prioritize splitting into 2-3 paragraphs (especially explanatory paragraphs).
- **"Fast paragraphs" for climax**: During climax/battle/chase, use more short sentences + short paragraphs to increase reading speed and impact.
- **"Slow paragraphs" for setup**: Setup allows slightly longer, but ensure each paragraph has new information, not pure descriptive stacking.

---

## 2. Dialogue Typesetting (Default Standard)

- **One person, one line**: Switch lines when switching speakers; don't cram 3-4 rounds of dialogue into one paragraph.
- **Embed action in dialogue**: Use action/expression/environment insertion to help readers identify speakers and control pace.
- **Avoid "who's talking" confusion**: In multi-character scenes, add clear speaker or action anchor every 2-3 sentences.

**Example (recommended)**:
```markdown
"You sure you want to go in?" Li Xue lowered her voice.

Lin Tian looked at the cave entrance swirling with black fog, throat rolling: "If I don't go in, the answer will always be outside."

"Then don't die." She stuffed a jade talisman into his palm.
```

---

## 3. Punctuation and Readability

- **Minimize long strings of ellipses/exclamation marks**: `……！！！` combinations, avoid appearing repeatedly within one chapter.
- **Explanatory sentences shouldn't taste like "thesis"**: Avoid structured formulas like "first/second/overall/itisnotable that."
- **Unified proper noun writing**: Character names/faction names/realm names/skill names, use one version consistently (write into `settings/` and track in `state.json`).

---

## 4. Scene Switching and Chapter Structure

- **Cut transitions need breathing room**: Leave one blank line before and after scene switches; use `---` as separator when necessary.
- **Information density should be visible**: Key settings/key clues/key turning points, try to fall at paragraph beginning or end to reduce "scrolling half screen before seeing the point."
- **Late section suggest having expectation anchor**: Either question/threat/promise/reversal one is fine (avoid mechanical endings like "went back to sleep").

---

## 5. 10-Point Quick Check Before Publishing

1. Does dialogue "switch speakers switch lines"
2. Any paragraphs exceeding 5 lines (can they be split)
3. Any single paragraph mixing multiple character dialogues (can they be split)
4. Any large explanatory passages with "summary/enumeration tone"
5. Do proper nouns match `settings/`
6. Any "???/placeholder text" exposed to readers
7. Scene switching clear (blank lines/separators/transitional sentences)
8. At least 1 clear advancing point within chapter (information/action/turning point)
9. Chapter-end hook present
10. New entity first appearance clear (name/identity/memory point); if manual annotation needed (optional): use hidden XML tags (see `${CLAUDE_PLUGIN_ROOT}/skills/wordsmith-query/references/tag-specification.md`)

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