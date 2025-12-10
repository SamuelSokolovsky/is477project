"""
Analysis & Modeling Script
===========================
Purpose: Feature engineering, EDA, and predictive modeling

Tasks:
1. Feature engineering (derived metrics)
2. Exploratory data analysis
3. Predictive modeling (match outcomes)
4. Model evaluation and comparison

Output:
- Trained models (saved as pickle files)
- Model performance metrics
- Feature importance analysis
- Analysis results in outputs/results/
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import pickle
import warnings
warnings.filterwarnings('ignore')


def load_and_prepare_data(data_path):
    """
    Load integrated dataset and prepare for modeling.

    Strategy:
    - Use only matches with complete shot/corner/foul data (post-2005)
    - Exclude target variables (goals, result) from features
    - Handle categorical variables (league)
    - Create temporal train/test split
    """
    print("\n[1/8] Loading data...")
    df = pd.read_csv(data_path)
    print(f"    Loaded {len(df):,} matches")

    # Filter to complete cases (has shot data)
    print("\n[2/8] Filtering to complete cases...")
    required_cols = ['home_shots', 'away_shots', 'home_shots_on_target',
                     'away_shots_on_target', 'home_corners', 'away_corners',
                     'home_fouls', 'away_fouls']

    df_complete = df.dropna(subset=required_cols).copy()

    # Convert match_date to datetime
    df_complete['match_date'] = pd.to_datetime(df_complete['match_date'], errors='coerce')

    print(f"    Complete cases: {len(df_complete):,} matches ({len(df_complete)/len(df)*100:.1f}%)")
    print(f"    Date range: {df_complete['match_date'].min()} to {df_complete['match_date'].max()}")

    return df_complete


def select_features(df):
    """
    Select features for modeling.

    Features to use (pre-match or during-match observables):
    - Shot statistics (shots, shots on target, accuracy)
    - Corners
    - Fouls
    - Cards
    - League (one-hot encoded)
    - Season

    Features to EXCLUDE (target leakage):
    - home_goals, away_goals (these are the target!)
    - goal_differential (derived from target)
    - result (this is what we're predicting)
    - match_id, date, team names (not predictive)
    """
    print("\n[3/8] Selecting features...")

    # Feature columns
    feature_cols = [
        # Shot statistics
        'home_shots', 'away_shots',
        'home_shots_on_target', 'away_shots_on_target',
        'home_shot_accuracy', 'away_shot_accuracy',

        # Other match statistics
        'home_corners', 'away_corners',
        'home_fouls', 'away_fouls',
        'home_yellow_cards', 'away_yellow_cards',
        'home_red_cards', 'away_red_cards',

        # Derived features (non-target)
        'shot_differential',
        'shots_on_target_differential',

        # Categorical
        'league',
        'season'
    ]

    # Target variable
    target_col = 'result'

    # Check all features exist
    missing_features = [col for col in feature_cols if col not in df.columns]
    if missing_features:
        print(f"    [WARNING] Missing features: {missing_features}")
        feature_cols = [col for col in feature_cols if col in df.columns]

    X = df[feature_cols].copy()
    y = df[target_col].copy()

    # Convert season to numeric (extract starting year from '2000-2001' -> 2000)
    if 'season' in X.columns:
        # Handle NaN values first
        X['season'] = X['season'].fillna('2000-2001')  # Use a default season for missing values
        X['season'] = X['season'].astype(str).str.split('-').str[0].astype(int)

    # One-hot encode league
    X = pd.get_dummies(X, columns=['league'], prefix='league', drop_first=True)

    # Fill NaN values in shot accuracy (happens when shots = 0)
    shot_accuracy_cols = [col for col in X.columns if 'shot_accuracy' in col]
    for col in shot_accuracy_cols:
        X[col] = X[col].fillna(0)

    # Fill any remaining NaN with 0
    X = X.fillna(0)

    print(f"    Features: {X.shape[1]} columns")
    print(f"    Target distribution:")
    print(f"      Home wins (H): {(y == 'H').sum():,} ({(y == 'H').sum()/len(y)*100:.1f}%)")
    print(f"      Draws (D): {(y == 'D').sum():,} ({(y == 'D').sum()/len(y)*100:.1f}%)")
    print(f"      Away wins (A): {(y == 'A').sum():,} ({(y == 'A').sum()/len(y)*100:.1f}%)")

    return X, y, feature_cols


def create_temporal_split(X, y, df, test_size=0.2):
    """
    Create temporal train/test split.

    Use most recent 20% of data for testing to simulate real prediction scenario.
    """
    print(f"\n[4/8] Creating temporal train/test split ({int((1-test_size)*100)}% train / {int(test_size*100)}% test)...")

    # Sort by date
    df_sorted = df.copy()
    df_sorted['match_date'] = pd.to_datetime(df_sorted['match_date'])
    df_sorted = df_sorted.sort_values('match_date')

    # Get indices for split
    split_idx = int(len(df_sorted) * (1 - test_size))

    train_indices = df_sorted.index[:split_idx]
    test_indices = df_sorted.index[split_idx:]

    X_train = X.loc[train_indices]
    X_test = X.loc[test_indices]
    y_train = y.loc[train_indices]
    y_test = y.loc[test_indices]

    print(f"    Training set: {len(X_train):,} matches")
    print(f"    Test set: {len(X_test):,} matches")
    print(f"    Train date range: {df_sorted.loc[train_indices, 'match_date'].min()} to {df_sorted.loc[train_indices, 'match_date'].max()}")
    print(f"    Test date range: {df_sorted.loc[test_indices, 'match_date'].min()} to {df_sorted.loc[test_indices, 'match_date'].max()}")

    return X_train, X_test, y_train, y_test


def scale_features(X_train, X_test):
    """
    Standardize features (important for Logistic Regression).
    """
    print("\n[5/8] Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Convert back to DataFrame to preserve column names
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns, index=X_train.index)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns, index=X_test.index)

    print("    Features scaled to mean=0, std=1")

    return X_train_scaled, X_test_scaled, scaler


def train_models(X_train, X_test, y_train, y_test):
    """
    Train three classification models:
    1. Logistic Regression (baseline)
    2. Random Forest (ensemble)
    3. Gradient Boosting (advanced ensemble)
    """
    print("\n[6/8] Training models...")

    models = {}
    predictions = {}
    probabilities = {}

    # Model 1: Logistic Regression
    print("    Training Logistic Regression...")
    lr = LogisticRegression(max_iter=1000, random_state=42, multi_class='multinomial')
    lr.fit(X_train, y_train)
    models['Logistic Regression'] = lr
    predictions['Logistic Regression'] = lr.predict(X_test)
    probabilities['Logistic Regression'] = lr.predict_proba(X_test)

    # Model 2: Random Forest
    print("    Training Random Forest...")
    rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    models['Random Forest'] = rf
    predictions['Random Forest'] = rf.predict(X_test)
    probabilities['Random Forest'] = rf.predict_proba(X_test)

    # Model 3: Gradient Boosting
    print("    Training Gradient Boosting...")
    gb = GradientBoostingClassifier(n_estimators=100, max_depth=5, random_state=42)
    gb.fit(X_train, y_train)
    models['Gradient Boosting'] = gb
    predictions['Gradient Boosting'] = gb.predict(X_test)
    probabilities['Gradient Boosting'] = gb.predict_proba(X_test)

    print("    [SUCCESS] All models trained!")

    return models, predictions, probabilities


def evaluate_models(y_test, predictions, probabilities):
    """
    Evaluate all models and compare performance.
    """
    print("\n[7/8] Evaluating models...")

    results = {}

    for model_name in predictions.keys():
        y_pred = predictions[model_name]
        y_proba = probabilities[model_name]

        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

        # Multi-class ROC AUC (one-vs-rest)
        try:
            # Encode labels for ROC AUC
            le = LabelEncoder()
            y_test_encoded = le.fit_transform(y_test)
            roc_auc = roc_auc_score(y_test_encoded, y_proba, multi_class='ovr', average='weighted')
        except:
            roc_auc = None

        results[model_name] = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'roc_auc': roc_auc,
            'confusion_matrix': confusion_matrix(y_test, y_pred)
        }

        print(f"\n    {model_name}:")
        print(f"      Accuracy:  {accuracy:.4f}")
        print(f"      Precision: {precision:.4f}")
        print(f"      Recall:    {recall:.4f}")
        print(f"      F1 Score:  {f1:.4f}")
        if roc_auc:
            print(f"      ROC AUC:   {roc_auc:.4f}")

    return results


def generate_visualizations(models, X_train, y_test, predictions, results, output_dir):
    """
    Generate visualizations:
    1. Feature importance (Random Forest & Gradient Boosting)
    2. Confusion matrices
    3. Model comparison chart
    """
    print("\n[8/8] Generating visualizations...")

    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Feature Importance
    print("    Creating feature importance plots...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for idx, model_name in enumerate(['Random Forest', 'Gradient Boosting']):
        model = models[model_name]
        importance = model.feature_importances_

        # Get top 15 features
        feature_importance_df = pd.DataFrame({
            'feature': X_train.columns,
            'importance': importance
        }).sort_values('importance', ascending=False).head(15)

        axes[idx].barh(range(len(feature_importance_df)), feature_importance_df['importance'])
        axes[idx].set_yticks(range(len(feature_importance_df)))
        axes[idx].set_yticklabels(feature_importance_df['feature'])
        axes[idx].set_xlabel('Importance')
        axes[idx].set_title(f'{model_name}\nTop 15 Features')
        axes[idx].invert_yaxis()

    plt.tight_layout()
    plt.savefig(output_dir / 'feature_importance.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Confusion Matrices
    print("    Creating confusion matrices...")
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    for idx, model_name in enumerate(predictions.keys()):
        cm = results[model_name]['confusion_matrix']

        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                    xticklabels=['Away', 'Draw', 'Home'],
                    yticklabels=['Away', 'Draw', 'Home'])
        axes[idx].set_title(f'{model_name}\nConfusion Matrix')
        axes[idx].set_ylabel('True Label')
        axes[idx].set_xlabel('Predicted Label')

    plt.tight_layout()
    plt.savefig(output_dir / 'confusion_matrices.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 3. Model Comparison
    print("    Creating model comparison chart...")
    metrics = ['accuracy', 'precision', 'recall', 'f1']
    model_names = list(predictions.keys())

    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.arange(len(metrics))
    width = 0.25

    for idx, model_name in enumerate(model_names):
        values = [results[model_name][metric] for metric in metrics]
        ax.bar(x + idx * width, values, width, label=model_name)

    ax.set_xlabel('Metrics')
    ax.set_ylabel('Score')
    ax.set_title('Model Performance Comparison')
    ax.set_xticks(x + width)
    ax.set_xticklabels([m.capitalize() for m in metrics])
    ax.legend()
    ax.set_ylim([0, 1])
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / 'model_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("    [SUCCESS] All visualizations saved!")


def generate_report(results, predictions, y_test, X_train, output_path):
    """
    Generate comprehensive analysis report.

    NOTE: This report generation code was created using AI assistance.
    The reports generated in outputs/reports/ are managerial reports for
    troubleshooting purposes only. AI is particularly effective at formatting
    and presenting output data in readable markdown format.
    """
    report = []
    report.append("# Analysis & Modeling Report\n")
    report.append(f"**Generated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append("---\n\n")

    report.append("## Executive Summary\n\n")
    report.append("This report presents the results of predictive modeling for soccer match outcomes.\n")
    report.append(f"Three classification models were trained on {len(X_train):,} matches to predict ")
    report.append("match results (Home Win, Draw, Away Win).\n\n")

    # Find best model
    best_model = max(results.items(), key=lambda x: x[1]['accuracy'])
    report.append(f"**Best Model:** {best_model[0]} (Accuracy: {best_model[1]['accuracy']:.4f})\n\n")
    report.append("---\n\n")

    report.append("## Model Performance\n\n")

    # Create performance table
    report.append("| Model | Accuracy | Precision | Recall | F1 Score | ROC AUC |\n")
    report.append("|-------|----------|-----------|--------|----------|----------|\n")

    for model_name in results.keys():
        r = results[model_name]
        roc_auc_str = f"{r['roc_auc']:.4f}" if r['roc_auc'] else "N/A"
        report.append(f"| {model_name} | {r['accuracy']:.4f} | {r['precision']:.4f} | ")
        report.append(f"{r['recall']:.4f} | {r['f1']:.4f} | {roc_auc_str} |\n")

    report.append("\n---\n\n")

    # Detailed results per model
    report.append("## Detailed Results\n\n")

    for model_name in results.keys():
        report.append(f"### {model_name}\n\n")

        # Classification report
        y_pred = predictions[model_name]
        class_report = classification_report(y_test, y_pred, output_dict=True)

        report.append("**Per-class Performance:**\n\n")
        report.append("| Class | Precision | Recall | F1-Score | Support |\n")
        report.append("|-------|-----------|--------|----------|----------|\n")

        for label in ['A', 'D', 'H']:
            if label in class_report:
                report.append(f"| {label} (")
                if label == 'H':
                    report.append("Home Win")
                elif label == 'D':
                    report.append("Draw")
                else:
                    report.append("Away Win")
                report.append(f") | {class_report[label]['precision']:.4f} | ")
                report.append(f"{class_report[label]['recall']:.4f} | ")
                report.append(f"{class_report[label]['f1-score']:.4f} | ")
                report.append(f"{int(class_report[label]['support'])} |\n")

        report.append("\n")

        # Confusion matrix
        cm = results[model_name]['confusion_matrix']
        report.append("**Confusion Matrix:**\n\n")
        report.append("```\n")
        report.append("              Predicted\n")
        report.append("              A      D      H\n")
        report.append("Actual  A  " + "  ".join([f"{cm[0][i]:4d}" for i in range(3)]) + "\n")
        report.append("        D  " + "  ".join([f"{cm[1][i]:4d}" for i in range(3)]) + "\n")
        report.append("        H  " + "  ".join([f"{cm[2][i]:4d}" for i in range(3)]) + "\n")
        report.append("```\n\n")

    report.append("---\n\n")

    report.append("## Insights\n\n")
    report.append("1. **Model Comparison:** ")
    report.append(f"{best_model[0]} achieved the best performance with {best_model[1]['accuracy']:.1%} accuracy.\n")
    report.append("2. **Class Imbalance:** Home wins are more common (~45-47%), making them easier to predict.\n")
    report.append("3. **Feature Importance:** Shot statistics (shots, shots on target, accuracy) are the most important predictors.\n")
    report.append("4. **Practical Application:** Models can be used for match outcome prediction with ~50-55% accuracy, ")
    report.append("significantly better than random guessing (33%).\n\n")

    report.append("---\n\n")

    report.append("## Visualizations\n\n")
    report.append("- **Feature Importance:** `outputs/figures/analysis/feature_importance.png`\n")
    report.append("- **Confusion Matrices:** `outputs/figures/analysis/confusion_matrices.png`\n")
    report.append("- **Model Comparison:** `outputs/figures/analysis/model_comparison.png`\n\n")

    # Write report
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(report)

    print(f"\n[SUCCESS] Report saved to: {output_path}")


def save_models(models, scaler, output_dir):
    """
    Save trained models and scaler for reproducibility.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    for model_name, model in models.items():
        filename = model_name.lower().replace(' ', '_') + '.pkl'
        with open(output_dir / filename, 'wb') as f:
            pickle.dump(model, f)

    # Save scaler
    with open(output_dir / 'scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

    print(f"\n[SUCCESS] Models saved to: {output_dir}")


def analyze_and_model():
    """Main analysis pipeline."""
    print("=" * 60)
    print("ANALYSIS & MODELING SCRIPT")
    print("=" * 60)
    print("\nPredictive Modeling: Match Outcome Classification")
    print("Target: Result (Home Win / Draw / Away Win)")
    print("Models: Logistic Regression, Random Forest, Gradient Boosting")

    # Paths
    data_path = Path('data/processed/integrated_dataset.csv')
    output_dir = Path('outputs/figures/analysis')
    report_dir = Path('outputs/reports')
    models_dir = Path('outputs/models')

    # Create output directories
    output_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)
    models_dir.mkdir(parents=True, exist_ok=True)

    # Load and prepare data
    df = load_and_prepare_data(data_path)

    # Select features
    X, y, feature_cols = select_features(df)

    # Create temporal split
    X_train, X_test, y_train, y_test = create_temporal_split(X, y, df)

    # Scale features
    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)

    # Train models
    models, predictions, probabilities = train_models(X_train_scaled, X_test_scaled, y_train, y_test)

    # Evaluate models
    results = evaluate_models(y_test, predictions, probabilities)

    # Generate visualizations
    generate_visualizations(models, X_train, y_test, predictions, results, output_dir)

    # Generate report
    report_path = report_dir / 'analysis_report.md'
    generate_report(results, predictions, y_test, X_train_scaled, report_path)

    # Save models
    save_models(models, scaler, models_dir)

    print("\n" + "=" * 60)
    print("[SUCCESS] ANALYSIS & MODELING COMPLETE!")
    print("=" * 60)
    print("\nOutputs:")
    print(f"  Reports:")
    print(f"    - {report_path}")
    print(f"\n  Visualizations:")
    print(f"    - {output_dir}/feature_importance.png")
    print(f"    - {output_dir}/confusion_matrices.png")
    print(f"    - {output_dir}/model_comparison.png")
    print(f"\n  Models:")
    print(f"    - {models_dir}/ (3 models + scaler)")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    analyze_and_model()
