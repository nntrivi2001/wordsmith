#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Modules - Configuration File

API configuration read via environment variables (supports .env files):
- EMBED_BASE_URL, EMBED_MODEL, EMBED_API_KEY
- RERANK_BASE_URL, RERANK_MODEL, RERANK_API_KEY
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

from runtime_compat import normalize_windows_path

from .context_weights import TEMPLATE_WEIGHTS_DYNAMIC_DEFAULT

def _get_user_claude_root() -> Path:
    raw = os.environ.get("WEBNOVEL_CLAUDE_HOME") or os.environ.get("CLAUDE_HOME")
    if raw:
        try:
            return normalize_windows_path(raw).expanduser().resolve()
        except Exception:
            return normalize_windows_path(raw).expanduser()
    return (Path.home() / ".claude").resolve()


def _load_dotenv_file(env_path: Path, *, override: bool = False) -> bool:
    if not env_path.exists():
        return False
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip()
                    if not key:
                        continue
                    # Do not override existing env vars by default (explicit > .env priority)
                    if override or key not in os.environ:
                        os.environ[key] = value
        return True
    except Exception:
        return False


def _load_dotenv():
    """
    Load .env file (best-effort).

    Convention:
    - Project-level `.env` (in current working directory) takes priority;
    - Global `.env` as fallback: `~/.claude/wordsmith/.env`
    """
    # 1) Current directory (common: user runs from project root)
    _load_dotenv_file(Path.cwd() / ".env", override=False)

    # 2) User-level global (common: skills/agents installed globally, API key stored here for convenience)
    global_env = _get_user_claude_root() / "wordsmith" / ".env"
    _load_dotenv_file(global_env, override=False)


def _load_project_dotenv(project_root: Path) -> None:
    """
    Load `.env` under a project root directory (best-effort).
    Note: Do not overwrite existing environment variables to avoid accidental cross-contamination.
    """
    try:
        _load_dotenv_file(Path(project_root) / ".env", override=False)
    except Exception:
        return

_load_dotenv()


def _default_context_template_weights_dynamic() -> dict[str, dict[str, dict[str, float]]]:
    return {
        stage: {
            template: dict(weights)
            for template, weights in templates.items()
        }
        for stage, templates in TEMPLATE_WEIGHTS_DYNAMIC_DEFAULT.items()
    }


