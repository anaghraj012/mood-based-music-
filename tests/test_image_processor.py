import pytest

from src.image_processor import ImageProcessor


def test_missing_image_is_reported(tmp_path):
    with pytest.raises(FileNotFoundError):
        ImageProcessor().load_image(tmp_path / "missing.jpg")


def test_unsupported_image_is_reported(tmp_path):
    path = tmp_path / "file.txt"
    path.write_text("not an image")
    with pytest.raises(ValueError):
        ImageProcessor().load_image(path)
