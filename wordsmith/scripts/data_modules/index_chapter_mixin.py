#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IndexChapterMixin extracted from IndexManager.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict, List, Optional


class IndexChapterMixin:
    def add_chapter(self, meta: ChapterMeta):
        """Add or update chapter metadata"""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO chapters
                (chapter, title, location, word_count, characters, summary)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    meta.chapter,
                    meta.title,
                    meta.location,
                    meta.word_count,
                    json.dumps(meta.characters, ensure_ascii=False),
                    meta.summary,
                ),
            )
            conn.commit()

    def get_chapter(self, chapter: int) -> Optional[Dict]:
        """Get chapter metadata"""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM chapters WHERE chapter = ?", (chapter,))
            row = cursor.fetchone()
            if row:
                return self._row_to_dict(row, parse_json=["characters"])
            return None

    def get_recent_chapters(self, limit: int = None) -> List[Dict]:
        """Get recent chapters"""
        if limit is None:
            limit = self.config.query_recent_chapters_limit
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM chapters
                ORDER BY chapter DESC
                LIMIT ?
            """,
                (limit,),
            )
            return [
                self._row_to_dict(row, parse_json=["characters"])
                for row in cursor.fetchall()
            ]

    # ==================== Scene Operations ====================

    def add_scenes(self, chapter: int, scenes: List[SceneMeta]):
        """Add chapter scenes"""
        with self._get_conn() as conn:
            cursor = conn.cursor()

            # Delete old scenes for this chapter first
            cursor.execute("DELETE FROM scenes WHERE chapter = ?", (chapter,))

            # Insert new scenes
            for scene in scenes:
                cursor.execute(
                    """
                    INSERT INTO scenes
                    (chapter, scene_index, start_line, end_line, location, summary, characters)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        scene.chapter,
                        scene.scene_index,
                        scene.start_line,
                        scene.end_line,
                        scene.location,
                        scene.summary,
                        json.dumps(scene.characters, ensure_ascii=False),
                    ),
                )

            conn.commit()

    def get_scenes(self, chapter: int) -> List[Dict]:
        """Get chapter scenes"""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM scenes
                WHERE chapter = ?
                ORDER BY scene_index
            """,
                (chapter,),
            )
            return [
                self._row_to_dict(row, parse_json=["characters"])
                for row in cursor.fetchall()
            ]

    def search_scenes_by_location(self, location: str, limit: int = None) -> List[Dict]:
        """Search scenes by location"""
        if limit is None:
            limit = self.config.query_scenes_by_location_limit
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM scenes
                WHERE location LIKE ?
                ORDER BY chapter DESC
                LIMIT ?
            """,
                (f"%{location}%", limit),
            )
            return [
                self._row_to_dict(row, parse_json=["characters"])
                for row in cursor.fetchall()
            ]

    # ==================== Appearance Record Operations ====================

    def record_appearance(
        self,
        entity_id: str,
        chapter: int,
        mentions: List[str],
        confidence: float = 1.0,
        skip_if_exists: bool = False,
    ):
        """Record entity appearance

        Args:
            entity_id: Entity ID
            chapter: Chapter number
            mentions: List of mentions
            confidence: Confidence score
            skip_if_exists: If True, skip when record already exists (to avoid overwriting existing mentions)
        """
        with self._get_conn() as conn:
            cursor = conn.cursor()

            if skip_if_exists:
                # Check if already exists first
                cursor.execute(
                    "SELECT 1 FROM appearances WHERE entity_id = ? AND chapter = ?",
                    (entity_id, chapter),
                )
                if cursor.fetchone():
                    return  # Already exists, skip

            cursor.execute(
                """
                INSERT OR REPLACE INTO appearances
                (entity_id, chapter, mentions, confidence)
                VALUES (?, ?, ?, ?)
            """,
                (
                    entity_id,
                    chapter,
                    json.dumps(mentions, ensure_ascii=False),
                    confidence,
                ),
            )
            conn.commit()

    def get_entity_appearances(self, entity_id: str, limit: int = None) -> List[Dict]:
        """Get entity appearance records"""
        if limit is None:
            limit = self.config.query_entity_appearances_limit
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM appearances
                WHERE entity_id = ?
                ORDER BY chapter DESC
                LIMIT ?
            """,
                (entity_id, limit),
            )
            return [
                self._row_to_dict(row, parse_json=["mentions"])
                for row in cursor.fetchall()
            ]

    def get_recent_appearances(self, limit: int = None) -> List[Dict]:
        """Get recently appearing entities"""
        if limit is None:
            limit = self.config.query_recent_appearances_limit
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT entity_id, MAX(chapter) as last_chapter, COUNT(*) as total
                FROM appearances
                GROUP BY entity_id
                ORDER BY last_chapter DESC
                LIMIT ?
            """,
                (limit,),
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_chapter_appearances(self, chapter: int) -> List[Dict]:
        """Get all appearing entities in a chapter"""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM appearances
                WHERE chapter = ?
                ORDER BY confidence DESC
            """,
                (chapter,),
            )
            return [
                self._row_to_dict(row, parse_json=["mentions"])
                for row in cursor.fetchall()
            ]

    # ==================== v5.1 Entity Operations ====================

    def process_chapter_data(
        self,
        chapter: int,
        title: str,
        location: str,
        word_count: int,
        entities: List[Dict],
        scenes: List[Dict],
    ) -> Dict[str, int]:
        """
        Process chapter data, batch write to index

        Returns write statistics
        """
        from .index_manager import ChapterMeta, SceneMeta

        stats = {"chapters": 0, "scenes": 0, "appearances": 0}

        # Extract appearing characters
        characters = [e.get("id") for e in entities if e.get("type") == "character"]

        # Write chapter metadata
        self.add_chapter(
            ChapterMeta(
                chapter=chapter,
                title=title,
                location=location,
                word_count=word_count,
                characters=characters,
                summary="",  # Can be generated later by Data Agent
            )
        )
        stats["chapters"] = 1

        # Write scenes
        scene_metas = []
        for s in scenes:
            scene_metas.append(
                SceneMeta(
                    chapter=chapter,
                    scene_index=s.get("index", 0),
                    start_line=s.get("start_line", 0),
                    end_line=s.get("end_line", 0),
                    location=s.get("location", ""),
                    summary=s.get("summary", ""),
                    characters=s.get("characters", []),
                )
            )
        self.add_scenes(chapter, scene_metas)
        stats["scenes"] = len(scene_metas)

        # Write appearance records
        for entity in entities:
            entity_id = entity.get("id")
            if entity_id and entity_id != "NEW":
                self.record_appearance(
                    entity_id=entity_id,
                    chapter=chapter,
                    mentions=entity.get("mentions", []),
                    confidence=entity.get("confidence", 1.0),
                )
                stats["appearances"] += 1

        return stats

    # ==================== Helper Methods ====================

