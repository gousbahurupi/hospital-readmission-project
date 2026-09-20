"""Text normalisation shared by the intent rules and the factor lookup."""

import re

_APOSTROPHES = re.compile(r"[’'`]")
_SEPARATORS = re.compile(r"[-_/]")
_NOT_WORD = re.compile(r"[^\w\s]")
_SPACES = re.compile(r"\s+")


def normalize(text: str) -> str:
    """Lower-case a question and strip punctuation so patterns stay simple.

    "What's the 72% risk?" -> "whats the 72 percent risk"
    "Follow-up"            -> "follow up"
    """
    text = text.lower()
    text = _APOSTROPHES.sub("", text)
    text = text.replace("%", " percent ")
    text = _SEPARATORS.sub(" ", text)
    text = _NOT_WORD.sub(" ", text)
    return _SPACES.sub(" ", text).strip()
