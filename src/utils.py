"""Small presentation and webcam helpers."""
from collections import Counter, deque


def stable_emotion(emotions: deque[str]) -> str | None:
    return Counter(emotions).most_common(1)[0][0] if emotions else None


def print_analysis(index: int, result, mood: str, recommendation):
    print(f"\nFace {index}")
    print("-----------------------------------------")
    print(f"Emotion      : {result.emotion.title()}")
    print(f"Confidence   : {result.confidence:.1%}")
    print(f"Mood         : {mood.title()}")
    print(f"Recommendation: {recommendation.name if recommendation else 'No local track found'}")
