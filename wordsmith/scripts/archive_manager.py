#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
state.json Data Archive Management Script

Goal: Prevent state.json from growing indefinitely, ensure stable long-term operation for 2 million word projects

Features:
1. Smart archive long-unused data (characters/foreshadowing/review reports)
2. Auto-trigger condition detection (file size/chapter count)
3. Safe backup and recovery mechanism
4. Archived data can be recovered at any time

Archive strategy:
- Characters: Minor characters not appearing for 50+ chapters → archive/characters.json
- Foreshadowing: status="resolved" and 20+ chapters old → archive/plot_threads.json
- Review reports: Reports older than 50 chapters → archive/reviews.json

Usage:
  # Auto archive check (recommended to call after update_state.py)
  python archive_manager.py --auto-check

  # Force archive (ignore trigger conditions)
  python archive_manager.py --force

  # Restore specific character
  python archive_manager.py --restore-character "Li Xue"

  # View archive statistics
  python archive_manager.py --stats

  # Dry-run mode (only show data to be archived)
  python archive_manager.py --auto-check --dry-run
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

from runtime_compat import enable_windows_utf8_stdio

# ============================================================================
# Security fix: Import security utility functions (P1 MEDIUM)
# ============================================================================
from security_utils import create_secure_directory, atomic_write_json
from project_locator import resolve_project_root

# v5.1: Use IndexManager to read entities
try:
    from data_modules.index_manager import IndexManager
    from data_modules.config import get_config
except ImportError:
    from scripts.data_modules.index_manager import IndexManager
    from scripts.data_modules.config import get_config

# Windows UTF-8 encoding fix
if sys.platform == "win32":
    enable_windows_utf8_stdio()


