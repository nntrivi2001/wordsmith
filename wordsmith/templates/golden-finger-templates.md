# Golden Finger Template Library

> **Purpose**: Provide a systematic golden finger design framework ensuring rationality, visualization, and excitement output capability for golden finger settings.

---

## 📋 Core Principles of Golden Finger Design

### 1. Functionality Principle
- **Clear positioning**: Golden finger must have a clear core function (upgrade assistance/combat enhancement/resource acquisition)
- **Growth**: Golden finger should upgrade as protagonist grows, avoid "unchanging forever"
- **Limitations**: Must have reasonable limitations (cooldown/consumable resources/usage conditions), avoid "invincible cheat"

### 2. Visualization Principle
- **Panel-based**: Use panels/attribute displays to give readers intuitive data feedback
- **Progress bars**: Use progress bars for skill proficiency, experience points, etc.
- **Immediate feedback**: Display effects immediately after use (+10 Strength/realm breakthrough notification)

### 3. Exciting Point Embedding Principle
- **Acquisition excitement**: Sense of ritual when golden finger is first obtained
- **Growth excitement**: Golden finger upgrades/unlocks new functions
- **Usage excitement**: Golden finger plays key role at critical moments (face-slapping/counterattack)

---

## ✅ Golden Finger Template Fields (Required)

| Field | Description | Example |
|-------|-------------|---------|
| Core Function | Core problem golden finger solves | Resource acquisition / Information gap / Combat supplement |
| Trigger Condition | When it takes effect | Specific scene / Cooldown complete / Price paid |
| Cost/Limitation | Must-pay cost | Lifespan/memory/resources/credibility |
| Counter Method | How enemies restrain | Rule blocking / Supply cut / Reverse exploitation |
| Visibility | Reader and character perception | Open / Semi-open / Hidden |
| Feedback Rhythm | Reader perception frequency | Small reward every N chapters |
| Upgrade Path | Ability growth curve | Three-stage/version iteration |
| Excitement Nodes | Key climaxes | Acquisition/first use/reversal |

---

## 🧩 Cost/Limitation Library (Common)

- **Lifespan/Health**: Each use reduces lifespan or harms body
- **Memory/Emotion**: Loss of important memories, emotional cooling
- **Resource Consumption**: Spirit stones/gold coins/contribution points/credit points
- **Relationship Cost**: Trust overdraft, interpersonal collapse
- **Rule Retaliation**: Cross-realm must retaliate, mandatory cooldown
- **Information Cost**: Information gained must lose equal amount of information

## 🛡️ Counter Method Library (Common)

- **Rule Blocking**: Hostile rules make golden finger ineffective
- **Supply Cut**: Resources/system points cut off
- **Mirror Counter**: Antagonist has similar abilities
- **Misleading Use**: System prompts reverse exploited
- **Cost Transfer**: Antagonist makes protagonist bear more cost

---

## ⏱️ Excitement/Feedback Rhythm Template

- **Small reward**: At least 1 perceptible feedback every 2-3 chapters
- **Medium reward**: Significant upgrade every 8-10 chapters
- **Big reward**: Version change every 20-30 chapters
- **Cost fulfillment**: Must fulfill cost before and after each big reward

---

## 📌 Type Quick Reference (Direct Selection)

| Type | Core Excitement | Typical Cost | Common Counter |
|------|----------------|-------------|---------------|
| System Panel | Numerical growth/visualization | Task failure penalty | Rule blocking/similar system |
| Storage Space | Hoarding/resource leap | Resource consumption | Supply cut/space seal |
| Rebirth/Transmigration | Information gap | Memory deviation | History changes/opponent rebirth |
| Check-in | Continuous rewards | Cooldown/count | Limited scene/seal |
| Artifact Spirit/Mentor | Guidance/inheritance | Recovery resources | Spirit sleeps/seal |
| Bloodline Awakening | Enhancement leap | Retaliation/loss of control | Bloodline restraint/seal |
| Power Awakening | Single-point burst | Mental/physical retaliation | Counter powers |

---

## 🧬 Compound Golden Finger Combination Rules

- **One main one auxiliary** (Avoid "cheat stacking cheat")
- **Cost stacking must be balanced** (At least one hard cost must remain)
- **Combination example**: System + Space (System handles tasks/upgrades, Space handles resources)

---

## 🧭 Genre-Golden Finger Matching Description

| Genre | Recommended Golden Finger |
|-------|-------------------------|
| Xuanhuan/Cultivation | System panel, Check-in, Old grandfather/inheritance, Bloodline awakening |
| Urban Fantasy | System panel, Rebirth memory, Power awakening, Storage space |
| Romance | Rebirth memory, Storage space, No golden finger |
| Zhihu Short | Single special ability, No golden finger |
| Rule Horror | System prompts, Rule interpretation ability |

