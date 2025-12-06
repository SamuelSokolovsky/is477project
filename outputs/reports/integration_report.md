# Data Integration Report

**Generated:** 2025-12-06 17:06:51

---

## Summary

- **Total Matches:** 57,865
- **Date Range:** 1993-07-23 00:00:00 to 2025-11-09 00:00:00
- **Seasons:** 34
- **Leagues:** 5
- **Teams:** 244
- **Total Columns:** 38

## Schema

### Core Fields

- `match_id`: Unique identifier (MD5 hash)
- `match_date`: Match date (YYYY-MM-DD)
- `season`: Season (e.g., 2023-2024)
- `league`: League name
- `home_team`, `away_team`: Standardized team names
- `home_goals`, `away_goals`: Full-time goals
- `result`: H (Home win), A (Away win), D (Draw)

### Statistics Fields

- Shots: `home_shots`, `away_shots`, `*_shots_on_target`
- Fouls: `home_fouls`, `away_fouls`
- Cards: `*_yellow_cards`, `*_red_cards`
- Corners: `home_corners`, `away_corners`

### Derived Features

- `goal_differential`: home_goals - away_goals
- `shot_differential`: home_shots - away_shots
- `*_shot_accuracy`: shots_on_target / total_shots
- `card_differential`: Weighted card difference
- `total_goals`: Total goals in match
- `home_win`, `away_win`, `draw`: Binary indicators

---

## Validation Results

**Status:** Some validation checks FAILED

### Checks

- [PASS] `record_count_match`
- [PASS] `no_duplicate_ids`
- [PASS] `no_missing_goals`
- [FAIL] `no_missing_dates`
- [PASS] `valid_results`

### Data Completeness

| Field | Completeness |
|-------|-------------|
| `home_shots` | 69.0% |
| `home_shots_on_target` | 67.4% |
| `home_fouls` | 67.7% |
| `home_yellow_cards` | 100.0% |
| `referee` | 19.0% |

---

## League Breakdown

| League | Matches | Seasons | Teams |
|--------|---------|---------|-------|
| bundesliga | 9,882 | 33 | 45 |
| la-liga | 12,444 | 33 | 49 |
| ligue-1 | 11,649 | 34 | 46 |
| premier-league | 12,434 | 33 | 51 |
| serie-a | 11,456 | 33 | 53 |

---

## Next Steps

1. Run `04_quality.py` for comprehensive quality assessment
2. Proceed to feature engineering and analysis in `05_analyze.py`
3. Generate visualizations with `06_visualize.py`

