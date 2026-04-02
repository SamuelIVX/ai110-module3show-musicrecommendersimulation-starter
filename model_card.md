# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder 1.0 generates ranked song recommendations from a 20-song catalog based on a user's stated genre, mood, and energy preferences. It is designed for classroom exploration of content-based filtering concepts, not for production use. The system assumes the user can articulate their preferences in advance as explicit values (e.g. "I want pop, happy, energy 0.85") rather than learning from listening history. It makes no assumptions about demographics, listening context, or time of day.

---

## 3. How the Model Works

The recommender works like a judge scoring each song in a competition. Every song in the catalog is evaluated against the user's stated preferences and receives a score between 0.0 and 1.0. Songs that match the user's favorite genre earn up to 20 points out of 100; songs that match the mood earn up to 30 points. The remaining 50 points come from how close the song's energy, emotional tone (valence), and acoustic texture are to the user's targets — the closer the song's values, the higher the score. Once every song has been scored, they are sorted from highest to lowest and the top five are returned with a plain-language explanation of what contributed to each song's score.

---

## 4. Data

The catalog contains 20 songs across 16 distinct genres and 10 distinct moods. The original 10-song starter set was expanded with 10 additional songs to increase genre diversity. Despite this, the distribution is highly uneven: lofi appears 3 times, pop and ambient each appear twice, and 13 other genres appear only once. Moods are more balanced (happy, chill, intense, and moody each appear 3 times), but rare moods like romantic, peaceful, and melancholic each have only a single representative song. The catalog reflects a Western, digitally-produced music perspective — there are no classical, Latin, African, or K-pop entries, which would affect users with those tastes.

---

## 5. Strengths

The system works best when the user's preferred genre has multiple catalog entries and aligns cleanly with their mood target. Profile B (lofi/chill) produced the most intuitive results: Library Rain and Midnight Coding scored 0.99 and 0.98 respectively, and the gap between matched and unmatched songs was large and meaningful. The explanation strings are a genuine strength — every recommendation tells the user exactly which features matched and by how much, which makes the system transparent in a way that real black-box recommenders are not. For simple, well-represented taste profiles, VibeFinder reliably surfaces the right songs.

---

## 6. Limitations and Bias

**The primary weakness discovered through testing is the winner-take-all genre problem.** Because genre matching contributes 20 out of 100 possible points and most genres appear only once in the catalog, any user whose preferred genre has a single representative song will almost always receive that song as #1 — regardless of how poorly it matches their mood or energy. Iron Cathedral (metal/intense) scored 0.99 for the metal profile purely because it is the only metal song; even if its energy had been 0.40 instead of 0.97, it would still rank first.

A second bias is that exact string matching for genre and mood creates invisible penalization. "Dance pop" and "indie pop" receive zero genre credit against a "pop" profile despite being sonically very close. Users who would genuinely enjoy these songs are shown a worse result than they deserve, and the system has no way to express that "rock" is closer to "metal" than "reggae" is. This means the recommender systematically underserves users whose taste sits near genre boundaries.

A third limitation is the absence of a diversity floor. All five recommendations can come from the same genre or share the same mood if those are the closest matches, creating a filter bubble. A user exploring new music will always be pushed back toward what they already said they liked, with no mechanism for serendipitous discovery.

---

## 7. Evaluation

Six user profiles were tested: three standard (high-energy pop, chill lofi, deep intense metal) and three adversarial edge cases (conflicting energy + mood, unknown genre, dead-center numeric values). For each profile, the top 5 results were inspected against musical intuition. The most revealing test was Profile E (genre = "classical", which does not exist in the catalog) — the system lost 20 points on every song and the top result scored only 0.59, barely ahead of the field. A weight-shift experiment was also run: halving genre weight (0.20) and doubling energy weight (0.30) improved rankings for near-genre matches like "dance pop" but allowed high-energy songs from unrelated genres to surface in low-energy profiles, confirming that the original genre weight is load-bearing even if too blunt.

---

## 8. Future Work

The most impactful improvement would be replacing exact string genre matching with a genre similarity graph — so that "rock" receives partial credit (e.g. 0.5) against a "metal" profile instead of zero. This alone would fix the winner-take-all problem and make the system useful for genre-adjacent users. A diversity constraint that prevents more than two songs from the same genre appearing in the top five would address the filter bubble issue. Adding listening context (time of day, activity type) as an optional profile field would make the numeric features more meaningful — a user who wants "chill" at 11pm means something different than one who wants it at 9am. Finally, replacing explicit user input with implicit signals (track skips, replays, playlist adds) would move the system toward the collaborative filtering approach that real platforms use.

---

## 9. Personal Reflection

Building VibeFinder made it clear how much of a recommendation is really just a set of design choices disguised as math. Choosing to weight genre at 0.40 versus 0.20 is not a neutral technical decision — it encodes a belief about how people relate to music, and that belief turns out to be partially wrong once you test it against real edge cases. The most surprising discovery was how badly the system degrades when a genre simply doesn't exist in the catalog, producing near-random results with no warning to the user. Real platforms like Spotify handle this gracefully because they have millions of songs — the cold-start problem is hidden by scale. At 20 songs, every gap in the dataset is immediately visible, which made the biases much easier to see and reason about than they would be in a production system.
