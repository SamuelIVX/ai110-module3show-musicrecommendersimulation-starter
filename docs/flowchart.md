# Music Recommender — Data Flow Diagram

This diagram traces the full pipeline from user input and CSV catalog to ranked recommendations.

```mermaid
flowchart TD
    A([User Preferences\ngenre · mood · energy\nvalence · acousticness]) --> C

    B[(data/songs.csv\n20 songs)] -->|load_songs| D[Song Catalog\nList of Dicts]

    D --> E{For each song\nin catalog}
    C[User Prefs Dict] --> E

    E --> F[score_song\ncalculate weighted score]

    F --> F1[genre_match × 0.40]
    F --> F2[mood_match × 0.30]
    F --> F3[energy proximity × 0.15]
    F --> F4[valence proximity × 0.10]
    F --> F5[acousticness proximity × 0.05]

    F1 & F2 & F3 & F4 & F5 --> G[song score\n0.0 – 1.0]

    G --> H[scored_songs\nList of song · score pairs]
    E -->|repeat for all 20 songs| E

    H --> I[Sort descending\nby score]
    I --> J[Slice top-k\ndefault k=5]

    J --> K[explain_recommendation\nbuild reason string]
    K --> L([Output\ntitle · score · explanation\nprinted to terminal])

    style A fill:#4a90d9,color:#fff
    style B fill:#7b68ee,color:#fff
    style L fill:#27ae60,color:#fff
    style F fill:#e67e22,color:#fff
    style G fill:#e67e22,color:#fff
```

## Scoring Formula

```
score = (0.40 × genre_match)
      + (0.30 × mood_match)
      + (0.15 × energy_proximity)
      + (0.10 × valence_proximity)
      + (0.05 × acousticness_proximity)

where proximity = 1.0 - abs(user_value - song_value)
      match     = 1.0 if equal else 0.0
```

## Stage-by-Stage Summary

| Stage | Function | Input | Output |
|---|---|---|---|
| Load | `load_songs()` | `data/songs.csv` | `List[Dict]` — 20 song dicts |
| Score | `score_song()` | 1 song + user prefs | float 0.0–1.0 |
| Rank | `recommend_songs()` | all scored songs | sorted top-k list |
| Explain | `explain_recommendation()` | 1 song + user prefs | reason string |
