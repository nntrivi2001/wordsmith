#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Modules - Data Chain Module Package.

Note:
- Uses lazy import to avoid triggering runpy's RuntimeWarning when executing
  `python -m data_modules.xxx` due to package-level __init__ importing submodules early.
- Recommended usage (always safe):
    from data_modules.index_manager import IndexManager
- For backward compatibility, also preserved:
    from data_modules import IndexManager
"""

from __future__ import annotations

from importlib import import_module
from typing import Any


__all__ = [
    # Config
    "DataModulesConfig",
    "get_config",
    "set_project_root",
    # API Client
    "ModalAPIClient",
    "get_client",
    # Entity Linker
    "EntityLinker",
    "DisambiguationResult",
    # State Manager
    "StateManager",
    "EntityState",
    "Relationship",
    "StateChange",
    # Index Manager
    "IndexManager",
    "ChapterMeta",
    "SceneMeta",
    "ReviewMetrics",
    "RelationshipEventMeta",
    # RAG Adapter
    "RAGAdapter",
    "SearchResult",
    "ContextManager",
    "ContextRanker",
    "SnapshotManager",
    "QueryRouter",
    # Style Sampler
    "StyleSampler",
    "StyleSample",
    "SceneType",
]


_LAZY_EXPORTS: dict[str, tuple[str, str]] = {
    # Config
    "DataModulesConfig": (".config", "DataModulesConfig"),
    "get_config": (".config", "get_config"),
    "set_project_root": (".config", "set_project_root"),
    # API Client
    "ModalAPIClient": (".api_client", "ModalAPIClient"),
    "get_client": (".api_client", "get_client"),
    # Entity Linker
    "EntityLinker": (".entity_linker", "EntityLinker"),
    "DisambiguationResult": (".entity_linker", "DisambiguationResult"),
    # State Manager
    "StateManager": (".state_manager", "StateManager"),
    "EntityState": (".state_manager", "EntityState"),
    "Relationship": (".state_manager", "Relationship"),
    "StateChange": (".state_manager", "StateChange"),
    # Index Manager
    "IndexManager": (".index_manager", "IndexManager"),
    "ChapterMeta": (".index_manager", "ChapterMeta"),
    "SceneMeta": (".index_manager", "SceneMeta"),
    "ReviewMetrics": (".index_manager", "ReviewMetrics"),
    "RelationshipEventMeta": (".index_manager", "RelationshipEventMeta"),
    # RAG Adapter
    "RAGAdapter": (".rag_adapter", "RAGAdapter"),
    "SearchResult": (".rag_adapter", "SearchResult"),
    "ContextManager": (".context_manager", "ContextManager"),
    "ContextRanker": (".context_ranker", "ContextRanker"),
    "SnapshotManager": (".snapshot_manager", "SnapshotManager"),
    "QueryRouter": (".query_router", "QueryRouter"),
    # Style Sampler
    "StyleSampler": (".style_sampler", "StyleSampler"),
    "StyleSample": (".style_sampler", "StyleSample"),
    "SceneType": (".style_sampler", "SceneType"),
}


def __getattr__(name: str) -> Any:  # pragma: no cover
    if name not in _LAZY_EXPORTS:
        raise AttributeError(name)

    module_path, attr = _LAZY_EXPORTS[name]
    module = import_module(module_path, __name__)
    value = getattr(module, attr)
    globals()[name] = value  # cache
    return value


def __dir__() -> list[str]:  # pragma: no cover
    return sorted(set(list(globals().keys()) + list(_LAZY_EXPORTS.keys())))

