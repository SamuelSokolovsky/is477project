# Workflow Diagram

## Soccer Analytics Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      DATA ACQUISITION                            │
│                     (01_acquire.py)                              │
│                                                                   │
│  ┌──────────────────┐         ┌──────────────────┐             │
│  │  Dataset 1       │         │  Dataset 2       │             │
│  │  (ESPN Kaggle)   │         │  (Football.co.uk)│             │
│  └────────┬─────────┘         └────────┬─────────┘             │
│           │                            │                        │
│           └────────────┬───────────────┘                        │
│                        │                                        │
│                   Generate SHA-256                              │
│                   Checksums                                     │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA CLEANING                               │
│                     (02_clean.py)                                │
│                                                                   │
│  • Standardize team names                                       │
│  • Handle missing values                                        │
│  • Validate data types                                          │
│  • Create mapping dictionaries                                  │
│                                                                   │
│  Output: dataset1_clean.csv, dataset2_clean.csv                 │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                     DATA INTEGRATION                             │
│                     (03_integrate.py)                            │
│                                                                   │
│  • Align schemas                                                │
│  • Merge on common fields                                       │
│  • Generate match_id                                            │
│  • Validate merge results                                       │
│                                                                   │
│  Output: integrated_dataset.csv                                 │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                   QUALITY ASSESSMENT                             │
│                     (04_quality.py)                              │
│                                                                   │
│  Assess 5 Quality Dimensions:                                   │
│  1. Completeness   → Missing value analysis                     │
│  2. Validity       → Constraint checking                        │
│  3. Consistency    → Cross-field validation                     │
│  4. Accuracy       → Sample verification                        │
│  5. Uniqueness     → Duplicate detection                        │
│                                                                   │
│  Output: data_quality_report.md                                 │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                  ANALYSIS & MODELING                             │
│                     (05_analyze.py)                              │
│                                                                   │
│  1. Feature Engineering                                         │
│     • Shot accuracy, differentials                              │
│     • Form metrics (last 5 games)                               │
│                                                                   │
│  2. Exploratory Data Analysis                                   │
│     • Correlation analysis                                      │
│     • League comparisons                                        │
│                                                                   │
│  3. Predictive Modeling                                         │
│     • Match outcome classifier                                  │
│     • Goals regression                                          │
│                                                                   │
│  Output: Trained models, performance metrics                    │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                     VISUALIZATION                                │
│                     (06_visualize.py)                            │
│                                                                   │
│  Generate Visualizations:                                       │
│  • Feature importance plots                                     │
│  • Performance trends over seasons                              │
│  • League comparison charts                                     │
│  • Correlation heatmap                                          │
│  • Model performance metrics                                    │
│                                                                   │
│  Output: All figures in outputs/figures/                        │
└─────────────────────────────────────────────────────────────────┘
```

## Dependency Graph

The Snakemake workflow manages these dependencies automatically:

```
acquire_data
    │
    ├─→ clean_data
    │       │
    │       └─→ integrate_data
    │               │
    │               ├─→ assess_quality
    │               │
    │               └─→ analyze
    │                       │
    │                       └─→ visualize
```

## Execution Options

### Option 1: Run All (Bash Script)
```bash
bash workflows/run_all.sh
```
Runs all scripts sequentially from start to finish.

### Option 2: Snakemake (Recommended)
```bash
snakemake --cores 4
```
Runs only necessary steps, skipping unchanged inputs.

### Option 3: Individual Scripts
```bash
python scripts/01_acquire.py
python scripts/02_clean.py
# ... etc
```
Useful for debugging individual steps.

---

## Data Flow Summary

| Stage | Input | Output | Key Operations |
|-------|-------|--------|----------------|
| Acquire | Raw sources | data/raw/ | Download, checksum |
| Clean | data/raw/ | data/processed/*_clean.csv | Standardize, validate |
| Integrate | Cleaned datasets | integrated_dataset.csv | Merge, align schemas |
| Quality | Integrated data | Quality report | Assess 5 dimensions |
| Analyze | Quality-checked data | Models, metrics | Feature eng., modeling |
| Visualize | Analysis results | Figures | Generate plots |
