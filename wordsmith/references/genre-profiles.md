# Genre Configuration Profiles

> **Purpose**: This document defines reader-retention configuration parameters for each genre, read by Step 1.5 / Context Agent / Checkers.
>
> **Principle**: Configurations are for "adjusting weight and guidance"; they are not used for mandatory rulings.
>
> **Note**: Expanded with empirical data from xslca.cc popular rankings; added history-travel / game-lit; updated key parameters for shuangwen / xianxia / urban-power.
>
> **Vietnamese Pattern Reference**: For vocabulary nuances, colloquial vs literary register, and genre-specific patterns (isekai/xuanhuan), see `STYLE_GUIDE_VN.md`.

---

## Vietnamese Pronoun Conventions (Reference)

| Pronoun | Gender | Context | Example |
|---------|--------|---------|---------|
| **hắn** | Third male | Action / provoking opponent | *"Hắn ta dám..."* (BNsr Chương 4) |
| **tao** | Peer / friends | Strong personality, confident | *"Tao cá là mày chưa từng..."* (UH Chương 4) |
| **mày** | Peer / friends | Familiar address | *"Mày nghĩ tao sợ mày à!"* (UH Chương 1) |
| **tụi mày** | Group | Addressing multiple people | *"Tụi mày có thể sống..."* (BNsr Chương 5) |
| **bọn tao** | In-group | Protagonist's group | *"Bọn tao sẽ không để mày..."* (BNsr Chương 5) |
| **ta** | Archaic / ceremonial | Nobility, formal occasions | *"Ta là Vincent..."* (BNsr Chương 3) |
| **ngài** | Honorific | Addressing authority | *"Ngài có thể để tôi..."* (UH Chương 1) |
| **tôi** | Polite | Serious context, social | *"Tôi muốn gia nhập..."* (UH Chương 2) |

**Key Pattern**: Pronouns shift with emotion — normal speech uses "mày/mày", anger shifts to "thằng khốn", "con nhóc". Main characters (Rosa, Jack) use "tao-mày" with each other but "tôi-ngài" with strangers.

---

## 1. Profile Field Descriptions

### 1.1 Core Fields

| Field | Type | Description |
|------|------|------|
| `id` | string | Genre unique identifier (English lowercase) |
| `name` | string | Genre Chinese name |
| `description` | string | One-sentence description of core selling point |
| `tags` | string[] | Stackable genre tags (reserved for multi-tag extension) |

### 1.2 Hook Configuration

| Field | Type | Description |
|------|------|------|
| `preferred_types` | string[] | Preferred hook types (sorted by priority) |
| `strength_baseline` | string | Default hook intensity: strong/medium/weak |
| `chapter_end_required` | boolean | Chapter-end hook preference (true=strong preference, not per-chapter mandatory) |
| `transition_allowance` | number | Transition chapter exemption cap (how many consecutive chapters can be downgraded) |

### 1.3 Cool-Point Configuration

| Field | Type | Description |
|------|------|------|
| `preferred_patterns` | string[] | Preferred cool-point patterns (sorted by priority) |
| `density_per_chapter` | string | Per-chapter cool-point density: high(2+)/medium(1)/low(0-1) |
| `combo_interval` | number | Combo cool-point recommended interval (reference 1 per N chapters) |
| `milestone_interval` | number | Milestone cool-point recommended interval (reference 1 per N chapters) |

### 1.4 Micro-Payoff Configuration

| Field | Type | Description |
|------|------|------|
| `preferred_types` | string[] | Preferred micro-payoff types |
| `min_per_chapter` | number | Per-chapter recommended micro-payoff minimum |
| `transition_min` | number | Transition chapter recommended micro-payoff minimum |

### 1.5 Pacing Red Lines

| Field | Type | Description |
|------|------|------|
| `stagnation_threshold` | number | Rhythm stagnation threshold (consecutive N chapters with no progression = HARD-003) |
| `strand_quest_max` | number | Quest main plot maximum consecutive chapters |
| `strand_fire_gap_max` | number | Fire romance line maximum gap chapters |
| `transition_max_consecutive` | number | Maximum consecutive transition chapters |

