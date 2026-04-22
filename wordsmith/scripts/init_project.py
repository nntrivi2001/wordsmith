#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web novel project initialization script

Goals:
- Generate a runnable project structure (webnovel-project)
- Create/update .webnovel/state.json (runtime truth)
- Generate base settings collection and outline template files (for use by /webnovel-plan and /webnovel-write)

Notes:
- This script is the "sole allowed file generation entry point" for the command /webnovel-init (consistent with command documentation).
- Generated content is primarily "template skeletons" for AI/author to fill in later; ensures all key files exist.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from runtime_compat import enable_windows_utf8_stdio
from typing import Any, Dict, List
import re

# Security fix: import security utility functions
from security_utils import sanitize_commit_message, atomic_write_json, is_git_available
from project_locator import write_current_project_pointer


# Windows encoding compatibility fix
if sys.platform == "win32":
    enable_windows_utf8_stdio()


def _read_text_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _write_text_if_missing(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return
    path.write_text(content, encoding="utf-8")


def _split_genre_keys(genre: str) -> list[str]:
    raw = (genre or "").strip()
    if not raw:
        return []
    # Support composite genres: A+B / A+B / A+B / A+B / A,B / A+B
    raw = re.sub(r"[＋/、]", "+", raw)
    raw = raw.replace("+", "+")
    parts = [p.strip() for p in raw.split("+") if p.strip()]
    return parts or [raw]


def _normalize_genre_key(key: str) -> str:
    aliases = {
        "xianxia/fantasy": "xianxia",
        "fantasy-xianxia": "xianxia",
        "fantasy": "xianxia",
        "cultivation": "xianxia",
        "urban-cultivation": "urban-abnormality",
        "urban-high-power": "high-power",
        "urban-supernatural": "urban-brainhole",
        "ancient-speculative": "historical",
        "gaming-esports": "esports",
        "esports": "esports",
        "livestream": "streaming",
        "streaming-commerce": "streaming",
        "streamer": "streaming",
        "lovecraftian": "lovecraftian",
        "lovecraftian-suspense": "lovecraftian",
    }
    return aliases.get(key, key)


def _apply_label_replacements(text: str, replacements: Dict[str, str]) -> str:
    if not text or not replacements:
        return text
    lines = text.splitlines()
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        for label, value in replacements.items():
            if not value:
                continue
            prefix = f"- {label}: "
            if stripped.startswith(prefix):
                leading = line[: len(line) - len(stripped)]
                lines[i] = f"{leading}{prefix}{value}"
    return "\n".join(lines)


def _parse_tier_map(raw: str) -> Dict[str, str]:
    result: Dict[str, str] = {}
    if not raw:
        return result
    for part in raw.split(";"):
        part = part.strip()
        if not part:
            continue
        if ":" in part:
            key, val = part.split(":", 1)
            result[key.strip()] = val.strip()
    return result


def _render_team_rows(names: List[str], roles: List[str]) -> List[str]:
    rows = []
    for idx, name in enumerate(names):
        role = roles[idx] if idx < len(roles) else ""
        rows.append(f"| {name} | {role or 'Main/Sub'} | | | |")
    return rows


def _ensure_state_schema(state: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure state.json has the field set required by the v5.1 schema (carried over in v5.4).

    v5.1 changes:
    - entities_v3 and alias_index have been migrated to index.db, no longer stored in state.json
    - structured_relationships has been migrated to index.db relationships table
    - state.json is kept lean (< 5KB)
    """
    state.setdefault("project_info", {})
    state.setdefault("progress", {})
    state.setdefault("protagonist_state", {})
    state.setdefault("relationships", {})  # required by update_state.py
    state.setdefault("disambiguation_warnings", [])
    state.setdefault("disambiguation_pending", [])
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
    # v5.1: entities_v3, alias_index, structured_relationships have been migrated to index.db
    # No longer initializing these fields in state.json

    # progress schema evolution
    state["progress"].setdefault("current_chapter", 0)
    state["progress"].setdefault("total_words", 0)
    state["progress"].setdefault("last_updated", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    state["progress"].setdefault("volumes_completed", [])
    state["progress"].setdefault("current_volume", 1)
    state["progress"].setdefault("volumes_planned", [])

    # protagonist schema evolution
    ps = state["protagonist_state"]
    ps.setdefault("name", "")
    ps.setdefault("power", {"realm": "", "layer": 1, "bottleneck": ""})
    ps.setdefault("location", {"current": "", "last_chapter": 0})
    ps.setdefault("golden_finger", {"name": "", "level": 1, "cooldown": 0, "skills": []})
    ps.setdefault("attributes", {})

    return state


def _build_master_outline(target_chapters: int, *, chapters_per_volume: int = 50) -> str:
    volumes = (target_chapters - 1) // chapters_per_volume + 1 if target_chapters > 0 else 1
    lines: list[str] = [
        "# Master Outline",
        "",
        "> This file is the 'master outline skeleton', to be refined into volume outlines and chapter outlines by /webnovel-plan.",
        "",
        "## Volume Structure",
        "",
    ]

    for v in range(1, volumes + 1):
        start = (v - 1) * chapters_per_volume + 1
        end = min(v * chapters_per_volume, target_chapters)
        lines.extend(
            [
                f"### Volume {v} (Chapters {start}-{end})",
                "- Core conflict:",
                "- Key payoff moments:",
                "- Volume climax:",
                "- Main characters:",
                "- Key foreshadowing (plant/resolve):",
                "",
            ]
        )

    return "\n".join(lines).rstrip() + "\n"


def _inject_volume_rows(template_text: str, target_chapters: int, *, chapters_per_volume: int = 50) -> str:
    """Inject volume rows into the master outline template's volume table (if a header exists)."""
    lines = template_text.splitlines()
    header_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("| Volume"):
            header_idx = i
            break
    if header_idx is None:
        return template_text

    insert_idx = header_idx + 2 if header_idx + 1 < len(lines) else len(lines)
    volumes = (target_chapters - 1) // chapters_per_volume + 1 if target_chapters > 0 else 1
    rows = []
    for v in range(1, volumes + 1):
        start = (v - 1) * chapters_per_volume + 1
        end = min(v * chapters_per_volume, target_chapters)
        rows.append(f"| {v} | | Ch{start}-{end} | | |")

    # Avoid duplicate insertion (if template already has data rows)
    existing = {line.strip() for line in lines}
    rows = [r for r in rows if r.strip() not in existing]
    return "\n".join(lines[:insert_idx] + rows + lines[insert_idx:])


def init_project(
    project_dir: str,
    title: str,
    genre: str,
    *,
    protagonist_name: str = "",
    target_words: int = 2_000_000,
    target_chapters: int = 600,
    golden_finger_name: str = "",
    golden_finger_type: str = "",
    golden_finger_style: str = "",
    core_selling_points: str = "",
    protagonist_structure: str = "",
    heroine_config: str = "",
    heroine_names: str = "",
    heroine_role: str = "",
    co_protagonists: str = "",
    co_protagonist_roles: str = "",
    antagonist_tiers: str = "",
    world_scale: str = "",
    factions: str = "",
    power_system_type: str = "",
    social_class: str = "",
    resource_distribution: str = "",
    gf_visibility: str = "",
    gf_irreversible_cost: str = "",
    protagonist_desire: str = "",
    protagonist_flaw: str = "",
    protagonist_archetype: str = "",
    antagonist_level: str = "",
    target_reader: str = "",
    platform: str = "",
    currency_system: str = "",
    currency_exchange: str = "",
    sect_hierarchy: str = "",
    cultivation_chain: str = "",
    cultivation_subtiers: str = "",
) -> None:
    project_path = Path(project_dir).expanduser().resolve()
    if ".claude" in project_path.parts:
        raise SystemExit("Refusing to initialize a project inside .claude. Choose a different directory.")
    project_path.mkdir(parents=True, exist_ok=True)

    # Directory structure (compatible with "volume directories" and future extensions)
    directories = [
        ".webnovel/backups",
        ".webnovel/archive",
        ".webnovel/summaries",
        "Settings/Characters/Main",
        "Settings/Characters/Secondary",
        "Settings/Characters/Antagonists",
        "Settings/Items",
        "Settings/Others",
        "Outlines",
        "Body",
        "ReviewReports",
    ]
    for dir_path in directories:
        (project_path / dir_path).mkdir(parents=True, exist_ok=True)

    # state.json (create or incrementally fill)
    state_path = project_path / ".webnovel" / "state.json"
    if state_path.exists():
        try:
            state: Dict[str, Any] = json.loads(state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            state = {}
    else:
        state = {}

    state = _ensure_state_schema(state)
    created_at = state.get("project_info", {}).get("created_at") or datetime.now().strftime("%Y-%m-%d")

    state["project_info"].update(
        {
            "title": title,
            "genre": genre,
            "created_at": created_at,
            "target_words": int(target_words),
            "target_chapters": int(target_chapters),
            # The following fields are "initialization metadata", not affecting runtime scripts
            "golden_finger_name": golden_finger_name,
            "golden_finger_type": golden_finger_type,
            "golden_finger_style": golden_finger_style,
            "core_selling_points": core_selling_points,
            "protagonist_structure": protagonist_structure,
            "heroine_config": heroine_config,
            "heroine_names": heroine_names,
            "heroine_role": heroine_role,
            "co_protagonists": co_protagonists,
            "co_protagonist_roles": co_protagonist_roles,
            "antagonist_tiers": antagonist_tiers,
            "world_scale": world_scale,
            "factions": factions,
            "power_system_type": power_system_type,
            "social_class": social_class,
            "resource_distribution": resource_distribution,
            "gf_visibility": gf_visibility,
            "gf_irreversible_cost": gf_irreversible_cost,
            "target_reader": target_reader,
            "platform": platform,
            "currency_system": currency_system,
            "currency_exchange": currency_exchange,
            "sect_hierarchy": sect_hierarchy,
            "cultivation_chain": cultivation_chain,
            "cultivation_subtiers": cultivation_subtiers,
        }
    )

    if protagonist_name:
        state["protagonist_state"]["name"] = protagonist_name

    gf_type_norm = (golden_finger_type or "").strip()
    if gf_type_norm in {"none", "no-golden-finger", "none"}:
        state["protagonist_state"]["golden_finger"]["name"] = "No golden finger"
        state["protagonist_state"]["golden_finger"]["level"] = 0
        state["protagonist_state"]["golden_finger"]["cooldown"] = 0
    elif golden_finger_name:
        state["protagonist_state"]["golden_finger"]["name"] = golden_finger_name

    # Ensure golden_finger field exists and is editable
    if not state["protagonist_state"]["golden_finger"].get("name"):
        state["protagonist_state"]["golden_finger"]["name"] = "Unnamed golden finger"

    state["progress"]["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    state_path.parent.mkdir(parents=True, exist_ok=True)
    # Use atomic write (initialization does not need to back up old file)
    atomic_write_json(state_path, state, use_lock=True, backup=False)

    # Read built-in templates (optional)
    script_dir = Path(__file__).resolve().parent
    templates_dir = script_dir.parent / "templates"
    output_templates_dir = templates_dir / "output"
    genre_key = (genre or "").strip()
    genre_keys = [_normalize_genre_key(k) for k in _split_genre_keys(genre_key)]
    genre_templates = []
    seen = set()
    for key in genre_keys:
        if not key or key in seen:
            continue
        seen.add(key)
        template_text = _read_text_if_exists(templates_dir / "genres" / f"{key}.md")
        if template_text:
            genre_templates.append(template_text.strip())
    genre_template = "\n\n---\n\n".join(genre_templates)
    golden_finger_templates = _read_text_if_exists(templates_dir / "golden-finger-templates.md")
    output_worldview = _read_text_if_exists(output_templates_dir / "Settings-Worldview.md")
    output_power = _read_text_if_exists(output_templates_dir / "Settings-PowerSystem.md")
    output_protagonist = _read_text_if_exists(output_templates_dir / "Settings-ProtagonistCard.md")
    output_heroine = _read_text_if_exists(output_templates_dir / "Settings-HeroineCard.md")
    output_team = _read_text_if_exists(output_templates_dir / "Settings-ProtagonistTeam.md")
    output_golden_finger = _read_text_if_exists(output_templates_dir / "Settings-GoldenFinger.md")
    output_outline = _read_text_if_exists(output_templates_dir / "Outline-Master.md")
    output_fusion = _read_text_if_exists(output_templates_dir / "CompositeGenre-FusionLogic.md")
    output_antagonist = _read_text_if_exists(output_templates_dir / "Settings-AntagonistDesign.md")

    # Base files (only generate when missing, to avoid overwriting existing content)
    now = datetime.now().strftime("%Y-%m-%d")

    worldview_content = output_worldview.strip() if output_worldview else ""
    if not worldview_content:
        worldview_content = "\n".join(
            [
                "# Worldview",
                "",
                f"> Project: {title} | Genre: {genre} | Created: {now}",
                "",
                "## One-sentence Worldview",
                "- (Describe the core rules and selling points of the world in one sentence)",
                "",
                "## Core Rules (setting as physics)",
                "- Rule 1:",
                "- Rule 2:",
                "- Rule 3:",
                "",
                "## Factions and Geography (brief)",
                "- Main factions:",
                "- Key locations:",
                "",
                "## Reference Genre Template (can be deleted/modified)",
                "",
                (genre_template.strip() + "\n") if genre_template else "(No matching genre template found; fill in manually)\n",
            ]
        ).rstrip() + "\n"
    else:
        worldview_content = _apply_label_replacements(
            worldview_content,
            {
                "Continent/Plane Count": world_scale,
                "Core Factions": factions,
                "Social Class": social_class,
                "Resource Distribution": resource_distribution,
                "Sect/Organization Hierarchy": sect_hierarchy,
                "Currency System": currency_system,
                "Exchange Rules": currency_exchange,
            },
        )
    _write_text_if_missing(
        project_path / "Settings" / "Worldview.md",
        worldview_content,
    )

    power_content = output_power.strip() if output_power else ""
    if not power_content:
        power_content = "\n".join(
            [
                "# Power System",
                "",
                f"> Project: {title} | Genre: {genre} | Created: {now}",
                "",
                "## Level/Realm Divisions",
                "- (List levels from weakest to strongest, with breakthrough conditions and costs)",
                "",
                "## Skills/Ability Rules",
                "- Acquisition method:",
                "- Costs and side effects:",
                "- Advancement and combinations:",
                "",
                "## Prohibitions (prevent worldbuilding collapse)",
                "- Cannot use high-level abilities without reaching the required level (setting as physics)",
                "- New abilities must be registered in the registry (inventions must be declared)",
                "",
            ]
        ).rstrip() + "\n"
    else:
        power_content = _apply_label_replacements(
            power_content,
            {
                "System Type": power_system_type,
                "Typical Realm Chain (optional)": cultivation_chain,
                "Sub-realm Divisions": cultivation_subtiers,
            },
        )
    _write_text_if_missing(
        project_path / "Settings" / "PowerSystem.md",
        power_content,
    )

    protagonist_content = output_protagonist.strip() if output_protagonist else ""
    if not protagonist_content:
        protagonist_content = "\n".join(
            [
                "# Protagonist Card",
                "",
                f"> Protagonist: {protagonist_name or '(to be filled)'} | Project: {title} | Created: {now}",
                "",
                "## Three Core Elements",
                f"- Desire: {protagonist_desire or '(to be filled)'}",
                f"- Flaw: {protagonist_flaw or '(to be filled)'}",
                f"- Archetype: {protagonist_archetype or '(to be filled)'}",
                "",
                "## Initial State (story start)",
                "- Identity:",
                "- Resources:",
                "- Constraints:",
                "",
                "## Golden Finger Overview",
                f"- Name: {golden_finger_name or '(to be filled)'}",
                f"- Type: {golden_finger_type or '(to be filled)'}",
                f"- Style: {golden_finger_style or '(to be filled)'}",
                "- Growth curve:",
                "",
            ]
        ).rstrip() + "\n"
    else:
        protagonist_content = _apply_label_replacements(
            protagonist_content,
            {
                "Name": protagonist_name,
                "True Desire (may be unaware)": protagonist_desire,
                "Character Flaw": protagonist_flaw,
            },
        )
    _write_text_if_missing(
        project_path / "Settings" / "ProtagonistCard.md",
        protagonist_content,
    )

    heroine_content = output_heroine.strip() if output_heroine else ""
    if heroine_content:
        heroine_content = _apply_label_replacements(
            heroine_content,
            {
                "Name": heroine_names,
                "Relationship with Protagonist (rival/ally/conspirator/restraint)": heroine_role,
            },
        )
        _write_text_if_missing(project_path / "Settings" / "HeroineCard.md", heroine_content)

    team_content = output_team.strip() if output_team else ""
    if team_content:
        names = [n.strip() for n in co_protagonists.split(",") if n.strip()] if co_protagonists else []
        roles = [r.strip() for r in co_protagonist_roles.split(",") if r.strip()] if co_protagonist_roles else []
        if names:
            lines = team_content.splitlines()
            new_rows = _render_team_rows(names, roles)
            replaced = False
            out_lines: List[str] = []
            for line in lines:
                if line.strip().startswith("| Protagonist A"):
                    out_lines.extend(new_rows)
                    replaced = True
                    continue
                if replaced and line.strip().startswith("| Protagonist"):
                    continue
                out_lines.append(line)
            team_content = "\n".join(out_lines)
        _write_text_if_missing(
            project_path / "Settings" / "ProtagonistTeam.md",
            team_content,
        )

    golden_finger_content = output_golden_finger.strip() if output_golden_finger else ""
    if not golden_finger_content:
        golden_finger_content = "\n".join(
            [
                "# Golden Finger Design",
                "",
                f"> Project: {title} | Genre: {genre} | Created: {now}",
                "",
                "## Selection",
                f"- Name: {golden_finger_name or '(to be filled)'}",
                f"- Type: {golden_finger_type or '(to be filled)'}",
                f"- Style: {golden_finger_style or '(to be filled)'}",
                "",
                "## Rules (must be clearly defined)",
                "- Trigger condition:",
                "- Cooldown/cost:",
                "- Upper limit:",
                "- Backlash/risk:",
                "",
                "## Growth Curve (chapter planning)",
                "- Lv1:",
                "- Lv2:",
                "- Lv3:",
                "",
                "## Template Reference (can be deleted/modified)",
                "",
                (golden_finger_templates.strip() + "\n") if golden_finger_templates else "(No golden finger template library found)\n",
            ]
        ).rstrip() + "\n"
    else:
        golden_finger_content = _apply_label_replacements(
            golden_finger_content,
            {
                "Type": golden_finger_type,
                "Reader Visibility": gf_visibility,
                "Irreversible Cost": gf_irreversible_cost,
            },
        )
    _write_text_if_missing(
        project_path / "Settings" / "GoldenFingerDesign.md",
        golden_finger_content,
    )

    fusion_content = output_fusion.strip() if output_fusion else ""
    if fusion_content:
        _write_text_if_missing(
            project_path / "Settings" / "CompositeGenre-FusionLogic.md",
            fusion_content,
        )

    antagonist_content = output_antagonist.strip() if output_antagonist else ""
    if not antagonist_content:
        antagonist_content = "\n".join(
            [
                "# Antagonist Design",
                "",
                f"> Project: {title} | Created: {now}",
                "",
                f"- Antagonist level: {antagonist_level or '(to be filled)'}",
                "- Motivation:",
                "- Resources/factions:",
                "- Mirror relationship with protagonist:",
                "- Final outcome:",
                "",
            ]
        ).rstrip() + "\n"
    else:
        tier_map = _parse_tier_map(antagonist_tiers)
        if tier_map:
            lines = antagonist_content.splitlines()
            out_lines = []
            for line in lines:
                if line.strip().startswith("| Minor Antagonist"):
                    name = tier_map.get("Minor Antagonist", "")
                    out_lines.append(f"| Minor Antagonist | {name} | Early stage | | |")
                    continue
                if line.strip().startswith("| Mid Antagonist"):
                    name = tier_map.get("Mid Antagonist", "")
                    out_lines.append(f"| Mid Antagonist | {name} | Mid stage | | |")
                    continue
                if line.strip().startswith("| Major Antagonist"):
                    name = tier_map.get("Major Antagonist", "")
                    out_lines.append(f"| Major Antagonist | {name} | Late stage | | |")
                    continue
                out_lines.append(line)
            antagonist_content = "\n".join(out_lines)
    _write_text_if_missing(project_path / "Settings" / "AntagonistDesign.md", antagonist_content)

    outline_content = output_outline.strip() if output_outline else ""
    if outline_content:
        outline_content = _inject_volume_rows(outline_content, int(target_chapters)).rstrip() + "\n"
    else:
        outline_content = _build_master_outline(int(target_chapters))
    _write_text_if_missing(project_path / "Outlines" / "MasterOutline.md", outline_content)

    _write_text_if_missing(
        project_path / "Outlines" / "PayoffPlanning.md",
        "\n".join(
            [
                "# Payoff Planning",
                "",
                f"> Project: {title} | Genre: {genre} | Created: {now}",
                "",
                "## Core Selling Points (from initialization input)",
                f"- {core_selling_points or '(to be filled; recommended 1-3 items separated by commas)'}",
                "",
                "## Density Goals (recommended)",
                "- At least 1 minor payoff per chapter",
                "- At least 1 major payoff every 5 chapters",
                "",
                "## Distribution Table (example, can be modified)",
                "",
                "| Chapter Range | Dominant Payoff Type | Notes |",
                "|---|---|---|",
                "| 1-5 | Golden finger/face-slap/reversal | Opening hook + character establishment |",
                "| 6-10 | Level-up/gains | Enter main story rhythm |",
                "",
            ]
        ),
    )

    # Generate environment variable template (do not write real keys)
    _write_text_if_missing(
        project_path / ".env.example",
        "\n".join(
            [
                "# Webnovel Writer configuration example (copy as .env and fill in)",
                "# Note: Do NOT commit .env files containing real API_KEYs to version control.",
                "",
                "# Embedding",
                "EMBED_BASE_URL=https://api-inference.modelscope.cn/v1",
                "EMBED_MODEL=Qwen/Qwen3-Embedding-8B",
                "EMBED_API_KEY=",
                "",
                "# Rerank",
                "RERANK_BASE_URL=https://api.jina.ai/v1",
                "RERANK_MODEL=jina-reranker-v3",
                "RERANK_API_KEY=",
                "",
            ]
        )
        + "\n",
    )

    # Git initialization (only if no .git exists in project directory and Git is available)
    git_dir = project_path / ".git"
    if not git_dir.exists():
        if not is_git_available():
            print("\nWARNING: Git is not available, skipping version control initialization")
            print("TIP: To enable Git version control, install Git: https://git-scm.com/")
        else:
            print("\nInitializing Git repository...")
            try:
                subprocess.run(["git", "init"], cwd=project_path, check=True, capture_output=True, text=True)

                gitignore_file = project_path / ".gitignore"
                if not gitignore_file.exists():
                    gitignore_file.write_text(
                        """# Python
__pycache__/
*.py[cod]
*.so

# Env (keep .env.example)
.env
.env.*
!.env.example

# Temporary files
*.tmp
*.bak
.DS_Store

# IDE
.vscode/
.idea/

# Don't ignore .webnovel (we need to track state.json)
# But ignore cache files
.webnovel/context_cache.json
.webnovel/*.lock
.webnovel/*.bak
""",
                        encoding="utf-8",
                    )

                subprocess.run(["git", "add", "."], cwd=project_path, check=True, capture_output=True)
                # Security fix: sanitize title to prevent command injection
                safe_title = sanitize_commit_message(title)
                subprocess.run(
                    ["git", "commit", "-m", f"Initialize web novel project: {safe_title}"],
                    cwd=project_path,
                    check=True,
                    capture_output=True,
                )
                print("Git initialized.")
            except subprocess.CalledProcessError as e:
                print(f"Git init failed (non-fatal): {e}")

    # Record workspace default project pointer (non-blocking)
    try:
        pointer_file = write_current_project_pointer(project_path)
        if pointer_file is not None:
            print(f"Default project pointer updated: {pointer_file}")
    except Exception as e:
        print(f"Default project pointer update failed (non-fatal): {e}")

    print(f"\nProject initialized at: {project_path}")
    print("Key files:")
    print(" - .webnovel/state.json")
    print(" - Settings/Worldview.md")
    print(" - Settings/PowerSystem.md")
    print(" - Settings/ProtagonistCard.md")
    print(" - Settings/GoldenFingerDesign.md")
    print(" - Outlines/MasterOutline.md")
    print(" - Outlines/PayoffPlanning.md")


def main() -> None:
    parser = argparse.ArgumentParser(description="Web novel project initialization script (generate project structure + state.json + base templates)")
    parser.add_argument("project_dir", help="Project directory (recommended: ./webnovel-project)")
    parser.add_argument("title", help="Novel title")
    parser.add_argument(
        "genre",
        help="Genre type (can combine with '+', e.g.: urban-brainhole+rule-horror; examples: cultivation/system/urban-power/historical/realistic)",
    )

    parser.add_argument("--protagonist-name", default="", help="Protagonist name")
    parser.add_argument("--target-words", type=int, default=2_000_000, help="Target total word count (default 2000000)")
    parser.add_argument("--target-chapters", type=int, default=600, help="Target total chapter count (default 600)")

    parser.add_argument("--golden-finger-name", default="", help="Golden finger name/system name (recommended reader-visible alias)")
    parser.add_argument("--golden-finger-type", default="", help="Golden finger type (e.g. system/appraisal/sign-in)")
    parser.add_argument("--golden-finger-style", default="", help="Golden finger style (e.g. cold-tool/snarky)")
    parser.add_argument("--core-selling-points", default="", help="Core selling points (comma-separated)")
    parser.add_argument("--protagonist-structure", default="", help="Protagonist structure (single/multiple)")
    parser.add_argument("--heroine-config", default="", help="Heroine configuration (none/single/multiple)")
    parser.add_argument("--heroine-names", default="", help="Heroine names (multiple separated by commas)")
    parser.add_argument("--heroine-role", default="", help="Heroine role (career/romance/confrontation)")
    parser.add_argument("--co-protagonists", default="", help="Co-protagonist names (comma-separated)")
    parser.add_argument("--co-protagonist-roles", default="", help="Co-protagonist roles (comma-separated)")
    parser.add_argument("--antagonist-tiers", default="", help="Antagonist tiers (e.g. minor:Zhang San;mid:Li Si;main:Wang Wu)")
    parser.add_argument("--world-scale", default="", help="World scale")
    parser.add_argument("--factions", default="", help="Faction layout/core factions")
    parser.add_argument("--power-system-type", default="", help="Power system type")
    parser.add_argument("--social-class", default="", help="Social class structure")
    parser.add_argument("--resource-distribution", default="", help="Resource distribution")
    parser.add_argument("--gf-visibility", default="", help="Golden finger visibility (open/semi-open/hidden)")
    parser.add_argument("--gf-irreversible-cost", default="", help="Golden finger irreversible cost")
    parser.add_argument("--currency-system", default="", help="Currency system")
    parser.add_argument("--currency-exchange", default="", help="Currency exchange/denomination rules")
    parser.add_argument("--sect-hierarchy", default="", help="Sect/organization hierarchy")
    parser.add_argument("--cultivation-chain", default="", help="Typical cultivation realm chain")
    parser.add_argument("--cultivation-subtiers", default="", help="Sub-realm divisions (early/mid/late/peak etc.)")

    # Deep mode optional parameters (for pre-filling templates)
    parser.add_argument("--protagonist-desire", default="", help="Protagonist's core desire (deep mode)")
    parser.add_argument("--protagonist-flaw", default="", help="Protagonist's character flaw (deep mode)")
    parser.add_argument("--protagonist-archetype", default="", help="Protagonist archetype type (deep mode)")
    parser.add_argument("--antagonist-level", default="", help="Antagonist level (deep mode)")
    parser.add_argument("--target-reader", default="", help="Target reader (deep mode)")
    parser.add_argument("--platform", default="", help="Publishing platform (deep mode)")

    args = parser.parse_args()

    init_project(
        args.project_dir,
        args.title,
        args.genre,
        protagonist_name=args.protagonist_name,
        target_words=args.target_words,
        target_chapters=args.target_chapters,
        golden_finger_name=args.golden_finger_name,
        golden_finger_type=args.golden_finger_type,
        golden_finger_style=args.golden_finger_style,
        core_selling_points=args.core_selling_points,
        protagonist_structure=args.protagonist_structure,
        heroine_config=args.heroine_config,
        heroine_names=args.heroine_names,
        heroine_role=args.heroine_role,
        co_protagonists=args.co_protagonists,
        co_protagonist_roles=args.co_protagonist_roles,
        antagonist_tiers=args.antagonist_tiers,
        world_scale=args.world_scale,
        factions=args.factions,
        power_system_type=args.power_system_type,
        social_class=args.social_class,
        resource_distribution=args.resource_distribution,
        gf_visibility=args.gf_visibility,
        gf_irreversible_cost=args.gf_irreversible_cost,
        protagonist_desire=args.protagonist_desire,
        protagonist_flaw=args.protagonist_flaw,
        protagonist_archetype=args.protagonist_archetype,
        antagonist_level=args.antagonist_level,
        target_reader=args.target_reader,
        platform=args.platform,
        currency_system=args.currency_system,
        currency_exchange=args.currency_exchange,
        sect_hierarchy=args.sect_hierarchy,
        cultivation_chain=args.cultivation_chain,
        cultivation_subtiers=args.cultivation_subtiers,
    )


if __name__ == "__main__":
    main()
