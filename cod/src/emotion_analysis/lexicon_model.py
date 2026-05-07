"""Weighted NRC hashtag lexicon scorer used by the rule-based baseline."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from .constants import EMOTIONS
from .resources import load_hashtag_lexicon
from .text import has_recent_intensifier, has_recent_negation, token_variants, tokenize


@dataclass
class LexiconHit:
    emotion: str
    term: str
    token_index: int
    contribution: float


class WeightedEmotionLexicon:
    def __init__(
        self,
        lexicon: dict[str, dict[str, float]] | None = None,
        *,
        lexicon_path: str | None = None,
        max_entries_per_emotion: int | None = None,
    ) -> None:
        self.lexicon = lexicon or load_hashtag_lexicon(
            lexicon_path,
            max_entries_per_emotion=max_entries_per_emotion,
            min_score=0.0,
        )

    def score(self, text: str) -> dict[str, Any]:
        tokens = tokenize(text)
        emotion_totals = {emotion: 0.0 for emotion in EMOTIONS}
        lexicon_hits: list[LexiconHit] = []

        for index, token in enumerate(tokens):
            context_multiplier = recent_context_multiplier(tokens, index)

            checked_terms: set[str] = set()
            for term in token_variants(token):
                if term in checked_terms:
                    continue
                checked_terms.add(term)

                for emotion in EMOTIONS:
                    weight = self.lexicon[emotion].get(term)
                    if weight is None or weight <= 0:
                        continue
                    contribution = weight * context_multiplier
                    emotion_totals[emotion] += contribution
                    lexicon_hits.append(
                        LexiconHit(
                            emotion=emotion,
                            term=term,
                            token_index=index,
                            contribution=contribution,
                        )
                    )

        normalized = normalize_emotion_totals(emotion_totals)
        dominant = max(normalized, key=normalized.get) if normalized else None
        matched_positions = {hit.token_index for hit in lexicon_hits}
        coverage = len(matched_positions) / max(len(tokens), 1)
        return {
            "method": "lexicon",
            "text": text,
            "tokens": tokens,
            "raw_scores": emotion_totals,
            "scores": normalized,
            "dominant_emotion": dominant,
            "confidence": normalized.get(dominant, 0.0) if dominant else 0.0,
            "coverage": coverage,
            "matches": summarize_lexicon_hits(lexicon_hits),
        }


def recent_context_multiplier(tokens: list[str], token_index: int) -> float:
    multiplier = 1.0
    if has_recent_negation(tokens, token_index):
        multiplier *= 0.35
    if has_recent_intensifier(tokens, token_index):
        multiplier *= 1.35
    return multiplier


def normalize_emotion_totals(emotion_totals: dict[str, float]) -> dict[str, float]:
    positive_scores = {
        emotion: max(score, 0.0)
        for emotion, score in emotion_totals.items()
    }
    total = sum(positive_scores.values())
    if total <= 0:
        return {emotion: 0.0 for emotion in EMOTIONS}
    return {
        emotion: score / total
        for emotion, score in positive_scores.items()
    }


def summarize_lexicon_hits(
    hits: list[LexiconHit],
    limit: int = 12,
) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], float] = defaultdict(float)
    for hit in hits:
        grouped[(hit.emotion, hit.term)] += hit.contribution

    ranked_hits = sorted(grouped.items(), key=lambda group: group[1], reverse=True)
    return [
        {"emotion": emotion, "term": term, "contribution": round(contribution, 4)}
        for (emotion, term), contribution in ranked_hits[:limit]
    ]
