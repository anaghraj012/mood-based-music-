"""Local music discovery and history-aware recommendations."""
import random
from pathlib import Path

from .config import LEGACY_MUSIC_DIR, MUSIC_DIR, SUPPORTED_AUDIO_EXTENSIONS
from .logger import get_logger

logger = get_logger(__name__)


class MusicRecommender:
    def __init__(self, music_dir: Path | str | None = None, rng=None):
        self.music_dir = Path(music_dir) if music_dir else MUSIC_DIR
        self.rng = rng or random
        self.recent_tracks: list[str] = []

    def discover(self, mood: str) -> list[Path]:
        roots = [self.music_dir]
        has_tracks = any(
            path.is_file()
            for extension in SUPPORTED_AUDIO_EXTENSIONS
            for path in self.music_dir.rglob(f"*{extension}")
        )
        if not has_tracks and LEGACY_MUSIC_DIR.is_dir():
            roots.append(LEGACY_MUSIC_DIR)
        mood_dir = self.music_dir / mood
        candidates = list(mood_dir.glob("*") if mood_dir.is_dir() else [])
        if not candidates and len(roots) > 1:
            candidates = list(roots[-1].glob("*"))
        return sorted(path for path in candidates if path.suffix.lower() in SUPPORTED_AUDIO_EXTENSIONS and path.is_file())

    def recommend(self, mood: str) -> Path | None:
        tracks = self.discover(mood)
        if not tracks:
            return None
        available = [track for track in tracks if str(track) not in self.recent_tracks] or tracks
        choice = self.rng.choice(available)
        self.recent_tracks.append(str(choice))
        self.recent_tracks = self.recent_tracks[-max(1, len(tracks)):]
        return choice
