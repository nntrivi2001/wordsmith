# Pronoun Selection: Context-Only System

## Core Philosophy

**Pronouns come from context, not rules.**

The current system uses static tables mapping "character type → pronoun pair." This produces unnatural dialogue because it ignores the complex factors that determine how people actually speak.

The new system is **pure context-based inference**. When writing dialogue, the AI should ask: "What would this person naturally say in THIS situation?"

---

## Key Context Factors

### Factor 1: Time Period / Genre (PRIMARY)

Time period is the **primary differentiator** for pronoun selection. Modern characters speak modernly; ancient characters speak archaically.

| Time Period | Common Forms | Examples |
|------------|--------------|-----------|
| **Modern (đương đại)** | tớ - cậu, tôi - bạn, mình - mày | Contemporary settings, isekai, modern romance |
| **Republican (cận đại)** | tao - mày, tôi - anh | Early 20th century, war stories |
| **Feudal (phong kiến)** | ta - ngươi, huynh - đệ, tỷ - muội | Period drama, wuxia, martial arts |
| **Ancient/Royal (cổ đại)** | trẫm - ngài, bổn cung - ngươi | Palace dramas, royal settings |

**Logic:** A modern high school student transmigrated to a fantasy world would NOT suddenly speak in feudal forms just because they're in a fantasy setting. Their background shapes their natural speech.

### Factor 2: Character Background

Ask: "What would this person naturally say?"

Character background includes:
- **Education level** - Scholarly people speak more formally
- **Social class** - Upper class vs street level
- **Tradition** - Martial (kiếm khách) vs scholarly (nho gia) vs merchant
- **Region** - Northern vs Southern speech patterns

### Factor 3: Power Dynamics

Ask: "Who has power in THIS moment?"

| Speaker Role | Common Forms | Notes |
|-------------|-------------|-------|
| Authority (master, leader) | Bổn tọa, ta | Commanding, dominant |
| Subordinate (disciple, servant) | Tại hạ, các hạ | Respectful, submissive |
| Equals in conflict | Ngươi, ngươi hả | Challenge, direct |
| Equals in harmony | Huynh, đệ, tỷ, muội | Brotherhood/sisterhood |

**Important:** Power can shift within a scene. When it does, pronouns should shift too.

### Factor 4: Relationship Arc

Ask: "Where are these two in their relationship journey?"

| Arc Stage | Common Forms | Example |
|----------|--------------|---------|
| First meeting | các hạ - tại hạ | Formal courtesy between strangers |
| Familiar/Brotherhood | huynh - đệ | Equals who have bonded |
| Life-and-death partners | huynh - đệ | Same as brotherhood |
| Rift forming | kẻ kia - [tên] | Growing distance |
| Broken/betrayal | [tên thật] | Direct address, pain revealed |

### Factor 5: Emotional Subtext

Ask: "What are they REALLY feeling?"

Pronouns can carry hidden meaning:

| Emotion | Pronoun Choice | Effect |
|--------|---------------|--------|
| Sarcasm | Formal forms used with wrong tone | Mocks rather than respects |
| Hidden love | Softened formal forms | Can't admit feelings directly |
| Rage masking hurt | Name at peak moment | Vulnerability through name |
| Fear/desperation | Primitive forms (thằng khốn) | Raw survival instinct |

### Factor 6: Combat Intensity

Ask: "What phase of combat is this?"

| Phase | Common Forms | Example |
|-------|-------------|---------|
| Pre-duel (courtesy) | các hạ, mời | "Các hạ, mời." |
| Active combat (challenge) | ngươi, ngươi hả | "Ngươi giấu chiêu!" |
| Desperate (survival) | tên khốn | "...Tên khốn!" |

### Factor 7: Name at Emotional Peaks

Ask: "Is this an emotional peak?"

At moments of high emotion (betrayal, confession, death, extreme danger), pronouns are often replaced with the person's actual name. This adds intensity.

| Context | Normal | Peak |
|--------|--------|------|
| Warning | "Sư muội cẩn thận." | **"Linh Nhi, lùi lại!"** |
| Betrayal | "Ngươi..." | **"Trí Vĩ, tại sao?!"** |
| Confession | "Ta thích..." | **"Minh Khang, ta yêu ngươi."** |

---

## Reasoning Process

When writing dialogue, follow this reasoning:

```
1. What is the time period/genre of this story?
   → This sets the BASE for what's natural

2. What is this character's background?
   → This shapes their natural speech patterns

3. Who has power in this moment?
   → This determines dominant vs submissive forms

4. What is the relationship between these two?
   → This determines formality level and intimacy

5. What is this character REALLY feeling?
   → This may shift pronouns for emotional effect

6. What phase of combat is this (if applicable)?
   → This shifts pronouns during action scenes

7. Is this an emotional peak moment?
   → If yes, consider using name instead of pronoun
```

---

## Examples of Context-Based Selection

### Example 1: Modern Isekai Character
**Context:** Modern high school student transmigrated to fantasy world
**Character:** Casual personality, modern education
**Natural form:** tớ - cậu (modern Vietnamese)
**Why:** Background is modern, so speech is modern regardless of setting

### Example 2: Period Drama - Sworn Brothers
**Context:** Two swordsmen who swore brotherhood in martial arts world
**Characters:** Wanderers from martial tradition, equal skill
**Natural form:** huynh - đệ
**Why:** Brotherhood arc + martial tradition + equals

### Example 3: Palace Drama - Emperor addressing servant
**Context:** Emperor in palace setting
**Character:** Royal, commanding authority
**Natural form:** trẫm addressing servant
**Why:** Royal tradition + absolute authority

### Example 4: Wuxia - Sect master disciplining disciple
**Context:** Sect master correcting a disciple's mistake
**Character:** Authority figure, formal training
**Natural form:** bổn tọa - ngươi
**Why:** Power dynamic (master > disciple) + formal tradition

### Example 5: Breaking relationship
**Context:** Two former brothers, one betrayed the other
**Before betrayal:** huynh - đệ
**After betrayal:** [tên thật]
**Why:** Relationship arc changed dramatically

---

## What NOT to Do

❌ **DON'T** use static tables like "sword wanderer → ta/ngươi"
❌ **DON'T** apply "mày/tao for all close friends" universally
❌ **DON'T** use feudal forms for modern characters just because setting is fantasy

✅ **DO** ask: "What would this person naturally say?"
✅ **DO** let time period/genre be the primary factor
✅ **DO** consider all context factors together
✅ **DO** use name at emotional peaks

---

## Integration with Other Files

This file works with:
- `STYLE_GUIDE_VN.md` - Main style reference (Section 13.5 updated)
- `agents/ooc-checker.md` - OOC validation using these factors
- `agents/context-agent.md` - Context inference adding time period as primary
- `skills/wordsmith-write/references/writing/dialogue-writing.md` - Reasoning prompts for writers

---

*Updated: 2026-04-22*
*System: Context-only pronoun inference (no static tables)*
