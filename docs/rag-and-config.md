# RAG & Configuration Guide

## RAG Retrieval Architecture

```text
Query → QueryRouter(auto) → vector / bm25 / hybrid / graph_hybrid
                     └→ RRF fusion + Rerank → Top-K
```

Default models:

- Embedding: `Qwen/Qwen3-Embedding-8B`
- Reranker: `jina-reranker-v3`

## Environment Variable Loading Order

1. Process environment variables (highest priority)
2. `.env` file in the book project root directory
3. User-level global: `~/.claude/wordsmith/.env`

## Minimal `.env` Configuration

```bash
EMBED_BASE_URL=https://api-inference.modelscope.cn/v1
EMBED_MODEL=Qwen/Qwen3-Embedding-8B
EMBED_API_KEY=your_embed_api_key

RERANK_BASE_URL=https://api.jina.ai/v1
RERANK_MODEL=jina-reranker-v3
RERANK_API_KEY=your_rerank_api_key
```

Notes:

- If an Embedding key is not configured, semantic search will fall back to BM25.
- It is recommended to configure a separate `${PROJECT_ROOT}/.env` for each book to avoid cross-project configuration interference.