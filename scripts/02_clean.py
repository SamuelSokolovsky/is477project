"""
Data Cleaning Script
====================
Purpose: Clean and standardize datasets

Tasks:
1. Team name standardization across datasets
2. Handle missing values appropriately
3. Data type validation and conversion
4. Create team name mapping dictionary

Output:
- Cleaned datasets in data/processed/
- Team name mappings in data/metadata/
"""

import pandas as pd
import numpy as np
import re
from pathlib import Path
from datetime import datetime


def standardize_team_name(name):
    """
    Standardize a single team name.

    Steps:
    1. Convert to lowercase
    2. Remove special characters and extra whitespace
    3. Apply known aliases

    Args:
        name: Original team name

    Returns:
        Standardized team name
    """
    if pd.isna(name):
        return name

    # Convert to string and lowercase
    name = str(name).lower().strip()

    # Remove special characters but keep spaces and hyphens
    name = re.sub(r'[^\w\s-]', '', name)

    # Remove extra whitespace
    name = re.sub(r'\s+', ' ', name)

    # Apply common aliases
    aliases = {
        'man united': 'manchester united',
        'man city': 'manchester city',
        'man utd': 'manchester united',
        'psg': 'paris saint germain',
        'paris sg': 'paris saint germain',
        'newcastle': 'newcastle united',
        'west ham': 'west ham united',
        'wolves': 'wolverhampton wanderers',
        'tottenham': 'tottenham hotspur',
        'spurs': 'tottenham hotspur',
        'brighton': 'brighton and hove albion',
        'nottm forest': 'nottingham forest',
        'nott\'m forest': 'nottingham forest',
        'notts forest': 'nottingham forest',
        'bayern': 'bayern munich',
        'bayern munchen': 'bayern munich',
        'fc bayern': 'bayern munich',
        'ein frankfurt': 'eintracht frankfurt',
        'fc barcelona': 'barcelona',
        'barca': 'barcelona',
        'real': 'real madrid',
        'atletico': 'atletico madrid',
        'inter': 'inter milan',
        'ac milan': 'milan',
        'munich 1860': '1860 munich',
        'werder bremen': 'werder',
    }

    # Apply alias mapping
    if name in aliases:
        name = aliases[name]

    return name


def clean_dataset2(df):
    """
    Clean Dataset 2 (all_leagues_all_seasons.csv).

    Args:
        df: Raw DataFrame

    Returns:
        Cleaned DataFrame
    """
    print("\n[Cleaning Dataset 2: Match Results]")
    print(f"  Original shape: {df.shape}")

    # Create a copy
    df_clean = df.copy()

    # 1. Standardize team names
    print("  Standardizing team names...")
    df_clean['HomeTeam_std'] = df_clean['HomeTeam'].apply(standardize_team_name)
    df_clean['AwayTeam_std'] = df_clean['AwayTeam'].apply(standardize_team_name)

    # 2. Parse dates properly
    print("  Parsing dates...")
    df_clean['Date'] = pd.to_datetime(df_clean['Date'], format='%d/%m/%y', errors='coerce')

    # Handle dates from 1900s vs 2000s (fix century)
    # If year > current year, assume 1900s
    current_year = datetime.now().year
    mask = df_clean['Date'].dt.year > current_year
    df_clean.loc[mask, 'Date'] = df_clean.loc[mask, 'Date'] - pd.DateOffset(years=100)

    # 3. Handle missing values
    print("  Handling missing values...")

    # Cards: Fill with 0 (no cards means 0)
    card_cols = ['HY', 'AY', 'HR', 'AR']
    for col in card_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna(0).astype(int)

    # Half-time stats: Keep as NaN if missing (don't impute)
    # Shots, fouls, corners: Keep as NaN for now (will impute in analysis if needed)

    # 4. Validate data types
    print("  Validating data types...")

    # Numeric columns
    numeric_cols = ['FTHG', 'FTAG', 'HTHG', 'HTAG', 'HS', 'AS', 'HST', 'AST',
                   'HF', 'AF', 'HC', 'AC']
    for col in numeric_cols:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

    # 5. Add season column (extract from date)
    print("  Adding season column...")
    df_clean['Season'] = df_clean['Date'].apply(lambda x: f"{x.year-1}-{x.year}" if x.month < 8 else f"{x.year}-{x.year+1}" if pd.notna(x) else None)

    # 6. Validate results match goals
    print("  Validating results...")
    df_clean['FTR_calculated'] = df_clean.apply(
        lambda row: 'H' if row['FTHG'] > row['FTAG']
                    else ('A' if row['FTAG'] > row['FTHG'] else 'D'),
        axis=1
    )

    mismatches = (df_clean['FTR'] != df_clean['FTR_calculated']).sum()
    if mismatches > 0:
        print(f"  [WARNING] Found {mismatches} result mismatches - using calculated results")
        df_clean['FTR'] = df_clean['FTR_calculated']

    df_clean = df_clean.drop('FTR_calculated', axis=1)

    print(f"  Cleaned shape: {df_clean.shape}")
    print(f"  Date range: {df_clean['Date'].min()} to {df_clean['Date'].max()}")
    print(f"  Unique teams: {df_clean['HomeTeam_std'].nunique()}")

    return df_clean


