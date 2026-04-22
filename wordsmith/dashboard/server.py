"""
Dashboard launch script

Usage:
    python -m dashboard.server --project-root /path/to/novel-project
    python -m dashboard.server                   # auto-detect from .claude pointer
"""

import argparse
import os
import sys
import webbrowser
from pathlib import Path


def _resolve_project_root(cli_root: str | None) -> Path:
    """Resolve PROJECT_ROOT by priority: CLI > environment variable > .claude pointer > CWD."""
    if cli_root:
        return Path(cli_root).resolve()

    env = os.environ.get("WORDSMITH_PROJECT_ROOT")
    if env:
        return Path(env).resolve()

    # Attempt to read from the .claude pointer file
    cwd = Path.cwd()
    pointer = cwd / ".claude" / ".wordsmith-current-project"
    if pointer.is_file():
        target = pointer.read_text(encoding="utf-8").strip()
        if target:
            p = Path(target)
            if p.is_dir() and (p / ".wordsmith" / "state.json").is_file():
                return p.resolve()

    # Final fallback: current directory
    if (cwd / ".wordsmith" / "state.json").is_file():
        return cwd.resolve()

    print("ERROR: Unable to locate PROJECT_ROOT (requires a directory containing .wordsmith/state.json)", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Webnovel Dashboard Server")
    parser.add_argument("--project-root", type=str, default=None, help="Novel project root directory")
    parser.add_argument("--host", default="127.0.0.1", help="Bind address")
    parser.add_argument("--port", type=int, default=8765, help="Bind port")
    parser.add_argument("--no-browser", action="store_true", help="Do not open the browser automatically")
    args = parser.parse_args()

    project_root = _resolve_project_root(args.project_root)
    print(f"Project path: {project_root}")

    # Deferred import so that the path is resolved before loading the app
    import uvicorn
    from .app import create_app

    app = create_app(project_root)

    url = f"http://{args.host}:{args.port}"
    print(f"Dashboard started: {url}")
    print(f"API docs: {url}/docs")

    if not args.no_browser:
        webbrowser.open(url)

    uvicorn.run(app, host=args.host, port=args.port, log_level="info")


if __name__ == "__main__":
    main()
