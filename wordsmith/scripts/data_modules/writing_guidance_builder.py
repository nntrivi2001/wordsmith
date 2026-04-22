#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Writing guidance and checklist builders.
"""

from __future__ import annotations

from typing import Any, Dict, List

from .genre_aliases import to_profile_key


GENRE_GUIDANCE_TEXT: dict[str, str] = {
    "xianxia": "Genre weighting: Strengthen visible feedback of level-up/confrontation results, defer terminology explanations.",
    "shuangwen": "Genre weighting: Maintain high coolpoint density, add one contrasting sub-axis beyond the main coolpoint.",
    "urban-power": "Genre weighting: Prioritize social feedback chain (others' reactions -> resource changes -> status changes).",
    "romance": "Genre weighting: Each chapter advances relationship displacement, avoid emotional stalling.",
    "mystery": "Genre weighting: Clues must be recoverable, prioritize suspense creation through rule conflicts.",
    "rules-mystery": "Genre weighting: Rules before explanations, costs before victories.",
    "zhihu-short": "Genre weighting: Compress setup, prioritize reversal and high-intensity ending hook.",
    "substitute": "Genre weighting: Strengthen misunderstanding-tension-decision chain, avoid repetitive torment points.",
    "esports": "Genre weighting: Each confrontation must clarify at least one tactical decision point and its consequences.",
    "livestream": "Genre weighting: Strengthen \"external feedback -> protagonist counter -> data changes\" immediate loop.",
    "cosmic-horror": "Genre weighting: Horror comes from rules and costs, do not rely on vague thriller descriptions.",
}


GENRE_METHOD_ANCHORS: dict[str, dict[str, str]] = {
    "xianxia": {
        "pressure_source": "Resource competition/realm suppression",
        "release_target": "Protagonist actively breaks out and gains visible benefits",
    },
    "urban-power": {
        "pressure_source": "Class positioning/power suppression",
        "release_target": "Protagonist gains status and rewards through resource gaming",
    },
    "romance": {
        "pressure_source": "Relationship misunderstanding/emotional tension",
        "release_target": "Relationship displacement lands and forms next commitment",
    },
    "mystery": {
        "pressure_source": "Clue missing/rule conflict",
        "release_target": "Provide verifiable new clues while preserving unknown areas",
    },
    "rules-mystery": {
        "pressure_source": "Rule backlash/escalating costs",
        "release_target": "Exchange cost for breakthrough while leaving higher-level rule questions",
    },
    "zhihu-short": {
        "pressure_source": "Information gap/stance collision",
        "release_target": "Reversal fulfilled and high-intensity tail hook formed",
    },
    "substitute": {
        "pressure_source": "Identity misread/emotional confrontation",
        "release_target": "Misunderstanding chain advances to clear decision",
    },
    "esports": {
        "pressure_source": "Tactical suppression/rhythm imbalance",
        "release_target": "Key decisions take effect and convert to situational advantage",
    },
    "livestream": {
        "pressure_source": "Public opinion fluctuation/data decline",
        "release_target": "Immediate counterattack forms visible data rebound",
    },
    "cosmic-horror": {
        "pressure_source": "Cognitive distortion/rule erosion",
        "release_target": "Exchange clear cost for a phased survival window",
    },
    "history-travel": {
        "pressure_source": "Historical inertia/ritual resistance",
        "release_target": "Knowledge advantage cashed in and triggers new chain reactions",
    },
    "game-lit": {
        "pressure_source": "System rule restrictions/resource scarcity",
        "release_target": "Numeric breakthrough and exposure of higher-level threats",
    },
}


def build_methodology_strategy_card(
    *,
    chapter: int,
    reader_signal: Dict[str, Any],
    genre_profile: Dict[str, Any],
    label: str = "digital-serial-v1",
) -> Dict[str, Any]:
    genre = str(genre_profile.get("genre") or "").strip()
    profile_key = to_profile_key(genre) or "general"

    hook_usage = reader_signal.get("hook_type_usage") or {}
    pattern_usage = reader_signal.get("pattern_usage") or {}
    review_trend = reader_signal.get("review_trend") or {}
    low_ranges = reader_signal.get("low_score_ranges") or []

    dominant_hook = ""
    if isinstance(hook_usage, dict) and hook_usage:
        dominant_hook = max(hook_usage.items(), key=lambda kv: kv[1])[0]

    dominant_pattern = ""
    if isinstance(pattern_usage, dict) and pattern_usage:
        dominant_pattern = max(pattern_usage.items(), key=lambda kv: kv[1])[0]

    overall_avg = float(review_trend.get("overall_avg") or 0.0)
    has_low_range = bool(low_ranges)
    hook_variety = len(hook_usage) if isinstance(hook_usage, dict) else 0
    pattern_variety = len(pattern_usage) if isinstance(pattern_usage, dict) else 0

    next_reason_clarity = 70.0 + (4.0 if has_low_range else 8.0)
    anchor_effectiveness = 68.0 + (6.0 if dominant_hook else 0.0) + (4.0 if overall_avg >= 75 else -4.0)
    rhythm_naturalness = 65.0 + min(10.0, float(hook_variety + pattern_variety) * 2.0)

    risk_flags: List[str] = []
    if has_low_range:
        risk_flags.append("low_score_recency")
    if dominant_pattern:
        risk_flags.append("pattern_overuse_watch")
    if overall_avg > 0 and overall_avg < 75:
        risk_flags.append("readability_guard")

    stage_mod = chapter % 5
    if stage_mod in {1, 2}:
        stage = "build_up"
    elif stage_mod in {3, 4}:
        stage = "confront"
    else:
        stage = "release"

    anchor_preset = GENRE_METHOD_ANCHORS.get(
        profile_key,
        {
            "pressure_source": "Survival goal/resource competition",
            "release_target": "Protagonist completes stage goal and leaves new action reason",
        },
    )

    return {
        "enabled": True,
        "framework": label,
        "pilot": profile_key,
        "genre_profile_key": profile_key,
        "chapter_stage": stage,
        "emotion_anchor": {
            "pressure_source": anchor_preset["pressure_source"],
            "release_target": anchor_preset["release_target"],
            "position_hint": "Set pressure in early section, release in middle-late section, avoid fixed character position marking",
        },
        "long_arc_controls": {
            "map_transition": "Stage transition inherits existing assets and relationship ledger, avoid ability and reward reset to zero",
            "power_guard": "Key victories must have mechanistic reasoning (information/resource/cost/strategy)",
            "antagonist_model": "Antagonist must have goal-means-cost three elements, avoid tool-person pushing plot",
        },
        "serialization_ops": {
            "next_reason": "Give a repeatable next chapter motivation sentence at chapter end or in late section",
            "interaction_note": "Reserve one debatable point for serialization interaction feedback",
        },
        "observability": {
            "next_reason_clarity": round(max(0.0, min(100.0, next_reason_clarity)), 2),
            "anchor_effectiveness": round(max(0.0, min(100.0, anchor_effectiveness)), 2),
            "rhythm_naturalness": round(max(0.0, min(100.0, rhythm_naturalness)), 2),
        },
        "signals": {
            "dominant_hook": dominant_hook,
            "dominant_pattern": dominant_pattern,
            "risk_flags": risk_flags,
        },
    }


def build_methodology_guidance_items(strategy_card: Dict[str, Any]) -> List[str]:
    if not isinstance(strategy_card, dict) or not strategy_card.get("enabled"):
        return []

    observability = strategy_card.get("observability") or {}
    signals = strategy_card.get("signals") or {}
    risk_flags = list(signals.get("risk_flags") or [])
    stage = str(strategy_card.get("chapter_stage") or "build_up")
    genre_key = str(strategy_card.get("genre_profile_key") or strategy_card.get("pilot") or "general")

    stage_text = {
        "build_up": "This chapter focuses on pressure setup, prioritize perceivable foreshadowing of threats and costs.",
        "confront": "This chapter focuses on direct confrontation, ensure break-out path is clear and reviewable.",
        "release": "This chapter focuses on release and aftermath, provide tangible benefits and introduce next question.",
    }.get(stage, "This chapter maintains complete pressure-breakout-aftermath chain.")

    items = [
        f"Methodology strategy (general/{genre_key}): {stage_text}",
        "Long-term control: Map transition inherits old assets, avoid protagonist entering new map with ability and resource reset to zero.",
        "Mechanism control: Key victories must state mechanistic reasoning and cost, do not use pure protagonist aura to crush.",
        (
            "Serialization interaction: Reserve one debatable point, strengthen next chapter update-chasing motivation."
            f"（next_reason={observability.get('next_reason_clarity')}）"
        ),
    ]

    if "pattern_overuse_watch" in risk_flags:
        dominant_pattern = str(signals.get("dominant_pattern") or "").strip()
        if dominant_pattern:
            items.append(f"Risk correction: Recent \"{dominant_pattern}\" frequency is high, add one heterogeneous sub-axis this chapter to avoid fatigue.")
    if "readability_guard" in risk_flags:
        items.append("Risk correction: Recent review average score is low, prioritize paragraph action-result closure and readability this chapter.")

    return items


def build_guidance_items(
    *,
    chapter: int,
    reader_signal: Dict[str, Any],
    genre_profile: Dict[str, Any],
    low_score_threshold: float,
    hook_diversify_enabled: bool,
) -> Dict[str, Any]:
    guidance: List[str] = []

    low_ranges = reader_signal.get("low_score_ranges") or []
    if low_ranges:
        worst = min(
            low_ranges,
            key=lambda row: float(row.get("overall_score", 9999)),
        )
        guidance.append(
            f"Chapter {chapter} prioritize fixing recent low score issues: reference chapters {worst.get('start_chapter')}-{worst.get('end_chapter')}, strengthen conflict progression and ending hook."
        )

    hook_usage = reader_signal.get("hook_type_usage") or {}
    if hook_usage and hook_diversify_enabled:
        dominant_hook = max(hook_usage.items(), key=lambda kv: kv[1])[0]
        guidance.append(
            f"Recent hook type \"{dominant_hook}\" usage is high, this chapter recommends hook differentiation to avoid continuous homogeneity."
        )

    pattern_usage = reader_signal.get("pattern_usage") or {}
    if pattern_usage:
        top_pattern = max(pattern_usage.items(), key=lambda kv: kv[1])[0]
        guidance.append(
            f"Coolpoint pattern \"{top_pattern}\" recent high frequency, this chapter can keep main coolpoint but add a new coolpoint sub-axis."
        )

    review_trend = reader_signal.get("review_trend") or {}
    overall_avg = review_trend.get("overall_avg")
    if isinstance(overall_avg, (int, float)) and float(overall_avg) < low_score_threshold:
        guidance.append(
            f"Recent review average {overall_avg:.1f} is below threshold {low_score_threshold:.1f}, recommend first securing stability: reduce scene skipping, add action-result closure each paragraph."
        )

    genre = str(genre_profile.get("genre") or "").strip()
    refs = genre_profile.get("reference_hints") or []
    if genre:
        guidance.append(f"Genre anchoring: Progress along \"{genre}\" narrative mainline, maintain genre reader expectation stable cash-in.")
    if refs:
        guidance.append(f"Genre strategy actionable hint: {refs[0]}")

    guidance.append("Web novel rhythm baseline: Give goal and resistance within 300 characters of chapter start, keep unclosed question at chapter end.")
    guidance.append("Cash-in density baseline: Give one micro cash-in every 600-900 characters, ensure at least 1 quantifiable change this chapter.")

    normalized_genre = to_profile_key(genre)
    genre_hint = GENRE_GUIDANCE_TEXT.get(normalized_genre)
    if genre_hint:
        guidance.append(genre_hint)

    composite_hints = genre_profile.get("composite_hints") or []
    if composite_hints:
        guidance.append(f"Composite genre synergy: {composite_hints[0]}")

    if not guidance:
        guidance.append("This chapter executes default high-readability strategy: conflict front-loaded, information back-loaded, section-end hook reserved.")

    return {
        "guidance": guidance,
        "low_ranges": low_ranges,
        "hook_usage": hook_usage,
        "pattern_usage": pattern_usage,
        "genre": genre,
    }


def build_writing_checklist(
    *,
    guidance_items: List[str],
    reader_signal: Dict[str, Any],
    genre_profile: Dict[str, Any],
    strategy_card: Dict[str, Any] | None = None,
    min_items: int,
    max_items: int,
    default_weight: float,
) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []

    def _add_item(
        item_id: str,
        label: str,
        *,
        weight: float | None = None,
        required: bool = False,
        source: str = "writing_guidance",
        verify_hint: str = "",
    ) -> None:
        if len(items) >= max_items:
            return
        if any(row.get("id") == item_id for row in items):
            return

        item_weight = float(weight if weight is not None else default_weight)
        if item_weight <= 0:
            item_weight = default_weight

        items.append(
            {
                "id": item_id,
                "label": label,
                "weight": round(item_weight, 2),
                "required": bool(required),
                "source": source,
                "verify_hint": verify_hint,
            }
        )

    low_ranges = reader_signal.get("low_score_ranges") or []
    if low_ranges:
        worst = min(low_ranges, key=lambda row: float(row.get("overall_score", 9999)))
        span = f"{worst.get('start_chapter')}-{worst.get('end_chapter')}"
        _add_item(
            "fix_low_score_range",
            f"Fix low score range issues (reference chapters {span})",
            weight=max(default_weight, 1.4),
            required=True,
            source="reader_signal.low_score_ranges",
            verify_hint="Complete at least 1 conflict upgrade, leave hook at section end.",
        )

    hook_usage = reader_signal.get("hook_type_usage") or {}
    if hook_usage:
        dominant_hook = max(hook_usage.items(), key=lambda kv: kv[1])[0]
        _add_item(
            "hook_diversification",
            f"Hook differentiation (avoid continuing single \"{dominant_hook}\")",
            weight=max(default_weight, 1.2),
            required=True,
            source="reader_signal.hook_type_usage",
            verify_hint="Ending hook type differs from main types in recent 20 chapters by at least 1.",
        )

    pattern_usage = reader_signal.get("pattern_usage") or {}
    if pattern_usage:
        top_pattern = max(pattern_usage.items(), key=lambda kv: kv[1])[0]
        _add_item(
            "coolpoint_combo",
            f"Main coolpoint + sub coolpoint combo (main coolpoint: {top_pattern})",
            weight=default_weight,
            required=False,
            source="reader_signal.pattern_usage",
            verify_hint="Add at least 1 new sub coolpoint that forms causal chain with main coolpoint.",
        )

    review_trend = reader_signal.get("review_trend") or {}
    overall_avg = review_trend.get("overall_avg")
    if isinstance(overall_avg, (int, float)):
        _add_item(
            "readability_loop",
            "Paragraph readability closure (action -> result -> emotion)",
            weight=max(default_weight, 1.1),
            required=True,
            source="reader_signal.review_trend",
            verify_hint="Spot check 3 paragraphs, all contain action-result closure.",
        )

    genre = str(genre_profile.get("genre") or "").strip()
    if genre:
        _add_item(
            "genre_anchor_consistency",
            f"Genre anchor consistency ({genre})",
            weight=max(default_weight, 1.1),
            required=True,
            source="genre_profile.genre",
            verify_hint="Main conflict remains consistent with genre core promise.",
        )

    if isinstance(strategy_card, dict) and strategy_card.get("enabled"):
        _add_item(
            "methodology_next_reason",
            "Methodology: Next chapter motivation must be repeatable (chapter end or late section)",
            weight=default_weight,
            required=False,
            source="methodology.next_reason",
            verify_hint="Extract one motivation sentence for \"why click next chapter\".",
        )
        _add_item(
            "methodology_power_guard",
            "Methodology: Level-up and break-out give mechanistic reasoning and cost",
            weight=default_weight,
            required=False,
            source="methodology.power_guard",
            verify_hint="Write clear at least 1 mechanistic reasoning and 1 cost."
        )
        _add_item(
            "methodology_antagonist_pressure",
            "Methodology: Antagonist actions have goal-means-cost",
            weight=default_weight,
            required=False,
            source="methodology.antagonist",
            verify_hint="Antagonist is not tool-person pushing plot, must have explainable action logic.",
        )

    for idx, text in enumerate(guidance_items, start=1):
        if len(items) >= max_items:
            break
        label = str(text).strip()
        if not label:
            continue
        _add_item(
            f"guidance_item_{idx}",
            label,
            weight=default_weight,
            required=False,
            source="writing_guidance.guidance_items",
            verify_hint="After completion, can locate corresponding paragraph in main text.",
        )

    fallback_items = [
        (
            "opening_conflict",
            "Give conflict trigger within 300 characters of opening",
            "Opening paragraph shows clear goal and resistance.",
        ),
        (
            "scene_goal_block",
            "Scene goal and resistance clear",
            "Each scene has at least 1 verifiable goal.",
        ),
        (
            "ending_hook",
            "Section-end hook and introduce next question",
            "Ending shows unresolved question or next action.",
        ),
    ]
    for item_id, label, verify_hint in fallback_items:
        if len(items) >= min_items or len(items) >= max_items:
            break
        _add_item(
            item_id,
            label,
            weight=default_weight,
            required=False,
            source="fallback",
            verify_hint=verify_hint,
        )

    return items[:max_items]


def is_checklist_item_completed(item: Dict[str, Any], reader_signal: Dict[str, Any]) -> bool:
    item_id = str(item.get("id") or "")
    if item_id in {"fix_low_score_range", "readability_loop"}:
        review_trend = reader_signal.get("review_trend") or {}
        overall = review_trend.get("overall_avg")
        return isinstance(overall, (int, float)) and float(overall) >= 75.0

    if item_id == "hook_diversification":
        hook_usage = reader_signal.get("hook_type_usage") or {}
        return len(hook_usage) >= 2

    if item_id == "coolpoint_combo":
        pattern_usage = reader_signal.get("pattern_usage") or {}
        return len(pattern_usage) >= 2

    if item_id == "genre_anchor_consistency":
        return True

    source = str(item.get("source") or "")
    if source.startswith("fallback"):
        return True

    if source.startswith("methodology."):
        # Methodology items currently serve as soft hints, only observe and guide, do not participate in scoring.
        return True

    return False
