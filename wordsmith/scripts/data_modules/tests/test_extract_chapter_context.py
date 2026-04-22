#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from pathlib import Path


def test_extract_state_summary_accepts_dominant_key(tmp_path):
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    from extract_chapter_context import extract_state_summary

    state = {
        "progress": {"current_chapter": 12, "total_words": 12345},
        "protagonist_state": {
            "power": {"realm": "Foundation Building", "layer": 2},
            "location": "Sect",
            "golden_finger": {"name": "System", "level": 1},
        },
        "strand_tracker": {
            "history": [
                {"chapter": 10, "dominant": "quest"},
                {"chapter": 11, "dominant": "fire"},
            ]
        },
    }

    wordsmith_dir = tmp_path / ".wordsmith"
    wordsmith_dir.mkdir(parents=True, exist_ok=True)
    (wordsmith_dir / "state.json").write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")

    text = extract_state_summary(tmp_path)
    assert "Ch10:quest" in text
    assert "Ch11:fire" in text


def test_extract_chapter_outline_supports_hyphen_filename(tmp_path):
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    from extract_chapter_context import extract_chapter_outline

    outline_dir = tmp_path / "Outline"
    outline_dir.mkdir(parents=True, exist_ok=True)
    (outline_dir / "Volume_1_detailed_outline.md").write_text("### Chapter 1: Test title\nTest outline", encoding="utf-8")

    outline = extract_chapter_outline(tmp_path, 1)
    assert "### Chapter 1: Test title" in outline
    assert "Test outline" in outline


def test_extract_chapter_outline_prefers_state_volume_mapping(tmp_path):
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    from extract_chapter_context import extract_chapter_outline

    wordsmith_dir = tmp_path / ".wordsmith"
    wordsmith_dir.mkdir(parents=True, exist_ok=True)
    state = {
        "progress": {
            "volumes_planned": [
                {"volume": 1, "chapters_range": "1-10"},
                {"volume": 2, "chapters_range": "11-20"},
            ]
        }
    }
    (wordsmith_dir / "state.json").write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")

    outline_dir = tmp_path / "Outline"
    outline_dir.mkdir(parents=True, exist_ok=True)
    (outline_dir / "Volume_2_detailed_outline.md").write_text("### Chapter 12: V2 title\nV2 outline", encoding="utf-8")

    outline = extract_chapter_outline(tmp_path, 12)
    assert "### Chapter 12: V2 title" in outline
    assert "V2 outline" in outline


def test_extract_chapter_outline_falls_back_when_state_has_no_match(tmp_path):
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    from extract_chapter_context import extract_chapter_outline

    wordsmith_dir = tmp_path / ".wordsmith"
    wordsmith_dir.mkdir(parents=True, exist_ok=True)
    state = {"progress": {"volumes_planned": [{"volume": 1, "chapters_range": "1-10"}]}}
    (wordsmith_dir / "state.json").write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")

    outline_dir = tmp_path / "Outline"
    outline_dir.mkdir(parents=True, exist_ok=True)
    (outline_dir / "Volume_2_detailed_outline.md").write_text("### Chapter 60: V2 title\nV2 outline", encoding="utf-8")

    outline = extract_chapter_outline(tmp_path, 60)
    assert "### Chapter 60: V2 title" in outline
    assert "V2 outline" in outline


def test_build_chapter_context_payload_includes_contract_sections(tmp_path):
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    from extract_chapter_context import build_chapter_context_payload
    from data_modules.config import DataModulesConfig
    from data_modules.index_manager import IndexManager, ChapterReadingPowerMeta, ReviewMetrics

    cfg = DataModulesConfig.from_project_root(tmp_path)
    cfg.ensure_dirs()

    state = {
        "project": {"genre": "xuanhuan"},
        "progress": {"current_chapter": 3, "total_words": 9000},
        "protagonist_state": {
            "power": {"realm": "Foundation Building", "layer": 2},
            "location": "Sect",
            "golden_finger": {"name": "System", "level": 1},
        },
        "strand_tracker": {"history": [{"chapter": 2, "dominant": "quest"}]},
        "chapter_meta": {},
        "disambiguation_warnings": [],
        "disambiguation_pending": [],
    }
    (cfg.wordsmith_dir / "state.json").write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")

    summaries_dir = cfg.wordsmith_dir / "summaries"
    summaries_dir.mkdir(parents=True, exist_ok=True)
    (summaries_dir / "ch0002.md").write_text("## Plot summary\nPrevious chapter summary", encoding="utf-8")

    outline_dir = tmp_path / "Outline"
    outline_dir.mkdir(parents=True, exist_ok=True)
    (outline_dir / "Volume 1 detailed outline.md").write_text("### Chapter 3: Test title\nTest outline", encoding="utf-8")

    refs_dir = tmp_path / ".claude" / "references"
    refs_dir.mkdir(parents=True, exist_ok=True)
    (refs_dir / "genre-profiles.md").write_text("## xuanhuan\n- Clear progression line", encoding="utf-8")
    (refs_dir / "reading-power-taxonomy.md").write_text("## xuanhuan\n- Suspense hookPriority", encoding="utf-8")

    idx = IndexManager(cfg)
    idx.save_chapter_reading_power(
        ChapterReadingPowerMeta(chapter=2, hook_type="Suspense hook", hook_strength="strong", coolpoint_patterns=["Identity reveal"])
    )
    idx.save_review_metrics(
        ReviewMetrics(start_chapter=1, end_chapter=2, overall_score=71, dimension_scores={"plot": 71})
    )

    payload = build_chapter_context_payload(tmp_path, 3)
    assert payload["context_contract_version"] == "v2"
    assert payload.get("context_weight_stage") in {"early", "mid", "late"}
    assert "writing_guidance" in payload
    assert isinstance(payload["writing_guidance"].get("guidance_items"), list)
    assert isinstance(payload["writing_guidance"].get("checklist"), list)
    assert isinstance(payload["writing_guidance"].get("checklist_score"), dict)
    assert payload["genre_profile"].get("genre") == "xuanhuan"
    assert "rag_assist" in payload
    assert isinstance(payload["rag_assist"], dict)
    assert payload["rag_assist"].get("invoked") is False


