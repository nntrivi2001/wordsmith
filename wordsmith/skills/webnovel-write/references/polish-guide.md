# Plot Polish Guide

---
name: polish-guide
purpose: Loaded at polishing stage after chapter generation, based on review report fixing issues + strengthening web novel taste
---

<context>
This file is for Step 4 polishing stage, goal is "fix problems" not "rewrite plot."

Input comes from two parts:
1. Chapter body (Step 2A/2B output)
2. Review report (Step 3 aggregated results)

Boundary with Step 2B:
- Step 2B: Style translation (expression layer)
- Step 4: Problem fixing (quality layer), including review problem fixing, Anti-AI final check, poison point avoidance

If Step 2B has been executed, this step does not repeat full-quantity sentence rewriting, only does "necessary modifications."
</context>

<instructions>

## 1. Input Contract

```json
{
  "chapter_file": "body/Chapter-0123-chapter-title.md",
  "overall_score": 82,
  "issues": [
    {"agent": "consistency-checker", "type": "POWER_CONFLICT", "severity": "critical", "location": "Paragraph 6", "suggestion": "Realm override"},
    {"agent": "ooc-checker", "type": "OOC", "severity": "high", "location": "Paragraph 9", "suggestion": "Character tone deviation"}
  ],
  "pass": true
}
```

`chapter_file` must be the actual file path of current chapter; if project has not migrated to titled filename, can also pass `body/Chapter-0123.md`.

## 2. Execution Order (must follow)

1. Fix problems in review report (first `critical/high`)
2. Validate web novel Hard/Soft/Style rules
3. Execute Phase 1 Anti-AI final check and rewrite
4. Execute No-Poison poison point avoidance check
5. Output polishing result and deviation (if any)

## 2A. Anti-AI Detection Rules (corresponding to execution order step 3)

> Word frequency statistics **only as reminder**, no longer as hard threshold.
> Note: Even if word frequency only as reminder, if final text still has obvious AI template traces, `anti_ai_force_check` should still be judged as `fail`.
> This section is execution summary; complete 7-layer rules and high-frequency word bank see "Phase 1 supplement" chapter below, the two sections execute together.

### Common AI Traces

| Feature | Performance |
|---------|-------------|
| Regular sentence structure | Similar sentence lengths, similar structures |
| Patterned vocabulary | First, second, finally, it is worth noting that |
| Overuse of connectors | Heavy use of however, therefore, moreover |
| Flat emotion | Lack of personalized emotional expression |
| Information dense | Every sentence has information, lack of white space |
| English template residue | Direct translation patterns from English |

### Vietnamese-Specific Anti-AI Patterns

| Vietnamese Pattern | English Equivalent (avoid) | Vietnamese Alternative |
|-------------------|---------------------------|----------------------|
| "nói chung" / "tóm lại" / "nhìn chung" | in summary / overall | Remove or use direct action |
| "thứ nhất" / "thứ hai" / "cuối cùng" | firstly / secondly / finally | Vary sentence structure |
| "vì vậy" / "do đó" / "nên" | therefore / thus / hence | Use action sequence instead |
| "hắn rất giận" / "hắn rất buồn" | he is very angry / sad | Action + physiological + decision |
| "hắn nghĩ rằng" | he thinks that | Direct internal monologue |
| "điều đầu tiên" / "điều tiếp theo" | the first thing / next | Natural paragraph flow |
| Summary narration | "In summary..." pattern | Direct conclusion with action |
| Dense explanation | Over-logical dialogue | Intentional confrontational dialogue |

### High-Frequency Word Reminder List

| Type | Keywords |
|------|----------|
| Summary words | in summary / overall / therefore / to sum up |
| Enumeration structure | firstly / secondly / finally / first / second / third |
| Academic tone | in terms of / to some extent / essentially |
| Causal conjunctions | because / therefore / due to / thus |

### Con Duong Ba Chu Combat Rhythm Patterns
For combat scenes, alternate between:
1. **Fragmented bursts**: "Ầm...!" / "Bắn!" / Short punchy sentences
2. **Elaborate descriptions**: Longer passages with sensory detail

