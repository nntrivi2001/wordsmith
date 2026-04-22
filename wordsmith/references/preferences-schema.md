# preferences.json Design

Used to save user preferences and writing constraints (can be set by `/webnovel-init` or edited manually by users).

## Example

```json
{
  "tone": "passionate",
  "pacing": {
    "chapter_words": 2500,
    "cliffhanger": true
  },
  "style": {
    "dialogue_ratio": 0.35,
    "narration_ratio": 0.65
  },
  "avoid": ["excessive narration", "repeated dialogue"],
  "focus": ["protagonist growth", "battle description"]
}
```

## Field Descriptions
- tone: Global emotional tone (passionate / measured / humorous — see STYLE_GUIDE_VN.md Section 7.3 for tone variations)
- pacing: Pacing preferences
- style: Narration-to-dialogue ratio (see STYLE_GUIDE_VN.md Section 2 for sentence structure patterns)
- avoid: Prohibited elements list
- focus: Directions that must be emphasized

---

## Vietnamese Style Alignment

When configuring preferences, consider Vietnamese webnovel patterns:

| Element | Vietnamese Pattern | Reference |
|---------|------------------|-----------|
| Dialogue ratio | Lower (0.30-0.40) for action, higher (0.40-0.50) for romance | STYLE_GUIDE_VN.md 7.4 |
| Sentence length | Short for action, long for emotional scenes | STYLE_GUIDE_VN.md 2.1, 3.1 |
| Cliffhanger style | Short punchy sentences, open-ended | STYLE_GUIDE_VN.md 6.2 |
| Character voice | Distinct pronoun usage per character | STYLE_GUIDE_VN.md 1.1 |