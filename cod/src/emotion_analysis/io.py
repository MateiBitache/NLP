from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from .constants import EMOTIONS


"""CSV input/output helpers used by CLI commands and experiments."""

def read_text_rows(path: str | Path, *, text_column: str = "text") -> list[dict[str, str]]:
    """Read CSV rows and validate that the configured text column exists."""
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or text_column not in reader.fieldnames:
            raise ValueError(f"CSV must contain a '{text_column}' column.")
        return list(reader)


def write_prediction_rows(path: str | Path, rows: list[dict[str, Any]]) -> None:
    """Write prediction rows with a stable column order."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["id", "text", "method", "dominant_emotion", "confidence", "coverage"]
    fieldnames.extend(f"score_{emotion}" for emotion in EMOTIONS)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name, "") for name in fieldnames})


def flatten_prediction(source_row: dict[str, str], prediction: dict[str, Any]) -> dict[str, Any]:
    """Convert a nested model result into one CSV-friendly row."""
    flat: dict[str, Any] = {
        "id": source_row.get("id", ""),
        "text": prediction["text"],
        "method": prediction["method"],
        "dominant_emotion": prediction["dominant_emotion"],
        "confidence": round(float(prediction["confidence"]), 4),
        "coverage": round(float(prediction.get("coverage", 0.0)), 4),
    }

    # Store one numeric column per emotion so results are easy to compare in tables.
    for emotion in EMOTIONS:
        flat[f"score_{emotion}"] = round(float(prediction["scores"].get(emotion, 0.0)), 4)
    return flat