def clean_dataset1_teams(df):
    """
    Clean Dataset 1 teams.csv.

    Args:
        df: Raw DataFrame

    Returns:
        Cleaned DataFrame
    """
    print("\n[Cleaning Dataset 1: Teams]")
    print(f"  Original shape: {df.shape}")

    df_clean = df.copy()

    # Standardize team name
    df_clean['name_std'] = df_clean['name'].apply(standardize_team_name)
    df_clean['displayName_std'] = df_clean['displayName'].apply(standardize_team_name)

    # Keep only relevant columns
    cols_to_keep = ['teamId', 'name', 'name_std', 'displayName', 'displayName_std',
                    'location', 'abbreviation']
    df_clean = df_clean[cols_to_keep]

    print(f"  Cleaned shape: {df_clean.shape}")

    return df_clean


def clean_dataset1_teamstats(df):
    """
    Clean Dataset 1 teamStats.csv.

    Args:
        df: Raw DataFrame

    Returns:
        Cleaned DataFrame
    """
    print("\n[Cleaning Dataset 1: Team Stats]")
    print(f"  Original shape: {df.shape}")

    df_clean = df.copy()

    # Convert numeric columns
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
    for col in numeric_cols:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

    print(f"  Cleaned shape: {df_clean.shape}")

    return df_clean


def clean_dataset1_standings(df):
    """
    Clean Dataset 1 standings.csv.

    Args:
        df: Raw DataFrame

    Returns:
        Cleaned DataFrame
    """
    print("\n[Cleaning Dataset 1: Standings]")
    print(f"  Original shape: {df.shape}")

    df_clean = df.copy()

    # Convert numeric columns
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
    for col in numeric_cols:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

    print(f"  Cleaned shape: {df_clean.shape}")

    return df_clean


def clean_dataset1_leagues(df):
    """
    Clean Dataset 1 leagues.csv.

    Args:
        df: Raw DataFrame

    Returns:
        Cleaned DataFrame
    """
    print("\n[Cleaning Dataset 1: Leagues]")
    print(f"  Original shape: {df.shape}")

    df_clean = df.copy()

    print(f"  Cleaned shape: {df_clean.shape}")

    return df_clean


def create_team_mapping(df2_teams, df1_teams):
    """
    Create mapping between Dataset 2 team names and Dataset 1 team names.

    Args:
        df2_teams: Unique teams from Dataset 2
        df1_teams: Teams DataFrame from Dataset 1

    Returns:
        DataFrame with team mappings
    """
    print("\n[Creating Team Name Mappings]")

    # Get unique standardized team names from Dataset 2
    d2_teams = sorted(df2_teams)

    mappings = []
    for team in d2_teams:
        mappings.append({
            'dataset2_name': team,
            'standardized_name': team,
            'matched_dataset1': False
        })

    mapping_df = pd.DataFrame(mappings)

    print(f"  Total unique teams in Dataset 2: {len(mapping_df)}")

    return mapping_df


def generate_cleaning_report(stats, output_dir):
    """Generate cleaning report."""
    report_file = output_dir / "cleaning_report.md"

    with open(report_file, 'w') as f:
        f.write("# Data Cleaning Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")

        f.write("## Summary\n\n")
        f.write(f"- **Files Processed:** 5\n")
        f.write(f"- **Cleaning Operations:** Standardization, Missing value handling, Type validation\n")
        f.write(f"- **Output Location:** `data/processed/`\n\n")

        f.write("## Dataset 2: Match Results\n\n")
        f.write(f"- **Records:** {stats['dataset2_records']:,}\n")
        f.write(f"- **Date Range:** {stats['dataset2_date_range']}\n")
        f.write(f"- **Unique Teams:** {stats['dataset2_teams']}\n")
        f.write(f"- **Leagues:** {', '.join(stats['dataset2_leagues'])}\n\n")

        f.write("### Cleaning Operations\n\n")
        f.write("1. **Team Names:** Standardized to lowercase, removed special characters\n")
        f.write("2. **Dates:** Parsed and validated (DD/MM/YY format)\n")
        f.write("3. **Missing Cards:** Filled with 0\n")
        f.write("4. **Result Validation:** Verified FTR matches FTHG vs FTAG\n")
        f.write("5. **Season Column:** Added based on match date\n\n")

        f.write("## Dataset 1 Files\n\n")
        f.write(f"- **Teams:** {stats['dataset1_teams']:,} records\n")
        f.write(f"- **Team Stats:** {stats['dataset1_teamstats']:,} records\n")
        f.write(f"- **Standings:** {stats['dataset1_standings']:,} records\n")
        f.write(f"- **Leagues:** {stats['dataset1_leagues']:,} records\n\n")

        f.write("---\n\n")
        f.write("## Next Steps\n\n")
        f.write("1. Run `03_integrate.py` to merge datasets\n")
        f.write("2. Team name matching will be performed during integration\n")
        f.write("3. Quality assessment in `04_quality.py`\n\n")

    print(f"  [SUCCESS] Cleaning report saved to: {report_file}")


