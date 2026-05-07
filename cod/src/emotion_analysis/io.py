"""CSV input/output helpers used by CLI commands and experiments."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from .constants import EMOTIONS


def read_text_rows(path: str | Path, *, text_column: str = "text") -> list[dict[str, str]]:
    csv_path = Path(path)
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = csv.DictReader(handle)
        if rows.fieldnames is None or text_column not in rows.fieldnames:
            raise ValueError(f"CSV must contain a '{text_column}' column.")
        return list(rows)


def write_prediction_rows(path: str | Path, rows: list[dict[str, Any]]) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    columns = ["id", "text", "method", "dominant_emotion", "confidence", "coverage"]
    columns.extend(f"score_{emotion}" for emotion in EMOTIONS)

    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def flatten_prediction(source_row: dict[str, str], prediction: dict[str, Any]) -> dict[str, Any]:
    csv_row: dict[str, Any] = {
        "id": source_row.get("id", ""),
        "text": prediction["text"],
        "method": prediction["method"],
        "dominant_emotion": prediction["dominant_emotion"],
        "confidence": round(float(prediction["confidence"]), 4),
        "coverage": round(float(prediction.get("coverage", 0.0)), 4),
    }

    for emotion in EMOTIONS:
        score = prediction["scores"].get(emotion, 0.0)
        csv_row[f"score_{emotion}"] = round(float(score), 4)
    return csv_row
