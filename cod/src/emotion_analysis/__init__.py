"""Emotion analysis package for the NLP final project."""

from .constants import EMOTIONS
from .experiments import run_experiment_suite
from .pipeline import EmotionAnalyzer

# Public API: useful if the package is imported from notebooks or future scripts.
__all__ = ["EMOTIONS", "EmotionAnalyzer", "run_experiment_suite"]