### 1.6 Override Exemption

| Field | Type | Description |
|------|------|------|
| `allowed_rationale_types` | string[] | Permitted override reason types |
| `debt_multiplier` | number | Debt multiplier (>1 means stricter for this genre) |
| `payback_window_default` | number | Default repayment window (chapter count) |

---

## 2. Built-in Genre Profiles

### 2.1 Power Fantasy / System (shuangwen)

```yaml
id: shuangwen
name: Power Fantasy/System Flow
description: Golden finger power-ups, fast-paced leveling, face-slapping and showing off in one go
tags: [shuangwen]

hook_config:
  preferred_types: [desire hook, crisis hook, emotion hook]
  strength_baseline: medium
  chapter_end_required: true
  transition_allowance: 2

coolpoint_config:
  preferred_patterns: [flex counter, underdog reveal, overlevel counter-kill, misunderstanding elevation]
  density_per_chapter: high
  combo_interval: 5
  milestone_interval: 10

micropayoff_config:
  preferred_types: [ability payoff, resource payoff, recognition payoff]
  min_per_chapter: 2
  transition_min: 1

pacing_config:
  stagnation_threshold: 3
  strand_quest_max: 5
  strand_fire_gap_max: 15
  transition_max_consecutive: 2

override_config:
  allowed_rationale_types: [TRANSITIONAL_SETUP, ARC_TIMING]
  debt_multiplier: 1.0
  payback_window_default: 3
```

**Genre characteristics**:
- Pursues high-density cool-points; readers expect fast rhythm
- Chapter-end prioritizes a clear hook (breakthrough incoming / face-slap incoming / fortune incoming)
- Very low tolerance for transition chapters; recommended not to exceed 2 consecutive chapters
- Numerical feedback is recommended to be visualized (combat power 50 → combat power 180, before/after comparison)
- Golden finger is recommended to have limits / consumption / cooldown to avoid unlimited use

---

### 2.2 Cultivation / Fantasy (xianxia)

```yaml
id: xianxia
name: Cultivation/Fantasy
description: Defy fate, cruel laws, opportunities and struggles coexist
tags: [xianxia]

hook_config:
  preferred_types: [crisis hook, desire hook, choice hook]
  strength_baseline: medium
  chapter_end_required: true
  transition_allowance: 3

coolpoint_config:
  preferred_patterns: [overlevel counter-kill, underdog reveal, identity reveal, villain blowback]
  density_per_chapter: high
  combo_interval: 5
  milestone_interval: 15

micropayoff_config:
  preferred_types: [ability payoff, resource payoff, information payoff]
  min_per_chapter: 1
  transition_min: 1

pacing_config:
  stagnation_threshold: 4
  strand_quest_max: 6
  strand_fire_gap_max: 12
  transition_max_consecutive: 3

override_config:
  allowed_rationale_types: [TRANSITIONAL_SETUP, WORLD_RULE_CONSTRAINT, ARC_TIMING]
  debt_multiplier: 0.9
  payback_window_default: 5
```

**Genre characteristics**:
- Requires world-building; more setup chapters are permitted
- Realm breakthrough is the core anticipation; rank system is recommended to be visualized (8–10 level system, before/after numerical comparison)
- Resource monetization system (spirit stones / pills / manuals) is the core micro-payoff carrier
- Setting constraints can serve as a reasonable override reason

---

### 2.3 Romance / Sweet (romance)