@dataclass
class DataModulesConfig:
    """Data modules configuration"""

    # ================= Project Paths =================
    project_root: Path = field(default_factory=lambda: Path.cwd())

    @property
    def webnovel_dir(self) -> Path:
        return self.project_root / ".webnovel"

    @property
    def state_file(self) -> Path:
        return self.webnovel_dir / "state.json"

    @property
    def index_db(self) -> Path:
        return self.webnovel_dir / "index.db"

    # v5.1 introduced: alias_index_file is deprecated; aliases stored in index.db aliases table

    @property
    def chapters_dir(self) -> Path:
        return self.project_root / "Chapters"

    @property
    def settings_dir(self) -> Path:
        return self.project_root / "Settings"

    @property
    def outline_dir(self) -> Path:
        return self.project_root / "Outline"


    # ================= Embedding API Configuration =================
    embed_api_type: str = "openai"
    embed_base_url: str = field(default_factory=lambda: os.getenv("EMBED_BASE_URL", "https://api-inference.modelscope.cn/v1"))
    embed_model: str = field(default_factory=lambda: os.getenv("EMBED_MODEL", "Qwen/Qwen3-Embedding-8B"))
    embed_api_key: str = field(default_factory=lambda: os.getenv("EMBED_API_KEY", ""))

    @property
    def embed_url(self) -> str:
        return self.embed_base_url

    # ================= Rerank API Configuration =================
    rerank_api_type: str = "openai"
    rerank_base_url: str = field(default_factory=lambda: os.getenv("RERANK_BASE_URL", "https://api.jina.ai/v1"))
    rerank_model: str = field(default_factory=lambda: os.getenv("RERANK_MODEL", "jina-reranker-v3"))
    rerank_api_key: str = field(default_factory=lambda: os.getenv("RERANK_API_KEY", ""))

    @property
    def rerank_url(self) -> str:
        return self.rerank_base_url

    # ================= Concurrency Configuration =================
    embed_concurrency: int = 64
    rerank_concurrency: int = 32
    embed_batch_size: int = 64

    # ================= Timeout Configuration =================
    cold_start_timeout: int = 300
    normal_timeout: int = 180

    # ================= Retry Configuration =================
    api_max_retries: int = 3  # Maximum retry attempts
    api_retry_delay: float = 1.0  # Initial retry delay (seconds), exponential backoff

    # ================= Retrieval Configuration =================
    vector_top_k: int = 30
    bm25_top_k: int = 20
    rerank_top_n: int = 10
    rrf_k: int = 60

    vector_full_scan_max_vectors: int = 500
    vector_prefilter_bm25_candidates: int = 200
    vector_prefilter_recent_candidates: int = 200

    # ================= Graph-RAG Configuration =================
    graph_rag_enabled: bool = False
    graph_rag_expand_hops: int = 1
    graph_rag_max_expanded_entities: int = 30
    graph_rag_candidate_limit: int = 150
    graph_rag_boost_same_entity: float = 0.2
    graph_rag_boost_related_entity: float = 0.1
    graph_rag_boost_recency: float = 0.05

    relationship_graph_from_index_enabled: bool = True

    # ================= Entity Extraction Configuration =================
    extraction_confidence_high: float = 0.8
    extraction_confidence_medium: float = 0.5

    # ================= List Truncation Limits =================
    max_disambiguation_warnings: int = 500
    max_disambiguation_pending: int = 1000
    max_state_changes: int = 2000

    context_recent_summaries_window: int = 3
    context_recent_meta_window: int = 3
    context_alerts_slice: int = 10
    context_max_appearing_characters: int = 10
    context_max_urgent_foreshadowing: int = 5
    context_story_skeleton_interval: int = 20
    context_story_skeleton_max_samples: int = 5
    context_story_skeleton_snippet_chars: int = 400
    context_extra_section_budget: int = 800
    context_ranker_enabled: bool = True
    context_ranker_recency_weight: float = 0.7
    context_ranker_frequency_weight: float = 0.3
    context_ranker_hook_bonus: float = 0.2
    context_ranker_length_bonus_cap: float = 0.2
    context_ranker_alert_critical_keywords: tuple[str, ...] = (
        "conflict",
        "contradiction",
        "critical",
        "break",
        "violation",
        "rupture",
    )
    context_ranker_debug: bool = False
    context_reader_signal_enabled: bool = True
    context_reader_signal_recent_limit: int = 5
    context_reader_signal_window_chapters: int = 20
    context_reader_signal_review_window: int = 5
    context_reader_signal_include_debt: bool = False
    context_genre_profile_enabled: bool = True
    context_genre_profile_max_refs: int = 8
    context_genre_profile_fallback: str = "shuangwen"
    context_compact_text_enabled: bool = True
    context_compact_min_budget: int = 120
    context_compact_head_ratio: float = 0.65
    context_writing_guidance_enabled: bool = True
    context_writing_guidance_max_items: int = 6
    context_writing_guidance_low_score_threshold: float = 75.0
    context_writing_guidance_hook_diversify: bool = True
    context_methodology_enabled: bool = True
    context_methodology_genre_whitelist: tuple[str, ...] = ("*",)
    context_methodology_label: str = "digital-serial-v1"
    context_writing_checklist_enabled: bool = True
    context_writing_checklist_min_items: int = 3
    context_writing_checklist_max_items: int = 6
    context_writing_checklist_default_weight: float = 1.0
    context_writing_score_persist_enabled: bool = True
    context_writing_score_include_reader_trend: bool = True
    context_writing_score_trend_window: int = 10
    context_rag_assist_enabled: bool = True
    context_rag_assist_top_k: int = 4
    context_rag_assist_min_outline_chars: int = 40
    context_rag_assist_max_query_chars: int = 120
    context_dynamic_budget_enabled: bool = True
    context_dynamic_budget_early_chapter: int = 30
    context_dynamic_budget_late_chapter: int = 120
    context_dynamic_budget_early_core_bonus: float = 0.08
    context_dynamic_budget_early_scene_bonus: float = 0.04
    context_dynamic_budget_late_global_bonus: float = 0.08
    context_dynamic_budget_late_scene_penalty: float = 0.06
    context_template_weights_dynamic: dict[str, dict[str, dict[str, float]]] = field(
        default_factory=_default_context_template_weights_dynamic
    )
    context_genre_profile_support_composite: bool = True
    context_genre_profile_max_genres: int = 2
    context_genre_profile_separators: tuple[str, ...] = (
        "+",
        "/",
        "|",
        ",",
    )

    export_recent_changes_slice: int = 20
    export_disambiguation_slice: int = 20

    # ================= Query Default Limits =================
    query_recent_chapters_limit: int = 10
    query_scenes_by_location_limit: int = 20
    query_entity_appearances_limit: int = 50
    query_recent_appearances_limit: int = 20

    # ================= Foreshadowing Urgency =================
    foreshadowing_urgency_pending_high: int = 100
    foreshadowing_urgency_pending_medium: int = 50
    foreshadowing_urgency_target_proximity: int = 5
    foreshadowing_urgency_score_high: int = 100
    foreshadowing_urgency_score_medium: int = 60
    foreshadowing_urgency_score_target: int = 80
    foreshadowing_urgency_score_low: int = 20
    foreshadowing_urgency_threshold_show: int = 60

    foreshadowing_tier_weight_core: float = 3.0
    foreshadowing_tier_weight_sub: float = 2.0
    foreshadowing_tier_weight_decor: float = 1.0

    # ================= Character Activity =================
    character_absence_warning: int = 30
    character_absence_critical: int = 100
    character_candidates_limit: int = 800

    # ================= Strand Weave Rhythm =================
    strand_quest_max_consecutive: int = 5
    strand_fire_max_gap: int = 10
    strand_constellation_max_gap: int = 15

    strand_quest_ratio_min: int = 55
    strand_quest_ratio_max: int = 65
    strand_fire_ratio_min: int = 20
    strand_fire_ratio_max: int = 30
    strand_constellation_ratio_min: int = 10
    strand_constellation_ratio_max: int = 20

    # ================= Payoff Rhythm =================
    pacing_segment_size: int = 100
    pacing_words_per_point_excellent: int = 1000
    pacing_words_per_point_good: int = 1500
    pacing_words_per_point_acceptable: int = 2000

    # ================= RAG Storage =================
    @property
    def rag_db(self) -> Path:
        return self.webnovel_dir / "rag.db"

    @property
    def vector_db(self) -> Path:
        return self.webnovel_dir / "vectors.db"

    def ensure_dirs(self):
        self.webnovel_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def from_project_root(cls, project_root: str | Path) -> "DataModulesConfig":
        root = normalize_windows_path(project_root).expanduser().resolve()
        # Load project-level `.env` before constructing config to ensure EMBED_*/RERANK_* fields take effect
        _load_project_dotenv(root)
        return cls(project_root=root)


_default_config: Optional[DataModulesConfig] = None


def get_config(project_root: Optional[Path] = None) -> DataModulesConfig:
    global _default_config
    if project_root is not None:
        return DataModulesConfig.from_project_root(project_root)
    if _default_config is None:
        # By default, do not blindly use CWD as project_root (easily writes to wrong directory).
        # Use unified project_locator for auto-detection:
        # - Supports WEBNOVEL_PROJECT_ROOT
        # - Supports `.claude/.wordsmith-current-project` pointer file
        # - Supports searching for `.webnovel/state.json` from current/parent directories
        from project_locator import resolve_project_root

        root = resolve_project_root()
        _default_config = DataModulesConfig.from_project_root(root)
    return _default_config


def set_project_root(project_root: str | Path):
    global _default_config
    _default_config = DataModulesConfig.from_project_root(project_root)
