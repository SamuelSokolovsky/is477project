# Project Results: European Soccer Analytics

**Project:** Integrated European Soccer Analytics
**Generated:** December 9, 2025
**Authors:** Yongyang Fu, Sam Sokolovsky
**Course:** IS 477 - Data Management, Curation, and Reproducibility

---

## Executive Summary

This project successfully integrated and analyzed 32 years of European soccer data, encompassing 57,327 matches across five major leagues (Premier League, La Liga, Serie A, Bundesliga, and Ligue 1) from 1993 to 2025. Through systematic data acquisition, cleaning, integration, quality assessment, predictive modeling, and visualization, we developed a reproducible data science pipeline that demonstrates best practices in data curation and computational research.

The analysis revealed significant insights into soccer dynamics, including quantifiable home advantage, scoring trends over time, and predictive patterns for match outcomes. Our machine learning models achieved approximately 59% accuracy in predicting match results, substantially better than random guessing (33%) and demonstrating the predictive power of in-game statistics.

---

## 1. Data Acquisition and Integration

### 1.1 Dataset Overview

We integrated two primary datasets:

**Dataset 1: ESPN Soccer Data (Kaggle)**
- Source: https://www.kaggle.com/datasets/excel4soccer/espn-soccer-data
- Size: 12.99 MB
- Components: 4 files containing league information, team data, standings, and team statistics
- Total records across all files: 114,274 records
  - Teams: 4,143 records
  - Team Stats: 102,978 records
  - Standings: 6,069 records
  - Leagues: 1,084 records

**Dataset 2: European Football Match Statistics (GitHub)**
- Source: https://github.com/datasets/football-datasets
- Match Results: 57,327 matches
- Date range: July 23, 1993 to May 25, 2025
- Coverage: 160 season files across 5 leagues

### 1.2 Data Integration Success

The integration process successfully merged these datasets into a unified analytical framework:
- **Total matches in integrated dataset:** 57,327
- **Unique match identifiers:** 57,327 (100% uniqueness)
- **Date span:** 32 years (33 seasons)
- **Leagues covered:** 5 (Bundesliga, La Liga, Ligue 1, Premier League, Serie A)
- **Unique teams tracked:** 242
- **Final schema:** 38 columns combining core match data, statistics, and derived features

All validation checks passed during integration, confirming data integrity and schema alignment.

---

## 2. League-Specific Findings

### 2.1 League Distribution

Our dataset provides comprehensive coverage across Europe's top five leagues:

| League | Total Matches | Seasons Covered | Unique Teams | Match Coverage |
|--------|--------------|-----------------|--------------|----------------|
| La Liga | 12,324 | 32 | 49 | 21.5% |
| Premier League | 12,324 | 32 | 51 | 21.5% |
| Ligue 1 | 11,541 | 33 | 45 | 20.1% |
| Serie A | 11,346 | 32 | 52 | 19.8% |
| Bundesliga | 9,792 | 32 | 45 | 17.1% |

The dataset demonstrates balanced representation across leagues, with slight variation in match counts due to different league structures (number of teams and matches per season).

### 2.2 Temporal Coverage

The dataset spans from the 1993-1994 season through the 2024-2025 season, providing:
- 33 years of continuous match data
- Coverage through multiple tactical evolution periods in European soccer
- Sufficient historical depth for longitudinal analysis
- Contemporary data through the current season

---

## 3. Data Quality Assessment

### 3.1 Overall Quality Status

**Assessment:** GOOD with minor issues detected

Five dimensions of data quality were systematically evaluated:

| Quality Dimension | Status | Finding |
|------------------|--------|---------|
| Completeness | PASS | Core fields 100% complete |
| Validity | WARNING | 2 minor issues detected |
| Consistency | WARNING | 1 minor issue detected |
| Accuracy | PASS | No anomalies detected |
| Uniqueness | PASS | 100% unique match records |

### 3.2 Completeness Analysis

**Key Findings:**
- Core match data (teams, dates, goals, results) is 100% complete across all 57,327 matches
- 10,846 matches (18.9%) have complete data across all 38 fields
- Average row completeness: 88.01%

**Missing Data Patterns:**

The missing data follows expected patterns based on historical data collection practices:

| Field | Completeness | Missing % | Explanation |
|-------|-------------|-----------|-------------|
| Basic match info (teams, goals, dates) | 100% | 0% | Core data always collected |
| Yellow/Red cards | 100% | 0% | Consistently tracked |
| Shots statistics | 67-69% | 31-33% | Limited availability pre-2005 |
| Fouls | 67.4% | 32.6% | Limited availability pre-2005 |
| Corners | 68.0% | 32.0% | Limited availability pre-2005 |
| Referee | 19.0% | 81.0% | Inconsistently recorded |

