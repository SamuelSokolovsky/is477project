#!/usr/bin/env python3
"""
Programmatic Data Acquisition Script for IS477 Soccer Analytics Project
========================================================================

This script automates the download and verification of all datasets required
for the project, ensuring reproducibility and data integrity.

Datasets:
1. ESPN Soccer Data (Kaggle) - Match fixtures and team statistics
2. European Football Match Statistics (GitHub) - Historical match data

Requirements:
- Kaggle API credentials configured (~/.kaggle/kaggle.json)
- Internet connection
- Git installed (for Dataset 2)

Usage:
    python acquire_data.py [--force] [--skip-kaggle] [--skip-github]

Options:
    --force         Re-download even if data exists
    --skip-kaggle   Skip Kaggle dataset download
    --skip-github   Skip GitHub dataset download
    --verify-only   Only verify checksums, don't download

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
        self.base_dir = Path.cwd()
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
        logger.info(f"Directory structure created at: {self.data_dir}")

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

    def _check_kaggle_credentials(self) -> bool:
        """
        Check if Kaggle API credentials are configured.

        Returns:
            True if credentials exist, False otherwise
        """
        kaggle_json = Path.home() / '.kaggle' / 'kaggle.json'

        if not kaggle_json.exists():
            logger.error("Kaggle API credentials not found!")
            logger.error(f"Expected location: {kaggle_json}")
            logger.error("Please follow these steps:")
            logger.error("1. Go to https://www.kaggle.com/settings")
            logger.error("2. Click 'Create New API Token'")
            logger.error("3. Place kaggle.json in ~/.kaggle/ directory")
            logger.error("4. Run: chmod 600 ~/.kaggle/kaggle.json (on Unix)")
            return False

        logger.info("Kaggle API credentials found")
        return True

    def acquire_dataset1_kaggle(self):
        """
        Download Dataset 1 from Kaggle using kagglehub.

        Dataset: ESPN Soccer Data
        Source: https://www.kaggle.com/datasets/excel4soccer/espn-soccer-data
        """
        logger.info("="*70)
        logger.info("ACQUIRING DATASET 1: ESPN Soccer Data (Kaggle)")
        logger.info("="*70)

        # Check credentials
        if not self._check_kaggle_credentials():
            raise DataAcquisitionError("Kaggle credentials not configured")

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

        # Download using kagglehub
        try:
            import kagglehub

            logger.info("Downloading from Kaggle (this may take a few minutes)...")
            logger.info("Dataset: excel4soccer/espn-soccer-data")

            # Download dataset
            download_path = kagglehub.dataset_download("excel4soccer/espn-soccer-data")

            logger.info(f"Dataset downloaded to: {download_path}")

            # Copy files to our directory structure
            source_dir = Path(download_path)

            for filename in expected_files:
                source_file = source_dir / filename
                dest_file = self.dataset1_dir / filename

                if source_file.exists():
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
                    logger.warning(f"  [WARN] {filename} not found in download")

            logger.info("Dataset 1 acquisition complete!")

        except ImportError:
            raise DataAcquisitionError(
                "kagglehub not installed. Run: pip install kagglehub"
            )
        except Exception as e:
            raise DataAcquisitionError(f"Failed to download Kaggle dataset: {e}")

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

        # Calculate checksums for key files
        datasets_dir = repo_dir / "datasets"

        if not datasets_dir.exists():
            raise DataAcquisitionError(f"Datasets directory not found: {datasets_dir}")

        logger.info("Calculating checksums for league data files...")

        # Key file to process: all_leagues_all_seasons.csv
        all_leagues_file = datasets_dir / "all_leagues_all_seasons.csv"

        if all_leagues_file.exists():
            checksum = self._calculate_checksum(all_leagues_file)
            relative_path = all_leagues_file.relative_to(self.base_dir)
            self.checksums[str(relative_path)] = checksum

            size_mb = all_leagues_file.stat().st_size / (1024 * 1024)
            logger.info(f"  [OK] all_leagues_all_seasons.csv ({size_mb:.2f} MB)")
            logger.info(f"       SHA-256: {checksum[:16]}...")
        else:
            logger.warning("  [WARN] all_leagues_all_seasons.csv not found")

        # Also checksum individual league directories
        leagues = [
            'english-premier-league',
            'spanish-la-liga',
            'italian-serie-a',
            'german-bundesliga',
            'french-ligue-1'
        ]

        for league in leagues:
            league_dir = datasets_dir / league
            if league_dir.exists():
                csv_files = list(league_dir.glob('*.csv'))
                logger.info(f"  Found {len(csv_files)} files in {league}")
            else:
                logger.warning(f"  [WARN] {league} directory not found")

        logger.info("Dataset 2 acquisition complete!")

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
        """Generate a detailed acquisition report."""
        report_file = self.metadata_dir / 'acquisition_report.txt'

        with open(report_file, 'w') as f:
            f.write("="*70 + "\n")
            f.write("DATA ACQUISITION REPORT\n")
            f.write("="*70 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # Dataset 1 info
            f.write("DATASET 1: ESPN Soccer Data (Kaggle)\n")
            f.write("-" * 70 + "\n")
            f.write("Source: https://www.kaggle.com/datasets/excel4soccer/espn-soccer-data\n")
            f.write(f"Location: {self.dataset1_dir}\n")

            if self.dataset1_dir.exists():
                files = list(self.dataset1_dir.glob('*.csv'))
                f.write(f"Files: {len(files)}\n")
                total_size = sum(f.stat().st_size for f in files)
                f.write(f"Total Size: {total_size / (1024*1024):.2f} MB\n")

                for file in sorted(files):
                    size_mb = file.stat().st_size / (1024 * 1024)
                    f.write(f"  - {file.name} ({size_mb:.2f} MB)\n")

            f.write("\n")

            # Dataset 2 info
            f.write("DATASET 2: European Football Match Statistics (GitHub)\n")
            f.write("-" * 70 + "\n")
            f.write("Source: https://github.com/datasets/football-datasets\n")
            f.write(f"Location: {self.dataset2_dir}\n")

            datasets_dir = self.dataset2_dir / "football-datasets" / "datasets"
            if datasets_dir.exists():
                all_leagues_file = datasets_dir / "all_leagues_all_seasons.csv"
                if all_leagues_file.exists():
                    size_mb = all_leagues_file.stat().st_size / (1024 * 1024)
                    f.write(f"Main File: all_leagues_all_seasons.csv ({size_mb:.2f} MB)\n")

                    # Count matches
                    try:
                        with open(all_leagues_file) as csv_file:
                            line_count = sum(1 for _ in csv_file) - 1  # Exclude header
                            f.write(f"Total Matches: {line_count:,}\n")
                    except:
                        pass

            f.write("\n")
            f.write("="*70 + "\n")
            f.write(f"Total Checksums Generated: {len(self.checksums)}\n")
            f.write(f"Checksum File: {self.metadata_dir / 'checksums.txt'}\n")
            f.write("="*70 + "\n")

        logger.info(f"Acquisition report saved to: {report_file}")

    def run_acquisition(self, skip_kaggle: bool = False, skip_github: bool = False):
        """
        Run complete data acquisition workflow.

        Args:
            skip_kaggle: Skip Kaggle dataset acquisition
            skip_github: Skip GitHub dataset acquisition
        """
        logger.info("="*70)
        logger.info("SOCCER ANALYTICS - DATA ACQUISITION")
        logger.info("="*70)
        logger.info(f"Base Directory: {self.base_dir}")
        logger.info(f"Force Download: {self.force_download}")
        logger.info("")

        try:
            # Acquire Dataset 1 (Kaggle)
            if not skip_kaggle:
                self.acquire_dataset1_kaggle()
                logger.info("")
            else:
                logger.info("Skipping Kaggle dataset acquisition (--skip-kaggle)")
                logger.info("")

            # Acquire Dataset 2 (GitHub)
            if not skip_github:
                self.acquire_dataset2_github()
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
            logger.info("  1. Verify data integrity: python acquire_data.py --verify-only")
            logger.info("  2. Run data cleaning: python scripts/02_clean.py")
            logger.info("  3. Continue with analysis pipeline")
            logger.info("")

        except Exception as e:
            logger.error(f"Data acquisition failed: {e}")
            raise


def main():
    """Main entry point for data acquisition script."""
    parser = argparse.ArgumentParser(
        description='Programmatic data acquisition for IS477 Soccer Analytics Project',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python acquire_data.py                    # Download all datasets
  python acquire_data.py --force            # Force re-download
  python acquire_data.py --skip-kaggle      # Skip Kaggle dataset
  python acquire_data.py --verify-only      # Only verify checksums

For more information, see DATA_ACQUISITION.md
        """
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='Force re-download even if data exists'
    )

    parser.add_argument(
        '--skip-kaggle',
        action='store_true',
        help='Skip Kaggle dataset acquisition'
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
            acquirer.run_acquisition(
                skip_kaggle=args.skip_kaggle,
                skip_github=args.skip_github
            )

            logger.info("="*70)
            logger.info("SUCCESS!")
            logger.info("="*70)

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
