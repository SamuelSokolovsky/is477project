"""
Test script to verify Kaggle dataset and kagglehub infrastructure
"""
import os
from dotenv import load_dotenv
load_dotenv()

print("=" * 70)
print("KAGGLE DATASET & INFRASTRUCTURE TEST")
print("=" * 70)
print()

# Check credentials
print("[1] Checking Kaggle Credentials...")
username = os.getenv('KAGGLE_USERNAME')
key = os.getenv('KAGGLE_KEY')
if username and key:
    print(f"  [OK] KAGGLE_USERNAME: {username}")
    print(f"  [OK] KAGGLE_KEY: {key[:15]}... (masked)")
else:
    print("  [ERROR] Credentials not found!")
print()

# Test kagglehub import
print("[2] Testing kagglehub import...")
try:
    import kagglehub
    from kagglehub import KaggleDatasetAdapter
    print(f"  [OK] kagglehub version: {kagglehub.__version__}")
    print(f"  [OK] KaggleDatasetAdapter imported")
except Exception as e:
    print(f"  [ERROR] Error: {e}")
    exit(1)
print()

# Try to list dataset files
print("[3] Attempting to download dataset metadata...")
dataset_name = "excel4soccer/espn-soccer-data"
try:
    # Use the new dataset_download method to get the path
    print(f"  Downloading: {dataset_name}")
    path = kagglehub.dataset_download(dataset_name)
    print(f"  [OK] Dataset downloaded to: {path}")

    # List files
    import os
    from pathlib import Path
    dataset_path = Path(path)

    print()
    print("[4] Listing available files in dataset...")
    all_files = list(dataset_path.rglob("*"))
    csv_files = [f for f in all_files if f.suffix == '.csv']
    zip_files = [f for f in all_files if f.suffix == '.zip']

    print(f"  Total files: {len(all_files)}")
    print(f"  CSV files: {len(csv_files)}")
    print(f"  ZIP files: {len(zip_files)}")
    print()

    if csv_files:
        print("  CSV Files found:")
        for f in csv_files:
            size_mb = f.stat().st_size / (1024 * 1024)
            print(f"    - {f.name} ({size_mb:.2f} MB)")

    if zip_files:
        print()
        print("  ZIP Files found:")
        for f in zip_files:
            size_mb = f.stat().st_size / (1024 * 1024)
            print(f"    - {f.name} ({size_mb:.2f} MB)")

    # Try loading with the new API
    print()
    print("[5] Testing data loading with kagglehub.load_dataset()...")

    # If we have CSV files, try loading the first one
    if csv_files:
        test_file = csv_files[0].name
        print(f"  Attempting to load: {test_file}")
        try:
            df = kagglehub.load_dataset(
                KaggleDatasetAdapter.PANDAS,
                dataset_name,
                test_file,
            )
            print(f"  [OK] Successfully loaded!")
            print(f"  Shape: {df.shape}")
            print(f"  Columns: {list(df.columns[:5])}...")
            print()
            print("  First 3 records:")
            print(df.head(3))
        except Exception as e:
            print(f"  [ERROR] Error loading file: {e}")

    print()
    print("=" * 70)
    print("[SUCCESS] DATASET INFRASTRUCTURE TEST COMPLETE")
    print("=" * 70)

except Exception as e:
    print(f"  [ERROR] Error: {e}")
    print()
    print("=" * 70)
    print("[FAILED] TEST FAILED")
    print("=" * 70)
    import traceback
    traceback.print_exc()
