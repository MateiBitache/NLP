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


"""Experiment runner for the final project deliverables."""

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
    """Run all selected methods on a labeled CSV and save report-ready artifacts."""
    rows = read_text_rows(input_path, text_column=text_column)
    validate_labeled_rows(rows, label_column=label_column)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # One analyzer is reused so the NB model is trained once, then shared by methods.
    analyzer = analyzer or EmotionAnalyzer(
        lexicon_path=lexicon_path,
        hybrid_lexicon_weight=hybrid_lexicon_weight,
    )
    summary: dict[str, Any] = {
        "dataset": str(input_path),
        "rows": len(rows),
        "hybrid_lexicon_weight": hybrid_lexicon_weight,
        "methods": {},
    }

    gold = [row[label_column] for row in rows]
    summary["gold_distribution"] = label_distribution(gold)

    # Save both machine-readable CSV and presentation-friendly SVG distributions.
    write_distribution_csv(output_path / "gold_distribution.csv", summary["gold_distribution"])
    write_distribution_svg(
        output_path / "gold_distribution.svg",
        summary["gold_distribution"],
        title="Gold emotion distribution",
    )

    comparison_rows = []
    for method in methods:
        method_predictions = []
        predicted_labels = []
        for row in rows:
            prediction = analyzer.analyze(row[text_column], method=method)
            predicted_labels.append(prediction["dominant_emotion"])
            flat = flatten_prediction(row, prediction)
            flat[label_column] = row[label_column]
            if domain_column in row:
                flat[domain_column] = row[domain_column]
            method_predictions.append(flat)

        # Each method gets the same set of artifacts for direct comparison.
        metrics = classification_metrics(gold, predicted_labels)
        distribution = label_distribution(predicted_labels)
        summary["methods"][method] = {
            "metrics": metrics,
            "predicted_distribution": distribution,
            "domain_metrics": domain_metrics(rows, predicted_labels, label_column, domain_column),
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
    write_domain_metrics_csv(output_path / "domain_metrics.csv", summary)
    (output_path / "metrics.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return summary


def validate_labeled_rows(rows: list[dict[str, str]], *, label_column: str) -> None:
    """Fail early if the experiment dataset is empty or has invalid labels."""
    if not rows:
        raise ValueError("Experiment dataset is empty.")
    invalid = sorted({row.get(label_column, "") for row in rows if row.get(label_column) not in EMOTIONS})
    if invalid:
        raise ValueError(f"Invalid labels in dataset: {', '.join(invalid)}")


def domain_metrics(
    rows: list[dict[str, str]],
    predicted_labels: list[str],
    label_column: str,
    domain_column: str,
) -> dict[str, dict[str, Any]]:
    """Compute aggregate metrics separately for each text domain."""
    if not rows or domain_column not in rows[0]:
        return {}
    grouped_gold: dict[str, list[str]] = defaultdict(list)
    grouped_pred: dict[str, list[str]] = defaultdict(list)
    for row, predicted in zip(rows, predicted_labels):
        domain = row.get(domain_column, "unknown") or "unknown"
        grouped_gold[domain].append(row[label_column])
        grouped_pred[domain].append(predicted)
    result = {}
    for domain in sorted(grouped_gold):
        metrics = classification_metrics(grouped_gold[domain], grouped_pred[domain])
        result[domain] = {
            "accuracy": metrics["accuracy"],
            "macro_f1": metrics["macro_f1"],
            "total": len(grouped_gold[domain]),
        }
    return result


def write_prediction_rows_flexible(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write prediction rows that may include optional label/domain columns."""
    if not rows:
        return
    base_fields = ["id", "domain", "label", "text", "method", "dominant_emotion", "confidence", "coverage"]
    score_fields = [f"score_{emotion}" for emotion in EMOTIONS]
    extra_fields = sorted({key for row in rows for key in row} - set(base_fields) - set(score_fields))
    fieldnames = [field for field in base_fields if any(field in row for row in rows)]
    fieldnames.extend(score_fields)
    fieldnames.extend(extra_fields)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def write_comparison_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write the compact table used in the report for method comparison."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["method", "accuracy", "macro_f1", "total"])
        writer.writeheader()
        writer.writerows(rows)


def write_domain_metrics_csv(path: Path, summary: dict[str, Any]) -> None:
    """Write per-domain metrics for social/news/blog analysis."""
    fieldnames = ["method", "domain", "accuracy", "macro_f1", "total"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for method, method_summary in summary["methods"].items():
            for domain, metrics in method_summary["domain_metrics"].items():
                row = {"method": method, "domain": domain}
                row.update(metrics)
                writer.writerow(row)


def write_confusion_csv(path: Path, confusion: dict[str, dict[str, int]]) -> None:
    """Write a confusion matrix with gold labels as rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["gold\\predicted", *EMOTIONS])
        for gold in EMOTIONS:
            writer.writerow([gold, *[confusion[gold][pred] for pred in EMOTIONS]])


def write_distribution_csv(path: Path, distribution: dict[str, int]) -> None:
    """Write label distribution counts in a simple two-column CSV."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["emotion", "count"])
        writer.writeheader()
        for emotion in EMOTIONS:
            writer.writerow({"emotion": emotion, "count": distribution.get(emotion, 0)})