The missing statistics for earlier seasons (pre-2005) reflect historical data availability rather than data quality issues. Detailed match statistics became more comprehensively tracked with the expansion of digital recording technology.

### 3.3 Validity Issues

Two minor validity issues were detected:
- **Home shots less than shots on target:** 2 cases (0.003% of records)
- **Away shots less than shots on target:** 3 cases (0.005% of records)

These represent probable data entry errors but affect less than 0.01% of the dataset, indicating high overall data quality.

### 3.4 Consistency Assessment

One minor consistency issue detected:
- **Shot accuracy out of bounds:** 1 case (0.002% of records)

This minimal inconsistency does not materially impact analysis quality.

### 3.5 Data Quality Recommendations

Based on our assessment:
1. The dataset is suitable for comprehensive analysis with appropriate handling of missing data
2. Core match data (goals, results, teams, dates) is completely reliable
3. Statistical analysis should account for missing shot/foul data in pre-2005 seasons
4. For complete statistical analysis, filtering to post-2005 matches yields 67-69% data coverage
5. The 5 validity/consistency issues represent less than 0.01% of data and can be safely excluded

---

## 4. Soccer Analytics: Quantitative Findings

### 4.1 Home Advantage Effect

One of the most significant findings is the quantifiable home advantage in European soccer:

**Overall Results Distribution:**
- Home wins: 46.2% of all matches (26,463 matches)
- Draws: 25.5% of all matches (14,608 matches)
- Away wins: 29.1% of all matches (16,677 matches)

This demonstrates a substantial home advantage, with home teams winning 17.1 percentage points more often than away teams. The home advantage persists across all leagues and time periods in our dataset.

**Interpretation:**
The home advantage likely stems from multiple factors including:
- Familiar playing conditions (pitch dimensions, climate)
- Reduced travel fatigue
- Crowd support and referee bias
- Psychological comfort

This finding has significant implications for match prediction, betting markets, and team strategy.

### 4.2 Scoring Patterns

**Average Goals Per Match:**
- Overall average: 2.67 goals per match
- This metric remained relatively stable across the 32-year period
- Indicates consistent offensive-defensive balance in European soccer

**Goals Distribution:**
The most common match result was a 1-1 draw, occurring in 7,039 matches (12.3% of all matches), highlighting the competitive balance in European soccer.

### 4.3 Shot Efficiency and Conversion

Analysis of shot statistics (available for 67-69% of matches, primarily post-2005) revealed:

**Shot Accuracy:**
- Teams demonstrate varying shot accuracy, with higher shot accuracy strongly correlated with winning outcomes
- Shot conversion rates serve as key differentiators between successful and unsuccessful teams

**Shots vs Goals Relationship:**
- Strong positive correlation between total shots and goals scored
- Shots on target proved to be a significantly better predictor than total shots
- Shot accuracy (shots on target / total shots) emerged as a critical performance metric

### 4.4 Discipline and Card Statistics

**Card Distribution:**
- Yellow cards: 100% data completeness across all 57,327 matches
- Red cards: 100% data completeness across all 57,327 matches
- Card data demonstrates consistent tracking throughout the dataset's history

The complete card data enabled analysis of:
- League-specific discipline patterns
- Evolution of refereeing standards over time
- Relationship between card accumulation and match outcomes

### 4.5 Temporal Evolution

Analysis of trends over the 32-year period revealed:

**Scoring Trends:**
- Goals per match remained relatively stable around 2.67 average
- No significant long-term increase or decrease in offensive output
- Suggests tactical balance between offense and defense has been maintained

**Home Advantage Stability:**
- Home advantage percentage (46.2% win rate) persisted throughout the time period
- Indicates home advantage is a fundamental feature of soccer rather than a temporal artifact

---

## 5. Predictive Modeling Results

### 5.1 Modeling Objective

We developed machine learning models to predict match outcomes (Home Win, Draw, Away Win) based on in-game statistics. The goal was to assess the predictability of soccer matches and identify the most important features for prediction.

### 5.2 Model Training Approach

**Data Preparation:**
- Complete cases only: 37,698 matches (65.8% of total dataset)
- Date range for complete cases: 2000-2025
- Temporal train/test split (80% train, 20% test) to avoid data leakage
  - Training set: 30,158 matches (through April 2021)
  - Test set: 7,540 matches (April 2021 through May 2025)

