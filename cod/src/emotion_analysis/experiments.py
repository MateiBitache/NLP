"""Experiment runner for final-project metrics and artifacts."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from .constants import EMOTIONS
from .io import flatten_prediction, read_text_rows
from .metrics import classification_metrics, label_distribution
from .pipeline import EmotionAnalyzer
from .visualization import write_distribution_svg


DEFAULT_METHODS = ("lexicon", "nb", "hybrid")


def run_experiment_suite(
    *,
    input_path: str | Path = "data/final_eval_texts.csv",
    output_dir: str | Path = "outputs/final_experiment",
    text_column: str = "text",
    label_column: str = "label",
    domain_column: str = "domain",
    methods: tuple[str, ...] = DEFAULT_METHODS,
    lexicon_path: str | None = None,
    hybrid_lexicon_weight: float = 0.85,
    analyzer: EmotionAnalyzer | None = None,
) -> dict[str, Any]:
    dataset_rows = read_text_rows(input_path, text_column=text_column)
    validate_labeled_rows(dataset_rows, label_column=label_column)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    analyzer = analyzer or EmotionAnalyzer(
        lexicon_path=lexicon_path,
        hybrid_lexicon_weight=hybrid_lexicon_weight,
    )
    experiment_summary: dict[str, Any] = {
        "dataset": str(input_path),
        "rows": len(dataset_rows),
        "hybrid_lexicon_weight": hybrid_lexicon_weight,
        "methods": {},
    }

    gold_labels = [row[label_column] for row in dataset_rows]
    experiment_summary["gold_distribution"] = label_distribution(gold_labels)

    write_distribution_csv(output_path / "gold_distribution.csv", experiment_summary["gold_distribution"])
    write_distribution_svg(
        output_path / "gold_distribution.svg",
        experiment_summary["gold_distribution"],
        title="Gold emotion distribution",
    )

    comparison_rows: list[dict[str, Any]] = []
    for method in methods:
        method_predictions: list[dict[str, Any]] = []
        predicted_labels: list[str] = []

        for row in dataset_rows:
            prediction = analyzer.analyze(row[text_column], method=method)
            predicted_labels.append(prediction["dominant_emotion"])
            prediction_row = flatten_prediction(row, prediction)
            prediction_row[label_column] = row[label_column]
            if domain_column in row:
                prediction_row[domain_column] = row[domain_column]
            method_predictions.append(prediction_row)

        metrics = classification_metrics(gold_labels, predicted_labels)
        distribution = label_distribution(predicted_labels)
        experiment_summary["methods"][method] = {
            "metrics": metrics,
            "predicted_distribution": distribution,
            "domain_metrics": domain_metrics(
                dataset_rows,
                predicted_labels,
                label_column,
                domain_column,
            ),
        }
        comparison_rows.append(
            {
                "method": method,
                "accuracy": metrics["accuracy"],
                "macro_f1": metrics["macro_f1"],
                "total": metrics["total"],
            }
        )

        write_prediction_rows_flexible(output_path / f"predictions_{method}.csv", method_predictions)
        write_confusion_csv(output_path / f"confusion_{method}.csv", metrics["confusion"])
        write_distribution_csv(output_path / f"predicted_distribution_{method}.csv", distribution)
        write_distribution_svg(
            output_path / f"predicted_distribution_{method}.svg",
            distribution,
            title=f"Predicted emotion distribution - {method}",
        )

    write_comparison_csv(output_path / "method_comparison.csv", comparison_rows)
    write_domain_metrics_csv(output_path / "domain_metrics.csv", experiment_summary)
    (output_path / "metrics.json").write_text(
        json.dumps(experiment_summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return experiment_summary


def validate_labeled_rows(rows: list[dict[str, str]], *, label_column: str) -> None:
    if not rows:
        raise ValueError("Experiment dataset is empty.")

    bad_labels = sorted(
        {
            row.get(label_column, "")
            for row in rows
            if row.get(label_column) not in EMOTIONS
        }
    )
    if bad_labels:
        raise ValueError(f"Invalid labels in dataset: {', '.join(bad_labels)}")


def domain_metrics(
    rows: list[dict[str, str]],
    predicted_labels: list[str],
    label_column: str,
    domain_column: str,
) -> dict[str, dict[str, Any]]:
    if not rows or domain_column not in rows[0]:
        return {}

    gold_by_domain: dict[str, list[str]] = defaultdict(list)
    predicted_by_domain: dict[str, list[str]] = defaultdict(list)
    for row, predicted in zip(rows, predicted_labels):
        domain = row.get(domain_column, "unknown") or "unknown"
        gold_by_domain[domain].append(row[label_column])
        predicted_by_domain[domain].append(predicted)

    scores_by_domain = {}
    for domain in sorted(gold_by_domain):
        metrics = classification_metrics(gold_by_domain[domain], predicted_by_domain[domain])
        scores_by_domain[domain] = {
            "accuracy": metrics["accuracy"],
            "macro_f1": metrics["macro_f1"],
            "total": len(gold_by_domain[domain]),
        }
    return scores_by_domain


def write_prediction_rows_flexible(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return

    base_columns = [
        "id",
        "domain",
        "label",
        "text",
        "method",
        "dominant_emotion",
        "confidence",
        "coverage",
    ]
    score_columns = [f"score_{emotion}" for emotion in EMOTIONS]
    extra_columns = sorted({key for row in rows for key in row} - set(base_columns) - set(score_columns))
    columns = [field for field in base_columns if any(field in row for row in rows)]
    columns.extend(score_columns)
    columns.extend(extra_columns)

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def write_comparison_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["method", "accuracy", "macro_f1", "total"])
        writer.writeheader()
        writer.writerows(rows)


def write_domain_metrics_csv(path: Path, summary: dict[str, Any]) -> None:
    columns = ["method", "domain", "accuracy", "macro_f1", "total"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for method, method_summary in summary["methods"].items():
            for domain, metrics in method_summary["domain_metrics"].items():
                row = {"method": method, "domain": domain}
                row.update(metrics)
                writer.writerow(row)


def write_confusion_csv(path: Path, confusion: dict[str, dict[str, int]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["gold\\predicted", *EMOTIONS])
        for gold in EMOTIONS:
            writer.writerow([gold, *[confusion[gold][pred] for pred in EMOTIONS]])


def write_distribution_csv(path: Path, distribution: dict[str, int]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["emotion", "count"])
        writer.writeheader()
        for emotion in EMOTIONS:
            writer.writerow({"emotion": emotion, "count": distribution.get(emotion, 0)})
