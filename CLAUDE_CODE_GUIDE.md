# Claude Code Implementation Guide: Soccer Analytics Project
**IS 477 Course Project - Fall 2025**

---

## Project Overview
Build an end-to-end reproducible data analysis pipeline that integrates two soccer datasets to predict match outcomes and analyze performance patterns across European leagues.

**Working Directory:** `C:\Users\Andre\Desktop\Andrew's Important Files\study\2025 Fall\IS 477\is477project-m`

---

## Core Requirements Checklist

### 1. Repository Structure
Create the following directory structure:
```
is477project-m/
├── data/
│   ├── raw/              # Original datasets (gitignored)
│   ├── processed/        # Cleaned & integrated data
│   └── metadata/         # Data dictionaries, schemas
├── scripts/
│   ├── 01_acquire.py     # Data acquisition
│   ├── 02_clean.py       # Data cleaning
│   ├── 03_integrate.py   # Dataset integration
│   ├── 04_quality.py     # Quality assessment
│   ├── 05_analyze.py     # Analysis & modeling
│   └── 06_visualize.py   # Visualizations
├── notebooks/            # Exploratory Jupyter notebooks
├── workflows/
│   └── run_all.sh        # Bash script to run entire pipeline
├── outputs/
│   ├── figures/          # Generated visualizations
│   ├── results/          # Model outputs, statistics
│   └── reports/          # Generated reports
├── docs/
│   ├── data_dictionary.md
│   ├── er_diagram.png
│   └── workflow_diagram.png
├── .gitignore
├── requirements.txt
├── README.md
├── ProjectPlan_v2.md     # Already exists
└── LICENSE
```

---

## Implementation Steps

### PHASE 1: Project Setup & Data Acquisition

#### Task 1.1: Initialize Git Repository
```bash
# If not already initialized
git init
git add .
git commit -m "Initial project structure"
```

