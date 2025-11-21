# StatusReport.md – Interim Status Report

## Overview
This interim status report summarizes the progress our team has made toward the objectives outlined in our updated project plan. Our project seeks to analyze professional soccer data from two large, complementary datasets to identify performance patterns, evaluate long-term trends, and build predictive models that forecast match outcomes. Over the past several weeks, our efforts have focused on dataset discovery, validation, acquisition, early integration work, exploratory cleaning, reproducibility design, and the initial preparation of the data structures needed to support downstream modeling.

Our progress has been shaped by challenges associated with dataset licensing, inconsistent structures across candidate datasets, and the high standard of data quality required by our research questions. As a result, we dedicated significantly more time than originally planned to sourcing, validating, and assembling Dataset 2, ultimately improving the long-term reliability and reproducibility of our project.

## Progress on Dataset Acquisition and Preparation

### Dataset 2 Progress
The first major task in this phase involved selecting a suitable replacement for our original Dataset 2 (SPI Global Rankings). Early discovery work revealed that the previously proposed SPI dataset did not meet the transparency, licensing, or structural standards required under IS 477 guidelines. With assistance from Perplexity AI, we examined multiple alternative datasets, including several listed in our dataset folder such as spi_global_rankings and club-football-match-data-2000-2025. Each of these candidates was ultimately abandoned. In most cases, licensing restrictions prevented redistribution or reuse within a reproducible academic workflow. In others, critical data fields were missing or were embedded in incompatible structures that would obstruct integration with Dataset 1.

This preliminary evaluation significantly informed our understanding of the data landscape and highlighted the need for a dataset that offered multi-decade match-level depth, high schema consistency, and clearly open licensing. These constraints led us to adopt the “football-datasets” repository, which mirrors data from football-data.co.uk under a PDDL 1.0 public-domain license. This dataset offers over twenty-five years of match-level statistics across the five major European leagues.

We invested substantial time into reproducing and understanding the source repository, including running the processing scripts, regenerating metadata packages, validating schemas, and resolving OS-specific path errors. During this process, we constructed a new consolidated master dataset that includes all leagues and all seasons. The consolidation pipeline is fully documented and reproducible. To regenerate our final version of Dataset 2, the user must run the notebook titled “[temp] preparation and producing consolidated Dataset2 csv file,” located in `is477project-main/data/Dataset 2/football-datasets`. This notebook loads every league’s datapackage.json, reads all corresponding CSVs, adds provenance columns, and produces a unified file named `all_leagues_all_seasons.csv`.

Beyond meeting the technical needs of the project, the revised Dataset 2 now aligns fully with the project’s goals, ethical requirements, and reproducibility expectations.

### Dataset 1 Progress
Work on Dataset 1 progressed in parallel. The ESPN Soccer Data (Excel4Soccer, 2023) collection includes a broad set of CSV files covering match-level and team-level statistics for the 2024–25 season. Sam began by downloading the five league folders and the base data folder, then examined the English Premier League (EPL) season as our initial focus area.

Through exploratory scripting, he imported the CSV files, identified the EPL’s league ID through the leagues.csv file, and filtered both the standings.csv and related files to isolate EPL-specific records. He then mapped team IDs to their corresponding names, removed unnecessary fields, and joined all relevant objects into a streamlined and human-interpretable table. This work produced a clean and structured dataset for the EPL season, which has been uploaded to the GitHub repository.

Dataset 1 is now largely prepared for integration, pending final refinements to variable selection and the creation of derived metrics that will be relevant to our modeling tasks.

## Integration Progress
Although the full integration workflow is scheduled for Weeks 3 and 4 of the project plan, we have already begun preparing the required alignment mechanisms. Our integration plan, originally described in the project plan, involves standardizing team names, league identifiers, and season representations across both datasets. We have already identified several cases where team names appear differently between the sources (“Man United” vs. “Manchester United,” for example), and we have drafted early mapping logic that will be implemented during the formal integration phase.

The consolidated Dataset 2 master file, with added league_name fields and consistent schema, is now well-positioned to connect to Dataset 1. Dataset 1’s internal keys (teamId, eventId) will allow us to generate season-level aggregates that can later be joined with Dataset 2’s long-term match histories.

