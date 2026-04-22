#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
webnovel unified entry script (no `cd` required)

Usage examples:
  python "<SCRIPTS_DIR>/webnovel.py" preflight
  python "<SCRIPTS_DIR>/webnovel.py" where
  python "<SCRIPTS_DIR>/webnovel.py" index stats

Notes:
- This script is only responsible for adding `.claude/scripts` to sys.path, then forwarding to `data_modules.webnovel`.
- Adapted for calling conventions when skills/agents are installed at project level or user level (~/.claude).
"""

from __future__ import annotations

import sys
from pathlib import Path

from runtime_compat import enable_windows_utf8_stdio


def main() -> None:
    scripts_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(scripts_dir))

    # Deferred import to avoid sys.path not ready
    from data_modules.webnovel import main as _main

    _main()


if __name__ == "__main__":
    enable_windows_utf8_stdio(skip_in_pytest=True)
    main()