#### Task 1.2: Create .gitignore
Add these patterns:
```
# Data files
data/raw/
data/processed/*.csv
*.xlsx

# Python
__pycache__/
*.pyc
.ipynb_checkpoints/
venv/
.env

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

#### Task 1.3: Data Acquisition Script (`scripts/01_acquire.py`)
**Purpose:** Download and verify both datasets

**Dataset 1 - ESPN Soccer Data (Kaggle):**
- Source: https://www.kaggle.com/datasets/excel4soccer/espn-soccer-data
- Files needed: `fixtures.csv`, `teamStats.csv`, `standings.csv`, `teams.csv`
- Method: Manual download or Kaggle API

**Dataset 2 - Football-Data.co.uk:**
- Source: https://github.com/datasets/football-datasets
- Clone repo or download CSVs for: Premier League, La Liga, Bundesliga, Serie A, Ligue 1
- Consolidate all seasons per league

**Requirements:**
- Generate SHA-256 checksums for all downloaded files
- Store checksums in `data/metadata/checksums.txt`
- Log download timestamps
- Handle errors gracefully

---

### PHASE 2: Data Cleaning & Standardization

#### Task 2.1: Team Name Standardization (`scripts/02_clean.py`)
**Goal:** Create consistent team identifiers across both datasets

**Steps:**
1. Convert all team names to lowercase
2. Remove special characters and extra whitespace
3. Create mapping dictionary for aliases:
   ```python
   team_aliases = {
       'man united': 'manchester united',
       'man city': 'manchester city',
       'psg': 'paris saint-germain',
       # ... more mappings
   }
   ```
4. Apply fuzzy matching for remaining mismatches
5. Create `data/metadata/team_name_mappings.csv`

#### Task 2.2: Handle Missing Values
- Document missing data patterns
- Apply appropriate imputation strategies:
  - Shots/Fouls: Use league/season medians
  - Cards: Treat as 0 if missing
  - Goals: NEVER impute (mark as invalid match)

#### Task 2.3: Data Type Validation
- Dates → datetime format (YYYY-MM-DD)
- Numeric columns → int/float
- Categorical columns → standardized strings

---

### PHASE 3: Data Integration

#### Task 3.1: Schema Alignment (`scripts/03_integrate.py`)
**Create unified schema combining both datasets:**

**Common Fields:**
- `match_id` (generated)
- `date`
- `home_team` (standardized)
- `away_team` (standardized)
- `league_name`
- `season`
- `home_goals` (FTHG from Dataset 2, goals from Dataset 1)
- `away_goals` (FTAG from Dataset 2)
- `home_shots`
- `away_shots`
- `home_shots_on_target`
- `away_shots_on_target`
- `home_fouls`
- `away_fouls`
- `home_yellow_cards`
- `away_yellow_cards`
- `home_red_cards`
- `away_red_cards`
- `result` (H/A/D)

#### Task 3.2: Perform Join
```python
# Pseudo-code
merged_df = dataset1.merge(
    dataset2,
    left_on=['team_name_std', 'league', 'season'],
    right_on=['HomeTeam_std', 'league_name', 'Season'],
    how='outer',
    indicator=True
)
```

#### Task 3.3: Validation
- Check row counts before/after merge
- Identify unmatched records
- Generate merge report in `outputs/reports/integration_report.md`

---

### PHASE 4: Data Quality Assessment

#### Task 4.1: Quality Profiling (`scripts/04_quality.py`)
**Generate quality report covering:**

1. **Completeness:**
   - % missing values per column
   - Row completeness distribution

2. **Validity:**
   - Goals ≥ 0
   - Shots ≥ Shots on Target
   - Cards are integers
   - Dates in valid range

3. **Consistency:**
   - HomeGoals + AwayGoals matches Result
   - Team names consistent across seasons

4. **Accuracy:**
   - Cross-reference known results (sample 100 matches)
   - Check for logical impossibilities (e.g., negative stats)

5. **Uniqueness:**
   - Detect duplicate matches
   - Check for duplicate team IDs

**Output:** `outputs/reports/data_quality_report.md` with visualizations

---

### PHASE 5: Feature Engineering & Analysis

#### Task 5.1: Feature Creation (`scripts/05_analyze.py`)
**Derived Features:**
- `shots_accuracy_home` = home_shots_on_target / home_shots
- `shots_accuracy_away` = away_shots_on_target / away_shots
- `shots_differential` = home_shots - away_shots
- `cards_differential` = (home_yellow + home_red*2) - (away_yellow + away_red*2)
- `home_win_rate_l5` = home team's wins in last 5 games
- `goal_differential` = home_goals - away_goals

#### Task 5.2: Exploratory Data Analysis
1. Correlation analysis between features and match outcomes
2. League-specific performance patterns
3. Temporal trends (performance over seasons)
4. Home advantage quantification

#### Task 5.3: Predictive Modeling
**Model 1: Match Outcome Classifier**
- Target: Result (Home Win / Draw / Away Win)
- Features: shots, fouls, cards, possession, form metrics
- Algorithms: Random Forest, XGBoost, Logistic Regression
- Evaluation: Accuracy, F1-score, Confusion Matrix

**Model 2: Goals Regression**
- Target: Total goals in match
- Features: team stats, historical averages
- Algorithms: Linear Regression, Random Forest Regressor
- Evaluation: RMSE, R², MAE

---

### PHASE 6: Visualization

#### Task 6.1: Create Visualizations (`scripts/06_visualize.py`)
**Required Plots:**
1. Feature importance from models
2. Performance trends over seasons
3. League comparison (shot accuracy, cards, goals)
4. Correlation heatmap
5. Model performance metrics

**Save all figures to:** `outputs/figures/`

---

### PHASE 7: Workflow Automation

#### Task 7.1: Create Bash Run-All Script
```bash
#!/bin/bash
# workflows/run_all.sh

echo "Starting soccer analytics pipeline..."

python scripts/01_acquire.py
python scripts/02_clean.py
python scripts/03_integrate.py
python scripts/04_quality.py
python scripts/05_analyze.py
python scripts/06_visualize.py

