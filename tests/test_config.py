from src.config import PROJECT_ROOT


def test_paths_are_repository_relative():
    assert PROJECT_ROOT.name == "mood-based-music-"
    assert not str(PROJECT_ROOT).startswith("C:\\Users\\Anuj")