```yaml
id: romance
name: Romance/Sweet
description: Emotional interaction, relationship progression, heart-fluttering and heart-wrenching intertwined
tags: [romance]

hook_config:
  preferred_types: [emotion hook, desire hook, choice hook]
  strength_baseline: medium
  chapter_end_required: true
  transition_allowance: 2

coolpoint_config:
  preferred_patterns: [sweet surprise, identity reveal, misunderstanding elevation]
  density_per_chapter: medium
  combo_interval: 6
  milestone_interval: 12

micropayoff_config:
  preferred_types: [relationship payoff, emotion payoff, recognition payoff]
  min_per_chapter: 1
  transition_min: 1

pacing_config:
  stagnation_threshold: 4
  strand_quest_max: 4
  strand_fire_gap_max: 5
  transition_max_consecutive: 2

override_config:
  allowed_rationale_types: [TRANSITIONAL_SETUP, CHARACTER_CREDIBILITY, ARC_TIMING]
  debt_multiplier: 1.0
  payback_window_default: 4
```

**Genre characteristics**:
- Romance line is the absolute core; tolerance for gaps is extremely low
- Emotion hook is the trump card (heartache / heart-fluttering / jealousy)
- Relationship progress is the most important micro-payoff

---

### 2.4 Mystery / Deduction (mystery)

```yaml
id: mystery
name: Mystery/Deduction
description: Puzzle-driven, logical deduction, truth revealed step by step
tags: [mystery]

hook_config:
  preferred_types: [mystery hook, crisis hook, choice hook]
  strength_baseline: medium
  chapter_end_required: true
  transition_allowance: 2

coolpoint_config:
  preferred_patterns: [villain blowback, identity reveal]
  density_per_chapter: low
  combo_interval: 10
  milestone_interval: 20

micropayoff_config:
  preferred_types: [information payoff, clue payoff]
  min_per_chapter: 1
  transition_min: 1

pacing_config:
  stagnation_threshold: 3
  strand_quest_max: 8
  strand_fire_gap_max: 20
  transition_max_consecutive: 2

override_config:
  allowed_rationale_types: [LOGIC_INTEGRITY, TRANSITIONAL_SETUP, ARC_TIMING]
  debt_multiplier: 0.8
  payback_window_default: 5
```

**Genre characteristics**:
- Logical integrity takes priority over cool-point density
- Information payoff is the core micro-payoff (continuous clue progress is recommended)
- LOGIC_INTEGRITY can serve as a reasonable reason for downgrading hook intensity

---

### 2.5 Rules Horror (rules-mystery)

```yaml
id: rules-mystery
name: Rules Horror
description: Eerie rules, survival deduction, counter-kill horror
tags: [rules-mystery, horror]

hook_config:
  preferred_types: [crisis hook, mystery hook, choice hook]
  strength_baseline: strong
  chapter_end_required: true
  transition_allowance: 1

coolpoint_config:
  preferred_patterns: [overlevel counter-kill, villain blowback]
  density_per_chapter: medium
  combo_interval: 5
  milestone_interval: 8

micropayoff_config:
  preferred_types: [information payoff, clue payoff, ability payoff]
  min_per_chapter: 1
  transition_min: 1

pacing_config:
  stagnation_threshold: 2
  strand_quest_max: 4
  strand_fire_gap_max: 15
  transition_max_consecutive: 1

override_config:
  allowed_rationale_types: [LOGIC_INTEGRITY, WORLD_RULE_CONSTRAINT]
  debt_multiplier: 1.2
  payback_window_default: 2
```

**Genre characteristics**:
- Tense atmosphere demands high hook intensity
- Extremely low tolerance for transition chapters (1 chapter)
- Rule constraints are reasonable override reasons

---

### 2.6 Urban Superpowers (urban-power)

```yaml
id: urban-power
name: Urban Superpowers
description: Modern setting, hidden superpowers, low-key showing off, industry chain games
tags: [urban, power, industry]

hook_config:
  preferred_types: [crisis hook, desire hook, emotion hook]
  strength_baseline: medium
  chapter_end_required: true
  transition_allowance: 2

coolpoint_config:
  preferred_patterns: [underdog reveal, flex counter, identity reveal, misunderstanding elevation]
  density_per_chapter: high
  combo_interval: 3
  milestone_interval: 10

micropayoff_config:
  preferred_types: [recognition payoff, ability payoff, relationship payoff]
  min_per_chapter: 2
  transition_min: 1

pacing_config:
  stagnation_threshold: 3
  strand_quest_max: 5
  strand_fire_gap_max: 8
  transition_max_consecutive: 2

override_config:
  allowed_rationale_types: [TRANSITIONAL_SETUP, ARC_TIMING]
  debt_multiplier: 1.0
  payback_window_default: 3
```

