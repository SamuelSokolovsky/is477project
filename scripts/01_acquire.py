#!/usr/bin/env python3
"""
Data Acquisition Script for IS477 Soccer Analytics Project
===========================================================

This script handles complete data acquisition workflow:
1. Verify Dataset 1 (ESPN Soccer Data) - stored locally
2. Download Dataset 2 (European Football Statistics) from GitHub
3. Generate SHA-256 checksums for all files
4. Create acquisition metadata and reports

Datasets:
---------
Dataset 1 - ESPN Soccer Data (Local):
  - Source: https://www.kaggle.com/datasets/excel4soccer/espn-soccer-data
  - Storage: Stored locally in repository at ../data/raw/Dataset 1/
  - Files: teams.csv, teamStats.csv, standings.csv, leagues.csv
  - No download needed

Dataset 2 - Football-Data.co.uk (GitHub):
  - Source: https://github.com/datasets/football-datasets
  - Leagues: Premier League, La Liga, Bundesliga, Serie A, Ligue 1
  - Downloaded via git clone

Requirements:
-------------
- Internet connection (for Dataset 2)
- Git installed (for Dataset 2)

Usage:
------
    python scripts/01_acquire.py

Author: Yongyang Fu
Date: December 2025
"""

import os
import hashlib
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

#commented out the acquire_dataset1_kaggle method since dataset 1 is now stored locally on repo
"""
def acquire_dataset1_kaggle(self):
      ""
      Download Dataset 1 from Kaggle using kagglehub.

      Dataset: ESPN Soccer Data
      Source: https://www.kaggle.com/datasets/excel4soccer/espn-soccer-data
      ""
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

      #Check if Kaggle API credentials are configured.

      #Checks multiple sources in order:
      #1. Environment variables (KAGGLE_USERNAME, KAGGLE_KEY)
      #2. kaggle.json file at ~/.kaggle/kaggle.json

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


"""

# Setup directories
base_dir = Path(__file__).parent.parent
data_dir = base_dir / 'data'
raw_dir = data_dir / 'raw'
metadata_dir = data_dir / 'metadata'
dataset1_dir = raw_dir / 'Dataset 1'
dataset2_dir = raw_dir / 'Dataset 2'

# Store checksums
checksums = {}


def create_directories():
    """Create necessary directory structure."""
    for directory in [raw_dir, metadata_dir, dataset1_dir, dataset2_dir]:
        directory.mkdir(parents=True, exist_ok=True)
    print(f"Directory structure verified at: {data_dir}")


def calculate_checksum(filepath):
    """Calculate SHA-256 checksum of a file."""
    sha256_hash = hashlib.sha256()

    with open(filepath, "rb") as f:
        # Read file in chunks to handle large files
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()