**Class Distribution:**
- Home wins: 45.4% (17,107 matches)
- Draws: 25.5% (9,603 matches)
- Away wins: 29.1% (10,988 matches)

The slight class imbalance (favoring home wins) reflects real-world patterns and was preserved in modeling.

**Features Used:**
20 statistical features including:
- Shot statistics (shots, shots on target, shot accuracy)
- Fouls
- Corner kicks
- Cards (yellow and red)
- Derived features (differentials, accuracy metrics)

### 5.3 Model Performance Comparison

Three classification models were evaluated:

| Model | Accuracy | Precision | Recall | F1 Score | ROC AUC | Overall Rank |
|-------|----------|-----------|--------|----------|---------|--------------|
| **Random Forest** | **58.91%** | **55.67%** | **58.91%** | **54.79%** | **75.78%** | **1st** |
| Gradient Boosting | 58.78% | 55.71% | 58.78% | 55.90% | 76.08% | 2nd |
| Logistic Regression | 58.83% | 54.57% | 58.83% | 53.06% | 75.55% | 3rd |

**Best Model: Random Forest**
- Achieved 58.91% accuracy on the test set
- Represents a 77% improvement over random guessing (33.33%)
- Demonstrates that match outcomes are partially predictable from in-game statistics

### 5.4 Detailed Performance Analysis

**Random Forest Per-Class Performance:**

| Match Outcome | Precision | Recall | F1-Score | Test Set Count |
|---------------|-----------|--------|----------|----------------|
| Away Win (A) | 59.16% | 64.29% | 61.62% | 2,366 matches |
| Draw (D) | 41.90% | 13.47% | 20.38% | 1,901 matches |
| Home Win (H) | 61.15% | 81.42% | 69.85% | 3,273 matches |

**Key Observations:**
1. **Home wins are most predictable:** 61.15% precision, 81.42% recall
2. **Draws are hardest to predict:** Only 41.90% precision, 13.47% recall
3. **Model bias:** The model tends to under-predict draws and over-predict home wins

**Confusion Matrix Analysis (Random Forest):**

```
Actual Results:
- Away Wins (2,366): Correctly predicted 1,521 (64.3%)
  - Mispredicted as Draw: 167 (7.1%)
  - Mispredicted as Home Win: 678 (28.7%)

- Draws (1,901): Correctly predicted 256 (13.5%)
  - Mispredicted as Away Win: 630 (33.1%)
  - Mispredicted as Home Win: 1,015 (53.4%)

- Home Wins (3,273): Correctly predicted 2,665 (81.4%)
  - Mispredicted as Away Win: 420 (12.8%)
  - Mispredicted as Draw: 188 (5.7%)
```

### 5.5 Feature Importance

The Random Forest model identified the most important predictive features (see `outputs/figures/analysis/feature_importance.png`):

**Top Predictive Features:**
1. Shot statistics (shots, shots on target)
2. Shot accuracy (conversion rate)
3. Goal differential patterns
4. Corners
5. Fouls and cards

**Insight:** Offensive statistics (shots and accuracy) are significantly more predictive than defensive actions (fouls, cards), suggesting that controlling possession and creating quality chances are the primary determinants of match outcomes.

### 5.6 Model Comparison Insights

All three models performed similarly (58.78% - 58.91% accuracy), indicating:
1. The problem has inherent complexity - soccer matches are not fully deterministic
2. The 59% accuracy ceiling may represent the limit of predictability from statistics alone
3. Non-statistical factors (team morale, injuries, tactics, momentum) likely account for remaining unpredictability

**Practical Applications:**
- Models can inform betting strategies (59% vs 33% random chance)
- Help teams identify key performance indicators for success
- Provide baseline predictions for sports analytics platforms
- Demonstrate limits of statistical prediction in team sports

---

## 6. Visualization Insights

Seven comprehensive visualizations were generated (see `outputs/figures/comprehensive/`), revealing additional insights:

### 6.1 Temporal Trends Analysis
**File:** `temporal_trends.png`

**Findings:**
- Goals per match remained stable around 2.67 throughout the 32-year period
- Home vs away goal differential shows consistent home advantage
- No evidence of increasing or decreasing offensive output over time
- Suggests tactical evolution has maintained offensive-defensive equilibrium

### 6.2 League Comparison Analysis
**File:** `league_comparison.png`

**Findings:**
- Different leagues show varying characteristics:
  - Average goals per match varies by league
  - Card discipline differs significantly between leagues
  - Shot accuracy patterns reveal league-specific playing styles
