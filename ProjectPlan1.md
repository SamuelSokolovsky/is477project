## Overview
The goal of our project is to analyze professional soccer data to identify patterns and relationships between team statistics and match outcomes. Using historical 
match data, player performance metrics, and team statistics, we aim to build a predictive model capable of forecasting game results and season standings. 
By integrating multiple data sources, we hope to uncover key performance indicators (KPIs) that drive success in professional soccer leagues.

Beyond modeling, this project also aims to demonstrate a complete, reproducible data-management lifecycle aligned with IS 477 content(from acquisition and 
integration to cleaning, documentation, and workflow automation). Our work will adhere to reproducibility and transparency principles (FAIR + CARE) 
through applying to a real-world sports analytics context.

## Research Questions:
- What factors or stats, for example, possession, shots on target, passing accuracy, and other(s) can best predict the outcome of a soccer match?
- Can we use historical team and player data to accurately predict results for future matches or entire seasons?
- How do trends in performance vary across leagues and seasons?
- To what extent do a team’s in-season performance metrics (e.g., goal differential, passing accuracy, shots on target) explain or predict its Soccer Power Index (SPI) rating?
This reframes SPI as a dependent variable representing overall team strength, enabling statistical analysis of which observable metrics contribute most strongly to team ratings.

## Team:
We will both contribute to as many sections of the project as possible and will work collaboratively to ensure the project is up to our standards. We will 
try not to strictly divide up the work.

## Datasets:
Two datasets from Kaggle were used in this study. The first, ESPN's Soccer Power Index (Soham, 2023), is hereafter referred to as Dataset 1. The second, 
ESPN Soccer Data (Excel4Soccer, 2023) is hereafter referred to as Dataset 2. Both datasets provide complementary statistics on team performance and ratings 
across major football leagues. Overview of Dataset 1Dataset 1 (Excel4Soccer 2023) contains match-level and team-level data for the 2024-25 season, 
organized across multiple CSV files (fixtures.csv, teamStats.csv, standings.csv, teams.csv, etc.). Covers > 30,000 matches, 400 + leagues, 3,000 teams, 
45,000 players. Key attributes we've identified: possession, shots, fouls, passes, goals, team IDs, and season type. Based on our current understanding, 
these files will be merged by identifiers(teamId and eventId) to create per-team season aggregates. Overview of Dataset 2Dataset 2 covers 217 national 
teams and major clubs across top leagues (Premier League, La Liga, Bundesliga, Serie A, Ligue 1). Source: FiveThirtyEight SPI dataset (spi_global_rankings.csv). 
Provides forward-looking metrics such as spi, off, def, rank, and league. It represents the predictive strength dimension of team performance.

## Integration plan:
TeamName and league fields will be standardized (lowercasing, removing accents and special characters) and used to obtain identifiers to form aggregates. 
The resulting aggregate table will combine SPI ratings with real-world match statistics to evaluate predictive relationships.

## Timeline & Implementation Plan:
Week 1 (Oct 13 – Oct 19) — Explore both datasets, review schemas, and draft an ER diagram and preliminary data dictionary.

Week 2 (Oct 20 – Oct 26) — Clean and standardize team names, league identifiers, and season fields across datasets.

Week 3 (Oct 27 – Nov 2) — Integrate datasets in pandas/DuckDB; test joins and validate data alignment.

Week 4 (Nov 3 – Nov 9) — Conduct exploratory data analysis (EDA) and feature engineering for key metrics (e.g., possession, shots, SPI).

Week 5 (Nov 10 – Nov 16) — Build and evaluate predictive models (KNN, Linear Regression) using the integrated dataset.

Week 6 (Nov 17 – Nov 23) — Visualize findings, summarize data-quality results, and prepare StatusReport.md milestone.

Week 7 (Nov 24 – Nov 30) — Develop reproducible workflow (Snakemake / Run-All script) and finalize metadata documentation.

Week 8 (Dec 1 – Dec 7) — Polish figures, finalize README and FAIR metadata; upload curated data to Box.

Week 9 (Dec 8 – Dec 10) — Complete final project release, verify reproducibility, and tag the GitHub repository for submission.

## Constraints:
There are no known constraints at this time with the data. The only constraint we have is our knowledge of predictive models and figuring out exactly 
how to get the most accurate model.

## Gaps:
We still need to finalize which leagues and seasons will be included in our analysis to ensure that our datasets align properly. Additionally, we must 
confirm the exact modeling technique we will use, whether it will be a regression or classification approach, based on the type of predictions we are trying
to make. Another potential gap is the need for more detailed player-level data, which could help improve the accuracy and depth of our model. Finally, 
we anticipate possible integration challenges if the datasets use different identifiers, naming conventions, or formats that require extra preprocessing 
to align correctly.

## References:
Excel4Soccer. (2023). ESPN Soccer Data [Data set 1]. Kaggle. https://www.kaggle.com/datasets/excel4soccer/espn-soccer-data Soham. (2023). 

ESPN's Soccer Power Index [Data set 2]. Kaggle. https://www.kaggle.com/datasets/soham1024/espns-soccer-power-index