def test_render_text_contains_writing_guidance_section(tmp_path):
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    from extract_chapter_context import _render_text

    payload = {
        "chapter": 10,
        "outline": "Test outline",
        "previous_summaries": ["### Ch9 summary\nPrevious chapter"],
        "state_summary": "Status",
        "context_contract_version": "v2",
        "context_weight_stage": "early",
        "reader_signal": {"review_trend": {"overall_avg": 72}, "low_score_ranges": [{"start_chapter": 8, "end_chapter": 9}]},
        "genre_profile": {
            "genre": "xuanhuan",
            "genres": ["xuanhuan", "realistic"],
            "composite_hints": ["Advance with fantasy mainline while preserving real-world themes"],
            "reference_hints": ["Clear progression line"],
        },
        "writing_guidance": {
            "guidance_items": ["Fix low scores first", "Hook differentiation"],
            "checklist": [
                {
                    "id": "fix_low_score_range",
                    "label": "Fix low score range issue",
                    "weight": 1.4,
                    "required": True,
                    "source": "reader_signal.low_score_ranges",
                    "verify_hint": "Complete at least 1 conflict level-up",
                }
            ],
            "checklist_score": {
                "score": 81.5,
                "completion_rate": 0.66,
                "required_completion_rate": 0.75,
            },
            "methodology": {
                "enabled": True,
                "framework": "digital-serial-v1",
                "pilot": "xianxia",
                "genre_profile_key": "xianxia",
                "chapter_stage": "confront",
                "observability": {
                    "next_reason_clarity": 78.0,
                    "anchor_effectiveness": 74.0,
                    "rhythm_naturalness": 72.0,
                },
                "signals": {"risk_flags": ["pattern_overuse_watch"]},
            },
        },
    }

    text = _render_text(payload)
    assert "## Writing execution suggestions" in text
    assert "Fix low scores first" in text
    assert "## Contract (v2)" in text
    assert "- Context stage weight: early" in text
    assert "### Execution checklist (scorable)" in text
    assert "- Total weight: 1.40" in text
    assert "[Required][w=1.4] Fix low score range issue" in text
    assert "### Execution score" in text
    assert "- Score: 81.5" in text
    assert "- Composite genre: xuanhuan + realistic" in text
    assert "## Long-form methodology strategy" in text
    assert "- Applicable genre: xianxia" in text
    assert "next_reason=78.0" in text


def test_render_text_contains_rag_assist_section_when_hits_exist(tmp_path):
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    from extract_chapter_context import _render_text

    payload = {
        "chapter": 12,
        "outline": "Test outline",
        "previous_summaries": [],
        "state_summary": "Status",
        "context_contract_version": "v2",
        "reader_signal": {},
        "genre_profile": {},
        "writing_guidance": {},
        "rag_assist": {
            "invoked": True,
            "mode": "auto",
            "intent": "relationship",
            "query": "Chapter 12 Character relationships and motivations: Xiao Yan and Elder Yao conflict",
            "hits": [
                {
                    "chapter": 9,
                    "scene_index": 2,
                    "source": "graph_hybrid",
                    "score": 0.91,
                    "content": "Xiao Yan and Elder Yao disagree on training direction.",
                }
            ],
        },
    }

    text = _render_text(payload)
    assert "## RAG retrieval clues" in text
    assert "- Mode: auto" in text
    assert "[graph_hybrid]" in text
    assert "Xiao Yan and Elder Yao" in text