At this stage, we have validated that the datasets are compatible in structure and that integration is feasible with careful standardization and mapping.

## Updated Timeline and Status of Tasks
Our initial schedule laid out a week-by-week plan beginning in mid-October. While we have made progress in most areas, we devoted additional time to dataset sourcing and reproducibility—an investment that strengthens the integrity of the project but slightly delays downstream tasks.

The Week 1 objective of reviewing schemas and drafting data dictionaries was completed on schedule. However, Weeks 2 and 3, originally allocated to cleaning and integration, were absorbed by the extended dataset evaluation and preparation work required for Dataset 2. As of now, the consolidation of Dataset 2 and the preliminary cleaning of Dataset 1 have been completed, meeting the foundational requirements for integration.

We will now proceed with the original Week 3 and Week 4 tasks: formal data integration, EDA, and feature engineering. Predictive model development, originally slated for Week 5, will follow once the integrated analytical tables are complete. Modeling remains on the critical path for addressing our research questions, and the extra preparatory work ensures that the datasets now meet the required standard for such analysis.

Our remaining timeline continues as planned, with workflow automation, metadata finalization, visualization refinement, and the final project report scheduled for late November and early December.

## Changes to the Original Project Plan
Several adjustments were made to the project plan as we progressed through the early phases. The most significant change relates to Dataset 2. The original dataset (FiveThirtyEight SPI) lacked the multi-season depth, structural detail, and licensing clarity required for our project. As our research questions require building predictive models across teams, seasons, and leagues, we determined that the data must include extensive match-level attributes spanning many years. This led to a full replacement of Dataset 2 and the creation of a reproducible consolidation pipeline.

We also extended the time allocated to data selection and preprocessing. These tasks proved more complex than initially expected, largely because our research questions require high-fidelity data and the ability to combine multiple statistical dimensions. Spending extra time here has strengthened the foundation for modeling and will enhance the reliability of our analytical results.

No major changes were made to the research questions themselves, but our understanding of the modeling requirements deepened. We now recognize that advanced machine-learning methods will be necessary, and our data preparation work reflects this requirement.

## Team Member Contributions

### Andrew’s Contribution Statement
At the beginning of the project, I focused on identifying a suitable replacement for Dataset 2. Using Perplexity AI and other external search tools, I evaluated multiple candidate datasets, including several listed in our folder such as spi_global_rankings and club-football-match-data-2000-2025. After examining their licensing restrictions, schema inconsistencies, and overall suitability for integration, I concluded that none of these options met the standards required for IS 477. This evaluation led us to adopt the football-datasets repository. I then worked extensively on reproducing the repository’s processing scripts, understanding the datapackage metadata system, resolving errors, and producing a fully consolidated master dataset using a standardized and reproducible workflow. My work ensures that Dataset 2 meets our project’s requirements for transparency, completeness, and reproducibility. I also contributed to shaping our integration plan and updating our understanding of the project’s technical challenges.

### Sam’s Contribution Statement
I began my work by exploring Dataset 1, the ESPN Soccer Data collection. I downloaded all the necessary zip folders and began cleaning and preparing the English Premier League portion of the dataset for use. I imported the CSV files, used the leagues CSV to locate the EPL league ID, filtered the standings dataset accordingly, and joined team IDs to team names to make the data interpretable. I removed unnecessary fields and organized the dataset into a format suitable for analysis. The resulting structured EPL dataset has been added to our repository. I have also begun preliminary exploration of the variables that will be most relevant to our modeling stage. I will continue refining the dataset and preparing it for integration with Dataset 2, after which I will shift toward developing predictive models and generating visualizations.

## Conclusion
In summary, although our early stages required more effort than originally planned due to the challenges of sourcing and preparing high-quality datasets, we have made significant progress. We now have a fully consolidated, reproducible Dataset 2 and a cleaned, structured Dataset 1 ready for integration. The project is positioned to move into its next phases, including EDA, feature engineering, integration, and predictive modeling. Our updated timeline reflects the additional work completed, and we remain on track to deliver a complete and rigorous end-to-end data curation and analysis workflow by the final project deadline.
