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

# Step 1: Data Acquisition
echo "[1/6] Running data acquisition..."
python scripts/01_acquire.py
echo "✓ Data acquisition complete"
echo ""

# Step 2: Data Cleaning
echo "[2/6] Running data cleaning..."
python scripts/02_clean.py
echo "✓ Data cleaning complete"
echo ""

# Step 3: Data Integration
echo "[3/6] Running data integration..."
python scripts/03_integrate.py
echo "✓ Data integration complete"
echo ""

# Step 4: Quality Assessment
echo "[4/6] Running quality assessment..."
python scripts/04_quality.py
echo "✓ Quality assessment complete"
echo ""

# Step 5: Analysis & Modeling
echo "[5/6] Running analysis and modeling..."
python scripts/05_analyze.py
echo "✓ Analysis and modeling complete"
echo ""

# Step 6: Visualization
echo "[6/6] Generating visualizations..."
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
