from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def pick_column(rows: list[dict[str, str]], options: tuple[str, ...], *, role: str) -> str:
    if not rows:
        raise ValueError(f"{role} file is empty.")
    for name in options:
        if name in rows[0]:
            return name
    raise ValueError(f"{role} file must contain one of these columns: {', '.join(options)}")


def load_valid_labels(task_root: Path | None, task: str | None) -> set[str] | None:
    if task_root is None or task is None:
        return None
    mapping = task_root / f"task_{task.upper()}" / "id_to_label.json"
    if not mapping.exists():
        raise FileNotFoundError(f"Label mapping not found: {mapping}")
    return set(json.loads(mapping.read_text(encoding="utf-8")).keys())


def macro_scores(gold: list[str], pred: list[str]) -> dict[str, float]:
    labels = sorted(set(gold) | set(pred))
    label_rows = []
    correct = sum(1 for expected, actual in zip(gold, pred) if expected == actual)

    for label in labels:
        tp, fp, fn = one_vs_rest_counts(gold, pred, label)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        label_rows.append((precision, recall, f1))

    total = len(gold)
    label_count = len(labels)
    return {
        "accuracy": round(correct / total, 4) if total else 0.0,
        "macro_precision": round(sum(row[0] for row in label_rows) / label_count, 4)
        if labels
        else 0.0,
        "macro_recall": round(sum(row[1] for row in label_rows) / label_count, 4)
        if labels
        else 0.0,
        "macro_f1": round(sum(row[2] for row in label_rows) / label_count, 4)
        if labels
        else 0.0,
    }


def one_vs_rest_counts(gold: list[str], pred: list[str], label: str) -> tuple[int, int, int]:
    tp = fp = fn = 0
    for expected, actual in zip(gold, pred):
        if expected == label and actual == label:
            tp += 1
        elif expected != label and actual == label:
            fp += 1
        elif expected == label and actual != label:
            fn += 1
    return tp, fp, fn


def check_predictions(
    predictions: Path,
    *,
    gold: Path | None = None,
    task_root: Path | None = None,
    task: str | None = None,
) -> dict[str, object]:
    pred_rows = read_rows(predictions)
    pred_id = pick_column(pred_rows, ("ID", "id"), role="Prediction")
    pred_label = pick_column(pred_rows, ("prediction", "label"), role="Prediction")

    valid_labels = load_valid_labels(task_root, task)
    if valid_labels is not None:
        invalid = sorted({row[pred_label] for row in pred_rows} - valid_labels)
        if invalid:
            raise ValueError(f"Invalid label IDs: {', '.join(invalid)}")

    report: dict[str, object] = {
        "rows": len(pred_rows),
        "id_column": pred_id,
        "prediction_column": pred_label,
        "format_ok": True,
    }

    if gold is None:
        return report

    gold_rows = read_rows(gold)
    gold_id = pick_column(gold_rows, ("ID", "id"), role="Gold")
    gold_label = pick_column(gold_rows, ("label",), role="Gold")
    gold_by_id = {row[gold_id]: row[gold_label] for row in gold_rows}

    paired_gold: list[str] = []
    paired_pred: list[str] = []
    for row in pred_rows:
        row_id = row[pred_id]
        if row_id not in gold_by_id:
            continue
        paired_gold.append(gold_by_id[row_id])
        paired_pred.append(row[pred_label])

    if not paired_gold:
        raise ValueError("No matching IDs between prediction and gold files.")
    report["matched_rows"] = len(paired_gold)
    report.update(macro_scores(paired_gold, paired_pred))
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--gold")
    parser.add_argument("--task-root")
    parser.add_argument("--task", choices=("A", "B", "C", "a", "b", "c"))
    args = parser.parse_args()

    report = check_predictions(
        Path(args.predictions),
        gold=Path(args.gold) if args.gold else None,
        task_root=Path(args.task_root) if args.task_root else None,
        task=args.task,
    )
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
