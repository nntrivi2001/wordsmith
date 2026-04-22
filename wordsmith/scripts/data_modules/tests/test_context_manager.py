#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ContextManager and SnapshotManager tests
"""

import json
import logging

import pytest

from data_modules.config import DataModulesConfig
from data_modules.index_manager import (
    IndexManager,
    EntityMeta,
    ChapterReadingPowerMeta,
    ReviewMetrics,
)
from data_modules.context_manager import ContextManager
from data_modules.snapshot_manager import SnapshotManager, SnapshotVersionMismatch
from data_modules.query_router import QueryRouter


@pytest.fixture
def temp_project(tmp_path):
    cfg = DataModulesConfig.from_project_root(tmp_path)
    cfg.ensure_dirs()
    return cfg


def test_snapshot_manager_roundtrip(temp_project):
    manager = SnapshotManager(temp_project)
    payload = {"hello": "world"}
    manager.save_snapshot(1, payload)
    loaded = manager.load_snapshot(1)
    assert loaded["payload"] == payload


def test_snapshot_version_mismatch(temp_project):
    manager = SnapshotManager(temp_project, version="1.0")
    manager.save_snapshot(1, {"a": 1})
    other = SnapshotManager(temp_project, version="2.0")
    with pytest.raises(SnapshotVersionMismatch):
        other.load_snapshot(1)


def test_snapshot_delete_roundtrip(temp_project):
    manager = SnapshotManager(temp_project)
    manager.save_snapshot(2, {"x": 1})

    assert manager.delete_snapshot(2) is True
    assert manager.load_snapshot(2) is None


def test_context_manager_build_and_filter(temp_project):
    state = {
        "protagonist_state": {"name": "Xiao Yan", "location": {"current": "Tianyun Sect"}},
        "chapter_meta": {"0001": {"hook": "Test"}},
    }
    temp_project.state_file.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")

    # preferences and memory
    (temp_project.wordsmith_dir / "preferences.json").write_text(json.dumps({"tone": "Passionate"}, ensure_ascii=False), encoding="utf-8")
    (temp_project.wordsmith_dir / "project_memory.json").write_text(json.dumps({"patterns": []}, ensure_ascii=False), encoding="utf-8")

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
            id="bad",
            type="Character",
            canonical_name="Bad person",
            current={},
            first_appearance=1,
            last_appearance=1,
        )
    )
    idx.record_appearance("xiaoyan", 1, ["Xiao Yan"], 1.0)
    idx.record_appearance("bad", 1, ["Bad person"], 1.0)
    invalid_id = idx.mark_invalid_fact("entity", "bad", "Error")
    idx.resolve_invalid_fact(invalid_id, "confirm")

    manager = ContextManager(temp_project)
    payload = manager.build_context(1, use_snapshot=False, save_snapshot=False)
    characters = payload["sections"]["scene"]["content"]["appearing_characters"]
    assert any(c.get("entity_id") == "xiaoyan" for c in characters)
    assert not any(c.get("entity_id") == "bad" for c in characters)
    assert payload["sections"]["preferences"]["content"].get("tone") == "Passionate"


def test_context_manager_loads_volume_outline_file(temp_project):
    state = {
        "progress": {
            "volumes_planned": [
                {"volume": 1, "chapters_range": "1-10"},
            ]
        },
        "protagonist_state": {},
        "chapter_meta": {},
        "disambiguation_warnings": [],
        "disambiguation_pending": [],
    }
    temp_project.state_file.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    temp_project.outline_dir.mkdir(parents=True, exist_ok=True)
    (temp_project.outline_dir / "Volume_1_detailed_outline.md").write_text(
        "### Chapter 2: Test title\nTest outline\n\n### Chapter 3: Next chapter",
        encoding="utf-8",
    )

    manager = ContextManager(temp_project)
    payload = manager.build_context(2, use_snapshot=False, save_snapshot=False)

    outline = payload["sections"]["core"]["content"]["chapter_outline"]
    assert "### Chapter 2: Test title" in outline
    assert "Test outline" in outline


def test_query_router():
    router = QueryRouter()
    assert router.route("Who is the character") == "entity"
    assert router.route("What plot happened") == "plot"
    intent = router.route_intent("Chapters 10-20 Xiao Yan and Elder Yao relationship graph")
    assert intent["intent"] == "relationship"
    assert intent["needs_graph"] is True
    assert intent["time_scope"]["from_chapter"] == 10
    assert intent["time_scope"]["to_chapter"] == 20
    plans = router.plan_subqueries(intent)
    assert plans
    assert plans[0]["strategy"] in {"graph_lookup", "graph_hybrid"}
    assert "A" in router.split("A, B; C")


def test_context_snapshot_respects_template(temp_project):
    state = {
        "protagonist_state": {"name": "Xiao Yan"},
        "chapter_meta": {},
        "disambiguation_warnings": [],
        "disambiguation_pending": [],
    }
    temp_project.state_file.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")

    manager = ContextManager(temp_project)

    plot_payload = manager.build_context(1, template="plot", use_snapshot=True, save_snapshot=True)
    battle_payload = manager.build_context(1, template="battle", use_snapshot=True, save_snapshot=True)

    assert plot_payload.get("template") == "plot"
    assert battle_payload.get("template") == "battle"


def test_context_manager_applies_ranker_and_contract_meta(temp_project):
    state = {
        "protagonist_state": {"name": "Xiao Yan"},
        "chapter_meta": {
            "0002": {"hook": "Steady"},
            "0003": {"hook": "Leave suspense"},
        },
        "disambiguation_warnings": [
            {"chapter": 1, "message": "Normal warning"},
            {"chapter": 3, "message": "Critical conflict warning", "severity": "high"},
        ],
        "disambiguation_pending": [],
    }
    temp_project.state_file.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")

    manager = ContextManager(temp_project)
    payload = manager.build_context(4, use_snapshot=False, save_snapshot=False)

    assert payload["meta"].get("context_contract_version") == "v2"
    recent_meta = payload["sections"]["core"]["content"]["recent_meta"]
    if recent_meta:
        assert recent_meta[0]["chapter"] == 3

    warnings = payload["sections"]["alerts"]["content"]["disambiguation_warnings"]
    if warnings and isinstance(warnings[0], dict):
        assert "critical" in str(warnings[0].get("message", "")) or warnings[0].get("severity") == "high"


def test_context_manager_includes_reader_signal_and_genre_profile(temp_project):
    state = {
        "project": {"genre": "xuanhuan"},
        "protagonist_state": {"name": "Xiao Yan"},
        "chapter_meta": {},
        "disambiguation_warnings": [],
        "disambiguation_pending": [],
    }
    temp_project.state_file.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")

    idx = IndexManager(temp_project)
    idx.save_chapter_reading_power(
        ChapterReadingPowerMeta(
            chapter=3,
            hook_type="Suspense hook",
            hook_strength="strong",
            coolpoint_patterns=["Identity reveal"],
        )
    )
    idx.save_review_metrics(
        ReviewMetrics(
            start_chapter=1,
            end_chapter=3,
            overall_score=72,
            dimension_scores={"plot": 72},
            severity_counts={"high": 1},
            critical_issues=["Pacing drag"],
        )
    )

    manager = ContextManager(temp_project)
    payload = manager.build_context(4, use_snapshot=False, save_snapshot=False)

    reader_signal = payload["sections"]["reader_signal"]["content"]
    assert "recent_reading_power" in reader_signal
    assert "pattern_usage" in reader_signal
    assert "hook_type_usage" in reader_signal
    assert "review_trend" in reader_signal
    assert isinstance(reader_signal.get("low_score_ranges"), list)

    genre_profile = payload["sections"]["genre_profile"]["content"]
    assert genre_profile.get("genre") == "xuanhuan"
    assert "profile_excerpt" in genre_profile
    assert "taxonomy_excerpt" in genre_profile


def test_context_manager_genre_section_and_refs_extraction(temp_project):
    refs_dir = temp_project.project_root / ".claude" / "references"
    refs_dir.mkdir(parents=True, exist_ok=True)

    (refs_dir / "genre-profiles.md").write_text(
        """