class ArchiveManager:
    """state.json data archive manager"""

    def __init__(self, project_root=None):
        if project_root is None:
            # Default to current directory
            project_root = Path.cwd()
        else:
            project_root = Path(project_root)

        self.project_root = project_root
        self.state_file = project_root / ".wordsmith" / "state.json"
        self.archive_dir = project_root / ".wordsmith" / "archive"

        # v5.1: IndexManager for reading entities
        self._config = get_config(project_root)
        self._index_manager = IndexManager(self._config)

        # ============================================================================
        # Security fix: Use secure directory creation function (P1 MEDIUM)
        # Original code: self.archive_dir.mkdir(parents=True, exist_ok=True)
        # Vulnerability: No permission settings, using OS default (possibly 755, allowing same group users to read)
        # ============================================================================
        create_secure_directory(str(self.archive_dir))

        # Archive file paths
        self.characters_archive = self.archive_dir / "characters.json"
        self.plot_threads_archive = self.archive_dir / "plot_threads.json"
        self.reviews_archive = self.archive_dir / "reviews.json"

        # Archive rules configuration
        self.config = {
            "character_inactive_threshold": 50,  # Characters not appearing for 50+ chapters are considered inactive
            "plot_resolved_threshold": 20,       # Resolved foreshadowing archived after 20+ chapters
            "review_old_threshold": 50,          # Review reports archived after 50+ chapters
            "file_size_trigger_mb": 1.0,         # state.json exceeds 1.0MB triggers forced archive
            "chapter_trigger": 10                # Check every 10 chapters
        }

    def load_state(self):
        """Load state.json"""
        if not self.state_file.exists():
            print(f"state.json does not exist: {self.state_file}")
            sys.exit(1)

        with open(self.state_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_state(self, state):
        """Save state.json (atomic write)"""
        # Use centralized atomic write (auto backup)
        atomic_write_json(self.state_file, state, use_lock=True, backup=True)
        print(f"state.json atomically updated")

    def load_archive(self, archive_file):
        """Load archive file"""
        if not archive_file.exists():
            return []

        with open(archive_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_archive(self, archive_file, data):
        """Save archive file"""
        with open(archive_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def check_trigger_conditions(self, state):
        """Check if archive should be triggered"""
        current_chapter = state.get("progress", {}).get("current_chapter", 0)

        # Condition 1: File size exceeds threshold
        file_size_mb = self.state_file.stat().st_size / (1024 * 1024)
        size_trigger = file_size_mb >= self.config["file_size_trigger_mb"]

        # Condition 2: Chapter count is multiple of trigger interval
        chapter_trigger = (current_chapter % self.config["chapter_trigger"]) == 0 and current_chapter > 0

        return {
            "should_archive": size_trigger or chapter_trigger,
            "file_size_mb": file_size_mb,
            "current_chapter": current_chapter,
            "size_trigger": size_trigger,
            "chapter_trigger": chapter_trigger
        }

    def identify_inactive_characters(self, state):
        """Identify inactive minor characters (v5.1 introduced, v5.4 continues)"""
        current_chapter = state.get("progress", {}).get("current_chapter", 0)
        threshold = self.config["character_inactive_threshold"]

        # v5.1: Get all character entities from SQLite
        characters = self._index_manager.get_entities_by_type("character")

        inactive = []
        for char in characters:
            # Only archive minor characters (tier="decor" or tier="minor")
            tier = str(char.get("tier", "")).strip()
            if tier == "core":
                continue

            # Check last appearance chapter
            last_appearance = char.get("last_appearance", 0)
            try:
                last_appearance = int(last_appearance)
            except (TypeError, ValueError):
                last_appearance = 0
            if last_appearance <= 0:
                continue

            inactive_chapters = current_chapter - last_appearance

            if inactive_chapters >= threshold:
                char_id = char.get("id", "")
                char_data = {
                    "id": char_id,
                    "name": char.get("canonical_name", char_id),
                    "tier": tier,
                    "last_appearance_chapter": last_appearance
                }
                char_data.update(char)
                inactive.append({
                    "character": char_data,
                    "inactive_chapters": inactive_chapters,
                    "last_appearance": last_appearance
                })

        return inactive

    def identify_resolved_plot_threads(self, state):
        """Identify archivable resolved foreshadowing"""
        current_chapter = state.get("progress", {}).get("current_chapter", 0)
        plot_threads = state.get("plot_threads", {}) or {}
        foreshadowing = plot_threads.get("foreshadowing", []) or []
        resolved_legacy = plot_threads.get("resolved", []) or []
        threshold = self.config["plot_resolved_threshold"]

        archivable = []
        # New format: plot_threads.foreshadowing (use status to mark if resolved)
        if isinstance(foreshadowing, list):
            for item in foreshadowing:
                if not isinstance(item, dict):
                    continue
                status = str(item.get("status", "")).strip()
                if status not in ["recovered", "resolved"]:
                    continue
                try:
                    resolved_chapter = int(item.get("resolved_chapter", 0))
                except (TypeError, ValueError):
                    continue
                chapters_since_resolved = current_chapter - resolved_chapter
                if chapters_since_resolved >= threshold:
                    archivable.append({
                        "thread": item,
                        "chapters_since_resolved": chapters_since_resolved,
                        "resolved_chapter": resolved_chapter
                    })

        # Legacy format compatibility: plot_threads.resolved (directly stored resolved list)
        if isinstance(resolved_legacy, list):
            for item in resolved_legacy:
                if not isinstance(item, dict):
                    continue
                try:
                    resolved_chapter = int(item.get("resolved_chapter", 0))
                except (TypeError, ValueError):
                    continue
                chapters_since_resolved = current_chapter - resolved_chapter
                if chapters_since_resolved >= threshold:
                    archivable.append({
                        "thread": item,
                        "chapters_since_resolved": chapters_since_resolved,
                        "resolved_chapter": resolved_chapter
                    })

        return archivable

    def identify_old_reviews(self, state):
        """Identify archivable old review reports"""
        current_chapter = state.get("progress", {}).get("current_chapter", 0)
        reviews = state.get("review_checkpoints", [])
        threshold = self.config["review_old_threshold"]

        def _parse_end_chapter(review: dict) -> int:
            # New format: {"chapters":"5-6","report":"...","reviewed_at":"..."}
            chapters = review.get("chapters")
            if isinstance(chapters, str):
                parts = [p.strip() for p in chapters.replace("—", "-").split("-") if p.strip()]
                if parts:
                    try:
                        return int(parts[-1])
                    except ValueError:
                        pass

            # Old format: {"chapter_range":[5,6], "date":"..."}
            cr = review.get("chapter_range")
            if isinstance(cr, (list, tuple)) and len(cr) >= 2:
                try:
                    return int(cr[1])
                except (TypeError, ValueError):
                    pass

            # Fallback: extract from report filename "Ch5-6" or "005-006"
            report = review.get("report")
            if isinstance(report, str):
                import re
                m = re.search(r"Ch(\d+)[-–—](\d+)", report)
                if m:
                    try:
                        return int(m.group(2))
                    except ValueError:
                        pass
                m = re.search(r"(\d+)[-–—](\d+)", report)
                if m:
                    try:
                        return int(m.group(2))
                    except ValueError:
                        pass

            return 0

        old_reviews = []
        for review in reviews:
            review_chapter = _parse_end_chapter(review)
            chapters_since_review = current_chapter - review_chapter

            if chapters_since_review >= threshold:
                old_reviews.append({
                    "review": review,
                    "chapters_since_review": chapters_since_review,
                    "review_chapter": review_chapter
                })

        return old_reviews

    def archive_characters(self, inactive_list, dry_run=False):
        """Archive inactive characters (v5.1 introduced: use IndexManager to update status)"""
        if not inactive_list:
            return 0

        # Load existing archive
        archived = self.load_archive(self.characters_archive)

        # Add timestamp
        timestamp = datetime.now().isoformat()
        for item in inactive_list:
            item["character"]["archived_at"] = timestamp
            archived.append(item["character"])

            # v5.1 introduced: Update entity status via IndexManager
            if not dry_run:
                try:
                    entity_id = item["character"].get("id")
                    if entity_id:
                        # Add archived mark to entity's current_json
                        self._index_manager.update_entity_field(
                            entity_id, "status", "archived"
                        )
                except Exception as e:
                    print(f"Entity status update failed (does not affect archiving): {e}")

        if not dry_run:
            self.save_archive(self.characters_archive, archived)

        return len(inactive_list)

    def archive_plot_threads(self, resolved_list, dry_run=False):
        """Archive resolved foreshadowing"""
        if not resolved_list:
            return 0

        # Load existing archive
        archived = self.load_archive(self.plot_threads_archive)

        # Add timestamp
        timestamp = datetime.now().isoformat()
        for item in resolved_list:
            item["thread"]["archived_at"] = timestamp
            archived.append(item["thread"])

        if not dry_run:
            self.save_archive(self.plot_threads_archive, archived)

        return len(resolved_list)

    def archive_reviews(self, old_reviews_list, dry_run=False):
        """Archive old review reports"""
        if not old_reviews_list:
            return 0

        # Load existing archive
        archived = self.load_archive(self.reviews_archive)

        # Add timestamp
        timestamp = datetime.now().isoformat()
        for item in old_reviews_list:
            item["review"]["archived_at"] = timestamp
            archived.append(item["review"])

        if not dry_run:
            self.save_archive(self.reviews_archive, archived)

        return len(old_reviews_list)

    def remove_from_state(self, state, inactive_chars, resolved_threads, old_reviews):
        """Remove archived data from state.json/SQLite (v5.1 introduced, v5.4 continues)"""
        # v5.1 introduced: Character data is in SQLite, archive_characters already handles status update
        # Here only need to handle foreshadowing and review reports in state.json

        # Remove archived foreshadowing
        if resolved_threads:
            thread_ids = {
                (item.get("thread", {}) or {}).get("content") or (item.get("thread", {}) or {}).get("description")
                for item in resolved_threads
            }
            thread_ids = {t for t in thread_ids if isinstance(t, str) and t.strip()}

            plot_threads = state.get("plot_threads", {}) or {}
            if isinstance(plot_threads.get("foreshadowing"), list):
                plot_threads["foreshadowing"] = [
                    t for t in plot_threads["foreshadowing"]
                    if not isinstance(t, dict) or (t.get("content") or t.get("description")) not in thread_ids
                ]
            if isinstance(plot_threads.get("resolved"), list):
                plot_threads["resolved"] = [
                    t for t in plot_threads["resolved"]
                    if not isinstance(t, dict) or (t.get("content") or t.get("description")) not in thread_ids
                ]
            state["plot_threads"] = plot_threads

        # Remove old review reports
        if old_reviews:
            review_keys = set()
            for item in old_reviews:
                review = item.get("review", {}) or {}
                key = review.get("report") or review.get("reviewed_at") or review.get("date")
                if isinstance(key, str) and key.strip():
                    review_keys.add(key)

            state["review_checkpoints"] = [
                review for review in state.get("review_checkpoints", [])
                if (review.get("report") or review.get("reviewed_at") or review.get("date")) not in review_keys
            ]

        return state

    def run_auto_check(self, force=False, dry_run=False):
        """Auto archive check"""
        state = self.load_state()

        # Check trigger conditions
        trigger = self.check_trigger_conditions(state)

        if not force and not trigger["should_archive"]:
            print("No archiving needed (trigger conditions not met)")
            print(f"   File size: {trigger['file_size_mb']:.2f} MB (threshold: {self.config['file_size_trigger_mb']} MB)")
            print(f"   Current chapter: {trigger['current_chapter']} (triggers every {self.config['chapter_trigger']} chapters)")
            return

        print("Starting archive check...")
        print(f"   File size: {trigger['file_size_mb']:.2f} MB")
        print(f"   Current chapter: {trigger['current_chapter']}")

        # Identify archivable data
        inactive_chars = self.identify_inactive_characters(state)
        resolved_threads = self.identify_resolved_plot_threads(state)
        old_reviews = self.identify_old_reviews(state)

        # Output statistics
        print(f"\nArchive statistics:")
        print(f"   Inactive characters: {len(inactive_chars)}")
        print(f"   Resolved foreshadowing: {len(resolved_threads)}")
        print(f"   Old review reports: {len(old_reviews)}")

        if not (inactive_chars or resolved_threads or old_reviews):
            print("\nNo archiving needed (no qualifying data)")
            return

        # Dry-run mode
        if dry_run:
            print("\n[Dry-run] Data to be archived:")
            if inactive_chars:
                print("\n   Inactive characters:")
                for item in inactive_chars[:5]:  # Only show first 5
                    print(f"   - {item['character']['name']} (no appearance for {item['inactive_chapters']} chapters)")
            if resolved_threads:
                print("\n   Resolved foreshadowing:")
                for item in resolved_threads[:5]:
                    desc = item["thread"].get("content") or item["thread"].get("description") or ""
                    print(f"   - {str(desc)[:30]}... (resolved {item['chapters_since_resolved']} chapters ago)")
            if old_reviews:
                print("\n   Old review reports:")
                for item in old_reviews[:5]:
                    print(f"   - Ch{item['review_chapter']} ({item['chapters_since_review']} chapters ago)")
            return

        # Execute archiving
        chars_archived = self.archive_characters(inactive_chars, dry_run=dry_run)
        threads_archived = self.archive_plot_threads(resolved_threads, dry_run=dry_run)
        reviews_archived = self.archive_reviews(old_reviews, dry_run=dry_run)

        # Remove from state.json
        state = self.remove_from_state(state, inactive_chars, resolved_threads, old_reviews)
        self.save_state(state)

        # Final statistics
        print(f"\nArchive complete:")
        print(f"   Character archive: {chars_archived} -> {self.characters_archive.name}")
        print(f"   Foreshadowing archive: {threads_archived} -> {self.plot_threads_archive.name}")
        print(f"   Report archive: {reviews_archived} -> {self.reviews_archive.name}")

        # Show post-archive file size
        new_size_mb = self.state_file.stat().st_size / (1024 * 1024)
        saved_mb = trigger["file_size_mb"] - new_size_mb
        print(f"\nFile size: {trigger['file_size_mb']:.2f} MB -> {new_size_mb:.2f} MB (saved {saved_mb:.2f} MB)")

    def restore_character(self, name):
        """Restore archived character (v5.1 introduced: use IndexManager to restore status)"""
        archived = self.load_archive(self.characters_archive)

        # Find character
        char_to_restore = None
        for char in archived:
            if char["name"] == name:
                char_to_restore = char
                break

        if not char_to_restore:
            print(f"Character not found in archive: {name}")
            return

        # Remove archived_at field
        char_to_restore.pop("archived_at", None)

        # Atomic fix: remove from archive first
        archived = [char for char in archived if char["name"] != name]
        self.save_archive(self.characters_archive, archived)

        # v5.1 introduced: Restore to SQLite (via IndexManager)
        char_id = char_to_restore.get("id", char_to_restore.get("name", "unknown"))
        try:
            # Update entity status to active
            self._index_manager.update_entity_field(char_id, "status", "active")
            print(f"Character restored: {name}")
        except Exception as e:
            print(f"Entity status restore failed: {e}")

    def show_stats(self):
        """Show archive statistics"""
        chars = self.load_archive(self.characters_archive)
        threads = self.load_archive(self.plot_threads_archive)
        reviews = self.load_archive(self.reviews_archive)

        print("Archive statistics:")
        print(f"   Character archive: {len(chars)}")
        print(f"   Foreshadowing archive: {len(threads)}")
        print(f"   Report archive: {len(reviews)}")

        # Calculate archive file size
        total_size = 0
        for archive_file in [self.characters_archive, self.plot_threads_archive, self.reviews_archive]:
            if archive_file.exists():
                total_size += archive_file.stat().st_size

        print(f"   Archive size: {total_size / 1024:.2f} KB")

        # Show state.json size
        state_size_mb = self.state_file.stat().st_size / (1024 * 1024)
        print(f"\nstate.json current size: {state_size_mb:.2f} MB")


def main():
    parser = argparse.ArgumentParser(description="state.json Data Archive Management")

    parser.add_argument("--auto-check", action="store_true", help="Auto archive check")
    parser.add_argument("--force", action="store_true", help="Force archive (ignore trigger conditions)")
    parser.add_argument("--dry-run", action="store_true", help="Dry-run mode (only show data to be archived)")
    parser.add_argument("--restore-character", metavar="NAME", help="Restore archived character")
    parser.add_argument("--stats", action="store_true", help="Show archive statistics")
    parser.add_argument("--project-root", metavar="PATH", help="Project root directory (default: current directory)")

    args = parser.parse_args()

    # Resolve project root (allow passing "workspace root directory", resolve to actual book project_root)
    try:
        project_root = str(resolve_project_root(args.project_root) if args.project_root else resolve_project_root())
    except FileNotFoundError as exc:
        print(f"Cannot locate project root (need .wordsmith/state.json): {exc}", file=sys.stderr)
        sys.exit(1)

    manager = ArchiveManager(project_root=project_root)

    # Execute operation
    if args.auto_check or args.force:
        manager.run_auto_check(force=args.force, dry_run=args.dry_run)
    elif args.restore_character:
        manager.restore_character(args.restore_character)
    elif args.stats:
        manager.show_stats()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
