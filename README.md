# Integrated European Soccer Analytics Project

**Predictive Modeling and Performance Analysis Across 32 Years of European Soccer**

## Contributors
- [Your Name] ([ORCID](https://orcid.org/))
- Course: IS 477 - Data Management, Curation, and Reproducibility
- Institution: University of Illinois Urbana-Champaign
- Semester: Fall 2025

## Summary

This project presents a comprehensive, reproducible data science pipeline for soccer analytics, integrating multiple datasets spanning 32 years (1993-2025) and 57,865 matches across Europe's top 5 leagues. We demonstrate end-to-end data management practices including acquisition validation, systematic cleaning, schema integration, quality assessment, predictive modeling, and publication-quality visualization.

### Project Goals

1. **Data Integration:** Merge heterogeneous soccer datasets with different schemas, team name conventions, and temporal coverage
2. **Quality Assessment:** Apply rigorous data quality framework across 5 dimensions (completeness, validity, consistency, accuracy, uniqueness)
3. **Predictive Analytics:** Build machine learning models to predict match outcomes using match statistics
4. **Reproducibility:** Create fully automated, well-documented pipeline following best practices

### Methodology

Our 6-phase pipeline processes data through:
- **Phase 1:** Data acquisition with SHA-256 checksum verification
- **Phase 2:** Systematic cleaning with team name standardization (244 teams mapped)
- **Phase 3:** Schema integration producing unified 38-column dataset
- **Phase 4:** Multi-dimensional quality assessment with automated reporting
- **Phase 5:** Predictive modeling (Logistic Regression, Random Forest, Gradient Boosting)
- **Phase 6:** Comprehensive visualization suite (7 publication-quality figures)

### Key Findings

Our analysis reveals:
- **Predictive models achieved 58.9% accuracy**, dramatically outperforming random baseline (33%)
- **Home advantage is declining** over time: 48% home win rate in 1990s → 40-46% in 2020s
- **Away teams are scoring more**: Away goals increased from ~1.0 to ~1.35 per match (1995-2025)
- **Shot statistics dominate** prediction: Shots on target is the #1 predictor across all models
- **League variations exist**: La Liga and Serie A show strongest home advantage (~48%), while Premier League is most competitive (~45%)

## Data Profile

### Dataset Integration Overview

**Final Integrated Dataset:**
- **57,865 matches** across 32 years (1993-2025)
- **5 major leagues:** Premier League, La Liga, Bundesliga, Serie A, Ligue 1
- **244 unique teams** with standardized naming
- **38 features** including goals, shots, fouls, cards, corners, referee
- **154,781 total goals** scored (2.67 goals/match average)
- **11 derived features** for predictive modeling

### Dataset 1: Football-Data.co.uk Historical Results

- **Source:** [GitHub - Football Datasets](https://github.com/datasets/football-datasets)
- **Coverage:** 1993-2025, all major European leagues
- **File:** all_leagues_all_seasons.csv
- **Records:** 57,865 matches
- **Size:** 5.23 MB
- **Key Metrics:** Match results, goals, shots, shots on target, fouls, cards, corners, betting odds, referee assignments
- **License:** PDDL 1.0 (Public Domain Dedication and License)
- **Update Frequency:** Continuously updated with recent seasons
- **Data Quality:** High-quality official statistics with detailed match-level data available from ~2005 onwards

**Temporal Coverage:**
- 1993-1999: Basic match results (goals, final result)
- 2000-2004: Added card statistics
- 2005-present: Full statistics including shots, corners, fouls (66% of dataset)

### Dataset 2: ESPN Soccer Data (Supporting - Local)

- **Source:** [Kaggle - ESPN Soccer Data](https://www.kaggle.com/datasets/excel4soccer/espn-soccer-data)
- **Storage:** Stored locally in repository at `data/raw/Dataset 1/`
- **Files Used:** teams.csv (503 KB), teamStats.csv (11.24 MB), standings.csv (638 KB), leagues.csv (138 KB)
- **Purpose:** Team name standardization and league metadata
- **Total Size:** 12.5 MB across 4 files
- **License:** Community Data License Agreement (CDLA)
- **Note:** No Kaggle API credentials needed - files are included in the repository

### Data Structure

**Integrated Schema (38 columns):**

*Core Fields (8):*
- match_id, match_date, season, league, home_team, away_team, home_team_original, away_team_original

*Match Results (6):*
- home_goals, away_goals, result (H/D/A), halftime_home_goals, halftime_away_goals, halftime_result

*Shot Statistics (6):*
- home_shots, away_shots, home_shots_on_target, away_shots_on_target, home_shot_accuracy, away_shot_accuracy

*Other Match Events (8):*
- home_fouls, away_fouls, home_corners, away_corners, home_yellow_cards, away_yellow_cards, home_red_cards, away_red_cards

*Derived Features (11):*
- goal_differential, shot_differential, shots_on_target_differential, home_win (binary), away_win (binary), draw (binary), plus 5 more analytical features

*Metadata (1):*
- referee (81% missing - not assigned in older seasons)

## Data Quality

Our comprehensive quality assessment evaluated 57,865 matches across 5 dimensions following data quality framework principles:

### Overall Quality Status: **GOOD** (Minor issues detected)

### 1. Completeness Assessment

**Row-Level Completeness:**
- 10,825 matches (18.7%) have 100% complete data
- Average row completeness: 88.09%
- Completeness improved dramatically after 2005

**Field-Level Completeness:**
- Core match data (goals, results, teams, dates): **100% complete**
- Shot statistics (post-2005): 67.4% complete
- Card statistics (post-2000): 67.7% complete
- Referee assignments: 19% complete (81% missing)

**Top Missing Fields:**
| Field | Missing % | Complete % | Reason |
|-------|-----------|------------|--------|
| referee | 81.0% | 19.0% | Not recorded pre-2010 |
| away_shot_accuracy | 32.6% | 67.3% | Calculated from shots (unavailable pre-2005) |
| home_shots_on_target | 32.6% | 67.4% | Not recorded pre-2005 |
| home_fouls | 32.3% | 67.7% | Not recorded pre-2005 |
| away_corners | 31.7% | 68.3% | Not recorded pre-2005 |

**Verdict:** [FAIL] - Expected due to historical data evolution. Core fields 100% complete.

### 2. Validity Assessment

**Range Validation:**
- Goals ≥ 0: **PASS** (all valid)
- Shots ≥ Shots on Target: **2 issues detected**
  - Home: 2 cases where shots < shots on target (data entry error)
  - Away: 3 cases where shots < shots on target (data entry error)
- Cards are non-negative integers: **PASS**
- Dates in valid range (1990-2026): **PASS**
- Result codes (H/D/A only): **PASS**

**Verdict:** [WARN] - 5 shot data anomalies out of 38,236 complete matches (0.01%)

### 3. Consistency Assessment

**Cross-Field Validation:**
- Result matches goal differential: **PASS** (100% consistent)
- Shot accuracy within bounds [0, 1]: **1 issue** (rounding error)
- Derived fields match calculations: **PASS**

**Verdict:** [WARN] - 1 minor rounding issue in shot accuracy calculation

### 4. Accuracy Assessment

**Statistical Distribution Checks:**
- Mean goals per match: 2.67 (within expected range 2.4-3.0)
- Home win rate: 46.2% (typical home advantage)
- Away win rate: 27.3% (typical away disadvantage)
- Draw rate: 26.4% (typical draw frequency)

**Logical Impossibility Checks:**
- No negative statistics: **PASS**
- No impossible score combinations: **PASS**
- Temporal ordering valid: **PASS**

**Verdict:** [PASS] - 0 anomalies detected, all distributions match expected patterns

### 5. Uniqueness Assessment

**Duplicate Detection:**
- Unique matches: 57,865
- Total records: 57,865
- Uniqueness rate: **100.00%**
- Duplicate match IDs: **0**

**Verdict:** [PASS] - Perfect uniqueness, no duplicates

### Quality Assessment Conclusions

1. **Core data is excellent:** Goals, results, teams, dates are 100% complete and valid
2. **Missing data is expected:** Shot/foul statistics unavailable for older seasons (pre-2005)
3. **Minimal errors:** Only 6 total issues out of 57,865 matches (99.99% accuracy)
4. **Dataset is suitable for analysis** with proper handling of missing values
5. **Recommendation:** Filter to post-2005 data (38,236 matches) for complete statistics analysis

## Findings

### Predictive Model Performance

We trained three classification models to predict match outcomes (Home Win / Draw / Away Win):

**Dataset:**
- Training: 30,588 matches (2000-08-13 to 2021-09-12)
- Test: 7,648 matches (2021-09-12 to 2025-11-09)
- Temporal split ensures no data leakage

**Model Comparison:**

| Model | Accuracy | Precision | Recall | F1 Score | ROC AUC |
|-------|----------|-----------|--------|----------|----------|
| **Logistic Regression** | **58.89%** | 0.5455 | 0.5889 | 0.5318 | 0.7555 |
| **Random Forest** | 58.89% | 0.5543 | 0.5889 | 0.5467 | **0.7569** |
| **Gradient Boosting** | 58.22% | **0.5604** | 0.5822 | **0.5666** | **0.7576** |

**Key Insights:**
1. **All models significantly outperform random baseline** (33% for 3 classes)
2. **78% improvement over random guessing** (58.9% vs 33%)
3. **Gradient Boosting** achieves best ROC-AUC (0.7576) and F1 score (0.5666)
4. **Logistic Regression & Random Forest** tie for best accuracy (58.89%)

**Per-Class Performance (Logistic Regression):**

| Outcome | Precision | Recall | F1-Score | Support |
|---------|-----------|--------|----------|---------|
| Home Win (H) | 0.6149 | **0.8203** | 0.7029 | 3,367 |
| Away Win (A) | 0.5726 | 0.6803 | 0.6218 | 2,355 |
| Draw (D) | 0.3911 | 0.0727 | 0.1226 | 1,926 |

**Observations:**
- **Home wins are easiest to predict** (82% recall) - models capture home advantage well
- **Draws are hardest to predict** (only 7% recall) - inherently random/unpredictable
- **Class imbalance affects performance**: Home wins (44%) > Away wins (31%) > Draws (25%)

### Feature Importance Analysis

**Top 5 Most Important Predictors (Random Forest & Gradient Boosting):**

1. **Away shots on target** (20-25% importance)
2. **Home shots on target** (15-20% importance)
3. **Home shot accuracy** (12-15% importance)
4. **Away shot accuracy** (10-12% importance)
5. **Home corners** (4-6% importance)

**Insight:** Shot quality (shots on target) is far more predictive than shot quantity. This validates the "quality over quantity" principle in soccer analytics.

### League Comparisons

**Home Advantage by League:**
| League | Home Win % | Observations |
|--------|------------|---------------|
| **Serie A** | ~48% | Strongest home advantage |
| **La Liga** | ~48% | Strongest home advantage |
| **Bundesliga** | ~46% | Moderate home advantage |
| **Ligue 1** | ~46% | Moderate home advantage |
| **Premier League** | ~45% | Most competitive, lowest home advantage |

**Scoring Patterns:**
- **Bundesliga:** Highest goals per match (~2.8)
- **Serie A:** Lowest goals per match (~2.5) - defensive league
- **La Liga, Premier League, Ligue 1:** ~2.6-2.7 goals/match

**Card Discipline:**
- **La Liga:** Most yellow cards per match (highest foul rate)
- **Bundesliga:** Fewest yellow cards (cleanest play)

**Shot Accuracy:**
- Remarkably consistent across leagues (~33-35% shot accuracy)
- Slight edge to Premier League and Bundesliga

### Temporal Trends (1995-2025)

**Scoring Evolution:**
- 1995-2005: Average 2.5-2.6 goals/match
- 2005-2015: Increase to 2.6-2.7 goals/match
- 2015-2025: Peak at 2.7-2.9 goals/match
- **Overall trend:** Soccer is becoming more offensive

**Home Advantage Decline:**
- 1995-2000: 48-49% home win rate
- 2000-2010: 47-48% home win rate
- 2010-2020: 46-47% home win rate
- **2020-2025:** Dramatic drop to 40-46% (COVID-19 effect: empty stadiums!)
- **Post-COVID:** Partial recovery but not to pre-pandemic levels

**Away Team Improvement:**
- 1995: ~1.0 goals per away match
- 2025: ~1.35 goals per away match
- **35% increase in away scoring** over 30 years

### Team Performance Leaders (All-Time)

**Top 5 Scoring Teams:**
1. Barcelona: 2,814 total goals
2. Real Madrid: 2,683 total goals
3. Bayern Munich: ~2,500 total goals
4. Manchester United: ~2,300 total goals
5. Arsenal: ~2,200 total goals

**Best Defensive Teams (Goals Conceded per Match):**
1. Juventus: ~0.85 goals/match
2. Paris Saint-Germain: ~0.90 goals/match
3. Bayern Munich: ~0.92 goals/match

**Best Goal Differential:**
1. Barcelona: +1,500
2. Bayern Munich: +1,400
3. Real Madrid: +1,300

### Most Common Score: 1-1 Draw (7,039 matches, 12.2%)

## Reproducibility & Workflow

### Complete Workflow Automation

This project implements **full pipeline automation** using:
- **6 Python scripts** (01_acquire.py → 06_visualize.py)
- **Snakemake workflow** with dependency management
- **Bash automation script** for sequential execution
- **SHA-256 checksums** for data integrity verification

### Outputs Generated

**Reports (6):**
- acquisition_report.md
- cleaning_report.md
- integration_report.md
- data_quality_report.md
- analysis_report.md
- visualization_report.md

**Visualizations (17 figures):**
- 3 quality assessment figures
- 3 model analysis figures
- 7 comprehensive analytics figures
- 4 feature importance and confusion matrices

**Models (4):**
- logistic_regression.pkl
- random_forest.pkl
- gradient_boosting.pkl
- scaler.pkl

**Data Products:**
- integrated_dataset.csv (9.9 MB, 57,865 matches)
- team_name_mappings.csv (244 teams)
- acquisition_metadata.json

## Reproducing This Analysis

**Quick Start:** For streamlined reproduction instructions, see [QUICK_START.md](QUICK_START.md)

**Data Acquisition:** For detailed acquisition setup, see [DATA_ACQUISITION.md](DATA_ACQUISITION.md)

### Prerequisites

- Python 3.11+ (tested on 3.11)
- Git for version control
- 2GB free disk space
- Windows/Mac/Linux compatible
- **Kaggle API credentials** (free account at https://www.kaggle.com)

### Step-by-Step Instructions

**1. Clone the repository**
```bash
git clone [repository-url]
cd is477project-main
```

**2. Install Python dependencies**
```bash
pip install -r requirements.txt
```

Required packages:
- pandas>=2.0.0
- numpy>=1.24.0
- scikit-learn>=1.3.0
- matplotlib>=3.7.0
- seaborn>=0.12.0
- snakemake>=7.32.0 (optional, for workflow automation)
- kagglehub>=0.2.0 (for data acquisition)
- requests>=2.31.0 (for data acquisition)

**3. Set up Kaggle API credentials (one-time setup - OPTIONAL)**

> **Note:** Kaggle credentials are optional. If not provided, the project will automatically skip Dataset 1 and use only Dataset 2 (GitHub data). The pipeline will still work with 57,000+ matches!

For detailed instructions, see [KAGGLE_SETUP.md](KAGGLE_SETUP.md). Quick setup:

**Option 1: Environment Variables (Recommended)**
```bash
# 1. Copy .env.example to .env
cp .env.example .env

# 2. Edit .env and add your credentials:
# KAGGLE_USERNAME=your_username
# KAGGLE_KEY=your_api_key

# 3. Get credentials from: https://www.kaggle.com/settings
```

**Option 2: kaggle.json File**
```bash
# 1. Go to https://www.kaggle.com/settings
# 2. Click "Create New API Token"
# 3. Save kaggle.json to:
#    - Linux/Mac: ~/.kaggle/kaggle.json
#    - Windows: C:\Users\<USERNAME>\.kaggle\kaggle.json

# On Linux/Mac, set permissions:
chmod 600 ~/.kaggle/kaggle.json
```

**4. Acquire datasets programmatically**

This project uses **fully automated data acquisition** for complete reproducibility:

```bash
python scripts/01_acquire.py
```

This will:
- Download Dataset 1 (ESPN Soccer Data) from Kaggle (~12 MB)
- Clone Dataset 2 (European Football Statistics) from GitHub (~5 MB)
- Calculate SHA-256 checksums for all files
- Generate acquisition metadata and reports

**Expected runtime:** 3-5 minutes (depending on internet speed)

**Verify data integrity:**
```bash
python scripts/01_acquire.py --verify-only
```

**5. Run the complete pipeline**

**Option A: Run all scripts sequentially (recommended)**
```bash
bash workflows/run_all.sh
```

**Option B: Run scripts individually**
```bash
python scripts/01_acquire.py      # Data acquisition & validation
python scripts/02_clean.py         # Data cleaning
python scripts/03_integrate.py    # Data integration
python scripts/04_quality.py      # Quality assessment
python scripts/05_analyze.py      # Predictive modeling
python scripts/06_visualize.py    # Visualization generation
```

**Option C: Use Snakemake workflow automation**
```bash
snakemake --cores 1
```

**Note:** The acquisition step (`acquire_data.py`) should be run before the pipeline scripts, as they depend on the downloaded data.

**6. View results**

After successful execution, outputs are organized in:
```
outputs/
├── reports/          # 6 comprehensive markdown reports
├── figures/
│   ├── quality/      # Data quality visualizations
│   ├── analysis/     # Model performance figures
│   └── comprehensive/ # Analytics visualizations
└── models/           # Trained ML models (.pkl files)
```

Processed data:
```
data/
├── processed/
│   └── integrated_dataset.csv  # Final unified dataset
└── metadata/
    ├── checksums.txt           # SHA-256 checksums
    ├── team_name_mappings.csv  # Standardized team names
    └── acquisition_metadata.json
```

### Expected Runtime

- **Data Acquisition** (acquire_data.py): ~3-5 minutes (one-time, internet-dependent)
- Phase 1 (Acquisition & Validation): ~30 seconds
- Phase 2 (Cleaning): ~45 seconds
- Phase 3 (Integration): ~60 seconds
- Phase 4 (Quality): ~90 seconds
- Phase 5 (Modeling): ~120 seconds (model training)
- Phase 6 (Visualization): ~60 seconds

**Total runtime: ~10-13 minutes** on standard laptop (varies by hardware and internet speed)
**Pipeline only (after data acquired): ~6-8 minutes**

### Verifying Reproducibility

**Check data integrity:**
```bash
# Verify checksums match
cat data/metadata/checksums.txt
```

**Validate outputs:**
```bash
# Count generated files
ls outputs/reports/*.md | wc -l      # Should be 6
ls outputs/figures/*/*.png | wc -l  # Should be 17
ls outputs/models/*.pkl | wc -l     # Should be 4
```

**Check dataset statistics:**
```bash
python -c "import pandas as pd; df = pd.read_csv('data/processed/integrated_dataset.csv'); print(f'Matches: {len(df):,}')"
# Output: Matches: 57,865
```

## Project Structure

```
is477project-main/
├── data/                          # Data directory (raw data gitignored)
│   ├── raw/
│   │   ├── Dataset 1/            # ESPN soccer data (4 CSV files)
│   │   └── Dataset 2/            # Football-data.co.uk (1 CSV file)
│   ├── processed/
│   │   └── integrated_dataset.csv # Final unified dataset (57,865 matches)
│   └── metadata/
│       ├── checksums.txt         # SHA-256 checksums for integrity
│       ├── team_name_mappings.csv # 244 standardized team names
│       ├── acquisition_metadata.json
│       └── data_integration_plan.md
├── scripts/                       # Complete analysis pipeline (6 scripts)
│   ├── 01_acquire.py             # Data acquisition & checksum generation
│   ├── 02_clean.py               # Data cleaning & standardization
│   ├── 03_integrate.py           # Schema integration & feature engineering
│   ├── 04_quality.py             # Quality assessment (5 dimensions)
│   ├── 05_analyze.py             # Predictive modeling (3 ML models)
│   └── 06_visualize.py           # Comprehensive visualization suite
├── workflows/
│   ├── Snakefile                 # Workflow automation with dependency management
│   └── run_all.sh                # Bash script for sequential execution
├── outputs/
│   ├── reports/                  # 6 generated markdown reports
│   ├── figures/
│   │   ├── quality/              # Quality assessment visualizations (3)
│   │   ├── analysis/             # Model performance figures (3)
│   │   └── comprehensive/        # Analytics visualizations (7)
│   └── models/                   # Trained ML models (4 .pkl files)
├── docs/
│   ├── data_dictionary.md        # Complete field documentation
│   └── workflow_diagram.md       # Pipeline visualization
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules (excludes large data)
├── LICENSE                       # MIT License
└── README.md                     # This file
```

## Future Work

### Enhanced Features & Data Integration

**Player-Level Statistics:**
- Individual player performance metrics (goals, assists, passes)
- Player position and formation analysis
- Substitution timing impact

**Contextual Factors:**
- Weather conditions (temperature, precipitation, wind)
- Venue characteristics (stadium size, pitch dimensions, altitude)
- Referee tendencies and bias analysis
- Injury and suspension data

**Match Context:**
- League standings at match time
- Recent form (last 5 games momentum)
- Head-to-head history
- Tournament stage (knockout vs group)

### Advanced Modeling Approaches

**Deep Learning:**
- LSTM networks for sequential match prediction
- Transformer models for attention-based feature learning
- Neural networks for player embedding

**Ensemble Methods:**
- Stacking multiple model types
- Boosting with custom loss functions
- Model averaging with uncertainty quantification

**Real-Time Systems:**
- Live in-game prediction updates
- Minute-by-minute win probability
- Expected goals (xG) modeling

**Causal Inference:**
- Treatment effect estimation for tactical decisions
- Counterfactual analysis ("what if" scenarios)
- Manager impact evaluation

### Extended Coverage

**Geographic Expansion:**
- Additional European leagues (Eredivisie, Scottish Premiership)
- Asian leagues (J-League, K-League, Chinese Super League)
- South American leagues (Brazilian Serie A, Argentine Primera)
- MLS and North American soccer

**Competitive Tiers:**
- Lower division data (Championship, Serie B, etc.)
- Promotion/relegation dynamics

**Other Competitions:**
- UEFA Champions League & Europa League
- Domestic cups (FA Cup, Copa del Rey)
- International tournaments (World Cup, Euros, Copa America)
- Women's soccer analytics (WSL, NWSL, UWCL)

### Operational Applications

**Sports Betting:**
- Odds optimization and value detection
- Arbitrage opportunity identification
- Bankroll management strategies

**Team Strategy:**
- Opponent scouting reports
- Tactical pattern recognition
- Set piece effectiveness analysis

**Player Valuation:**
- Transfer market price prediction
- Contract negotiation support
- Youth prospect evaluation

**Fantasy Sports:**
- Optimal lineup selection
- Captain choice optimization
- Differential picks for tournaments

### Research Extensions

**Methodological Improvements:**
- Bayesian hierarchical models for league effects
- Time series forecasting with seasonality
- Network analysis of passing patterns
- Graph neural networks for team tactics

**Theoretical Questions:**
- Does home advantage still exist post-COVID?
- Impact of VAR technology on match outcomes
- Tactical evolution over decades
- Optimal rest days between matches

## License

- **Code & Scripts:** MIT License - free to use, modify, and distribute
- **Documentation:** CC-BY-4.0 - attribution required
- **Data:** See individual dataset licenses
  - Football-Data.co.uk: PDDL 1.0 (Public Domain)
  - ESPN Soccer Data: CDLA (Community Data License Agreement)

## References

### Data Sources

1. Football-Data.co.uk. (2025). *Historical soccer results and betting odds data*. GitHub. https://github.com/datasets/football-datasets

2. Excel4Soccer. (2024). *ESPN soccer data*. Kaggle. https://www.kaggle.com/datasets/excel4soccer/espn-soccer-data

### Software & Libraries

3. McKinney, W. (2010). Data structures for statistical computing in Python. *Proceedings of the 9th Python in Science Conference*, 56-61. https://doi.org/10.25080/Majora-92bf1922-00a

4. Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., ... & Duchesnay, É. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, 12, 2825-2830.

5. Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering*, 9(3), 90-95. https://doi.org/10.1109/MCSE.2007.55

6. Waskom, M. L. (2021). seaborn: statistical data visualization. *Journal of Open Source Software*, 6(60), 3021. https://doi.org/10.21105/joss.03021

7. Harris, C. R., Millman, K. J., van der Walt, S. J., et al. (2020). Array programming with NumPy. *Nature*, 585(7825), 357-362. https://doi.org/10.1038/s41586-020-2649-2

8. Mölder, F., Jablonski, K. P., Letcher, B., et al. (2021). Sustainable data analysis with Snakemake. *F1000Research*, 10, 33. https://doi.org/10.12688/f1000research.29032.2

### Soccer Analytics Literature

9. Constantinou, A. C., & Fenton, N. E. (2012). Solving the problem of inadequate scoring rules for assessing probabilistic football forecast models. *Journal of Quantitative Analysis in Sports*, 8(1). https://doi.org/10.1515/1559-0410.1418

10. Rein, R., & Memmert, D. (2016). Big data and tactical analysis in elite soccer: future challenges and opportunities for sports science. *SpringerPlus*, 5(1), 1-13. https://doi.org/10.1186/s40064-016-3108-2

## Contact

For questions, issues, or collaboration inquiries:
- **GitHub Issues:** [Open an issue](https://github.com/[username]/is477project/issues)
- **Email:** [your-email@illinois.edu]
- **ORCID:** [https://orcid.org/]

---

**Project Completion:** December 2025
**Course:** IS 477 - Data Management, Curation, and Reproducibility
**Institution:** University of Illinois Urbana-Champaign, School of Information Sciences
**Instructor:** [Instructor Name]

*This project demonstrates best practices in reproducible research, data curation, and transparent documentation for computational research workflows.*