## shuangwen
- Fast pacing
- Frequent authority slaps

## xuanhuan
- Clear progression line
- Resource competition
""".strip(),
        encoding="utf-8",
    )
    (refs_dir / "reading-power-taxonomy.md").write_text(
        """
## xuanhuan
- Hook strengthPriority strong
- Cool point uses power level leap
""".strip(),
        encoding="utf-8",
    )

    manager = ContextManager(temp_project)

    profile = manager._load_genre_profile({"project": {"genre": "xuanhuan"}})
    assert profile["genre"] == "xuanhuan"
    assert "Clear progression line" in profile["profile_excerpt"]
    assert "Hook strength" in profile["taxonomy_excerpt"]
    assert isinstance(profile["reference_hints"], list)
    assert profile["reference_hints"]

    fallback_excerpt = manager._extract_genre_section("## a\n1\n## b\n2", "unknown")
    assert fallback_excerpt.startswith("## a")


def test_context_manager_reader_signal_with_debt_and_disable_switch(temp_project):
    manager = ContextManager(temp_project)
    manager.config.context_reader_signal_include_debt = True

    signal = manager._load_reader_signal(chapter=5)
    assert "debt_summary" in signal

    manager.config.context_reader_signal_enabled = False
    assert manager._load_reader_signal(chapter=5) == {}

    manager.config.context_genre_profile_enabled = False
    assert manager._load_genre_profile({"project": {"genre": "xuanhuan"}}) == {}


def test_context_manager_includes_writing_guidance(temp_project):
    state = {
        "project": {"genre": "xuanhuan"},
        "protagonist_state": {"name": "Xiao Yan"},
        "chapter_meta": {},
        "disambiguation_warnings": [],
        "disambiguation_pending": [],
    }
    temp_project.state_file.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")

    idx = IndexManager(temp_project)
    idx.save_chapter_reading_power(
        ChapterReadingPowerMeta(
            chapter=3,
            hook_type="Suspense hook",
            hook_strength="strong",
            coolpoint_patterns=["Identity reveal"],
        )
    )
    idx.save_review_metrics(
        ReviewMetrics(
            start_chapter=1,
            end_chapter=3,
            overall_score=70,
            dimension_scores={"plot": 70},
            severity_counts={"high": 1},
            critical_issues=["Pacing drag"],
        )
    )

    manager = ContextManager(temp_project)
    payload = manager.build_context(4, use_snapshot=False, save_snapshot=False)

    guidance = payload["sections"]["writing_guidance"]["content"]
    assert guidance.get("chapter") == 4
    items = guidance.get("guidance_items") or []
    assert isinstance(items, list)
    assert items
    assert guidance.get("signals_used", {}).get("genre") == "xuanhuan"
    checklist = guidance.get("checklist") or []
    assert isinstance(checklist, list)
    assert checklist
    checklist_score = guidance.get("checklist_score") or {}
    assert isinstance(checklist_score, dict)
    assert "score" in checklist_score
    assert "completion_rate" in checklist_score
    first_item = checklist[0]
    assert isinstance(first_item, dict)
    assert {"id", "label", "weight", "required", "source", "verify_hint"}.issubset(first_item.keys())

    persisted = idx.get_writing_checklist_score(4)
    assert isinstance(persisted, dict)
    assert persisted.get("chapter") == 4
    assert persisted.get("score") is not None


def test_context_manager_dynamic_weights_and_composite_genre(temp_project):
    refs_dir = temp_project.project_root / ".claude" / "references"
    refs_dir.mkdir(parents=True, exist_ok=True)
    (refs_dir / "genre-profiles.md").write_text(
        """
