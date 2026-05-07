"""Resolve and load the NRC Hashtag Emotion Lexicon used by the project."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from .constants import EMOTIONS
from .text import normalize_token


DEFAULT_LEXICON_RELATIVE = Path(
    "linkuri_extrase"
    "/archives"
    "/061_saifmohammad.com_NRC-Hashtag-Emotion-Lexicon-v0.2"
    "/NRC-Hashtag-Emotion-Lexicon-v0.2"
    "/NRC-Hashtag-Emotion-Lexicon-v0.2.txt"
)


@dataclass(frozen=True)
class LexiconEntry:
    emotion: str
    term: str
    score: float


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def workspace_root() -> Path:
    return project_root().parent


def default_lexicon_path() -> Path:
    env_path = os.environ.get("EMOTION_LEXICON_PATH")
    if env_path:
        return Path(env_path).expanduser()

    for root in (project_root(), workspace_root()):
        candidate = root / DEFAULT_LEXICON_RELATIVE
        if candidate.exists():
            return candidate
    return workspace_root() / DEFAULT_LEXICON_RELATIVE


def resolve_lexicon_path(path: str | Path | None = None) -> Path:
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
    entries = load_hashtag_entries(
        path,
        max_entries_per_emotion=max_entries_per_emotion,
        min_score=min_score,
    )
    lexicon = {emotion: {} for emotion in EMOTIONS}

    for entry in entries:
        previous_score = lexicon[entry.emotion].get(entry.term)
        if previous_score is None or entry.score > previous_score:
            lexicon[entry.emotion][entry.term] = entry.score
    return lexicon


def load_hashtag_entries(
    path: str | Path | None = None,
    *,
    max_entries_per_emotion: int | None = None,
    min_score: float | None = None,
) -> list[LexiconEntry]:
    lexicon_path = resolve_lexicon_path(path)
    kept_per_emotion = {emotion: 0 for emotion in EMOTIONS}
    entries: list[LexiconEntry] = []

    with lexicon_path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) != 3:
                continue
            emotion, raw_term, raw_score = parts
            if emotion not in kept_per_emotion:
                continue

            if (
                max_entries_per_emotion is not None
                and kept_per_emotion[emotion] >= max_entries_per_emotion
            ):
                continue
            try:
                score = float(raw_score)
            except ValueError:
                continue
            if min_score is not None and score < min_score:
                continue

            term = normalize_token(raw_term)
            if not term:
                continue
            entries.append(LexiconEntry(emotion=emotion, term=term, score=score))
            kept_per_emotion[emotion] += 1
    return entries
