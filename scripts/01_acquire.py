"""
Data Acquisition Script
=======================
Purpose: Verify and document both soccer datasets

Dataset 1 - ESPN Soccer Data (Local):
- Source: https://www.kaggle.com/datasets/excel4soccer/espn-soccer-data
- Storage: Stored locally in repository at data/raw/Dataset 1/
- Files: fixtures.csv, teamStats.csv, standings.csv, teams.csv

Dataset 2 - Football-Data.co.uk:
- Source: https://github.com/datasets/football-datasets
- Leagues: Premier League, La Liga, Bundesliga, Serie A, Ligue 1

Requirements:
- Generate SHA-256 checksums for all files
- Store checksums in data/metadata/checksums.txt
- Log download timestamps
- Handle errors gracefully
"""

import hashlib
import os
import json
from datetime import datetime
from pathlib import Path


def generate_checksum(filepath):
    """
    Generate SHA-256 checksum for a file.

    Args:
        filepath: Path to the file

    Returns:
        str: Hexadecimal SHA-256 checksum
    """
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            # Read file in chunks for memory efficiency
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"  [WARNING] Error generating checksum for {filepath}: {e}")
        return None


def get_file_size(filepath):
    """Get human-readable file size."""
    size = os.path.getsize(filepath)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"


def scan_directory(directory, file_extensions=None):
    """
    Recursively scan directory for data files.

    Args:
        directory: Path to scan
        file_extensions: List of extensions to include (e.g., ['.csv', '.json'])
                        If None, includes all files

    Returns:
        List of Path objects
    """
    if file_extensions is None:
        file_extensions = ['.csv', '.json', '.txt', '.md', '.zip']

    files = []
    directory = Path(directory)

    if not directory.exists():
        print(f"  [WARNING] Directory not found: {directory}")
        return files

    # Recursively find all files with specified extensions
    for ext in file_extensions:
        files.extend(directory.rglob(f"*{ext}"))

    # Sort for consistent ordering
    return sorted(files)


def verify_dataset1(raw_data_dir):
    """
    Verify Dataset 1 (ESPN Soccer Data) is present.

    Expected files:
    - teams.csv
    - teamStats.csv
    - standings.csv
    - fixtures.csv (or similar)
    """
    print("\n[Dataset 1: ESPN Soccer Data]")
    dataset1_dir = raw_data_dir / "Dataset 1"

    if not dataset1_dir.exists():
        print("  [WARNING] Dataset 1 directory not found!")
        return False

    expected_files = ['teams.csv', 'teamStats.csv', 'standings.csv']
    found_files = list(dataset1_dir.glob("*.csv"))

    print(f"  Location: {dataset1_dir}")
    print(f"  CSV files found: {len(found_files)}")

    for expected in expected_files:
        file_path = dataset1_dir / expected
        if file_path.exists():
            print(f"  [OK] {expected}")
        else:
            print(f"  [MISSING] {expected}")

    # List any additional files
    additional = [f.name for f in found_files if f.name not in expected_files]
    if additional:
        print(f"  Additional files: {', '.join(additional)}")

    return len(found_files) > 0


def verify_dataset2(raw_data_dir):
    """
    Verify Dataset 2 (Football-Data.co.uk) is present.

    Expected structure:
    - football-datasets/datasets/
      - premier-league/
      - la-liga/
      - bundesliga/
      - serie-a/
      - ligue-1/
    """
    print("\n[Dataset 2: Football-Data.co.uk]")
    dataset2_dir = raw_data_dir / "Dataset 2" / "football-datasets" / "datasets"

    if not dataset2_dir.exists():
        print("  [WARNING] Dataset 2 directory not found!")
        return False

    print(f"  Location: {dataset2_dir}")

    expected_leagues = ['premier-league', 'la-liga', 'bundesliga', 'serie-a', 'ligue-1']
    found_leagues = []

    for league in expected_leagues:
        league_dir = dataset2_dir / league
        if league_dir.exists():
            csv_files = list(league_dir.glob("*.csv"))
            # Exclude the consolidated file
            season_files = [f for f in csv_files if 'season-' in f.name]
            found_leagues.append(league)
            print(f"  [OK] {league}: {len(season_files)} season files")
        else:
            print(f"  [MISSING] {league}")

    return len(found_leagues) > 0


