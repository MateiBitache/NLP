from __future__ import annotations

import argparse
import json
from typing import Any

from .constants import EMOTIONS
from .experiments import DEFAULT_METHODS, run_experiment_suite
from .io import flatten_prediction, read_text_rows, write_prediction_rows
from .nb_model import evaluate_nb_from_lexicon
from .pipeline import EmotionAnalyzer


"""Command-line interface for running predictions, evaluation and experiments."""

def build_parser() -> argparse.ArgumentParser:
    """Define all terminal commands accepted by emotion_cli.py."""
    parser = argparse.ArgumentParser(
        prog="emotion_cli.py",
        description="Detect Plutchik-style emotions in text.",
    )
    parser.add_argument("--lexicon", default=None, help="Path to NRC Hashtag Emotion Lexicon.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Predict one text passed directly in the command line.
    predict = subparsers.add_parser("predict", help="Analyze one text.")
    predict.add_argument("--text", required=True)
    predict.add_argument("--method", choices=("lexicon", "nb", "hybrid"), default="hybrid")
    predict.add_argument("--hybrid-weight", type=float, default=0.85)
    predict.add_argument("--top", type=int, default=3)
    predict.add_argument("--json", action="store_true")

    # Predict many rows from a CSV file with a configurable text column.
    predict_file = subparsers.add_parser("predict-file", help="Analyze a CSV file.")
    predict_file.add_argument("--input", required=True)
    predict_file.add_argument("--output", required=True)
    predict_file.add_argument("--text-column", default="text")
    predict_file.add_argument("--method", choices=("lexicon", "nb", "hybrid"), default="hybrid")
    predict_file.add_argument("--hybrid-weight", type=float, default=0.85)

    # Evaluate the weakly supervised NB model on a held-out split from the lexicon.
    evaluate = subparsers.add_parser("evaluate", help="Evaluate NB on a held-out lexicon split.")
    evaluate.add_argument("--max-per-emotion", type=int, default=2500)
    evaluate.add_argument("--min-score", type=float, default=0.3)
    evaluate.add_argument("--json", action="store_true")

    # Generate all final project artifacts: predictions, metrics, confusion matrices, charts.
    experiments = subparsers.add_parser(
        "run-experiments",
        help="Compare lexicon, NB and hybrid on a labeled CSV dataset.",
    )
    experiments.add_argument("--input", default="data/final_eval_texts.csv")
    experiments.add_argument("--output-dir", default="outputs/final_experiment")
    experiments.add_argument("--text-column", default="text")
    experiments.add_argument("--label-column", default="label")
    experiments.add_argument("--domain-column", default="domain")
    experiments.add_argument("--hybrid-weight", type=float, default=0.85)
    experiments.add_argument(
        "--methods",
        nargs="+",
        choices=DEFAULT_METHODS,
        default=list(DEFAULT_METHODS),
    )
    experiments.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Route CLI arguments to the correct project workflow."""
    parser = build_parser()
    args = parser.parse_args(argv)

    # This command is special because it only evaluates NB; it does not need the pipeline.
    if args.command == "evaluate":
        metrics = evaluate_nb_from_lexicon(
            args.lexicon,
            max_per_emotion=args.max_per_emotion,
            min_score=args.min_score,
        )
        if args.json:
            print(json.dumps(metrics, indent=2, ensure_ascii=False))
        else:
            print_evaluation(metrics)
        return 0

    if args.command == "run-experiments":
        # The experiment runner writes all report-ready files under output-dir.
        summary = run_experiment_suite(
            input_path=args.input,
            output_dir=args.output_dir,
            text_column=args.text_column,
            label_column=args.label_column,
            domain_column=args.domain_column,
            methods=tuple(args.methods),
            lexicon_path=args.lexicon,
            hybrid_lexicon_weight=args.hybrid_weight,
        )
        if args.json:
            print(json.dumps(summary, indent=2, ensure_ascii=False))
        else:
            print_experiment_summary(summary, output_dir=args.output_dir)
        return 0

    analyzer = EmotionAnalyzer(
        lexicon_path=args.lexicon,
        hybrid_lexicon_weight=getattr(args, "hybrid_weight", 0.85),
    )
    if args.command == "predict":
        # Human-readable output is the default; --json exposes the full result.
        result = analyzer.analyze(args.text, method=args.method)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print_prediction(result, top=args.top)
        return 0

    if args.command == "predict-file":
        # CSV output is flattened so each emotion score becomes its own column.
        rows = read_text_rows(args.input, text_column=args.text_column)
        predictions = [
            flatten_prediction(row, analyzer.analyze(row[args.text_column], method=args.method))
            for row in rows
        ]
        write_prediction_rows(args.output, predictions)
        print(f"Wrote {len(predictions)} predictions to {args.output}")
        return 0

    parser.error("Unknown command.")
    return 2


def print_prediction(result: dict[str, Any], *, top: int = 3) -> None:
    """Print a compact single-text prediction summary."""
    print(f"method: {result['method']}")
    print(f"dominant_emotion: {result['dominant_emotion']}")
    print(f"confidence: {result['confidence']:.4f}")
    if "coverage" in result:
        print(f"lexicon_coverage: {result['coverage']:.4f}")
    print("top_scores:")
    for emotion, score in top_scores(result["scores"], limit=top):
        print(f"  {emotion}: {score:.4f}")
    if result.get("matches"):
        print("evidence:")
        for match in result["matches"][:top]:
            print(f"  {match['term']} -> {match['emotion']} ({match['contribution']:.3f})")


def print_evaluation(metrics: dict[str, Any]) -> None:
    """Print NB held-out evaluation metrics."""
    print(f"train_examples: {metrics['examples']['train']}")
    print(f"test_examples: {metrics['examples']['test']}")
    print(f"accuracy: {metrics['accuracy']:.4f}")
    print(f"macro_f1: {metrics['macro_f1']:.4f}")
    print("per_label:")
    for emotion in EMOTIONS:
        values = metrics["per_label"][emotion]
        print(
            f"  {emotion}: precision={values['precision']:.4f} "
            f"recall={values['recall']:.4f} f1={values['f1']:.4f} "
            f"support={values['support']}"
        )


def print_experiment_summary(summary: dict[str, Any], *, output_dir: str) -> None:
    """Print the main comparison table after run-experiments."""
    print(f"dataset: {summary['dataset']}")
    print(f"rows: {summary['rows']}")
    print(f"output_dir: {output_dir}")
    print("method_comparison:")
    for method, details in summary["methods"].items():
        metrics = details["metrics"]
        print(
            f"  {method}: accuracy={metrics['accuracy']:.4f} "
            f"macro_f1={metrics['macro_f1']:.4f} total={metrics['total']}"
        )


def top_scores(scores: dict[str, float], *, limit: int) -> list[tuple[str, float]]:
    """Return the highest-scoring emotions for display."""
    return sorted(scores.items(), key=lambda item: item[1], reverse=True)[:limit]