**Genre characteristics**:
- Face-slapping series is the core cool-point
- Modern setting requires identity hiding → reveal rhythm control
- Social status change is an important micro-payoff
- Entertainment industry / industry chain backgrounds are popular; romance line weight is high (gap tolerance drops to 8 chapters)
- Three-chapter peak rhythm: Chapter 1 predicament, Chapter 2 ability initially shown, Chapter 3 small victory + new obstacle

---

### 2.7 Zhihu Short (zhihu-short)

```yaml
id: zhihu-short
name: Zhihu Short
description: Short and fast, strong reversals, emotional impact
tags: [short, zhihu]

hook_config:
  preferred_types: [emotion hook, mystery hook, choice hook]
  strength_baseline: strong
  chapter_end_required: true
  transition_allowance: 0

coolpoint_config:
  preferred_patterns: [villain blowback, identity reveal, sweet surprise]
  density_per_chapter: high
  combo_interval: 2
  milestone_interval: 3

micropayoff_config:
  preferred_types: [emotion payoff, information payoff, relationship payoff]
  min_per_chapter: 2
  transition_min: 2

pacing_config:
  stagnation_threshold: 1
  strand_quest_max: 2
  strand_fire_gap_max: 3
  transition_max_consecutive: 0

override_config:
  allowed_rationale_types: []
  debt_multiplier: 2.0
  payback_window_default: 1
```

**Genre characteristics**:
- Transition chapter window is extremely narrow; recommend at least one perceivable gain per chapter
- Extremely high hook intensity requirement
- Highest debt multiplier (short pieces should avoid long-term debt)

---

### 2.8 Substitute / Angst (substitute)

```yaml
id: substitute
name: Substitute/Angst
description: Emotional entanglement, misunderstandings and reversals, chase wife to cremation
tags: [substitute, angst]

hook_config:
  preferred_types: [emotion hook, choice hook, mystery hook]
  strength_baseline: strong
  chapter_end_required: true
  transition_allowance: 2

coolpoint_config:
  preferred_patterns: [identity reveal, villain blowback, sweet surprise]
  density_per_chapter: medium
  combo_interval: 5
  milestone_interval: 10

micropayoff_config:
  preferred_types: [emotion payoff, relationship payoff, recognition payoff]
  min_per_chapter: 1
  transition_min: 1

pacing_config:
  stagnation_threshold: 3
  strand_quest_max: 3
  strand_fire_gap_max: 4
  transition_max_consecutive: 2

override_config:
  allowed_rationale_types: [CHARACTER_CREDIBILITY, ARC_TIMING, TRANSITIONAL_SETUP]
  debt_multiplier: 1.0
  payback_window_default: 4
```

**Genre characteristics**:
- Emotion hook is the absolute core (heart-wrenching → empathy → anticipation)
- Identity reveal is the trump card cool-point
- Extremely low tolerance for romance line gaps

---

### 2.9 Esports (esports)

```yaml
id: esports
name: Esports
description: Competition arena strategy, team bonding, comeback and championship pursuit
tags: [esports, competition]

hook_config:
  preferred_types: [crisis hook, choice hook, desire hook]
  strength_baseline: strong
  chapter_end_required: true
  transition_allowance: 1

coolpoint_config:
  preferred_patterns: [overlevel counter-kill, villain blowback, misunderstanding elevation]
  density_per_chapter: high
  combo_interval: 4
  milestone_interval: 8

micropayoff_config:
  preferred_types: [information payoff, recognition payoff, relationship payoff]
  min_per_chapter: 2
  transition_min: 1

pacing_config:
  stagnation_threshold: 2
  strand_quest_max: 4
  strand_fire_gap_max: 8
  transition_max_consecutive: 1

override_config:
  allowed_rationale_types: [TRANSITIONAL_SETUP, ARC_TIMING, LOGIC_INTEGRITY]
  debt_multiplier: 1.1
  payback_window_default: 2
```