echo "Pipeline complete!"
```

---

### PHASE 8: Documentation & Metadata

#### Task 8.1: Data Dictionary (`docs/data_dictionary.md`)
Document every field in final integrated dataset:
- Column name
- Data type
- Description
- Valid range/values
- Source (Dataset 1, Dataset 2, or derived)

#### Task 8.2: Create ER Diagram
Show relationships between:
- Teams
- Matches
- Seasons
- Leagues

Tool suggestions: draw.io, dbdiagram.io, or Python (eralchemy)

#### Task 8.3: Metadata File
Create JSON metadata following DataCite schema:
```json
{
  "title": "Integrated European Soccer Statistics (2015-2025)",
  "creators": ["Team Member 1", "Team Member 2"],
  "subjects": ["soccer", "sports analytics", "machine learning"],
  "version": "1.0",
  "rights": "CC-BY-4.0",
  "sources": [...]
}
```

---

### PHASE 9: Reproducibility Package

#### Task 9.1: Requirements File
```bash
# Generate requirements.txt
pip freeze > requirements.txt
```

Essential packages:
- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn

#### Task 9.2: Upload Data to Box
1. Upload `data/raw/` and `data/processed/` to Box
2. Generate shareable link
3. Document in README.md

#### Task 9.3: README.md
Structure:
```markdown
# Project Title

## Contributors
- Name 1 (ORCID)
- Name 2 (ORCID)

## Summary
[500-1000 words]

## Data Profile
[500-1000 words]

## Data Quality
[500-1000 words]

## Findings
[~500 words]

## Future Work
[500-1000 words]

## Reproducing
1. Clone repository
2. Download data from Box: [link]
3. Install dependencies: `pip install -r requirements.txt`
4. Run pipeline: `bash workflows/run_all.sh`

## References
[Citations in APA format]
```

---

## Critical Requirements Summary

### Must-Haves for Full Credit:
- ✅ Clear Git history showing both team members' contributions
- ✅ All scripts executable and documented
- ✅ Complete workflow automation (run_all.sh)
- ✅ Data uploaded to Box with working shared link
- ✅ Comprehensive README.md (2700-4500 words)
- ✅ Data quality report with findings
- ✅ Reproducible from scratch by TAs
- ✅ Proper licensing (data + code)
- ✅ FAIR metadata (DataCite or similar)
- ✅ Citations for all data sources and libraries

---

## Ethical & Legal Considerations

1. **Dataset 1 (Kaggle):**
   - License: Check Kaggle dataset page
   - Attribution required
   - May redistribute with credit

2. **Dataset 2 (football-data.co.uk):**
   - License: PDDL 1.0 (Public Domain)
   - No restrictions
   - Cite original source

3. **Privacy:**
   - No personal data involved (only team/match statistics)
   - No consent issues

4. **Copyright:**
   - All code: MIT or Apache 2.0 license
   - Documentation: CC-BY-4.0

---

## Testing & Validation Strategy

Before final submission:
1. **Delete all generated files**
2. **Run complete pipeline from scratch**
3. **Verify outputs match previous run**
4. **Check all links work (Box, GitHub)**
5. **Have teammate clone repo and reproduce**

---

## Submission Checklist

- [ ] All code pushed to GitHub
- [ ] Data uploaded to Box with shareable link
- [ ] README.md complete (2700-4500 words)
- [ ] requirements.txt present
- [ ] Workflow automation implemented
- [ ] Data dictionary created
- [ ] Quality report generated
- [ ] Visualizations saved
- [ ] License files added
- [ ] Metadata file created
- [ ] Git history shows both contributors
- [ ] Create "final-project" tag
- [ ] Create GitHub release
- [ ] Submit release URL to Canvas

---

## Common Pitfalls to Avoid

1. **Hardcoded paths:** Use `os.path.join()` or `pathlib.Path`
2. **Missing data upload:** TAs can't grade without data access
3. **Unclear instructions:** README must be step-by-step
4. **No error handling:** Scripts should fail gracefully
5. **Insufficient documentation:** Every script needs comments
6. **License omission:** Both data and code need licenses
7. **Git history gaps:** Both members must commit regularly

---

## Quick Start for Claude Code

When you start working with Claude Code, show it this file and say:

"I'm working on the IS 477 soccer analytics project. Please help me implement [specific phase] following the structure outlined in CLAUDE_CODE_GUIDE.md. The working directory is C:\Users\Andre\Desktop\Andrew's Important Files\study\2025 Fall\IS 477\is477project-m"

Then Claude Code can:
- Generate any script listed above
- Create directory structures
- Write documentation
- Debug issues
- Suggest improvements

---

## Contact & Support

- Campuswire: For technical questions
- Office Hours: For project guidance
- GitHub Issues: Track your own progress

**Final Due Date: December 7, 2025**

---

*Good luck! This guide should keep you organized and on track.*
