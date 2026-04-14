from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from recommender import load_songs, recommend_songs, score_song, compute_confidence


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

    strong_score, _, strong_conf = score_song(user, strong_match_song)
    weak_score, _, weak_conf = score_song(user, weak_match_song)

    assert strong_score > weak_score
    assert strong_conf > weak_conf


def test_score_song_supports_typo_tolerant_label_matching():
    user = {"genre": "lo-fi", "mood": "chill", "energy": 0.3}
    song = {"title": "Lofi Track", "genre": "lofi", "mood": "chill", "energy": 0.3}

    _, reasons, _ = score_song(user, song)

    assert any("genre match" in reason for reason in reasons)
    assert any("mood match" in reason for reason in reasons)


def test_score_song_normalizes_out_of_range_user_energy():
    user = {"genre": "rock", "mood": "intense", "energy": 1.8}
    song = {"title": "Rock Track", "genre": "rock", "mood": "intense", "energy": 1.0}

    score, reasons, confidence = score_song(user, song)

    assert score >= 0
    assert any("normalized" in reason for reason in reasons)
    # Confidence should be lower due to normalized input
    assert confidence < 1.0


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
    _, _, explanation, _ = recommendations[0]

    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_confidence_score_is_in_valid_range():
    """Confidence should always be between 0.0 and 1.0."""
    user = {"genre": "pop", "mood": "happy", "energy": 0.8}
    songs = [
        {"title": "Perfect", "genre": "pop", "mood": "happy", "energy": 0.8},
        {"title": "Mismatch", "genre": "metal", "mood": "angry", "energy": 0.95},
        {"title": "Partial", "genre": "pop", "mood": "sad", "energy": 0.7},
    ]

    recommendations = recommend_songs(user, songs, k=3)

    for song, score, explanation, confidence in recommendations:
        assert 0.0 <= confidence <= 1.0, f"Invalid confidence {confidence} for {song['title']}"


def test_confidence_higher_for_strong_matches():
    """Strong matches (genre + mood + energy) should have higher confidence than weak matches."""
    user = {"genre": "pop", "mood": "happy", "energy": 0.8}
    strong_match = {"title": "Strong", "genre": "pop", "mood": "happy", "energy": 0.8}
    weak_match = {"title": "Weak", "genre": "metal", "mood": "angry", "energy": 0.2}

    strong_recommendations = recommend_songs(user, [strong_match], k=1)
    weak_recommendations = recommend_songs(user, [weak_match], k=1)

    strong_conf = strong_recommendations[0][3]
    weak_conf = weak_recommendations[0][3]

    assert strong_conf > weak_conf, f"Strong match confidence {strong_conf} should be > weak {weak_conf}"


def test_confidence_penalizes_missing_context():
    """Recommendations from incomplete user context should have lower confidence."""
    user_complete = {"genre": "pop", "mood": "happy", "energy": 0.8}
    user_incomplete = {"genre": "", "mood": "", "energy": 0.8}  # no genre or mood
    
    song = {"title": "Test", "genre": "pop", "mood": "happy", "energy": 0.8}

    complete_recommendations = recommend_songs(user_complete, [song], k=1)
    incomplete_recommendations = recommend_songs(user_incomplete, [song], k=1)

    complete_conf = complete_recommendations[0][3]
    incomplete_conf = incomplete_recommendations[0][3]

    assert complete_conf > incomplete_conf, \
        f"Complete context confidence {complete_conf} should be > incomplete {incomplete_conf}"


def test_accuracy_with_real_data():
    """Test accuracy on real song data with known user profile."""
    songs = load_songs(str(ROOT / "data" / "songs.csv"))
    
    # Profile: Pop + Happy should strongly match "Sunrise City"
    user = {"genre": "pop", "mood": "happy", "energy": 0.8}
    recommendations = recommend_songs(user, songs, k=1)
    
    top_song, _, _, confidence = recommendations[0]
    
    # "Sunrise City" should be recommended with high confidence
    assert top_song.get("title") == "Sunrise City", f"Expected Sunrise City, got {top_song.get('title')}"
    assert confidence > 0.7, f"Expected high confidence (>0.7), got {confidence:.2f}"
