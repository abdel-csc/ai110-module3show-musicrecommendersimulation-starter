from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv


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
        """Score all songs and return the top k for this user."""
        scored = []
        for song in self.songs:
            score = 0.0
            if song.genre.lower() == user.favorite_genre.lower():
                score += 2.0
            if song.mood.lower() == user.favorite_mood.lower():
                score += 1.0
            energy_similarity = 1 - abs(song.energy - user.target_energy)
            score += energy_similarity
            if user.likes_acoustic and song.acousticness > 0.5:
                score += 0.5
            scored.append((song, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, score in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain why a song was recommended to this user."""
        reasons = []
        if song.genre.lower() == user.favorite_genre.lower():
            reasons.append("genre match (+2.0)")
        if song.mood.lower() == user.favorite_mood.lower():
            reasons.append("mood match (+1.0)")
        energy_similarity = 1 - abs(song.energy - user.target_energy)
        reasons.append(f"energy similarity (+{energy_similarity:.2f})")
        if user.likes_acoustic and song.acousticness > 0.5:
            reasons.append("acoustic preference match (+0.5)")
        return ", ".join(reasons) if reasons else "general recommendation"


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['id'] = int(row['id'])
            row['energy'] = float(row['energy'])
            row['tempo_bpm'] = float(row['tempo_bpm'])
            row['valence'] = float(row['valence'])
            row['danceability'] = float(row['danceability'])
            row['acousticness'] = float(row['acousticness'])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """Score a single song against user preferences. Returns (score, explanation)."""
    score = 0.0
    reasons = []

    if song['genre'].lower() == user_prefs['genre'].lower():
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song['mood'].lower() == user_prefs['mood'].lower():
        score += 1.0
        reasons.append("mood match (+1.0)")

    energy_similarity = 1 - abs(song['energy'] - user_prefs['energy'])
    score += energy_similarity
    reasons.append(f"energy similarity (+{energy_similarity:.2f})")

    return score, ", ".join(reasons)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, explanation = score_song(user_prefs, song)
        scored.append((song, score, explanation))

    # sorted() returns a new sorted list without modifying the original
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return ranked[:k]