## xuanhuan
- Clear progression line

## realistic
- Social issue mapping
""".strip(),
        encoding="utf-8",
    )
    (refs_dir / "reading-power-taxonomy.md").write_text(
        """
## xuanhuan
- Hook strengthPriority

## realistic
- Consistent character motivations
""".strip(),
        encoding="utf-8",
    )

    state = {
        "project": {"genre": "xuanhuan+realistic"},
        "protagonist_state": {"name": "Xiao Yan"},
        "chapter_meta": {},
        "disambiguation_warnings": [],
        "disambiguation_pending": [],
    }
    temp_project.state_file.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")

    manager = ContextManager(temp_project)
    payload_early = manager.build_context(10, template="plot", use_snapshot=False, save_snapshot=False)
    payload_late = manager.build_context(150, template="plot", use_snapshot=False, save_snapshot=False)

    assert payload_early.get("weights", {}).get("core") >= payload_late.get("weights", {}).get("core")
    assert payload_late.get("weights", {}).get("global") >= payload_early.get("weights", {}).get("global")
    assert payload_early.get("meta", {}).get("context_weight_stage") == "early"
    assert payload_late.get("meta", {}).get("context_weight_stage") == "late"

    profile = payload_early["sections"]["genre_profile"]["content"]
    assert profile.get("composite") is True
    assert profile.get("genre") == "xuanhuan"
    assert isinstance(profile.get("genres"), list)
    assert "realistic" in (profile.get("genres") or [])
    assert isinstance(profile.get("composite_hints"), list)
    assert profile.get("composite_hints")


def test_context_manager_genre_alias_guidance_and_heading_extraction(temp_project):
    refs_dir = temp_project.project_root / ".claude" / "references"
    refs_dir.mkdir(parents=True, exist_ok=True)
    (refs_dir / "genre-profiles.md").write_text(
        """
