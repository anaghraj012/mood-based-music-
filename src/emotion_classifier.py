"""Validation and normalization of emotion model output."""
from dataclasses import dataclass, field

from .config import EMOTIONS


@dataclass(frozen=True)
class EmotionResult:
    emotion: str
    confidence: float
    scores: dict[str, float] = field(default_factory=dict)

    def __post_init__(self):
        if self.emotion not in EMOTIONS:
            raise ValueError(f"Unsupported emotion: {self.emotion}")
        if not 0 <= self.confidence <= 1:
            raise ValueError("Confidence must be between 0 and 1")


class EmotionClassifier:
    def classify(self, raw_result: dict) -> EmotionResult:
        emotion = str(raw_result.get("emotion", raw_result.get("dominant_emotion", ""))).lower()
        if emotion not in EMOTIONS:
            raise ValueError(f"Unsupported emotion: {emotion or '<missing>'}")
        raw_scores = raw_result.get("scores", raw_result.get("emotion_scores", {}))
        scores = {str(key).lower(): float(value) / 100 if float(value) > 1 else float(value) for key, value in raw_scores.items()}
        confidence = raw_result.get("confidence")
        if confidence is None:
            confidence = scores.get(emotion, 0.0)
        confidence = float(confidence)
        if confidence > 1:
            confidence /= 100
        return EmotionResult(emotion, confidence, scores)
