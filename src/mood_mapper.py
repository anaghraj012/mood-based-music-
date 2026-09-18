"""Configurable emotion-to-mood mapping."""
import json
from pathlib import Path

from .config import PROJECT_ROOT

DEFAULT_MAPPING = {
    "happy": "energetic", "surprise": "energetic", "neutral": "calm",
    "sad": "reflective", "fear": "tense", "angry": "intense", "disgust": "intense",
}


class MoodMapper:
    def __init__(self, mapping_path: Path | str | None = None):
        path = Path(mapping_path) if mapping_path else PROJECT_ROOT / "data" / "emotions.json"
        self.mapping = dict(DEFAULT_MAPPING)
        if path.is_file():
            data = json.loads(path.read_text(encoding="utf-8"))
            self.mapping.update(data.get("emotion_to_mood", {}))

    def map_emotion(self, emotion: str) -> str:
        try:
            return self.mapping[emotion.lower()]
        except KeyError as exc:
            raise ValueError(f"No mood mapping for emotion: {emotion}") from exc
