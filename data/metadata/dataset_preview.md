# Integrated Soccer Dataset - Preview & Statistics

**Generated:** 2025-12-06
**Dataset:** `data/processed/integrated_dataset.csv`

---

## Dataset Overview

- **Total Matches:** 57,865
- **Date Range:** 1993-07-23 to 2025-11-09 (32+ years)
- **Total Goals Scored:** 154,781
- **Average Goals per Match:** 2.67
- **Unique Teams:** 244
- **Leagues:** 5 (Bundesliga, La Liga, Ligue 1, Premier League, Serie A)
- **Seasons:** 34
- **Features:** 38 columns (27 core + 11 derived)

---

## Match Outcome Statistics

| Outcome | Count | Percentage |
|---------|-------|------------|
| Home Wins | 26,739 | 46.2% |
| Away Wins | 15,825 | 27.3% |
| Draws | 15,301 | 26.4% |

**Home Advantage:**
- Home teams score 1.54 goals/match on average
- Away teams score 1.14 goals/match on average
- Clear home advantage across all leagues

---

## League Breakdown

| League | Matches | Seasons | Teams | Avg Goals | Home Win % | Draw % |
|--------|---------|---------|-------|-----------|-----------|--------|
| Bundesliga | 9,882 | 33 | 45 | 2.94 | 46.0% | 25.0% |
| La Liga | 12,444 | 33 | 49 | 2.66 | 47.0% | 26.0% |
| Ligue 1 | 11,649 | 34 | 46 | 2.47 | 46.0% | 28.0% |
| Premier League | 12,434 | 33 | 51 | 2.70 | 46.0% | 25.0% |
| Serie A | 11,456 | 33 | 53 | 2.66 | 45.0% | 28.0% |

**Observations:**
- Bundesliga has highest average goals (2.94)
- Ligue 1 has lowest average goals (2.47)
- La Liga has highest home win rate (47.0%)
- Ligue 1 and Serie A have most draws (~28%)

---

## Top Scoring Teams (All-Time)

1. Barcelona - 2,814 goals
2. Real Madrid - 2,683 goals
3. Bayern Munich - 2,545 goals
4. Manchester United - 2,296 goals
5. Arsenal - 2,245 goals
6. Liverpool - 2,224 goals
7. Chelsea - 2,122 goals
8. Paris Saint-Germain - 2,113 goals
9. Inter Milan - 2,092 goals
10. Borussia Dortmund - 2,068 goals

---

## Scoring Statistics

- **Most Common Score:** 1-1 (7,039 matches)
- **Highest Scoring Match:** Real Madrid 10-2 Vallecano (2015-12-20) - 12 goals
- **Goalless Draws:** 4,665 matches
- **Matches with 5+ Goals:** 7,871 (13.6%)
- **Average Goals per Match:** 2.67

**Other High-Scoring Matches:**
- Bayern Munich 9-2 Hamburg (2013-03-30) - 11 goals
- Schalke 04 7-4 Leverkusen (2006-02-11) - 11 goals
- Portsmouth 7-4 Reading (2007-09-29) - 11 goals

---

## Disciplinary Statistics

- **Matches with Red Cards:** 7,566 (13.1%)
- **Matches with Multiple Reds:** 1,105
- **Average Yellow Cards:** ~2-3 per match (varies by league)

**Most Aggressive Teams (Cards per Match):**
1. Getafe - 3.18 cards/match
2. Granada - 3.11 cards/match
3. Elche - 3.00 cards/match

---

## Temporal Trends

**Goals per Match by Decade:**
- 1990s: 2.62 goals/match (47.9% home wins, 28.5% draws)
- 2000s: 2.59 goals/match (47.1% home wins, 27.0% draws)
- 2010s: 2.71 goals/match (46.0% home wins, 25.3% draws)
- 2020s: 2.81 goals/match (42.9% home wins, 25.3% draws)

**Observations:**
- Goals per match increasing in recent decades
- Home advantage slightly decreasing
- Draws becoming slightly less common

---

## Data Completeness

| Category | Completeness | Notes |
|----------|-------------|-------|
| Match Info (date, teams, league) | 99.8-100% | Nearly perfect |
| Goals & Results | 100% | Complete |
| Yellow/Red Cards | 100% | Missing filled with 0 |
| Shots | 69.0% | Older seasons missing |
| Shots on Target | 67.4% | Older seasons missing |
| Fouls | 67.7% | Older seasons missing |
| Referee | 19.0% | Many matches don't record |
| Halftime Stats | 93.4% | Most matches have |

**Why Missing Data?**
- Older seasons (1990s-early 2000s) didn't track detailed statistics
- Modern matches (2010+) have nearly complete shot/foul data
- Referee names often not recorded in older datasets

---

## Derived Features Available

The dataset includes 11 engineered features:

1. **goal_differential** - Home goals minus away goals
2. **shot_differential** - Home shots minus away shots
3. **home_shot_accuracy** - Home shots on target / total shots
4. **away_shot_accuracy** - Away shots on target / total shots
5. **home_total_cards** - Weighted cards (yellow=1, red=2)
6. **away_total_cards** - Weighted cards (yellow=1, red=2)
7. **card_differential** - Home cards minus away cards
8. **total_goals** - Total goals in match
9. **home_win** - Binary indicator (1 if home win)
10. **away_win** - Binary indicator (1 if away win)
11. **draw** - Binary indicator (1 if draw)

---

## Use Cases

This dataset is ready for:

**Predictive Modeling:**
- Match outcome prediction (Home/Away/Draw)
- Goals prediction (over/under)
- Shot accuracy modeling
- Disciplinary incident prediction

**Exploratory Analysis:**
- Home advantage quantification
- League comparisons
- Team performance trends
- Tactical evolution over time

**Visualization:**
- Performance heatmaps
- Temporal trend charts
- League comparison plots
- Team statistics dashboards

---

## Next Steps

1. **Quality Assessment** - Comprehensive quality profiling
2. **Feature Engineering** - Create rolling averages, form metrics
3. **Predictive Modeling** - Build classifiers for match outcomes
4. **Visualization** - Generate publication-ready charts

---

## Sample Records

```
match_id         | date       | home_team      | away_team     | result | goals
e40c737d8a6f1932 | 1999-08-13 | duisburg       | leverkusen    | D      | 0-0
cd06a130e3185f7c | 1999-08-13 | wolfsburg      | munich 1860   | H      | 2-1
67819a2077076139 | 1999-08-14 | bayern munich  | hamburg       | D      | 2-2
```

---

**Dataset Location:** `data/processed/integrated_dataset.csv` (9.9 MB)
**Integration Report:** `outputs/reports/integration_report.md`
