from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from recommender import load_songs, recommend_songs, score_song


def test_load_songs_reads_csv_and_parses_numeric_fields():
    songs = load_songs(str(ROOT / "data" / "songs.csv"))

    assert len(songs) > 0
    first = songs[0]
    assert "title" in first
    assert "genre" in first
    assert "mood" in first
    assert isinstance(first["energy"], float)


def test_score_song_gives_higher_score_for_stronger_match():
    user = {"genre": "pop", "mood": "happy", "energy": 0.8}
    strong_match_song = {"title": "A", "genre": "pop", "mood": "happy", "energy": 0.8}
    weak_match_song = {"title": "B", "genre": "rock", "mood": "sad", "energy": 0.2}

    strong_score, _ = score_song(user, strong_match_song)
    weak_score, _ = score_song(user, weak_match_song)

    assert strong_score > weak_score


def test_score_song_supports_typo_tolerant_label_matching():
    user = {"genre": "lo-fi", "mood": "chill", "energy": 0.3}
    song = {"title": "Lofi Track", "genre": "lofi", "mood": "chill", "energy": 0.3}

    _, reasons = score_song(user, song)

    assert any("genre match" in reason for reason in reasons)
    assert any("mood match" in reason for reason in reasons)


def test_score_song_normalizes_out_of_range_user_energy():
    user = {"genre": "rock", "mood": "intense", "energy": 1.8}
    song = {"title": "Rock Track", "genre": "rock", "mood": "intense", "energy": 1.0}

    score, reasons = score_song(user, song)

    assert score >= 0
    assert any("normalized" in reason for reason in reasons)


def test_recommend_songs_returns_top_k_in_descending_score_order():
    user = {"genre": "pop", "mood": "happy", "energy": 0.8}
    songs = [
        {"title": "Top", "genre": "pop", "mood": "happy", "energy": 0.8},
        {"title": "Mid", "genre": "pop", "mood": "happy", "energy": 0.5},
        {"title": "Low", "genre": "rock", "mood": "sad", "energy": 0.2},
    ]

    recommendations = recommend_songs(user, songs, k=2)

    assert len(recommendations) == 2
    assert recommendations[0][1] >= recommendations[1][1]
    assert recommendations[0][0]["title"] == "Top"


def test_recommend_songs_includes_human_readable_explanations():
    user = {"genre": "pop", "mood": "happy", "energy": 0.8}
    songs = [{"title": "Song", "genre": "pop", "mood": "happy", "energy": 0.8}]

    recommendations = recommend_songs(user, songs, k=1)
    _, _, explanation = recommendations[0]

    assert isinstance(explanation, str)
    assert explanation.strip() != ""