### Esports
- League progression

### Livestream fiction
- Feedback loop

### Lovecraftian
- Truth cost
""".strip(),
        encoding="utf-8",
    )
    (refs_dir / "reading-power-taxonomy.md").write_text(
        """
### Esports
- Tactical decision point
""".strip(),
        encoding="utf-8",
    )

    state = {
        "project": {"genre": "Esports"},
        "protagonist_state": {"name": "Lin Ran"},
        "chapter_meta": {},
        "disambiguation_warnings": [],
        "disambiguation_pending": [],
    }
    temp_project.state_file.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")

    manager = ContextManager(temp_project)
    payload = manager.build_context(12, template="plot", use_snapshot=False, save_snapshot=False)
    guidance = payload["sections"]["writing_guidance"]["content"]
    items = guidance.get("guidance_items") or []

    assert any("Tactical decision point" in str(text) for text in items)
    assert any("Web novel pacing baseline" in str(text) for text in items)
    assert any("Redemption density baseline" in str(text) for text in items)


def test_context_manager_genre_aliases_normalized_for_profile_lookup(temp_project):
    refs_dir = temp_project.project_root / ".claude" / "references"
    refs_dir.mkdir(parents=True, exist_ok=True)
    (refs_dir / "genre-profiles.md").write_text(
        """
## Esports
- League progression

## Livestream fiction
- Real-time feedback

## Lovecraftian
- Truth cost
""".strip(),
        encoding="utf-8",
    )
    (refs_dir / "reading-power-taxonomy.md").write_text(
        """
## Esports
- Decision consequence

## Livestream fiction
- Data loop

