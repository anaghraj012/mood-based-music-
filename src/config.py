"""Central application configuration using repository-relative paths."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
HISTORY_DIR = DATA_DIR / "history"
HISTORY_FILE = HISTORY_DIR / "analysis_history.json"
CAPTURE_DIR = DATA_DIR / "captures"
LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIR / "application.log"
MUSIC_DIR = PROJECT_ROOT / "music"
LEGACY_MUSIC_DIR = PROJECT_ROOT / "project" / "music"
CASCADE_PATH = Path(__import__("cv2").data.haarcascades) / "haarcascade_frontalface_default.xml"
WEBCAM_INDEX = 0
FRAME_SKIP = 5
SMOOTHING_WINDOW = 5
MIN_CONFIDENCE = 0.40
DEFAULT_VOLUME = 0.70
SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
SUPPORTED_AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg"}
EMOTIONS = {"angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"}
