"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from recommender import load_songs, recommend_songs
except ModuleNotFoundError:
    from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # --- User Profiles ---
    # Each profile targets a distinct region of the song catalog.
    # Swap which one is active to test different recommendation outcomes.

    # Profile A: High-energy pop fan — expects Gym Hero, Neon Carnival, Sunrise City
    user_prefs = {
        "genre":        "pop",
        "mood":         "happy",
        "energy":       0.85,   # wants driving, high-energy tracks
        "valence":      0.80,   # emotionally positive / upbeat
        "acousticness": 0.10,   # prefers produced/electronic over acoustic
    }

    # Profile B: Late-night chill listener — expects lofi, ambient, jazz results
    # user_prefs = {
    #     "genre":        "lofi",
    #     "mood":         "chill",
    #     "energy":       0.38,   # low-energy background listening
    #     "valence":      0.60,   # neutral-to-warm, not intense
    #     "acousticness": 0.80,   # prefers organic, mellow textures
    # }

    # Profile C: Intense/dark listener — expects metal, rock, moody electronic
    # user_prefs = {
    #     "genre":        "metal",
    #     "mood":         "intense",
    #     "energy":       0.95,   # maximum energy
    #     "valence":      0.35,   # low valence = dark, aggressive tone
    #     "acousticness": 0.05,   # fully produced/distorted, nothing acoustic
    # }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    # --- Header ---
    profile_summary = (
        f"genre={user_prefs.get('genre','?')}  "
        f"mood={user_prefs.get('mood','?')}  "
        f"energy={user_prefs.get('energy','?')}"
    )
    print("\n" + "=" * 60)
    print("  MUSIC RECOMMENDER — Top 5 Results")
    print(f"  Profile: {profile_summary}")
    print("=" * 60)

    # --- Results ---
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        bar = "#" * int(score * 20)   # 20-char ASCII progress bar
        print(f"\n  #{rank}  {song['title']}  ({song['artist']})")
        print(f"       Score : {score:.2f}  [{bar:<20}]")
        print(f"       Genre : {song['genre']}   Mood: {song['mood']}")
        print("       Why   :")
        for reason in explanation.split(" | "):
            print(f"               - {reason}")

    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
