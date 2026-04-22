#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entity Linker - Entity Disambiguation Helper Module (v5.4)

Provides entity disambiguation helper functions for Data Agent:
- Confidence judgment
- Alias index management (via index.db aliases table)
- Disambiguation result recording

v5.1 changes (v5.4 continues):
- Alias storage migrated from state.json to index.db aliases table
- Uses IndexManager for alias read/write
- Removed direct state.json operations
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field

from .config import get_config
from .index_manager import IndexManager
from .observability import safe_log_tool_call


@dataclass
class DisambiguationResult:
    """Disambiguation result"""
    mention: str
    entity_id: Optional[str]
    confidence: float
    candidates: List[str] = field(default_factory=list)
    adopted: bool = False
    warning: Optional[str] = None


class EntityLinker:
    """Entity linker - assists Data Agent with entity disambiguation (v5.1 SQLite, v5.4 continues)"""

    def __init__(self, config=None):
        self.config = config or get_config()
        self._index_manager = IndexManager(self.config)

    # ==================== Alias Management (v5.1 SQLite, v5.4 continues) ====================

    def register_alias(self, entity_id: str, alias: str, entity_type: str = "Character") -> bool:
        """Register new alias (v5.1 introduced: writes to index.db aliases table)"""
        if not alias or not entity_id:
            return False
        return self._index_manager.register_alias(alias, entity_id, entity_type)

    def lookup_alias(self, mention: str, entity_type: str = None) -> Optional[str]:
        """Look up entity ID for alias (returns first match, optional type filter)"""
        entries = self._index_manager.get_entities_by_alias(mention)
        if not entries:
            return None

        if entity_type:
            for entry in entries:
                if entry.get("type") == entity_type:
                    return entry.get("id")
            return None
        else:
            return entries[0].get("id") if entries else None

    def lookup_alias_all(self, mention: str) -> List[Dict]:
        """Look up all entities for an alias (one-to-many)"""
        entries = self._index_manager.get_entities_by_alias(mention)
        return [{"type": e.get("type"), "id": e.get("id")} for e in entries]

    def get_all_aliases(self, entity_id: str, entity_type: str = None) -> List[str]:
        """Get all aliases for an entity"""
        return self._index_manager.get_entity_aliases(entity_id)

    # ==================== Confidence Judgment ====================

    def evaluate_confidence(self, confidence: float) -> Tuple[str, bool, Optional[str]]:
        """
        Evaluate confidence, returns (action, adopt, warning).

        - action: "auto" | "warn" | "manual"
        - adopt: whether to adopt
        - warning: warning message
        """
        if confidence >= self.config.extraction_confidence_high:
            return ("auto", True, None)
        elif confidence >= self.config.extraction_confidence_medium:
            return ("warn", True, f"Medium confidence match (confidence: {confidence:.2f})")
        else:
            return ("manual", False, f"Requires manual confirmation (confidence: {confidence:.2f})")

    def process_uncertain(
        self,
        mention: str,
        candidates: List[str],
        suggested: str,
        confidence: float,
        context: str = ""
    ) -> DisambiguationResult:
        """
        Process uncertain entity match.

        Returns disambiguation result, including whether to adopt, warning message, etc.
        """
        action, adopt, warning = self.evaluate_confidence(confidence)

        result = DisambiguationResult(
            mention=mention,
            entity_id=suggested if adopt else None,
            confidence=confidence,
            candidates=candidates,
            adopted=adopt,
            warning=warning
        )

        return result

    # ==================== Batch Processing ====================

    def process_extraction_result(
        self,
        uncertain_items: List[Dict]
    ) -> Tuple[List[DisambiguationResult], List[str]]:
        """
        Process uncertain items from AI extraction results.

        Returns (results, warnings)
        """
        results = []
        warnings = []

        for item in uncertain_items:
            result = self.process_uncertain(
                mention=item.get("mention", ""),
                candidates=item.get("candidates", []),
                suggested=item.get("suggested", ""),
                confidence=item.get("confidence", 0.0),
                context=item.get("context", "")
            )
            results.append(result)

            if result.warning:
                warnings.append(f"{result.mention} -> {result.entity_id}: {result.warning}")

        return results, warnings

    def register_new_entities(
        self,
        new_entities: List[Dict]
    ) -> List[str]:
        """
        Register aliases for new entities (v5.1 introduced, v5.4 continues).

        Returns list of registered entity IDs.
        """
        registered = []

        for entity in new_entities:
            entity_id = entity.get("suggested_id") or entity.get("id")
            if not entity_id or entity_id == "NEW":
                continue

            entity_type = entity.get("type", "Character")

            # Register main name
            name = entity.get("name", "")
            if name:
                self.register_alias(entity_id, name, entity_type)

            # Register mention variants
            for mention in entity.get("mentions", []):
                if mention and mention != name:
                    self.register_alias(entity_id, mention, entity_type)

            registered.append(entity_id)

        return registered