**Genre characteristics**:
- Competition chapters recommend having trackable win/loss goals and decision nodes
- Comeback matches are the core cool-point source
- Very low tolerance for transition chapters; need to maintain real-time feedback (score / public opinion / status)

---

### 2.10 Livestream (livestream)

```yaml
id: livestream
name: Livestream
description: Platform traffic games, real-time feedback driven, public opinion and business dual-track
tags: [livestream, urban]

hook_config:
  preferred_types: [crisis hook, emotion hook, choice hook]
  strength_baseline: strong
  chapter_end_required: true
  transition_allowance: 1

coolpoint_config:
  preferred_patterns: [flex counter, villain blowback, identity reveal]
  density_per_chapter: high
  combo_interval: 3
  milestone_interval: 6

micropayoff_config:
  preferred_types: [recognition payoff, resource payoff, information payoff]
  min_per_chapter: 2
  transition_min: 1

pacing_config:
  stagnation_threshold: 2
  strand_quest_max: 4
  strand_fire_gap_max: 6
  transition_max_consecutive: 1

override_config:
  allowed_rationale_types: [TRANSITIONAL_SETUP, ARC_TIMING, CHARACTER_CREDIBILITY]
  debt_multiplier: 1.1
  payback_window_default: 2
```

**Genre characteristics**:
- Prioritize forming an "external feedback → protagonist reaction → result change" closed loop
- Public opinion reversals and business maneuvering must rely on evidence chains, not just slogans
- Data changes (viewer count / rankings / conversion) can serve as high-frequency micro-payoffs

---

### 2.11 Cosmic Horror (cosmic-horror)

```yaml
id: cosmic-horror
name: Cthulhu
description: Rule contamination and rationality collapse in parallel, higher cost closer to truth
tags: [horror, mystery, cosmic]

hook_config:
  preferred_types: [mystery hook, crisis hook, choice hook]
  strength_baseline: strong
  chapter_end_required: true
  transition_allowance: 1

coolpoint_config:
  preferred_patterns: [villain blowback, misunderstanding elevation, overlevel counter-kill]
  density_per_chapter: medium
  combo_interval: 6
  milestone_interval: 10

micropayoff_config:
  preferred_types: [clue payoff, information payoff, emotion payoff]
  min_per_chapter: 1
  transition_min: 1

pacing_config:
  stagnation_threshold: 2
  strand_quest_max: 4
  strand_fire_gap_max: 12
  transition_max_consecutive: 1

override_config:
  allowed_rationale_types: [LOGIC_INTEGRITY, WORLD_RULE_CONSTRAINT, ARC_TIMING]
  debt_multiplier: 1.3
  payback_window_default: 2
```

**Genre characteristics**:
- Horror comes from rules and costs, not pure atmosphere buildup
- Every truth advancement should be tied to a clear loss (sanity / relationships / resources)
- High-intensity hooks prioritize "unclosed rule questions" over simple scares

### 2.12 History Travel (history-travel)

```yaml
id: history-travel
name: History Travel
description: Modern soul travels to ancient times, knowledge advantage changes history, farming and wealth-building to rise
tags: [history, travel, knowledge]

hook_config:
  preferred_types: [choice hook, crisis hook, desire hook]
  strength_baseline: medium
  chapter_end_required: true
  transition_allowance: 2

coolpoint_config:
  preferred_patterns: [authority challenge, underdog reveal, villain blowback, identity reveal]
  density_per_chapter: medium
  combo_interval: 3
  milestone_interval: 10

micropayoff_config:
  preferred_types: [information payoff, resource payoff, recognition payoff]
  min_per_chapter: 1
  transition_min: 1

pacing_config:
  stagnation_threshold: 3
  strand_quest_max: 5
  strand_fire_gap_max: 10
  transition_max_consecutive: 2

override_config:
  allowed_rationale_types: [WORLD_RULE_CONSTRAINT, CHARACTER_CREDIBILITY, ARC_TIMING]
  debt_multiplier: 0.9
  payback_window_default: 4
```

