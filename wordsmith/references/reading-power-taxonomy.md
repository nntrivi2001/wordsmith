# Reading Power Taxonomy

> **Purpose**: This document defines unified classification standards for "reader retention power" (reader retention), shared by Step 1.5 / Context Agent / Checkers.
>
> **Principle**: All classifications serve as "guideline suggestions"; they are not used as mandatory scoring rulings.
>
> **Vietnamese Pattern Reference**: For genre-specific patterns (isekai/xuanhuan power systems, harem triggers, underdog-to-stronger patterns), see `STYLE_GUIDE_VN.md` Section 8.

---

## 1. Hook Types

### 1.1 Existing Types (Compatible Mapping)

| Old Type | New Taxonomy | Description |
|--------|-------------|------|
| Crisis type | Crisis Hook | Enemy appears / danger approaches |
| Mystery type | Mystery Hook | Information gap / unsolved mystery |
| Benefit type | Desire Hook | Good thing about to happen / reward in sight |

### 1.2 Extended Types

#### 1.2.1 Emotion Hook

**Definition**: Drives reading by triggering strong emotional responses in readers (anger / empathy / injustice / shame / heart-fluttering / attraction).

**Trigger scenarios**:
- Protagonist suffers an unjust accusation
- Betrayed by someone they trusted
- The weak are bullied
- Relationship breakthrough / heart-fluttering moment

**Genre adaptation**:
| Genre | Preferred Emotion | Intensity Recommendation |
|------|---------|------|
| Romance | Empathy / heart-fluttering / shame | strong |
| Power fantasy | Anger / injustice | medium→strong |
| Mystery | Empathy / fear | medium |

**Transition chapter downgrade**: Light emotions (e.g., faint worry / anticipation) can replace strong emotions.

**Soft prompt questions**:
- What emotion will readers feel at the end of this chapter?
- Is that emotion strong enough to make them want to know "what happens next"?

**Common misuse**:
- ❌ Emotion without setup (demanding reader empathy without buildup)
- ❌ Emotion mismatched with character behavior
- ❌ Overly melodramatic causing fatigue

**Examples**:
- Power fantasy: "Xiao Yan stared at Elder Yao lying in a pool of blood, fists clenched — he vowed to settle this score."
- Romance: "She finally understood; that man who never explained anything had been protecting her in his own way all along."
- Mystery: "The figure in the surveillance footage was clearly someone who had died three days earlier."

---

#### 1.2.2 Choice Hook

**Definition**: Drives reading by presenting a dilemma / high-stakes decision; readers want to know how the character will choose.

**Trigger scenarios**:
- Life-or-death either/or
- Interest vs. morality conflict
- Decision caused by misunderstanding
- Decision under time pressure

**Genre adaptation**:
| Genre | Preferred Choice Type | Intensity Recommendation |
|------|-------------|---------|
| Mystery | Truth vs. safety | strong |
| Romance | Emotion vs. reality | medium→strong |
| Power fantasy | Risk vs. stability | medium |

**Transition chapter downgrade**: Small choices (e.g., where to go / whom to see / whom to trust) can replace life-or-death decisions.

**Soft prompt questions**:
- What choice does the character face?
- What are the stakes for each option?
- Which side will readers root for?

**Common misuse**:
- ❌ Choice has no stakes (fake dilemma)
- ❌ Correct answer is too obvious
- ❌ Choice mismatched with character personality

**Examples**:
- Mystery: "Behind the door comes his daughter's crying, but the rules are clear: do not open it."
- Romance: "The plane tickets are booked, the luggage is packed — she only needs to decide whether to look back at him one last time."
- Power fantasy: "Taking this pill gives a thirty percent chance of breakthrough and a seventy percent chance of going feral."

---

#### 1.2.3 Desire Hook

**Definition**: Drives reading by showing an anticipated reward / achievement / progress; readers want to see the wish fulfilled.

**Trigger scenarios**:
- Breakthrough imminent
- Treasure about to be obtained
- Revenge timing is ripe
- Relationship about to progress
- Truth about to be revealed

**Subtypes**:
| Subtype | Description | Example |
|--------|------|------|
| Growth desire | Want to see protagonist get stronger | "Three more days and I'll break through" |
| Relationship desire | Want to see the CP deliver sweetness | "She agreed to that promise" |
| Revenge desire | Want to see the villain suffer | "Young Master Wang doesn't know; his doom is near" |
| Truth desire | Want to know the answer | "The answer may lie in this jade pendant" |
| Gain desire | Want to see good things obtained | "This fire lotus is enough to transform him" |

**Genre adaptation**:
| Genre | Preferred Desire Type | Intensity Recommendation |
|------|-------------|------|
| Power fantasy | Growth / revenge / gain | strong |
| Romance | Relationship / truth | medium→strong |
| Mystery | Truth | strong |

**Transition chapter downgrade**: Small anticipation (e.g., about to see someone / about to arrive somewhere) can replace big anticipation.

**Soft prompt questions**:
- What are readers anticipating?
- When will this expectation be fulfilled?
- Does this chapter give hope for fulfillment?

