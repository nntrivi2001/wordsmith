#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAGAdapter tests
"""

import sys
import json
import asyncio
import logging
import sqlite3
from contextlib import closing

import pytest

import data_modules.rag_adapter as rag_module
from data_modules.rag_adapter import RAGAdapter
from data_modules.config import DataModulesConfig
from data_modules.index_manager import EntityMeta, RelationshipMeta


class StubClient:
    async def embed(self, texts):
        return [[1.0, 0.0] for _ in texts]

    async def embed_batch(self, texts, skip_failures=True):
        return [[1.0, 0.0] for _ in texts]

    async def rerank(self, query, documents, top_n=None):
        top_n = top_n or len(documents)
        return [{"index": i, "relevance_score": 1.0 / (i + 1)} for i in range(min(top_n, len(documents)))]


class StubClientWithFailures(StubClient):
    async def embed_batch(self, texts, skip_failures=True):
        if len(texts) == 1:
            return [None]
        return [None, [1.0, 0.0]]


class StubEmbedClient401:
    def __init__(self):
        self.last_error_status = 401
        self.last_error_message = "auth failed"


class StubClientAuthFailure(StubClient):
    def __init__(self):
        self._embed_client = StubEmbedClient401()

    async def embed(self, texts):
        return None


class StubClientRerankFailure(StubClient):
    async def rerank(self, query, documents, top_n=None):
        return []


@pytest.fixture
def temp_project(tmp_path, monkeypatch):
    cfg = DataModulesConfig.from_project_root(tmp_path)
    cfg.ensure_dirs()
    monkeypatch.setattr(rag_module, "get_client", lambda config: StubClient())
    return cfg


@pytest.mark.asyncio
async def test_store_and_search(temp_project):
    adapter = RAGAdapter(temp_project)
    chunks = [
        {"chapter": 1, "scene_index": 1, "content": "Xiao Yan cultivates battle qi at Tianyun Sect"},
        {"chapter": 1, "scene_index": 2, "content": "Elder Yao teaches alchemy techniques"},
    ]
    stored = await adapter.store_chunks(chunks)
    assert stored == 2

    vec_results = await adapter.vector_search("Xiao Yan", top_k=2)
    assert len(vec_results) == 2

    bm25_results = adapter.bm25_search("Xiao Yan", top_k=2)
    assert len(bm25_results) >= 1

    stats = adapter.get_stats()
    assert stats["vectors"] == 2


@pytest.mark.asyncio
async def test_store_chunks_with_embedding_failure(tmp_path, monkeypatch):
    cfg = DataModulesConfig.from_project_root(tmp_path)
    cfg.ensure_dirs()
    monkeypatch.setattr(rag_module, "get_client", lambda config: StubClientWithFailures())

    adapter = RAGAdapter(cfg)
    chunks = [
        {"chapter": 1, "scene_index": 1, "content": "Short content"},
        {"chapter": 1, "scene_index": 2, "content": "Slightly longer content for indexing"},
    ]
    stored = await adapter.store_chunks(chunks)
    assert stored == 1


@pytest.mark.asyncio
async def test_hybrid_search_full_scan(temp_project):
    adapter = RAGAdapter(temp_project)
    await adapter.store_chunks(
        [{"chapter": 1, "scene_index": 1, "content": "Xiao Yan trains"}]
    )
    results = await adapter.hybrid_search("Xiao Yan", vector_top_k=5, bm25_top_k=5, rerank_top_n=1)
    assert results
    assert results[0].source == "hybrid"


@pytest.mark.asyncio
async def test_hybrid_search_prefilter(tmp_path, monkeypatch):
    cfg = DataModulesConfig.from_project_root(tmp_path)
    cfg.ensure_dirs()
    cfg.vector_full_scan_max_vectors = 0
    monkeypatch.setattr(rag_module, "get_client", lambda config: StubClient())
    adapter = RAGAdapter(cfg)
    await adapter.store_chunks(
        [
            {"chapter": 1, "scene_index": 1, "content": "Xiao Yan trains"},
            {"chapter": 2, "scene_index": 1, "content": "Elder Yao appears"},
        ]
    )
    results = await adapter.hybrid_search("Elder Yao", vector_top_k=2, bm25_top_k=2, rerank_top_n=1)
    assert results


@pytest.mark.asyncio
async def test_search_respects_chapter_filter_across_strategies(tmp_path, monkeypatch):
    cfg = DataModulesConfig.from_project_root(tmp_path)
    cfg.ensure_dirs()
    cfg.vector_full_scan_max_vectors = 0  # Force pre-filter branch
    monkeypatch.setattr(rag_module, "get_client", lambda config: StubClient())
    adapter = RAGAdapter(cfg)
    await adapter.store_chunks(
        [
            {"chapter": 1, "scene_index": 1, "content": "Previous clues, key treasure not yet involved"},
            {"chapter": 2, "scene_index": 1, "content": "Secret treasure appears, triggers competition"},
            {"chapter": 3, "scene_index": 1, "content": "Secret treasure war fully erupts"},
        ]
    )

    vector_results = await adapter.vector_search("Secret treasure", top_k=5, chapter=1)
    assert vector_results
    assert all((r.chapter or 0) <= 1 for r in vector_results)

    bm25_results = adapter.bm25_search("Secret treasure", top_k=5, chapter=1)
    assert bm25_results
    assert all((r.chapter or 0) <= 1 for r in bm25_results)

    hybrid_results = await adapter.hybrid_search(
        "Secret treasure",
        vector_top_k=5,
        bm25_top_k=5,
        rerank_top_n=3,
        chapter=1,
    )
    assert hybrid_results
    assert all((r.chapter or 0) <= 1 for r in hybrid_results)


@pytest.mark.asyncio
async def test_graph_hybrid_search_with_entity_expansion(tmp_path, monkeypatch):
    cfg = DataModulesConfig.from_project_root(tmp_path)
    cfg.ensure_dirs()
    cfg.graph_rag_enabled = True
    monkeypatch.setattr(rag_module, "get_client", lambda config: StubClient())
    adapter = RAGAdapter(cfg)

    adapter.index_manager.upsert_entity(
        EntityMeta(
            id="xiaoyan",
            type="Character",
            canonical_name="Xiao Yan",
            current={},
            first_appearance=1,
            last_appearance=2,
        )
    )
    adapter.index_manager.upsert_entity(
        EntityMeta(
            id="yaolao",
            type="Character",
            canonical_name="Elder Yao",
            current={},
            first_appearance=1,
            last_appearance=2,
        )
    )
    adapter.index_manager.register_alias("Xiao Yan", "xiaoyan", "Character")
    adapter.index_manager.register_alias("Elder Yao", "yaolao", "Character")
    adapter.index_manager.upsert_relationship(
        RelationshipMeta(
            from_entity="xiaoyan",
            to_entity="yaolao",
            type="Master-disciple",
            description="Accept disciple",
            chapter=1,
        )
    )

    await adapter.store_chunks(
        [
            {"chapter": 1, "scene_index": 1, "content": "Becomes Elder Yao disciple, officially becomes master-disciple"},
            {"chapter": 2, "scene_index": 1, "content": "Xiao Yan cultivates battle qi at Tianyun Sect"},
        ]
    )

    results = await adapter.graph_hybrid_search(
        "Xiao Yan and Elder YaoRelationship",
        top_k=2,
        center_entities=["Xiao Yan", "Elder Yao"],
    )
    assert results
    assert any("Elder Yao" in r.content for r in results)
    assert all(r.source == "graph_hybrid" for r in results)


@pytest.mark.asyncio
async def test_search_auto_uses_graph_strategy_when_enabled(tmp_path, monkeypatch):
    cfg = DataModulesConfig.from_project_root(tmp_path)
    cfg.ensure_dirs()
    cfg.graph_rag_enabled = True
    monkeypatch.setattr(rag_module, "get_client", lambda config: StubClient())
    adapter = RAGAdapter(cfg)
    adapter.index_manager.upsert_entity(
        EntityMeta(
            id="xiaoyan",
            type="Character",
            canonical_name="Xiao Yan",
            current={},
            first_appearance=1,
            last_appearance=1,
        )
    )
    adapter.index_manager.register_alias("Xiao Yan", "xiaoyan", "Character")
    await adapter.store_chunks(
        [{"chapter": 1, "scene_index": 1, "content": "Xiao Yan breaks through to Battle Master"}]
    )

    results = await adapter.search("Xiao YanRelationship", top_k=1, strategy="auto")
    assert results
    assert results[0].source in {"graph_hybrid", "hybrid"}


@pytest.mark.asyncio
async def test_graph_hybrid_search_fallback_when_graph_disabled(tmp_path, monkeypatch):
    cfg = DataModulesConfig.from_project_root(tmp_path)
    cfg.ensure_dirs()
    cfg.graph_rag_enabled = False
    monkeypatch.setattr(rag_module, "get_client", lambda config: StubClient())
    adapter = RAGAdapter(cfg)
    await adapter.store_chunks(
        [{"chapter": 1, "scene_index": 1, "content": "Xiao Yan cultivates battle qi at Tianyun Sect"}]
    )

    modes = []

    def _record_log(query, mode, results, latency_ms, chapter=None):
        modes.append(mode)

    monkeypatch.setattr(adapter, "_log_query", _record_log)
    results = await adapter.graph_hybrid_search("Xiao YanRelationship", top_k=1)

    assert results
    assert modes
    assert modes[-1] == "graph_hybrid_fallback"
    assert all(r.source == "hybrid" for r in results)


@pytest.mark.asyncio
async def test_graph_hybrid_search_rerank_failure_uses_candidates(tmp_path, monkeypatch):
    cfg = DataModulesConfig.from_project_root(tmp_path)
    cfg.ensure_dirs()
    cfg.graph_rag_enabled = True
    monkeypatch.setattr(rag_module, "get_client", lambda config: StubClientRerankFailure())
    adapter = RAGAdapter(cfg)

    adapter.index_manager.upsert_entity(
        EntityMeta(
            id="xiaoyan",
            type="Character",
            canonical_name="Xiao Yan",
            current={},
            first_appearance=1,
            last_appearance=2,
        )
    )
    adapter.index_manager.upsert_entity(
        EntityMeta(
            id="yaolao",
            type="Character",
            canonical_name="Elder Yao",
            current={},
            first_appearance=1,
            last_appearance=2,
        )
    )
    adapter.index_manager.register_alias("Xiao Yan", "xiaoyan", "Character")
    adapter.index_manager.register_alias("Elder Yao", "yaolao", "Character")
    adapter.index_manager.upsert_relationship(
        RelationshipMeta(
            from_entity="xiaoyan",
            to_entity="yaolao",
            type="Master-disciple",
            description="Accept disciple",
            chapter=1,
        )
    )

    await adapter.store_chunks(
        [
            {"chapter": 1, "scene_index": 1, "content": "Becomes Elder Yao disciple, officially becomes master-disciple"},
            {"chapter": 2, "scene_index": 1, "content": "Xiao Yan cultivates battle qi at Tianyun Sect"},
        ]
    )

    results = await adapter.graph_hybrid_search(
        "Xiao Yan and Elder YaoRelationship",
        top_k=2,
        center_entities=["Xiao Yan", "Elder Yao"],
    )

    assert results
    assert len(results) <= 2
    assert all(r.source == "graph_hybrid" for r in results)


@pytest.mark.asyncio
async def test_search_unknown_strategy_falls_back_to_hybrid(tmp_path, monkeypatch):
    cfg = DataModulesConfig.from_project_root(tmp_path)
    cfg.ensure_dirs()
    monkeypatch.setattr(rag_module, "get_client", lambda config: StubClient())
    adapter = RAGAdapter(cfg)
    await adapter.store_chunks(
        [{"chapter": 1, "scene_index": 1, "content": "Xiao Yan cultivates battle qi at Tianyun Sect"}]
    )

    results = await adapter.search("Xiao Yan", top_k=1, strategy="not_exists")
    assert results
    assert all(r.source == "hybrid" for r in results)


@pytest.mark.asyncio
async def test_search_with_backtrack(temp_project):
    adapter = RAGAdapter(temp_project)
    chunks = [
        {
            "chapter": 1,
            "scene_index": 0,
            "content": "Chapter summary",
            "chunk_type": "summary",
            "chunk_id": "ch0001_summary",
            "source_file": "summaries/ch0001.md",
        },
        {
            "chapter": 1,
            "scene_index": 1,
            "content": "Scene content",
            "chunk_type": "scene",
            "chunk_id": "ch0001_s1",
            "parent_chunk_id": "ch0001_summary",
            "source_file": "Main/Ch0001.md#scene_1",
        },
    ]
    await adapter.store_chunks(chunks)
    results = await adapter.search_with_backtrack("Scene", top_k=1)
    assert any(r.chunk_type == "summary" for r in results)


def test_vector_helpers(temp_project):
    adapter = RAGAdapter(temp_project)
    emb = [1.0, 0.0]
    data = adapter._serialize_embedding(emb)
    assert adapter._deserialize_embedding(data) == emb

    assert adapter._cosine_similarity([0.0, 0.0], [1.0, 0.0]) == 0.0


def test_recent_and_fetch_vectors(temp_project):
    adapter = RAGAdapter(temp_project)
    with adapter._get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO vectors (chunk_id, chapter, scene_index, content, embedding, parent_chunk_id, chunk_type, source_file) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ("ch0001_s1", 1, 1, "Content", b"", None, "scene", "Main/Ch0001.md#scene_1"),
        )
        cursor.execute(
            "INSERT INTO vectors (chunk_id, chapter, scene_index, content, embedding, parent_chunk_id, chunk_type, source_file) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ("ch0002_s1", 2, 1, "Later content", b"", None, "scene", "Main/Ch0002.md#scene_1"),
        )
        conn.commit()

    assert adapter._get_vectors_count() == 2
    assert adapter._get_recent_chunk_ids(1) == ["ch0002_s1"]
    assert adapter._get_recent_chunk_ids(10, chapter=1) == ["ch0001_s1"]
    rows = adapter._fetch_vectors_by_chunk_ids(["ch0001_s1"])
    assert len(rows) == 1


def test_init_db_migrates_legacy_vectors_schema(tmp_path, monkeypatch):
    cfg = DataModulesConfig.from_project_root(tmp_path)
    cfg.ensure_dirs()
    monkeypatch.setattr(rag_module, "get_client", lambda config: StubClient())

    # Old structure: missing parent_chunk_id/chunk_type/source_file/created_at
    with closing(sqlite3.connect(str(cfg.vector_db))) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE vectors (
                chunk_id TEXT PRIMARY KEY,
                chapter INTEGER,
                scene_index INTEGER,
                content TEXT,
                embedding BLOB
            )
            """
        )
        cursor.execute(
            """
            INSERT INTO vectors (chunk_id, chapter, scene_index, content, embedding)
            VALUES (?, ?, ?, ?, ?)
            """,
            ("ch0001_s1", 1, 1, "Old data", b""),
        )
        conn.commit()

    adapter = RAGAdapter(cfg)

    with adapter._get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(vectors)")
        cols = {row[1] for row in cursor.fetchall()}
        assert {"parent_chunk_id", "chunk_type", "source_file", "created_at"}.issubset(cols)
        cursor.execute("SELECT COUNT(*) FROM vectors")
        assert cursor.fetchone()[0] == 1
        cursor.execute("SELECT chunk_type FROM vectors WHERE chunk_id = ?", ("ch0001_s1",))
        row = cursor.fetchone()
        assert row is not None
        assert row[0] == "scene"

    backup_dir = cfg.webnovel_dir / "backups"
    backups = list(backup_dir.glob("vectors.db.schema_migration.v*.bak"))
    assert backups


