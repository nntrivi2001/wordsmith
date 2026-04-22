"""
Path Traversal Guard

All file-read APIs MUST pass through this module for validation before accessing the disk.
"""

from pathlib import Path
from fastapi import HTTPException


def safe_resolve(project_root: Path, relative: str) -> Path:
    """Resolve a relative path to an absolute path, ensuring it stays within project_root.

    Raises:
        HTTPException 403 if the resolved path escapes from project_root.
    """
    try:
        resolved = (project_root / relative).resolve()
    except (OSError, ValueError):
        raise HTTPException(status_code=403, detail="Invalid path")

    # Strictly require that the target path is a subpath of or equal to project_root
    try:
        resolved.relative_to(project_root.resolve())
    except ValueError:
        raise HTTPException(status_code=403, detail="Path out of bounds: access to files outside PROJECT_ROOT is forbidden")

    return resolved
