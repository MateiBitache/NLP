"""Command-line interface for predictions, evaluation and experiment runs."""

from __future__ import annotations

import argparse
import json
from typing import Any

from .constants import EMOTIONS
from .experiments import DEFAULT_METHODS, run_experiment_suite
from .io import flatten_prediction, read_text_rows, write_prediction_rows
from .nb_model import evaluate_nb_from_lexicon
from .pipeline import EmotionAnalyzer


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="emotion_cli.py",
        description="Detect Plutchik-style emotions in text.",
    )
    parser.add_argument("--lexicon", default=None, help="Path to NRC Hashtag Emotion Lexicon.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    predict_cmd = subparsers.add_parser("predict", help="Analyze one text.")
    predict_cmd.add_argument("--text", required=True)
    predict_cmd.add_argument("--method", choices=("lexicon", "nb", "hybrid"), default="hybrid")
    predict_cmd.add_argument("--hybrid-weight", type=float, default=0.85)
    predict_cmd.add_argument("--top", type=int, default=3)
    predict_cmd.add_argument("--json", action="store_true")

    file_cmd = subparsers.add_parser("predict-file", help="Analyze a CSV file.")
    file_cmd.add_argument("--input", required=True)
    file_cmd.add_argument("--output", required=True)
    file_cmd.add_argument("--text-column", default="text")
    file_cmd.add_argument("--method", choices=("lexicon", "nb", "hybrid"), default="hybrid")
    file_cmd.add_argument("--hybrid-weight", type=float, default=0.85)

    evaluate_cmd = subparsers.add_parser("evaluate", help="Evaluate NB on a held-out lexicon split.")
    evaluate_cmd.add_argument("--max-per-emotion", type=int, default=2500)
    evaluate_cmd.add_argument("--min-score", type=float, default=0.3)
    evaluate_cmd.add_argument("--json", action="store_true")

    experiment_cmd = subparsers.add_parser(
        "run-experiments",
        help="Compare lexicon, NB and hybrid on a labeled CSV dataset.",
    )
    experiment_cmd.add_argument("--input", default="data/final_eval_texts.csv")
    experiment_cmd.add_argument("--output-dir", default="outputs/final_experiment")
    experiment_cmd.add_argument("--text-column", default="text")
    experiment_cmd.add_argument("--label-column", default="label")
    experiment_cmd.add_argument("--domain-column", default="domain")
    experiment_cmd.add_argument("--hybrid-weight", type=float, default=0.85)
    experiment_cmd.add_argument(
        "--methods",
        nargs="+",
        choices=DEFAULT_METHODS,
        default=list(DEFAULT_METHODS),
    )
    experiment_cmd.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

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
        result = analyzer.analyze(args.text, method=args.method)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print_prediction(result, top=args.top)
        return 0

    if args.command == "predict-file":
        rows = read_text_rows(args.input, text_column=args.text_column)
        predictions = []
        for row in rows:
            prediction = analyzer.analyze(row[args.text_column], method=args.method)
            predictions.append(flatten_prediction(row, prediction))
        write_prediction_rows(args.output, predictions)
        print(f"Wrote {len(predictions)} predictions to {args.output}")
        return 0

    parser.error("Unknown command.")
    return 2


def print_prediction(result: dict[str, Any], *, top: int = 3) -> None:
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
    print(f"dataset: {summary['dataset']}")
    print(f"rows: {summary['rows']}")
    print(f"output_dir: {output_dir}")
    print("method_comparison:")
    for method, details in summary["methods"].items():
        metrics = details["metrics"]
        print(
            f"  {method}: accuracy={metrics['accuracy']:.4f} "
            f"macro_precision={metrics['macro_precision']:.4f} "
            f"macro_recall={metrics['macro_recall']:.4f} "
            f"macro_f1={metrics['macro_f1']:.4f} total={metrics['total']}"
        )


def top_scores(scores: dict[str, float], *, limit: int) -> list[tuple[str, float]]:
    return sorted(scores.items(), key=lambda item: item[1], reverse=True)[:limit]
