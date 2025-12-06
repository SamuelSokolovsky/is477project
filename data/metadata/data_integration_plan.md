# Data Integration Plan
## Soccer Analytics Project

**Created:** 2025-12-06
**Purpose:** Document which CSV files will be used for data integration

---

## Files for Integration

### Dataset 1: ESPN Soccer Data (Kaggle)
**Location:** `data/raw/Dataset 1/`

| File Name | Purpose | Key Columns |
|-----------|---------|-------------|
| `teams.csv` | Team information | teamId, name, location, abbreviation, displayName |
| `teamStats.csv` | Team performance statistics | Team stats per season |
| `standings.csv` | League standings | Team rankings and points |
| `leagues.csv` | League information | League names and metadata |

**Source:** https://www.kaggle.com/datasets/excel4soccer/espn-soccer-data

---

### Dataset 2: Football-Data.co.uk Historical Results
**Location:** `data/raw/Dataset 2/football-datasets/datasets/`

| File Name | Purpose | Key Columns |
|-----------|---------|-------------|
| `all_leagues_all_seasons.csv` | Consolidated match results for all 5 leagues (1993-2025) | Date, HomeTeam, AwayTeam, FTHG, FTAG, FTR, HS, AS, HST, AST, HF, AF, HC, AC, HY, AY, HR, AR |

**Leagues Included:**
- Premier League (England)
- La Liga (Spain)
- Bundesliga (Germany)
- Serie A (Italy)
- Ligue 1 (France)

**Source:** https://github.com/datasets/football-datasets
**License:** PDDL 1.0 (Public Domain)

---

## Column Mapping

### Dataset 2 Key Columns Explained

| Column | Full Name | Description |
|--------|-----------|-------------|
| Date | Match Date | Date when match was played |
| HomeTeam | Home Team Name | Name of home team |
| AwayTeam | Away Team Name | Name of away team |
| FTHG | Full Time Home Goals | Goals scored by home team |
| FTAG | Full Time Away Goals | Goals scored by away team |
| FTR | Full Time Result | H (Home win), A (Away win), D (Draw) |
| HTHG | Half Time Home Goals | Goals at half time |
| HTAG | Half Time Away Goals | Goals at half time |
| HTR | Half Time Result | Result at half time |
| HS | Home Shots | Total shots by home team |
| AS | Away Shots | Total shots by away team |
| HST | Home Shots on Target | Shots on target by home team |
| AST | Away Shots on Target | Shots on target by away team |
| HF | Home Fouls | Fouls committed by home team |
| AF | Away Fouls | Fouls committed by away team |
| HC | Home Corners | Corner kicks for home team |
| AC | Away Corners | Corner kicks for away team |
| HY | Home Yellow Cards | Yellow cards issued to home team |
| AY | Away Yellow Cards | Yellow cards issued to away team |
| HR | Home Red Cards | Red cards issued to home team |
| AR | Away Red Cards | Red cards issued to away team |
| Referee | Referee Name | Name of match referee |

---

## Integration Strategy

### Step 1: Load Data
- Load all 4 CSV files from Dataset 1
- Load `all_leagues_all_seasons.csv` from Dataset 2

### Step 2: Team Name Standardization
- Standardize team names across both datasets
- Create mapping dictionary for aliases
- Handle variations (e.g., "Man United" → "Manchester United")

### Step 3: Schema Alignment
Create unified schema with fields:
- match_id (generated)
- date, home_team, away_team
- league_name, season
- home_goals, away_goals, result
- shots statistics (total, on target)
- disciplinary stats (fouls, cards)

### Step 4: Merge Datasets
- Join on common fields: team names, season, league
- Use outer join to preserve all records
- Track data source with merge indicator

---

## Files to IGNORE

From Dataset 2, **DO NOT USE**:
- Any file with `[invalid]` in the filename
- Individual season files (season-XXXX.csv)
- League-specific consolidated files (e.g., premier-league_all_seasons.csv)

**Use ONLY:** `all_leagues_all_seasons.csv`

---

## Expected Output

**Integrated Dataset:** `data/processed/integrated_dataset.csv`

**Expected Features:**
- ~10,000+ match records (spanning 1993-2025)
- 5 European leagues
- Complete statistics per match
- Standardized team names
- Quality-checked data

---

## Next Steps

1. Run `scripts/01_acquire.py` - Verify and checksum files
2. Run `scripts/02_clean.py` - Clean and standardize team names
3. Run `scripts/03_integrate.py` - Merge datasets into unified schema
4. Run `scripts/04_quality.py` - Assess data quality
5. Run `scripts/05_analyze.py` - Feature engineering and modeling
6. Run `scripts/06_visualize.py` - Generate visualizations
