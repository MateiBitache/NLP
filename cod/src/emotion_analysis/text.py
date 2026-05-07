"""Text cleanup shared by the lexicon and NB baselines."""

from __future__ import annotations

import re
from typing import Iterable


URL_PATTERN = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
TOKEN_PATTERN = re.compile(r"#?[\w][\w'_-]*|[!?]+", re.UNICODE)
LONG_CHAR_RUN = re.compile(r"(.)\1{2,}")

NEGATIONS = {
    "no",
    "not",
    "never",
    "none",
    "nobody",
    "nothing",
    "nowhere",
    "cannot",
    "can't",
    "dont",
    "don't",
    "isnt",
    "isn't",
    "wasnt",
    "wasn't",
    "nu",
    "niciodata",
    "nimic",
    "nimeni",
}

INTENSIFIERS = {
    "very",
    "really",
    "extremely",
    "so",
    "too",
    "absolutely",
    "completely",
    "foarte",
    "super",
    "extrem",
}


def normalize_text(text: str) -> str:
    without_links = URL_PATTERN.sub(" URL ", text)
    return without_links.lower()


def normalize_token(token: str) -> str:
    token = token.strip().lower()
    token = token.strip("\"'.,;:()[]{}")
    return LONG_CHAR_RUN.sub(r"\1\1", token)


def tokenize(text: str) -> list[str]:
    normalized = normalize_text(text)
    tokens: list[str] = []
    for match in TOKEN_PATTERN.finditer(normalized):
        token = normalize_token(match.group(0))
        if not token or token == "url":
            continue
        tokens.append(token)
    return tokens


def token_variants(token: str) -> Iterable[str]:
    yield token
    if token.startswith("#") and len(token) > 1:
        yield token[1:]
    if token.endswith("'s") and len(token) > 3:
        yield token[:-2]


def has_recent_negation(tokens: list[str], index: int, window: int = 3) -> bool:
    start = max(0, index - window)
    recent_tokens = tokens[start:index]
    return any(token in NEGATIONS for token in recent_tokens)


def has_recent_intensifier(tokens: list[str], index: int, window: int = 2) -> bool:
    start = max(0, index - window)
    recent_tokens = tokens[start:index]
    return any(token in INTENSIFIERS for token in recent_tokens)
