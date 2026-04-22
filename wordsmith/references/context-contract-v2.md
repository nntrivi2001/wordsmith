# Context Contract

## Purpose
- Provide a unified, sortable, and traceable context contract for `Context Agent`, `Writer`, and `Review`.
- Enhance context stability and hit-rate without breaking existing callers.

## Output Structure
- Root fields remain compatible: `meta`, `sections`, `template`, `weights`.
- `meta` additions:
  - `context_contract_version`: fixed as `v2`
  - `ranker`: snapshot of current ranker configuration (for reproducibility)

## Section Ordering Rules
- `core.recent_summaries`
  - Primarily sorted by chapter recency (most recent = highest rank)
  - Extra score boost when "hook / suspense / twist / conflict" cues are present
- `core.recent_meta`
  - Primarily sorted by chapter recency
  - Entries with a `hook` are prioritized
- `scene.appearing_characters`
  - Sorted by combined recency + appearance frequency
  - Entries with `warning` (e.g., pending invalid) are down-ranked
- `story_skeleton`
  - Recency-first, balanced against summary information density
- `alerts`
  - `critical/high` items or entries containing critical risk keywords are prioritized

## Phase B Extensions
- `reader_signal`
  - Aggregates reader-retention metadata from recent chapters (hooks / cool-points / micro-payoffs)
  - Aggregates pattern usage statistics over the recent window (`pattern_usage` / `hook_type_usage`)
  - Aggregates review trends and low-score ranges (`review_trend` / `low_score_ranges`)
- `genre_profile`
  - Automatically selects genre strategy snippets based on `state.json -> project.genre`
  - References `${CLAUDE_PLUGIN_ROOT}/references/genre-profiles.md` and `${CLAUDE_PLUGIN_ROOT}/references/reading-power-taxonomy.md`
  - Outputs `reference_hints` for quick execution by the Writer

## Phase C Extensions
- `writing_guidance`
  - Generates chapter-level execution guidance based on `reader_signal` + `genre_profile`
  - Prioritizes low-score range fixes, hook diversification, cool-point pattern optimization, and genre anchoring
  - Outputs `guidance_items` and `signals_used`

## Compact Text Strategy
- When a section exceeds its budget, text is compacted with head + truncation marker + tail
- Truncation marker is fixed as `…[TRUNCATED]`
- The original `content` structure is preserved; `text` is used for fast model context injection

## Compatibility Constraints
- Existing key names and field semantics are not changed.
- Only list ordering is adjusted; content is not deleted or modified (aside from existing filter logic).
- Callers that ignore `meta.context_contract_version` behave equivalently to v1.

## Recommended Call Points
- `Context Agent` calls this when aggregating context in Step 1.
- `webnovel-write` and `webnovel-review` call this at the start of each run.
- Recovery workflow (`webnovel-resume`) calls this to rebuild context after `detect`.

## Configuration Options (DataModulesConfig)
- `context_ranker_enabled`
- `context_ranker_recency_weight`
- `context_ranker_frequency_weight`
- `context_ranker_hook_bonus`
- `context_ranker_length_bonus_cap`
- `context_ranker_alert_critical_keywords`
- `context_ranker_debug`

Phase B:
- `context_reader_signal_enabled`
- `context_reader_signal_recent_limit`
- `context_reader_signal_window_chapters`
- `context_reader_signal_review_window`
- `context_reader_signal_include_debt`
- `context_genre_profile_enabled`
- `context_genre_profile_max_refs`
- `context_genre_profile_fallback`

Phase C:
- `context_compact_text_enabled`
- `context_compact_min_budget`
- `context_compact_head_ratio`
- `context_writing_guidance_enabled`
- `context_writing_guidance_max_items`
- `context_writing_guidance_low_score_threshold`
- `context_writing_guidance_hook_diversify`

Phase E:
- `context_writing_checklist_enabled`
- `context_writing_checklist_min_items`
- `context_writing_checklist_max_items`
- `context_writing_checklist_default_weight`

Phase F:
- `context_writing_score_persist_enabled`
- `context_writing_score_include_reader_trend`
- `context_writing_score_trend_window`
- `writing_guidance.checklist_score` writes to `index.db -> writing_checklist_scores`

Phase H:
- `context_dynamic_budget_enabled`
- `context_dynamic_budget_early_chapter`
- `context_dynamic_budget_late_chapter`
- New field `meta.context_weight_stage` (early/mid/late)

Phase I:
- `context_genre_profile_support_composite`
- `context_genre_profile_max_genres`
- `context_genre_profile_separators`
- New fields `genre_profile.genres/composite/composite_hints`