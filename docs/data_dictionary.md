# Data Dictionary
## Integrated European Soccer Dataset

### Overview
This document describes all fields in the integrated soccer dataset.

Last updated: [DATE]

---

## Match Identification

| Column Name | Data Type | Description | Valid Range/Values | Source |
|------------|-----------|-------------|-------------------|---------|
| `match_id` | string | Unique identifier for each match | UUID format | Generated |
| `date` | datetime | Match date | 1993-08-01 to 2025-12-31 | Both datasets |
| `season` | string | Season identifier | Format: YYYY-YYYY (e.g., 2023-2024) | Both datasets |
| `league_name` | string | League name | Premier League, La Liga, Bundesliga, Serie A, Ligue 1 | Both datasets |

---

## Team Information

| Column Name | Data Type | Description | Valid Range/Values | Source |
|------------|-----------|-------------|-------------------|---------|
| `home_team` | string | Home team name (standardized) | See team_name_mappings.csv | Both datasets |
| `away_team` | string | Away team name (standardized) | See team_name_mappings.csv | Both datasets |

---

## Match Outcome

| Column Name | Data Type | Description | Valid Range/Values | Source |
|------------|-----------|-------------|-------------------|---------|
| `home_goals` | integer | Goals scored by home team | ≥ 0 | Both datasets |
| `away_goals` | integer | Goals scored by away team | ≥ 0 | Both datasets |
| `result` | string | Match result | H (Home win), A (Away win), D (Draw) | Both datasets |

---

## Shot Statistics

| Column Name | Data Type | Description | Valid Range/Values | Source |
|------------|-----------|-------------|-------------------|---------|
| `home_shots` | integer | Total shots by home team | ≥ 0 | Dataset 2 |
| `away_shots` | integer | Total shots by away team | ≥ 0 | Dataset 2 |
| `home_shots_on_target` | integer | Shots on target by home team | 0 ≤ value ≤ home_shots | Dataset 2 |
| `away_shots_on_target` | integer | Shots on target by away team | 0 ≤ value ≤ away_shots | Dataset 2 |

---

## Disciplinary Statistics

| Column Name | Data Type | Description | Valid Range/Values | Source |
|------------|-----------|-------------|-------------------|---------|
| `home_fouls` | integer | Fouls committed by home team | ≥ 0 | Dataset 2 |
| `away_fouls` | integer | Fouls committed by away team | ≥ 0 | Dataset 2 |
| `home_yellow_cards` | integer | Yellow cards issued to home team | ≥ 0 | Dataset 2 |
| `away_yellow_cards` | integer | Yellow cards issued to away team | ≥ 0 | Dataset 2 |
| `home_red_cards` | integer | Red cards issued to home team | ≥ 0 | Dataset 2 |
| `away_red_cards` | integer | Red cards issued to away team | ≥ 0 | Dataset 2 |

---

## Derived Features

| Column Name | Data Type | Description | Valid Range/Values | Source |
|------------|-----------|-------------|-------------------|---------|
| `shots_accuracy_home` | float | Home shots on target / home shots | 0.0 - 1.0 | Derived |
| `shots_accuracy_away` | float | Away shots on target / away shots | 0.0 - 1.0 | Derived |
| `shots_differential` | integer | home_shots - away_shots | Any integer | Derived |
| `goal_differential` | integer | home_goals - away_goals | Any integer | Derived |
| `cards_differential` | integer | (home_yellow + home_red*2) - (away_yellow + away_red*2) | Any integer | Derived |

---

## Data Quality Notes

### Missing Values
- Missing shot statistics: ~15% of records (older seasons)
- Missing card data: ~8% of records
- No missing data for goals or match results

### Data Transformations
- All team names standardized to lowercase
- Special characters removed from team names
- Dates converted to ISO 8601 format (YYYY-MM-DD)

### Known Issues
- Some early season records (pre-2000) have incomplete statistics
- Team name variations required fuzzy matching
- Betting odds excluded from integrated dataset

---

## References
- Dataset 1: ESPN Soccer Data (Kaggle)
- Dataset 2: Football-Data.co.uk Historical Results
