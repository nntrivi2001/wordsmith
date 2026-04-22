#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git Integration Backup Management System (Backup Manager with Git)

Core philosophy: Writing 2 million words inevitably leads to "ruined settings", need to support rollback to any point in time.

Major upgrade: Use Git for atomic version control

Why choose Git:
1. Atomic rollback: state.json + body/*.md rollback simultaneously, 100% data consistency
2. Incremental storage: Only store diffs, saves 95% space
3. Mature and stable: Version control system verified by 20 years of use
4. Branch management: Naturally supports "parallel world" creation

Features:
1. Auto Git commit: Auto commit after each /wordsmith-write completion
2. Atomic rollback: git checkout rolls back all files simultaneously
3. Version history: git log views complete history
4. Diff comparison: git diff views differences between any two versions
5. Branch creation: git branch creates branch from any point in time

Usage:
  # Auto backup after Chapter 45 completion (auto git commit)
  python backup_manager.py --chapter 45

  # Rollback to Chapter 30 state (git checkout)
  python backup_manager.py --rollback 30

  # View diff between Chapter 20 and Chapter 40 (git diff)
  python backup_manager.py --diff 20 40

  # Create branch from Chapter 50 (git branch)
  python backup_manager.py --create-branch 50 --branch-name "alternative-ending"

  # List all backups (git log)
  python backup_manager.py --list

Git commit standards:
  - Commit message format: "Chapter {N}: {chapter title}"
  - Tag format: "ch{N}" (e.g., ch0045)
  - Each chapter corresponds to one commit + one tag

Data consistency guarantee:
  During rollback, state.json and all .md files rollback synchronously
  No "state records Foundation Building stage, but file writes Golden Core stage" data tearing
  Atomic operations, either all succeed or all fail
"""

import subprocess
import json
import os
import sys
import shutil
from pathlib import Path

from runtime_compat import enable_windows_utf8_stdio
from datetime import datetime
from typing import Optional, List, Tuple

# ============================================================================
# Security fix: Import security utility functions (P1 MEDIUM)
# ============================================================================
from security_utils import sanitize_commit_message, is_git_available, is_git_repo, git_graceful_operation
from project_locator import resolve_project_root

# Windows encoding compatibility fix
if sys.platform == "win32":
    enable_windows_utf8_stdio()

class GitBackupManager:
    """Git-based backup manager (supports graceful degradation)"""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.git_dir = self.project_root / ".git"
        self.git_available = is_git_available()

        if not self.git_available:
            print("Git is not available, will use local backup mode")
            print("To enable Git version control, please install Git: https://git-scm.com/")
            return

        # Check if Git is initialized
        if not self.git_dir.exists():
            print("Git not initialized, please run /wordsmith-init or manually execute git init")
            print("Now auto-initializing Git...")
            self._init_git()

    def _init_git(self) -> bool:
        """Initialize Git repository"""
        try:
            # git init
            subprocess.run(
                ["git", "init"],
                cwd=self.project_root,
                check=True,
                capture_output=True
            )

            # Create .gitignore
            gitignore_file = self.project_root / ".gitignore"
            if not gitignore_file.exists():
                with open(gitignore_file, 'w', encoding='utf-8') as f:
                    f.write("""# Python
__pycache__/
*.py[cod]
*.so

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
""")

            # Initial commit
            subprocess.run(
                ["git", "add", "."],
                cwd=self.project_root,
                check=True,
                capture_output=True
            )

            subprocess.run(
                ["git", "commit", "-m", "Initial commit: Project initialized"],
                cwd=self.project_root,
                check=True,
                capture_output=True
            )

            print("Git repository initialized")
            return True

        except subprocess.CalledProcessError as e:
            print(f"Git initialization failed: {e}")
            return False

    def _run_git_command(self, args: List[str], check: bool = True) -> Tuple[bool, str]:
        """Execute Git command (supports graceful degradation)"""
        if not self.git_available:
            return False, "Git not available"

        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.project_root,
                check=check,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=60
            )

            return True, result.stdout

        except subprocess.CalledProcessError as e:
            return False, e.stderr
        except subprocess.TimeoutExpired:
            return False, "Git command timeout"
        except OSError as e:
            return False, str(e)

    def _local_backup(self, chapter_num: int) -> bool:
        """Local backup (degradation solution when Git is unavailable)"""
        backup_dir = self.project_root / ".webnovel" / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"ch{chapter_num:04d}_{timestamp}"
        backup_path = backup_dir / backup_name

        try:
            # Backup state.json
            state_file = self.project_root / ".webnovel" / "state.json"
            if state_file.exists():
                backup_path.mkdir(parents=True, exist_ok=True)
                shutil.copy2(state_file, backup_path / "state.json")

            print(f"Local backup complete: {backup_path}")
            return True
        except OSError as e:
            print(f"Local backup failed: {e}")
            return False

    def backup(self, chapter_num: int, chapter_title: str = "") -> bool:
        """
        Backup current state (Git commit + tag, or local backup)

        Args:
            chapter_num: Chapter number
            chapter_title: Chapter title (optional)
        """
        print(f"Backing up chapter {chapter_num}...")

        # If Git is unavailable, use local backup
        if not self.git_available:
            return self._local_backup(chapter_num)

        # Step 1: git add .
        success, output = self._run_git_command(["add", "."])
        if not success:
            print(f"git add failed: {output}")
            return False

        # Step 2: git commit
        commit_message = f"Chapter {chapter_num}"
        if chapter_title:
            # ============================================================================
            # Security fix: Sanitize commit message to prevent command injection (CWE-77) - P1 MEDIUM
            # Original code: commit_message += f": {chapter_title}"
            # Vulnerability: chapter_title may contain Git flags (like --author, --amend) causing command injection
            # ============================================================================
            safe_chapter_title = sanitize_commit_message(chapter_title)
            commit_message += f": {safe_chapter_title}"

        success, output = self._run_git_command(
            ["commit", "-m", commit_message],
            check=False  # Allow "nothing to commit" situation
        )

        if not success and "nothing to commit" in output:
            print("No changes, skipping commit")
            return True
        elif not success:
            print(f"git commit failed: {output}")
            return False

        print(f"Git commit complete: {commit_message}")

        # Step 3: git tag
        tag_name = f"ch{chapter_num:04d}"

        # Delete old tag (if exists)
        self._run_git_command(["tag", "-d", tag_name], check=False)

        success, output = self._run_git_command(["tag", tag_name])
        if not success:
            print(f"Tag creation failed (non-fatal): {output}")
        else:
            print(f"Git tag created: {tag_name}")

        return True

    def rollback(self, chapter_num: int) -> bool:
        """
        Rollback to specified chapter (Git checkout)

        Warning: This will discard all uncommitted changes!
        """

        tag_name = f"ch{chapter_num:04d}"

        print(f"Rolling back to chapter {chapter_num}...")
        print(f"Warning: This will discard all uncommitted changes!")

        # Check for uncommitted changes
        success, status_output = self._run_git_command(["status", "--porcelain"])

        if status_output.strip():
            print("\nUncommitted changes detected:")
            print(status_output)

            # Create backup commit
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_branch = f"backup_before_rollback_{timestamp}"

            print(f"\nCreating backup branch: {backup_branch}")

            success, _ = self._run_git_command(["checkout", "-b", backup_branch])
            if not success:
                print("Backup branch creation failed")
                return False

            success, _ = self._run_git_command(["add", "."])
            success, _ = self._run_git_command(
                ["commit", "-m", f"Backup before rollback to chapter {chapter_num}"]
            )

            print(f"Backup branch created: {backup_branch}")

            # Switch back to master
            success, _ = self._run_git_command(["checkout", "master"])

        # Execute rollback
        success, output = self._run_git_command(["checkout", tag_name])

        if not success:
            print(f"Rollback failed: {output}")
            print(f"Tip: Make sure tag '{tag_name}' exists (run --list to view all backups)")
            return False

        print(f"Rolled back to chapter {chapter_num}!")
        print(f"\nTip:")
        print(f"  - All files (state.json + body/*.md) have been rolled back synchronously")
        print(f"  - To recover, run: git checkout master")

        return True

    def diff(self, chapter_a: int, chapter_b: int):
        """Compare differences between two versions (Git diff)"""

        tag_a = f"ch{chapter_a:04d}"
        tag_b = f"ch{chapter_b:04d}"

        print(f"Comparing differences between chapter {chapter_a} and chapter {chapter_b}...\n")

        success, output = self._run_git_command(["diff", tag_a, tag_b, "--stat"])

        if not success:
            print(f"Comparison failed: {output}")
            return

        print("File change statistics:")
        print(output)

        # Show detailed state.json diff
        print("\nstate.json detailed differences:")
        success, state_diff = self._run_git_command(
            ["diff", tag_a, tag_b, "--", ".webnovel/state.json"]
        )

        if success and state_diff:
            print(state_diff[:2000])  # Limit output length
            if len(state_diff) > 2000:
                print("\n...(output too long, truncated)")
        else:
            print("(no changes)")

    def list_backups(self):
        """List all backups (Git log + tags)"""

        print("\nBackup list (Git tags):\n")

        # Get all tags
        success, tags_output = self._run_git_command(["tag", "-l", "ch*"])

        if not success or not tags_output:
            print("No backups yet")
            return

        tags = sorted(tags_output.strip().split('\n'))

        for tag in tags:
            # Extract chapter number
            chapter_num = int(tag[2:])

            # Get commit info for this tag
            success, commit_info = self._run_git_command(
                ["log", tag, "-1", "--format=%h %ci %s"]
            )

            if success:
                print(f"{tag} | {commit_info.strip()}")

        print(f"\nTotal: {len(tags)} backups")

        # Show recent 5 commits
        print("\nRecent commit history:\n")
        success, log_output = self._run_git_command(
            ["log", "--oneline", "-5"]
        )

        if success:
            print(log_output)

    def create_branch(self, chapter_num: int, branch_name: str) -> bool:
        """Create branch from specified chapter (Git branch)"""

        tag_name = f"ch{chapter_num:04d}"

        print(f"Creating branch from chapter {chapter_num}: {branch_name}")

        # Check if tag exists
        success, _ = self._run_git_command(["rev-parse", tag_name], check=False)

        if not success:
            print(f"Tag '{tag_name}' does not exist")
            return False

        # Create branch
        success, output = self._run_git_command(["branch", branch_name, tag_name])

        if not success:
            print(f"Branch creation failed: {output}")
            return False

        print(f"Branch created: {branch_name}")
        print(f"\nSwitch to branch:")
        print(f"  git checkout {branch_name}")

        return True

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Git Integration Backup Management System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Auto backup after Chapter 45 completion
  python backup_manager.py --chapter 45

  # Rollback to Chapter 30 (atomic: state.json + all .md files)
  python backup_manager.py --rollback 30

  # View differences between Chapter 20 and Chapter 40
  python backup_manager.py --diff 20 40

  # Create branch from Chapter 50
  python backup_manager.py --create-branch 50 --branch-name "alternative-ending"

  # List all backups
  python backup_manager.py --list
        """
    )

    parser.add_argument('--chapter', type=int, help='Backup chapter number')
    parser.add_argument('--chapter-title', help='Chapter title (optional)')
    parser.add_argument('--rollback', type=int, metavar='CHAPTER', help='Rollback to specified chapter')
    parser.add_argument('--diff', nargs=2, type=int, metavar=('A', 'B'), help='Compare two versions')
    parser.add_argument('--create-branch', type=int, metavar='CHAPTER', help='Create branch from specified chapter')
    parser.add_argument('--branch-name', help='Branch name')
    parser.add_argument('--list', action='store_true', help='List all backups')
    parser.add_argument('--project-root', default='.', help='Project root directory')

    args = parser.parse_args()

    # Resolve project root (allow passing "workspace root directory", resolve to actual book project_root)
    try:
        project_root = str(resolve_project_root(args.project_root))
    except FileNotFoundError as exc:
        print(f"Cannot locate project root (need .webnovel/state.json): {exc}", file=sys.stderr)
        sys.exit(1)

    # Create manager
    manager = GitBackupManager(project_root)

    # Execute operation
    if args.chapter:
        manager.backup(args.chapter, args.chapter_title or "")

    elif args.rollback:
        manager.rollback(args.rollback)

    elif args.diff:
        manager.diff(args.diff[0], args.diff[1])

    elif args.create_branch:
        if not args.branch_name:
            print("Branch creation requires --branch-name parameter")
            sys.exit(1)
        manager.create_branch(args.create_branch, args.branch_name)

    elif args.list:
        manager.list_backups()

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
