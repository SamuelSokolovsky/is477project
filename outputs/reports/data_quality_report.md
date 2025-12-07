# Data Quality Assessment Report

**Generated:** 2025-12-06 17:59:08

---

## Executive Summary

**Overall Status:** [GOOD] Minor issues detected

### Quality Dimensions

| Dimension | Status | Issues |
|-----------|--------|--------|
| Completeness | [FAIL] | Core fields complete |
| Validity | [WARN] | 2 issues |
| Consistency | [WARN] | 1 issues |
| Accuracy | [PASS] | 0 anomalies |
| Uniqueness | [PASS] | 0 issues |

---

## 1. Completeness Assessment

- **Rows with 100% completeness:** 10,825
- **Average row completeness:** 88.09%
- **Core fields complete:** False

### Top Missing Fields

| Field | Missing % | Complete % |
|-------|-----------|------------|
| `referee` | 81.0% | 19.0% |
| `away_shot_accuracy` | 32.6% | 67.3% |
| `away_shots_on_target` | 32.6% | 67.4% |
| `home_shots_on_target` | 32.6% | 67.4% |
| `home_shot_accuracy` | 32.6% | 67.4% |
| `home_fouls` | 32.3% | 67.7% |
| `away_fouls` | 32.3% | 67.7% |
| `away_corners` | 31.7% | 68.3% |
| `home_corners` | 31.7% | 68.3% |
| `away_shots` | 31.0% | 69.0% |

---

## 2. Validity Assessment

Issues found:

- Home shots < shots on target: 2 cases
- Away shots < shots on target: 3 cases

---

## 3. Consistency Assessment

Issues found:

- Shot accuracy out of bounds: 1 cases

---

## 4. Accuracy Assessment

- **Mean goals per match:** 2.67
- **Home win rate:** 46.2%


---

## 5. Uniqueness Assessment

- **Unique matches:** 57,865
- **Total records:** 57,865
- **Uniqueness rate:** 100.00%


---

## Recommendations

1. Missing shot/foul data is expected for older seasons (pre-2005)
2. Core match data (goals, results, teams) is 100% complete
3. Dataset is suitable for analysis with proper handling of missing data
4. Consider filtering by date range for complete statistics

