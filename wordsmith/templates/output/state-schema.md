# state.json Structure Reference

> This file represents the lean runtime state to prevent size bloat. Large data such as entities is stored in index.db.
>
> The following example is consistent with the fields currently validated by `update_state.py`.

```json
{
  "project_info": {
    "title": "",
    "genre": "",
    "target_words": 0,
    "target_chapters": 0
  },
  "progress": {
    "current_chapter": 0,
    "total_words": 0,
    "last_updated": "",
    "volumes_completed": [],
    "current_volume": 1,
    "volumes_planned": [
      {"volume": 1, "chapters_range": "1-100", "planned_at": "2026-02-01"}
    ]
  },
  "protagonist_state": {
    "name": "",
    "power": {"realm": "", "layer": 0, "bottleneck": ""},
    "location": {"current": "", "last_chapter": 0},
    "golden_finger": {"name": "", "level": 0, "cooldown": 0}
  },
  "relationships": {},
  "world_settings": {
    "power_system": [],
    "factions": [],
    "locations": []
  },
  "review_checkpoints": [
    {"chapters": "1-5", "report": "review-reports/chapters-1-5-review.md", "reviewed_at": "2026-02-26 20:00:00"}
  ],
  "strand_tracker": {
    "last_quest_chapter": 0,
    "last_fire_chapter": 0,
    "last_constellation_chapter": 0,
    "current_dominant": "quest",
    "chapters_since_switch": 0,
    "history": []
  },
  "plot_threads": {
    "active_threads": [],
    "foreshadowing": []
  },
  "disambiguation_warnings": [],
  "disambiguation_pending": [],
  "chapter_meta": {
    "0001": {
      "hook": {"type": "crisis-hook", "content": "...", "strength": "strong"},
      "pattern": {
        "opening": "conflict-opening",
        "hook": "crisis-hook",
        "emotion_rhythm": "low→high",
        "info_density": "medium"
      },
      "ending": {"time": "night", "location": "sect-great-hall", "emotion": "tense"}
    }
  }
}
```