**Common misuse**:
- ❌ Expectation never fulfilled (crying wolf effect)
- ❌ Expectation too easy to fulfill (no tension)
- ❌ Expectation not resonant with readers

**Examples**:
- Power fantasy: "Tomorrow at the sect tournament, everyone who mocked him will witness his rise."
- Romance: "He said, when this is over, he has something to tell her."
- Mystery: "The truth of the fire ten years ago is hidden in this archive."

---

### 1.3 Hook Intensity Grading

| Intensity | Suitable Scene | Characteristics |
|------|---------|------|
| **strong** | Volume end / key turning point / before major conflict | Reader must know what happens next immediately |
| **medium** | Normal plot chapters | Reader wants to know, but can wait |
| **weak** | Transition / setup chapters | Just maintain reading momentum |

### 1.4 Within-Chapter vs. Chapter-End

| Position | Common Hooks | Function |
|------|---------|------|
| **Within chapter** | Mystery hook, emotion hook | Maintain immersion within the chapter |
| **Chapter end** | Crisis hook, choice hook, desire hook | Drive reader to the next chapter |

---

## 2. Cool-Point Patterns

### 2.1 Existing 6 Patterns (Retained)

| Pattern | Tag | Typical Trigger |
|------|------|---------|
| Flex & Counter | Flex & Counter | Mockery → reversal → shock |
| Underdog Reveal | Underdog Reveal | Show weakness → reveal truth → crush |
| Overlevel Counter-Kill | Underdog Victory | Gap → strategy → reversal |
| Authority Challenge | Authority Challenge | Authority → challenge → success |
| Villain Blowback | Villain Downfall | Villain smug → plan fails → humiliation |
| Sweet Exceeded Expectation | Sweet Surprise | Expectation → exceed → escalation |

### 2.2 Extended Patterns

#### 2.2.1 Misunderstanding Elevation

**Definition**: The protagonist does something ordinary / casual; side characters brainwash themselves into believing the protagonist is unfathomable / a hidden master.

**Core structure**:
1. Protagonist's casual action (unintentional)
2. Side characters' information gap (don't know protagonist's real situation)
3. Side characters elevate and rationalize (brainwash themselves)
4. Reader's superiority (I know the truth)

**Genre adaptation**:
| Genre | Suitability | Notes |
|------|--------|---------|
| Power fantasy / System | High | Avoid being too contrived |
| Slice-of-life / Light | High | Can serve as comedy element |
| Serious / Mystery | Low | Can break the atmosphere easily |

**Alternative suggestions**:
- If misunderstanding elevation is overused → switch to "real strength display"
- If side characters are too dumb → add reasonable information support for the brainwashing

**Examples**:
- "Xiao Yan just said 'not bad' casually; the elder shuddered — such a genius, yet so humble!"
- "He only stayed in the ruined temple because he was broke; everyone else thought he was in secluded meditation."

---

#### 2.2.2 Identity Reveal

**Definition**: A hidden identity is revealed at a critical moment, creating enormous contrast and shock.

**Core structure**:
1. Identity disguise (long-term buildup)
2. Critical moment (crisis / highlight)
3. Identity reveal (unexpected or voluntary)
4. Crowd reactions (shock / regret / reverence)

**Genre adaptation**:
| Genre | Suitability | Common Identity Contrast |
|------|---------|-------------|
| CEO / Romance | High | Poor relative → real princess |
| Power fantasy / Xianxia | High | underdog → hidden master |
| Mystery | Medium | Bystander → key person |

**Alternative suggestions**:
- If identity reveals are overused → switch to "ability display" or "background reveal"
- If there's no buildup → add identity hints first

**Examples**:
- "When that jade pendant rolled from her chest, everyone's expression changed — that was a royal seal."
- "The underdog Xiao Yan you speak of is the reincarnation of me, Dou Di Strongman Xiao Yan."

---

### 2.3 Structure Reference (30/40/30 Soft Version)

> **Note**: The following structure is for reference only and is not a mandatory requirement.

| Phase | Ratio Recommendation | Function |
|------|---------|------|
| Setup | ~30% | Establish information gap, pressure, anticipation |
| Delivery | ~40% | Core cool-point execution |
| Aftermath | ~30% | Reactions, gains, new anticipation |

**Soft prompt questions**:
- Is there sufficient setup / pressure before the cool-point?
- Is there sufficient development at the delivery moment?
- Are there reactions and aftermath after the cool-point?

---

## 3. Micro-Payoffs

### 3.1 Definition

**Micro-payoff**: Small gains given within a chapter that make readers feel "this chapter wasn't a waste."

> Unlike big cool-points, micro-payoffs are lighter and more frequent, used to maintain immersion within a chapter.

### 3.2 Micro-Payoff Types