## Lovecraftian
- Rules first
""".strip(),
        encoding="utf-8",
    )

    manager = ContextManager(temp_project)

    assert manager._parse_genre_tokens("Esports fiction") == ["Esports"]
    assert manager._parse_genre_tokens("Livestream") == ["Livestream fiction"]
    assert manager._parse_genre_tokens("Lovecraft-style") == ["Lovecraftian"]
    assert manager._parse_genre_tokens("Cultivation/Fantasy") == ["Cultivation"]
    assert manager._parse_genre_tokens("Urban cultivation") == ["Urban supernatural"]
    assert manager._parse_genre_tokens("Ancient romance AU") == ["Ancient romance"]

    state = {
        "project": {"genre": "Esports fiction+Livestream"},
        "protagonist_state": {"name": "Ye Xiu"},
        "chapter_meta": {},
        "disambiguation_warnings": [],
        "disambiguation_pending": [],
    }
    temp_project.state_file.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")

    payload = manager.build_context(20, template="plot", use_snapshot=False, save_snapshot=False)
    profile = payload["sections"]["genre_profile"]["content"]

    assert profile.get("genre") == "Esports"
    assert "Livestream fiction" in (profile.get("genres") or [])


def test_context_manager_enables_methodology_for_xianxia(temp_project):
    state = {
        "project": {"genre": "Cultivation"},
        "protagonist_state": {"name": "Han Li"},
        "chapter_meta": {},
        "disambiguation_warnings": [],
        "disambiguation_pending": [],
    }
    temp_project.state_file.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")

    manager = ContextManager(temp_project)
    manager.config.context_writing_checklist_max_items = 8
    payload = manager.build_context(21, template="plot", use_snapshot=False, save_snapshot=False)

    guidance = payload["sections"]["writing_guidance"]["content"]
    strategy = guidance.get("methodology") or {}
    assert strategy.get("enabled") is True
    assert strategy.get("pilot") == "xianxia"
    assert strategy.get("genre_profile_key") == "xianxia"
    assert guidance.get("signals_used", {}).get("methodology_enabled") is True
    assert isinstance(strategy.get("observability"), dict)


def test_context_manager_enables_methodology_for_non_xianxia_by_default(temp_project):
    state = {
        "project": {"genre": "xuanhuan"},
        "protagonist_state": {"name": "Xiao Yan"},
        "chapter_meta": {},
        "disambiguation_warnings": [],
        "disambiguation_pending": [],
    }
    temp_project.state_file.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")

    manager = ContextManager(temp_project)
    payload = manager.build_context(21, template="plot", use_snapshot=False, save_snapshot=False)

    guidance = payload["sections"]["writing_guidance"]["content"]
    strategy = guidance.get("methodology") or {}
    assert strategy.get("enabled") is True
    assert strategy.get("genre_profile_key") == "xuanhuan"
    assert guidance.get("signals_used", {}).get("methodology_enabled") is True


def test_context_manager_allows_methodology_whitelist_restriction(temp_project):
    state = {
        "project": {"genre": "Livestream fiction"},
        "protagonist_state": {"name": "Lin Mo"},
        "chapter_meta": {},
        "disambiguation_warnings": [],
        "disambiguation_pending": [],
    }
    temp_project.state_file.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")

    manager = ContextManager(temp_project)
    manager.config.context_methodology_genre_whitelist = ("xianxia",)
    payload = manager.build_context(21, template="plot", use_snapshot=False, save_snapshot=False)

    guidance = payload["sections"]["writing_guidance"]["content"]
    strategy = guidance.get("methodology") or {}
    assert strategy == {}
    assert guidance.get("signals_used", {}).get("methodology_enabled") is False


def test_context_manager_compact_text_truncation(temp_project):
    manager = ContextManager(temp_project)
    manager.config.context_compact_text_enabled = True
    manager.config.context_compact_min_budget = 80
    manager.config.context_compact_head_ratio = 0.6

    content = {"a": "x" * 200, "b": "y" * 200}
    compact = manager._compact_json_text(content, budget=120)
    assert len(compact) <= 120
    assert "[TRUNCATED]" in compact

    manager.config.context_compact_text_enabled = False
    raw_cut = manager._compact_json_text(content, budget=100)
    assert len(raw_cut) <= 100


def test_context_manager_persist_writing_checklist_score_logs_failure(temp_project, monkeypatch, caplog):
    manager = ContextManager(temp_project)

    def _raise_save_error(_meta):
        raise RuntimeError("simulated save failure")

    monkeypatch.setattr(manager.index_manager, "save_writing_checklist_score", _raise_save_error)

    with caplog.at_level(logging.WARNING):
        manager._persist_writing_checklist_score(
            {
                "chapter": 6,
                "score": 70.0,
                "total_items": 3,
                "required_items": 1,
                "completed_items": 1,
                "completed_required": 1,
                "total_weight": 3.0,
                "completed_weight": 1.0,
                "completion_rate": 0.33,
                "pending_items": ["test"],
            }
        )

    message_text = "\n".join(record.getMessage() for record in caplog.records)
    assert "failed to persist writing checklist score" in message_text


def test_context_manager_composite_genre_boundary_three_plus(temp_project):
    manager = ContextManager(temp_project)
    manager.config.context_genre_profile_support_composite = True
    manager.config.context_genre_profile_max_genres = 3

    genre_raw = "Esports fiction+Livestream+Lovecraft-style+Cultivation/Fantasy+Esports fiction"
    tokens = manager._parse_genre_tokens(genre_raw)
    assert tokens[:4] == ["Esports", "Livestream fiction", "Lovecraftian", "Cultivation"]

    state = {
        "project": {"genre": genre_raw},
        "protagonist_state": {"name": "Protagonist"},
        "chapter_meta": {},
        "disambiguation_warnings": [],
        "disambiguation_pending": [],
    }

    profile = manager._load_genre_profile(state)
    assert profile.get("composite") is True
    assert profile.get("genres") == ["Esports", "Livestream fiction", "Lovecraftian"]
    assert profile.get("secondary_genres") == ["Livestream fiction", "Lovecraftian"]

    profile_again = manager._load_genre_profile(state)
    assert profile_again.get("genres") == profile.get("genres")


def test_context_manager_dynamic_weights_from_config_override(temp_project):
    manager = ContextManager(temp_project)
    manager.config.context_dynamic_budget_enabled = True
    manager.config.context_template_weights_dynamic = {
        "early": {
            "plot": {"core": 0.60, "scene": 0.20, "global": 0.20},
        }
    }

    weights = manager._resolve_template_weights("plot", chapter=1)
    assert weights == {"core": 0.60, "scene": 0.20, "global": 0.20}


def test_context_manager_genre_profile_fallbacks_to_project_info(temp_project):
    manager = ContextManager(temp_project)

    profile = manager._load_genre_profile({"project_info": {"genre": "xuanhuan"}})

    assert profile.get("genre_raw") == "xuanhuan"
    assert profile.get("genre") == "xuanhuan"


def test_context_manager_genre_profile_prefers_project_over_project_info(temp_project):
    manager = ContextManager(temp_project)

    profile = manager._load_genre_profile(
        {
            "project": {"genre": "xuanhuan"},
            "project_info": {"genre": "dushi"},
        }
    )

    assert profile.get("genre_raw") == "xuanhuan"
    assert profile.get("genre") == "xuanhuan"