Example pattern:
```
Ầm...!
Hắn ta ngã xuống. Máu meos ra.
Nhưng hắn cười.
"Chỉ có vậy sao?"
Cậu — kẻ đứng xem — run bần bật.
"Keng! Enemy HP: 0"
```

---

## Naturalization Degree Standard (suggestion)

| Indicator | Not passing | Passing |
|---------|-------------|---------|
| Pause words | < 0.5 times/500 words | 1-2 times/500 words |
| Uncertain expression | 0 times | >= 2 times/chapter |
| Short sentence ratio | < 20% | 30-50% |
| Colloquial words | 0 times/1000 words | >= 2 times/1000 words |

> **Tip**: Naturalization is not the more the better, excess will seem deliberate.

### Mandatory Execution Protocol (new)

- Must completely execute this section's "7-layer rules + high-frequency word bank + final check list," prohibition from cutting to "suggestion items."
- Must check paragraph by paragraph across full text, prohibit sampling check.
- Step 4 completion must output `anti_ai_force_check: pass/fail`.
- If result is `fail`, must continue staying in Step 4 rewrite, cannot enter Step 5.
- If high-risk expression hit but necessary for plot to preserve, must write into `deviation` (location + reason + cost).

### Full Text Check Scope (required)

- Check all chapter paragraphs
- Check all dialogue rounds
- Chapter start/middle/end all must pass Anti-AI rules
- Any hit must be rewritten or recorded as deviation

---

## Phase 1 Supplement: Anti-AI Specification (7 layers, original version)

> Goal: Reduce template tone, explanatory tone, mechanical tone.
> Principle: Prioritize "readability and character authenticity," not mechanical replacement of every word.

### Layer 1: High-Risk Vocabulary (200+ word bank, first batch)

#### A. Summary Inductive Words (22)

in summary, overall, to sum up, it can be seen that, as can be seen, it is not hard to find, at the root of it all, at the end of the day, looking at the big picture, from this perspective, in other words, in brief, to summarize, one could say, from this we derive, the conclusion is, ultimately it can be known, generally speaking, taken together, as a whole, on the whole, in conclusion.

#### B. Enumeration Template Words (24)

firstly, secondly, once more, finally, first, second, third, for one, for two, for three, on one hand, on the other hand, furthermore, in addition, additionally, at the same time, next, then, subsequently, immediately after, the last step, the next step, the first point, the second point.

#### C. Written Academic Tone (24)

to some extent, essentially, in the sense of, on the dimension of, at the level of, lies in, manifests as, constitutes, forms, achieves, completes, carries out, unfolds, drives, promotes, provides, possesses, owns, attains, presents as, expresses as, reflects, contains, refracts.

#### D. Logical Connector Abuse Words (22)

therefore, thus, so, due to, however, but, yet, at the same time, similarly, correspondingly, accordingly, further, even further, thereby, and then, so, the result is, and so it was, hence, from this, by comparison, conversely.

#### E. Emotion Direct Statement Words (22)

extremely angry, extremely happy, extremely sad, mixed feelings in his heart, a hundred emotions at once, emotionally complex, deeply shaken inside, couldn't help but sigh, felt helpless, felt pained, felt relieved, felt afraid, deeply moved, emotions surging, heavy-hearted, emotionally complicated, heart warmed, heart sank, heart tightened, couldn't help but freeze, couldn't help but startle, inner shock.

#### F. Action Clichés (22)

furrowed brow, let out a sigh, took a deep breath, slowly opened his mouth, said in a heavy voice, said lightly, said coldly, said softly, corners of the mouth curved up, corners of the mouth twitched, eyes narrowed, eyes flashed, body stiffened, footsteps paused, whole body shook, heart skipped a beat, involuntarily stepped back half a step, spun around sharply, raised hand and waved, slowly nodded, gently shook his head, instinctively stepped back.

#### G. Environment Clichés (22)

the air seemed to freeze, the atmosphere suddenly tensed, the pressure dropped sharply, the night was ink-black, the moonlight was like water, the cold wind pierced to the bone, complete silence all around, dead silence, time seemed to stand still, space seemed to warp, the room was filled with, the only light source, teetering on the edge, oppressive enough to steal one's breath, silence like a tide, the air was full of, everything seemed, the world seemed, just at this moment, all of a sudden, in an instant, in the blink of an eye.

