from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from .constants import EMOTIONS
from .resources import load_hashtag_lexicon
from .text import has_recent_intensifier, has_recent_negation, token_variants, tokenize


"""Classic emotion detection baseline based on weighted lexicon lookup."""

@dataclass
class Match:
    """A single lexical match that explains part of an emotion score."""

    emotion: str
    term: str
    token_index: int
    contribution: float


class WeightedEmotionLexicon:
    """Classic lexicon baseline using weighted NRC hashtag emotion associations."""

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
        """Score one text and return normalized emotion probabilities plus evidence."""
        tokens = tokenize(text)
        raw_scores = {emotion: 0.0 for emotion in EMOTIONS}
        matches: list[Match] = []

        for index, token in enumerate(tokens):
            multiplier = 1.0

            # Negation and intensifiers are simple heuristics, not full syntax parsing.
            if has_recent_negation(tokens, index):
                multiplier *= 0.35
            if has_recent_intensifier(tokens, index):
                multiplier *= 1.35

            seen_terms: set[str] = set()
            for term in token_variants(token):
                if term in seen_terms:
                    continue
                seen_terms.add(term)

                # A term can contribute to several emotions in the NRC resource.
                for emotion in EMOTIONS:
                    weight = self.lexicon[emotion].get(term)
                    if weight is None or weight <= 0:
                        continue
                    contribution = weight * multiplier
                    raw_scores[emotion] += contribution
                    matches.append(
                        Match(
                            emotion=emotion,
                            term=term,
                            token_index=index,
                            contribution=contribution,
                        )
                    )

        normalized = normalize_scores(raw_scores)
        dominant = max(normalized, key=normalized.get) if normalized else None
        coverage = len({match.token_index for match in matches}) / max(len(tokens), 1)
        return {
            "method": "lexicon",
            "text": text,
            "tokens": tokens,
            "raw_scores": raw_scores,
            "scores": normalized,
            "dominant_emotion": dominant,
            "confidence": normalized.get(dominant, 0.0) if dominant else 0.0,
            "coverage": coverage,
            "matches": summarize_matches(matches),
        }


def normalize_scores(scores: dict[str, float]) -> dict[str, float]:
    """Convert raw positive scores to a distribution over emotions."""
    positive = {emotion: max(value, 0.0) for emotion, value in scores.items()}
    total = sum(positive.values())
    if total <= 0:
        return {emotion: 0.0 for emotion in EMOTIONS}
    return {emotion: value / total for emotion, value in positive.items()}


def summarize_matches(matches: list[Match], limit: int = 12) -> list[dict[str, Any]]:
    """Group repeated matches so CLI/CSV evidence stays readable."""
    grouped: dict[tuple[str, str], float] = defaultdict(float)
    for match in matches:
        grouped[(match.emotion, match.term)] += match.contribution
    ranked = sorted(grouped.items(), key=lambda item: item[1], reverse=True)
    return [
        {"emotion": emotion, "term": term, "contribution": round(score, 4)}
        for (emotion, term), score in ranked[:limit]
    ]