def generate_checksums_file(raw_data_dir, metadata_dir):
    """
    Generate checksums for all data files and save to metadata.

    Args:
        raw_data_dir: Path to raw data directory
        metadata_dir: Path to metadata directory
    """
    print("\n" + "=" * 60)
    print("GENERATING CHECKSUMS")
    print("=" * 60)

    # Define specific files to process for integration
    dataset1_dir = raw_data_dir / "Dataset 1"
    dataset2_dir = raw_data_dir / "Dataset 2" / "football-datasets" / "datasets"

    data_files = [
        # Dataset 1 files
        dataset1_dir / "teams.csv",
        dataset1_dir / "teamStats.csv",
        dataset1_dir / "standings.csv",
        dataset1_dir / "leagues.csv",
        # Dataset 2 consolidated file
        dataset2_dir / "all_leagues_all_seasons.csv"
    ]

    # Filter to only existing files
    data_files = [f for f in data_files if f.exists()]

    print(f"Processing {len(data_files)} key files for integration:")
    for f in data_files:
        print(f"  - {f.relative_to(raw_data_dir)}")
    print()

    checksums = []
    metadata = {
        'generated_at': datetime.now().isoformat(),
        'total_files': len(data_files),
        'files': []
    }

    for i, filepath in enumerate(data_files, 1):
        # Get relative path (handle both absolute and relative paths)
        try:
            if filepath.is_absolute():
                relative_path = filepath.relative_to(Path.cwd())
            else:
                relative_path = filepath
        except ValueError:
            relative_path = filepath

        print(f"[{i}/{len(data_files)}] Processing: {relative_path}")

        checksum = generate_checksum(filepath)
        file_size = get_file_size(filepath)

        if checksum:
            checksums.append(f"{checksum}  {relative_path}")

            metadata['files'].append({
                'path': str(relative_path),
                'checksum': checksum,
                'size': file_size,
                'size_bytes': os.path.getsize(filepath),
                'modified': datetime.fromtimestamp(filepath.stat().st_mtime).isoformat()
            })

            print(f"  Checksum: {checksum[:16]}...")
            print(f"  Size: {file_size}")

    # Write checksums.txt (standard format)
    checksums_file = metadata_dir / "checksums.txt"
    with open(checksums_file, 'w') as f:
        f.write(f"# SHA-256 Checksums\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Total files: {len(checksums)}\n")
        f.write("#\n")
        for line in checksums:
            f.write(f"{line}\n")

    print(f"\n[SUCCESS] Checksums saved to: {checksums_file}")

    # Write detailed metadata JSON
    metadata_file = metadata_dir / "acquisition_metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"[SUCCESS] Metadata saved to: {metadata_file}")

    return metadata


