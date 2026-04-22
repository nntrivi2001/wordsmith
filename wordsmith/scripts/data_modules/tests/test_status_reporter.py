#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import tempfile

from data_modules.config import DataModulesConfig
from data_modules.index_manager import (
    IndexManager,
    ChapterReadingPowerMeta,
    EntityMeta,
    RelationshipMeta,
    RelationshipEventMeta,
)
from status_reporter import StatusReporter


def _write_state(project_root, state: dict):
    webnovel_dir = project_root / ".webnovel"
    webnovel_dir.mkdir(parents=True, exist_ok=True)
    (webnovel_dir / "state.json").write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def test_foreshadowing_analysis_uses_real_chapters_and_handles_missing_data():
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = DataModulesConfig.from_project_root(tmpdir).project_root

        state = {
            "progress": {"current_chapter": 120, "total_words": 360000},
            "plot_threads": {
                "foreshadowing": [
                    {
                        "content": "Secret of Lin family treasury inscription",
                        "status": "Not recovered",
                        "tier": "Core",
                        "planted_chapter": 20,
                        "target_chapter": 100,
                    },
                    {
                        "content": "Origin of mysterious jade pendant",
                        "status": "Pending recovery",
                        "tier": "Subplot",
                        "added_chapter": 50,
                        "target": 150,
                    },
                    {
                        "content": "Old oath",
                        "status": "Not recovered",
                        "tier": "Decoration",
                    },
                    {
                        "content": "Fulfilled foreshadowing",
                        "status": "Already recovered",
                        "planted_chapter": 10,
                        "target_chapter": 20,
                    },
                ]
            },
        }
        _write_state(project_root, state)

        reporter = StatusReporter(str(project_root))
        assert reporter.load_state() is True

        foreshadowing = reporter.analyze_foreshadowing()
        assert len(foreshadowing) == 3

        records = {item["content"]: item for item in foreshadowing}
        assert records["Secret of Lin family treasury inscription"]["planted_chapter"] == 20
        assert records["Secret of Lin family treasury inscription"]["elapsed"] == 100
        assert records["Secret of Lin family treasury inscription"]["status"] == "🔴 Already overdue"

        assert records["Origin of mysterious jade pendant"]["planted_chapter"] == 50
        assert records["Origin of mysterious jade pendant"]["target_chapter"] == 150
        assert records["Origin of mysterious jade pendant"]["status"] in {"🟡 Slightly overdue", "🟢 Normal"}

        assert records["Old oath"]["planted_chapter"] is None
        assert records["Old oath"]["status"] == "⚪ Insufficient data"

        urgency = reporter.analyze_foreshadowing_urgency()
        urgency_by_content = {item["content"]: item for item in urgency}

        assert urgency_by_content["Secret of Lin family treasury inscription"]["urgency"] is not None
        assert urgency_by_content["Secret of Lin family treasury inscription"]["status"] == "🔴 Already overdue"
        assert urgency_by_content["Old oath"]["urgency"] is None
        assert urgency_by_content["Old oath"]["status"] == "⚪ Insufficient data"


def test_pacing_analysis_prefers_real_coolpoint_metadata_over_estimation():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = DataModulesConfig.from_project_root(tmpdir)
        config.ensure_dirs()
        project_root = config.project_root

        state = {
            "progress": {"current_chapter": 3, "total_words": 12000},
            "chapter_meta": {
                "0003": {
                    "hook": "Something happens next chapter",
                    "coolpoint_patterns": ["Identity reveal", "Villain setback"],
                }
            },
        }
        _write_state(project_root, state)

        idx = IndexManager(config)
        idx.save_chapter_reading_power(
            ChapterReadingPowerMeta(
                chapter=1,
                hook_type="Desire hook",
                hook_strength="strong",
                coolpoint_patterns=["Authority slap", "Identity reveal"],
            )
        )
        idx.save_chapter_reading_power(
            ChapterReadingPowerMeta(
                chapter=2,
                hook_type="Suspense hook",
                hook_strength="medium",
                coolpoint_patterns=["Identity reveal"],
            )
        )

        reporter = StatusReporter(str(project_root))
        assert reporter.load_state() is True
        reporter.chapters_data = [
            {"chapter": 1, "word_count": 4000, "cool_point": "", "dominant": "", "characters": []},
            {"chapter": 2, "word_count": 3000, "cool_point": "", "dominant": "", "characters": []},
            {"chapter": 3, "word_count": 5000, "cool_point": "", "dominant": "", "characters": []},
        ]

        segments = reporter.analyze_pacing()
        assert len(segments) == 1

        seg = segments[0]
        assert seg["cool_points"] == 5
        assert round(seg["words_per_point"], 2) == 2400.00
        assert seg["missing_chapters"] == 0
        assert seg["dominant_source"] == "chapter_reading_power"


def test_pacing_analysis_marks_missing_data_instead_of_assuming_one_point_per_chapter():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = DataModulesConfig.from_project_root(tmpdir)
        config.ensure_dirs()
        project_root = config.project_root

        state = {
            "progress": {"current_chapter": 1, "total_words": 2000},
            "chapter_meta": {},
        }
        _write_state(project_root, state)

        reporter = StatusReporter(str(project_root))
        assert reporter.load_state() is True
        reporter.chapters_data = [
            {"chapter": 1, "word_count": 2000, "cool_point": "", "dominant": "", "characters": []}
        ]

        seg = reporter.analyze_pacing()[0]
        assert seg["cool_points"] == 0
        assert seg["words_per_point"] is None
        assert seg["rating"] == "Insufficient data"
        assert seg["missing_chapters"] == 1


def test_relationship_graph_prefers_index_db_data():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = DataModulesConfig.from_project_root(tmpdir)
        config.ensure_dirs()
        project_root = config.project_root

        state = {
            "progress": {"current_chapter": 12, "total_words": 24000},
            "protagonist_state": {"name": "Xiao Yan"},
            "relationships": {"allies": [{"name": "Old ally", "relation": "Friendly"}], "enemies": []},
        }
        _write_state(project_root, state)

        idx = IndexManager(config)
        idx.upsert_entity(
            EntityMeta(
                id="xiaoyan",
                type="Character",
                canonical_name="Xiao Yan",
                tier="Core",
                current={},
                first_appearance=1,
                last_appearance=12,
                is_protagonist=True,
            )
        )
        idx.upsert_entity(
            EntityMeta(
                id="yaolao",
                type="Character",
                canonical_name="Elder Yao",
                tier="Important",
                current={},
                first_appearance=1,
                last_appearance=12,
            )
        )
        idx.upsert_relationship(
            RelationshipMeta(
                from_entity="xiaoyan",
                to_entity="yaolao",
                type="Master-disciple",
                description="Master-disciple relationship",
                chapter=10,
            )
        )
        idx.record_relationship_event(
            RelationshipEventMeta(
                from_entity="xiaoyan",
                to_entity="yaolao",
                type="Master-disciple",
                chapter=10,
                action="create",
                polarity=1,
                strength=0.9,
                description="Become disciple",
                evidence="Becomes Elder Yao disciple",
            )
        )

        reporter = StatusReporter(str(project_root))
        assert reporter.load_state() is True
        graph = reporter.generate_relationship_graph()
        assert "mermaid" in graph
        assert "Elder Yao" in graph
        assert "Master-disciple" in graph
