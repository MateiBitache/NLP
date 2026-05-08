from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


LABEL_NAMES = {
    0: "human",
    1: "machine",
}
TASK_A_PARQUET = "tools/SemEval-2026-Task13/task_A/task_a_trial.parquet"


def load_task_a_rows(task_a_parquet: Path, *, max_rows: int | None) -> pd.DataFrame:
    rows = pd.read_parquet(task_a_parquet)
    needed = {"code", "label"}
    missing = needed - set(rows.columns)
    if missing:
        raise ValueError(f"Task A parquet is missing columns: {', '.join(sorted(missing))}")

    rows = rows.dropna(subset=["code", "label"]).copy()
    rows["label"] = rows["label"].astype(int)
    if max_rows is not None and len(rows) > max_rows:
        rows = rows.sample(n=max_rows, random_state=13)
    return rows


def build_detector() -> Pipeline:
    vectorizer = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 6),
        min_df=2,
        max_features=120_000,
    )
    classifier = LogisticRegression(
        max_iter=1200,
        class_weight="balanced",
        solver="liblinear",
    )
    return Pipeline(
        steps=[
            ("tfidf", vectorizer),
            ("clf", classifier),
        ]
    )


def train_detector(rows: pd.DataFrame) -> tuple[Pipeline, dict[str, float]]:
    train_code, test_code, train_label, test_label = train_test_split(
        rows["code"],
        rows["label"],
        test_size=0.2,
        random_state=13,
        stratify=rows["label"],
    )

    detector = build_detector()
    detector.fit(train_code, train_label)
    validation_pred = detector.predict(test_code)
    metrics = {
        "validation_accuracy": round(accuracy_score(test_label, validation_pred), 4),
        "validation_macro_f1": round(
            f1_score(test_label, validation_pred, average="macro"),
            4,
        ),
    }
    return detector, metrics


def classify_file(detector: Pipeline, code_path: Path) -> dict[str, object]:
    code = code_path.read_text(encoding="utf-8")
    prediction = int(detector.predict([code])[0])
    probabilities = detector.predict_proba([code])[0]
    scores = {
        LABEL_NAMES[index]: round(float(probability), 4)
        for index, probability in enumerate(probabilities)
    }
    return {
        "file": str(code_path),
        "prediction_id": prediction,
        "prediction": LABEL_NAMES[prediction],
        "scores": scores,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, nargs="+", help="Source code file(s) to classify.")
    parser.add_argument(
        "--task-a",
        default=TASK_A_PARQUET,
        help="Path to the SemEval Task A parquet file.",
    )
    parser.add_argument("--max-rows", type=int, default=None)
    args = parser.parse_args()

    rows = load_task_a_rows(Path(args.task_a), max_rows=args.max_rows)
    detector, metrics = train_detector(rows)
    files = [classify_file(detector, Path(path)) for path in args.file]
    result = {
        "training_rows": int(len(rows)),
        **metrics,
        "files": files,
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
