"""High-level analyzer for lexicon, NB and hybrid emotion prediction."""

from __future__ import annotations

from typing import Any

from .constants import EMOTIONS
from .lexicon_model import WeightedEmotionLexicon
from .nb_model import EmotionNaiveBayes, train_nb_from_lexicon


class EmotionAnalyzer:
    def __init__(
        self,
        *,
        lexicon_path: str | None = None,
        lexicon_max_entries: int | None = None,
        nb_max_per_emotion: int = 3500,
        hybrid_lexicon_weight: float = 0.85,
        lexicon_model: WeightedEmotionLexicon | None = None,
        nb_model: EmotionNaiveBayes | None = None,
    ) -> None:
        if not 0.0 <= hybrid_lexicon_weight <= 1.0:
            raise ValueError("hybrid_lexicon_weight must be between 0 and 1.")

        self.lexicon_model = lexicon_model or WeightedEmotionLexicon(
            lexicon_path=lexicon_path, max_entries_per_emotion=lexicon_max_entries
        )
        self.nb_model = nb_model
        self.lexicon_path = lexicon_path
        self.nb_max_per_emotion = nb_max_per_emotion
        self.hybrid_lexicon_weight = hybrid_lexicon_weight

    def analyze(self, text: str, *, method: str = "hybrid") -> dict[str, Any]:
        method = method.lower()
        if method == "lexicon":
            return self.lexicon_model.score(text)
        if method == "nb":
            return self._nb_model().predict(text)
        if method != "hybrid":
            raise ValueError("method must be one of: lexicon, nb, hybrid")

        lexicon_result = self.lexicon_model.score(text)
        nb_result = self._nb_model().predict(text)
        lexicon_share = self.hybrid_lexicon_weight
        nb_share = 1.0 - lexicon_share
        scores = {
            emotion: lexicon_share * lexicon_result["scores"][emotion]
            + nb_share * nb_result["scores"][emotion]
            for emotion in EMOTIONS
        }
        dominant = max(scores, key=scores.get)
        return {
            "method": "hybrid",
            "text": text,
            "tokens": lexicon_result["tokens"],
            "scores": scores,
            "dominant_emotion": dominant,
            "confidence": scores[dominant],
            "coverage": lexicon_result["coverage"],
            "matches": lexicon_result["matches"],
            "components": {
                "lexicon": lexicon_result["scores"],
                "nb": nb_result["scores"],
                "hybrid_lexicon_weight": lexicon_share,
            },
        }

    def _nb_model(self) -> EmotionNaiveBayes:
        if self.nb_model is None:
            self.nb_model = train_nb_from_lexicon(
                self.lexicon_path,
                max_per_emotion=self.nb_max_per_emotion,
            )
        return self.nb_model
