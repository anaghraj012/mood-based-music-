import pytest

from src.face_detector import FaceDetector


def test_missing_cascade_is_reported(tmp_path):
    with pytest.raises(FileNotFoundError):
        FaceDetector(tmp_path / "missing.xml")
