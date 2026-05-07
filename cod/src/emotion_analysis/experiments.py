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
SEMEVAL_ID_COLUMN = "ID"
SOURCE_ID_COLUMN = "source_id"
PREDICTION_COLUMN = "prediction"


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
    rows = read_text_rows(input_path, text_column=text_column)
    check_labels(rows, label_column=label_column)
    check_methods(methods)

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

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

    # These artifact names are referenced by the README, report and slides.
    write_dist_csv(out_dir / "gold_distribution.csv", summary["gold_distribution"])
    write_distribution_svg(
        out_dir / "gold_distribution.svg",
        summary["gold_distribution"],
        title="Gold emotion distribution",
    )

    comparison: list[dict[str, Any]] = []
    for method in methods:
        out_rows: list[dict[str, Any]] = []
        preds: list[str] = []

        for row in rows:
            prediction = analyzer.analyze(row[text_column], method=method)
            preds.append(prediction["dominant_emotion"])
            out_row = flatten_prediction(row, prediction)
            out_row[label_column] = row[label_column]
            out_row[PREDICTION_COLUMN] = prediction["dominant_emotion"]
            semeval_id = semeval_row_id(row)
            if semeval_id:
                out_row[SEMEVAL_ID_COLUMN] = semeval_id
            if domain_column in row:
                out_row[domain_column] = row[domain_column]
            out_rows.append(out_row)

        metrics = classification_metrics(gold, preds)
        distribution = label_distribution(preds)
        summary["methods"][method] = {
            "metrics": metrics,
            "predicted_distribution": distribution,
            "domain_metrics": scores_by_domain(
                rows,
                preds,
                label_column,
                domain_column,
            ),
        }
        comparison.append(
            {
                "method": method,
                "accuracy": metrics["accuracy"],
                "macro_precision": metrics["macro_precision"],
                "macro_recall": metrics["macro_recall"],
                "macro_f1": metrics["macro_f1"],
                "total": metrics["total"],
            }
        )

        write_preds_csv(out_dir / f"predictions_{method}.csv", out_rows)
        write_conf_csv(out_dir / f"confusion_{method}.csv", metrics["confusion"])
        write_dist_csv(out_dir / f"predicted_distribution_{method}.csv", distribution)
        write_distribution_svg(
            out_dir / f"predicted_distribution_{method}.svg",
            distribution,
            title=f"Predicted emotion distribution - {method}",
        )

    write_compare_csv(out_dir / "method_comparison.csv", comparison)
    write_domain_csv(out_dir / "domain_metrics.csv", summary)
    (out_dir / "metrics.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return summary


def check_labels(rows: list[dict[str, str]], *, label_column: str) -> None:
    if not rows:
        raise ValueError("Experiment dataset is empty.")

    bad_labels = set()
    for row in rows:
        label = row.get(label_column, "")
        if label not in EMOTIONS:
            bad_labels.add(label)

    if bad_labels:
        raise ValueError(f"Invalid labels in dataset: {', '.join(sorted(bad_labels))}")


def check_methods(methods: tuple[str, ...]) -> None:
    unknown = sorted(set(methods) - set(DEFAULT_METHODS))
    if unknown:
        raise ValueError(f"Unknown experiment methods: {', '.join(unknown)}")


def semeval_row_id(row: dict[str, str]) -> str:
    return row.get(SEMEVAL_ID_COLUMN) or row.get("id") or row.get(SOURCE_ID_COLUMN, "")


def scores_by_domain(
    rows: list[dict[str, str]],
    preds: list[str],
    label_column: str,
    domain_column: str,
) -> dict[str, dict[str, Any]]:
    if not rows or domain_column not in rows[0]:
        return {}

    gold_by_domain: dict[str, list[str]] = defaultdict(list)
    pred_by_domain: dict[str, list[str]] = defaultdict(list)
    for row, pred in zip(rows, preds):
        domain = row.get(domain_column, "unknown") or "unknown"
        gold_by_domain[domain].append(row[label_column])
        pred_by_domain[domain].append(pred)

    domain_scores = {}
    for domain in sorted(gold_by_domain):
        metrics = classification_metrics(gold_by_domain[domain], pred_by_domain[domain])
        domain_scores[domain] = {
            "accuracy": metrics["accuracy"],
            "macro_precision": metrics["macro_precision"],
            "macro_recall": metrics["macro_recall"],
            "macro_f1": metrics["macro_f1"],
            "total": len(gold_by_domain[domain]),
        }
    return domain_scores


def write_preds_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return

    # Experiment rows may carry label/domain columns besides model scores.
    base_columns = [
        SEMEVAL_ID_COLUMN,
        SOURCE_ID_COLUMN,
        "domain",
        "label",
        "text",
        "method",
        "dominant_emotion",
        PREDICTION_COLUMN,
        "confidence",
        "coverage",
    ]
    score_columns = [f"score_{emotion}" for emotion in EMOTIONS]
    extra_columns = sorted(
        {key for row in rows for key in row} - set(base_columns) - set(score_columns)
    )
    columns = [field for field in base_columns if any(field in row for row in rows)]
    columns.extend(score_columns)
    columns.extend(extra_columns)

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def write_compare_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    columns = ["method", "accuracy", "macro_precision", "macro_recall", "macro_f1", "total"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def write_domain_csv(path: Path, summary: dict[str, Any]) -> None:
    columns = [
        "method",
        "domain",
        "accuracy",
        "macro_precision",
        "macro_recall",
        "macro_f1",
        "total",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for method, method_summary in summary["methods"].items():
            for domain, metrics in method_summary["domain_metrics"].items():
                row = {"method": method, "domain": domain}
                row.update(metrics)
                writer.writerow(row)


def write_conf_csv(path: Path, confusion: dict[str, dict[str, int]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["gold\\predicted", *EMOTIONS])
        for gold in EMOTIONS:
            writer.writerow([gold, *[confusion[gold][pred] for pred in EMOTIONS]])


def write_dist_csv(path: Path, distribution: dict[str, int]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["emotion", "count"])
        writer.writeheader()
        for emotion in EMOTIONS:
            writer.writerow({"emotion": emotion, "count": distribution.get(emotion, 0)})
