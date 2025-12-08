"""
Pipeline Validation Script
===========================
Quick validation that all pipeline outputs exist and are valid.

Usage: python workflows/validate_pipeline.py
"""

import os
from pathlib import Path
import pandas as pd

def validate_files():
    """Check that all expected outputs exist."""
    print("=" * 60)
    print("PIPELINE VALIDATION")
    print("=" * 60)

    errors = []
    warnings = []

    # Expected reports
    print("\n[1/6] Checking reports...")
    reports = [
        'outputs/reports/acquisition_report.md',
        'outputs/reports/cleaning_report.md',
        'outputs/reports/integration_report.md',
        'outputs/reports/data_quality_report.md',
        'outputs/reports/analysis_report.md',
        'outputs/reports/visualization_report.md',
    ]

    for report in reports:
        if not Path(report).exists():
            errors.append(f"Missing: {report}")
        else:
            print(f"  [OK] {report}")

    # Expected visualizations
    print("\n[2/6] Checking visualizations...")
    viz_dirs = {
        'outputs/figures/quality': 3,
        'outputs/figures/analysis': 3,
        'outputs/figures/comprehensive': 7,
    }

    for viz_dir, expected_count in viz_dirs.items():
        if not Path(viz_dir).exists():
            errors.append(f"Missing directory: {viz_dir}")
        else:
            png_files = list(Path(viz_dir).glob('*.png'))
            actual_count = len(png_files)
            if actual_count != expected_count:
                warnings.append(f"{viz_dir}: Expected {expected_count} files, found {actual_count}")
            else:
                print(f"  [OK] {viz_dir}: {actual_count} files")

    # Expected models
    print("\n[3/6] Checking models...")
    models = [
        'outputs/models/logistic_regression.pkl',
        'outputs/models/random_forest.pkl',
        'outputs/models/gradient_boosting.pkl',
        'outputs/models/scaler.pkl',
    ]

    for model in models:
        if not Path(model).exists():
            errors.append(f"Missing: {model}")
        else:
            size_mb = Path(model).stat().st_size / 1024 / 1024
            print(f"  [OK] {model} ({size_mb:.2f} MB)")

    # Check processed data
    print("\n[4/6] Checking processed data...")
    dataset_path = 'data/processed/integrated_dataset.csv'

    if not Path(dataset_path).exists():
        errors.append(f"Missing: {dataset_path}")
    else:
        try:
            df = pd.read_csv(dataset_path)
            expected_matches = 57865
            expected_columns = 38

            if len(df) != expected_matches:
                warnings.append(f"Dataset has {len(df):,} matches, expected {expected_matches:,}")
            else:
                print(f"  [OK] {dataset_path}")
                print(f"       Matches: {len(df):,}")
                print(f"       Columns: {len(df.columns)}")

            if len(df.columns) != expected_columns:
                warnings.append(f"Dataset has {len(df.columns)} columns, expected {expected_columns}")

        except Exception as e:
            errors.append(f"Error reading {dataset_path}: {e}")

    # Check metadata
    print("\n[5/6] Checking metadata...")
    metadata_files = [
        'data/metadata/checksums.txt',
        'data/metadata/team_name_mappings.csv',
        'data/metadata/acquisition_metadata.json',
    ]

    for metadata in metadata_files:
        if not Path(metadata).exists():
            errors.append(f"Missing: {metadata}")
        else:
            print(f"  [OK] {metadata}")

    # Summary
    print("\n[6/6] Validation Summary...")
    print("=" * 60)

    if not errors and not warnings:
        print("[SUCCESS] All pipeline outputs validated!")
        print("\nPipeline is complete and ready for:")
        print("  - Submission")
        print("  - Peer review")
        print("  - Reproduction by others")
        return True
    else:
        if errors:
            print(f"\n[ERROR] Found {len(errors)} critical issues:")
            for error in errors:
                print(f"  - {error}")

        if warnings:
            print(f"\n[WARNING] Found {len(warnings)} warnings:")
            for warning in warnings:
                print(f"  - {warning}")

        return False


if __name__ == "__main__":
    success = validate_files()
    exit(0 if success else 1)
