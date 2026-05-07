from __future__ import annotations

from typing import Any

from .constants import EMOTIONS
from .lexicon_model import WeightedEmotionLexicon
from .nb_model import EmotionNaiveBayes, train_nb_from_lexicon


"""High-level analyzer that exposes lexicon, NB and hybrid methods."""

class EmotionAnalyzer:
    """Facade used by the CLI and experiments to run emotion analysis."""

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

        # Model injection is used by tests; normal CLI usage loads models from resources.
        self.lexicon_model = lexicon_model or WeightedEmotionLexicon(
            lexicon_path=lexicon_path, max_entries_per_emotion=lexicon_max_entries
        )
        self.nb_model = nb_model
        self.lexicon_path = lexicon_path
        self.nb_max_per_emotion = nb_max_per_emotion
        self.hybrid_lexicon_weight = hybrid_lexicon_weight

    def analyze(self, text: str, *, method: str = "hybrid") -> dict[str, Any]:
        """Run the selected method on a single text."""
        method = method.lower()
        if method == "lexicon":
            return self.lexicon_model.score(text)
        if method == "nb":
            return self._nb().predict(text)
        if method != "hybrid":
            raise ValueError("method must be one of: lexicon, nb, hybrid")

        # Hybrid keeps the interpretable lexical signal and adds the learned NB signal.
        lexicon_result = self.lexicon_model.score(text)
        nb_result = self._nb().predict(text)
        weight = self.hybrid_lexicon_weight
        scores = {
            emotion: weight * lexicon_result["scores"][emotion]
            + (1.0 - weight) * nb_result["scores"][emotion]
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
                "hybrid_lexicon_weight": weight,
            },
        }

    def _nb(self) -> EmotionNaiveBayes:
        """Train NB lazily so lexicon-only commands start quickly."""
        if self.nb_model is None:
            self.nb_model = train_nb_from_lexicon(
                self.lexicon_path,
                max_per_emotion=self.nb_max_per_emotion,
            )
        return self.nb_model
