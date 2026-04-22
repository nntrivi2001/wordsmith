#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Query router for RAG requests."""
from __future__ import annotations

import re
from typing import Any, Dict, List


class QueryRouter:
    def __init__(self):
        self.intent_patterns = {
            "relationship": [r"relationship", r"relations", r"timeline", r"who_with_whom", r"hostile", r"ally", r"allies"],
            "entity": [r"character", r"role", r"who", r"identity", r"alias"],
            "scene": [r"location", r"scene", r"where", r"place", r"position"],
            "setting": [r"setting", r"rules", r"system", r"world"],
            "plot": [r"plot", r"happen", r"event", r"happenings"],
        }
        self.patterns = {
            "entity": list(self.intent_patterns["entity"]),
            "scene": list(self.intent_patterns["scene"]),
            "setting": list(self.intent_patterns["setting"]),
            "plot": list(self.intent_patterns["plot"]),
        }

    def _extract_entities(self, query: str) -> List[str]:
        # Lightweight heuristic extraction: extract Chinese phrases of length 2-6, filtering common query words
        candidates = re.findall(r"[\u4e00-\u9fff]{2,6}", query)
        stopwords = {
            "relationship",
            "relations",
            "timeline",
            "plot",
            "happen",
            "event",
            "character",
            "role",
            "setting",
            "world",
            "location",
            "scene",
        }
        entities: List[str] = []
        for c in candidates:
            if c in stopwords:
                continue
            if c not in entities:
                entities.append(c)
        return entities[:4]

    def _extract_time_scope(self, query: str) -> Dict[str, Any]:
        m_range = re.search(r"Chapter\s*(\d+)\s*[-~to]+\s*(\d+)\s*(?:Chapter|Ch)", query)
        if m_range:
            start = int(m_range.group(1))
            end = int(m_range.group(2))
            if start > end:
                start, end = end, start
            return {"from_chapter": start, "to_chapter": end}

        m_single = re.search(r"Chapter\s*(\d+)", query)
        if m_single:
            chapter = int(m_single.group(1))
            return {"from_chapter": chapter, "to_chapter": chapter}

        return {}

    def route_intent(self, query: str) -> Dict[str, Any]:
        query = str(query or "")
        intent = "plot"
        for intent_name, patterns in self.intent_patterns.items():
            if any(re.search(pat, query) for pat in patterns):
                intent = intent_name
                break

        time_scope = self._extract_time_scope(query)
        entities = self._extract_entities(query)
        needs_graph = intent == "relationship" or "relationship" in query or "relations" in query
        return {
            "intent": intent,
            "entities": entities,
            "time_scope": time_scope,
            "needs_graph": needs_graph,
            "raw_query": query,
        }

    def plan_subqueries(self, intent_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        intent = str((intent_payload or {}).get("intent") or "plot")
        entities = list((intent_payload or {}).get("entities") or [])
        time_scope = dict((intent_payload or {}).get("time_scope") or {})
        needs_graph = bool((intent_payload or {}).get("needs_graph"))

        steps: List[Dict[str, Any]] = []
        if intent == "relationship":
            steps.append(
                {
                    "name": "relationship_graph",
                    "strategy": "graph_lookup",
                    "entities": entities,
                    "time_scope": time_scope,
                }
            )
            steps.append(
                {
                    "name": "relationship_evidence",
                    "strategy": "graph_hybrid",
                    "entities": entities,
                    "time_scope": time_scope,
                }
            )
            return steps

        if needs_graph and entities:
            steps.append(
                {
                    "name": "graph_enhanced_retrieval",
                    "strategy": "graph_hybrid",
                    "entities": entities,
                    "time_scope": time_scope,
                }
            )
            return steps

        strategy_map = {
            "entity": "hybrid",
            "scene": "bm25",
            "setting": "bm25",
            "plot": "hybrid",
        }
        steps.append(
            {
                "name": "default_retrieval",
                "strategy": strategy_map.get(intent, "hybrid"),
                "entities": entities,
                "time_scope": time_scope,
            }
        )
        return steps

    def route(self, query: str) -> str:
        return str(self.route_intent(query).get("intent") or "plot")

    def split(self, query: str) -> List[str]:
        parts = re.split(r"[,,;and\s]+\s*", query)
        return [p.strip() for p in parts if p.strip()]
