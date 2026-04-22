#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    import chapter_paths

    return chapter_paths


def test_default_chapter_draft_path_uses_outline_heading_title(tmp_path):
    module = _load_module()

    outline_dir = tmp_path / "Outline"
    outline_dir.mkdir(parents=True, exist_ok=True)
    (outline_dir / "Volume_1_detailed_outline.md").write_text("### Chapter 1: Test title\nTest outline", encoding="utf-8")

    draft_path = module.default_chapter_draft_path(tmp_path, 1)

    assert draft_path.name == "Ch0001-Test title.md"


def test_default_chapter_draft_path_falls_back_to_split_outline_filename(tmp_path):
    module = _load_module()

    outline_dir = tmp_path / "Outline"
    outline_dir.mkdir(parents=True, exist_ok=True)
    (outline_dir / "Ch0002-Title_File.md").write_text("No chapter title heading", encoding="utf-8")

    draft_path = module.default_chapter_draft_path(tmp_path, 2)

    assert draft_path.name == "Ch0002-Title_File.md"


def test_find_chapter_file_supports_titled_flat_filename(tmp_path):
    module = _load_module()

    chapter_path = tmp_path / "Main text" / "Ch0003-Storm is coming.md"
    chapter_path.parent.mkdir(parents=True, exist_ok=True)
    chapter_path.write_text("Main text", encoding="utf-8")

    found = module.find_chapter_file(tmp_path, 3)

    assert found == chapter_path