#### H. Narrative Fill Words (22)

in fact, in reality, in a sense, strictly speaking, objectively, subjectively, generally speaking, under normal circumstances, under these circumstances, at this moment, on this basis, in this sense, from a certain angle, for him, for her, this means, this shows, this represents, this is not surprising, not by chance, undeniably, without a doubt.

#### I. Abstract Empty Words (22)

destiny, growth, transformation, transcendence, value, meaning, choice, perseverance, belief, original intention, hope, despair, courage, justice, evil, authenticity, hypocrisy, complexity, profundity, grandeur, insignificance, weight.

#### J. Mechanical Opening/Closing Words (24)

the story must begin from, let us turn our eyes to, the camera shifts to, meanwhile on the other side, back to the present, returning to, all of this starts from, he didn't know, the gears of fate began to turn, a new chapter has begun, to be continued, the story has only just begun, the real test is yet to come, a storm is coming, a greater conspiracy is brewing, this is only the beginning, the answer has yet to be revealed, what the future holds, no one knows, he knew well, she understood, but what he didn't know was, but what she didn't know was, yet everything had only just begun.

### Layer 2: Sentence Rules (anti-template)

- Prohibition of "first/second/third" three-paragraph explanation writing.
- Prohibition of three consecutive "subject + predicate + object" same-structure sentences.
- Prohibition of "he thinks he needs to do three things: one, two, three" listified narration.
- Every 3-5 paragraphs should have at least one sentence length change (short sentence interruption/insert action/dialogue rhetorical question).

### Layer 3: Adjective and Adverb Restrictions

- Two or more consecutive adjectives modifying same noun, default rewrite.
- Per 300 words, "very/extremely/incredibly/especially/quite" total suggestion no more than 4.
- Prioritize "action + result + cost," weaken "abstract evaluation words."

### Layer 4: Four-Character Clichés/Idiom Limitation

- Prohibition of high-frequency empty cliched phrases densely stacked (e.g., "emotions surging, a hundred feelings at once, mixed emotions" consecutively).
- Per 500 words, four-character clichés suggestion no more than 3, cannot appear consecutively.
- If using idiom, must bear narrative function (advance information/conflict/character attitude).

### Layer 5: Dialogue De-AI

- Prohibition of "instruction manual style dialogue" (complete background explanation, overfull logic).
- Dialogue must have intention (probe/avoid/pressure/induce/defend).
- Allow real oral pauses, interruptions, rhetorical questions, avoid everyone "standard written language."

### Layer 6: Paragraph Structure

- Single-sentence paragraphs suggestion 25%-45% (can increase in conflict chapters).
- Paragraph length suggestion 20-100 characters, avoid consecutive long explanatory paragraphs.
- Scene switch prioritize using action/sound/location change, not "Act 1/Act 2" labels.

### Layer 7: Punctuation Rhythm

- Prohibition of consecutive `......` or `!!!`.
- Ellipsis, exclamation marks max 1 per paragraph (except special emotional explosion points).
- When long sentence has more than 4 commas, prioritize splitting.

### Anti-AI Rewrite Algorithm (execution actions)

1. Abstract emotion sentence → `physiological reaction + immediate intention + next action`
2. Conclusion sentence → `factual detail + cost/risk + decision`
3. Consecutive explanatory sentences (>=3) → change to "dialogue/action/ rhetorical question" mixed arrangement
4. Consecutive same-structure sentences (>=3) → at least break 1 sentence as short sentence or insert action anchor
5. Dialogue entire paragraph explaining background → change to "intentional confrontational dialogue"

### Pass Threshold (manual judgment)

- Full text must not retain unprocessed three-paragraph enumeration template sentences.
- All high-risk expressions hit in full text have been rewritten or recorded as deviation.
- At least complete 3 "abstract sentence→behavior sentence" rewrites (full text scope statistics).
- Chapter end has perceivable next step pressure or unclosed issue.
- If high-risk expressions still retained, need deviation explaining retention reason.

### Phase 1 Final Check (original version retained)

- [ ] High-risk vocabulary has been checked across full text and necessary replacements made.
- [ ] Three-paragraph explanatory sentences (first/second/last) not appearing.
- [ ] Dialogue has real conflict intention, not information preaching.
- [ ] No-Poison poison point red line check see section 5 (this checklist only covers Anti-AI).
- [ ] After modification, "settings are physics / outline is law" not broken.

