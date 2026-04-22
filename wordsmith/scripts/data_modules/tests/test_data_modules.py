#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Modules Unit Tests
"""

import pytest
import asyncio
import json
import tempfile
import sys
from pathlib import Path

from data_modules import (
    DataModulesConfig,
    EntityLinker,
    StateManager,
    IndexManager,
    RAGAdapter,
    StyleSampler,
    EntityState,
    ChapterMeta,
    SceneMeta,
    StyleSample,
)
import data_modules.index_manager as index_manager_module
from data_modules.index_manager import (
    EntityMeta,
    StateChangeMeta,
    RelationshipMeta,
    OverrideContractMeta,
    ChaseDebtMeta,
    ChapterReadingPowerMeta,
    ReviewMetrics,
    WritingChecklistScoreMeta,
)


@pytest.fixture
def temp_project():
    """Create temporary project directory"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = DataModulesConfig.from_project_root(tmpdir)
        config.ensure_dirs()
        yield config


class TestEntityLinker:
    """Entity Linker Tests"""

    def test_register_and_lookup_alias(self, temp_project):
        linker = EntityLinker(temp_project)
        # First register entity, otherwise aliases JOIN won't return
        IndexManager(temp_project).upsert_entity(
            EntityMeta(
                id="xiaoyan",
                type="Character",
                canonical_name="Xiao Yan",
                current={},
                first_appearance=1,
                last_appearance=1,
            )
        )

        # Register alias
        assert linker.register_alias("xiaoyan", "Xiao Yan")
        assert linker.register_alias("xiaoyan", "Little Yan")

        # Lookup
        assert linker.lookup_alias("Xiao Yan") == "xiaoyan"
        assert linker.lookup_alias("Little Yan") == "xiaoyan"
        assert linker.lookup_alias("Does not exist") is None

    def test_alias_one_to_many(self, temp_project):
        """v5.0: Same alias can map to multiple entities (one-to-many)"""
        linker = EntityLinker(temp_project)

        idx = IndexManager(temp_project)
        idx.upsert_entity(
            EntityMeta(
                id="xiaoyan",
                type="Character",
                canonical_name="Xiao Yan",
                current={},
                first_appearance=1,
                last_appearance=1,
            )
        )
        idx.upsert_entity(
            EntityMeta(
                id="other_person",
                type="Character",
                canonical_name="Xiao Yan",
                current={},
                first_appearance=1,
                last_appearance=1,
            )
        )

        linker.register_alias("xiaoyan", "Xiao Yan", "Character")
        # v5.0: Same alias can bind different entities (one-to-many)
        assert linker.register_alias("other_person", "Xiao Yan", "Character")

        # Lookup all matches
        entries = linker.lookup_alias_all("Xiao Yan")
        assert len(entries) == 2

    def test_get_all_aliases(self, temp_project):
        linker = EntityLinker(temp_project)
        IndexManager(temp_project).upsert_entity(
            EntityMeta(
                id="xiaoyan",
                type="Character",
                canonical_name="Xiao Yan",
                current={},
                first_appearance=1,
                last_appearance=1,
            )
        )

        linker.register_alias("xiaoyan", "Xiao Yan")
        linker.register_alias("xiaoyan", "Little Yan")
        linker.register_alias("xiaoyan", "Brother Yan")

        aliases = linker.get_all_aliases("xiaoyan")
        assert len(aliases) == 3
        assert "Xiao Yan" in aliases

    def test_confidence_evaluation(self, temp_project):
        linker = EntityLinker(temp_project)

        # High confidence
        action, adopt, warning = linker.evaluate_confidence(0.9)
        assert action == "auto"
        assert adopt is True
        assert warning is None

        # Medium confidence
        action, adopt, warning = linker.evaluate_confidence(0.6)
        assert action == "warn"
        assert adopt is True
        assert warning is not None

        # Low confidence
        action, adopt, warning = linker.evaluate_confidence(0.3)
        assert action == "manual"
        assert adopt is False

    def test_process_uncertain(self, temp_project):
        linker = EntityLinker(temp_project)

        result = linker.process_uncertain(
            mention="That senior",
            candidates=["yaolao", "elder_zhang"],
            suggested="yaolao",
            confidence=0.7
        )

        assert result.mention == "That senior"
        assert result.entity_id == "yaolao"
        assert result.adopted is True
        assert result.warning is not None


