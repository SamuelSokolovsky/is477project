# ProjectPlan.v2

## Overview
The goal of our project is to analyze professional soccer data to identify patterns and relationships between team statistics and match outcomes. Using historical match data, player performance metrics, and team-level season statistics, we aim to build predictive models capable of forecasting match results and examining long-term performance trends.

By integrating two large, complementary datasets—one containing rich ESPN-derived team and match statistics, and the other containing multi-decade European match-level data from football-data.co.uk—we will explore how quantifiable in-game factors (shots, fouls, goals, cards, etc.) relate to game outcomes and team success. Our broader objective is to demonstrate a complete and reproducible data-management lifecycle aligned with IS 477 concepts, including acquisition, cleaning, integration, documentation, and workflow automation.

Our work will adhere to FAIR and CARE principles to ensure reproducibility, transparency, and responsible data handling.

---

## Research Questions
We refined and expanded our research questions based on the combined strengths of Dataset 1 and Dataset 2:

1. **Which match-level or season-level statistics (e.g., possession, shots on target, passing accuracy, fouls, shots, cards, etc.) best predict the outcome of a soccer match?**
2. **Can historical team and player performance records be used to accurately predict future match results or full-season outcomes?**
3. **How do observable performance factors vary across leagues and seasons, and what long-term trends can be identified?**
4. **Given the integrated datasets, can predictive models be developed to answer the above questions across multiple leagues and time periods?**

These research questions are directly supported by the statistical richness of Dataset 1 and the multi-decade depth of Dataset 2.

---

## Team
We will both contribute collaboratively to as many components of the project as possible. Work will not be strictly divided; instead, we will jointly participate in data exploration, integration, modeling, and documentation to ensure consistent quality and shared ownership of the results.

---

## Datasets

### **Dataset 1 — ESPN Soccer Data (Excel4Soccer, 2023)**
Dataset 1 contains match-level and team-level ESPN soccer data drawn from the 2024–25 season. It includes multiple CSV files such as `fixtures.csv`, `teamStats.csv`, `standings.csv`, and `teams.csv`. These files collectively cover:
- 30,000+ matches  
- 3,000+ teams  
- 400+ leagues  
- 45,000+ players  

Key fields include possession, total shots, fouls, passes, goals, team identifiers, and event identifiers. We plan to merge these components using shared keys such as `teamId` and `eventId` to produce per-team seasonal aggregates as well as individual match-level records.

---

### **Dataset 2 — Football Match Statistics (football-data.co.uk via datasets/football-datasets)**

**Source repository:** https://github.com/datasets/football-datasets  
**Upstream provider:** https://www.football-data.co.uk/  
**License:** Open Data Commons Public Domain Dedication and License (PDDL 1.0)

Dataset 2 provides historical match-level statistics for the five major European football leagues:
- Premier League  
- La Liga  
- Bundesliga  
- Serie A  
- Ligue 1  

The dataset spans multiple decades (approx. 1993–present) and includes standardized CSVs per season for every league. All leagues share a consistent schema, enabling clean merging and long-term comparative analysis.

**We constructed our own consolidated version of Dataset 2 as follows:**
- Parsed all CSV files listed in each league’s `datapackage.json`
- Combined all seasons per league into per-league consolidated CSVs
- Added provenance fields such as `SeasonFile` and `league_name`
- Created one master CSV containing all leagues:


### **Column Definitions (core fields across all leagues)**  
- **Date** — match date  
- **HomeTeam / AwayTeam** — participating clubs  
- **FTHG / FTAG / FTR** — full-time goals & result  
- **HTHG / HTAG / HTR** — half-time goals & result  
- **HS / AS** — total shots  
- **HST / AST** — shots on target  
- **HF / AF** — fouls  
- **HY / AY** — yellow cards  
- **HR / AR** — red cards  
- **HC / AC** — corners  
- **league_name** — league label added during our consolidation  

These fields allow us to model outcomes, compare performance factors across leagues, and integrate Dataset 2 with ESPN-derived statistics in Dataset 1.

---

## Integration Plan
Our integration approach is based on aligning team identifiers, names, and league labels between the two datasets. Steps include:

1. **Standardize team names in both datasets**  
   - Lowercasing  
   - Removing accents  
   - Normalizing spacing and punctuation  
   - Mapping alias variations (e.g., “Man United” vs “Manchester United”)  

2. **Add consistent league identifiers**  
   Dataset 2 already includes a `league_name` column; Dataset 1 will require mapping to equivalent league categories.

3. **Join datasets on (TeamName, League)**  
   - A left join from Dataset 1 (feature-rich statistics) to Dataset 2 (historical match logs)  
   - Validation using record counts and manual inspection  

4. **Create integrated analytical tables**  
   - Per-team season aggregates  
   - Per-match combined records  
   - Feature-engineered tables including rolling averages, form indicators, and shot-based KPIs  

This combined dataset will support both descriptive analytics and predictive modeling.

---

## Timeline & Implementation Plan

### **Week 1 (Oct 13 – Oct 19)**  
Explore both datasets, review schemas, and draft ER diagrams and a preliminary data dictionary.

### **Week 2 (Oct 20 – Oct 26)**  
Clean and standardize team names, league identifiers, and season fields.

### **Week 3 (Oct 27 – Nov 2)**  
Integrate datasets using pandas/DuckDB; validate joins; test for alignment and resolve mismatched identifiers.

### **Week 4 (Nov 3 – Nov 9)**  
Conduct exploratory data analysis (EDA) across both datasets; develop initial feature engineering strategies (e.g., shots ratio, cards differential, home-field advantage metrics).

### **Week 5 (Nov 10 – Nov 16)**  
Develop predictive models (classification and regression) evaluating match outcomes, season-level strengths, or expected goals based on integrated feature sets.

### **Week 6 (Nov 17 – Nov 23)**  
Visualize key findings; conduct data-quality analysis; prepare StatusReport.md.

### **Week 7 (Nov 24 – Nov 30)**  
Develop a reproducible workflow using Snakemake or an equivalent Run-All script; finalize metadata and documentation.

### **Week 8 (Dec 1 – Dec 7)**  
Polish figures; complete README and FAIR metadata; upload final curated data to Box.

### **Week 9 (Dec 8 – Dec 10)**  
Produce final project release; verify reproducibility; tag GitHub repo for submission.

---

## Constraints
No licensing or access constraints exist for Dataset 2 due to its public-domain status. Dataset 1 is openly available on Kaggle and can be redistributed with attribution.  
The main constraints relate to:
- complexity of team-name alignment across leagues,
- variation in season coverage across datasets, and
- selecting the most appropriate modeling techniques for our research questions.

---

## Gaps
We still need to:
- Determine which specific leagues and seasons from Dataset 1 most effectively align with the multi-decade coverage of Dataset 2.  
- Finalize whether our predictive modeling will focus on per-match prediction, per-team season prediction, or both.  
- Conduct deeper feature engineering to create meaningful cross-dataset metrics that support modeling.  
- Identify any edge cases where team identifier mismatches require manual correction.

---

## References
Excel4Soccer. (2023). *ESPN Soccer Data* [Dataset]. Kaggle. https://www.kaggle.com/datasets/excel4soccer/espn-soccer-data  

Football-Data.co.uk. (2023). *European Football Match Statistics* [Dataset]. Via datasets/football-datasets GitHub mirror. https://github.com/datasets/football-datasets  
