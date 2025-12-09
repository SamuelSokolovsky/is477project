#!/bin/bash
# Complete Pipeline Execution Script
# Run entire soccer analytics pipeline from start to finish

echo "=========================================="
echo "SOCCER ANALYTICS PIPELINE"
echo "=========================================="
echo "Starting pipeline execution..."
echo ""

# Set error handling
set -e  # Exit on error

# Step 0: Download Datasets
echo "[1/7] Downloading datasets from external sources..."
python acquire_data.py
echo "✓ Dataset download complete"
echo ""

# Step 1: Data Acquisition Verification
echo "[2/7] Running data acquisition verification..."
python scripts/01_acquire.py
echo "✓ Data acquisition verification complete"
echo ""

# Step 2: Data Cleaning
echo "[3/7] Running data cleaning..."
python scripts/02_clean.py
echo "✓ Data cleaning complete"
echo ""

# Step 3: Data Integration
echo "[4/7] Running data integration..."
python scripts/03_integrate.py
echo "✓ Data integration complete"
echo ""

# Step 4: Quality Assessment
echo "[5/7] Running quality assessment..."
python scripts/04_quality.py
echo "✓ Quality assessment complete"
echo ""

# Step 5: Analysis & Modeling
echo "[6/7] Running analysis and modeling..."
python scripts/05_analyze.py
echo "✓ Analysis and modeling complete"
echo ""

# Step 6: Visualization
echo "[7/7] Generating visualizations..."
python scripts/06_visualize.py
echo "✓ Visualizations complete"
echo ""

echo "=========================================="
echo "PIPELINE COMPLETE!"
echo "=========================================="
echo "Results available in:"
echo "  - outputs/figures/     (visualizations)"
echo "  - outputs/results/     (model outputs)"
echo "  - outputs/reports/     (quality reports)"
echo "  - data/processed/      (processed data)"
echo ""
