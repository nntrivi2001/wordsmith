#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Index Manager - Index Management Module (v5.4)

Manages read/write operations for index.db (SQLite):
- Chapter metadata index
- Entity appearance records
- Scene index
- Entity storage (migrated from state.json)
- Alias index (one-to-many)
- State change records
- Relationship storage
- Fast query interfaces
- Reading power debt management (v5.3 introduced, v5.4 continues)

v5.4 changes:
- New invalid_facts table: Track invalid facts (pending/confirmed)
- New tool_call_stats table: Record tool call success rate and error messages
- New review_metrics table: Record review metrics and trend data

v5.3 changes:
- New override_contracts table: Record Override Contracts when violating soft suggestions
- New chase_debt table: Reading power debt tracking
- New debt_events table: Debt event log (creation/repayment/interest)
- New chapter_reading_power table: Chapter reading power metadata

v5.1 changes:
- New entities table to replace entities_v3 in state.json
- New aliases table to replace alias_index in state.json (supports one-to-many)
- New state_changes table to replace state_changes in state.json
- New relationships table to replace structured_relationships in state.json
"""

import sqlite3
import json
import time
from pathlib import Path

from runtime_compat import enable_windows_utf8_stdio
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from contextlib import contextmanager
from datetime import datetime

from .config import get_config
from .index_chapter_mixin import IndexChapterMixin
from .index_entity_mixin import IndexEntityMixin
from .index_debt_mixin import IndexDebtMixin
from .index_reading_mixin import IndexReadingMixin
from .index_observability_mixin import IndexObservabilityMixin
from .observability import safe_append_perf_timing, safe_log_tool_call


@dataclass
class ChapterMeta:
    """Chapter metadata"""

    chapter: int
    title: str
    location: str
    word_count: int
    characters: List[str]
    summary: str = ""


@dataclass
class SceneMeta:
    """Scene metadata"""

    chapter: int
    scene_index: int
    start_line: int
    end_line: int
    location: str
    summary: str
    characters: List[str]


@dataclass
class EntityMeta:
    """Entity metadata (v5.1 introduced)"""

    id: str
    type: str  # character/location/item/faction/skill
    canonical_name: str
    tier: str = "decor"  # core/important/minor/decor
    desc: str = ""
    current: Dict = field(default_factory=dict)  # Current state (realm/location/items etc.)
    first_appearance: int = 0
    last_appearance: int = 0
    is_protagonist: bool = False
    is_archived: bool = False


@dataclass
class StateChangeMeta:
    """State change record (v5.1 introduced)"""

    entity_id: str
    field: str
    old_value: str
    new_value: str
    reason: str
    chapter: int


@dataclass
class RelationshipMeta:
    """Relationship record (v5.1 introduced)"""

    from_entity: str
    to_entity: str
    type: str
    description: str
    chapter: int


@dataclass
class RelationshipEventMeta:
    """Relationship event record (v5.5 introduced)"""

    from_entity: str
    to_entity: str
    type: str
    chapter: int
    action: str = "update"  # create/update/decay/remove
    polarity: int = 0  # -1/0/1
    strength: float = 0.5  # 0~1
    description: str = ""
    scene_index: int = 0
    evidence: str = ""
    confidence: float = 1.0


@dataclass
class OverrideContractMeta:
    """Override Contract (v5.3 introduced)"""

    chapter: int
    constraint_type: str  # SOFT_HOOK_STRENGTH / SOFT_MICROPAYOFF / etc.
    constraint_id: str  # Specific constraint identifier
    rationale_type: str  # TRANSITIONAL_SETUP / LOGIC_INTEGRITY / etc.
    rationale_text: str  # Specific rationale explanation
    payback_plan: str  # Repayment plan description
    due_chapter: int  # Repayment deadline chapter
    status: str = "pending"  # pending / fulfilled / overdue / cancelled


@dataclass
class ChaseDebtMeta:
    """Reading power debt (v5.3 introduced)"""

    id: int = 0
    debt_type: str = ""  # hook_strength / micropayoff / coolpoint / etc.
    original_amount: float = 1.0  # Initial debt amount
    current_amount: float = 1.0  # Current debt amount (with interest)
    interest_rate: float = 0.1  # Interest rate (per chapter)
    source_chapter: int = 0  # Chapter where debt was created
    due_chapter: int = 0  # Deadline chapter
    override_contract_id: int = 0  # Associated Override Contract
    status: str = "active"  # active / paid / overdue / written_off


@dataclass
class DebtEventMeta:
    """Debt event log (v5.3 introduced)"""

    debt_id: int
    event_type: (
        str  # created / interest_accrued / partial_payment / full_payment / overdue
    )
    amount: float
    chapter: int
    note: str = ""


@dataclass
class ChapterReadingPowerMeta:
    """Chapter reading power metadata (v5.3 introduced)"""

    chapter: int
    hook_type: str = ""  # Chapter-end hook type
    hook_strength: str = "medium"  # strong / medium / weak
    coolpoint_patterns: List[str] = field(default_factory=list)  # Coolpoint patterns used
    micropayoffs: List[str] = field(default_factory=list)  # Micropayoff list
    hard_violations: List[str] = field(default_factory=list)  # Hard constraint violations
    soft_suggestions: List[str] = field(default_factory=list)  # Soft suggestions
    is_transition: bool = False  # Whether it is a transition chapter
    override_count: int = 0  # Override Contract count
    debt_balance: float = 0.0  # Current debt balance


@dataclass
class ReviewMetrics:
    """Review metrics record (v5.4 introduced)"""

    start_chapter: int
    end_chapter: int
    overall_score: float = 0.0
    dimension_scores: Dict[str, float] = field(default_factory=dict)
    severity_counts: Dict[str, int] = field(default_factory=dict)
    critical_issues: List[str] = field(default_factory=list)
    report_file: str = ""
    notes: str = ""


@dataclass
class WritingChecklistScoreMeta:
    """Writing checklist score record (Context Contract v2 Phase F)"""

    chapter: int
    template: str = "plot"
    total_items: int = 0
    required_items: int = 0
    completed_items: int = 0
    completed_required: int = 0
    total_weight: float = 0.0
    completed_weight: float = 0.0
    completion_rate: float = 0.0
    score: float = 0.0
    score_breakdown: Dict[str, Any] = field(default_factory=dict)
    pending_items: List[str] = field(default_factory=list)
    source: str = "context_manager"
    notes: str = ""


class IndexManager(IndexChapterMixin, IndexEntityMixin, IndexDebtMixin, IndexReadingMixin, IndexObservabilityMixin):
    """Index manager"""

    def __init__(self, config=None):
        self.config = config or get_config()
        self._init_db()

    def _init_db(self):
        """Initialize database tables"""
        self.config.ensure_dirs()

        with self._get_conn() as conn:
            cursor = conn.cursor()

            # Chapter table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chapters (
                    chapter INTEGER PRIMARY KEY,
                    title TEXT,
                    location TEXT,
                    word_count INTEGER,
                    characters TEXT,
                    summary TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Scene table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scenes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chapter INTEGER,
                    scene_index INTEGER,
                    start_line INTEGER,
                    end_line INTEGER,
                    location TEXT,
                    summary TEXT,
                    characters TEXT,
                    UNIQUE(chapter, scene_index)
                )
            """)

            # Entity appearance table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS appearances (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entity_id TEXT,
                    chapter INTEGER,
                    mentions TEXT,
                    confidence REAL,
                    UNIQUE(entity_id, chapter)
                )
            """)

            # Create indexes
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_scenes_chapter ON scenes(chapter)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_appearances_entity ON appearances(entity_id)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_appearances_chapter ON appearances(chapter)"
            )

            # ==================== Tables introduced in v5.1 ====================

            # Entity table (replaces entities_v3 in state.json)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS entities (
                    id TEXT PRIMARY KEY,
                    type TEXT NOT NULL,
                    canonical_name TEXT NOT NULL,
                    tier TEXT DEFAULT 'decor',
                    desc TEXT,
                    current_json TEXT,
                    first_appearance INTEGER DEFAULT 0,
                    last_appearance INTEGER DEFAULT 0,
                    is_protagonist INTEGER DEFAULT 0,
                    is_archived INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Alias table (replaces alias_index in state.json, supports one-to-many)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS aliases (
                    alias TEXT NOT NULL,
                    entity_id TEXT NOT NULL,
                    entity_type TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (alias, entity_id, entity_type)
                )
            """)

            # State changes table (replaces state_changes in state.json)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS state_changes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entity_id TEXT NOT NULL,
                    field TEXT NOT NULL,
                    old_value TEXT,
                    new_value TEXT,
                    reason TEXT,
                    chapter INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Relationships table (replaces structured_relationships in state.json)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS relationships (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    from_entity TEXT NOT NULL,
                    to_entity TEXT NOT NULL,
                    type TEXT NOT NULL,
                    description TEXT,
                    chapter INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(from_entity, to_entity, type)
                )
            """)

            # Indexes introduced in v5.1
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(type)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_entities_tier ON entities(tier)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_entities_protagonist ON entities(is_protagonist)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_aliases_entity ON aliases(entity_id)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_aliases_alias ON aliases(alias)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_state_changes_entity ON state_changes(entity_id)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_state_changes_chapter ON state_changes(chapter)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_relationships_from ON relationships(from_entity)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_relationships_to ON relationships(to_entity)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_relationships_chapter ON relationships(chapter)"
            )

            # Relationship events table (v5.5 introduced, for timeline replay/graph analysis)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS relationship_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    from_entity TEXT NOT NULL,
                    to_entity TEXT NOT NULL,
                    type TEXT NOT NULL,
                    action TEXT NOT NULL DEFAULT 'update',
                    polarity INTEGER DEFAULT 0,
                    strength REAL DEFAULT 0.5,
                    description TEXT,
                    chapter INTEGER NOT NULL,
                    scene_index INTEGER DEFAULT 0,
                    evidence TEXT,
                    confidence REAL DEFAULT 1.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_relationship_events_from_chapter ON relationship_events(from_entity, chapter)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_relationship_events_to_chapter ON relationship_events(to_entity, chapter)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_relationship_events_chapter ON relationship_events(chapter)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_relationship_events_type_chapter ON relationship_events(type, chapter)"
            )

            # ==================== Tables introduced in v5.3: Reading power debt management ====================

            # Override Contract table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS override_contracts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chapter INTEGER NOT NULL,
                    constraint_type TEXT NOT NULL,
                    constraint_id TEXT NOT NULL,
                    rationale_type TEXT NOT NULL,
                    rationale_text TEXT,
                    payback_plan TEXT,
                    due_chapter INTEGER NOT NULL,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fulfilled_at TIMESTAMP,
                    UNIQUE(chapter, constraint_type, constraint_id)
                )
            """)

            # Reading power debt table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chase_debt (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    debt_type TEXT NOT NULL,
                    original_amount REAL DEFAULT 1.0,
                    current_amount REAL DEFAULT 1.0,
                    interest_rate REAL DEFAULT 0.1,
                    source_chapter INTEGER NOT NULL,
                    due_chapter INTEGER NOT NULL,
                    override_contract_id INTEGER,
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (override_contract_id) REFERENCES override_contracts(id)
                )
            """)

            # Debt event log table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS debt_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    debt_id INTEGER NOT NULL,
                    event_type TEXT NOT NULL,
                    amount REAL NOT NULL,
                    chapter INTEGER NOT NULL,
                    note TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (debt_id) REFERENCES chase_debt(id)
                )
            """)

            # Chapter reading power metadata table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chapter_reading_power (
                    chapter INTEGER PRIMARY KEY,
                    hook_type TEXT,
                    hook_strength TEXT DEFAULT 'medium',
                    coolpoint_patterns TEXT,
                    micropayoffs TEXT,
                    hard_violations TEXT,
                    soft_suggestions TEXT,
                    is_transition INTEGER DEFAULT 0,
                    override_count INTEGER DEFAULT 0,
                    debt_balance REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Indexes introduced in v5.3
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_override_contracts_chapter ON override_contracts(chapter)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_override_contracts_status ON override_contracts(status)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_override_contracts_due ON override_contracts(due_chapter)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_chase_debt_status ON chase_debt(status)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_chase_debt_source ON chase_debt(source_chapter)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_chase_debt_due ON chase_debt(due_chapter)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_debt_events_debt ON debt_events(debt_id)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_debt_events_chapter ON debt_events(chapter)"
            )

            # ==================== New tables in v5.4: Invalid facts and logs ====================

            # Invalid facts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS invalid_facts (
                    id INTEGER PRIMARY KEY,
                    source_type TEXT NOT NULL,
                    source_id TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    marked_by TEXT NOT NULL,
                    marked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    confirmed_at TIMESTAMP,
                    chapter_discovered INTEGER
                )
            """)

            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_invalid_status ON invalid_facts(status)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_invalid_source ON invalid_facts(source_type, source_id)"
            )

            # Review metrics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS review_metrics (
                    start_chapter INTEGER NOT NULL,
                    end_chapter INTEGER NOT NULL,
                    overall_score REAL DEFAULT 0,
                    dimension_scores TEXT,
                    severity_counts TEXT,
                    critical_issues TEXT,
                    report_file TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (start_chapter, end_chapter)
                )
            """)
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_review_metrics_end ON review_metrics(end_chapter)"
            )

            # RAG query log
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rag_query_log (
                    id INTEGER PRIMARY KEY,
                    query TEXT,
                    query_type TEXT,
                    results_count INTEGER,
                    hit_sources TEXT,
                    latency_ms INTEGER,
                    chapter INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_rag_query_type ON rag_query_log(query_type)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_rag_query_chapter ON rag_query_log(chapter)"
            )

            # Tool call stats
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tool_call_stats (
                    id INTEGER PRIMARY KEY,
                    tool_name TEXT,
                    success BOOLEAN,
                    retry_count INTEGER DEFAULT 0,
                    error_code TEXT,
                    error_message TEXT,
                    chapter INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_tool_stats_name ON tool_call_stats(tool_name)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_tool_stats_chapter ON tool_call_stats(chapter)"
            )

            # Writing checklist score record (Phase F)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS writing_checklist_scores (
                    chapter INTEGER PRIMARY KEY,
                    template TEXT DEFAULT 'plot',
                    total_items INTEGER DEFAULT 0,
                    required_items INTEGER DEFAULT 0,
                    completed_items INTEGER DEFAULT 0,
                    completed_required INTEGER DEFAULT 0,
                    total_weight REAL DEFAULT 0,
                    completed_weight REAL DEFAULT 0,
                    completion_rate REAL DEFAULT 0,
                    score REAL DEFAULT 0,
                    score_breakdown TEXT,
                    pending_items TEXT,
                    source TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_checklist_score_value ON writing_checklist_scores(score)"
            )

            conn.commit()

    @contextmanager
    def _get_conn(self):
        """Get database connection"""
        conn = sqlite3.connect(str(self.config.index_db))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    # ==================== Chapter Operations ====================