- Dataset provides balanced coverage across all five leagues

### 6.3 Team Performance Analysis
**File:** `team_performance.png`

**Findings:**
- Top 10 scoring teams identified across 32-year period
- Top 10 defensive teams (fewest goals conceded)
- Best goal differential teams represent sustained excellence
- Performance metrics enable historical team comparisons

### 6.4 Home Advantage Deep Dive
**File:** `home_advantage.png`

**Findings:**
- Home advantage persists across all leagues (42-48% home win rate)
- Pie chart visualization confirms 46.2% overall home win rate
- Home advantage is consistent across different leagues and seasons
- Validates home field advantage as a fundamental soccer phenomenon

### 6.5 Shot Efficiency Analysis
**File:** `shot_efficiency.png`

**Findings:**
- Shot accuracy distribution shows wide variation between teams
- Hexbin plot reveals strong positive correlation between shots and goals
- Shot quality (accuracy) matters more than shot quantity
- Efficient shooting is a key differentiator of successful teams

### 6.6 Seasonal Pattern Analysis
**File:** `seasonal_patterns.png`

**Findings:**
- Goals by month analysis reveals:
  - Slight variation in scoring across different months
  - No strong seasonal effect on overall goal production
- Home advantage remains consistent throughout the calendar year
- Season timing (start/middle/end) does not significantly affect outcomes

### 6.7 Feature Correlation Analysis
**File:** `correlation_heatmap.png`

**Findings:**
- Strong positive correlation between:
  - Total shots and goals scored (0.5-0.6 correlation)
  - Shots on target and goals (0.7-0.8 correlation)
  - Corners and offensive pressure
- Weak correlation between:
  - Fouls and match outcomes
  - Cards and winning probability
- Correlation matrix confirms that offensive metrics are better outcome predictors than defensive actions

---

## 7. Key Insights and Conclusions

### 7.1 Primary Findings

1. **Quantifiable Home Advantage:** European soccer exhibits a robust home advantage effect, with home teams winning 46.2% of matches compared to 29.1% for away teams, representing a 17.1 percentage point advantage that persists across leagues and decades.

2. **Scoring Stability:** Average goals per match (2.67) has remained remarkably stable over 32 years, suggesting that tactical evolution has maintained offensive-defensive balance despite changes in playing styles.

3. **Predictability Limits:** Match outcomes are partially predictable (59% accuracy) from in-game statistics, but substantial unpredictability remains, highlighting the complex, dynamic nature of team sports.

4. **Offensive Metrics Dominate:** Shot statistics, particularly shots on target and shot accuracy, are the strongest predictors of match outcomes, more important than defensive actions like fouls or cards.

5. **Draw Prediction Challenge:** Draws are the most difficult outcome to predict (13.5% recall), likely because draws can result from multiple pathways (evenly matched teams, defensive tactics, or balanced attacking play).

### 7.2 Data Quality Insights

1. **Historical Data Limitations:** Detailed statistics (shots, fouls, corners) are only available for approximately 67-69% of matches, primarily from 2005 onwards, reflecting technological improvements in sports data collection.

2. **Core Data Reliability:** Essential match data (teams, goals, results, cards) is 100% complete and highly reliable across all 57,327 matches and 32 years.

3. **Data Integration Success:** Merging two distinct datasets with different schemas was successful, achieving 100% match uniqueness and passing all validation checks.

### 7.3 Methodological Achievements

1. **Reproducible Pipeline:** The complete workflow from data acquisition through analysis is fully automated via bash script (`workflows/run_all.sh`), enabling one-command reproduction.

2. **FAIR Data Principles:** Data is Findable (documented sources), Accessible (programmatic download), Interoperable (standard CSV format), and Reusable (comprehensive documentation and metadata).

3. **Quality Assurance:** Systematic quality assessment across five dimensions (completeness, validity, consistency, accuracy, uniqueness) ensures analysis integrity.

4. **Temporal Validation:** Using temporal train-test split prevents data leakage and ensures model performance reflects genuine predictive capability on future matches.

### 7.4 Limitations and Future Work

**Limitations:**
1. **Missing Contextual Data:** Player injuries, team form, head-to-head history, and tactical information are not included, limiting predictive accuracy.
2. **Pre-2005 Statistics:** Limited availability of detailed statistics for earlier matches constrains longitudinal statistical analysis.
3. **Binary Prediction:** Models predict only final outcomes, not goal totals or match dynamics.

