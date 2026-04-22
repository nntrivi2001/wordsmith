#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQL State Manager - SQLite State Management Module (v5.4)

Extends IndexManager to provide a StateManager-compatible high-level interface,
storing large data (entities, aliases, state changes, relationships) in SQLite
instead of JSON.

Goals (v5.1 introduced, v5.4 continues):
- Replace large data fields in state.json
- Maintain interface compatibility with Data Agent / Context Agent
- Support incremental writes and on-demand queries
"""

import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

from .index_manager import (
    IndexManager,
    EntityMeta,
    StateChangeMeta,
    RelationshipMeta,
    RelationshipEventMeta,
)
from .config import get_config
from .observability import safe_log_tool_call


@dataclass
class EntityData:
    """Entity data (for Data Agent input)"""
    id: str
    type: str  # Character/Location/Item/Faction/Skill
    name: str
    tier: str = "decor"
    desc: str = ""
    current: Dict[str, Any] = field(default_factory=dict)
    aliases: List[str] = field(default_factory=list)
    first_appearance: int = 0
    last_appearance: int = 0
    is_protagonist: bool = False


class SQLStateManager:
    """
    SQLite State Manager (v5.1 introduced, v5.4 continues)

    Provides a StateManager-compatible interface, but data is stored in SQLite (index.db).
    Used to replace bloated data structures in state.json.

    Usage:
    ```python
    manager = SQLStateManager(config)

    # Write entity
    manager.upsert_entity(EntityData(
        id="xiaoyan",
        type="character",
        name="Xiao Yan",
        tier="core",
        current={"realm": "Dou Shi", "location": "Tianyun Sect"},
        aliases=["Xiao Yan", "trash"],  # "trash" = "trash/waste" (disparaging nickname)
        is_protagonist=True
    ))

    # Write state change
    manager.record_state_change(
        entity_id="xiaoyan",
        field="realm",
        old_value="Dou Zhe",
        new_value="Dou Shi",
        reason="breakthrough",
        chapter=100
    )

    # Write relationship
    manager.upsert_relationship(
        from_entity="xiaoyan",
        to_entity="yaolao",
        type="master_disciple",  # "master_disciple" = master-disciple relationship
        description="Master accepts Xiao Yan as disciple",
        chapter=5
    )

    # Read
    protagonist = manager.get_protagonist()
    core_entities = manager.get_core_entities()
    changes = manager.get_recent_state_changes(limit=50)
    ```
    """

    # Entity types introduced in v5.0
    ENTITY_TYPES = ["character", "location", "item", "faction", "skill"]

    def __init__(self, config=None):
        self.config = config or get_config()
        self._index_manager = IndexManager(config)

    # ==================== Entity Operations ====================

    def upsert_entity(self, entity: EntityData) -> bool:
        """
        Insert or update entity

        Automatically handles:
        - Entity basic info writes to entities table
        - Alias writes to aliases table
        - canonical_name automatically added as alias

        Returns: Whether it is a new entity
        """
        # Build EntityMeta
        meta = EntityMeta(
            id=entity.id,
            type=entity.type,
            canonical_name=entity.name,
            tier=entity.tier,
            desc=entity.desc,
            current=entity.current,
            first_appearance=entity.first_appearance,
            last_appearance=entity.last_appearance,
            is_protagonist=entity.is_protagonist,
            is_archived=False
        )

        is_new = self._index_manager.upsert_entity(meta)

        # Register aliases
        # 1. canonical_name itself as alias
        self._index_manager.register_alias(entity.name, entity.id, entity.type)

        # 2. Other aliases
        for alias in entity.aliases:
            if alias and alias != entity.name:
                self._index_manager.register_alias(alias, entity.id, entity.type)

        return is_new

    def get_entity(self, entity_id: str) -> Optional[Dict]:
        """Get entity details"""
        entity = self._index_manager.get_entity(entity_id)
        if entity:
            # Add aliases
            entity["aliases"] = self._index_manager.get_entity_aliases(entity_id)
        return entity

    def get_entities_by_type(self, entity_type: str, include_archived: bool = False) -> List[Dict]:
        """Get entities by type"""
        entities = self._index_manager.get_entities_by_type(entity_type, include_archived)
        for e in entities:
            e["aliases"] = self._index_manager.get_entity_aliases(e["id"])
        return entities

    def get_core_entities(self) -> List[Dict]:
        """
        Get core entities (for Context Agent full load)

        Returns all entities with tier=core/important or is_protagonist=1
        (minor/decor entities queried on-demand, not full-loaded)
        """
        entities = self._index_manager.get_core_entities()
        for e in entities:
            e["aliases"] = self._index_manager.get_entity_aliases(e["id"])
        return entities

    def get_protagonist(self) -> Optional[Dict]:
        """Get protagonist entity"""
        protagonist = self._index_manager.get_protagonist()
        if protagonist:
            protagonist["aliases"] = self._index_manager.get_entity_aliases(protagonist["id"])
        return protagonist

    def update_entity_current(self, entity_id: str, updates: Dict) -> bool:
        """Incrementally update entity's current field"""
        return self._index_manager.update_entity_current(entity_id, updates)

    def resolve_alias(self, alias: str) -> List[Dict]:
        """
        Resolve entity by alias (one-to-many)

        Returns all matching entities
        """
        return self._index_manager.get_entities_by_alias(alias)

    def register_alias(self, alias: str, entity_id: str, entity_type: str) -> bool:
        """Register alias"""
        return self._index_manager.register_alias(alias, entity_id, entity_type)

    # ==================== State Change Operations ====================

    def record_state_change(
        self,
        entity_id: str,
        field: str,
        old_value: Any,
        new_value: Any,
        reason: str,
        chapter: int
    ) -> int:
        """
        Record state change

        Returns: Record ID
        """
        change = StateChangeMeta(
            entity_id=entity_id,
            field=field,
            old_value=str(old_value) if old_value is not None else "",
            new_value=str(new_value),
            reason=reason,
            chapter=chapter
        )
        return self._index_manager.record_state_change(change)

    def get_entity_state_changes(self, entity_id: str, limit: int = 20) -> List[Dict]:
        """Get entity's state change history"""
        return self._index_manager.get_entity_state_changes(entity_id, limit)

    def get_recent_state_changes(self, limit: int = 50) -> List[Dict]:
        """Get recent state changes"""
        return self._index_manager.get_recent_state_changes(limit)

    def get_chapter_state_changes(self, chapter: int) -> List[Dict]:
        """Get all state changes for a chapter"""
        return self._index_manager.get_chapter_state_changes(chapter)

    # ==================== Relationship Operations ====================

    def upsert_relationship(
        self,
        from_entity: str,
        to_entity: str,
        type: str,
        description: str,
        chapter: int
    ) -> bool:
        """
        Insert or update relationship

        Returns: Whether it is a new relationship
        """
        rel = RelationshipMeta(
            from_entity=from_entity,
            to_entity=to_entity,
            type=type,
            description=description,
            chapter=chapter
        )
        return self._index_manager.upsert_relationship(rel)

    def get_entity_relationships(self, entity_id: str, direction: str = "both") -> List[Dict]:
        """Get entity's relationships"""
        return self._index_manager.get_entity_relationships(entity_id, direction)

    def get_relationship_between(self, entity1: str, entity2: str) -> List[Dict]:
        """Get all relationships between two entities"""
        return self._index_manager.get_relationship_between(entity1, entity2)

    def get_recent_relationships(self, limit: int = 30) -> List[Dict]:
        """Get recently established relationships"""
        return self._index_manager.get_recent_relationships(limit)

    # ==================== Batch Write (for Data Agent) ====================

    def process_chapter_entities(
        self,
        chapter: int,
        entities_appeared: List[Dict],
        entities_new: List[Dict],
        state_changes: List[Dict],
        relationships_new: List[Dict]
    ) -> Dict[str, int]:
        """
        Process chapter entity data (Data Agent main entry)

        Parameters:
        - chapter: Chapter number
        - entities_appeared: Already existing entities that appeared
          [{"id": "xiaoyan", "type": "character", "mentions": ["Xiao Yan", "he"], "confidence": 0.95}]
        - entities_new: Newly discovered entities
          [{"suggested_id": "hongyi_girl", "name": "Red-clothed girl", "type": "character", "tier": "decor"}]
        - state_changes: State changes
          [{"entity_id": "xiaoyan", "field": "realm", "old": "Dou Zhe", "new": "Dou Shi", "reason": "breakthrough"}]
        - relationships_new: New relationships
          [{"from": "xiaoyan", "to": "hongyi_girl", "type": "meeting", "description": "first meeting"}]

        Returns: Write statistics
        """
        stats = {
            "entities_updated": 0,
            "entities_created": 0,
            "state_changes": 0,
            "relationships": 0,
            "aliases": 0
        }

        # 1. Process appearing entities (update last_appearance)
        for entity in entities_appeared:
            entity_id = entity.get("id")
            if not entity_id:
                continue

            self._index_manager.update_entity_current(entity_id, {})  # Trigger updated_at
            # Update last_appearance
            existing = self._index_manager.get_entity(entity_id)
            if existing:
                # Use SQL to directly update last_appearance
                self._update_last_appearance(entity_id, chapter)
                stats["entities_updated"] += 1

            # Record appearance (keep original logic)
            self._index_manager.record_appearance(
                entity_id=entity_id,
                chapter=chapter,
                mentions=entity.get("mentions", []),
                confidence=entity.get("confidence", 1.0)
            )

        # 2. Process new entities
        for entity in entities_new:
            suggested_id = entity.get("suggested_id") or entity.get("id")
            if not suggested_id:
                continue

            entity_data = EntityData(
                id=suggested_id,
                type=entity.get("type", "character"),
                name=entity.get("name", suggested_id),
                tier=entity.get("tier", "decor"),
                desc=entity.get("desc", ""),
                current=entity.get("current", {}),
                aliases=entity.get("aliases", []),
                first_appearance=chapter,
                last_appearance=chapter,
                is_protagonist=entity.get("is_protagonist", False)
            )
            is_new = self.upsert_entity(entity_data)
            if is_new:
                stats["entities_created"] += 1
            else:
                stats["entities_updated"] += 1

            # Count aliases
            stats["aliases"] += 1 + len(entity_data.aliases)

            # Record first appearance of new entity (solve appearances missing problem)
            mentions = entity.get("mentions", [])
            if not mentions:
                mentions = [entity_data.name]  # At least contains entity name
            self._index_manager.record_appearance(
                entity_id=suggested_id,
                chapter=chapter,
                mentions=mentions,
                confidence=entity.get("confidence", 1.0)
            )

        # 3. Process state changes
        for change in state_changes:
            entity_id = change.get("entity_id")
            if not entity_id:
                continue

            self.record_state_change(
                entity_id=entity_id,
                field=change.get("field", ""),
                old_value=change.get("old", change.get("old_value", "")),
                new_value=change.get("new", change.get("new_value", "")),
                reason=change.get("reason", ""),
                chapter=chapter
            )
            stats["state_changes"] += 1

            # Sync update entity's current
            field_name = change.get("field")
            new_value = change.get("new", change.get("new_value"))
            # Note: new_value may be 0/""/False etc. falsy values, need to use is not None
            if field_name and new_value is not None:
                self._index_manager.update_entity_current(entity_id, {field_name: new_value})

        # 4. Process new relationships
        for rel in relationships_new:
            from_entity = rel.get("from", rel.get("from_entity"))
            to_entity = rel.get("to", rel.get("to_entity"))
            if not from_entity or not to_entity:
                continue
            rel_type = rel.get("type", "meeting")
            description = rel.get("description", "")

            # v5.5: First record relationship event, then update relationship snapshot
            self._index_manager.record_relationship_event(
                RelationshipEventMeta(
                    from_entity=from_entity,
                    to_entity=to_entity,
                    type=rel_type,
                    chapter=chapter,
                    action=rel.get("action", "update"),
                    polarity=rel.get("polarity", 0),
                    strength=rel.get("strength", 0.5),
                    description=description,
                    scene_index=rel.get("scene_index", 0),
                    evidence=rel.get("evidence", ""),
                    confidence=rel.get("confidence", 1.0),
                )
            )

            self.upsert_relationship(
                from_entity=from_entity,
                to_entity=to_entity,
                type=rel_type,
                description=description,
                chapter=chapter
            )
            stats["relationships"] += 1

        return stats

    def _update_last_appearance(self, entity_id: str, chapter: int):
        """Update entity's last_appearance"""
        with self._index_manager._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE entities SET
                    last_appearance = MAX(last_appearance, ?),
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (chapter, entity_id))
            conn.commit()

    # ==================== Statistics ====================

    def get_stats(self) -> Dict[str, int]:
        """Get statistics"""
        return self._index_manager.get_stats()

    # ==================== Format Conversion (Compatibility) ====================

    def export_to_entities_v3_format(self) -> Dict[str, Dict[str, Dict]]:
        """
        Export to entities_v3 format (for compatibility)

        Returns: {"character": {"xiaoyan": {...}}, "location": {...}, ...}
        """
        result = {t: {} for t in self.ENTITY_TYPES}

        for entity_type in self.ENTITY_TYPES:
            entities = self.get_entities_by_type(entity_type, include_archived=True)
            for e in entities:
                entity_dict = {
                    "canonical_name": e.get("canonical_name"),
                    "name": e.get("canonical_name"),  # Compatibility alias
                    "tier": e.get("tier", "decor"),
                    "aliases": e.get("aliases", []),
                    "desc": e.get("desc", ""),
                    "current": e.get("current_json", {}),
                    "history": [],  # History records need to be queried from state_changes table
                    "first_appearance": e.get("firstappearance", 0),
                    "last_appearance": e.get("lastappearance", 0)
                }
                if e.get("is_protagonist"):
                    entity_dict["is_protagonist"] = True
                result[entity_type][e["id"]] = entity_dict

        return result

    def export_to_alias_index_format(self) -> Dict[str, List[Dict[str, str]]]:
        """
        Export to alias_index format (for compatibility)

        Returns: {"Xiao Yan": [{"type": "character", "id": "xiaoyan"}], ...}
        """
        result = {}

        with self._index_manager._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT alias, entity_id, entity_type FROM aliases")
            for row in cursor.fetchall():
                alias = row["alias"]
                if alias not in result:
                    result[alias] = []
                result[alias].append({
                    "type": row["entity_type"],
                    "id": row["entity_id"]
                })

        return result


