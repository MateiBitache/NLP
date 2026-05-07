from __future__ import annotations

import math
import random
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any, Iterable

from .constants import EMOTIONS
from .resources import LexiconEntry, load_hashtag_entries
from .text import tokenize


"""Weakly supervised Naive Bayes model for emotion classification."""

@dataclass
class TrainingExample:
    """One training item for the Naive Bayes baseline."""

    text: str
    label: str
    weight: float = 1.0


class EmotionNaiveBayes:
    """A lightweight learned baseline trained from emotion-labeled lexical items."""

    def __init__(self, *, alpha: float = 0.5) -> None:
        self.alpha = alpha
        self.labels = list(EMOTIONS)
        self.vocabulary: set[str] = set()
        self.class_feature_counts: dict[str, Counter[str]] = {
            label: Counter() for label in self.labels
        }
        self.class_totals = {label: 0.0 for label in self.labels}
        self.class_priors = {label: 0.0 for label in self.labels}
        self._fitted = False

    def fit(self, examples: Iterable[TrainingExample]) -> "EmotionNaiveBayes":
        """Estimate class priors and feature likelihoods from weighted examples."""
        class_weights = {label: 0.0 for label in self.labels}
        for example in examples:
            if example.label not in self.class_feature_counts:
                continue
            features = extract_features(example.text)
            if not features:
                continue
            weight = max(float(example.weight), 0.001)
            class_weights[example.label] += weight
            for feature, count in features.items():
                # Weighted counts let stronger lexicon associations influence training more.
                weighted_count = count * weight
                self.class_feature_counts[example.label][feature] += weighted_count
                self.class_totals[example.label] += weighted_count
                self.vocabulary.add(feature)

        total_class_weight = sum(class_weights.values())
        if total_class_weight <= 0:
            raise ValueError("Cannot fit model: no usable training examples.")
        for label in self.labels:
            self.class_priors[label] = (
                class_weights[label] + self.alpha
            ) / (total_class_weight + self.alpha * len(self.labels))
        self._fitted = True
        return self

    def predict_proba(self, text: str) -> dict[str, float]:
        """Return a probability distribution over the eight emotions."""
        self._require_fitted()
        features = extract_features(text)
        vocab_size = max(len(self.vocabulary), 1)
        log_scores: dict[str, float] = {}
        for label in self.labels:
            log_score = math.log(self.class_priors[label])
            denominator = self.class_totals[label] + self.alpha * vocab_size
            for feature, count in features.items():
                observed = self.class_feature_counts[label].get(feature, 0.0)

                # Additive smoothing keeps unseen features from producing zero probability.
                probability = (observed + self.alpha) / denominator
                log_score += count * math.log(probability)
            log_scores[label] = log_score
        return softmax(log_scores)

    def predict(self, text: str) -> dict[str, Any]:
        """Return the dominant emotion and all emotion scores for one text."""
        scores = self.predict_proba(text)
        dominant = max(scores, key=scores.get)
        return {
            "method": "nb",
            "text": text,
            "tokens": tokenize(text),
            "scores": scores,
            "dominant_emotion": dominant,
            "confidence": scores[dominant],
        }

    def _require_fitted(self) -> None:
        if not self._fitted:
            raise RuntimeError("EmotionNaiveBayes must be fitted before prediction.")


def train_nb_from_lexicon(
    lexicon_path: str | None = None,
    *,
    max_per_emotion: int = 3500,
    min_score: float = 0.3,
) -> EmotionNaiveBayes:
    """Build the learned baseline directly from the NRC lexicon."""
    entries = load_hashtag_entries(
        lexicon_path,
        max_entries_per_emotion=max_per_emotion,
        min_score=min_score,
    )
    examples = [entry_to_example(entry) for entry in entries if is_training_term(entry.term)]
    return EmotionNaiveBayes().fit(examples)


def evaluate_nb_from_lexicon(
    lexicon_path: str | None = None,
    *,
    max_per_emotion: int = 2500,
    min_score: float = 0.3,
    test_ratio: float = 0.2,
    seed: int = 13,
) -> dict[str, Any]:
    """Evaluate NB with a deterministic held-out split from the lexicon."""
    entries = [
        entry
        for entry in load_hashtag_entries(
            lexicon_path,
            max_entries_per_emotion=max_per_emotion,
            min_score=min_score,
        )
        if is_training_term(entry.term)
    ]
    by_label: dict[str, list[LexiconEntry]] = defaultdict(list)
    for entry in entries:
        by_label[entry.emotion].append(entry)

    rng = random.Random(seed)
    train: list[TrainingExample] = []
    test: list[TrainingExample] = []
    for label in EMOTIONS:
        label_entries = by_label[label]
        rng.shuffle(label_entries)

        # Split each emotion separately so every class appears in train and test.
        split = max(1, int(len(label_entries) * test_ratio))
        test.extend(entry_to_example(entry) for entry in label_entries[:split])
        train.extend(entry_to_example(entry) for entry in label_entries[split:])

    model = EmotionNaiveBayes().fit(train)
    confusion = {gold: {pred: 0 for pred in EMOTIONS} for gold in EMOTIONS}
    correct = 0
    for example in test:
        probabilities = model.predict_proba(example.text)
        prediction = max(probabilities, key=probabilities.get)
        confusion[example.label][prediction] += 1
        correct += int(prediction == example.label)

    per_label = {}
    for label in EMOTIONS:
        tp = confusion[label][label]
        fp = sum(confusion[other][label] for other in EMOTIONS if other != label)
        fn = sum(confusion[label][other] for other in EMOTIONS if other != label)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        per_label[label] = {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "support": sum(confusion[label].values()),
        }
    macro_f1 = sum(metrics["f1"] for metrics in per_label.values()) / len(EMOTIONS)
    return {
        "examples": {"train": len(train), "test": len(test)},
        "accuracy": round(correct / max(len(test), 1), 4),
        "macro_f1": round(macro_f1, 4),
        "per_label": per_label,
        "confusion": confusion,
    }


def extract_features(text: str) -> Counter[str]:
    """Extract word and character n-gram features for robust short-text matching."""
    features: Counter[str] = Counter()
    tokens = tokenize(text)
    for token in tokens:
        if token.startswith("#") and len(token) > 1:
            features[f"word={token[1:]}"] += 1
        features[f"word={token}"] += 2
        compact = f"^{token}$"

        # Character n-grams help with related word forms, typos and hashtags.
        for n in (3, 4, 5):
            if len(compact) < n:
                continue
            for index in range(0, len(compact) - n + 1):
                features[f"char{n}={compact[index:index+n]}"] += 1
    return features


def entry_to_example(entry: LexiconEntry) -> TrainingExample:
    """Convert a lexical association into a weakly supervised training example."""
    weight = 1.0 + min(max(entry.score, 0.0), 3.0)
    return TrainingExample(text=entry.term.replace("_", " "), label=entry.emotion, weight=weight)


def is_training_term(term: str) -> bool:
    """Filter noisy social-media artifacts that are not useful as training text."""
    if term.startswith("@") or "http" in term:
        return False
    letters = sum(ch.isalpha() for ch in term)
    return letters >= 3


def softmax(log_scores: dict[str, float]) -> dict[str, float]:
    """Normalize log-scores in a numerically stable way."""
    max_log = max(log_scores.values())
    exps = {label: math.exp(value - max_log) for label, value in log_scores.items()}
    total = sum(exps.values())
    return {label: value / total for label, value in exps.items()}
