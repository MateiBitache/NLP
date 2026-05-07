from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from .constants import EMOTIONS
from .text import normalize_token


"""Loading and path resolution for the local NRC Hashtag Emotion Lexicon."""

# The large downloaded resources stay outside rezolvari, so the loader checks both
# rezolvari/linkuri_extrase and ../linkuri_extrase.
DEFAULT_LEXICON_RELATIVE = Path(
    "linkuri_extrase"
    "/archives"
    "/061_saifmohammad.com_NRC-Hashtag-Emotion-Lexicon-v0.2"
    "/NRC-Hashtag-Emotion-Lexicon-v0.2"
    "/NRC-Hashtag-Emotion-Lexicon-v0.2.txt"
)


@dataclass(frozen=True)
class LexiconEntry:
    """One row from the NRC Hashtag Emotion Lexicon."""

    emotion: str
    term: str
    score: float


def project_root() -> Path:
    """Return the rezolvari folder when code is imported from src/."""
    return Path(__file__).resolve().parents[2]


def workspace_root() -> Path:
    """Return the parent workspace that contains linkuri_extrase."""
    return project_root().parent


def default_lexicon_path() -> Path:
    """Find the default NRC lexicon path without requiring a CLI argument."""
    env_path = os.environ.get("EMOTION_LEXICON_PATH")
    if env_path:
        return Path(env_path).expanduser()
    for root in (project_root(), workspace_root()):
        candidate = root / DEFAULT_LEXICON_RELATIVE
        if candidate.exists():
            return candidate
    return workspace_root() / DEFAULT_LEXICON_RELATIVE


def resolve_lexicon_path(path: str | Path | None = None) -> Path:
    """Resolve user-provided or default lexicon paths and fail clearly."""
    candidate = Path(path).expanduser() if path else default_lexicon_path()
    if not candidate.is_absolute():
        for root in (project_root(), workspace_root()):
            rooted = root / candidate
            if rooted.exists():
                candidate = rooted
                break
        else:
            candidate = project_root() / candidate
    if not candidate.exists():
        raise FileNotFoundError(
            "Emotion lexicon not found. Expected NRC Hashtag Emotion Lexicon at "
            f"{candidate}. Pass --lexicon PATH or set EMOTION_LEXICON_PATH."
        )
    return candidate


def load_hashtag_lexicon(
    path: str | Path | None = None,
    *,
    max_entries_per_emotion: int | None = None,
    min_score: float | None = None,
) -> dict[str, dict[str, float]]:
    """Load entries grouped as emotion -> term -> score."""
    entries = load_hashtag_entries(
        path,
        max_entries_per_emotion=max_entries_per_emotion,
        min_score=min_score,
    )
    lexicon = {emotion: {} for emotion in EMOTIONS}
    for entry in entries:
        current = lexicon[entry.emotion].get(entry.term)
        if current is None or entry.score > current:
            lexicon[entry.emotion][entry.term] = entry.score
    return lexicon


def load_hashtag_entries(
    path: str | Path | None = None,
    *,
    max_entries_per_emotion: int | None = None,
    min_score: float | None = None,
) -> list[LexiconEntry]:
    """Read the NRC TSV file and keep only usable emotion entries."""
    lexicon_path = resolve_lexicon_path(path)
    counters = {emotion: 0 for emotion in EMOTIONS}
    entries: list[LexiconEntry] = []
    with lexicon_path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) != 3:
                continue
            emotion, raw_term, raw_score = parts
            if emotion not in counters:
                continue

            # Limit entries per emotion for fast experiments/tests when requested.
            if max_entries_per_emotion is not None and counters[emotion] >= max_entries_per_emotion:
                continue
            try:
                score = float(raw_score)
            except ValueError:
                continue
            if min_score is not None and score < min_score:
                continue

            # Normalize lexicon terms exactly like text tokens for consistent lookup.
            term = normalize_token(raw_term)
            if not term:
                continue
            entries.append(LexiconEntry(emotion=emotion, term=term, score=score))
            counters[emotion] += 1
    return entries
