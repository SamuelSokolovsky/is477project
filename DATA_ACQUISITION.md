# Data Acquisition Guide

**IS477 Soccer Analytics Project - Programmatic Data Acquisition**

This guide explains how to programmatically download and verify all datasets required for the Soccer Analytics project, ensuring complete reproducibility.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Dataset Overview](#dataset-overview)
4. [Kaggle API Setup](#kaggle-api-setup)
5. [Running the Acquisition Script](#running-the-acquisition-script)
6. [Directory Structure](#directory-structure)
7. [Verifying Data Integrity](#verifying-data-integrity)
8. [Troubleshooting](#troubleshooting)
9. [Manual Download (Alternative)](#manual-download-alternative)

---

## Prerequisites

### Required Software

1. **Python 3.11+**
   ```bash
   python --version  # Should be 3.11 or higher
   ```

2. **Git** (for Dataset 2)
   ```bash
   git --version  # Any recent version
   ```
   Download from: https://git-scm.com/downloads

3. **Internet Connection**
   - Required for downloading datasets
   - Estimated total download: ~20-50 MB

### Required Python Packages

Install all dependencies:

```bash
pip install -r requirements.txt
```

Key packages for data acquisition:
- `pandas` - Data processing
- `requests` - HTTP requests (optional)
- `GitPython` - Git operations (optional)

**Note:** `kagglehub` is no longer required as Dataset 1 is stored locally

---

## Quick Start

**For first-time users**, follow these steps:

### Step 1: Run the acquisition script

```bash
python scripts/01_acquire.py
```

That's it! The script will:
- ✅ Verify Dataset 1 (ESPN Soccer Data) - stored locally in repository
- ✅ Clone Dataset 2 (European Football Statistics) from GitHub
- ✅ Calculate SHA-256 checksums for all files
- ✅ Generate acquisition metadata and reports

**Expected Runtime:** 2-3 minutes (depending on internet speed)

**Note:** Dataset 1 is now included in the repository - no Kaggle API credentials needed!

---

## Dataset Overview

### Dataset 1: ESPN Soccer Data (Local)

**Source:** https://www.kaggle.com/datasets/excel4soccer/espn-soccer-data

**Storage:** Stored locally in repository at `data/raw/Dataset 1/`

**Description:** Comprehensive soccer statistics from ESPN including match fixtures, team statistics, standings, and team information.

**Files Included:**
- `teams.csv` (~500 KB) - Team information
- `teamStats.csv` (~11 MB) - Detailed team statistics
- `standings.csv` (~600 KB) - League standings
- `leagues.csv` (~140 KB) - League metadata

**License:** Community Data License Agreement - Permissive

**Method:** No download needed - files are included in the repository

---

### Dataset 2: European Football Match Statistics (GitHub)

**Source:** https://github.com/datasets/football-datasets

**Description:** Historical match results and statistics for 5 major European leagues (1993-2025).

**Leagues Included:**
- English Premier League
- Spanish La Liga
- Italian Serie A
- German Bundesliga
- French Ligue 1

**Key File:**
- `all_leagues_all_seasons.csv` (~5 MB) - Consolidated match data for all leagues

**Individual League Directories:**
- `datasets/english-premier-league/` - Season-by-season files
- `datasets/spanish-la-liga/` - Season-by-season files
- `datasets/italian-serie-a/` - Season-by-season files
- `datasets/german-bundesliga/` - Season-by-season files
- `datasets/french-ligue-1/` - Season-by-season files

**License:** PDDL 1.0 (Public Domain Dedication and License)

**Method:** Git clone

---

## ~~Kaggle API Setup~~ (No Longer Required)

> **UPDATE:** Dataset 1 is now stored locally in the repository. Kaggle API credentials are no longer needed!
>
> This section is kept for reference only.

<details>
<summary>Click to view deprecated Kaggle setup instructions (not needed)</summary>

### Detailed Setup Instructions

#### 1. Create a Kaggle Account

If you don't have one: https://www.kaggle.com/account/login

#### 2. Generate API Credentials

1. Log in to Kaggle
2. Go to **Account Settings**: https://www.kaggle.com/settings
3. Scroll down to the **API** section
4. Click **"Create New API Token"**
5. This will download `kaggle.json` to your computer

#### 3. Install kaggle.json

**On Windows:**

```powershell
# Create .kaggle directory
mkdir C:\Users\<YOUR_USERNAME>\.kaggle

# Move kaggle.json to the directory
move Downloads\kaggle.json C:\Users\<YOUR_USERNAME>\.kaggle\
```

**On Linux/Mac:**

```bash
# Create .kaggle directory
mkdir -p ~/.kaggle

# Move kaggle.json to the directory
mv ~/Downloads/kaggle.json ~/.kaggle/

# Set proper permissions (important!)
chmod 600 ~/.kaggle/kaggle.json
```

#### 4. Verify Installation

```bash
python -c "from pathlib import Path; print('Kaggle config:', Path.home() / '.kaggle' / 'kaggle.json', 'exists:', (Path.home() / '.kaggle' / 'kaggle.json').exists())"
```

Expected output:
```
Kaggle config: /Users/yourname/.kaggle/kaggle.json exists: True
```

</details>

---

## Running the Acquisition Script

### Basic Usage

```bash
# Download all datasets
python scripts/01_acquire.py
```

### Command-Line Options

```bash
# Force re-download (even if data exists)
python scripts/01_acquire.py --force

# Skip Kaggle dataset (only download GitHub data)
python scripts/01_acquire.py --skip-kaggle

# Skip GitHub dataset (only download Kaggle data)
python scripts/01_acquire.py --skip-github

# Only verify checksums (don't download)
python scripts/01_acquire.py --verify-only

# Get help
python scripts/01_acquire.py --help
```

### What Happens During Acquisition

The script performs these steps:

1. **Directory Setup**
   - Creates `data/raw/Dataset 1/` for Kaggle data
   - Creates `data/raw/Dataset 2/` for GitHub data
   - Creates `data/metadata/` for checksums and reports

2. **Dataset 1 Acquisition (Kaggle)**
   - Checks for existing Kaggle API credentials
   - Downloads ESPN Soccer Data using `kagglehub`
   - Copies files to `data/raw/Dataset 1/`
   - Calculates SHA-256 checksums

3. **Dataset 2 Acquisition (GitHub)**
   - Clones `https://github.com/datasets/football-datasets`
   - Places repository in `data/raw/Dataset 2/football-datasets/`
   - Calculates checksums for key files

4. **Metadata Generation**
   - Saves checksums to `data/metadata/checksums.txt`
   - Saves checksum JSON to `data/metadata/checksums.json`
   - Generates acquisition report: `data/metadata/acquisition_report.txt`

5. **Logging**
   - Console output shows progress
   - Detailed log saved to `data_acquisition.log`

---

## Directory Structure

After successful acquisition, your project structure will be:

```
is477project-main/
├── scripts/01_acquire.py                 # Data acquisition script
├── data/
│   ├── raw/
│   │   ├── Dataset 1/             # Kaggle data
│   │   │   ├── teams.csv
│   │   │   ├── teamStats.csv
│   │   │   ├── standings.csv
│   │   │   └── leagues.csv
│   │   └── Dataset 2/             # GitHub data
│   │       └── football-datasets/
│   │           ├── datasets/
│   │           │   ├── all_leagues_all_seasons.csv
│   │           │   ├── english-premier-league/
│   │           │   ├── spanish-la-liga/
│   │           │   ├── italian-serie-a/
│   │           │   ├── german-bundesliga/
│   │           │   └── french-ligue-1/
│   │           └── README.md
│   ├── processed/                 # Generated by analysis scripts
│   └── metadata/
│       ├── checksums.txt          # SHA-256 checksums
│       ├── checksums.json         # Checksums in JSON format
│       └── acquisition_report.txt # Acquisition summary
├── data_acquisition.log           # Detailed acquisition log
└── ...
```

---

## Verifying Data Integrity

### Why Verify Checksums?

SHA-256 checksums ensure:
- Data has not been corrupted during download
- Files match the expected versions
- Reproducibility of analysis results

### How to Verify

**Method 1: Using the acquisition script**

```bash
python scripts/01_acquire.py --verify-only
```

Expected output:
```
[OK] data/raw/Dataset 1/teams.csv
[OK] data/raw/Dataset 1/teamStats.csv
[OK] data/raw/Dataset 1/standings.csv
...
All checksums verified successfully!
```

**Method 2: Manual verification (Linux/Mac)**

```bash
cd data
sha256sum -c metadata/checksums.txt
```

**Method 3: Manual verification (Windows)**

```powershell
Get-FileHash -Algorithm SHA256 "data\raw\Dataset 1\teams.csv"
# Compare output with checksums.txt
```

**Method 4: Python script**

```python
import hashlib
from pathlib import Path

def verify_file(filepath, expected_checksum):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)

    actual = sha256_hash.hexdigest()
    return actual == expected_checksum

# Example
filepath = Path("data/raw/Dataset 1/teams.csv")
expected = "your_expected_checksum_here"
print(f"Valid: {verify_file(filepath, expected)}")
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: "Kaggle credentials not configured"

**Error:**
```
Kaggle API credentials not found!
Expected location: /Users/yourname/.kaggle/kaggle.json
```

**Solution:**
1. Follow the [Kaggle API Setup](#kaggle-api-setup) instructions
2. Ensure `kaggle.json` is in the correct location
3. On Unix systems, run: `chmod 600 ~/.kaggle/kaggle.json`

---

#### Issue 2: "Git not found"

**Error:**
```
Git not found. Please install Git: https://git-scm.com/
```

**Solution:**
1. Install Git from https://git-scm.com/downloads
2. Verify installation: `git --version`
3. Restart your terminal/command prompt
4. Try again

---

#### Issue 3: "kagglehub not installed"

**Error:**
```
kagglehub not installed. Run: pip install kagglehub
```

**Solution:**
```bash
pip install kagglehub
# Or install all requirements:
pip install -r requirements.txt
```

---

#### Issue 4: Download fails midway

**Solution:**
```bash
# The script is idempotent - safe to re-run
python scripts/01_acquire.py

# Or force complete re-download:
python scripts/01_acquire.py --force
```

---

#### Issue 5: "Permission denied" errors

**On Windows:**
- Run Command Prompt as Administrator

**On Linux/Mac:**
```bash
# Fix Kaggle credentials permissions
chmod 600 ~/.kaggle/kaggle.json

# Fix data directory permissions
chmod -R 755 data/
```

---

#### Issue 6: Slow download speeds

**Solutions:**
- Check your internet connection
- Try during off-peak hours
- For large files, use `--skip-kaggle` or `--skip-github` to download datasets separately

---

#### Issue 7: "Repository already exists" but data missing

**Solution:**
```bash
# Force fresh download
python scripts/01_acquire.py --force
```

---

### Getting Help

If you encounter issues not covered here:

1. Check the log file: `data_acquisition.log`
2. Run with verbose logging:
   ```bash
   python scripts/01_acquire.py 2>&1 | tee acquisition_output.txt
   ```
3. Review Kaggle API docs: https://github.com/Kaggle/kaggle-api
4. Check GitHub repository issues: https://github.com/datasets/football-datasets/issues

---

## Manual Download (Alternative)

If programmatic acquisition fails, you can download datasets manually:

### Dataset 1 (Kaggle) - Manual Download

1. Go to: https://www.kaggle.com/datasets/excel4soccer/espn-soccer-data
2. Click "Download" button
3. Extract ZIP to `data/raw/Dataset 1/`
4. Ensure these files exist:
   - `teams.csv`
   - `teamStats.csv`
   - `standings.csv`
   - `leagues.csv`

### Dataset 2 (GitHub) - Manual Download

**Option A: Git Clone**
```bash
cd data/raw/Dataset 2
git clone https://github.com/datasets/football-datasets.git
```

**Option B: Direct Download**
1. Go to: https://github.com/datasets/football-datasets
2. Click "Code" → "Download ZIP"
3. Extract to `data/raw/Dataset 2/football-datasets/`

### After Manual Download

Generate checksums:
```bash
python -c "
from acquire_data import SoccerDataAcquisition
acquirer = SoccerDataAcquisition()
acquirer._save_checksums()
"
```

---

## Best Practices

### For Reproducibility

1. ✅ **Always use programmatic acquisition** when possible
2. ✅ **Document any manual steps** if needed
3. ✅ **Verify checksums** after download
4. ✅ **Commit checksums.txt** to version control
5. ✅ **Never commit raw data** to Git (use .gitignore)

### For Data Management

1. ✅ Keep raw data separate from processed data
2. ✅ Don't modify files in `data/raw/`
3. ✅ Use `data/processed/` for cleaned data
4. ✅ Keep metadata in `data/metadata/`

---

## Next Steps

After successful data acquisition:

1. **Verify data:**
   ```bash
   python scripts/01_acquire.py --verify-only
   ```

2. **Run data cleaning:**
   ```bash
   python scripts/02_clean.py
   ```

3. **Continue with analysis pipeline:**
   ```bash
   bash workflows/run_all.sh
   ```

---

## Appendix: Technical Details

### Checksum Format

`checksums.txt` format:
```
# SHA-256 Checksums for Soccer Analytics Dataset
# Generated: 2025-12-07 12:00:00
#======================================================================

69a836fbba90e275...  data/raw/Dataset 1/teams.csv
a9f233ba3ad7f6e2...  data/raw/Dataset 1/teamStats.csv
```

### API Endpoints Used

**Kaggle:**
- API: `kagglehub.dataset_download("excel4soccer/espn-soccer-data")`
- Endpoint: Kaggle's official API

**GitHub:**
- Repository: `https://github.com/datasets/football-datasets.git`
- Protocol: Git clone over HTTPS

### Data Provenance

All datasets include:
- Source URL
- Download date/time
- SHA-256 checksum
- File size
- License information

Stored in: `data/metadata/acquisition_report.txt`

---

## License & Attribution

**Dataset Licenses:**
- Dataset 1: Community Data License Agreement (CDLA)
- Dataset 2: PDDL 1.0 (Public Domain)

**Acquisition Script:**
- MIT License
- Author: IS477 Student
- Course: Data Management, Curation, and Reproducibility

---

## Updates & Maintenance

To update datasets with latest data:

```bash
# Update GitHub repository (Dataset 2)
cd data/raw/Dataset 2/football-datasets
git pull

# Re-download Kaggle dataset (Dataset 1)
python scripts/01_acquire.py --force

# Verify new checksums
python scripts/01_acquire.py --verify-only
```

---

**Last Updated:** December 7, 2025
**Version:** 1.0
**Contact:** [Your Email] for questions or issues
