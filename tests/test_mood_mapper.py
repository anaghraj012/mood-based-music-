import pytest

from src.mood_mapper import MoodMapper


def test_maps_emotion_to_mood():
    assert MoodMapper().map_emotion("happy") == "energetic"


def test_rejects_unknown_emotion():
    with pytest.raises(ValueError):
        MoodMapper().map_emotion("unknown")
