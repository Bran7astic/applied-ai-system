import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from difflib import SequenceMatcher


def _normalize_label(value: str) -> str:
    """Normalize text for tolerant matching by removing punctuation and spacing differences."""
    cleaned = "".join(ch for ch in value.strip().lower() if ch.isalnum() or ch.isspace())
    return "".join(cleaned.split())


def _is_typo_tolerant_match(user_value: str, song_value: str, threshold: float = 0.82) -> bool:
    """Return True when two labels are exact or close enough under typo-tolerant matching."""
    normalized_user = _normalize_label(user_value)
    normalized_song = _normalize_label(song_value)

    if not normalized_user or not normalized_song:
        return False
    if normalized_user == normalized_song:
        return True

    similarity = SequenceMatcher(None, normalized_user, normalized_song).ratio()
    return similarity >= threshold


def _normalize_energy(value: float) -> float:
    """Clamp energy values to the supported [0.0, 1.0] range."""
    return max(0.0, min(1.0, value))

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs and attributes from a CSV file into a list of dictionaries."""
    songs: List[Dict] = []

    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            song: Dict = {}
            for key, value in row.items():
                cleaned_value = value.strip() if isinstance(value, str) else value
                if cleaned_value == "":
                    song[key] = cleaned_value
                    continue

                try:
                    song[key] = float(cleaned_value)
                except (TypeError, ValueError):
                    song[key] = cleaned_value

            songs.append(song)

    return songs

def compute_confidence(user_prefs: Dict, song: Dict, score: float) -> float:
    """
    Compute confidence score (0.0 to 1.0) based on match strength and input validity.
    
    Confidence factors:
    - Genre and mood matches (categorical certainty)
    - Energy similarity (numeric closeness)
    - Input completeness and validity
    """
    user_genre = str(user_prefs.get("genre", "")).strip()
    user_mood = str(user_prefs.get("mood", "")).strip()
    raw_target_energy = float(user_prefs.get("energy", 0.0))
    target_energy = _normalize_energy(raw_target_energy)

    song_genre = str(song.get("genre", "")).strip()
    song_mood = str(song.get("mood", "")).strip()
    song_energy = float(song.get("energy", 0.0))

    # Category match confidence (binary): 0.3 each if matched
    category_confidence = 0.0
    if user_genre and _is_typo_tolerant_match(user_genre, song_genre):
        category_confidence += 0.3
    if user_mood and _is_typo_tolerant_match(user_mood, song_mood):
        category_confidence += 0.3

    # Energy similarity confidence: 0.4 based on closeness
    energy_similarity = max(0.0, 1.0 - abs(target_energy - song_energy))
    energy_confidence = energy_similarity * 0.4

    # Input validity confidence: 0.0 if input was invalid/out-of-range, 0.0 otherwise
    input_validity = 1.0 if raw_target_energy == target_energy else 0.85  # penalty for normalization

    # Combined confidence clamped to [0.0, 1.0]
    confidence = (category_confidence + energy_confidence) * input_validity
    return min(1.0, max(0.0, confidence))


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str], float]:
    """Score one song using genre, mood, and energy similarity against user preferences."""
    genre_weight = 1.0
    mood_weight = 1.0
    energy_weight = 2.0

    score = 0.0
    reasons: List[str] = []

    user_genre = str(user_prefs.get("genre", "")).strip()
    user_mood = str(user_prefs.get("mood", "")).strip()
    raw_target_energy = float(user_prefs.get("energy", 0.0))
    target_energy = _normalize_energy(raw_target_energy)

    song_genre = str(song.get("genre", "")).strip()
    song_mood = str(song.get("mood", "")).strip()
    song_energy = float(song.get("energy", 0.0))

    if _is_typo_tolerant_match(user_genre, song_genre):
        score += genre_weight
        reasons.append(f"genre match (typo-tolerant)! (+{genre_weight:.1f})")
    else:
        reasons.append("genre mismatch (+0.0)")

    if _is_typo_tolerant_match(user_mood, song_mood):
        score += mood_weight
        reasons.append(f"mood match (typo-tolerant)! (+{mood_weight:.1f})")
    else:
        reasons.append("mood mismatch (+0.0)")

    energy_similarity = max(0.0, 1.0 - abs(target_energy - song_energy))
    weighted_energy = energy_similarity * energy_weight
    score += weighted_energy
    reasons.append(f"energy similarity (+{weighted_energy:.2f})")
    if target_energy != raw_target_energy:
        reasons.append(f"user energy normalized from {raw_target_energy:.2f} to {target_energy:.2f}")

    confidence = compute_confidence(user_prefs, song, score)
    return score, reasons, confidence

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str, float]]:
    """Rank songs by score and return the top k recommendations with explanations and confidence scores."""
    scored_songs: List[Tuple[Dict, float, str, float]] = []

    for song in songs:
        score, reasons, confidence = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored_songs.append((song, score, explanation, confidence))

    scored_songs.sort(key=lambda item: item[1], reverse=True)
    return scored_songs[:k]