class TestStateManager:
    """State Manager Tests"""

    def test_add_and_get_entity(self, temp_project):
        manager = StateManager(temp_project)

        entity = EntityState(
            id="xiaoyan",
            name="Xiao Yan",
            type="Character",
            tier="Core"
        )
        assert manager.add_entity(entity)

        # Get entity
        result = manager.get_entity("xiaoyan")
        assert result is not None
        assert result["canonical_name"] == "Xiao Yan"

    def test_update_entity(self, temp_project):
        manager = StateManager(temp_project)

        entity = EntityState(id="xiaoyan", name="Xiao Yan", type="Character")
        manager.add_entity(entity)

        # Update attributes (v5.0: attributes stored in current field)
        manager.update_entity("xiaoyan", {"current": {"realm": "Battle Master"}})

        result = manager.get_entity("xiaoyan")
        assert result["current"]["realm"] == "Battle Master"

    def test_record_state_change(self, temp_project):
        manager = StateManager(temp_project)

        entity = EntityState(id="xiaoyan", name="Xiao Yan", type="Character")
        manager.add_entity(entity)

        manager.record_state_change(
            entity_id="xiaoyan",
            field="realm",
            old_value="Fighter stage",
            new_value="Battle Master",
            reason="Breakthrough",
            chapter=100
        )

        changes = manager.get_state_changes("xiaoyan")
        assert len(changes) == 1
        assert changes[0]["new_value"] == "Battle Master"

    def test_add_relationship(self, temp_project):
        manager = StateManager(temp_project)

        manager.add_relationship(
            from_entity="xiaoyan",
            to_entity="yaolao",
            rel_type="Master-disciple",
            description="Elder Yao takes Xiao Yan as disciple",
            chapter=10
        )

        rels = manager.get_relationships("xiaoyan")
        assert len(rels) == 1
        assert rels[0]["type"] == "Master-disciple"

    def test_process_chapter_result(self, temp_project):
        manager = StateManager(temp_project)

        result = {
            "entities_appeared": [
                {"id": "xiaoyan", "mentions": ["Xiao Yan", "him"]}
            ],
            "entities_new": [
                {"suggested_id": "hongyi_girl", "name": "Red-clothed girl", "type": "Character", "tier": "Decoration"}
            ],
            "state_changes": [
                {"entity_id": "xiaoyan", "field": "realm", "old": "Fighter stage", "new": "Battle Master", "reason": "Breakthrough"}
            ],
            "relationships_new": [
                {"from": "xiaoyan", "to": "hongyi_girl", "type": "Acquaintance", "description": "First meeting"}
            ]
        }

        # First add xiaoyan
        manager.add_entity(EntityState(id="xiaoyan", name="Xiao Yan", type="Character"))

        warnings = manager.process_chapter_result(100, result)

        # Verify new entity added
        assert manager.get_entity("hongyi_girl") is not None

        # Verify state changes
        changes = manager.get_state_changes("xiaoyan")
        assert len(changes) == 1

        # Verify progress updated
        assert manager.get_current_chapter() == 100

    def test_save_state_with_init_project_schema(self, temp_project):
        """Regression: state.json generated by init_project, StateManager should still be writable. (v5.1 SQLite-only)"""
        # v5.1: state.json no longer contains entities_v3/alias_index, entity data in SQLite
        init_state = {
            "project_info": {"title": "Test book title", "genre": "Cultivation/Fantasy", "created_at": "2026-01-01"},
            "progress": {"current_chapter": 0, "total_words": 0, "last_updated": "2026-01-01 00:00:00"},
            "protagonist_state": {"name": "Test protagonist"},
            "relationships": {},
            "world_settings": {"power_system": [], "factions": [], "locations": []},
            "plot_threads": {"active_threads": [], "foreshadowing": []},
            "review_checkpoints": [],
            "strand_tracker": {"current_dominant": "quest", "history": []},
        }
        temp_project.state_file.write_text(json.dumps(init_state, ensure_ascii=False, indent=2), encoding="utf-8")

        manager = StateManager(temp_project)
        manager.update_progress(5, words=100)
        manager.save_state()

        saved = json.loads(temp_project.state_file.read_text(encoding="utf-8"))
        assert "meta" not in saved
        assert saved["progress"]["current_chapter"] == 5
        assert saved["progress"]["total_words"] == 100
        # v5.1: entities_v3/alias_index no longer in state.json

    def test_save_state_preserves_unrelated_fields(self, temp_project):
        """Regression: Only write increments, should not overwrite/lose fields maintained by other modules. (v5.1 SQLite-only)"""
        init_state = {
            "project_info": {"title": "Test book title", "genre": "Cultivation/Fantasy", "created_at": "2026-01-01"},
            "progress": {"current_chapter": 10, "total_words": 1000, "last_updated": "2026-01-01 00:00:00"},
            "protagonist_state": {"name": "Test protagonist"},
            "relationships": {"allies": ["Elder Yao"], "enemies": []},
            "world_settings": {"power_system": [], "factions": [], "locations": []},
            "plot_threads": {"active_threads": [{"id": "t1", "title": "Main plot"}], "foreshadowing": []},
            "review_checkpoints": [],
            "strand_tracker": {"current_dominant": "quest", "history": []},
            "custom_field": {"keep": True},
        }
        temp_project.state_file.write_text(json.dumps(init_state, ensure_ascii=False, indent=2), encoding="utf-8")

        manager = StateManager(temp_project)
        manager.add_entity(EntityState(id="xiaoyan", name="Xiao Yan", type="Character", tier="Core"))
        manager.save_state()

        saved = json.loads(temp_project.state_file.read_text(encoding="utf-8"))
        assert saved.get("custom_field", {}).get("keep") is True
        assert saved.get("plot_threads", {}).get("active_threads", [])[0].get("id") == "t1"
        assert isinstance(saved.get("relationships"), dict)

    def test_disambiguation_feedback_persisted(self, temp_project):
        """Regression: Medium/low confidence disambiguation must be visible to Writer (write to state.json)."""
        manager = StateManager(temp_project)

        result = {
            "entities_appeared": [],
            "entities_new": [],
            "state_changes": [],
            "relationships_new": [],
            "uncertain": [
                {
                    "mention": "That senior",
                    "context": "That seniorglanced at him",
                    "candidates": [{"type": "Character", "id": "yaolao"}, {"type": "Character", "id": "elder_zhang"}],
                    "suggested": "yaolao",
                    "confidence": 0.6,
                },
                {
                    "mention": "Sect Master",
                    "context": "Sect Masterappears inBlood Evil Secret Realm",
                    "candidates": ["xueshazonzhu", "lintian"],
                    "suggested": "xueshazonzhu",
                    "confidence": 0.4,
                },
            ],
        }

        warnings = manager.process_chapter_result(100, result)
        manager.save_state()

        state = json.loads(temp_project.state_file.read_text(encoding="utf-8"))
        assert isinstance(state.get("disambiguation_warnings"), list)
        assert isinstance(state.get("disambiguation_pending"), list)

        assert len(state["disambiguation_warnings"]) == 1
        assert len(state["disambiguation_pending"]) == 1

        warn = state["disambiguation_warnings"][0]
        assert warn.get("chapter") == 100
        assert warn.get("mention") == "That senior"
        assert warn.get("chosen_id") == "yaolao"

        pending = state["disambiguation_pending"][0]
        assert pending.get("chapter") == 100
        assert pending.get("mention") == "Sect Master"

        # Return value should also contain visible warnings for CLI/log output
        assert any("Disambiguation warning" in w for w in warnings)
        assert any("Requires manual confirmation" in w for w in warnings)


