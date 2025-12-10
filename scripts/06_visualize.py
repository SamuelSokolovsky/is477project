"""
Visualization Script
====================
Purpose: Generate comprehensive analytics visualizations

Visualizations:
1. Temporal trends (goals, results over time)
2. League comparisons (scoring patterns, card discipline)
3. Team performance analytics (top scorers, best defenses)
4. Home advantage analysis
5. Shot efficiency analysis
6. Seasonal patterns
7. Correlation heatmap

Output:
- All figures saved to outputs/figures/comprehensive/
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style for publication-quality plots
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10


def load_data():
    """Load integrated dataset for visualization."""
    print("\n[1/9] Loading data...")
    df = pd.read_csv('data/processed/integrated_dataset.csv')
    df['match_date'] = pd.to_datetime(df['match_date'], errors='coerce')
    df['year'] = df['match_date'].dt.year
    print(f"    Loaded {len(df):,} matches")
    return df


def plot_temporal_trends(df, output_dir):
    """
    Create temporal trend visualizations:
    - Goals per season
    - Results distribution over time
    - Home advantage evolution
    """
    print("\n[2/9] Creating temporal trends...")

    # Prepare data
    df_temporal = df.groupby('year').agg({
        'home_goals': 'mean',
        'away_goals': 'mean',
        'result': lambda x: (x == 'H').sum() / len(x) * 100
    }).reset_index()
    df_temporal['total_goals'] = df_temporal['home_goals'] + df_temporal['away_goals']

    # Create figure with 3 subplots
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # Plot 1: Goals per match over time
    axes[0].plot(df_temporal['year'], df_temporal['total_goals'],
                 marker='o', linewidth=2, markersize=6, color='steelblue')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Average Goals per Match')
    axes[0].set_title('Scoring Trends Over Time')
    axes[0].grid(True, alpha=0.3)

    # Plot 2: Home vs Away goals
    axes[1].plot(df_temporal['year'], df_temporal['home_goals'],
                 marker='o', linewidth=2, markersize=5, label='Home', color='green')
    axes[1].plot(df_temporal['year'], df_temporal['away_goals'],
                 marker='s', linewidth=2, markersize=5, label='Away', color='red')
    axes[1].set_xlabel('Year')
    axes[1].set_ylabel('Average Goals')
    axes[1].set_title('Home vs Away Goals Over Time')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    # Plot 3: Home win percentage over time
    axes[2].plot(df_temporal['year'], df_temporal['result'],
                 marker='o', linewidth=2, markersize=6, color='darkgreen')
    axes[2].set_xlabel('Year')
    axes[2].set_ylabel('Home Win %')
    axes[2].set_title('Home Advantage Over Time')
    axes[2].axhline(y=50, color='gray', linestyle='--', alpha=0.5, label='50% baseline')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / 'temporal_trends.png', bbox_inches='tight')
    plt.close()
    print("    Saved: temporal_trends.png")


def plot_league_comparison(df, output_dir):
    """
    Compare leagues across key metrics:
    - Average goals per match
    - Card discipline
    - Shot accuracy
    """
    print("\n[3/9] Creating league comparisons...")

    # Prepare league statistics
    league_stats = df.groupby('league').agg({
        'home_goals': 'mean',
        'away_goals': 'mean',
        'home_yellow_cards': 'mean',
        'away_yellow_cards': 'mean',
        'home_red_cards': 'mean',
        'away_red_cards': 'mean',
        'home_shot_accuracy': 'mean',
        'away_shot_accuracy': 'mean',
        'match_id': 'count'
    }).reset_index()

    league_stats['total_goals'] = league_stats['home_goals'] + league_stats['away_goals']
    league_stats['total_yellows'] = league_stats['home_yellow_cards'] + league_stats['away_yellow_cards']
    league_stats['total_reds'] = league_stats['home_red_cards'] + league_stats['away_red_cards']
    league_stats['avg_shot_accuracy'] = (league_stats['home_shot_accuracy'] + league_stats['away_shot_accuracy']) / 2

    # Sort by total goals for better visualization
    league_stats = league_stats.sort_values('total_goals', ascending=False)

    # Create figure with 2x2 subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Plot 1: Goals per match by league
    axes[0, 0].barh(league_stats['league'], league_stats['total_goals'], color='steelblue')
    axes[0, 0].set_xlabel('Average Goals per Match')
    axes[0, 0].set_title('Scoring by League')
    axes[0, 0].grid(axis='x', alpha=0.3)

    # Plot 2: Yellow cards by league
    axes[0, 1].barh(league_stats['league'], league_stats['total_yellows'], color='gold')
    axes[0, 1].set_xlabel('Average Yellow Cards per Match')
    axes[0, 1].set_title('Card Discipline by League')
    axes[0, 1].grid(axis='x', alpha=0.3)

    # Plot 3: Shot accuracy by league
    axes[1, 0].barh(league_stats['league'], league_stats['avg_shot_accuracy'] * 100, color='green')
    axes[1, 0].set_xlabel('Shot Accuracy (%)')
    axes[1, 0].set_title('Shot Accuracy by League')
    axes[1, 0].grid(axis='x', alpha=0.3)

    # Plot 4: Number of matches by league
    axes[1, 1].barh(league_stats['league'], league_stats['match_id'], color='coral')
    axes[1, 1].set_xlabel('Number of Matches')
    axes[1, 1].set_title('Dataset Coverage by League')
    axes[1, 1].grid(axis='x', alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / 'league_comparison.png', bbox_inches='tight')
    plt.close()
    print("    Saved: league_comparison.png")


def plot_team_performance(df, output_dir):
    """
    Analyze team performance:
    - Top scoring teams
    - Best defensive teams
    - Most disciplined teams
    """
    print("\n[4/9] Creating team performance analytics...")

    # Calculate team statistics (home + away combined)
    home_stats = df.groupby('home_team').agg({
        'home_goals': 'sum',
        'away_goals': 'sum',
        'match_id': 'count'
    }).rename(columns={'home_goals': 'goals_scored', 'away_goals': 'goals_conceded', 'match_id': 'matches'})

    away_stats = df.groupby('away_team').agg({
        'away_goals': 'sum',
        'home_goals': 'sum',
        'match_id': 'count'
    }).rename(columns={'away_goals': 'goals_scored', 'home_goals': 'goals_conceded', 'match_id': 'matches'})

    # Combine home and away stats
    team_stats = pd.DataFrame({
        'goals_scored': home_stats['goals_scored'] + away_stats['goals_scored'],
        'goals_conceded': home_stats['goals_conceded'] + away_stats['goals_conceded'],
        'matches': home_stats['matches'] + away_stats['matches']
    })

    team_stats['goals_per_match'] = team_stats['goals_scored'] / team_stats['matches']
    team_stats['goals_conceded_per_match'] = team_stats['goals_conceded'] / team_stats['matches']
    team_stats['goal_differential'] = team_stats['goals_scored'] - team_stats['goals_conceded']

    # Create figure with 3 subplots
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Plot 1: Top 10 scoring teams
    top_scorers = team_stats.nlargest(10, 'goals_scored')
    axes[0].barh(range(len(top_scorers)), top_scorers['goals_scored'], color='darkgreen')
    axes[0].set_yticks(range(len(top_scorers)))
    axes[0].set_yticklabels(top_scorers.index)
    axes[0].set_xlabel('Total Goals Scored')
    axes[0].set_title('Top 10 Scoring Teams (All-Time)')
    axes[0].invert_yaxis()
    axes[0].grid(axis='x', alpha=0.3)

    # Plot 2: Best defensive teams (fewest goals conceded)
    best_defense = team_stats.nsmallest(10, 'goals_conceded_per_match')
    axes[1].barh(range(len(best_defense)), best_defense['goals_conceded_per_match'], color='steelblue')
    axes[1].set_yticks(range(len(best_defense)))
    axes[1].set_yticklabels(best_defense.index)
    axes[1].set_xlabel('Goals Conceded per Match')
    axes[1].set_title('Top 10 Defensive Teams (Lowest Rate)')
    axes[1].invert_yaxis()
    axes[1].grid(axis='x', alpha=0.3)

    # Plot 3: Best goal differential
    best_differential = team_stats.nlargest(10, 'goal_differential')
    colors = ['green' if x > 0 else 'red' for x in best_differential['goal_differential']]
    axes[2].barh(range(len(best_differential)), best_differential['goal_differential'], color=colors)
    axes[2].set_yticks(range(len(best_differential)))
    axes[2].set_yticklabels(best_differential.index)
    axes[2].set_xlabel('Goal Differential (+/-)')
    axes[2].set_title('Top 10 Teams by Goal Differential')
    axes[2].invert_yaxis()
    axes[2].axvline(x=0, color='black', linewidth=0.5)
    axes[2].grid(axis='x', alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / 'team_performance.png', bbox_inches='tight')
    plt.close()
    print("    Saved: team_performance.png")


def plot_home_advantage(df, output_dir):
    """
    Analyze home advantage:
    - Home vs Away performance
    - Home advantage by league
    """
    print("\n[5/9] Creating home advantage analysis...")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Plot 1: Overall result distribution
    result_counts = df['result'].value_counts()
    result_labels = {'H': 'Home Win', 'D': 'Draw', 'A': 'Away Win'}
    colors = ['green', 'gray', 'red']

    axes[0].pie([result_counts['H'], result_counts['D'], result_counts['A']],
                labels=[result_labels['H'], result_labels['D'], result_labels['A']],
                colors=colors, autopct='%1.1f%%', startangle=90)
    axes[0].set_title('Overall Match Results Distribution')

    # Plot 2: Home advantage by league
    league_results = df.groupby('league').agg({
        'result': lambda x: (x == 'H').sum() / len(x) * 100
    }).reset_index()
    league_results = league_results.sort_values('result', ascending=False)

    axes[1].barh(league_results['league'], league_results['result'], color='darkgreen')
    axes[1].set_xlabel('Home Win %')
    axes[1].set_title('Home Advantage by League')
    axes[1].axvline(x=50, color='gray', linestyle='--', alpha=0.5, label='50% baseline')
    axes[1].legend()
    axes[1].grid(axis='x', alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / 'home_advantage.png', bbox_inches='tight')
    plt.close()
    print("    Saved: home_advantage.png")


def plot_shot_efficiency(df, output_dir):
    """
    Analyze shot efficiency:
    - Shot accuracy vs goals
    - Shots on target distribution
    """
    print("\n[6/9] Creating shot efficiency analysis...")

    # Filter to matches with complete shot data
    df_shots = df.dropna(subset=['home_shots', 'home_shots_on_target',
                                  'away_shots', 'away_shots_on_target'])

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Plot 1: Shot accuracy distribution
    shot_accuracy = pd.concat([
        df_shots['home_shot_accuracy'],
        df_shots['away_shot_accuracy']
    ]).dropna()

    axes[0].hist(shot_accuracy, bins=30, color='steelblue', edgecolor='black', alpha=0.7)
    axes[0].set_xlabel('Shot Accuracy (Shots on Target / Total Shots)')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title('Distribution of Shot Accuracy')
    axes[0].axvline(x=shot_accuracy.mean(), color='red', linestyle='--',
                    linewidth=2, label=f'Mean: {shot_accuracy.mean():.2f}')
    axes[0].legend()
    axes[0].grid(axis='y', alpha=0.3)

    # Plot 2: Shots vs Goals (scatter plot)
    total_shots = df_shots['home_shots'] + df_shots['away_shots']
    total_goals = df_shots['home_goals'] + df_shots['away_goals']

    axes[1].hexbin(total_shots, total_goals, gridsize=20, cmap='YlOrRd', mincnt=1)
    axes[1].set_xlabel('Total Shots')
    axes[1].set_ylabel('Total Goals')
    axes[1].set_title('Relationship: Shots vs Goals')
    axes[1].grid(True, alpha=0.3)

    # Add colorbar
    cb = plt.colorbar(axes[1].collections[0], ax=axes[1])
    cb.set_label('Match Frequency')

    plt.tight_layout()
    plt.savefig(output_dir / 'shot_efficiency.png', bbox_inches='tight')
    plt.close()
    print("    Saved: shot_efficiency.png")


def plot_seasonal_patterns(df, output_dir):
    """
    Analyze seasonal patterns:
    - Goals by month
    - Results by month
    """
    print("\n[7/9] Creating seasonal pattern analysis...")

    # Extract month from date
    df['month'] = df['match_date'].dt.month

    # Calculate monthly statistics
    monthly_stats = df.groupby('month').agg({
        'home_goals': 'mean',
        'away_goals': 'mean',
        'result': lambda x: (x == 'H').sum() / len(x) * 100
    }).reset_index()
    monthly_stats['total_goals'] = monthly_stats['home_goals'] + monthly_stats['away_goals']

    # Month names
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Plot 1: Goals by month
    axes[0].plot(monthly_stats['month'], monthly_stats['total_goals'],
                 marker='o', linewidth=2, markersize=8, color='steelblue')
    axes[0].set_xlabel('Month')
    axes[0].set_ylabel('Average Goals per Match')
    axes[0].set_title('Seasonal Scoring Patterns')
    axes[0].set_xticks(range(1, 13))
    axes[0].set_xticklabels(month_names)
    axes[0].grid(True, alpha=0.3)
    axes[0].tick_params(axis='x', rotation=45)

    # Plot 2: Home win % by month
    axes[1].plot(monthly_stats['month'], monthly_stats['result'],
                 marker='o', linewidth=2, markersize=8, color='darkgreen')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Home Win %')
    axes[1].set_title('Home Advantage by Month')
    axes[1].set_xticks(range(1, 13))
    axes[1].set_xticklabels(month_names)
    axes[1].axhline(y=50, color='gray', linestyle='--', alpha=0.5)
    axes[1].grid(True, alpha=0.3)
    axes[1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(output_dir / 'seasonal_patterns.png', bbox_inches='tight')
    plt.close()
    print("    Saved: seasonal_patterns.png")


def plot_correlation_heatmap(df, output_dir):
    """
    Create correlation heatmap of key features.
    """
    print("\n[8/9] Creating correlation heatmap...")

    # Select numeric columns for correlation
    corr_cols = ['home_goals', 'away_goals', 'home_shots', 'away_shots',
                 'home_shots_on_target', 'away_shots_on_target',
                 'home_fouls', 'away_fouls', 'home_corners', 'away_corners',
                 'home_yellow_cards', 'away_yellow_cards']

    # Filter to available columns and complete data
    corr_cols = [col for col in corr_cols if col in df.columns]
    df_corr = df[corr_cols].dropna()

    # Calculate correlation matrix
    corr_matrix = df_corr.corr()

    # Create heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm',
                center=0, square=True, linewidths=0.5,
                cbar_kws={"shrink": 0.8})
    plt.title('Feature Correlation Heatmap', fontsize=14, pad=20)
    plt.tight_layout()
    plt.savefig(output_dir / 'correlation_heatmap.png', bbox_inches='tight')
    plt.close()
    print("    Saved: correlation_heatmap.png")


def generate_summary_report(df, output_path):
    """
    Generate comprehensive visualization summary report.

    NOTE: This report generation code was created using AI assistance.
    The reports generated in outputs/reports/ are managerial reports for
    troubleshooting purposes only. AI is particularly effective at formatting
    and presenting output data in readable markdown format.
    """
    print("\n[9/9] Generating visualization summary report...")

    report = []
    report.append("# Visualization Summary Report\n")
    report.append(f"**Generated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append("---\n\n")

    report.append("## Overview\n\n")
    report.append("This report summarizes all comprehensive visualizations generated for the soccer analytics project.\n")
    report.append(f"Dataset: {len(df):,} matches across {df['league'].nunique()} leagues from ")
    report.append(f"{df['match_date'].min().strftime('%Y')} to {df['match_date'].max().strftime('%Y')}\n\n")

    report.append("---\n\n")

    report.append("## Generated Visualizations\n\n")

    report.append("### 1. Temporal Trends\n")
    report.append("**File:** `temporal_trends.png`\n\n")
    report.append("Analyzes how soccer has evolved over time:\n")
    report.append("- Overall scoring trends (goals per match over years)\n")
    report.append("- Home vs away goal trends\n")
    report.append("- Home advantage evolution\n\n")

    report.append("### 2. League Comparison\n")
    report.append("**File:** `league_comparison.png`\n\n")
    report.append("Compares the 5 European leagues:\n")
    report.append("- Average goals per match\n")
    report.append("- Card discipline (yellow/red cards)\n")
    report.append("- Shot accuracy\n")
    report.append("- Dataset coverage\n\n")

    report.append("### 3. Team Performance\n")
    report.append("**File:** `team_performance.png`\n\n")
    report.append("All-time team statistics:\n")
    report.append("- Top 10 scoring teams\n")
    report.append("- Top 10 defensive teams\n")
    report.append("- Best goal differentials\n\n")

    report.append("### 4. Home Advantage Analysis\n")
    report.append("**File:** `home_advantage.png`\n\n")
    report.append("Home field advantage patterns:\n")
    report.append("- Overall result distribution (pie chart)\n")
    report.append("- Home win percentage by league\n\n")

    report.append("### 5. Shot Efficiency\n")
    report.append("**File:** `shot_efficiency.png`\n\n")
    report.append("Shot quality and conversion analysis:\n")
    report.append("- Shot accuracy distribution\n")
    report.append("- Shots vs goals relationship (hexbin plot)\n\n")

    report.append("### 6. Seasonal Patterns\n")
    report.append("**File:** `seasonal_patterns.png`\n\n")
    report.append("Month-by-month analysis:\n")
    report.append("- Goals by month of the year\n")
    report.append("- Home advantage by month\n\n")

    report.append("### 7. Correlation Heatmap\n")
    report.append("**File:** `correlation_heatmap.png`\n\n")
    report.append("Feature correlation analysis for:\n")
    report.append("- Goals, shots, fouls, corners, cards\n")
    report.append("- Identifies strongest relationships between variables\n\n")

    report.append("---\n\n")

    report.append("## Key Insights\n\n")

    # Calculate some key statistics
    home_win_pct = (df['result'] == 'H').sum() / len(df) * 100
    avg_goals = (df['home_goals'] + df['away_goals']).mean()

    report.append(f"1. **Home Advantage:** {home_win_pct:.1f}% of matches are won by the home team\n")
    report.append(f"2. **Average Scoring:** {avg_goals:.2f} goals per match across all leagues and years\n")
    report.append(f"3. **Dataset Coverage:** {len(df):,} matches from {df['year'].nunique()} different years\n")
    report.append(f"4. **League Diversity:** Data from {df['league'].nunique()} major European leagues\n")
    report.append(f"5. **Team Coverage:** {df['home_team'].nunique()} unique teams tracked\n\n")

    report.append("---\n\n")

    report.append("## File Locations\n\n")
    report.append("All visualizations are saved in: `outputs/figures/comprehensive/`\n\n")

    # Write report
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(report)

    print(f"    Report saved: {output_path}")


def generate_visualizations():
    """Main visualization pipeline."""
    print("=" * 60)
    print("COMPREHENSIVE VISUALIZATION SCRIPT")
    print("=" * 60)
    print("\nGenerating publication-quality analytics visualizations...")

    # Create output directory
    output_dir = Path('outputs/figures/comprehensive')
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load data
    df = load_data()

    # Generate all visualizations
    plot_temporal_trends(df, output_dir)
    plot_league_comparison(df, output_dir)
    plot_team_performance(df, output_dir)
    plot_home_advantage(df, output_dir)
    plot_shot_efficiency(df, output_dir)
    plot_seasonal_patterns(df, output_dir)
    plot_correlation_heatmap(df, output_dir)

    # Generate summary report
    report_path = Path('outputs/reports/visualization_report.md')
    generate_summary_report(df, report_path)

    print("\n" + "=" * 60)
    print("[SUCCESS] VISUALIZATION COMPLETE!")
    print("=" * 60)
    print("\nOutputs:")
    print(f"  Visualizations (7 figures):")
    print(f"    - {output_dir}/temporal_trends.png")
    print(f"    - {output_dir}/league_comparison.png")
    print(f"    - {output_dir}/team_performance.png")
    print(f"    - {output_dir}/home_advantage.png")
    print(f"    - {output_dir}/shot_efficiency.png")
    print(f"    - {output_dir}/seasonal_patterns.png")
    print(f"    - {output_dir}/correlation_heatmap.png")
    print(f"\n  Report:")
    print(f"    - {report_path}")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    generate_visualizations()
