# index.db Table Structure Reference

> Stores large-scale data (entities, aliases, scenes, relationships) in SQLite.
>
> The current structure includes reading-engagement / observability-related tables.

## Table Overview

### Core Index Tables

### chapters
- chapter (INTEGER, PK)
- title (TEXT)
- location (TEXT)
- word_count (INTEGER)
- characters (TEXT)
- summary (TEXT)
- created_at (TIMESTAMP)

### scenes
- id (INTEGER, PK)
- chapter (INTEGER)
- scene_index (INTEGER)
- start_line (INTEGER)
- end_line (INTEGER)
- location (TEXT)
- summary (TEXT)
- characters (TEXT)

### appearances
- id (INTEGER, PK)
- entity_id (TEXT)
- chapter (INTEGER)
- mentions (TEXT)
- confidence (REAL)

### entities
- id (TEXT, PK)
- type (TEXT)
- canonical_name (TEXT)
- tier (TEXT)
- desc (TEXT)
- current_json (TEXT)
- first_appearance (INTEGER)
- last_appearance (INTEGER)
- is_protagonist (INTEGER)
- is_archived (INTEGER)

### aliases
- alias (TEXT)
- entity_id (TEXT)
- entity_type (TEXT)

### state_changes
- id (INTEGER, PK)
- entity_id (TEXT)
- field (TEXT)
- old_value (TEXT)
- new_value (TEXT)
- reason (TEXT)
- chapter (INTEGER)

### relationships
- id (INTEGER, PK)
- from_entity (TEXT)
- to_entity (TEXT)
- type (TEXT)
- description (TEXT)
- chapter (INTEGER)

### Reading Engagement Debt Tables
- override_contracts
- chase_debt
- debt_events
- chapter_reading_power

### Observability and Review Tables
- invalid_facts
- review_metrics
- rag_query_log
- tool_call_stats
- writing_checklist_scores

> Actual fields and constraints are defined in `.claude/scripts/data_modules/index_manager.py`.