| Type | Description | Example |
|------|------|------|
| **Information payoff** | Reveals new information / clues | "So the true purpose of that key was actually..." |
| **Relationship payoff** | Relationship progresses / confirms | "She reached for his hand for the first time" |
| **Ability payoff** | Ability improves / new skill | "He finally mastered the essence of this technique" |
| **Resource payoff** | Gains items / resources | "There was actually another Gathering Qi Pill hidden in the storage bag" |
| **Recognition payoff** | Gains recognition / face | "The way everyone looked at him had changed" |
| **Emotion payoff** | Emotional release / resonance | "He finally said what had been buried in his heart" |
| **Clue payoff** | Foreshadowing payoff / progress | "The incident from three years ago finally had a clue" |

### 3.3 Genre Preferences

| Genre | Preferred Micro-Payoffs | Recommended Per Chapter |
|------|-----------|-------------|
| Power fantasy | Ability / resource / recognition | 2–3 |
| Romance | Relationship / emotion / recognition | 1–2 |
| Mystery | Information / clues | 1–2 |
| Slice-of-life | Relationship / emotion | 1 |

### 3.3.1 Additional Genre Supplements

| Genre | Key Reader Retention Trigger | Hook Preference | Micro-Payoff Focus |
|------|-------------|---------|-----------|
| Esports | Competition outcomes and in-game decisions | Crisis hook / choice hook | Recognition payoff / information payoff |
| Livestream | Real-time feedback and public opinion reversal | Crisis hook / emotion hook | Resource payoff / recognition payoff |
| Cosmic Horror | Rule truth and escalating costs | Mystery hook / crisis hook | Clue payoff / emotion payoff |

**Execution tips**:
- Esports: Recommend one verifiable decision point per chapter (BP / tactics / execution) with consequences.
- Livestream: Prioritize forming a "feedback → reaction → data change" closed loop.
- Cosmic Horror: Prioritize redeeming rule clues; avoid pushing forward with shock adjectives alone.

### 3.4 Transition Chapter Micro-Payoffs

Transition chapters can relax requirements, prioritizing at least 1 micro-payoff:

| Transition Chapter Allows | Transition Chapter Not Recommended |
|-----------|-------------|
| Information payoff (new clue) | Big cool-points |
| Relationship payoff (small interaction) | Strong conflict |
| Emotion payoff (light emotion) | High-density rhythm |

**Soft prompt questions**:
- What will readers gain after reading this chapter?
- Is there a feeling of "this chapter had progress"?

---

## 4. Constraint Layering Standards

### 4.1 Hard Invariants

> **Violation = MUST_FIX; cannot be appealed or skipped**

| ID | Constraint Name | Definition | Trigger Condition |
|----|---------|------|---------|
| HARD-001 | Readability baseline | Key information missing causes incomprehension | Reader cannot understand "what happened / who did what / why" |
| HARD-002 | Promise violation | Previous chapter's hook is completely unfulfilled | A clear chapter-end promise has zero response in the next chapter |
| HARD-003 | Rhythm disaster | Consecutive N chapters with zero progression | No new information / no relationship change / no ability change / no situation change (N is determined by genre profile) |
| HARD-004 | Conflict vacuum | Entire chapter has no question / goal / stakes | Reader cannot answer "what is this chapter trying to solve" |

### 4.2 Soft Guidance

> **Violation = Can be appealed, but must record Override Contract and bear debt**

Including but not limited to:
- Chapter-end hook intensity insufficient
- Micro-payoff missing
- Emotion curve is flat
- Pattern repetition causing fatigue
- Paragraphs too long affecting readability

### 4.3 rationale_type Enumeration

When violating Soft Guidance, one of the following reasons must be selected:

| Type | Description | Debt Impact |
|------|------|------|
| `TRANSITIONAL_SETUP` | Setup / transition needed | Standard |
| `LOGIC_INTEGRITY` | Plot logic / mystery fairness prioritized | Reduced |
| `CHARACTER_CREDIBILITY` | Character credibility / growth rhythm prioritized | Reduced |
| `WORLD_RULE_CONSTRAINT` | Setting / rule constraints prevent fulfillment | Reduced |
| `ARC_TIMING` | Long-term big payoff rhythm arrangement | Standard (must specify window) |
| `GENRE_CONVENTION` | Genre convention | Standard (must cite profile) |
| `EDITORIAL_INTENT` | Author's subjective intent | Increased (quota is stricter) |

---

## 5. Compatibility Notes

### 5.1 Integration with Existing Checkers

| Existing Checker | Used Taxonomy |
|--------------|----------------|
| `reader-pull-checker` | Hook type, hook intensity, HARD-002 |
| `high-point-checker` | Cool-point patterns, micro-payoffs |
| `pacing-checker` | HARD-003 (rhythm disaster) |
| `continuity-checker` | HARD-001 (readability baseline) |

### 5.2 Output Field Mapping

| New Field | Corresponding Existing Field | Description |
|--------|-------------|------|
| `hook_type` | Compatible extension | New emotion hook / choice hook / desire hook |
| `hook_strength` | Unchanged | strong / medium / weak |
| `coolpoint_pattern` | Compatible extension | New misunderstanding elevation / identity reveal |
| `micro_payoffs` | New | Micro-payoff list |
| `hard_violations` | New | Hard constraint violation list |
| `soft_suggestions` | New | Soft guidance suggestion list |