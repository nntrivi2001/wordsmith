#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genre alias normalization and profile key mapping.
"""

from __future__ import annotations


GENRE_INPUT_ALIASES: dict[str, str] = {
    "xianxia/fantasy": "xianxia",
    "fantasy-cultivation": "xianxia",
    "fantasy": "xianxia",
    "cultivation": "xianxia",
    "urban-cultivation": "urban-power",
    "urban-high-combat": "high-combat",
    "urban-oddities": "urban-brainhole",
    "ancient-brainhole": "ancient-romance",
    "gaming-esports": "esports",
    "esports-fiction": "esports",
    "livestream": "livestream-fiction",
    "livestream-selling": "livestream-fiction",
    "anchor": "livestream-fiction",
    "lovecraftian": "cosmic-horror",
    "lovecraftian-mystery": "cosmic-horror",
}


GENRE_PROFILE_KEY_ALIASES: dict[str, str] = {
    "xianxia": "xianxia",
    "xianxia/fantasy": "xianxia",
    "fantasy": "xianxia",
    "shuangwen/system-flow": "shuangwen",
    "high-combat": "xianxia",
    "western-fantasy": "xianxia",
    "urban-power": "urban-power",
    "urban-brainhole": "urban-power",
    "urban-daily": "urban-power",
    "dog-blood-romance": "romance",
    "ancient-romance": "romance",
    "youth-sweet": "romance",
    "substitute-fiction": "substitute",
    "rule-horror": "rules-mystery",
    "mystery-brainhole": "mystery",
    "mystery-supernatural": "mystery",
    "zhihu-short": "zhihu-short",
    "esports": "esports",
    "livestream-fiction": "livestream",
    "cosmic-horror": "cosmic-horror",
}


def normalize_genre_token(token: str) -> str:
    value = str(token or "").strip()
    if not value:
        return ""
    return GENRE_INPUT_ALIASES.get(value, value)


def to_profile_key(genre: str) -> str:
    value = str(genre or "").strip()
    if not value:
        return ""
    normalized = normalize_genre_token(value)
    return GENRE_PROFILE_KEY_ALIASES.get(normalized, normalized.lower())
