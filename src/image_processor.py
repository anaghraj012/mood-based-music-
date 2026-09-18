"""Image loading and face preprocessing."""
from pathlib import Path

import cv2

from .config import SUPPORTED_IMAGE_EXTENSIONS
from .logger import get_logger

logger = get_logger(__name__)


class ImageProcessor:
    def load_image(self, path: Path | str):
        image_path = Path(path)
        if image_path.suffix.lower() not in SUPPORTED_IMAGE_EXTENSIONS:
            raise ValueError(f"Unsupported image type: {image_path.suffix or '<none>'}")
        if not image_path.is_file():
            raise FileNotFoundError(f"Image not found: {image_path}")
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Could not read image: {image_path}")
        return image

    @staticmethod
    def crop_face(image, box: tuple[int, int, int, int]):
        x, y, width, height = box
        return image[y:y + height, x:x + width]

    @staticmethod
    def preprocess_face(face):
        if face is None or getattr(face, "size", 0) == 0:
            raise ValueError("Cannot preprocess an empty face")
        return cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
