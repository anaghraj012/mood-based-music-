"""Pygame-backed local audio playback."""
from pathlib import Path

from .config import DEFAULT_VOLUME
from .logger import get_logger

logger = get_logger(__name__)


class MusicPlayer:
    def __init__(self, volume: float = DEFAULT_VOLUME, pygame_module=None):
        self._pygame = pygame_module
        self._initialized = False
        self.volume = max(0.0, min(1.0, volume))

    def _mixer(self):
        if self._pygame is None:
            import pygame
            self._pygame = pygame
        if not self._initialized:
            self._pygame.mixer.init()
            self._pygame.mixer.music.set_volume(self.volume)
            self._initialized = True
        return self._pygame.mixer.music

    def play(self, path: Path | str) -> bool:
        audio_path = Path(path)
        if not audio_path.is_file():
            logger.warning("Music file not found: %s", audio_path)
            return False
        try:
            music = self._mixer()
            music.load(str(audio_path))
            music.play(-1)
            return True
        except Exception:
            logger.exception("Music loading failed: %s", audio_path)
            return False

    def pause(self):
        if self._initialized:
            self._mixer().pause()

    def resume(self):
        if self._initialized:
            self._mixer().unpause()

    def stop(self):
        if self._initialized:
            self._mixer().stop()

    def set_volume(self, volume: float):
        self.volume = max(0.0, min(1.0, float(volume)))
        if self._initialized:
            self._mixer().set_volume(self.volume)

    def is_playing(self) -> bool:
        return bool(self._initialized and self._mixer().get_busy())
