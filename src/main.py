"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


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

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
