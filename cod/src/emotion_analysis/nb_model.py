"""Naive Bayes baseline trained from NRC hashtag emotion associations."""

from __future__ import annotations

import math
import random
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any, Iterable

from .constants import EMOTIONS
from .resources import LexiconEntry, load_hashtag_entries
from .text import tokenize


@dataclass
class TrainingExample:
    text: str
    label: str
    weight: float = 1.0


class NaiveBayesNotFittedError(RuntimeError):
    pass


class EmotionNaiveBayes:
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
        label_weights = {label: 0.0 for label in self.labels}

        for example in examples:
            if example.label not in self.class_feature_counts:
                continue

            feature_counts = count_emotion_token_features(example.text)
            if not feature_counts:
                continue

            weight = max(float(example.weight), 0.001)
            label_weights[example.label] += weight

            for feature, count in feature_counts.items():
                weighted_hits = count * weight
                self.class_feature_counts[example.label][feature] += weighted_hits
                self.class_totals[example.label] += weighted_hits
                self.vocabulary.add(feature)

        total_label_weight = sum(label_weights.values())
        if total_label_weight <= 0:
            raise ValueError("Cannot fit model: no usable training examples.")

        for label in self.labels:
            self.class_priors[label] = (
                label_weights[label] + self.alpha
            ) / (total_label_weight + self.alpha * len(self.labels))
        self._fitted = True
        return self

    def predict_proba(self, text: str) -> dict[str, float]:
        self._require_fitted()
        features = count_emotion_token_features(text)
        vocab_size = max(len(self.vocabulary), 1)
        log_scores: dict[str, float] = {}
        for label in self.labels:
            log_score = math.log(self.class_priors[label])
            denominator = self.class_totals[label] + self.alpha * vocab_size

            for feature, count in features.items():
                observed = self.class_feature_counts[label].get(feature, 0.0)

                probability = (observed + self.alpha) / denominator
                log_score += count * math.log(probability)
            log_scores[label] = log_score
        return normalize_log_emotion_scores(log_scores)

    def predict(self, text: str) -> dict[str, Any]:
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
            raise NaiveBayesNotFittedError(
                "Train EmotionNaiveBayes with fit() or train_nb_from_lexicon() before prediction."
            )


def train_nb_from_lexicon(
    lexicon_path: str | None = None,
    *,
    max_per_emotion: int = 3500,
    min_score: float = 0.3,
) -> EmotionNaiveBayes:
    entries = load_hashtag_entries(
        lexicon_path,
        max_entries_per_emotion=max_per_emotion,
        min_score=min_score,
    )
    examples = [
        nrc_entry_to_training_example(entry)
        for entry in entries
        if looks_like_training_phrase(entry.term)
    ]
    return EmotionNaiveBayes().fit(examples)


def evaluate_nb_from_lexicon(
    lexicon_path: str | None = None,
    *,
    max_per_emotion: int = 2500,
    min_score: float = 0.3,
    test_ratio: float = 0.2,
    seed: int = 13,
) -> dict[str, Any]:
    entries = [
        entry
        for entry in load_hashtag_entries(
            lexicon_path,
            max_entries_per_emotion=max_per_emotion,
            min_score=min_score,
        )
        if looks_like_training_phrase(entry.term)
    ]
    by_label: dict[str, list[LexiconEntry]] = defaultdict(list)
    for entry in entries:
        by_label[entry.emotion].append(entry)

    rng = random.Random(seed)
    train_examples: list[TrainingExample] = []
    test_examples: list[TrainingExample] = []

    for label in EMOTIONS:
        emotion_entries = by_label[label]
        rng.shuffle(emotion_entries)

        test_size = max(1, int(len(emotion_entries) * test_ratio))
        test_examples.extend(
            nrc_entry_to_training_example(entry) for entry in emotion_entries[:test_size]
        )
        train_examples.extend(
            nrc_entry_to_training_example(entry) for entry in emotion_entries[test_size:]
        )

    model = EmotionNaiveBayes().fit(train_examples)
    confusion = {gold: {pred: 0 for pred in EMOTIONS} for gold in EMOTIONS}
    correct = 0

    for example in test_examples:
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
        "examples": {"train": len(train_examples), "test": len(test_examples)},
        "accuracy": round(correct / max(len(test_examples), 1), 4),
        "macro_f1": round(macro_f1, 4),
        "per_label": per_label,
        "confusion": confusion,
    }


def count_emotion_token_features(text: str) -> Counter[str]:
    counts: Counter[str] = Counter()
    tokens = tokenize(text)

    for token in tokens:
        if token.startswith("#") and len(token) > 1:
            counts[f"word={token[1:]}"] += 1
        counts[f"word={token}"] += 2

        padded_token = f"^{token}$"

        for width in (3, 4, 5):
            last_start = len(padded_token) - width
            if last_start < 0:
                continue

            for start in range(last_start + 1):
                ngram = padded_token[start:start + width]
                counts[f"char{width}={ngram}"] += 1
    return counts


def nrc_entry_to_training_example(entry: LexiconEntry) -> TrainingExample:
    usable_score = min(max(entry.score, 0.0), 3.0)
    phrase = entry.term.replace("_", " ")
    return TrainingExample(text=phrase, label=entry.emotion, weight=1.0 + usable_score)


def looks_like_training_phrase(term: str) -> bool:
    if term.startswith("@") or "http" in term:
        return False
    letter_count = sum(ch.isalpha() for ch in term)
    return letter_count >= 3


def normalize_log_emotion_scores(log_scores: dict[str, float]) -> dict[str, float]:
    max_log = max(log_scores.values())
    shifted_scores = {
        label: math.exp(value - max_log)
        for label, value in log_scores.items()
    }
    total = sum(shifted_scores.values())
    return {label: value / total for label, value in shifted_scores.items()}
