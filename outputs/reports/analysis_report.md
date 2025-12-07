# Analysis & Modeling Report
**Generated:** 2025-12-06 18:11:18
---

## Executive Summary

This report presents the results of predictive modeling for soccer match outcomes.
Three classification models were trained on 30,588 matches to predict match results (Home Win, Draw, Away Win).

**Best Model:** Logistic Regression (Accuracy: 0.5889)

---

## Model Performance

| Model | Accuracy | Precision | Recall | F1 Score | ROC AUC |
|-------|----------|-----------|--------|----------|----------|
| Logistic Regression | 0.5889 | 0.5455 | 0.5889 | 0.5318 | 0.7555 |
| Random Forest | 0.5889 | 0.5543 | 0.5889 | 0.5467 | 0.7569 |
| Gradient Boosting | 0.5822 | 0.5604 | 0.5822 | 0.5666 | 0.7576 |

---

## Detailed Results

### Logistic Regression

**Per-class Performance:**

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|----------|
| A (Away Win) | 0.5726 | 0.6803 | 0.6218 | 2355 |
| D (Draw) | 0.3911 | 0.0727 | 0.1226 | 1926 |
| H (Home Win) | 0.6149 | 0.8203 | 0.7029 | 3367 |

**Confusion Matrix:**

```
              Predicted
              A      D      H
Actual  A  1602    98   655
        D   711   140  1075
        H   485   120  2762
```

### Random Forest

**Per-class Performance:**

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|----------|
| A (Away Win) | 0.5850 | 0.6488 | 0.6153 | 2355 |
| D (Draw) | 0.4096 | 0.1282 | 0.1953 | 1926 |
| H (Home Win) | 0.6156 | 0.8105 | 0.6997 | 3367 |

**Confusion Matrix:**

```
              Predicted
              A      D      H
Actual  A  1528   158   669
        D   644   247  1035
        H   440   198  2729
```

### Gradient Boosting

**Per-class Performance:**

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|----------|
| A (Away Win) | 0.5749 | 0.6565 | 0.6130 | 2355 |
| D (Draw) | 0.3646 | 0.2399 | 0.2894 | 1926 |
| H (Home Win) | 0.6622 | 0.7262 | 0.6927 | 3367 |

**Confusion Matrix:**

```
              Predicted
              A      D      H
Actual  A  1546   352   457
        D   674   462   790
        H   469   453  2445
```

---

## Insights

1. **Model Comparison:** Logistic Regression achieved the best performance with 58.9% accuracy.
2. **Class Imbalance:** Home wins are more common (~45-47%), making them easier to predict.
3. **Feature Importance:** Shot statistics (shots, shots on target, accuracy) are the most important predictors.
4. **Practical Application:** Models can be used for match outcome prediction with ~50-55% accuracy, significantly better than random guessing (33%).

---

## Visualizations

- **Feature Importance:** `outputs/figures/analysis/feature_importance.png`
- **Confusion Matrices:** `outputs/figures/analysis/confusion_matrices.png`
- **Model Comparison:** `outputs/figures/analysis/model_comparison.png`