**Expansion suggestions (optional)**:
- Apocalypse: Storage space / Resource exchange system
- Infinite flow: Task system / Level rule prompts
- Realistic themes: No golden finger / Light resource aid

> Note: Matching table is for "priority recommendation," not mandatory.

---

## 🎮 Golden Finger Type Templates

### Type 1: System Panel Flow

**Core Mechanism**: Digitalized cultivation, visualized growth

**Standard Panel Structure**:

```markdown
【Cultivation System v1.0】

╔═══════════════════════════════════════╗
║ Host Information                           ║
╠═══════════════════════════════════════╣
║ Name: Lin Tian                         ║
║ Realm: Foundation Building Layer 3     ║
║ Lifespan: 18/150                      ║
║ Luck: 78 (Greatly Auspicious)         ║
╚═══════════════════════════════════════╝

╔═══════════════════════════════════════╗
║ Base Attributes                          ║
╠═══════════════════════════════════════╣
║ Strength: 25 (Normal 1)               ║
║ Agility: 18 (Normal 1)                ║
║ Spirit: 32 (Normal 1)                 ║
║ Spiritual Power: 1580/1580             ║
╚═══════════════════════════════════════╝

╔═══════════════════════════════════════╗
║ Technique Skills                         ║
╠═══════════════════════════════════════╣
║ [Devouring Divine Art] Level 5 (4523/5000) [Can Break Through]║
║ [Thunder Sword] Level 3 (890/1000)          ║
║ [Vajra Body]   Level 2 (350/500)           ║
╚═══════════════════════════════════════╝

╔═══════════════════════════════════════╗
║ Talent Lines                              ║
╠═══════════════════════════════════════╣
║ [Heaven Rewards Diligence·Gold] Cultivation speed +1000%          ║
║ [Battle Intuition·Purple] Can sense danger in battle               ║
╚═══════════════════════════════════════╝

╔═══════════════════════════════════════╗
║ Resource Pool                             ║
╠═══════════════════════════════════════╣
║ Spirit Stones: 10,580 pieces            ║
║ Potential Points: 250 points [Can allocate]║
║ Task Points: 18 points                 ║
╚═══════════════════════════════════════╝
```

**Entity Tag Format**:
```xml
<entity type="system_module" name="module_name" desc="function_description" tier="tier" unlock="unlock_condition"/>

Example:
<entity type="system_module" name="mall_system" desc="can use spirit stones to exchange for pills/techniques/treasures" tier="core" unlock="foundation_building"/>
<entity type="system_module" name="lottery_system" desc="consume task points for random lottery" tier="branch" unlock="golden_core"/>
<entity type="system_module" name="time_space_travel" desc="can travel to other planes for experience" tier="core" unlock="yuan_ying"/>
```

**System Function Version Iteration Example**:

| Version | Unlock Condition | New Functions | Excitement Design |
|---------|-----------------|---------------|-------------------|
| **v1.0** | Initial acquisition | Attribute panel, Skill bar, Storage space | Shock when acquiring system |
| **v2.0** | Foundation Building | Mall, Tasks, Lottery | Mall opens, purchases first treasure |
| **v3.0** | Golden Core | Side professions (Alchemy/Artifact forging), Pet system | Refines first furnace of pills/tames divine beast |
| **v4.0** | Yuan Ying | Time-space travel, Plane merchant | Travel to other worlds for adventure |

---

### Type 2: Storage Space Flow

**Core Mechanism**: Private storage space + special functions

**Standard Space Attributes**:

```markdown
【Carrying Space】

Basic Parameters:
- Space size: 100 m² (upgradable)
- Time flow: 1 day outside = 10 days inside
- Planting acceleration: Spiritual medicine growth speed +500%
- Storage function: Unlimited stacking of same-type items

Special Functions:
1. [Time Freeze] - Food/medicine stays fresh after storage
2. [Dense Spiritual Energy] - Cultivation speed inside space +300%
3. [Intent Collection] - Can store items by touching them
4. [Living Entity Storage] - Can store spirit beasts/combat prisoners (requires spiritual power consumption)
```

**Upgrade Path**:
```markdown
Level 1 → 100 m² (initial)
Level 2 → 500 m² (requires Foundation Building + 1000 spirit stones)
Level 3 → 1000 m² (requires Golden Core + 10000 spirit stones)
Level 4 → Small World (requires Yuan Ying + special opportunity)
```

**Excitement Design**:
- **Hoarding excitement**: Frenetically hoarding supplies before apocalypse/war
- **Planting excitement**: Planting spiritual medicine in space, quickly obtaining resources
- **Hidden excitement**: Pulling out big weapons from space at critical moments

