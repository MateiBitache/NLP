"""Emotion analysis package for the NLP final project."""

from .constants import EMOTIONS
from .experiments import run_experiment_suite
from .pipeline import EmotionAnalyzer

__all__ = ["EMOTIONS", "EmotionAnalyzer", "run_experiment_suite"]
