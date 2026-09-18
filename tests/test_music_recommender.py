from src.music_recommender import MusicRecommender


def test_discovery_and_non_repeating_recommendation(tmp_path):
    mood_dir = tmp_path / "calm"
    mood_dir.mkdir()
    first = mood_dir / "one.mp3"
    second = mood_dir / "two.ogg"
    first.write_bytes(b"")
    second.write_bytes(b"")
    recommender = MusicRecommender(tmp_path)
    assert {path.name for path in recommender.discover("calm")} == {"one.mp3", "two.ogg"}
    choices = {recommender.recommend("calm").name for _ in range(2)}
    assert choices == {"one.mp3", "two.ogg"}
