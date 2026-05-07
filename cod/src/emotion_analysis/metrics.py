from __future__ import annotations

from typing import Any

from .constants import EMOTIONS


"""Evaluation utilities independent of any specific model."""

def classification_metrics(
    gold_labels: list[str],
    predicted_labels: list[str],
    *,
    labels: tuple[str, ...] = EMOTIONS,
) -> dict[str, Any]:
    """Compute accuracy, macro-F1, per-label metrics and confusion matrix."""
    if len(gold_labels) != len(predicted_labels):
        raise ValueError("gold_labels and predicted_labels must have the same length.")

    confusion = confusion_matrix(gold_labels, predicted_labels, labels=labels)
    total = len(gold_labels)
    correct = sum(1 for gold, pred in zip(gold_labels, predicted_labels) if gold == pred)
    per_label: dict[str, dict[str, float | int]] = {}

    for label in labels:
        # One-vs-rest counts for each class.
        tp = confusion[label][label]
        fp = sum(confusion[other][label] for other in labels if other != label)
        fn = sum(confusion[label][other] for other in labels if other != label)
        support = sum(confusion[label].values())
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        per_label[label] = {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "support": support,
        }

    macro_f1 = sum(float(values["f1"]) for values in per_label.values()) / len(labels)
    return {
        "accuracy": round(correct / total, 4) if total else 0.0,
        "macro_f1": round(macro_f1, 4),
        "total": total,
        "per_label": per_label,
        "confusion": confusion,
    }


def confusion_matrix(
    gold_labels: list[str],
    predicted_labels: list[str],
    *,
    labels: tuple[str, ...] = EMOTIONS,
) -> dict[str, dict[str, int]]:
    """Build a gold-label by predicted-label confusion matrix."""
    label_set = set(labels)
    matrix = {gold: {pred: 0 for pred in labels} for gold in labels}
    for gold, predicted in zip(gold_labels, predicted_labels):
        if gold not in label_set or predicted not in label_set:
            continue
        matrix[gold][predicted] += 1
    return matrix


def label_distribution(labels: list[str]) -> dict[str, int]:
    """Count how many examples belong to each emotion label."""
    return {label: labels.count(label) for label in EMOTIONS}