# ==================== CLI Interface ====================

def main():
    import argparse
    import sys
    from .cli_output import print_success, print_error
    from .cli_args import normalize_global_project_root, load_json_arg
    from .index_manager import IndexManager

    parser = argparse.ArgumentParser(description="SQL State Manager CLI (v5.4)")
    parser.add_argument("--project-root", type=str, help="Project root directory")

    subparsers = parser.add_subparsers(dest="command")

    # Get statistics
    subparsers.add_parser("stats")

    # Get protagonist
    subparsers.add_parser("get-protagonist")

    # Get core entities
    subparsers.add_parser("get-core-entities")

    # Export entities_v3 format
    subparsers.add_parser("export-entities-v3")

    # Export alias_index format
    subparsers.add_parser("export-alias-index")

    # Process chapter data
    process_parser = subparsers.add_parser("process-chapter")
    process_parser.add_argument("--chapter", type=int, required=True)
    process_parser.add_argument("--data", required=True, help="Chapter data in JSON format")

    argv = normalize_global_project_root(sys.argv[1:])
    args = parser.parse_args(argv)

    # Initialize
    config = None
    if args.project_root:
        # Allow passing "workspace root directory", resolve to actual book project_root (must contain .wordsmith/state.json)
        from project_locator import resolve_project_root
        from .config import DataModulesConfig

        resolved_root = resolve_project_root(args.project_root)
        config = DataModulesConfig.from_project_root(resolved_root)

    manager = SQLStateManager(config)
    logger = IndexManager(config)
    tool_name = f"sql_state_manager:{args.command or 'unknown'}"

    def emit_success(data=None, message: str = "ok"):
        print_success(data, message=message)
        safe_log_tool_call(logger, tool_name=tool_name, success=True)

    def emit_error(code: str, message: str, suggestion: str | None = None):
        print_error(code, message, suggestion=suggestion)
        safe_log_tool_call(
            logger,
            tool_name=tool_name,
            success=False,
            error_code=code,
            error_message=message,
        )

    if args.command == "stats":
        stats = manager.get_stats()
        emit_success(stats, message="stats")

    elif args.command == "get-protagonist":
        protagonist = manager.get_protagonist()
        if protagonist:
            emit_success(protagonist, message="protagonist")
        else:
            emit_error("NOT_FOUND", "Protagonist not set")

    elif args.command == "get-core-entities":
        entities = manager.get_core_entities()
        emit_success(entities, message="core_entities")

    elif args.command == "export-entities-v3":
        data = manager.export_to_entities_v3_format()
        emit_success(data, message="entities_v3")

    elif args.command == "export-alias-index":
        data = manager.export_to_alias_index_format()
        emit_success(data, message="alias_index")

    elif args.command == "process-chapter":
        data = load_json_arg(args.data)
        stats = manager.process_chapter_entities(
            chapter=args.chapter,
            entities_appeared=data.get("entities_appeared", []),
            entities_new=data.get("entities_new", []),
            state_changes=data.get("state_changes", []),
            relationships_new=data.get("relationships_new", []),
        )
        emit_success(stats, message="chapter_processed")

    else:
        emit_error("UNKNOWN_COMMAND", "No valid command specified", suggestion="Please see --help")


if __name__ == "__main__":
    main()
