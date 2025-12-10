# Integrated European Soccer Analytics Project

Predictive Modeling and Data Curation Across 32 Years of European Soccer
Contributors:
This project was completed by Yongyang Fu (ORCID:https://orcid.org/0009-0009-6222-4732) and Sam Sokolovsky for IS 477: Data Management, Curation, and Reproducibility at the University of Illinois Urbana-Champaign Fall 2025.


The project that we decided to create looks at thirty-two years of European soccer data from the top five leagues which are the Premier League, La Liga, Bundesliga, Serie A, and Ligue 1. We were motivated by the challenge of combining different historical datasets and making an analytical framework that could answer both practical and theoretical questions about soccer performance, prediction, and long-term trends in the sport. Our goal was to determine how predictable game outcomes are based only on game-level stats, how scoring and home-advantage patterns have shifted over time, and how data quality affects what types of analyses are possible.

To address these goals, we developed a six-phase pipeline that guides data through acquisition, cleaning, schema integration, quality assessment, predictive modeling, and visualization. All steps are fully automated using Python scripts and a single workflow script (`run_all.sh`), allowing others to replicate the entire analysis with no manual data handling. The datasets we used include a large public-domain archive of match statistics from Football-Data.co.uk, along with team and league metadata from a Kaggle ESPN dataset. After integrating these sources and standardizing 244 team names across multiple leagues and years, our final dataset contains 57,865 matches played between 1993 and 2025. The combined dataset includes match identifiers, goal statistics, disciplinary events, shot metrics, referee assignments, and derived features such as accuracy and differential statistics.

Using this base dataset, we trained three machine learning models which were logistic regression, random forest, and gradient boosting, to predict the result of the game. Our model predicted either a home win, tie, or away win. Each model reached approximately 58.9% accuracy, which was a large improvement over the 33% baseline expected from random guessing. The performance of the model showed us some important patterns in the data. Those were that shots on target and shot accuracy were the most informative predictors, while ties were extremely difficult to predict, showing the randomness of evenly matched games. This is also true in real life as a tie is usually the least likely chance or highest odds when trying to bet on a game with two fairly even teams. Home wins were easier to predict due to the influence of home filed advantage which has been there over many years.

However, our long-term trend analysis also showed how the sport has evolved and how that advantage is not as effective as it used to be. Home advantage has declined over time, dropping from nearly 49% home win rates in the late 1990s to closer to 40-46% in recent years, especially during the COVID-19 period when stadiums were empty. This particular result showed that a home crowd can influence the result of a game and they can boost the team to a win.  Also, away team scoring has increased over the past three decades, and average goals per game started growing from the mid-2000s onward. These patterns highlight tactical innovations, increased attacking play, and changing environmental conditions within professional soccer.

The project concludes with a full collection of our final results, including processed datasets, figures, model files, metadata, documentation, and acquisition logs,that allow anyone to repeat the full analysis from start to finish. By following FAIR and reproducibility principles, this project demonstrates the importance of transparent data workflows and responsible data curation in computational research.


## Data Profile

In our project, we used two main datasets that have differences in structure, historical coverage, and licensing. The first and largest dataset comes from Football-Data.co.uk, which gives many years of match-level statistics across major European leagues. This dataset is openly licensed under the Public Domain Dedication License (PDDL 1.0), meaning it can be reused freely. It includes results, goals, shots, fouls, corners, cards, referee assignments, and betting odds. Other detailed stats such as shots and corners are available mostly from 2005 onward, while the earlier seasons contain only the main results. Since the data has no personal identifying information and is already publicly available, there are no ethical concerns that come with this dataset. All usage complies with its public-domain status, and the data is acquired programmatically using our scripts rather than placed in the repository.

The second dataset supplements the first by providing team names, team statistics, and league mappings from the ESPN Soccer Dataset on Kaggle. It is licensed under the CDLA, which allows use for research but prevents redistribution. To comply with this license, our project does not include these files in the repository. Instead, data is downloaded locally through our acquisition script (`01_acquire.py`), which records checksums and metadata to make sure everything is transparent and reproducible. This dataset contains no sensitive personal information as it primarily provides metadata that improves integration by establishing consistent team naming conventions across data sources.

After combining the datasets, we had a combined dataset containing 38 columns across several categories which included match identifiers, team names that were standardized as well as original, goals scored, halftime scores, shots, shots on target, fouls, corners, yellow and red cards, referee assignments, and several calculated features such as shot accuracy, goal differential, and binary outcome indicators. Since neither dataset had unique match identifiers originally, we generated deterministic IDs based on match date, league, and team names. This made sure that every match in the integrated dataset could be referenced across scripts and analyses.

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

For a comprehensive reference of all fields, data types, valid ranges, and sources, please see our **data dictionary** at `docs/data_dictionary.md`. This document provides detailed descriptions of each column, including transformation notes, data quality information, and known issues for each field in the integrated dataset.

All data is organized in a structured directory layout which shows the differences between raw data, processed data, and metadata. Raw files are excluded from GitHub through `.gitignore` to comply with licensing and storage constraints. Processed data such as `integrated_dataset.csv`, team name mappings, and acquisition metadata are retained because they can be regenerated programmatically. The system allows any user to reproduce the complete dataset without manual downloads simply by running the acquisition script.

Together, these datasets support a wide range of analyses,from descriptive statistics to machine learning models,and their integration reflects practices in schema alignment, standardization, and ethical data reuse.



## Data Quality

We evaluated data quality across five categories which were completeness, validity, consistency, accuracy, and uniqueness. Completeness varied depending on the historical period. Core fields such as match dates, teams, goals, and results were completely filled across all 57,865 matches. However, detailed statistical fields such as shots, corners, and fouls were often missing before 2005. We assumed this is due to the lack of technology that tracked these stats before 2005. On average, rows were about 88% complete, but completeness rose dramatically in modern seasons. Additionally, referee assignments were available for only about 19% of matches which was pretty low and could pose some challenges.

Some of our validity checks brought a few issues to light. First, we found two games where a team recorded fewer total shots than shots on target, and three similar issues on the away side. These issues are most likely from data entry errors but affect less than 0.01% of the dataset. It was also possible that these were the true stats as teams can score goals on their own net accidentally which are not shots on target meaning this could have been accurate data so we kept it in. All goals, card counts, and foul numbers were within expected ranges, and all match dates fell within a valid timeline.

Consistency checks showed strong quality across all the fields. Results always matched goal differentials, binary outcome indicators correctly reflected match outcomes, and halftime results aligned with halftime goal counts. The only exception was a single rounding error in shot accuracy. Cross-season consistency was also strong, with no mismatched league codes or irregular season boundaries.

Accuracy was assessed through distributional checks. The average number of goals per match (2.67) was consistent with historical norms in European soccer. Home teams won roughly 46% of matches, a finding that is similar to global soccer statistics. No records showed impossible values such as negative goals or excessively large numbers. 

Uniqueness checks confirmed that all match IDs were distinct and that no duplicate matches existed. Altogether, our assessment rated the data as good, with some missing values in older seasons and very few things that were out of the ordinary. After filtering to post-2005 matches, completeness increases to about 70% for event-level statistics, making that portion of the data very strong for modeling or fine-grained analysis.

## Findings

Our analysis produced several meaningful findings about European soccer. First, our predictive modeling efforts demonstrated that match outcomes are moderately predictable using only match-level statistics. Across logistic regression, random forest, and gradient boosting models, accuracy consistently hovered around 58.9%, substantially above the 33% random baseline for predicting three outcomes. The models identified shots on target, shot accuracy, and shot differentials as the most influential predictors, confirming the centrality of attack quality in determining match outcomes. Results that were tied were usually hard to classify, with extremely low recall rates because draws come from a variety of game patterns, including defensive stalemates and evenly balanced contests.

Second, long-term analysis revealed clear shifts in the sport. Home advantage, once a dominant feature, has slowly weakened. In the late 1990s, home teams won nearly half of their matches where today, win percentages often fall closer to 40-46%. This decline was even more clear during the COVID-19 years, when empty stadiums reduced crowd influence. Meanwhile, away teams slowly increased their average goals per match, rising from around 1.0 in the mid-1990s to about 1.35 by 2025.

Third, league-level comparisons showed that each league has its own statistical identity. Serie A and La Liga display the strongest home-advantage effects, whereas the Premier League is the most balanced. The Bundesliga records the highest scoring rates, while La Liga tends to have more fouls and disciplinary actions. Across all leagues and seasons, the single most common scoreline was the 1-1 draw, which occurred in more than 12% of matches. These things are also pretty accurate with the public perception of these leagues as Serie A and Ligue 1 have a lot of very passionate fans, the Premier League is the strongest league overall, and many teams from La Liga like to play physically.

These findings show how the combined dataset allow for both predictive and descriptive insights into large-scale soccer behavior.

For comprehensive findings, detailed statistics, and in-depth analysis, please review our complete results document:

**[Project Results (outputs/project_results.md)](outputs/project_results.md)**

This document provides:
- Detailed quantitative findings across all 57,327 matches
- Comprehensive model performance analysis and evaluation metrics
- In-depth data quality assessment results
- League-specific statistical breakdowns
- Complete methodology documentation
- References to all generated visualizations and reports


## Future Work

There are many opportunities for extending this project. One important direction is the integration of player-level statistics, such as passes, assists, distances covered, and expected-goals (xG) metrics. These features would enable for even more accurate predictive models which could evaluate player contributions, detect tactical patterns, or estimate value in the transfer market. Another extension would incorporate contextual information including weather, stadium characteristics, and referee tendencies, which could give another variable that would be used in both modeling and causal inference.

From a modeling perspective, deep learning approaches such as LSTMs or Transformers could be used to model dependencies across seasons or sequences of actions within matches. Ensemble blending might also raise predictive accuracy by combining multiple types of models. Expanding the dataset to include additional leagues, international competitions, women’s soccer, or second-division play would make the dataset more globally representative and broaden the scope of analysis.

Finally, the development of real-time prediction systems could allow for minute-by-minute win probability estimates or live match analytics, which could support broadcasters, fans, and sports betting markets. In short, while our current project offers a complete analysis of historical match statistics, it also opens the door to many future ideas that can help expand the reach of our project.


## Reproducing the Analysis

For a visual overview of the complete data pipeline and workflow dependencies, please refer to the **workflow diagram** at `docs/workflow_diagram.md`. This diagram illustrates the six-stage process from data acquisition through visualization, showing how each script connects and what outputs are generated at each stage.

Anyone can reproduce the full workflow by running these steps in a terminal one by one:

Note that the main branch is required to reproduce the entire project using the latest version of scripts and methods

git clone --branch main --single-branch https://github.com/SamuelSokolovsky/is477project.git
cd is477project
pip install -r requirements.txt
python scripts/01_acquire.py
bash workflows/run_all.sh


All processed data, model outputs, and figures will appear automatically in the `outputs/` directory, and the integrated dataset will be saved to `data/processed/integrated_dataset.csv`.


## References

Football-Data.co.uk. (2025). Historical Soccer Results. Public Domain. (https://github.com/datasets/football-datasets)

Excel4Soccer. (2024). ESPN Soccer Data. Kaggle.](https://www.kaggle.com/datasets/excel4soccer/espn-soccer-data)

Constantinou, A. C., & Fenton, N. E. (2012). Solving the problem of inadequate scoring rules for probabilistic football models. Journal of Quantitative Analysis in Sports, 8(1).

Rein, R., & Memmert, D. (2016). Big data and tactical analysis in elite soccer. SpringerPlus, 5(1).


### Appendix
Code getting data using API from kaggle

Directory structure
  your_file_name/
  └── is477project/
      ├── scripts/          
	├──01_acquire ← Main Kaggle download script
      ├── data/
      │   ├── raw/
      │   │   └── Dataset 1/       ← Kaggle data downloaded here
      │   │       ├── teams.csv
      │   │       ├── teamStats.csv
      │   │       ├── standings.csv
      │   │       └── leagues.csv
      │   └── metadata/
      │       ├── checksums.txt
      │       └── checksums.json
      ├── scripts/
      │   └── 01_acquire.py        ← Verification script
      └── .env                     ← Kaggle credentials stored here

The code for downloading data using Kaggle API is in is477project/scripts/ acquire_data.py at

  def acquire_dataset1_kaggle(self):
      """
      Download Dataset 1 from Kaggle using kagglehub.

      Dataset: ESPN Soccer Data
      Source: https://www.kaggle.com/datasets/excel4soccer/espn-soccer-data
      """
      logger.info("="*70)
      logger.info("ACQUIRING DATASET 1: ESPN Soccer Data (Kaggle)")
      logger.info("="*70)

      # Check credentials
      if not self._check_kaggle_credentials():
          logger.warning("Dataset 1 will be skipped due to missing credentials")
          return

      # Check if data already exists
      expected_files = ['teams.csv', 'teamStats.csv', 'standings.csv', 'leagues.csv']
      all_exist = all((self.dataset1_dir / f).exists() for f in expected_files)

      if all_exist and not self.force_download:
          logger.info("Dataset 1 files already exist. Use --force to re-download")
          logger.info("Calculating checksums for existing files...")
          for filename in expected_files:
              filepath = self.dataset1_dir / filename
              checksum = self._calculate_checksum(filepath)
              relative_path = filepath.relative_to(self.base_dir)
              self.checksums[str(relative_path)] = checksum
              logger.info(f"  {filename}: {checksum[:16]}...")
          return

      # Download using kagglehub with correct API
      try:
          import kagglehub

          logger.info("Downloading from Kaggle (this may take a few minutes)...")
          logger.info("Dataset: excel4soccer/espn-soccer-data")

          # Download entire dataset to kagglehub cache
          download_path = kagglehub.dataset_download("excel4soccer/espn-soccer-data")
          logger.info(f"Dataset downloaded to cache: {download_path}")

          # Copy the files we need to our project directory
          # Files are in the base_data subdirectory
          source_dir = Path(download_path) / "base_data"

          logger.info("Copying files to project directory...")
          for filename in expected_files:
              source_file = source_dir / filename
              dest_file = self.dataset1_dir / filename

              if source_file.exists():
                  # Copy the file
                  shutil.copy2(source_file, dest_file)

                  # Calculate checksum
                  checksum = self._calculate_checksum(dest_file)
                  relative_path = dest_file.relative_to(self.base_dir)
                  self.checksums[str(relative_path)] = checksum

                  # Get file size
                  size_mb = dest_file.stat().st_size / (1024 * 1024)

                  logger.info(f"  [OK] {filename} ({size_mb:.2f} MB)")
                  logger.info(f"       SHA-256: {checksum[:16]}...")
              else:
                  logger.warning(f"  [WARN] {filename} not found in downloaded dataset")

          logger.info("Dataset 1 acquisition complete!")
          logger.info(f"Files saved to: {self.dataset1_dir}")

      except ImportError:
          raise DataAcquisitionError(
              "kagglehub not installed. Run: pip install kagglehub"
          )
      except Exception as e:
          raise DataAcquisitionError(f"Failed to download Kaggle dataset: {e}")

  Credential Checking (lines 145-194)

  def _check_kaggle_credentials(self) -> bool:
      """
      Check if Kaggle API credentials are configured.

      Checks multiple sources in order:
      1. Environment variables (KAGGLE_USERNAME, KAGGLE_KEY)
      2. kaggle.json file at ~/.kaggle/kaggle.json
      """
      # Check environment variables first
      has_env_vars = bool(os.getenv('KAGGLE_USERNAME') and os.getenv('KAGGLE_KEY'))

      # Check for kaggle.json file
      kaggle_json = Path.home() / '.kaggle' / 'kaggle.json'
      has_json_file = kaggle_json.exists()

      if has_env_vars:
          logger.info("Kaggle API credentials found (environment variables)")
          return True
      elif has_json_file:
          logger.info(f"Kaggle API credentials found ({kaggle_json})")
          return True
      else:
          # [Warning messages omitted for brevity]
          return False




