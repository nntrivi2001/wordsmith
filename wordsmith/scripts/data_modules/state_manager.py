#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
State Manager - State Management Module (v5.4)

Manages state.json read/write operations:
- Entity state management
- Progress tracking
- Relationship recording

v5.1 changes (continued in v5.4):
- Integrated SQLStateManager, synchronized writes to SQLite (index.db)
- state.json retains lean data, large data automatically migrated to SQLite
"""

import json
import logging
import sys
import time
from copy import deepcopy
from pathlib import Path

from runtime_compat import enable_windows_utf8_stdio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
import filelock

from .config import get_config
from .observability import safe_append_perf_timing, safe_log_tool_call


logger = logging.getLogger(__name__)

try:
    # When scripts directory is in sys.path (common: running from scripts/)
    from security_utils import atomic_write_json, read_json_safe
except ImportError:  # pragma: no cover
    # When running via `python -m scripts.data_modules...` from repo root
    from scripts.security_utils import atomic_write_json, read_json_safe


@dataclass
class EntityState:
    """Entity state"""
    id: str
    name: str
    type: str  # character/location/item/faction
    tier: str = "decor"  # core/important/minor/decor
    aliases: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)
    first_appearance: int = 0
    last_appearance: int = 0


@dataclass
class Relationship:
    """Entity relationship"""
    from_entity: str
    to_entity: str
    type: str
    description: str
    chapter: int


@dataclass
class StateChange:
    """State change record"""
    entity_id: str
    field: str
    old_value: Any
    new_value: Any
    reason: str
    chapter: int
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class _EntityPatch:
    """Entity incremental patch pending write (for merge within lock)"""
    entity_type: str
    entity_id: str
    replace: bool = False
    base_entity: Optional[Dict[str, Any]] = None  # Full snapshot for new entity (used to fill missing fields)
    top_updates: Dict[str, Any] = field(default_factory=dict)
    current_updates: Dict[str, Any] = field(default_factory=dict)
    appearance_chapter: Optional[int] = None


class StateManager:
    """State manager (v5.1 entities_v3 format + SQLite sync, v5.4 continues)"""

    # Entity types introduced in v5.0
    ENTITY_TYPES = ["character", "location", "item", "faction", "skill"]

    def __init__(self, config=None, enable_sqlite_sync: bool = True):
        """
        Initialize state manager

        Parameters:
        - config: Configuration object
        - enable_sqlite_sync: Whether to enable SQLite sync (default True)
        """
        self.config = config or get_config()
        self._state: Dict[str, Any] = {}
        # Consistent with security_utils.atomic_write_json: state.json.lock
        self._lock_path = self.config.state_file.with_suffix(self.config.state_file.suffix + ".lock")

        # v5.1 introduced: SQLite sync
        self._enable_sqlite_sync = enable_sqlite_sync
        self._sql_state_manager = None
        if enable_sqlite_sync:
            try:
                from .sql_state_manager import SQLStateManager
                self._sql_state_manager = SQLStateManager(self.config)
            except ImportError:
                pass  # Silent degradation when SQLStateManager is unavailable

        # Increments pending write (re-read + merge + write within lock)
        self._pending_entity_patches: Dict[tuple[str, str], _EntityPatch] = {}
        self._pending_alias_entries: Dict[str, List[Dict[str, str]]] = {}
        self._pending_state_changes: List[Dict[str, Any]] = []
        self._pending_structured_relationships: List[Dict[str, Any]] = []
        self._pending_disambiguation_warnings: List[Dict[str, Any]] = []
        self._pending_disambiguation_pending: List[Dict[str, Any]] = []
        self._pending_progress_chapter: Optional[int] = None
        self._pending_progress_words_delta: int = 0
        self._pending_chapter_meta: Dict[str, Any] = {}

        # v5.1 introduced: Cache data pending sync to SQLite
        self._pending_sqlite_data: Dict[str, Any] = {
            "entities_appeared": [],
            "entities_new": [],
            "state_changes": [],
            "relationships_new": [],
            "chapter": None
        }

        self._load_state()

    def _now_progress_timestamp(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _ensure_state_schema(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure state.json has required fields for running (try not to destroy existing data)."""
        if not isinstance(state, dict):
            state = {}

        state.setdefault("project_info", {})
        state.setdefault("progress", {})
        state.setdefault("protagonist_state", {})

        # relationships: Old version may be list (entity relationships), v5.0 runtime uses dict (character relationships/important relationships)
        relationships = state.get("relationships")
        if isinstance(relationships, list):
            state.setdefault("structured_relationships", [])
            if isinstance(state.get("structured_relationships"), list):
                state["structured_relationships"].extend(relationships)
            state["relationships"] = {}
        elif not isinstance(relationships, dict):
            state["relationships"] = {}

        state.setdefault("world_settings", {"power_system": [], "factions": [], "locations": []})
        state.setdefault("plot_threads", {"active_threads": [], "foreshadowing": []})
        state.setdefault("review_checkpoints", [])
        state.setdefault("chapter_meta", {})
        state.setdefault(
            "strand_tracker",
            {
                "last_quest_chapter": 0,
                "last_fire_chapter": 0,
                "last_constellation_chapter": 0,
                "current_dominant": "quest",
                "chapters_since_switch": 0,
                "history": [],
            },
        )

        entities_v3 = state.get("entities_v3")
        # v5.1 introduced: entities_v3, alias_index, state_changes, structured_relationships migrated to index.db
        # No longer initializing or maintaining these fields in state.json

        if not isinstance(state.get("disambiguation_warnings"), list):
            state["disambiguation_warnings"] = []

        if not isinstance(state.get("disambiguation_pending"), list):
            state["disambiguation_pending"] = []

        # progress base fields
        progress = state["progress"]
        if not isinstance(progress, dict):
            progress = {}
            state["progress"] = progress
        progress.setdefault("current_chapter", 0)
        progress.setdefault("total_words", 0)
        progress.setdefault("last_updated", self._now_progress_timestamp())

        return state

    def _load_state(self):
        """Load state file"""
        if self.config.state_file.exists():
            self._state = read_json_safe(self.config.state_file, default={})
            self._state = self._ensure_state_schema(self._state)
        else:
            self._state = self._ensure_state_schema({})

    def save_state(self):
        """
        Save state file (re-read + merge + atomic write within lock).

        Solves "read-modify-write overwrite" risk under multi-Agent parallelism:
        - Acquire lock
        - Re-read latest state.json from disk
        - Only merge increments generated by this instance (pending_*)
        - Atomic write
        """
        # Don't write when no increment, avoid meaningless overwrite
        has_pending = any(
            [
                self._pending_entity_patches,
                self._pending_alias_entries,
                self._pending_state_changes,
                self._pending_structured_relationships,
                self._pending_disambiguation_warnings,
                self._pending_disambiguation_pending,
                self._pending_chapter_meta,
                self._pending_progress_chapter is not None,
                self._pending_progress_words_delta != 0,
            ]
        )
        if not has_pending:
            return

        self.config.ensure_dirs()

        lock = filelock.FileLock(str(self._lock_path), timeout=10)
        try:
            with lock:
                disk_state = read_json_safe(self.config.state_file, default={})
                disk_state = self._ensure_state_schema(disk_state)

                # progress (merge as max(chapter) + words_delta accumulation)
                if self._pending_progress_chapter is not None or self._pending_progress_words_delta != 0:
                    progress = disk_state.get("progress", {})
                    if not isinstance(progress, dict):
                        progress = {}
                        disk_state["progress"] = progress

                    try:
                        current_chapter = int(progress.get("current_chapter", 0) or 0)
                    except (TypeError, ValueError):
                        current_chapter = 0

                    if self._pending_progress_chapter is not None:
                        progress["current_chapter"] = max(current_chapter, int(self._pending_progress_chapter))

                    if self._pending_progress_words_delta:
                        try:
                            total_words = int(progress.get("total_words", 0) or 0)
                        except (TypeError, ValueError):
                            total_words = 0
                        progress["total_words"] = total_words + int(self._pending_progress_words_delta)

                    progress["last_updated"] = self._now_progress_timestamp()

                # v5.1 introduced: Force SQLite mode, remove large data fields
                # Ensure these bloated fields do not exist in state.json
                for field in ["entities_v3", "alias_index", "state_changes", "structured_relationships"]:
                    disk_state.pop(field, None)
                # Mark as migrated
                disk_state["_migrated_to_sqlite"] = True

                # disambiguation_warnings (append dedup + truncate)
                if self._pending_disambiguation_warnings:
                    warnings_list = disk_state.get("disambiguation_warnings")
                    if not isinstance(warnings_list, list):
                        warnings_list = []
                        disk_state["disambiguation_warnings"] = warnings_list

                    def _warn_key(w: Dict[str, Any]) -> tuple:
                        return (
                            w.get("chapter"),
                            w.get("mention"),
                            w.get("chosen_id"),
                            w.get("confidence"),
                        )

                    existing_keys = {_warn_key(w) for w in warnings_list if isinstance(w, dict)}
                    for w in self._pending_disambiguation_warnings:
                        if not isinstance(w, dict):
                            continue
                        k = _warn_key(w)
                        if k in existing_keys:
                            continue
                        warnings_list.append(w)
                        existing_keys.add(k)

                    # Only keep recent N entries, avoid file growing indefinitely
                    max_keep = self.config.max_disambiguation_warnings
                    if len(warnings_list) > max_keep:
                        disk_state["disambiguation_warnings"] = warnings_list[-max_keep:]

                # disambiguation_pending (append dedup + truncate)
                if self._pending_disambiguation_pending:
                    pending_list = disk_state.get("disambiguation_pending")
                    if not isinstance(pending_list, list):
                        pending_list = []
                        disk_state["disambiguation_pending"] = pending_list

                    def _pending_key(w: Dict[str, Any]) -> tuple:
                        return (
                            w.get("chapter"),
                            w.get("mention"),
                            w.get("suggested_id"),
                            w.get("confidence"),
                        )

                    existing_keys = {_pending_key(w) for w in pending_list if isinstance(w, dict)}
                    for w in self._pending_disambiguation_pending:
                        if not isinstance(w, dict):
                            continue
                        k = _pending_key(w)
                        if k in existing_keys:
                            continue
                        pending_list.append(w)
                        existing_keys.add(k)

                    max_keep = self.config.max_disambiguation_pending
                    if len(pending_list) > max_keep:
                        disk_state["disambiguation_pending"] = pending_list[-max_keep:]

                # chapter_meta (new: overwrite write by chapter number)
                if self._pending_chapter_meta:
                    chapter_meta = disk_state.get("chapter_meta")
                    if not isinstance(chapter_meta, dict):
                        chapter_meta = {}
                        disk_state["chapter_meta"] = chapter_meta
                    chapter_meta.update(self._pending_chapter_meta)

                # Atomic write (lock already held, no second lock)
                atomic_write_json(self.config.state_file, disk_state, use_lock=False, backup=True)

                # v5.1 introduced: Sync to SQLite (retain pending on failure for retry)
                sqlite_pending_snapshot = self._snapshot_sqlite_pending()
                sqlite_sync_ok = self._sync_to_sqlite()

                # Sync memory as latest disk snapshot
                self._state = disk_state

                # state.json side pending already written to disk, clear directly
                self._pending_disambiguation_warnings.clear()
                self._pending_disambiguation_pending.clear()
                self._pending_chapter_meta.clear()
                self._pending_progress_chapter = None
                self._pending_progress_words_delta = 0

                # SQLite side pending: clear on success, restore snapshot on failure (avoid silent data loss)
                if sqlite_sync_ok:
                    self._pending_entity_patches.clear()
                    self._pending_alias_entries.clear()
                    self._pending_state_changes.clear()
                    self._pending_structured_relationships.clear()
                    self._clear_pending_sqlite_data()
                else:
                    self._restore_sqlite_pending(sqlite_pending_snapshot)

        except filelock.Timeout:
            raise RuntimeError("Unable to acquire state.json file lock, please retry later")

    def _sync_to_sqlite(self) -> bool:
        """Sync pending data to SQLite (v5.1 introduced, v5.4 continues)"""
        if not self._sql_state_manager:
            return True

        # Method 1: Data collected via process_chapter_result
        sqlite_data = self._pending_sqlite_data
        chapter = sqlite_data.get("chapter")

        # Record processed (entity_id, chapter) combinations to avoid duplicate writes to appearances
        processed_appearances = set()

        if chapter is not None:
            try:
                self._sql_state_manager.process_chapter_entities(
                    chapter=chapter,
                    entities_appeared=sqlite_data.get("entities_appeared", []),
                    entities_new=sqlite_data.get("entities_new", []),
                    state_changes=sqlite_data.get("state_changes", []),
                    relationships_new=sqlite_data.get("relationships_new", [])
                )
                # Mark processed appearance records
                for entity in sqlite_data.get("entities_appeared", []):
                    if entity.get("id"):
                        processed_appearances.add((entity.get("id"), chapter))
                for entity in sqlite_data.get("entities_new", []):
                    eid = entity.get("suggested_id") or entity.get("id")
                    if eid:
                        processed_appearances.add((eid, chapter))
            except Exception as exc:
                logger.warning("SQLite sync failed (process_chapter_entities): %s", exc)
                return False

        # Method 2: Incremental data collected via add_entity/update_entity.
        # Data cached in _pending_entity_patches and other variables.
        return self._sync_pending_patches_to_sqlite(processed_appearances)

    def _sync_pending_patches_to_sqlite(self, processed_appearances: set = None) -> bool:
        """Sync _pending_entity_patches etc. to SQLite (v5.1 introduced, v5.4 continues)

        Args:
            processed_appearances: Set of (entity_id, chapter) already processed via process_chapter_entities,
                                   used to avoid duplicate writes to appearances table (prevent overwriting mentions)
        """
        if not self._sql_state_manager:
            return True

        if processed_appearances is None:
            processed_appearances = set()

        # Metadata fields (should not write to current_json)
        METADATA_FIELDS = {"canonical_name", "tier", "desc", "is_protagonist", "is_archived"}

        try:
            from .sql_state_manager import EntityData
            from .index_manager import EntityMeta

            # Sync entity patches
            for (entity_type, entity_id), patch in self._pending_entity_patches.items():
                if patch.base_entity:
                    # New entity
                    entity_data = EntityData(
                        id=entity_id,
                        type=entity_type,
                        name=patch.base_entity.get("canonical_name", entity_id),
                        tier=patch.base_entity.get("tier", "decor"),
                        desc=patch.base_entity.get("desc", ""),
                        current=patch.base_entity.get("current", {}),
                        aliases=[],
                        first_appearance=patch.base_entity.get("first_appearance", 0),
                        last_appearance=patch.base_entity.get("last_appearance", 0),
                        is_protagonist=patch.base_entity.get("is_protagonist", False)
                    )
                    self._sql_state_manager.upsert_entity(entity_data)

                    # Record first appearance (skip already processed to avoid overwriting mentions)
                    if patch.appearance_chapter is not None:
                        if (entity_id, patch.appearance_chapter) not in processed_appearances:
                            self._sql_state_manager._index_manager.record_appearance(
                                entity_id=entity_id,
                                chapter=patch.appearance_chapter,
                                mentions=[entity_data.name],
                                confidence=1.0,
                                skip_if_exists=True  # Key: don't overwrite existing record
                            )
                else:
                    # Update existing entity
                    has_metadata_updates = bool(patch.top_updates and
                                                 any(k in METADATA_FIELDS for k in patch.top_updates))

                    # Non-metadata top_updates should be treated as current updates
                    # For example: realm, layer, location and other state fields
                    non_metadata_top_updates = {
                        k: v for k, v in patch.top_updates.items()
                        if k not in METADATA_FIELDS
                    } if patch.top_updates else {}

                    # Merge current_updates and non-metadata top_updates
                    effective_current_updates = {**non_metadata_top_updates}
                    if patch.current_updates:
                        effective_current_updates.update(patch.current_updates)

                    if has_metadata_updates:
                        # Has metadata updates: use upsert_entity(update_metadata=True)
                        existing = self._sql_state_manager.get_entity(entity_id)
                        if existing:
                            # Merge current
                            current = existing.get("current_json", {})
                            if isinstance(current, str):
                                import json
                                current = json.loads(current) if current else {}
                            if effective_current_updates:
                                current.update(effective_current_updates)

                            new_canonical_name = patch.top_updates.get("canonical_name")
                            old_canonical_name = existing.get("canonical_name", "")

                            entity_meta = EntityMeta(
                                id=entity_id,
                                type=existing.get("type", entity_type),
                                canonical_name=new_canonical_name or old_canonical_name,
                                tier=patch.top_updates.get("tier", existing.get("tier", "decor")),
                                desc=patch.top_updates.get("desc", existing.get("desc", "")),
                                current=current,
                                first_appearance=existing.get("first_appearance", 0),
                                last_appearance=patch.appearance_chapter or existing.get("last_appearance", 0),
                                is_protagonist=patch.top_updates.get("is_protagonist", existing.get("is_protagonist", False)),
                                is_archived=patch.top_updates.get("is_archived", existing.get("is_archived", False))
                            )
                            self._sql_state_manager._index_manager.upsert_entity(entity_meta, update_metadata=True)

                            # If canonical_name renamed, automatically register new name as alias
                            if new_canonical_name and new_canonical_name != old_canonical_name:
                                self._sql_state_manager.register_alias(
                                    new_canonical_name, entity_id, existing.get("type", entity_type)
                                )
                    elif effective_current_updates:
                        # Only has current updates (including non-metadata top_updates)
                        self._sql_state_manager.update_entity_current(entity_id, effective_current_updates)

                    # Update last_appearance and record appearance
                    if patch.appearance_chapter is not None:
                        self._sql_state_manager._update_last_appearance(entity_id, patch.appearance_chapter)
                        # Supplement appearances record
                        # Use skip_if_exists=True to avoid overwriting existing record's mentions
                        if (entity_id, patch.appearance_chapter) not in processed_appearances:
                            self._sql_state_manager._index_manager.record_appearance(
                                entity_id=entity_id,
                                chapter=patch.appearance_chapter,
                                mentions=[],
                                confidence=1.0,
                                skip_if_exists=True  # Key: don't overwrite existing record
                            )

            # Sync aliases
            for alias, entries in self._pending_alias_entries.items():
                for entry in entries:
                    entity_type = entry.get("type")
                    entity_id = entry.get("id")
                    if entity_type and entity_id:
                        self._sql_state_manager.register_alias(alias, entity_id, entity_type)

            # Sync state changes
            for change in self._pending_state_changes:
                self._sql_state_manager.record_state_change(
                    entity_id=change.get("entity_id", ""),
                    field=change.get("field", ""),
                    old_value=change.get("old", change.get("old_value", "")),
                    new_value=change.get("new", change.get("new_value", "")),
                    reason=change.get("reason", ""),
                    chapter=change.get("chapter", 0)
                )

            # Sync relationships
            for rel in self._pending_structured_relationships:
                self._sql_state_manager.upsert_relationship(
                    from_entity=rel.get("from_entity", ""),
                    to_entity=rel.get("to_entity", ""),
                    type=rel.get("type", "meeting"),
                    description=rel.get("description", ""),
                    chapter=rel.get("chapter", 0)
                )

            return True

        except Exception as e:
            # Log warning when SQLite sync fails (don't interrupt main flow)
            logger.warning("SQLite sync failed: %s", e)
            return False

    def _snapshot_sqlite_pending(self) -> Dict[str, Any]:
        """Capture SQLite side pending snapshot for sync failure rollback memory queue."""
        return {
            "entity_patches": deepcopy(self._pending_entity_patches),
            "alias_entries": deepcopy(self._pending_alias_entries),
            "state_changes": deepcopy(self._pending_state_changes),
            "structured_relationships": deepcopy(self._pending_structured_relationships),
            "sqlite_data": deepcopy(self._pending_sqlite_data),
        }

    def _restore_sqlite_pending(self, snapshot: Dict[str, Any]) -> None:
        """Restore SQLite side pending snapshot to avoid data loss after sync failure."""
        self._pending_entity_patches = snapshot.get("entity_patches", {})
        self._pending_alias_entries = snapshot.get("alias_entries", {})
        self._pending_state_changes = snapshot.get("state_changes", [])
        self._pending_structured_relationships = snapshot.get("structured_relationships", [])
        self._pending_sqlite_data = snapshot.get("sqlite_data", {
            "entities_appeared": [],
            "entities_new": [],
            "state_changes": [],
            "relationships_new": [],
            "chapter": None,
        })

    def _clear_pending_sqlite_data(self):
        """Clear pending SQLite data"""
        self._pending_sqlite_data = {
            "entities_appeared": [],
            "entities_new": [],
            "state_changes": [],
            "relationships_new": [],
            "chapter": None
        }

    # ==================== Progress Management ====================

    def get_current_chapter(self) -> int:
        """Get current chapter number"""
        return self._state.get("progress", {}).get("current_chapter", 0)

    def update_progress(self, chapter: int, words: int = 0):
        """Update progress"""
        if "progress" not in self._state:
            self._state["progress"] = {}
        self._state["progress"]["current_chapter"] = chapter
        if words > 0:
            total = self._state["progress"].get("total_words", 0)
            self._state["progress"]["total_words"] = total + words

        # Record increment: use max(chapter) + words_delta accumulation within lock
        if self._pending_progress_chapter is None:
            self._pending_progress_chapter = chapter
        else:
            self._pending_progress_chapter = max(self._pending_progress_chapter, chapter)
        if words > 0:
            self._pending_progress_words_delta += int(words)

    # ==================== Entity Management (v5.1 SQLite-first) ====================

    def get_entity(self, entity_id: str, entity_type: str = None) -> Optional[Dict]:
        """Get entity (v5.1 introduced: prefer reading from SQLite)"""
        # v5.1 introduced: prefer reading from SQLite
        if self._sql_state_manager:
            entity = self._sql_state_manager._index_manager.get_entity(entity_id)
            if entity:
                return entity

        # Fallback to memory state (compatible with unmigrated scenario)
        entities_v3 = self._state.get("entities_v3", {})
        if entity_type:
            return entities_v3.get(entity_type, {}).get(entity_id)

        # Traverse all types to find
        for type_name, entities in entities_v3.items():
            if entity_id in entities:
                return entities[entity_id]
        return None

    def get_entity_type(self, entity_id: str) -> Optional[str]:
        """Get entity's type"""
        # v5.1 introduced: prefer reading from SQLite
        if self._sql_state_manager:
            entity = self._sql_state_manager._index_manager.get_entity(entity_id)
            if entity:
                return entity.get("type")

        # Fallback to memory state
        for type_name, entities in self._state.get("entities_v3", {}).items():
            if entity_id in entities:
                return type_name
        return None

    def get_all_entities(self) -> Dict[str, Dict]:
        """Get all entities (flattened view)"""
        # v5.1 introduced: prefer reading from SQLite
        if self._sql_state_manager:
            result = {}
            for entity_type in self.ENTITY_TYPES:
                entities = self._sql_state_manager._index_manager.get_entities_by_type(entity_type)
                for e in entities:
                    eid = e.get("id")
                    if eid:
                        result[eid] = {**e, "type": entity_type}
            if result:
                return result

        # Fallback to memory state
        result = {}
        for type_name, entities in self._state.get("entities_v3", {}).items():
            for eid, e in entities.items():
                result[eid] = {**e, "type": type_name}
        return result

    def get_entities_by_type(self, entity_type: str) -> Dict[str, Dict]:
        """Get entities by type"""
        # v5.1 introduced: prefer reading from SQLite
        if self._sql_state_manager:
            entities = self._sql_state_manager._index_manager.get_entities_by_type(entity_type)
            if entities:
                return {e.get("id"): e for e in entities if e.get("id")}

        # Fallback to memory state
        return self._state.get("entities_v3", {}).get(entity_type, {})

    def get_entities_by_tier(self, tier: str) -> Dict[str, Dict]:
        """Get entities by tier"""
        # v5.1 introduced: prefer reading from SQLite
        if self._sql_state_manager:
            result = {}
            for entity_type in self.ENTITY_TYPES:
                entities = self._sql_state_manager._index_manager.get_entities_by_tier(tier)
                for e in entities:
                    eid = e.get("id")
                    if eid and e.get("type") == entity_type:
                        result[eid] = {**e, "type": entity_type}
            if result:
                return result

        # Fallback to memory state
        result = {}
        for type_name, entities in self._state.get("entities_v3", {}).items():
            for eid, e in entities.items():
                if e.get("tier") == tier:
                    result[eid] = {**e, "type": type_name}
        return result

    def add_entity(self, entity: EntityState) -> bool:
        """Add new entity (v5.0 entities_v3 format, v5.4 continues)"""
        entity_type = entity.type
        if entity_type not in self.ENTITY_TYPES:
            entity_type = "character"

        if "entities_v3" not in self._state:
            self._state["entities_v3"] = {t: {} for t in self.ENTITY_TYPES}

        if entity_type not in self._state["entities_v3"]:
            self._state["entities_v3"][entity_type] = {}

        # Check if already exists
        if entity.id in self._state["entities_v3"][entity_type]:
            return False

        # Convert to v3 format
        v3_entity = {
            "canonical_name": entity.name,
            "tier": entity.tier,
            "desc": "",
            "current": entity.attributes,
            "first_appearance": entity.first_appearance,
            "last_appearance": entity.last_appearance,
            "history": []
        }
        self._state["entities_v3"][entity_type][entity.id] = v3_entity

        # Record entity patch (new: only fill missing fields to avoid overwriting concurrent writes)
        patch = self._pending_entity_patches.get((entity_type, entity.id))
        if patch is None:
            patch = _EntityPatch(entity_type=entity_type, entity_id=entity.id)
            self._pending_entity_patches[(entity_type, entity.id)] = patch
        patch.replace = True
        patch.base_entity = v3_entity

        # v5.1 introduced: Register alias to index.db (via SQLStateManager)
        if self._sql_state_manager:
            self._sql_state_manager._index_manager.register_alias(entity.name, entity.id, entity_type)
            for alias in entity.aliases:
                if alias:
                    self._sql_state_manager._index_manager.register_alias(alias, entity.id, entity_type)

        return True

    def _register_alias_internal(self, entity_id: str, entity_type: str, alias: str):
        """Internal method: Register alias to index.db (v5.1 introduced)"""
        if not alias:
            return
        # v5.1 introduced: Write directly to SQLite
        if self._sql_state_manager:
            self._sql_state_manager._index_manager.register_alias(alias, entity_id, entity_type)

    def update_entity(self, entity_id: str, updates: Dict[str, Any], entity_type: str = None) -> bool:
        """Update entity attributes (v5.0 introduced, v5.4 continues)"""
        # v5.1+ SQLite-first:
        # - entity_type may come from SQLite (entities table), but state.json no longer persists entities_v3.
        # - Therefore cannot assume self._state["entities_v3"][type][id] exists (issues7 log had KeyError).
        resolved_type = entity_type or self.get_entity_type(entity_id)
        if not resolved_type:
            return False
        if resolved_type not in self.ENTITY_TYPES:
            resolved_type = "character"

        # Only update memory snapshot when entity exists in memory (don't forcibly create to avoid state.json re-expansion)
        entities_v3 = self._state.get("entities_v3")
        entity = None
        if isinstance(entities_v3, dict):
            bucket = entities_v3.get(resolved_type)
            if isinstance(bucket, dict):
                entity = bucket.get(entity_id)

        # When SQLite is enabled, even if memory entity is missing, record patch to ensure current can incrementally write back to index.db
        patch = None
        if self._sql_state_manager:
            patch = self._pending_entity_patches.get((resolved_type, entity_id))
            if patch is None:
                patch = _EntityPatch(entity_type=resolved_type, entity_id=entity_id)
                self._pending_entity_patches[(resolved_type, entity_id)] = patch

        if entity is None and patch is None:
            return False

        did_any = False
        for key, value in updates.items():
            if key == "attributes" and isinstance(value, dict):
                if entity is not None:
                    if "current" not in entity:
                        entity["current"] = {}
                    entity["current"].update(value)
                if patch is not None:
                    patch.current_updates.update(value)
                did_any = True
            elif key == "current" and isinstance(value, dict):
                if entity is not None:
                    if "current" not in entity:
                        entity["current"] = {}
                    entity["current"].update(value)
                if patch is not None:
                    patch.current_updates.update(value)
                did_any = True
            else:
                if entity is not None:
                    entity[key] = value
                if patch is not None:
                    patch.top_updates[key] = value
                did_any = True

        return did_any

    def update_entity_appearance(self, entity_id: str, chapter: int, entity_type: str = None):
        """Update entity appearance chapter"""
        if not entity_type:
            entity_type = self.get_entity_type(entity_id)
        if not entity_type:
            return

        entities_v3 = self._state.get("entities_v3")
        if not isinstance(entities_v3, dict):
            entities_v3 = {t: {} for t in self.ENTITY_TYPES}
            self._state["entities_v3"] = entities_v3
        entities_v3.setdefault(entity_type, {})

        entity = entities_v3[entity_type].get(entity_id)
        if entity:
            if entity.get("first_appearance", 0) == 0:
                entity["first_appearance"] = chapter
            entity["last_appearance"] = chapter

            # Record patch: apply first=min(non-zero), last=max within lock
            patch = self._pending_entity_patches.get((entity_type, entity_id))
            if patch is None:
                patch = _EntityPatch(entity_type=entity_type, entity_id=entity_id)
                self._pending_entity_patches[(entity_type, entity_id)] = patch
            if patch.appearance_chapter is None:
                patch.appearance_chapter = chapter
            else:
                patch.appearance_chapter = max(int(patch.appearance_chapter), int(chapter))

    # ==================== State Change Recording ====================

    def record_state_change(
        self,
        entity_id: str,
        field: str,
        old_value: Any,
        new_value: Any,
        reason: str,
        chapter: int
    ):
        """Record state change"""
        if "state_changes" not in self._state:
            self._state["state_changes"] = []

        change = StateChange(
            entity_id=entity_id,
            field=field,
            old_value=old_value,
            new_value=new_value,
            reason=reason,
            chapter=chapter
        )
        change_dict = asdict(change)
        self._state["state_changes"].append(change_dict)
        self._pending_state_changes.append(change_dict)

        # Also update entity attributes
        self.update_entity(entity_id, {"attributes": {field: new_value}})

    def get_state_changes(self, entity_id: Optional[str] = None) -> List[Dict]:
        """Get state change history"""
        changes = self._state.get("state_changes", [])
        if entity_id:
            changes = [c for c in changes if c.get("entity_id") == entity_id]
        return changes

    # ==================== Relationship Management ====================

    def add_relationship(
        self,
        from_entity: str,
        to_entity: str,
        rel_type: str,
        description: str,
        chapter: int
    ):
        """Add relationship"""
        rel = Relationship(
            from_entity=from_entity,
            to_entity=to_entity,
            type=rel_type,
            description=description,
            chapter=chapter
        )

        # v5.0 introduced: Store entity relationships in structured_relationships, avoid conflict with relationships(character relationships dict)
        if "structured_relationships" not in self._state:
            self._state["structured_relationships"] = []
        rel_dict = asdict(rel)
        self._state["structured_relationships"].append(rel_dict)
        self._pending_structured_relationships.append(rel_dict)

    def get_relationships(self, entity_id: Optional[str] = None) -> List[Dict]:
        """Get relationship list"""
        rels = self._state.get("structured_relationships", [])
        if entity_id:
            rels = [
                r for r in rels
                if r.get("from_entity") == entity_id or r.get("to_entity") == entity_id
            ]
        return rels

    # ==================== Batch Operations ====================

    def _record_disambiguation(self, chapter: int, uncertain_items: Any) -> List[str]:
        """
        Record disambiguation feedback to state.json for Writer/Context Agent to perceive risk.

        Convention:
        - >= extraction_confidence_medium: Write to disambiguation_warnings (adopted but warned)
        - < extraction_confidence_medium: Write to disambiguation_pending (needs manual confirmation)
        """
        if not isinstance(uncertain_items, list) or not uncertain_items:
            return []

        warnings: List[str] = []
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for item in uncertain_items:
            if not isinstance(item, dict):
                continue

            mention = str(item.get("mention", "") or "").strip()
            if not mention:
                continue

            raw_conf = item.get("confidence", 0.0)
            try:
                confidence = float(raw_conf)
            except (TypeError, ValueError):
                confidence = 0.0

            # Candidates: supports both [{"type","id"}...] and ["id1","id2"] formats
            candidates_raw = item.get("candidates", [])
            candidates: List[Dict[str, str]] = []
            if isinstance(candidates_raw, list):
                for c in candidates_raw:
                    if isinstance(c, dict):
                        cid = str(c.get("id", "") or "").strip()
                        ctype = str(c.get("type", "") or "").strip()
                        entry: Dict[str, str] = {}
                        if ctype:
                            entry["type"] = ctype
                        if cid:
                            entry["id"] = cid
                        if entry:
                            candidates.append(entry)
                    else:
                        cid = str(c).strip()
                        if cid:
                            candidates.append({"id": cid})

            entity_type = str(item.get("type", "") or "").strip()
            suggested_id = str(item.get("suggested", "") or "").strip()

            adopted_raw = item.get("adopted", None)
            chosen_id = ""
            if isinstance(adopted_raw, str):
                chosen_id = adopted_raw.strip()
            elif adopted_raw is True:
                chosen_id = suggested_id
            else:
                # Compatible field names: entity_id / chosen_id
                chosen_id = str(item.get("entity_id") or item.get("chosen_id") or "").strip() or suggested_id

            context = str(item.get("context", "") or "").strip()
            note = str(item.get("warning", "") or "").strip()

            record: Dict[str, Any] = {
                "chapter": int(chapter),
                "mention": mention,
                "type": entity_type,
                "suggested_id": suggested_id,
                "chosen_id": chosen_id,
                "confidence": confidence,
                "candidates": candidates,
                "context": context,
                "note": note,
                "created_at": now,
            }

            if confidence >= float(self.config.extraction_confidence_medium):
                self._state.setdefault("disambiguation_warnings", []).append(record)
                self._pending_disambiguation_warnings.append(record)
                chosen_part = f" -> {chosen_id}" if chosen_id else ""
                warnings.append(f"Disambiguation warning: {mention}{chosen_part} (confidence: {confidence:.2f})")
            else:
                self._state.setdefault("disambiguation_pending", []).append(record)
                self._pending_disambiguation_pending.append(record)
                warnings.append(f"Disambiguation needs manual confirmation: {mention} (confidence: {confidence:.2f})")

        return warnings

    def process_chapter_result(self, chapter: int, result: Dict) -> List[str]:
        """
        Process Data Agent's chapter processing result (v5.1 introduced, v5.4 continues)

        Input format:
        - entities_appeared: Appearing entity list
        - entities_new: New entity list
        - state_changes: State change list
        - relationships_new: New relationship list

        Returns warning list
        """
        warnings = []

        # v5.1 introduced: Record chapter number for SQLite sync
        self._pending_sqlite_data["chapter"] = chapter

        # Process appearing entities
        for entity in result.get("entities_appeared", []):
            entity_id = entity.get("id")
            entity_type = entity.get("type")
            if entity_id:
                self.update_entity_appearance(entity_id, chapter, entity_type)
                # v5.1 introduced: Cache for SQLite sync
                self._pending_sqlite_data["entities_appeared"].append(entity)

        # Process new entities
        for entity in result.get("entities_new", []):
            entity_id = entity.get("suggested_id") or entity.get("id")
            if entity_id and entity_id != "NEW":
                new_entity = EntityState(
                    id=entity_id,
                    name=entity.get("name", ""),
                    type=entity.get("type", "character"),
                    tier=entity.get("tier", "decor"),
                    aliases=entity.get("mentions", []),
                    first_appearance=chapter,
                    last_appearance=chapter
                )
                if not self.add_entity(new_entity):
                    warnings.append(f"Entity already exists: {entity_id}")
                # v5.1 introduced: Cache for SQLite sync
                self._pending_sqlite_data["entities_new"].append(entity)

        # Process state changes
        for change in result.get("state_changes", []):
            self.record_state_change(
                entity_id=change.get("entity_id", ""),
                field=change.get("field", ""),
                old_value=change.get("old"),
                new_value=change.get("new"),
                reason=change.get("reason", ""),
                chapter=chapter
            )
            # v5.1 introduced: Cache for SQLite sync
            self._pending_sqlite_data["state_changes"].append(change)

        # Process relationships
        for rel in result.get("relationships_new", []):
            self.add_relationship(
                from_entity=rel.get("from", ""),
                to_entity=rel.get("to", ""),
                rel_type=rel.get("type", ""),
                description=rel.get("description", ""),
                chapter=chapter
            )
            # v5.1 introduced: Cache for SQLite sync
            self._pending_sqlite_data["relationships_new"].append(rel)

        # Process disambiguation uncertain items (doesn't affect entity write but must be visible to Writer)
        warnings.extend(self._record_disambiguation(chapter, result.get("uncertain", [])))

        # Write chapter_meta (hook/pattern/end state)
        chapter_meta = result.get("chapter_meta")
        if isinstance(chapter_meta, dict):
            meta_key = f"{int(chapter):04d}"
            self._state.setdefault("chapter_meta", {})
            self._state["chapter_meta"][meta_key] = chapter_meta
            self._pending_chapter_meta[meta_key] = chapter_meta

        # Update progress
        self.update_progress(chapter)

        # Sync protagonist state (entities_v3 -> protagonist_state)
        self.sync_protagonist_from_entity()

        return warnings

    # ==================== Export ====================

    def export_for_context(self) -> Dict:
        """Export lean version state for context (v5.0 introduced, v5.4 continues)"""
        # Build lean view from entities_v3
        entities_flat = {}
        for type_name, entities in self._state.get("entities_v3", {}).items():
            for eid, e in entities.items():
                entities_flat[eid] = {
                    "name": e.get("canonical_name", eid),
                    "type": type_name,
                    "tier": e.get("tier", "decor"),
                    "current": e.get("current", {})
                }

        return {
            "progress": self._state.get("progress", {}),
            "entities": entities_flat,
            # v5.1 introduced: alias_index migrated to index.db, return empty here (compatibility)
            "alias_index": {},
            "recent_changes": [],  # v5.1 introduced: query from index.db
            "disambiguation": {
                "warnings": self._state.get("disambiguation_warnings", [])[-self.config.export_disambiguation_slice:],
                "pending": self._state.get("disambiguation_pending", [])[-self.config.export_disambiguation_slice:],
            },
        }

    # ==================== Protagonist Sync ====================

    def get_protagonist_entity_id(self) -> Optional[str]:
        """Get protagonist entity ID (via is_protagonist flag or SQLite query)"""
        # Method 1: Query via SQLStateManager (v5.1)
        if self._sql_state_manager:
            protagonist = self._sql_state_manager.get_protagonist()
            if protagonist:
                return protagonist.get("id")

        # Method 2: Find alias via protagonist_state.name
        protag_name = self._state.get("protagonist_state", {}).get("name")
        if protag_name and self._sql_state_manager:
            entities = self._sql_state_manager._index_manager.get_entities_by_alias(protag_name)
            for entry in entities:
                if entry.get("type") == "character":
                    return entry.get("id")

        return None

    def sync_protagonist_from_entity(self, entity_id: str = None):
        """
        Sync protagonist entity state to protagonist_state (v5.1: read from SQLite)

        Used to ensure components depending on protagonist_state like consistency-checker get latest data
        """
        if entity_id is None:
            entity_id = self.get_protagonist_entity_id()
        if entity_id is None:
            return

        entity = self.get_entity(entity_id, "character")
        if not entity:
            return

        current = entity.get("current")
        if not isinstance(current, dict):
            current = entity.get("current_json", {})
        if isinstance(current, str):
            try:
                current = json.loads(current) if current else {}
            except (json.JSONDecodeError, TypeError):
                current = {}
        if not isinstance(current, dict):
            current = {}
        protag = self._state.setdefault("protagonist_state", {})

        # Sync realm
        if "realm" in current:
            power = protag.setdefault("power", {})
            power["realm"] = current["realm"]
            if "layer" in current:
                power["layer"] = current["layer"]

        # Sync location
        if "location" in current:
            loc = protag.setdefault("location", {})
            loc["current"] = current["location"]
            if "last_chapter" in current:
                loc["last_chapter"] = current["last_chapter"]

    def sync_protagonist_to_entity(self, entity_id: str = None):
        """
        Sync protagonist_state to protagonist entity in entities_v3

        Used after initialization or manual editing of protagonist_state to maintain consistency
        """
        if entity_id is None:
            entity_id = self.get_protagonist_entity_id()
        if entity_id is None:
            return

        protag = self._state.get("protagonist_state", {})
        if not protag:
            return

        updates = {}

        # Sync realm
        power = protag.get("power", {})
        if power.get("realm"):
            updates["realm"] = power["realm"]
        if power.get("layer"):
            updates["layer"] = power["layer"]

        # Sync location
        loc = protag.get("location", {})
        if loc.get("current"):
            updates["location"] = loc["current"]

        if updates:
            self.update_entity(entity_id, updates, "character")


