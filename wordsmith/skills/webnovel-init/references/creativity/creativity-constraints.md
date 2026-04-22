# Creativity Constraints

> **Positioning**: Define structured constraints for creative generation, drive non-trope creative output.
> **Principle**: Constraints are not limitations, but catalysts for creativity; structured constraints help improve novelty and differentiation.

## Table of Contents
- I. Idea Package Schema
- II. Three-Axis Mashup
- III. Anti-Trope Triggers
- IV. Antagonist Mirror
- V. Hook-First Design
- VI. Hard Constraints
- VII. Three-Question Filter
- VIII. Scoring System
- IX. Output Format

---

## I. Idea Package Schema

Each idea must contain the following fields:

```json
{
  "id": "uuid",
  "title": "Book title",
  "one_liner": "One-line selling point (10-second elevator pitch)",
  "genre": "Genre",
  "novelty_axes": {
    "genre_base": "Genre foundation",
    "rule_constraint": "Rule constraint (at least 1 anti-convention)",
    "character_conflict": "Character conflict"
  },
  "anti_trope": "Selected anti-trope rules",
  "protagonist": {
    "flaw": "Protagonist flaw (required)",
    "desire": "Core desire"
  },
  "antagonist_mirror": {
    "shared_trait": "Shared desire/flaw with protagonist",
    "opposite_path": "The opposite path taken"
  },
  "opening_hook": {
    "hook_sentence": "One hook sentence",
    "opening_scene": "Opening scene summary",
    "chapter_end_suspense": "Chapter 1 ending suspense"
  },
  "hard_constraints": ["Hard constraint 1", "Hard constraint 2"],
  "score": {
    "novelty": 0,
    "market_fit": 0,
    "writability": 0,
    "cool_point_density": 0,
    "long_term_potential": 0,
    "total": 0
  },
  "three_questions": {
    "q1_why_this_way": "Why must this genre be written this way?",
    "q2_protagonist_swap": "Would the story collapse if protagonist swapped to a conventional character design?",
    "q3_one_liner_unique": "Can the selling point be explained in one sentence and not hit common tropes?"
  },
  "status": "pending|selected|rejected",
  "created_at": "ISO date"
}
```

---

## II. Three-Axis Mashup

### 2.1 Three Axes Definition

| Axis | Description | Example |
|------|-------------|---------|
| **Genre Foundation** | Worldview type of the story | Cultivation, urban, rules |
| **Rule Constraint** | Hard constraints on world/abilities/behavior | Resource scarcity, cheat has cost, prohibit direct combat |
| **Character Conflict** | Protagonist's internal conflict or conflict with the world | Anti-power-fantasy (not pursuing crushing dominance), moral dilemma, identity recognition |

### 2.2 Mashup Rules

**At least 2/3 axes must be "non-default options" for that genre**

| Genre | Default Options | Non-Default Options (Recommended) |
|-------|-----------------|-----------------------------------|
| Cultivation | Sufficient resources, cheat no cost, pursuing crushing dominance | Resource scarcity, cheat has cost, anti-power-fantasy/Low profile |
| Urban | Modern technology, hidden identity, face-slapping | Rule invasion, identity public, strategy game |
| Romance | Male strong female weak, misunderstanding driven, HE ending | Equals, information transparent, open ending |
| Rules | Rules can be cracked, protagonist special ability, escape | Rules irreversible, protagonist no special ability, cost survival |

### 2.3 Mashup Examples

```
✅ Good mashup:
Cultivation (genre) + Severe resource scarcity (rule) + Protagonist anti-power-fantasy (character)
→ 3/3 axes non-default, large creative space

⚠️ General mashup:
Cultivation (genre) + Cheat has cost (rule) + Pursuing crushing dominance (character)
→ 2/3 axes non-default, acceptable

❌ Trope mashup:
Cultivation (genre) + Sufficient resources (rule) + Pursuing crushing dominance (character)
→ 0/3 axes non-default, reject
```

---

## III. Anti-Trope Triggers

### 3.1 Required Rules

**Each project must select at least 1 anti-convention rule**