---

### Type 3: Rebirth/Transmigration Flow

**Core Mechanism**: Information gap advantage

**Prophet Types**:

```markdown
【Rebirth Advantage List】

1. Time Node Memory:
   - 3 months later: Tianyun Sect secret realm opens
   - 6 months later: Blood Evil Sect invasion
   - 1 year later: Spiritual vein major eruption
   - 3 years later: Ancient ruins emerge

2. Key Character Intelligence:
   - Li Xue: Becomes Pill Sage in future, now still outer sect disciple
   - Young Master Wang: Seems like genius, actually demon cultivator, betrays in 3 years
   - Elder Yun: Hidden identity as Yuan Ying powerhouse

3. Treasure/Opportunity Locations:
   - Deep in Black Wind Mountain Range: Thunder Lightning Fruit (Foundation Building divine fruit)
   - Back mountain of Qingyun Peak: Ancient Sword Tomb entrance
   - Tianyun City Auction: Hidden auction items on 15th of each month
```

**Entity Tag Format**:
```xml
<entity type="future_event" name="event_name" desc="event_description" tier="tier" time="occurrence_time" strategy="response_strategy"/>

Example:
<entity type="future_event" name="secret_realm_opening" desc="Tianyun Sect back mountain secret realm opens, contains Foundation Building pills" tier="core" time="3_months_later" strategy="prepare passage token in advance"/>
<entity type="future_event" name="blood_evil_invasion" desc="Evil path attack, family suffers disaster" tier="core" time="6_months_later" strategy="evacuate family and assets in advance"/>
```

---

### Type 4: Check-in Flow

**Core Mechanism**: Continuous check-in to obtain rewards

**Check-in System Design**:

```markdown
【Daily Check-in System】

Check-in Rules:
- Normal check-in: Can check in 1 time daily, obtain basic reward
- Consecutive check-in: More consecutive days, richer rewards
- Special location check-in: Special location check-in grants extra rewards

Reward Examples:
┌─────────────────────────────────┐
│ Day 1: Gathering Qi Pills x3                │
│ Day 7: Foundation Building Pill x1           │
│ Day 30: Mystery Grade technique book x1       │
│ Day 100: Heavenly Grade treasure x1          │
│ Day 365: Divine-level bloodline awakening     │
└─────────────────────────────────┘

Special Check-in Locations:
- [Check-in at Tianyun Sect Main Hall]: Gain 10x sect contributions
- [Check-in at Secret Realm Entrance]: Random chance to obtain secret realm key
- [Check-in at Hostile Sect]: Obtain "Bold Madman" achievement + rare item
```

**Excitement Rhythm**:
- Daily small excitement: Normal check-in rewards
- Weekly medium excitement: 7-day check-in rewards
- Monthly big excitement: 30-day check-in rewards
- Yearly super excitement: 365-day check-in rewards

---

### Type 5: Old Grandfather/Artifact Spirit Flow

**Core Mechanism**: Mentor assistance + knowledge transmission

**Artifact Spirit Setting Template**:

```markdown
【Artifact Spirit: Sword Spirit·Gu Chen】

Basic Information:
- True identity: Ancient sword immortal's remnant soul
- Peak realm: Crossing Tribulation stage
- Proficient fields: Sword dao, Artifact forging, Formations
- Personality traits: Tsundere, sharp-tongued, says no but means yes

Assistance Functions:
1. [Transmit Technique]: Can teach protagonist sword techniques/cultivation methods
2. [Appraisal]: Can appraise treasure grade and usage
3. [Guidance]: Provide strategic advice in battle
4. [Book Collection]: Owns ancient technique library

Limitation Conditions:
- Teaching techniques requires protagonist's realm to meet requirements
- Each guidance consumes protagonist's spiritual power
- Artifact spirit recovery requires specific resources (spirit stones/blood essence)
```

**Dialogue Style Examples**:
```markdown
❌ Wrong (mechanical):
"Detecting enemy strength at Golden Core stage, recommend retreat."

✅ Correct (personified):
"Boy, that old guy's aura is thick, at least Golden Core late stage! You're only Foundation Building, going up is just sending yourself to death! Run now, don't embarrass this old man!"
```

---

### Type 6: Bloodline/Talent Type

**Core Mechanism**: Bloodline awakening brings ability leap, combined with growth limitations and costs.

**Template Points**:
- Bloodline source: Ancient remnant clan / Divine beast descendant / Ancestral hidden bloodline
- Awakening condition: Life-and-death crisis / Specific spiritual medicine / Emotional eruption
- Ability limitations: Awakening count / Side effects / Cooldown