def main():
    """Main cleaning pipeline."""
    print("=" * 60)
    print("DATA CLEANING SCRIPT")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Define paths
    raw_dir = Path("data/raw")
    processed_dir = Path("data/processed")
    metadata_dir = Path("data/metadata")

    # Create output directories
    processed_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load Dataset 2 (match results)
    print("\n" + "=" * 60)
    print("LOADING DATASETS")
    print("=" * 60)

    df2_path = raw_dir / "Dataset 2" / "football-datasets" / "datasets" / "all_leagues_all_seasons.csv"
    print(f"Loading: {df2_path}")
    df2_raw = pd.read_csv(df2_path)

    # 2. Load Dataset 1 files
    df1_teams_raw = pd.read_csv(raw_dir / "Dataset 1" / "teams.csv")
    df1_teamstats_raw = pd.read_csv(raw_dir / "Dataset 1" / "teamStats.csv")
    df1_standings_raw = pd.read_csv(raw_dir / "Dataset 1" / "standings.csv")
    df1_leagues_raw = pd.read_csv(raw_dir / "Dataset 1" / "leagues.csv")

    # 3. Clean datasets
    print("\n" + "=" * 60)
    print("CLEANING DATASETS")
    print("=" * 60)

    df2_clean = clean_dataset2(df2_raw)
    df1_teams_clean = clean_dataset1_teams(df1_teams_raw)
    df1_teamstats_clean = clean_dataset1_teamstats(df1_teamstats_raw)
    df1_standings_clean = clean_dataset1_standings(df1_standings_raw)
    df1_leagues_clean = clean_dataset1_leagues(df1_leagues_raw)

    # 4. Create team name mappings
    unique_teams = pd.concat([
        df2_clean['HomeTeam_std'],
        df2_clean['AwayTeam_std']
    ]).unique()

    team_mapping = create_team_mapping(unique_teams, df1_teams_clean)

    # 5. Save cleaned datasets
    print("\n" + "=" * 60)
    print("SAVING CLEANED DATASETS")
    print("=" * 60)

    df2_clean.to_csv(processed_dir / "dataset2_clean.csv", index=False)
    print(f"  [OK] Saved: dataset2_clean.csv")

    df1_teams_clean.to_csv(processed_dir / "dataset1_teams_clean.csv", index=False)
    print(f"  [OK] Saved: dataset1_teams_clean.csv")

    df1_teamstats_clean.to_csv(processed_dir / "dataset1_teamstats_clean.csv", index=False)
    print(f"  [OK] Saved: dataset1_teamstats_clean.csv")

    df1_standings_clean.to_csv(processed_dir / "dataset1_standings_clean.csv", index=False)
    print(f"  [OK] Saved: dataset1_standings_clean.csv")

    df1_leagues_clean.to_csv(processed_dir / "dataset1_leagues_clean.csv", index=False)
    print(f"  [OK] Saved: dataset1_leagues_clean.csv")

    team_mapping.to_csv(metadata_dir / "team_name_mappings.csv", index=False)
    print(f"  [OK] Saved: team_name_mappings.csv")

    # 6. Generate cleaning report
    print("\n" + "=" * 60)
    print("GENERATING REPORT")
    print("=" * 60)

    stats = {
        'dataset2_records': len(df2_clean),
        'dataset2_date_range': f"{df2_clean['Date'].min().strftime('%Y-%m-%d')} to {df2_clean['Date'].max().strftime('%Y-%m-%d')}",
        'dataset2_teams': df2_clean['HomeTeam_std'].nunique(),
        'dataset2_leagues': sorted(df2_clean['league_name'].unique()),
        'dataset1_teams': len(df1_teams_clean),
        'dataset1_teamstats': len(df1_teamstats_clean),
        'dataset1_standings': len(df1_standings_clean),
        'dataset1_leagues': len(df1_leagues_clean)
    }

    generate_cleaning_report(stats, processed_dir)

    print("\n" + "=" * 60)
    print("[SUCCESS] DATA CLEANING COMPLETE!")
    print("=" * 60)
    print(f"\nCleaned files saved to: {processed_dir}/")
    print("  - dataset2_clean.csv")
    print("  - dataset1_teams_clean.csv")
    print("  - dataset1_teamstats_clean.csv")
    print("  - dataset1_standings_clean.csv")
    print("  - dataset1_leagues_clean.csv")
    print(f"\nMetadata saved to: {metadata_dir}/")
    print("  - team_name_mappings.csv")
    print("\n")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