def test_rag_adapter_cli(temp_project, monkeypatch, capsys):
    # stats
    def run_cli(args):
        monkeypatch.setattr(sys, "argv", ["rag_adapter"] + args)
        rag_module.main()

    root = str(temp_project.project_root)
    run_cli(["--project-root", root, "stats"])

    # index-chapter
    run_cli(
        [
            "--project-root",
            root,
            "index-chapter",
            "--chapter",
            "1",
            "--scenes",
            json.dumps([{"index": 1, "summary": "Summary", "content": "Content"}], ensure_ascii=False),
        ]
    )

    # search
    run_cli(["--project-root", root, "search", "--query", "Content", "--mode", "bm25", "--top-k", "5"])
    run_cli(["--project-root", root, "search", "--query", "Content", "--mode", "vector", "--top-k", "5"])
    run_cli(["--project-root", root, "search", "--query", "Content", "--mode", "hybrid", "--top-k", "5"])
    run_cli(["--project-root", root, "search", "--query", "Content", "--mode", "auto", "--top-k", "5"])

    capsys.readouterr()


def test_rag_adapter_log_query_failure_is_reported(temp_project, monkeypatch, caplog):
    adapter = RAGAdapter(temp_project)

    def _raise_log_error(*args, **kwargs):
        raise RuntimeError("log write failed")

    monkeypatch.setattr(adapter.index_manager, "log_rag_query", _raise_log_error)

    with caplog.at_level(logging.WARNING):
        adapter._log_query("q", "vector", [], 1)

    message_text = "\n".join(record.getMessage() for record in caplog.records)
    assert "failed to log rag query" in message_text


def test_rag_adapter_cli_search_shows_degraded_warning(temp_project, monkeypatch, capsys):
    monkeypatch.setattr(rag_module, "get_client", lambda config: StubClientAuthFailure())

    def run_cli(args):
        monkeypatch.setattr(sys, "argv", ["rag_adapter"] + args)
        rag_module.main()

    root = str(temp_project.project_root)
    run_cli(["--project-root", root, "search", "--query", "Test", "--mode", "vector", "--top-k", "3"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out.strip().splitlines()[-1])
    assert payload.get("status") == "success"
    warnings = payload.get("warnings") or []
    assert warnings
    assert warnings[0].get("code") == "DEGRADED_MODE"
    assert warnings[0].get("reason") == "embedding_auth_failed"