### 3.2 Universal Anti-Trope Library

| ID | Anti-Trope Rule | Applicable Genre | Creative Driver |
|----|----------------|-----------------|-----------------|
| AT-001 | Cheat has cost and is irreversible | All genres | Every use is a choice |
| AT-002 | Protagonist cannot directly face-slap, can only counterkill through rules/system | Power fantasy/Cultivation | Strategy replaces combat |
| AT-003 | Protagonist's advantage is simultaneously a fatal weakness | All genres | Double-edged sword design |
| AT-004 | Antagonist and protagonist share same cheat/ability | All genres | Mirror confrontation |
| AT-005 | Protagonist's goal is opposite to reader expectation | All genres | Anti-expectation narrative |
| AT-006 | World rules are unfavorable to protagonist (not protagonist privilege) | Rules/Cultivation | Fair game |
| AT-007 | Protagonist's growth costs losing something | All genres | Weight of growth |
| AT-008 | Information symmetry (protagonist doesn't know more than readers) | Mystery/Rules | Common reasoning |
| AT-009 | Protagonist's "correct choice" leads to negative consequences | All genres | Moral gray area |
| AT-010 | Cheat has usage count/cooldown limit | System flow | Resource management |

### 3.3 Vietnamese Webnovel Anti-Trope Patterns

Based on STYLE_GUIDE_VN.md analysis of Vietnamese webnovels (Biên niên sử rồng, Useless hero from another world):

| Pattern ID | Vietnamese Anti-Trope | Example from Source |
|------------|---------------------|---------------------|
| VN-AT-01 | Status card system has hidden limitations | "Thẻ trạng thái" in UH shows misleading info |
| VN-AT-02 | Underdog protagonist's "correct" decisions lead to suffering | Tanaka's choices cause setbacks (UH Chương 2) |
| VN-AT-03 | Power comes with irreversible cost to identity | "Cơ Địa Của Kẻ Vô Dụng" reduces exp gain by 80% |
| VN-AT-04 | Antagonist shares protagonist's core motivation | Endou and Tanaka both want recognition |
| VN-AT-05 | Information asymmetry between protagonist and reader | Tanaka misjudges coin value (UH Chương 1) |
| VN-AT-06 | Low-level protagonist faces high-level threats fairly | No protagonist privilege in UH |
| VN-AT-07 | Growth requires sacrifice (memory/lifespan/resources) | Level up has 5% HP recovery chance (UH) |

### 3.4 Vietnamese Pronoun System for Character Design

Vietnamese has distinct formality levels that affect character voice:

| Formality | Pronouns | Usage Context | Example |
|-----------|----------|---------------|---------|
| Highest | ngài, tôi | Nobles, ceremonies, strangers | "Ngài có thể giúp tôi..." (UH Chương 1) |
| High | tôi, ông, bà | Strangers, formal settings | "Tôi muốn gia nhập..." (UH Chương 2) |
| Equal | mày, tao | Close friends, allies, rivals | "Tao cá là mày chưa từng..." (UH Chương 4) |
| Low | thằng/kẻ (derogatory) | Enemies, contempt | "Thằng chó đó mà dám..." (UH Chương 3) |

**Character conflict design**: Use pronoun shifts to show emotional state. Normal dialogue uses "mày/mày" but anger shifts to "thằng khốn", "con nhóc".

### 3.3 Genre-Specific Anti-Tropes

See:
- `anti-trope-xianxia.md` - Fantasy/Cultivation anti-tropes
- `anti-trope-urban.md` - Urban/History anti-tropes
- `anti-trope-game.md` - Game/Sci-Fi anti-tropes
- `anti-trope-rules-mystery.md` - Rules anti-tropes

---

## IV. Antagonist Mirror

### 4.1 Core Principle

**Antagonist and protagonist share the same "desire/flaw," but take opposite paths**

### 4.2 Mirror Template

| Shared Trait | Protagonist Path | Antagonist Path |
|-------------|------------------|-----------------|
| Desire for power | Gain power through effort/sacrifice | Gain power through plunder/betrayal |
| Fear of loss | Learn to let go/accept | Control/possess everything |
| Pursuit of recognition | Prove own value | Force others to recognize |
| Escape from past | Face and reconcile | Destroy all evidence |
| Protecting loved ones | Let loved ones grow | Imprison/control loved ones |

### 4.3 Mirror Examples

```
Protagonist: Lin Tian, desires power to protect family
Antagonist: Murong Zhan, desires power to dominate everything

Shared trait: Desire for power
Protagonist path: Gain power through cultivation and sacrifice
Antagonist path: Gain power by devouring others

Mirror conflict: Their confrontation is not only a battle of strength, but also a contest of "how to gain power"
```

---

## V. Hook-First Design

### 5.1 Core Principle

**Generate hook first, then outline**

Before determining complete outline, must design:
1. One hook sentence (within 10 words)
2. One opening scene (within 50 words)
3. One Chapter 1 ending suspense (within 30 words)

### 5.2 Hook Template

| Hook Type | Template | Example |
|-----------|----------|---------|
| Contrast hook | [Identity A] yet [Behavior B] | Trash young master yet makes sect leader kneel |
| Suspense hook | [Abnormal phenomenon], [question] | He died three times, remembering each |
| Cost hook | [Gain X], cost is [Y] | Gain divine system, cost is lifespan |
| Choice hook | [Dilemma], he chooses [unexpected] | Save wife or save world, he chooses third path |
| Reversal hook | [Expectation A], actually [B] | Everyone thought he was dead, including himself |

### 5.3 Opening Scene Template

| Scene Type | Characteristics | Applicable Genre |
|------------|-----------------|------------------|
| Crisis opening | Protagonist at life-and-death edge | Rules, Cultivation |
| Contrast opening | Protagonist identity/ability vs. performance contrast | Playing pig to kill tiger, Urban |
| Suspense opening | Throw unsolved mystery | Mystery, Rules |
| Conflict opening | Protagonist directly conflicts with others | Power fantasy, Romance |
| Daily broken | Peaceful daily life broken | All genres |

---

## VI. Hard Constraints

### 6.1 Core Principle

**Define 2-3 hard constraints, force out unique plot solutions**

### 6.2 Hard Constraint Types

| Type | Description | Example |
|------|-------------|---------|
| Worldview constraint | Unbreakable rules of world operation | "Immortals cannot kill mortals" |
| Ability constraint | Hard limits on protagonist's abilities | "Cheat can only be used once per day" |
| Behavior constraint | Protagonist behavior forbidden zones | "Protagonist cannot attack proactively" |
| Information constraint | Boundaries of what protagonist knows/doesn't know | "Protagonist doesn't know they're a transmigrator" |
| Resource constraint | Hard limits on scarce resources | "Only 100 spirit stones in entire world" |

### 6.3 Vietnamese Webnovel-Specific Constraints

From VN webnovel analysis (Biên niên sử rồng, Useless hero):

| Constraint Type | Vietnamese Pattern | Narrative Effect |
|-----------------|-------------------|------------------|
| System limitation | Status card shows info but protagonist misunderstands | Information gap drives conflict |
| Cost type | Cheat has usage limit (5% HP recovery on level up) | Every choice matters |
| Identity constraint | Protagonist unaware of true ability magnitude | Anti-power-fantasy |
| Social constraint | Must use formal pronouns with authority figures | Character development through language shift |

### 6.4 Constraint Combination Examples

```
Project: "Rule Prison"

Hard Constraint 1 (Worldview): Once triggered, rules cannot be revoked
Hard Constraint 2 (Ability): Protagonist can only "see" rules, not "change" rules
Hard Constraint 3 (Behavior): Each time protagonist reminds others of rules, they lose a memory

Creative drivers:
- How can protagonist help others without changing rules?
- How does protagonist make choices at the cost of losing memory?
- How do irrevocable rules create tension?
```

**Vietnamese variant:**
```
Project: "Kẻ Vô Dụng" (The Useless One)

Hard Constraint 1 (System): Status card displays stats but true values hidden
Hard Constraint 2 (Cost): Level up only 5% HP recovery, no mana refund
Hard Constraint 3 (Identity): Protagonist thinks weak but actually has unique ability

Creative drivers (UH pattern):
- How does protagonist survive when every stat is below average?
- How does misinterpretation of "Cơ Địa Của Kẻ Vô Dụng" create anti-tension?
- Why does the protagonist's "wrong" understanding lead to discovery?
```

---

## VII. Three-Question Filter

### 7.1 Filtering Questions

| # | Question | Pass Standard |
|---|----------|---------------|
| Q1 | Why must this genre be written "this way"? | Can state at least 1 unique reason |
| Q2 | Would the story collapse if protagonist swapped to a conventional character design? | Yes (indicates character design deeply bound with story depth) |
| Q3 | Can this selling point be explained clearly in one sentence and not hit common tropes? | Yes (indicates selling point clear and differentiated) |

### 7.2 Filtering Process

```
Generate 3-5 ideas
    ↓
Three-question filter
    ↓
Pass 3/3 → Enter scoring
Pass 2/3 → Modify and rescreen
Pass 1/3 or 0/3 → Eliminate
```

---

## VIII. Scoring System

### 8.1 Five-Dimensional Scoring

| Dimension | Weight | 1 Point | 3 Points | 5 Points |
|-----------|--------|---------|----------|----------|
| Novelty | 25% | Cliché | Micro-innovation | Create new category |
| Market Fit | 20% | Niche | Medium audience | Mass market |
| Writability | 20% | Extremely difficult | Medium difficulty | Easy to implement |
| Cool Point Density | 20% | Sparse cool points | Medium density | High density |
| Long-term Potential | 15% | Hard to continue | Can continue | Infinitely expandable |

### 8.2 Calculation Formula

```
Total = Novelty×2.5 + Market Fit×2 + Writability×2 + Cool Point Density×2 + Long-term Potential×1.5
Full score = 50 points
Passing line = 30 points
Recommended line = 40 points
```

---

## IX. Output Format

### 9.1 Idea Card Format

```markdown
## Idea #{N}: {title}

**One-line selling point**: {one_liner}

**Three-Axis Mashup**:
- Genre foundation: {genre_base}
- Rule constraint: {rule_constraint}
- Character conflict: {character_conflict}

**Anti-trope rules**: {anti_trope}

**Protagonist design**:
- Flaw: {flaw}
- Desire: {desire}

**Antagonist mirror**:
- Shared trait: {shared_trait}
- Opposite path: {opposite_path}

**Opening hook**:
- Hook: {hook_sentence}
- Opening: {opening_scene}
- Suspense: {chapter_end_suspense}

**Hard constraints**:
1. {constraint_1}
2. {constraint_2}

**Three-question filter**:
- Q1: {answer_1}
- Q2: {answer_2}
- Q3: {answer_3}

**Score**: {total}/50
- Novelty: {novelty}/5
- Market Fit: {market_fit}/5
- Writability: {writability}/5
- Cool Point Density: {cool_point_density}/5
- Long-term Potential: {long_term_potential}/5
```

---

## Con Duong Ba Chu - Creative Constraint Templates

Pattern từ **Con Duong Ba Chu** cho creative constraints:

### Con Duong Ba Chu Constraint Types

| Constraint Type | Description | Example |
|----------------|-------------|---------|
| **World Constraint** | Unbreakable world rules | "Immortals cannot directly intervene in mortal affairs" |
| **Ability Constraint** | Hard limits on protagonist abilities | "Cheat can only be activated 3 times per day" |
| **Social Constraint** | Societal rules protagonist must follow | "Must use formal pronouns with superiors" |
| **Identity Constraint** | Protagonist unaware of their true nature | "Thinks weak but actually has hidden potential" |
| **Resource Constraint** | Scarce resources create competition | "Only 100 spirit stones exist in the entire world" |
| **Cost Constraint** | Power comes with irreversible cost | "Using forbidden technique costs lifespan" |

### Golden Finger Constraint Templates (Con Duong Ba Chu)

**Template 1: Inverted Ability**
```
Golden Finger: [Positive ability] disguised as [Negative condition]
Example: "Cơ Địa Của Kẻ Vô Dụng" (Useless Body)
- Appears as: Terrible stats,废物
- Actually: 80% less exp needed for level up
- Cost: Must endure being looked down upon
```

**Template 2: Usage Limit**
```
Golden Finger: [Powerful ability] with [strict limit]
Example: "System Shop"
- Ability: Can exchange for any skill/item
- Limit: Currency only obtained through combat (risk)
- Cost: Must fight dangerous battles to afford upgrades
```

**Template 3: Hidden Information**
```
Golden Finger: [Status display] that misleads
Example: Status Card (UH pattern)
- Shows: Low stats, weak potential
- Hidden: True values are multiplier-based
- Cost: Protagonist and enemies both misjudge
```

**Template 4: Double-Edged Sword**
```
Golden Finger: [Strength] that is also [weakness]
Example: "Overconfidence in Crypto" (Trí Vĩ)
- Strength: High risk tolerance leads to big gains
- Weakness: One failure causes total collapse
- Cost: Every decision is life-or-death
```

### Protagonist Desire/Flaw Constraint Templates (Con Duong Ba Chu)

**Template 1: Survival + Overconfidence**
```
Protagonist: Trí Vĩ (Crypto trader example)
- Desire: Survive and profit in crypto world
- Flaw: Overconfidence leads to excessive risk-taking
- Constraint: Single bad decision can wipe out everything
- Plot Driver: Flaw constantly threatens desire
```

**Template 2: Power + Protective Nature**
```
Protagonist: Lin Thiên
- Desire: Become powerful enough to protect family
- Flaw: Over-protective, makes reckless decisions
- Constraint: Can't always be everywhere to protect
- Plot Driver: Must learn when to let others fight
```

**Template 3: Revenge + Moral Code**
```
Protagonist: Hidden Identity cultivator
- Desire: Revenge against sect that destroyed family
- Flaw: Honorable upbringing conflicts with required ruthlessness
- Constraint: Can't use certain methods even if effective
- Plot Driver: Must find creative ways that align with values
```

### World-Building Constraint Templates (Con Duong Ba Chu)

**Template 1: Tu Chân Giới Style**
```
World: Tu Chân Giới (Cultivation World)
Constraint: "Cấm Kỵ" (Forbidden techniques)
- Forbidden techniques have extreme power but cause backlash
- Using them marks protagonist as "demonic cultivator"
- Social stigma creates additional obstacles
```

**Template 2: Cấm Kỵ Zone**
```
World Area: Cấm Kỵ Zone (Forbidden Zone)
Constraint: "Ngàn năm không ai sống sót"
- Entering requires special permission
- Resources inside are invaluable but dangerous
- Protagonist must find creative way to survive
```

**Template 3: Hồn Lực System**
```
World: Hồn Lực (Soul Power) System
Constraint: "Hồn lực cạn kiệt = death"
- Soul power is finite resource
- Recovery requires rare opportunities
- Every fight has permanent consequence
```

### Con Duong Ba Chu Constraint Checklist

**Constraint Design:**
- [ ] Constraint is NOT purely numerical (specific, situational)
- [ ] Constraint creates PLOT complications (not just power limits)
- [ ] Constraint affects protagonist's RELATIONSHIPS
- [ ] Constraint has IRREVERSIBLE consequences
- [ ] Constraint can be worked around (not absolute block)

**Golden Finger Constraints:**
- [ ] Has clear limitation (usage, cost, condition)
- [ ] Limitation creates meaningful choices
- [ ] Cost is visible but not disabling
- [ ] Strength/weakness are connected

**World Rules Constraints:**
- [ ] Rules fit genre expectations (cultivation world has Tu Chân Giới concepts)
- [ ] Rules create natural antagonist forces
- [ ] Rules enable protagonist's unique path
- [ ] Rules have internal consistency

**Protagonist Constraints:**
- [ ] Desire is clear and compelling
- [ ] Flaw is specific psychological trait (not generic "weak")
- [ ] Desire and flaw are CONNECTED
- [ ] Flaw creates constant tension with desire
