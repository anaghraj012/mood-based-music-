"""JSON persistence and session statistics for analyses."""
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from .config import HISTORY_FILE


class HistoryManager:
    def __init__(self, history_file: Path | str | None = None):
        self.history_file = Path(history_file) if history_file else HISTORY_FILE

    def load_history(self) -> list[dict]:
        if not self.history_file.is_file():
            return []
        try:
            data = json.loads(self.history_file.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except (OSError, json.JSONDecodeError):
            return []

    def save_analysis(self, source: str, emotion: str, confidence: float, mood: str, recommended_track: str | None = None) -> dict:
        entry = {"timestamp": datetime.now(timezone.utc).isoformat(), "source": source, "emotion": emotion, "confidence": confidence, "mood": mood, "recommended_track": recommended_track}
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        history = self.load_history()
        history.append(entry)
        self.history_file.write_text(json.dumps(history, indent=2), encoding="utf-8")
        return entry

    def get_recent(self, count: int = 10) -> list[dict]:
        return self.load_history()[-count:]

    def clear_history(self):
        if self.history_file.exists():
            self.history_file.unlink()

    def summary(self, entries: list[dict] | None = None) -> dict:
        records = self.load_history() if entries is None else entries
        if not records:
            return {"analyses": 0, "most_frequent_emotion": None, "average_confidence": 0.0, "most_frequent_mood": None}
        average_confidence = sum(float(item["confidence"]) for item in records) / len(records)
        return {"analyses": len(records), "most_frequent_emotion": Counter(item["emotion"] for item in records).most_common(1)[0][0], "average_confidence": round(average_confidence, 6), "most_frequent_mood": Counter(item["mood"] for item in records).most_common(1)[0][0]}
