"""Loads the knowledge base and finds risk factors mentioned in free text."""

import json
import re
from pathlib import Path
from typing import Any

from app.agent.text import normalize

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_BASE_PATH = BASE_DIR / "knowledge_base.json"


def load_knowledge_base(path: Path = KNOWLEDGE_BASE_PATH) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


KNOWLEDGE_BASE: dict[str, Any] = load_knowledge_base()
FACTOR_DETAILS: dict[str, dict[str, Any]] = KNOWLEDGE_BASE["factor_details"]


def _compile_factor_patterns(details: dict[str, dict[str, Any]]) -> dict[str, re.Pattern]:
    patterns: dict[str, re.Pattern] = {}
    for key, entry in details.items():
        names = {normalize(entry["label"])} | {normalize(a) for a in entry["aliases"]}
        # Longest first so "number of diagnoses" wins over "diagnoses".
        ordered = sorted(names, key=len, reverse=True)
        patterns[key] = re.compile(r"\b(?:" + "|".join(re.escape(n) for n in ordered) + r")\b")
    return patterns


_FACTOR_PATTERNS = _compile_factor_patterns(FACTOR_DETAILS)


def find_factor_mentions(text: str) -> list[tuple[int, str]]:
    """Return (position, factor_key) for every known factor named in `text`."""
    normalized = normalize(text)
    mentions = []
    for key, pattern in _FACTOR_PATTERNS.items():
        match = pattern.search(normalized)
        if match:
            mentions.append((match.start(), key))
    return sorted(mentions)