# ==================== CLI Interface ====================

def main():
    import argparse
    import sys
    from pydantic import ValidationError
    from .cli_output import print_success, print_error
    from .cli_args import normalize_global_project_root, load_json_arg
    from .schemas import validate_data_agent_output, format_validation_error, normalize_data_agent_output
    from .index_manager import IndexManager

    parser = argparse.ArgumentParser(description="State Manager CLI (v5.4)")
    parser.add_argument("--project-root", type=str, help="Project root directory")

    subparsers = parser.add_subparsers(dest="command")

    # Read progress
    subparsers.add_parser("get-progress")

    # Get entity
    get_entity_parser = subparsers.add_parser("get-entity")
    get_entity_parser.add_argument("--id", required=True)

    # List entities
    list_parser = subparsers.add_parser("list-entities")
    list_parser.add_argument("--type", help="Filter by type")
    list_parser.add_argument("--tier", help="Filter by tier")

    # Process chapter result
    process_parser = subparsers.add_parser("process-chapter")
    process_parser.add_argument("--chapter", type=int, required=True, help="Chapter number")
    process_parser.add_argument("--data", required=True, help="Processing result in JSON format")

    argv = normalize_global_project_root(sys.argv[1:])
    args = parser.parse_args(argv)
    command_started_at = time.perf_counter()

    # Initialize
    config = None
    if args.project_root:
        # Allow passing "workspace root directory", resolve to actual book project_root (must contain .wordsmith/state.json)
        from project_locator import resolve_project_root
        from .config import DataModulesConfig

        resolved_root = resolve_project_root(args.project_root)
        config = DataModulesConfig.from_project_root(resolved_root)

    manager = StateManager(config)
    logger = IndexManager(config)
    tool_name = f"state_manager:{args.command or 'unknown'}"

    def _append_timing(success: bool, *, error_code: str | None = None, error_message: str | None = None, chapter: int | None = None):
        elapsed_ms = int((time.perf_counter() - command_started_at) * 1000)
        safe_append_perf_timing(
            manager.config.project_root,
            tool_name=tool_name,
            success=success,
            elapsed_ms=elapsed_ms,
            chapter=chapter,
            error_code=error_code,
            error_message=error_message,
        )

    def emit_success(data=None, message: str = "ok", chapter: int | None = None):
        print_success(data, message=message)
        safe_log_tool_call(logger, tool_name=tool_name, success=True)
        _append_timing(True, chapter=chapter)

    def emit_error(code: str, message: str, suggestion: str | None = None, chapter: int | None = None):
        print_error(code, message, suggestion=suggestion)
        safe_log_tool_call(
            logger,
            tool_name=tool_name,
            success=False,
            error_code=code,
            error_message=message,
        )
        _append_timing(False, error_code=code, error_message=message, chapter=chapter)

    if args.command == "get-progress":
        emit_success(manager._state.get("progress", {}), message="progress")

    elif args.command == "get-entity":
        entity = manager.get_entity(args.id)
        if entity:
            emit_success(entity, message="entity")
        else:
            emit_error("NOT_FOUND", f"Entity not found: {args.id}")

    elif args.command == "list-entities":
        if args.type:
            entities = manager.get_entities_by_type(args.type)
        elif args.tier:
            entities = manager.get_entities_by_tier(args.tier)
        else:
            entities = manager.get_all_entities()

        payload = [{"id": eid, **e} for eid, e in entities.items()]
        emit_success(payload, message="entities")

    elif args.command == "process-chapter":
        data = load_json_arg(args.data)
        validated = None
        last_exc = None
        for _ in range(3):
            try:
                validated = validate_data_agent_output(data)
                break
            except ValidationError as exc:
                last_exc = exc
                data = normalize_data_agent_output(data)
        if validated is None:
            err = format_validation_error(last_exc) if last_exc else {
                "code": "SCHEMA_VALIDATION_FAILED",
                "message": "Data structure validation failed",
                "details": {"errors": []},
                "suggestion": "Please check if data-agent output fields are complete and types are correct",
            }
            emit_error(err["code"], err["message"], suggestion=err.get("suggestion"))
            return

        warnings = manager.process_chapter_result(args.chapter, validated.model_dump(by_alias=True))
        manager.save_state()
        emit_success({"chapter": args.chapter, "warnings": warnings}, message="chapter_processed", chapter=args.chapter)

    else:
        emit_error("UNKNOWN_COMMAND", "No valid command specified", suggestion="Please see --help")


if __name__ == "__main__":
    if sys.platform == "win32":
        enable_windows_utf8_stdio()
    main()
