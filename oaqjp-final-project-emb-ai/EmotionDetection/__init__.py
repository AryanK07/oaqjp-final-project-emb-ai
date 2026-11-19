"""Public interface for the EmotionDetection package."""

from .emotion_detection import EMOTIONS, WatsonServiceError, emotion_detector

__all__ = ["EMOTIONS", "WatsonServiceError", "emotion_detector"]
