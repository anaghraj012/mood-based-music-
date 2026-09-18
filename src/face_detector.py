"""OpenCV Haar-cascade face detection."""
from pathlib import Path
from typing import Iterable

import cv2

from .config import CASCADE_PATH
from .logger import get_logger

logger = get_logger(__name__)


class FaceDetector:
    def __init__(self, cascade_path: Path | str | None = None):
        path = Path(cascade_path) if cascade_path else CASCADE_PATH
        if not path.is_file():
            raise FileNotFoundError(f"Face cascade not found: {path}")
        self.cascade = cv2.CascadeClassifier(str(path))
        if self.cascade.empty():
            raise ValueError(f"Could not load face cascade: {path}")

    def detect_faces(self, frame) -> list[tuple[int, int, int, int]]:
        if frame is None or getattr(frame, "size", 0) == 0:
            return []
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detected = self.cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return [tuple(int(value) for value in box) for box in detected]

    def draw_faces(self, frame, faces: Iterable[tuple[int, int, int, int]], labels: Iterable[str] | None = None):
        labels = list(labels or [])
        for index, (x, y, width, height) in enumerate(faces):
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 220, 120), 2)
            if index < len(labels):
                cv2.putText(frame, labels[index], (x, max(20, y - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 220, 120), 2)
        return frame
