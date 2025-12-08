# Quick Start Guide

**IS477 Soccer Analytics Project - Get Started in Minutes**

---

## For Reviewers & Reproducers

This project uses **fully programmatic data acquisition** for complete reproducibility. Follow these steps to reproduce the entire analysis:

### Step 1: Clone Repository

```bash
git clone [your-repo-url]
cd is477project-main
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Set Up Kaggle API (One-Time Setup)

1. Go to: https://www.kaggle.com/settings
2. Click "Create New API Token"
3. Save `kaggle.json` to:
   - **Linux/Mac:** `~/.kaggle/kaggle.json`
   - **Windows:** `C:\Users\<USERNAME>\.kaggle\kaggle.json`

```bash
# On Linux/Mac, set permissions:
chmod 600 ~/.kaggle/kaggle.json
```

### Step 4: Acquire Data Programmatically

```bash
python acquire_data.py
```

**What happens:**
- ✅ Downloads ESPN Soccer Data from Kaggle (~12 MB)
- ✅ Clones European Football Statistics from GitHub (~5 MB)
- ✅ Calculates SHA-256 checksums for all files
- ✅ Generates acquisition metadata and reports

**Expected Runtime:** 3-5 minutes (depending on internet speed)

### Step 5: Verify Data Integrity

```bash
python acquire_data.py --verify-only
```

Expected output:
```
[OK] All checksums verified successfully!
```

### Step 6: Run Complete Analysis Pipeline

```bash
# Option A: Run all scripts sequentially
bash workflows/run_all.sh

# Option B: Use Snakemake workflow
snakemake --cores 1

# Option C: Run individual scripts
python scripts/01_acquire.py
python scripts/02_clean.py
python scripts/03_integrate.py
python scripts/04_quality.py
python scripts/05_analyze.py
python scripts/06_visualize.py
```

**Expected Total Runtime:** ~8-10 minutes

### Step 7: View Results

```bash
# Reports
ls outputs/reports/*.md

# Visualizations
ls outputs/figures/

# Trained Models
ls outputs/models/
```

---

## Troubleshooting

**Problem:** Kaggle credentials not found

**Solution:** Follow [Step 3](#step-3-set-up-kaggle-api-one-time-setup) carefully. See `DATA_ACQUISITION.md` for detailed instructions.

---

**Problem:** Git not installed

**Solution:** Install Git from https://git-scm.com/downloads

---

**Problem:** Download interrupted

**Solution:** The script is idempotent - just run it again:
```bash
python acquire_data.py
```

---

## For More Information

- **Data Acquisition Details:** See `DATA_ACQUISITION.md`
- **Full Project Documentation:** See `README.md`
- **Pipeline Validation:** Run `python workflows/validate_pipeline.py`

---

## Project Reproducibility Checklist

✅ **Programmatic data acquisition** - No manual downloads required
✅ **SHA-256 checksums** - Data integrity verification
✅ **Automated workflow** - Snakemake + Bash scripts
✅ **Version control** - All code in Git
✅ **Dependency management** - `requirements.txt`
✅ **Comprehensive documentation** - README, DATA_ACQUISITION, this guide

---

**Questions?** See `DATA_ACQUISITION.md` for detailed troubleshooting and manual download alternatives.