**Genre characteristics**:
- Knowledge advantage > martial advantage; derivation process must be shown (not just giving the answer)
- Three-chapter peak rhythm: Chapter 1 predicament / crossroad, Chapter 2 knowledge initially displayed, Chapter 3 small victory + new obstacle
- Antagonists have reasonable motivations (interest conflicts); authority figures are not easily persuaded (need multiple demonstrations)
- History has inertia; changing one thing triggers chain reactions (nonlinear results)
- Female protagonist ratio is rising; farming / wealth-building / industry reform tags are popular

---

### 2.13 Game Lit (game-lit)

```yaml
id: game-lit
name: Game Lit
description: Game-based worldview, system golden finger driving, numerical feedback satisfaction, extreme contrast starting point
tags: [game, system, apocalypse]

hook_config:
  preferred_types: [crisis hook, desire hook, choice hook]
  strength_baseline: strong
  chapter_end_required: true
  transition_allowance: 0

coolpoint_config:
  preferred_patterns: [overlevel counter-kill, flex counter, underdog reveal, villain blowback]
  density_per_chapter: high
  combo_interval: 3
  milestone_interval: 10

micropayoff_config:
  preferred_types: [ability payoff, resource payoff, recognition payoff]
  min_per_chapter: 2
  transition_min: 1

pacing_config:
  stagnation_threshold: 2
  strand_quest_max: 5
  strand_fire_gap_max: 15
  transition_max_consecutive: 0

override_config:
  allowed_rationale_types: [WORLD_RULE_CONSTRAINT, ARC_TIMING]
  debt_multiplier: 1.1
  payback_window_default: 2
```

**Genre characteristics**:
- Early chapters recommend revealing the golden finger quickly (usually within the first 1–2 chapters)
- Numerical feedback is recommended to be visualized (combat power 50 → combat power 180, before/after comparison)
- Golden finger is recommended to have limits / consumption / cooldown to avoid unlimited use
- Transition chapter window is very narrow; recommend maintaining at least one of "cool-point or numerical progress"
- IP fusion (LOL / Pokemon etc.) is a differentiating tag; post-apocalyptic survival series is rising
- Early stage (recommend first 3 chapters) should include a clear opponent (environment / rules / specific antagonist — any one)

---

## 3. Profile Loading Mechanism

### 3.1 Loading Timing

1. **Step 1.5**: Load corresponding profile based on `state.json → project.genre`
2. **Context Agent**: Injects profile-related fields into the creative task brief
3. **Checkers**: Adjusts detection thresholds and guidance weights based on profile

### 3.2 Multi-Tag Support (Reserved)

Currently single-tag mode. When multi-tag support is added in the future:
- Use `tags` field for stacking
- For conflicting fields, take the stricter value
- Example: `[romance, mystery]` → romance line gap takes `min(5, 20) = 5`

### 3.3 Custom Profile

Users can override defaults in `state.json`:

```json
{
  "project": {
    "genre": "xianxia",
    "genre_overrides": {
      "pacing_config": {
        "stagnation_threshold": 5
      }
    }
  }
}
```

---

## 4. Relationship with Taxonomy

| Taxonomy Definition | Profile Configuration |
|--------------|-------------|
| Hook type list | Which types are preferred |
| Cool-point pattern list | Which patterns are preferred |
| Micro-payoff type list | Which types are preferred |
| Hard/Soft standards | Threshold adjustments |
| Override reason types | Which reasons are permitted |

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