## 3. Review Problem Fix Priority

| Severity | Processing Rule |
|----------|-----------------|
| critical | Must fix; if cannot fix must record deviation and reason |
| high | Must prioritize processing; if cannot fix record deviation |
| medium | Process based on scope and benefit |
| low | Can process by preference |

Type corresponding fix actions:
- `OOC`: Restore character rhetoric, risk preference, decision boundaries
- `POWER_CONFLICT`: Ability regresses to legal realm, or add "acquisition path + cost"
- `TIMELINE_ISSUE`: Add time passage anchor
- `LOCATION_ERROR`: Add movement process and space anchor
- `PACING_IMBALANCE`: Add missing advancing events or delete redundant explanatory paragraphs
- `CONTINUITY_BREAK`: Add bridging sentences and transition actions

## 4. Web Novel Layered Rules

### Hard (must satisfy)

1. This chapter has at least 1 clear advancing point (information/action/relationship/situation at least one).
2. Key dialogue can determine intention (probe/pressure/avoid/induce at least one).
3. Abstract judgment sentences changed to "action/reaction/cost" expression.

### Soft (suggest satisfying)

1. Chapter start suggest entering conflict/risk/strong emotion in first 200-400 characters.
2. Chapter middle has rhythm pulse (reference 800-1400 characters one wave, short chapter at least once).
3. Later paragraph or chapter end retains unclosed issue or next step expectation anchor.

### Style (prioritize by chapter type)

1. Avoid consecutive long paragraphs of pure explanation, prioritize "information + action/reaction" alternating.
2. Allow calm ending, but cannot mechanically cut off.

## 5. No-Poison Poison Point Avoidance (5 types)

1. Intelligence-lowering advancement: Character ignores common sense only to serve plot.
2. Forced misunderstanding: Can be explained in one sentence but long-term delay.
3. Martyr-like without cost: Boundless forgiveness of high-risk objects.
4. Tool-person supporting characters: Only appear at functional nodes, no independent motivation.
5. Double-standard ruling: Same behavior has inconsistent evaluation standards without narrative explanation.

When hitting any poison point, must add at least two of "motivation/resistance/cost."

## 6. Polishing Red Lines (cannot breach)

- Do not change plot direction (outline is law)
- Do not change settings physics boundaries (settings are physics)
- Do not delete key foreshadowing
- Do not forcibly rewrite character relationship baseline

## 7. Output Format (after polishing complete)

Must output:
1. Polished chapter body
2. Fix summary (structure as follows)

```text
[Polishing Report]
- Critical issues fixed: N
- High priority fixed: N
- Medium/low priority fixed: N
- Anti-AI rewrite: N
- anti_ai_force_check: pass/fail
- Poison point risk: pass/fail
- Deviation records:
  - {location}: {reason}
```

If `critical` not cleared to zero, must explicitly mark "not passed," and return to Step 4 continue fixing.

</instructions>

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

<examples>

<example>
<input>AI style: First, he needs to get evidence; second, he needs to stabilize teammates; finally, he will publicly counterattack.</input>
<output>He first clutches evidence in hand, turns to find teammates. People need stabilizing before the counterattack can be decisive.</output>
</example>

<example>
<input>AI style: He is very angry, inner mixed emotions.</input>
<output>His knuckles go white, a breath crushed in his throat. One more second, and he'd act.</output>
</example>

</examples>

<errors>
❌ Skip critical/high directly do style micro-adjustment
✅ Clear problems first, then style

❌ Only replace high-risk words, don't change sentence group structure
✅ Rewrite sentence groups per "abstract→behavior" method

❌ Change plot facts for de-AI flavor
✅ Only change expression, not event results
</errors>

<checklist>
- [ ] `critical` fixed or recorded deviation
- [ ] `high` fixed or recorded deviation
- [ ] Hard rules all passed
- [ ] Phase 1 Anti-AI full text check passed
- [ ] `anti_ai_force_check=pass`
- [ ] No-Poison five poison types checked
- [ ] Polishing red lines not touched
</checklist>
