import pytest

from src.emotion_classifier import EmotionClassifier


def test_classifier_normalizes_percent_confidence():
    result = EmotionClassifier().classify({"emotion": "happy", "scores": {"happy": 92}})
    assert result.emotion == "happy"
    assert result.confidence == pytest.approx(0.92)


def test_classifier_rejects_unknown_emotion():
    with pytest.raises(ValueError):
        EmotionClassifier().classify({"emotion": "unknown"})
