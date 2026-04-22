# System Flow Genre Template

> **Core Appeal**: Data visualization + Task-driven + Deterministic return. The system is the MC's strongest cheat, but possibly also the biggest shackle.

---

## Creative Constraints (Optional)
- Recommended Pack: Pack M13 / Pack M05
- Universal Overlay: Pack U03

## 1. Core Mechanism Design

### Visualization Panel
- **Principle**: Simple and direct. Don't list dozens of useless data (like: charm, luck, spirit - unless these are actually used).
- **Exception rule**: If you decide to keep "charm/luck/spirit" etc non-combat attributes, must satisfy two conditions:
  1. **Short-term feedback**: In the next 5-10 chapters trigger at least 1 perceptible plot feedback (negotiation/social/luck/insight), let readers feel "this value is useful".
  2. **Don't spam**: Panel display should be restrained, avoid repeating complete attribute table every chapter (only show changes at upgrades/key moments).
- **Dynamic feedback**: After each training/combat, data must increase (e.g., swing sword 1000 times, experience +10).

### Task Generation Logic
- **Main quest**: Mandatory, failure has punishment (erasure/life deducted). Engine pushing plot development.
- **Side quest**: Optional, rich rewards. Enrich worldview.
- **Achievement quest**: Hidden trigger. Give readers surprise.

---

## 2. Numerical Inflation Control Valve (Inflation Control)

### Why Does It Break?
- **Exponential growth**: Level 1 100 atk, level 10 10000 atk, level 100 100 million atk. Numbers too big, readers numb.
- **Currency devaluation**: Late game billions of points casually spent, system mall loses meaning.

### Control Plan
1. **Attribute compression**: When changing maps, perform numerical compression (e.g., after ascension, lower realm 100 million combat power = upper realm 1 point divine power).
2. **Currency recovery**: Launch "money-eating beast" function (e.g., system upgrade, lottery pity, artifact repair), massively consume player points.
3. **Marginal effect**: Higher level, exponential increase in experience needed for upgrade, slow upgrade speed.

---

## 3. Relationship Between System and Host (The Relationship)

### Stage One: Tool Period (Chapters 1-200)
- System cold and mechanical, mechanically issues tasks. MC depends on system to survive.
- **Naming suggestion**: When system name/function temporarily unknown, use "code name/call" in text (e.g., "Inheritor System" "panel"), don't use "???" as reader-visible text.

### Stage Two: Partner Period (Chapters 201-500)
- System unlocks intelligent voice/elf image. Start complaining, being cute, providing suggestions.
- MC starts thinking about system's source.

### Stage Three: Gaming Period (Chapters 501+)
- **Conspiracy theory**: Who created the system? For what purpose? (Cultivate soldiers? Body snatching? Cultivate savior?)
- **Resistance**: MC tries to break system's control, find ways to get strong without system.

---

## 4. Classic System Types Detailed

### Check-in Flow (Sign-in)
- **Core**: Clock in at specific location/time.
- **Satisfaction**: Exploring map = obtaining rewards.
- **Trap**: Easy to become water journal. Must combine with plot (being forced to enter forbidden area for check-in).

### Gacha Flow (Lottery)
- **Core**: Randomness. Bike becomes motorcycle.
- **Satisfaction**: Lucky moment, desperate reversal.
- **Trap**: Luck too good seems fake. Need foreshadow "luck value" or "sacrifice" cost.

### Shop Flow (Exchange)
- **Core**: As long as you have money/points, you can buy anything.
- **Satisfaction**: As long as you grind, you can be strong.
- **Trap**: Easy to become "working grind flow".

---

## 5. Task Generator (Task Generator Prompt)

In `/wordsmith-write`, if needing to generate system tasks, use this Prompt:

```text
Please generate a [type] task for the MC.
Current situation: [What MC is doing]
Requirements:
1. Task objective must be challenging but completable.
2. Reward must include [item MC urgently needs].
3. Failure punishment must make MC feel pain (but not fatal).
4. Task description style: [cold/tsundere/comedic].
```

---

## Tools: Entity Tag Extensions

```xml
<entity type="system function" name="function name" desc="effect" tier="level" unlock="unlock condition"/>
<entity type="system item" name="item name" desc="effect" tier="level" price="price"/>
<entity type="system task" name="task name" desc="reward" tier="level" difficulty="difficulty" penalty="punishment"/>
```
