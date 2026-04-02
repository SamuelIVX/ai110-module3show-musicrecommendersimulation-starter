from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

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
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":            int(row["id"]),
                "title":         row["title"],
                "artist":        row["artist"],
                "genre":         row["genre"].strip().lower(),
                "mood":          row["mood"].strip().lower(),
                "energy":        float(row["energy"]),
                "tempo_bpm":     float(row["tempo_bpm"]),
                "valence":       float(row["valence"]),
                "danceability":  float(row["danceability"]),
                "acousticness":  float(row["acousticness"]),
            })
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.

    Returns:
        (score, reasons) where score is 0.0–1.0 and reasons is a list
        of strings explaining each component's contribution.

    Weights (sum to 1.0):
        genre        0.40
        mood         0.30
        energy       0.15
        valence      0.10
        acousticness 0.05
    """
    score = 0.0
    reasons = []

    # --- Genre match (0.40) ---
    if song["genre"] == user_prefs.get("genre", "").lower():
        score += 0.40
        reasons.append(f"genre match ({song['genre']}) +0.40")
    else:
        reasons.append(f"genre mismatch ({song['genre']} ≠ {user_prefs.get('genre', '?')}) +0.00")

    # --- Mood match (0.30) ---
    if song["mood"] == user_prefs.get("mood", "").lower():
        score += 0.30
        reasons.append(f"mood match ({song['mood']}) +0.30")
    else:
        reasons.append(f"mood mismatch ({song['mood']} ≠ {user_prefs.get('mood', '?')}) +0.00")

    # --- Energy proximity (0.15) ---
    if "energy" in user_prefs:
        energy_proximity = 1.0 - abs(user_prefs["energy"] - song["energy"])
        contribution = round(energy_proximity * 0.15, 3)
        score += contribution
        reasons.append(
            f"energy {song['energy']:.2f} vs target {user_prefs['energy']:.2f} → +{contribution:.3f}"
        )

    # --- Valence proximity (0.10) ---
    if "valence" in user_prefs:
        valence_proximity = 1.0 - abs(user_prefs["valence"] - song["valence"])
        contribution = round(valence_proximity * 0.10, 3)
        score += contribution
        reasons.append(
            f"valence {song['valence']:.2f} vs target {user_prefs['valence']:.2f} → +{contribution:.3f}"
        )

    # --- Acousticness proximity (0.05) ---
    if "acousticness" in user_prefs:
        acousticness_proximity = 1.0 - abs(user_prefs["acousticness"] - song["acousticness"])
        contribution = round(acousticness_proximity * 0.05, 3)
        score += contribution
        reasons.append(
            f"acousticness {song['acousticness']:.2f} vs target {user_prefs['acousticness']:.2f} → +{contribution:.3f}"
        )

    return round(score, 4), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Scores every song, sorts descending, and returns the top-k results.
    Required by src/main.py

    Return format: list of (song_dict, score, explanation_string)
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = " | ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
