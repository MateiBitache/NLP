"""Regression tests for the main project workflows."""

import unittest
from tempfile import TemporaryDirectory
from pathlib import Path

from emotion_analysis.experiments import run_experiment_suite
from emotion_analysis.lexicon_model import WeightedEmotionLexicon
from emotion_analysis.metrics import classification_metrics
from emotion_analysis.nb_model import EmotionNaiveBayes, TrainingExample
from emotion_analysis.pipeline import EmotionAnalyzer


class EmotionAnalysisTests(unittest.TestCase):
    def test_lexicon_scores_known_words(self):
        lexicon = {
            "anger": {"furious": 2.0},
            "anticipation": {},
            "disgust": {},
            "fear": {},
            "joy": {"happy": 3.0},
            "sadness": {},
            "surprise": {},
            "trust": {},
        }
        model = WeightedEmotionLexicon(lexicon=lexicon)
        result = model.score("I am very happy, not furious.")
        self.assertEqual(result["dominant_emotion"], "joy")
        self.assertGreater(result["scores"]["joy"], result["scores"]["anger"])

    def test_nb_learns_simple_examples(self):
        model = EmotionNaiveBayes().fit(
            [
                TrainingExample("happy delighted smile", "joy"),
                TrainingExample("furious angry rage", "anger"),
                TrainingExample("scared afraid panic", "fear"),
            ]
        )
        result = model.predict("angry and furious")
        self.assertEqual(result["dominant_emotion"], "anger")

    def test_pipeline_hybrid_with_injected_nb(self):
        lexicon = {
            "anger": {},
            "anticipation": {},
            "disgust": {},
            "fear": {},
            "joy": {"happy": 1.0},
            "sadness": {},
            "surprise": {},
            "trust": {},
        }
        nb_model = EmotionNaiveBayes().fit(
            [
                TrainingExample("happy", "joy"),
                TrainingExample("sad", "sadness"),
            ]
        )
        analyzer = EmotionAnalyzer(
            lexicon_model=WeightedEmotionLexicon(lexicon=lexicon),
            nb_model=nb_model,
        )
        result = analyzer.analyze("happy", method="hybrid")
        self.assertEqual(result["dominant_emotion"], "joy")

    def test_metrics_macro_f1(self):
        metrics = classification_metrics(
            ["joy", "joy", "anger", "fear"],
            ["joy", "anger", "anger", "fear"],
        )
        self.assertEqual(metrics["accuracy"], 0.75)
        self.assertEqual(metrics["confusion"]["joy"]["anger"], 1)

    def test_invalid_hybrid_weight_is_rejected(self):
        with self.assertRaises(ValueError):
            EmotionAnalyzer(hybrid_lexicon_weight=1.5)

    def test_experiment_suite_writes_outputs(self):
        lexicon = {
            "anger": {"furious": 2.0},
            "anticipation": {},
            "disgust": {},
            "fear": {},
            "joy": {"happy": 2.0},
            "sadness": {},
            "surprise": {},
            "trust": {},
        }
        analyzer = EmotionAnalyzer(
            lexicon_model=WeightedEmotionLexicon(lexicon=lexicon),
            nb_model=EmotionNaiveBayes().fit(
                [
                    TrainingExample("happy", "joy"),
                    TrainingExample("furious", "anger"),
                ]
            ),
        )
        with TemporaryDirectory() as temp_dir:
            work_dir = Path(temp_dir)
            dataset = work_dir / "eval.csv"
            dataset.write_text(
                "id,domain,label,text\n"
                "1,demo,joy,I am happy\n"
                "2,demo,anger,I am furious\n",
                encoding="utf-8",
            )
            summary = run_experiment_suite(
                input_path=dataset,
                output_dir=work_dir / "out",
                methods=("hybrid",),
                analyzer=analyzer,
            )
            self.assertEqual(summary["methods"]["hybrid"]["metrics"]["accuracy"], 1.0)
            self.assertTrue((work_dir / "out" / "metrics.json").exists())
            self.assertTrue((work_dir / "out" / "predicted_distribution_hybrid.svg").exists())


if __name__ == "__main__":
    unittest.main()
