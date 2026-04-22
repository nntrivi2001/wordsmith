#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI Argument Compatibility Utilities.

Background:
- CLIs under data_modules commonly use argparse + subparsers.
- argparse global arguments (e.g., --project-root) are required to appear before subcommands:
    python -m data_modules.index_manager --project-root X get-core-entities
  But in actual writing workflows (skills/agents documentation, tool calls), --project-root is often placed after subcommands:
    python -m data_modules.index_manager get-core-entities --project-root X
  This directly raises "unrecognized arguments" (see issues7 log).

This provides a lightweight argv preprocessing: extracts --project-root from any position and prepends it,
so existing argparse definitions can be compatible with both without major changes.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any
from typing import List, Optional, Tuple


def _extract_flag_value(argv: List[str], flag: str) -> Tuple[Optional[str], List[str]]:
    """
    Extract a flag value from argv.

    Supports:
    - --flag VALUE
    - --flag=VALUE

    Returns:
    - (value, remaining_argv)
    - value uses the *last* occurrence when repeated.
    - if a dangling `--flag` has no value, it is kept in remaining_argv for argparse to raise.
    """
    value: Optional[str] = None
    rest: List[str] = []
    i = 0
    while i < len(argv):
        token = argv[i]
        if token == flag:
            if i + 1 < len(argv):
                value = argv[i + 1]
                i += 2
                continue
            # Dangling flag; keep it so argparse can error out properly.
            rest.append(token)
            i += 1
            continue
        if token.startswith(flag + "="):
            value = token.split("=", 1)[1]
            i += 1
            continue
        rest.append(token)
        i += 1
    return value, rest


def normalize_global_project_root(argv: List[str], *, flag: str = "--project-root") -> List[str]:
    """
    Normalize argv so a global `--project-root` (when present) is moved before subcommands.

    This makes argparse+subparsers accept both:
    - `... --project-root X cmd ...`
    - `... cmd ... --project-root X`
    """
    value, rest = _extract_flag_value(argv, flag)
    if value is None:
        return argv
    return [flag, value] + rest


def load_json_arg(raw: str) -> Any:
    """
    Parse CLI JSON arguments, supports two forms:
    - Direct JSON string: '{"a":1}'
    - @ file path: '@data.json' (read JSON from file, avoid shell quote hell)
      - Special case: '@-' means read from stdin
    """
    if raw is None:
        raise ValueError("missing json arg")
    text = str(raw).strip()
    if text.startswith("@"):
        target = text[1:].strip()
        if not target:
            raise ValueError("invalid json arg: '@' without path")
        if target == "-":
            content = sys.stdin.read()
        else:
            content = Path(target).read_text(encoding="utf-8")
        return json.loads(content)
    return json.loads(text)
