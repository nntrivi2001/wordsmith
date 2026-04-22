#!/usr/bin/env python3
"""
Visual Status Reporter System

Core Philosophy: Facing 1000 chapters, authors get lost. They need a "macro view" capability.

Features:
1. Character activity analysis: Which characters haven't appeared too long (dropped character stats)
2. Foreshadowing depth analysis: Which plot holes have been open too long (>200k words unresolved) + urgency ranking
3. Cool point rhythm distribution: Frequency of climax points throughout the book (heatmap)
4. Word count distribution stats: Word count distribution per volume/section
5. Relationship graph: Affection/hatred trends
6. Strand Weave rhythm analysis: Quest/Fire/Constellation three-strand ratio stats
7. Foreshadowing urgency ranking: Priority calculation based on three-tier system (core/side/decor)

Output format:
  - Markdown report (.wordsmith/health_report.md)
  - Contains Mermaid charts (character relationship graph, cool point heatmap)

Usage:
  # Generate complete health report
  python status_reporter.py --output .wordsmith/health_report.md

  # Analyze character activity only
  python status_reporter.py --focus characters

  # Analyze foreshadowing only
  python status_reporter.py --focus foreshadowing

  # Analyze cool point rhythm only
  python status_reporter.py --focus pacing

  # Analyze Strand Weave rhythm
  python status_reporter.py --focus strand

Report example:
  # Full Book Health Report

  ## 📊 Basic Data

  - **Total chapters**: 450 chapters
  - **Total words**: 1,985,432 words
  - **Average words per chapter**: 4,412 words
  - **Progress**: 99.3% (target 2,000,000 words)

  ## ⚠️ Character Drop (3 characters)

  | Character | Last Appearance | Absent Chapters | Status |
  |------|---------|---------|------|
  | Li Xue | Chapter 350 | 100 chapters | 🔴 Critical drop |
  | Blood Evil Sect Leader | Chapter 300 | 150 chapters | 🔴 Critical drop |
  | Tian Yun Sect Leader | Chapter 400 | 50 chapters | 🟡 Mild drop |

  ## ⚠️ Foreshadowing Timeout (2 items)

  | Foreshadowing Content | Planted Chapter | Chapters Elapsed | Status |
  |---------|---------|---------|------|
  | "Secret of Lin Family Treasury Inscription" | Chapter 200 | 250 chapters | 🔴 Critical timeout |
  | "Origin of Mysterious Jade Pendant" | Chapter 270 | 180 chapters | 🟡 Mild timeout |

  ## 📈 Cool Point Rhythm Distribution

  ```
  Chapters 1-100    ████████████ Excellent (1200 words/point)
  Chapters 101-200  ██████████ Good (1500 words/point)
  Chapters 201-300  ████████ Good (1600 words/point)
  Chapters 301-400  ████ Low (2200 words/point) ⚠️
  Chapters 401-450  ██████ Good (1550 words/point)
  ```

  ## 💑 Relationship Trends

  ```mermaid
  graph LR
    Protagonist -->|Affection 95| Li Xue
    Protagonist -->|Affection 60| Murong Xue
    Protagonist -->|Hatred 100| Blood Evil Sect
  ```
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
from collections import defaultdict
from project_locator import resolve_project_root
from chapter_paths import extract_chapter_num_from_filename
from runtime_compat import enable_windows_utf8_stdio

# Import configuration
try:
    from data_modules.config import get_config, DataModulesConfig
    from data_modules.index_manager import IndexManager
    from data_modules.state_validator import (
        get_chapter_meta_entry,
        is_resolved_foreshadowing_status,
        normalize_foreshadowing_tier,
        normalize_state_runtime_sections,
        resolve_chapter_field,
        to_positive_int,
    )
except ImportError:
    from scripts.data_modules.config import get_config, DataModulesConfig
    from scripts.data_modules.index_manager import IndexManager
    from scripts.data_modules.state_validator import (
        get_chapter_meta_entry,
        is_resolved_foreshadowing_status,
        normalize_foreshadowing_tier,
        normalize_state_runtime_sections,
        resolve_chapter_field,
        to_positive_int,
    )

def _is_resolved_foreshadowing_status(raw_status: Any) -> bool:
    """Determine if foreshadowing has been resolved (compatible with historical fields and synonyms)."""
    return is_resolved_foreshadowing_status(raw_status)

def _enable_windows_utf8_stdio() -> None:
    """Enable UTF-8 output on Windows; skip in pytest to avoid capture conflicts."""
    enable_windows_utf8_stdio(skip_in_pytest=True)


class StatusReporter:
    """Status report generator"""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.config = get_config(self.project_root)
        self.state_file = self.project_root / ".wordsmith/state.json"
        self.chapters_dir = self.project_root / "body"

        self.state = None
        self.chapters_data = []
        self._reading_power_cache: Dict[int, Optional[Dict[str, Any]]] = {}

        # v5.1: Use IndexManager to read entities
        self._index_manager = IndexManager(self.config)

    def _extract_stats_field(self, content: str, field_name: str) -> str:
        """
        Extract field value from "chapter stats" block, for example:
        - **Dominant Strand**: quest
        """
        pattern = rf"^\s*-\s*\*\*{re.escape(field_name)}\*\*\s*:\s*(.+?)\s*$"
        for line in content.splitlines():
            m = re.match(pattern, line)
            if m:
                return m.group(1).strip()
        return ""

    def load_state(self) -> bool:
        """Load state.json"""
        if not self.state_file.exists():
            print(f"❌ State file does not exist: {self.state_file}")
            return False

        with open(self.state_file, 'r', encoding='utf-8') as f:
            self.state = json.load(f)

        if isinstance(self.state, dict):
            self.state = normalize_state_runtime_sections(self.state)

        return True

    def _to_positive_int(self, value: Any) -> Optional[int]:
        """Parse input as positive integer; return None on parse failure."""
        return to_positive_int(value)

    def _normalize_foreshadowing_tier(self, raw_tier: Any) -> Tuple[str, float]:
        """Normalize foreshadowing tier and return corresponding weight."""
        tier = normalize_foreshadowing_tier(raw_tier)

        if tier == "core":
            return "core", self.config.foreshadowing_tier_weight_core
        if tier == "decor":
            return "decor", self.config.foreshadowing_tier_weight_decor
        return "sub", self.config.foreshadowing_tier_weight_sub

    def _resolve_chapter_field(self, item: Dict[str, Any], keys: List[str]) -> Optional[int]:
        """Read chapter number by candidate key order."""
        return resolve_chapter_field(item, keys)

    def _collect_foreshadowing_records(self) -> List[Dict[str, Any]]:
        """Collect unresolved foreshadowing and build analysis records based on real fields."""
        if not self.state:
            return []

        current_chapter = self.state.get("progress", {}).get("current_chapter", 0)
        plot_threads = self.state.get("plot_threads", {}) if isinstance(self.state.get("plot_threads"), dict) else {}
        foreshadowing = plot_threads.get("foreshadowing", [])
        if not isinstance(foreshadowing, list):
            return []

        records: List[Dict[str, Any]] = []
        for item in foreshadowing:
            if not isinstance(item, dict):
                continue
            if _is_resolved_foreshadowing_status(item.get("status")):
                continue

            content = str(item.get("content") or "").strip() or "[Unnamed foreshadowing]"
            tier, weight = self._normalize_foreshadowing_tier(item.get("tier"))

            planted_chapter = self._resolve_chapter_field(
                item,
                [
                    "planted_chapter",
                    "added_chapter",
                    "source_chapter",
                    "start_chapter",
                    "chapter",
                ],
            )
            target_chapter = self._resolve_chapter_field(
                item,
                [
                    "target_chapter",
                    "due_chapter",
                    "deadline_chapter",
                    "resolve_by_chapter",
                    "target",
                ],
            )

            elapsed = None
            if planted_chapter is not None:
                elapsed = max(0, current_chapter - planted_chapter)

            remaining = None
            if target_chapter is not None:
                remaining = target_chapter - current_chapter

            if remaining is not None and remaining < 0:
                overtime_status = "🔴 overdue"
            elif elapsed is None:
                overtime_status = "⚪ insufficient_data"
            else:
                overtime_status = self._get_foreshadowing_status(elapsed)

            urgency: Optional[float] = None
            if (
                planted_chapter is not None
                and target_chapter is not None
                and target_chapter > planted_chapter
                and elapsed is not None
            ):
                urgency = round((elapsed / (target_chapter - planted_chapter)) * weight, 2)
            elif (
                planted_chapter is not None
                and target_chapter is not None
                and target_chapter <= planted_chapter
                and elapsed is not None
            ):
                urgency = round(weight * 2.0, 2)

            if remaining is not None and remaining < 0:
                urgency_status = "🔴 overdue"
            elif urgency is None:
                urgency_status = "⚪ insufficient_data"
            else:
                urgency_status = self._get_urgency_status(urgency, remaining if remaining is not None else 0)

            records.append(
                {
                    "content": content,
                    "tier": tier,
                    "weight": weight,
                    "planted_chapter": planted_chapter,
                    "target_chapter": target_chapter,
                    "elapsed": elapsed,
                    "remaining": remaining,
                    "status": overtime_status,
                    "urgency": urgency,
                    "urgency_status": urgency_status,
                }
            )

        return records

    def _get_chapter_meta(self, chapter: int) -> Dict[str, Any]:
        """Read chapter_meta for specified chapter (supports both 0001/1 key formats)."""
        if not self.state:
            return {}
        return get_chapter_meta_entry(self.state, chapter)

    def _parse_pattern_count(self, raw_value: Any) -> Optional[int]:
        """Parse cool point pattern count, return None on parse failure."""
        if raw_value is None:
            return None

        if isinstance(raw_value, list):
            patterns = [str(x).strip() for x in raw_value if str(x).strip()]
            return len(set(patterns))

        if isinstance(raw_value, str):
            text = raw_value.strip()
            if not text:
                return None
            parts = [p.strip() for p in re.split(r"[、,，/|+；;]+", text) if p.strip()]
            if parts:
                return len(set(parts))
            return 1

        return None

    def _get_chapter_reading_power_cached(self, chapter: int) -> Optional[Dict[str, Any]]:
        """Read and cache chapter_reading_power."""
        if chapter in self._reading_power_cache:
            return self._reading_power_cache[chapter]

        try:
            record = self._index_manager.get_chapter_reading_power(chapter)
        except Exception:
            record = None

        self._reading_power_cache[chapter] = record
        return record

    def _get_chapter_cool_points(self, chapter: int, chapter_data: Dict[str, Any]) -> Tuple[Optional[int], str]:
        """Get cool point count for single chapter (real metadata priority)."""
        reading_power = self._get_chapter_reading_power_cached(chapter)
        if isinstance(reading_power, dict):
            count = self._parse_pattern_count(reading_power.get("coolpoint_patterns"))
            if count is not None:
                return count, "chapter_reading_power"

        chapter_meta = self._get_chapter_meta(chapter)
        for key in ("coolpoint_patterns", "coolpoint_pattern", "cool_point_patterns", "cool_point_pattern", "patterns", "pattern"):
            count = self._parse_pattern_count(chapter_meta.get(key))
            if count is not None:
                return count, "chapter_meta"

        count = self._parse_pattern_count(chapter_data.get("cool_point"))
        if count is not None:
            return count, "chapter_stats"

        return None, "none"

    def scan_chapters(self):
        """Scan all chapter files"""
        if not self.chapters_dir.exists():
            print(f"⚠️  Chapters directory does not exist: {self.chapters_dir}")
            return

        # Support two directory structures:
        # 1) body/Chapter-0001.md
        # 2) body/Volume-1/Chapter-001-Title.md
        chapter_files = sorted(self.chapters_dir.rglob("Chapter-*.md"))

        # v5.1: Get known character names from SQLite
        known_character_names: List[str] = []
        protagonist_name = ""
        if self.state:
            protagonist_name = self.state.get("protagonist_state", {}).get("name", "") or ""

        # Get canonical_name for all characters from SQLite
        try:
            characters_from_db = self._index_manager.get_entities_by_type("character")
            known_character_names = [
                c.get("canonical_name", c.get("id", ""))
                for c in characters_from_db
                if c.get("canonical_name")
            ]
        except Exception:
            known_character_names = []

        for chapter_file in chapter_files:
            chapter_num = extract_chapter_num_from_filename(chapter_file.name)
            if not chapter_num:
                continue

            # Read chapter content
            with open(chapter_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Count words (remove Markdown markers)
            text = re.sub(r'```[\s\S]*?```', '', content)  # Remove code blocks
            text = re.sub(r'#+ .+', '', text)  # Remove headers
            text = re.sub(r'---', '', text)  # Remove horizontal rules
            word_count = len(text.strip())

            # Dominant Strand / cool point type (prefer parsing from "chapter stats")
            dominant_strand = (self._extract_stats_field(content, "dominant_strand") or "").lower()
            cool_point_type = self._extract_stats_field(content, "cool_point")

            # v5.1: Character extraction from SQLite chapters table
            characters: List[str] = []
            try:
                chapter_info = self._index_manager.get_chapter(chapter_num)
                if chapter_info and chapter_info.get("characters"):
                    stored = chapter_info["characters"]
                    if isinstance(stored, str):
                        stored = json.loads(stored)
                    if isinstance(stored, list):
                        for entity_id in stored:
                            entity_id = str(entity_id).strip()
                            if not entity_id:
                                continue
                            # Try to get canonical_name
                            entity = self._index_manager.get_entity(entity_id)
                            name = entity.get("canonical_name", entity_id) if entity else entity_id
                            characters.append(name)
            except Exception:
                characters = []

            if not characters and (protagonist_name or known_character_names):
                # Limit candidate size to avoid slowdown with large character libraries
                candidates = []
                if protagonist_name:
                    candidates.append(protagonist_name)
                candidates.extend(known_character_names[:self.config.character_candidates_limit])

                seen = set()
                for name in candidates:
                    if not name or name in seen:
                        continue
                    if name in content:
                        characters.append(name)
                        seen.add(name)

            self.chapters_data.append({
                "chapter": chapter_num,
                "file": chapter_file,
                "word_count": word_count,
                "characters": characters,
                "dominant": dominant_strand,
                "cool_point": cool_point_type,
            })

    def analyze_characters(self) -> Dict:
        """Analyze character activity (v5.1 introduced, v5.4 continues)"""
        if not self.state:
            return {}

        current_chapter = self.state.get("progress", {}).get("current_chapter", 0)

        # v5.1: Get all characters from SQLite
        try:
            characters_list = self._index_manager.get_entities_by_type("character")
        except Exception:
            characters_list = []

        # Track last appearance chapter for each character
        character_activity = {}

        for char in characters_list:
            char_name = char.get("canonical_name", char.get("id", ""))
            if not char_name:
                continue

            # Find last appearance chapter
            last_appearance = char.get("last_appearance", 0) or 0

            # Also check from chapters_data
            for ch_data in self.chapters_data:
                if char_name in ch_data.get("characters", []):
                    last_appearance = max(last_appearance, ch_data["chapter"])

            absence = current_chapter - last_appearance

            character_activity[char_name] = {
                "last_appearance": last_appearance,
                "absence": absence,
                "status": self._get_absence_status(absence)
            }

        return character_activity

    def _get_absence_status(self, absence: int) -> str:
        """Determine dropped character status"""
        if absence == 0:
            return "✅ active"
        elif absence < self.config.character_absence_warning:
            return "🟢 normal"
        elif absence < self.config.character_absence_critical:
            return "🟡 mild_drop"
        else:
            return "🔴 critical_drop"

    def analyze_foreshadowing(self) -> List[Dict]:
        """Analyze foreshadowing depth"""
        records = self._collect_foreshadowing_records()
        return [
            {
                "content": item["content"],
                "planted_chapter": item["planted_chapter"],
                "estimated_chapter": item["planted_chapter"],
                "target_chapter": item["target_chapter"],
                "elapsed": item["elapsed"],
                "status": item["status"],
            }
            for item in records
        ]

    def _get_foreshadowing_status(self, elapsed: int) -> str:
        """Determine foreshadowing timeout status"""
        if elapsed < self.config.foreshadowing_urgency_pending_medium:
            return "🟢 normal"
        elif elapsed < self.config.foreshadowing_urgency_pending_high + 50:
            return "🟡 mild_overtime"
        else:
            return "🔴 critical_overtime"

    def analyze_foreshadowing_urgency(self) -> List[Dict]:
        """
        Analyze foreshadowing urgency (based on three-tier system)

        Three-tier weights:
        - Core: Weight 3.0 - Must resolve, otherwise plot collapses
        - Sub: Weight 2.0 - Should resolve, otherwise author appears forgetful
        - Decor: Weight 1.0 - Optional resolution, only adds realism

        Urgency calculation formula:
        urgency = (elapsed chapters / target resolution chapters) × tier weight
        """
        records = self._collect_foreshadowing_records()
        urgency_list = [
            {
                "content": item["content"],
                "tier": item["tier"],
                "weight": item["weight"],
                "planted_chapter": item["planted_chapter"],
                "target_chapter": item["target_chapter"],
                "elapsed": item["elapsed"],
                "remaining": item["remaining"],
                "urgency": item["urgency"],
                "status": item["urgency_status"],
            }
            for item in records
        ]

        # Sort by "calculability" first, then by urgency descending
        return sorted(
            urgency_list,
            key=lambda x: (x["urgency"] is None, -(x["urgency"] if x["urgency"] is not None else -1)),
        )

    def _get_urgency_status(self, urgency: float, remaining: int) -> str:
        """Determine urgency status"""
        if remaining < 0:
            return "🔴 overdue"
        elif urgency >= self.config.foreshadowing_tier_weight_sub:
            return "🔴 critical"
        elif urgency >= 1.0:
            return "🟡 warning"
        else:
            return "🟢 normal"

    def analyze_strand_weave(self) -> Dict:
        """
        Analyze Strand Weave rhythm distribution

        Three-strand definition:
        - Quest (Main): Combat, missions, level-ups - target 55-65%
        - Fire (Romance): Romance, interpersonal interaction - target 20-30%
        - Constellation (Worldbuilding): World expansion, faction background - target 10-20%

        Check rules:
        - Quest strand consecutive chapters should not exceed 5
        - Fire strand gap should not exceed 10 chapters
        - Constellation strand gap should not exceed 15 chapters
        """
        if not self.state:
            return {}

        strand_tracker = self.state.get("strand_tracker", {})
        history = strand_tracker.get("history", [])

        if not history:
            return {
                "has_data": False,
                "message": "No Strand Weave data yet"
            }

        # Count strand ratios
        quest_count = 0
        fire_count = 0
        constellation_count = 0
        total = len(history)

        for entry in history:
            strand = (entry.get("strand") or entry.get("dominant") or "").lower()
            if strand in ["quest", "combat", "mission"]:
                quest_count += 1
            elif strand in ["fire"]:
                fire_count += 1
            elif strand in ["constellation"]:
                constellation_count += 1

        # Calculate ratios
        quest_ratio = (quest_count / total * 100) if total > 0 else 0
        fire_ratio = (fire_count / total * 100) if total > 0 else 0
        constellation_ratio = (constellation_count / total * 100) if total > 0 else 0

        # Check violations
        violations = []

        # Check Quest consecutive exceeds 5 chapters
        quest_streak = 0
        max_quest_streak = 0
        for entry in history:
            strand = (entry.get("strand") or entry.get("dominant") or "").lower()
            if strand in ["quest", "combat", "mission"]:
                quest_streak += 1
                max_quest_streak = max(max_quest_streak, quest_streak)
            else:
                quest_streak = 0

        if max_quest_streak > self.config.strand_quest_max_consecutive:
            violations.append(f"Quest strand consecutive {max_quest_streak} chapters (exceeds limit of {self.config.strand_quest_max_consecutive})")

        # Check Fire gap exceeds 10 chapters
        fire_gap = 0
        max_fire_gap = 0
        for entry in history:
            strand = (entry.get("strand") or entry.get("dominant") or "").lower()
            if strand in ["fire"]:
                max_fire_gap = max(max_fire_gap, fire_gap)
                fire_gap = 0
            else:
                fire_gap += 1
        max_fire_gap = max(max_fire_gap, fire_gap)

        if max_fire_gap > self.config.strand_fire_max_gap:
            violations.append(f"Fire strand gap {max_fire_gap} chapters (exceeds limit of {self.config.strand_fire_max_gap})")

        # Check Constellation gap exceeds 15 chapters
        const_gap = 0
        max_const_gap = 0
        for entry in history:
            strand = (entry.get("strand") or entry.get("dominant") or "").lower()
            if strand in ["constellation"]:
                max_const_gap = max(max_const_gap, const_gap)
                const_gap = 0
            else:
                const_gap += 1
        max_const_gap = max(max_const_gap, const_gap)

        if max_const_gap > self.config.strand_constellation_max_gap:
            violations.append(f"Constellation strand gap {max_const_gap} chapters (exceeds limit of {self.config.strand_constellation_max_gap})")

        # Check if ratios are within reasonable range
        cfg = self.config
        if quest_ratio < cfg.strand_quest_ratio_min:
            violations.append(f"Quest ratio {quest_ratio:.1f}% is low (target {cfg.strand_quest_ratio_min}-{cfg.strand_quest_ratio_max}%)")
        elif quest_ratio > cfg.strand_quest_ratio_max:
            violations.append(f"Quest ratio {quest_ratio:.1f}% is high (target {cfg.strand_quest_ratio_min}-{cfg.strand_quest_ratio_max}%)")

        if fire_ratio < cfg.strand_fire_ratio_min:
            violations.append(f"Fire ratio {fire_ratio:.1f}% is low (target {cfg.strand_fire_ratio_min}-{cfg.strand_fire_ratio_max}%)")
        elif fire_ratio > cfg.strand_fire_ratio_max:
            violations.append(f"Fire ratio {fire_ratio:.1f}% is high (target {cfg.strand_fire_ratio_min}-{cfg.strand_fire_ratio_max}%)")

        if constellation_ratio < cfg.strand_constellation_ratio_min:
            violations.append(f"Constellation ratio {constellation_ratio:.1f}% is low (target {cfg.strand_constellation_ratio_min}-{cfg.strand_constellation_ratio_max}%)")
        elif constellation_ratio > cfg.strand_constellation_ratio_max:
            violations.append(f"Constellation ratio {constellation_ratio:.1f}% is high (target {cfg.strand_constellation_ratio_min}-{cfg.strand_constellation_ratio_max}%)")

        return {
            "has_data": True,
            "total_chapters": total,
            "quest": {"count": quest_count, "ratio": quest_ratio},
            "fire": {"count": fire_count, "ratio": fire_ratio},
            "constellation": {"count": constellation_count, "ratio": constellation_ratio},
            "violations": violations,
            "max_quest_streak": max_quest_streak,
            "max_fire_gap": max_fire_gap,
            "max_const_gap": max_const_gap,
            "health": "✅ Healthy" if not violations else f"⚠️ {len(violations)} issues"
        }

    def analyze_pacing(self) -> List[Dict]:
        """Analyze cool point rhythm distribution (N chapters per segment)"""
        segment_size = self.config.pacing_segment_size
        segments = []

        for i in range(0, len(self.chapters_data), segment_size):
            segment_chapters = self.chapters_data[i:i+segment_size]

            if not segment_chapters:
                continue

            start_ch = segment_chapters[0]["chapter"]
            end_ch = segment_chapters[-1]["chapter"]
            total_words = sum(ch["word_count"] for ch in segment_chapters)

            cool_points = 0
            chapters_with_data = 0
            source_counter: Dict[str, int] = {}

            for chapter_data in segment_chapters:
                chapter = chapter_data["chapter"]
                count, source = self._get_chapter_cool_points(chapter, chapter_data)
                source_counter[source] = source_counter.get(source, 0) + 1
                if count is None:
                    continue
                chapters_with_data += 1
                cool_points += count

            words_per_point = None
            if cool_points > 0:
                words_per_point = total_words / cool_points

            rating = self._get_pacing_rating(words_per_point)
            missing_chapters = len(segment_chapters) - chapters_with_data
            dominant_source = "none"
            if source_counter:
                dominant_source = max(source_counter.items(), key=lambda x: x[1])[0]

            segments.append({
                "start": start_ch,
                "end": end_ch,
                "total_words": total_words,
                "cool_points": cool_points,
                "words_per_point": words_per_point,
                "rating": rating,
                "missing_chapters": missing_chapters,
                "data_coverage": (chapters_with_data / len(segment_chapters)) if segment_chapters else 0.0,
                "dominant_source": dominant_source,
            })

        return segments

    def _get_pacing_rating(self, words_per_point: Optional[float]) -> str:
        """Determine rhythm rating"""
        if words_per_point is None:
            return "Insufficient data"
        if words_per_point < self.config.pacing_words_per_point_excellent:
            return "Excellent"
        elif words_per_point < self.config.pacing_words_per_point_good:
            return "Good"
        elif words_per_point < self.config.pacing_words_per_point_acceptable:
            return "Acceptable"
        else:
            return "Low⚠️"

    def _resolve_protagonist_entity_id(self) -> Optional[str]:
        """Resolve protagonist entity ID (prefer index.db)."""
        protagonist = self._index_manager.get_protagonist()
        if protagonist and protagonist.get("id"):
            return str(protagonist["id"])

        if not self.state:
            return None
        name = str(self.state.get("protagonist_state", {}).get("name", "") or "").strip()
        if not name:
            return None
        hits = self._index_manager.get_entities_by_alias(name)
        if hits:
            return str(hits[0].get("id") or "")
        return None

    def _generate_relationship_graph_from_index(self) -> str:
        """Generate relationship graph based on index.db."""
        protagonist_id = self._resolve_protagonist_entity_id()
        if not protagonist_id:
            return ""

        current_chapter = 0
        if self.state:
            current_chapter = int(self.state.get("progress", {}).get("current_chapter", 0) or 0)
        chapter = current_chapter if current_chapter > 0 else None

        graph = self._index_manager.build_relationship_subgraph(
            center_entity=protagonist_id,
            depth=2,
            chapter=chapter,
            top_edges=40,
        )
        if not graph.get("nodes"):
            return ""
        return self._index_manager.render_relationship_subgraph_mermaid(graph)

    def generate_relationship_graph(self) -> str:
        """Generate interpersonal relationship Mermaid diagram"""
        if not self.state:
            return ""

        # v5.5: Prefer using index.db relationship graph (can be disabled via config)
        if bool(getattr(self.config, "relationship_graph_from_index_enabled", True)):
            try:
                graph = self._generate_relationship_graph_from_index()
                if graph:
                    return graph
            except Exception:
                # Fallback to old logic to avoid interrupting report generation
                pass

        # Compatibility with old state.json relationships structure
        relationships = self.state.get("relationships", {})
        protagonist_name = self.state.get("protagonist_state", {}).get("name", "Protagonist")

        lines = ["```mermaid", "graph LR"]

        # Support two formats:
        # Format1 (new): {"allies": [...], "enemies": [...]}
        # Format2 (old): {"character_name": {"affection": X, "hatred": Y}}

        allies = relationships.get("allies", [])
        enemies = relationships.get("enemies", [])

        if allies or enemies:
            # New format
            for ally in allies:
                if isinstance(ally, dict):
                    name = ally.get("name", "Unknown")
                    relation = ally.get("relation", "Friendly")
                    lines.append(f"    {protagonist_name} -->|{relation}| {name}")

            for enemy in enemies:
                if isinstance(enemy, dict):
                    name = enemy.get("name", "Unknown")
                    relation = enemy.get("relation", "Hostile")
                    lines.append(f"    {protagonist_name} -.->|{relation}| {name}")
        else:
            # Old format compatibility
            for char_name, rel_data in relationships.items():
                if isinstance(rel_data, dict):
                    affection = rel_data.get("affection", 0)
                    hatred = rel_data.get("hatred", 0)

                    if affection > 0:
                        lines.append(f"    {protagonist_name} -->|Affection{affection}| {char_name}")

                    if hatred > 0:
                        lines.append(f"    {protagonist_name} -.->|Hatred{hatred}| {char_name}")

        lines.append("```")

        return "\n".join(lines)

    def generate_report(self, focus: str = "all") -> str:
        """Generate health report (Markdown format)"""

        report_lines = [
            "# Full Book Health Report",
            "",
            f"> **Generated at**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "---",
            ""
        ]

        # Basic data
        if focus in ["all", "basic"]:
            report_lines.extend(self._generate_basic_stats())

        # Character activity
        if focus in ["all", "characters"]:
            report_lines.extend(self._generate_character_section())

        # Foreshadowing depth
        if focus in ["all", "foreshadowing"]:
            report_lines.extend(self._generate_foreshadowing_section())

        # Foreshadowing urgency (new)
        if focus in ["all", "foreshadowing", "urgency"]:
            report_lines.extend(self._generate_urgency_section())

        # Cool point rhythm
        if focus in ["all", "pacing"]:
            report_lines.extend(self._generate_pacing_section())

        # Strand Weave rhythm (new)
        if focus in ["all", "strand", "pacing"]:
            report_lines.extend(self._generate_strand_section())

        # Interpersonal relationships
        if focus in ["all", "relationships"]:
            report_lines.extend(self._generate_relationship_section())

        return "\n".join(report_lines)

    def _generate_basic_stats(self) -> List[str]:
        """Generate basic statistics"""
        if not self.state:
            return []

        progress = self.state.get("progress", {})
        current_chapter = progress.get("current_chapter", 0)
        total_words = progress.get("total_words", 0)
        target_words = self.state.get("project_info", {}).get("target_words", 2000000)

        avg_words = total_words / current_chapter if current_chapter > 0 else 0
        completion = (total_words / target_words * 100) if target_words > 0 else 0

        return [
            "## 📊 Basic Data",
            "",
            f"- **Total chapters**: {current_chapter} chapters",
            f"- **Total words**: {total_words:,} words",
            f"- **Average words per chapter**: {avg_words:,.0f} words",
            f"- **Progress**: {completion:.1f}% (target {target_words:,} words)",
            "",
            "---",
            ""
        ]

    def _generate_character_section(self) -> List[str]:
        """Generate character analysis section"""
        activity = self.analyze_characters()

        if not activity:
            return []

        # Filter dropped characters
        dropped = {name: data for name, data in activity.items()
                  if "dropped" in data["status"]}

        lines = [
            f"## ⚠️ Character Drops ({len(dropped)} characters)",
            ""
        ]

        if dropped:
            lines.extend([
                "| Character | Last Appearance | Absent Chapters | Status |",
                "|------|---------|---------|------|"
            ])

            for char_name, data in sorted(dropped.items(),
                                         key=lambda x: x[1]["absence"],
                                         reverse=True):
                lines.append(
                    f"| {char_name} | Chapter {data['last_appearance']} | "
                    f"{data['absence']} chapters | {data['status']} |"
                )
        else:
            lines.append("✅ All characters are active")

        lines.extend(["", "---", ""])

        return lines

    def _generate_foreshadowing_section(self) -> List[str]:
        """Generate foreshadowing analysis section"""
        overdue = self.analyze_foreshadowing()

        # Filter overdue foreshadowing
        overdue_items = [
            item for item in overdue if "overtime" in item["status"] or "overdue" in item["status"]
        ]
        unknown_items = [item for item in overdue if item["status"] == "⚪ insufficient_data"]

        lines = [
            f"## ⚠️ Foreshadowing Timeout ({len(overdue_items)} items)",
            ""
        ]

        if overdue_items:
            lines.extend([
                "| Foreshadowing Content | Planted Chapter | Chapters Elapsed | Status |",
                "|---------|---------|---------|------|"
            ])

            for item in sorted(overdue_items, key=lambda x: (x["elapsed"] if x["elapsed"] is not None else -1), reverse=True):
                planted = item["planted_chapter"] if item["planted_chapter"] is not None else "Unknown"
                elapsed = item["elapsed"] if item["elapsed"] is not None else "Unknown"
                lines.append(
                    f"| {item['content'][:30]}... | Chapter {planted} | "
                    f"{elapsed} chapters | {item['status']} |"
                )
        else:
            lines.append("✅ All foreshadowing progress is normal")

        if unknown_items:
            lines.append("")
            lines.append(f"⚪ Another {len(unknown_items)} foreshadowing items lack chapter information, cannot determine if timed out")

        lines.extend(["", "---", ""])

        return lines

    def _generate_urgency_section(self) -> List[str]:
        """Generate foreshadowing urgency section (based on three-tier system)"""
        urgency_list = self.analyze_foreshadowing_urgency()

        # Filter urgent foreshadowing
        urgent_items = [
            item
            for item in urgency_list
            if (item["urgency"] is not None and item["urgency"] >= 1.0) or item["status"] == "🔴 overdue"
        ]

        lines = [
            f"## 🚨 Foreshadowing Urgency Ranking ({len(urgent_items)} items need attention)",
            "",
            "> Based on three-tier system: Core(×3) / Sub(×2) / Decor(×1)",
            "> Urgency = (elapsed chapters / (target chapter - planted chapter)) × tier weight",
            ""
        ]

        unknown_items = [item for item in urgency_list if item["urgency"] is None]
        if unknown_items:
            lines.append(f"> {len(unknown_items)} foreshadowing items lack planted/target chapters, urgency marked as N/A")
            lines.append("")

        if urgency_list:
            lines.extend([
                "| Foreshadowing Content | Tier | Planted | Target | Urgency | Status |",
                "|---------|------|------|------|--------|------|"
            ])

            for item in urgency_list[:10]:  # Only show top 10
                planted = f"Chapter {item['planted_chapter']}" if item["planted_chapter"] is not None else "Unknown"
                target = f"Chapter {item['target_chapter']}" if item["target_chapter"] is not None else "Unknown"
                urgency_text = f"{item['urgency']:.2f}" if item["urgency"] is not None else "N/A"
                lines.append(
                    f"| {item['content'][:20]}... | {item['tier']} | "
                    f"{planted} | {target} | "
                    f"{urgency_text} | {item['status']} |"
                )
        else:
            lines.append("✅ No foreshadowing data yet")

        lines.extend(["", "---", ""])

        return lines

    def _generate_strand_section(self) -> List[str]:
        """Generate Strand Weave rhythm section"""
        strand_data = self.analyze_strand_weave()

        lines = [
            "## 🎭 Strand Weave Rhythm Analysis",
            ""
        ]

        if not strand_data.get("has_data"):
            lines.append(f"⚠️ {strand_data.get('message', 'No data yet')}")
            lines.extend(["", "---", ""])
            return lines

        # Ratio statistics
        cfg = self.config
        lines.extend([
            "### Three-Strand Ratio",
            "",
            "| Strand | Chapters | Ratio | Target Range | Status |",
            "|--------|--------|------|----------|------|"
        ])

        q = strand_data["quest"]
        q_status = "✅" if cfg.strand_quest_ratio_min <= q["ratio"] <= cfg.strand_quest_ratio_max else "⚠️"
        lines.append(f"| Quest (Main) | {q['count']} | {q['ratio']:.1f}% | {cfg.strand_quest_ratio_min}-{cfg.strand_quest_ratio_max}% | {q_status} |")

        f = strand_data["fire"]
        f_status = "✅" if cfg.strand_fire_ratio_min <= f["ratio"] <= cfg.strand_fire_ratio_max else "⚠️"
        lines.append(f"| Fire (Romance) | {f['count']} | {f['ratio']:.1f}% | {cfg.strand_fire_ratio_min}-{cfg.strand_fire_ratio_max}% | {f_status} |")

        c = strand_data["constellation"]
        c_status = "✅" if cfg.strand_constellation_ratio_min <= c["ratio"] <= cfg.strand_constellation_ratio_max else "⚠️"
        lines.append(f"| Constellation (Worldbuilding) | {c['count']} | {c['ratio']:.1f}% | {cfg.strand_constellation_ratio_min}-{cfg.strand_constellation_ratio_max}% | {c_status} |")

        lines.append("")

        # Consecutivity check
        lines.extend([
            "### Consecutivity Check",
            "",
            f"- Quest max consecutive: {strand_data['max_quest_streak']} chapters (limit ≤5)",
            f"- Fire max gap: {strand_data['max_fire_gap']} chapters (limit ≤10)",
            f"- Constellation max gap: {strand_data['max_const_gap']} chapters (limit ≤15)",
            ""
        ])

        # Violation list
        if strand_data["violations"]:
            lines.extend([
                "### ⚠️ Violation List",
                ""
            ])
            for v in strand_data["violations"]:
                lines.append(f"- {v}")
        else:
            lines.append("### ✅ No Violations")

        lines.extend(["", f"**Overall Health**: {strand_data['health']}", "", "---", ""])

        return lines

    def _generate_pacing_section(self) -> List[str]:
        """Generate rhythm analysis section"""
        segments = self.analyze_pacing()

        lines = [
            "## 📈 Cool Point Rhythm Distribution",
            "",
            "```"
        ]

        for seg in segments:
            words_per_point = seg["words_per_point"]
            if words_per_point is None:
                lines.append(
                    f"Chapters {seg['start']}-{seg['end']}   ░ Insufficient data"
                    f"(missing cool point data for {seg['missing_chapters']} chapters)"
                )
                continue

            bar_length = int(12 - (words_per_point / 2000 * 12))
            bar_length = max(1, min(12, bar_length))
            bar = "█" * bar_length

            suffix = ""
            if seg["missing_chapters"] > 0:
                suffix = f", missing cool point data for {seg['missing_chapters']} chapters"

            lines.append(
                f"Chapters {seg['start']}-{seg['end']}   {bar} {seg['rating']}"
                f"({words_per_point:.0f} words/point, recorded {seg['cool_points']} cool points{suffix})"
            )

        lines.extend(["```", "", "---", ""])

        return lines

    def _generate_relationship_section(self) -> List[str]:
        """Generate interpersonal relationship section"""
        graph = self.generate_relationship_graph()

        lines = [
            "## 💑 Interpersonal Relationship Trends",
            "",
            graph,
            "",
            "---",
            ""
        ]

        return lines

def main():
    import argparse

    _enable_windows_utf8_stdio()

    parser = argparse.ArgumentParser(
        description="Visual status report generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate complete health report
  python status_reporter.py --output .wordsmith/health_report.md

  # Analyze character activity only
  python status_reporter.py --focus characters

  # Analyze foreshadowing only
  python status_reporter.py --focus foreshadowing

  # Analyze cool point rhythm only
  python status_reporter.py --focus pacing
        """
    )

    parser.add_argument('--output', default='.wordsmith/health_report.md',
                       help='Output file path')
    parser.add_argument('--focus', choices=['all', 'basic', 'characters',
                                            'foreshadowing', 'urgency', 'pacing',
                                            'strand', 'relationships'],
                       default='all', help='Analysis focus (new: urgency, strand)')
    parser.add_argument('--project-root', default='.', help='Project root directory')

    args = parser.parse_args()

    # Resolve project root (allows passing "workspace root", resolves to actual book project_root)
    try:
        project_root = str(resolve_project_root(args.project_root))
    except FileNotFoundError as exc:
        print(f"❌ Cannot locate project root (need .wordsmith/state.json): {exc}", file=sys.stderr)
        sys.exit(1)

    # Create report generator
    reporter = StatusReporter(project_root)

    # Load state
    if not reporter.load_state():
        sys.exit(1)

    print("📖 Scanning chapter files...")
    reporter.scan_chapters()

    print(f"✅ Scanned {len(reporter.chapters_data)} chapters")

    print("\n📊 Analyzing...")

    # Generate report
    report = reporter.generate_report(args.focus)

    # Save report
    output_file = Path(args.output)
    if args.output == '.wordsmith/health_report.md' and project_root != '.':
        output_file = Path(project_root) / '.wordsmith' / 'health_report.md'
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n✅ Health report generated: {output_file}")

    # Preview report (first 30 lines)
    print("\n" + "="*60)
    print("📄 Report preview:\n")
    print("\n".join(report.split("\n")[:30]))
    print("\n...")
    print("="*60)

if __name__ == "__main__":
    main()