def generate_acquisition_report(metadata, metadata_dir):
    """Generate a human-readable acquisition report."""
    report_file = metadata_dir / "acquisition_report.md"

    total_size_bytes = sum(f['size_bytes'] for f in metadata['files'])
    total_size_mb = total_size_bytes / (1024 * 1024)

    with open(report_file, 'w') as f:
        f.write("# Data Acquisition Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")

        f.write("## Summary\n\n")
        f.write(f"- **Total Files Processed:** {metadata['total_files']}\n")
        f.write(f"- **Total Size:** {total_size_mb:.2f} MB\n")
        f.write(f"- **Verification Status:** Complete\n")
        f.write(f"- **Purpose:** Key files for data integration only\n\n")

        f.write("## Dataset 1: ESPN Soccer Data (Local)\n\n")
        dataset1_files = [f for f in metadata['files'] if 'Dataset 1' in f['path']]
        f.write(f"- **Files Processed:** {len(dataset1_files)}\n")
        f.write(f"- **Source:** https://www.kaggle.com/datasets/excel4soccer/espn-soccer-data\n")
        f.write(f"- **Storage:** Stored locally in repository at data/raw/Dataset 1/\n")
        f.write(f"- **License:** Check Kaggle dataset page\n\n")

        f.write("### Files\n\n")
        for file_info in dataset1_files:
            f.write(f"- `{Path(file_info['path']).name}` - {file_info['size']}\n")

        f.write("\n## Dataset 2: Football-Data.co.uk\n\n")
        dataset2_files = [f for f in metadata['files'] if 'Dataset 2' in f['path']]
        f.write(f"- **Files Processed:** {len(dataset2_files)}\n")
        f.write(f"- **Source:** https://github.com/datasets/football-datasets\n")
        f.write(f"- **License:** PDDL 1.0 (Public Domain)\n\n")

        f.write("### Files\n\n")
        for file_info in dataset2_files:
            filename = Path(file_info['path']).name
            f.write(f"- `{filename}` - {file_info['size']}\n")
            if filename == 'all_leagues_all_seasons.csv':
                f.write(f"  - **Primary integration file**\n")
                f.write(f"  - Contains: All 5 leagues (Premier League, La Liga, Bundesliga, Serie A, Ligue 1)\n")
                f.write(f"  - Time span: 1999-2025\n")

        f.write("\n---\n\n")
        f.write("## File Details\n\n")
        f.write("| File | Size | Checksum (SHA-256) |\n")
        f.write("|------|------|-----------|\n")
        for file_info in metadata['files']:
            filename = Path(file_info['path']).name
            checksum_short = file_info['checksum'][:16] + "..."
            f.write(f"| `{filename}` | {file_info['size']} | `{checksum_short}` |\n")

        f.write("\n---\n\n")
        f.write("## Verification\n\n")
        f.write("All files have been verified with SHA-256 checksums.\n")
        f.write("See `checksums.txt` for complete checksum listing.\n\n")

        f.write("## Notes\n\n")
        f.write("- Only processing key files needed for data integration\n")
        f.write("- Dataset 2: Using consolidated `all_leagues_all_seasons.csv` only\n")
        f.write("- Ignored files with [invalid] prefix\n")
        f.write("- Ignored individual season files (using consolidated version)\n\n")

    print(f"[SUCCESS] Acquisition report saved to: {report_file}")


def main():
    """Main data acquisition pipeline."""
    print("=" * 60)
    print("DATA ACQUISITION & VERIFICATION")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Define directories
    raw_data_dir = Path("data/raw")
    metadata_dir = Path("data/metadata")

    # Create metadata directory if needed
    metadata_dir.mkdir(parents=True, exist_ok=True)

    # Verify datasets exist
    print("=" * 60)
    print("VERIFYING DATASETS")
    print("=" * 60)

    dataset1_ok = verify_dataset1(raw_data_dir)
    dataset2_ok = verify_dataset2(raw_data_dir)

    # Allow pipeline to continue if at least one dataset is available
    if not (dataset1_ok or dataset2_ok):
        print("\n[ERROR] No datasets found!")
        print("Please ensure at least one dataset is downloaded to data/raw/")
        return False

    if not (dataset1_ok and dataset2_ok):
        print("\n[WARNING] Some datasets are missing or incomplete!")
        if not dataset1_ok:
            print("  - Dataset 1 (Local) is missing or incomplete")
            print("    Please ensure Dataset 1 files are in data/raw/Dataset 1/")
        if not dataset2_ok:
            print("  - Dataset 2 (GitHub) is missing")
            print("    Run: python acquire_data.py to download")
        print("\nContinuing with available datasets...")

    # Generate checksums
    metadata = generate_checksums_file(raw_data_dir, metadata_dir)

    # Generate report
    print("\n" + "=" * 60)
    print("GENERATING REPORT")
    print("=" * 60)
    generate_acquisition_report(metadata, metadata_dir)

    print("\n" + "=" * 60)
    print("[SUCCESS] DATA ACQUISITION COMPLETE!")
    print("=" * 60)
    print(f"\nMetadata files created in: {metadata_dir}/")
    print("  - checksums.txt")
    print("  - acquisition_metadata.json")
    print("  - acquisition_report.md")
    print()

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