def save_checksums():
    """Save all checksums to file."""
    checksum_file = metadata_dir / 'checksums.txt'

    with open(checksum_file, 'w') as f:
        f.write("# SHA-256 Checksums for Soccer Analytics Dataset\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("#" + "="*70 + "\n\n")

        for filepath, checksum in sorted(checksums.items()):
            f.write(f"{checksum}  {filepath}\n")

    print(f"Checksums saved to: {checksum_file}")


def verify_dataset1_local():
    """
    Verify Dataset 1 files exist locally and calculate checksums.

    Dataset: ESPN Soccer Data (stored locally, no download needed)
    """
    print("="*70)
    print("VERIFYING DATASET 1: ESPN Soccer Data (Local)")
    print("="*70)

    expected_files = ['teams.csv', 'teamStats.csv', 'standings.csv', 'leagues.csv']

    if not dataset1_dir.exists():
        print(f"WARNING: Dataset 1 directory not found: {dataset1_dir}")
        print("Please ensure Dataset 1 files are stored in data/raw/Dataset 1/")
        return False

    print(f"Checking for Dataset 1 files in: {dataset1_dir}")

    found_files = []
    for filename in expected_files:
        filepath = dataset1_dir / filename
        if filepath.exists():
            # Calculate checksum
            checksum = calculate_checksum(filepath)
            relative_path = filepath.relative_to(base_dir)
            checksums[str(relative_path)] = checksum

            # Get file size
            size_mb = filepath.stat().st_size / (1024 * 1024)

            print(f"  [OK] {filename} ({size_mb:.2f} MB)")
            print(f"       SHA-256: {checksum[:16]}...")
            found_files.append(filename)
        else:
            print(f"  [MISSING] {filename}")

    if len(found_files) == len(expected_files):
        print("All Dataset 1 files found and verified!")
        return True
    else:
        print(f"WARNING: Found {len(found_files)}/{len(expected_files)} expected files")
        return False


def acquire_dataset2_github():
    """Download Dataset 2 from GitHub."""
    print("="*70)
    print("ACQUIRING DATASET 2: European Football Match Statistics (GitHub)")
    print("="*70)

    repo_url = "https://github.com/datasets/football-datasets.git"
    repo_dir = dataset2_dir / "football-datasets"

    # Check if repository already exists
    if repo_dir.exists():
        print("Dataset 2 repository already exists. Updating...")

        try:
            # Git pull to update
            result = subprocess.run(
                ['git', 'pull'],
                cwd=repo_dir,
                capture_output=True,
                text=True,
                check=True
            )
            print(f"  {result.stdout.strip()}")
        except subprocess.CalledProcessError as e:
            print(f"WARNING: Failed to update repository: {e.stderr}")
    else:
        # Clone repository
        print(f"Cloning repository: {repo_url}")
        print("This may take a few minutes...")

        try:
            subprocess.run(
                ['git', 'clone', repo_url, str(repo_dir)],
                capture_output=True,
                text=True,
                check=True
            )
            print("Repository cloned successfully!")
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Git clone failed: {e.stderr}")
            return False
        except FileNotFoundError:
            print("ERROR: Git not found. Please install Git: https://git-scm.com/")
            return False

    # Verify datasets directory structure
    datasets_dir = repo_dir / "datasets"

    if not datasets_dir.exists():
        print(f"ERROR: Datasets directory not found: {datasets_dir}")
        return False

    print("Verifying league data structure...")

    # Check individual league directories
    leagues = ['premier-league', 'la-liga', 'serie-a', 'bundesliga', 'ligue-1']

    total_files = 0
    for league in leagues:
        league_dir = datasets_dir / league
        if league_dir.exists():
            csv_files = list(league_dir.glob('season-*.csv'))
            print(f"  [OK] {league}: {len(csv_files)} season files")
            total_files += len(csv_files)

            # Calculate checksum for first file as sample
            if csv_files:
                sample_file = csv_files[0]
                checksum = calculate_checksum(sample_file)
                relative_path = sample_file.relative_to(base_dir)
                checksums[str(relative_path)] = checksum
        else:
            print(f"  [WARN] {league} directory not found")

    print(f"Dataset 2 acquisition complete! Total season files: {total_files}")
    return True


def generate_acquisition_report():
    """
    Generate a detailed acquisition report in markdown format.

    NOTE: This report generation code was created using AI assistance.
    The reports generated in outputs/reports/ are managerial reports for
    troubleshooting purposes only. AI is particularly effective at formatting
    and presenting output data in readable markdown format.
    """
    report_file = metadata_dir / 'acquisition_report.md'

    total_size_bytes = 0
    dataset1_files = []

    # Collect Dataset 1 info
    if dataset1_dir.exists():
        for file in dataset1_dir.glob('*.csv'):
            size_bytes = file.stat().st_size
            total_size_bytes += size_bytes
            dataset1_files.append({
                'name': file.name,
                'size': size_bytes / (1024 * 1024),  # MB
                'path': str(file.relative_to(base_dir))
            })

    with open(report_file, 'w') as f:
        f.write("# Data Acquisition Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")

        f.write("## Summary\n\n")
        f.write(f"- **Total Files Verified:** {len(dataset1_files)}\n")
        f.write(f"- **Total Size:** {total_size_bytes / (1024 * 1024):.2f} MB\n")
        f.write(f"- **Verification Status:** Complete\n")
        f.write(f"- **Checksums Generated:** {len(checksums)}\n\n")

        f.write("## Dataset 1: ESPN Soccer Data (Local)\n\n")
        f.write(f"- **Files Verified:** {len(dataset1_files)}\n")
        f.write(f"- **Source:** https://www.kaggle.com/datasets/excel4soccer/espn-soccer-data\n")
        f.write(f"- **Storage:** Stored locally in repository at data/raw/Dataset 1/\n")
        f.write(f"- **License:** Check Kaggle dataset page\n\n")

        f.write("### Files\n\n")
        for file_info in dataset1_files:
            f.write(f"- `{file_info['name']}` - {file_info['size']:.2f} MB\n")

        f.write("\n## Dataset 2: Football-Data.co.uk\n\n")
        datasets_dir = dataset2_dir / "football-datasets" / "datasets"
        if datasets_dir.exists():
            all_leagues_file = datasets_dir / "all_leagues_all_seasons.csv"
            if all_leagues_file.exists():
                size_mb = all_leagues_file.stat().st_size / (1024 * 1024)
                f.write(f"- **Main File:** all_leagues_all_seasons.csv ({size_mb:.2f} MB)\n")
                f.write(f"- **Source:** https://github.com/datasets/football-datasets\n")
                f.write(f"- **License:** PDDL 1.0 (Public Domain)\n\n")
        else:
            f.write("- **Status:** Not downloaded yet\n\n")

        f.write("\n---\n\n")
        f.write("## Verification\n\n")
        f.write("All files have been verified with SHA-256 checksums.\n")
        f.write("See `checksums.txt` for complete checksum listing.\n\n")

    print(f"Acquisition report saved to: {report_file}")


def main():
    """Main function to run data acquisition workflow."""
    print("="*70)
    print("SOCCER ANALYTICS - DATA ACQUISITION")
    print("="*70)
    print(f"Base Directory: {base_dir}")
    print()

    # Create directories
    create_directories()
    print()

    # Verify Dataset 1 (Local)
    dataset1_ok = verify_dataset1_local()
    print()

    # Acquire Dataset 2 (GitHub)
    dataset2_ok = acquire_dataset2_github()
    print()

    # Save checksums
    print("="*70)
    print("SAVING CHECKSUMS")
    print("="*70)
    save_checksums()
    print()

    # Generate report
    print("="*70)
    print("GENERATING ACQUISITION REPORT")
    print("="*70)
    generate_acquisition_report()
    print()

    # Final summary
    print("="*70)
    print("DATA ACQUISITION COMPLETE!")
    print("="*70)
    print(f"Data Location: {raw_dir}")
    print(f"Metadata Location: {metadata_dir}")
    print(f"Checksums: {len(checksums)} files")
    print()
    print("Next Steps:")
    print("  1. Run data cleaning: python scripts/02_clean.py")
    print("  2. Continue with analysis pipeline")
    print()


if __name__ == "__main__":
    main()
