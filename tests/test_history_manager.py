from src.history_manager import HistoryManager


def test_history_round_trip_and_summary(tmp_path):
    manager = HistoryManager(tmp_path / "history.json")
    manager.save_analysis("image", "happy", 0.9, "energetic", "song.mp3")
    manager.save_analysis("webcam", "happy", 0.8, "energetic")
    assert len(manager.load_history()) == 2
    summary = manager.summary()
    assert summary["analyses"] == 2
    assert summary["most_frequent_emotion"] == "happy"
    assert summary["average_confidence"] == 0.85


def test_empty_summary_is_realistic(tmp_path):
    assert HistoryManager(tmp_path / "missing.json").summary()["analyses"] == 0
