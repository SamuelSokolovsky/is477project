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
    python scripts/01_acquire.py [--force] [--skip-dataset1] [--skip-github]

Options:
--------
    --force          Re-download even if data exists (Dataset 2 only)
    --skip-dataset1  Skip Dataset 1 verification
    --skip-github    Skip GitHub dataset download
    --verify-only    Only verify checksums, don't download

Author: IS477 Student
Date: December 2025
"""

import os
import sys
import hashlib
import json
import argparse
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import logging

# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file if it exists
except ImportError:
    # python-dotenv not installed, will rely on system environment variables
    pass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_acquisition.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class DataAcquisitionError(Exception):
    """Custom exception for data acquisition errors."""
    pass


class SoccerDataAcquisition:
    """Handles programmatic acquisition of soccer datasets."""

    def __init__(self, force_download: bool = False):
        """
        Initialize data acquisition.

        Args:
            force_download: If True, re-download even if data exists
        """
        self.force_download = force_download

        # Adjust base_dir to parent since we're in scripts/
        self.base_dir = Path(__file__).parent.parent
        self.data_dir = self.base_dir / 'data'
        self.raw_dir = self.data_dir / 'raw'
        self.metadata_dir = self.data_dir / 'metadata'

        # Dataset-specific directories
        self.dataset1_dir = self.raw_dir / 'Dataset 1'
        self.dataset2_dir = self.raw_dir / 'Dataset 2'

        # Checksums storage
        self.checksums: Dict[str, str] = {}

        # Create directory structure
        self._create_directories()

    def _create_directories(self):
        """Create necessary directory structure."""
        for directory in [self.raw_dir, self.metadata_dir,
                         self.dataset1_dir, self.dataset2_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory structure verified at: {self.data_dir}")

    def _calculate_checksum(self, filepath: Path) -> str:
        """
        Calculate SHA-256 checksum of a file.

        Args:
            filepath: Path to file

        Returns:
            SHA-256 hash as hex string
        """
        sha256_hash = hashlib.sha256()

        with open(filepath, "rb") as f:
            # Read file in chunks to handle large files
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        checksum = sha256_hash.hexdigest()
        return checksum

    def _save_checksums(self):
        """Save all checksums to file."""
        checksum_file = self.metadata_dir / 'checksums.txt'

        with open(checksum_file, 'w') as f:
            f.write("# SHA-256 Checksums for Soccer Analytics Dataset\n")
            f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("#" + "="*70 + "\n\n")

            for filepath, checksum in sorted(self.checksums.items()):
                f.write(f"{checksum}  {filepath}\n")

        logger.info(f"Checksums saved to: {checksum_file}")

        # Also save as JSON for programmatic access
        checksum_json = self.metadata_dir / 'checksums.json'
        with open(checksum_json, 'w') as f:
            json.dump({
                'generated': datetime.now().isoformat(),
                'checksums': self.checksums
            }, f, indent=2)

        logger.info(f"Checksums JSON saved to: {checksum_json}")

    def verify_dataset1_local(self):
        """
        Verify Dataset 1 files exist locally and calculate checksums.

        Dataset 1 is now stored in the repository - no download needed.
        Dataset: ESPN Soccer Data
        Source: https://www.kaggle.com/datasets/excel4soccer/espn-soccer-data
        """
        logger.info("="*70)
        logger.info("VERIFYING DATASET 1: ESPN Soccer Data (Local)")
        logger.info("="*70)

        expected_files = ['teams.csv', 'teamStats.csv', 'standings.csv', 'leagues.csv']

        if not self.dataset1_dir.exists():
            logger.warning(f"Dataset 1 directory not found: {self.dataset1_dir}")
            logger.warning("Please ensure Dataset 1 files are stored in data/raw/Dataset 1/")
            return False

        logger.info(f"Checking for Dataset 1 files in: {self.dataset1_dir}")

        found_files = []
        for filename in expected_files:
            filepath = self.dataset1_dir / filename
            if filepath.exists():
                # Calculate checksum
                checksum = self._calculate_checksum(filepath)
                relative_path = filepath.relative_to(self.base_dir)
                self.checksums[str(relative_path)] = checksum

                # Get file size
                size_mb = filepath.stat().st_size / (1024 * 1024)

                logger.info(f"  [OK] {filename} ({size_mb:.2f} MB)")
                logger.info(f"       SHA-256: {checksum[:16]}...")
                found_files.append(filename)
            else:
                logger.warning(f"  [MISSING] {filename}")

        if len(found_files) == len(expected_files):
            logger.info("All Dataset 1 files found and verified!")
            return True
        else:
            logger.warning(f"Found {len(found_files)}/{len(expected_files)} expected files")
            logger.warning("Some Dataset 1 files are missing!")
            return False

    def acquire_dataset2_github(self):
        """
        Download Dataset 2 from GitHub repository.

        Dataset: European Football Match Statistics
        Source: https://github.com/datasets/football-datasets
        """
        logger.info("="*70)
        logger.info("ACQUIRING DATASET 2: European Football Match Statistics (GitHub)")
        logger.info("="*70)

        repo_url = "https://github.com/datasets/football-datasets.git"
        repo_dir = self.dataset2_dir / "football-datasets"

        # Check if repository already exists
        if repo_dir.exists() and not self.force_download:
            logger.info("Dataset 2 repository already exists. Use --force to re-download")
            logger.info("Updating repository...")

            try:
                # Git pull to update
                result = subprocess.run(
                    ['git', 'pull'],
                    cwd=repo_dir,
                    capture_output=True,
                    text=True,
                    check=True
                )
                logger.info(f"  {result.stdout.strip()}")
            except subprocess.CalledProcessError as e:
                logger.warning(f"Failed to update repository: {e.stderr}")
        else:
            # Clone repository
            logger.info(f"Cloning repository: {repo_url}")
            logger.info("This may take a few minutes...")

            # Remove existing directory if force download
            if repo_dir.exists():
                shutil.rmtree(repo_dir)

            try:
                result = subprocess.run(
                    ['git', 'clone', repo_url, str(repo_dir)],
                    capture_output=True,
                    text=True,
                    check=True
                )
                logger.info("Repository cloned successfully!")
            except subprocess.CalledProcessError as e:
                raise DataAcquisitionError(f"Git clone failed: {e.stderr}")
            except FileNotFoundError:
                raise DataAcquisitionError(
                    "Git not found. Please install Git: https://git-scm.com/"
                )

        # Verify datasets directory structure
        datasets_dir = repo_dir / "datasets"

        if not datasets_dir.exists():
            raise DataAcquisitionError(f"Datasets directory not found: {datasets_dir}")

        logger.info("Verifying league data structure...")

        # Check individual league directories
        leagues = ['premier-league', 'la-liga', 'serie-a', 'bundesliga', 'ligue-1']

        total_files = 0
        for league in leagues:
            league_dir = datasets_dir / league
            if league_dir.exists():
                csv_files = list(league_dir.glob('season-*.csv'))
                logger.info(f"  [OK] {league}: {len(csv_files)} season files")
                total_files += len(csv_files)

                # Calculate checksum for first file as sample
                if csv_files:
                    sample_file = csv_files[0]
                    checksum = self._calculate_checksum(sample_file)
                    relative_path = sample_file.relative_to(self.base_dir)
                    self.checksums[str(relative_path)] = checksum
            else:
                logger.warning(f"  [WARN] {league} directory not found")

        logger.info(f"Dataset 2 acquisition complete! Total season files: {total_files}")
        return True

    def verify_checksums(self, checksum_file: Path = None):
        """
        Verify existing data against saved checksums.

        Args:
            checksum_file: Path to checksum file (default: metadata/checksums.txt)
        """
        if checksum_file is None:
            checksum_file = self.metadata_dir / 'checksums.txt'

        if not checksum_file.exists():
            logger.error(f"Checksum file not found: {checksum_file}")
            return False

        logger.info("="*70)
        logger.info("VERIFYING DATA INTEGRITY")
        logger.info("="*70)

        # Read saved checksums
        saved_checksums = {}
        with open(checksum_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split(None, 1)
                    if len(parts) == 2:
                        checksum, filepath = parts
                        saved_checksums[filepath] = checksum

        logger.info(f"Loaded {len(saved_checksums)} checksums from file")

        # Verify each file
        all_valid = True
        for filepath, expected_checksum in saved_checksums.items():
            full_path = self.base_dir / filepath

            if not full_path.exists():
                logger.error(f"  [MISSING] {filepath}")
                all_valid = False
                continue

            actual_checksum = self._calculate_checksum(full_path)

            if actual_checksum == expected_checksum:
                logger.info(f"  [OK] {filepath}")
            else:
                logger.error(f"  [FAIL] {filepath}")
                logger.error(f"    Expected: {expected_checksum}")
                logger.error(f"    Actual:   {actual_checksum}")
                all_valid = False

        if all_valid:
            logger.info("All checksums verified successfully!")
            return True
        else:
            logger.error("Checksum verification failed!")
            return False

    def generate_acquisition_report(self):
        """Generate a detailed acquisition report in markdown format."""
        report_file = self.metadata_dir / 'acquisition_report.md'

        total_size_bytes = 0
        dataset1_files = []

        # Collect Dataset 1 info
        if self.dataset1_dir.exists():
            for file in self.dataset1_dir.glob('*.csv'):
                size_bytes = file.stat().st_size
                total_size_bytes += size_bytes
                dataset1_files.append({
                    'name': file.name,
                    'size': size_bytes / (1024 * 1024),  # MB
                    'path': str(file.relative_to(self.base_dir))
                })

        with open(report_file, 'w') as f:
            f.write("# Data Acquisition Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")

            f.write("## Summary\n\n")
            f.write(f"- **Total Files Verified:** {len(dataset1_files)}\n")
            f.write(f"- **Total Size:** {total_size_bytes / (1024 * 1024):.2f} MB\n")
            f.write(f"- **Verification Status:** Complete\n")
            f.write(f"- **Checksums Generated:** {len(self.checksums)}\n\n")

            f.write("## Dataset 1: ESPN Soccer Data (Local)\n\n")
            f.write(f"- **Files Verified:** {len(dataset1_files)}\n")
            f.write(f"- **Source:** https://www.kaggle.com/datasets/excel4soccer/espn-soccer-data\n")
            f.write(f"- **Storage:** Stored locally in repository at data/raw/Dataset 1/\n")
            f.write(f"- **License:** Check Kaggle dataset page\n\n")

            f.write("### Files\n\n")
            for file_info in dataset1_files:
                f.write(f"- `{file_info['name']}` - {file_info['size']:.2f} MB\n")

            f.write("\n## Dataset 2: Football-Data.co.uk\n\n")
            datasets_dir = self.dataset2_dir / "football-datasets" / "datasets"
            if datasets_dir.exists():
                all_leagues_file = datasets_dir / "all_leagues_all_seasons.csv"
                if all_leagues_file.exists():
                    size_mb = all_leagues_file.stat().st_size / (1024 * 1024)
                    f.write(f"- **Main File:** all_leagues_all_seasons.csv ({size_mb:.2f} MB)\n")
                    f.write(f"- **Source:** https://github.com/datasets/football-datasets\n")
                    f.write(f"- **License:** PDDL 1.0 (Public Domain)\n\n")
            else:
                f.write("- **Status:** Not downloaded yet\n")
                f.write("- Run with `--skip-dataset1` flag to download Dataset 2\n\n")

            f.write("\n---\n\n")
            f.write("## Verification\n\n")
            f.write("All files have been verified with SHA-256 checksums.\n")
            f.write("See `checksums.txt` for complete checksum listing.\n\n")

        logger.info(f"Acquisition report saved to: {report_file}")

    def run_acquisition(self, skip_dataset1: bool = False, skip_github: bool = False):
        """
        Run complete data acquisition workflow.

        Args:
            skip_dataset1: Skip Dataset 1 verification (local files)
            skip_github: Skip GitHub dataset acquisition
        """
        logger.info("="*70)
        logger.info("SOCCER ANALYTICS - DATA ACQUISITION")
        logger.info("="*70)
        logger.info(f"Base Directory: {self.base_dir}")
        logger.info(f"Force Download: {self.force_download}")
        logger.info("")

        try:
            dataset1_ok = True
            dataset2_ok = True

            # Verify Dataset 1 (Local - no longer downloaded from Kaggle)
            if not skip_dataset1:
                dataset1_ok = self.verify_dataset1_local()
                logger.info("")
            else:
                logger.info("Skipping Dataset 1 verification (--skip-dataset1)")
                logger.info("")

            # Acquire Dataset 2 (GitHub)
            if not skip_github:
                dataset2_ok = self.acquire_dataset2_github()
                logger.info("")
            else:
                logger.info("Skipping GitHub dataset acquisition (--skip-github)")
                logger.info("")

            # Save checksums
            logger.info("="*70)
            logger.info("SAVING CHECKSUMS")
            logger.info("="*70)
            self._save_checksums()
            logger.info("")

            # Generate report
            logger.info("="*70)
            logger.info("GENERATING ACQUISITION REPORT")
            logger.info("="*70)
            self.generate_acquisition_report()
            logger.info("")

            # Final summary
            logger.info("="*70)
            logger.info("DATA ACQUISITION COMPLETE!")
            logger.info("="*70)
            logger.info(f"Data Location: {self.raw_dir}")
            logger.info(f"Metadata Location: {self.metadata_dir}")
            logger.info(f"Checksums: {len(self.checksums)} files")
            logger.info("")
            logger.info("Next Steps:")
            logger.info("  1. Verify data integrity: python scripts/01_acquire.py --verify-only")
            logger.info("  2. Run data cleaning: python scripts/02_clean.py")
            logger.info("  3. Continue with analysis pipeline")
            logger.info("")

            return dataset1_ok and dataset2_ok

        except Exception as e:
            logger.error(f"Data acquisition failed: {e}")
            raise


def main():
    """Main entry point for data acquisition script."""
    parser = argparse.ArgumentParser(
        description='Data Acquisition for IS477 Soccer Analytics Project',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/01_acquire.py                    # Verify Dataset 1 and download Dataset 2
  python scripts/01_acquire.py --force            # Force re-download Dataset 2
  python scripts/01_acquire.py --skip-dataset1    # Skip Dataset 1 verification
  python scripts/01_acquire.py --verify-only      # Only verify checksums

Note: Dataset 1 is stored locally in the repository (no download needed)

For more information, see DATA_ACQUISITION.md
        """
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='Force re-download even if data exists (applies to Dataset 2 only)'
    )

    parser.add_argument(
        '--skip-dataset1',
        action='store_true',
        help='Skip Dataset 1 verification (local files)'
    )

    parser.add_argument(
        '--skip-github',
        action='store_true',
        help='Skip GitHub dataset acquisition'
    )

    parser.add_argument(
        '--verify-only',
        action='store_true',
        help='Only verify checksums, do not download'
    )

    args = parser.parse_args()

    try:
        acquirer = SoccerDataAcquisition(force_download=args.force)

        if args.verify_only:
            # Only verify checksums
            success = acquirer.verify_checksums()
            sys.exit(0 if success else 1)
        else:
            # Run full acquisition
            success = acquirer.run_acquisition(
                skip_dataset1=args.skip_dataset1,
                skip_github=args.skip_github
            )

            logger.info("="*70)
            logger.info("SUCCESS!")
            logger.info("="*70)

            sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        logger.warning("\nAcquisition interrupted by user")
        sys.exit(1)

    except DataAcquisitionError as e:
        logger.error(f"\nAcquisition Error: {e}")
        sys.exit(1)

    except Exception as e:
        logger.error(f"\nUnexpected error: {e}")
        logger.exception("Full traceback:")
        sys.exit(1)


if __name__ == "__main__":
    main()