class TestIndexManager:
    """Index Manager Tests"""

    def test_add_and_get_chapter(self, temp_project):
        manager = IndexManager(temp_project)

        meta = ChapterMeta(
            chapter=100,
            title="Breakthrough",
            location="Tianyun Sect",
            word_count=3500,
            characters=["xiaoyan", "yaolao"]
        )
        manager.add_chapter(meta)

        result = manager.get_chapter(100)
        assert result is not None
        assert result["title"] == "Breakthrough"
        assert "xiaoyan" in result["characters"]

    def test_add_scenes(self, temp_project):
        manager = IndexManager(temp_project)

        scenes = [
            SceneMeta(chapter=100, scene_index=1, start_line=1, end_line=50,
                     location="Tianyun Sect Secluded Chamber", summary="Xiao YanSecluded training breakthrough", characters=["xiaoyan"]),
            SceneMeta(chapter=100, scene_index=2, start_line=51, end_line=100,
                     location="Tianyun Sect Martial Arts Arena", summary="Display strength", characters=["xiaoyan", "lintian"])
        ]
        manager.add_scenes(100, scenes)

        result = manager.get_scenes(100)
        assert len(result) == 2
        assert result[0]["location"] == "Tianyun Sect Secluded Chamber"

    def test_record_appearance(self, temp_project):
        manager = IndexManager(temp_project)

        manager.record_appearance("xiaoyan", 100, ["Xiao Yan", "him"], 0.95)
        manager.record_appearance("yaolao", 100, ["Elder Yao"], 0.92)

        appearances = manager.get_chapter_appearances(100)
        assert len(appearances) == 2

        entity_history = manager.get_entity_appearances("xiaoyan")
        assert len(entity_history) == 1

    def test_search_scenes_by_location(self, temp_project):
        manager = IndexManager(temp_project)

        scenes = [
            SceneMeta(chapter=100, scene_index=1, start_line=1, end_line=50,
                     location="Tianyun Sect Secluded Chamber", summary="Secluded training", characters=[]),
            SceneMeta(chapter=101, scene_index=1, start_line=1, end_line=50,
                     location="Tianyun Sect Main Hall", summary="Discuss affairs", characters=[])
        ]
        manager.add_scenes(100, scenes[:1])
        manager.add_scenes(101, scenes[1:])

        results = manager.search_scenes_by_location("Tianyun Sect")
        assert len(results) == 2

    def test_get_stats(self, temp_project):
        manager = IndexManager(temp_project)

        manager.upsert_entity(
            EntityMeta(
                id="xiaoyan",
                type="Character",
                canonical_name="Xiao Yan",
                current={},
                first_appearance=1,
                last_appearance=1,
            )
        )
        manager.add_chapter(ChapterMeta(chapter=1, title="", location="", word_count=1000, characters=[]))
        manager.add_scenes(1, [SceneMeta(chapter=1, scene_index=1, start_line=1, end_line=50,
                                        location="", summary="", characters=[])])
        manager.record_appearance("xiaoyan", 1, [], 1.0)

        stats = manager.get_stats()
        assert stats["chapters"] == 1
        assert stats["scenes"] == 1
        assert stats["entities"] == 1

    def test_entity_alias_and_relationships(self, temp_project):
        manager = IndexManager(temp_project)

        entity_main = EntityMeta(
            id="xiaoyan",
            type="Character",
            canonical_name="Xiao Yan",
            tier="Core",
            desc="Protagonist",
            current={"realm": "Fighter stage"},
            first_appearance=1,
            last_appearance=1,
            is_protagonist=True,
        )
        entity_other = EntityMeta(
            id="yaolao",
            type="Character",
            canonical_name="Elder Yao",
            tier="Important",
            current={},
            first_appearance=1,
            last_appearance=2,
        )

        assert manager.upsert_entity(entity_main) is True
        assert manager.upsert_entity(entity_other) is True

        # Update current
        assert manager.update_entity_current("xiaoyan", {"realm": "Battle Master"}) is True
        entity = manager.get_entity("xiaoyan")
        assert entity["current_json"]["realm"] == "Battle Master"

        # Metadata update
        entity_main.desc = "Protagonist(Updated)"
        entity_main.last_appearance = 3
        assert manager.upsert_entity(entity_main, update_metadata=True) is False

        # Alias management
        assert manager.register_alias("Flame Emperor", "xiaoyan", "Character")
        assert "Flame Emperor" in manager.get_entity_aliases("xiaoyan")
        assert manager.get_entities_by_alias("Flame Emperor")[0]["id"] == "xiaoyan"
        assert manager.remove_alias("Flame Emperor", "xiaoyan")
        assert manager.get_entities_by_alias("Flame Emperor") == []

        # Type/tier/core/protagonist queries
        assert len(manager.get_entities_by_type("Character")) == 2
        assert any(e["id"] == "xiaoyan" for e in manager.get_entities_by_tier("Core"))
        assert any(e["id"] == "xiaoyan" for e in manager.get_core_entities())
        assert manager.get_protagonist()["id"] == "xiaoyan"

        # Archive entity
        assert manager.archive_entity("yaolao") is True
        assert all(e["id"] != "yaolao" for e in manager.get_entities_by_type("Character"))
        assert any(
            e["id"] == "yaolao"
            for e in manager.get_entities_by_type("Character", include_archived=True)
        )

        # Relationship management (create + update)
        rel = RelationshipMeta(
            from_entity="xiaoyan",
            to_entity="yaolao",
            type="Master-disciple",
            description="Accept disciple",
            chapter=1,
        )
        assert manager.upsert_relationship(rel) is True
        rel.description = "Accept disciple(Updated)"
        rel.chapter = 2
        assert manager.upsert_relationship(rel) is False

        assert len(manager.get_entity_relationships("xiaoyan", "from")) == 1
        assert len(manager.get_entity_relationships("yaolao", "to")) == 1
        assert len(manager.get_entity_relationships("xiaoyan", "both")) >= 1
        assert len(manager.get_relationship_between("xiaoyan", "yaolao")) == 1
        assert len(manager.get_recent_relationships(limit=5)) >= 1

    def test_state_changes_and_appearances(self, temp_project):
        manager = IndexManager(temp_project)

        entity = EntityMeta(
            id="xiaoyan",
            type="Character",
            canonical_name="Xiao Yan",
            current={},
            first_appearance=1,
            last_appearance=1,
        )
        manager.upsert_entity(entity)

        change = StateChangeMeta(
            entity_id="xiaoyan",
            field="realm",
            old_value="Fighter stage",
            new_value="Battle Master",
            reason="Breakthrough",
            chapter=2,
        )
        change_id = manager.record_state_change(change)
        assert change_id > 0

        assert len(manager.get_entity_state_changes("xiaoyan")) == 1
        assert len(manager.get_recent_state_changes(limit=5)) == 1
        assert len(manager.get_chapter_state_changes(2)) == 1

        # Appearance records (including skip_if_exists branch)
        manager.record_appearance("xiaoyan", 2, ["Xiao Yan"], 1.0)
        manager.record_appearance("xiaoyan", 2, ["Xiao Yan"], 1.0, skip_if_exists=True)
        manager.record_appearance("xiaoyan", 3, ["Xiao Yan"], 1.0)

        assert len(manager.get_entity_appearances("xiaoyan")) == 2
        assert len(manager.get_recent_appearances(limit=5)) >= 1
        assert len(manager.get_chapter_appearances(2)) == 1

    def test_chapter_queries_and_bulk(self, temp_project):
        manager = IndexManager(temp_project)

        manager.add_chapter(
            ChapterMeta(
                chapter=1,
                title="Starting point",
                location="Tianyun Sect",
                word_count=1000,
                characters=["xiaoyan"],
            )
        )
        manager.add_chapter(
            ChapterMeta(
                chapter=2,
                title="Breakthrough",
                location="Tianyun Sect",
                word_count=1200,
                characters=["xiaoyan", "yaolao"],
            )
        )

        recent = manager.get_recent_chapters()
        assert recent[0]["chapter"] == 2

        scenes = [
            SceneMeta(
                chapter=1,
                scene_index=1,
                start_line=1,
                end_line=50,
                location="Tianyun Sect Secluded Chamber",
                summary="Secluded training",
                characters=["xiaoyan"],
            ),
            SceneMeta(
                chapter=1,
                scene_index=2,
                start_line=51,
                end_line=80,
                location="Tianyun Sect Martial Arts Arena",
                summary="Practice",
                characters=["xiaoyan"],
            ),
        ]
        manager.add_scenes(1, scenes)
        assert len(manager.get_scenes(1)) == 2

        results = manager.search_scenes_by_location("Tianyun Sect")
        assert len(results) >= 2

        stats = manager.process_chapter_data(
            chapter=10,
            title="Trial",
            location="Secret realm",
            word_count=1500,
            entities=[{"id": "xiaoyan", "type": "Character", "mentions": ["Xiao Yan"]}],
            scenes=[{"index": 1, "start_line": 1, "end_line": 20, "location": "Secret realm", "summary": "Opening", "characters": ["xiaoyan"]}],
        )
        assert stats["chapters"] == 1
        assert stats["scenes"] == 1
        assert stats["appearances"] == 1

    def test_debt_and_override_flow(self, temp_project):
        manager = IndexManager(temp_project)

        contract = OverrideContractMeta(
            chapter=1,
            constraint_type="SOFT_MICROPAYOFF",
            constraint_id="micropayoff_count",
            rationale_type="TRANSITIONAL_SETUP",
            rationale_text="Setup needs",
            payback_plan="Next chapterCompensation",
            due_chapter=3,
            status="pending",
        )
        contract_id = manager.create_override_contract(contract)
        assert contract_id > 0

        # pending status allows update
        contract.rationale_text = "Adjustment reason"
        contract.due_chapter = 4
        assert manager.create_override_contract(contract) == contract_id
        updated = manager.get_chapter_overrides(1)[0]
        assert updated["rationale_text"] == "Adjustment reason"
        assert updated["due_chapter"] == 4

        # Final state frozen
        contract.status = "fulfilled"
        contract.rationale_text = "Final state reason"
        contract.due_chapter = 5
        manager.create_override_contract(contract)
        frozen = manager.get_chapter_overrides(1)[0]
        assert frozen["status"] == "fulfilled"
        assert frozen["rationale_text"] == "Final state reason"

        # Try to write back to pending, should not change final state fields
        contract.status = "pending"
        contract.rationale_text = "Should not take effect"
        contract.due_chapter = 99
        manager.create_override_contract(contract)
        frozen_again = manager.get_chapter_overrides(1)[0]
        assert frozen_again["status"] == "fulfilled"
        assert frozen_again["rationale_text"] == "Final state reason"
        assert frozen_again["due_chapter"] == 5

        debt_contract_id = manager.create_override_contract(
            OverrideContractMeta(
                chapter=2,
                constraint_type="SOFT_HOOK_STRENGTH",
                constraint_id="hook_strength",
                rationale_type="ARC_TIMING",
                rationale_text="Pacing arrangement",
                payback_plan="Follow-up reinforcement",
                due_chapter=4,
                status="pending",
            )
        )

        debt1 = ChaseDebtMeta(
            debt_type="hook_strength",
            original_amount=1.0,
            current_amount=1.0,
            interest_rate=0.1,
            source_chapter=1,
            due_chapter=2,
            override_contract_id=debt_contract_id,
            status="active",
        )
        debt2 = ChaseDebtMeta(
            debt_type="micropayoff",
            original_amount=2.0,
            current_amount=2.0,
            interest_rate=0.2,
            source_chapter=1,
            due_chapter=2,
            override_contract_id=debt_contract_id,
            status="active",
        )
        debt_id_1 = manager.create_debt(debt1)
        debt_id_2 = manager.create_debt(debt2)
        assert len(manager.get_active_debts()) == 2
        assert manager.get_total_debt_balance() > 0

        # Interest accrual and idempotent protection
        result = manager.accrue_interest(current_chapter=2)
        assert result["debts_processed"] == 2
        result_again = manager.accrue_interest(current_chapter=2)
        assert result_again["skipped_already_processed"] == 2

        # Overdue marking
        result_overdue = manager.accrue_interest(current_chapter=3)
        assert result_overdue["new_overdues"] >= 1
        overdue = manager.get_overdue_debts(current_chapter=3)
        assert any(d["status"] == "overdue" for d in overdue)
        history = manager.get_debt_history(debt_id_1)
        assert any(h["event_type"] == "interest_accrued" for h in history)

        # Amount validation
        error = manager.pay_debt(debt_id_1, 0, chapter=3)
        assert "error" in error

        # Partial repayment
        partial = manager.pay_debt(debt_id_1, 0.5, chapter=3)
        assert partial["fully_paid"] is False

        # Full repayment (when another debt still exists, should not fulfilled)
        full = manager.pay_debt(debt_id_1, 100, chapter=3)
        assert full["fully_paid"] is True
        assert full["override_fulfilled"] is False

        # Clear last debt -> fulfilled
        full2 = manager.pay_debt(debt_id_2, 100, chapter=3)
        assert full2["fully_paid"] is True
        assert full2["override_fulfilled"] is True

    def test_reading_power_and_debt_summary(self, temp_project):
        manager = IndexManager(temp_project)

        # Reading power metadata
        manager.save_chapter_reading_power(
            ChapterReadingPowerMeta(
                chapter=1,
                hook_type="Desire hook",
                hook_strength="strong",
                coolpoint_patterns=["Authority slap", "Identity reveal"],
                micropayoffs=["Ability redemption"],
                hard_violations=[],
                soft_suggestions=["SOFT_HOOK_STRENGTH"],
                is_transition=False,
                override_count=1,
                debt_balance=1.5,
            )
        )
        manager.save_chapter_reading_power(
            ChapterReadingPowerMeta(
                chapter=2,
                hook_type="Suspense hook",
                hook_strength="medium",
                coolpoint_patterns=["Identity reveal"],
                micropayoffs=["Information redemption"],
                hard_violations=["HARD-004"],
                soft_suggestions=[],
                is_transition=True,
                override_count=0,
                debt_balance=0.0,
            )
        )

        record = manager.get_chapter_reading_power(1)
        assert record["hook_type"] == "Desire hook"
        assert "Identity reveal" in record["coolpoint_patterns"]
        assert record["is_transition"] == 0  # SQLite stores as 0/1
        assert manager.get_chapter_reading_power(999) is None

        recent = manager.get_recent_reading_power(limit=2)
        assert len(recent) == 2

        pattern_stats = manager.get_pattern_usage_stats(last_n_chapters=5)
        assert pattern_stats.get("Identity reveal") == 2

        hook_stats = manager.get_hook_type_stats(last_n_chapters=5)
        assert hook_stats.get("Desire hook") == 1

        # Debt summary
        contract_id = manager.create_override_contract(
            OverrideContractMeta(
                chapter=3,
                constraint_type="SOFT_HOOK_STRENGTH",
                constraint_id="hook_strength",
                rationale_type="ARC_TIMING",
                rationale_text="Pacing arrangement",
                payback_plan="Follow-up reinforcement",
                due_chapter=5,
                status="pending",
            )
        )
        manager.create_debt(
            ChaseDebtMeta(
                debt_type="hook_strength",
                original_amount=1.0,
                current_amount=1.0,
                interest_rate=0.1,
                source_chapter=3,
                due_chapter=4,
                override_contract_id=contract_id,
                status="active",
            )
        )
        manager.create_debt(
            ChaseDebtMeta(
                debt_type="micropayoff",
                original_amount=2.0,
                current_amount=2.0,
                interest_rate=0.1,
                source_chapter=3,
                due_chapter=4,
                override_contract_id=0,
                status="overdue",
            )
        )

        summary = manager.get_debt_summary()
        assert summary["active_debts"] == 1
        assert summary["overdue_debts"] == 1
        assert summary["pending_overrides"] >= 1
        assert summary["total_balance"] == summary["active_total"] + summary["overdue_total"]

        pending = manager.get_pending_overrides()
        assert any(o["id"] == contract_id for o in pending)
        pending_before = manager.get_pending_overrides(before_chapter=10)
        assert any(o["id"] == contract_id for o in pending_before)
        overdue_overrides = manager.get_overdue_overrides(current_chapter=6)
        assert any(o["id"] == contract_id for o in overdue_overrides)

        other_id = manager.create_override_contract(
            OverrideContractMeta(
                chapter=4,
                constraint_type="SOFT_EXPECTATION_OVERLOAD",
                constraint_id="expectation_count",
                rationale_type="EDITORIAL_INTENT",
                rationale_text="Author intent",
                payback_plan="Follow-up supplement",
                due_chapter=6,
                status="pending",
            )
        )
        assert manager.fulfill_override(other_id) is True
        assert manager.get_chapter_overrides(4)[0]["status"] == "fulfilled"

    def test_review_metrics_and_trends(self, temp_project):
        manager = IndexManager(temp_project)

        manager.save_review_metrics(
            ReviewMetrics(
                start_chapter=1,
                end_chapter=1,
                overall_score=48,
                dimension_scores={
                    "Cool point density": 8,
                    "Setting consistency": 7,
                    "Pacing control": 7,
                    "Character development": 8,
                    "Coherence": 9,
                    "Reading engagement": 9,
                },
                severity_counts={"critical": 0, "high": 1, "medium": 2, "low": 0},
                critical_issues=[],
                report_file="Review report/Ch1-1_review_report.md",
            )
        )
        manager.save_review_metrics(
            ReviewMetrics(
                start_chapter=2,
                end_chapter=2,
                overall_score=42,
                dimension_scores={
                    "Cool point density": 6,
                    "Setting consistency": 8,
                    "Pacing control": 7,
                    "Character development": 7,
                    "Coherence": 7,
                    "Reading engagement": 7,
                },
                severity_counts={"critical": 1, "high": 0, "medium": 1, "low": 2},
                critical_issues=["Setting contradiction"],
                report_file="Review report/Ch2-2_review_report.md",
            )
        )

        recent = manager.get_recent_review_metrics(limit=2)
        assert len(recent) == 2

        trends = manager.get_review_trend_stats(last_n=5)
        assert trends["count"] == 2
        assert trends["overall_avg"] > 0
        assert "Cool point density" in trends["dimension_avg"]

    def test_writing_checklist_score_persistence_and_trend(self, temp_project):
        manager = IndexManager(temp_project)

        manager.save_writing_checklist_score(
            WritingChecklistScoreMeta(
                chapter=10,
                template="plot",
                total_items=6,
                required_items=4,
                completed_items=4,
                completed_required=3,
                total_weight=6.2,
                completed_weight=4.1,
                completion_rate=0.6667,
                score=78.5,
                score_breakdown={"weighted_completion_rate": 0.66},
                pending_items=["Hook at end of segment"],
            )
        )
        manager.save_writing_checklist_score(
            WritingChecklistScoreMeta(
                chapter=11,
                template="plot",
                total_items=6,
                required_items=4,
                completed_items=5,
                completed_required=4,
                total_weight=6.2,
                completed_weight=5.4,
                completion_rate=0.8333,
                score=86.0,
                score_breakdown={"weighted_completion_rate": 0.87},
                pending_items=[],
            )
        )

        one = manager.get_writing_checklist_score(10)
        assert one is not None
        assert one["chapter"] == 10
        assert one["score"] == 78.5

        recent = manager.get_recent_writing_checklist_scores(limit=2)
        assert len(recent) == 2
        assert recent[0]["chapter"] == 11

        trend = manager.get_writing_checklist_score_trend(last_n=5)
        assert trend["count"] == 2
        assert trend["score_avg"] > 0
        assert trend["completion_avg"] > 0

    def test_index_manager_cli(self, temp_project, monkeypatch, capsys):
        root = str(temp_project.project_root)
        manager = IndexManager(temp_project)

        # Basic data
        manager.upsert_entity(
            EntityMeta(
                id="xiaoyan",
                type="Character",
                canonical_name="Xiao Yan",
                tier="Core",
                current={"realm": "Fighter stage"},
                first_appearance=1,
                last_appearance=1,
                is_protagonist=True,
            )
        )
        manager.upsert_entity(
            EntityMeta(
                id="yaolao",
                type="Character",
                canonical_name="Elder Yao",
                tier="Important",
                current={},
                first_appearance=1,
                last_appearance=2,
            )
        )

        manager.register_alias("Flame Emperor", "xiaoyan", "Character")
        manager.add_chapter(
            ChapterMeta(
                chapter=1,
                title="Starting point",
                location="Tianyun Sect",
                word_count=1000,
                characters=["xiaoyan"],
            )
        )
        manager.add_scenes(
            1,
            [
                SceneMeta(
                    chapter=1,
                    scene_index=1,
                    start_line=1,
                    end_line=20,
                    location="Tianyun Sect Secluded Chamber",
                    summary="Secluded training",
                    characters=["xiaoyan"],
                )
            ],
        )
        manager.record_appearance("xiaoyan", 1, ["Xiao Yan"], 1.0)
        manager.record_state_change(
            StateChangeMeta(
                entity_id="xiaoyan",
                field="realm",
                old_value="Fighter stage",
                new_value="Battle Master",
                reason="Breakthrough",
                chapter=1,
            )
        )
        manager.upsert_relationship(
            RelationshipMeta(
                from_entity="xiaoyan",
                to_entity="yaolao",
                type="Master-disciple",
                description="Accept disciple",
                chapter=1,
            )
        )

        # Reading power and debt
        manager.save_chapter_reading_power(
            ChapterReadingPowerMeta(
                chapter=1,
                hook_type="Desire hook",
                hook_strength="medium",
                coolpoint_patterns=["Identity reveal"],
                micropayoffs=["Ability redemption"],
                hard_violations=[],
                soft_suggestions=[],
            )
        )
        contract_id = manager.create_override_contract(
            OverrideContractMeta(
                chapter=1,
                constraint_type="SOFT_HOOK_STRENGTH",
                constraint_id="hook_strength",
                rationale_type="ARC_TIMING",
                rationale_text="Pacing arrangement",
                payback_plan="Follow-up reinforcement",
                due_chapter=2,
                status="pending",
            )
        )
        debt_id = manager.create_debt(
            ChaseDebtMeta(
                debt_type="hook_strength",
                original_amount=1.0,
                current_amount=1.0,
                interest_rate=0.1,
                source_chapter=1,
                due_chapter=2,
                override_contract_id=contract_id,
                status="active",
            )
        )

        def run_cli(args):
            monkeypatch.setattr(sys, "argv", ["index_manager"] + args)
            index_manager_module.main()

        # Basic commands
        run_cli(["--project-root", root, "stats"])
        run_cli(["--project-root", root, "get-chapter", "--chapter", "1"])
        run_cli(["--project-root", root, "get-chapter", "--chapter", "99"])
        run_cli(["--project-root", root, "recent-appearances", "--limit", "5"])
        run_cli(["--project-root", root, "entity-appearances", "--entity", "xiaoyan", "--limit", "5"])
        run_cli(["--project-root", root, "search-scenes", "--location", "Tianyun Sect", "--limit", "5"])

        # Process chapter
        run_cli(
            [
                "--project-root",
                root,
                "process-chapter",
                "--chapter",
                "2",
                "--title",
                "Trial",
                "--location",
                "Secret realm",
                "--word-count",
                "1200",
                "--entities",
                json.dumps([{"id": "xiaoyan", "mentions": ["Xiao Yan"]}], ensure_ascii=False),
                "--scenes",
                json.dumps(
                    [
                        {
                            "index": 1,
                            "start_line": 1,
                            "end_line": 10,
                            "location": "Secret realm",
                            "summary": "Opening",
                            "characters": ["xiaoyan"],
                        }
                    ],
                    ensure_ascii=False,
                ),
            ]
        )

        # v5.1 commands
        run_cli(["--project-root", root, "get-entity", "--id", "xiaoyan"])
        run_cli(["--project-root", root, "get-entity", "--id", "missing"])
        run_cli(["--project-root", root, "get-core-entities"])
        run_cli(["--project-root", root, "get-protagonist"])
        run_cli(
            ["--project-root", root, "get-entities-by-type", "--type", "Character", "--include-archived"]
        )
        run_cli(["--project-root", root, "get-by-alias", "--alias", "Flame Emperor"])
        run_cli(["--project-root", root, "get-by-alias", "--alias", "Does not exist"])
        run_cli(["--project-root", root, "get-aliases", "--entity", "xiaoyan"])
        run_cli(["--project-root", root, "register-alias", "--alias", "Brother Yan", "--entity", "xiaoyan", "--type", "Character"])
        run_cli(["--project-root", root, "get-relationships", "--entity", "xiaoyan", "--direction", "from"])
        run_cli(["--project-root", root, "get-state-changes", "--entity", "xiaoyan", "--limit", "20"])
        run_cli(
            [
                "--project-root",
                root,
                "upsert-entity",
                "--data",
                json.dumps(
                    {
                        "id": "lintian",
                        "type": "Character",
                        "canonical_name": "Lin Tian",
                        "tier": "Decoration",
                        "current": {"realm": "Fighter stage"},
                    },
                    ensure_ascii=False,
                ),
            ]
        )
        run_cli(
            [
                "--project-root",
                root,
                "upsert-relationship",
                "--data",
                json.dumps(
                    {
                        "from_entity": "xiaoyan",
                        "to_entity": "lintian",
                        "type": "Acquaintance",
                        "description": "First encounter",
                        "chapter": 2,
                    },
                    ensure_ascii=False,
                ),
            ]
        )
        run_cli(
            [
                "--project-root",
                root,
                "record-state-change",
                "--data",
                json.dumps(
                    {
                        "entity_id": "xiaoyan",
                        "field": "realm",
                        "old_value": "Fighter stage",
                        "new_value": "Battle Master",
                        "reason": "Breakthrough",
                        "chapter": 2,
                    },
                    ensure_ascii=False,
                ),
            ]
        )

        # v5.3 commands
        run_cli(["--project-root", root, "get-debt-summary"])
        run_cli(["--project-root", root, "get-recent-reading-power", "--limit", "5"])
        run_cli(["--project-root", root, "get-chapter-reading-power", "--chapter", "1"])
        run_cli(["--project-root", root, "get-chapter-reading-power", "--chapter", "99"])
        run_cli(["--project-root", root, "get-pattern-usage-stats", "--last-n", "5"])
        run_cli(["--project-root", root, "get-hook-type-stats", "--last-n", "5"])
        run_cli(["--project-root", root, "get-pending-overrides"])
        run_cli(["--project-root", root, "get-overdue-overrides", "--current-chapter", "3"])
        run_cli(["--project-root", root, "get-active-debts"])
        run_cli(["--project-root", root, "get-overdue-debts", "--current-chapter", "3"])
        run_cli(["--project-root", root, "accrue-interest", "--current-chapter", "3"])
        run_cli(["--project-root", root, "pay-debt", "--debt-id", str(debt_id), "--amount", "0", "--chapter", "3"])
        run_cli(["--project-root", root, "pay-debt", "--debt-id", str(debt_id), "--amount", "5", "--chapter", "3"])
        run_cli(
            [
                "--project-root",
                root,
                "create-override-contract",
                "--data",
                json.dumps(
                    {
                        "chapter": 3,
                        "constraint_type": "SOFT_MICROPAYOFF",
                        "constraint_id": "micropayoff_count",
                        "rationale_type": "TRANSITIONAL_SETUP",
                        "rationale_text": "Setup",
                        "payback_plan": "Follow-up compensation",
                        "due_chapter": 4,
                    },
                    ensure_ascii=False,
                ),
            ]
        )
        run_cli(
            [
                "--project-root",
                root,
                "create-debt",
                "--data",
                json.dumps(
                    {
                        "debt_type": "micropayoff",
                        "original_amount": 1.0,
                        "current_amount": 1.0,
                        "interest_rate": 0.1,
                        "source_chapter": 3,
                        "due_chapter": 4,
                        "override_contract_id": contract_id,
                    },
                    ensure_ascii=False,
                ),
            ]
        )
        run_cli(["--project-root", root, "fulfill-override", "--contract-id", str(contract_id)])
        run_cli(
            [
                "--project-root",
                root,
                "save-chapter-reading-power",
                "--data",
                json.dumps(
                    {
                        "chapter": 3,
                        "hook_type": "Suspense hook",
                        "hook_strength": "medium",
                        "coolpoint_patterns": ["Authority slap"],
                        "micropayoffs": ["Information redemption"],
                        "hard_violations": [],
                        "soft_suggestions": [],
                        "is_transition": False,
                        "override_count": 0,
                        "debt_balance": 0.0,
                    },
                    ensure_ascii=False,
                ),
            ]
        )

        review_payload = {
            "start_chapter": 1,
            "end_chapter": 1,
            "overall_score": 50,
            "dimension_scores": {
                "Cool point density": 8,
                "Setting consistency": 7,
                "Pacing control": 8,
                "Character development": 8,
                "Coherence": 9,
                "Reading engagement": 10,
            },
            "severity_counts": {"critical": 0, "high": 1, "medium": 2, "low": 0},
            "critical_issues": [],
            "report_file": "Review report/Ch1-1_review_report.md",
        }
        run_cli(
            [
                "--project-root",
                root,
                "save-review-metrics",
                "--data",
                json.dumps(review_payload, ensure_ascii=False),
            ]
        )
        run_cli(["--project-root", root, "get-recent-review-metrics", "--limit", "5"])
        run_cli(["--project-root", root, "get-review-trend-stats", "--last-n", "5"])

        checklist_payload = {
            "chapter": 5,
            "template": "plot",
            "total_items": 6,
            "required_items": 4,
            "completed_items": 4,
            "completed_required": 3,
            "total_weight": 6.5,
            "completed_weight": 4.8,
            "completion_rate": 0.6667,
            "score": 79.2,
            "score_breakdown": {"weighted_completion_rate": 0.73},
            "pending_items": ["Hook differentiation"],
            "source": "context_manager",
        }
        run_cli(
            [
                "--project-root",
                root,
                "save-writing-checklist-score",
                "--data",
                json.dumps(checklist_payload, ensure_ascii=False),
            ]
        )
        run_cli(["--project-root", root, "get-writing-checklist-score", "--chapter", "5"])
        run_cli(["--project-root", root, "get-writing-checklist-score", "--chapter", "99"])
        run_cli(["--project-root", root, "get-recent-writing-checklist-scores", "--limit", "5"])
        run_cli(["--project-root", root, "get-writing-checklist-score-trend", "--last-n", "5"])

        capsys.readouterr()


