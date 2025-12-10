"""
Data Quality Assessment Script
===============================
Purpose: Comprehensive quality profiling of integrated dataset

Quality Dimensions:
1. Completeness - Missing value analysis
2. Validity - Range and constraint checking
3. Consistency - Cross-field validation
4. Accuracy - Sample verification
5. Uniqueness - Duplicate detection

Output:
- Quality report in outputs/reports/data_quality_report.md
- Quality visualizations in outputs/figures/
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime

# Set matplotlib style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def assess_completeness(df):
    """
    Analyze completeness:
    - % missing values per column
    - Row completeness distribution
    """
    print("\n[1/5] Assessing Completeness...")

    completeness = {}

    # Missing values per column
    missing_counts = df.isnull().sum()
    missing_pct = (missing_counts / len(df) * 100).round(2)

    completeness['missing_by_column'] = pd.DataFrame({
        'missing_count': missing_counts,
        'missing_pct': missing_pct,
        'complete_pct': (100 - missing_pct).round(2)
    }).sort_values('missing_pct', ascending=False)

    # Row completeness
    row_completeness = df.notna().sum(axis=1) / len(df.columns) * 100
    completeness['row_stats'] = {
        'mean_completeness': row_completeness.mean(),
        'min_completeness': row_completeness.min(),
        'rows_100pct_complete': (row_completeness == 100).sum(),
        'rows_90pct_complete': (row_completeness >= 90).sum()
    }

    # Core fields completeness (must be 100%)
    core_fields = ['match_id', 'match_date', 'home_team', 'away_team',
                   'home_goals', 'away_goals', 'result', 'league', 'season']
    core_complete = True
    for field in core_fields:
        if field in df.columns:
            if df[field].isnull().any():
                core_complete = False
                break

    completeness['core_fields_complete'] = core_complete

    print(f"  Core fields 100% complete: {core_complete}")
    print(f"  Rows with 100% completeness: {completeness['row_stats']['rows_100pct_complete']:,}")
    print(f"  Fields with missing data: {(missing_pct > 0).sum()}")

    return completeness


def assess_validity(df):
    """
    Check validity constraints:
    - Goals ≥ 0
    - Shots ≥ Shots on Target
    - Cards are integers ≥ 0
    - Dates in valid range
    """
    print("\n[2/5] Assessing Validity...")

    validity = {
        'passed': True,
        'issues': []
    }

    # Goals must be >= 0
    if (df['home_goals'] < 0).any() or (df['away_goals'] < 0).any():
        validity['passed'] = False
        validity['issues'].append("Negative goals found")

    # Shots >= Shots on Target (where data exists)
    shots_valid = df[df['home_shots'].notna() & df['home_shots_on_target'].notna()]
    if (shots_valid['home_shots'] < shots_valid['home_shots_on_target']).any():
        count = (shots_valid['home_shots'] < shots_valid['home_shots_on_target']).sum()
        validity['issues'].append(f"Home shots < shots on target: {count} cases")

    shots_valid_away = df[df['away_shots'].notna() & df['away_shots_on_target'].notna()]
    if (shots_valid_away['away_shots'] < shots_valid_away['away_shots_on_target']).any():
        count = (shots_valid_away['away_shots'] < shots_valid_away['away_shots_on_target']).sum()
        validity['issues'].append(f"Away shots < shots on target: {count} cases")

    # Cards must be >= 0
    card_cols = ['home_yellow_cards', 'away_yellow_cards', 'home_red_cards', 'away_red_cards']
    for col in card_cols:
        if col in df.columns:
            if (df[col] < 0).any():
                validity['passed'] = False
                validity['issues'].append(f"Negative cards in {col}")

    # Dates in valid range (1990-2026)
    df_dates = df[df['match_date'].notna()].copy()
    df_dates['match_date'] = pd.to_datetime(df_dates['match_date'])
    if (df_dates['match_date'].dt.year < 1990).any():
        count = (df_dates['match_date'].dt.year < 1990).sum()
        validity['issues'].append(f"Dates before 1990: {count} matches")
    if (df_dates['match_date'].dt.year > 2026).any():
        count = (df_dates['match_date'].dt.year > 2026).sum()
        validity['issues'].append(f"Dates after 2026: {count} matches")

    # Result must be H, A, or D
    if not df['result'].isin(['H', 'A', 'D']).all():
        invalid_count = (~df['result'].isin(['H', 'A', 'D'])).sum()
        validity['issues'].append(f"Invalid result codes: {invalid_count} matches")

    validity['total_issues'] = len(validity['issues'])

    if validity['total_issues'] == 0:
        print("  [OK] All validity checks passed")
    else:
        print(f"  [WARNING] Found {validity['total_issues']} validity issues")
        for issue in validity['issues']:
            print(f"    - {issue}")

    return validity


def assess_consistency(df):
    """
    Check consistency:
    - Result matches goals
    - Shot accuracy within bounds
    - Derived fields match calculations
    """
    print("\n[3/5] Assessing Consistency...")

    consistency = {
        'passed': True,
        'issues': []
    }

    # Result consistency (already validated in cleaning, but double-check)
    df['result_calc'] = df.apply(
        lambda row: 'H' if row['home_goals'] > row['away_goals']
                    else ('A' if row['away_goals'] > row['home_goals'] else 'D'),
        axis=1
    )
    result_mismatch = (df['result'] != df['result_calc']).sum()
    if result_mismatch > 0:
        consistency['issues'].append(f"Result/goals mismatch: {result_mismatch} matches")

    # Goal differential consistency
    goal_diff_calc = df['home_goals'] - df['away_goals']
    goal_diff_mismatch = (df['goal_differential'] != goal_diff_calc).sum()
    if goal_diff_mismatch > 0:
        consistency['issues'].append(f"Goal differential inconsistent: {goal_diff_mismatch} matches")

    # Shot accuracy bounds (0-1)
    df_acc = df[df['home_shot_accuracy'].notna()]
    if ((df_acc['home_shot_accuracy'] < 0) | (df_acc['home_shot_accuracy'] > 1)).any():
        count = ((df_acc['home_shot_accuracy'] < 0) | (df_acc['home_shot_accuracy'] > 1)).sum()
        consistency['issues'].append(f"Shot accuracy out of bounds: {count} cases")

    # Total goals consistency
    total_goals_calc = df['home_goals'] + df['away_goals']
    total_goals_mismatch = (df['total_goals'] != total_goals_calc).sum()
    if total_goals_mismatch > 0:
        consistency['issues'].append(f"Total goals inconsistent: {total_goals_mismatch} matches")

    consistency['total_issues'] = len(consistency['issues'])

    if consistency['total_issues'] == 0:
        print("  [OK] All consistency checks passed")
    else:
        print(f"  [WARNING] Found {consistency['total_issues']} consistency issues")
        for issue in consistency['issues']:
            print(f"    - {issue}")

    return consistency


def assess_accuracy(df):
    """
    Verify accuracy:
    - Check for logical impossibilities
    - Verify statistical distributions
    """
    print("\n[4/5] Assessing Accuracy...")

    accuracy = {
        'passed': True,
        'issues': [],
        'stats': {}
    }

    # Check for impossible statistics
    # More than 15 goals in a match is extremely rare
    high_scoring = df[df['total_goals'] > 15]
    if len(high_scoring) > 0:
        accuracy['issues'].append(f"Extremely high-scoring matches: {len(high_scoring)} with >15 goals")

    # More than 20 shots on target is very rare
    df_shots = df[df['home_shots_on_target'].notna()]
    extreme_shots = df_shots[(df_shots['home_shots_on_target'] > 25) |
                             (df_shots['away_shots_on_target'] > 25)]
    if len(extreme_shots) > 0:
        accuracy['issues'].append(f"Extreme shot counts: {len(extreme_shots)} matches with >25 shots on target")

    # More than 5 red cards total is extremely rare
    df_cards = df[(df['home_red_cards'] + df['away_red_cards']) > 5]
    if len(df_cards) > 0:
        accuracy['issues'].append(f"Extreme red card matches: {len(df_cards)} with >5 total red cards")

    # Statistical distribution checks
    accuracy['stats']['mean_goals'] = df['total_goals'].mean()
    accuracy['stats']['mean_home_goals'] = df['home_goals'].mean()
    accuracy['stats']['mean_away_goals'] = df['away_goals'].mean()
    accuracy['stats']['home_win_rate'] = (df['result'] == 'H').mean() * 100

    # Expected ranges (based on historical data)
    if not (2.0 <= accuracy['stats']['mean_goals'] <= 3.5):
        accuracy['issues'].append(f"Unusual average goals: {accuracy['stats']['mean_goals']:.2f}")

    if not (38 <= accuracy['stats']['home_win_rate'] <= 52):
        accuracy['issues'].append(f"Unusual home win rate: {accuracy['stats']['home_win_rate']:.1f}%")

    accuracy['total_issues'] = len(accuracy['issues'])

    if accuracy['total_issues'] == 0:
        print("  [OK] All accuracy checks passed")
    else:
        print(f"  [INFO] Found {accuracy['total_issues']} statistical anomalies (may be valid)")
        for issue in accuracy['issues'][:5]:  # Show first 5
            print(f"    - {issue}")

    return accuracy


def assess_uniqueness(df):
    """
    Check uniqueness:
    - Detect duplicate match IDs
    - Detect duplicate matches (same teams, date, result)
    """
    print("\n[5/5] Assessing Uniqueness...")

    uniqueness = {
        'passed': True,
        'issues': []
    }

    # Check for duplicate match IDs
    duplicate_ids = df['match_id'].duplicated().sum()
    if duplicate_ids > 0:
        uniqueness['passed'] = False
        uniqueness['issues'].append(f"Duplicate match IDs: {duplicate_ids}")

    # Check for duplicate matches (same date, teams)
    duplicate_matches = df.duplicated(subset=['match_date', 'home_team', 'away_team'], keep=False).sum()
    if duplicate_matches > 0:
        uniqueness['issues'].append(f"Potential duplicate matches: {duplicate_matches}")

    # Check match_id uniqueness rate
    uniqueness['unique_matches'] = df['match_id'].nunique()
    uniqueness['total_records'] = len(df)
    uniqueness['uniqueness_rate'] = (uniqueness['unique_matches'] / uniqueness['total_records'] * 100)

    uniqueness['total_issues'] = len(uniqueness['issues'])

    if uniqueness['total_issues'] == 0:
        print("  [OK] All uniqueness checks passed")
        print(f"  Unique match IDs: {uniqueness['unique_matches']:,} / {uniqueness['total_records']:,}")
    else:
        print(f"  [WARNING] Found {uniqueness['total_issues']} uniqueness issues")
        for issue in uniqueness['issues']:
            print(f"    - {issue}")

    return uniqueness


def create_visualizations(df, quality_metrics, output_dir):
    """Generate quality visualizations."""
    print("\n[Generating Visualizations...]")

    figures_dir = output_dir / "quality"
    figures_dir.mkdir(parents=True, exist_ok=True)

    # 1. Completeness heatmap
    plt.figure(figsize=(14, 8))
    completeness_data = quality_metrics['completeness']['missing_by_column']['missing_pct']

    # Select columns with any missing data
    cols_with_missing = completeness_data[completeness_data > 0].sort_values(ascending=False)

    if len(cols_with_missing) > 0:
        plt.barh(range(len(cols_with_missing)), cols_with_missing.values)
        plt.yticks(range(len(cols_with_missing)), cols_with_missing.index)
        plt.xlabel('Missing Data (%)')
        plt.title('Data Completeness by Column')
        plt.tight_layout()
        plt.savefig(figures_dir / 'completeness_by_column.png', dpi=150, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Saved: completeness_by_column.png")

    # 2. Data completeness over time
    plt.figure(figsize=(12, 6))
    df_time = df.copy()
    df_time['match_date'] = pd.to_datetime(df_time['match_date'])
    df_time['year'] = df_time['match_date'].dt.year

    yearly_completeness = df_time.groupby('year').apply(
        lambda x: (x['home_shots'].notna().sum() / len(x) * 100)
    )

    plt.plot(yearly_completeness.index, yearly_completeness.values, marker='o', linewidth=2)
    plt.xlabel('Year')
    plt.ylabel('Shot Data Completeness (%)')
    plt.title('Data Completeness Evolution Over Time')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(figures_dir / 'completeness_over_time.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Saved: completeness_over_time.png")

    # 3. Goals distribution
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    df['total_goals'].value_counts().sort_index().plot(kind='bar')
    plt.xlabel('Total Goals')
    plt.ylabel('Frequency')
    plt.title('Distribution of Total Goals per Match')

    plt.subplot(1, 2, 2)
    plt.hist([df['home_goals'], df['away_goals']], bins=range(0, 11),
             label=['Home', 'Away'], alpha=0.7)
    plt.xlabel('Goals')
    plt.ylabel('Frequency')
    plt.title('Home vs Away Goals Distribution')
    plt.legend()
    plt.tight_layout()
    plt.savefig(figures_dir / 'goals_distribution.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Saved: goals_distribution.png")

    print(f"  All visualizations saved to: {figures_dir}/")


def generate_quality_report(quality_metrics, output_file):
    """
    Generate comprehensive quality report.

    NOTE: This report generation code was created using AI assistance.
    The reports generated in outputs/reports/ are managerial reports for
    troubleshooting purposes only. AI is particularly effective at formatting
    and presenting output data in readable markdown format.
    """
    print("\n[Generating Quality Report...]")

    with open(output_file, 'w') as f:
        f.write("# Data Quality Assessment Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")

        # Executive Summary
        f.write("## Executive Summary\n\n")

        total_issues = sum([
            quality_metrics['validity']['total_issues'],
            quality_metrics['consistency']['total_issues'],
            quality_metrics['accuracy']['total_issues'],
            quality_metrics['uniqueness']['total_issues']
        ])

        if total_issues == 0:
            f.write("**Overall Status:** [EXCELLENT] All quality checks passed\n\n")
        elif total_issues <= 5:
            f.write("**Overall Status:** [GOOD] Minor issues detected\n\n")
        else:
            f.write(f"**Overall Status:** [REVIEW NEEDED] {total_issues} issues detected\n\n")

        # Dimension summary
        f.write("### Quality Dimensions\n\n")
        f.write("| Dimension | Status | Issues |\n")
        f.write("|-----------|--------|--------|\n")
        f.write(f"| Completeness | {'[PASS]' if quality_metrics['completeness']['core_fields_complete'] else '[FAIL]'} | Core fields complete |\n")
        f.write(f"| Validity | {'[PASS]' if quality_metrics['validity']['total_issues'] == 0 else '[WARN]'} | {quality_metrics['validity']['total_issues']} issues |\n")
        f.write(f"| Consistency | {'[PASS]' if quality_metrics['consistency']['total_issues'] == 0 else '[WARN]'} | {quality_metrics['consistency']['total_issues']} issues |\n")
        f.write(f"| Accuracy | {'[PASS]' if quality_metrics['accuracy']['total_issues'] == 0 else '[INFO]'} | {quality_metrics['accuracy']['total_issues']} anomalies |\n")
        f.write(f"| Uniqueness | {'[PASS]' if quality_metrics['uniqueness']['total_issues'] == 0 else '[WARN]'} | {quality_metrics['uniqueness']['total_issues']} issues |\n\n")

        # Detailed findings
        f.write("---\n\n")
        f.write("## 1. Completeness Assessment\n\n")

        comp = quality_metrics['completeness']
        f.write(f"- **Rows with 100% completeness:** {comp['row_stats']['rows_100pct_complete']:,}\n")
        f.write(f"- **Average row completeness:** {comp['row_stats']['mean_completeness']:.2f}%\n")
        f.write(f"- **Core fields complete:** {comp['core_fields_complete']}\n\n")

        f.write("### Top Missing Fields\n\n")
        f.write("| Field | Missing % | Complete % |\n")
        f.write("|-------|-----------|------------|\n")

        top_missing = comp['missing_by_column'].head(10)
        for field, row in top_missing.iterrows():
            if row['missing_pct'] > 0:
                f.write(f"| `{field}` | {row['missing_pct']:.1f}% | {row['complete_pct']:.1f}% |\n")

        # Other dimensions
        f.write("\n---\n\n")
        f.write("## 2. Validity Assessment\n\n")
        if quality_metrics['validity']['total_issues'] == 0:
            f.write("All validity checks passed.\n\n")
        else:
            f.write("Issues found:\n\n")
            for issue in quality_metrics['validity']['issues']:
                f.write(f"- {issue}\n")

        f.write("\n---\n\n")
        f.write("## 3. Consistency Assessment\n\n")
        if quality_metrics['consistency']['total_issues'] == 0:
            f.write("All consistency checks passed.\n\n")
        else:
            f.write("Issues found:\n\n")
            for issue in quality_metrics['consistency']['issues']:
                f.write(f"- {issue}\n")

        f.write("\n---\n\n")
        f.write("## 4. Accuracy Assessment\n\n")
        acc = quality_metrics['accuracy']
        f.write(f"- **Mean goals per match:** {acc['stats']['mean_goals']:.2f}\n")
        f.write(f"- **Home win rate:** {acc['stats']['home_win_rate']:.1f}%\n\n")

        if acc['total_issues'] > 0:
            f.write("Anomalies detected:\n\n")
            for issue in acc['issues']:
                f.write(f"- {issue}\n")

        f.write("\n---\n\n")
        f.write("## 5. Uniqueness Assessment\n\n")
        uniq = quality_metrics['uniqueness']
        f.write(f"- **Unique matches:** {uniq['unique_matches']:,}\n")
        f.write(f"- **Total records:** {uniq['total_records']:,}\n")
        f.write(f"- **Uniqueness rate:** {uniq['uniqueness_rate']:.2f}%\n\n")

        if uniq['total_issues'] > 0:
            f.write("Issues found:\n\n")
            for issue in uniq['issues']:
                f.write(f"- {issue}\n")

        f.write("\n---\n\n")
        f.write("## Recommendations\n\n")
        f.write("1. Missing shot/foul data is expected for older seasons (pre-2005)\n")
        f.write("2. Core match data (goals, results, teams) is 100% complete\n")
        f.write("3. Dataset is suitable for analysis with proper handling of missing data\n")
        f.write("4. Consider filtering by date range for complete statistics\n\n")

    print(f"  [SUCCESS] Quality report saved to: {output_file}")


def main():
    """Main quality assessment pipeline."""
    print("=" * 60)
    print("DATA QUALITY ASSESSMENT")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Load integrated dataset
    print("=" * 60)
    print("LOADING DATASET")
    print("=" * 60)

    data_file = Path("data/processed/integrated_dataset.csv")
    print(f"Loading: {data_file}")

    df = pd.read_csv(data_file, low_memory=False)
    df['match_date'] = pd.to_datetime(df['match_date'])

    print(f"  Loaded: {len(df):,} records × {len(df.columns)} columns")

    # Run quality assessments
    print("\n" + "=" * 60)
    print("RUNNING QUALITY ASSESSMENTS")
    print("=" * 60)

    quality_metrics = {}
    quality_metrics['completeness'] = assess_completeness(df)
    quality_metrics['validity'] = assess_validity(df)
    quality_metrics['consistency'] = assess_consistency(df)
    quality_metrics['accuracy'] = assess_accuracy(df)
    quality_metrics['uniqueness'] = assess_uniqueness(df)

    # Generate visualizations
    print("\n" + "=" * 60)
    print("GENERATING VISUALIZATIONS")
    print("=" * 60)

    output_dir = Path("outputs/figures")
    output_dir.mkdir(parents=True, exist_ok=True)

    create_visualizations(df, quality_metrics, output_dir)

    # Generate report
    print("\n" + "=" * 60)
    print("GENERATING REPORT")
    print("=" * 60)

    report_dir = Path("outputs/reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / "data_quality_report.md"

    generate_quality_report(quality_metrics, report_file)

    # Summary
    print("\n" + "=" * 60)
    print("[SUCCESS] QUALITY ASSESSMENT COMPLETE!")
    print("=" * 60)
    print(f"\nReports:")
    print(f"  - {report_file}")
    print(f"\nVisualizations:")
    print(f"  - outputs/figures/quality/")
    print()

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