**Future Research Directions:**
1. **Enhanced Feature Engineering:** Incorporate rolling team form (last 5-10 matches), head-to-head records, and team strength ratings.
2. **Player-Level Analysis:** Integrate player statistics and lineup information for deeper insights.
3. **Tactical Analysis:** Incorporate formation data and tactical patterns.
4. **Real-Time Prediction:** Develop in-game prediction models that update as matches progress.
5. **Expanded Coverage:** Include additional European leagues and international competitions.

---

## 8. Dataset Availability

**Integrated Dataset Location:** `data/processed/integrated_dataset.csv`

**Dataset Characteristics:**
- 57,327 rows (matches)
- 38 columns (features)
- File size: 9.9 MB
- Format: CSV (comma-separated values)
- Encoding: UTF-8

**Team Name Mapping:** `data/metadata/team_name_mappings.csv`
- 242 unique teams
- Standardized naming across datasets

**Data Verification:**
- SHA-256 checksums: `data/metadata/checksums.txt`
- Acquisition metadata: `data/metadata/acquisition_report.md`

---

## 9. Model Artifacts

**Trained Models Location:** `outputs/models/`

**Available Models:**
1. `logistic_regression.pkl` - Baseline linear model
2. `random_forest.pkl` - Best performing model (58.91% accuracy)
3. `gradient_boosting.pkl` - Ensemble model with best ROC AUC
4. `scaler.pkl` - Feature scaling parameters for inference

All models are saved in scikit-learn pickle format and can be loaded for prediction on new data.

---

## 10. Reproducibility Statement

This analysis is fully reproducible. To reproduce all results:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run complete pipeline
bash workflows/run_all.sh
```

Expected runtime: ~8-10 minutes

All outputs (reports, figures, models, processed data) will be regenerated identically, demonstrating complete computational reproducibility.

---

## 11. References to Generated Assets

**Reports:**
- Data Acquisition: `data/metadata/acquisition_report.md`
- Data Cleaning: `outputs/reports/cleaning_report.md`
- Data Integration: `outputs/reports/integration_report.md`
- Quality Assessment: `outputs/reports/data_quality_report.md`
- Predictive Modeling: `outputs/reports/analysis_report.md`
- Visualization Summary: `outputs/reports/visualization_report.md`

**Visualizations:**

*Quality Assessment:*
- `outputs/figures/quality/completeness_by_column.png`
- `outputs/figures/quality/completeness_over_time.png`
- `outputs/figures/quality/goals_distribution.png`

*Predictive Modeling:*
- `outputs/figures/analysis/feature_importance.png`
- `outputs/figures/analysis/confusion_matrices.png`
- `outputs/figures/analysis/model_comparison.png`

*Comprehensive Analytics:*
- `outputs/figures/comprehensive/temporal_trends.png`
- `outputs/figures/comprehensive/league_comparison.png`
- `outputs/figures/comprehensive/team_performance.png`
- `outputs/figures/comprehensive/home_advantage.png`
- `outputs/figures/comprehensive/shot_efficiency.png`
- `outputs/figures/comprehensive/seasonal_patterns.png`
- `outputs/figures/comprehensive/correlation_heatmap.png`

---

## 12. Conclusion

This project successfully demonstrates end-to-end reproducible data science practices applied to European soccer analytics. Through systematic data management, rigorous quality assessment, statistical analysis, and predictive modeling, we have:

1. **Integrated 32 years of soccer data** into a coherent analytical framework
2. **Quantified fundamental soccer phenomena** including home advantage and scoring patterns
3. **Developed predictive models** achieving 59% accuracy on match outcome prediction
4. **Created comprehensive visualizations** revealing insights across multiple analytical dimensions
5. **Established a fully reproducible pipeline** enabling verification and extension by other researchers

The findings contribute to soccer analytics literature by providing quantitative validation of home advantage effects, demonstrating the limits of statistical match prediction, and identifying shot efficiency as the primary determinant of match success. The reproducible methodology serves as a template for sports analytics research and demonstrates FAIR data principles in computational research.

---

**For questions or collaboration opportunities, contact:**
- Yongyang Fu: yf14@illinois.edu
- ORCID: https://orcid.org/0009-0009-6222-4732
- GitHub: https://github.com/SamuelSokolovsky/is477project

**Project Completion:** December 2025
**Institution:** University of Illinois Urbana-Champaign, School of Information Sciences
**Course:** IS 477 - Data Management, Curation, and Reproducibility
**Instructor:** Nicola Carboni
