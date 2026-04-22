#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
migrate_state_to_sqlite.py - Data Migration Script (v5.4)

Migrates large data from state.json to SQLite (index.db):
- entities_v3 → entities table
- alias_index → aliases table
- state_changes → state_changes table
- structured_relationships → relationships table

After migration, state.json retains only streamlined data (< 5KB):
- progress
- protagonist_state
- strand_tracker
- disambiguation_warnings/pending
- project_info
- world_settings (skeleton)
- plot_threads
- relationships (simplified)
- review_checkpoints

Usage:
    python -m data_modules.migrate_state_to_sqlite --project-root "D:/wk/Battle-Through-the-Heavens"
    python -m data_modules.migrate_state_to_sqlite --project-root "." --dry-run
    python -m data_modules.migrate_state_to_sqlite --project-root "." --backup
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

from .config import get_config, DataModulesConfig
from .sql_state_manager import SQLStateManager, EntityData


def migrate_state_to_sqlite(
    config: DataModulesConfig,
    dry_run: bool = False,
    backup: bool = True,
    verbose: bool = True
) -> Dict[str, int]:
    """
    Execute migration.

    Parameters:
    - config: Configuration object
    - dry_run: Analyze only, do not write
    - backup: Backup state.json before migration
    - verbose: Print detailed logs

    Returns: Migration statistics
    """
    stats = {
        "entities": 0,
        "aliases": 0,
        "state_changes": 0,
        "relationships": 0,
        "skipped": 0,
        "errors": 0
    }

    # Read state.json
    state_file = config.state_file
    if not state_file.exists():
        if verbose:
            print(f"❌ state.json does not exist: {state_file}")
        return stats

    with open(state_file, 'r', encoding='utf-8') as f:
        state = json.load(f)

    if verbose:
        file_size = state_file.stat().st_size / 1024
        print(f"📄 Reading state.json ({file_size:.1f} KB)")

    # Backup
    if backup and not dry_run:
        backup_file = state_file.with_suffix(f".json.backup-{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        shutil.copy(state_file, backup_file)
        if verbose:
            print(f"💾 Backed up to: {backup_file}")

    # Initialize SQLStateManager
    sql_manager = SQLStateManager(config)

    # 1. Migrate entities_v3
    entities_v3 = state.get("entities_v3", {})
    if verbose:
        print(f"\n🔄 Migrating entities_v3...")

    for entity_type, entities in entities_v3.items():
        if not isinstance(entities, dict):
            continue

        for entity_id, entity_data in entities.items():
            if not isinstance(entity_data, dict):
                stats["skipped"] += 1
                continue

            try:
                entity = EntityData(
                    id=entity_id,
                    type=entity_type,
                    name=entity_data.get("canonical_name", entity_data.get("name", entity_id)),
                    tier=entity_data.get("tier", "decorative"),
                    desc=entity_data.get("desc", ""),
                    current=entity_data.get("current", {}),
                    aliases=[],  # Aliases handled separately
                    first_appearance=entity_data.get("first_appearance", 0),
                    last_appearance=entity_data.get("last_appearance", 0),
                    is_protagonist=entity_data.get("is_protagonist", False)
                )

                if not dry_run:
                    sql_manager.upsert_entity(entity)
                stats["entities"] += 1

                if verbose and stats["entities"] % 50 == 0:
                    print(f"  Migrated {stats['entities']} entities...")

            except Exception as e:
                stats["errors"] += 1
                if verbose:
                    print(f"  ⚠️ Entity migration failed {entity_id}: {e}")

    if verbose:
        print(f"  ✅ Entities: {stats['entities']}")

    # 2. Migrate alias_index
    alias_index = state.get("alias_index", {})
    if verbose:
        print(f"\n🔄 Migrating alias_index...")

    for alias, entries in alias_index.items():
        if not isinstance(entries, list):
            continue

        for entry in entries:
            if not isinstance(entry, dict):
                stats["skipped"] += 1
                continue

            entity_id = entry.get("id")
            entity_type = entry.get("type")
            if not entity_id or not entity_type:
                stats["skipped"] += 1
                continue

            try:
                if not dry_run:
                    sql_manager.register_alias(alias, entity_id, entity_type)
                stats["aliases"] += 1

            except Exception as e:
                stats["errors"] += 1
                if verbose:
                    print(f"  ⚠️ Alias migration failed {alias}: {e}")

    if verbose:
        print(f"  ✅ Aliases: {stats['aliases']}")

    # 3. Migrate state_changes
    state_changes = state.get("state_changes", [])
    if verbose:
        print(f"\n🔄 Migrating state_changes...")

    for change in state_changes:
        if not isinstance(change, dict):
            stats["skipped"] += 1
            continue

        try:
            entity_id = change.get("entity_id", "")
            if not entity_id:
                stats["skipped"] += 1
                continue

            if not dry_run:
                sql_manager.record_state_change(
                    entity_id=entity_id,
                    field=change.get("field", ""),
                    old_value=change.get("old", change.get("old_value", "")),
                    new_value=change.get("new", change.get("new_value", "")),
                    reason=change.get("reason", ""),
                    chapter=change.get("chapter", 0)
                )
            stats["state_changes"] += 1

        except Exception as e:
            stats["errors"] += 1
            if verbose:
                print(f"  ⚠️ State change migration failed: {e}")

    if verbose:
        print(f"  ✅ State changes: {stats['state_changes']}")

    # 4. Migrate structured_relationships
    relationships = state.get("structured_relationships", [])
    if verbose:
        print(f"\n🔄 Migrating structured_relationships...")

    for rel in relationships:
        if not isinstance(rel, dict):
            stats["skipped"] += 1
            continue

        try:
            from_entity = rel.get("from", rel.get("from_entity", ""))
            to_entity = rel.get("to", rel.get("to_entity", ""))
            if not from_entity or not to_entity:
                stats["skipped"] += 1
                continue

            if not dry_run:
                sql_manager.upsert_relationship(
                    from_entity=from_entity,
                    to_entity=to_entity,
                    type=rel.get("type", "met"),
                    description=rel.get("description", ""),
                    chapter=rel.get("chapter", 0)
                )
            stats["relationships"] += 1

        except Exception as e:
            stats["errors"] += 1
            if verbose:
                print(f"  ⚠️ Relationship migration failed: {e}")

    if verbose:
        print(f"  ✅ Relationships: {stats['relationships']}")

    # 5. Slim down state.json (remove migrated fields)
    if not dry_run:
        if verbose:
            print(f"\n🔄 Slimming down state.json...")

        # Fields to keep
        slim_state = {
            "project_info": state.get("project_info", {}),
            "progress": state.get("progress", {}),
            "protagonist_state": state.get("protagonist_state", {}),
            "strand_tracker": state.get("strand_tracker", {}),
            "world_settings": _slim_world_settings(state.get("world_settings", {})),
            "plot_threads": state.get("plot_threads", {}),
            "relationships": _slim_relationships(state.get("relationships", {})),
            "review_checkpoints": state.get("review_checkpoints", [])[-10:],  # Keep only last 10
            "disambiguation_warnings": state.get("disambiguation_warnings", [])[-20:],
            "disambiguation_pending": state.get("disambiguation_pending", [])[-10:],
            # v5.1 introduced marker
            "_migrated_to_sqlite": True,
            # v5.1 introduced marker
            "_migrated_to_sqlite": True,
            "_migration_timestamp": datetime.now().isoformat()
        }

        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(slim_state, f, ensure_ascii=False, indent=2)

        new_size = state_file.stat().st_size / 1024
        if verbose:
            print(f"  ✅ After slimming: {new_size:.1f} KB")

    # Print statistics
    if verbose:
        print(f"\n" + "=" * 50)
        print(f"📊 Migration Statistics:")
        print(f"  Entities: {stats['entities']}")
        print(f"  Aliases: {stats['aliases']}")
        print(f"  State changes: {stats['state_changes']}")
        print(f"  Relationships: {stats['relationships']}")
        print(f"  Skipped: {stats['skipped']}")
        print(f"  Errors: {stats['errors']}")
        if dry_run:
            print(f"\n⚠️ This is dry-run mode, no data was actually written")

    return stats


def _slim_world_settings(world_settings: Dict) -> Dict:
    """Slim down world_settings, keeping only skeleton"""
    if not isinstance(world_settings, dict):
        return {}

    slim = {}

    # power_system: Keep only level names
    power_system = world_settings.get("power_system", [])
    if isinstance(power_system, list):
        slim["power_system"] = [
            p.get("name") if isinstance(p, dict) else p
            for p in power_system[:20]  # Max 20 levels
        ]

    # factions: Keep only name and brief description
    factions = world_settings.get("factions", [])
    if isinstance(factions, list):
        slim["factions"] = [
            {"name": f.get("name"), "type": f.get("type")}
            if isinstance(f, dict) else f
            for f in factions[:30]  # Max 30 factions
        ]

    # locations: Keep only names
    locations = world_settings.get("locations", [])
    if isinstance(locations, list):
        slim["locations"] = [
            loc.get("name") if isinstance(loc, dict) else loc
            for loc in locations[:50]  # Max 50 locations
        ]

    return slim


def _slim_relationships(relationships: Dict) -> Dict:
    """Slim down relationships, keeping only core relationships"""
    if not isinstance(relationships, dict):
        return {}

    # Only keep the relationships dict itself, no additional slimming
    # because this field itself should be relatively small
    return relationships


def main():
    import argparse
    from .cli_output import print_success, print_error
    from .index_manager import IndexManager

    parser = argparse.ArgumentParser(description="Migrate state.json to SQLite (v5.4)")
    parser.add_argument("--project-root", type=str, required=True, help="Project root directory")
    parser.add_argument("--dry-run", action="store_true", help="Analyze only, do not write")
    parser.add_argument("--backup", action="store_true", default=True, help="Backup before migration")
    parser.add_argument("--no-backup", action="store_true", help="Do not backup")
    parser.add_argument("--quiet", action="store_true", help="Quiet mode")

    args = parser.parse_args()

    # Allows passing “workspace root directory”, resolves to actual book project_root (must contain .webnovel/state.json)
    from project_locator import resolve_project_root

    resolved_root = resolve_project_root(args.project_root)
    config = DataModulesConfig.from_project_root(resolved_root)
    backup = not args.no_backup
    logger = IndexManager(config)
    tool_name = "migrate_state_to_sqlite"

    try:
        stats = migrate_state_to_sqlite(
            config=config,
            dry_run=args.dry_run,
            backup=backup,
            verbose=False,
        )
    except Exception as exc:
        print_error("MIGRATE_FAILED", str(exc), suggestion="Check state.json and index.db permissions")
        try:
            logger.log_tool_call(tool_name, False, error_code="MIGRATE_FAILED", error_message=str(exc))
        except Exception:
            pass
        raise SystemExit(1)

    if stats.get("errors", 0) > 0:
        print_error("MIGRATE_ERRORS", "Migration errors occurred", details=stats)
        try:
            logger.log_tool_call(tool_name, False, error_code="MIGRATE_ERRORS", error_message="Migration errors occurred")
        except Exception:
            pass
        raise SystemExit(1)

    print_success({"project": str(config.project_root), **stats}, message="migrated")
    try:
        logger.log_tool_call(tool_name, True)
    except Exception:
        pass


if __name__ == "__main__":
    main()
