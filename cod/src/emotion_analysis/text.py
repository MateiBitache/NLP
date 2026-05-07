from __future__ import annotations

import re
from typing import Iterable


"""Text normalization helpers shared by lexical and learned models."""

# URL removal avoids giving random links emotional meaning.
URL_RE = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)

# The tokenizer keeps hashtags because the NRC Hashtag Emotion Lexicon contains them.
TOKEN_RE = re.compile(r"#?[\w][\w'_-]*|[!?]+", re.UNICODE)
REPEATED_CHAR_RE = re.compile(r"(.)\1{2,}")

# Small rule lists used by the lexicon baseline.
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
    """Lowercase text and remove URLs before tokenization."""
    text = URL_RE.sub(" URL ", text)
    return text.lower()


def normalize_token(token: str) -> str:
    """Normalize a token while keeping useful forms such as hashtags."""
    token = token.strip().lower()
    token = token.strip("\"'.,;:()[]{}")
    token = REPEATED_CHAR_RE.sub(r"\1\1", token)
    return token


def tokenize(text: str) -> list[str]:
    """Return normalized tokens used by both baselines."""
    normalized = normalize_text(text)
    tokens: list[str] = []
    for match in TOKEN_RE.finditer(normalized):
        token = normalize_token(match.group(0))
        if not token or token == "url":
            continue
        tokens.append(token)
    return tokens


def token_variants(token: str) -> Iterable[str]:
    """Yield lookup variants, e.g. both '#happy' and 'happy'."""
    yield token
    if token.startswith("#") and len(token) > 1:
        yield token[1:]
    if token.endswith("'s") and len(token) > 3:
        yield token[:-2]


def has_recent_negation(tokens: list[str], index: int, window: int = 3) -> bool:
    """Check whether a token is under a short negation window."""
    start = max(0, index - window)
    return any(tokens[i] in NEGATIONS for i in range(start, index))


def has_recent_intensifier(tokens: list[str], index: int, window: int = 2) -> bool:
    """Check whether a token is preceded by a simple intensifier."""
    start = max(0, index - window)
    return any(tokens[i] in INTENSIFIERS for i in range(start, index))