# ==================== CLI Interface ====================


def main():
    import argparse
    import sys
    from .cli_output import print_success, print_error
    from .cli_args import normalize_global_project_root, load_json_arg

    parser = argparse.ArgumentParser(description="Index Manager CLI (v5.4)")
    parser.add_argument("--project-root", type=str, help="Project root directory")

    subparsers = parser.add_subparsers(dest="command")

    # Get statistics
    subparsers.add_parser("stats")

    # Query chapter
    chapter_parser = subparsers.add_parser("get-chapter")
    chapter_parser.add_argument("--chapter", type=int, required=True)

    # Query recent appearances
    recent_parser = subparsers.add_parser("recent-appearances")
    recent_parser.add_argument("--limit", type=int, default=None)

    # Query entity appearances
    entity_parser = subparsers.add_parser("entity-appearances")
    entity_parser.add_argument("--entity", required=True)
    entity_parser.add_argument("--limit", type=int, default=None)

    # Search scenes
    search_parser = subparsers.add_parser("search-scenes")
    search_parser.add_argument("--location", required=True)
    search_parser.add_argument("--limit", type=int, default=None)

    # Process chapter data (write)
    process_parser = subparsers.add_parser("process-chapter")
    process_parser.add_argument("--chapter", type=int, required=True)
    process_parser.add_argument("--title", required=True)
    process_parser.add_argument("--location", required=True)
    process_parser.add_argument("--word-count", type=int, required=True)
    process_parser.add_argument("--entities", required=True, help="Entity list in JSON format")
    process_parser.add_argument("--scenes", required=True, help="Scene list in JSON format")

    # ==================== Commands introduced in v5.1 ====================

    # Get entity
    get_entity_parser = subparsers.add_parser("get-entity")
    get_entity_parser.add_argument("--id", required=True, help="Entity ID")

    # Get core entities
    subparsers.add_parser("get-core-entities")

    # Get protagonist
    subparsers.add_parser("get-protagonist")

    # Get entities by type
    type_parser = subparsers.add_parser("get-entities-by-type")
    type_parser.add_argument(
        "--type", required=True, help="Entity type (character/location/item/faction/skill)"
    )
    type_parser.add_argument("--include-archived", action="store_true")

    # Find entity by alias
    alias_parser = subparsers.add_parser("get-by-alias")
    alias_parser.add_argument("--alias", required=True, help="Alias")

    # Get entity aliases
    aliases_parser = subparsers.add_parser("get-aliases")
    aliases_parser.add_argument("--entity", required=True, help="Entity ID")

    # Register alias
    reg_alias_parser = subparsers.add_parser("register-alias")
    reg_alias_parser.add_argument("--alias", required=True)
    reg_alias_parser.add_argument("--entity", required=True)
    reg_alias_parser.add_argument("--type", required=True, help="Entity type")

    # Get entity relationships
    rel_parser = subparsers.add_parser("get-relationships")
    rel_parser.add_argument("--entity", required=True)
    rel_parser.add_argument(
        "--direction", choices=["from", "to", "both"], default="both"
    )

    # Get relationship events
    rel_events_parser = subparsers.add_parser("get-relationship-events")
    rel_events_parser.add_argument("--entity", required=True)
    rel_events_parser.add_argument("--direction", choices=["from", "to", "both"], default="both")
    rel_events_parser.add_argument("--from-chapter", type=int, default=None)
    rel_events_parser.add_argument("--to-chapter", type=int, default=None)
    rel_events_parser.add_argument("--limit", type=int, default=100)

    # Get relationship graph
    rel_graph_parser = subparsers.add_parser("get-relationship-graph")
    rel_graph_parser.add_argument("--center", required=True, help="Center entity ID")
    rel_graph_parser.add_argument("--depth", type=int, default=2)
    rel_graph_parser.add_argument("--chapter", type=int, default=None)
    rel_graph_parser.add_argument("--top-edges", type=int, default=50)
    rel_graph_parser.add_argument("--format", choices=["json", "mermaid"], default="json")

    # Get relationship timeline
    rel_timeline_parser = subparsers.add_parser("get-relationship-timeline")
    rel_timeline_parser.add_argument("--a", required=True, help="Entity A")
    rel_timeline_parser.add_argument("--b", required=True, help="Entity B")
    rel_timeline_parser.add_argument("--from-chapter", type=int, default=None)
    rel_timeline_parser.add_argument("--to-chapter", type=int, default=None)
    rel_timeline_parser.add_argument("--limit", type=int, default=100)

    # Write relationship event
    rel_event_record_parser = subparsers.add_parser("record-relationship-event")
    rel_event_record_parser.add_argument("--data", required=True, help="Relationship event data in JSON format")

    # Get state changes
    changes_parser = subparsers.add_parser("get-state-changes")
    changes_parser.add_argument("--entity", required=True)
    changes_parser.add_argument("--limit", type=int, default=20)

    # Write entity
    upsert_entity_parser = subparsers.add_parser("upsert-entity")
    upsert_entity_parser.add_argument(
        "--data", required=True, help="Entity data in JSON format"
    )

    # Write relationship
    upsert_rel_parser = subparsers.add_parser("upsert-relationship")
    upsert_rel_parser.add_argument("--data", required=True, help="Relationship data in JSON format")

    # Write state change
    state_change_parser = subparsers.add_parser("record-state-change")
    state_change_parser.add_argument(
        "--data", required=True, help="State change data in JSON format"
    )

    # ==================== New commands in v5.4 ====================
    invalid_parser = subparsers.add_parser("mark-invalid")
    invalid_parser.add_argument("--source-type", required=True)
    invalid_parser.add_argument("--source-id", required=True)
    invalid_parser.add_argument("--reason", required=True)
    invalid_parser.add_argument("--marked-by", default="user")
    invalid_parser.add_argument("--chapter", type=int, default=None)

    resolve_parser = subparsers.add_parser("resolve-invalid")
    resolve_parser.add_argument("--id", type=int, required=True)
    resolve_parser.add_argument("--action", choices=["confirm", "dismiss"], required=True)

    list_invalid_parser = subparsers.add_parser("list-invalid")
    list_invalid_parser.add_argument("--status", choices=["pending", "confirmed"], default=None)

    review_save_parser = subparsers.add_parser("save-review-metrics")
    review_save_parser.add_argument("--data", required=True, help="Review metrics data in JSON format")

    review_recent_parser = subparsers.add_parser("get-recent-review-metrics")
    review_recent_parser.add_argument("--limit", type=int, default=5)

    review_trend_parser = subparsers.add_parser("get-review-trend-stats")
    review_trend_parser.add_argument("--last-n", type=int, default=5)

    checklist_score_save_parser = subparsers.add_parser("save-writing-checklist-score")
    checklist_score_save_parser.add_argument("--data", required=True, help="Writing checklist score data in JSON format")

    checklist_score_get_parser = subparsers.add_parser("get-writing-checklist-score")
    checklist_score_get_parser.add_argument("--chapter", type=int, required=True)

    checklist_score_recent_parser = subparsers.add_parser("get-recent-writing-checklist-scores")
    checklist_score_recent_parser.add_argument("--limit", type=int, default=10)

    checklist_score_trend_parser = subparsers.add_parser("get-writing-checklist-score-trend")
    checklist_score_trend_parser.add_argument("--last-n", type=int, default=10)

    # ==================== Commands introduced in v5.3 ====================

    # Get debt summary
    subparsers.add_parser("get-debt-summary")

    # Get recent chapter reading power metadata
    reading_power_parser = subparsers.add_parser("get-recent-reading-power")
    reading_power_parser.add_argument("--limit", type=int, default=10)

    # Get chapter reading power metadata
    chapter_rp_parser = subparsers.add_parser("get-chapter-reading-power")
    chapter_rp_parser.add_argument("--chapter", type=int, required=True)

    # Get coolpoint pattern usage stats
    pattern_stats_parser = subparsers.add_parser("get-pattern-usage-stats")
    pattern_stats_parser.add_argument("--last-n", type=int, default=20)

    # Get hook type usage stats
    hook_stats_parser = subparsers.add_parser("get-hook-type-stats")
    hook_stats_parser.add_argument("--last-n", type=int, default=20)

    # Get pending overrides
    pending_override_parser = subparsers.add_parser("get-pending-overrides")
    pending_override_parser.add_argument("--before-chapter", type=int, default=None)

    # Get overdue overrides
    overdue_override_parser = subparsers.add_parser("get-overdue-overrides")
    overdue_override_parser.add_argument("--current-chapter", type=int, required=True)

    # Get active debts
    subparsers.add_parser("get-active-debts")

    # Get overdue debts
    overdue_debt_parser = subparsers.add_parser("get-overdue-debts")
    overdue_debt_parser.add_argument("--current-chapter", type=int, required=True)

    # Calculate interest
    accrue_parser = subparsers.add_parser("accrue-interest")
    accrue_parser.add_argument("--current-chapter", type=int, required=True)

    # Repay debt
    pay_debt_parser = subparsers.add_parser("pay-debt")
    pay_debt_parser.add_argument("--debt-id", type=int, required=True)
    pay_debt_parser.add_argument("--amount", type=float, required=True)
    pay_debt_parser.add_argument("--chapter", type=int, required=True)

    # Create Override Contract
    create_override_parser = subparsers.add_parser("create-override-contract")
    create_override_parser.add_argument(
        "--data", required=True, help="Override Contract data in JSON format"
    )

    # Create debt
    create_debt_parser = subparsers.add_parser("create-debt")
    create_debt_parser.add_argument("--data", required=True, help="Debt data in JSON format")

    # Mark Override as fulfilled
    fulfill_override_parser = subparsers.add_parser("fulfill-override")
    fulfill_override_parser.add_argument("--contract-id", type=int, required=True)

    # Save chapter reading power metadata
    save_rp_parser = subparsers.add_parser("save-chapter-reading-power")
    save_rp_parser.add_argument(
        "--data", required=True, help="Chapter reading power metadata in JSON format"
    )

    argv = normalize_global_project_root(sys.argv[1:])
    args = parser.parse_args(argv)
    command_started_at = time.perf_counter()

    # Initialize
    config = None
    if args.project_root:
        # Allow passing "workspace root directory", resolve to actual book project_root (must contain .webnovel/state.json)
        from project_locator import resolve_project_root
        from .config import DataModulesConfig

        resolved_root = resolve_project_root(args.project_root)
        config = DataModulesConfig.from_project_root(resolved_root)

    manager = IndexManager(config)
    tool_name = f"index_manager:{args.command or 'unknown'}"

    def _append_timing(
        success: bool,
        *,
        error_code: Optional[str] = None,
        error_message: Optional[str] = None,
        chapter: Optional[int] = None,
    ):
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

    def emit_success(data=None, message: str = "ok", chapter: Optional[int] = None):
        print_success(data, message=message)
        safe_log_tool_call(manager, tool_name=tool_name, success=True, chapter=chapter)
        _append_timing(True, chapter=chapter)

    def emit_error(code: str, message: str, suggestion: Optional[str] = None, chapter: Optional[int] = None):
        print_error(code, message, suggestion=suggestion)
        safe_log_tool_call(
            manager,
            tool_name=tool_name,
            success=False,
            error_code=code,
            error_message=message,
            chapter=chapter,
        )
        _append_timing(False, error_code=code, error_message=message, chapter=chapter)

    if args.command == "stats":
        emit_success(manager.get_stats(), message="stats")

    elif args.command == "get-chapter":
        chapter = manager.get_chapter(args.chapter)
        if chapter:
            emit_success(chapter, message="chapter")
        else:
            emit_error("NOT_FOUND", f"Chapter not found: {args.chapter}")

    elif args.command == "recent-appearances":
        appearances = manager.get_recent_appearances(args.limit)
        emit_success(appearances, message="recent_appearances")

    elif args.command == "entity-appearances":
        appearances = manager.get_entity_appearances(args.entity, args.limit)
        emit_success({"entity": args.entity, "appearances": appearances}, message="entity_appearances")

    elif args.command == "search-scenes":
        scenes = manager.search_scenes_by_location(args.location, args.limit)
        emit_success(scenes, message="scenes")

    elif args.command == "process-chapter":
        entities = load_json_arg(args.entities)
        scenes = load_json_arg(args.scenes)
        stats = manager.process_chapter_data(
            chapter=args.chapter,
            title=args.title,
            location=args.location,
            word_count=args.word_count,
            entities=entities,
            scenes=scenes,
        )
        emit_success(stats, message="chapter_processed", chapter=args.chapter)

    # ==================== Command processing introduced in v5.1 ====================

    elif args.command == "get-entity":
        entity = manager.get_entity(args.id)
        if entity:
            emit_success(entity, message="entity")
        else:
            emit_error("NOT_FOUND", f"Entity not found: {args.id}")

    elif args.command == "get-core-entities":
        entities = manager.get_core_entities()
        emit_success(entities, message="core_entities")

    elif args.command == "get-protagonist":
        protagonist = manager.get_protagonist()
        if protagonist:
            emit_success(protagonist, message="protagonist")
        else:
            emit_error("NOT_FOUND", "Protagonist not set")

    elif args.command == "get-entities-by-type":
        entities = manager.get_entities_by_type(args.type, args.include_archived)
        emit_success(entities, message="entities_by_type")

    elif args.command == "get-by-alias":
        entities = manager.get_entities_by_alias(args.alias)
        if entities:
            emit_success(entities, message="entities_by_alias")
        else:
            emit_error("NOT_FOUND", f"Alias not found: {args.alias}")

    elif args.command == "get-aliases":
        aliases = manager.get_entity_aliases(args.entity)
        if aliases:
            emit_success({"entity": args.entity, "aliases": aliases}, message="aliases")
        else:
            emit_error("NOT_FOUND", f"{args.entity} has no aliases")

    elif args.command == "register-alias":
        success = manager.register_alias(args.alias, args.entity, args.type)
        if success:
            emit_success(
                {"alias": args.alias, "entity": args.entity, "type": args.type},
                message="alias_registered",
            )
        else:
            emit_error("ALIAS_EXISTS", f"Alias already exists or registration failed: {args.alias}")

    elif args.command == "get-relationships":
        rels = manager.get_entity_relationships(args.entity, args.direction)
        emit_success(rels, message="relationships")

    elif args.command == "get-relationship-events":
        events = manager.get_relationship_events(
            entity_id=args.entity,
            direction=args.direction,
            from_chapter=args.from_chapter,
            to_chapter=args.to_chapter,
            limit=args.limit,
        )
        emit_success(events, message="relationship_events")

    elif args.command == "get-relationship-graph":
        graph = manager.build_relationship_subgraph(
            center_entity=args.center,
            depth=args.depth,
            chapter=args.chapter,
            top_edges=args.top_edges,
        )
        if args.format == "mermaid":
            emit_success({"mermaid": manager.render_relationship_subgraph_mermaid(graph)}, message="relationship_graph")
        else:
            emit_success(graph, message="relationship_graph")

    elif args.command == "get-relationship-timeline":
        timeline = manager.get_relationship_timeline(
            entity1=args.a,
            entity2=args.b,
            from_chapter=args.from_chapter,
            to_chapter=args.to_chapter,
            limit=args.limit,
        )
        emit_success(timeline, message="relationship_timeline")

    elif args.command == "get-state-changes":
        changes = manager.get_entity_state_changes(args.entity, args.limit)
        emit_success(changes, message="state_changes")

    elif args.command == "record-relationship-event":
        try:
            data = load_json_arg(args.data)
        except (TypeError, ValueError, json.JSONDecodeError):
            emit_error("INVALID_RELATIONSHIP_EVENT", "Invalid relationship event JSON")
        else:
            event = RelationshipEventMeta(
                from_entity=data.get("from_entity", ""),
                to_entity=data.get("to_entity", ""),
                type=data.get("type", ""),
                chapter=data.get("chapter", 0),
                action=data.get("action", "update"),
                polarity=data.get("polarity", 0),
                strength=data.get("strength", 0.5),
                description=data.get("description", ""),
                scene_index=data.get("scene_index", 0),
                evidence=data.get("evidence", ""),
                confidence=data.get("confidence", 1.0),
            )
            event_id = manager.record_relationship_event(event)
            if event_id > 0:
                emit_success({"id": event_id}, message="relationship_event_recorded")
            else:
                emit_error("INVALID_RELATIONSHIP_EVENT", "Invalid relationship event parameters, not written")

    elif args.command == "upsert-entity":
        data = load_json_arg(args.data)
        entity = EntityMeta(
            id=data["id"],
            type=data["type"],
            canonical_name=data["canonical_name"],
            tier=data.get("tier", "decor"),
            desc=data.get("desc", ""),
            current=data.get("current", {}),
            first_appearance=data.get("first_appearance", 0),
            last_appearance=data.get("last_appearance", 0),
            is_protagonist=data.get("is_protagonist", False),
            is_archived=data.get("is_archived", False),
        )
        is_new = manager.upsert_entity(entity)
        emit_success({"id": entity.id, "created": is_new}, message="entity_upserted")

    elif args.command == "upsert-relationship":
        data = load_json_arg(args.data)
        rel = RelationshipMeta(
            from_entity=data["from_entity"],
            to_entity=data["to_entity"],
            type=data["type"],
            description=data.get("description", ""),
            chapter=data["chapter"],
        )
        is_new = manager.upsert_relationship(rel)
        emit_success(
            {"from": rel.from_entity, "to": rel.to_entity, "type": rel.type, "created": is_new},
            message="relationship_upserted",
        )

    elif args.command == "record-state-change":
        data = load_json_arg(args.data)
        change = StateChangeMeta(
            entity_id=data["entity_id"],
            field=data["field"],
            old_value=data.get("old_value", ""),
            new_value=data["new_value"],
            reason=data.get("reason", ""),
            chapter=data["chapter"],
        )
        record_id = manager.record_state_change(change)
        emit_success({"id": record_id, "entity": change.entity_id, "field": change.field}, message="state_change_recorded")

    # ==================== Invalid fact command processing in v5.4 ====================

    elif args.command == "mark-invalid":
        invalid_id = manager.mark_invalid_fact(
            args.source_type,
            args.source_id,
            args.reason,
            marked_by=args.marked_by,
            chapter_discovered=args.chapter,
        )
        emit_success({"id": invalid_id}, message="invalid_marked")

    elif args.command == "resolve-invalid":
        ok = manager.resolve_invalid_fact(args.id, args.action)
        if ok:
            emit_success({"id": args.id, "action": args.action}, message="invalid_resolved")
        else:
            emit_error("INVALID_ACTION", f"Cannot process action: {args.action}")

    elif args.command == "list-invalid":
        rows = manager.list_invalid_facts(args.status)
        emit_success(rows, message="invalid_list")

    elif args.command == "save-review-metrics":
        data = load_json_arg(args.data)
        metrics = ReviewMetrics(
            start_chapter=data["start_chapter"],
            end_chapter=data["end_chapter"],
            overall_score=data.get("overall_score", 0.0),
            dimension_scores=data.get("dimension_scores", {}),
            severity_counts=data.get("severity_counts", {}),
            critical_issues=data.get("critical_issues", []),
            report_file=data.get("report_file", ""),
            notes=data.get("notes", ""),
        )
        manager.save_review_metrics(metrics)
        emit_success(
            {"start_chapter": metrics.start_chapter, "end_chapter": metrics.end_chapter},
            message="review_metrics_saved",
        )

    elif args.command == "get-recent-review-metrics":
        records = manager.get_recent_review_metrics(args.limit)
        emit_success(records, message="recent_review_metrics")

    elif args.command == "get-review-trend-stats":
        stats = manager.get_review_trend_stats(args.last_n)
        emit_success(stats, message="review_trend_stats")

    elif args.command == "save-writing-checklist-score":
        data = load_json_arg(args.data)
        metrics = WritingChecklistScoreMeta(
            chapter=data["chapter"],
            template=data.get("template", "plot"),
            total_items=data.get("total_items", 0),
            required_items=data.get("required_items", 0),
            completed_items=data.get("completed_items", 0),
            completed_required=data.get("completed_required", 0),
            total_weight=data.get("total_weight", 0.0),
            completed_weight=data.get("completed_weight", 0.0),
            completion_rate=data.get("completion_rate", 0.0),
            score=data.get("score", 0.0),
            score_breakdown=data.get("score_breakdown", {}),
            pending_items=data.get("pending_items", []),
            source=data.get("source", "context_manager"),
            notes=data.get("notes", ""),
        )
        manager.save_writing_checklist_score(metrics)
        emit_success({"chapter": metrics.chapter, "score": metrics.score}, message="writing_checklist_score_saved")

    elif args.command == "get-writing-checklist-score":
        score = manager.get_writing_checklist_score(args.chapter)
        if score:
            emit_success(score, message="writing_checklist_score")
        else:
            emit_error("NOT_FOUND", f"Writing checklist score for chapter {args.chapter} not found")

    elif args.command == "get-recent-writing-checklist-scores":
        scores = manager.get_recent_writing_checklist_scores(args.limit)
        emit_success(scores, message="recent_writing_checklist_scores")

    elif args.command == "get-writing-checklist-score-trend":
        trend = manager.get_writing_checklist_score_trend(args.last_n)
        emit_success(trend, message="writing_checklist_score_trend")

    # ==================== Command processing introduced in v5.3 ====================

    elif args.command == "get-debt-summary":
        summary = manager.get_debt_summary()
        emit_success(summary, message="debt_summary")

    elif args.command == "get-recent-reading-power":
        records = manager.get_recent_reading_power(args.limit)
        emit_success(records, message="recent_reading_power")

    elif args.command == "get-chapter-reading-power":
        record = manager.get_chapter_reading_power(args.chapter)
        if record:
            emit_success(record, message="chapter_reading_power")
        else:
            emit_error("NOT_FOUND", f"Reading power metadata for chapter {args.chapter} not found")

    elif args.command == "get-pattern-usage-stats":
        stats = manager.get_pattern_usage_stats(args.last_n)
        emit_success(stats, message="pattern_usage_stats")

    elif args.command == "get-hook-type-stats":
        stats = manager.get_hook_type_stats(args.last_n)
        emit_success(stats, message="hook_type_stats")

    elif args.command == "get-pending-overrides":
        overrides = manager.get_pending_overrides(args.before_chapter)
        emit_success(overrides, message="pending_overrides")

    elif args.command == "get-overdue-overrides":
        overrides = manager.get_overdue_overrides(args.current_chapter)
        emit_success(overrides, message="overdue_overrides")

    elif args.command == "get-active-debts":
        debts = manager.get_active_debts()
        emit_success(debts, message="active_debts")

    elif args.command == "get-overdue-debts":
        debts = manager.get_overdue_debts(args.current_chapter)
        emit_success(debts, message="overdue_debts")

    elif args.command == "accrue-interest":
        result = manager.accrue_interest(args.current_chapter)
        emit_success(result, message="interest_accrued", chapter=args.current_chapter)

    elif args.command == "pay-debt":
        result = manager.pay_debt(args.debt_id, args.amount, args.chapter)
        if "error" in result:
            emit_error("PAY_DEBT_FAILED", result["error"], chapter=args.chapter)
        else:
            emit_success(result, message="debt_payment", chapter=args.chapter)

    elif args.command == "create-override-contract":
        data = load_json_arg(args.data)
        contract = OverrideContractMeta(
            chapter=data["chapter"],
            constraint_type=data["constraint_type"],
            constraint_id=data["constraint_id"],
            rationale_type=data["rationale_type"],
            rationale_text=data.get("rationale_text", ""),
            payback_plan=data.get("payback_plan", ""),
            due_chapter=data["due_chapter"],
            status=data.get("status", "pending"),
        )
        contract_id = manager.create_override_contract(contract)
        emit_success({"id": contract_id}, message="override_contract_created")

    elif args.command == "create-debt":
        data = load_json_arg(args.data)
        debt = ChaseDebtMeta(
            debt_type=data["debt_type"],
            original_amount=data.get("original_amount", 1.0),
            current_amount=data.get("current_amount", data.get("original_amount", 1.0)),
            interest_rate=data.get("interest_rate", 0.1),
            source_chapter=data["source_chapter"],
            due_chapter=data["due_chapter"],
            override_contract_id=data.get("override_contract_id", 0),
            status=data.get("status", "active"),
        )
        debt_id = manager.create_debt(debt)
        emit_success({"id": debt_id, "debt_type": debt.debt_type}, message="debt_created")

    elif args.command == "fulfill-override":
        success = manager.fulfill_override(args.contract_id)
        if success:
            emit_success({"id": args.contract_id}, message="override_fulfilled")
        else:
            emit_error("NOT_FOUND", f"Override Contract #{args.contract_id} not found")

    elif args.command == "save-chapter-reading-power":
        data = load_json_arg(args.data)
        meta = ChapterReadingPowerMeta(
            chapter=data["chapter"],
            hook_type=data.get("hook_type", ""),
            hook_strength=data.get("hook_strength", "medium"),
            coolpoint_patterns=data.get("coolpoint_patterns", []),
            micropayoffs=data.get("micropayoffs", []),
            hard_violations=data.get("hard_violations", []),
            soft_suggestions=data.get("soft_suggestions", []),
            is_transition=data.get("is_transition", False),
            override_count=data.get("override_count", 0),
            debt_balance=data.get("debt_balance", 0.0),
        )
        manager.save_chapter_reading_power(meta)
        emit_success({"chapter": meta.chapter}, message="reading_power_saved")

    else:
        emit_error("UNKNOWN_COMMAND", "No valid command specified", suggestion="Please see --help")


if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        enable_windows_utf8_stdio()
    main()