**Example**:
```markdown
【Bloodline: Azure Dragon Blood】
- Awakening condition: Triggered when near death
- Core ability: Body strength +200%, Speed +50%
- Side effect: Need to rest for 3 days after awakening
```

---

### Type 7: Power Awakening Type (Urban Fantasy Only)

**Core Mechanism**: Awaken single or compound powers, emphasizing cost and growth ceiling.

**Template Points**:
- Power source: Experiment accident / Talent inheritance / External substance stimulation
- Ceiling and cost: Physical consumption / Spiritual backlash / Usage count
- Evolution direction: Single-line enhancement / Multi-branch growth

**Example**:
```markdown
【Power: Time Stasis (Brief)】
- Initial ceiling: 3 seconds / use
- Cost: 30 seconds of dizziness after each use
- Evolution direction: Extend duration OR shorten cooldown
```

---

## No Golden Finger (Pure Growth Route)

**Applicable Scenarios**: Romance, realistic-oriented, Zhihu short stories or anti-trope themes.

**Alternative Enhancement Points**:
- Protagonist talent: Specialty/talent/extremely strong will
- Special opportunities: Master inheritance/resources/connections
- Growth route: Skill tree/career path/psychological growth

**Note**: No golden finger doesn't equal "no excitement points," excitement points need to be transferred to character design, choices, costs, and counterattacks.

---

## 🛠️ Golden Finger Design Workflow

### Step 1: Determine Core Positioning

**Question checklist**:
1. What is the protagonist's biggest weakness? (Slow cultivation speed/lack of resources/insufficient information)
2. What problem does the golden finger solve?
3. What is the golden finger's unique selling point?

### Step 2: Set Acquisition Method

**Common methods**:
- ✅ Accidental fusion (picked up ancient ring/was struck by lightning)
- ✅ Inheritance activation (bloodline awakening/ancestral treasure)
- ✅ System descent (mysterious voice/pop-up light screen)
- ❌ Avoid: Appearing out of nowhere, no reason at all

### Step 3: Design Panel/Interface

Use Markdown tables or ASCII art to design visualized panels

### Step 4: Plan Upgrade Route

```markdown
Level 1 → Level 2 → Level 3 → ... → Final form
(Corresponding protagonist realm: Qi Gathering → Foundation Building → Golden Core → ...)
```

### Step 5: Embed Excitement Nodes

- First acquisition: Sense of shock
- First use: Immediate effect
- Version upgrade: Unlock new functions
- Critical moment: Golden finger saves life/counterattack

---

## ✅ Golden Finger Design Checklist

**Required Elements**:
- [ ] Clear core function
- [ ] Visualized panel/interface
- [ ] Reasonable limitation conditions
- [ ] Clear upgrade route
- [ ] Embedded excitement nodes

**Avoiding Minefields**:
- ❌ Functions too complex, readers can't remember
- ❌ Unlimited invincible cheat with no restrictions
- ❌ Acquisition method too random
- ❌ Long-term no upgrade, losing freshness

---

## 📝 Entity Tag Expansion Description

For golden finger systems, the following XML tag types can be used:

```xml
<entity type="system_module" name="module_name" desc="function_description" tier="tier" unlock="unlock_condition"/>
<entity type="system_currency" name="currency_name" desc="acquisition_method" tier="tier" initial="initial_amount"/>
<entity type="system_item" name="item_name" desc="effect" tier="tier" grade="grade" source="acquisition_path"/>
<entity type="future_event" name="event_name" desc="event_description" tier="tier" time="occurrence_time" strategy="response_strategy"/>
```

> **v5.0 Introduction (v5.4 continues)**: These tags are **optional**. Data Agent can automatically extract entities from pure text, tags are only for manual annotation scenarios.

---

## 📚 Reference Cases

### Case 1: 《Global Martial Arts》- Wealth Conversion System
- Core function: Real money → Cultivation resources
- Excitement: Rich second-generation identity + spending money to grow stronger
- Limitation: Must earn money legally, can't rob

### Case 2: 《I Have an Adventure House》- Mobile APP System
- Core function: Phone publishes tasks, completing earns rewards
- Excitement: Tasks are bizarre, rewards are generous
- Limitation: Task failure has penalties

### Case 3: 《Cultivation Chat Group》- Chat Group System
- Core function: Join immortal chat group, obtain cultivation resources and intelligence
- Excitement: Exchange with big shots, grab red packets
- Limitation: Group rules are strict, violations get kicked out

---

**Final Reminder**: Golden finger isn't stronger is better, it's more "clever" is better. The best golden finger lets protagonist "effort + cheat" work together, neither appearing to get something for nothing, yet able to happily crush opponents.