class TestStyleSampler:
    """Style Sampler Tests"""

    def test_add_and_get_sample(self, temp_project):
        sampler = StyleSampler(temp_project)

        sample = StyleSample(
            id="ch100_s1",
            chapter=100,
            scene_type="Battle",
            content="Xiao YanThrows a punch...",
            score=0.85,
            tags=["Battle", "Intense"]
        )
        assert sampler.add_sample(sample)

        results = sampler.get_samples_by_type("Battle")
        assert len(results) == 1
        assert results[0].id == "ch100_s1"

    def test_extract_candidates(self, temp_project):
        sampler = StyleSampler(temp_project)

        scenes = [
            {"index": 1, "summary": "Battle scene", "content": "Xiao YanThrows a punch, battle qi blazing, sending the opponent flying three zhang away, the surrounding air buzzing from the impact..." + "a" * 200}
        ]

        # Low score not extracted
        candidates = sampler.extract_candidates(100, "", 70, scenes)
        assert len(candidates) == 0

        # High score extracted
        candidates = sampler.extract_candidates(100, "", 85, scenes)
        assert len(candidates) == 1
        assert candidates[0].scene_type == "Battle"

    def test_select_samples_for_chapter(self, temp_project):
        sampler = StyleSampler(temp_project)

        # Add some samples
        for i in range(3):
            sampler.add_sample(StyleSample(
                id=f"battle_{i}",
                chapter=i,
                scene_type="Battle",
                content=f"Battle content {i}",
                score=0.9,
                tags=[]
            ))

        samples = sampler.select_samples_for_chapter("This chapter has an intense battle")
        assert len(samples) <= 3
        assert all(s.scene_type == "Battle" for s in samples)