# ==================== CLI Interface ====================

def main():
    import argparse
    import sys
    from .cli_output import print_success, print_error
    from .cli_args import normalize_global_project_root
    from .index_manager import IndexManager

    parser = argparse.ArgumentParser(description="Entity Linker CLI (v5.4 SQLite)")
    parser.add_argument("--project-root", type=str, help="Project root directory")

    subparsers = parser.add_subparsers(dest="command")

    # Register alias
    register_parser = subparsers.add_parser("register-alias")
    register_parser.add_argument("--entity", required=True, help="Entity ID")
    register_parser.add_argument("--alias", required=True, help="Alias")
    register_parser.add_argument("--type", default="Character", help="Entity type (default: Character)")

    # Lookup alias
    lookup_parser = subparsers.add_parser("lookup")
    lookup_parser.add_argument("--mention", required=True, help="Mention text")
    lookup_parser.add_argument("--type", help="Filter by type")

    # Lookup all matches (one-to-many)
    lookup_all_parser = subparsers.add_parser("lookup-all")
    lookup_all_parser.add_argument("--mention", required=True, help="Mention text")

    # List aliases
    list_parser = subparsers.add_parser("list-aliases")
    list_parser.add_argument("--entity", required=True, help="Entity ID")
    list_parser.add_argument("--type", help="Entity type")

    argv = normalize_global_project_root(sys.argv[1:])
    args = parser.parse_args(argv)

    # Initialize
    config = None
    if args.project_root:
        # Allows passing "workspace root directory", resolves to actual book project_root (must contain .wordsmith/state.json)
        from project_locator import resolve_project_root
        from .config import DataModulesConfig

        resolved_root = resolve_project_root(args.project_root)
        config = DataModulesConfig.from_project_root(resolved_root)

    linker = EntityLinker(config)
    logger = IndexManager(config)
    tool_name = f"entity_linker:{args.command or 'unknown'}"

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

    if args.command == "register-alias":
        entity_type = getattr(args, "type", "Character")
        success = linker.register_alias(args.entity, args.alias, entity_type)
        if success:
            emit_success({"entity": args.entity, "alias": args.alias, "type": entity_type}, message="alias_registered")
        else:
            emit_error("ALIAS_EXISTS", "Registration failed or already exists")

    elif args.command == "lookup":
        entity_type = getattr(args, "type", None)
        entity_id = linker.lookup_alias(args.mention, entity_type)
        if entity_id:
            emit_success({"mention": args.mention, "entity": entity_id}, message="lookup")
        else:
            emit_error("NOT_FOUND", f"Alias not found: {args.mention}")

    elif args.command == "lookup-all":
        matches = linker.lookup_alias_all(args.mention)
        emit_success(matches, message="lookup_all")

    elif args.command == "list-aliases":
        entity_type = getattr(args, "type", None)
        aliases = linker.get_all_aliases(args.entity, entity_type)
        emit_success(aliases, message="aliases")

    else:
        emit_error("UNKNOWN_COMMAND", "No valid command specified", suggestion="Please check --help")


if __name__ == "__main__":
    main()