class TestRAGAdapter:
    """RAG Adapter Tests (no API calls)"""

    def test_bm25_search(self, temp_project):
        adapter = RAGAdapter(temp_project)

        # Manually insert some test data
        with adapter._get_conn() as conn:
            cursor = conn.cursor()

            # Insert vector record (empty vector, only test BM25)
            cursor.execute("""
                INSERT INTO vectors (chunk_id, chapter, scene_index, content, embedding)
                VALUES (?, ?, ?, ?, ?)
            """, ("ch1_s1", 1, 1, "Xiao Yan cultivates battle qi at Tianyun Sect", b""))

            cursor.execute("""
                INSERT INTO vectors (chunk_id, chapter, scene_index, content, embedding)
                VALUES (?, ?, ?, ?, ?)
            """, ("ch1_s2", 1, 2, "Elder Yao teaches alchemy techniques", b""))

            conn.commit()

            # Update BM25 index
            adapter._update_bm25_index(cursor, "ch1_s1", "Xiao Yan cultivates battle qi at Tianyun Sect")
            adapter._update_bm25_index(cursor, "ch1_s2", "Elder Yao teaches alchemy techniques")
            conn.commit()

        # BM25 search
        results = adapter.bm25_search("Xiao Yan trains", top_k=5)
        assert len(results) >= 1
        assert results[0].chunk_id == "ch1_s1"

    def test_tokenize(self, temp_project):
        adapter = RAGAdapter(temp_project)

        tokens = adapter._tokenize("Xiao YanhelloWorldworld")
        assert "Xiao" in tokens
        assert "Yan" in tokens
        assert "hello" in tokens
        assert "world" in tokens


if __name__ == "__main__":
    pytest.main([__file__, "-v"])